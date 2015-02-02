import datetime
import json
import requests
import random
import string

from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from stormpath.client import Client as StormpathClient
import elasticsearch

from alliterativeanimals import get_name
import settings

# Flask
app = Flask(__name__)

# Elastic Search
es = elasticsearch.Elasticsearch([settings.ELASTICSEARCH_URL])
INDEX = "main"
DOC_TYPE = "idea"

"""
es.search(index="main", body={"query":{"fuzzy":{"_all":"run"}}});
"""

# Stormpath
stormpath_client = StormpathClient(
                       api_key_id=settings.STORMPATH_API_KEY_ID,
                       api_key_secret=settings.STORMPATH_API_KEY_SECRET)
stormpath_application = stormpath_client.applications.search(settings.STORMPATH_APPLICATION_NAME)[0]

# STATIC FILES

@app.route("/")
def main():
    template_name="html/index.html"
    return app.send_static_file(template_name)

# API

@app.route("/api/ideas/new/", methods=['POST'])
def api_ideas_create():
    data = json.loads(request.data)
    insert_idea(
        data['user'],
        data['headline'],
        data['detail']
    )
    # Other idea fields? modified, views, upvotes, comments?
    return 'OK: Idea "{}" entered.'.format(data['headline'])

@app.route("/api/ideas/")
def api_ideas():
    NUM_RESULTS = 100
    if request.args:
        query = " OR ".join( ["{}={}".format(key, request.args[key]) for key in request.args.keys()])
        results = es.search(index=INDEX, doc_type=DOC_TYPE, size=NUM_RESULTS, q=query)
    else:
        results = es.search(index=INDEX, doc_type=DOC_TYPE, size=NUM_RESULTS)
    return jsonify(results)

@app.route("/api/users/<user>/")
def api_user_detail(user):
    body = {"query":{"match":{"user":user}}}
    results = es.search(index="main", body=body)
    # ['hits']['hits']
    return jsonify(results)

@app.route("/api/ideas/<ideaID>/")
def api_idea_detail(ideaID):
    results = es.search(index="main",body={"query":{"match":{"_id":ideaID}}})['hits']['hits'][0]
    return jsonify(results)

# HELPER FUNCTIONS

def insert_idea(user, headline, detail=""):
    CREATE_USERS = True
    if CREATE_USERS is True:
        # First check to see if the user exists
        stormpath_accounts = stormpath_application.accounts.search(user)
        if len(stormpath_accounts) == 0:
            # If not, try to create the user
            try:
                given_name, surname = get_name().split(" ", 1)
                name_slug = (given_name + surname).lower().replace(" ","")
                stormpath_account = stormpath_application.accounts.create({
                    'given_name': given_name,
                    'surname':    surname,
                    'username':   name_slug,
                    'email':      user,
                    'password':   "".join(random.sample(string.letters + string.digits,16)),
                })
            except Exception, e:
                print e
                pass
                """
                A stormpath exception looks like this:
                    {u'code': 2001,
                     u'developerMessage': u'Account with that email already exists.  Please choose another email.',
                     u'message': u'Account with that email already exists.  Please choose another email.',
                     u'moreInfo': u'http://docs.stormpath.com/errors/2001',
                     u'status': 409}
                """

    body = dict(
        user      = user,
        headline  = headline,
        detail    = detail,
        created   = datetime.datetime.now(),
        private   = False,
    )
    result = es.index(index=INDEX, doc_type=DOC_TYPE, body=body)
    return result.get("_id")

# The only real route -- to receive emails from Mailgun
# Handler for HTTP POST to http://myhost.com/messages for the route defined above

@app.route("/receive_email/", methods=["POST"])
def process_incoming_email():
    """
    Test this from the command line:
        curl -X POST localhost:5000/receive_email/ -d recipient="recipient" -d sender=sender -d subject=subject -d body-plain="i like turtles"
    """
    post = request.form
    files = request.files

    sender     = post.get('sender')
    recipient  = post.get('recipient')
    subject    = post.get('subject', '')
    body_plain = post.get('body-plain', '')
    body_without_quotes = post.get('stripped-text', '')

    if settings.DEBUG:
        print "Incoming email message from mailgun:"
        print sender, recipient, subject, body_plain

    assert sender is not None, "Need sender!"
    SEPARATOR = "\n"
    try:
        headline, detail = body_plain.split(SEPARATOR, 1)
        detail = detail.strip()
    except:
        headline = body_plain
        detail = ""

    # attachments:
    for filename in files:
        f = files[filename]
        # do something with the file
        # probably store somewhere like fileinkpicker?

    idea_id = insert_idea(sender, headline, detail)

    # craft a response email
    today = datetime.datetime.now().date()
    subject ="{} Idea Saved: {}".format(str(today), headline)
    url= "http://dailyidea.com/#/ideas/{}".format(idea_id)
    context = dict(
        headline=headline,
        detail=detail,
        url=url,
        )
    text = render_template("emails/idea_receipt_confirmation.email", **context)
    _ = send_email(
        to=sender,
        subject=subject,
        text=text,
        )

    response =  'OK: {}'.format(", ".join([sender, recipient, subject, body_plain]))
    return response

def send_email(to, subject, text, from_="Eric from Daily Idea <eric@dailyidea.com>", extra_data=None):
    data = {"from": from_,
            "to": [to],
            "subject": subject,
            "text": text
    }
    if extra_data is not None:
        data.update(extra_data)

    response = requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_API_KEY),
        data=data
    )
    print "          sent mail!"
    print response
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.DEBUG, port=settings.PORT)

import datetime
import json
import requests

from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import elasticsearch

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
    body = dict(
        user      = user,
        headline  = headline,
        detail    = detail,
        created   = datetime.datetime.now(),
        private   = False,
    )
    es.index(index=INDEX, doc_type=DOC_TYPE, body=body)

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

    insert_idea(sender, headline, detail)

    # craft a response email
    today = datetime.datetime.now().date()
    subject="{} Idea Saved: {}".format(str(today), headline),
    text = "Hello!"
    send_email(
        to=sender,
        subject=subject,
        text=text,
        )

    return 'OK: {}'.format(", ".join([sender, recipient, subject, body_plain]))

def send_email(to, subject, text, from_="Eric from Daily Idea <eric@dailyidea.com>", extra_data=None):
    data = {"from": from_,
            "to": [to],
            "subject": subject,
            "text": text
    }
    if extra_data is not None:
        data.update(extra_data)

    print "          sending mail!"

    response = requests.post(
        settings.MAILGUN_URL,
        auth=("api", settings.MAILGUN_API_KEY),
        data=data
    )
    print "          sent mail!"
    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=settings.DEBUG, port=settings.PORT)

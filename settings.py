MAILGUN_URL = "https://api.mailgun.net/v2/dailyidea.com/messages"



DEBUG = True
ELASTICSEARCH_URL = ""
PORT = 5000
HOST = "localhost"



import os
ELASTICSEARCH_URL = os.environ['ELASTICSEARCH_URL']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']

DEBUG = False
PORT = 80
HOST = "/"


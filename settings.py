MAILGUN_URL = "https://api.mailgun.net/v2/dailyidea.com/messages"



DEBUG = True
ELASTICSEARCH_URL = ""
PORT = 5000
HOST = "localhost"



import os
ELASTICSEARCH_URL = os.environ['ELASTICSEARCH_URL']
MAILGUN_API_KEY = os.environ['MAILGUN_API_KEY']
STORMPATH_API_KEY_ID = os.environ['STORMPATH_API_KEY_ID']
STORMPATH_API_KEY_SECRET = os.environ['STORMPATH_API_KEY_SECRET']
STORMPATH_APPLICATION_NAME = "Daily Idea"

DEBUG = False
PORT = 80
HOST = "/"


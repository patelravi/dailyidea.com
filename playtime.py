from stormpath.client import Client as StormpathClient

STORMPATH_API_KEY_ID="4FESWTU76DNA7UVHUCNJ6E0AB"
STORMPATH_API_KEY_SECRET="dx5/ABWKvnjxMM5nEMwNLyCc90y0wwUXfNsKWBJWaJ4"
STORMPATH_APPLICATION_NAME="Daily Idea"

stormpath_client = StormpathClient(
                       api_key_id=STORMPATH_API_KEY_ID,
                       api_key_secret=STORMPATH_API_KEY_SECRET)
stormpath_application = stormpath_client.applications.search(STORMPATH_APPLICATION_NAME)[0]


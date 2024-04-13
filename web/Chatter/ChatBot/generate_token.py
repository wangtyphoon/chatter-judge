import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/generative-language.tuning']

def load_creds():
    """Converts `client_secret.json` to a credential object.

    This function caches the generated tokens to minimize the use of the
    consent screen.
    """
    creds = None

    flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', SCOPES)
    creds = flow.run_local_server()

        # Save the credentials for the next run
    with open('token1.json', 'w') as token:
        token.write(creds.to_json())
    return creds

load_creds()

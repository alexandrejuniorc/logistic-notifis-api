import os
import sys
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv('BITBUCKET_CLIENT_ID')
CLIENT_SECRET = os.getenv('BITBUCKET_CLIENT_SECRET')

def get_bitbucket_token():
    """it generates a bitbucket token"""

    get_token_response = requests.post(
        "https://bitbucket.org/site/oauth2/access_token",
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            "grant_type": "client_credentials",
        },
        timeout=10,
    )

    if get_token_response.status_code != 200:
        return None, get_token_response.text

    get_token_data = get_token_response.json()

    return get_token_data['access_token'], None


bitbucket_token, error = get_bitbucket_token()

if error is not None:
    print(f"Failed to get bitbucket token. {error}")
    sys.exit(1)

print(bitbucket_token)

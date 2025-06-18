#!/usr/bin/python

import os

import httplib2
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

from utils.notifications import send_error_notification, send_success_notification

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the Google API Console at
# https://console.cloud.google.com/.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "credentials/client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(
    os.path.join(os.path.dirname(__file__), CLIENT_SECRETS_FILE)
)


def update_credentials():
    """Update YouTube API credentials by forcing re-authentication."""
    try:
        print("Updating YouTube API credentials...")

        flow = flow_from_clientsecrets(
            CLIENT_SECRETS_FILE,
            scope=YOUTUBE_UPLOAD_SCOPE,
            message=MISSING_CLIENT_SECRETS_MESSAGE,
        )

        storage = Storage("./credentials/tokens.json")

        # Get new credentials
        args = argparser.parse_args([])
        credentials = run_flow(flow, storage, args)

        if credentials:
            success_msg = (
                "Successfully updated credentials and saved to credentials/tokens.json"
            )
            print(success_msg)
            send_success_notification(success_msg, "Credential Update")
        else:
            error_msg = "Failed to update credentials"
            print(error_msg)
            send_error_notification(error_msg, context="Credential Update")

    except Exception as e:
        error_msg = "Failed to update YouTube API credentials"
        print(f"{error_msg}: {e}")
        send_error_notification(error_msg, e, "Credential Update")


if __name__ == "__main__":
    update_credentials()

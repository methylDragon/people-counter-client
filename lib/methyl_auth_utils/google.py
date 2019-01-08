'''
  methyl_auth_utils.google

  Utilities for authenticating with Google's APIs.


                                   .     .
                                .  |\-^-/|  .
                               /| } O.=.O { |\
                              /´ \ \_ ~ _/ / `\
                            /´ |  \-/ ~ \-/  | `\
                            |   |  /\\ //\  |   |
                             \|\|\/-""-""-\/|/|/
                                     ______/ /
                                     '------'
                       _   _        _  ___
             _ __  ___| |_| |_ _  _| ||   \ _ _ __ _ __ _ ___ _ _
            | '  \/ -_)  _| ' \ || | || |) | '_/ _` / _` / _ \ ' \
            |_|_|_\___|\__|_||_\_, |_||___/|_| \__,_\__, \___/_||_|
                               |__/                 |___/
            -------------------------------------------------------
                            github.com/methylDragon

  CloudPasswordLogin:
  Credential object for logging in with an email, password, and API key.

  Login is done via Google's password verify REST API.
  Also implements REST API auth token refresh.

  Parameters
  ----------
  email : str
  password : str
  api_key : str
    Google application API key.

  ---

  License: BSD-2-Clause

'''

import json
import requests
import datetime
import google.auth.credentials

class CloudPasswordLogin(google.auth.credentials.Credentials):
    def __init__(self, email, password, api_key):
        self.email = email
        self.password = password
        self.api_key = api_key

        self.login_obj = self.login(self.email, self.password)

        self.uid = self.fetch_uid(self.login_obj)
        self.token = self.fetch_token(self.login_obj)

        self.expiry_duration = self.fetch_expiry_duration(self.login_obj)
        self.expiry = self.calculate_expiry(self.expiry_duration)

    def login(self, email=None, password=None):
        """Obtain login response JSON object."""
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={0}".format(self.api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": self.email, "password": self.password, "returnSecureToken": True})

        return requests.post(request_ref, headers=headers, data=data)

    def fetch_token(self, login_obj):
        """Parse login response for ID token."""
        try:
            token = login_obj.json()['idToken']
        except:
            try:
                token = login_obj.json()['users'][0]['idToken']
            except:
                return None
                pass

        return token

    def fetch_uid(self, login_obj):
        """Parse login response for UID."""
        try:
            uid = login_obj.json()['localId']
        except:
            try:
                uid = login_obj.json()['users'][0]['localId']
            except:
                return None
                pass

        return uid

    def fetch_expiry_duration(self, login_obj):
        """Parse login response for token validity duration."""
        try:
            expiry_duration = login_obj.json()['expiresIn']
        except:
            try:
                expiry_duration = login_obj.json()['users'][0]['expiresIn']
            except:
                return None
                pass

        return int(expiry_duration)

    def calculate_expiry(self, expiry_duration):
        """Calculate token expiry time."""
        try:
            return datetime.datetime.now() + datetime.timedelta(seconds=expiry_duration)
        except:
            return None

    @property
    def expired(self):
        if not self.expiry:
            return False

        return datetime.datetime.now() >= self.expiry - datetime.timedelta(seconds=5)

    def refresh(self, email=None, password=None, api_key=None, expiry_duration=None):
        """Obtain new valid token."""
        self.login_obj = self.login(self.email, self.password)

        self.uid = self.fetch_uid(self.login_obj)
        self.token = self.fetch_token(self.login_obj)

        self.expiry_duration = self.fetch_expiry_duration(self.login_obj)
        self.expiry = self.calculate_expiry(self.expiry_duration)


## Test code
if __name__ == "__main__":
    from google.cloud import firestore

    email = "[TEST EMAIL HERE]"
    password = "[TEST PASSWORD]"
    api_key = "[API KEY]"

    creds = FirestoreCredentials(email, password, api_key)
    db = firestore.Client(project='[PROJECT ID]', credentials=creds)

    docs = db.collection('').where('uid', '==', creds.uid).get()

    for doc in docs:
        print(doc.id)
        print(doc.to_dict())

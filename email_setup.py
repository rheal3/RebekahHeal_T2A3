import pickle
import os.path
import time
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from email.mime.text import MIMEText
import base64


class EmailSetup:

    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send']

    @classmethod
    def get_credentials(cls, current_user):
        credentials = None
        token_file = f'{current_user}_token.pickle'

        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', EmailSetup.SCOPES)
                credentials = flow.run_local_server(port=0)

            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)

        return credentials

    @classmethod
    def create_message(cls, to, subject, message_text, sender='me'):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
        return {'raw': raw_message.decode("utf-8")}

    @classmethod
    def send_message(cls, message, current_user, user_id='me'):
        service = build('gmail', 'v1', credentials=EmailSetup.get_credentials(current_user))

        try:
            message = service.users().messages().send(userId=user_id, body=message).execute()
            # print(f"Message Id: {message['id']}")
            print("Message sent.")
            time.sleep(1.5)
            return message
        except Exception:
            print("Unable to send message.")
            return None

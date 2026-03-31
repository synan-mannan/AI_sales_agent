from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import base64


creds = Credentials.from_authorized_user_file(
    "C:/Users/syedm/Synelime/coirei/Email/ai_sales_agent/sales/token.json"
)
service = build("gmail", "v1", credentials=creds)

# fetch messages
results = service.users().messages().list(userId='me', maxResults=5).execute()
messages = results.get('messages', [])


# decode base64
def decodeMail(data):
    return base64.urlsafe_b64decode(data).decode("utf-8")


def get_sender(message):
    headers = message['payload']['headers']
    for header in headers:
        if header['name'] == 'From':
            return header['value']
    return None


def get_subject(message):
    headers = message['payload']['headers']
    for header in headers:
        if header['name'] == 'Subject':
            return header['value']
    return None



def extractEmailbody(message):
    payload = message['payload']

    # case 1: multipart
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                data = part['body'].get('data')
                if data:
                    return decodeMail(data)

    
    if 'body' in payload and 'data' in payload['body']:
        return decodeMail(payload['body']['data'])

    return ""



for msg in messages:
    data = service.users().messages().get(
        userId='me',
        id=msg['id']
    ).execute()

    sender = get_sender(data)
    subject = get_subject(data)
    body = extractEmailbody(data)

    final_data = {
        "sender": sender,
        "subject": subject,
        "body": body
    }

    print(final_data)
    print("-" * 50)
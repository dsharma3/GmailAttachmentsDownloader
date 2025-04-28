from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import base64
import os
import zipfile

# Gmail API scope for reading emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = build('gmail', 'v1', credentials=creds)
    return service

def get_sender_domain(headers):
    for header in headers:
        if header['name'] == 'From':
            email = header['value'].split('<')[-1].replace('>', '').strip()
            domain = email.split('@')[-1]
            return domain.replace('.', '_')
    return 'unknown_domain'

def save_attachment(service, message, domain_folder):
    payload = message.get('payload', {})
    parts = payload.get('parts', [])

    if not parts:
        parts = [payload]

    for part in parts:
        filename = part.get('filename')
        body = part.get('body', {})
        if filename and 'attachmentId' in body:
            attachment = service.users().messages().attachments().get(
                userId='me',
                messageId=message['id'],
                id=body['attachmentId']
            ).execute()

            data = base64.urlsafe_b64decode(attachment['data'])

            os.makedirs(domain_folder, exist_ok=True)
            filepath = os.path.join(domain_folder, filename)
            with open(filepath, 'wb') as f:
                f.write(data)
            print(f"Saved: {filepath}")

            # After saving, check if it's a zip file
            if filename.lower().endswith('.zip'):
                unzip_file(filepath, domain_folder)

def unzip_file(zip_path, extract_to):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        print(f"Unzipped: {zip_path} to {extract_to}")

        # Optionally delete the zip file after extraction
        os.remove(zip_path)
        print(f"Deleted zip: {zip_path}")

    except zipfile.BadZipFile:
        print(f"Bad zip file: {zip_path}. Skipping unzip.")

def download_all_attachments(service):
    results = service.users().messages().list(userId='me', q="has:attachment").execute()
    messages = results.get('messages', [])

    if not messages:
        print("No attachments found.")
        return

    for msg in messages:
        message = service.users().messages().get(userId='me', id=msg['id']).execute()
        headers = message['payload'].get('headers', [])
        sender_domain = get_sender_domain(headers)
        domain_folder = f"attachments/{sender_domain}"
        
        save_attachment(service, message, domain_folder)

if __name__ == "__main__":
    service = authenticate_gmail()
    download_all_attachments(service)

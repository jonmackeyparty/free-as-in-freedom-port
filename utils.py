import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from bs4 import BeautifulSoup

def get_unread_emails(service):
    query = "is:inbox"
    response = service.users().messages().list(userId='me', q=query).execute()
    messages = []

    if 'messages' in response:
        messages.extend(response['messages'])

    # while 'nextPageToken' in response:
    #     page_token = response['nextPageToken']
    #     response = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        
    #     if 'messages' in response:
    #         messages.extend(response['messages'])

    return messages
  

def get_email_data(service, message_id):
    msg = service.users().messages().get(userId='me', id=message_id, format='full').execute()
    payload = msg['payload']
    headers = payload['headers']
    email_data = {'id': message_id}
    email_data['links'] = []
    for header in headers:
        name = header['name']
        value = header['value']
        if name == 'From':
            email_data['from'] = value
        if name == 'Date':
            email_data['date'] = value
        if name == 'Subject':
            email_data['subject'] = value

    if 'parts' in payload:
        parts = payload['parts']
        data = None
        for part in parts:
            if part['mimeType'] == 'text/plain':
                data = part['body']['data']
            elif part['mimeType'] == 'text/html':
                data = part['body']['data']

        if data is not None:
            text = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
            soup = BeautifulSoup(text, 'html.parser')
            clean_text = soup.get_text()
            links = soup.find_all("a")
            for link in links:
                email_data['links'].append(link.get("href"))
            email_data['text'] = clean_text
        else:
            data = payload['body']['data']
            text = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
            soup = BeautifulSoup(text, 'html.parser')
            clean_text = soup.get_text()
            links = soup.find_all("a")
            for link in links:
                email_data['links'].append(link.get("href"))
            email_data['text'] = clean_text
    else:
        data = payload['body']['data']
        text = base64.urlsafe_b64decode(data.encode('UTF-8')).decode('UTF-8')
        soup = BeautifulSoup(text, 'html.parser')
        email_data['text'] = soup.get_text()

    return email_data
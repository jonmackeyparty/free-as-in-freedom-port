import base64
import os
import time 
import random
import re
import asyncio
import pickle  
import email 
import mimetypes
from playwright.async_api import async_playwright
from playwright.sync_api import Page, expect, sync_playwright
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow 
from google.auth.transport.requests import Request 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from bs4 import BeautifulSoup

# Define the SCOPES. If modifying it, delete the token.pickle file. 
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"] 

def getLink(): 
    # Variable creds will store the user access token. 
    # If no valid token found, we will create one. 
    creds = None
   
    # The file token.pickle contains the user access token. 
    # Check if it exists 
    if os.path.exists('token.pickle'): 
  
        # Read the token from the file and store it in the variable creds 
        with open('token.pickle', 'rb') as token: 
            creds = pickle.load(token) 
            
    # If credentials are not available or are invalid, ask the user to log in. 
    if not creds or not creds.valid: 
        if creds and creds.expired and creds.refresh_token: 
            creds.refresh(Request()) 
        else: 
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES) 
            creds = flow.run_local_server(port=0) 
  
        # Save the access token in token.pickle file for the next run 
        with open('token.pickle', 'wb') as token: 
            pickle.dump(creds, token) 
  
    # Connect to the Gmail API 
    service = build('gmail', 'v1', credentials=creds) 

    new_msg = list_new_message(service)
    email_data = get_email_data(service, new_msg)
    print("SUCCESS: LINK RETRIEVED")
    return email_data['links'][0]

async def sendLink():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        try:
            await page.goto("http://accounts.craigslist.org/login")
            await page.get_by_label('Email / Handle').fill(os.getenv('ID'))
            await page.get_by_label('Password').fill(os.getenv('PASSWORD'))
            await page.get_by_role('button', name='Log in').click()
            await page.get_by_role('button', name='click here').click()
        except Exception as e:
            print(f"An error occurred: {str(e)}, failed at link retrieval")
        finally:
            print("SUCCESS: LINK SENT")
            await page.close()

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

def list_new_message(service):
    response = service.users().messages().list(userId='me', maxResults=1, q="is:inbox").execute()
    messages = []

    if 'messages' in response:
        messages.extend(response['messages'])
    
    return messages[0]['id']

    
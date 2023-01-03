'''
This module sends emails with attachments to the participants
Reference - https://developers.google.com/gmail/api/quickstart/python
'''
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow       #pip install google_auth_oauthlib 
from googleapiclient.discovery import build      # pip install google-api-python-client
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText           # pip install email
#for attachment import following 
from email.mime.multipart import MIMEMultipart
import mimetypes
from email.mime.base import MIMEBase


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

#path of attachment file(s)
file_attachments = [r'/home/riya-gupta/Documents/Projects/project1-Email by GmailAPI/Custom t-shirt sizes.ods' , r'//home/riya-gupta/Documents/Projects/project1-Email by GmailAPI/details GiVentures.xlsx']

def aunthentication():
    creds = None
    # The file token.json storesthe user's access and refresh tokens,and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('project1-Email by GmailAPI/client_secrets.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def prepare_and_send_email(recipient, subject, message_text):
    """Prepares and send email with attachment to the participants
    """
    creds = aunthentication()
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        #create message
        msg = create_message('riya.gupta@giindia.com', recipient,subject, message_text)
        send_message(service, 'me', msg)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

def create_message(sender, to, subject, message_text):
    '''Create a message for an email.
    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.
    Returns:
    An object containing a base64url encoded email object.
    '''
    #for attachment 
    #replace MIMEText() object with MIMEMultipart()
    #message = MIMEText(message_text)
    message = MIMEMultipart()
    message['from'] = sender
    message['to'] = to
    message['subject'] = subject
    message['message text'] = message_text
    # for attaching attachment(s)
    for attachment in file_attachments:
        content_type , encoding = mimetypes.guess_type(attachment)
        main_type , sub_type = content_type.split('/' , 1)
        file_name = os.path.basename(attachment)

        f = open(attachment ,  'rb')
        
        myFile = MIMEBase(main_type , sub_type)
        myFile.set_payload(f.read())
        myFile.add_header('content-disposition' , 'attachment' , filename = file_name)

        f.close()

        message.attach(myFile)

    # return the complete message      
    return {'raw':base64.urlsafe_b64encode(message.as_string().encode()).decode()}

def send_message(service, user_id, message):
    """Send an email message.
    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.
    Returns:
    Sent Message."""
    try:  #check this ofr service.users() for multiple senders
        message = (service.users().messages().send(userId=user_id,body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print('An error occurred: %s' % error)
if __name__ == '__main__':
        emails = ['riyagupta0823@gmail.com' , 'sheenuriyagupta16@gmail.com' , 'riya088888@gmail.com']
        #prepare_and_send_email('sugandh.gupta@giindia.com', 'Greeting from Global Infoventures', 'This is a test email for our upcoming app')
        for email in emails:
            prepare_and_send_email(email,'HI FILE IS ATTACHED' , 'This is a test email of attachment by gmailAPI method Thanks.')
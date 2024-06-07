from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import pickle
import datetime

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def authenticate_google_drive():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def get_latest_file_in_folder(folder_id):
    creds = authenticate_google_drive()
    service = build('drive', 'v3', credentials=creds)

    # Get the list of files in the folder
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=10,
        fields="nextPageToken, files(id, name, createdTime, modifiedTime)"
    ).execute()
    
    items = results.get('files', [])
    
    if not items:
        print('No files found.')
        return None
    
    # Find the latest file based on modifiedTime
    latest_file = max(items, key=lambda x: x['modifiedTime'])
    
    print(f"Latest file: {latest_file['name']} (ID: {latest_file['id']})")
    return latest_file

# Replace with your folder ID
folder_id = '19SFs0vqGWTEqiUJoHDrNXpZmFtbkLoGy'
latest_file = get_latest_file_in_folder(folder_id)

from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import io
from googleapiclient.http import MediaIoBaseDownload

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/home/src/divelog/credentials.json'

# Define the required scope
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def authenticate_service_account():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def get_latest_file_in_folder(folder_id):
    creds = authenticate_service_account()
    service = build('drive', 'v3', credentials=creds)

    # Get the list of files in the folder
    results = service.files().list(
        q=f"'{folder_id}' in parents",
        pageSize=100,
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


def download_file(file_id, file_name):
    creds = authenticate_service_account()
    service = build('drive', 'v3', credentials=creds)
    
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

@data_loader
def load_data(*args, **kwargs):
    """
    Template code for loading data from any source.

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your data loading logic here

    folder_id = '19SFs0vqGWTEqiUJoHDrNXpZmFtbkLoGy'
    latest_file = get_latest_file_in_folder(folder_id)

    if latest_file:
        download_file(latest_file['id'], latest_file['name'])

    return latest_file


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

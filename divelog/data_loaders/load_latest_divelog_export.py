from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime
import io
import os
from googleapiclient.http import MediaIoBaseDownload

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


# Path to your service account key file
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH")
FOLDER_ID = os.getenv("FOLDER_ID")

# Define the required scope
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


def authenticate_service_account():
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_PATH, scopes=SCOPES
    )
    return creds


def get_latest_file_in_folder(folder_id):
    creds = authenticate_service_account()
    service = build("drive", "v3", credentials=creds)

    # Get the list of files in the folder
    results = (
        service.files()
        .list(
            q=f"'{folder_id}' in parents",
            pageSize=100,
            fields="nextPageToken, files(id, name, createdTime, modifiedTime)",
        )
        .execute()
    )

    items = results.get("files", [])

    if not items:
        print("No files found.")
        return None

    # Find the latest file based on modifiedTime
    latest_file = max(items, key=lambda x: x["modifiedTime"])

    print(f"Latest file: {latest_file['name']} (ID: {latest_file['id']})")
    return latest_file


def download_file(file_id, file_name):
    creds = authenticate_service_account()
    service = build("drive", "v3", credentials=creds)

    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_name, "wb")
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
    if not (CREDENTIALS_PATH and FOLDER_ID):
        return "anonymized_subsurface_export.ssrf"
    else:
        latest_file = get_latest_file_in_folder(FOLDER_ID)

        if latest_file:
            download_file(latest_file["id"], latest_file["name"])

        return latest_file["name"]


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
    assert os.path.isfile(output), "The output is not a valid file path"
    assert os.path.getsize(output) > 0, "The output file is empty"

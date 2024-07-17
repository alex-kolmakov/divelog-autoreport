# Setup and requirements
Project requires Docker and docker-compose(insert cool image here) to start. 

Data loading pipeline **will use anonymized data from my dives if the credentials file and folder_id are not available**. This is to ensure that the pipeline can be run without any issues.

There is also an option to run batch inference pipeline and use async requests to export resulted data to a Notion page. This requires a Notion token and a database id. **If they are not provided - the pipeline will only print the data to the console.**

## (Optional) How to load data from Google Drive

- Step 1: [Create a Project in the Google Cloud Console](https://developers.google.com/workspace/guides/create-project)

- Step 2: Enable the [Google Drive API](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com) for the project. 

- Step 3: Create Service Account Credentials
    - Navigate to APIs & Services > Credentials.
    - Click Create credentials and select Service account.
    - Fill in the required fields and click Create(no additional permissions required)

- Step 4: Download the Service Account Key in JSON format
    - After creating the service account, navigate to it under APIs & Services > Credentials.
    - Click on your service account.
    - Under the Keys section, click Add Key > Create New Key.
    - Choose JSON and click Create. This will download the key file to your computer.
    - Rename the file to credentials.json and place it in the root directory of the project.
- Step 5: Get the Folder ID
    - Open the folder in Google Drive. The URL will look something like this: https://drive.google.com/drive/u/0/folders/XXXXXXXXXXXXX.
    - Copy the folder ID (XXXXXXXXXXXXX).

In the .env.sample look for the section with Google Drive comment and amend the following code:

```plaintext
CREDENTIALS_PATH=/home/src/credentials.json
FOLDER_ID=XXXXXXXXXXXXX
```
Now you can run the pipeline and it will load the data from the specified folder in Google Drive.


## (Optional) How to setup Notion database

- Step 1: Setup a page with properties like on the image

<img width="996" alt="Properties" src="https://github.com/user-attachments/assets/a8ec9827-53bd-41ea-829a-1ee2aeb05157">

- Step 2: Proceed with the [official tutorial](https://developers.notion.com/docs/create-a-notion-integration#create-your-integration-in-notion)






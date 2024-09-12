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



## How to run the project

Assuming you already started the Codespace, and finished docker-compose procedures, now we can start runnin the project.

Since we are using Global Data product, if you try to run the last pipeline without running the first one, it will start the prerequisite pipeline automatically. But to have more visibility, my advice is to run them in order:

**Load data** -> **Train model** -> **Batch inference**.

When running training pipeline there is an option sneak peek into MLflow UI by visiting forwarded port(or localhost:8012 if you are running locally) and see the model training process and check out training metrics and resulting model in the registry. Check out video below on how to do it in the Codespace:

https://github.com/user-attachments/assets/3bdc2e1f-0dc2-4a1b-9c41-f710c6c51d45


There is also an option to run this project by setting up your own Google Drive and Notion API credentials. This will allow you to load the data from your own logbook and export the results to your Notion page. For this - please refer to the [additional documentaion](./documentation/setup.md).



https://github.com/user-attachments/assets/c82adc73-58e9-4afb-af79-e7dd3c368dbe
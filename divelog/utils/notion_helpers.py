
import pandas as pd
import requests
import json
import os


NOTION_API_TOKEN = os.getenv('NOTION_API_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# Headers for Notion API requests
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def form_properties(report):
    return {
        "Dive Number": {
            "title": [
                {
                    "text": {
                        "content": str(report["Dive Number"])
                    }
                }
            ]
        },
        "Trip": {
            "rich_text": [
                {
                    "text": {
                        "content": report["Trip"]
                    }
                }
            ]
        },
        "Dive Site": {
            "rich_text": [
                {
                    "text": {
                        "content": report["Dive Site"]
                    }
                }
            ]
        },
        "Minimal NDL": {
            "number": report["Minimal NDL"]
        },
        "SAC Rate": {
            "number": report["SAC Rate"]
        },
        "Likelihood of Adverse Conditions": {
            "number": report["Likelihood of Adverse Conditions"]
        },
        "Issues": {
            "multi_select": [
                {"name": item} for item in report['Issues']
            ]
        }
        
    }

# Function to send data to Notion
def send_to_notion(report, api_token, database_id):
    url = "https://api.notion.com/v1/pages"
    
    data = {
        "parent": {"database_id": database_id},
        "properties": form_properties(report)
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

# Function to retrieve all pages in a Notion database
def get_all_pages(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data.get('results', [])

# Function to update a page in Notion
def update_page(page_id, report, headers):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    data = {
        "properties": form_properties(report)
    }
    
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

# Function to add or update a page in Notion
def add_or_update_page(report):
    pages = get_all_pages(NOTION_DATABASE_ID, headers)
    page_id = None
    for page in pages:
        title = page['properties']['Dive Number']['title'][0]['text']['content']
        if title == str(report["Dive Number"]):
            page_id = page['id']
            break
    
    if page_id:
        status_code, response = update_page(page_id, report, headers)
        if status_code == 200:
            print(f"Successfully updated report for Dive {report['Dive Number']}")
        else:
            print(f"Failed to update report for Dive {report['Dive Number']}: {response}")
    else:
        status_code, response = send_to_notion(report, NOTION_API_TOKEN, NOTION_DATABASE_ID)
        if status_code == 200:
            print(f"Successfully added report for Dive {report['Dive Number']}")
        else:
            print(f"Failed to add report for Dive {report['Dive Number']}: {response}")

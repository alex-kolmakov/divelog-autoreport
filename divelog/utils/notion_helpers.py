import pandas as pd
import aiohttp
import asyncio
import json
import os

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

# Headers for Notion API requests
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def form_properties(report):
    return {
        "Dive Number": {
            "rich_text": [{"text": {"content": str(report["Dive Number"])}}]
        },
        "Trip": {"rich_text": [{"text": {"content": report["Trip"]}}]},
        "Dive Site": {"title": [{"text": {"content": report["Dive Site"]}}]},
        "Minimal NDL": {"number": report["Minimal NDL"]},
        "SAC Rate": {"number": report["SAC Rate"]},
        "Rating": {"number": report["Rating"]},
        "Issues": {"multi_select": [{"name": item} for item in report["Issues"]]},
    }


# Function to send data to Notion
async def send_to_notion(report, session, api_token, database_id):
    url = "https://api.notion.com/v1/pages"

    data = {
        "parent": {"database_id": database_id},
        "properties": form_properties(report),
    }

    async with session.post(url, headers=headers, data=json.dumps(data)) as response:
        return response.status, await response.json()


async def get_all_pages(session, database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    all_pages = []
    payload = {}

    while True:
        async with session.post(url, headers=headers, json=payload) as response:
            data = await response.json()
            all_pages.extend(data.get("results", []))
            next_cursor = data.get("next_cursor")
            if not next_cursor:
                break
            payload["start_cursor"] = next_cursor

    return all_pages


# Function to update a page in Notion
async def update_page(session, page_id, report, headers):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    data = {"properties": form_properties(report)}

    async with session.patch(url, headers=headers, data=json.dumps(data)) as response:
        return response.status, await response.json()


async def collect_dive_number_to_page_id_map(session):
    pages = await get_all_pages(session, NOTION_DATABASE_ID, headers)
    dive_number_to_page_id = {}
    for page in pages:
        dive_number = page["properties"]["Dive Number"]["rich_text"][0]["text"][
            "content"
        ]
        dive_number_to_page_id[dive_number] = page["id"]
    return dive_number_to_page_id


async def add_or_update_page(session, report, dive_number_to_page_id):
    if report["Dive Number"] in dive_number_to_page_id:
        page_id = dive_number_to_page_id[str(report["Dive Number"])]

        status_code, response = await update_page(session, page_id, report, headers)
        if status_code != 200:
            print(
                f"Failed to update report for Dive {report['Dive Number']}: {response}"
            )
    else:
        status_code, response = await send_to_notion(
            report, session, NOTION_API_TOKEN, NOTION_DATABASE_ID
        )
        if status_code != 200:
            print(f"Failed to add report for Dive {report['Dive Number']}: {response}")


async def export_data(reports):
    async with aiohttp.ClientSession() as session:
        dive_number_to_page_id = await collect_dive_number_to_page_id_map(session)
        tasks = []
        for index, report in reports.iterrows():
            tasks.append(add_or_update_page(session, report, dive_number_to_page_id))
        await asyncio.gather(*tasks)

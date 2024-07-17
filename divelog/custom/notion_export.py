import nest_asyncio
import asyncio
import aiohttp
import os

from divelog.utils.notion_helpers import (
    add_or_update_page,
    collect_dive_number_to_page_id_map,
)

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom

nest_asyncio.apply()

NOTION_API_TOKEN = os.getenv("NOTION_API_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


@custom
def export_data(reports, *args, **kwargs):
    if not (NOTION_API_TOKEN or NOTION_DATABASE_ID):
        print(f"Notion details were not provided, skipping export to notion..")
        return reports

    async def get_dive_number_to_page_id():
        async with aiohttp.ClientSession() as session:
            dive_number_to_page_id = await collect_dive_number_to_page_id_map(session)
        return dive_number_to_page_id

    async def update_notion_pages(reports, dive_number_to_page_id):
        async with aiohttp.ClientSession() as session:
            tasks = [
                add_or_update_page(session, report, dive_number_to_page_id)
                for index, report in reports.iterrows()
            ]
            await asyncio.gather(*tasks)

    async def main(reports):
        dive_number_to_page_id = await get_dive_number_to_page_id()
        await update_notion_pages(reports, dive_number_to_page_id)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(reports))

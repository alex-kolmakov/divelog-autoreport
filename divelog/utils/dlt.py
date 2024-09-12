import dlt
import re
import lancedb

import time
from dlt.sources.helpers.rest_client.paginators import BasePaginator
from requests import Request, Response
from typing import List, Optional, Any
from rest_api import rest_api_source
from dlt.destinations.adapters import lancedb_adapter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup


BASE_URL = "https://dan.org/wp-json/wp/v2/"
PER_PAGE = 100
START_DATE = "2000-01-01T00:00:00"


class WordPressPaginator(BasePaginator):
    def __init__(self, start_page: int = 1, per_page: int = PER_PAGE):
        self.current_page = start_page
        self.per_page = per_page

    def update_request(self, request: Request) -> None:
        """Updates the request with the current page."""
        if request.params is None:
            request.params = {}
        request.params["page"] = self.current_page
        request.params["per_page"] = self.per_page

    def update_state(
        self, response: Response, data: Optional[List[Any]] = None
    ) -> None:
        """Updates the state to stop pagination if no more data is returned or fewer posts than per_page are returned."""

        if not data or len(data) < self.per_page or response.status_code == 400:
            self._has_next_page = False
        else:
            self.current_page += 1
            self._has_next_page = True


def remove_html_tags(text):
    """Remove HTML tags, JavaScript, and extra spaces from a string."""
    soup = BeautifulSoup(text, "html.parser")

    # Remove all script and iframe tags and their content
    for script in soup(["script", "iframe"]):
        script.extract()

    cleaned_text = soup.get_text(separator=" ")

    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()

    return cleaned_text


def chunk_text(text):

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)

    return text_splitter.split_text(text)


def wordpress_rest_api_source():
    return rest_api_source(
        {
            "client": {
                "base_url": BASE_URL,
                "paginator": WordPressPaginator(start_page=1),
            },
            "resource_defaults": {
                "primary_key": "id",
                "write_disposition": "merge",
                "endpoint": {
                    "params": {
                        "per_page": PER_PAGE,
                    },
                },
            },
            "resources": [
                {
                    "name": "dan_health_resources",
                    "endpoint": {
                        "path": "dan_health_resources",
                        "params": {
                            "modified_after": {
                                "type": "incremental",
                                "cursor_path": "modified",
                                "initial_value": START_DATE,
                            },
                        },
                    },
                },
                {
                    "name": "dan_alert_diver",
                    "endpoint": {
                        "path": "dan_alert_diver",
                        "params": {
                            "modified_after": {
                                "type": "incremental",
                                "cursor_path": "modified",
                                "initial_value": START_DATE,
                            },
                        },
                    },
                },
                {
                    "name": "dan_diving_incidents",
                    "endpoint": {
                        "path": "dan_diving_incidents",
                        "params": {
                            "modified_after": {
                                "type": "incremental",
                                "cursor_path": "modified",
                                "initial_value": START_DATE,
                            },
                        },
                    },
                },
                {
                    "name": "dan_diseases_conds",
                    "endpoint": {
                        "path": "dan_diseases_conds",
                        "params": {
                            "modified_after": {
                                "type": "incremental",
                                "cursor_path": "modified",
                                "initial_value": START_DATE,
                            },
                        },
                    },
                },
            ],
        }
    )


@dlt.transformer()
def dan_articles(article):
    clean_content = remove_html_tags(article["content"]["rendered"])
    for chunk in chunk_text(clean_content):
        yield chunk


def run_pipeline(*args, **kwargs):
    pipeline = dlt.pipeline(
        pipeline_name="dan_articles",
        destination="lancedb",
        dataset_name="dan_articles",
    )

    data = wordpress_rest_api_source() | dan_articles

    load_info = pipeline.run(
        lancedb_adapter(data, embed="value"),
        table_name="texts",
        write_disposition="merge",
    )

    db = lancedb.connect(".lancedb")
    dbtable = db.open_table("dan_articles___texts")
    dbtable.create_fts_index("value", replace=True)

    return "dan_articles___texts"

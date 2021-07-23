import json
import os
from typing import Union, Dict

import requests


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


def get_headers():
    with open("../config.json", 'r') as config_file:
        config = json.load(config_file)
        return config["request-headers"]


def map_reset_values(date):
    with open("../config.json", 'r') as config_file:
        config = json.load(config_file)
        reset_values = config["reset-values"]
        reset_values["date"]["date"]["start"] = date
        return reset_values


def make_request(request_type: str, url: str, data: Union[Dict, None] = None):

    if request_type == "post":
        request_callback = requests.post
    elif request_type == "get":
        request_callback = requests.get
    elif request_type == "patch":
        request_callback = requests.patch
    else:
        raise Exception("Invalid Request Type!")

    res = request_callback(
        url=url,
        headers=get_headers(),
        auth=BearerAuth(os.environ["NOTION_KEY"]),
        data=json.dumps(data) if data is not None else {}
    )

    return res.json()


def query_database(database_key_name: str):
    return make_request(
        request_type="post",
        url=f"{os.environ['NOTION_API']}/databases/{os.environ[database_key_name]}/query"
    )


def get_database(database_key_name: str):
    return make_request(
        request_type="get",
        url=f"{os.environ['NOTION_API']}/databases/{os.environ[database_key_name]}"
    )


def update_page(page_key: str, new_data: Dict):
    return make_request(
        request_type="patch",
        url=f"{os.environ['NOTION_API']}/pages/{page_key.replace('-', '')}",
        data={
            "properties": new_data
        }
    )


def add_page_to_database(database_key_name: str, page_data: Dict):
    return make_request(
        request_type="post",
        url="https://api.notion.com/v1/pages",
        data={
            "parent": {
                "database_id": os.environ[database_key_name]
            },
            "properties": page_data
        }
    )

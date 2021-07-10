import json
import os
from typing import Union, Dict

import requests
import toml as toml


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, request):
        request.headers["Authorization"] = f"Bearer {self.token}"
        return request


def get_headers():
    config = toml.load("../config.toml")
    return config["request-headers"]


def make_request(request_type: str, url: str, data: Union[Dict, None] = None):

    if request_type == "post":
        request_callback = requests.post
    elif request_type == "get":
        request_callback = requests.get
    elif request_type == "patch":
        request_callback = requests.patch
    else:
        raise Exception("Invalid Request Type!")

    print(url, data)

    res = request_callback(
        url=url,
        headers=get_headers(),
        auth=BearerAuth(os.environ["NOTION_KEY"]),
        data=json.dumps(data) if data is not None else {}
    )
    print(res)
    return res.json()


def query_database(database_key_name: str):
    return make_request(request_type="post", url=f"{os.environ['NOTION_API']}/databases/{os.environ[database_key_name]}/query")


def update_page(page_key: str, data: Dict):
    return make_request(request_type="patch", url=f"{os.environ['NOTION_API']}/pages/{page_key.replace('-', '')}", data=data)

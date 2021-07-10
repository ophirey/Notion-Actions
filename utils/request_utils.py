import os
from typing import Union

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


def make_request(url: str, data: Union[str, None]=None):
    res = requests.post(
        url=url,
        headers=get_headers(),
        auth=BearerAuth(os.environ["NOTION_KEY"]),
        data=data
    )
    return res.json()


def query_database(database_key_name: str, data: Union[str, None]=None):
    return make_request(url=f"{os.environ['NOTION_API']}/databases/{os.environ[database_key_name]}/query", data=data)

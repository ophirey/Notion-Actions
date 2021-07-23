from typing import Dict, List
from datetime import datetime, timedelta

from utils.request_utils import query_database, update_page, add_page_to_database, map_reset_values, get_database


def create_new_pages_in_db(db_key_name: str, properties: Dict[str, str], num_of_entries: int = 1):
    for i in range(num_of_entries):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        reset_config = map_reset_values(date)
        data = {k: reset_config[properties[k]] for k in properties if properties[k] in reset_config}
        add_page_to_database(db_key_name, data)


def archive_past_week(pages: Dict):

    for page_data in [page["properties"] for page in pages["results"]]:
        add_page_to_database("NOTION_HABITS_ARCHIVE_DB_KEY", page_data)


if __name__ == '__main__':
    db_properties = get_database("NOTION_HABITS_DB_KEY")["properties"]
    db_properties = {k: db_properties[k]["type"] for k in db_properties}
    # type_mappings = {
    #     prop: prev_week_db["results"][0]["properties"][prop]["type"]
    #     for prop in prev_week_db["results"][0]["properties"]
    # }
    create_new_pages_in_db("NOTION_HABITS_DB_KEY", db_properties, 7)
    # archive_past_week(prev_week_db)
    # update_previous_week([page["id"] for page in prev_week_db["results"]], type_mappings)

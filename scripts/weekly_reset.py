from typing import Dict, List
from datetime import datetime, timedelta

from utils.request_utils import query_database, update_page, add_page_to_database, map_reset_values


def get_previous_week():
    return query_database(database_key_name="NOTION_HABITS_DB_KEY")


def update_previous_week(pages_to_update: List[str], properties: Dict[str, str]):
    for num_of_days, page_id in enumerate(pages_to_update):
        date = (datetime.now() + timedelta(days=num_of_days)).strftime("%Y-%m-%d")
        reset_config = map_reset_values(date)
        data = {k: reset_config[properties[k]] for k in properties if properties[k] in reset_config}
        update_page(page_id, data)


def archive_past_week(pages: Dict):

    for page_data in [page["properties"] for page in pages["results"]]:
        add_page_to_database("NOTION_HABITS_ARCHIVE_DB_KEY", page_data)


if __name__ == '__main__':
    prev_week_db = get_previous_week()
    archive_past_week(prev_week_db)
    type_mappings = {
        prop: prev_week_db["results"][0]["properties"][prop]["type"]
        for prop in prev_week_db["results"][0]["properties"]
    }
    update_previous_week([page["id"] for page in prev_week_db["results"]], type_mappings)

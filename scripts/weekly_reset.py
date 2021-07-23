from typing import Dict, List
from datetime import datetime, timedelta

from utils.request_utils import query_database, update_page, add_page_to_database, map_reset_values, get_database


def create_new_pages_in_db(db_key_name: str, properties: Dict[str, str], num_of_entries: int = 1):
    for i in range(num_of_entries):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        reset_config = map_reset_values(date)
        data = {k: reset_config[properties[k]] for k in properties if properties[k] in reset_config}
        add_page_to_database(db_key_name, data)


if __name__ == '__main__':
    db_properties = get_database("NOTION_HABITS_DB_KEY")["properties"]
    db_properties = {k: db_properties[k]["type"] for k in db_properties}
    create_new_pages_in_db("NOTION_HABITS_DB_KEY", db_properties, 7)

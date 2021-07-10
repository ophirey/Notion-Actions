from typing import Dict, List
from datetime import datetime, timedelta

from utils.request_utils import query_database


def get_previous_week():
    return query_database(database_key_name="NOTION_HABITS_DB_KEY")


def update_previous_week(pages_to_update: List[str], properties: Dict[str, str]):
    reset_mapper = lambda iso_date: {
        "checkbox": {"checkbox": False},
        "rich_text": [{"text": {"content": ""}}],
        "date": {"date": {"start": iso_date}}
    }

    for num_of_days, page in enumerate(pages_to_update):
        date = (datetime.now() + timedelta(days=num_of_days)).isoformat()
        reset_config = reset_mapper(date)
        data = {
            "properties": {
                k: reset_config[properties[k]] for k in properties
            }
        }
        print(data)

if __name__ == '__main__':
    print(
        update_previous_week(
            ["1", "2", "3"],
            {
                "Date": "date",
                "Comments": "rich_text",
                "Habit #1": "checkbox",
                "Habit #2": "checkbox"
            }
        )
    )

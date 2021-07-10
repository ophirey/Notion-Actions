
from utils.request_utils import query_database


def get_previous_week():
    return query_database(database_key_name="NOTION_HABITS_DB_KEY")


if __name__ == '__main__':
    print(get_previous_week())

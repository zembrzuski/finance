from datetime import datetime


def parse_date_to_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d")

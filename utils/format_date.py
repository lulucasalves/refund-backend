from datetime import datetime


def format_date(date):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

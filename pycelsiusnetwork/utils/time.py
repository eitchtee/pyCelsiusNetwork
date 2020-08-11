import arrow


def convert_to_datetime(date: str):
    return arrow.get(date)

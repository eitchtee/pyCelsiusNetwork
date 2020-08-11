from ..exceptions import AbstractionFailure
from .time import convert_to_datetime


def get_key(key: str, json: dict, silent: bool):
    try:
        key = json[key]
    except KeyError:
        if silent:
            return None
        else:
            raise AbstractionFailure(json=json)
    else:
        return key


def filter_json(lst,
                dt_from = None,
                dt_to = None,
                amount_bigger_than = None,
                amount_lower_than = None,
                state = None,
                nature = None):

    dt_from = convert_to_datetime(dt_from) if dt_from else None
    dt_to = convert_to_datetime(dt_to) if dt_to else None
    result = lst

    if dt_from:
        result = [x for x in result if
                  convert_to_datetime(x['time']) >= dt_from]

    if dt_to:
        result = [x for x in result if
                  convert_to_datetime(x['time']) <= dt_to]

    if state:
        result = [x for x in result if
                  x['state'] == state]

    if nature:
        result = [x for x in result if
                  x['nature'] == nature]

    if amount_bigger_than:
        result = [x for x in result if
                  float(x['amount']) >= amount_bigger_than]

    if amount_lower_than:
        result = [x for x in result if
                  float(x['amount']) <= amount_lower_than]

    return result

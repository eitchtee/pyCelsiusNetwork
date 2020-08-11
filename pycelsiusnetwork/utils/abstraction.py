from ..exceptions import AbstractionFailure


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

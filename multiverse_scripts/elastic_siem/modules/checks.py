import json
import sys

def check_json(data):
    try:
        return json.loads(data)
    except:
        return False

def check_crud():
    if len(sys.argv) != 2:
        return False
    if sys.argv[1] not in [
        "create",
        "read",
        "update",
        "delete"]:
        return False

    return sys.argv[1]


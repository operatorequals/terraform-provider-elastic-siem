import sys
import json
import requests

from modules.checks import check_json, check_crud
from modules.utils import read_data
from modules.auth import KIBANA_URL, KIBANA_USERNAME, KIBANA_PASSWORD

URL = KIBANA_URL
BASIC_AUTH = (KIBANA_USERNAME, KIBANA_PASSWORD)
API = {
    "create" : {
        "endpoint" : "/api/exception_lists/items",
        "method" : "POST",
    },
    "read" : {
        "endpoint" : "/api/exception_lists/items",
        "method" : "GET",
    },
    "update" : {
        "endpoint" : "/api/exception_lists/items",
        "method" : "PUT",
    },
    "delete" : {
        "endpoint" : "/api/exception_lists/items",
        "method" : "DELETE",
    },
}

def handler(event, data):
    if event in ["read", "delete"]:
        """
        The READ call does ONLY need 'item_id'
        """
        data = {"item_id":data["item_id"]}
    elif event == "update":
        """
        The UPDATE call does not accept 'list_id'
        """
        del data["list_id"]


    response = requests.request(
        url=f'{URL}{API[event]["endpoint"]}',
        method=API[event]["method"],
        params=data if API[event]["method"] in ["GET","DELETE"] else None,
        json=data if not API[event]["method"] in ["GET","DELETE"] else None,
        auth=BASIC_AUTH,
        headers={
            'kbn-xsrf': 'monitoring'
        },
    )
    return response.json()
   
if __name__ == '__main__':
    data = read_data()
    context = check_json(data)
    if not context: raise ValueError(f"data block: '{data}' is not JSON")
    crud = check_crud()
    if not crud:
        print("""Usage:
    python3 -m elastic_siem [create|read|update|delete]
""")
        sys.exit(1)

    print(json.dumps(handler(sys.argv[1], context)))


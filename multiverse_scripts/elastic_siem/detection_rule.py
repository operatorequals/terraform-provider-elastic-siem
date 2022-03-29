import sys
import json
import requests

from modules.checks import check_json, check_yaml, check_toml, check_crud
from modules.utils import read_data
from modules.auth import KIBANA_URL, KIBANA_USERNAME, KIBANA_PASSWORD

URL = KIBANA_URL
BASIC_AUTH = (KIBANA_USERNAME, KIBANA_PASSWORD)
API = {
    "create" : {
        "endpoint" : "/api/detection_engine/rules",
        "method" : "POST",
    },
    "read" : {
        "endpoint" : "/api/detection_engine/rules",
        "method" : "GET",
    },
    "update" : {
        "endpoint" : "/api/detection_engine/rules",
        "method" : "PUT",
    },
    "delete" : {
        "endpoint" : "/api/detection_engine/rules",
        "method" : "DELETE",
    },
}

def handler(event, data):
    data=data['rule']
    if event in ["read", "delete"]:
        """
        The READ call does ONLY need 'item_id'
        """
        data = {"rule_id":data["rule_id"]}

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

    context = {}
    context.update(check_json(data))
    if not context:
        # JSON failed - try YAML
        context.update(check_yaml(data))
    if not context:
        # YAML failed - try TOML
        context.update(check_toml(data))
    if not context: raise ValueError(f"data block: '{data}' is not of supported format")

    crud = check_crud()
    if not crud: raise ValueError(f"No CRUD verb provided")

    print(json.dumps(handler(sys.argv[1], context)))


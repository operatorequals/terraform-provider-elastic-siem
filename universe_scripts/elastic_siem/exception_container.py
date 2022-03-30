import sys
import json
import requests

from modules.checks import check_json, check_yaml, check_toml, check_crud
from modules.utils import read_data, set_primary_id
from modules.auth import KIBANA_URL, KIBANA_USERNAME, KIBANA_PASSWORD

KEY_ID = 'list_id'
URL = KIBANA_URL
BASIC_AUTH = (KIBANA_USERNAME, KIBANA_PASSWORD)
API = {
    "create" : {
        "endpoint" : "/api/exception_lists",
        "method" : "POST",
    },
    "read" : {
        "endpoint" : "/api/exception_lists",
        "method" : "GET",
    },
    "update" : {
        "endpoint" : "/api/exception_lists",
        "method" : "PUT",
    },
    "delete" : {
        "endpoint" : "/api/exception_lists",
        "method" : "DELETE",
    },
}

def handler(event, data):
    if event == "exists": event = "read"
    if event in ["read", "delete"]:
        """
        The READ call does ONLY need 'list_id'
        """
        data = {"list_id":data["list_id"]}

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
    return response.status_code, response.json()
   
if __name__ == '__main__':
    data = read_data()

    crud = check_crud()
    if not crud: raise ValueError(f"No CRUD verb provided")
 
    context = {}
    context.update(check_json(data))
    if not context:
        # JSON failed - try YAML
        context.update(check_yaml(data))
    if not context:
        # YAML failed - try TOML
        context.update(check_toml(data))

    set_primary_id(KEY_ID, context)

    if not context: raise ValueError(f"data block: '{data}' is not of supported format for '{crud}'")

    response_code, output = handler(crud, context)

    if crud == 'exists':
        """
        The 'exists' argument does need a 'true/false' output
        """
        print('true' if 300 > response_code >= 200 else 'false')
    else:
        print(json.dumps(output))

    sys.exit(0)


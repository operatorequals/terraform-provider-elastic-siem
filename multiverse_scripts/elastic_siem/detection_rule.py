import sys
import os
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
    if event == "exists": event = "read"
    if event in ["read"]:
        """
        The READ call does ONLY need 'rule_id'
        """
        data = {"rule_id": data["rule_id"]}

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

    if 'rule' in context:
        """
        In case the schema is read from rules writen
        using the TOML format of 'github.com/elastic/detection-rules',
        the payload (as documented in the docs:
        https://www.elastic.co/guide/en/security/current/rules-api-create.html#_request_body)
        is wrapped in the 'rule' TOML directive.
        """
        context=context['rule']

    if 'rule_id' not in context:
        """
        In case the 'rule_id' is not populated through stdin
        (as with 'delete' - https://github.com/manasmbellani/terraform-provider-universe#output)
        it is retrieved through Environment Variable passed by Terraform
        """
        if 'rule_id' in os.environ:
            context['rule_id'] = os.environ['rule_id']

    if not context: raise ValueError(f"data block: '{data}' is not of supported format for '{crud}'")

    response_code, output = handler(crud, context)

    if crud == 'exists':
        """
        The 'exists' argument does need a 'true/false' output
        """
        print('true' if 300 > response_code >= 200 else 'false')
    else:
        print(json.dumps(output))

    sys.exit(0 if 300 > response_code >= 200 else 255)


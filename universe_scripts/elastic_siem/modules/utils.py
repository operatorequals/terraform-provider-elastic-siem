import sys
import os

def read_data():
    data = ''
    for line in sys.stdin:
        data += line

    return data

def set_primary_id(keyname, context):
    if keyname not in context:
        """
        In case the primary id is not populated through stdin
        (as with 'delete' - https://github.com/manasmbellani/terraform-provider-universe#output)
        it is retrieved through Environment Variable passed by Terraform
        """
        if keyname in os.environ:
            context[keyname] = os.environ[keyname]



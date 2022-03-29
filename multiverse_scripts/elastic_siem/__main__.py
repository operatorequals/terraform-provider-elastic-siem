import sys
import json

from elastic_siem.modules.checks import check_json
from elastic_siem.modules.utils import read_data

   
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


import sys
import json

def handler(event, data):
    if event == "create":
        pass
        
    elif event == "read":
        pass
        
    elif event == "update":
        pass
        
    elif event == "delete":
        pass
   
def read_data():
    data = ''
    for line in sys.stdin:
        data += line

    return data
   
if __name__ == '__main__':
    context = read_data()
    print(json.dumps(handler(sys.argv[1], context)))

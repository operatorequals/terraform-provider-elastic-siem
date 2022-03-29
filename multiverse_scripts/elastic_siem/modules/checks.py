import json
import sys

def check_toml(data):
    try:
        import toml
        return toml.loads(data)
    except ImportError:
        print("TOML not supported - use: 'pip install toml'")
    return {}

def check_yaml(data):
    try:
        import yaml
        return yaml.safe_load(data)
    except ImportError:
        print("YAML not supported - use: 'pip install PyYAML'")
    except yaml.parser.ParserError:
        return {}
    return {}

def check_json(data):
    try:
        return json.loads(data)
    except:
        return {}

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


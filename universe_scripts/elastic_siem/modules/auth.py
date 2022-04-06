"""
This submodule reads from Environment Variables
and populates the Globals below with Credentials
and Configuration

"""

import os

ELASTICSEARCH_URL = os.environ.get("ELASTICSEARCH_URL", "https://127.0.0.1:9200")
ELASTICSEARCH_USERNAME = os.environ.get("ELASTICSEARCH_USERNAME", "elastic")
ELASTICSEARCH_PASSWORD = os.environ.get("ELASTICSEARCH_PASSWORD", "")
ELASTICSEARCH_VERSION = os.environ.get("ELASTICSEARCH_VERSION", "latest")

KIBANA_URL = os.environ.get("KIBANA_URL", "https://127.0.0.1:5601")
KIBANA_USERNAME = os.environ.get("KIBANA_USERNAME", "")
KIBANA_PASSWORD = os.environ.get("KIBANA_PASSWORD", "")
KIBANA_VERSION = os.environ.get("KIBANA_VERSION", "latest")

KIBANA_ML_ENABLED = os.environ.get("KIBANA_ML_ENABLED", "true")

if not KIBANA_USERNAME:
    KIBANA_USERNAME = ELASTICSEARCH_USERNAME

if not not KIBANA_PASSWORD:
    KIBANA_PASSWORD = KIBANA_PASSWORD


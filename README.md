# terraform-provider-elastic-siem
----

A Terraform Provider for Elastic Detection Rules and Exceptions, powered by [Universe Terraform Provider](https://github.com/operatorequals/terraform-provider-universe)

## Install

To install this provider one needs to first install the [`universe-terraform-provider`](https://github.com/operatorequals/terraform-provider-universe#installing-the-provider), and then use the following `provider` blocks:

```hcl
terraform {
  required_version = ">= 0.13.0"
  required_providers {
    universe = {
      source = "github.com/operatorequals/universe"
      version = ">=0.1.0"
    }
  }
}

provider "universe" {
  alias = "detection_rule"
  environment = {
    KIBANA_URL = "..."
    KIBANA_USERNAME = "..."
    KIBANA_PASSWORD = "..."
  }
  executor = "python3"
  id_key   = "rule_id"
  script   = "universe_scripts/elastic_siem/detection_rule.py"
}

provider "universe" {
  alias = "exception_item"
  environment = {
    KIBANA_URL = "..."
    KIBANA_USERNAME = "..."
    KIBANA_PASSWORD = "..."
  }
  executor = "python3"
  id_key   = "item_id"
  script   = "universe_scripts/elastic_siem/exception_item.py"
}

provider "universe" {
  alias = "exception_container"
  environment = {
    KIBANA_URL = "..."
    KIBANA_USERNAME = "..."
    KIBANA_PASSWORD = "..."
  }
  executor = "python3"
  id_key   = "list_id"
  script   = "universe_scripts/elastic_siem/exception_container.py"
}
```

## Usage

An example `main.tf` that utilizes the Universe Provider:

```hcl
resource "universe" "non_working_hours" {
  provider = universe.detection_rule

  config   = file("rules/linux/credential_access_ssh_backdoor_log.toml") // [1]
}

resource "universe" "ldap_exception" {
  provider = universe.exception_container

  config   = file("sshd_weird_places.yaml") // [2]
}

resource "universe" "ldap_exception_item" {
  provider = universe.exception_item

  config   = file("sshd_in_usr_tmp.yaml") // [2]
}
```

[1] : A TOML file describing a rule, like the ones found in [`elastic/detection-rules`](https://github.com/elastic/detection-rules/blob/main/rules/linux/credential_access_ssh_backdoor_log.toml)
[2] : YAML files (or TOML files) that describe the Exception Container and Item as per the [Elastic Exceptions API](https://www.elastic.co/guide/en/security/current/exceptions-api-overview.html)

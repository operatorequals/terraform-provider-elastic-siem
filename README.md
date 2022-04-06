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

provider "universe" {
  alias = "list_item"
  environment = {
    KIBANA_URL = "..."
    KIBANA_USERNAME = "..."
    KIBANA_PASSWORD = "..."
  }
  executor = "python3"
  id_key   = "id"
  script   = "universe_scripts/elastic_siem/list_item.py"
}

provider "universe" {
  alias = "list_container"
  environment = {
    KIBANA_URL = "..."
    KIBANA_USERNAME = "..."
    KIBANA_PASSWORD = "..."
  }
  executor = "python3"
  id_key   = "id"
  script   = "universe_scripts/elastic_siem/list_container.py"
}
```

## Usage

An example `main.tf` that utilizes the Universe Provider:

```hcl
resource "universe" "credential_access_ssh_backdoor_log" {
  provider = universe.detection_rule

  config   = file("rules/linux/credential_access_ssh_backdoor_log.toml") // [1]
}

resource "universe" "ssh_exception" {
  provider = universe.exception_container

  config   = file("sshd_weird_places.yaml") // [2]
}

resource "universe" "ssh_exception_in_tmp" {
  provider = universe.exception_item

  config   = file("sshd_in_usr_tmp.yaml") // [2]
}

resource "universe" "internal_ips" {
  provider = universe.list_container

  // [3]
  config   =<< LIST
id: "list_1"

description: |
  The IPs that are considered Internal and should be excepted
from Exfiltration Rules
name: "ips"
type: "ip_range"
LIST
}

resource "universe" "internal_ip_1" {
  provider = universe.list_container

  // [3]
  config   =<< LIST_ITEM
id: list_item_1
list_id: list_1

value: 10.10.10.0/24
LIST_ITEM
}
```

[1] : A TOML file describing a rule, like the ones found in [`elastic/detection-rules`](https://github.com/elastic/detection-rules/blob/main/rules/linux/credential_access_ssh_backdoor_log.toml)

[2] : YAML files (or TOML files) that describe the Exception Container and Item as per the [Elastic Exceptions API](https://www.elastic.co/guide/en/security/current/exceptions-api-overview.html)

[3] : YAML files (or TOML files), that describe List and List Items as per the [Elastic Lists API](https://www.elastic.co/guide/en/security/7.16/lists-api-overview.html)

## Integration with  [`elastic/detection-rules`](https://github.com/elastic/detection-rules)

To use the original Elastic Ruleset with `terraform-provider-elastic-siem`, one needs to:

* Install Terraform Universe Provider
* Clone this Repository
* In this Repository clone [`elastic/detection-rules`](https://github.com/elastic/detection-rules)
* Use the below Terraform file:

`main.tf`

```hcl
# ================= Provider Setup
provider "universe" {
  alias = "detection_rule"
  environment = {
/* The below Environment Variables need to be defined before execution,
or in this block:
    KIBANA_USERNAME = "elastic"              // <-- Default value
    KIBANA_PASSWORD = ""                     // <-- Default value
    KIBANA_URL      = "https:127.0.0.1:5601" // <-- Default value
*/
  }
  executor = "python3"
/*
The Container Image (see below) locates the Provider's scripts
under root directory:
  script   = "/universe_scripts/elastic_siem/detection_rule.py"

Use the above when running in the container.
*/
  script   = "universe_scripts/elastic_siem/detection_rule.py"
  id_key   = "rule_id"
}

# ================= Rule Loading
locals{
  rule_dir = "${path.module}/rules"
}

/*
This Terraform Resource monitors all TOML rules for
changes.
*/
resource "universe" "rules" {
  provider = universe.detection_rule
  for_each = fileset(local.rule_dir, "**/**.toml")

  config   =<<CONFIG
${file("${local.rule_dir}/${each.key}")}

# The TOML can be furtherly modified here
# for addition of Exceptions and Lists
CONFIG
}
```

## Usage as Container

Build and Run the container from the repository.
```bash
$ docker build . -t terraform-provider-elastic-siem
$ docker run -ti --entrypoint sh terraform-provider-elastic-siem
```

Use it with the above `main.tf`:
```bash
$ docker run -v `pwd`:/opt/src/ \
                --entrypoint sh \
                -e KIBANA_USERNAME=<username> \
                -e KIBANA_PASSWORD=<password> \
                -e KIBANA_URL=<url> \
 -ti ghcr.io/operatorequals/terraform-provider-elastic-siem:master

/opt/src# terraform init
/opt/src# terraform apply
```


## Why?

As I have been working with Elastic SIEM and its Ruleset for a good while, I needed to have my Rules and their Exceptions trackable by Git
and deployable.

While I tried to use the `detection_rules` CLI tool, it was impossible to work with it in a Automated Pipeline as it [cannot *overwrite* a rule](https://github.com/elastic/detection-rules/issues/612).
Additionally, the tool could not upload exceptions, as it does not consume the
[Exceptions API](https://www.elastic.co/guide/en/security/current/exceptions-api-overview.html).

So I created a Terraform Provider for Rules and Exceptions, that is compatible with the `elastic/detection_rules` repo, as it is the primary source of the Elastic Ruleset.


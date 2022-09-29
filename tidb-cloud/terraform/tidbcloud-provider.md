---
title: Get TiDB Cloud Provider
summary: Learn how to get TiDB Cloud provider
---

# Get TiDB Cloud Provider

> **Note:**
>
> Make sure meet the requirements in [overview](/tidb-cloud/terraform/terraform-overview.md)

## Set up terraform

TiDB Cloud provider has released to terraform registry. All you need to do is install terraform (>=1.0).

For Mac user, you can install it with Homebrew.

First, install the HashiCorp tap, a repository of all our Homebrew packages.

```shell
brew tap hashicorp/tap
```

Now, install Terraform with hashicorp/tap/terraform.

```shell
brew install hashicorp/tap/terraform
```

See [terraform doc](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/aws-get-started) for other installation methods.

## Create an API key

The TiDB Cloud API uses HTTP Digest Authentication. It protects your private key from being sent over the network.

However, terraform-provider-tidbcloud does not support managing API key now. So you need to create the API key in the [console](https://tidbcloud.com/console/clusters).

Turn to [TiDB Cloud API doc](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management) for help if you meet any problems.

## Get TiDB Cloud provider

Create a main.tf file:

```
terraform {
  required_providers {
    tidbcloud = {
      source = "tidbcloud/tidbcloud"
      version = "~> 0.0.1"
    }
  }
  required_version = ">= 1.0.0"
}
```

- The `source` attribute defines the provider which will be downloaded from [Terraform Registry](https://registry.terraform.io/) by default
- The `version` attribute is optional which defines the version of the provider, it will use the latest version by default
- The `required_version` is optional which defines the version of the terraform, it will use the latest version by default

To get the TiDB Cloud provider, execute `terraform init`. It will download the provider from terraform registry.

```
$ terraform init

Initializing the backend...

Initializing provider plugins...
- Reusing previous version of tidbcloud/tidbcloud from the dependency lock file
- Using previously-installed tidbcloud/tidbcloud v0.0.1

Terraform has been successfully initialized!

You may now begin working with Terraform. Try running "terraform plan" to see
any changes that are required for your infrastructure. All Terraform commands
should now work.

If you ever set or change modules or backend configuration for Terraform,
rerun this command to reinitialize your working directory. If you forget, other
commands will detect it and remind you to do so if necessary.
```

## Configure the provider with API Key

You need to configure the provider like:

```
terraform {
  required_providers {
    tidbcloud = {
      source = "tidbcloud/tidbcloud"
      version = "~> 0.0.1"
    }
  }
  required_version = ">= 1.0.0"
}

provider "tidbcloud" {
  username = "fake_username"
  password = "fake_password"
}
```

username and password are the API key's public key and private key, you can also pass them with the environment:

```
export TIDBCLOUD_USERNAME = ${public_key}
export TIDBCLOUD_PASSWORD = ${private_key}
```

Now, you can use the TiDB Cloud provider. 

> Next, you can manage the cluster with [cluster resource](/tidb-cloud/terraform/cluster-resource.md)
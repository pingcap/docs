---
title: Get TiDB Cloud Terraform Provider
summary: Learn how to get TiDB Cloud Terraform Provider
---

# Get TiDB Cloud Terraform Provider

You will learn how to get TiDB Cloud Terraform Provider in this document.

## Prerequisites

Before you begin, make sure that the requirements in [TiDB Cloud Terraform Provider Overview](/tidb-cloud/terraform/terraform-overview.md) are met.

## Step 1. Install terraform

TiDB Cloud Terraform Provider has been released to [Terraform registry](https://registry.terraform.io/). All you need to do is install Terraform (>=1.0).

For Mac users, you can install Terraform with Homebrew.

1. Install the HashiCorp tap, a repository with all the required Homebrew packages.

    ```shell
    brew tap hashicorp/tap
    ```

2. Install Terraform with hashicorp/tap/terraform.

    ```shell
    brew install hashicorp/tap/terraform
    ```

For other operating systems, see [Terraform documentation](https://learn.hashicorp.com/tutorials/terraform/install-cli) for instructions.

## Step 2. Create an API key

The TiDB Cloud API uses HTTP Digest Authentication. It protects your private key from being sent over the network.

Currently, TiDB Cloud Terraform Provider does not support managing API keys. So you need to create an API key in the [TiDB Cloud console](https://tidbcloud.com/console/clusters).

For detailed steps, see [TiDB Cloud API documentation](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management).

## Step 3. Download TiDB Cloud Terraform Provider

1. Create a main.tf file:

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

   - The `source` attribute specifies the target Terraform provider to be downloaded from [Terraform Registry](https://registry.terraform.io/).
   - The `version` attribute is optional, which specifies the version of the provider. If it is not specified, the latest provider version is used by default.
   - The `required_version` is optional, which specifies the version of Terraform. If  it is not specified, the latest Terraform version is used by default.

2. To get the TiDB Cloud Terraform Provider, run the `terraform init` command. It will download the provider from the Terraform registry.

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

## Step 4. Configure TiDB Cloud Terraform Provider with the API Key

You can configure the provider as follows:

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

`username` and `password` are the API key's public key and private key. You can also pass them with the environment variables:

```
export TIDBCLOUD_USERNAME = ${public_key}
export TIDBCLOUD_PASSWORD = ${private_key}
```

Now, you can use the TiDB Cloud Terraform Provider. You can get started by managing a cluster with [cluster resource](/tidb-cloud/terraform/cluster-resource.md).
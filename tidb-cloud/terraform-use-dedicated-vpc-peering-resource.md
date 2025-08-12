---
title: Use TiDB Cloud Dedicated VPC Peering Resource
summary: Learn how to use the TiDB Cloud Dedicated VPC peering resource to create and modify a TiDB Cloud Dedicated VPC peering.
---

# Use TiDB Cloud Dedicated VPC Peering Resource

This document describes how to manage a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) VPC peering with the `tidbcloud_dedicated_vpc_peering` resource.

The features of the `tidbcloud_dedicated_vpc_peering` resource include the following:

- Create TiDB Cloud Dedicated VPC peering.
- Import TiDB Cloud Dedicated VPC peering.
- Delete TiDB Cloud Dedicated VPC peering.

> **Note:**
>
> TiDB Cloud Dedicated VPC peering resource cannot be modified. If you want to change the configuration of a TiDB Cloud Dedicated VPC peering, you need to delete the existing one, and then create a new one.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.

## Create a TiDB Cloud Dedicated VPC peering

You can create a TiDB Cloud Dedicated VPC peering using the `tidbcloud_dedicated_vpc_peering` resource.

The following example shows how to create a TiDB Cloud Dedicated VPC peering.

1. Create a directory for the TiDB Cloud Dedicated VPC peering and enter it.

2. Create a `vpc_peering.tf` file:

    ```
    terraform {
      required_providers {
        tidbcloud = {
          source = "tidbcloud/tidbcloud"
        }
      }
    }

    provider "tidbcloud" {
      public_key = "your_public_key"
      private_key = "your_private_key"
    }

    resource "tidbcloud_dedicated_vpc_peering" "example" {
      tidb_cloud_region_id = "your_tidb_cloud_region_id"
      customer_region_id   = "your_customer_region_id"
      customer_account_id  = "your_customer_account_id"
      customer_vpc_id      = "your_customer_vpc_id"
      customer_vpc_cidr    = "your_customer_vpc_cidr"
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the TiDB Cloud Dedicated VPC peering resource, set the resource type as `tidbcloud_dedicated_vpc_peering`.
    - For the resource name, you can define it as needed. For example, `example`.
    - If you do not know how to get the values of the required arguments, see [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md).
    - To get the TiDB Cloud Dedicated VPC peering specification information, see [tidbcloud_dedicated_vpc_peering (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_vpc_peering).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
        + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_vpc_peering.example will be created
        + resource "tidbcloud_dedicated_vpc_peering" "example" {
            + aws_vpc_peering_connection_id = (known after apply)
            + customer_account_id           = "986330900000"
            + customer_region_id            = "aws-us-west-2"
            + customer_vpc_cidr             = "172.16.32.0/21"
            + customer_vpc_id               = "vpc-0c0c7d59702000000"
            + labels                        = (known after apply)
            + project_id                    = (known after apply)
            + state                         = (known after apply)
            + tidb_cloud_account_id         = (known after apply)
            + tidb_cloud_cloud_provider     = (known after apply)
            + tidb_cloud_region_id          = "aws-us-west-2"
            + tidb_cloud_vpc_cidr           = (known after apply)
            + tidb_cloud_vpc_id             = (known after apply)
            + vpc_peering_id                = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    In the preceding result, Terraform generates an execution plan for you, which describes the actions Terraform will take:

    - You can check the differences between the configurations and the states.
    - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
    - `known after apply` indicates that you will get the corresponding value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_vpc_peering.example: Creating...
    tidbcloud_dedicated_vpc_peering.example: Still creating... [10s elapsed]
    ```

    The status of the resource will remain `Creating` until you approve the VPC peering connection in your cloud provider console. After you approve the VPC peering connection, you can take [Approve and Configure the VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md#step-2-approve-and-configure-the-vpc-peering) as a reference, the status will change to `Active`.

5. Use the `terraform show` or `terraform state show tidbcloud_dedicated_vpc_peering.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_dedicated_vpc_peering.example
    # tidbcloud_dedicated_vpc_peering.example:
    resource "tidbcloud_dedicated_vpc_peering" "example" {
        aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000"
        customer_account_id           = "986330900000"
        customer_region_id            = "aws-us-west-2"
        customer_vpc_cidr             = "172.16.32.0/21"
        customer_vpc_id               = "vpc-0c0c7d59702000000"
        labels                        = {
            "tidb.cloud/project" = "1372813089187000000"
        }
        project_id                    = "13728130891870000000"
        state                         = "ACTIVE"
        tidb_cloud_account_id         = "380838400000"
        tidb_cloud_cloud_provider     = "aws"
        tidb_cloud_region_id          = "aws-us-west-2"
        tidb_cloud_vpc_cidr           = "10.250.0.0/16"
        tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000"
        vpc_peering_id                = "aws-1934187953894000000"
    }
    ```

## Import a TiDB Cloud Dedicated VPC peering

For a TiDB Cloud Dedicated VPC peering that is not managed by Terraform, you can use Terraform to manage it just by importing it.

For example, you can import a VPC peering that is not created by Terraform.

1. Add an import block for the new TiDB Cloud Dedicated VPC peering resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,vpc_peering_id`:

    ```
    import {
      to = tidbcloud_dedicated_vpc_peering.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new TiDB Cloud Dedicated VPC peering resource according to the import block:

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    Do not specify an existing `.tf` filename in the preceding command. Otherwise, Terraform will return an error.

    Then the `generated.tf` file is created in the current directory, which contains the configuration of the imported resource.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_dedicated_vpc_peering.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_vpc_peering.example: Import complete [id=aws-19341879538940000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported TiDB Cloud Dedicated VPC peering with Terraform.

## Delete a TiDB Cloud Dedicated VPC peering

To delete a TiDB Cloud Dedicated VPC peering, you can delete the configuration of the `tidbcloud_dedicated_vpc_peering` resource, and then use the `terraform apply` command to destroy the resource:

```shell
  $ terraform apply
  tidbcloud_dedicated_vpc_peering.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

  Terraform will perform the following actions:

  # tidbcloud_dedicated_vpc_peering.example will be destroyed
  # (because tidbcloud_dedicated_vpc_peering.example is not in configuration)
  - resource "tidbcloud_dedicated_vpc_peering" "example" {
      - aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000" -> null
      - customer_account_id           = "986330900000" -> null
      - customer_region_id            = "aws-us-west-2" -> null
      - customer_vpc_cidr             = "172.16.32.0/21" -> null
      - customer_vpc_id               = "vpc-0c0c7d59702000000" -> null
      - labels                        = {
          - "tidb.cloud/project" = "1372813089187000000"
          } -> null
      - project_id                    = "1372813089187000000" -> null
      - state                         = "ACTIVE" -> null
      - tidb_cloud_account_id         = "380838000000" -> null
      - tidb_cloud_cloud_provider     = "aws" -> null
      - tidb_cloud_region_id          = "aws-us-west-2" -> null
      - tidb_cloud_vpc_cidr           = "10.250.0.0/16" -> null
      - tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000" -> null
      - vpc_peering_id                = "aws-1934187953894000000" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

  tidbcloud_dedicated_vpc_peering.example: Destroying...
  tidbcloud_dedicated_vpc_peering.example: Destruction complete after 1s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

Now, if you run the `terraform show` command, you will get nothing because the resource has been cleared:

```
$ terraform show
```

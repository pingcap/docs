---
title: Use TiDB Cloud Serverless Branch Resource
summary: Learn how to use the serverless branch resource to create and modify a TiDB Cloud Serverless branch.
---

# Use TiDB Cloud Serverless Branch Resource

This document describes how to manage a [TiDB Cloud Serverless branch](/tidb-cloud/branch-manage.md) using the `tidbcloud_serverless_branch` resource.

The features of the `tidbcloud_serverless_branch` resource include the following:

- Create TiDB Cloud Serverless branches.
- Import TiDB Cloud Serverless branches.
- Delete TiDB Cloud Serverless branches.

> **Note:**
>
> TiDB Cloud Serverless branch resource cannot be modified. If you want to change the configuration of a serverless branch resource, you need to delete the existing one and create a new one.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.
- [Create a TiDB Cloud Serverless cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

## Create a TiDB Cloud Serverless branch

You can create a TiDB Cloud Serverless branch using the `tidbcloud_serverless_branch` resource.

The following example shows how to create a TiDB Cloud Serverless branch.

1. Create a directory for the branch and enter it.

2. Create a `branch.tf` file:

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

    resource "tidbcloud_serverless_branch" "example" {
      cluster_id   = 10581524018573000000
      display_name = "example"
      parent_id = 10581524018573000000
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the serverless branch resource, set the resource type as `tidbcloud_serverless_branch`.
    - For the resource name, you can define it as needed. For example, `example`.
    - For the resource details, you can configure them according to the serverless branch specification information.
    - To get the serverless branch specification information, see [tidbcloud_serverless_branch (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_branch).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_serverless_branch.example will be created
      + resource "tidbcloud_serverless_branch" "example" {
          + annotations         = (known after apply)
          + branch_id           = (known after apply)
          + cluster_id          = "10581524018573000000"
          + create_time         = (known after apply)
          + created_by          = (known after apply)
          + display_name        = "example"
          + endpoints           = (known after apply)
          + parent_display_name = (known after apply)
          + parent_id           = "10581524018573000000"
          + parent_timestamp    = (known after apply)
          + state               = (known after apply)
          + update_time         = (known after apply)
          + user_prefix         = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    In the preceding result, Terraform generates an execution plan for you, which describes the actions that Terraform will take:

    - You can check the differences between the configurations and the states.
    - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
    - `known after apply` indicates that you will get the corresponding value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_branch.example: Creating...
    tidbcloud_serverless_branch.example: Still creating... [10s elapsed]
    tidbcloud_serverless_branch.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. Use the `terraform show` or `terraform state show tidbcloud_serverless_branch.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_serverless_branch.example 
    # tidbcloud_serverless_branch.example:
    resource "tidbcloud_serverless_branch" "example" {
        annotations         = {
            "tidb.cloud/has-set-password" = "false"
        }
        branch_id           = "bran-qt3fij6jufcf5pluot5h000000"
        cluster_id          = "10581524018573000000"
        create_time         = "2025-06-16T07:55:51Z"
        created_by          = "apikey-S2000000"
        display_name        = "example"
        endpoints           = {
            private = {
                aws  = {
                    availability_zone = [
                        "use1-az6",
                    ]
                    service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
                }
                host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
                port = 4000
            }
            public  = {
                disabled = false
                host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
                port     = 4000
            }
        }
        parent_display_name = "test-tf"
        parent_id           = "10581524018573000000"
        parent_timestamp    = "2025-06-16T07:55:51Z"
        state               = "ACTIVE"
        update_time         = "2025-06-16T07:56:49Z"
        user_prefix         = "4ER5SbndR000000"
    }
    ```

## Import a TiDB Cloud Serverless branch

For a TiDB Cloud Serverless branch that is not managed by Terraform, you can use Terraform to manage it just by importing it.

Import a TiDB Cloud Serverless branch that is not created by Terraform as follows:

1. Add an import block for the new TiDB Cloud Serverless branch resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,branch_id`:

    ```
    import {
      to = tidbcloud_serverless_branch.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new TiDB Cloud Serverless branch resource according to the import block:

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    Do not specify an existing `.tf` filename in the preceding command. Otherwise, Terraform will return an error.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_serverless_branch.example: Importing... 
    tidbcloud_serverless_branch.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported branch with Terraform.

## Delete a TiDB Cloud Serverless branch

To delete a TiDB Cloud Serverless branch, you can delete the configuration of the `tidbcloud_serverless_branch` resource, then use the `terraform apply` command to destroy the resource:

```shell
$ terraform apply
tidbcloud_serverless_branch.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_branch.example will be destroyed
  # (because tidbcloud_serverless_branch.example is not in configuration)
  - resource "tidbcloud_serverless_branch" "example" {
      - annotations         = {
          - "tidb.cloud/has-set-password" = "false"
        } -> null
      - branch_id           = "bran-qt3fij6jufcf5pluot5h000000" -> null
      - cluster_id          = "10581524018573000000" -> null
      - create_time         = "2025-06-16T07:55:51Z" -> null
      - created_by          = "apikey-S2000000" -> null
      - display_name        = "example" -> null
      - endpoints           = {
          - private = {
              - aws  = {
                  - availability_zone = [
                      - "use1-az6",
                    ] -> null
                  - service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000" -> null
                } -> null
              - host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com" -> null
              - port = 4000 -> null
            } -> null
          - public  = {
              - disabled = false -> null
              - host     = "gateway01.us-east-1.prod.aws.tidbcloud.com" -> null
              - port     = 4000 -> null
            } -> null
        } -> null
      - parent_display_name = "test-tf" -> null
      - parent_id           = "10581524018573000000" -> null
      - parent_timestamp    = "2025-06-16T07:55:51Z" -> null
      - state               = "ACTIVE" -> null
      - update_time         = "2025-06-16T07:56:49Z" -> null
      - user_prefix         = "4ER5SbndR000000" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_branch.example: Destroying...
tidbcloud_serverless_branch.example: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

Now, if you run the `terraform show` command, it will show no managed resources because the resource has been cleared:

```
$ terraform show
```

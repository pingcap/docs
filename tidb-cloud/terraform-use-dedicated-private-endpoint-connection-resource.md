---
title: Use Dedicated private endpoint connection Resource
summary: Learn how to use the dedicated private endpoint connection resource to create and modify a TiDB Cloud dedicated private endpoint connection.
---

# Use Dedicated Private Endpoint Connection Resource

You can learn how to manage a TiDB Cloud dedicated private endpoint connection with the `tidbcloud_dedicated_private_endpoint_connection` resource in this document.

The features of the `tidbcloud_dedicated_private_endpoint_connection` resource include the following:

- Create TiDB Cloud Dedicated private endpoint connection.
- Import TiDB Cloud Dedicated private endpoint connection.
- Delete TiDB Cloud Dedicated private endpoint connection.

> **Note:**
>
> TiDB Cloud Dedicated Private Endpoint Connection resource can not be modified. If you want to modify a dedicated private endpoint connection, you need to delete the existing one and create a new one.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.
- Create a TiDB Cloud Dedicated cluster. For more information, see [Create a TiDB Cloud Dedicated Cluster](/tidb-cloud/terraform-use-dedicated-cluster-resource.md).

## Create a dedicated private endpoint connection using the dedicated private endpoint connection resource

You can create a dedicated private endpoint connection using the `tidbcloud_dedicated_private_endpoint_connection` resource.

The following example shows how to create a TiDB Cloud dedicated private endpoint connection.

1. Create a directory for the dedicated private endpoint connection and enter it.

2. Create a `private_endpoint_connection.tf` file:
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

    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
      cluster_id = "your_cluster_id"
      node_group_id = "your_node_group_id"
      endpoint_id = "your_endpoint_id"
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the dedicated private endpoint connection resource, set the resource type as `tidbcloud_dedicated_dedicated_private_endpoint_connection`.
    - For the resource name, you can define it according to your need. For example, `example`.
    - If you don't know how to get the values of the required arguments, see [Connect to a TiDB Cloud Dedicated Cluster via Private Endpoint with AWS](/tidb-cloud/set-up-private-endpoint-connections.md).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_private_endpoint_connection.example will be created
        + resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
            + account_id                     = (known after apply)
            + cloud_provider                 = (known after apply)
            + cluster_display_name           = (known after apply)
            + cluster_id                     = "10757937805044000000"
            + endpoint_id                    = "vpce-03367e9618000000"
            + endpoint_state                 = (known after apply)
            + host                           = (known after apply)
            + labels                         = (known after apply)
            + message                        = (known after apply)
            + node_group_id                  = "1934178998036000000"
            + port                           = (known after apply)
            + private_endpoint_connection_id = (known after apply)
            + private_link_service_name      = (known after apply)
            + region_display_name            = (known after apply)
            + region_id                      = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

   As in the above result, Terraform generates an execution plan for you, which describes the actions Terraform will take:

   - You can check the difference between the configurations and the states.
   - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
   - The `known after apply` shows that you will get the value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_private_endpoint_connection.example: Creating...
    tidbcloud_dedicated_private_endpoint_connection.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5. Use the `terraform show` or `terraform state show tidbcloud_dedicated_private_endpoint.${resource-name}` command to inspect the state of your resource. The former will show the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_dedicated_private_endpoint_connection.example
    # tidbcloud_dedicated_private_endpoint_connection.example:
    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
        cloud_provider                 = "aws"
        cluster_display_name           = "test-tf"
        cluster_id                     = "10757937805044000000"
        endpoint_id                    = "vpce-03367e96180000000"
        endpoint_state                 = "ACTIVE"
        host                           = "privatelink-19341000.ubkypd000000.clusters.tidb-cloud.com"
        labels                         = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist"
        node_group_id                  = "1934178998036000000"
        port                           = 4000
        private_endpoint_connection_id = "1934214559409000000"
        private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000"
        region_display_name            = "Oregon (us-west-2)"
        region_id                      = "aws-us-west-2"
    }
    ```

## Import a Dedicated private endpoint connection

For a TiDB Cloud dedicated private endpoint connection that is not managed by Terraform, you can use Terraform to manage it just by importing it.

For example, you can import a private endpoint connection that is not created by Terraform.

1. Add an import block for the new dedicated private endpoint connection resource

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,dedicated_private_endpoint_connection_id`:

    ```
    import {
      to = tidbcloud_sql_user.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file

Generate the new configuration file for the new dedicated private endpoint connection resource according to the import block:

  ```shell
  terraform plan -generate-config-out=generated.tf
  ```

Do not specify an existing `.tf` file name in the preceding command. Otherwise, Terraform will return an error.

Then the `generated.tf` file is created in the current directory, which contains the configuration of the imported resource.

3. Review and apply the generated configuration

Review the generated configuration file to ensure it meets your needs. Optionally, you can move the contents of this file to your preferred location.

Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

  ```shell
  tidbcloud_dedicated_private_endpoint_connection.example: Importing... [id=aws-1934187953894000000,example]
  tidbcloud_dedicated_private_endpoint_connection.example: Import complete [id=aws-19341879538940000000,example]

  Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
  ```

Now you can manage the imported dedicated private endpoint connection with Terraform.

## Delete a Dedicated private endpoint connection

To delete a dedicated private endpoint connection, you can delete the configuration of the `tidbcloud_dedicated_private_endpoint_connection` resource, then use the `terraform apply` command to destroy the resource:
  ```shell
    $ terraform apply
    tidbcloud_dedicated_private_endpoint_connection.example: Refreshing state...

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

    Terraform will perform the following actions:

    # tidbcloud_dedicated_private_endpoint_connection.example will be destroyed
    # (because tidbcloud_dedicated_private_endpoint_connection.example is not in configuration)
    - resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
        - cloud_provider                 = "aws" -> null
        - cluster_display_name           = "test-tf" -> null
        - cluster_id                     = "10757937805044000000" -> null
        - endpoint_id                    = "vpce-03367e96180000000" -> null
        - endpoint_state                 = "ACTIVE" -> null
        - host                           = "privatelink-19341000.ubkypd1sx000.clusters.tidb-cloud.com" -> null
        - labels                         = {
            - "tidb.cloud/project" = "1372813089454000000"
            } -> null
        - message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist" -> null
        - node_group_id                  = "1934178998036000000" -> null
        - port                           = 4000 -> null
        - private_endpoint_connection_id = "1934214559409000000" -> null
        - private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000" -> null
        - region_display_name            = "Oregon (us-west-2)" -> null
        - region_id                      = "aws-us-west-2" -> null
        }

    Plan: 0 to add, 0 to change, 1 to destroy.

    Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

    tidbcloud_dedicated_private_endpoint_connection.example: Destroying...
    tidbcloud_dedicated_private_endpoint_connection.example: Destruction complete after 1s

    Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
  ```
Now, if you run the `terraform show` command, you will get nothing because the resource has been cleared:

```
$ terraform show
```
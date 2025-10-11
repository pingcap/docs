---
title: Use TiDB Cloud Dedicated Network Container Resource
summary: Learn how to use the TiDB Cloud Dedicated network container resource to create and modify a TiDB Cloud Dedicated network container.
---

# Use TiDB Cloud Dedicated Network Container Resource

This document describes how to manage a [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) network container using the `tidbcloud_dedicated_network_container` resource.

A network container is a logical networking resource that lets you define and manage a CIDR block (IP address range) for a specific project and region. This CIDR block is used for creating a VPC for TiDB Cloud Dedicated clusters and is required before setting up VPC peering in that region.

Before adding VPC peering requests to a region, you must first set a CIDR block for that region and create an initial TiDB Cloud Dedicated cluster. Once the first cluster is created, TiDB Cloud automatically creates the associated VPC, enabling you to establish a peering connection with your application's VPC.

The features of the `tidbcloud_dedicated_network_container` resource include the following:

- Create TiDB Cloud Dedicated network containers.
- Import TiDB Cloud Dedicated network containers.
- Delete TiDB Cloud Dedicated network containers.

> **Note:**
>
> TiDB Cloud Dedicated network containers cannot be modified or deleted if the status is `ACTIVE`. Make sure that the configuration of the `tidbcloud_network_container` resource is correct before you apply it.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.

## Create a TiDB Cloud Dedicated network container

You can create a TiDB Cloud Dedicated network container using the `tidbcloud_dedicated_network_container` resource.

The following example shows how to create a TiDB Cloud Dedicated network container.

1. Create a directory for the TiDB Cloud Dedicated network container and enter it.

2. Create a `network_container.tf` file:

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

    resource "tidbcloud_dedicated_network_container" "example" {
      project_id = "1372813089454000000"
      region_id = "aws-ap-northeast-2"
      cidr_notation = "172.16.16.0/21"
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the TiDB Cloud Dedicated network container resource, set the resource type as `tidbcloud_dedicated_network_container`.
    - For the resource name, you can define it as needed, for example, `example`.
    - If you do not know how to get the values of the required arguments, see [Set a CIDR for a Region](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region).
    - For more information about the TiDB Cloud Dedicated network container specification, see [tidbcloud_dedicated_network_container (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_network_container).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_network_container.example will be created
        + resource "tidbcloud_dedicated_network_container" "example" {
            + cidr_notation        = "172.16.16.0/21"
            + cloud_provider       = (known after apply)
            + labels               = (known after apply)
            + network_container_id = (known after apply)
            + project_id           = "1372813089454543324"
            + region_display_name  = (known after apply)
            + region_id            = "aws-ap-northeast-2"
            + state                = (known after apply)
            + vpc_id               = (known after apply)
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

    tidbcloud_dedicated_network_container.example: Creating...
    tidbcloud_dedicated_network_container.example: Creation complete after 4s
    ```

    The status of the resource will remain `INACTIVE` until you create a TiDB Cloud Dedicated cluster in the region of the TiDB Cloud Dedicated network container. Then, the status will change to `ACTIVE`.

5. Use the `terraform show` or `terraform state show tidbcloud_dedicated_network_container.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_dedicated_network_container.example          
    # tidbcloud_dedicated_network_container.example:
    resource "tidbcloud_dedicated_network_container" "example" {
        cidr_notation        = "172.16.16.0/21"
        cloud_provider       = "aws"
        labels               = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        network_container_id = "1934235512696000000"
        project_id           = "1372813089454000000"
        region_display_name  = "Seoul (ap-northeast-2)"
        region_id            = "aws-ap-northeast-2"
        state                = "INACTIVE"
        vpc_id               = null
    }
    ```

## Import a TiDB Cloud Dedicated network container

For a TiDB Cloud Dedicated network container that is not managed by Terraform, you can use Terraform to manage it just by importing it.

For example, you can import a network container that is not created by Terraform.

1. Add an import block for the new TiDB Cloud Dedicated network container resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,network_container_id`:

    ```
    import {
      to = tidbcloud_dedicated_network_container.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new TiDB Cloud Dedicated network container resource according to the import block:

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    Do not specify an existing `.tf` filename in the preceding command. Otherwise, Terraform will return an error.

    Then the `generated.tf` file is created in the current directory, which contains the configuration of the imported resource.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_dedicated_network_container.example: Importing... [id=10423692645683000000,example]
    tidbcloud_dedicated_network_container.example: Import complete [id=10423692645683000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported TiDB Cloud Dedicated network container with Terraform.

## Delete a TiDB Cloud Dedicated network container

To delete a TiDB Cloud Dedicated cluster, you can delete the configuration of the `tidbcloud_dedicated_cluster` resource, then use the `terraform apply` command to destroy the resource. However, you must ensure that the status of the TiDB Cloud Dedicated network container is not `ACTIVE`. If it is `ACTIVE`, you cannot delete it.

If the status is `INACTIVE`, you can delete it by running the following command:

```shell
  $ terraform apply
  tidbcloud_dedicated_network_container.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_dedicated_network_container.example will be destroyed
    # (because tidbcloud_dedicated_network_container.example is not in configuration)
    - resource "tidbcloud_dedicated_network_container" "example" {
        - cidr_notation        = "172.16.16.0/21" -> null
        - cloud_provider       = "aws" -> null
        - labels               = {
            - "tidb.cloud/project" = "1372813089454000000"
          } -> null
        - network_container_id = "1934235512696000000" -> null
        - project_id           = "1372813089454000000" -> null
        - region_display_name  = "Seoul (ap-northeast-2)" -> null
        - region_id            = "aws-ap-northeast-2" -> null
        - state                = "INACTIVE" -> null
          # (1 unchanged attribute hidden)
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_dedicated_network_container.example: Destroying...
  tidbcloud_dedicated_network_container.example: Destruction complete after 2s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

Now, if you run the `terraform show` command, it will show no managed resources because the resource has been cleared:

```
$ terraform show
```

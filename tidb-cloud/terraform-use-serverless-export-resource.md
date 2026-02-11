---
title: Use `tidbcloud_serverless_export` Resource
summary: Learn how to use the `tidbcloud_serverless_export` resource to create and modify data export tasks for {{{ .starter }}} or {{{ .essential }}} clusters.
---

# Use `tidbcloud_serverless_export` Resource

This document describes how to manage data export tasks for {{{ .starter }}} or {{{ .essential }}} clusters using the `tidbcloud_serverless_export` resource.

The features of the `tidbcloud_serverless_export` resource include the following:

- Create data export tasks for {{{ .starter }}} or {{{ .essential }}} clusters.
- Import data export tasks for {{{ .starter }}} or {{{ .essential }}} clusters.
- Delete data export tasks for {{{ .starter }}} or {{{ .essential }}} clusters.

> **Note:**
>
> The `tidbcloud_serverless_export` resource cannot be modified. If you want to change the configuration of the `tidbcloud_serverless_export` resource, you need to delete the existing one, and then create a new one.

## Prerequisites

- [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0 or later.
- [Create a {{{ .starter }}} or {{{ .essential }}} cluster](/tidb-cloud/create-tidb-cluster-serverless.md).

## Create a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster

You can create a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster using the `tidbcloud_serverless_export` resource.

1. Create a directory for the export and enter it.

2. Create a `export.tf` file for the data export task.

    The following is an example of the `export.tf` file:

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

    resource "tidbcloud_serverless_export" "example" {
      cluster_id   = 10476959660988000000
    }
    ```

    Use the `resource` block to define the resource of TiDB Cloud, including the resource type, resource name, and resource details.

    - To use the serverless export resource, set the resource type as `tidbcloud_serverless_export`.
    - For the resource name, you can define it as needed. For example, `example`.
    - For the resource details, you can configure them according to the serverless export specification information.
    - To get the serverless export specification information, see [tidbcloud_serverless_export (Resource)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_export).

3. Run the `terraform apply` command. It is not recommended to use `terraform apply --auto-approve` when you apply a resource.

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
        + create

    Terraform will perform the following actions:

        # tidbcloud_serverless_export.example will be created
        + resource "tidbcloud_serverless_export" "example" {
            + cluster_id     = "10476959660988000000"
            + complete_time  = (known after apply)
            + create_time    = (known after apply)
            + created_by     = (known after apply)
            + display_name   = (known after apply)
            + expire_time    = (known after apply)
            + export_id      = (known after apply)
            + export_options = (known after apply)
            + reason         = (known after apply)
            + snapshot_time  = (known after apply)
            + state          = (known after apply)
            + target         = (known after apply)
            + update_time    = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    In the preceding result, Terraform generates an execution plan for you, which describes the actions that Terraform will take:

    - You can check the difference between the configurations and the states.
    - You can also see the results of this `apply`. It will add a new resource, and no resource will be changed or destroyed.
    - `known after apply` indicates that you will get the corresponding value after `apply`.

4. If everything in your plan looks fine, type `yes` to continue:

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_export.example: Creating...
    tidbcloud_serverless_export.example: Creation complete after 1s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    In this example, the `tidbcloud_serverless_export.example` resource will create an export task to export data from the entire cluster. 
    
    This resource is not synchronized. You can use `terraform refresh` to retrieve its latest state.

5. Use the `terraform show` or `terraform state show tidbcloud_serverless_export.${resource-name}` command to inspect the state of your resource. The former command shows the states of all resources and data sources.

    ```shell
    $ terraform state show tidbcloud_serverless_export.example
    # tidbcloud_serverless_export.example:
    resource "tidbcloud_serverless_export" "example" {
        cluster_id     = "10476959660988000000"
        create_time    = "2025-06-16T08:54:10Z"
        created_by     = "apikey-S2000000"
        display_name   = "SNAPSHOT_2025-06-16T08:54:10Z"
        export_id      = "exp-ezsli6ugtzg2nkmzaitt000000"
        export_options = {
            compression = "GZIP"
            file_type   = "CSV"
        }
        snapshot_time  = "2025-06-16T08:54:10Z"
        state          = "RUNNING"
        target         = {
            type = "LOCAL"
        }
    }
    ```

## Import a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster

If a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster is not managed by Terraform, you can bring it under Terraform management by importing it.

1. Add an import block for the new `tidbcloud_serverless_export` resource.

    Add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the format of `cluster_id,export_id`:

    ```
    import {
      to = tidbcloud_serverless_export.example
      id = "${id}"
    }
    ```

2. Generate the new configuration file.

    Generate the new configuration file for the new serverless export resource according to the import block:

      ```shell
      terraform plan -generate-config-out=generated.tf
      ```

    Do not specify an existing `.tf` filename in the preceding command. Otherwise, Terraform will return an error.

3. Review and apply the generated configuration.

    Review the generated configuration file to ensure that it meets your needs. Optionally, you can move the contents of this file to your preferred location.

    Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

    ```shell
    tidbcloud_serverless_export.example: Importing... 
    tidbcloud_serverless_export.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

Now you can manage the imported export with Terraform.

## Delete a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster

To delete a data export task for a {{{ .starter }}} or {{{ .essential }}} cluster, you can delete the configuration of the `tidbcloud_serverless_export` resource, then use the `terraform apply` command to destroy the resource:

```shell
$ terraform apply
tidbcloud_serverless_export.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_export.example will be destroyed
  # (because tidbcloud_serverless_export.example is not in configuration)
  - resource "tidbcloud_serverless_export" "example" {
      - cluster_id     = "10476959660988000000" -> null
      - create_time    = "2025-06-16T08:54:10Z" -> null
      - created_by     = "apikey-S2000000" -> null
      - display_name   = "SNAPSHOT_2025-06-16T08:54:10Z" -> null
      - export_id      = "exp-ezsli6ugtzg2nkmzaitt000000" -> null
      - export_options = {
          - compression = "GZIP" -> null
          - file_type   = "CSV" -> null
        } -> null
      - snapshot_time  = "2025-06-16T08:54:10Z" -> null
      - state          = "RUNNING" -> null
      - target         = {
          - type = "LOCAL" -> null
        } -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_export.example: Destroying...
tidbcloud_serverless_export.example: Destruction complete after 2s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

Now, if you run the `terraform show` command, it will show no managed resources because the resource has been cleared:

```
$ terraform show
```

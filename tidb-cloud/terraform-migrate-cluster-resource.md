---
title: Migrate Cluster Resource to Serverless or Dedicated Cluster Resource
summary: Learn how to migrate a cluster resource to a serverless or dedicated cluster resource.
---

# Migrate Cluster Resource to Serverless or Dedicated Cluster Resource

Starting from TiDB Cloud Terraform Provider v0.4.0, the `tidbcloud_cluster` resource is replaced by two new resources: `tidbcloud_serverless_cluster` and `tidbcloud_dedicated_cluster`. If you are using TiDB Cloud Terraform Provider v0.4.0 or a later version, you can follow this document to migrate your `tidbcloud_cluster` resource to the `tidbcloud_serverless_cluster` or `tidbcloud_dedicated_cluster` resource. 

> **Tip:**
>
> The steps in this document use the configuration generation feature of Terraform to simplify the migration process by automatically recreating the `.tf` configuration for your cluster resource. To learn more about it, see [Generating configuration](https://developer.hashicorp.com/terraform/language/import/generating-configuration) in Terraform documentation.

## Prerequisites

- Upgrade to [TiDB Cloud Terraform Provider v0.4.0 or later](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest)

## Step 1. Identify the `tidbcloud_cluster` resource to migrate

1. List all `tidbcloud_cluster` resources:

    ```shell
    terraform state list | grep "tidbcloud_cluster"
    ```

2. Choose a target cluster resource to migrate and get its cluster `id` for later use:

    ```shell
    terraform state show ${your_target_cluster_resource} | grep ' id '
    ```

## Step 2. Remove the existing resource from the Terraform state

Remove your target cluster resource from the Terraform state:

```shell
terraform state rm ${your_target_cluster_resource}
```

## Step 3. Delete the configuration of your target cluster resource

In your `.tf` file, find the configuration of your target cluster resource and delete the corresponding code.

## Step 4. Add an import block for the new serverless or dedicated cluster resource

- If your target cluster is TiDB Cloud Serverless, add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the cluster ID you get from [Step 1](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate):

    ```
    # TiDB Cloud Serverless
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

- If your target cluster is TiDB Cloud Dedicated, add the following import block to your `.tf` file, replace `example` with a desired resource name, and replace `${id}` with the cluster ID you get from [Step 1](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate):

    ```
    # TiDB Cloud Dedicated
    import {
      to = tidbcloud_dedicated_cluster.example
      id = "${id}"
    }
    ```

## Step 5. Generate the new configuration file

Generate the new configuration file for the new serverless or dedicated cluster resource according to the import block:

```shell
terraform plan -generate-config-out=generated.tf
```

Do not specify an existing `.tf` file name in the preceding command. Otherwise, Terraform will return an error.

## Step 6. Review and apply the generated configuration

Review the generated configuration file to ensure it meets your needs. Optionally, you can move the contents of this file to your preferred location.

Then, run `terraform apply` to import your infrastructure. After applying, the example output is as follows: 

```shell
tidbcloud_serverless_cluster.example: Importing... 
tidbcloud_serverless_cluster.example: Import complete 

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```

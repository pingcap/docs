---
title: Migrate Cluster Resource to Serverless/Dedicated Cluster Resource
summary: Learn how to migrate cluster resource to serverless/dedicated cluster resource.
---

# Migrate Cluster Resource to Serverless/Dedicated Cluster Resource

From TiDB Cloud Terraform Provider 0.4.0, we add `tidbcloud_serverless_cluster` and `tidbcloud_dedicated_cluster` resources to replace `tidbcloud_cluster` resource. You will learn how to migrate `tidbcloud_cluster` resource to `tidbcloud_serverless_cluster`/`tidbcloud_dedicated_cluster` resource in this document.
You can refer to the [official Terraform import documentation](https://developer.hashicorp.com/terraform/language/import/generating-configuration) as a reference.

## Prerequisites

- [Update TiDB Cloud Terraform Provider at least 0.4.0](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest)

## Step 1. Select the `tidbcloud_cluster` resource to migrate

Use the command below to list all the `tidbcloud_cluster` resources.

```shell
terraform state list | grep "tidbcloud_cluster"
```

Select the cluster resource to migrate and execute the command below to get the cluster `id` for later use.

```shell
terraform state show ${your_target_cluster_resource} | grep ' id '
```

## Step 2. Delete the existed resource from state

Run the `terraform state rm ${your_target_cluster_resource}` command to delete the target cluster resource from the state.

## Step 3. Delete the configuration of your target resource

Find the configuration of your target cluster resource in the tf file and delete the related code.

## Step 4. Add the import block for your new serverless/dedicated cluster resource

Add the import block for your new serverless or dedicated cluster resource in the tf file as shown below, replacing ${id} with the previously recorded cluster ID:
```
# Serverless
import {
  to = tidbcloud_serverless_cluster.example
  id = "${id}"
}  
# Dedicated
import {
  to = tidbcloud_dedicated_cluster.example
  id = "${id}"
}  
```

## Step 5. Plan and generate configuration for the target cluster

Run the following command to generate the configuration for the target cluster. Do not supply a path to an existing file, or Terraform throws an error.
```shell
terraform plan -generate-config-out=generated.tf
```

## Step 6. Review generated configuration and apply

Review the generated configuration file to ensure it meets your requirements. You may also move the contents of this file to your desired location.

Run `terraform apply` to import your infrastructure. After applying, the console will show the message like:
```shell
tidbcloud_serverless_cluster.example: Importing... 
tidbcloud_serverless_cluster.example: Import complete 

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```

## Next step

Next, you can start managing a cluster with the [serverless cluster resource](/tidb-cloud/terraform-use-serverless-cluster-resource.md) or [dedicated cluster resource](/tidb-cloud/terraform-use-dedicated-cluster-resource.md).

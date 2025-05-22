---
title: Migrate Cluster Resource to Serverless/Dedicated Cluster Resource
summary: Learn how to migrate cluster resource to serverless/dedicated cluster resource.
---

# Migrate Cluster Resource to Serverless/Dedicated Cluster Resource

You will learn how to migrate cluster resource to serverless/dedicated cluster resource in this document.

## Prerequisites

- [Update TiDB Cloud Terraform Provider at least 0.4.0]()

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

## Step 4. Create the configuration of your new serverless/dedicated cluster resource

Create the configuration for your new serverless or dedicated cluster resource in the tf file as shown below:
```
resource "tidbcloud_serverless_cluster" "new_cluster" {}  # Serverless
resource "tidbcloud_dedicated_cluster" "new_cluster" {}  # Dedicated
```

## Step 5. Import the target cluster

Run the following command to import the target cluster, replacing ${id} with the previously recorded cluster ID:
```shell
terraform import tidbcloud_serverless_cluster.new_cluster ${id}  # Serverless
terraform import tidbcloud_dedicated_cluster.new_cluster ${id}   # Dedicated
```

If the import succeeds, you'll see a confirmation message like this:
```
Import successful!

The resources that were imported are shown above. These resources are now in
your Terraform state and will henceforth be managed by Terraform.
```

## Next step

Next, you can start managing a cluster with the [serverless cluster resource](/tidb-cloud/terraform-use-serverless-cluster-resource.md) or [dedicated cluster resource](/tidb-cloud/terraform-use-dedicated-cluster-resource.md).

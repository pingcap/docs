---
title: Backup Resource
summary: Learn how to use backup resource
---

# Backup Resource

You can learn how to create a backup of a TiDB Cloud cluster with backup resource in this document.

## Prerequisites

- Before you begin, you need to [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform/tidbcloud-provider.md) first.
- The backup and restore feature is unavailable to Developer Tier clusters. To use backup resources, make sure that you have created a Dedicated Tier cluster.

## Create a backup with backup resource

1. Copy the following configuration example. You need to replace the `project_id` and `cluster_id` values with your own.

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
    resource "tidbcloud_backup" "example_backup" {
      project_id  = "1372813089189561287"
      cluster_id  = "1379661944630234067"
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

   If you have maintained a cluster resource named `example_cluster`, you can also get project_id and cluster_id like:

    ```
    resource "tidbcloud_backup" "example_backup" {
      project_id  = tidbcloud_cluster.example_cluster.project_id
      cluster_id  = tidbcloud_cluster.example_cluster.id
      name        = "firstBackup"
      description = "create by terraform"
    }
    ```

2. Run the `terraform apply` command:

    ```
    $ terraform apply
    
    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
    
    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create
    
    Terraform will perform the following actions:
    
      # tidbcloud_backup.example_backup will be created
      + resource "tidbcloud_backup" "example_backup" {
          + cluster_id       = "1379661944630234067"
          + create_timestamp = (known after apply)
          + description      = "create by terraform"
          + id               = (known after apply)
          + name             = "firstBackup"
          + project_id       = "1372813089189561287"
          + size             = (known after apply)
          + status           = (known after apply)
          + type             = (known after apply)
        }
    
    Plan: 1 to add, 0 to change, 0 to destroy.
    
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.
    
      Enter a value: 
    ```

3. Type `yes` to create a backup:

    ```
      Enter a value: yes
    
    tidbcloud_backup.example_backup: Creating...
    tidbcloud_backup.example_backup: Creation complete after 2s [id=1350048]
    
    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    
    ```

4. Use `terraform state show tidbcloud_backup.example_backup` to check the status of the backup:

    ```
    $ terraform state show tidbcloud_backup.example_backup
    
    # tidbcloud_backup.example_backup:
    resource "tidbcloud_backup" "example_backup" {
        cluster_id       = "1379661944630234067"
        create_timestamp = "2022-08-26T07:56:10Z"
        description      = "create by terraform"
        id               = "1350048"
        name             = "firstBackup"
        project_id       = "1372813089189561287"
        size             = "0"
        status           = "PENDING"
        type             = "MANUAL"
    }
    ```

5. Wait for some minutes. Then use `terraform refersh`  to update the states:

    ```
    $ terraform refresh  
    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
    tidbcloud_backup.example_backup: Refreshing state... [id=1350048]
    $ terraform state show tidbcloud_backup.example_backup
    # tidbcloud_backup.example_backup:
    resource "tidbcloud_backup" "example_backup" {
        cluster_id       = "1379661944630234067"
        create_timestamp = "2022-08-26T07:56:10Z"
        description      = "create by terraform"
        id               = "1350048"
        name             = "firstBackup"
        project_id       = "1372813089189561287"
        size             = "198775"
        status           = "SUCCESS"
        type             = "MANUAL"
    }
    ```

If you see the status turns to `SUCCESS`, it indicates that you have created a backup for your cluster. Pay attention that the backup cannot be updated.

Now, you have created a backup for the cluster. Next, you can try [restoring a cluster](/tidb-cloud/terraform/restore-resource.md) with the backup.

## Delete a backup

To delete a backup, you can run the `terraform destroy` command to destroy the backup resource.

```
$ terraform destroy

Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
Terraform will destroy all your managed infrastructure, as shown above.
There is no undo. Only 'yes' will be accepted to confirm.

Enter a value: yes
```

Now, if you run the `terraform show` command, you will get nothing because the resource have been cleared:

```
$ terraform show
```
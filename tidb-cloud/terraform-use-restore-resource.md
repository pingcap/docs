---
title: 使用 `tidbcloud_restore` 资源
summary: 了解如何使用 `tidbcloud_restore` 资源来创建和修改恢复任务。
---

# 使用 `tidbcloud_restore` 资源

你可以在本文档中学习如何使用 `tidbcloud_restore` 资源来管理恢复任务。

`tidbcloud_restore` 资源的功能包括：

- 根据你的备份为 TiDB Cloud 专属集群创建恢复任务。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。
- 本文介绍的备份与恢复功能不适用于 starter 和 essential 集群。要使用 `tidbcloud_restore` 资源，请确保你已创建 TiDB Cloud 专属集群。

## 创建恢复任务

在为集群创建备份后，你可以通过 `tidbcloud_restore` 资源创建恢复任务来恢复集群。

> **Note:**
>
> 你只能将数据从较小的节点规格恢复到相同或更大的节点规格。

1. 为恢复任务创建一个目录并进入该目录。

2. 创建一个 `restore.tf` 文件。

    例如：

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
    resource "tidbcloud_restore" "example_restore" {
      project_id = tidbcloud_cluster.example_cluster.project_id
      backup_id  = tidbcloud_backup.example_backup.id
      name       = "restoreCluster"
      config = {
        root_password = "Your_root_password1."
        port          = 4000
        components = {
          tidb = {
            node_size : "8C16G"
            node_quantity : 2
          }
          tikv = {
            node_size : "8C32G"
            storage_size_gib : 500
            node_quantity : 6
          }
          tiflash = {
            node_size : "8C64G"
            storage_size_gib : 500
            node_quantity : 2
          }
        }
      }
    }
    ```

3. 运行 `terraform apply` 命令，并输入 `yes` 进行确认：

    ```
    $ terraform apply
    tidbcloud_cluster.example_cluster: Refreshing state... [id=1379661944630234067]
    tidbcloud_backup.example_backup: Refreshing state... [id=1350048]

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_restore.example_restore will be created
      + resource "tidbcloud_restore" "example_restore" {
          + backup_id        = "1350048"
          + cluster          = {
              + id     = (known after apply)
              + name   = (known after apply)
              + status = (known after apply)
            }
          + cluster_id       = (known after apply)
          + config           = {
              + components    = {
                  + tidb    = {
                      + node_quantity = 2
                      + node_size     = "8C16G"
                    }
                  + tiflash = {
                      + node_quantity    = 2
                      + node_size        = "8C64G"
                      + storage_size_gib = 500
                    }
                  + tikv    = {
                      + node_quantity    = 6
                      + node_size        = "8C32G"
                      + storage_size_gib = 500
                    }
                }
              + port          = 4000
              + root_password = "Your_root_password1."
            }
          + create_timestamp = (known after apply)
          + error_message    = (known after apply)
          + id               = (known after apply)
          + name             = "restoreCluster"
          + project_id       = "1372813089189561287"
          + status           = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_restore.example_restore: Creating...
    tidbcloud_restore.example_restore: Creation complete after 1s [id=780114]

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

4. 使用 `terraform state show tidbcloud_restore.${resource-name}` 命令查看恢复任务的状态：

    ```
    $ terraform state show tidbcloud_restore.example_restore

    # tidbcloud_restore.example_restore:
    resource "tidbcloud_restore" "example_restore" {
        backup_id        = "1350048"
        cluster          = {
            id     = "1379661944630264072"
            name   = "restoreCluster"
            status = "INITIALIZING"
        }
        cluster_id       = "1379661944630234067"
        config           = {
            components    = {
                tidb    = {
                    node_quantity = 2
                    node_size     = "8C16G"
                }
                tiflash = {
                    node_quantity    = 2
                    node_size        = "8C64G"
                    storage_size_gib = 500
                }
                tikv    = {
                    node_quantity    = 6
                    node_size        = "8C32G"
                    storage_size_gib = 500
                }
            }
            port          = 4000
            root_password = "Your_root_password1."
        }
        create_timestamp = "2022-08-26T08:16:33Z"
        id               = "780114"
        name             = "restoreCluster"
        project_id       = "1372813089189561287"
        status           = "PENDING"
    }
    ```

    你可以看到恢复任务的状态为 `PENDING`，集群的状态为 `INITIALIZING`。

5. 等待几分钟，然后使用 `terraform refersh` 更新状态。

6. 当集群状态变为 `AVAILABLE` 后，恢复任务会变为 `RUNNING`，最终变为 `SUCCESS`。

注意，恢复后的集群不会被 Terraform 管理。你可以通过[导入集群](/tidb-cloud/terraform-use-cluster-resource.md#import-a-cluster)来管理恢复后的集群。

## 更新恢复任务

恢复任务无法被更新。

## 删除恢复任务

恢复任务无法被删除。
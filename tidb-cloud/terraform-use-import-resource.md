---
title: 使用 Import 资源
summary: 学习如何使用 import 资源管理导入任务。
---

# 使用 Import 资源

你可以在本文档中学习如何使用 `tidbcloud_import` 资源将数据导入到 TiDB Cloud 集群。

`tidbcloud_import` 资源的功能包括：

- 为 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群创建导入任务。
- 支持从本地磁盘或 Amazon S3 存储桶导入数据。
- 取消正在进行的导入任务。

## 前置条件

- [获取 TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md)。
- [创建 TiDB Cloud Serverless 集群](/tidb-cloud/create-tidb-cluster-serverless.md) 或 [创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。

## 创建并运行导入任务

你可以使用 import 资源管理本地导入任务或 Amazon S3 导入任务。

### 创建并运行本地导入任务

> **Note:**
>
> 本地文件导入仅支持 TiDB Cloud Serverless 集群，不支持 TiDB Cloud Dedicated 集群。

1. 创建一个用于导入的 CSV 文件。例如：

   ```
   id;name;age
   1;Alice;20
   2;Bob;30
   ```

2. 创建一个 `import` 目录，并在其中创建 `main.tf` 文件。例如：

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

    resource "tidbcloud_import" "example_local" {
      project_id  = "your_project_id"
      cluster_id  = "your_cluster_id"
      type        = "LOCAL"
      data_format = "CSV"
      csv_format = {
        separator = ";"
      }
      target_table = {
        database = "test"
        table  = "import_test"
      }
      file_name = "your_csv_path"
    }
    ```

   将文件中的资源值（如 project ID、cluster ID 和 CSV 路径）替换为你自己的值。你可以在 [配置页面](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import#nested-schema-for-csv_format) 查看 `csv_format` 的详细信息。

3. 运行 `terraform apply` 命令以创建导入任务，然后输入 `yes` 确认创建并开始导入：

   ```
   $ terraform apply
   ...
   Plan: 1 to add, 0 to change, 0 to destroy.

   Do you want to perform these actions?
   Terraform will perform the actions described above.
   Only 'yes' will be accepted to approve.

   Enter a value: yes

   tidbcloud_import.example_local: Creating...
   tidbcloud_import.example_local: Creation complete after 6s [id=781074]
   ```

4. 使用 `terraform state show tidbcloud_import.${resource-name}` 查看导入任务的状态：

   ```
   $ terraform state show tidbcloud_import.example_local
   # tidbcloud_import.example_local:
   resource "tidbcloud_import" "example_local" {
       all_completed_tables          = [
           {
               message    = ""
               result     = "SUCCESS"
               table_name = "`test`.`import_test`"
           },
       ]
       cluster_id                    = "1379661944641274168"
       completed_percent             = 100
       completed_tables              = 1
       created_at                    = "2023-02-06T05:39:46.000Z"
       csv_format                    = {
           separator = ";"
       }
       data_format                   = "CSV"
       elapsed_time_seconds          = 48
       file_name                     = "./t.csv"
       id                            = "781074"
       new_file_name                 = "2023-02-06T05:39:42Z-t.csv"
       pending_tables                = 0
       post_import_completed_percent = 100
       processed_source_data_size    = "31"
       project_id                    = "1372813089191151295"
       status                        = "IMPORTING"
       target_table                  = {
           database = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

5. 过几分钟后，使用 `terraform refresh` 更新状态：

   ```
   $ terraform refresh && terraform state show tidbcloud_import.example_local
   tidbcloud_import.example_local: Refreshing state... [id=781074]
   # tidbcloud_import.example_local:
   resource "tidbcloud_import" "example_local" {
       all_completed_tables          = [
           {
               message    = ""
               result     = "SUCCESS"
               table_name = "`test`.`import_test`"
           },
       ]
       cluster_id                    = "1379661944641274168"
       completed_percent             = 100
       completed_tables              = 1
       created_at                    = "2023-02-06T05:39:46.000Z"
       csv_format                    = {
           separator = ";"
       }
       data_format                   = "CSV"
       elapsed_time_seconds          = 49
       file_name                     = "./t.csv"
       id                            = "781074"
       new_file_name                 = "2023-02-06T05:39:42Z-t.csv"
       pending_tables                = 0
       post_import_completed_percent = 100
       processed_source_data_size    = "31"
       project_id                    = "1372813089191151295"
       status                        = "COMPLETED"
       target_table                  = {
           database = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

   当 status 变为 `COMPLETED` 时，表示导入任务已完成。

6. 使用 MySQL CLI 检查导入的数据：

   ```
   mysql> SELECT * FROM test.import_test;
   +------+-------+------+
   | id   | name  | age  |
   +------+-------+------+
   |    1 | Alice |   20 |
   |    2 | Bob   |   30 |
   +------+-------+------+
   2 rows in set (0.24 sec)
   ```

### 创建并运行 Amazon S3 导入任务

> **Note:**
>
> 为了让 TiDB Cloud 访问你在 Amazon S3 存储桶中的文件，你需要先[配置 Amazon S3 访问权限](/tidb-cloud/dedicated-external-storage.md#configure-amazon-s3-access)。

1. 创建一个 `import` 目录，并在其中创建 `main.tf` 文件。例如：

   ```
   terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
       }
     }
   }

   provider "tidbcloud" {
     public_key  = "your_public_key"
     private_key = "your_private_key"
   }

   resource "tidbcloud_import" "example_s3_csv" {
     project_id   = "your_project_id"
     cluster_id   = "your_cluster_id"
     type         = "S3"
     data_format  = "CSV"
     aws_role_arn = "your_arn"
     source_url   = "your_url"
   }

   resource "tidbcloud_import" "example_s3_parquet" {
     project_id   = "your_project_id"
     cluster_id   = "your_cluster_id"
     type         = "S3"
     data_format  = "Parquet"
     aws_role_arn = "your_arn"
     source_url   = "your_url"
   }
   ```

2. 运行 `terraform apply` 命令以创建导入任务，然后输入 `yes` 确认创建并开始导入：

   ```
   $ terraform apply
   ...
   Plan: 2 to add, 0 to change, 0 to destroy.

   Do you want to perform these actions?
   Terraform will perform the actions described above.
   Only 'yes' will be accepted to approve.

   Enter a value: yes

   tidbcloud_import.example_s3_csv: Creating...
   tidbcloud_import.example_s3_csv: Creation complete after 3s [id=781075]
   tidbcloud_import.example_s3_parquet: Creating...
   tidbcloud_import.example_s3_parquet: Creation complete after 4s [id=781076]
   ```

3. 使用 `terraform refresh` 和 `terraform state show tidbcloud_import.${resource-name}` 更新并检查导入任务的状态。

## 更新导入任务

导入任务无法被更新。

## 删除导入任务

对于 Terraform，删除导入任务意味着取消对应的 import 资源。

你无法取消状态为 `COMPLETED` 的导入任务。否则，你会收到如下所示的 `Delete Error`：

```
$ terraform destroy
...
Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

tidbcloud_import.example_local: Destroying... [id=781074]
╷
│ Error: Delete Error
│
│ Unable to call CancelImport, got error: [DELETE /api/internal/projects/{project_id}/clusters/{cluster_id}/imports/{id}][500] CancelImport default  &{Code:59900104 Details:[] Message:failed to cancel
│ import}
╵
```

你可以取消状态为 `IMPORTING` 的导入任务。例如：

```
$ terraform destroy
...
Plan: 0 to add, 0 to change, 1 to destroy.

Do you really want to destroy all resources?
  Terraform will destroy all your managed infrastructure, as shown above.
  There is no undo. Only 'yes' will be accepted to confirm.

  Enter a value: yes

tidbcloud_import.example_local: Destroying... [id=781074]
tidbcloud_import.example_local: Destruction complete after 0s

Destroy complete! Resources: 1 destroyed.
```

## 配置项

请参阅 [配置文档](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import) 获取 import 资源的所有可用配置项。
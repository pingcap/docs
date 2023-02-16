---
title: Use Import Resource
summary: Learn how to manage the import task using the import resource.
---

# Import Resource

Import resource supports:

- Create import tasks in serverless tier and dedicated tier.
- LOCAL and S3 import type.
- Cancel import tasks.

You can learn how to manage an import task with the `tidbcloud_import` resource in this document.

## Before you start

- Learn how to [Get TiDB Cloud Terraform Provider](/tidb-cloud/terraform-get-tidbcloud-provider.md) first.
- A serverless tier or dedicated tier cluster is required.

## Manage the import resource

Here is an example on how to manage a LOCAL import task with import resource.

### Create

1. Create a csv file for import. For example:

   ```
   id;name;age
   1;Alice;20
   2;Bob;30
   ```

2. Create an `import` directory then create a `main.tf` inside it. For example:

    ```
    terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
         version = "~> 0.2.0"
       }
     }
   }

   provider "tidbcloud" {
     public_key = "fake_public_key"
     private_key = "fake_private_key"
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
        schema = "test"
        table  = "import_test"
      }
      file_name = "your_csv_path"
    }
    ```

   Replace resource values (such as project ID and cluster ID) in the file with your own. And you can find the details of `csv_format` in [CSV Configurations for Importing Data](/tidb-cloud/csv-config-for-import-data.md).

3. Run the `terraform apply` command and type `yes` to confirm the creation:

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

4. Use `terraform state show tidbcloud_import.${resource-name}` to check the status of the import task:

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
           schema = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

5. Use `terraform refersh` to update the status after several minutes

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
           schema = "test"
           table  = "import_test"
       }
       total_files                   = 0
       total_size                    = "31"
       total_tables_count            = 1
       type                          = "LOCAL"
   }
   ```

   When the status turns to `COMPLETED`, it indicates that the import task has finished.

6. Check the import results with MySQL CLI

   ```
   mysql> select * from test.import_test;
   +------+-------+------+
   | id   | name  | age  |
   +------+-------+------+
   |    1 | Alice |   20 |
   |    2 | Bob   |   30 |
   +------+-------+------+
   2 rows in set (0.24 sec)
   ```

### Update

Import tasks cannot be updated.

### Delete

Delete is actually cancel in import resource, and you can not cancel a `COMPLETED` import task.

Cancel an import task which has completed:

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

Cancel an import task which status is `IMPORTING`:

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

## Configurations

See [configuration documentation](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import) to get all the available configurations for import resource.
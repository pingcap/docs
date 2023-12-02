---
title: Use Import Resource
summary: Learn how to manage the import task using the import resource.
---

# インポートリソースを使用する {#use-import-resource}

このドキュメントの`tidbcloud_import`リソースを使用してTiDB Cloudクラスターにデータをインポートする方法を学習できます。

`tidbcloud_import`リソースの特徴は次のとおりです。

-   TiDB サーバーレス クラスターおよび TiDB 専用クラスターのインポート タスクを作成します。
-   ローカル ディスクまたは Amazon S3 バケットからデータをインポートします。
-   進行中のインポートタスクをキャンセルします。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) 。
-   [TiDB サーバーレスクラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)または[TiDB 専用クラスターの作成](/tidb-cloud/create-tidb-cluster.md) 。

## インポートタスクを作成して実行する {#create-and-run-an-import-task}

インポート リソースを使用して、ローカル インポート タスクまたは Amazon S3 インポート タスクのいずれかを管理できます。

### ローカルインポートタスクを作成して実行する {#create-and-run-a-local-import-task}

> **注記：**
>
> ローカル ファイルのインポートは、TiDB サーバーレス クラスターでのみサポートされており、TiDB 専用クラスターではサポートされていません。

1.  インポート用のCSVファイルを作成します。例えば：

        id;name;age
        1;Alice;20
        2;Bob;30

2.  `import`ディレクトリを作成し、その中に`main.tf`を作成します。例えば：

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

    ファイル内のリソース値 (プロジェクト ID、クラスター ID、CSV パスなど) を独自の値に置き換えます。そしてその[設定ページ](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import#nested-schema-for-csv_format) `csv_format`の詳細。

3.  `terraform apply`コマンドを実行してインポート タスクを作成し、 `yes`を入力して作成を確認し、インポートを開始します。

        $ terraform apply
        ...
        Plan: 1 to add, 0 to change, 0 to destroy.

        Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value: yes

        tidbcloud_import.example_local: Creating...
        tidbcloud_import.example_local: Creation complete after 6s [id=781074]

4.  インポート タスクのステータスを確認するには、 `terraform state show tidbcloud_import.${resource-name}`を使用します。

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

5.  数分後にステータスを更新するには、 `terraform refresh`を使用します。

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

    ステータスが`COMPLETED`に変わると、インポート タスクが完了したことを示します。

6.  MySQL CLI でインポートされたデータを確認します。

        mysql> SELECT * FROM test.import_test;
        +------+-------+------+
        | id   | name  | age  |
        +------+-------+------+
        |    1 | Alice |   20 |
        |    2 | Bob   |   30 |
        +------+-------+------+
        2 rows in set (0.24 sec)

### Amazon S3 インポート タスクを作成して実行する {#create-and-run-an-amazon-s3-import-task}

> **注記：**
>
> TiDB Cloud がAmazon S3 バケット内のファイルにアクセスできるようにするには、まず[Amazon S3 アクセスを設定する](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access)を行う必要があります。

1.  `import`ディレクトリを作成し、その中に`main.tf`を作成します。例えば：

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

2.  `terraform apply`コマンドを実行してインポート タスクを作成し、 `yes`を入力して作成を確認し、インポートを開始します。

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

3.  `terraform refresh`と`terraform state show tidbcloud_import.${resource-name}`を使用して、インポート タスクのステータスを更新および確認します。

## インポートタスクを更新する {#update-an-import-task}

インポートタスクは更新できません。

## インポートタスクを削除する {#delete-an-import-task}

Terraform の場合、インポート タスクの削除は、対応するインポート リソースをキャンセルすることを意味します。

`COMPLETED`インポート タスクはキャンセルできません。それ以外の場合は、次の例のように`Delete Error`が返されます。

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

ステータスが`IMPORTING`のインポートタスクはキャンセルできます。例えば：

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

## 構成 {#configurations}

インポート リソースで使用可能なすべての構成を取得するには、 [設定ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/import)を参照してください。

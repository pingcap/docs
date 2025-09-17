---
title: Use `tidbcloud_serverless_export` Resource
summary: tidbcloud_serverless_export` リソースを使用して、 TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを作成および変更する方法を学習します。
---

# <code>tidbcloud_serverless_export</code>リソースを使用する {#use-code-tidbcloud-serverless-export-code-resource}

このドキュメントでは、 `tidbcloud_serverless_export`リソースを使用して、TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを管理する方法について説明します。

`tidbcloud_serverless_export`リソースの機能は次のとおりです。

-   TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを作成します。
-   TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクをインポートします。
-   TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを削除します。

> **注記：**
>
> `tidbcloud_serverless_export`リソースは変更できません。3 `tidbcloud_serverless_export`のリソースの設定を変更する場合は、既存のリソースを削除してから、新しいリソースを作成する必要があります。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。
-   [TiDB Cloud Starter またはTiDB Cloud Essential クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md) 。

## TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを作成する {#create-a-data-export-task-for-a-tidb-cloud-starter-or-tidb-cloud-essential-cluster}

`tidbcloud_serverless_export`リソースを使用して、 TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを作成できます。

1.  エクスポート用のディレクトリを作成してそこに入ります。

2.  データ エクスポート タスク用に`export.tf`ファイルを作成します。

    以下は`export.tf`ファイルの例です。

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

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   サーバーレス エクスポート リソースを使用するには、リソース タイプを`tidbcloud_serverless_export`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   リソースの詳細については、サーバーレス エクスポート仕様情報に従って設定できます。
    -   サーバーレス エクスポート仕様情報を取得するには、 [tidbcloud_serverless_export (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_export)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

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

    上記の結果では、Terraform によって実行プランが生成され、Terraform が実行するアクションが記述されています。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` `apply`後の対応する値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_export.example: Creating...
    tidbcloud_serverless_export.example: Creation complete after 1s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

    この例では、 `tidbcloud_serverless_export.example`リソースがクラスター全体からデータをエクスポートするエクスポート タスクを作成します。

    このリソースは同期されていません。1 `terraform refresh`使用すると最新の状態を取得できます。

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_serverless_export.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

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

## TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクをインポートします {#import-a-data-export-task-for-a-tidb-cloud-starter-or-tidb-cloud-essential-cluster}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクが Terraform によって管理されていない場合は、インポートすることで Terraform 管理下に置くことができます。

1.  新しい`tidbcloud_serverless_export`リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,export_id`の形式に置き換えます。

        import {
          to = tidbcloud_serverless_export.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しいサーバーレス エクスポート リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後、出力例は次のようになります。

    ```shell
    tidbcloud_serverless_export.example: Importing... 
    tidbcloud_serverless_export.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたエクスポートを Terraform で管理できるようになりました。

## TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを削除します {#delete-a-data-export-task-for-a-tidb-cloud-starter-or-tidb-cloud-essential-cluster}

TiDB Cloud Starter またはTiDB Cloud Essential クラスターのデータ エクスポート タスクを削除するには、 `tidbcloud_serverless_export`リソースの構成を削除してから、 `terraform apply`コマンドを使用してリソースを破棄します。

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

ここで、 `terraform show`コマンドを実行すると、リソースがクリアされているため、管理対象リソースは表示されません。

    $ terraform show

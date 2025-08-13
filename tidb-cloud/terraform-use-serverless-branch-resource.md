---
title: Use `tidbcloud_serverless_branch` Resource
summary: サーバーレス ブランチ リソースを使用してTiDB Cloud Starter ブランチを作成および変更する方法を学習します。
---

# <code>tidbcloud_serverless_branch</code>リソースを使用する {#use-the-code-tidbcloud-serverless-branch-code-resource}

このドキュメントでは、 `tidbcloud_serverless_branch`リソースを使用して[TiDB Cloudスターター ブランチ](/tidb-cloud/branch-manage.md)管理する方法について説明します。

`tidbcloud_serverless_branch`リソースの機能は次のとおりです。

-   TiDB Cloud Starter ブランチを作成します。
-   TiDB Cloud Starter ブランチをインポートします。
-   TiDB Cloud Starter ブランチを削除します。

> **注記：**
>
> `tidbcloud_serverless_branch`リソースは変更できません。サーバーレスブランチリソースの設定を変更する場合は、既存のリソースを削除して新しいリソースを作成する必要があります。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。
-   [TiDB Cloud Starter クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md) 。

## TiDB Cloud Starterブランチを作成する {#create-a-tidb-cloud-starter-branch}

`tidbcloud_serverless_branch`リソースを使用して、 TiDB Cloud Starter ブランチを作成できます。

次の例は、TiDB Cloud Starter ブランチを作成する方法を示しています。

1.  ブランチ用のディレクトリを作成してそこに入ります。

2.  `branch.tf`ファイルを作成します。

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

        resource "tidbcloud_serverless_branch" "example" {
          cluster_id   = 10581524018573000000
          display_name = "example"
          parent_id = 10581524018573000000
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   サーバーレス ブランチ リソースを使用するには、リソース タイプを`tidbcloud_serverless_branch`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   リソースの詳細については、サーバーレス ブランチの仕様情報に従って設定できます。
    -   サーバーレス ブランチの仕様情報を取得するには、 [tidbcloud_serverless_branch (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/serverless_branch)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

      # tidbcloud_serverless_branch.example will be created
      + resource "tidbcloud_serverless_branch" "example" {
          + annotations         = (known after apply)
          + branch_id           = (known after apply)
          + cluster_id          = "10581524018573000000"
          + create_time         = (known after apply)
          + created_by          = (known after apply)
          + display_name        = "example"
          + endpoints           = (known after apply)
          + parent_display_name = (known after apply)
          + parent_id           = "10581524018573000000"
          + parent_timestamp    = (known after apply)
          + state               = (known after apply)
          + update_time         = (known after apply)
          + user_prefix         = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value:
    ```

    上記の結果では、Terraform によって実行されるアクションを記述した実行プランが生成されます。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` `apply`後の対応する値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_serverless_branch.example: Creating...
    tidbcloud_serverless_branch.example: Still creating... [10s elapsed]
    tidbcloud_serverless_branch.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_serverless_branch.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_serverless_branch.example 
    # tidbcloud_serverless_branch.example:
    resource "tidbcloud_serverless_branch" "example" {
        annotations         = {
            "tidb.cloud/has-set-password" = "false"
        }
        branch_id           = "bran-qt3fij6jufcf5pluot5h000000"
        cluster_id          = "10581524018573000000"
        create_time         = "2025-06-16T07:55:51Z"
        created_by          = "apikey-S2000000"
        display_name        = "example"
        endpoints           = {
            private = {
                aws  = {
                    availability_zone = [
                        "use1-az6",
                    ]
                    service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000"
                }
                host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com"
                port = 4000
            }
            public  = {
                disabled = false
                host     = "gateway01.us-east-1.prod.aws.tidbcloud.com"
                port     = 4000
            }
        }
        parent_display_name = "test-tf"
        parent_id           = "10581524018573000000"
        parent_timestamp    = "2025-06-16T07:55:51Z"
        state               = "ACTIVE"
        update_time         = "2025-06-16T07:56:49Z"
        user_prefix         = "4ER5SbndR000000"
    }
    ```

## TiDB Cloud Starterブランチをインポートする {#import-a-tidb-cloud-starter-branch}

Terraform で管理されていないTiDB Cloud Starter ブランチの場合は、インポートするだけで Terraform を使用して管理できます。

次のように、Terraform によって作成されていないTiDB Cloud Starter ブランチをインポートします。

1.  新しい`tidbcloud_serverless_branch`リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,branch_id`の形式に置き換えます。

        import {
          to = tidbcloud_serverless_branch.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しい`tidbcloud_serverless_branch`リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`を実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

    ```shell
    tidbcloud_serverless_branch.example: Importing... 
    tidbcloud_serverless_branch.example: Import complete 

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたブランチを Terraform で管理できるようになりました。

## TiDB Cloud Starterブランチを削除する {#delete-a-tidb-cloud-starter-branch}

TiDB Cloud Starter ブランチを削除するには、 `tidbcloud_serverless_branch`リソースの構成を削除してから、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
$ terraform apply
tidbcloud_serverless_branch.example: Refreshing state...

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

Terraform will perform the following actions:

  # tidbcloud_serverless_branch.example will be destroyed
  # (because tidbcloud_serverless_branch.example is not in configuration)
  - resource "tidbcloud_serverless_branch" "example" {
      - annotations         = {
          - "tidb.cloud/has-set-password" = "false"
        } -> null
      - branch_id           = "bran-qt3fij6jufcf5pluot5h000000" -> null
      - cluster_id          = "10581524018573000000" -> null
      - create_time         = "2025-06-16T07:55:51Z" -> null
      - created_by          = "apikey-S2000000" -> null
      - display_name        = "example" -> null
      - endpoints           = {
          - private = {
              - aws  = {
                  - availability_zone = [
                      - "use1-az6",
                    ] -> null
                  - service_name      = "com.amazonaws.vpce.us-east-1.vpce-svc-0062ecf0683000000" -> null
                } -> null
              - host = "gateway01-privatelink.us-east-1.prod.aws.tidbcloud.com" -> null
              - port = 4000 -> null
            } -> null
          - public  = {
              - disabled = false -> null
              - host     = "gateway01.us-east-1.prod.aws.tidbcloud.com" -> null
              - port     = 4000 -> null
            } -> null
        } -> null
      - parent_display_name = "test-tf" -> null
      - parent_id           = "10581524018573000000" -> null
      - parent_timestamp    = "2025-06-16T07:55:51Z" -> null
      - state               = "ACTIVE" -> null
      - update_time         = "2025-06-16T07:56:49Z" -> null
      - user_prefix         = "4ER5SbndR000000" -> null
    }

Plan: 0 to add, 0 to change, 1 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

tidbcloud_serverless_branch.example: Destroying...
tidbcloud_serverless_branch.example: Destruction complete after 1s

Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、 `terraform show`コマンドを実行すると、リソースがクリアされているため、管理対象リソースは表示されません。

    $ terraform show

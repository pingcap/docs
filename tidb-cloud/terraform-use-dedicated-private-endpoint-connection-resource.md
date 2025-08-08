---
title: Use TiDB Cloud Dedicated Private Endpoint Connection Resource
summary: TiDB Cloud Dedicated プライベート エンドポイント接続リソースを使用して、 TiDB Cloud Dedicated プライベート エンドポイント接続を作成および変更する方法を学習します。
---

# TiDB Cloud専用プライベートエンドポイント接続リソースを使用する {#use-tidb-cloud-dedicated-private-endpoint-connection-resource}

このドキュメントでは、 `tidbcloud_dedicated_private_endpoint_connection`リソースを使用して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)プライベート エンドポイント接続を管理する方法について説明します。

`tidbcloud_dedicated_private_endpoint_connection`リソースの機能は次のとおりです。

-   TiDB Cloud Dedicated プライベート エンドポイント接続を作成します。
-   TiDB Cloud Dedicated プライベート エンドポイント接続をインポートします。
-   TiDB Cloud Dedicated プライベート エンドポイント接続を削除します。

> **注記：**
>
> TiDB Cloud Dedicated プライベートエンドポイント接続リソースは変更できません。TiDB TiDB Cloud Dedicated プライベートエンドポイント接続を変更する場合は、既存の接続を削除してから、新しい接続を作成する必要があります。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。
-   [TiDB Cloud専用クラスタを作成する](/tidb-cloud/create-tidb-cluster.md) 。

## TiDB Cloud Dedicatedプライベートエンドポイント接続を作成する {#create-a-tidb-cloud-dedicated-private-endpoint-connection}

`tidbcloud_dedicated_private_endpoint_connection`リソースを使用して、 TiDB Cloud Dedicated プライベート エンドポイント接続を作成できます。

次の例は、 TiDB Cloud Dedicated プライベート エンドポイント接続を作成する方法を示しています。

1.  TiDB Cloud Dedicated プライベート エンドポイント接続用のディレクトリを作成し、そこに入ります。

2.  `private_endpoint_connection.tf`ファイルを作成します。

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

        resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
          cluster_id = "your_cluster_id"
          node_group_id = "your_node_group_id"
          endpoint_id = "your_endpoint_id"
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   TiDB Cloud Dedicated プライベート エンドポイント接続リソースを使用するには、リソース タイプを`tidbcloud_dedicated_private_endpoint_connection`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   必要な引数の値を取得する方法がわからない場合は、 [AWS のプライベートエンドポイント経由でTiDB Cloud専用クラスタに接続する](/tidb-cloud/set-up-private-endpoint-connections.md)参照してください。
    -   TiDB Cloud Dedicated プライベート エンドポイント接続仕様情報を取得するには、 [tidbcloud_private_endpoint_connection (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_private_endpoint_connection)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_private_endpoint_connection.example will be created
        + resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
            + account_id                     = (known after apply)
            + cloud_provider                 = (known after apply)
            + cluster_display_name           = (known after apply)
            + cluster_id                     = "10757937805044000000"
            + endpoint_id                    = "vpce-03367e9618000000"
            + endpoint_state                 = (known after apply)
            + host                           = (known after apply)
            + labels                         = (known after apply)
            + message                        = (known after apply)
            + node_group_id                  = "1934178998036000000"
            + port                           = (known after apply)
            + private_endpoint_connection_id = (known after apply)
            + private_link_service_name      = (known after apply)
            + region_display_name            = (known after apply)
            + region_id                      = (known after apply)
        }

    Plan: 1 to add, 0 to change, 0 to destroy.

    Do you want to perform these actions?
        Terraform will perform the actions described above.
        Only 'yes' will be accepted to approve.

        Enter a value:
    ```

    上記の結果では、Terraform によって実行プランが生成され、Terraform が実行するアクションが記述されます。

    -   構成と状態の違いを確認できます。
    -   `apply`の結果も確認できます。新しいリソースが追加されますが、リソースは変更または破棄されません。
    -   `known after apply` `apply`後の対応する値が取得されることを示します。

4.  計画の内容がすべて問題ない場合は、「 `yes`と入力して続行します。

    ```shell
    Do you want to perform these actions?
      Terraform will perform the actions described above.
      Only 'yes' will be accepted to approve.

      Enter a value: yes

    tidbcloud_dedicated_private_endpoint_connection.example: Creating...
    tidbcloud_dedicated_private_endpoint_connection.example: Creation complete after 10s

    Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
    ```

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_dedicated_private_endpoint_connection.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_dedicated_private_endpoint_connection.example
    # tidbcloud_dedicated_private_endpoint_connection.example:
    resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
        cloud_provider                 = "aws"
        cluster_display_name           = "test-tf"
        cluster_id                     = "10757937805044000000"
        endpoint_id                    = "vpce-03367e96180000000"
        endpoint_state                 = "ACTIVE"
        host                           = "privatelink-19341000.ubkypd000000.clusters.tidb-cloud.com"
        labels                         = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist"
        node_group_id                  = "1934178998036000000"
        port                           = 4000
        private_endpoint_connection_id = "1934214559409000000"
        private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000"
        region_display_name            = "Oregon (us-west-2)"
        region_id                      = "aws-us-west-2"
    }
    ```

## TiDB Cloud Dedicatedプライベートエンドポイント接続をインポートする {#import-a-tidb-cloud-dedicated-private-endpoint-connection}

Terraform によって管理されていないTiDB Cloud Dedicated プライベート エンドポイント接続の場合は、インポートすることで Terraform による管理を開始できます。

1.  新しいTiDB Cloud Dedicated プライベート エンドポイント接続リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,dedicated_private_endpoint_connection_id`の形式に置き換えます。

        import {
          to = tidbcloud_dedicated_private_endpoint_connection.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しいTiDB Cloud Dedicated プライベート エンドポイント接続リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

    次に、インポートされたリソースの構成を含む`generated.tf`ファイルが現在のディレクトリに作成されます。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`を実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

    ```shell
    tidbcloud_dedicated_private_endpoint_connection.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_private_endpoint_connection.example: Import complete [id=aws-19341879538940000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

    これで、インポートしたTiDB Cloud Dedicated プライベート エンドポイント接続を Terraform を使用して管理できるようになりました。

## TiDB Cloud Dedicated プライベートエンドポイント接続を削除する {#delete-a-tidb-cloud-dedicated-private-endpoint-connection}

TiDB Cloud Dedicated プライベート エンドポイント接続を削除するには、 `tidbcloud_dedicated_private_endpoint_connection`リソースの構成を削除してから、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
  $ terraform apply
  tidbcloud_dedicated_private_endpoint_connection.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

  Terraform will perform the following actions:

  # tidbcloud_dedicated_private_endpoint_connection.example will be destroyed
  # (because tidbcloud_dedicated_private_endpoint_connection.example is not in configuration)
  - resource "tidbcloud_dedicated_private_endpoint_connection" "example" {
      - cloud_provider                 = "aws" -> null
      - cluster_display_name           = "test-tf" -> null
      - cluster_id                     = "10757937805044000000" -> null
      - endpoint_id                    = "vpce-03367e96180000000" -> null
      - endpoint_state                 = "ACTIVE" -> null
      - host                           = "privatelink-19341000.ubkypd1sx000.clusters.tidb-cloud.com" -> null
      - labels                         = {
          - "tidb.cloud/project" = "1372813089454000000"
          } -> null
      - message                        = "The VPC Endpoint Id '{vpce-03367e961805e35b6 []}' does not exist" -> null
      - node_group_id                  = "1934178998036000000" -> null
      - port                           = 4000 -> null
      - private_endpoint_connection_id = "1934214559409000000" -> null
      - private_link_service_name      = "com.amazonaws.vpce.us-west-2.vpce-svc-07468b31cc9000000" -> null
      - region_display_name            = "Oregon (us-west-2)" -> null
      - region_id                      = "aws-us-west-2" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

  tidbcloud_dedicated_private_endpoint_connection.example: Destroying...
  tidbcloud_dedicated_private_endpoint_connection.example: Destruction complete after 1s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、コマンド`terraform show`実行すると、リソースがクリアされているため何も表示されません。

    $ terraform show

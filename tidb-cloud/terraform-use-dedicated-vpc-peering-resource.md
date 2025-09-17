---
title: Use the `tidbcloud_dedicated_vpc_peering` Resource
summary: tidbcloud_dedicated_vpc_peering` リソースを使用して、 TiDB Cloud Dedicated VPC ピアリングを作成および変更する方法を学習します。
---

# <code>tidbcloud_dedicated_vpc_peering</code>リソースを使用する {#use-the-code-tidbcloud-dedicated-vpc-peering-code-resource}

このドキュメントでは、 `tidbcloud_dedicated_vpc_peering`リソースとの[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) VPC ピアリングを管理する方法について説明します。

`tidbcloud_dedicated_vpc_peering`リソースの機能は次のとおりです。

-   TiDB Cloud専用 VPC ピアリングを作成します。
-   TiDB Cloud専用 VPC ピアリングをインポートします。
-   TiDB Cloud専用 VPC ピアリングを削除します。

> **注記：**
>
> `tidbcloud_dedicated_vpc_peering`リソースは変更できません。TiDB TiDB Cloud Dedicated VPC ピアリングの設定を変更する場合は、既存のピアリングを削除してから、新しいピアリングを作成する必要があります。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。

## TiDB Cloud専用VPCピアリングを作成する {#create-a-tidb-cloud-dedicated-vpc-peering}

`tidbcloud_dedicated_vpc_peering`リソースを使用して、 TiDB Cloud Dedicated VPC ピアリングを作成できます。

次の例は、TiDB Cloud Dedicated VPC ピアリングを作成する方法を示しています。

1.  TiDB Cloud Dedicated VPC ピアリング用のディレクトリを作成してそこに入ります。

2.  `vpc_peering.tf`ファイルを作成します。

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

        resource "tidbcloud_dedicated_vpc_peering" "example" {
          tidb_cloud_region_id = "your_tidb_cloud_region_id"
          customer_region_id   = "your_customer_region_id"
          customer_account_id  = "your_customer_account_id"
          customer_vpc_id      = "your_customer_vpc_id"
          customer_vpc_cidr    = "your_customer_vpc_cidr"
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   `tidbcloud_dedicated_vpc_peering`リソースを使用するには、リソース タイプを`tidbcloud_dedicated_vpc_peering`に設定します。
    -   リソース名は必要に応じて定義できます。例： `example` 。
    -   必要な引数の値を取得する方法がわからない場合は、 [VPC ピアリング経由でTiDB Cloud Dedicated に接続する](/tidb-cloud/set-up-vpc-peering-connections.md)参照してください。
    -   TiDB Cloud Dedicated VPC ピアリング仕様情報を取得するには、 [tidbcloud_dedicated_vpc_peering (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_vpc_peering)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
        + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_vpc_peering.example will be created
        + resource "tidbcloud_dedicated_vpc_peering" "example" {
            + aws_vpc_peering_connection_id = (known after apply)
            + customer_account_id           = "986330900000"
            + customer_region_id            = "aws-us-west-2"
            + customer_vpc_cidr             = "172.16.32.0/21"
            + customer_vpc_id               = "vpc-0c0c7d59702000000"
            + labels                        = (known after apply)
            + project_id                    = (known after apply)
            + state                         = (known after apply)
            + tidb_cloud_account_id         = (known after apply)
            + tidb_cloud_cloud_provider     = (known after apply)
            + tidb_cloud_region_id          = "aws-us-west-2"
            + tidb_cloud_vpc_cidr           = (known after apply)
            + tidb_cloud_vpc_id             = (known after apply)
            + vpc_peering_id                = (known after apply)
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

    tidbcloud_dedicated_vpc_peering.example: Creating...
    tidbcloud_dedicated_vpc_peering.example: Still creating... [10s elapsed]
    ```

    クラウドプロバイダーのコンソールでVPCピアリング接続を承認するまで、リソースのステータスは`Creating`ままです。VPCピアリング接続を承認すると、ステータスは[VPC ピアリングの承認と設定](/tidb-cloud/set-up-vpc-peering-connections.md#step-2-approve-and-configure-the-vpc-peering)基準に`Active`に変わります。

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_dedicated_vpc_peering.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_dedicated_vpc_peering.example
    # tidbcloud_dedicated_vpc_peering.example:
    resource "tidbcloud_dedicated_vpc_peering" "example" {
        aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000"
        customer_account_id           = "986330900000"
        customer_region_id            = "aws-us-west-2"
        customer_vpc_cidr             = "172.16.32.0/21"
        customer_vpc_id               = "vpc-0c0c7d59702000000"
        labels                        = {
            "tidb.cloud/project" = "1372813089187000000"
        }
        project_id                    = "13728130891870000000"
        state                         = "ACTIVE"
        tidb_cloud_account_id         = "380838400000"
        tidb_cloud_cloud_provider     = "aws"
        tidb_cloud_region_id          = "aws-us-west-2"
        tidb_cloud_vpc_cidr           = "10.250.0.0/16"
        tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000"
        vpc_peering_id                = "aws-1934187953894000000"
    }
    ```

## TiDB Cloud Dedicated VPC ピアリングをインポートする {#import-a-tidb-cloud-dedicated-vpc-peering}

Terraform によって管理されていないTiDB Cloud Dedicated VPC ピアリングの場合は、インポートすることで Terraform の管理下に置くことができます。

たとえば、Terraform によって作成されていない VPC ピアリングをインポートできます。

1.  新しい`tidbcloud_dedicated_vpc_peering`リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,vpc_peering_id`の形式に置き換えます。

        import {
          to = tidbcloud_dedicated_vpc_peering.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しい`tidbcloud_dedicated_vpc_peering`リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

    次に、インポートされたリソースの構成を含む`generated.tf`ファイルが現在のディレクトリに作成されます。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後、出力例は次のようになります。

    ```shell
    tidbcloud_dedicated_vpc_peering.example: Importing... [id=aws-1934187953894000000,example]
    tidbcloud_dedicated_vpc_peering.example: Import complete [id=aws-19341879538940000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたTiDB Cloud Dedicated VPC ピアリングを Terraform で管理できるようになりました。

## TiDB Cloud Dedicated VPC ピアリングを削除する {#delete-a-tidb-cloud-dedicated-vpc-peering}

TiDB Cloud Dedicated VPC ピアリングを削除するには、 `tidbcloud_dedicated_vpc_peering`リソースの設定を削除してから、 `terraform apply`コマンドを使用してリソースを破棄します。

```shell
  $ terraform apply
  tidbcloud_dedicated_vpc_peering.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  - destroy

  Terraform will perform the following actions:

  # tidbcloud_dedicated_vpc_peering.example will be destroyed
  # (because tidbcloud_dedicated_vpc_peering.example is not in configuration)
  - resource "tidbcloud_dedicated_vpc_peering" "example" {
      - aws_vpc_peering_connection_id = "pcx-0b2e5211d48000000" -> null
      - customer_account_id           = "986330900000" -> null
      - customer_region_id            = "aws-us-west-2" -> null
      - customer_vpc_cidr             = "172.16.32.0/21" -> null
      - customer_vpc_id               = "vpc-0c0c7d59702000000" -> null
      - labels                        = {
          - "tidb.cloud/project" = "1372813089187000000"
          } -> null
      - project_id                    = "1372813089187000000" -> null
      - state                         = "ACTIVE" -> null
      - tidb_cloud_account_id         = "380838000000" -> null
      - tidb_cloud_cloud_provider     = "aws" -> null
      - tidb_cloud_region_id          = "aws-us-west-2" -> null
      - tidb_cloud_vpc_cidr           = "10.250.0.0/16" -> null
      - tidb_cloud_vpc_id             = "vpc-0b9fa4b78ef000000" -> null
      - vpc_peering_id                = "aws-1934187953894000000" -> null
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

  tidbcloud_dedicated_vpc_peering.example: Destroying...
  tidbcloud_dedicated_vpc_peering.example: Destruction complete after 1s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、コマンド`terraform show`実行すると、リソースがクリアされているため何も表示されません。

    $ terraform show

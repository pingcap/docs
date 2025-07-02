---
title: Use TiDB Cloud Dedicated Network Container Resource
summary: TiDB Cloud Dedicated ネットワーク コンテナ リソースを使用して、 TiDB Cloud Dedicated ネットワーク コンテナを作成および変更する方法を学習します。
---

# TiDB Cloud専用ネットワークコンテナリソースを使用する {#use-tidb-cloud-dedicated-network-container-resource}

このドキュメントでは、 `tidbcloud_dedicated_network_container`リソースを使用して[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)ネットワーク コンテナーを管理する方法について説明します。

ネットワークコンテナは、特定のプロジェクトとリージョンのCIDRブロック（IPアドレス範囲）を定義および管理できる論理ネットワークリソースです。このCIDRブロックは、 TiDB Cloud Dedicatedクラスター用のVPCを作成するために使用され、そのリージョンでVPCピアリングを設定する前に必要です。

リージョンにVPCピアリングリクエストを追加する前に、まずそのリージョンのCIDRブロックを設定し、最初のTiDB Cloud Dedicatedクラスターを作成する必要があります。最初のクラスターが作成されると、 TiDB Cloudは関連するVPCを自動的に作成し、アプリケーションのVPCとのピアリング接続を確立できるようになります。

`tidbcloud_dedicated_network_container`リソースの機能は次のとおりです。

-   TiDB Cloud専用ネットワーク コンテナーを作成します。
-   TiDB Cloud Dedicated ネットワーク コンテナーをインポートします。
-   TiDB Cloud Dedicated ネットワーク コンテナーを削除します。

> **注記：**
>
> TiDB Cloud Dedicatedネットワークコンテナは、ステータスが`ACTIVE`場合、変更または削除できません。適用する前に、 `tidbcloud_network_container`リソースの構成が正しいことを確認してください。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md) v0.4.0以降。

## TiDB Cloud専用ネットワークコンテナを作成する {#create-a-tidb-cloud-dedicated-network-container}

`tidbcloud_dedicated_network_container`リソースを使用して、 TiDB Cloud専用ネットワーク コンテナーを作成できます。

次の例は、TiDB Cloud Dedicated ネットワーク コンテナを作成する方法を示しています。

1.  TiDB Cloud Dedicated ネットワーク コンテナのディレクトリを作成してそこに入ります。

2.  `network_container.tf`ファイルを作成します。

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

        resource "tidbcloud_dedicated_network_container" "example" {
          project_id = "1372813089454000000"
          region_id = "aws-ap-northeast-2"
          cidr_notation = "172.16.16.0/21"
        }

    `resource`ブロックを使用して、リソース タイプ、リソース名、リソースの詳細など、 TiDB Cloudのリソースを定義します。

    -   TiDB Cloud Dedicated ネットワーク コンテナ リソースを使用するには、リソース タイプを`tidbcloud_dedicated_network_container`に設定します。
    -   リソース名は、必要に応じて定義できます（例： `example` ）。
    -   必要な引数の値を取得する方法がわからない場合は、 [リージョンの CIDR を設定する](/tidb-cloud/set-up-vpc-peering-connections.md#prerequisite-set-a-cidr-for-a-region)参照してください。
    -   TiDB Cloud Dedicated ネットワーク コンテナ仕様の詳細については、 [tidbcloud_dedicated_network_container (リソース)](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs/resources/dedicated_network_container)参照してください。

3.  `terraform apply`コマンドを実行します。リソースを適用する場合は`terraform apply --auto-approve`の使用は推奨されません。

    ```shell
    $ terraform apply

    Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
      + create

    Terraform will perform the following actions:

        # tidbcloud_dedicated_network_container.example will be created
        + resource "tidbcloud_dedicated_network_container" "example" {
            + cidr_notation        = "172.16.16.0/21"
            + cloud_provider       = (known after apply)
            + labels               = (known after apply)
            + network_container_id = (known after apply)
            + project_id           = "1372813089454543324"
            + region_display_name  = (known after apply)
            + region_id            = "aws-ap-northeast-2"
            + state                = (known after apply)
            + vpc_id               = (known after apply)
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

    tidbcloud_dedicated_network_container.example: Creating...
    tidbcloud_dedicated_network_container.example: Creation complete after 4s
    ```

    TiDB Cloud Dedicated ネットワークコンテナのリージョンにTiDB Cloud Dedicated クラスターを作成するまで、リソースのステータスは`INACTIVE`ままです。その後、ステータスは`ACTIVE`に変わります。

5.  リソースの状態を確認するには、コマンド`terraform show`または`terraform state show tidbcloud_dedicated_network_container.${resource-name}`使用します。コマンド 1 は、すべてのリソースとデータソースの状態を表示します。

    ```shell
    $ terraform state show tidbcloud_dedicated_network_container.example          
    # tidbcloud_dedicated_network_container.example:
    resource "tidbcloud_dedicated_network_container" "example" {
        cidr_notation        = "172.16.16.0/21"
        cloud_provider       = "aws"
        labels               = {
            "tidb.cloud/project" = "1372813089454000000"
        }
        network_container_id = "1934235512696000000"
        project_id           = "1372813089454000000"
        region_display_name  = "Seoul (ap-northeast-2)"
        region_id            = "aws-ap-northeast-2"
        state                = "INACTIVE"
        vpc_id               = null
    }
    ```

## TiDB Cloud専用ネットワークコンテナをインポートする {#import-a-tidb-cloud-dedicated-network-container}

Terraform で管理されていないTiDB Cloud Dedicated ネットワーク コンテナの場合は、インポートするだけで Terraform を使用して管理できます。

たとえば、Terraform によって作成されていないネットワーク コンテナーをインポートできます。

1.  新しいTiDB Cloud Dedicated ネットワーク コンテナ リソースのインポート ブロックを追加します。

    次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` `cluster_id,network_container_id`の形式に置き換えます。

        import {
          to = tidbcloud_dedicated_network_container.example
          id = "${id}"
        }

2.  新しい構成ファイルを生成します。

    インポート ブロックに従って、新しいTiDB Cloud Dedicated ネットワーク コンテナ リソースの新しい構成ファイルを生成します。

    ```shell
    terraform plan -generate-config-out=generated.tf
    ```

    上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

    次に、インポートされたリソースの構成を含む`generated.tf`ファイルが現在のディレクトリに作成されます。

3.  生成された構成を確認して適用します。

    生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

    次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

    ```shell
    tidbcloud_dedicated_network_container.example: Importing... [id=10423692645683000000,example]
    tidbcloud_dedicated_network_container.example: Import complete [id=10423692645683000000,example]

    Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
    ```

これで、インポートしたTiDB Cloud Dedicated ネットワーク コンテナを Terraform で管理できるようになりました。

## TiDB Cloud Dedicatedネットワークコンテナを削除する {#delete-a-tidb-cloud-dedicated-network-container}

TiDB Cloud Dedicated クラスターを削除するには、 `tidbcloud_dedicated_cluster`リソースの設定を削除し、 `terraform apply`コマンドを使用してリソースを破棄します。ただし、 TiDB Cloud Dedicated ネットワークコンテナのステータスが`ACTIVE`でないことを確認する必要があります。ステータスが`ACTIVE`場合は削除できません。

ステータスが`INACTIVE`の場合は、次のコマンドを実行して削除できます。

```shell
  $ terraform apply
  tidbcloud_dedicated_network_container.example: Refreshing state...

  Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
    - destroy

  Terraform will perform the following actions:

    # tidbcloud_dedicated_network_container.example will be destroyed
    # (because tidbcloud_dedicated_network_container.example is not in configuration)
    - resource "tidbcloud_dedicated_network_container" "example" {
        - cidr_notation        = "172.16.16.0/21" -> null
        - cloud_provider       = "aws" -> null
        - labels               = {
            - "tidb.cloud/project" = "1372813089454000000"
          } -> null
        - network_container_id = "1934235512696000000" -> null
        - project_id           = "1372813089454000000" -> null
        - region_display_name  = "Seoul (ap-northeast-2)" -> null
        - region_id            = "aws-ap-northeast-2" -> null
        - state                = "INACTIVE" -> null
          # (1 unchanged attribute hidden)
      }

  Plan: 0 to add, 0 to change, 1 to destroy.

  Do you want to perform these actions?
    Terraform will perform the actions described above.
    Only 'yes' will be accepted to approve.

    Enter a value: yes

  tidbcloud_dedicated_network_container.example: Destroying...
  tidbcloud_dedicated_network_container.example: Destruction complete after 2s

  Apply complete! Resources: 0 added, 0 changed, 1 destroyed.
```

ここで、 `terraform show`コマンドを実行すると、リソースがクリアされているため、管理対象リソースは表示されません。

    $ terraform show

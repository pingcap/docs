---
title: Migrate Cluster Resource to Serverless or Dedicated Cluster Resource
summary: クラスター リソースをサーバーレスまたは専用のクラスター リソースに移行する方法を学習します。
---

# クラスタリソースをサーバーレスまたは専用クラスタリソースに移行する {#migrate-cluster-resource-to-serverless-or-dedicated-cluster-resource}

TiDB Cloud Terraform Provider v0.4.0 以降では、 `tidbcloud_cluster`リソースが`tidbcloud_serverless_cluster`と`tidbcloud_dedicated_cluster` 2 つの新しいリソースに置き換えられます。TiDB TiDB Cloud Terraform Provider v0.4.0 以降のバージョンをご利用の場合は、このドキュメントに従って`tidbcloud_cluster`リソースを`tidbcloud_serverless_cluster`または`tidbcloud_dedicated_cluster`リソースに移行できます。

> **ヒント：**
>
> このドキュメントの手順では、Terraform の構成生成機能を使用して、クラスターリソースの`.tf`構成を自動的に再作成することで、移行プロセスを簡素化します。詳細については、Terraform ドキュメントの[構成の生成](https://developer.hashicorp.com/terraform/language/import/generating-configuration)参照してください。

## 前提条件 {#prerequisites}

-   [TiDB Cloud Terraform プロバイダー v0.4.0 以降](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest)にアップグレード

## ステップ1. 移行する<code>tidbcloud_cluster</code>リソースを特定する {#step-1-identify-the-code-tidbcloud-cluster-code-resource-to-migrate}

1.  すべての`tidbcloud_cluster`リソースを一覧表示します:

    ```shell
    terraform state list | grep "tidbcloud_cluster"
    ```

2.  移行するターゲット クラスター リソースを選択し、後で使用するためにクラスター`id`を取得します。

    ```shell
    terraform state show ${your_target_cluster_resource} | grep ' id '
    ```

## ステップ2. Terraform状態から既存のリソースを削除する {#step-2-remove-the-existing-resource-from-the-terraform-state}

ターゲット クラスター リソースを Terraform 状態から削除します。

```shell
terraform state rm ${your_target_cluster_resource}
```

## ステップ3. ターゲットクラスタリソースの構成を削除する {#step-3-delete-the-configuration-of-your-target-cluster-resource}

`.tf`ファイルで、ターゲット クラスター リソースの構成を見つけて、対応するコードを削除します。

## ステップ4. 新しいサーバーレスまたは専用クラスターリソースのインポートブロックを追加する {#step-4-add-an-import-block-for-the-new-serverless-or-dedicated-cluster-resource}

-   ターゲット クラスターがTiDB Cloud Serverless の場合は、次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` [ステップ1](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate)から取得したクラスター ID に置き換えます。

        # TiDB Cloud Serverless
        import {
          to = tidbcloud_serverless_cluster.example
          id = "${id}"
        }

-   ターゲット クラスターがTiDB Cloud Dedicated の場合は、次のインポート ブロックを`.tf`ファイルに追加し、 `example`目的のリソース名に置き換え、 `${id}` [ステップ1](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate)から取得したクラスター ID に置き換えます。

        # TiDB Cloud Dedicated
        import {
          to = tidbcloud_dedicated_cluster.example
          id = "${id}"
        }

## ステップ5. 新しい構成ファイルを生成する {#step-5-generate-the-new-configuration-file}

インポート ブロックに従って、新しいサーバーレスまたは専用クラスター リソースの新しい構成ファイルを生成します。

```shell
terraform plan -generate-config-out=generated.tf
```

上記のコマンドでは、既存の`.tf`名を指定しないでください。指定した場合、Terraform はエラーを返します。

## ステップ6. 生成された構成を確認して適用する {#step-6-review-and-apply-the-generated-configuration}

生成された構成ファイルを確認し、ニーズを満たしていることを確認してください。必要に応じて、このファイルの内容を任意の場所に移動することもできます。

次に、 `terraform apply`実行してインフラストラクチャをインポートします。適用後の出力例は次のとおりです。

```shell
tidbcloud_serverless_cluster.example: Importing... 
tidbcloud_serverless_cluster.example: Import complete 

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```

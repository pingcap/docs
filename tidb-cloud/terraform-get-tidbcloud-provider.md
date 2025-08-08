---
title: Get TiDB Cloud Terraform Provider
summary: TiDB Cloud Terraform Provider を取得する方法を学びます。
---

# TiDB Cloud Terraform プロバイダーを入手する {#get-tidb-cloud-terraform-provider}

このドキュメントでは、 TiDB Cloud Terraform Provider を取得する方法を学習します。

## 前提条件 {#prerequisites}

[TiDB CloudTerraform プロバイダーの概要](/tidb-cloud/terraform-tidbcloud-provider-overview.md#requirements)の要件が満たされていることを確認してください。

## ステップ1. Terraformをインストールする {#step-1-install-terraform}

TiDB Cloud Terraform Provider が[Terraform レジストリ](https://registry.terraform.io/)にリリースされました。Terraform (&gt;=1.0) をインストールするだけです。

macOS の場合、次の手順に従ってHomebrewを使用して Terraform をインストールできます。

1.  必要なすべてのHomebrewパッケージを含むリポジトリである HashiCorp tap をインストールします。

    ```shell
    brew tap hashicorp/tap
    ```

2.  `hashicorp/tap/terraform`で Terraform をインストールします。

    ```shell
    brew install hashicorp/tap/terraform
    ```

その他のオペレーティング システムについては、手順[Terraform ドキュメント](https://learn.hashicorp.com/tutorials/terraform/install-cli)参照してください。

## ステップ2. APIキーを作成する {#step-2-create-an-api-key}

TiDB Cloud APIはHTTPダイジェスト認証を使用します。これにより、秘密鍵がネットワーク経由で送信されるのを防ぎます。

現在、 TiDB Cloud Terraform Provider は API キーの管理をサポートしていません。そのため、 [TiDB Cloudコンソール](https://tidbcloud.com/project/clusters)で API キーを作成する必要があります。

詳細な手順については、 [TiDB Cloud API ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)参照してください。

## ステップ3. TiDB Cloud Terraform Providerをダウンロードする {#step-3-download-tidb-cloud-terraform-provider}

1.  `main.tf`ファイルを作成します。

        terraform {
          required_providers {
            tidbcloud = {
              source = "tidbcloud/tidbcloud"
              version = "~> 0.3.0"
            }
          }
          required_version = ">= 1.0.0"
        }

    -   `source`属性は、 [Terraform レジストリ](https://registry.terraform.io/)からダウンロードする対象の Terraform プロバイダーを指定します。
    -   `version`属性はオプションで、Terraformプロバイダのバージョンを指定します。指定されていない場合は、デフォルトで最新のプロバイダバージョンが使用されます。
    -   `required_version`はオプションで、Terraform のバージョンを指定します。指定されていない場合は、デフォルトで最新の Terraform バージョンが使用されます。

2.  `terraform init`コマンドを実行して、Terraform Registry からTiDB Cloud Terraform Provider をダウンロードします。

        $ terraform init

        Initializing the backend...

        Initializing provider plugins...
        - Reusing previous version of tidbcloud/tidbcloud from the dependency lock file
        - Using previously-installed tidbcloud/tidbcloud v0.1.0

        Terraform has been successfully initialized!

        You may now begin working with Terraform. Try running "terraform plan" to see
        any changes that are required for your infrastructure. All Terraform commands
        should now work.

        If you ever set or change modules or backend configuration for Terraform,
        rerun this command to reinitialize your working directory. If you forget, other
        commands will detect it and remind you to do so if necessary.

## ステップ4. APIキーを使用してTiDB Cloud Terraform Providerを構成する {#step-4-configure-tidb-cloud-terraform-provider-with-the-api-key}

`main.tf`ファイルを次のように設定できます。

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

`public_key`と`private_key` APIキーの公開鍵と秘密鍵です。環境変数を通して渡すこともできます。

    export TIDBCLOUD_PUBLIC_KEY=${public_key}
    export TIDBCLOUD_PRIVATE_KEY=${private_key}

これで、 TiDB Cloud Terraform プロバイダーを使用できるようになります。

## ステップ5. 同期構成でTiDB Cloud Terraform Providerを構成する {#step-5-configure-tidb-cloud-terraform-provider-with-sync-configuration}

Terraform プロバイダー (&gt;= 0.3.0) は、オプションのパラメーター`sync`サポートします。

`sync`を`true`に設定すると、リソースを同期的に作成、更新、削除できます。以下に例を示します。

    provider "tidbcloud" {
      public_key = "your_public_key"
      private_key = "your_private_key"
    }

`sync` ～ `true`設定が推奨されますが、 `sync`現在クラスターリソースでのみ機能することに注意してください。他のリソースに対して同期操作が必要な場合は、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)してください。

## 次のステップ {#next-step}

[クラスターリソース](/tidb-cloud/terraform-use-cluster-resource.md)を使用してクラスターの管理を開始します。

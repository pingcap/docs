---
title: Get TiDB Cloud Terraform Provider
summary: Learn how to get TiDB Cloud Terraform Provider.
---

# TiDB Cloud Terraform プロバイダーを入手する {#get-tidb-cloud-terraform-provider}

このドキュメントでは、 TiDB Cloud Terraform Provider を取得する方法を学習します。

## 前提条件 {#prerequisites}

[TiDB Cloud Terraform プロバイダーの概要](/tidb-cloud/terraform-tidbcloud-provider-overview.md#requirements)の要件が満たされていることを確認してください。

## ステップ 1. Terraform をインストールする {#step-1-install-terraform}

TiDB Cloud Terraform プロバイダーが[Terraform レジストリ](https://registry.terraform.io/)にリリースされました。必要なのは、Terraform (&gt;=1.0) をインストールすることだけです。

macOS の場合は、次の手順に従ってHomebrewを使用して Terraform をインストールできます。

1.  必要なすべてのHomebrewパッケージを含むリポジトリである HashiCorp Tap をインストールします。

    ```shell
    brew tap hashicorp/tap
    ```

2.  `hashicorp/tap/terraform`で Terraform をインストールします。

    ```shell
    brew install hashicorp/tap/terraform
    ```

他のオペレーティング システムの手順については、 [Terraform ドキュメント](https://learn.hashicorp.com/tutorials/terraform/install-cli)を参照してください。

## ステップ 2. API キーを作成する {#step-2-create-an-api-key}

TiDB CloudAPI は HTTP ダイジェスト認証を使用します。秘密キーがネットワーク経由で送信されるのを防ぎます。

現在、 TiDB Cloud Terraform Provider は API キーの管理をサポートしていません。したがって、 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)で API キーを作成する必要があります。

詳細な手順については、 [TiDB CloudAPI ドキュメント](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)を参照してください。

## ステップ 3. TiDB Cloud Terraform プロバイダーをダウンロードする {#step-3-download-tidb-cloud-terraform-provider}

1.  `main.tf`ファイルを作成します。

        terraform {
          required_providers {
            tidbcloud = {
              source = "tidbcloud/tidbcloud"
              version = "~> 0.1.0"
            }
          }
          required_version = ">= 1.0.0"
        }

    -   `source`属性は、ダウンロード元のターゲット Terraform プロバイダーを指定します。 [Terraform レジストリ](https://registry.terraform.io/) 。
    -   `version`属性はオプションで、Terraform プロバイダーのバージョンを指定します。指定しない場合は、最新のプロバイダーのバージョンがデフォルトで使用されます。
    -   `required_version`はオプションで、Terraform のバージョンを指定します。指定しない場合は、デフォルトで最新の Terraform バージョンが使用されます。

2.  `terraform init`コマンドを実行して、Terraform レジストリからTiDB Cloud Terraform Provider をダウンロードします。

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

## ステップ 4. API キーを使用してTiDB Cloud Terraform プロバイダーを構成する {#step-4-configure-tidb-cloud-terraform-provider-with-the-api-key}

`main.tf`ファイルは次のように設定できます。

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

`public_key`と`private_key`は API キーの公開キーと秘密キーです。環境変数を介して渡すこともできます。

    export TIDBCLOUD_PUBLIC_KEY = ${public_key}
    export TIDBCLOUD_PRIVATE_KEY = ${private_key}

これで、 TiDB Cloud Terraform プロバイダーを使用できるようになりました。

## 次のステップ {#next-step}

[クラスターリソース](/tidb-cloud/terraform-use-cluster-resource.md)を使用してクラスターを管理することから始めます。

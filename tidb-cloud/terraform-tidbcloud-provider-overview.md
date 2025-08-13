---
title: Terraform Integration Overview
summary: Terraform を使用してTiDB Cloudリソースを作成、管理、更新します。
---

# Terraform 統合の概要 {#terraform-integration-overview}

[テラフォーム](https://www.terraform.io/)は、人間が読める構成ファイルでクラウド リソースと自己ホスト リソースの両方を定義でき、バージョン管理、再利用、共有できるコード ツールとしてのインフラストラクチャです。

[TiDB CloudTerraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud) 、Terraform を使用してクラスター、バックアップ、リストアなどのTiDB Cloudリソースを管理できるようにするプラグインです。

リソースのプロビジョニングとインフラストラクチャ ワークフローを自動化する簡単な方法を探している場合は、次の機能を提供するTiDB Cloud Terraform Provider を試してみてください。

-   プロジェクト情報を取得します。
-   サポートされているクラウド プロバイダー、リージョン、ノード サイズなどのクラスター仕様情報を取得します。
-   クラスターの作成、スケーリング、一時停止、再開など、TiDB クラスターを管理します。
-   クラスターのバックアップを作成および削除します。
-   クラスターの復元タスクを作成します。

## 要件 {#requirements}

-   [TiDB Cloudアカウント](https://tidbcloud.com/free-trial)
-   [Terraformバージョン](https://www.terraform.io/downloads.html) &gt;= 1.0
-   [Goバージョン](https://golang.org/doc/install) &gt;= 1.18 (ローカルで[TiDB CloudTerraform プロバイダー](https://github.com/tidbcloud/terraform-provider-tidbcloud)ビルドする場合にのみ必要)

## サポートされているリソースとデータソース {#supported-resources-and-data-sources}

[リソース](https://www.terraform.io/language/resources)と[データソース](https://www.terraform.io/language/data-sources) 、Terraform 言語で最も重要な 2 つの要素です。

TiDB Cloud は次のリソースとデータ ソースをサポートしています。

-   リソース

    -   `tidbcloud_cluster`
    -   `tidbcloud_backup`
    -   `tidbcloud_restore`
    -   `tidbcloud_import`

-   データソース

    -   `tidbcloud_projects`
    -   `tidbcloud_cluster_specs`
    -   `tidbcloud_clusters`
    -   `tidbcloud_restores`
    -   `tidbcloud_backups`

リソースとデータ ソースの使用可能なすべての構成を取得するには、こちら[構成ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

## 次のステップ {#next-step}

-   [Terraformについて詳しくはこちら](https://www.terraform.io/docs)
-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md)
-   [`tidbcloud_serverless_cluster`リソースを使用する](/tidb-cloud/terraform-use-serverless-cluster-resource.md)
-   [`tidbcloud_dedicated_cluster`リソースを使用する](/tidb-cloud/terraform-use-dedicated-cluster-resource.md)
-   [`tidbcloud_backup`リソースを使用する](/tidb-cloud/terraform-use-backup-resource.md)
-   [`tidbcloud_restore`リソースを使用する](/tidb-cloud/terraform-use-restore-resource.md)

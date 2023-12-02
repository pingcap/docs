---
title: Terraform Integration Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform.
---

# Terraform 統合の概要 {#terraform-integration-overview}

[テラフォーム](https://www.terraform.io/)は、コードとしてのインフラストラクチャ ツールであり、クラウド リソースとセルフホスト リソースの両方を、バージョン管理、再利用、共有できる人間が判読できる構成ファイルで定義できます。

[TiDB CloudTerraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud)は、Terraform を使用して、クラスター、バックアップ、復元などのTiDB Cloudリソースを管理できるようにするプラグインです。

リソース プロビジョニングとインフラストラクチャ ワークフローを自動化する簡単な方法を探している場合は、次の機能を提供するTiDB Cloud Terraform Provider を試すことができます。

-   プロジェクト情報を取得します。
-   サポートされているクラウドプロバイダー、リージョン、ノードサイズなどのクラスター仕様情報を取得します。
-   クラスターの作成、スケーリング、一時停止、再開など、TiDB クラスターを管理します。
-   クラスターのバックアップを作成および削除します。
-   クラスターの復元タスクを作成します。

## 要件 {#requirements}

-   [TiDB Cloudアカウント](https://tidbcloud.com/free-trial)
-   [Terraform バージョン](https://www.terraform.io/downloads.html) &gt;= 1.0
-   [Goのバージョン](https://golang.org/doc/install) &gt;= 1.18 (ローカルで[TiDB CloudTerraform プロバイダー](https://github.com/tidbcloud/terraform-provider-tidbcloud)をビルドする場合にのみ必要)

## サポートされているリソースとデータソース {#supported-resources-and-data-sources}

[リソース](https://www.terraform.io/language/resources)と[データソース](https://www.terraform.io/language/data-sources)は、Terraform 言語の 2 つの最も重要な要素です。

TiDB Cloud は、次のリソースとデータ ソースをサポートします。

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

リソースとデータ ソースで使用可能なすべての構成を取得するには、この[設定ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)を参照してください。

## 次のステップ {#next-step}

-   [Terraform について詳しく見る](https://www.terraform.io/docs)
-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md)
-   [クラスタリソースの使用](/tidb-cloud/terraform-use-cluster-resource.md)
-   [バックアップリソースの使用](/tidb-cloud/terraform-use-backup-resource.md)
-   [復元リソースの使用](/tidb-cloud/terraform-use-restore-resource.md)

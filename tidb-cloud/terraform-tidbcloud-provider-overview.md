---
title: Terraform Integration Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform.
---

# Terraform 統合の概要 {#terraform-integration-overview}

[テラフォーム](https://www.terraform.io/)はコード ツールとしてのインフラストラクチャであり、バージョン管理、再利用、共有が可能な、人間が判読できる構成ファイルでクラウドとオンプレミスの両方のリソースを定義できます。

[TiDB Cloud Terraform プロバイダー](https://registry.terraform.io/providers/tidbcloud/tidbcloud)は、Terraform を使用してクラスター、バックアップ、復元などのTiDB Cloudリソースを管理できるようにするプラグインです。

リソースのプロビジョニングとインフラストラクチャのワークフローを自動化する簡単な方法を探している場合は、次の機能を提供するTiDB Cloud Terraform Provider を試すことができます。

-   プロジェクト情報を取得します。
-   サポートされているクラウド プロバイダー、リージョン、ノード サイズなど、クラスターの仕様情報を取得します。
-   クラスターの作成、スケーリング、一時停止、再開など、TiDB クラスターを管理します。
-   クラスターのバックアップを作成および削除します。
-   クラスターの復元タスクを作成します。

## 要件 {#requirements}

-   [TiDB Cloudアカウント](https://tidbcloud.com/free-trial)
-   [Terraform バージョン](https://www.terraform.io/downloads.html) &gt;= 1.0
-   [バージョンを行く](https://golang.org/doc/install) &gt;= 1.18 ( [TiDB Cloud Terraform プロバイダー](https://github.com/tidbcloud/terraform-provider-tidbcloud)ローカルでビルドする場合にのみ必要)

## サポートされているリソースとデータ ソース {#supported-resources-and-data-sources}

[資力](https://www.terraform.io/language/resources)と[データソース](https://www.terraform.io/language/data-sources)は、Terraform 言語で最も重要な 2 つの要素です。

TiDB Cloud は、次のリソースとデータ ソースをサポートしています。

-   資力

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

リソースとデータ ソースで使用可能なすべての構成を取得するには、この[構成ドキュメント](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

## 次のステップ {#next-step}

-   [Terraform の詳細](https://www.terraform.io/docs)
-   [TiDB Cloud Terraform プロバイダーを入手する](/tidb-cloud/terraform-get-tidbcloud-provider.md)
-   [クラスタリソースを使用する](/tidb-cloud/terraform-use-cluster-resource.md)
-   [バックアップ リソースを使用する](/tidb-cloud/terraform-use-backup-resource.md)
-   [復元リソースを使用](/tidb-cloud/terraform-use-restore-resource.md)

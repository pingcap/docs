---
title: Terraform Integration Overview
summary: Create, manage, and update your TiDB Cloud resources through Terraform.
---

# Terraform 統合の概要 {#terraform-integration-overview}

[<a href="https://www.terraform.io/">テラフォーム</a>](https://www.terraform.io/)は、コードとしてのインフラストラクチャ ツールであり、これを使用すると、バージョン管理、再利用、共有が可能な人間が判読できる構成ファイルでクラウド リソースとオンプレミス リソースの両方を定義できます。

[<a href="https://registry.terraform.io/providers/tidbcloud/tidbcloud">TiDB CloudTerraform プロバイダー</a>](https://registry.terraform.io/providers/tidbcloud/tidbcloud)は、Terraform を使用して、クラスター、バックアップ、復元などのTiDB Cloudリソースを管理できるようにするプラグインです。

リソース プロビジョニングとインフラストラクチャ ワークフローを自動化する簡単な方法を探している場合は、次の機能を提供するTiDB Cloud Terraform Provider を試すことができます。

-   プロジェクト情報を取得します。
-   サポートされているクラウドプロバイダー、リージョン、ノードサイズなどのクラスター仕様情報を取得します。
-   クラスターの作成、スケーリング、一時停止、再開など、TiDB クラスターを管理します。
-   クラスターのバックアップを作成および削除します。
-   クラスターの復元タスクを作成します。

## 要件 {#requirements}

-   [<a href="https://tidbcloud.com/free-trial">TiDB Cloudアカウント</a>](https://tidbcloud.com/free-trial)
-   [<a href="https://www.terraform.io/downloads.html">Terraform バージョン</a>](https://www.terraform.io/downloads.html) &gt;= 1.0
-   [<a href="https://golang.org/doc/install">Goのバージョン</a>](https://golang.org/doc/install) &gt;= 1.18 (ローカルで[<a href="https://github.com/tidbcloud/terraform-provider-tidbcloud">TiDB CloudTerraform プロバイダー</a>](https://github.com/tidbcloud/terraform-provider-tidbcloud)をビルドする場合にのみ必要)

## サポートされているリソースとデータソース {#supported-resources-and-data-sources}

[<a href="https://www.terraform.io/language/resources">資力</a>](https://www.terraform.io/language/resources)と[<a href="https://www.terraform.io/language/data-sources">データソース</a>](https://www.terraform.io/language/data-sources)は、Terraform 言語の 2 つの最も重要な要素です。

TiDB Cloudは、次のリソースとデータ ソースをサポートします。

-   資力

    -   `tidbcloud_cluster`
    -   `tidbcloud_backup` (アップデートはサポートされていません)
    -   `tidbcloud_restore` (更新と削除はサポートされていません)

-   データソース

    -   `tidbcloud_projects`
    -   `tidbcloud_cluster_specs`
    -   `tidbcloud_clusters`
    -   `tidbcloud_restores`
    -   `tidbcloud_backups`

リソースとデータ ソースで使用可能なすべての構成を取得するには、この[<a href="https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs">設定ドキュメント</a>](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest/docs)参照してください。

## 次のステップ {#next-step}

-   [<a href="https://www.terraform.io/docs">Terraform について詳しく見る</a>](https://www.terraform.io/docs)
-   [<a href="/tidb-cloud/terraform-get-tidbcloud-provider.md">TiDB Cloud Terraform プロバイダーを入手する</a>](/tidb-cloud/terraform-get-tidbcloud-provider.md)
-   [<a href="/tidb-cloud/terraform-use-cluster-resource.md">クラスタリソースの使用</a>](/tidb-cloud/terraform-use-cluster-resource.md)
-   [<a href="/tidb-cloud/terraform-use-backup-resource.md">バックアップリソースの使用</a>](/tidb-cloud/terraform-use-backup-resource.md)
-   [<a href="/tidb-cloud/terraform-use-restore-resource.md">復元リソースの使用</a>](/tidb-cloud/terraform-use-restore-resource.md)

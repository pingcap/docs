---
title: Serverless Tier Limitations
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tierの制限 {#serverless-tier-limitations}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、Serverless Tierの制限について説明します。

私たちは、Serverless TierとDedicated Tierの間の機能のギャップを常に埋めています。これらの機能またはギャップ内の機能が必要な場合は、機能リクエストに[<a href="/tidb-cloud/select-cluster-tier.md#dedicated-tier">Dedicated Tier</a>](/tidb-cloud/select-cluster-tier.md#dedicated-tier)または[<a href="https://www.pingcap.com/contact-us/?from=en">お問い合わせ</a>](https://www.pingcap.com/contact-us/?from=en)を使用してください。

## 一般的な制限事項 {#general-limitations}

-   TiDB Cloudアカウントごとに、ベータ段階で最大 5 つの無料のServerless Tierクラスターを作成できます。
-   各Serverless Tierクラスターには次の制限があります。
    -   storageサイズは、OLTPstorageの場合は 5 GiB (論理サイズ)、OLAPstorageの場合は 5 GiB (論理サイズ) に制限されます。
    -   コンピューティング リソースは 1 vCPU と 1 GiB RAM に制限されます。
    -   **注**: 今後数か月間、無料のスターター プランの提供を継続しながら、追加のリソースとより高いパフォーマンスを目的とした従量制の料金プランを提供する予定です。今後のリリースでは、無料のServerless Tierの制限が変更される可能性があります。

## SQL {#sql}

-   現在、Serverless Tierクラスターでは[<a href="/time-to-live.md">生存時間 (TTL)</a>](/time-to-live.md)を使用できません。
-   [<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">`FLASHBACK CLUSTER TO TIMESTAMP`</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)構文はTiDB Cloud [<a href="/tidb-cloud/select-cluster-tier.md#serverless-tier-beta">Serverless Tier</a>](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターには適用されません。

## システムテーブル {#system-tables}

-   テーブル`CLUSTER_SLOW_QUERY` 、 `SLOW_QUERY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 、 `STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY`は、Serverless Tierクラスターでは使用できません。

## トランザクション {#transaction}

-   単一トランザクションの合計サイズは、ベータ段階ではServerless Tierで 10 MB 以下に設定されます。

## 繋がり {#connection}

-   [<a href="/tidb-cloud/connect-via-standard-connection.md">標準接続</a>](/tidb-cloud/connect-via-standard-connection.md)だけ使用できます。 [<a href="/tidb-cloud/set-up-private-endpoint-connections.md">プライベートエンドポイント</a>](/tidb-cloud/set-up-private-endpoint-connections.md)または[<a href="/tidb-cloud/set-up-vpc-peering-connections.md">VPC ピアリング</a>](/tidb-cloud/set-up-vpc-peering-connections.md)使用してServerless Tierクラスターに接続することはできません。
-   「IP アクセス リスト」はサポートされません。

## バックアップと復元 {#backup-and-restore}

-   現在、 [<a href="/tidb-cloud/backup-and-restore.md">バックアップと復元</a>](/tidb-cloud/backup-and-restore.md)はServerless Tierではサポートされていません。

## モニタリング {#monitoring}

-   [<a href="/tidb-cloud/built-in-monitoring.md">内蔵モニタリング</a>](/tidb-cloud/built-in-monitoring.md)は現在、Serverless Tierでは使用できません。
-   現在、Serverless Tierでは[<a href="/tidb-cloud/third-party-monitoring-integrations.md">サードパーティの監視統合</a>](/tidb-cloud/third-party-monitoring-integrations.md)を使用できません。

## 診断 {#diagnosis}

-   [<a href="/tidb-cloud/tune-performance.md">SQL診断</a>](/tidb-cloud/tune-performance.md)は現在、Serverless Tierでは使用できません。

## ストリームデータ {#stream-data}

-   現在、 [<a href="/tidb-cloud/changefeed-overview.md">チェンジフィード</a>](/tidb-cloud/changefeed-overview.md)はServerless Tierではサポートされていません。
-   現在、 [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)はServerless Tierではサポートされていません。

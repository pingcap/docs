---
title: Serverless Tier Limitations
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tierの制限 {#serverless-tier-limitations}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、Serverless Tierの制限について説明します。

私たちは、Serverless TierとDedicated Tierの間の機能のギャップを常に埋めています。これらの機能またはギャップ内の機能が必要な場合は、機能リクエストに[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)を使用してください。

## 一般的な制限事項 {#general-limitations}

-   TiDB Cloudアカウントごとに、ベータ段階で最大 5 つの無料のServerless Tierクラスターを作成できます。
-   各Serverless Tierクラスターには次の制限があります。
    -   storageサイズは、OLTPstorageの場合は 5 GiB (論理サイズ)、OLAPstorageの場合は 5 GiB (論理サイズ) に制限されます。
    -   コンピューティング リソースは 1 vCPU と 1 GiB RAM に制限されます。
    -   **注**: 今後数か月間、無料のスターター プランの提供を継続しながら、追加のリソースとより高いパフォーマンスを目的とした従量制の料金プランを提供する予定です。今後のリリースでは、無料のServerless Tierの制限が変更される可能性があります。

## SQL {#sql}

-   現在、Serverless Tierクラスターでは[生存時間 (TTL)](/time-to-live.md)を使用できません。
-   [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターには適用されません。

## システムテーブル {#system-tables}

-   テーブル`CLUSTER_SLOW_QUERY` 、 `SLOW_QUERY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 、 `STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY`は、Serverless Tierクラスターでは使用できません。

## トランザクション {#transaction}

-   単一トランザクションの合計サイズは、ベータ段階ではServerless Tierで 10 MB 以下に設定されます。

## 繋がり {#connection}

-   [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)使用してServerless Tierクラスターに接続することはできません。
-   「IP アクセス リスト」はサポートされません。

## バックアップと復元 {#backup-and-restore}

-   現在、 [バックアップと復元](/tidb-cloud/backup-and-restore.md)はServerless Tierではサポートされていません。

## モニタリング {#monitoring}

-   [内蔵モニタリング](/tidb-cloud/built-in-monitoring.md)は現在、Serverless Tierでは使用できません。
-   現在、Serverless Tierでは[サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)を使用できません。

## 診断 {#diagnosis}

-   [SQL診断](/tidb-cloud/tune-performance.md)は現在、Serverless Tierでは使用できません。

## ストリームデータ {#stream-data}

-   現在、 [チェンジフィード](/tidb-cloud/changefeed-overview.md)はServerless Tierではサポートされていません。
-   現在、 [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)はServerless Tierではサポートされていません。

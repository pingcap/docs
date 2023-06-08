---
title: TiDB Serverless Limitations and Quotas
summary: Learn about the limitations of TiDB Serverless.
---

# TiDB Serverlessの制限とクォータ {#tidb-serverless-limitations-and-quotas}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、TiDB Serverlessの制限について説明します。

私たちは常に、TiDB Serverless と TiDB Dended の間の機能のギャップを埋めています。これらの機能またはギャップ内の機能が必要な場合は、機能リクエストに[<a href="/tidb-cloud/select-cluster-tier.md#tidb-dedicated">TiDB Dedicated</a>](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)または[<a href="https://www.pingcap.com/contact-us/?from=en">お問い合わせ</a>](https://www.pingcap.com/contact-us/?from=en)を使用してください。

## 制限事項 {#limitations}

### SQL {#sql}

-   現在、TiDB Serverless クラスタでは[<a href="/time-to-live.md">生存時間 (TTL)</a>](/time-to-live.md)を使用できません。
-   [<a href="/sql-statements/sql-statement-flashback-to-timestamp.md">`FLASHBACK CLUSTER TO TIMESTAMP`</a>](/sql-statements/sql-statement-flashback-to-timestamp.md)構文は[<a href="/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta">TiDB Serverless</a>](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta)クラスターには適用されません。
-   [<a href="/functions-and-operators/miscellaneous-functions.md">`SLEEP()`関数</a>](/functions-and-operators/miscellaneous-functions.md)最大 300 秒のスリープ時間のみをサポートします。

### システムテーブル {#system-tables}

-   テーブル`CLUSTER_SLOW_QUERY` 、 `SLOW_QUERY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 、 `STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY`は、TiDB Serverless クラスタでは使用できません。

### トランザクション {#transaction}

-   TiDB Serverlessでは、ベータ段階では 1 つのトランザクションの合計サイズが 10 MB 以下に設定されます。

### 繋がり {#connection}

-   [<a href="/tidb-cloud/connect-via-standard-connection.md">標準接続</a>](/tidb-cloud/connect-via-standard-connection.md)と[<a href="/tidb-cloud/set-up-private-endpoint-connections.md">プライベートエンドポイント</a>](/tidb-cloud/set-up-private-endpoint-connections.md)のみ使用可能です。 [<a href="/tidb-cloud/set-up-vpc-peering-connections.md">VPC ピアリング</a>](/tidb-cloud/set-up-vpc-peering-connections.md)使用して TiDB Serverless クラスタに接続することはできません。
-   「IP アクセス リスト」はサポートされません。

### モニタリング {#monitoring}

-   [<a href="/tidb-cloud/third-party-monitoring-integrations.md">サードパーティの監視統合</a>](/tidb-cloud/third-party-monitoring-integrations.md)は現在、TiDB Serverlessでは使用できません。
-   [<a href="/tidb-cloud/tidb-cloud-events.md">クラスタイベント</a>](/tidb-cloud/tidb-cloud-events.md)は現在、TiDB Serverlessでは使用できません。
-   [<a href="/tidb-cloud/monitor-built-in-alerting.md">組み込みのアラート</a>](/tidb-cloud/monitor-built-in-alerting.md)は現在、TiDB Serverlessでは使用できません。

### 診断 {#diagnosis}

-   [<a href="/tidb-cloud/tune-performance.md#key-visualizer">キービジュアライザー</a>](/tidb-cloud/tune-performance.md#key-visualizer)は TiDB Serverlessでは使用できません。

### ストリームデータ {#stream-data}

-   [<a href="/tidb-cloud/changefeed-overview.md">チェンジフィード</a>](/tidb-cloud/changefeed-overview.md)は現在、TiDB Serverlessではサポートされていません。
-   [<a href="/tidb-cloud/migrate-from-mysql-using-data-migration.md">データ移行</a>](/tidb-cloud/migrate-from-mysql-using-data-migration.md)は現在、TiDB Serverlessではサポートされていません。

### メンテナンス期間 {#maintenance-window}

-   [<a href="/tidb-cloud/configure-maintenance-window.md">メンテナンス期間</a>](/tidb-cloud/configure-maintenance-window.md)は TiDB Serverlessでは使用できません。

## 使用量割り当て {#usage-quota}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB Serverless クラスタを作成できます。さらに TiDB Serverless クラスタを作成するには、クレジット カードを追加し、使用量を[<a href="/tidb-cloud/tidb-cloud-glossary.md#spend-limit">支出制限</a>](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

組織内の最初の 5 つの TiDB Serverless クラスタに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行storage: 5 GiB
-   [<a href="/tidb-cloud/tidb-cloud-glossary.md#request-unit">リクエストユニット (RU)</a>](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

リクエスト ユニット (RU) は、クエリまたはトランザクションのリソース消費を追跡するために使用される測定単位です。これは、データベース内の特定のリクエストを処理するために必要な計算リソースを見積もることができるメトリクスです。リクエスト単位は、 TiDB Cloud Serverless サービスの請求単位でもあります。

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[<a href="/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit">割り当てを増やす</a>](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit)されるまでスロットルされます。たとえば、クラスターのstorageが 5 GiB を超えると、単一トランザクションの最大サイズ制限が 10 MiB から 1 MiB に減ります。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [<a href="https://www.pingcap.com/tidb-cloud-serverless-pricing-details">TiDB Serverlessの料金詳細</a>](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

追加のクォータを使用して TiDB Serverless クラスタを作成する場合は、クラスター作成ページで使用制限を編集できます。詳細については、 [<a href="/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster">TiDB クラスターを作成する</a>](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster)を参照してください。

TiDB Serverlessを作成した後も、クラスターの概要ページで使用制限を確認および編集できます。詳細については、 [<a href="/tidb-cloud/manage-serverless-spend-limit.md">TiDB Serverless クラスタの支出制限を管理する</a>](/tidb-cloud/manage-serverless-spend-limit.md)を参照してください。

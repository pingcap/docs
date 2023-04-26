---
title: Serverless Tier Limitations and Quotas
summary: Learn about the limitations of TiDB Cloud Serverless Tier.
---

# Serverless Tierの制限と割り当て {#serverless-tier-limitations-and-quotas}

<!-- markdownlint-disable MD026 -->

このドキュメントでは、Serverless Tierの制限について説明します。

Serverless TierとDedicated Tierの間の機能のギャップを常に埋めています。ギャップ内でこれらの機能が必要な場合は、機能リクエストに[Dedicated Tier](/tidb-cloud/select-cluster-tier.md#dedicated-tier)または[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)を使用してください。

## 制限事項 {#limitations}

### SQL {#sql}

-   現在、 Serverless Tierクラスターでは[生存時間 (TTL)](/time-to-live.md)を使用できません。
-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)構文は、 TiDB Cloud [Serverless Tier](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta)クラスターには適用されません。
-   [`SLEEP()`関数](/functions-and-operators/miscellaneous-functions.md)最大 300 秒のスリープ時間のみをサポートします。

### システム テーブル {#system-tables}

-   表`CLUSTER_SLOW_QUERY` 、 `SLOW_QUERY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、 `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 、 `STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY`は、Serverless Tierクラスターでは使用できません。

### トランザクション {#transaction}

-   ベータ フェーズ中のServerless Tierでは、1 つのトランザクションの合計サイズが 10 MB を超えないように設定されています。

### 繋がり {#connection}

-   使用できるのは[標準接続](/tidb-cloud/connect-via-standard-connection.md)つだけです。 [プライベート エンドポイント](/tidb-cloud/set-up-private-endpoint-connections.md)または[VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)使用してServerless Tierクラスターに接続することはできません。
-   「IP アクセス リスト」はサポートされていません。

### モニタリング {#monitoring}

-   [サードパーティのモニタリング統合](/tidb-cloud/third-party-monitoring-integrations.md)は現在、Serverless Tierでは利用できません。
-   [クラスタイベント](/tidb-cloud/tidb-cloud-events.md)は現在、Serverless Tierでは利用できません。
-   [組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)は現在、Serverless Tierでは使用できません。

### 診断 {#diagnosis}

-   Serverless Tierでは[ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)と[キー ビジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)は使用できません。

### ストリームデータ {#stream-data}

-   現在、 Serverless Tierでは[チェンジフィード](/tidb-cloud/changefeed-overview.md)サポートされていません。
-   現在、 Serverless Tierでは[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)サポートされていません。

### メンテナンスウィンドウ {#maintenance-window}

-   Serverless Tierでは[メンテナンスウィンドウ](/tidb-cloud/configure-maintenance-window.md)は使用できません。

## 利用枠 {#usage-quota}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つのServerless Tierクラスターを作成できます。さらにServerless Tierクラスターを作成するには、クレジット カードを追加し、使用量を[使用制限](/tidb-cloud/tidb-cloud-glossary.md#spend-limit)に設定する必要があります。

組織内の最初の 5 つのServerless Tierクラスターについて、 TiDB Cloud は、次のようにそれぞれに無料の使用量割り当てを提供します。

-   行storage: 5 GiB
-   [リクエスト ユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 1 か月あたり 5,000 万 RU

要求単位 (RU) は、クエリまたはトランザクションのリソース消費を追跡するために使用される測定単位です。これは、データベースで特定のリクエストを処理するために必要な計算リソースを見積もることができるメトリックです。リクエスト単位は、 TiDB Cloudサーバーレス サービスの課金単位でもあります。

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、 [クォータを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spend-limit)または新しい月の開始時に使用量がリセットされるまで調整されます。たとえば、クラスターのstorageが 5 GiB を超えると、1 つのトランザクションの最大サイズ制限が 10 MiB から 1 MiB に減少します。

さまざまなリソース (読み取り、書き込み、SQL CPU、およびネットワーク エグレスを含む) の RU 消費、料金の詳細、調整された情報について詳しくは、 [TiDB CloudServerless Tierの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

追加のクォータを使用してServerless Tierクラスターを作成する場合は、クラスター作成ページで使用制限を編集できます。詳細については、 [TiDB クラスターを作成する](/tidb-cloud/create-tidb-cluster.md#step-4-create-a-tidb-cluster)を参照してください。

Serverless Tierを作成した後でも、クラスターの概要ページで使用制限を確認および編集できます。詳細については、 [Serverless Tierクラスターの使用制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)を参照してください。

---
title: TiDB Cloud Serverless Limitations and Quotas
summary: TiDB Cloud Serverless の制限について説明します。
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloudサーバーレスの制限とクォータ {#tidb-cloud-serverless-limitations-and-quotas}

<!-- markdownlint-disable MD026 -->

TiDB Cloud Serverless は、TiDB がサポートするほぼすべてのワークロードで動作しますが、TiDB Self-Managed またはTiDB Cloud Dedicated クラスターとTiDB Cloud Serverless クラスターの間には機能上の違いがいくつかあります。このドキュメントでは、TiDB Cloud Serverless の制限について説明します。

当社は、TiDB Cloud Serverless とTiDB Cloud Dedicated 間の機能ギャップを継続的に埋めています。ギャップにこれらの機能や機能が必要な場合は、機能リクエストに[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)または[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)使用してください。

## 制限事項 {#limitations}

### 監査ログ {#audit-logs}

-   [データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)は現在利用できません。

### 繋がり {#connection}

-   使用できるのは[パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)と[プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)のみです。5 [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)使用してTiDB Cloud Serverless クラスターに接続することはできません。
-   [IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)サポート。

### 暗号化 {#encryption}

-   TiDB Cloud Serverless クラスターに保存されるデータは、クラスターを管理するクラウド プロバイダーが提供する暗号化ツールを使用して暗号化されます。 [スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)場合、クラスター作成プロセス中にオプションの 2レイヤーの暗号化レイヤーが利用可能になり、保存時のデフォルトの暗号化を超える追加のセキュリティ レベルが提供されます。
-   [顧客管理暗号化キー (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek.md)使用は現在利用できません。

### メンテナンス期間 {#maintenance-window}

-   [メンテナンス期間](/tidb-cloud/configure-maintenance-window.md)は現在利用できません。

### 監視と診断 {#monitoring-and-diagnosis}

-   現在[サードパーティのモニタリング統合](/tidb-cloud/third-party-monitoring-integrations.md)はご利用いただけません。
-   [組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)は現在利用できません。
-   [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)は現在利用できません。
-   [インデックスインサイト](/tidb-cloud/tune-performance.md#index-insight-beta)は現在利用できません。

### セルフサービスアップグレード {#self-service-upgrades}

-   TiDB Cloud Serverless は、TiDB の完全に管理されたデプロイメントです。TiDB TiDB Cloud Serverless のメジャー バージョンとマイナー バージョンのアップグレードはTiDB Cloudによって処理されるため、ユーザーが開始することはできません。

### ストリームデータ {#stream-data}

-   [チェンジフィード](/tidb-cloud/changefeed-overview.md)は現在、 TiDB Cloud Serverless ではサポートされていません。
-   [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)は現在、 TiDB Cloud Serverless ではサポートされていません。

### 存続時間 (TTL) {#time-to-live-ttl}

-   TiDB Cloud Serverless では、テーブルの[`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job)属性は`15m`に固定されており、変更できません。つまり、 TiDB Cloud Serverless は、期限切れのデータをクリーンアップするために 15 分ごとにバックグラウンド ジョブをスケジュールします。

### その他 {#others}

-   トランザクションは30分以上継続することはできません。
-   SQL の制限の詳細については、 [制限されたSQL機能](/tidb-cloud/limited-sql-features.md)を参照してください。

## 使用量制限 {#usage-quota}

TiDB Cloudの各組織では、デフォルトで最大 5 つの[フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)を作成できます。さらにTiDB Cloud Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)作成する必要があります。

組織内の最初の 5 つのTiDB Cloud Serverless クラスターについては、無料かスケーラブルかに関係なく、 TiDB Cloud はそれぞれに対して次のように無料使用量の割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列型storage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 毎月5000万RU

リクエスト ユニット (RU) は、クエリまたはトランザクションのリソース消費を追跡するために使用される測定単位です。これは、データベース内の特定のリクエストを処理するために必要な計算リソースを見積もることができるメトリックです。リクエスト ユニットは、 TiDB Cloud Serverless サービスの課金単位でもあります。

クラスターが使用量の割り当てに達すると、新しい月の開始時に使用量がリセットされるか、 [割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)行われるまで、新しい接続の試行は直ちに拒否されます。割り当てに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)参照してください。

追加のクォータを持つTiDB Cloud Serverless クラスターを作成する場合は、スケーラブル クラスター プランを選択し、クラスター作成ページで使用制限を編集できます。詳細については、 [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)参照してください。

TiDB Cloud Serverless クラスターを作成した後でも、クラスターの概要ページで使用制限を確認および編集できます。詳細については、 [TiDB Cloudサーバーレス クラスターの支出制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)参照してください。

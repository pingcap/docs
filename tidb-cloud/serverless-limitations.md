---
title: TiDB Cloud Serverless Limitations and Quotas
summary: TiDB Cloud Serverless の制限について説明します。
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloud Serverless の制限とクォータ {#tidb-cloud-serverless-limitations-and-quotas}

<!-- markdownlint-disable MD026 -->

TiDB Cloud Serverlessは、TiDBがサポートするほぼすべてのワークロードで動作しますが、TiDBセルフマネージドまたはTiDB Cloud DedicatedクラスタとTiDB Cloud Serverlessクラスタの間には機能に若干の違いがあります。このドキュメントでは、TiDB Cloud Serverlessの制限事項について説明します。

TiDB Cloud ServerlessとTiDB Cloud Dedicated間の機能ギャップを常に埋めています。ギャップを埋める機能や性能が必要な場合は、機能リクエストに[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)または[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)ご記入ください。

## 制限事項 {#limitations}

### 監査ログ {#audit-logs}

-   [データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)は現在利用できません。

### 繋がり {#connection}

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)と[プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)のみ使用できます。5 [VPCピアリング](/tidb-cloud/set-up-vpc-peering-connections.md) TiDB Cloud Serverlessクラスターへの接続には使用できません。
-   [IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md)サポート。

### 暗号化 {#encryption}

-   TiDB Cloud Serverless クラスターに保存されるデータは、クラスターを管理するクラウドプロバイダーが提供する暗号化ツールを使用して暗号化されます[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)の場合、クラスター作成プロセス中にオプションで第2レイヤーの暗号化を利用でき、保存時のデフォルトの暗号化よりも高いレベルのセキュリティを実現できます。
-   [顧客管理暗号化キー（CMEK）](/tidb-cloud/tidb-cloud-encrypt-cmek.md)使用は現在利用できません。

### メンテナンスウィンドウ {#maintenance-window}

-   [メンテナンスウィンドウ](/tidb-cloud/configure-maintenance-window.md)は現在利用できません。

### 監視と診断 {#monitoring-and-diagnosis}

-   現在[サードパーティのモニタリング統合](/tidb-cloud/third-party-monitoring-integrations.md)はご利用いただけません。
-   [組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)は現在利用できません。
-   [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)は現在利用できません。
-   [インデックスインサイト](/tidb-cloud/tune-performance.md#index-insight-beta)は現在利用できません。

### セルフサービスアップグレード {#self-service-upgrades}

-   TiDB Cloud Serverlessは、TiDBのフルマネージドなデプロイメントです。TiDB TiDB Cloud ServerlessのメジャーバージョンとマイナーバージョンのアップグレードはTiDB Cloudによって処理されるため、ユーザーが開始することはできません。

### ストリームデータ {#stream-data}

-   現在、 TiDB Cloud Serverless では[チェンジフィード](/tidb-cloud/changefeed-overview.md)はサポートされていません。
-   現在、 TiDB Cloud Serverless では[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)はサポートされていません。

### 存続時間（TTL） {#time-to-live-ttl}

-   TiDB Cloud Serverlessでは、テーブルの属性[`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job) `15m`に固定されており、変更できません。つまり、 TiDB Cloud Serverlessは15分ごとにバックグラウンドジョブをスケジュールし、期限切れのデータをクリーンアップします。

### その他 {#others}

-   トランザクションは30分以上継続することはできません。
-   SQL の制限の詳細については、 [制限されたSQL機能](/tidb-cloud/limited-sql-features.md)を参照してください。

## 使用量制限 {#usage-quota}

TiDB Cloudでは、組織ごとに最大5つのクラスター（デフォルトでは[フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)を作成できます。TiDB TiDB Cloud Serverlessクラスターをさらに作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)クラスターを作成する必要があります。

組織内の最初の 5 つのTiDB Cloud Serverless クラスターについては、無料かスケーラブルかに関係なく、 TiDB Cloud は次のようにクラスターごとに無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月間5,000万RU

リクエストユニット（RU）は、クエリまたはトランザクションのリソース消費量を追跡するために使用される測定単位です。これは、データベース内の特定のリクエストを処理するために必要な計算リソースを見積もることができる指標です。リクエストユニットは、 TiDB Cloud Serverlessサービスの課金単位でもあります。

クラスターが使用量クォータに達すると、新しい月の開始時に使用量がリセットされるか、 [割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)なるまで、新規接続の試行は直ちに拒否されます。クォータに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)参照してください。

追加のクォータを持つTiDB Cloud Serverlessクラスターを作成する場合は、スケーラブルクラスタープランを選択し、クラスター作成ページで使用制限を編集できます。詳細については、 [TiDB Cloud Serverless クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)ご覧ください。

TiDB Cloud Serverless クラスターを作成した後でも、クラスターの概要ページで使用制限を確認および編集できます。詳細については、 [TiDB Cloudサーバーレス クラスターの支出制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)ご覧ください。

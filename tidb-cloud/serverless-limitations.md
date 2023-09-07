---
title: TiDB Serverless Limitations and Quotas
summary: Learn about the limitations of TiDB Serverless.
aliases: ['/tidbcloud/serverless-tier-limitations']
---

# TiDB サーバーレスの制限とクォータ {#tidb-serverless-limitations-and-quotas}

TiDB サーバーレスは、TiDB がサポートするほぼすべてのワークロードで動作しますが、TiDB セルフホストまたは TiDB 専用クラスターと TiDB サーバーレス クラスターの間には機能の違いがいくつかあります。このドキュメントでは、TiDB サーバーレスの制限について説明します。

私たちは常に、TiDB Serverless と TiDB Dended の間の機能のギャップを埋めています。これらの機能またはギャップ内の機能が必要な場合は、機能リクエストに[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)または[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)を使用してください。

## 制限事項 {#limitations}

### 監査ログ {#audit-logs}

-   [データベース監査ログ](/tidb-cloud/tidb-cloud-auditing.md)は現在利用できません。

### 繋がり {#connection}

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)と[プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)のみ使用可能です。 [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md)使用して TiDB サーバーレス クラスターに接続することはできません。
-   サポート[IPアクセスリスト](/tidb-cloud/configure-ip-access-list.md) 。

### 暗号化 {#encryption}

-   TiDB サーバーレス クラスターに保存されるデータは、クラスターを管理するクラウド プロバイダーが提供する暗号化ツールを使用して暗号化されます。ただし、TiDB サーバーレスは、インフラストラクチャ レベルの暗号化を超えて、ディスク上の保存データを保護するための追加のオプション手段を提供しません。
-   [顧客管理の暗号化キー (CMEK)](/tidb-cloud/tidb-cloud-encrypt-cmek.md)の使用は現在利用できません。

### メンテナンス期間 {#maintenance-window}

-   [メンテナンス期間](/tidb-cloud/configure-maintenance-window.md)は現在利用できません。

### 監視と診断 {#monitoring-and-diagnosis}

-   [サードパーティの監視統合](/tidb-cloud/third-party-monitoring-integrations.md)は現在利用できません。
-   [組み込みのアラート](/tidb-cloud/monitor-built-in-alerting.md)は現在利用できません。
-   [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)は現在利用できません。
-   [インデックスの洞察](/tidb-cloud/tune-performance.md#index-insight-beta)は現在利用できません。

### セルフサービスアップグレード {#self-service-upgrades}

-   TiDB サーバーレスは、TiDB のフルマネージド展開です。 TiDB Serverless のメジャー バージョンおよびマイナー バージョンのアップグレードはTiDB Cloudによって処理されるため、ユーザーが開始することはできません。

### ストリームデータ {#stream-data}

-   [チェンジフィード](/tidb-cloud/changefeed-overview.md)は現在、TiDB サーバーレスではサポートされていません。
-   [データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)は現在、TiDB サーバーレスではサポートされていません。

### その他 {#others}

-   [生存時間 (TTL)](/time-to-live.md)は現在利用できません。
-   トランザクションは30 分を超えて継続することはできません。
-   SQL の制限の詳細については、 [制限された SQL 機能](/tidb-cloud/limited-sql-features.md)を参照してください。

## 使用量割り当て {#usage-quota}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス クラスターを作成できます。さらに TiDB サーバーレス クラスターを作成するには、クレジット カードを追加し、使用量を[支出制限](/tidb-cloud/tidb-cloud-glossary.md#spending-limit)に設定する必要があります。

組織内の最初の 5 つの TiDB サーバーレス クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行ベースのstorage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

リクエスト ユニット (RU) は、クエリまたはトランザクションのリソース消費を追跡するために使用される測定単位です。これは、データベース内の特定のリクエストを処理するために必要な計算リソースを見積もることができるメトリクスです。リクエスト単位は、 TiDB Cloud Serverless サービスの請求単位でもあります。

クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)されるまでスロットルされます。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク下りなど) の RU 消費量、料金の詳細、および調整された情報の詳細については、 [TiDB サーバーレスの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details)を参照してください。

追加のクォータを使用して TiDB サーバーレス クラスターを作成する場合は、クラスター作成ページで使用制限を編集できます。詳細については、 [TiDB サーバーレスクラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)を参照してください。

TiDB サーバーレスを作成した後も、クラスターの概要ページで使用量制限を確認および編集できます。詳細については、 [TiDB サーバーレス クラスターの支出制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)を参照してください。

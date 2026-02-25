---
title: Limitations and Quotas of TiDB Cloud Starter and Essential
summary: TiDB Cloud Starter の制限について説明します。
aliases: ['/ja/tidbcloud/serverless-tier-limitations']
---

# TiDB Cloud StarterおよびEssentialの制限とクォータ {#limitations-and-quotas-of-tidb-cloud-starter-and-essential}

<!-- markdownlint-disable MD026 -->

TiDB Cloud StarterおよびEssentialは、TiDBがサポートするほぼすべてのワークロードで動作しますが、TiDB Self-ManagedまたはTiDB Cloud Dedicatedクラスタと比較して機能に若干の違いがあります。このドキュメントでは、TiDB Cloud StarterおよびTiDB Cloud Essentialの制限事項について説明します。

TiDB Cloud Starter/EssentialとTiDB Cloud Dedicated間の機能ギャップを継続的に埋めています。ギャップを埋める機能や性能が必要な場合は、機能リクエストに[TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)または[お問い合わせ](https://www.pingcap.com/contact-us/?from=en)使用してください。

## 制限事項 {#limitations}

### 監査ログ {#audit-logs}

-   [データベース監査ログ](/tidb-cloud/essential-database-audit-logging.md)は現在、 TiDB Cloud Starter クラスターでは使用できません。

### 繋がり {#connection}

-   [パブリックエンドポイント](/tidb-cloud/connect-via-standard-connection-serverless.md)と[プライベートエンドポイント](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)のみ使用できます。5 [VPC ピアリング](/tidb-cloud/set-up-vpc-peering-connections.md) TiDB Cloud StarterまたはTiDB Cloud Essentialクラスターに接続するためには使用できません。
-   プライベートエンドポイントのサポート[ファイアウォールルール](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md) 。
-   データベースクライアント接続は、30分以上開いたままになっていると、予期せず終了する可能性があります。これは、TiDBサーバーのシャットダウン、再起動、またはメンテナンス時に発生する可能性があり、アプリケーションの中断につながる可能性があります。この問題を回避するには、最大接続有効期間を設定してください。最初は5分から始め、テールレイテンシーに影響がある場合は徐々に増やすことを推奨します。詳細については、 [接続プールの推奨設定](/develop/dev-guide-connection-parameters.md)参照してください。
-   TiDB Cloud Starterクラスターでは、最大400の同時接続が可能です。1 [支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)設定すると、この制限は5,000に増加します。

> **注記：**
>
> [AWS Global Acceleratorの制限](https://docs.aws.amazon.com/global-accelerator/latest/dg/introduction-how-it-works.html#about-idle-timeout)ため、AWS のパブリックエンドポイント接続のアイドルタイムアウトは 340 秒です。同じ理由から、TCP キープアライブパケットを使用して接続を維持することはできません。

### 暗号化 {#encryption}

-   TiDB Cloud Starter またはTiDB Cloud Essential クラスターに保存されるデータは、クラスターを管理するクラウドプロバイダーが提供する暗号化ツールを使用して暗号化されます。TiDB TiDB Cloud Starter（使用制限が 0 より大きい）およびTiDB Cloud Essential クラスターでは、クラスター作成プロセス中にオプションで第 2レイヤーの暗号化を利用できます。これにより、保存時のデフォルトの暗号化よりも高いレベルのセキュリティが確保されます。
-   [顧客管理暗号鍵（CMEK）](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md)使用は現在利用できません。

### メンテナンスウィンドウ {#maintenance-window}

-   [メンテナンスウィンドウ](/tidb-cloud/configure-maintenance-window.md)は現在利用できません。

### 監視と診断 {#monitoring-and-diagnosis}

-   現在[サードパーティのモニタリング統合](/tidb-cloud/third-party-monitoring-integrations.md)はご利用いただけません。
-   [組み込みアラート](/tidb-cloud/monitor-built-in-alerting.md)は現在利用できません。
-   [キービジュアライザー](/tidb-cloud/tune-performance.md#key-visualizer)は現在利用できません。

### セルフサービスアップグレード {#self-service-upgrades}

-   TiDB Cloud StarterとTiDB Cloud Essentialは、TiDBのフルマネージドデプロイメントです。TiDB TiDB Cloud StarterとTiDB Cloud EssentialのメジャーバージョンとマイナーバージョンのアップグレードはTiDB Cloudによって処理されるため、ユーザーが開始することはできません。

### ストリームデータ {#stream-data}

-   現在、 TiDB Cloud Starter では[チェンジフィード](/tidb-cloud/changefeed-overview.md)はサポートされていません。
-   現在、 TiDB Cloud Starter では[データ移行](/tidb-cloud/migrate-from-mysql-using-data-migration.md)はサポートされていません。

### 存続時間（TTL） {#time-to-live-ttl}

-   TiDB Cloud StarterとTiDB Cloud Essentialでは、テーブルの属性[`TTL_JOB_INTERVAL`](/time-to-live.md#ttl-job)は`15m`に固定されており、変更できません。つまり、 TiDB Cloud StarterとTiDB Cloud Essentialは、期限切れのデータをクリーンアップするために15分ごとにバックグラウンドジョブをスケジュールします。

### その他 {#others}

-   トランザクションは30分以上継続することはできません。
-   SQL の制限の詳細については、 [制限されたSQL機能](/tidb-cloud/limited-sql-features.md)を参照してください。

## 使用量制限 {#usage-quota}

TiDB Cloudでは、組織ごとに最大5つのクラスター（デフォルトでは[無料のTiDB Cloud Starterクラスター](/tidb-cloud/select-cluster-tier.md#starter)を作成できます。TiDB TiDB Cloud Starterクラスターをさらに作成するには、クレジットカード情報と使用量に応じた[毎月の支出限度額を設定する](/tidb-cloud/manage-serverless-spend-limit.md)追加する必要があります。

組織内の最初の 5 つのTiDB Cloud Starter クラスターについては、 TiDB Cloud は次のようにクラスターごとに無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) : 月間5000万RU

リクエストユニット（RU）は、クエリまたはトランザクションのリソース消費量を追跡するために使用される測定単位です。これは、データベース内の特定のリクエストを処理するために必要な計算リソースを見積もることができる指標です。リクエストユニットは、 TiDB Cloud Starterサービスの課金単位でもあります。

クラスターが使用量のクォータに達すると、新しい接続試行はすべて拒否されます。これは、新しい月の開始時に使用量がリセットされるか、 [割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)なるまで継続されます。クォータに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。

さまざまなリソース (読み取り、書き込み、SQL CPU、ネットワーク送信など) の RU 消費量、価格の詳細、スロットル情報の詳細については、 [TiDB Cloud Starter の価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

追加のクォータを持つTiDB Cloud Starterクラスターを作成する場合は、クラスター作成ページで月間使用制限を設定できます。詳細については、 [TiDB Cloud Starter クラスターを作成する](/tidb-cloud/create-tidb-cluster-serverless.md)ご覧ください。

TiDB Cloud Starterクラスターを作成した後でも、クラスターの概要ページで使用制限を確認および編集できます。詳細については、 [TiDB Cloud Starter Clusters の支出制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)ご覧ください。

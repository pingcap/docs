---
title: TiDB Serverless FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Serverless.
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB サーバーレスに関するよくある質問 {#tidb-serverless-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB Serverless に関するよくある質問が記載されています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Serverless とは何ですか? {#what-is-tidb-serverless}

TiDB Serverless は、お客様とお客様の組織に完全な HTAP 機能を備えた TiDB データベースを提供します。これは、完全に管理された自動スケーリングの TiDB デプロイメントであり、データベースをすぐに使い始め、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングすることができます。

### TiDB Serverless を使い始めるにはどうすればよいですか? {#how-do-i-get-started-with-tidb-serverless}

5 分間の[TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)から始めましょう。

### TiDB Cloudで作成できる TiDB Serverless クラスターの数はいくつですか? {#how-many-tidb-serverless-clusters-can-i-create-in-tidb-cloud}

TiDB Cloudの各組織では、デフォルトで最大 5 [フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)のクラスターを作成できます。さらに TiDB Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)作成する必要があります。

### すべてのTiDB Cloud機能は TiDB Serverless で完全にサポートされていますか? {#are-all-tidb-cloud-features-fully-supported-on-tidb-serverless}

TiDB Cloud の機能の一部は、TiDB Serverless では部分的にサポートされているか、サポートされていません。詳細については、 [TiDB サーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md)参照してください。

### TiDB サーバーレスは、Google Cloud や Azure など、AWS 以外のクラウド プラットフォームでいつ利用できるようになりますか? {#when-will-tidb-serverless-be-available-on-cloud-platforms-other-than-aws-such-as-google-cloud-or-azure}

私たちは、Google Cloud や Azure などの他のクラウド プラットフォームに TiDB Serverless を拡張することに積極的に取り組んでいます。ただし、現在はギャップを埋め、すべての環境でシームレスな機能を確保することに重点を置いているため、正確なタイムラインは現時点ではわかりません。ご安心ください。私たちは、TiDB Serverless をより多くのクラウド プラットフォームで利用できるように懸命に取り組んでおり、進捗状況はコミュニティに随時お知らせします。

### TiDB Serverless が利用可能になる前にDeveloper Tierクラスターを作成しました。そのクラスターをまだ使用できますか? {#i-created-a-developer-tier-cluster-before-tidb-serverless-was-available-can-i-still-use-my-cluster}

はい、 Developer Tierクラスターは TiDB Serverless クラスターに自動的に移行されており、以前の使用状況に支障をきたすことなく、ユーザー エクスペリエンスが向上します。

## 課金と計測に関するよくある質問 {#billing-and-metering-faqs}

### リクエストユニットとは何ですか? {#what-are-request-units}

TiDB Serverless は従量課金モデルを採用しており、storageスペースとクラスターの使用に対してのみ料金を支払います。このモデルでは、SQL クエリ、一括操作、バックグラウンド ジョブなどのすべてのクラスター アクティビティが[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)で定量化されます。RU は、クラスターで開始されたリクエストのサイズと複雑さを表す抽象的な測定値です。詳細については、 [TiDB サーバーレスの価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)を参照してください。

### TiDB Serverless には無料プランはありますか? {#is-there-any-free-plan-available-for-tidb-serverless}

組織内の最初の 5 つの TiDB Serverless クラスターに対して、 TiDB Cloud はそれぞれに次の無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 毎月5000万RU

スケーラブル クラスターを使用している場合、無料割り当て量を超えた使用量には料金が発生します。無料クラスターの場合、無料割り当て量に達すると、スケーラブル クラスターにアップグレードするか、新しい月の開始時に使用量がリセットされるまで、このクラスターの読み取りおよび書き込み操作は制限されます。

詳細については[TiDB サーバーレス使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)参照してください。

### 無料プランの制限は何ですか? {#what-are-the-limitations-of-the-free-plan}

無料プランでは、スケーラブルでないリソースが原因でクラスターのパフォーマンスが制限されます。このため、クエリあたりのメモリ割り当てが 256 MiB に制限され、1 秒あたりのリクエスト ユニット (RU) に顕著なボトルネックが発生する可能性があります。クラスターのパフォーマンスを最大化し、これらの制限を回避するには、 [スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)にアップグレードします。

### ワークロードに必要な RU の数を見積もり、月間予算を計画するにはどうすればよいですか? {#how-can-i-estimate-the-number-of-rus-required-by-my-workloads-and-plan-my-monthly-budget}

個々の SQL ステートメントの RU 消費量を取得するには、SQL ステートメント[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)を使用できます。ただし、 `EXPLAIN ANALYZE`で返される RU 使用量には出力 RU が組み込まれていないことに注意してください。出力使用量はゲートウェイで個別に測定され、TiDBサーバーには認識されないためです。

クラスターで使用されている RU とstorageを取得するには、クラスターの概要ページの**[今月の**使用状況] ペインを表示します。このペインの過去のリソース使用状況データとリアルタイムのリソース使用状況を使用して、クラスターのリソース消費を追跡し、適切な使用制限を見積もることができます。無料の割り当てで要件を満たせない場合は、 [スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)にアップグレードして使用制限を編集できます。詳細については、 [TiDB サーバーレス使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)を参照してください。

### 消費される RU の数を最小限に抑えるためにワークロードを最適化するにはどうすればよいでしょうか? {#how-can-i-optimize-my-workload-to-minimize-the-number-of-rus-consumed}

[SQL パフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)のガイドラインに従って、クエリが最適なパフォーマンスを得るために慎重に最適化されていることを確認してください。また、RU の消費量を削減するには、送信トラフィックの量を最小限に抑えることも重要です。これを実現するには、クエリで必要な列と行のみを返すことをお勧めします。これにより、ネットワーク送信トラフィックが削減されます。これは、返される列と行を慎重に選択してフィルター処理することで実現でき、ネットワーク使用率が最適化されます。

### TiDB Serverless のstorageはどのように計測されますか? {#how-storage-is-metered-for-tidb-serverless}

storageは、 TiDB Serverless クラスターに保存されるデータの量に基づいて計測され、1 か月あたりの GiB 単位で測定されます。これは、すべてのテーブルとインデックスの合計サイズ (データ圧縮またはレプリカを除く) と、その月にデータが保存される時間数を掛けて計算されます。

### テーブルまたはデータベースをすぐに削除した後、storage使用量のサイズが変更されないのはなぜですか? {#why-does-the-storage-usage-size-remain-unchanged-after-dropping-a-table-or-database-immediately}

これは、TiDB が削除されたテーブルとデータベースを一定期間保持するためです。この保持期間により、これらのテーブルに依存するトランザクションが中断されることなく実行を継続できます。さらに、保持期間により[`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)機能[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)実現可能になり、誤って削除されたテーブルやデータベースを回復できるようになります。

### クエリをアクティブに実行していないのに RU が消費されるのはなぜですか? {#why-are-there-ru-consumptions-when-i-m-not-actively-running-any-queries}

RU の消費はさまざまなシナリオで発生する可能性があります。一般的なシナリオの 1 つは、TiDB インスタンス間のスキーマ変更の同期など、バックグラウンド クエリの実行時です。もう 1 つのシナリオは、スキーマの読み込みなど、特定の Web コンソール機能によってクエリが生成される場合です。これらのプロセスでは、明示的なユーザー トリガーがなくても RU が使用されます。

### ワークロードが安定しているのに、RU 使用量が急増するのはなぜですか? {#why-is-there-a-spike-in-ru-usage-when-my-workload-is-steady}

TiDB の必要なバックグラウンド ジョブが原因で、RU 使用量が急増する可能性があります。テーブルの自動分析や統計の再構築などのこれらのジョブは、最適化されたクエリ プランを生成するために必要です。

### クラスターの無料割り当てを使い果たしたり、使用制限を超えたりするとどうなりますか? {#what-happens-when-my-cluster-exhausts-its-free-quota-or-exceeds-its-spending-limit}

クラスターが無料割り当てまたは使用制限に達すると、割り当てが増加するか、新しい月の開始時に使用量がリセットされるまで、クラスターは新しい接続試行を直ちに拒否します。割り当てに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。詳細については、 [TiDB サーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md#usage-quota)を参照してください。

### データのインポート中に RU 使用量が急増するのはなぜですか? {#why-do-i-observe-spikes-in-ru-usage-while-importing-data}

TiDB Serverless クラスターのデータ インポート プロセス中、RU の消費はデータが正常にインポートされた場合にのみ発生するため、RU 使用量が急増します。

## Securityに関するよくある質問 {#security-faqs}

### TiDB Serverless は共有ですか、それとも専用ですか? {#is-my-tidb-serverless-shared-or-dedicated}

サーバーレス テクノロジーはマルチテナント向けに設計されており、すべてのクラスターで使用されるリソースは共有されます。分離されたインフラストラクチャとリソースを備えたマネージド TiDB サービスを取得するには、 [TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)にアップグレードできます。

### TiDB Serverless はどのようにしてセキュリティを確保しますか? {#how-does-tidb-serverless-ensure-security}

-   接続はトランスポート層Security(TLS) によって暗号化されます。TLS を使用して TiDB Serverless に接続する方法の詳細については、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
-   TiDB Serverless に保存されるすべてのデータは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。TiDB Serverless クラスターは、 TiDB Cloudで新しい TiDB バージョンがロールアウトされると自動的にアップグレードされます。クラスターで実行されている TiDB のバージョンは、 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。または、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB のバージョンを確認することもできます。

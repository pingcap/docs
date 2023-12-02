---
title: TiDB Serverless FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Serverless.
---

# TiDB サーバーレスに関するよくある質問 {#tidb-serverless-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB サーバーレスに関して最もよくある質問がリストされています。

## 一般的な FAQ {#general-faqs}

### TiDB サーバーレスとは​​何ですか? {#what-is-tidb-serverless}

TiDB サーバーレスは、あなたとあなたの組織に、完全な HTAP 機能を備えた TiDB データベースを提供します。これは TiDB のフルマネージドで自動スケーリングのデプロイメントであり、データベースの使用をすぐに開始し、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングすることができます。

### TiDB サーバーレスを使い始めるにはどうすればよいですか? {#how-do-i-get-started-with-tidb-serverless}

5 分間から始めましょう[TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md) 。

### TiDB Cloudでは TiDB サーバーレス クラスターをいくつ作成できますか? {#how-many-tidb-serverless-clusters-can-i-create-in-tidb-cloud}

TiDB Cloudの組織ごとに、デフォルトで最大 5 つの TiDB サーバーレス クラスターを作成できます。さらに TiDB サーバーレス クラスターを作成するには、クレジット カードを追加し、使用量を[支出制限](/tidb-cloud/tidb-cloud-glossary.md#spending-limit)に設定する必要があります。

### すべてのTiDB Cloud機能は TiDB サーバーレスで完全にサポートされていますか? {#are-all-tidb-cloud-features-fully-supported-on-tidb-serverless}

TiDB Cloud機能の一部は、TiDB サーバーレスで部分的にサポートされているか、サポートされていません。詳細については、 [TiDB サーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md)を参照してください。

### TiDB サーバーレスはいつ Google Cloud や Azure などの AWS 以外のクラウド プラットフォームで利用できるようになりますか? {#when-will-tidb-serverless-be-available-on-cloud-platforms-other-than-aws-such-as-google-cloud-or-azure}

私たちは、TiDB Serverless を Google Cloud や Azure などの他のクラウド プラットフォームに拡張することに積極的に取り組んでいます。ただし、現時点ではギャップを埋め、すべての環境でシームレスな機能を確保することに重点を置いているため、正確なスケジュールはありません。ご安心ください。私たちは TiDB Serverless をより多くのクラウド プラットフォームで利用できるようにするために懸命に取り組んでおり、進捗に合わせてコミュニティに常に最新の情報を提供していきます。

### TiDB サーバーレスが利用可能になる前に、Developer Tierクラスターを作成しました。クラスターを引き続き使用できますか? {#i-created-a-developer-tier-cluster-before-tidb-serverless-was-available-can-i-still-use-my-cluster}

はい、Developer Tierクラスターは TiDB サーバーレス クラスターに自動的に移行され、以前の使用状況を中断することなくユーザー エクスペリエンスが向上しました。

## 請求と計測に関するよくある質問 {#billing-and-metering-faqs}

### リクエストユニットとは何ですか? {#what-are-request-units}

TiDB サーバーレスは従量課金制モデルを採用しています。つまり、storageスペースとクラスターの使用量に対してのみ料金を支払います。このモデルでは、SQL クエリ、一括操作、バックグラウンド ジョブなどのすべてのクラスター アクティビティが[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)に定量化されます。 RU は、クラスター上で開始されたリクエストのサイズと複雑さの抽象的な測定値です。詳細については、 [TiDB サーバーレスの料金詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)を参照してください。

### TiDB サーバーレスで利用できる無料プランはありますか? {#is-there-any-free-plan-available-for-tidb-serverless}

組織内の最初の 5 つの TiDB サーバーレス クラスターに対して、 TiDB Cloud は各クラスターに次のように無料の使用量クォータを提供します。

-   行ベースのstorage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 月あたり 5,000 万 RU

無料割り当てを超えた使用には料金が発生します。クラスターの無料クォータに達すると、このクラスターでの読み取りおよび書き込み操作は、新しい月の初めに使用量が[割り当てを増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)されるまでスロットルされます。

詳細については、 [TiDB サーバーレスの使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)を参照してください。

### 無料プランの制限は何ですか? {#what-are-the-limitations-of-the-free-plan}

無料プランでは、クラスターのパフォーマンスは、実際のワークロードに基づいて 1 秒あたり最大 10,000 RU に制限されます。さらに、クエリごとのメモリ割り当ては 256 MiB に制限されています。クラスターのパフォーマンスを最大化するには、商用製品を[利用限度額を増やす](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit)で有効にすることを選択できます。

### ワークロードに必要な RU の数を見積もり、毎月の予算を計画するにはどうすればよいですか? {#how-can-i-estimate-the-number-of-rus-required-by-my-workloads-and-plan-my-monthly-budget}

個々の SQL ステートメントの RU 消費量を取得するには、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption) SQL ステートメントを使用できます。ただし、出力使用量はゲートウェイで個別に測定され、TiDBサーバーには認識されないため、 `EXPLAIN ANALYZE`で返される RU 使用量には出力 RU が含まれていないことに注意することが重要です。

クラスターで使用されている RU とstorageを取得するには、クラスターの概要ページの**[今月の使用量]**ペインを表示します。このペインに過去のリソース使用量データとリアルタイムのリソース使用量を表示することで、クラスターのリソース消費を追跡し、適切な使用制限を見積もることができます。無料割り当てが要件を満たせない場合は、支出制限を簡単に編集できます。詳細については、 [TiDB サーバーレス クラスターの支出制限を管理する](/tidb-cloud/manage-serverless-spend-limit.md)を参照してください。

### 消費される RU の数を最小限に抑えるためにワークロードを最適化するにはどうすればよいですか? {#how-can-i-optimize-my-workload-to-minimize-the-number-of-rus-consumed}

[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)のガイドラインに従って、最適なパフォーマンスが得られるようにクエリが慎重に最適化されていることを確認します。さらに、送信トラフィックの量を最小限に抑えることも、RU の消費量を削減するために重要です。これを実現するには、クエリで必要な列と行のみを返すことをお勧めします。これにより、ネットワーク下りトラフィックが削減されます。これは、返される列と行を慎重に選択してフィルタリングすることで実現でき、それによってネットワークの使用率が最適化されます。

### TiDB サーバーレスのstorageはどのように計測されますか? {#how-storage-is-metered-for-tidb-serverless}

storageは、TiDB サーバーレス クラスターに保存されているデータ量に基づいて測定され、月あたりの GiB 単位で測定されます。これは、すべてのテーブルとインデックス (データ圧縮またはレプリカを除く) の合計サイズに、その月にデータが保存されている時間数を乗算して計算されます。

### テーブルまたはデータベースをすぐに削除した後、storage使用量のサイズが変わらないのはなぜですか? {#why-does-the-storage-usage-size-remain-unchanged-after-dropping-a-table-or-database-immediately}

これは、TiDB が削除されたテーブルとデータベースを一定期間保持するためです。この保持期間により、これらのテーブルに依存するトランザクションは中断することなく実行を継続できます。さらに、保持期間により[`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) / [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)機能が実現可能になり、削除されたテーブルやデータベースが誤って削除された場合に回復できます。

### クエリをアクティブに実行していないときに RU が消費されるのはなぜですか? {#why-are-there-ru-consumptions-when-i-m-not-actively-running-any-queries}

RU の消費はさまざまなシナリオで発生する可能性があります。一般的なシナリオの 1 つは、TiDB インスタンス間でのスキーマ変更の同期など、バックグラウンド クエリ中です。もう 1 つのシナリオは、スキーマの読み込みなど、特定の Web コンソール機能がクエリを生成する場合です。これらのプロセスは、明示的なユーザー トリガーがなくても RU を使用します。

### ワークロードが安定しているのに、RU 使用量が急増するのはなぜですか? {#why-is-there-a-spike-in-ru-usage-when-my-workload-is-steady}

TiDB で必要なバックグラウンド ジョブが原因で、RU 使用量の急増が発生する可能性があります。テーブルの自動分析や統計の再構築などのこれらのジョブは、最適化されたクエリ プランを生成するために必要です。

### クラスターが無料クォータを使い果たすか、使用制限を超えるとどうなりますか? {#what-happens-when-my-cluster-exhausts-its-free-quota-or-exceeds-its-spending-limit}

クラスターが無料クォータまたは使用制限に達すると、クラスターは読み取りおよび書き込み操作にスロットル措置を適用します。これらの操作は、クォータが増加するか、新しい月の初めに使用量がリセットされるまで制限されます。詳細については、 [TiDB サーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md#usage-quota)を参照してください。

## Securityよくある質問 {#security-faqs}

### 私の TiDB サーバーレスは共有ですか、それとも専用ですか? {#is-my-tidb-serverless-shared-or-dedicated}

サーバーレス テクノロジーはマルチテナンシー向けに設計されており、すべてのクラスターで使用されるリソースが共有されます。分離されたインフラストラクチャとリソースを使用してマネージド TiDB サービスを利用するには、サービスを[TiDB専用](/tidb-cloud/select-cluster-tier.md#tidb-dedicated)にアップグレードします。

### TiDB サーバーレスはどのようにセキュリティを確保しますか? {#how-does-tidb-serverless-ensure-security}

-   接続は Transport Layer Security (TLS) によって暗号化されます。 TLS を使用して TiDB サーバーレスに接続する方法の詳細については、 [TiDB サーバーレスへの TLS 接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)を参照してください。
-   TiDB サーバーレス上のすべての永続データは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。TiDB サーバーレス クラスターは、 TiDB Cloudで新しい TiDB バージョンを展開すると自動的にアップグレードされます。クラスターが実行している TiDB のバージョンは[TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。あるいは、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`を使用して TiDB バージョンを確認することもできます。

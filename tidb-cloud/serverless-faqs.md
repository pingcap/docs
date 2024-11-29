---
title: TiDB Cloud Serverless FAQs
summary: TiDB Cloud Serverless に関するよくある質問 (FAQ) について説明します。
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB Cloudサーバーレスに関するよくある質問 {#tidb-cloud-serverless-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、 TiDB Cloud Serverless に関するよくある質問が記載されています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloud Serverless とは何ですか? {#what-is-tidb-cloud-serverless}

TiDB Cloud Serverless は、お客様とお客様の組織に完全な HTAP 機能を備えた TiDB データベースを提供します。これは、完全に管理された自動スケーリングの TiDB デプロイメントであり、データベースをすぐに使い始め、基盤となるノードを気にせずにアプリケーションを開発および実行し、アプリケーションのワークロードの変化に基づいて自動的にスケーリングすることができます。

### TiDB Cloud Serverless を使い始めるにはどうすればよいですか? {#how-do-i-get-started-with-tidb-cloud-serverless}

5 分間の[TiDB Cloudクイック スタート](/tidb-cloud/tidb-cloud-quickstart.md)から始めましょう。

### TiDB Cloudで作成できるTiDB Cloud Serverless クラスターの数はいくつですか? {#how-many-tidb-cloud-serverless-clusters-can-i-create-in-tidb-cloud}

TiDB Cloudの各組織では、デフォルトで最大 5 つの[フリークラスター](/tidb-cloud/select-cluster-tier.md#free-cluster-plan)を作成できます。さらにTiDB Cloud Serverless クラスターを作成するには、クレジットカードを追加し、使用量に応じて[スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)作成する必要があります。

### TiDB Cloud Serverless ではすべてのTiDB Cloud機能が完全にサポートされていますか? {#are-all-tidb-cloud-features-fully-supported-on-tidb-cloud-serverless}

TiDB Cloud の機能の一部は、 TiDB Cloud Serverless では部分的にサポートされているか、サポートされていません。詳細については、 [TiDB Cloudサーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md)参照してください。

### TiDB Cloud Serverless は、Google Cloud や Azure など、AWS 以外のクラウド プラットフォームでいつ利用できるようになりますか? {#when-will-tidb-cloud-serverless-be-available-on-cloud-platforms-other-than-aws-such-as-google-cloud-or-azure}

当社は、Google Cloud や Azure などの他のクラウド プラットフォームにTiDB Cloud Serverless を拡張することに積極的に取り組んでいます。ただし、現在はギャップを埋め、すべての環境でシームレスな機能を確保することに重点を置いているため、正確なタイムラインは現時点ではわかりません。ご安心ください。当社は、 TiDB Cloud Serverless をより多くのクラウド プラットフォームで利用できるように懸命に取り組んでおり、進捗状況はコミュニティに随時お知らせします。

### TiDB Cloud Serverless が利用可能になる前にDeveloper Tierクラスターを作成しました。クラスターをまだ使用できますか? {#i-created-a-developer-tier-cluster-before-tidb-cloud-serverless-was-available-can-i-still-use-my-cluster}

はい、 Developer TierクラスターはTiDB Cloud Serverless クラスターに自動的に移行されており、以前の使用状況に支障をきたすことなく、ユーザー エクスペリエンスが向上します。

### TiDB Cloud Serverless の列指向storageとは何ですか? {#what-is-columnar-storage-in-tidb-cloud-serverless}

TiDB Cloud Serverless の列指向storageは、行ベースstorageの追加レプリカとして機能し、強力な一貫性を保証します。データを行に格納する従来の行ベースstorageとは異なり、列指向storageはデータを列に整理し、データ分析タスクに最適化します。

列指向storageは、トランザクション ワークロードと分析ワークロードをシームレスに融合することで、TiDB のハイブリッド トランザクションおよび分析処理 (HTAP) 機能を有効にする重要な機能です。

列指向storageデータを効率的に管理するために、 TiDB Cloud Serverless は別個の柔軟なTiFlashエンジンを使用します。クエリ実行中、オプティマイザーはクラスターをガイドして、行ベース ストレージと列指向storageのどちらからデータを取得するかを自動的に決定します。

### TiDB Cloud Serverless で列指向storageを使用するのはいつですか? {#when-should-i-use-columnar-storage-in-tidb-cloud-serverless}

次のシナリオでは、 TiDB Cloud Serverless の列指向storageの使用を検討してください。

-   ワークロードには、効率的なデータスキャンと集約を必要とする分析タスクが含まれます。
-   特に分析ワークロードのパフォーマンス向上を優先します。
-   トランザクション処理 (TP) ワークロードのパフォーマンスへの影響を防ぐために、分析処理をトランザクション処理から分離する必要があります。個別の列型storageは、これらの異なるワークロード パターンを最適化するのに役立ちます。

このようなシナリオでは、列指向storageクエリのパフォーマンスが大幅に向上し、システム内の混合ワークロードに対してシームレスなエクスペリエンスを提供できます。

### TiDB Cloud Serverless で列指向storageを使用する方法は? {#how-to-use-columnar-storage-in-tidb-cloud-serverless}

TiDB Cloud Serverless での列指向storageの使用は、 TiFlashでの使用に似ています。テーブル レベルとデータベース レベルの両方で列指向storageを有効にできます。

-   テーブル レベル: テーブルにTiFlashレプリカを割り当てて、その特定のテーブルの列指向storageを有効にします。
-   データベース レベル: データベース全体で列型storageを使用するように、データベース内のすべてのテーブルのTiFlashレプリカを構成します。

テーブルにTiFlashレプリカが設定されると、TiDB は行ベースのstorageからそのテーブルの列ベースのstorageにデータを自動的に複製します。これにより、データの一貫性が確保され、分析クエリのパフォーマンスが最適化されます。

TiFlashレプリカの設定方法の詳細については、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)参照してください。

## 課金と計測に関するよくある質問 {#billing-and-metering-faqs}

### リクエストユニットとは何ですか? {#what-are-request-units}

TiDB Cloud Serverless は従量課金モデルを採用しており、storageスペースとクラスターの使用に対してのみ料金を支払います。このモデルでは、SQL クエリ、一括操作、バックグラウンド ジョブなどのすべてのクラスター アクティビティが[リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit)で定量化されます。RU は、クラスターで開始されたリクエストのサイズと複雑さを表す抽象的な測定値です。詳細については、 [TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-cloud-serverless-pricing-details/)参照してください。

### TiDB Cloud Serverless には無料プランはありますか? {#is-there-any-free-plan-available-for-tidb-cloud-serverless}

組織内の最初の 5 つのTiDB Cloud Serverless クラスターに対して、 TiDB Cloud はそれぞれに次の無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   [リクエストユニット (RU)](/tidb-cloud/tidb-cloud-glossary.md#request-unit) : 毎月5000万RU

スケーラブル クラスターを使用している場合、無料割り当て量を超えた使用量には料金が発生します。無料クラスターの場合、無料割り当て量に達すると、スケーラブル クラスターにアップグレードするか、新しい月の開始時に使用量がリセットされるまで、このクラスターの読み取りおよび書き込み操作は制限されます。

詳細については[TiDB Cloud Serverless 使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)参照してください。

### 無料プランの制限は何ですか? {#what-are-the-limitations-of-the-free-plan}

無料プランでは、スケーラブルでないリソースが原因でクラスターのパフォーマンスが制限されます。このため、クエリあたりのメモリ割り当てが 256 MiB に制限され、1 秒あたりのリクエスト ユニット (RU) に顕著なボトルネックが発生する可能性があります。クラスターのパフォーマンスを最大化し、これらの制限を回避するには、 [スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)にアップグレードします。

### ワークロードに必要な RU の数を見積もり、月間予算を計画するにはどうすればよいですか? {#how-can-i-estimate-the-number-of-rus-required-by-my-workloads-and-plan-my-monthly-budget}

個々の SQL ステートメントの RU 消費量を取得するには、SQL ステートメント[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)を使用できます。ただし、 `EXPLAIN ANALYZE`で返される RU 使用量には出力 RU が組み込まれていないことに注意してください。出力使用量はゲートウェイで個別に測定され、TiDBサーバーには認識されないためです。

クラスターで使用されている RU とstorageを取得するには、クラスターの概要ページの [**今月の使用状況]**ペインを表示します。このペインの過去のリソース使用状況データとリアルタイムのリソース使用状況を使用して、クラスターのリソース消費を追跡し、適切な使用制限を見積もることができます。無料の割り当てで要件を満たせない場合は、 [スケーラブルなクラスター](/tidb-cloud/select-cluster-tier.md#scalable-cluster-plan)にアップグレードして使用制限を編集できます。詳細については、 [TiDB Cloud Serverless 使用量割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)参照してください。

### 消費される RU の数を最小限に抑えるためにワークロードを最適化するにはどうすればよいでしょうか? {#how-can-i-optimize-my-workload-to-minimize-the-number-of-rus-consumed}

[SQL パフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)のガイドラインに従って、クエリが最適なパフォーマンスを得るために慎重に最適化されていることを確認します。RU を最も多く消費する SQL ステートメントを特定するには、クラスターの概要ページで**[診断] &gt; [SQL ステートメント]**に移動します。ここで、SQL 実行を観察し、**合計 RU**または**平均 RU**で並べ替えられた上位のステートメントを表示できます。詳細については、 [ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)参照してください。また、出力トラフィックの量を最小限に抑えることも、RU の消費量を削減するために重要です。これを実現するには、クエリで必要な列と行のみを返すことをお勧めします。これにより、ネットワークの出力トラフィックが削減されます。これは、返される列と行を慎重に選択してフィルター処理することで実現でき、それによってネットワーク使用率が最適化されます。

### TiDB Cloud Serverless のstorageはどのように計測されますか? {#how-storage-is-metered-for-tidb-cloud-serverless}

storageは、 TiDB Cloud Serverless クラスターに保存されるデータの量に基づいて計測され、1 か月あたりの GiB 単位で測定されます。これは、すべてのテーブルとインデックスの合計サイズ (データ圧縮またはレプリカを除く) と、その月にデータが保存される時間数を掛けて計算されます。

### テーブルまたはデータベースをすぐに削除した後、storage使用量のサイズが変更されないのはなぜですか? {#why-does-the-storage-usage-size-remain-unchanged-after-dropping-a-table-or-database-immediately}

これは[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) TiDB が削除されたテーブルとデータベースを一定期間保持するためです。この保持期間により、これらのテーブルに依存するトランザクションが中断されることなく実行を継続できます。さらに、保持期間により[`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)機能も実現可能になり、誤って削除されたテーブルやデータベースを回復できるようになります。

### クエリをアクティブに実行していないのに RU が消費されるのはなぜですか? {#why-are-there-ru-consumptions-when-i-m-not-actively-running-any-queries}

RU の消費はさまざまなシナリオで発生する可能性があります。一般的なシナリオの 1 つは、TiDB インスタンス間のスキーマ変更の同期など、バックグラウンド クエリの実行時です。もう 1 つのシナリオは、スキーマの読み込みなど、特定の Web コンソール機能によってクエリが生成される場合です。これらのプロセスでは、明示的なユーザー トリガーがなくても RU が使用されます。

### ワークロードが安定しているのに、RU 使用量が急増するのはなぜですか? {#why-is-there-a-spike-in-ru-usage-when-my-workload-is-steady}

TiDB の必要なバックグラウンド ジョブが原因で、RU 使用量が急増する可能性があります。テーブルの自動分析や統計の再構築などのこれらのジョブは、最適化されたクエリ プランを生成するために必要です。

### クラスターの無料割り当てを使い果たしたり、使用制限を超えたりするとどうなりますか? {#what-happens-when-my-cluster-exhausts-its-free-quota-or-exceeds-its-spending-limit}

クラスターが無料割り当てまたは使用制限に達すると、割り当てが増加するか、新しい月の開始時に使用量がリセットされるまで、クラスターは新しい接続試行を直ちに拒否します。割り当てに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。詳細については、 [TiDB Cloudサーバーレスの制限とクォータ](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

### データのインポート中に RU 使用量が急増するのはなぜですか? {#why-do-i-observe-spikes-in-ru-usage-while-importing-data}

TiDB Cloud Serverless クラスターのデータ インポート プロセス中、RU の消費はデータが正常にインポートされた場合にのみ発生するため、RU 使用量が急増します。

### TiDB Cloud Serverless で列指向storageを使用する場合、どのようなコストがかかりますか? {#what-costs-are-involved-when-using-columnar-storage-in-tidb-cloud-serverless}

TiDB Cloud Serverless の列指向storageの料金は、行指向storageの料金と同様です。列指向storageを使用すると、データ (インデックスなし) を保存するための追加のレプリカが作成されます。行指向ストレージから列指向storageへのデータのレプリケーションには追加料金はかかりません。

詳細な価格情報については[TiDB Cloud Serverless の価格詳細](https://www.pingcap.com/tidb-serverless-pricing-details/)参照してください。

### 列指向storageを使用するとコストは高くなりますか? {#is-using-columnar-storage-more-expensive}

TiDB Cloud Serverless の列指向storageでは、追加のレプリカにより追加コストが発生し、データ複製にさらに多くのstorageとリソースが必要になります。ただし、分析クエリを実行する場合、列指向storageはよりコスト効率が高くなります。

TPC-H ベンチマーク テストによると、列ベースのstorageで分析クエリを実行するコストは、行ベースのstorageを使用する場合のコストの約 3 分の 1 です。

したがって、追加のレプリカによる初期コストは発生する可能性がありますが、分析中の計算コストが削減されるため、特定のユースケースではコスト効率が向上します。特に分析ニーズのあるユーザーにとって、列指向storageはコストを大幅に削減し、かなりのコスト節約の機会を提供します。

## Securityよくある質問 {#security-faqs}

### TiDB Cloud Serverless は共有ですか、それとも専用ですか? {#is-my-tidb-cloud-serverless-shared-or-dedicated}

サーバーレス テクノロジーはマルチテナント向けに設計されており、すべてのクラスターで使用されるリソースは共有されます。分離されたインフラストラクチャとリソースを備えたマネージド TiDB サービスを取得するには、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)にアップグレードできます。

### TiDB Cloud Serverless はどのようにしてセキュリティを確保しますか? {#how-does-tidb-cloud-serverless-ensure-security}

-   接続はトランスポート層Security(TLS) によって暗号化されます。TLS を使用してTiDB Cloud Serverless に接続する方法の詳細については、 [TiDB Cloud ServerlessへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)参照してください。
-   TiDB Cloud Serverless に保存されるすべてのデータは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。TiDB TiDB Cloud Serverless クラスターは、TiDB Cloudで新しい TiDB バージョンがロールアウトされると自動的にアップグレードされます。クラスターで実行されている TiDB のバージョンは、 [TiDB Cloudコンソール](https://tidbcloud.com/console/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。または、クラスターに接続し、 `SELECT version()`または`SELECT tidb_version()`使用して TiDB のバージョンを確認することもできます。

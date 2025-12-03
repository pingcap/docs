---
title: "TiDB Cloud Starter FAQs"
summary: TiDB Cloud Starter に関するよくある質問 (FAQ) について説明します。
aliases: ['/tidbcloud/serverless-tier-faqs']
---

# TiDB Cloud Starterに関するよくある質問 {#tidb-cloud-starter-faqs}

<!-- markdownlint-disable MD026 -->

このドキュメントには、TiDB Cloud Starter に関してよく寄せられる質問が記載されています。

## 一般的なよくある質問 {#general-faqs}

### TiDB Cloud Starter とは何ですか? {#what-is-tidb-cloud-starter}

TiDB Cloud Starterは、お客様と組織に完全なHTAP機能を備えたTiDBデータベースを提供します。これは、TiDBのフルマネージドかつ自動スケーリング可能なデプロイメントであり、データベースをすぐに使い始めることができ、基盤となるノードを気にすることなくアプリケーションを開発・実行し、アプリケーションのワークロードの変化に応じて自動的にスケーリングできます。

### TiDB Cloud Starter とTiDB Cloud Serverless の関係は何ですか? {#what-is-the-relationship-between-tidb-cloud-starter-and-tidb-cloud-serverless}

TiDB Cloud Starter は、2025 年 8 月 12 日よりTiDB Cloud Serverless の新しい名前になります。

Starter に名前が変更される前、 TiDB Cloudの Serverless 層は何千人もの開発者のエントリ ポイントとして機能し、自動的にスケーリングされ、数秒で起動し、十分な無料割り当てを超えるまでコストがかからない、本番環境対応のデータベースを提供していました。

「サーバーレス」は、サービスが舞台裏でどのように動作するかを正確に反映していますが、初めて使用するユーザーの多くは、この用語が抽象的で、さまざまな意味が詰め込まれていると感じました。

このエントリー層の目的をより明確にするため、 TiDB Cloudを使った構築を最も早く開始できる「Starter」に名称を変更しました。Serverless層に関するこれまでの内容はそのままです。

-   行ベースと列ベースの両方のstorageを備えた完全に管理されたデータベースで、ハイブリッド OLTP および OLAP ワークロードに最適です。
-   自動かつリクエスト主導型のスケーリング。容量計画や手動の調整は必要ありません。
-   ベクター検索とフルテキスト検索が組み込まれており、GenAI 検索、チャットボット、その他の AI アプリケーションを強化します。
-   組織ごとに最大 5 つのクラスターまで、月間クォータが常時無料です (5 GiB の行データ + 5 GiB の列データ + クラスターあたり 5,000 万[RU](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) )。

### TiDB Cloud Starter を使い始めるにはどうすればよいですか? {#how-do-i-get-started-with-tidb-cloud-starter}

5分間の[TiDB Cloudクイックスタート](/tidb-cloud/tidb-cloud-quickstart.md)から始めましょう

### TiDB Cloudで作成できるTiDB Cloud Starter クラスターの数はいくつですか? {#how-many-tidb-cloud-starter-clusters-can-i-create-in-tidb-cloud}

TiDB Cloudでは、組織ごとにデフォルトで最大5つの[TiDB Cloudスターター](/tidb-cloud/select-cluster-tier.md#starter)クラスターを作成できます。TiDB TiDB Cloud Starter クラスターをさらに作成するには、クレジットカードを追加し、使用量を[支出限度額](/tidb-cloud/manage-serverless-spend-limit.md)に設定する必要があります。

### TiDB Cloud Starter ではすべてのTiDB Cloud機能が完全にサポートされていますか? {#are-all-tidb-cloud-features-fully-supported-on-tidb-cloud-starter}

TiDB Cloudの一部の機能は、 TiDB Cloud Starterでは部分的にサポートされるか、サポートされていません。詳細については、 [TiDB Cloud Starter の制限とクォータ](/tidb-cloud/serverless-limitations.md)ご覧ください。

### TiDB Cloud Starter は、Google Cloud や Azure など、AWS 以外のクラウド プラットフォームでいつ利用できるようになりますか? {#when-will-tidb-cloud-starter-be-available-on-cloud-platforms-other-than-aws-such-as-google-cloud-or-azure}

TiDB Cloud StarterをGoogle CloudやAzureを含む他のクラウドプラットフォームに拡張すべく、積極的に取り組んでいます。ただし、現状ではギャップを埋め、あらゆる環境でシームレスな機能を実現することに注力しているため、具体的なスケジュールは未定です。ご安心ください。TiDB TiDB Cloud Starterをより多くのクラウドプラットフォームでご利用いただけるよう、鋭意取り組んでおり、進捗状況についてはコミュニティの皆様に随時お知らせいたします。

### TiDB Cloud Starterが利用可能になる前にDeveloper Tierクラスターを作成しました。このクラスターは引き続き使用できますか？ {#i-created-a-developer-tier-cluster-before-tidb-cloud-starter-was-available-can-i-still-use-my-cluster}

はい、 Developer TierクラスターはTiDB Cloud Starter クラスターに自動的に移行されており、以前の使用状況に支障をきたすことなく、ユーザー エクスペリエンスが向上します。

### TiDB Cloud Starter の列指向storageとは何ですか? {#what-is-columnar-storage-in-tidb-cloud-starter}

TiDB Cloud Starterの列指向storageは、行ベースstorageの追加レプリカとして機能し、強力な一貫性を確保します。従来の行ベースstorageはデータを行単位で保存しますが、列指向storageはデータを列単位で整理し、データ分析タスクに最適化します。

列指向storageは、トランザクション ワークロードと分析ワークロードをシームレスに融合することで、TiDB のハイブリッド トランザクションおよび分析処理 (HTAP) 機能を有効にする重要な機能です。

列指向storageデータを効率的に管理するために、 TiDB Cloud Starterは独立したElastic TiFlashエンジンを使用します。クエリ実行中、オプティマイザーはクラスターに対し、行ベースストレージと列指向storageのどちらからデータを取得するかを自動的に決定するよう指示します。

### TiDB Cloud Starter で列指向storageを使用するのはいつですか? {#when-should-i-use-columnar-storage-in-tidb-cloud-starter}

次のシナリオでは、 TiDB Cloud Starter の列指向storageの使用を検討してください。

-   ワークロードには、効率的なデータスキャンと集約を必要とする分析タスクが含まれます。
-   特に分析ワークロードのパフォーマンス向上を優先します。
-   トランザクション処理（TP）ワークロードへのパフォーマンスへの影響を防ぐため、分析処理とトランザクション処理を分離する必要があります。独立した列指向storageは、これらの異なるワークロードパターンを最適化するのに役立ちます。

このようなシナリオでは、列指向storageによりクエリのパフォーマンスが大幅に向上し、システム内の混合ワークロードに対してシームレスなエクスペリエンスを提供できます。

### TiDB Cloud Starter で列指向storageを使用する方法 {#how-to-use-columnar-storage-in-tidb-cloud-starter}

TiDB Cloud Starter での列指向storageの使用は、 TiFlashでの使用と同様です。列指向storageは、テーブルレベルとデータベースレベルの両方で有効にできます。

-   テーブル レベル: TiFlashレプリカをテーブルに割り当てて、特定のテーブルの列指向storageを有効にします。
-   データベース レベル: データベース全体で列型storageを使用するように、データベース内のすべてのテーブルに対してTiFlashレプリカを構成します。

テーブルにTiFlashレプリカが設定されると、TiDBは行ベースstorageからそのテーブルの列指向storageにデータを自動的に複製します。これにより、データの一貫性が確保され、分析クエリのパフォーマンスが最適化されます。

TiFlashレプリカの設定方法の詳細については、 [TiFlashレプリカを作成する](/tiflash/create-tiflash-replicas.md)参照してください。

### 数分間アイドル状態が続いた後に接続が切断されるのはなぜですか? {#why-is-my-connection-disconnected-after-being-idle-for-several-minutes}

パブリックエンドポイント経由で接続する場合、接続は様々なネットワークプロバイダーや中間デバイスを経由します。これらのデバイスにはそれぞれ短いアイドルタイムアウトが設定されている場合があり、接続が途中で中断される可能性があります。詳しくは[接続制限](/tidb-cloud/serverless-limitations.md#connection)ご覧ください。

## 請求と計測に関するよくある質問 {#billing-and-metering-faqs}

### リクエストユニットとは何ですか? {#what-are-request-units}

TiDB Cloud Starterは従量課金モデルを採用しており、storage容量とクラスターの使用量に対してのみ料金が発生します。このモデルでは、SQLクエリ、一括操作、バックグラウンドジョブなど、すべてのクラスターアクティビティが[リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru)で定量化されます。RUは、クラスターで開始されたリクエストのサイズと複雑さを表す抽象的な指標です。詳細については、 [TiDB Cloud Starter の価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)ご覧ください。

### TiDB Cloud Starter には無料プランはありますか? {#is-there-any-free-plan-available-for-tidb-cloud-starter}

組織内の最初の 5 つのTiDB Cloud Starter クラスターについては、 TiDB Cloud は次のようにクラスターごとに無料使用量割り当てを提供します。

-   行ベースのstorage: 5 GiB
-   列指向storage: 5 GiB
-   [リクエストユニット（RU）](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru) : 月間5000万RU

TiDB Cloud Starter クラスターに月間使用制限が設定されている場合、無料割り当て量を超えた使用量には課金されます。無料クラスターの場合、無料割り当て量に達すると、月間使用制限を設定するか、新しい月の開始時に使用量がリセットされるまで、このクラスターの読み取りおよび書き込み操作は制限されます。

詳細については[TiDB Cloud Starter の使用割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)参照してください。

### 無料プランの制限は何ですか? {#what-are-the-limitations-of-the-free-plan}

無料プランでは、スケーラブルでないリソースのため、クラスターのパフォーマンスが制限されます。そのため、クエリあたりのメモリ割り当てが256MiBに制限され、1秒あたりのリクエストユニット（RU）に顕著なボトルネックが発生する可能性があります。クラスターのパフォーマンスを最大化し、これらの制限を回避するには、 TiDB Cloud Starterクラスターに[毎月の支出限度額を設定する](/tidb-cloud/manage-serverless-spend-limit.md)追加できます。

### ワークロードに必要な RU の数を見積もって、月間予算を計画するにはどうすればよいですか? {#how-can-i-estimate-the-number-of-rus-required-by-my-workloads-and-plan-my-monthly-budget}

個々のSQL文のRU消費量を取得するには、SQL文[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md#ru-request-unit-consumption)を使用できます。ただし、 `EXPLAIN ANALYZE`で返されるRU使用量には、出力RUは含まれていないことに注意してください。出力使用量はゲートウェイで個別に測定され、TiDBサーバーには認識されないためです。

クラスターで使用されているRUとstorageを確認するには、クラスターの概要ページの**「今月の使用量」**ペインをご覧ください。このペインに表示される過去のリソース使用量データとリアルタイムのリソース使用量を参考に、クラスターのリソース消費量を追跡し、適切な使用制限を見積もることができます。無料割り当てで要件を満たせない場合は、追加リソースの使用制限を編集できます。詳細については、 [TiDB Cloud Starter の使用割り当て](/tidb-cloud/select-cluster-tier.md#usage-quota)ご覧ください。

### 消費される RU の数を最小限に抑えるためにワークロードを最適化するにはどうすればよいでしょうか? {#how-can-i-optimize-my-workload-to-minimize-the-number-of-rus-consumed}

[SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)のガイドラインに従って、クエリが最適なパフォーマンスを得るために注意深く最適化されていることを確認してください。 RU を最も多く消費する SQL ステートメントを特定するには、クラスターの[**診断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)ページに移動し、 **[SQL ステートメント]**タブを確認します。ここで、SQL 実行を観察し、**合計 RU**または**平均 RU**でソートされた上位のステートメントを表示できます。 詳細については、 [ステートメント分析](/tidb-cloud/tune-performance.md#statement-analysis)参照してください。 また、出力トラフィックの量を最小限に抑えることも、RU の消費量を削減するために重要です。 これを実現するには、クエリで必要な列と行のみを返すことをお勧めします。これにより、ネットワークの出力トラフィックが削減されます。 これは、返される列と行を慎重に選択してフィルター処理することで実現でき、それによってネットワーク使用率が最適化されます。

### TiDB Cloud Starter のstorageはどのように計測されますか? {#how-storage-is-metered-for-tidb-cloud-starter}

storageは、 TiDB Cloud Starter クラスターに保存されるデータ量（月間GiB単位）に基づいて課金されます。これは、すべてのテーブルとインデックスの合計サイズ（データ圧縮とレプリカを除く）と、その月のデータの保存時間数を掛けて算出されます。

### テーブルまたはデータベースをすぐに削除した後でも、storage使用量のサイズが変更されないのはなぜですか? {#why-does-the-storage-usage-size-remain-unchanged-after-dropping-a-table-or-database-immediately}

これは、TiDBが削除されたテーブルとデータベースを一定期間保持するためです。この保持期間により[`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)これらのテーブルに依存するトランザクションは中断することなく実行を継続できます。さらに、この保持期間によって[`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md)機能が実現可能となり、誤って削除されたテーブルやデータベースを回復できるようになります。

### アクティブにクエリを実行していないのに RU が消費されるのはなぜですか? {#why-are-there-ru-consumptions-when-i-m-not-actively-running-any-queries}

RU の消費は様々なシナリオで発生する可能性があります。一般的なシナリオの一つは、バックグラウンドクエリの実行時です。これには、TiDB インスタンス間のスキーマ変更の同期、DDL ジョブの実行、権限の更新、SQL バインディングの更新、グローバル変数の更新などが含まれますが、これらに限定されません。別のシナリオとしては、スキーマの読み込みなど、特定の Web コンソール機能がクエリを生成する場合が挙げられます。これらのプロセスは、明示的なユーザートリガーがなくても RU を使用します。

### ワークロードが安定しているのに RU 使用量が急増するのはなぜですか? {#why-is-there-a-spike-in-ru-usage-when-my-workload-is-steady}

TiDB の必須バックグラウンドジョブが原因で、RU 使用量が急増する可能性があります。これらのジョブ（テーブルの自動分析や統計の再構築など）は、最適化されたクエリプランを生成するために必要です。

### クラスターの無料割り当てを使い果たしたり、使用制限を超えたりするとどうなりますか? {#what-happens-when-my-cluster-exhausts-its-free-quota-or-exceeds-its-spending-limit}

クラスターが無料割り当てまたは使用制限に達すると、割り当てが増加するか、新しい月の開始時に使用量がリセットされるまで、クラスターは新しい接続試行を直ちに拒否します。割り当てに達する前に確立された既存の接続はアクティブなままですが、スロットリングが発生します。詳細については、 [TiDB Cloud Starter の制限とクォータ](/tidb-cloud/serverless-limitations.md#usage-quota)参照してください。

### データのインポート中に RU 使用量が急増するのはなぜですか? {#why-do-i-observe-spikes-in-ru-usage-while-importing-data}

TiDB Cloud Starter クラスターのデータ インポート プロセス中、データが正常にインポートされた場合にのみ RU 消費が発生するため、RU 使用量が急増します。

### TiDB Cloud Starter で列指向storageを使用する場合、どのようなコストがかかりますか? {#what-costs-are-involved-when-using-columnar-storage-in-tidb-cloud-starter}

TiDB Cloud Starter の列指向storageの料金は、行指向storageの料金とほぼ同じです。列指向storageを使用すると、データ（インデックスなし）を保存するための追加のレプリカが作成されます。行指向ストレージから列指向storageへのデータのレプリケーションには追加料金は発生しません。

詳細な価格情報については、 [TiDB Cloud Starterの価格詳細](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)参照してください。

### 列指向storageを使用するとコストは高くなりますか? {#is-using-columnar-storage-more-expensive}

TiDB Cloud Starterの列指向storageは、追加のレプリカが必要となり、データレプリケーションに必要なstorageとリソースが増えるため、追加コストが発生します。ただし、分析クエリを実行する際には、列指向storageがコスト効率が高くなります。

TPC-H ベンチマーク テストによると、列ベースのstorageで分析クエリを実行するコストは、行ベースのstorageを使用する場合のコストの約 3 分の 1 になります。

したがって、追加のレプリカによる初期コストは発生する可能性がありますが、分析時の計算コストが削減されるため、特定のユースケースではより費用対効果の高いものになる可能性があります。特に分析ニーズが高いユーザーにとって、列指向storageはコストを大幅に削減し、大幅なコスト削減の機会を提供します。

## Securityよくある質問 {#security-faqs}

### TiDB Cloud Starter は共有ですか、それとも専用ですか? {#is-my-tidb-cloud-starter-shared-or-dedicated}

サーバーレステクノロジーはマルチテナント向けに設計されており、すべてのクラスターで使用されるリソースは共有されます。分離されたインフラストラクチャとリソースを備えたマネージドTiDBサービスをご利用いただくには、 [TiDB Cloud専用](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated)にアップグレードしてください。

### TiDB Cloud Starter はどのようにしてセキュリティを確保しますか? {#how-does-tidb-cloud-starter-ensure-security}

-   接続はトランスポート層Security（TLS）によって暗号化されます。TLSを使用してTiDB Cloud Starterに接続する方法の詳細については、 [TiDB Cloud StarterへのTLS接続](/tidb-cloud/secure-connections-to-serverless-clusters.md)ご覧ください。
-   TiDB Cloud Starter に保存されるすべてのデータは、クラスターが実行されているクラウド プロバイダーのツールを使用して保存時に暗号化されます。

## メンテナンスに関するFAQ {#maintenance-faq}

### クラスターが実行されている TiDB のバージョンをアップグレードできますか? {#can-i-upgrade-the-version-of-tidb-that-my-cluster-is-running-on}

いいえ。TiDB TiDB Cloud Starterクラスターは、 TiDB Cloudに新しいバージョンの TiDB がロールアウトされるたびに自動的にアップグレードされます。クラスターで実行されている TiDB のバージョンは、 [TiDB Cloudコンソール](https://tidbcloud.com/project/clusters)または最新の[リリースノート](https://docs.pingcap.com/tidbcloud/tidb-cloud-release-notes)で確認できます。または、クラスターに接続して`SELECT version()`または`SELECT tidb_version()`を使用して TiDB のバージョンを確認することもできます。

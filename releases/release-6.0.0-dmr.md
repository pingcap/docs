---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 リリースノート {#tidb-6-0-0-release-notes}

発売日：2022年4月7日

TiDB バージョン: 6.0.0-DMR

> **ノート：**
>
> TiDB 6.0.0-DMR のドキュメントは[<a href="https://docs-archive.pingcap.com/tidb/v6.0/">アーカイブされた</a>](https://docs-archive.pingcap.com/tidb/v6.0/)になりました。 PingCAP では、 [<a href="https://docs.pingcap.com/tidb/stable">最新のLTSバージョン</a>](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

6.0.0-DMR の主な新機能または改善点は次のとおりです。

-   SQL での配置ルールをサポートし、データ配置のより柔軟な管理を提供します。
-   カーネル レベルでデータとインデックス間の整合性チェックを追加すると、リソースのオーバーヘッドが非常に低くなり、システムの安定性と堅牢性が向上します。
-   非専門家向けの自己サービス型データベース パフォーマンス監視および診断機能であるTop SQLを提供します。
-   クラスターのパフォーマンス データを常に収集する継続的プロファイリングをサポートし、技術専門家の MTTR を削減します。
-   ホットスポットの小さなテーブルをメモリにキャッシュすることで、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが減少します。
-   メモリ内の悲観的ロックを最適化します。悲観的ロックによって引き起こされるパフォーマンスのボトルネックの下では、悲観的ロックのメモリ最適化により、レイテンシーを効果的に 10% 削減し、QPS を 10% 向上させることができます。
-   プリペアド ステートメントを強化して実行プランを共有することで、CPU リソースの消費が削減され、SQL の実行効率が向上します。
-   より多くの式のプッシュダウンとエラスティック スレッド プールの一般公開 (GA) をサポートすることで、MPP エンジンのコンピューティング パフォーマンスを向上させます。
-   DM WebUIを追加して、多数の移行タスクの管理を容易にします。
-   大規模なクラスターでデータをレプリケートする際の TiCDC の安定性と効率が向上します。 TiCDC は、100,000 テーブルの同時複製をサポートするようになりました。
-   TiKV ノードの再起動後のリーダー バランシングを加速し、再起動後のビジネス回復速度を向上させます。
-   統計の自動更新のキャンセルをサポートします。これにより、リソースの競合が軽減され、SQL パフォーマンスへの影響が制限されます。
-   TiDBクラスタの自動診断サービス「PingCAPクリニック」を提供（テクニカルプレビュー版）。
-   エンタープライズレベルのデータベース管理プラットフォームである TiDB Enterprise Manager を提供します。

また、TiDB の HTAP ソリューションの中核コンポーネントとして、 TiFlash <sup>TM は</sup>このリリースで正式にオープンソースになります。詳細は[<a href="https://github.com/pingcap/tiflash">TiFlashリポジトリ</a>](https://github.com/pingcap/tiflash)を参照してください。

## リリース戦略の変更 {#release-strategy-changes}

TiDB v6.0.0 以降、TiDB は 2 種類のリリースを提供します。

-   長期サポートのリリース

    長期サポート (LTS) リリースは、約 6 か月ごとにリリースされます。 LTS リリースでは、新機能と改善が導入され、リリース ライフサイクル内でパッチ リリースが受け入れられます。たとえば、v6.1.0 は LTS リリースになります。

-   開発マイルストーンのリリース

    開発マイルストーン リリース (DMR) は、約 2 か月ごとにリリースされます。 DMR は新機能と改善を導入しますが、パッチ リリースは受け入れません。オンプレミスのユーザーが本番環境で DMR を使用することはお勧めできません。たとえば、v6.0.0-DMR は DMR です。

TiDB v6.0.0 は DMR であり、そのバージョンは 6.0.0-DMR です。

## 新機能 {#new-features}

### SQL {#sql}

-   データの SQL ベースの配置ルール

    TiDB は、拡張性に優れた分散データベースです。通常、データは複数のサーバー、さらには複数のデータセンターに展開されます。したがって、データ スケジュール管理は TiDB の最も重要な基本機能の 1 つです。ほとんどの場合、ユーザーはデータのスケジュールと管理の方法を気にする必要はありません。しかし、アプリケーションの複雑さの増大に伴い、分離とアクセスレイテンシーによって引き起こされるデプロイメントの変更が TiDB にとって新たな課題となっています。 TiDB は v6.0.0 以降、SQL インターフェースに基づいたデータのスケジューリングおよび管理機能を正式に提供しています。レプリカの数、ロールの種類、データの配置場所などの次元での柔軟なスケジューリングと管理をサポートします。 TiDB は、マルチサービス共有クラスターおよびクロス AZ デプロイメントでのデータ配置のより柔軟な管理もサポートしています。

    [<a href="/placement-rules-in-sql.md">ユーザードキュメント</a>](/placement-rules-in-sql.md)

-   データベースによるTiFlashレプリカの構築をサポートします。データベース内のすべてのテーブルにTiFlashレプリカを追加するには、単一の SQL ステートメントを使用するだけで済み、運用とメンテナンスのコストが大幅に節約されます。

    [<a href="/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases">ユーザードキュメント</a>](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### トランザクション {#transaction}

-   カーネル レベルでのデータ インデックスの整合性チェックを追加する

    トランザクションの実行時にデータ インデックスの整合性チェックを追加します。これにより、リソースのオーバーヘッドが非常に低くなり、システムの安定性と堅牢性が向上します。 `tidb_enable_mutation_checker`および`tidb_txn_assertion_level`変数を使用してチェック動作を制御できます。デフォルト設定では、ほとんどのシナリオで QPS 低下は 2% 以内に制御されます。整合性チェックのエラーの説明については、 [<a href="/troubleshoot-data-inconsistency-errors.md">ユーザードキュメント</a>](/troubleshoot-data-inconsistency-errors.md)を参照してください。

### 可観測性 {#observability}

-   Top SQL: 非専門家向けのパフォーマンス診断

    Top SQLは、DBA およびアプリ開発者向けの TiDB ダッシュボードの自己サービス型データベース パフォーマンス監視および診断機能であり、TiDB v6.0 で一般提供されるようになりました。

    専門家向けの既存の診断機能とは異なり、 Top SQL は非専門家向けに設計されています。相関関係を見つけたり、 Raft Snapshot、RocksDB、MVCC、TSO などの TiDB 内部メカニズムを理解するために何千もの監視チャートを横断する必要はありません。 Top SQLを使用してデータベースの負荷を迅速に分析し、アプリのパフォーマンスを向上させるには、基本的なデータベースの知識 (インデックス、ロックの競合、実行プランなど) のみが必要です。

    Top SQL はデフォルトでは有効になっていません。 Top SQLを有効にすると、各 TiKV ノードまたは TiDB ノードのリアルタイムの CPU 負荷が提供されます。したがって、高い CPU 負荷を消費する SQL ステートメントを一目で特定し、データベースのホットスポットや突然の負荷の増加などの問題を迅速に分析できます。たとえば、 Top SQL を使用すると、単一 TiKV ノードの CPU の 90% を消費する異常なクエリを特定して診断できます。

    [<a href="/dashboard/top-sql.md">ユーザードキュメント</a>](/dashboard/top-sql.md)

-   継続的プロファイリングのサポート

    TiDB ダッシュボードには継続プロファイリング機能が導入されており、この機能は TiDB v6.0 で一般提供されるようになりました。継続的プロファイリングはデフォルトでは有効になっていません。有効にすると、個々の TiDB、TiKV、PD インスタンスのパフォーマンス データが常に収集され、オーバーヘッドは無視できます。履歴パフォーマンス データを使用すると、問題の再現が難しい場合でも、技術専門家はメモリ消費量の多さなどの問題の根本原因を遡って特定できます。このようにして、平均回復時間 (MTTR) を短縮できます。

    [<a href="/dashboard/continuous-profiling.md">ユーザードキュメント</a>](/dashboard/continuous-profiling.md)

### パフォーマンス {#performance}

-   キャッシュホットスポットの小さなテーブル

    ホットスポットの小さなテーブルにアクセスするシナリオのユーザー アプリケーションの場合、TiDB はホットスポット テーブルのメモリへの明示的なキャッシュをサポートします。これにより、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが短縮されます。このソリューションにより、サードパーティのキャッシュ ミドルウェアの導入を効果的に回避し、アーキテクチャの複雑さを軽減し、運用とメンテナンスのコストを削減できます。このソリューションは、構成テーブルや為替レート テーブルなど、小さなテーブルが頻繁にアクセスされるが、ほとんど更新されないシナリオに適しています。

    [<a href="/cached-tables.md">ユーザードキュメント</a>](/cached-tables.md) [<a href="https://github.com/pingcap/tidb/issues/25293">#25293</a>](https://github.com/pingcap/tidb/issues/25293)

-   インメモリ悲観的ロック

    TiDB v6.0.0 以降、メモリ内の悲観的ロックはデフォルトで有効になっています。この機能を有効にすると、悲観的トランザクション ロックがメモリ内で管理されます。これにより、悲観的ロックの持続とロック情報のRaftレプリケーションが回避され、悲観的トランザクション ロックの管理にかかるオーバーヘッドが大幅に削減されます。悲観的ロックによって引き起こされるパフォーマンスのボトルネックの下では、悲観的ロックのメモリ最適化により、レイテンシーを効果的に 10% 削減し、QPS を 10% 向上させることができます。

    [<a href="/pessimistic-transaction.md#in-memory-pessimistic-lock">ユーザードキュメント</a>](/pessimistic-transaction.md#in-memory-pessimistic-lock) [<a href="https://github.com/tikv/tikv/issues/11452">#11452</a>](https://github.com/tikv/tikv/issues/11452)

-   Read Committed 分離レベルで TSO を取得するための最適化

    クエリのレイテンシーを短縮するため、読み取り/書き込みの競合がまれな場合、TiDB は[<a href="/transaction-isolation-levels.md#read-committed-isolation-level">コミットされた分離レベルの読み取り</a>](/transaction-isolation-levels.md#read-committed-isolation-level)に`tidb_rc_read_check_ts`システム変数を追加して、不必要な TSO を減らします。この変数はデフォルトでは無効になっています。変数が有効になっている場合、この最適化により重複した TSO の取得が回避され、読み取り/書き込みの競合がないシナリオでのレイテンシーが短縮されます。ただし、読み取り/書き込みの競合が頻繁に発生するシナリオでは、この変数を有効にするとパフォーマンスの低下が発生する可能性があります。

    [<a href="/transaction-isolation-levels.md#read-committed-isolation-level">ユーザードキュメント</a>](/transaction-isolation-levels.md#read-committed-isolation-level) [<a href="https://github.com/pingcap/tidb/issues/33159">#33159</a>](https://github.com/pingcap/tidb/issues/33159)

-   プリペアドステートメントを強化して実行計画を共有する

    SQL 実行プランを再利用すると、SQL ステートメントの解析時間を効果的に短縮し、CPU リソースの消費を減らし、SQL 実行効率を向上させることができます。 SQL チューニングの重要な方法の 1 つは、SQL 実行プランを効果的に再利用することです。 TiDB は、プリペアド ステートメントを使用した実行計画の共有をサポートしています。ただし、準備されたステートメントが閉じられると、TiDB は対応するプラン キャッシュを自動的にクリアします。その後、TiDB は繰り返される SQL ステートメントを不必要に解析し、実行効率に影響を与える可能性があります。 v6.0.0 以降、TiDB は`tidb_ignore_prepared_cache_close_stmt`パラメータによる`COM_STMT_CLOSE`コマンドを無視するかどうかの制御をサポートしています (デフォルトでは無効)。このパラメーターが有効な場合、TiDB はプリペアド ステートメントを閉じるコマンドを無視し、実行プランをキャッシュに保持するため、実行プランの再利用率が向上します。

    [<a href="/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement">ユーザードキュメント</a>](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) [<a href="https://github.com/pingcap/tidb/issues/31056">#31056</a>](https://github.com/pingcap/tidb/issues/31056)

-   クエリのプッシュダウンを改善する

    コンピューティングとstorageを分離するネイティブアーキテクチャにより、TiDB は演算子をプッシュダウンすることで無効なデータをフィルタリングして除外することをサポートします。これにより、TiDB と TiKV 間のデータ送信が大幅に削減され、クエリ効率が向上します。 v6.0.0 では、TiDB は、より多くの式と`BIT`データ型を TiKV にプッシュダウンすることをサポートし、式とデータ型を計算する際のクエリ効率を向上させます。

    [<a href="/functions-and-operators/expressions-pushed-down.md">ユーザードキュメント</a>](/functions-and-operators/expressions-pushed-down.md) [<a href="https://github.com/pingcap/tidb/issues/30738">#30738</a>](https://github.com/pingcap/tidb/issues/30738)

-   ホットスポットインデックスの最適化

    単調増加するデータをバッチでセカンダリ インデックスに書き込むと、インデックス ホットスポットが発生し、全体的な書き込みスループットに影響します。 v6.0.0 以降、TiDB は書き込みパフォーマンスを向上させるために`tidb_shard`関数を使用したインデックス ホットスポットの分散をサポートしています。現在、 `tidb_shard`一意のセカンダリ インデックスに対してのみ有効です。このアプリケーションフレンドリーなソリューションでは、元のクエリ条件を変更する必要がありません。このソリューションは、高い書き込みスループット、ポイント クエリ、およびバッチ ポイント クエリのシナリオで使用できます。範囲クエリによって分散されたデータをアプリケーションで使用すると、パフォーマンスの低下が発生する可能性があることに注意してください。したがって、このような場合には検証せずにこの機能を使用しないでください。

    [<a href="/functions-and-operators/tidb-functions.md#tidb_shard">ユーザードキュメント</a>](/functions-and-operators/tidb-functions.md#tidb_shard) [<a href="https://github.com/pingcap/tidb/issues/31040">#31040</a>](https://github.com/pingcap/tidb/issues/31040)

-   TiFlash MPP エンジンでパーティション化されたテーブルの動的プルーニング モードをサポート (実験的)

    このモードでは、TiDB はTiFlashの MPP エンジンを使用してパーティション テーブル上のデータを読み取り、計算できます。これにより、パーティション テーブルのクエリ パフォーマンスが大幅に向上します。

    [<a href="/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode">ユーザードキュメント</a>](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

-   MPP エンジンのコンピューティング パフォーマンスを向上させる

    -   より多くの関数と演算子を MPP エンジンにプッシュダウンするサポート

        -   `IS NOT`関数： `IS`
        -   文字`NOT REGEXP()`関数: `REGEXP()`
        -   数学関数: `GREATEST(int/real)` 、 `LEAST(int/real)`
        -   日付関数: `DAYNAME()` 、 `DAYOFMONTH()` 、 `DAYOFWEEK()` 、 `DAYOFYEAR()` 、 `LAST_DAY()` 、 `MONTHNAME()`
        -   演算子: アンチ左アウター セミ ジョイン、左アウター セミ ジョイン

        [<a href="/tiflash/tiflash-supported-pushdown-calculations.md">ユーザードキュメント</a>](/tiflash/tiflash-supported-pushdown-calculations.md)

    -   エラスティック スレッド プール (デフォルトで有効) が GA になります。この機能は、CPU 使用率を改善することを目的としています。

        [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">ユーザードキュメント</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### 安定性 {#stability}

-   実行計画のベースライン取得を強化する

    テーブル名、頻度、ユーザー名などのディメンションを含むブロックリストを追加することで、実行計画のベースライン キャプチャの使いやすさが向上します。バインディングをキャッシュするためのメモリ管理を最適化する新しいアルゴリズムを導入します。ベースライン キャプチャを有効にすると、システムはほとんどの OLTP クエリのバインディングを自動的に作成します。バインドされたステートメントの実行計画は固定されており、実行計画の変更によるパフォーマンスの問題を回避します。ベースライン キャプチャは、メジャー バージョンのアップグレードやクラスターの移行などのシナリオに適用でき、実行計画の回帰によって引き起こされるパフォーマンスの問題を軽減するのに役立ちます。

    [<a href="/sql-plan-management.md#baseline-capturing">ユーザードキュメント</a>](/sql-plan-management.md#baseline-capturing) [<a href="https://github.com/pingcap/tidb/issues/32466">#32466</a>](https://github.com/pingcap/tidb/issues/32466)

-   TiKV クォータ リミッターのサポート (実験的)

    TiKV を使用してデプロイされたマシンのリソースが限られており、フォアグラウンドに過剰な量のリクエストの負担がかかる場合、バックグラウンドの CPU リソースがフォアグラウンドによって占有され、TiKV のパフォーマンスが不安定になります。 TiDB v6.0.0 では、クォータ関連の構成項目を使用して、CPU や読み取り/書き込み帯域幅など、フォアグラウンドで使用されるリソースを制限できます。これにより、長期にわたる高負荷のワークロード下でのクラスターの安定性が大幅に向上します。

    [<a href="/tikv-configuration-file.md#quota">ユーザードキュメント</a>](/tikv-configuration-file.md#quota) [<a href="https://github.com/tikv/tikv/issues/12131">#12131</a>](https://github.com/tikv/tikv/issues/12131)

-   TiFlashで zstd 圧縮アルゴリズムをサポート

    TiFlash、ユーザーがパフォーマンスと容量のバランスに基づいて最適な圧縮アルゴリズムを選択できるようにする 2 つのパラメーター`profiles.default.dt_compression_method`と`profiles.default.dt_compression_level`が導入されています。

    [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">ユーザードキュメント</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   すべての I/O チェック (チェックサム) をデフォルトで有効にする

    この機能は、v5.4.0 で実験的に導入されました。ユーザーのビジネスに明らかな影響を与えることなく、データの正確性とセキュリティを強化します。

    警告: 新しいバージョンのデータ形式を v5.4.0 より前のバージョンにダウングレードすることはできません。このようなダウングレード中は、 TiFlashレプリカを削除し、ダウングレード後にデータを複製する必要があります。または、 [<a href="/tiflash/tiflash-command-line-flags.md#dttool-migrate">dttool 移行</a>](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してダウングレードを実行することもできます。

    [<a href="/tiflash/tiflash-data-validation.md">ユーザードキュメント</a>](/tiflash/tiflash-data-validation.md)

-   スレッド使用率の向上

    TiFlash、非同期 gRPC および Min-TSO スケジューリング メカニズムが導入されています。このようなメカニズムにより、スレッドがより効率的に使用され、過剰なスレッドによって引き起こされるシステムクラッシュが回避されます。

    [<a href="/tiflash/monitor-tiflash.md#coprocessor">ユーザードキュメント</a>](/tiflash/monitor-tiflash.md#coprocessor)

### データ移行 {#data-migration}

#### TiDB データ移行 (DM) {#tidb-data-migration-dm}

-   WebUI を追加 (実験的)

    WebUI を使用すると、多数の移行タスクを簡単に管理できます。 WebUI では次のことができます。

    -   ダッシュボードで移行タスクをビュー
    -   移行タスクを管理する
    -   アップストリーム設定を構成する
    -   レプリケーションステータスのクエリ
    -   マスターとワーカーの情報をビュー

    WebUI はまだ実験的であり、開発中です。したがって、トライアルのみにお勧めします。既知の問題として、WebUI と dmctl を使用して同じタスクを操作すると問題が発生する可能性があります。この問題は、以降のバージョンで解決される予定です。

    [<a href="/dm/dm-webui-guide.md">ユーザードキュメント</a>](/dm/dm-webui-guide.md)

-   エラー処理メカニズムを追加する

    移行タスクを中断する問題に対処するために、より多くのコマンドが導入されました。例えば：

    -   スキーマ エラーが発生した場合は、スキーマ ファイルを個別に編集するのではなく、 `binlog-schema update`コマンドの`--from-source/--from-target`パラメータを使用してスキーマ ファイルを更新できます。
    -   binlogの位置を指定して、DDL ステートメントを挿入、置換、スキップ、または元に戻すことができます。

    [<a href="/dm/dm-manage-schema.md">ユーザードキュメント</a>](/dm/dm-manage-schema.md)

-   Amazon S3 への完全なデータstorageをサポート

    DM がすべてまたは完全なデータ移行タスクを実行する場合、アップストリームからの完全なデータを保存するために十分なハード ディスク容量が必要です。 EBS と比較して、Amazon S3 は低コストでほぼ無限のstorageを備えています。 DM は、ダンプ ディレクトリとして Amazon S3 の設定をサポートするようになりました。つまり、すべてまたは完全なデータ移行タスクを実行するときに、S3 を使用して完全なデータを保存できます。

    [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">ユーザードキュメント</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   指定した時間からの移行タスクの開始をサポート

    新しいパラメータ`--start-time`が移行タスクに追加されます。時刻は「2021-10-21 00:01:00」または「2021-10-21T00:01:00」の形式で定義できます。

    この機能は、シャード mysql インスタンスから増分データを移行およびマージするシナリオで特に役立ちます。具体的には、増分移行タスクでソースごとにbinlogの開始ポイントを設定する必要はありません。代わりに、 `safe-mode`の`--start-time`パラメータを使用すると、増分移行タスクをすばやく作成できます。

    [<a href="/dm/dm-create-task.md#flags-description">ユーザードキュメント</a>](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning {#tidb-lightning}

-   許容可能なエラーの最大数の構成をサポート

    設定項目`lightning.max-error`を追加しました。デフォルト値は 0 です。値が 0 より大きい場合、最大エラー機能が有効になります。エンコード中に行でエラーが発生した場合、この行を含むレコードがターゲット TiDB の`lightning_task_info.type_error_v1`に追加され、この行は無視されます。エラーのある行がしきい値を超えると、 TiDB Lightning は直ちに終了します。

    `lightning.max-error`構成と一致して、 `lightning.task-info-schema-name`構成項目には、データ保存エラーを報告するデータベースの名前が記録されます。

    この機能は、すべてのタイプのエラーをカバーするわけではありません。たとえば、構文エラーは適用されません。

    [<a href="/tidb-lightning/tidb-lightning-error-resolution.md#type-error">ユーザードキュメント</a>](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   100,000 テーブルの同時複製をサポート

    データ処理フローを最適化することで、TiCDC は各テーブルの増分データの処理に伴うリソース消費を削減し、大規模なクラスターでデータをレプリケートする際のレプリケーションの安定性と効率を大幅に向上させます。内部テストの結果、TiCDC は 100,000 テーブルの同時複製を安定してサポートできることがわかりました。

### 導入とメンテナンス {#deployment-and-maintenance}

-   新しい照合順序ルールをデフォルトで有効にする

    v4.0 以降、TiDB は、大文字と小文字を区別しない、アクセントを区別しない、およびパディング ルールにおいて MySQL と同じように動作する新しい照合順序ルールをサポートしています。新しい照合順序ルールは、デフォルトでは無効になっている`new_collations_enabled_on_first_bootstrap`パラメータによって制御されます。 v6.0 以降、TiDB はデフォルトで新しい照合順序ルールを有効にします。この構成は、TiDB クラスターの初期化時にのみ有効になることに注意してください。

    [<a href="/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap">ユーザードキュメント</a>](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

-   TiKV ノードの再起動後にリーダーのバランシングを加速する

    TiKV ノードの再起動後、負荷分散のために不均一に分散したリーダーを再分散する必要があります。大規模クラスターでは、リーダーのバランスをとる時間はリージョンの数と正の相関があります。たとえば、100K リージョンのリーダー バランシングには 20 ～ 30 分かかる場合があり、不均一な負荷によるパフォーマンスの問題や安定性のリスクが発生する傾向があります。 TiDB v6.0.0 は、バランシングの同時実行性を制御するパラメーターを提供し、デフォルト値を元の 4 倍に拡大します。これにより、リーダーのリバランス時間が大幅に短縮され、TiKV ノードの再起動後のビジネスの回復が加速されます。

    [<a href="/pd-control.md#scheduler-config-balance-leader-scheduler">ユーザードキュメント</a>](/pd-control.md#scheduler-config-balance-leader-scheduler) [<a href="https://github.com/tikv/pd/issues/4610">#4610</a>](https://github.com/tikv/pd/issues/4610)

-   統計の自動更新のキャンセルをサポート

    統計は、 SQL のパフォーマンスに影響を与える最も重要な基本データの 1 つです。統計の完全性と適時性を確保するために、TiDB はオブジェクト統計をバックグラウンドで定期的に自動的に更新します。ただし、統計の自動更新によりリソースの競合が発生し、SQL のパフォーマンスに影響を与える可能性があります。この問題に対処するには、v6.0 以降の統計の自動更新を手動でキャンセルできます。

    [<a href="/statistics.md#automatic-update">ユーザードキュメント</a>](/statistics.md#automatic-update)

-   PingCAPクリニック診断サービス（テクニカルプレビュー版）

    PingCAPクリニック は、 TiDB クラスターの診断サービスです。このサービスは、クラスターの問題をリモートでトラブルシューティングするのに役立ち、クラスターのステータスをローカルで簡単に確認できます。 PingCAPクリニックを使用すると、TiDB クラスターのライフサイクル全体を通じて安定した動作を保証し、潜在的な問題を予測し、問題の可能性を減らし、クラスターの問題を迅速にトラブルシューティングできます。

    クラスターの問題をトラブルシューティングするためのリモート アシスタンスについて PingCAP テクニカル サポートに問い合わせる場合、 PingCAPクリニックサービスを使用して診断データを収集およびアップロードすることができるため、トラブルシューティングの効率が向上します。

    [<a href="/clinic/clinic-introduction.md">ユーザードキュメント</a>](/clinic/clinic-introduction.md)

-   エンタープライズレベルのデータベース管理プラットフォーム、TiDB Enterprise Manager

    TiDB Enterprise Manager (TiEM) は、TiDB データベースに基づくエンタープライズ レベルのデータベース管理プラットフォームであり、ユーザーがオンプレミスまたはパブリック クラウド環境で TiDB クラスターを管理できるようにすることを目的としています。

    TiEM は、TiDB クラスターのライフサイクル全体を視覚的に管理するだけでなく、パラメーター管理、バージョン アップグレード、クラスター クローン、アクティブ/スタンバイ クラスター切り替え、データのインポートとエクスポート、データのレプリケーション、データのバックアップと復元サービスなどのワンストップ サービスも提供します。 TiEM は、TiDB 上の DevOps の効率を向上させ、企業の DevOps コストを削減できます。

    現在、TiEM は[<a href="https://en.pingcap.com/tidb-enterprise/">TiDB エンタープライズ</a>](https://en.pingcap.com/tidb-enterprise/)エディションのみで提供されています。 TiEM を入手するには、 [<a href="https://en.pingcap.com/tidb-enterprise/">TiDB エンタープライズ</a>](https://en.pingcap.com/tidb-enterprise/)ページからお問い合わせください。

-   監視コンポーネントの構成のカスタマイズをサポート

    TiUPを使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視コンポーネントを自動的にデプロイし、スケールアウト後に監視スコープに新しいノードを自動的に追加します。 `topology.yaml`ファイルに構成項目を追加することで、監視コンポーネントの構成をカスタマイズできます。

    [<a href="/tiup/customized-montior-in-tiup-environment.md">ユーザードキュメント</a>](/tiup/customized-montior-in-tiup-environment.md)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v6.0.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[<a href="/releases/release-notes.md">リリースノート</a>](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                    | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                                                                                                        |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `placement_checks`                                                                                                                                                                                     | 削除されました  | DDL ステートメントが[<a href="/placement-rules-in-sql.md">SQL の配置ルール</a>](/placement-rules-in-sql.md)で指定された配置ルールを検証するかどうかを制御します。 `tidb_placement_mode`に置き換えられます。                                                                                                                                                                                                                                  |
| `tidb_enable_alter_placement`                                                                                                                                                                          | 削除されました  | [<a href="/placement-rules-in-sql.md">SQL の配置ルール</a>](/placement-rules-in-sql.md)を有効にするかどうかを制御します。                                                                                                                                                                                                                                                                                        |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn`              | 削除されました  | v5.0 以降、これらの変数は`tidb_mem_quota_query`に置き換えられ、 [<a href="/system-variables.md">システム変数</a>](/system-variables.md)ドキュメントから削除されました。互換性を確保するために、これらの変数はソース コード内に保持されています。 TiDB 6.0.0 以降、これらの変数もコードから削除されています。                                                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_enable_mutation_checker-new-in-v600">`tidb_enable_mutation_checker`</a>](/system-variables.md#tidb_enable_mutation_checker-new-in-v600)                            | 新しく追加された | 突然変異チェッカーを有効にするかどうかを制御します。デフォルト値は`ON`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、ミューテーション チェッカーはデフォルトで無効になっています。                                                                                                                                                                                                                                                                           |
| [<a href="/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600">`tidb_ignore_prepared_cache_close_stmt`</a>](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) | 新しく追加された | プリペアドステートメントを閉じるコマンドを無視するかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                                                                                                       |
| [<a href="/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600">`tidb_mem_quota_binding_cache`</a>](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)                            | 新しく追加された | キャッシュ保持のメモリ使用量のしきい値を`binding`設定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                                                                                                                                                                         |
| [<a href="/system-variables.md#tidb_placement_mode-new-in-v600">`tidb_placement_mode`</a>](/system-variables.md#tidb_placement_mode-new-in-v600)                                                       | 新しく追加された | DDL ステートメントが[<a href="/placement-rules-in-sql.md">SQL の配置ルール</a>](/placement-rules-in-sql.md)で指定された配置ルールを無視するかどうかを制御します。デフォルト値は`strict`です。これは、DDL ステートメントが配置ルールを無視しないことを意味します。                                                                                                                                                                                                            |
| [<a href="/system-variables.md#tidb_rc_read_check_ts-new-in-v600">`tidb_rc_read_check_ts`</a>](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                 | 新しく追加された | <ul><li>トランザクション内の読み取りステートメントのレイテンシーを最適化します。読み取り/書き込みの競合がより深刻な場合、この変数をオンにすると、オーバーヘッドとレイテンシーが追加され、パフォーマンスの低下が発生します。デフォルト値は`off`です。</li><li>この変数はまだ[<a href="/system-variables.md#tidb_replica_read-new-in-v40">レプリカ読み取り</a>](/system-variables.md#tidb_replica_read-new-in-v40)と互換性がありません。読み取りリクエストに`tidb_rc_read_check_ts`付いている場合、レプリカ読み取りを使用できない可能性があります。両方の変数を同時にオンにしないでください。</li></ul> |
| [<a href="/system-variables.md#tidb_sysdate_is_now-new-in-v600">`tidb_sysdate_is_now`</a>](/system-variables.md#tidb_sysdate_is_now-new-in-v600)                                                       | 新しく追加された | `SYSDATE`関数を`NOW`関数で置き換えることができるかどうかを制御します。この設定項目は、MySQL オプション[<a href="https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now">`sysdate-is-now`</a>](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。デフォルト値は`OFF`です。                                                                                |
| [<a href="/system-variables.md#tidb_table_cache_lease-new-in-v600">`tidb_table_cache_lease`</a>](/system-variables.md#tidb_table_cache_lease-new-in-v600)                                              | 新しく追加された | [<a href="/cached-tables.md">テーブルキャッシュ</a>](/cached-tables.md)のリース時間を秒単位で制御します。デフォルト値は`3`です。                                                                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600">`tidb_top_sql_max_meta_count`</a>](/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600)                               | 新しく追加された | 収集される SQL ステートメント タイプの最大数を[<a href="/dashboard/top-sql.md">Top SQL</a>](/dashboard/top-sql.md)分あたり 1 つずつ制御します。デフォルト値は`5000`です。                                                                                                                                                                                                                                                            |
| [<a href="/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600">`tidb_top_sql_max_time_series_count`</a>](/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600)          | 新しく追加された | 負荷に最も寄与する SQL ステートメント (つまり、上位 N) を[<a href="/dashboard/top-sql.md">Top SQL</a>](/dashboard/top-sql.md)分あたり 1 つずつ記録できる数を制御します。デフォルト値は`100`です。                                                                                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_txn_assertion_level-new-in-v600">`tidb_txn_assertion_level`</a>](/system-variables.md#tidb_txn_assertion_level-new-in-v600)                                        | 新しく追加された | アサーション レベルを制御します。アサーションは、データとインデックス間の整合性チェックであり、書き込まれるキーがトランザクション コミット プロセスに存在するかどうかをチェックします。デフォルトでは、このチェックではほとんどのチェック項目が有効になり、パフォーマンスにはほとんど影響がありません。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、このチェックはデフォルトで無効になっています。                                                                                                                                                                      |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                                       | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                             |
| :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | 削除されました  | [<a href="/statement-summary-tables.md">ステートメント概要テーブル</a>](/statement-summary-tables.md)に関連するコンフィグレーション。これらの構成項目はすべて削除されます。ステートメント要約テーブルを制御するには、SQL 変数を使用する必要があります。                                                                                                                                            |
| TiDB           | [<a href="/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap">`new_collations_enabled_on_first_bootstrap`</a>](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)         | 修正済み     | 新しい照合順序のサポートを有効にするかどうかを制御します。 v6.0 以降、デフォルト値は`false`から`true`に変更されました。この構成項目は、クラスターが初めて初期化されるときにのみ有効になります。最初のブートストラップの後は、この構成項目を使用して新しい照合順序フレームワークを有効または無効にすることはできません。                                                                                                                                          |
| TiKV           | [<a href="/tikv-configuration-file.md#num-threads-1">`backup.num-threads`</a>](/tikv-configuration-file.md#num-threads-1)                                                                                        | 修正済み     | 値の範囲は`[1, CPU]`に変更されます。                                                                                                                                                                                                                                                                                        |
| TiKV           | [<a href="/tikv-configuration-file.md#apply-max-batch-size">`raftstore.apply-max-batch-size`</a>](/tikv-configuration-file.md#apply-max-batch-size)                                                              | 修正済み     | 最大値は`10240`に変更されます。                                                                                                                                                                                                                                                                                            |
| TiKV           | [<a href="/tikv-configuration-file.md#raft-max-size-per-msg">`raftstore.raft-max-size-per-msg`</a>](/tikv-configuration-file.md#raft-max-size-per-msg)                                                           | 修正済み     | <ul><li>最小値が`0`から`0`より大きい値に変更されます。</li><li>最大値は`3GB`に設定されます。</li><li>単位が`MB`から`KB\|MB\|GB`に変更されます。</li></ul>                                                                                                                                                                                                   |
| TiKV           | [<a href="/tikv-configuration-file.md#store-max-batch-size">`raftstore.store-max-batch-size`</a>](/tikv-configuration-file.md#store-max-batch-size)                                                              | 修正済み     | 最大値は`10240`に設定されます。                                                                                                                                                                                                                                                                                            |
| TiKV           | [<a href="/tikv-configuration-file.md#max-thread-count">`readpool.unified.max-thread-count`</a>](/tikv-configuration-file.md#max-thread-count)                                                                   | 修正済み     | 調整範囲が`[min-thread-count, MAX(4, CPU)]`に変更されます。                                                                                                                                                                                                                                                                 |
| TiKV           | [<a href="/tikv-configuration-file.md#enable-pipelined-write">`rocksdb.enable-pipelined-write`</a>](/tikv-configuration-file.md#enable-pipelined-write)                                                          | 修正済み     | デフォルト値が`true`から`false`に変更されました。この構成が有効な場合、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプライン コミット メカニズムが使用されます。                                                                                                                                                                                                        |
| TiKV           | [<a href="/tikv-configuration-file.md#max-background-flushes">`rocksdb.max-background-flushes`</a>](/tikv-configuration-file.md#max-background-flushes)                                                          | 修正済み     | <ul><li>CPU コア数が 10 の場合、デフォルト値は`3`です。</li><li> CPU コアの数が 8 の場合、デフォルト値は`2`です。</li></ul>                                                                                                                                                                                                                         |
| TiKV           | [<a href="/tikv-configuration-file.md#max-background-jobs">`rocksdb.max-background-jobs`</a>](/tikv-configuration-file.md#max-background-jobs)                                                                   | 修正済み     | <ul><li>CPU コア数が 10 の場合、デフォルト値は`9`です。</li><li> CPU コアの数が 8 の場合、デフォルト値は`7`です。</li></ul>                                                                                                                                                                                                                         |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`profiles.default.dt_enable_logical_split`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                    | 修正済み     | DeltaTree Storage Engine のセグメントが論理分割を使用するかどうかを決定します。デフォルト値が`true`から`false`に変更されました。                                                                                                                                                                                                                            |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`profiles.default.enable_elastic_threadpool`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                  | 修正済み     | エラスティック スレッド プールを有効にするかどうかを制御します。デフォルト値が`false`から`true`に変更されました。                                                                                                                                                                                                                                               |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`storage.format_version`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                      | 修正済み     | TiFlashのデータ検証機能を制御します。デフォルト値が`2`から`3`に変更されました。<br/> `format_version`を`3`に設定すると、ハードウェア障害による誤った読み取りを回避するために、すべてのTiFlashデータの読み取り操作で一貫性チェックが実行されます。<br/>新しいフォーマットのバージョンを v5.4 より前のバージョンにダウングレードすることはできないことに注意してください。                                                                                               |
| TiDB           | [<a href="/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600">`pessimistic-txn.pessimistic-auto-commit`</a>](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)                       | 新しく追加された | 悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` )、自動コミット トランザクションが使用するトランザクション モードを決定します。                                                                                                                                                                                                     |
| TiKV           | [<a href="/tikv-configuration-file.md#in-memory-new-in-v600">`pessimistic-txn.in-memory`</a>](/tikv-configuration-file.md#in-memory-new-in-v600)                                                                 | 新しく追加された | メモリ内の悲観的ロックを有効にするかどうかを制御します。この機能を有効にすると、悲観的トランザクションは、悲観的ロックをディスクに書き込んだり、他のレプリカに複製したりするのではなく、可能な限り TiKVメモリに悲観的ロックを保存します。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われる可能性は低いため、悲観的トランザクションがコミットに失敗する可能性があります。デフォルト値は`true`です。                                                                                  |
| TiKV           | [<a href="/tikv-configuration-file.md#quota">`quota`</a>](/tikv-configuration-file.md#quota)                                                                                                                     | 新しく追加された | フロントエンドリクエストによって占有されるリソースを制限するクォータリミッターに関連する構成項目を追加します。クォータ リミッターは実験的機能であり、デフォルトでは無効になっています。新しいクォータ関連の構成項目は、 `foreground-cpu-time` 、 `foreground-write-bandwidth` 、 `foreground-read-bandwidth` 、および`max-delay-duration`です。                                                                                    |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`profiles.default.dt_compression_method`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                      | 新しく追加された | TiFlashの圧縮アルゴリズムを指定します。オプションの値は`LZ4` 、 `zstd` 、および`LZ4HC`で、すべて大文字と小文字が区別されません。デフォルト値は`LZ4`です。                                                                                                                                                                                                                  |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">`profiles.default.dt_compression_level`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                       | 新しく追加された | TiFlashの圧縮レベルを指定します。デフォルト値は`1`です。                                                                                                                                                                                                                                                                              |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`loaders.&#x3C;name>.import-mode`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)   | 新しく追加された | 完全インポートフェーズ中のインポートモード。 v6.0 以降、DM は TiDB Lightning の TiDB バックエンド モードを使用して、完全なインポート フェーズ中にデータをインポートします。以前の Loaderコンポーネントは使用されなくなりました。これは内部交換であり、日常業務に明らかな影響はありません。<br/>デフォルト値は`sql`に設定されており、これは`tidb-backend`モードを使用することを意味します。まれに、 `tidb-backend`完全な互換性がない可能性があります。このパラメータを`loader`に設定すると、ローダー モードにフォールバックできます。 |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`loaders.&#x3C;name>.on-duplicate`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)  | 新しく追加された | 完全インポートフェーズ中に競合を解決する方法を指定します。デフォルト値は`replace`で、新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                                                                                                                                                                |
| TiCDC          | [<a href="/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka">`dial-timeout`</a>](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                            | 新しく追加された | ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                               |
| TiCDC          | [<a href="/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka">`read-timeout`</a>](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                            | 新しく追加された | ダウンストリーム Kafka から返される応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                           |
| TiCDC          | [<a href="/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka">`write-timeout`</a>](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                           | 新しく追加された | ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                             |

### その他 {#others}

-   データ配置ポリシーには、次の互換性の変更があります。
    -   バインディングはサポートされていません。直接配置オプションが構文から削除されました。
    -   `CREATE PLACEMENT POLICY`および`ALTER PLACEMENT POLICY`ステートメントは、 `VOTERS`および`VOTER_CONSTRAINTS`配置オプションをサポートしなくなりました。
    -   TiDB 移行ツール (TiDB Binlog、TiCDC、およびBR) が配置ルールと互換性を持つようになりました。配置オプションは TiDB Binlogの特別なコメントに移動されました。
    -   `information_schema.placement_rules`システム テーブルの名前が`information_schema.placement_policies`に変更されます。このテーブルには、配置ポリシーに関する情報のみが表示されるようになりました。
    -   `placement_checks`システム変数は`tidb_placement_mode`に置き換えられます。
    -   TiFlashレプリカがあるテーブルに配置ルールを使用してパーティションを追加することは禁止されています。
    -   `INFORMATION_SCHEMA`テーブルから`TIDB_DIRECT_PLACEMENT`列を削除します。
-   SQL プラン管理 (SPM) バインディングの`status`値が変更されます。
    -   `using`を削除します。
    -   `enabled` (利用可能) を追加して`using`を置き換えます。
    -   `disabled`を追加します (使用不可)。
-   DM は OpenAPI インターフェースを変更します
    -   内部機構の変更により、タスク管理に関するインターフェースが以前の実験的版と互換性がありません。適応するには新しい[<a href="/dm/dm-open-api.md">DM OpenAPI ドキュメント</a>](/dm/dm-open-api.md)を参照する必要があります。
-   DM は、完全なインポート段階で競合を解決する方法を変更します。
    -   パラメータが`loader.<name>.on-duplicate`追加されます。デフォルト値は`replace`で、新しいデータを使用して既存のデータを置き換えることを意味します。以前の動作を維持したい場合は、値を`error`に設定できます。このパラメータは、完全なインポート フェーズ中の動作のみを制御します。
-   DM を使用するには、対応するバージョン`dmctl`を使用する必要があります。
    -   内部メカニズムの変更により、DM を v6.0.0 にアップグレードした後、 `dmctl`も v6.0.0 にアップグレードする必要があります。
-   v5.4 (v5.4 のみ) では、TiDB は一部の noop システム変数に不正な値を許可します。 v6.0.0 以降、TiDB ではシステム変数に不正な値を設定することが禁止されています。 [<a href="https://github.com/pingcap/tidb/issues/31538">#31538</a>](https://github.com/pingcap/tidb/issues/31538)

## 改善点 {#improvements}

-   TiDB

    -   `FLASHBACK`または`RECOVER`ステートメントを使用してテーブルを復元した後、テーブルの配置ルール設定を自動的にクリアします[<a href="https://github.com/pingcap/tidb/issues/31668">#31668</a>](https://github.com/pingcap/tidb/issues/31668)
    -   パフォーマンス概要ダッシュボードを追加して、一般的なクリティカル パスに関するコア パフォーマンス メトリクスを表示し、TiDB でのメトリクス分析を容易にします[<a href="https://github.com/pingcap/tidb/issues/31676">#31676</a>](https://github.com/pingcap/tidb/issues/31676)
    -   `LOAD DATA LOCAL INFILE`ステートメントでの`REPLACE`キーワードの使用のサポート[<a href="https://github.com/pingcap/tidb/issues/24515">#24515</a>](https://github.com/pingcap/tidb/issues/24515)
    -   範囲パーティション テーブル[<a href="https://github.com/pingcap/tidb/issues/26739">#26739</a>](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティション プルーニングをサポートします。
    -   MPP 集約クエリで潜在的に冗長な Exchange 操作を排除することで、クエリの効率を向上します[<a href="https://github.com/pingcap/tidb/issues/31762">#31762</a>](https://github.com/pingcap/tidb/issues/31762)
    -   `TRUNCATE PARTITION`と`DROP PARTITION`ステートメントで重複するパーティション名を許可することで、MySQL との互換性を向上します[<a href="https://github.com/pingcap/tidb/issues/31681">#31681</a>](https://github.com/pingcap/tidb/issues/31681)
    -   `ADMIN SHOW DDL JOBS`ステートメント[<a href="https://github.com/pingcap/tidb/issues/23494">#23494</a>](https://github.com/pingcap/tidb/issues/23494)の結果に`CREATE_TIME`情報を表示するサポート
    -   新しい組み込み関数をサポート`CHARSET()` [<a href="https://github.com/pingcap/tidb/issues/3931">#3931</a>](https://github.com/pingcap/tidb/issues/3931)
    -   ユーザー名によるベースライン キャプチャ ブロックリストのフィルタリングをサポート[<a href="https://github.com/pingcap/tidb/issues/32558">#32558</a>](https://github.com/pingcap/tidb/issues/32558)
    -   ベースライン キャプチャ ブロックリストでのワイルドカードの使用のサポート[<a href="https://github.com/pingcap/tidb/issues/32714">#32714</a>](https://github.com/pingcap/tidb/issues/32714)
    -   現在の`time_zone` [<a href="https://github.com/pingcap/tidb/issues/26642">#26642</a>](https://github.com/pingcap/tidb/issues/26642)に従って時間を表示することで、 `ADMIN SHOW DDL JOBS`と`SHOW TABLE STATUS`ステートメントの結果を最適化します。
    -   `DAYNAME()`と`MONTHNAME()`関数をTiFlash [<a href="https://github.com/pingcap/tidb/issues/32594">#32594</a>](https://github.com/pingcap/tidb/issues/32594)にプッシュダウンするサポート
    -   `REGEXP`機能をTiFlash [<a href="https://github.com/pingcap/tidb/issues/32637">#32637</a>](https://github.com/pingcap/tidb/issues/32637)にプッシュダウンするサポート
    -   `DAYOFMONTH()`と`LAST_DAY()`関数をTiFlash [<a href="https://github.com/pingcap/tidb/issues/33012">#33012</a>](https://github.com/pingcap/tidb/issues/33012)にプッシュダウンするサポート
    -   `DAYOFWEEK()`と`DAYOFYEAR()`関数をTiFlash [<a href="https://github.com/pingcap/tidb/issues/33130">#33130</a>](https://github.com/pingcap/tidb/issues/33130)にプッシュダウンするサポート
    -   `IS_TRUE` 、 `IS_FALSE` 、および`IS_TRUE_WITH_NULL`関数のTiFlash [<a href="https://github.com/pingcap/tidb/issues/33047">#33047</a>](https://github.com/pingcap/tidb/issues/33047)へのプッシュダウンをサポート
    -   `GREATEST`と`LEAST`関数をTiFlash [<a href="https://github.com/pingcap/tidb/issues/32787">#32787</a>](https://github.com/pingcap/tidb/issues/32787)にプッシュダウンするサポート
    -   `UnionScan`オペレーター[<a href="https://github.com/pingcap/tidb/issues/32631">#32631</a>](https://github.com/pingcap/tidb/issues/32631)の実行の追跡をサポート
    -   `_tidb_rowid`列[<a href="https://github.com/pingcap/tidb/issues/31543">#31543</a>](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリに対する PointGet プランの使用のサポート
    -   `EXPLAIN`ステートメントの出力で、名前を小文字に変換せずに元のパーティション名を表示するサポート[<a href="https://github.com/pingcap/tidb/issues/32719">#32719</a>](https://github.com/pingcap/tidb/issues/32719)
    -   IN 条件および文字列型列[<a href="https://github.com/pingcap/tidb/issues/32626">#32626</a>](https://github.com/pingcap/tidb/issues/32626)での RANGE COLUMNS パーティションのパーティション プルーニングを有効にする
    -   システム変数が NULL に設定されている場合にエラー メッセージを返す[<a href="https://github.com/pingcap/tidb/issues/32850">#32850</a>](https://github.com/pingcap/tidb/issues/32850)
    -   非 MPP モードからブロードキャスト参加を削除する[<a href="https://github.com/pingcap/tidb/issues/31465">#31465</a>](https://github.com/pingcap/tidb/issues/31465)
    -   動的プルーニング モード[<a href="https://github.com/pingcap/tidb/issues/32347">#32347</a>](https://github.com/pingcap/tidb/issues/32347)でのパーティション化されたテーブルでの MPP プランの実行のサポート
    -   共通テーブル式 (CTE) の述語のプッシュダウンのサポート[<a href="https://github.com/pingcap/tidb/issues/28163">#28163</a>](https://github.com/pingcap/tidb/issues/28163)
    -   `Statement Summary`と`Capture Plan Baselines`の構成を簡素化し、グローバル ベースでのみ利用できるようにする[<a href="https://github.com/pingcap/tidb/issues/30557">#30557</a>](https://github.com/pingcap/tidb/issues/30557)
    -   macOS 12 [<a href="https://github.com/pingcap/tidb/issues/31607">#31607</a>](https://github.com/pingcap/tidb/issues/31607)でバイナリをビルドするときに報告されるアラームに対処するために、gopsutil を v3.21.12 に更新します。

-   TiKV

    -   多くのキー範囲を持つバッチのRaftstoreのサンプリング精度を向上させます[<a href="https://github.com/tikv/tikv/issues/12327">#12327</a>](https://github.com/tikv/tikv/issues/12327)
    -   プロファイルをより簡単に識別できるように、 `debug/pprof/profile`に正しい「Content-Type」を追加します[<a href="https://github.com/tikv/tikv/issues/11521">#11521</a>](https://github.com/tikv/tikv/issues/11521)
    -   Raftstoreにハートビートがあるとき、または読み取りリクエストを処理するときに、リーダーのリース時間を無限に更新します。これにより、レイテンシージッターの削減に役立ちます[<a href="https://github.com/tikv/tikv/issues/11579">#11579</a>](https://github.com/tikv/tikv/issues/11579)
    -   リーダーを切り替えるときに最もコストの低いストアを選択すると、パフォーマンスの安定性が向上します[<a href="https://github.com/tikv/tikv/issues/10602">#10602</a>](https://github.com/tikv/tikv/issues/10602)
    -   Raftログを非同期的に取得して、 Raftstore [<a href="https://github.com/tikv/tikv/issues/11320">#11320</a>](https://github.com/tikv/tikv/issues/11320)のブロックによって引き起こされるパフォーマンスのジッターを軽減します。
    -   ベクトル計算[<a href="https://github.com/tikv/tikv/issues/5751">#5751</a>](https://github.com/tikv/tikv/issues/5751)の`QUARTER`機能をサポート
    -   `BIT`データ型の TiKV [<a href="https://github.com/pingcap/tidb/issues/30738">#30738</a>](https://github.com/pingcap/tidb/issues/30738)へのプッシュダウンをサポート
    -   TiKV [<a href="https://github.com/tikv/tikv/issues/11916">#11916</a>](https://github.com/tikv/tikv/issues/11916)への`MOD`機能と`SYSDATE`機能のプッシュダウンをサポート
    -   ロックの解決ステップ[<a href="https://github.com/tikv/tikv/issues/11993">#11993</a>](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   `raftstore.raft-max-inflight-msgs` [<a href="https://github.com/tikv/tikv/issues/11865">#11865</a>](https://github.com/tikv/tikv/issues/11865)の動的変更をサポート
    -   動的プルーニング モード[<a href="https://github.com/tikv/tikv/issues/11888">#11888</a>](https://github.com/tikv/tikv/issues/11888)を有効にする`EXTRA_PHYSICAL_TABLE_ID_COL_ID`サポート
    -   バケット[<a href="https://github.com/tikv/tikv/issues/11759">#11759</a>](https://github.com/tikv/tikv/issues/11759)での計算をサポート
    -   RawKV API V2 のキーを`user-key` + `memcomparable-padding` + `timestamp` [<a href="https://github.com/tikv/tikv/issues/11965">#11965</a>](https://github.com/tikv/tikv/issues/11965)としてエンコードします。
    -   RawKV API V2 の値を`user-value` + `ttl` + `ValueMeta`としてエンコードし、 `delete` `ValueMeta` [<a href="https://github.com/tikv/tikv/issues/11965">#11965</a>](https://github.com/tikv/tikv/issues/11965)としてエンコードします。
    -   `raftstore.raft-max-size-per-msg` [<a href="https://github.com/tikv/tikv/issues/12017">#12017</a>](https://github.com/tikv/tikv/issues/12017)の動的変更をサポート
    -   Grafana [<a href="https://github.com/tikv/tikv/issues/12014">#12014</a>](https://github.com/tikv/tikv/issues/12014)での multi-k8 の監視のサポート
    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[<a href="https://github.com/tikv/tikv/issues/12111">#12111</a>](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   `raftstore.apply_max_batch_size`と`raftstore.store_max_batch_size`の動的変更をサポート[<a href="https://github.com/tikv/tikv/issues/11982">#11982</a>](https://github.com/tikv/tikv/issues/11982)
    -   RawKV V2 は`raw_get`または`raw_scan`リクエストを受信すると最新バージョンを返します[<a href="https://github.com/tikv/tikv/issues/11965">#11965</a>](https://github.com/tikv/tikv/issues/11965)
    -   RCCheckTS の一貫性読み取り[<a href="https://github.com/tikv/tikv/issues/12097">#12097</a>](https://github.com/tikv/tikv/issues/12097)をサポートします。
    -   動的変更のサポート`storage.scheduler-worker-pool-size` (スケジューラ プールのスレッド数) [<a href="https://github.com/tikv/tikv/issues/12067">#12067</a>](https://github.com/tikv/tikv/issues/12067)
    -   グローバル フォアグラウンド フロー コントローラーを使用して CPU と帯域幅の使用を制御し、TiKV [<a href="https://github.com/tikv/tikv/issues/11855">#11855</a>](https://github.com/tikv/tikv/issues/11855)のパフォーマンスの安定性を向上させます。
    -   動的変更のサポート`readpool.unified.max-thread-count` (UnifyReadPool のスレッド数) [<a href="https://github.com/tikv/tikv/issues/11781">#11781</a>](https://github.com/tikv/tikv/issues/11781)
    -   TiKV 内部パイプラインを使用して RocksDB パイプラインを置き換え、 `rocksdb.enable-multibatch-write`パラメータ[<a href="https://github.com/tikv/tikv/issues/12059">#12059</a>](https://github.com/tikv/tikv/issues/12059)を非推奨にします。

-   PD

    -   リーダーを排除する際に、転送用に最も速いオブジェクトを自動的に選択する機能をサポートします。これにより、排除プロセスのスピードアップに役立ちます[<a href="https://github.com/tikv/pd/issues/4229">#4229</a>](https://github.com/tikv/pd/issues/4229)
    -   リージョンが使用できなくなった場合に備えて、2 レプリカRaftグループから投票者を削除することを禁止します[<a href="https://github.com/tikv/pd/issues/4564">#4564</a>](https://github.com/tikv/pd/issues/4564)
    -   バランスリーダー[<a href="https://github.com/tikv/pd/issues/4652">#4652</a>](https://github.com/tikv/pd/issues/4652)のスケジューリングを高速化します。

-   TiFlash

    -   TiFlashファイルの論理分割を禁止し (デフォルト値の`profiles.default.dt_enable_logical_split`を`false`に調整します。詳細については[<a href="/tiflash/tiflash-configuration.md#tiflash-configuration-parameters">ユーザードキュメント</a>](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)参照)、 TiFlashに同期されたテーブルのスペース占有率が、 TiFlashカラムナstorageのスペース使用効率を向上させます。 TiKV のテーブルの占有
    -   以前のクラスター管理モジュールを TiDB に統合することで、 TiFlashのクラスター管理とレプリカ レプリケーション メカニズムを最適化し、小さなテーブルのレプリカ作成を高速化します[<a href="https://github.com/pingcap/tidb/issues/29924">#29924</a>](https://github.com/pingcap/tidb/issues/29924)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップデータの復元速度が向上しました。 BR が15 ノード (各ノードに 16 個の CPU コアがある) を備えた TiKV クラスターに 16 TB データを復元するシミュレーション テストでは、スループットは 2.66 GiB/秒に達します。 [<a href="https://github.com/pingcap/tidb/issues/27036">#27036</a>](https://github.com/pingcap/tidb/issues/27036)

        -   配置ルールのインポートとエクスポートをサポートします。 `--with-tidb-placement-mode`パラメータを追加して、データのインポート時に配置ルールを無視するかどうかを制御します。 [<a href="https://github.com/pingcap/tidb/issues/32290">#32290</a>](https://github.com/pingcap/tidb/issues/32290)

    -   TiCDC

        -   Grafana [<a href="https://github.com/pingcap/tiflow/issues/4891">#4891</a>](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   サポート配置ルール[<a href="https://github.com/pingcap/tiflow/issues/4846">#4846</a>](https://github.com/pingcap/tiflow/issues/4846)
        -   HTTP API 処理の同期[<a href="https://github.com/pingcap/tiflow/issues/1710">#1710</a>](https://github.com/pingcap/tiflow/issues/1710)
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します[<a href="https://github.com/pingcap/tiflow/issues/3329">#3329</a>](https://github.com/pingcap/tiflow/issues/3329)
        -   MySQL [<a href="https://github.com/pingcap/tiflow/issues/3589">#3589</a>](https://github.com/pingcap/tiflow/issues/3589)のデッドロックを軽減するために、MySQL シンクのデフォルトの分離レベルを読み取りコミットに設定します。
        -   作成時に変更フィードパラメータを検証し、エラーメッセージを修正する[<a href="https://github.com/pingcap/tiflow/issues/1716">#1716</a>](https://github.com/pingcap/tiflow/issues/1716) [<a href="https://github.com/pingcap/tiflow/issues/1718">#1718</a>](https://github.com/pingcap/tiflow/issues/1718) [<a href="https://github.com/pingcap/tiflow/issues/1719">#1719</a>](https://github.com/pingcap/tiflow/issues/1719) [<a href="https://github.com/pingcap/tiflow/issues/4472">#4472</a>](https://github.com/pingcap/tiflow/issues/4472)
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [<a href="https://github.com/pingcap/tiflow/issues/4385">#4385</a>](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。

    -   TiDB データ移行 (DM)

        -   アップストリーム テーブル スキーマに一貫性がなく、楽観的モードである場合のタスクの開始をサポート[<a href="https://github.com/pingcap/tiflow/issues/3629">#3629</a>](https://github.com/pingcap/tiflow/issues/3629) [<a href="https://github.com/pingcap/tiflow/issues/3708">#3708</a>](https://github.com/pingcap/tiflow/issues/3708) [<a href="https://github.com/pingcap/tiflow/issues/3786">#3786</a>](https://github.com/pingcap/tiflow/issues/3786)
        -   `stopped`状態[<a href="https://github.com/pingcap/tiflow/issues/4484">#4484</a>](https://github.com/pingcap/tiflow/issues/4484)でのタスクの作成をサポート
        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[<a href="https://github.com/pingcap/tiflow/issues/4107">#4107</a>](https://github.com/pingcap/tiflow/issues/4107)
        -   事前チェックが改善されました。いくつかの重要なチェックがスキップされなくなりました。 [<a href="https://github.com/pingcap/tiflow/issues/3608">#3608</a>](https://github.com/pingcap/tiflow/issues/3608)

    -   TiDB Lightning

        -   再試行可能なエラー タイプをさらに追加[<a href="https://github.com/pingcap/tidb/issues/31376">#31376</a>](https://github.com/pingcap/tidb/issues/31376)
        -   Base64形式のパスワード文字列[<a href="https://github.com/pingcap/tidb/issues/31194">#31194</a>](https://github.com/pingcap/tidb/issues/31194)をサポートします
        -   エラーコードとエラー出力の標準化[<a href="https://github.com/pingcap/tidb/issues/32239">#32239</a>](https://github.com/pingcap/tidb/issues/32239)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SCHEDULE = majority_in_primary` 、 `PrimaryRegion` 、 `Regions`が同じ値[<a href="https://github.com/pingcap/tidb/issues/31271">#31271</a>](https://github.com/pingcap/tidb/issues/31271)の場合、TiDB が配置ルールを含むテーブルの作成に失敗するバグを修正
    -   インデックス検索結合[<a href="https://github.com/pingcap/tidb/issues/30468">#30468</a>](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正しました。
    -   `show grants` 2 つ以上の権限が付与されている場合に不正な結果が返されるバグを修正[<a href="https://github.com/pingcap/tidb/issues/30855">#30855</a>](https://github.com/pingcap/tidb/issues/30855)
    -   デフォルトで`CURRENT_TIMESTAMP` [<a href="https://github.com/pingcap/tidb/issues/29926">#29926</a>](https://github.com/pingcap/tidb/issues/29926)に設定されているフィールドのタイムスタンプを`INSERT INTO t1 SET timestamp_col = DEFAULT`にするとタイムスタンプが 0 に設定されてしまうバグを修正
    -   文字列タイプ[<a href="https://github.com/pingcap/tidb/issues/31721">#31721</a>](https://github.com/pingcap/tidb/issues/31721)の最大値と最小の非 null 値のエンコードを回避することで、結果の読み取り時に報告されたエラーを修正しました。
    -   エスケープ文字[<a href="https://github.com/pingcap/tidb/issues/31589">#31589</a>](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のロード データpanicを修正
    -   照合順序のある`greatest`または`least`関数が間違った結果を取得する問題を修正[<a href="https://github.com/pingcap/tidb/issues/31789">#31789</a>](https://github.com/pingcap/tidb/issues/31789)
    -   date_add 関数と date_sub関数が間違ったデータ型を返す可能性があるバグを修正しました[<a href="https://github.com/pingcap/tidb/issues/31809">#31809</a>](https://github.com/pingcap/tidb/issues/31809)
    -   insert ステートメントを使用して仮想生成された列にデータを挿入するときに発生する可能性のあるpanicを修正しました[<a href="https://github.com/pingcap/tidb/issues/31735">#31735</a>](https://github.com/pingcap/tidb/issues/31735)
    -   作成したリストパーティション[<a href="https://github.com/pingcap/tidb/issues/31784">#31784</a>](https://github.com/pingcap/tidb/issues/31784)に重複カラムが存在してもエラーが報告されないバグを修正
    -   `select for update union select`間違ったスナップショットを使用した場合に返される間違った結果を修正[<a href="https://github.com/pingcap/tidb/issues/31530">#31530</a>](https://github.com/pingcap/tidb/issues/31530)
    -   復元操作の完了後にリージョンが不均等に分散される可能性がある潜在的な問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31034">#31034</a>](https://github.com/pingcap/tidb/issues/31034)
    -   `json`タイプ[<a href="https://github.com/pingcap/tidb/issues/31541">#31541</a>](https://github.com/pingcap/tidb/issues/31541)の COERCIBILITY が間違っているバグを修正
    -   この型が組み込み機能[<a href="https://github.com/pingcap/tidb/issues/31320">#31320</a>](https://github.com/pingcap/tidb/issues/31320)を使用して処理される場合、 `json`型の間違った照合順序を修正しました。
    -   TiFlashレプリカ数を 0 [<a href="https://github.com/pingcap/tidb/issues/32190">#32190</a>](https://github.com/pingcap/tidb/issues/32190)に設定すると PD ルールが削除されないバグを修正
    -   `alter column set default`テーブル スキーマが誤って更新される問題を修正[<a href="https://github.com/pingcap/tidb/issues/31074">#31074</a>](https://github.com/pingcap/tidb/issues/31074)
    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`を処理する問題を修正します[<a href="https://github.com/pingcap/tidb/issues/32232">#32232</a>](https://github.com/pingcap/tidb/issues/32232)
    -   結合[<a href="https://github.com/pingcap/tidb/issues/31629">#31629</a>](https://github.com/pingcap/tidb/issues/31629)を使用したパーティションテーブルの更新時にエラーが発生することがあるバグを修正
    -   Enum 値[<a href="https://github.com/pingcap/tidb/issues/32428">#32428</a>](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   `upper()`および`lower()`関数で発生する可能性のあるpanicを修正[<a href="https://github.com/pingcap/tidb/issues/32488">#32488</a>](https://github.com/pingcap/tidb/issues/32488)
    -   他のタイプの列をタイムスタンプ タイプの列[<a href="https://github.com/pingcap/tidb/issues/29585">#29585</a>](https://github.com/pingcap/tidb/issues/29585)に変更するときに発生するタイム ゾーンの問題を修正します。
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[<a href="https://github.com/pingcap/tidb/issues/31981">#31981</a>](https://github.com/pingcap/tidb/issues/31981) [<a href="https://github.com/pingcap/tidb/issues/30880">#30880</a>](https://github.com/pingcap/tidb/issues/30880)
    -   動的パーティションプルーニングモード[<a href="https://github.com/pingcap/tidb/issues/32516">#32516</a>](https://github.com/pingcap/tidb/issues/32516)でサブSELECT LIMITが期待通りに動作しないバグを修正
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[<a href="https://github.com/pingcap/tidb/issues/32655">#32655</a>](https://github.com/pingcap/tidb/issues/32655)のビットデフォルト値の間違った形式または一貫性のない形式を修正しました。
    -   サーバーの再起動後にパーティション テーブルのリストを作成する場合にパーティション テーブルのプルーニングが機能しない可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/32416">#32416</a>](https://github.com/pingcap/tidb/issues/32416)
    -   `SET timestamp`の実行後に`add column`間違ったデフォルトのタイムスタンプを使用する可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/31968">#31968</a>](https://github.com/pingcap/tidb/issues/31968)
    -   MySQL 5.5 または 5.6 クライアントから TiDB パスワードなしアカウントへの接続が失敗することがあるバグを修正しました[<a href="https://github.com/pingcap/tidb/issues/32334">#32334</a>](https://github.com/pingcap/tidb/issues/32334)
    -   トランザクション[<a href="https://github.com/pingcap/tidb/issues/29851">#29851</a>](https://github.com/pingcap/tidb/issues/29851)の動的モードでパーティション化されたテーブルを読み取るときの誤った結果を修正しました。
    -   TiDB が重複したタスクをTiFlash [<a href="https://github.com/pingcap/tidb/issues/32814">#32814</a>](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   `timdiff`関数の入力にミリ秒が含まれている場合に返される間違った結果を修正しました[<a href="https://github.com/pingcap/tidb/issues/31680">#31680</a>](https://github.com/pingcap/tidb/issues/31680)
    -   明示的にパーティションを読み取り、IndexJoin プラン[<a href="https://github.com/pingcap/tidb/issues/32007">#32007</a>](https://github.com/pingcap/tidb/issues/32007)を使用する場合の誤った結果を修正しました。
    -   列の型を同時に変更すると列名の変更が失敗するバグを修正[<a href="https://github.com/pingcap/tidb/issues/31075">#31075</a>](https://github.com/pingcap/tidb/issues/31075)
    -   TiFlashプランの純コストの計算式が TiKV プラン[<a href="https://github.com/pingcap/tidb/issues/30103">#30103</a>](https://github.com/pingcap/tidb/issues/30103)と一致しないバグを修正
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならないバグを修正[<a href="https://github.com/pingcap/tidb/issues/24031">#24031</a>](https://github.com/pingcap/tidb/issues/24031)
    -   生成された列を含むテーブルをクエリするときに発生する可能性のある間違った結果を修正します[<a href="https://github.com/pingcap/tidb/issues/33038">#33038</a>](https://github.com/pingcap/tidb/issues/33038)
    -   `left join` [<a href="https://github.com/pingcap/tidb/issues/31321">#31321</a>](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   `SUBTIME`関数がオーバーフローの場合に間違った結果を返すバグを修正[<a href="https://github.com/pingcap/tidb/issues/31868">#31868</a>](https://github.com/pingcap/tidb/issues/31868)
    -   集計クエリに`having`条件[<a href="https://github.com/pingcap/tidb/issues/33166">#33166</a>](https://github.com/pingcap/tidb/issues/33166)が含まれる場合、 `selection`演算子をプッシュダウンできないバグを修正
    -   クエリがエラーを報告すると CTE がブロックされる可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/31302">#31302</a>](https://github.com/pingcap/tidb/issues/31302)
    -   非厳密モードでテーブルを作成するときに varbinary または varchar 列の長さが長すぎるとエラーが発生する可能性があるバグを修正[<a href="https://github.com/pingcap/tidb/issues/30328">#30328</a>](https://github.com/pingcap/tidb/issues/30328)
    -   フォロワーが指定されていない場合の`information_schema.placement_policies`のフォロワー数が間違っていたのを修正[<a href="https://github.com/pingcap/tidb/issues/31702">#31702</a>](https://github.com/pingcap/tidb/issues/31702)
    -   TiDB がインデックスの作成時に列のプレフィックス長を 0 として指定できる問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31972">#31972</a>](https://github.com/pingcap/tidb/issues/31972)
    -   TiDB でスペースで終わるパーティション名が許可される問題を修正[<a href="https://github.com/pingcap/tidb/issues/31535">#31535</a>](https://github.com/pingcap/tidb/issues/31535)
    -   `RENAME TABLE`ステートメント[<a href="https://github.com/pingcap/tidb/issues/29893">#29893</a>](https://github.com/pingcap/tidb/issues/29893)のエラー メッセージを修正します。

-   TiKV

    -   ピアのステータスが`Applying` [<a href="https://github.com/tikv/tikv/issues/11746">#11746</a>](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合の QPS ドロップの問題を修正します[<a href="https://github.com/tikv/tikv/issues/11424">#11424</a>](https://github.com/tikv/tikv/issues/11424)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/10210">#10210</a>](https://github.com/tikv/tikv/issues/10210)
    -   GC ワーカーがビジー状態[<a href="https://github.com/tikv/tikv/issues/11903">#11903</a>](https://github.com/tikv/tikv/issues/11903)の場合、TiKV が一定範囲のデータを削除できない (内部コマンド`unsafe_destroy_range`が実行されることを意味します) というバグを修正します。
    -   一部の特殊なケースで`StoreMeta`のデータが誤って削除された場合に TiKV がパニックになるバグを修正[<a href="https://github.com/tikv/tikv/issues/11852">#11852</a>](https://github.com/tikv/tikv/issues/11852)
    -   ARM プラットフォームでプロファイリングを実行すると TiKV がパニックになるバグを修正[<a href="https://github.com/tikv/tikv/issues/10658">#10658</a>](https://github.com/tikv/tikv/issues/10658)
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[<a href="https://github.com/tikv/tikv/issues/11940">#11940</a>](https://github.com/tikv/tikv/issues/11940)
    -   SSE 命令セット[<a href="https://github.com/tikv/tikv/issues/12034">#12034</a>](https://github.com/tikv/tikv/issues/12034)の欠落によって引き起こされる ARM64アーキテクチャでのコンパイルの問題を修正
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[<a href="https://github.com/tikv/tikv/issues/10533">#10533</a>](https://github.com/tikv/tikv/issues/10533)
    -   古いメッセージによって TiKV がpanicになるバグを修正[<a href="https://github.com/tikv/tikv/issues/12023">#12023</a>](https://github.com/tikv/tikv/issues/12023)
    -   TsSet変換[<a href="https://github.com/tikv/tikv/issues/12070">#12070</a>](https://github.com/tikv/tikv/issues/12070)で未定義動作(UB)が発生する場合がある問題を修正
    -   レプリカの読み取りが線形化可能性[<a href="https://github.com/tikv/tikv/issues/12109">#12109</a>](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[<a href="https://github.com/tikv/tikv/issues/9765">#9765</a>](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[<a href="https://github.com/tikv/tikv/issues/12329">#12329</a>](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   メモリメトリクス[<a href="https://github.com/tikv/tikv/issues/12160">#12160</a>](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV [<a href="https://github.com/tikv/tikv/issues/12231">#12231</a>](https://github.com/tikv/tikv/issues/12231)を終了するときに TiKV パニックを誤って報告する潜在的な問題を修正

-   PD

    -   PD が共同合意[<a href="https://github.com/tikv/pd/issues/4362">#4362</a>](https://github.com/tikv/pd/issues/4362)の無意味なステップを持つオペレーターを生成する問題を修正
    -   PD クライアント[<a href="https://github.com/tikv/pd/issues/4549">#4549</a>](https://github.com/tikv/pd/issues/4549)を閉じるときに TSO 取り消しプロセスが停止することがあるバグを修正
    -   リージョンスキャッタラー スケジューリングで一部のピアが失われる問題を修正します[<a href="https://github.com/tikv/pd/issues/4565">#4565</a>](https://github.com/tikv/pd/issues/4565)
    -   `dr-autosync`の`Duration`フィールドを動的に設定できない問題を修正[<a href="https://github.com/tikv/pd/issues/4651">#4651</a>](https://github.com/tikv/pd/issues/4651)

-   TiFlash

    -   メモリ制限が有効になっている場合に発生するTiFlashpanicの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/3902">#3902</a>](https://github.com/pingcap/tiflash/issues/3902)
    -   期限切れデータのリサイクルが遅い問題を修正[<a href="https://github.com/pingcap/tiflash/issues/4146">#4146</a>](https://github.com/pingcap/tiflash/issues/4146)
    -   `Snapshot`が複数の DDL 操作と同時に適用される場合のTiFlashpanicの潜在的な問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4072">#4072</a>](https://github.com/pingcap/tiflash/issues/4072)
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[<a href="https://github.com/pingcap/tiflash/issues/3967">#3967</a>](https://github.com/pingcap/tiflash/issues/3967)
    -   負の引数を持つ`SQRT`関数が`Null` [<a href="https://github.com/pingcap/tiflash/issues/3598">#3598</a>](https://github.com/pingcap/tiflash/issues/3598)ではなく`NaN`を返す問題を修正
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/3920">#3920</a>](https://github.com/pingcap/tiflash/issues/3920)
    -   複数値式[<a href="https://github.com/pingcap/tiflash/issues/4016">#4016</a>](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[<a href="https://github.com/pingcap/tiflash/issues/4036">#4036</a>](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   同時実行性の高いシナリオ[<a href="https://github.com/pingcap/tiflash/issues/3555">#3555</a>](https://github.com/pingcap/tiflash/issues/3555)で学習者の読み取りプロセスに時間がかかりすぎる問題を修正します。
    -   `DATETIME`から`DECIMAL` [<a href="https://github.com/pingcap/tiflash/issues/4151">#4151</a>](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[<a href="https://github.com/pingcap/tiflash/issues/4098">#4098</a>](https://github.com/pingcap/tiflash/issues/4098)
    -   エラスティック スレッド プールを有効にするとメモリリークが発生する可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4098">#4098</a>](https://github.com/pingcap/tiflash/issues/4098)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[<a href="https://github.com/pingcap/tiflash/issues/4229">#4229</a>](https://github.com/pingcap/tiflash/issues/4229)
    -   HashJoin ビルド側の失敗により MPP クエリが永久にハングする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4195">#4195</a>](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[<a href="https://github.com/pingcap/tiflash/issues/4238">#4238</a>](https://github.com/pingcap/tiflash/issues/4238)

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作で回復不能なエラーが発生した場合にBR がスタックするバグを修正[<a href="https://github.com/pingcap/tidb/issues/33200">#33200</a>](https://github.com/pingcap/tidb/issues/33200)
        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正しました[<a href="https://github.com/pingcap/tidb/issues/32423">#32423</a>](https://github.com/pingcap/tidb/issues/32423)

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4501">#4501</a>](https://github.com/pingcap/tiflow/issues/4501)
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4248">#4248</a>](https://github.com/pingcap/tiflow/issues/4248)
        -   一部の MySQL バージョン[<a href="https://github.com/pingcap/tiflow/issues/4504">#4504</a>](https://github.com/pingcap/tiflow/issues/4504)のエラー`Unknown system variable 'transaction_isolation'`を修正
        -   `Canal-JSON` `string` [<a href="https://github.com/pingcap/tiflow/issues/4635">#4635</a>](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性がある TiCDCpanicの問題を修正
        -   場合によってはシーケンスが不正に複製されるバグを修正[<a href="https://github.com/pingcap/tiflow/issues/4552">#4563</a>](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON`が nil [<a href="https://github.com/pingcap/tiflow/issues/4736">#4736</a>](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性がある TiCDCpanic問題を修正
        -   タイプ`Enum/Set`および`TinyText/MediumText/Text/LongText`の avro コーデックの誤ったデータ マッピングを修正[<a href="https://github.com/pingcap/tiflow/issues/4454">#4454</a>](https://github.com/pingcap/tiflow/issues/4454)
        -   Avro が`NOT NULL`列を Nullable フィールド[<a href="https://github.com/pingcap/tiflow/issues/4818">#4818</a>](https://github.com/pingcap/tiflow/issues/4818)に変換するバグを修正
        -   TiCDC が終了できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/4699">#4699</a>](https://github.com/pingcap/tiflow/issues/4699)

    -   TiDB データ移行 (DM)

        -   ステータス[<a href="https://github.com/pingcap/tiflow/issues/4281">#4281</a>](https://github.com/pingcap/tiflow/issues/4281)をクエリする場合にのみ同期メトリクスが更新される問題を修正
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーpanic[<a href="https://github.com/pingcap/tiflow/issues/4317">#4317</a>](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   long varchar がエラーを報告するバグを修正`Column length too big` [<a href="https://github.com/pingcap/tiflow/issues/4637">#4637</a>](https://github.com/pingcap/tiflow/issues/4637)
        -   複数の DM ワーカーが同じアップストリーム[<a href="https://github.com/pingcap/tiflow/issues/3737">#3737</a>](https://github.com/pingcap/tiflow/issues/3737)からデータを書き込むことによって引き起こされる競合の問題を修正します。
        -   ログに何百もの「チェックポイントに変更はありません。同期フラッシュ チェックポイントをスキップします」と出力され、レプリケーションが非常に遅くなる問題を修正します[<a href="https://github.com/pingcap/tiflow/issues/4619">#4619</a>](https://github.com/pingcap/tiflow/issues/4619)
        -   悲観的モード[<a href="https://github.com/pingcap/tiflow/issues/5002">#5002</a>](https://github.com/pingcap/tiflow/issues/5002)でシャードをマージし、アップストリームから増分データをレプリケートするときの DML 損失の問題を修正します。

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[<a href="https://github.com/pingcap/tidb/issues/28144">#28144</a>](https://github.com/pingcap/tidb/issues/28144)
        -   ソース ファイルとターゲット クラスターのテーブル名が異なる場合に発生するpanicを修正します[<a href="https://github.com/pingcap/tidb/issues/31771">#31771</a>](https://github.com/pingcap/tidb/issues/31771)
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [<a href="https://github.com/pingcap/tidb/issues/32733">#32733</a>](https://github.com/pingcap/tidb/issues/32733)を修正
        -   TiDB Lightning が空のテーブルのチェックに失敗するとスタックする問題を修正[<a href="https://github.com/pingcap/tidb/issues/31797">#31797</a>](https://github.com/pingcap/tidb/issues/31797)

    -   Dumpling

        -   `dumpling --sql $query` [<a href="https://github.com/pingcap/tidb/issues/30532">#30532</a>](https://github.com/pingcap/tidb/issues/30532)実行時に表示される進行状況が不正確になる問題を修正
        -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正します[<a href="https://github.com/pingcap/tidb/issues/30534">#30534</a>](https://github.com/pingcap/tidb/issues/30534)

    -   TiDBBinlog

        -   大規模なアップストリーム書き込みトランザクションが Kafka [<a href="https://github.com/pingcap/tidb-binlog/issues/1136">#1136</a>](https://github.com/pingcap/tidb-binlog/issues/1136)にレプリケートされるときに、TiDB Binlogがスキップされる可能性がある問題を修正します。

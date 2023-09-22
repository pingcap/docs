---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 リリースノート {#tidb-6-0-0-release-notes}

発売日：2022年4月7日

TiDB バージョン: 6.0.0-DMR

> **ノート：**
>
> TiDB 6.0.0-DMR のドキュメントは[アーカイブされた](https://docs-archive.pingcap.com/tidb/v6.0/)になりました。 PingCAP では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

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

また、TiDB の HTAP ソリューションの中核コンポーネントとして、 TiFlash <sup>TM は</sup>このリリースで正式にオープンソースになります。詳細は[TiFlashリポジトリ](https://github.com/pingcap/tiflash)を参照してください。

## リリース戦略の変更 {#release-strategy-changes}

TiDB v6.0.0 以降、TiDB は 2 種類のリリースを提供します。

-   長期サポートのリリース

    長期サポート (LTS) リリースは、約 6 か月ごとにリリースされます。 LTS リリースでは、新機能と改善が導入され、リリース ライフサイクル内でパッチ リリースが受け入れられます。たとえば、v6.1.0 は LTS リリースになります。

-   開発マイルストーンのリリース

    開発マイルストーン リリース (DMR) は、約 2 か月ごとにリリースされます。 DMR は新機能と改善を導入しますが、パッチ リリースは受け入れません。ユーザーが本番環境で DMR を使用することはお勧めできません。たとえば、v6.0.0-DMR は DMR です。

TiDB v6.0.0 は DMR であり、そのバージョンは 6.0.0-DMR です。

## 新機能 {#new-features}

### SQL {#sql}

-   データの SQL ベースの配置ルール

    TiDB は、拡張性に優れた分散データベースです。通常、データは複数のサーバー、さらには複数のデータセンターに展開されます。したがって、データ スケジュール管理は TiDB の最も重要な基本機能の 1 つです。ほとんどの場合、ユーザーはデータのスケジュールと管理の方法を気にする必要はありません。しかし、アプリケーションの複雑さの増大に伴い、分離とアクセスレイテンシーによって引き起こされるデプロイメントの変更が TiDB にとって新たな課題となっています。 TiDB は v6.0.0 以降、SQL インターフェースに基づいたデータのスケジューリングおよび管理機能を正式に提供しています。レプリカの数、ロールの種類、データの配置場所などの次元での柔軟なスケジューリングと管理をサポートします。 TiDB は、マルチサービス共有クラスターおよびクロス AZ デプロイメントでのデータ配置のより柔軟な管理もサポートしています。

    [ユーザードキュメント](/placement-rules-in-sql.md)

-   データベースによるTiFlashレプリカの構築をサポートします。データベース内のすべてのテーブルにTiFlashレプリカを追加するには、単一の SQL ステートメントを使用するだけで済み、運用とメンテナンスのコストが大幅に節約されます。

    [ユーザードキュメント](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### トランザクション {#transaction}

-   カーネル レベルでのデータ インデックスの整合性チェックを追加する

    トランザクションの実行時にデータ インデックスの整合性チェックを追加します。これにより、リソースのオーバーヘッドが非常に低くなり、システムの安定性と堅牢性が向上します。 `tidb_enable_mutation_checker`および`tidb_txn_assertion_level`変数を使用してチェック動作を制御できます。デフォルト設定では、ほとんどのシナリオで QPS 低下は 2% 以内に制御されます。整合性チェックのエラーの説明については、 [ユーザードキュメント](/troubleshoot-data-inconsistency-errors.md)を参照してください。

### 可観測性 {#observability}

-   Top SQL: 非専門家向けのパフォーマンス診断

    Top SQLは、DBA およびアプリ開発者向けの TiDB ダッシュボードの自己サービス型データベース パフォーマンス監視および診断機能であり、TiDB v6.0 で一般提供されるようになりました。

    専門家向けの既存の診断機能とは異なり、 Top SQL は非専門家向けに設計されています。相関関係を見つけたり、 Raft Snapshot、RocksDB、MVCC、TSO などの TiDB 内部メカニズムを理解するために何千もの監視チャートを横断する必要はありません。 Top SQLを使用してデータベースの負荷を迅速に分析し、アプリのパフォーマンスを向上させるには、基本的なデータベースの知識 (インデックス、ロックの競合、実行プランなど) のみが必要です。

    Top SQL はデフォルトでは有効になっていません。 Top SQLを有効にすると、各 TiKV ノードまたは TiDB ノードのリアルタイムの CPU 負荷が提供されます。したがって、高い CPU 負荷を消費する SQL ステートメントを一目で特定し、データベースのホットスポットや突然の負荷の増加などの問題を迅速に分析できます。たとえば、 Top SQL を使用すると、単一 TiKV ノードの CPU の 90% を消費する異常なクエリを特定して診断できます。

    [ユーザードキュメント](/dashboard/top-sql.md)

-   継続的プロファイリングのサポート

    TiDB ダッシュボードには継続プロファイリング機能が導入されており、この機能は TiDB v6.0 で一般提供されるようになりました。継続的プロファイリングはデフォルトでは有効になっていません。有効にすると、個々の TiDB、TiKV、PD インスタンスのパフォーマンス データが常に収集され、オーバーヘッドは無視できます。履歴パフォーマンス データを使用すると、問題の再現が難しい場合でも、技術専門家はメモリ消費量の多さなどの問題の根本原因を遡って特定できます。このようにして、平均回復時間 (MTTR) を短縮できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

### パフォーマンス {#performance}

-   キャッシュホットスポットの小さなテーブル

    ホットスポットの小さなテーブルにアクセスするシナリオのユーザー アプリケーションの場合、TiDB はホットスポット テーブルのメモリへの明示的なキャッシュをサポートします。これにより、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが短縮されます。このソリューションにより、サードパーティのキャッシュ ミドルウェアの導入を効果的に回避し、アーキテクチャの複雑さを軽減し、運用とメンテナンスのコストを削減できます。このソリューションは、構成テーブルや為替レート テーブルなど、小さなテーブルが頻繁にアクセスされるが、ほとんど更新されないシナリオに適しています。

    [ユーザードキュメント](/cached-tables.md) [#25293](https://github.com/pingcap/tidb/issues/25293)

-   インメモリ悲観的ロック

    TiDB v6.0.0 以降、メモリ内の悲観的ロックはデフォルトで有効になっています。この機能を有効にすると、悲観的トランザクション ロックがメモリ内で管理されます。これにより、悲観的ロックの持続とロック情報のRaftレプリケーションが回避され、悲観的トランザクション ロックの管理にかかるオーバーヘッドが大幅に削減されます。悲観的ロックによって引き起こされるパフォーマンスのボトルネックの下では、悲観的ロックのメモリ最適化により、レイテンシーを効果的に 10% 削減し、QPS を 10% 向上させることができます。

    [ユーザードキュメント](/pessimistic-transaction.md#in-memory-pessimistic-lock) [#11452](https://github.com/tikv/tikv/issues/11452)

-   Read Committed 分離レベルで TSO を取得するための最適化

    クエリのレイテンシーを短縮するため、読み取り/書き込みの競合がまれな場合、TiDB は[コミットされた分離レベルの読み取り](/transaction-isolation-levels.md#read-committed-isolation-level)に`tidb_rc_read_check_ts`システム変数を追加して、不必要な TSO を減らします。この変数はデフォルトでは無効になっています。変数が有効になっている場合、この最適化により重複した TSO の取得が回避され、読み取り/書き込みの競合がないシナリオでのレイテンシーが短縮されます。ただし、読み取り/書き込みの競合が頻繁に発生するシナリオでは、この変数を有効にするとパフォーマンスの低下が発生する可能性があります。

    [ユーザードキュメント](/transaction-isolation-levels.md#read-committed-isolation-level) [#33159](https://github.com/pingcap/tidb/issues/33159)

-   プリペアドステートメントを強化して実行計画を共有する

    SQL 実行プランを再利用すると、SQL ステートメントの解析時間を効果的に短縮し、CPU リソースの消費を減らし、SQL 実行効率を向上させることができます。 SQL チューニングの重要な方法の 1 つは、SQL 実行プランを効果的に再利用することです。 TiDB は、プリペアド ステートメントを使用した実行計画の共有をサポートしています。ただし、準備されたステートメントが閉じられると、TiDB は対応するプラン キャッシュを自動的にクリアします。その後、TiDB は繰り返される SQL ステートメントを不必要に解析し、実行効率に影響を与える可能性があります。 v6.0.0 以降、TiDB は`tidb_ignore_prepared_cache_close_stmt`パラメータによる`COM_STMT_CLOSE`コマンドを無視するかどうかの制御をサポートしています (デフォルトでは無効)。このパラメーターが有効な場合、TiDB はプリペアド ステートメントを閉じるコマンドを無視し、実行プランをキャッシュに保持するため、実行プランの再利用率が向上します。

    [ユーザードキュメント](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) [#31056](https://github.com/pingcap/tidb/issues/31056)

-   クエリのプッシュダウンを改善する

    コンピューティングとstorageを分離するネイティブアーキテクチャにより、TiDB は演算子をプッシュダウンすることで無効なデータをフィルタリングして除外することをサポートします。これにより、TiDB と TiKV 間のデータ送信が大幅に削減され、クエリ効率が向上します。 v6.0.0 では、TiDB は、より多くの式と`BIT`データ型を TiKV にプッシュダウンすることをサポートし、式とデータ型を計算する際のクエリ効率を向上させます。

    [ユーザードキュメント](/functions-and-operators/expressions-pushed-down.md) [#30738](https://github.com/pingcap/tidb/issues/30738)

-   ホットスポットインデックスの最適化

    単調増加するデータをバッチでセカンダリ インデックスに書き込むと、インデックス ホットスポットが発生し、全体的な書き込みスループットに影響します。 v6.0.0 以降、TiDB は書き込みパフォーマンスを向上させるために`tidb_shard`関数を使用したインデックス ホットスポットの分散をサポートしています。現在、 `tidb_shard`一意のセカンダリ インデックスに対してのみ有効です。このアプリケーションフレンドリーなソリューションでは、元のクエリ条件を変更する必要がありません。このソリューションは、高い書き込みスループット、ポイント クエリ、およびバッチ ポイント クエリのシナリオで使用できます。範囲クエリによって分散されたデータをアプリケーションで使用すると、パフォーマンスの低下が発生する可能性があることに注意してください。したがって、このような場合には検証せずにこの機能を使用しないでください。

    [ユーザードキュメント](/functions-and-operators/tidb-functions.md#tidb_shard) [#31040](https://github.com/pingcap/tidb/issues/31040)

-   TiFlash MPP エンジンでパーティション化されたテーブルの動的プルーニング モードをサポート (実験的)

    このモードでは、TiDB はTiFlashの MPP エンジンを使用してパーティション テーブル上のデータを読み取り、計算できます。これにより、パーティション テーブルのクエリ パフォーマンスが大幅に向上します。

    [ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

-   MPP エンジンのコンピューティング パフォーマンスを向上させる

    -   より多くの関数と演算子を MPP エンジンにプッシュダウンするサポート

        -   `IS NOT`関数： `IS`
        -   文字`NOT REGEXP()`関数: `REGEXP()`
        -   数学関数: `GREATEST(int/real)` 、 `LEAST(int/real)`
        -   日付関数: `DAYNAME()` 、 `DAYOFMONTH()` 、 `DAYOFWEEK()` 、 `DAYOFYEAR()` 、 `LAST_DAY()` 、 `MONTHNAME()`
        -   演算子: アンチ左アウター セミ ジョイン、左アウター セミ ジョイン

        [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)

    -   エラスティック スレッド プール (デフォルトで有効) が GA になります。この機能は、CPU 使用率を改善することを目的としています。

        [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### 安定性 {#stability}

-   実行計画のベースライン取得を強化する

    テーブル名、頻度、ユーザー名などのディメンションを含むブロックリストを追加することで、実行計画のベースライン キャプチャの使いやすさが向上します。バインディングをキャッシュするためのメモリ管理を最適化する新しいアルゴリズムを導入します。ベースライン キャプチャを有効にすると、システムはほとんどの OLTP クエリのバインディングを自動的に作成します。バインドされたステートメントの実行計画は固定されており、実行計画の変更によるパフォーマンスの問題を回避します。ベースライン キャプチャは、メジャー バージョンのアップグレードやクラスターの移行などのシナリオに適用でき、実行計画の回帰によって引き起こされるパフォーマンスの問題を軽減するのに役立ちます。

    [ユーザードキュメント](/sql-plan-management.md#baseline-capturing) [#32466](https://github.com/pingcap/tidb/issues/32466)

-   TiKV クォータ リミッターのサポート (実験的)

    TiKV を使用してデプロイされたマシンのリソースが限られており、フォアグラウンドに過剰な量のリクエストの負担がかかる場合、バックグラウンドの CPU リソースがフォアグラウンドによって占有され、TiKV のパフォーマンスが不安定になります。 TiDB v6.0.0 では、クォータ関連の構成項目を使用して、CPU や読み取り/書き込み帯域幅など、フォアグラウンドで使用されるリソースを制限できます。これにより、長期にわたる高負荷のワークロード下でのクラスターの安定性が大幅に向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#quota) [#12131](https://github.com/tikv/tikv/issues/12131)

-   TiFlashで zstd 圧縮アルゴリズムをサポート

    TiFlash、ユーザーがパフォーマンスと容量のバランスに基づいて最適な圧縮アルゴリズムを選択できるようにする 2 つのパラメーター`profiles.default.dt_compression_method`と`profiles.default.dt_compression_level`が導入されています。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   デフォルトですべての I/O チェック (チェックサム) を有効にする

    この機能は、v5.4.0 で実験的に導入されました。ユーザーのビジネスに明らかな影響を与えることなく、データの正確性とセキュリティを強化します。

    警告: 新しいバージョンのデータ形式を v5.4.0 より前のバージョンにダウングレードすることはできません。このようなダウングレード中は、 TiFlashレプリカを削除し、ダウングレード後にデータを複製する必要があります。または、 [dttool 移行](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してダウングレードを実行することもできます。

    [ユーザードキュメント](/tiflash/tiflash-data-validation.md)

-   スレッド使用率の向上

    TiFlash、非同期 gRPC および Min-TSO スケジューリング メカニズムが導入されています。このようなメカニズムにより、スレッドがより効率的に使用され、過剰なスレッドによって引き起こされるシステムクラッシュが回避されます。

    [ユーザードキュメント](/tiflash/monitor-tiflash.md#coprocessor)

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

    [ユーザードキュメント](/dm/dm-webui-guide.md)

-   エラー処理メカニズムを追加する

    移行タスクを中断する問題に対処するために、より多くのコマンドが導入されました。例えば：

    -   スキーマ エラーが発生した場合は、スキーマ ファイルを個別に編集するのではなく、 `binlog-schema update`コマンドの`--from-source/--from-target`パラメータを使用してスキーマ ファイルを更新できます。
    -   binlogの位置を指定して、DDL ステートメントを挿入、置換、スキップ、または元に戻すことができます。

    [ユーザードキュメント](/dm/dm-manage-schema.md)

-   Amazon S3 への完全なデータstorageをサポート

    DM がすべてまたは完全なデータ移行タスクを実行する場合、アップストリームからの完全なデータを保存するために十分なハード ディスク容量が必要です。 EBS と比較して、Amazon S3 は低コストでほぼ無限のstorageを備えています。 DM は、ダンプ ディレクトリとして Amazon S3 の設定をサポートするようになりました。つまり、すべてまたは完全なデータ移行タスクを実行するときに、S3 を使用して完全なデータを保存できます。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   指定した時間からの移行タスクの開始をサポート

    新しいパラメータ`--start-time`が移行タスクに追加されます。時刻は「2021-10-21 00:01:00」または「2021-10-21T00:01:00」の形式で定義できます。

    この機能は、シャード mysql インスタンスから増分データを移行およびマージするシナリオで特に役立ちます。具体的には、増分移行タスクでソースごとにbinlogの開始ポイントを設定する必要はありません。代わりに、 `safe-mode`の`--start-time`パラメータを使用すると、増分移行タスクをすばやく作成できます。

    [ユーザードキュメント](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning {#tidb-lightning}

-   許容可能なエラーの最大数の構成をサポート

    設定項目`lightning.max-error`を追加しました。デフォルト値は 0 です。値が 0 より大きい場合、最大エラー機能が有効になります。エンコード中に行でエラーが発生した場合、この行を含むレコードがターゲット TiDB の`lightning_task_info.type_error_v1`に追加され、この行は無視されます。エラーのある行がしきい値を超えると、 TiDB Lightning は直ちに終了します。

    `lightning.max-error`構成と一致して、 `lightning.task-info-schema-name`構成項目には、データ保存エラーを報告するデータベースの名前が記録されます。

    この機能は、すべてのタイプのエラーをカバーするわけではありません。たとえば、構文エラーは適用されません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   100,000 テーブルの同時複製をサポート

    データ処理フローを最適化することで、TiCDC は各テーブルの増分データの処理に伴うリソース消費を削減し、大規模なクラスターでデータをレプリケートする際のレプリケーションの安定性と効率を大幅に向上させます。内部テストの結果、TiCDC は 100,000 テーブルの同時複製を安定してサポートできることがわかりました。

### 導入とメンテナンス {#deployment-and-maintenance}

-   新しい照合順序ルールをデフォルトで有効にする

    v4.0 以降、TiDB は、大文字と小文字を区別しない、アクセントを区別しない、およびパディング ルールにおいて MySQL と同じように動作する新しい照合順序ルールをサポートしています。新しい照合順序ルールは、デフォルトでは無効になっている`new_collations_enabled_on_first_bootstrap`パラメータによって制御されます。 v6.0 以降、TiDB はデフォルトで新しい照合順序ルールを有効にします。この構成は、TiDB クラスターの初期化時にのみ有効になることに注意してください。

    [ユーザードキュメント](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

-   TiKV ノードの再起動後にリーダーのバランシングを加速する

    TiKV ノードの再起動後、負荷分散のために不均一に分散したリーダーを再分散する必要があります。大規模クラスターでは、リーダーのバランスをとる時間はリージョンの数と正の相関があります。たとえば、100K リージョンのリーダー バランシングには 20 ～ 30 分かかる場合があり、不均一な負荷によるパフォーマンスの問題や安定性のリスクが発生する傾向があります。 TiDB v6.0.0 は、バランシングの同時実行性を制御するパラメーターを提供し、デフォルト値を元の 4 倍に拡大します。これにより、リーダーのリバランス時間が大幅に短縮され、TiKV ノードの再起動後のビジネスの回復が加速されます。

    [ユーザードキュメント](/pd-control.md#scheduler-config-balance-leader-scheduler) [#4610](https://github.com/tikv/pd/issues/4610)

-   統計の自動更新のキャンセルをサポート

    統計は、 SQL のパフォーマンスに影響を与える最も重要な基本データの 1 つです。統計の完全性と適時性を確保するために、TiDB はオブジェクト統計をバックグラウンドで定期的に自動的に更新します。ただし、統計の自動更新によりリソースの競合が発生し、SQL のパフォーマンスに影響を与える可能性があります。この問題に対処するには、v6.0 以降の統計の自動更新を手動でキャンセルできます。

    [ユーザードキュメント](/statistics.md#automatic-update)

-   PingCAPクリニック診断サービス（テクニカルプレビュー版）

    PingCAPクリニック は、 TiDB クラスターの診断サービスです。このサービスは、クラスターの問題をリモートでトラブルシューティングするのに役立ち、クラスターのステータスをローカルで簡単に確認できます。 PingCAPクリニックを使用すると、TiDB クラスターのライフサイクル全体を通じて安定した動作を保証し、潜在的な問題を予測し、問題の可能性を減らし、クラスターの問題を迅速にトラブルシューティングできます。

    クラスターの問題をトラブルシューティングするためのリモート アシスタンスについて PingCAP テクニカル サポートに問い合わせる場合、 PingCAPクリニックサービスを使用して診断データを収集およびアップロードすることができるため、トラブルシューティングの効率が向上します。

    [ユーザードキュメント](/clinic/clinic-introduction.md)

-   エンタープライズレベルのデータベース管理プラットフォーム、TiDB Enterprise Manager

    TiDB Enterprise Manager (TiEM) は、TiDB データベースに基づくエンタープライズ レベルのデータベース管理プラットフォームであり、ユーザーがセルフホストまたはパブリック クラウド環境で TiDB クラスターを管理できるようにすることを目的としています。

    TiEM は、TiDB クラスターのライフサイクル全体を視覚的に管理するだけでなく、パラメーター管理、バージョン アップグレード、クラスター クローン、アクティブ/スタンバイ クラスター切り替え、データのインポートとエクスポート、データのレプリケーション、データのバックアップと復元サービスなどのワンストップ サービスも提供します。 TiEM は、TiDB 上の DevOps の効率を向上させ、企業の DevOps コストを削減できます。

    現在、TiEM は[TiDB エンタープライズ](https://en.pingcap.com/tidb-enterprise/)エディションのみで提供されています。 TiEM を入手するには、 [TiDB エンタープライズ](https://en.pingcap.com/tidb-enterprise/)ページからお問い合わせください。

-   監視コンポーネントの構成のカスタマイズをサポート

    TiUPを使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視コンポーネントを自動的にデプロイし、スケールアウト後に監視スコープに新しいノードを自動的に追加します。 `topology.yaml`ファイルに構成項目を追加することで、監視コンポーネントの構成をカスタマイズできます。

    [ユーザードキュメント](/tiup/customized-montior-in-tiup-environment.md)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v6.0.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、対応するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                       | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                               |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `placement_checks`                                                                                                                                                                        | 削除されました  | DDL ステートメントが[SQL の配置ルール](/placement-rules-in-sql.md)で指定された配置ルールを検証するかどうかを制御します。 `tidb_placement_mode`に置き換えられます。                                                                                                                                                                                                  |
| `tidb_enable_alter_placement`                                                                                                                                                             | 削除されました  | [SQL の配置ルール](/placement-rules-in-sql.md)を有効にするかどうかを制御します。                                                                                                                                                                                                                                                        |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | 削除されました  | v5.0 以降、これらの変数は`tidb_mem_quota_query`に置き換えられ、 [システム変数](/system-variables.md)ドキュメントから削除されました。互換性を確保するために、これらの変数はソース コード内に保持されています。 TiDB 6.0.0 以降、これらの変数もコードから削除されています。                                                                                                                                            |
| [`tidb_enable_mutation_checker`](/system-variables.md#tidb_enable_mutation_checker-new-in-v600)                                                                                           | 新しく追加された | 突然変異チェッカーを有効にするかどうかを制御します。デフォルト値は`ON`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、ミューテーション チェッカーはデフォルトで無効になっています。                                                                                                                                                                                                  |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)                                                                         | 新しく追加された | プリペアドステートメントを閉じるコマンドを無視するかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                              |
| [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)                                                                                           | 新しく追加された | キャッシュ保持のメモリ使用量のしきい値を`binding`設定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                                                                                                |
| [`tidb_placement_mode`](/system-variables.md#tidb_placement_mode-new-in-v600)                                                                                                             | 新しく追加された | DDL ステートメントが[SQL の配置ルール](/placement-rules-in-sql.md)で指定された配置ルールを無視するかどうかを制御します。デフォルト値は`strict`です。これは、DDL ステートメントが配置ルールを無視しないことを意味します。                                                                                                                                                                            |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                                                         | 新しく追加された | <li>トランザクション内の読み取りステートメントのレイテンシーを最適化します。読み取り/書き込みの競合がより深刻な場合、この変数をオンにすると、オーバーヘッドとレイテンシーが追加され、パフォーマンスの低下が発生します。デフォルト値は`off`です。</li><li>この変数はまだ[レプリカ読み取り](/system-variables.md#tidb_replica_read-new-in-v40)と互換性がありません。読み取りリクエストに`tidb_rc_read_check_ts`付いている場合、レプリカ読み取りを使用できない可能性があります。両方の変数を同時にオンにしないでください。</li> |
| [`tidb_sysdate_is_now`](/system-variables.md#tidb_sysdate_is_now-new-in-v600)                                                                                                             | 新しく追加された | `SYSDATE`関数を`NOW`関数で置き換えることができるかどうかを制御します。この設定項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。デフォルト値は`OFF`です。                                                                                                              |
| [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600)                                                                                                       | 新しく追加された | [テーブルキャッシュ](/cached-tables.md)のリース時間を秒単位で制御します。デフォルト値は`3`です。                                                                                                                                                                                                                                                     |
| [`tidb_top_sql_max_meta_count`](/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600)                                                                                             | 新しく追加された | 収集される SQL ステートメント タイプの最大数を[Top SQL](/dashboard/top-sql.md)分あたり 1 つずつ制御します。デフォルト値は`5000`です。                                                                                                                                                                                                                       |
| [`tidb_top_sql_max_time_series_count`](/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600)                                                                               | 新しく追加された | 負荷に最も寄与する SQL ステートメント (つまり、上位 N) を[Top SQL](/dashboard/top-sql.md)分あたり 1 つずつ記録できる数を制御します。デフォルト値は`100`です。                                                                                                                                                                                                         |
| [`tidb_txn_assertion_level`](/system-variables.md#tidb_txn_assertion_level-new-in-v600)                                                                                                   | 新しく追加された | アサーション レベルを制御します。アサーションは、データとインデックス間の整合性チェックであり、書き込まれるキーがトランザクション コミット プロセスに存在するかどうかをチェックします。デフォルトでは、このチェックではほとんどのチェック項目が有効になり、パフォーマンスにはほとんど影響がありません。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、このチェックはデフォルトで無効になっています。                                                                                             |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                                       | 種類の変更    | 説明                                                                                                                                                                                                                                                                                                             |
| :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | 削除されました  | [ステートメント概要テーブル](/statement-summary-tables.md)に関連するコンフィグレーション。これらの構成項目はすべて削除されます。ステートメント要約テーブルを制御するには、SQL 変数を使用する必要があります。                                                                                                                                                                                       |
| TiDB           | [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)                                                                                             | 修正済み     | 新しい照合順序のサポートを有効にするかどうかを制御します。 v6.0 以降、デフォルト値は`false`から`true`に変更されました。この構成項目は、クラスターが初めて初期化されるときにのみ有効になります。最初のブートストラップの後は、この構成項目を使用して新しい照合順序フレームワークを有効または無効にすることはできません。                                                                                                                                          |
| TiKV           | [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)                                                                                                                                                | 修正済み     | 値の範囲は`[1, CPU]`に変更されます。                                                                                                                                                                                                                                                                                        |
| TiKV           | [`raftstore.apply-max-batch-size`](/tikv-configuration-file.md#apply-max-batch-size)                                                                                                                             | 修正済み     | 最大値は`10240`に変更されます。                                                                                                                                                                                                                                                                                            |
| TiKV           | [`raftstore.raft-max-size-per-msg`](/tikv-configuration-file.md#raft-max-size-per-msg)                                                                                                                           | 修正済み     | <li>最小値が`0`から`0`より大きい値に変更されます。</li><li>最大値は`3GB`に設定されます。</li><li>単位が`MB`から`KB\|MB\|GB`に変更されます。</li>                                                                                                                                                                                                            |
| TiKV           | [`raftstore.store-max-batch-size`](/tikv-configuration-file.md#store-max-batch-size)                                                                                                                             | 修正済み     | 最大値は`10240`に設定されます。                                                                                                                                                                                                                                                                                            |
| TiKV           | [`readpool.unified.max-thread-count`](/tikv-configuration-file.md#max-thread-count)                                                                                                                              | 修正済み     | 調整範囲が`[min-thread-count, MAX(4, CPU)]`に変更されます。                                                                                                                                                                                                                                                                 |
| TiKV           | [`rocksdb.enable-pipelined-write`](/tikv-configuration-file.md#enable-pipelined-write)                                                                                                                           | 修正済み     | デフォルト値が`true`から`false`に変更されました。この構成が有効な場合、以前のパイプライン書き込みが使用されます。この設定を無効にすると、新しいパイプライン コミット メカニズムが使用されます。                                                                                                                                                                                                        |
| TiKV           | [`rocksdb.max-background-flushes`](/tikv-configuration-file.md#max-background-flushes)                                                                                                                           | 修正済み     | <li>CPU コア数が 10 の場合、デフォルト値は`3`です。</li><li> CPU コアの数が 8 の場合、デフォルト値は`2`です。</li>                                                                                                                                                                                                                                  |
| TiKV           | [`rocksdb.max-background-jobs`](/tikv-configuration-file.md#max-background-jobs)                                                                                                                                 | 修正済み     | <li>CPU コア数が 10 の場合、デフォルト値は`9`です。</li><li> CPU コアの数が 8 の場合、デフォルト値は`7`です。</li>                                                                                                                                                                                                                                  |
| TiFlash        | [`profiles.default.dt_enable_logical_split`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                   | 修正済み     | DeltaTree Storage Engine のセグメントが論理分割を使用するかどうかを決定します。デフォルト値が`true`から`false`に変更されました。                                                                                                                                                                                                                            |
| TiFlash        | [`profiles.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                 | 修正済み     | エラスティック スレッド プールを有効にするかどうかを制御します。デフォルト値が`false`から`true`に変更されました。                                                                                                                                                                                                                                               |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                     | 修正済み     | TiFlashのデータ検証機能を制御します。デフォルト値が`2`から`3`に変更されました。<br/> `format_version`を`3`に設定すると、ハードウェア障害による誤った読み取りを回避するために、すべてのTiFlashデータの読み取り操作で一貫性チェックが実行されます。<br/>新しいフォーマットのバージョンを v5.4 より前のバージョンにダウングレードすることはできないことに注意してください。                                                                                               |
| TiDB           | [`pessimistic-txn.pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)                                                                                                     | 新しく追加された | 悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` )、自動コミット トランザクションが使用するトランザクション モードを決定します。                                                                                                                                                                                                     |
| TiKV           | [`pessimistic-txn.in-memory`](/tikv-configuration-file.md#in-memory-new-in-v600)                                                                                                                                 | 新しく追加された | メモリ内の悲観的ロックを有効にするかどうかを制御します。この機能を有効にすると、悲観的トランザクションは、悲観的ロックをディスクに書き込んだり、他のレプリカに複製したりするのではなく、可能な限り TiKVメモリに悲観的ロックを保存します。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われる可能性は低いため、悲観的トランザクションがコミットに失敗する可能性があります。デフォルト値は`true`です。                                                                                  |
| TiKV           | [`quota`](/tikv-configuration-file.md#quota)                                                                                                                                                                     | 新しく追加された | フロントエンドリクエストによって占有されるリソースを制限するクォータリミッターに関連する構成項目を追加します。クォータ リミッターは実験的機能であり、デフォルトでは無効になっています。新しいクォータ関連の構成項目は、 `foreground-cpu-time` 、 `foreground-write-bandwidth` 、 `foreground-read-bandwidth` 、および`max-delay-duration`です。                                                                                    |
| TiFlash        | [`profiles.default.dt_compression_method`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                     | 新しく追加された | TiFlashの圧縮アルゴリズムを指定します。オプションの値は`LZ4` 、 `zstd` 、および`LZ4HC`で、すべて大文字と小文字が区別されません。デフォルト値は`LZ4`です。                                                                                                                                                                                                                  |
| TiFlash        | [`profiles.default.dt_compression_level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                      | 新しく追加された | TiFlashの圧縮レベルを指定します。デフォルト値は`1`です。                                                                                                                                                                                                                                                                              |
| DM             | [`loaders.&#x3C;name>.import-mode`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                               | 新しく追加された | 完全インポートフェーズ中のインポートモード。 v6.0 以降、DM は TiDB Lightning の TiDB バックエンド モードを使用して、完全なインポート フェーズ中にデータをインポートします。以前の Loaderコンポーネントは使用されなくなりました。これは内部交換であり、日常業務に明らかな影響はありません。<br/>デフォルト値は`sql`に設定されており、これは`tidb-backend`モードを使用することを意味します。まれに、 `tidb-backend`完全な互換性がない可能性があります。このパラメータを`loader`に設定すると、ローダー モードにフォールバックできます。 |
| DM             | [`loaders.&#x3C;name>.on-duplicate`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                              | 新しく追加された | 完全インポートフェーズ中に競合を解決する方法を指定します。デフォルト値は`replace`で、新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                                                                                                                                                                |
| TiCDC          | [`dial-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                     | 新しく追加された | ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                               |
| TiCDC          | [`read-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                     | 新しく追加された | ダウンストリーム Kafka から返される応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                           |
| TiCDC          | [`write-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                    | 新しく追加された | ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                             |

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
    -   内部機構の変更により、タスク管理に関するインターフェースが以前の実験的版と互換性がありません。適応するには新しい[DM OpenAPI ドキュメント](/dm/dm-open-api.md)を参照する必要があります。
-   DM は、完全なインポート段階で競合を解決する方法を変更します。
    -   パラメータが`loader.<name>.on-duplicate`追加されます。デフォルト値は`replace`で、新しいデータを使用して既存のデータを置き換えることを意味します。以前の動作を維持したい場合は、値を`error`に設定できます。このパラメータは、完全なインポート フェーズ中の動作のみを制御します。
-   DM を使用するには、対応するバージョン`dmctl`を使用する必要があります。
    -   内部メカニズムの変更により、DM を v6.0.0 にアップグレードした後、 `dmctl`も v6.0.0 にアップグレードする必要があります。
-   v5.4 (v5.4 のみ) では、TiDB は一部の noop システム変数に不正な値を許可します。 v6.0.0 以降、TiDB ではシステム変数に不正な値を設定することが禁止されています。 [#31538](https://github.com/pingcap/tidb/issues/31538)

## 改善点 {#improvements}

-   TiDB

    -   `FLASHBACK`または`RECOVER`ステートメントを使用してテーブルを復元した後、テーブルの配置ルール設定を自動的にクリアします[#31668](https://github.com/pingcap/tidb/issues/31668)
    -   パフォーマンス概要ダッシュボードを追加して、一般的なクリティカル パスに関するコア パフォーマンス メトリクスを表示し、TiDB でのメトリクス分析を容易にします[#31676](https://github.com/pingcap/tidb/issues/31676)
    -   `LOAD DATA LOCAL INFILE`ステートメントでの`REPLACE`キーワードの使用のサポート[#24515](https://github.com/pingcap/tidb/issues/24515)
    -   範囲パーティション テーブル[#26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティション プルーニングをサポートします。
    -   MPP 集約クエリで潜在的に冗長な Exchange 操作を排除することで、クエリの効率を向上します[#31762](https://github.com/pingcap/tidb/issues/31762)
    -   `TRUNCATE PARTITION`と`DROP PARTITION`ステートメントで重複するパーティション名を許可することで、MySQL との互換性を向上します[#31681](https://github.com/pingcap/tidb/issues/31681)
    -   `ADMIN SHOW DDL JOBS`ステートメント[#23494](https://github.com/pingcap/tidb/issues/23494)の結果に`CREATE_TIME`情報を表示するサポート
    -   新しい組み込み関数をサポート`CHARSET()` [#3931](https://github.com/pingcap/tidb/issues/3931)
    -   ユーザー名によるベースライン キャプチャ ブロックリストのフィルタリングをサポート[#32558](https://github.com/pingcap/tidb/issues/32558)
    -   ベースライン キャプチャ ブロックリストでのワイルドカードの使用のサポート[#32714](https://github.com/pingcap/tidb/issues/32714)
    -   現在の`time_zone` [#26642](https://github.com/pingcap/tidb/issues/26642)に従って時間を表示することで、 `ADMIN SHOW DDL JOBS`と`SHOW TABLE STATUS`ステートメントの結果を最適化します。
    -   `DAYNAME()`と`MONTHNAME()`関数をTiFlash [#32594](https://github.com/pingcap/tidb/issues/32594)にプッシュダウンするサポート
    -   `REGEXP`機能をTiFlash [#32637](https://github.com/pingcap/tidb/issues/32637)にプッシュダウンするサポート
    -   `DAYOFMONTH()`と`LAST_DAY()`関数をTiFlash [#33012](https://github.com/pingcap/tidb/issues/33012)にプッシュダウンするサポート
    -   `DAYOFWEEK()`と`DAYOFYEAR()`関数をTiFlash [#33130](https://github.com/pingcap/tidb/issues/33130)にプッシュダウンするサポート
    -   `IS_TRUE` 、 `IS_FALSE` 、および`IS_TRUE_WITH_NULL`関数のTiFlash [#33047](https://github.com/pingcap/tidb/issues/33047)へのプッシュダウンをサポート
    -   `GREATEST`と`LEAST`関数をTiFlash [#32787](https://github.com/pingcap/tidb/issues/32787)にプッシュダウンするサポート
    -   `UnionScan`オペレーター[#32631](https://github.com/pingcap/tidb/issues/32631)の実行の追跡をサポート
    -   `_tidb_rowid`列[#31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリに対する PointGet プランの使用のサポート
    -   `EXPLAIN`ステートメントの出力で、名前を小文字に変換せずに元のパーティション名を表示するサポート[#32719](https://github.com/pingcap/tidb/issues/32719)
    -   IN 条件および文字列型列[#32626](https://github.com/pingcap/tidb/issues/32626)での RANGE COLUMNS パーティションのパーティション プルーニングを有効にする
    -   システム変数が NULL に設定されている場合にエラー メッセージを返す[#32850](https://github.com/pingcap/tidb/issues/32850)
    -   非 MPP モードからブロードキャスト参加を削除する[#31465](https://github.com/pingcap/tidb/issues/31465)
    -   動的プルーニング モード[#32347](https://github.com/pingcap/tidb/issues/32347)でのパーティション化されたテーブルでの MPP プランの実行のサポート
    -   共通テーブル式 (CTE) の述語のプッシュダウンのサポート[#28163](https://github.com/pingcap/tidb/issues/28163)
    -   `Statement Summary`と`Capture Plan Baselines`の構成を簡素化し、グローバル ベースでのみ利用できるようにする[#30557](https://github.com/pingcap/tidb/issues/30557)
    -   macOS 12 [#31607](https://github.com/pingcap/tidb/issues/31607)でバイナリをビルドするときに報告されるアラームに対処するために、gopsutil を v3.21.12 に更新します。

-   TiKV

    -   多くのキー範囲を持つバッチのRaftstoreのサンプリング精度を向上させます[#12327](https://github.com/tikv/tikv/issues/12327)
    -   プロファイルをより簡単に識別できるように、 `debug/pprof/profile`に正しい「Content-Type」を追加します[#11521](https://github.com/tikv/tikv/issues/11521)
    -   Raftstoreにハートビートがあるとき、または読み取りリクエストを処理するときに、リーダーのリース時間を無限に更新します。これにより、レイテンシージッターの削減に役立ちます[#11579](https://github.com/tikv/tikv/issues/11579)
    -   リーダーを切り替えるときに最もコストの低いストアを選択すると、パフォーマンスの安定性が向上します[#10602](https://github.com/tikv/tikv/issues/10602)
    -   Raftログを非同期的に取得して、 Raftstore [#11320](https://github.com/tikv/tikv/issues/11320)のブロックによって引き起こされるパフォーマンスのジッターを軽減します。
    -   ベクトル計算[#5751](https://github.com/tikv/tikv/issues/5751)の`QUARTER`機能をサポート
    -   `BIT`データ型の TiKV [#30738](https://github.com/pingcap/tidb/issues/30738)へのプッシュダウンをサポート
    -   TiKV [#11916](https://github.com/tikv/tikv/issues/11916)への`MOD`機能と`SYSDATE`機能のプッシュダウンをサポート
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   `raftstore.raft-max-inflight-msgs` [#11865](https://github.com/tikv/tikv/issues/11865)の動的変更をサポート
    -   動的プルーニング モード[#11888](https://github.com/tikv/tikv/issues/11888)を有効にする`EXTRA_PHYSICAL_TABLE_ID_COL_ID`サポート
    -   バケット[#11759](https://github.com/tikv/tikv/issues/11759)での計算をサポート
    -   RawKV API V2 のキーを`user-key` + `memcomparable-padding` + `timestamp` [#11965](https://github.com/tikv/tikv/issues/11965)としてエンコードします。
    -   RawKV API V2 の値を`user-value` + `ttl` + `ValueMeta`としてエンコードし、 `delete` `ValueMeta` [#11965](https://github.com/tikv/tikv/issues/11965)としてエンコードします。
    -   `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)の動的変更をサポート
    -   Grafana [#12014](https://github.com/tikv/tikv/issues/12014)での multi-k8 の監視のサポート
    -   リーダーシップを CDC オブザーバーに移管して、レイテンシージッター[#12111](https://github.com/tikv/tikv/issues/12111)を削減します。
    -   `raftstore.apply_max_batch_size`と`raftstore.store_max_batch_size`の動的変更をサポート[#11982](https://github.com/tikv/tikv/issues/11982)
    -   RawKV V2 は`raw_get`または`raw_scan`リクエストを受信すると最新バージョンを返します[#11965](https://github.com/tikv/tikv/issues/11965)
    -   RCCheckTS の一貫性読み取り[#12097](https://github.com/tikv/tikv/issues/12097)をサポートします。
    -   動的変更のサポート`storage.scheduler-worker-pool-size` (スケジューラ プールのスレッド数) [#12067](https://github.com/tikv/tikv/issues/12067)
    -   グローバル フォアグラウンド フロー コントローラーを使用して CPU と帯域幅の使用を制御し、TiKV [#11855](https://github.com/tikv/tikv/issues/11855)のパフォーマンスの安定性を向上させます。
    -   動的変更のサポート`readpool.unified.max-thread-count` (UnifyReadPool のスレッド数) [#11781](https://github.com/tikv/tikv/issues/11781)
    -   TiKV 内部パイプラインを使用して RocksDB パイプラインを置き換え、 `rocksdb.enable-multibatch-write`パラメータ[#12059](https://github.com/tikv/tikv/issues/12059)を非推奨にします。

-   PD

    -   リーダーを排除する際に、転送用に最も速いオブジェクトを自動的に選択する機能をサポートします。これにより、排除プロセスのスピードアップに役立ちます[#4229](https://github.com/tikv/pd/issues/4229)
    -   リージョンが使用できなくなった場合に備えて、2 レプリカRaftグループから投票者を削除することを禁止します[#4564](https://github.com/tikv/pd/issues/4564)
    -   バランスリーダー[#4652](https://github.com/tikv/pd/issues/4652)のスケジューリングを高速化します。

-   TiFlash

    -   TiFlashファイルの論理分割を禁止し (デフォルト値の`profiles.default.dt_enable_logical_split`を`false`に調整します。詳細については[ユーザードキュメント](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)参照)、 TiFlashに同期されたテーブルのスペース占有率が、 TiFlashカラムナstorageのスペース使用効率を向上させます。 TiKV のテーブルの占有
    -   以前のクラスター管理モジュールを TiDB に統合することで、 TiFlashのクラスター管理とレプリカ レプリケーション メカニズムを最適化し、小さなテーブルのレプリカ作成を高速化します[#29924](https://github.com/pingcap/tidb/issues/29924)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップデータの復元速度が向上しました。 BR が15 ノード (各ノードに 16 個の CPU コアがある) を備えた TiKV クラスターに 16 TB データを復元するシミュレーション テストでは、スループットは 2.66 GiB/秒に達します。 [#27036](https://github.com/pingcap/tidb/issues/27036)

        -   配置ルールのインポートとエクスポートをサポートします。 `--with-tidb-placement-mode`パラメータを追加して、データのインポート時に配置ルールを無視するかどうかを制御します。 [#32290](https://github.com/pingcap/tidb/issues/32290)

    -   TiCDC

        -   Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   サポート配置ルール[#4846](https://github.com/pingcap/tiflow/issues/4846)
        -   HTTP API 処理の同期[#1710](https://github.com/pingcap/tiflow/issues/1710)
        -   変更フィードを再開するための指数バックオフ メカニズムを追加します[#3329](https://github.com/pingcap/tiflow/issues/3329)
        -   MySQL [#3589](https://github.com/pingcap/tiflow/issues/3589)のデッドロックを軽減するために、MySQL シンクのデフォルトの分離レベルを読み取りコミットに設定します。
        -   作成時に変更フィードパラメータを検証し、エラーメッセージを修正する[#1716](https://github.com/pingcap/tiflow/issues/1716) [#1718](https://github.com/pingcap/tiflow/issues/1718) [#1719](https://github.com/pingcap/tiflow/issues/1719) [#4472](https://github.com/pingcap/tiflow/issues/4472)
        -   Kafka プロデューサの構成パラメータを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成できるようにします。

    -   TiDB データ移行 (DM)

        -   アップストリーム テーブル スキーマに一貫性がなく、楽観的モードである場合のタスクの開始をサポート[#3629](https://github.com/pingcap/tiflow/issues/3629) [#3708](https://github.com/pingcap/tiflow/issues/3708) [#3786](https://github.com/pingcap/tiflow/issues/3786)
        -   `stopped`状態[#4484](https://github.com/pingcap/tiflow/issues/4484)でのタスクの作成をサポート
        -   Syncer は内部ファイルの書き込みに`/tmp`ではなく DM ワーカーの作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングすることをサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)
        -   事前チェックが改善されました。いくつかの重要なチェックがスキップされなくなりました。 [#3608](https://github.com/pingcap/tiflow/issues/3608)

    -   TiDB Lightning

        -   再試行可能なエラー タイプをさらに追加[#31376](https://github.com/pingcap/tidb/issues/31376)
        -   Base64形式のパスワード文字列[#31194](https://github.com/pingcap/tidb/issues/31194)をサポートします
        -   エラーコードとエラー出力の標準化[#32239](https://github.com/pingcap/tidb/issues/32239)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SCHEDULE = majority_in_primary` 、 `PrimaryRegion` 、 `Regions`が同じ値[#31271](https://github.com/pingcap/tidb/issues/31271)の場合、TiDB が配置ルールを含むテーブルの作成に失敗するバグを修正
    -   インデックス検索結合[#30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正しました。
    -   `show grants` 2 つ以上の権限が付与されている場合に不正な結果が返されるバグを修正[#30855](https://github.com/pingcap/tidb/issues/30855)
    -   デフォルトで`CURRENT_TIMESTAMP` [#29926](https://github.com/pingcap/tidb/issues/29926)に設定されているフィールドのタイムスタンプを`INSERT INTO t1 SET timestamp_col = DEFAULT`にするとタイムスタンプが 0 に設定されてしまうバグを修正
    -   文字列タイプ[#31721](https://github.com/pingcap/tidb/issues/31721)の最大値と最小の非 null 値のエンコードを回避することで、結果の読み取り時に報告されたエラーを修正しました。
    -   エスケープ文字[#31589](https://github.com/pingcap/tidb/issues/31589)でデータが壊れた場合のロード データpanicを修正
    -   照合順序のある`greatest`または`least`関数が間違った結果を取得する問題を修正[#31789](https://github.com/pingcap/tidb/issues/31789)
    -   date_add 関数と date_sub関数が間違ったデータ型を返す可能性があるバグを修正しました[#31809](https://github.com/pingcap/tidb/issues/31809)
    -   insert ステートメントを使用して仮想生成された列にデータを挿入するときに発生する可能性のあるpanicを修正しました[#31735](https://github.com/pingcap/tidb/issues/31735)
    -   作成したリストパーティション[#31784](https://github.com/pingcap/tidb/issues/31784)に重複カラムが存在してもエラーが報告されないバグを修正
    -   `select for update union select`間違ったスナップショットを使用した場合に返される間違った結果を修正[#31530](https://github.com/pingcap/tidb/issues/31530)
    -   復元操作の終了後にリージョンが不均一に分散される可能性がある潜在的な問題を修正します[#31034](https://github.com/pingcap/tidb/issues/31034)
    -   `json`タイプ[#31541](https://github.com/pingcap/tidb/issues/31541)の COERCIBILITY が間違っているバグを修正
    -   この型が組み込み機能[#31320](https://github.com/pingcap/tidb/issues/31320)を使用して処理される場合、 `json`型の間違った照合順序を修正しました。
    -   TiFlashレプリカ数を 0 [#32190](https://github.com/pingcap/tidb/issues/32190)に設定すると PD ルールが削除されないバグを修正
    -   `alter column set default`テーブル スキーマが誤って更新される問題を修正[#31074](https://github.com/pingcap/tidb/issues/31074)
    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[#32232](https://github.com/pingcap/tidb/issues/32232)
    -   結合[#31629](https://github.com/pingcap/tidb/issues/31629)を使用したパーティションテーブルの更新時にエラーが発生することがあるバグを修正
    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)に対する Nulleq 関数の間違った範囲計算結果を修正しました。
    -   `upper()`および`lower()`関数で発生する可能性のあるpanicを修正[#32488](https://github.com/pingcap/tidb/issues/32488)
    -   他のタイプの列をタイムスタンプ タイプの列[#29585](https://github.com/pingcap/tidb/issues/29585)に変更するときに発生するタイム ゾーンの問題を修正します。
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    -   動的パーティションプルーニングモード[#32516](https://github.com/pingcap/tidb/issues/32516)でサブSELECT LIMITが期待通りに動作しないバグを修正
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[#32655](https://github.com/pingcap/tidb/issues/32655)のビットデフォルト値の間違った形式または一貫性のない形式を修正しました。
    -   サーバーの再起動後にパーティション テーブルのリストを作成する場合にパーティション テーブルのプルーニングが機能しない可能性があるバグを修正[#32416](https://github.com/pingcap/tidb/issues/32416)
    -   `SET timestamp`の実行後に`add column`間違ったデフォルトのタイムスタンプを使用する可能性があるバグを修正[#31968](https://github.com/pingcap/tidb/issues/31968)
    -   MySQL 5.5 または 5.6 クライアントから TiDB パスワードなしアカウントへの接続が失敗することがあるバグを修正しました[#32334](https://github.com/pingcap/tidb/issues/32334)
    -   トランザクション[#29851](https://github.com/pingcap/tidb/issues/29851)の動的モードでパーティション化されたテーブルを読み取るときの誤った結果を修正しました。
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   `timdiff`関数の入力にミリ秒が含まれている場合に返される間違った結果を修正しました[#31680](https://github.com/pingcap/tidb/issues/31680)
    -   明示的にパーティションを読み取り、IndexJoin プラン[#32007](https://github.com/pingcap/tidb/issues/32007)を使用する場合の誤った結果を修正しました。
    -   列の型を同時に変更すると列名の変更が失敗するバグを修正[#31075](https://github.com/pingcap/tidb/issues/31075)
    -   TiFlashプランの純コストの計算式が TiKV プラン[#30103](https://github.com/pingcap/tidb/issues/30103)と一致しないバグを修正
    -   アイドル状態の接続で`KILL TIDB`がすぐに有効にならないバグを修正[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   生成された列を含むテーブルをクエリするときに発生する可能性のある間違った結果を修正します[#33038](https://github.com/pingcap/tidb/issues/33038)
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   `SUBTIME`関数がオーバーフローの場合に間違った結果を返すバグを修正[#31868](https://github.com/pingcap/tidb/issues/31868)
    -   集計クエリに`having`条件[#33166](https://github.com/pingcap/tidb/issues/33166)が含まれる場合、 `selection`演算子をプッシュダウンできないバグを修正
    -   クエリがエラーを報告すると CTE がブロックされる可能性があるバグを修正[#31302](https://github.com/pingcap/tidb/issues/31302)
    -   非厳密モードでテーブルを作成するときに varbinary または varchar 列の長さが長すぎるとエラーが発生する可能性があるバグを修正[#30328](https://github.com/pingcap/tidb/issues/30328)
    -   フォロワーが指定されていない場合の`information_schema.placement_policies`のフォロワー数が間違っていたのを修正[#31702](https://github.com/pingcap/tidb/issues/31702)
    -   TiDB がインデックスの作成時に列のプレフィックス長を 0 として指定できる問題を修正します[#31972](https://github.com/pingcap/tidb/issues/31972)
    -   TiDB でスペースで終わるパーティション名が許可される問題を修正[#31535](https://github.com/pingcap/tidb/issues/31535)
    -   `RENAME TABLE`ステートメント[#29893](https://github.com/pingcap/tidb/issues/29893)のエラー メッセージを修正します。

-   TiKV

    -   ピアのステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除することによって引き起こされるpanicの問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定されている場合の QPS ドロップの問題を修正します[#11424](https://github.com/tikv/tikv/issues/11424)
    -   ピアを破棄するとレイテンシーが長くなる可能性がある問題を修正[#10210](https://github.com/tikv/tikv/issues/10210)
    -   GC ワーカーがビジー状態[#11903](https://github.com/tikv/tikv/issues/11903)の場合、TiKV が一定範囲のデータを削除できない (内部コマンド`unsafe_destroy_range`が実行されることを意味します) というバグを修正します。
    -   一部の特殊なケースで`StoreMeta`のデータが誤って削除された場合に TiKV がパニックになるバグを修正[#11852](https://github.com/tikv/tikv/issues/11852)
    -   ARM プラットフォームでプロファイリングを実行すると TiKV がパニックになるバグを修正[#10658](https://github.com/tikv/tikv/issues/10658)
    -   TiKV が 2 年以上実行されている場合にpanicになる可能性があるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   SSE 命令セット[#12034](https://github.com/tikv/tikv/issues/12034)の欠落によって引き起こされる ARM64アーキテクチャでのコンパイルの問題を修正
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   古いメッセージによって TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   TsSet変換[#12070](https://github.com/tikv/tikv/issues/12070)で未定義動作(UB)が発生する場合がある問題を修正
    -   レプリカの読み取りが線形化可能性[#12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   TiKV が Ubuntu 18.04 でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します[#9765](https://github.com/tikv/tikv/issues/9765)
    -   間違った文字列一致[#12329](https://github.com/tikv/tikv/issues/12329)が原因で tikv-ctl が間違った結果を返す問題を修正
    -   メモリメトリクス[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローによって引き起こされる断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV [#12231](https://github.com/tikv/tikv/issues/12231)を終了するときに TiKV パニックを誤って報告する潜在的な問題を修正

-   PD

    -   PD が共同合意[#4362](https://github.com/tikv/pd/issues/4362)の無意味なステップを持つオペレーターを生成する問題を修正
    -   PD クライアント[#4549](https://github.com/tikv/pd/issues/4549)を閉じるときに TSO 取り消しプロセスが停止することがあるバグを修正
    -   リージョンスキャッタラー スケジューリングで一部のピアが失われる問題を修正します[#4565](https://github.com/tikv/pd/issues/4565)
    -   `dr-autosync`の`Duration`フィールドを動的に設定できない問題を修正[#4651](https://github.com/tikv/pd/issues/4651)

-   TiFlash

    -   メモリ制限が有効になっている場合に発生するTiFlashpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   期限切れデータのリサイクルが遅い問題を修正[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `Snapshot`が複数の DDL 操作と同時に適用される場合のTiFlashpanicの潜在的な問題を修正します[#4072](https://github.com/pingcap/tiflash/issues/4072)
    -   重い読み取りワークロードで列を追加した後の潜在的なクエリ エラーを修正[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   負の引数を持つ`SQRT`関数が`Null` [#3598](https://github.com/pingcap/tiflash/issues/3598)ではなく`NaN`を返す問題を修正
    -   `INT`から`DECIMAL`にキャストするとオーバーフローが発生する可能性がある問題を修正[#3920](https://github.com/pingcap/tiflash/issues/3920)
    -   複数値式[#4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付形式で`'\n'`無効な区切り文字[#4036](https://github.com/pingcap/tiflash/issues/4036)として識別される問題を修正します。
    -   同時実行性の高いシナリオ[#3555](https://github.com/pingcap/tiflash/issues/3555)で学習者の読み取りプロセスに時間がかかりすぎる問題を修正します。
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストするときに発生する間違った結果を修正
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します[#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   エラスティック スレッド プールを有効にするとメモリリークが発生する可能性があるバグを修正[#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルするとタスクが永久にハングする可能性があるバグを修正します[#4229](https://github.com/pingcap/tiflash/issues/4229)
    -   HashJoin ビルド側の失敗により MPP クエリが永久にハングする可能性があるバグを修正[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[#4238](https://github.com/pingcap/tiflash/issues/4238)

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作で回復不能なエラーが発生した場合にBR がスタックするバグを修正[#33200](https://github.com/pingcap/tidb/issues/33200)
        -   バックアップの再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正しました[#32423](https://github.com/pingcap/tidb/issues/32423)

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   PDリーダーがキルされた場合にTiCDCノードが異常終了するバグを修正[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   一部の MySQL バージョン[#4504](https://github.com/pingcap/tiflow/issues/4504)のエラー`Unknown system variable 'transaction_isolation'`を修正
        -   `Canal-JSON` `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性がある TiCDCpanicの問題を修正
        -   場合によってはシーケンスが不正に複製されるバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON`が nil [#4736](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性がある TiCDCpanic問題を修正
        -   タイプ`Enum/Set`および`TinyText/MediumText/Text/LongText`の avro コーデックの誤ったデータ マッピングを修正[#4454](https://github.com/pingcap/tiflow/issues/4454)
        -   Avro が`NOT NULL`列を Nullable フィールド[#4818](https://github.com/pingcap/tiflow/issues/4818)に変換するバグを修正
        -   TiCDC が終了できない問題を修正[#4699](https://github.com/pingcap/tiflow/issues/4699)

    -   TiDB データ移行 (DM)

        -   ステータス[#4281](https://github.com/pingcap/tiflow/issues/4281)をクエリする場合にのみ同期メトリクスが更新される問題を修正
        -   セーフモードでの更新ステートメントの実行エラーにより DM ワーカーpanic[#4317](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   long varchar がエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        -   複数の DM ワーカーが同じアップストリーム[#3737](https://github.com/pingcap/tiflow/issues/3737)からデータを書き込むことによって引き起こされる競合の問題を修正します。
        -   ログに何百もの「チェックポイントに変更はありません。同期フラッシュ チェックポイントをスキップします」と出力され、レプリケーションが非常に遅くなる問題を修正します[#4619](https://github.com/pingcap/tiflow/issues/4619)
        -   悲観的モード[#5002](https://github.com/pingcap/tiflow/issues/5002)でシャードをマージし、アップストリームから増分データをレプリケートするときの DML 損失の問題を修正します。

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合、 TiDB Lightning がメタデータスキーマを削除できないことがあるバグを修正[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   ソース ファイルとターゲット クラスターのテーブル名が異なる場合に発生するpanicを修正します[#31771](https://github.com/pingcap/tidb/issues/31771)
        -   チェックサム エラー「GC ライフタイムがトランザクション期間よりも短い」 [#32733](https://github.com/pingcap/tidb/issues/32733)を修正
        -   TiDB Lightning が空のテーブルのチェックに失敗するとスタックする問題を修正[#31797](https://github.com/pingcap/tidb/issues/31797)

    -   Dumpling

        -   `dumpling --sql $query` [#30532](https://github.com/pingcap/tidb/issues/30532)実行時に表示される進行状況が不正確になる問題を修正
        -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正します[#30534](https://github.com/pingcap/tidb/issues/30534)

    -   TiDBBinlog

        -   大規模なアップストリーム書き込みトランザクションが Kafka [#1136](https://github.com/pingcap/tidb-binlog/issues/1136)にレプリケートされるときに、TiDB Binlogがスキップされる可能性がある問題を修正します。

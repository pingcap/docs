---
title: TiDB 6.0.0 Release Notes
summary: TiDB 6.0.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.0.0 リリースノート {#tidb-6-0-0-release-notes}

発売日: 2022年4月7日

TiDB バージョン: 6.0.0-DMR

> **注記：**
>
> TiDB 6.0.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.0/)です。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨しています。

6.0.0-DMR の主な新機能または改善点は次のとおりです。

-   SQL の配置ルールをサポートし、データ配置をより柔軟に管理します。
-   カーネル レベルでデータとインデックス間の一貫性チェックを追加します。これにより、リソースのオーバーヘッドが非常に少なくなり、システムの安定性と堅牢性が向上します。
-   非専門家向けのセルフサービス型データベース パフォーマンス監視および診断機能でTop SQLを提供します。
-   クラスターのパフォーマンス データを常に収集する継続的なプロファイリングをサポートし、技術専門家の MTTR を短縮します。
-   ホットスポットの小さなテーブルをメモリにキャッシュすることで、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが短縮されます。
-   メモリ内の悲観的ロックを最適化します。悲観的ロックによって発生するパフォーマンスのボトルネックに対して、悲観的ロックのメモリ最適化により、レイテンシーを10% 削減し、QPS を 10% 向上させることができます。
-   実行プランを共有するように準備済みステートメントを強化することで、CPU リソースの消費が削減され、SQL 実行の効率が向上します。
-   より多くの式のプッシュダウンとエラスティック スレッド プールの一般提供 (GA) をサポートすることで、MPP エンジンの計算パフォーマンスが向上します。
-   多数の移行タスクの管理を容易にするためにDM WebUIを追加します。
-   大規模クラスターでデータを複製する際の TiCDC の安定性と効率性が向上しました。TiCDC は現在、100,000 個のテーブルを同時に複製することをサポートしています。
-   TiKV ノードの再起動後のリーダー バランシングを高速化し、再起動後のビジネス回復の速度を向上させます。
-   統計の自動更新のキャンセルをサポートし、リソースの競合を減らし、SQL パフォーマンスへの影響を制限します。
-   TiDB クラスターの自動診断サービスであるPingCAPクリニックを提供します (テクニカル プレビュー版)。
-   エンタープライズ レベルのデータベース管理プラットフォームである TiDB Enterprise Manager を提供します。

また、TiDB の HTAP ソリューションのコアコンポーネントとして、 TiFlash <sup>TM が</sup>今回のリリースで正式にオープンソース化されました。詳細については、 [TiFlashリポジトリ](https://github.com/pingcap/tiflash)を参照してください。

## リリース戦略の変更 {#release-strategy-changes}

TiDB v6.0.0 以降、TiDB は次の 2 種類のリリースを提供します。

-   長期サポートリリース

    長期サポート (LTS) リリースは、約 6 か月ごとにリリースされます。LTS リリースでは、新しい機能と改善が導入され、リリース ライフサイクル内でパッチ リリースが受け入れられます。たとえば、v6.1.0 は LTS リリースになります。

-   開発マイルストーンリリース

    開発マイルストーン リリース (DMR) は、約 2 か月ごとにリリースされます。DMR では、新しい機能と改善が導入されますが、パッチ リリースは受け入れられません。ユーザーが本番環境で DMR を使用することは推奨されません。たとえば、v6.0.0-DMR は DMR です。

TiDB v6.0.0 は DMR であり、そのバージョンは 6.0.0-DMR です。

## 新機能 {#new-features}

### 構文 {#sql}

-   SQLベースのデータ配置ルール

    TiDB は、優れたスケーラビリティを備えた分散データベースです。通常、データは複数のサーバー、さらには複数のデータセンターにまたがって展開されます。そのため、データ スケジューリング管理は、TiDB の最も重要な基本機能の 1 つです。ほとんどの場合、ユーザーはデータのスケジュールと管理方法を気にする必要はありません。ただし、アプリケーションの複雑さが増すにつれて、分離とアクセスレイテンシーによって発生する展開の変更が TiDB の新たな課題になっています。v6.0.0 以降、TiDB は SQL インターフェイスに基づくデータ スケジューリングおよび管理機能を正式に提供しています。レプリカ数、ロール タイプ、データの配置場所などのディメンションで柔軟なスケジューリングと管理をサポートします。TiDB は、マルチサービス共有クラスターとクロス AZ 展開でのデータ配置のより柔軟な管理もサポートします。

    [ユーザードキュメント](/placement-rules-in-sql.md)

-   データベースによるTiFlashレプリカの構築をサポートします。データベース内のすべてのテーブルにTiFlashレプリカを追加するには、1 つの SQL ステートメントを使用するだけでよいため、運用および保守コストが大幅に削減されます。

    [ユーザードキュメント](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### トランザクション {#transaction}

-   カーネルレベルでデータインデックスの一貫性のチェックを追加する

    トランザクションの実行時にデータ インデックスの一貫性のチェックを追加します。これにより、リソース オーバーヘッドが非常に少なく、システムの安定性と堅牢性が向上します。チェックの動作は、変数`tidb_enable_mutation_checker`と`tidb_txn_assertion_level`を使用して制御できます。デフォルト構成では、ほとんどのシナリオで QPS の低下は 2% 以内に抑えられます。一貫性チェックのエラーの説明については、 [ユーザードキュメント](/troubleshoot-data-inconsistency-errors.md)を参照してください。

### 可観測性 {#observability}

-   Top SQL: 非専門家向けのパフォーマンス診断

    Top SQL は、DBA およびアプリケーション開発者向けの TiDB ダッシュボードのセルフサービス型データベース パフォーマンス監視および診断機能であり、現在 TiDB v6.0 で一般提供されています。

    専門家向けの既存の診断機能とは異なり、 Top SQLは非専門家向けに設計されています。相関関係を見つけるために何千もの監視チャートを調べたり、 Raft Snapshot、RocksDB、MVCC、TSO などの TiDB の内部メカニズムを理解したりする必要はありません。Top Top SQLを使用してデータベースの負荷を迅速に分析し、アプリのパフォーマンスを向上させるには、基本的なデータベースの知識 (インデックス、ロックの競合、実行プランなど) のみが必要です。

    Top SQLはデフォルトでは有効になっていません。有効にすると、 Top SQL は各 TiKV または TiDB ノードの CPU 負荷をリアルタイムで提供します。そのため、一目で CPU 負荷の高い SQL ステートメントを特定し、データベースのホットスポットや突然の負荷増加などの問題を迅速に分析できます。たとえば、 Top SQLを使用して、単一の TiKV ノードの CPU を 90% 消費する異常なクエリを特定して診断できます。

    [ユーザードキュメント](/dashboard/top-sql.md)

-   継続的なプロファイリングをサポート

    TiDB ダッシュボードでは、継続的プロファイリング機能が導入され、現在 TiDB v6.0 で一般提供されています。継続的プロファイリングはデフォルトでは有効になっていません。有効にすると、個々の TiDB、TiKV、PD インスタンスのパフォーマンス データが常に収集され、オーバーヘッドは無視できます。履歴パフォーマンス データを使用すると、技術専門家は、問題を再現するのが難しい場合でも、メモリ消費量が多いなどの問題の根本原因をさかのぼって特定できます。このようにして、平均復旧時間 (MTTR) を短縮できます。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

### パフォーマンス {#performance}

-   キャッシュホットスポットの小さなテーブル

    ホットスポットの小さなテーブルにアクセスするシナリオのユーザー アプリケーションの場合、TiDB はホットスポット テーブルをメモリに明示的にキャッシュすることをサポートしています。これにより、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが短縮されます。このソリューションにより、サードパーティのキャッシュ ミドルウェアの導入を効果的に回避し、アーキテクチャの複雑さを軽減し、運用と保守のコストを削減できます。このソリューションは、構成テーブルや為替レート テーブルなど、小さなテーブルに頻繁にアクセスされるが、めったに更新されないシナリオに適しています。

    [ユーザードキュメント](/cached-tables.md) , [＃25293](https://github.com/pingcap/tidb/issues/25293)

-   インメモリ悲観的ロック

    TiDB v6.0.0 以降、メモリ内悲観的ロックがデフォルトで有効になっています。この機能を有効にすると、悲観的トランザクション ロックはメモリ内で管理されます。これにより、悲観的的ロックの永続化とロック情報のRaftレプリケーションが回避され、悲観的トランザクション ロックの管理のオーバーヘッドが大幅に削減されます。悲観的ロックによって生じるパフォーマンスのボトルネックでは、悲観的ロックのメモリ最適化により、レイテンシーが10% 削減され、QPS が 10% 向上します。

    [ユーザードキュメント](/pessimistic-transaction.md#in-memory-pessimistic-lock) , [＃11452](https://github.com/tikv/tikv/issues/11452)

-   リードコミット分離レベルでTSOを取得するための最適化

    クエリのレイテンシーを削減するために、読み取り/書き込み競合がまれな場合、TiDB は[コミット読み取り分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)に`tidb_rc_read_check_ts`システム変数を追加して、不要な TSO を減らします。この変数は、デフォルトでは無効になっています。変数を有効にすると、この最適化により、読み取り/書き込み競合がないシナリオで TSO の重複が回避され、レイテンシーが削減されます。ただし、読み取り/書き込み競合が頻繁に発生するシナリオでは、この変数を有効にするとパフォーマンスが低下する可能性があります。

    [ユーザードキュメント](/transaction-isolation-levels.md#read-committed-isolation-level) , [＃33159](https://github.com/pingcap/tidb/issues/33159)

-   実行計画を共有するために準備されたステートメントを強化する

    SQL 実行プランを再利用すると、SQL 文の解析時間を効果的に短縮し、CPU リソースの消費を抑え、SQL 実行効率を向上させることができます。SQL チューニングの重要な方法の 1 つは、SQL 実行プランを効果的に再利用することです。TiDB は、準備済みステートメントとの実行プランの共有をサポートしています。ただし、準備済みステートメントが閉じられると、TiDB は対応するプラン キャッシュを自動的にクリアします。その後、TiDB は繰り返される SQL 文を不必要に解析し、実行効率に影響を与える可能性があります。v6.0.0 以降、TiDB は`tidb_ignore_prepared_cache_close_stmt`のパラメータ (デフォルトでは無効) を通じて`COM_STMT_CLOSE`のコマンドを無視するかどうかの制御をサポートしています。パラメータを有効にすると、TiDB は準備済みステートメントを閉じるコマンドを無視し、実行プランをキャッシュに保持するため、実行プランの再利用率が向上します。

    [ユーザードキュメント](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) , [＃31056](https://github.com/pingcap/tidb/issues/31056)

-   クエリプッシュダウンの改善

    TiDB は、コンピューティングとstorageを分離するネイティブアーキテクチャを備え、演算子をプッシュダウンすることで無効なデータをフィルター処理します。これにより、TiDB と TiKV 間のデータ転送が大幅に削減され、クエリの効率が向上します。v6.0.0 では、TiDB はより多くの式と`BIT`データ型を TiKV にプッシュダウンし、式とデータ型を計算する際のクエリの効率が向上します。

    [ユーザードキュメント](/functions-and-operators/expressions-pushed-down.md) , [＃30738](https://github.com/pingcap/tidb/issues/30738)

-   ホットスポットインデックスの最適化

    単調に増加するデータをバッチでセカンダリ インデックスに書き込むと、インデックス ホットスポットが発生し、全体的な書き込みスループットに影響します。v6.0.0 以降、TiDB は、書き込みパフォーマンスを向上させるために、 `tidb_shard`関数を使用してインデックス ホットスポットを分散することをサポートしています。現在、 `tidb_shard`一意のセカンダリ インデックスにのみ影響します。このアプリケーション フレンドリなソリューションでは、元のクエリ条件を変更する必要がありません。このソリューションは、書き込みスループットが高い、ポイント クエリ、バッチ ポイント クエリのシナリオで使用できます。範囲クエリによって分散されたデータをアプリケーションで使用すると、パフォーマンスが低下する可能性があることに注意してください。したがって、このような場合には、検証せずにこの機能を使用しないでください。

    [ユーザードキュメント](/functions-and-operators/tidb-functions.md#tidb_shard) , [＃31040](https://github.com/pingcap/tidb/issues/31040)

-   TiFlash MPP エンジンのパーティション テーブルの動的プルーニング モードをサポート (実験的)

    このモードでは、TiDB はTiFlashの MPP エンジンを使用してパーティション テーブル上のデータを読み取って計算できるため、パーティション テーブルのクエリ パフォーマンスが大幅に向上します。

    [ユーザードキュメント](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

-   MPPエンジンの計算パフォーマンスを向上させる

    -   より多くの関数と演算子をMPPエンジンにプッシュダウンするサポート

        -   論理関数`IS NOT` `IS`
        -   文字列関数: `REGEXP()` , `NOT REGEXP()`
        -   数学関数: `GREATEST(int/real)` , `LEAST(int/real)`
        -   `LAST_DAY()`関数`MONTHNAME()` `DAYNAME()` `DAYOFMONTH()` `DAYOFWEEK()` `DAYOFYEAR()`
        -   演算子: 反左外部セミ結合、左外部セミ結合

        [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md)

    -   エラスティック スレッド プール (デフォルトで有効) が GA になります。この機能は、CPU 使用率を向上させることを目的としています。

        [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### 安定性 {#stability}

-   実行計画のベースラインキャプチャを強化する

    テーブル名、頻度、ユーザー名などのディメンションを含むブロックリストを追加することで、実行プランのベースライン キャプチャの使いやすさが向上します。キャッシュ バインディングのメモリ管理を最適化する新しいアルゴリズムを導入します。ベースライン キャプチャを有効にすると、ほとんどの OLTP クエリのバインディングが自動的に作成されます。バインドされたステートメントの実行プランは固定されるため、実行プランの変更によるパフォーマンスの問題は回避されます。ベースライン キャプチャは、メジャー バージョン アップグレードやクラスターの移行などのシナリオに適用でき、実行プランの回帰によって発生するパフォーマンスの問題を軽減するのに役立ちます。

    [ユーザードキュメント](/sql-plan-management.md#baseline-capturing) , [＃32466](https://github.com/pingcap/tidb/issues/32466)

-   TiKV クォータ リミッターのサポート (実験的)

    TiKV を導入したマシンのリソースが限られており、フォアグラウンドに過度のリクエスト負荷がかかると、バックグラウンドの CPU リソースがフォアグラウンドによって占有され、TiKV のパフォーマンスが不安定になります。TiDB v6.0.0 では、クォータ関連の設定項目を使用して、CPU や読み取り/書き込み帯域幅など、フォアグラウンドで使用されるリソースを制限できます。これにより、長期間にわたる高負荷のワークロード下でもクラスターの安定性が大幅に向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#quota) , [＃12131](https://github.com/tikv/tikv/issues/12131)

-   TiFlashのzstd圧縮アルゴリズムをサポート

    TiFlashでは、 `profiles.default.dt_compression_method`と`profiles.default.dt_compression_level` 2 つのパラメーターが導入され、ユーザーはパフォーマンスと容量のバランスに基づいて最適な圧縮アルゴリズムを選択できます。

    [ユーザードキュメント](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   すべてのI/Oチェック（チェックサム）をデフォルトで有効にする

    この機能は、v5.4.0 で実験的に導入されました。ユーザーのビジネスに明らかな影響を与えることなく、データの精度とセキュリティを強化します。

    警告: 新しいバージョンのデータ形式は、v5.4.0 より前のバージョンにそのままダウングレードすることはできません。このようなダウングレード中は、ダウングレード後にTiFlashレプリカとレプリケートされたデータを削除する必要があります。または、 [dttool 移行](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してダウングレードを実行することもできます。

    [ユーザードキュメント](/tiflash/tiflash-data-validation.md)

-   スレッドの使用率を向上させる

    TiFlash は、非同期 gRPC および Min-TSO スケジューリング メカニズムを導入します。これらのメカニズムにより、スレッドのより効率的な使用が保証され、過剰なスレッドによるシステム クラッシュが回避されます。

    [ユーザードキュメント](/tiflash/monitor-tiflash.md#coprocessor)

### データ移行 {#data-migration}

#### TiDB データ移行 (DM) {#tidb-data-migration-dm}

-   WebUI を追加 (実験的)

    WebUI を使用すると、多数の移行タスクを簡単に管理できます。WebUI では、次の操作を実行できます。

    -   ダッシュボードで移行タスクをビュー
    -   移行タスクの管理
    -   アップストリーム設定を構成する
    -   レプリケーションステータスのクエリ
    -   マスターとワーカーの情報をビュー

    WebUI はまだ実験的であり、開発中です。したがって、試用のみに推奨されます。既知の問題として、WebUI と dmctl を使用して同じタスクを操作すると問題が発生する場合があります。この問題は、今後のバージョンで解決される予定です。

    [ユーザードキュメント](/dm/dm-webui-guide.md)

-   エラー処理メカニズムを追加する

    移行タスクを中断する問題に対処するために、さらに多くのコマンドが導入されています。例:

    -   スキーマ エラーが発生した場合は、スキーマ ファイルを個別に編集するのではなく、 `binlog-schema update`コマンドの`--from-source/--from-target`パラメータを使用してスキーマ ファイルを更新できます。
    -   binlogの位置を指定して、DDL ステートメントを挿入、置換、スキップ、または元に戻すことができます。

    [ユーザードキュメント](/dm/dm-manage-schema.md)

-   Amazon S3への完全なデータstorageをサポート

    DM がすべてのデータ移行タスクまたは完全なデータ移行タスクを実行する場合、上流からの全データを格納するために十分なハードディスク容量が必要です。EBS と比較すると、Amazon S3 は低コストでほぼ無制限のstorageを備えています。現在、DM は Amazon S3 をダンプ ディレクトリとして構成することをサポートしています。つまり、すべてのデータ移行タスクまたは完全なデータ移行タスクを実行するときに、S3 を使用して全データを格納できます。

    [ユーザードキュメント](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   指定した時間から移行タスクを開始することをサポート

    移行タスクに新しいパラメータ`--start-time`が追加されました。「2021-10-21 00:01:00」または「2021-10-21T00:01:00」の形式で時間を定義できます。

    この機能は、シャード MySQL インスタンスから増分データを移行およびマージするシナリオで特に役立ちます。具体的には、増分移行タスクでソースごとにbinlog開始ポイントを設定する必要はありません。代わりに、 `safe-mode`の`--start-time`パラメータを使用して、増分移行タスクをすばやく作成できます。

    [ユーザードキュメント](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning {#tidb-lightning}

-   許容可能なエラーの最大数の設定をサポート

    設定項目`lightning.max-error`を追加しました。デフォルト値は 0 です。値が 0 より大きい場合、max-error 機能が有効になります。エンコード中に行にエラーが発生した場合、この行を含むレコードがターゲット TiDB の`lightning_task_info.type_error_v1`に追加され、この行は無視されます。エラーのある行がしきい値を超えると、 TiDB Lightning は直ちに終了します。

    `lightning.max-error`の構成と一致して、 `lightning.task-info-schema-name`の構成項目は、データ保存エラーを報告するデータベースの名前を記録します。

    この機能はすべてのタイプのエラーをカバーするわけではありません。たとえば、構文エラーは適用されません。

    [ユーザードキュメント](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   100,000 個のテーブルを同時に複製するサポート

    TiCDC は、データ処理フローを最適化することで、各テーブルの増分データ処理のリソース消費を削減し、大規模クラスターでデータを複製する際のレプリケーションの安定性と効率を大幅に向上させます。内部テストの結果、TiCDC は 100,000 個のテーブルを同時に複製することを安定してサポートできることが示されています。

### 導入とメンテナンス {#deployment-and-maintenance}

-   新しい照合順序ルールをデフォルトで有効にする

    v4.0 以降、TiDB は、大文字と小文字を区別しない、アクセントを区別しない、およびパディング ルールにおいて MySQL と同じように動作する新しい照合順序ルールをサポートしています。新しい照合順序ルールは、デフォルトでは無効になっている`new_collations_enabled_on_first_bootstrap`パラメータによって制御されます。v6.0 以降、TiDB は新しい照合順序ルールをデフォルトで有効にします。この構成は、TiDB クラスターの初期化時にのみ有効になることに注意してください。

    [ユーザードキュメント](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

-   TiKVノードの再起動後のリーダーバランシングを高速化

    TiKV ノードの再起動後、不均等に分散されたリーダーは負荷分散のために再配分する必要があります。大規模クラスターでは、リーダー分散時間はリージョン数と正の相関関係にあります。たとえば、100K リージョンのリーダー分散には 20 ～ 30 分かかることがあり、不均等な負荷によるパフォーマンスの問題や安定性のリスクが生じやすくなります。TiDB v6.0.0 では、分散同時実行を制御するパラメータが提供され、デフォルト値が元の 4 倍に拡大されました。これにより、リーダーの再分散時間が大幅に短縮され、TiKV ノードの再起動後のビジネス回復が加速されます。

    [ユーザードキュメント](/pd-control.md#scheduler-config-balance-leader-scheduler) , [＃4610](https://github.com/tikv/pd/issues/4610)

-   統計の自動更新のキャンセルをサポート

    統計は、SQL パフォーマンスに影響を与える最も重要な基本データの 1 つです。統計の完全性と適時性を確保するために、TiDB はオブジェクト統計をバックグラウンドで定期的に自動更新します。ただし、統計の自動更新によってリソースの競合が発生し、SQL パフォーマンスに影響を与える可能性があります。この問題に対処するために、v6.0 以降では統計の自動更新を手動でキャンセルできます。

    [ユーザードキュメント](/statistics.md#automatic-update)

-   PingCAPクリニック診断サービス（テクニカルプレビュー版）

    PingCAPクリニック は、 TiDB クラスターの診断サービスです。このサービスは、クラスターの問題をリモートでトラブルシューティングするのに役立ち、クラスターの状態をローカルですばやく確認できます。PingCAP PingCAPクリニックを使用すると、TiDB クラスターのライフサイクル全体にわたって安定した動作を確保し、潜在的な問題を予測し、問題の発生確率を減らし、クラスターの問題をすばやくトラブルシューティングできます。

    クラスターの問題をトラブルシューティングするために PingCAP テクニカル サポートにリモート アシスタンスを依頼する場合、 PingCAPクリニックサービスを使用して診断データを収集およびアップロードすることで、トラブルシューティングの効率を向上させることができます。

    [ユーザードキュメント](/clinic/clinic-introduction.md)

-   エンタープライズレベルのデータベース管理プラットフォーム、TiDB Enterprise Manager

    TiDB Enterprise Manager (TiEM) は、TiDB データベースに基づくエンタープライズ レベルのデータベース管理プラットフォームであり、ユーザーがセルフホスト環境またはパブリック クラウド環境で TiDB クラスターを管理できるようにすることを目的としています。

    TiEM は、TiDB クラスターのライフサイクル全体の視覚的な管理を提供するだけでなく、パラメーター管理、バージョン アップグレード、クラスター クローン、アクティブ/スタンバイ クラスターの切り替え、データのインポートとエクスポート、データのレプリケーション、データのバックアップと復元サービスなど、ワンストップ サービスも提供します。TiEM は、TiDB での DevOps の効率を向上させ、企業の DevOps コストを削減します。

    現在、TiEM は[TiDBエンタープライズ](https://en.pingcap.com/tidb-enterprise/)エディションのみで提供されています。TiEM を入手するには、 [TiDBエンタープライズ](https://en.pingcap.com/tidb-enterprise/)ページからお問い合わせください。

-   監視コンポーネントの構成のカスタマイズをサポート

    TiUPを使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視コンポーネントを自動的にデプロイし、スケールアウト後に新しいノードを監視スコープに自動的に追加します。1 ファイルに構成項目を追加することで`topology.yaml`監視コンポーネントの構成をカスタマイズできます。

    [ユーザードキュメント](/tiup/customized-montior-in-tiup-environment.md)

## 互換性の変更 {#compatibility-changes}

> **注記：**
>
> 以前の TiDB バージョンから v6.0.0 にアップグレードする場合、すべての中間バージョンの互換性変更ノートを知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

<table><thead><tr><th>変数名</th><th>タイプを変更</th><th>説明</th></tr></thead><tbody><tr><td><code>placement_checks</code></td><td>削除されました</td><td>DDL ステートメントが<a href="https://docs.pingcap.com/tidb/dev/placement-rules-in-sql">SQL の配置ルール</a>で指定され<code>tidb_placement_mode</code>配置ルールを検証するかどうかを制御します。tidb_placement_mode に置き換えられました。</td></tr><tr><td> <code>tidb_enable_alter_placement</code></td><td>削除されました</td><td><a href="https://docs.pingcap.com/tidb/dev/placement-rules-in-sql">SQL で配置ルール</a>を有効にするかどうかを制御します。</td></tr><tr><td> <code>tidb_mem_quota_hashjoin</code><br/> <code>tidb_mem_quota_indexlookupjoin</code><br/> <code>tidb_mem_quota_indexlookupreader</code><br/> <code>tidb_mem_quota_mergejoin</code><br/> <code>tidb_mem_quota_sort</code><br/> <code>tidb_mem_quota_topn</code></td><td>削除されました</td><td>v5.0 以降、これらの変数は<code>tidb_mem_quota_query</code>に置き換えられ、<a href="https://docs.pingcap.com/tidb/dev/system-variables">システム変数</a>ドキュメントから削除されました。互換性を確保するため、これらの変数はソース コードに保持されていました。TiDB 6.0.0 以降、これらの変数もコードから削除されています。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_enable_mutation_checker-new-in-v600"><code>tidb_enable_mutation_checker</code></a></td><td>新しく追加された</td><td>ミューテーション チェッカーを有効にするかどうかを制御します。デフォルト値は<code>ON</code>です。v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、ミューテーション チェッカーはデフォルトで無効になっています。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_ignore_prepared_cache_close_stmt-new-in-v600"><code>tidb_ignore_prepared_cache_close_stmt</code></a></td><td>新しく追加された</td><td>準備されたステートメントを閉じるコマンドを無視するかどうかを制御します。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_mem_quota_binding_cache-new-in-v600"><code>tidb_mem_quota_binding_cache</code></a></td><td>新しく追加された</td><td>キャッシュ保持バインディングのメモリ使用量しきい値を設定します。デフォルト値は<code>67108864</code> (64 MiB) です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_placement_mode-new-in-v600"><code>tidb_placement_mode</code></a></td><td>新しく追加された</td><td>DDL ステートメントが<a href="https://docs.pingcap.com/tidb/dev/placement-rules-in-sql">SQL の配置ルール</a>で指定された配置ルールを無視するかどうかを制御します。デフォルト値は<code>strict</code>で、DDL ステートメントが配置ルールを無視しないことを意味します。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_rc_read_check_ts-new-in-v600"><code>tidb_rc_read_check_ts</code></a></td><td>新しく追加された</td><td><ul><li>トランザクション内の読み取りステートメントのレイテンシーを最適化します。読み取り/書き込みの競合が深刻な場合は、この変数をオンにすると、オーバーヘッドとレイテンシーが追加され、パフォーマンスが低下します。デフォルト値は<code>off</code>です。</li><li>この変数はまだ<a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_replica_read-new-in-v40">replica-read</a>と互換性がありません。読み取り要求で<code>tidb_rc_read_check_ts</code>がオンになっている場合、replica-read を使用できない可能性があります。両方の変数を同時にオンにしないでください。</li></ul></td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_sysdate_is_now-new-in-v600"><code>tidb_sysdate_is_now</code></a></td><td>新しく追加された</td><td><code>SYSDATE</code>関数を<code>NOW</code>関数に置き換えることができるかどうかを制御します。この構成項目は、MySQL オプション<a href="https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now"><code>sysdate-is-now</code></a>と同じ効果があります。デフォルト値は<code>OFF</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_table_cache_lease-new-in-v600"><code>tidb_table_cache_lease</code></a></td><td>新しく追加された</td><td><a href="https://docs.pingcap.com/tidb/dev/cached-tables">テーブル キャッシュ</a>のリース時間を秒単位で制御します。デフォルト値は<code>3</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_top_sql_max_meta_count-new-in-v600"><code>tidb_top_sql_max_meta_count</code></a></td><td>新しく追加された</td><td><a href="https://docs.pingcap.com/tidb/dev/top-sql">Top SQL</a>によって 1 分あたりに収集される SQL ステートメント タイプの最大数を制御します。デフォルト値は<code>5000</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_top_sql_max_time_series_count-new-in-v600"><code>tidb_top_sql_max_time_series_count</code></a></td><td>新しく追加された</td><td>負荷に最も寄与する SQL ステートメント (つまり、上位 N) を 1 分あたり<a href="https://docs.pingcap.com/tidb/dev/top-sql">Top SQL</a>で記録できる数を制御します。デフォルト値は<code>100</code>です。</td></tr><tr><td> <a href="https://docs.pingcap.com/tidb/dev/system-variables#tidb_txn_assertion_level-new-in-v600"><code>tidb_txn_assertion_level</code></a></td><td>新しく追加された</td><td>アサーション レベルを制御します。アサーションは、データとインデックス間の一貫性チェックであり、トランザクション コミット プロセスで書き込まれるキーが存在するかどうかをチェックします。デフォルトでは、チェックによってほとんどのチェック項目が有効になり、パフォーマンスにはほとんど影響しません。v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、チェックはデフォルトで無効になっています。</td></tr></tbody></table>

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

<table><thead><tr><th>コンフィグレーションファイル</th><th>コンフィグレーション</th><th>タイプを変更</th><th>説明</th></tr></thead><tbody><tr><td>ティビ</td><td><code>stmt-summary.enable</code><br/> <code>stmt-summary.enable-internal-query</code><br/> <code>stmt-summary.history-size</code><br/> <code>stmt-summary.max-sql-length</code><br/> <code>stmt-summary.max-stmt-count</code><br/> <code>stmt-summary.refresh-interval</code></td><td>削除されました</td><td><a href="https://docs.pingcap.com/tidb/dev/statement-summary-tables">ステートメント サマリー テーブル</a>に関連するコンフィグレーション。これらの構成項目はすべて削除されます。ステートメント サマリー テーブルを制御するには、SQL 変数を使用する必要があります。</td></tr><tr><td>ティビ</td><td><a href="https://docs.pingcap.com/tidb/dev/tidb-configuration-file#new_collations_enabled_on_first_bootstrap"><code>new_collations_enabled_on_first_bootstrap</code></a></td><td>修正済み</td><td>新しい照合順序のサポートを有効にするかどうかを制御します。v6.0 以降、デフォルト値は<code>false</code>から<code>true</code>に変更されました。この構成項目は、クラスターが初めて初期化されるときにのみ有効になります。最初のブートストラップの後は、この構成項目を使用して新しい照合順序フレームワークを有効または無効にすることはできません。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#num-threads-1"><code>backup.num-threads</code></a></td><td>修正済み</td><td>値の範囲は<code>[1, CPU]</code>に変更されます。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#apply-max-batch-size"><code>raftstore.apply-max-batch-size</code></a></td><td>修正済み</td><td>最大値は<code>10240</code>に変更されます。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#raft-max-size-per-msg"><code>raftstore.raft-max-size-per-msg</code></a></td><td>修正済み</td><td>最小値が<code>0</code>から<code>0</code>より大きい値に変更されます。<br/>最大値は<code>3GB</code>に設定されています。<br/>単位が<code>MB</code>から<code>KB|MB|GB</code>に変更されます。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#store-max-batch-size"><code>raftstore.store-max-batch-size</code></a></td><td>修正済み</td><td>最大値は<code>10240</code>に設定されています。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#max-thread-count"><code>readpool.unified.max-thread-count</code></a></td><td>修正済み</td><td>調整可能な範囲は<code>[min-thread-count, MAX(4, CPU)]</code>に変更されます。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#enable-pipelined-write"><code>rocksdb.enable-pipelined-write</code></a></td><td>修正済み</td><td>デフォルト値は<code>true</code>から<code>false</code>に変更されます。この構成を有効にすると、以前のパイプライン書き込みが使用されます。この構成を無効にすると、新しいパイプラインコミット メカニズムが使用されます。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#max-background-flushes"><code>rocksdb.max-background-flushes</code></a></td><td>修正済み</td><td>CPU コア数が 10 の場合、デフォルト値は<code>3</code>です。<br/> CPU コア数が 8 の場合、デフォルト値は<code>2</code>です。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#max-background-jobs"><code>rocksdb.max-background-jobs</code></a></td><td>修正済み</td><td>CPU コア数が 10 の場合、デフォルト値は<code>9</code>です。<br/> CPU コア数が 8 の場合、デフォルト値は<code>7</code>です。</td></tr><tr><td>TiFlash</td><td><a href="https://docs.pingcap.com/tidb/dev/tiflash-configuration#configure-the-tiflashtoml-file"><code>profiles.default.dt_enable_logical_split</code></a></td><td>修正済み</td><td>DeltaTree ストレージ エンジンのセグメントが論理分割を使用するかどうかを決定します。デフォルト値は<code>true</code>から<code>false</code>に変更されます。</td></tr><tr><td>TiFlash</td><td><a href="https://docs.pingcap.com/tidb/dev/tiflash-configuration#configure-the-tiflashtoml-file"><code>profiles.default.enable_elastic_threadpool</code></a></td><td>修正済み</td><td>エラスティック スレッド プールを有効にするかどうかを制御します。デフォルト値は<code>false</code>から<code>true</code>に変更されます。</td></tr><tr><td>TiFlash</td><td><a href="https://docs.pingcap.com/tidb/dev/tiflash-configuration#configure-the-tiflashtoml-file"><code>storage.format_version</code></a></td><td>修正済み</td><td>TiFlashのデータ検証機能を制御します。デフォルト値は<code>2</code>から<code>3</code>に変更されます。<br/> <code>format_version</code>が<code>3</code>に設定されている場合、ハードウェア障害による誤った読み取りを回避するために、すべてのTiFlashデータの読み取り操作に対して一貫性チェックが実行されます。<br/>新しい形式のバージョンは、v5.4 より前のバージョンにそのままダウングレードすることはできないことに注意してください。</td></tr><tr><td>ティビ</td><td><a href="https://docs.pingcap.com/tidb/dev/tidb-configuration-file#pessimistic-auto-commit-new-in-v600"><code>pessimistic-txn.pessimistic-auto-commit</code></a></td><td>新しく追加された</td><td>悲観的トランザクション モードがグローバルに有効になっている場合 ( <code>tidb_txn_mode=&#39;pessimistic&#39;</code> )、自動コミット トランザクションが使用するトランザクション モードを決定します。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#in-memory-new-in-v600"><code>pessimistic-txn.in-memory</code></a></td><td>新しく追加された</td><td>メモリ内の悲観的ロックを有効にするかどうかを制御します。この機能を有効にすると、悲観的トランザクションは、悲観的ロックをディスクに書き込んだり、他のレプリカに複製したりするのではなく、可能な限り TiKVメモリに悲観的ロックを保存します。これにより、悲観的的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われる可能性は低く、悲観的トランザクションがコミットに失敗する可能性があります。デフォルト値は<code>true</code>です。</td></tr><tr><td>ティクヴ</td><td><a href="https://docs.pingcap.com/tidb/dev/tikv-configuration-file#quota"><code>quota</code></a></td><td>新しく追加された</td><td>フロントエンド リクエストによって占有されるリソースを制限する Quota Limiter に関連する設定項目を追加します。Quota Limiter は実験的機能であり、デフォルトでは無効になっています。新しいクォータ関連の設定項目は<code>foreground-cpu-time</code> 、 <code>foreground-write-bandwidth</code> 、 <code>foreground-read-bandwidth</code> 、および<code>max-delay-duration</code>です。</td></tr><tr><td>TiFlash</td><td><a href="https://docs.pingcap.com/tidb/dev/tiflash-configuration#configure-the-tiflashtoml-file"><code>profiles.default.dt_compression_method</code></a></td><td>新しく追加された</td><td>TiFlashの圧縮アルゴリズムを指定します。オプションの値は<code>LZ4</code> 、 <code>zstd</code> 、 <code>LZ4HC</code>で、すべて大文字と小文字は区別されません。デフォルト値は<code>LZ4</code>です。</td></tr><tr><td>TiFlash</td><td><a href="https://docs.pingcap.com/tidb/dev/tiflash-configuration#configure-the-tiflashtoml-file"><code>profiles.default.dt_compression_level</code></a></td><td>新しく追加された</td><td>TiFlashの圧縮レベルを指定します。デフォルト値は<code>1</code>です。</td></tr><tr><td> DM</td><td> <a href="https://docs.pingcap.com/tidb/dev/task-configuration-file-full#task-configuration-file-template-advanced"><code>loaders.&lt;name&gt;.import-mode</code></a></td><td>新しく追加された</td><td>完全インポート フェーズ中のインポート モード。v6.0 以降、DM は完全インポート フェーズ中にデータをインポートするために TiDB Lightning の TiDB バックエンド モードを使用します。以前の Loaderコンポーネントは使用されなくなりました。これは内部的な置き換えであり、日常業務に明らかな影響はありません。<br/>デフォルト値は<code>sql</code>に設定されており、これは tidb-backend モードを使用することを意味します。まれに、 tidb-backend が完全に互換性がない場合があります。このパラメータを<code>loader</code>に設定することで、Loader モードにフォールバックできます。</td></tr><tr><td> DM</td><td> <a href="https://docs.pingcap.com/tidb/dev/task-configuration-file-full#task-configuration-file-template-advanced"><code>loaders.&lt;name&gt;.on-duplicate</code></a></td><td>新しく追加された</td><td>完全インポート フェーズ中に競合を解決する方法を指定します。デフォルト値は<code>replace</code>で、これは新しいデータを使用して既存のデータを置き換えることを意味します。</td></tr><tr><td>ティCDC</td><td> <a href="https://docs.pingcap.com/tidb/dev/ticdc-sink-to-kafka#configure-sink-uri-for-kafka"><code>dial-timeout</code></a></td><td>新しく追加された</td><td>ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は<code>10s</code>です。</td></tr><tr><td>ティCDC</td><td> <a href="https://docs.pingcap.com/tidb/dev/ticdc-sink-to-kafka#configure-sink-uri-for-kafka"><code>read-timeout</code></a></td><td>新しく追加された</td><td>ダウンストリーム Kafka から返される応答を取得する際のタイムアウト。デフォルト値は<code>10s</code>です。</td></tr><tr><td>ティCDC</td><td> <a href="https://docs.pingcap.com/tidb/dev/ticdc-sink-to-kafka#configure-sink-uri-for-kafka"><code>write-timeout</code></a></td><td>新しく追加された</td><td>ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は<code>10s</code>です。</td></tr></tbody></table>

### その他 {#others}

-   データ配置ポリシーには、次の互換性の変更があります。
    -   バインディングはサポートされていません。直接配置オプションは構文から削除されています。
    -   `CREATE PLACEMENT POLICY`および`ALTER PLACEMENT POLICY`ステートメントは、 `VOTERS`および`VOTER_CONSTRAINTS`配置オプションをサポートしなくなりました。
    -   TiDB 移行ツール (TiDB Binlog、TiCDC、 BR) が配置ルールと互換性を持つようになりました。配置オプションは、TiDB Binlogの特別なコメントに移動されました。
    -   `information_schema.placement_rules`システム テーブルの名前が`information_schema.placement_policies`に変更されました。このテーブルには、配置ポリシーに関する情報のみが表示されるようになりました。
    -   `placement_checks`システム変数は`tidb_placement_mode`に置き換えられます。
    -   TiFlashレプリカを持つテーブルに配置ルールを持つパーティションを追加することは禁止されています。
    -   `INFORMATION_SCHEMA`テーブルから`TIDB_DIRECT_PLACEMENT`列目を削除します。
-   SQL プラン管理 (SPM) バインディングの`status`値が変更されます。
    -   `using`削除します。
    -   `using`の代わりに`enabled` (使用可能) を追加します。
    -   `disabled`追加します (利用不可)。
-   DMはOpenAPIインターフェースを変更する
    -   内部機構の変更により、タスク管理に関するインターフェースは以前の実験的バージョンとの互換性がありません。適応するには新しいバージョン[DM OpenAPI ドキュメント](/dm/dm-open-api.md)を参照する必要があります。
-   DMは、完​​全なインポートフェーズ中に競合を解決する方法を変更します。
    -   `loader.<name>.on-duplicate`パラメータが追加されました。デフォルト値は`replace`で、これは新しいデータを使用して既存のデータを置き換えることを意味します。以前の動作を維持する場合は、値を`error`に設定できます。このパラメータは、完全なインポート フェーズでの動作のみを制御します。
-   DMを使用するには、 `dmctl`の対応するバージョンを使用する必要があります。
    -   内部メカニズムの変更により、DM を v6.0.0 にアップグレードした後、 `dmctl` v6.0.0 にアップグレードする必要があります。
-   v5.4 (v5.4 のみ) では、TiDB は一部の noop システム変数に不正な値を許可します。v6.0.0 以降、TiDB はシステム変数に不正な値を設定することを許可しません[＃31538](https://github.com/pingcap/tidb/issues/31538)

## 改善点 {#improvements}

-   ティビ

    -   `FLASHBACK`または`RECOVER`ステートメントを使用してテーブルを復元した後、テーブルの配置ルール設定を自動的にクリアします[＃31668](https://github.com/pingcap/tidb/issues/31668)
    -   パフォーマンス概要ダッシュボードを追加して、一般的なクリティカルパスのコアパフォーマンスメトリックを表示し、TiDB でのメトリック分析を容易にします[＃31676](https://github.com/pingcap/tidb/issues/31676)
    -   `LOAD DATA LOCAL INFILE`ステートメント[＃24515](https://github.com/pingcap/tidb/issues/24515)で`REPLACE`キーワードの使用をサポート
    -   範囲パーティションテーブル[＃26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティションプルーニングをサポート
    -   MPP 集計クエリで冗長な Exchange 操作を排除することでクエリの効率を向上[＃31762](https://github.com/pingcap/tidb/issues/31762)
    -   `TRUNCATE PARTITION`と`DROP PARTITION`ステートメントで重複するパーティション名を許可することでMySQLとの互換性を向上させる[＃31681](https://github.com/pingcap/tidb/issues/31681)
    -   `ADMIN SHOW DDL JOBS`ステートメント[＃23494](https://github.com/pingcap/tidb/issues/23494)の結果に`CREATE_TIME`情報を表示することをサポートします
    -   新しい組み込み関数`CHARSET()` [＃3931](https://github.com/pingcap/tidb/issues/3931)をサポート
    -   ユーザー名によるベースラインキャプチャブロックリストのフィルタリングをサポート[＃32558](https://github.com/pingcap/tidb/issues/32558)
    -   ベースラインキャプチャブロックリストでのワイルドカードの使用をサポート[＃32714](https://github.com/pingcap/tidb/issues/32714)
    -   `ADMIN SHOW DDL JOBS`と`SHOW TABLE STATUS`ステートメントの結果を、現在の`time_zone` [＃26642](https://github.com/pingcap/tidb/issues/26642)に従って時間を表示することで最適化します。
    -   `DAYNAME()`と`MONTHNAME()`関数をTiFlash [＃32594](https://github.com/pingcap/tidb/issues/32594)にプッシュダウンするサポート
    -   `REGEXP`機能をTiFlash [＃32637](https://github.com/pingcap/tidb/issues/32637)にプッシュダウンするサポート
    -   `DAYOFMONTH()`と`LAST_DAY()`関数をTiFlash [＃33012](https://github.com/pingcap/tidb/issues/33012)にプッシュダウンするサポート
    -   `DAYOFWEEK()`と`DAYOFYEAR()`関数をTiFlash [＃33130](https://github.com/pingcap/tidb/issues/33130)にプッシュダウンするサポート
    -   `IS_TRUE` `IS_FALSE`関数を`IS_TRUE_WITH_NULL` TiFlash [＃33047](https://github.com/pingcap/tidb/issues/33047)プッシュダウンするサポート
    -   `GREATEST`と`LEAST`関数をTiFlash [＃32787](https://github.com/pingcap/tidb/issues/32787)にプッシュダウンするサポート
    -   `UnionScan`オペレータ[＃32631](https://github.com/pingcap/tidb/issues/32631)の実行の追跡をサポート
    -   `_tidb_rowid`列[＃31543](https://github.com/pingcap/tidb/issues/31543)列を読み取るクエリにPointGetプランの使用をサポート
    -   `EXPLAIN`ステートメントの出力で、名前を小文字に変換せずに元のパーティション名を表示することをサポート[＃32719](https://github.com/pingcap/tidb/issues/32719)
    -   IN条件と文字列型列のRANGE COLUMNSパーティションのパーティションプルーニングを有効にする[＃32626](https://github.com/pingcap/tidb/issues/32626)
    -   システム変数がNULLに設定されている場合にエラーメッセージを返す[＃32850](https://github.com/pingcap/tidb/issues/32850)
    -   非MPPモード[＃31465](https://github.com/pingcap/tidb/issues/31465)からブロードキャスト参加を削除する
    -   動的プルーニングモード[＃32347](https://github.com/pingcap/tidb/issues/32347)でパーティションテーブル上でMPPプランの実行をサポート
    -   共通テーブル式 (CTE) の述語のプッシュダウンをサポート[＃28163](https://github.com/pingcap/tidb/issues/28163)
    -   `Statement Summary`と`Capture Plan Baselines`の構成を簡素化し、グローバルベースでのみ利用可能にする[＃30557](https://github.com/pingcap/tidb/issues/30557)
    -   macOS 12 [＃31607](https://github.com/pingcap/tidb/issues/31607)でバイナリをビルドするときに報告されるアラームに対処するため、gopsutil を v3.21.12 に更新しました。

-   ティクヴ

    -   多くのキー範囲を持つバッチに対するRaftstoreのサンプリング精度を向上[＃12327](https://github.com/tikv/tikv/issues/12327)
    -   `debug/pprof/profile`に正しい「Content-Type」を追加して、プロファイルをより簡単に識別できるようにします[＃11521](https://github.com/tikv/tikv/issues/11521)
    -   Raftstore がハートビートを持っているときや読み取り要求を処理しているときに、リーダーのリースの時間を無期限に更新します。これにより、レイテンシージッターが削減されます[＃11579](https://github.com/tikv/tikv/issues/11579)
    -   リーダーを切り替える際にコストが最も少ないストアを選択すると、パフォーマンスの安定性が向上します[＃10602](https://github.com/tikv/tikv/issues/10602)
    -   Raftログを非同期に取得して、 Raftstore [＃11320](https://github.com/tikv/tikv/issues/11320)をブロックすることによって発生するパフォーマンスジッターを軽減します。
    -   ベクトル計算[＃5751](https://github.com/tikv/tikv/issues/5751) `QUARTER`関数をサポート
    -   `BIT`データ型を TiKV [＃30738](https://github.com/pingcap/tidb/issues/30738)にプッシュダウンするサポート
    -   `MOD`関数と`SYSDATE`関数をTiKV [＃11916](https://github.com/tikv/tikv/issues/11916)にプッシュダウンするサポート
    -   解決ロックを必要とする領域の数を減らすことで、TiCDC の回復時間を短縮します (ステップ[＃11993](https://github.com/tikv/tikv/issues/11993)
    -   `raftstore.raft-max-inflight-msgs` [＃11865](https://github.com/tikv/tikv/issues/11865)動的変更をサポート
    -   動的プルーニングモード[＃11888](https://github.com/tikv/tikv/issues/11888)を有効にするには`EXTRA_PHYSICAL_TABLE_ID_COL_ID`サポート
    -   バケット[＃11759](https://github.com/tikv/tikv/issues/11759)での計算をサポート
    -   RawKV API V2のキーを`user-key` + `memcomparable-padding` + `timestamp` [＃11965](https://github.com/tikv/tikv/issues/11965)としてエンコードします。
    -   RawKV API V2の値を`user-value` + `ttl` + `ValueMeta`としてエンコードし、 `delete` `ValueMeta` [＃11965](https://github.com/tikv/tikv/issues/11965)としてエンコードする
    -   `raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)動的変更をサポート
    -   Grafana [＃12014](https://github.com/tikv/tikv/issues/12014)でマルチ k8 の監視をサポート
    -   レイテンシージッターを減らすためにリーダーシップをCDCオブザーバーに移譲する[＃12111](https://github.com/tikv/tikv/issues/12111)
    -   `raftstore.apply_max_batch_size`と`raftstore.store_max_batch_size`動的変更をサポート[＃11982](https://github.com/tikv/tikv/issues/11982)
    -   RawKV V2は`raw_get`または`raw_scan`リクエストを受信すると最新バージョンを返します[＃11965](https://github.com/tikv/tikv/issues/11965)
    -   RCCheckTS 一貫性読み取り[＃12097](https://github.com/tikv/tikv/issues/12097)サポート
    -   `storage.scheduler-worker-pool-size` (スケジューラプールのスレッド数) [＃12067](https://github.com/tikv/tikv/issues/12067)の動的変更をサポート
    -   グローバルフォアグラウンドフローコントローラを使用してCPUと帯域幅の使用を制御し、TiKV [＃11855](https://github.com/tikv/tikv/issues/11855)のパフォーマンス安定性を向上させます。
    -   `readpool.unified.max-thread-count` (UnifyReadPool のスレッド数) [＃11781](https://github.com/tikv/tikv/issues/11781)の動的変更をサポート
    -   TiKV内部パイプラインを使用してRocksDBパイプラインを置き換え、 `rocksdb.enable-multibatch-write`パラメータ[＃12059](https://github.com/tikv/tikv/issues/12059)を廃止します。

-   PD

    -   リーダーを退去させる際に、転送に最も速いオブジェクトを自動的に選択する機能をサポートし、退去プロセスの高速化に貢献します[＃4229](https://github.com/tikv/pd/issues/4229)
    -   リージョンが利用できなくなった場合に、2レプリカRaftグループから投票者を削除することを禁止する[＃4564](https://github.com/tikv/pd/issues/4564)
    -   バランスリーダー[＃4652](https://github.com/tikv/pd/issues/4652)のスケジュールを高速化

-   TiFlash

    -   TiFlashファイルの論理分割を禁止し (デフォルト値の`profiles.default.dt_enable_logical_split`を`false`に調整します。詳細については[ユーザードキュメント](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)を参照してください)、 TiFlash列storageのスペース使用効率を改善して、 TiFlashに同期されたテーブルのスペース占有が TiKV のテーブルのスペース占有と同等になるようにします。
    -   以前のクラスタ管理モジュールを TiDB に統合することで、 TiFlashのクラスタ管理とレプリカ複製メカニズムを最適化し、小さなテーブルのレプリカ作成を高速化します[＃29924](https://github.com/pingcap/tidb/issues/29924)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップデータの復元速度を向上。シミュレーションテストでは、 BR が15 ノード (各ノードに 16 個の CPU コア) の TiKV クラスターに 16 TB のデータを復元すると、スループットは 2.66 GiB/s に達します[＃27036](https://github.com/pingcap/tidb/issues/27036)

        -   配置ルールのインポートとエクスポートをサポートします。データのインポート時に配置ルールを無視するかどうかを制御する`--with-tidb-placement-mode`パラメータを追加します[＃32290](https://github.com/pingcap/tidb/issues/32290)

    -   ティCDC

        -   Grafana [＃4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   サポート配置ルール[＃4846](https://github.com/pingcap/tiflow/issues/4846)
        -   HTTP API処理の同期[＃1710](https://github.com/pingcap/tiflow/issues/1710)
        -   チェンジフィード[＃3329](https://github.com/pingcap/tiflow/issues/3329)を再開するための指数バックオフ メカニズムを追加します。
        -   MySQL [＃3589](https://github.com/pingcap/tiflow/issues/3589)でのデッドロックを減らすために、MySQL シンクのデフォルトの分離レベルを読み取りコミットに設定します。
        -   作成時に変更フィードパラメータを検証し、エラーメッセージを改善する[＃1716](https://github.com/pingcap/tiflow/issues/1716) [＃1718](https://github.com/pingcap/tiflow/issues/1718) [＃1719](https://github.com/pingcap/tiflow/issues/1719) [＃4472](https://github.com/pingcap/tiflow/issues/4472)
        -   Kafka プロデューサーの設定パラメータを公開して、TiCDC [＃4385](https://github.com/pingcap/tiflow/issues/4385)で設定できるようにします。

    -   TiDB データ移行 (DM)

        -   上流のテーブルスキーマが不整合で楽観的モードの場合のタスクの開始をサポート[＃3629](https://github.com/pingcap/tiflow/issues/3629) [＃3708](https://github.com/pingcap/tiflow/issues/3708) [＃3786](https://github.com/pingcap/tiflow/issues/3786)
        -   `stopped`状態[＃4484](https://github.com/pingcap/tiflow/issues/4484)でのタスク作成をサポート
        -   Syncer が`/tmp`ではなく DM ワーカーの作業ディレクトリを使用して内部ファイルを書き込み、タスクが停止した後にディレクトリを消去するのをサポートします[＃4107](https://github.com/pingcap/tiflow/issues/4107)
        -   事前チェックが改善されました。重要なチェックがスキップされなくなりました[＃3608](https://github.com/pingcap/tiflow/issues/3608)

    -   TiDB Lightning

        -   再試行可能なエラータイプを追加する[＃31376](https://github.com/pingcap/tidb/issues/31376)
        -   base64形式のパスワード文字列[＃31194](https://github.com/pingcap/tidb/issues/31194)をサポートする
        -   エラーコードとエラー出力を標準化する[＃32239](https://github.com/pingcap/tidb/issues/32239)

## バグの修正 {#bug-fixes}

-   ティビ

    -   `SCHEDULE = majority_in_primary` `PrimaryRegion`同じ値の場合に`Regions`が配置ルールを使用してテーブルを作成できないバグを修正[＃31271](https://github.com/pingcap/tidb/issues/31271)
    -   インデックスルックアップ結合[＃30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときに発生する`invalid transaction`エラーを修正
    -   2つ以上の権限が付与されている場合に誤った結果`show grants`返されるバグを修正しました[＃30855](https://github.com/pingcap/tidb/issues/30855)
    -   `INSERT INTO t1 SET timestamp_col = DEFAULT`デフォルトで`CURRENT_TIMESTAMP` [＃29926](https://github.com/pingcap/tidb/issues/29926)に設定されているフィールドのタイムスタンプをゼロタイムスタンプに設定するバグを修正しました。
    -   文字列型[＃31721](https://github.com/pingcap/tidb/issues/31721)の最大値と最小の非 null 値のエンコードを回避することで、結果の読み取り時に報告されるエラーを修正しました。
    -   データがエスケープ文字[＃31589](https://github.com/pingcap/tidb/issues/31589)で壊れている場合のロード データpanicを修正
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を返す問題を修正[＃31789](https://github.com/pingcap/tidb/issues/31789)
    -   date_add および date_sub関数が誤ったデータ型を返す可能性があるバグを修正[＃31809](https://github.com/pingcap/tidb/issues/31809)
    -   挿入ステートメントを使用して仮想的に生成された列にデータを挿入するときに発生する可能性のあるpanicを修正[＃31735](https://github.com/pingcap/tidb/issues/31735)
    -   作成されたリストパーティション[＃31784](https://github.com/pingcap/tidb/issues/31784)に重複した列が存在する場合にエラーが報告されないバグを修正
    -   `select for update union select`誤ったスナップショットを使用した場合に返される誤った結果を修正[＃31530](https://github.com/pingcap/tidb/issues/31530)
    -   復元操作が完了した後にリージョンが不均等に分散される可能性がある問題を修正[＃31034](https://github.com/pingcap/tidb/issues/31034)
    -   `json`型[＃31541](https://github.com/pingcap/tidb/issues/31541)のCOERCIBILITYが間違っているバグを修正
    -   この型が組み込み関数[＃31320](https://github.com/pingcap/tidb/issues/31320)を使用して処理されるときに、 `json`型の誤った照合順序を修正しました。
    -   TiFlashレプリカの数が0に設定されている場合にPDルールが削除されないバグを修正[＃32190](https://github.com/pingcap/tidb/issues/32190)
    -   `alter column set default`テーブルスキーマ[＃31074](https://github.com/pingcap/tidb/issues/31074)を誤って更新する問題を修正
    -   TiDBの`date_format`が`'\n'`をMySQLと互換性のない方法で処理する問題を修正[＃32232](https://github.com/pingcap/tidb/issues/32232)
    -   結合[＃31629](https://github.com/pingcap/tidb/issues/31629)を使用してパーティションテーブルを更新するときにエラーが発生する可能性があるバグを修正しました
    -   列挙値[＃32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正
    -   `upper()`と`lower()`関数で起こりpanicを修正[＃32488](https://github.com/pingcap/tidb/issues/32488)
    -   他のタイプの列をタイムスタンプタイプの列に変更するときに発生するタイムゾーンの問題を修正[＃29585](https://github.com/pingcap/tidb/issues/29585)
    -   ChunkRPC [＃31981](https://github.com/pingcap/tidb/issues/31981) [＃30880](https://github.com/pingcap/tidb/issues/30880)を使用してデータをエクスポートする際の TiDB OOM を修正
    -   動的パーティションプルーニングモード[＃32516](https://github.com/pingcap/tidb/issues/32516)でサブSELECT LIMITが期待どおりに動作しないバグを修正
    -   `INFORMATION_SCHEMA.COLUMNS`表[＃32655](https://github.com/pingcap/tidb/issues/32655)のビットデフォルト値の形式が間違っているか、一貫性がない問題を修正
    -   サーバーの再起動後にパーティションテーブルの一覧表示でパーティションテーブルの整理が機能しない可能性があるバグを修正[＃32416](https://github.com/pingcap/tidb/issues/32416)
    -   `SET timestamp`の実行後に`add column`間違ったデフォルトのタイムスタンプを使用する可能性があるバグを修正[＃31968](https://github.com/pingcap/tidb/issues/31968)
    -   MySQL 5.5 または 5.6 クライアントから TiDB パスワードなしアカウントへの接続が失敗する可能性があるバグを修正[＃32334](https://github.com/pingcap/tidb/issues/32334)
    -   トランザクション[＃29851](https://github.com/pingcap/tidb/issues/29851)で動的モードでパーティション テーブルを読み取るときに誤った結果が発生する問題を修正
    -   TiDBが重複したタスクをTiFlash [＃32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   `timdiff`関数の入力にミリ秒が含まれている場合に返される誤った結果を修正[＃31680](https://github.com/pingcap/tidb/issues/31680)
    -   パーティションを明示的に読み取り、IndexJoin プラン[＃32007](https://github.com/pingcap/tidb/issues/32007)を使用した場合に誤った結果が発生する問題を修正しました。
    -   列タイプを同時に変更すると列名の変更が失敗するバグを修正[＃31075](https://github.com/pingcap/tidb/issues/31075)
    -   TiFlashプランの純コストを計算する式が TiKV プランと一致しないバグを修正[#30103](https://github.com/pingcap/tidb/issues/30103)
    -   `KILL TIDB`アイドル接続時にすぐに効果を発揮できないバグを修正[＃24031](https://github.com/pingcap/tidb/issues/24031)
    -   生成された列を持つテーブルをクエリするときに誤った結果が発生する可能性がある問題を修正[＃33038](https://github.com/pingcap/tidb/issues/33038)
    -   `left join` [＃31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除した場合の誤った結果を修正
    -   オーバーフロー[＃31868](https://github.com/pingcap/tidb/issues/31868)の場合に`SUBTIME`関数が誤った結果を返すバグを修正
    -   集計クエリに条件`having` [＃33166](https://github.com/pingcap/tidb/issues/33166)含まれている場合に演算子`selection`をプッシュダウンできないバグを修正しました。
    -   クエリがエラーを報告したときに CTE がブロックされる可能性があるバグを修正[＃31302](https://github.com/pingcap/tidb/issues/31302)
    -   非厳密モードでテーブルを作成するときに、varbinary または varchar 列の長さが長すぎるとエラーが発生する可能性があるバグを修正しました[＃30328](https://github.com/pingcap/tidb/issues/30328)
    -   フォロワーが指定されていない場合の`information_schema.placement_policies`のフォロワー数の誤りを修正[＃31702](https://github.com/pingcap/tidb/issues/31702)
    -   TiDB でインデックス作成時に列プレフィックス長を 0 に指定できる問題を修正[＃31972](https://github.com/pingcap/tidb/issues/31972)
    -   TiDBがスペースで終わるパーティション名を許可する問題を修正[＃31535](https://github.com/pingcap/tidb/issues/31535)
    -   `RENAME TABLE`文[＃29893](https://github.com/pingcap/tidb/issues/29893)のエラーメッセージを修正する

-   ティクヴ

    -   ピアステータスが`Applying` [＃11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショットファイルを削除すると発生するpanic問題を修正しました。
    -   フロー制御が有効で、 `level0_slowdown_trigger`明示的に設定されている場合に QPS が低下する問題を修正[＃11424](https://github.com/tikv/tikv/issues/11424)
    -   ピアを破棄するとレイテンシーが大きくなる可能性がある問題を修正[＃10210](https://github.com/tikv/tikv/issues/10210)
    -   GCワーカーがビジー状態のときにTiKVがデータの範囲を削除できない（つまり内部コマンド`unsafe_destroy_range`が実行される）バグを修正[＃11903](https://github.com/tikv/tikv/issues/11903)
    -   `StoreMeta`のデータが誤って削除されたときに TiKV がパニックを起こすバグを修正[＃11852](https://github.com/tikv/tikv/issues/11852)
    -   ARM プラットフォームでプロファイリングを実行するときに TiKV がパニックになるバグを修正[＃10658](https://github.com/tikv/tikv/issues/10658)
    -   TiKV が 2 年以上実行されている場合にpanicが発生する可能性があるバグを修正[＃11940](https://github.com/tikv/tikv/issues/11940)
    -   SSE命令セット[＃12034](https://github.com/tikv/tikv/issues/12034)欠落により発生するARM64アーキテクチャでのコンパイル問題を修正
    -   初期化されていないレプリカを削除すると古いレプリカが再作成される可能性がある問題を修正[＃10533](https://github.com/tikv/tikv/issues/10533)
    -   古いメッセージにより TiKV がpanicを起こすバグを修正[＃12023](https://github.com/tikv/tikv/issues/12023)
    -   TsSet 変換で未定義の動作 (UB) が発生する可能性がある問題を修正[＃12070](https://github.com/tikv/tikv/issues/12070)
    -   レプリカ読み取りが線形化可能性[＃12109](https://github.com/tikv/tikv/issues/12109)に違反する可能性があるバグを修正
    -   Ubuntu 18.04 [＃9765](https://github.com/tikv/tikv/issues/9765)でTiKVがプロファイリングを実行するときに発生する潜在的なpanic問題を修正
    -   tikv-ctl が間違った文字列一致のために誤った結果を返す問題を修正[＃12329](https://github.com/tikv/tikv/issues/12329)
    -   メモリメトリックのオーバーフローによって発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正しました[＃12160](https://github.com/tikv/tikv/issues/12160)
    -   TiKV [＃12231](https://github.com/tikv/tikv/issues/12231)を終了するときに誤って TiKV パニックを報告する潜在的な問題を修正しました。

-   PD

    -   PDがジョイントコンセンサス[＃4362](https://github.com/tikv/pd/issues/4362)の意味のないステップを含む演算子を生成する問題を修正
    -   PDクライアント[＃4549](https://github.com/tikv/pd/issues/4549)を閉じるときにTSO取り消しプロセスが停止する可能性があるバグを修正
    -   リージョンスキャッタラーのスケジューリングで一部のピアが失われる問題を修正[＃4565](https://github.com/tikv/pd/issues/4565)
    -   `dr-autosync`の`Duration`フィールドが動的に構成できない問題を修正[＃4651](https://github.com/tikv/pd/issues/4651)

-   TiFlash

    -   メモリ制限が有効になっているときに発生するTiFlashpanicの問題を修正[＃3902](https://github.com/pingcap/tiflash/issues/3902)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正[＃4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `Snapshot`複数の DDL 操作[＃4072](https://github.com/pingcap/tiflash/issues/4072)と同時に適用された場合にTiFlashpanicが発生する可能性がある問題を修正
    -   読み取り負荷が高い状態で列を追加した後に発生する可能性のあるクエリエラーを修正[＃3967](https://github.com/pingcap/tiflash/issues/3967)
    -   負の引数を持つ`SQRT`関数が`Null`ではなく`NaN`を返す問題を修正しました[＃3598](https://github.com/pingcap/tiflash/issues/3598)
    -   `INT`を`DECIMAL`にキャストするとオーバーフロー[＃3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正
    -   複数値式[＃4016](https://github.com/pingcap/tiflash/issues/4016)で`IN`の結果が正しくない問題を修正
    -   日付の形式で`'\n'`無効な区切り文字として認識される問題を修正[＃4036](https://github.com/pingcap/tiflash/issues/4036)
    -   同時実行性の高いシナリオで学習者の読み取りプロセスに時間がかかりすぎる問題を修正[＃3555](https://github.com/pingcap/tiflash/issues/3555)
    -   `DATETIME`を`DECIMAL` [＃4151](https://github.com/pingcap/tiflash/issues/4151)にキャストするときに発生する誤った結果を修正
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   エラスティックスレッドプールを有効にするとメモリリークが発生する可能性があるバグを修正[＃4098](https://github.com/pingcap/tiflash/issues/4098)
    -   ローカルトンネルが有効になっている場合、キャンセルされた MPP クエリによってタスクが永久にハングアップする可能性があるバグを修正[＃4229](https://github.com/pingcap/tiflash/issues/4229)
    -   HashJoin ビルド側の障害により MPP クエリが永久にハングする可能性があるバグを修正[＃4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正[＃4238](https://github.com/pingcap/tiflash/issues/4238)

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作中に回復不可能なエラーが発生するとBR が停止するバグを修正[＃33200](https://github.com/pingcap/tidb/issues/33200)
        -   バックアップ再試行中に暗号化情報が失われた場合に復元操作が失敗するバグを修正[＃32423](https://github.com/pingcap/tidb/issues/32423)

    -   ティCDC

        -   `batch-replace-enable`が無効になっている場合に MySQL シンクが重複した`replace` SQL 文を生成するバグを修正[＃4501](https://github.com/pingcap/tiflow/issues/4501)
        -   PDリーダーが強制終了するとTiCDCノードが異常終了するバグを修正[＃4248](https://github.com/pingcap/tiflow/issues/4248)
        -   一部のMySQLバージョン[＃4504](https://github.com/pingcap/tiflow/issues/4504)のエラー`Unknown system variable 'transaction_isolation'`を修正
        -   `Canal-JSON` `string` [＃4635](https://github.com/pingcap/tiflow/issues/4635)を誤って処理した場合に発生する可能性がある TiCDCpanic問題を修正しました。
        -   一部のケースでシーケンスが誤って複製されるバグを修正[＃4552](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON` nil [＃4736](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性がある TiCDCpanic問題を修正
        -   タイプ`Enum/Set`および`TinyText/MediumText/Text/LongText`の Avro コーデックの誤ったデータ マッピングを修正しました[＃4454](https://github.com/pingcap/tiflow/issues/4454)
        -   Avroが`NOT NULL`列目をNULL可能フィールド[＃4818](https://github.com/pingcap/tiflow/issues/4818)に変換するバグを修正
        -   TiCDC が終了できない問題を修正[＃4699](https://github.com/pingcap/tiflow/issues/4699)

    -   TiDB データ移行 (DM)

        -   ステータス[＃4281](https://github.com/pingcap/tiflow/issues/4281)を照会するときにのみ同期メトリックが更新される問題を修正しました
        -   セーフモードでの更新ステートメントの実行エラーにより、DM ワーカーがpanicになる可能性がある問題を修正しました[＃4317](https://github.com/pingcap/tiflow/issues/4317)
        -   長いvarcharがエラーを報告するバグを修正`Column length too big` [＃4637](https://github.com/pingcap/tiflow/issues/4637)
        -   複数の DM ワーカーが同じアップストリーム[＃3737](https://github.com/pingcap/tiflow/issues/3737)からデータを書き込むことで発生する競合の問題を修正しました。
        -   ログに「チェックポイントに変更はありません。同期フラッシュチェックポイントをスキップしてください」というメッセージが何百も出力され、レプリケーションが非常に遅くなる問題を修正しました[＃4619](https://github.com/pingcap/tiflow/issues/4619)
        -   悲観的モード[＃5002](https://github.com/pingcap/tiflow/issues/5002)でシャードをマージし、アップストリームから増分データを複製する際の DML 損失の問題を修正しました。

    -   TiDB Lightning

        -   一部のインポートタスクにソースファイルが含まれていない場合に、 TiDB Lightning がメタデータスキーマを削除しない可能性があるバグを修正しました[＃28144](https://github.com/pingcap/tidb/issues/28144)
        -   ソースファイルとターゲットクラスタ内のテーブル名が異なる場合に発生するpanicを修正[＃31771](https://github.com/pingcap/tidb/issues/31771)
        -   チェックサムエラー「GC の有効期間がトランザクション期間より短い」を修正[＃32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブル[＃31797](https://github.com/pingcap/tidb/issues/31797)チェックに失敗したときにTiDB Lightning が停止する問題を修正しました

    -   Dumpling

        -   `dumpling --sql $query` [＃30532](https://github.com/pingcap/tidb/issues/30532)実行時に表示される進行状況が正確でない問題を修正
        -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正[＃30534](https://github.com/pingcap/tidb/issues/30534)

    -   TiDBBinlog

        -   大規模なアップストリーム書き込みトランザクションが Kafka [＃1136](https://github.com/pingcap/tidb-binlog/issues/1136)にレプリケートされるときに TiDB Binlog がスキップされる可能性がある問題を修正しました。

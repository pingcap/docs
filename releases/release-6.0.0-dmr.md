---
title: TiDB 6.0.0 Release Notes
---

# TiDB 6.0.0 リリースノート {#tidb-6-0-0-release-notes}

発売日：2022年4月7日

TiDB バージョン: 6.0.0-DMR

> **ノート：**
>
> TiDB 6.0.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.0/)です。 PingCAP では、 [最新の LTS バージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

6.0.0-DMR の主な新機能または改善点は次のとおりです。

-   SQL の配置ルールをサポートして、データ配置のより柔軟な管理を提供します。
-   カーネル レベルでデータとインデックス間の整合性チェックを追加します。これにより、システムの安定性と堅牢性が向上し、リソースのオーバーヘッドは非常に低くなります。
-   Top SQLを提供します。これは、非専門家向けのセルフサービス データベース パフォーマンス モニタリングおよび診断機能です。
-   クラスターのパフォーマンス データを常に収集する継続的なプロファイリングをサポートし、技術者の MTTR を短縮します。
-   ホットスポットの小さなテーブルをメモリにキャッシュします。これにより、アクセスのパフォーマンスが大幅に向上し、スループットが向上し、アクセスのレイテンシーが短縮されます。
-   インメモリの悲観的ロックを最適化します。悲観的ロックによって引き起こされるパフォーマンスのボトルネックの下では、悲観的ロックのメモリ最適化により、レイテンシーを効果的に 10% 削減し、QPS を 10% 向上させることができます。
-   準備済みステートメントを拡張して実行計画を共有することで、CPU リソースの消費を減らし、SQL の実行効率を向上させます。
-   より多くの式のプッシュ ダウンとエラスティック スレッド プールの一般提供 (GA) をサポートすることで、MPP エンジンのコンピューティング パフォーマンスを向上させます。
-   DM WebUIを追加して、多数の移行タスクの管理を容易にします。
-   大規模なクラスターでデータを複製する際の TiCDC の安定性と効率を向上させます。 TiCDC は、100,000 テーブルの同時レプリケートをサポートするようになりました。
-   TiKV ノードの再起動後のリーダー バランシングを加速し、再起動後のビジネス リカバリの速度を向上させます。
-   統計の自動更新のキャンセルをサポートします。これにより、リソースの競合が減少し、SQL パフォーマンスへの影響が制限されます。
-   TiDBクラスタの自動診断サービス「PingCAPクリニック」を提供（テクニカルプレビュー版）。
-   エンタープライズ レベルのデータベース管理プラットフォームである TiDB Enterprise Manager を提供します。

また、TiDB の HTAP ソリューションのコアコンポーネントであるTiFlash <sup>TM は</sup>、このリリースで正式にオープン ソースとなります。詳細については、 [TiFlashリポジトリ](https://github.com/pingcap/tiflash)を参照してください。

## リリース戦略の変更 {#release-strategy-changes}

TiDB v6.0.0 以降、TiDB は 2 種類のリリースを提供します。

-   長期サポート リリース

    長期サポート (LTS) リリースは、約 6 か月ごとにリリースされます。 LTS リリースでは、新しい機能と改善が導入され、リリース ライフサイクル内でパッチ リリースが受け入れられます。たとえば、v6.1.0 は LTS リリースになります。

-   開発マイルストーン リリース

    開発マイルストーン リリース (DMR) は、約 2 か月ごとにリリースされます。 DMR は新機能と改善を導入しますが、パッチ リリースは受け入れません。オンプレミス ユーザーが本番環境で DMR を使用することはお勧めしません。たとえば、v6.0.0-DMR は DMR です。

TiDB v6.0.0 は DMR であり、そのバージョンは 6.0.0-DMR です。

## 新機能 {#new-features}

### SQL {#sql}

-   データの SQL ベースの配置規則

    TiDB はスケーラビリティに優れた分散データベースです。通常、データは複数のサーバーまたは複数のデータ センターに展開されます。したがって、データ スケジューリング管理は、TiDB の最も重要な基本機能の 1 つです。ほとんどの場合、ユーザーはデータのスケジュールと管理の方法を気にする必要はありません。ただし、アプリケーションの複雑さが増すにつれて、分離とアクセスのレイテンシーに起因する展開の変更が TiDB の新たな課題になっています。 v6.0.0 以降、TiDB は SQL インターフェイスに基づいたデータ スケジューリングおよび管理機能を正式に提供しています。レプリカの数、役割の種類、データの配置場所などのディメンションで、柔軟なスケジューリングと管理をサポートします。 TiDB は、マルチサービス共有クラスターおよびクロス AZ 配置でのデータ配置のより柔軟な管理もサポートします。

    [ユーザー文書](/placement-rules-in-sql.md)

-   データベースによるTiFlashレプリカの構築をサポートします。データベース内のすべてのテーブルにTiFlashレプリカを追加するには、単一の SQL ステートメントを使用するだけでよく、運用と保守のコストを大幅に節約できます。

    [ユーザー文書](/tiflash/create-tiflash-replicas.md#create-tiflash-replicas-for-databases)

### トランザクション {#transaction}

-   カーネル レベルでのデータ インデックスの一貫性のチェックを追加します。

    トランザクションの実行時にデータ インデックスの整合性チェックを追加します。これにより、システムの安定性と堅牢性が向上し、リソースのオーバーヘッドが非常に低くなります。 `tidb_enable_mutation_checker`変数と`tidb_txn_assertion_level`変数を使用して、チェックの動作を制御できます。デフォルト設定では、QPS ドロップはほとんどのシナリオで 2% 以内に制御されます。整合性チェックのエラーの説明については、 [ユーザー文書](/troubleshoot-data-inconsistency-errors.md)を参照してください。

### 可観測性 {#observability}

-   Top SQL: 非専門家向けのパフォーマンス診断

    Top SQLは、DBA およびアプリ開発者向けの TiDB ダッシュボードのセルフサービス データベース パフォーマンス監視および診断機能であり、TiDB v6.0 で一般的に利用可能になりました。

    専門家向けの既存の診断機能とは異なり、 Top SQL は非専門家向けに設計されています。相関関係を見つけたり、 Raftスナップショット、RocksDB、MVCC、TSO などの TiDB 内部メカニズムを理解したりするために、何千もの監視チャートを走査する必要はありません。 Top SQLを使用してデータベースの負荷を迅速に分析し、アプリのパフォーマンスを向上させるために必要なのは、基本的なデータベースの知識 (インデックス、ロックの競合、実行計画など) だけです。

    Top SQL はデフォルトでは有効になっていません。有効にすると、 Top SQL は各 TiKV または TiDB ノードのリアルタイムの CPU 負荷を提供します。したがって、高い CPU 負荷を消費している SQL ステートメントを一目で特定し、データベースのホットスポットや急激な負荷の増加などの問題をすばやく分析できます。たとえば、 Top SQL を使用して、単一の TiKV ノードの 90% の CPU を消費する異常なクエリを特定して診断できます。

    [ユーザー文書](/dashboard/top-sql.md)

-   継続的なプロファイリングをサポート

    TiDB ダッシュボードには継続的プロファイリング機能が導入されており、TiDB v6.0 で一般的に利用できるようになりました。デフォルトでは、継続的なプロファイリングは有効になっていません。有効にすると、個々の TiDB、TiKV、および PD インスタンスのパフォーマンス データが常に収集され、オーバーヘッドは無視できます。履歴パフォーマンス データを使用すると、技術専門家は、問題の再現が困難な場合でも、高メモリ消費などの問題の根本原因を遡って特定できます。このようにして、回復までの平均時間 (MTTR) を短縮できます。

    [ユーザー文書](/dashboard/continuous-profiling.md)

### パフォーマンス {#performance}

-   ホットスポットの小さなテーブルをキャッシュする

    ホットスポットの小さなテーブルにアクセスするシナリオのユーザー アプリケーションの場合、TiDB はホットスポット テーブルをメモリに明示的にキャッシュすることをサポートしています。これにより、アクセス パフォーマンスが大幅に向上し、スループットが向上し、アクセスレイテンシーが短縮されます。このソリューションは、サードパーティのキャッシュ ミドルウェアの導入を効果的に回避し、アーキテクチャの複雑さを軽減し、運用と保守のコストを削減できます。このソリューションは、構成テーブルや為替レート テーブルなど、小さなテーブルが頻繁にアクセスされるがほとんど更新されないシナリオに適しています。

    [ユーザー文書](/cached-tables.md) 、 [#25293](https://github.com/pingcap/tidb/issues/25293)

-   インメモリ悲観的ロック

    TiDB v6.0.0 以降、メモリ内悲観的ロックはデフォルトで有効になっています。この機能を有効にすると、悲観的トランザクション ロックはメモリで管理されます。これにより、悲観的ロックの永続化とロック情報のRaftレプリケーションが回避され、悲観的トランザクション ロックを管理するオーバーヘッドが大幅に削減されます。悲観的ロックによって引き起こされるパフォーマンスのボトルネックの下では、悲観的ロックのメモリ最適化により、レイテンシーを効果的に 10% 削減し、QPS を 10% 向上させることができます。

    [ユーザー文書](/pessimistic-transaction.md#in-memory-pessimistic-lock) 、 [#11452](https://github.com/tikv/tikv/issues/11452)

-   Read Committed 分離レベルで TSO を取得するための最適化

    クエリのレイテンシーを短縮するために、読み取りと書き込みの競合がまれな場合、TiDB は[読み取りコミット分離レベル](/transaction-isolation-levels.md#read-committed-isolation-level)に`tidb_rc_read_check_ts`システム変数を追加して不要な TSO を減らします。この変数はデフォルトで無効になっています。変数が有効な場合、この最適化により TSO の重複が回避され、読み取りと書き込みの競合がないシナリオでのレイテンシーが短縮されます。ただし、読み取りと書き込みの競合が頻繁に発生するシナリオでは、この変数を有効にすると、パフォーマンスが低下する可能性があります。

    [ユーザー文書](/transaction-isolation-levels.md#read-committed-isolation-level) 、 [#33159](https://github.com/pingcap/tidb/issues/33159)

-   準備済みステートメントを強化して実行計画を共有する

    SQL 実行計画を再利用すると、SQL ステートメントの解析時間を効果的に短縮し、CPU リソースの消費を減らし、SQL 実行効率を向上させることができます。 SQL チューニングの重要な方法の 1 つは、SQL 実行計画を効果的に再利用することです。 TiDB は、準備済みステートメントとの実行計画の共有をサポートしています。ただし、準備されたステートメントが閉じられると、TiDB は対応するプラン キャッシュを自動的にクリアします。その後、TiDB は繰り返される SQL ステートメントを不必要に解析し、実行効率に影響を与える可能性があります。 v6.0.0 以降、TiDB は`tidb_ignore_prepared_cache_close_stmt`パラメータ (デフォルトでは無効) を介して`COM_STMT_CLOSE`コマンドを無視するかどうかの制御をサポートしています。このパラメーターを有効にすると、TiDB は準備済みステートメントを閉じるコマンドを無視し、実行プランをキャッシュに保持するため、実行プランの再利用率が向上します。

    [ユーザー文書](/sql-prepared-plan-cache.md#ignore-the-com_stmt_close-command-and-the-deallocate-prepare-statement) 、 [#31056](https://github.com/pingcap/tidb/issues/31056)

-   クエリのプッシュダウンを改善する

    コンピューティングをstorageから分離するネイティブアーキテクチャにより、TiDB は演算子を押し下げることで無効なデータを除外することをサポートします。これにより、TiDB と TiKV 間のデータ転送が大幅に削減され、クエリの効率が向上します。 v6.0.0 では、TiDB はより多くの式と`BIT`データ型を TiKV にプッシュすることをサポートし、式とデータ型を計算する際のクエリ効率を向上させます。

    [ユーザー文書](/functions-and-operators/expressions-pushed-down.md) 、 [#30738](https://github.com/pingcap/tidb/issues/30738)

-   ホットスポット インデックスの最適化

    単調に増加するデータをバッチでセカンダリ インデックスに書き込むと、インデックス ホットスポットが発生し、全体的な書き込みスループットに影響します。 v6.0.0 以降、TiDB は書き込みパフォーマンスを向上させるために`tidb_shard`関数を使用してインデックス ホットスポットを分散することをサポートしています。現在、 `tidb_shard`一意のセカンダリ インデックスでのみ有効です。このアプリケーション フレンドリーなソリューションでは、元のクエリ条件を変更する必要はありません。このソリューションは、高い書き込みスループット、ポイント クエリ、およびバッチ ポイント クエリのシナリオで使用できます。アプリケーションで範囲クエリによって分散されたデータを使用すると、パフォーマンスが低下する可能性があることに注意してください。したがって、このような場合は、この機能を確認せずに使用しないでください。

    [ユーザー文書](/functions-and-operators/tidb-functions.md#tidb_shard) 、 [#31040](https://github.com/pingcap/tidb/issues/31040)

-   TiFlash MPP エンジンで分割テーブルの動的プルーニング モードをサポート (実験的)

    このモードでは、TiDB はTiFlashの MPP エンジンを使用して、分割されたテーブルのデータを読み取って計算できます。これにより、分割されたテーブルのクエリ パフォーマンスが大幅に向上します。

    [ユーザー文書](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

-   MPP エンジンのコンピューティング パフォーマンスを向上させる

    -   より多くの関数と演算子を MPP エンジンにプッシュ ダウンするサポート

        -   論理関数: `IS` , `IS NOT`
        -   文字列関数: `REGEXP()` 、 `NOT REGEXP()`
        -   数学関数: `GREATEST(int/real)` , `LEAST(int/real)`
        -   日付関数: `DAYNAME()` 、 `DAYOFMONTH()` 、 `DAYOFWEEK()` 、 `DAYOFYEAR()` 、 `LAST_DAY()` 、 `MONTHNAME()`
        -   演算子: Anti Left Outer Semi Join、Left Outer Semi Join

        [ユーザー文書](/tiflash/tiflash-supported-pushdown-calculations.md)

    -   エラスティック スレッド プール (デフォルトで有効) が GA になります。この機能は、CPU 使用率を改善することを目的としています。

        [ユーザー文書](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

### 安定性 {#stability}

-   実行計画のベースライン取得を強化

    テーブル名、頻度、ユーザー名などのディメンションを含むブロックリストを追加して、実行計画のベースライン キャプチャの使いやすさを向上させます。キャッシュ バインディングのメモリ管理を最適化する新しいアルゴリズムを導入します。ベースライン キャプチャを有効にすると、システムはほとんどの OLTP クエリのバインディングを自動的に作成します。バインドされたステートメントの実行計画は固定されているため、実行計画の変更によるパフォーマンスの問題が回避されます。ベースラインのキャプチャは、メジャー バージョンのアップグレードやクラスターの移行などのシナリオに適用でき、実行計画の回帰によって引き起こされるパフォーマンスの問題を軽減するのに役立ちます。

    [ユーザー文書](/sql-plan-management.md#baseline-capturing) 、 [#32466](https://github.com/pingcap/tidb/issues/32466)

-   TiKV クォータ リミッターのサポート (実験的)

    TiKV で展開されたマシンのリソースが限られており、フォアグラウンドが過度に大量のリクエストによって負荷がかかる場合、バックグラウンドの CPU リソースがフォアグラウンドによって占有され、TiKV のパフォーマンスが不安定になります。 TiDB v6.0.0 では、クォータ関連の構成項目を使用して、CPU や読み取り/書き込み帯域幅など、フォアグラウンドで使用されるリソースを制限できます。これにより、長期にわたる負荷の高いワークロード下でのクラスターの安定性が大幅に向上します。

    [ユーザー文書](/tikv-configuration-file.md#quota) 、 [#12131](https://github.com/tikv/tikv/issues/12131)

-   TiFlashで zstd 圧縮アルゴリズムをサポート

    TiFlash には`profiles.default.dt_compression_method`と`profiles.default.dt_compression_level`の 2 つのパラメーターが導入されており、ユーザーはパフォーマンスと容量のバランスに基づいて最適な圧縮アルゴリズムを選択できます。

    [ユーザー文書](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)

-   デフォルトですべての I/O チェック (チェックサム) を有効にする

    この機能は v5.4.0 で実験的に導入されました。ユーザーのビジネスに明らかな影響を与えることなく、データの正確性とセキュリティを強化します。

    警告: データ形式の新しいバージョンを v5.4.0 より前のバージョンにダウングレードすることはできません。このようなダウングレード中は、 TiFlashレプリカを削除し、ダウングレード後にデータを複製する必要があります。または、 [dttool 移行](/tiflash/tiflash-command-line-flags.md#dttool-migrate)を参照してダウングレードを実行できます。

    [ユーザー文書](/tiflash/tiflash-data-validation.md)

-   スレッドの使用率を改善する

    TiFlash、非同期 gRPC および Min-TSO スケジューリング メカニズムが導入されています。このようなメカニズムにより、スレッドがより効率的に使用され、過剰なスレッドによるシステム クラッシュが回避されます。

    [ユーザー文書](/tiflash/monitor-tiflash.md#coprocessor)

### データ移行 {#data-migration}

#### TiDB データ移行 (DM) {#tidb-data-migration-dm}

-   WebUI を追加 (実験的)

    WebUI を使用すると、多数の移行タスクを簡単に管理できます。 WebUI では、次のことができます。

    -   ダッシュボードで移行タスクをビュー
    -   移行タスクの管理
    -   アップストリーム設定を構成する
    -   クエリのレプリケーション ステータス
    -   マスターとワーカーの情報をビュー

    WebUI はまだ実験的、まだ開発中です。そのため、試用のみをお勧めします。 WebUI と dmctl を使用して同じタスクを操作すると、問題が発生する可能性があるという既知の問題があります。この問題は、以降のバージョンで解決される予定です。

    [ユーザー文書](/dm/dm-webui-guide.md)

-   エラー処理メカニズムを追加する

    移行タスクを中断する問題に対処するために、より多くのコマンドが導入されています。例えば：

    -   スキーマ エラーが発生した場合は、スキーマ ファイルを個別に編集する代わりに、 `binlog-schema update`コマンドの`--from-source/--from-target`パラメータを使用してスキーマ ファイルを更新できます。
    -   binlog の位置を指定して、DDL ステートメントを挿入、置換、スキップ、または元に戻すことができます。

    [ユーザー文書](/dm/dm-manage-schema.md)

-   Amazon S3 へのフル データstorageをサポート

    DM がすべてまたは完全なデータ移行タスクを実行する場合、アップストリームからの完全なデータを格納するために十分なハード ディスク領域が必要です。 EBS と比較して、Amazon S3 には低コストでほぼ無限のstorageがあります。現在、DM は Amazon S3 をダンプ ディレクトリとして設定することをサポートしています。つまり、すべてまたは完全なデータ移行タスクを実行するときに、S3 を使用して完全なデータを保存できます。

    [ユーザー文書](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)

-   指定した時間からの移行タスクの開始をサポート

    移行タスクに新しいパラメータ`--start-time`が追加されました。 「2021-10-21 00:01:00」または「2021-10-21T00:01:00」の形式で時間を定義できます。

    この機能は、シャード mysql インスタンスから増分データを移行およびマージするシナリオで特に役立ちます。具体的には、増分移行タスクでソースごとにbinlogの開始点を設定する必要はありません。代わりに、 `safe-mode`の`--start-time`パラメーターを使用して、増分移行タスクをすばやく作成できます。

    [ユーザー文書](/dm/dm-create-task.md#flags-description)

#### TiDB Lightning {#tidb-lightning}

-   許容エラーの最大数の構成をサポート

    設定項目`lightning.max-error`を追加しました。デフォルト値は 0 です。値が 0 より大きい場合、最大エラー機能が有効になります。エンコード中に行でエラーが発生した場合、この行を含むレコードがターゲット TiDB の`lightning_task_info.type_error_v1`に追加され、この行は無視されます。エラーのある行がしきい値を超えると、 TiDB Lightning はすぐに終了します。

    `lightning.max-error`構成に一致する`lightning.task-info-schema-name`構成アイテムは、データ保存エラーを報告するデータベースの名前を記録します。

    この機能は、すべての種類のエラーをカバーしているわけではありません。たとえば、構文エラーは該当しません。

    [ユーザー文書](/tidb-lightning/tidb-lightning-error-resolution.md#type-error)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   100,000 テーブルの同時複製をサポート

    データ処理フローを最適化することで、TiCDC は各テーブルの増分データ処理のリソース消費を削減します。これにより、大規模なクラスターでデータを複製する際の複製の安定性と効率が大幅に向上します。内部テストの結果は、TiCDC が 100,000 テーブルの同時複製を安定してサポートできることを示しています。

### 展開とメンテナンス {#deployment-and-maintenance}

-   デフォルトで新しい照合順序規則を有効にする

    v4.0 以降、TiDB は、大文字と小文字を区別しない、アクセントを区別しない、およびパディング ルールで MySQL と同じように動作する新しい照合順序ルールをサポートしています。新しい照合順序規則は、デフォルトで無効になっている`new_collations_enabled_on_first_bootstrap`パラメーターによって制御されます。 v6.0 以降、TiDB はデフォルトで新しい照合順序規則を有効にします。この構成は、TiDB クラスターの初期化時にのみ有効になることに注意してください。

    [ユーザー文書](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)

-   TiKV ノードの再起動後にリーダーのバランシングを加速する

    TiKV ノードの再起動後、ロード バランスのために、不均等に分散されたリーダーを再分散する必要があります。大規模なクラスターでは、リーダーのバランシング時間はリージョン数と正の相関があります。たとえば、100K リージョンのリーダー バランシングには 20 ～ 30 分かかることがあります。これは、負荷が不均等であるため、パフォーマンスの問題や安定性のリスクが発生しやすくなります。 TiDB v6.0.0 は、バランシングの同時実行を制御するパラメーターを提供し、デフォルト値を元の 4 倍に拡大します。これにより、リーダーのリバランス時間が大幅に短縮され、TiKV ノードの再起動後のビジネスの回復が加速されます。

    [ユーザー文書](/pd-control.md#scheduler-config-balance-leader-scheduler) 、 [#4610](https://github.com/tikv/pd/issues/4610)

-   統計の自動更新のキャンセルをサポート

    統計は、SQL パフォーマンスに影響を与える最も重要な基本データの 1 つです。統計の完全性と適時性を確保するために、TiDB はバックグラウンドで定期的にオブジェクトの統計を自動的に更新します。ただし、統計の自動更新によってリソースの競合が発生し、SQL のパフォーマンスに影響を与える可能性があります。この問題に対処するために、v6.0 以降の統計の自動更新を手動でキャンセルできます。

    [ユーザー文書](/statistics.md#automatic-update)

-   PingCAPクリニック診断サービス（テクニカルプレビュー版）

    PingCAPクリニック は、 TiDB クラスターの診断サービスです。このサービスは、クラスターの問題をリモートでトラブルシューティングするのに役立ち、ローカルでクラスターの状態をすばやく確認できます。 PingCAPクリニックを使用すると、ライフ サイクル全体で TiDB クラスターの安定した運用を確保し、潜在的な問題を予測し、問題の可能性を減らし、クラスターの問題を迅速にトラブルシューティングできます。

    クラスターの問題をトラブルシューティングするためのリモート アシスタンスについて PingCAP テクニカル サポートに連絡する場合、 PingCAPクリニックサービスを使用して診断データを収集およびアップロードし、トラブルシューティングの効率を向上させることができます。

    [ユーザー文書](/clinic/clinic-introduction.md)

-   エンタープライズレベルのデータベース管理プラットフォーム、TiDB Enterprise Manager

    TiDB Enterprise Manager (TiEM) は、TiDB データベースに基づくエンタープライズ レベルのデータベース管理プラットフォームであり、ユーザーがオンプレミスまたはパブリック クラウド環境で TiDB クラスターを管理できるようにすることを目的としています。

    TiEM は、TiDB クラスターの完全なライフサイクルのビジュアル管理を提供するだけでなく、パラメーター管理、バージョン アップグレード、クラスター クローン、アクティブ/スタンバイ クラスターの切り替え、データのインポートとエクスポート、データ レプリケーション、およびデータのバックアップと復元サービスなどのワンストップ サービスも提供します。 TiEM は、TiDB での DevOps の効率を向上させ、企業の DevOps コストを削減できます。

    現在、TiEM は[TiDB エンタープライズ](https://en.pingcap.com/tidb-enterprise/)エディションのみで提供されています。 TiEM を入手するには、 [TiDB エンタープライズ](https://en.pingcap.com/tidb-enterprise/)ページからお問い合わせください。

-   監視コンポーネントの構成のカスタマイズをサポート

    TiUPを使用して TiDB クラスターをデプロイすると、 TiUP はPrometheus、Grafana、Alertmanager などの監視コンポーネントを自動的にデプロイし、スケールアウト後に新しいノードを監視スコープに自動的に追加します。 `topology.yaml`ファイルに構成項目を追加することで、監視コンポーネントの構成をカスタマイズできます。

    [ユーザー文書](/tiup/customized-montior-in-tiup-environment.md)

## 互換性の変更 {#compatibility-changes}

> **ノート：**
>
> 以前の TiDB バージョンから v6.0.0 にアップグレードする場合、すべての中間バージョンの互換性の変更点を知りたい場合は、該当するバージョンの[リリースノート](/releases/release-notes.md)を確認できます。

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                       | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                            |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `placement_checks`                                                                                                                                                                        | 削除しました | [SQL の配置規則](/placement-rules-in-sql.md)で指定された配置規則を DDL ステートメントが検証するかどうかを制御します。 `tidb_placement_mode`に置き換えられました。                                                                                                                                                                                               |
| `tidb_enable_alter_placement`                                                                                                                                                             | 削除しました | [SQL の配置規則](/placement-rules-in-sql.md)を有効にするかどうかを制御します。                                                                                                                                                                                                                                                      |
| `tidb_mem_quota_hashjoin`<br/>`tidb_mem_quota_indexlookupjoin`<br/>`tidb_mem_quota_indexlookupreader` <br/>`tidb_mem_quota_mergejoin`<br/>`tidb_mem_quota_sort`<br/>`tidb_mem_quota_topn` | 削除しました | v5.0 以降、これらの変数は`tidb_mem_quota_query`に置き換えられ、 [システム変数](/system-variables.md)ドキュメントから削除されました。互換性を確保するために、これらの変数はソース コードに保持されていました。 TiDB 6.0.0 以降、これらの変数もコードから削除されています。                                                                                                                                         |
| [`tidb_enable_mutation_checker`](/system-variables.md#tidb_enable_mutation_checker-new-in-v600)                                                                                           | 新規追加   | ミューテーション チェッカーを有効にするかどうかを制御します。デフォルト値は`ON`です。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、ミューテーション チェッカーはデフォルトで無効になっています。                                                                                                                                                                                          |
| [`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)                                                                         | 新規追加   | Prepared Statement を閉じるコマンドを無視するかどうかを制御します。デフォルト値は`OFF`です。                                                                                                                                                                                                                                                    |
| [`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)                                                                                           | 新規追加   | `binding`を保持するキャッシュのメモリ使用量のしきい値を設定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                                                                                          |
| [`tidb_placement_mode`](/system-variables.md#tidb_placement_mode-new-in-v600)                                                                                                             | 新規追加   | [SQL の配置規則](/placement-rules-in-sql.md)で指定された配置規則を DDL ステートメントが無視するかどうかを制御します。デフォルト値は`strict`です。これは、DDL ステートメントが配置規則を無視しないことを意味します。                                                                                                                                                                           |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                                                         | 新規追加   | <li>トランザクション内の読み取りステートメントのレイテンシーを最適化します。読み取り/書き込みの競合がより深刻な場合、この変数をオンにすると、オーバーヘッドとレイテンシーが追加され、パフォーマンスが低下します。デフォルト値は`off`です。</li><li>この変数はまだ[レプリカ読み取り](/system-variables.md#tidb_replica_read-new-in-v40)と互換性がありません。読み取り要求で`tidb_rc_read_check_ts`オンになっている場合、レプリカ読み取りを使用できない可能性があります。両方の変数を同時にオンにしないでください。</li> |
| [`tidb_sysdate_is_now`](/system-variables.md#tidb_sysdate_is_now-new-in-v600)                                                                                                             | 新規追加   | `SYSDATE`関数を`NOW`関数で置き換えることができるかどうかを制御します。この構成項目は、MySQL オプション[`sysdate-is-now`](https://dev.mysql.com/doc/refman/8.0/en/server-options.html#option_mysqld_sysdate-is-now)と同じ効果があります。デフォルト値は`OFF`です。                                                                                                           |
| [`tidb_table_cache_lease`](/system-variables.md#tidb_table_cache_lease-new-in-v600)                                                                                                       | 新規追加   | [テーブルキャッシュ](/cached-tables.md)のリース時間を秒単位で制御します。デフォルト値は`3`です。                                                                                                                                                                                                                                                  |
| [`tidb_top_sql_max_meta_count`](/system-variables.md#tidb_top_sql_max_meta_count-new-in-v600)                                                                                             | 新規追加   | [Top SQL](/dashboard/top-sql.md)分あたり 1 で収集される SQL ステートメント タイプの最大数を制御します。デフォルト値は`5000`です。                                                                                                                                                                                                                      |
| [`tidb_top_sql_max_time_series_count`](/system-variables.md#tidb_top_sql_max_time_series_count-new-in-v600)                                                                               | 新規追加   | 負荷に最も寄与する SQL ステートメントの数 (つまり、上位 N 個) を 1 分間に[Top SQL](/dashboard/top-sql.md)ずつ記録できるように制御します。デフォルト値は`100`です。                                                                                                                                                                                                   |
| [`tidb_txn_assertion_level`](/system-variables.md#tidb_txn_assertion_level-new-in-v600)                                                                                                   | 新規追加   | アサーション レベルを制御します。アサーションは、データとインデックス間の整合性チェックであり、トランザクション コミット プロセスで書き込まれるキーが存在するかどうかをチェックします。デフォルトでは、チェックはほとんどのチェック項目を有効にしますが、パフォーマンスへの影響はほとんどありません。 v6.0.0 より前のバージョンからアップグレードする既存のクラスターの場合、このチェックはデフォルトで無効になっています。                                                                                           |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                                       | タイプを変更 | 説明                                                                                                                                                                                                                                                                                                            |
| :------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TiDB           | `stmt-summary.enable` <br/> `stmt-summary.enable-internal-query` <br/> `stmt-summary.history-size` <br/> `stmt-summary.max-sql-length` <br/> `stmt-summary.max-stmt-count` <br/> `stmt-summary.refresh-interval` | 削除しました | に関連するコンフィグレーション[ステートメント要約表](/statement-summary-tables.md) ．これらの構成アイテムはすべて削除されます。ステートメント要約テーブルを制御するには、SQL 変数を使用する必要があります。                                                                                                                                                                                      |
| TiDB           | [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)                                                                                             | 修正済み   | 新しい照合順序のサポートを有効にするかどうかを制御します。 v6.0 以降、デフォルト値が`false`から`true`に変更されました。この構成項目は、クラスターが初めて初期化されたときにのみ有効になります。最初のブートストラップの後、この構成項目を使用して新しい照合順序ワークを有効または無効にすることはできません。                                                                                                                                              |
| TiKV           | [`backup.num-threads`](/tikv-configuration-file.md#num-threads-1)                                                                                                                                                | 修正済み   | 値の範囲は`[1, CPU]`に変更されます。                                                                                                                                                                                                                                                                                       |
| TiKV           | [`raftstore.apply-max-batch-size`](/tikv-configuration-file.md#apply-max-batch-size)                                                                                                                             | 修正済み   | 最大値は`10240`に変更されます。                                                                                                                                                                                                                                                                                           |
| TiKV           | [`raftstore.raft-max-size-per-msg`](/tikv-configuration-file.md#raft-max-size-per-msg)                                                                                                                           | 修正済み   | <li>最小値が`0`から`0`より大きい値に変更されました。</li><li>最大値は`3GB`に設定されています。</li><li>単位は`MB`から`KB\|MB\|GB`に変更されます。</li>                                                                                                                                                                                                        |
| TiKV           | [`raftstore.store-max-batch-size`](/tikv-configuration-file.md#store-max-batch-size)                                                                                                                             | 修正済み   | 最大値は`10240`に設定されます。                                                                                                                                                                                                                                                                                           |
| TiKV           | [`readpool.unified.max-thread-count`](/tikv-configuration-file.md#max-thread-count)                                                                                                                              | 修正済み   | 調整範囲が`[min-thread-count, MAX(4, CPU)]`に変更されます。                                                                                                                                                                                                                                                                |
| TiKV           | [`rocksdb.enable-pipelined-write`](/tikv-configuration-file.md#enable-pipelined-write)                                                                                                                           | 修正済み   | デフォルト値が`true`から`false`に変更されました。この構成が有効な場合、以前の Pipelined Write が使用されます。この構成を無効にすると、新しい Pipelined Commit メカニズムが使用されます。                                                                                                                                                                                          |
| TiKV           | [`rocksdb.max-background-flushes`](/tikv-configuration-file.md#max-background-flushes)                                                                                                                           | 修正済み   | <li>CPU コア数が 10 の場合、デフォルト値は`3`です。</li><li> CPU コア数が 8 の場合、デフォルト値は`2`です。</li>                                                                                                                                                                                                                                  |
| TiKV           | [`rocksdb.max-background-jobs`](/tikv-configuration-file.md#max-background-jobs)                                                                                                                                 | 修正済み   | <li>CPU コア数が 10 の場合、デフォルト値は`9`です。</li><li> CPU コア数が 8 の場合、デフォルト値は`7`です。</li>                                                                                                                                                                                                                                  |
| TiFlash        | [`profiles.default.dt_enable_logical_split`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                   | 修正済み   | DeltaTree ストレージ エンジンのセグメントが論理分割を使用するかどうかを決定します。デフォルト値が`true`から`false`に変更されました。                                                                                                                                                                                                                                |
| TiFlash        | [`profiles.default.enable_elastic_threadpool`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                 | 修正済み   | エラスティック スレッド プールを有効にするかどうかを制御します。デフォルト値が`false`から`true`に変更されました。                                                                                                                                                                                                                                              |
| TiFlash        | [`storage.format_version`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                                     | 修正済み   | TiFlashのデータ検証機能を制御します。デフォルト値が`2`から`3`に変更されました。<br/> `format_version`が`3`に設定されている場合、ハードウェア障害による誤った読み取りを回避するために、すべてのTiFlashデータの読み取り操作に対して整合性チェックが実行されます。<br/>新しい形式のバージョンは、v5.4 より前のバージョンにダウングレードできないことに注意してください。                                                                                                |
| TiDB           | [`pessimistic-txn.pessimistic-auto-commit`](/tidb-configuration-file.md#pessimistic-auto-commit-new-in-v600)                                                                                                     | 新規追加   | 悲観的トランザクション モードがグローバルに有効になっている場合 ( `tidb_txn_mode='pessimistic'` )、自動コミット トランザクションが使用するトランザクション モードを決定します。                                                                                                                                                                                                    |
| TiKV           | [`pessimistic-txn.in-memory`](/tikv-configuration-file.md#in-memory-new-in-v600)                                                                                                                                 | 新規追加   | インメモリ悲観的ロックを有効にするかどうかを制御します。この機能を有効にすると、悲観的トランザクションは、悲観的的ロックをディスクに書き込んだり、他のレプリカに複製したりする代わりに、悲観的ロックを可能な限り TiKVメモリに格納します。これにより、悲観的トランザクションのパフォーマンスが向上します。ただし、悲観的ロックが失われる可能性は低いため、悲観的トランザクションがコミットに失敗する可能性があります。デフォルト値は`true`です。                                                                                 |
| TiKV           | [`quota`](/tikv-configuration-file.md#quota)                                                                                                                                                                     | 新規追加   | フロントエンド リクエストが占有するリソースを制限する Quota Limiter に関連する構成項目を追加します。 Quota Limiter は実験的機能であり、デフォルトでは無効になっています。新しいクォータ関連の構成アイテムは`foreground-cpu-time` 、 `foreground-write-bandwidth` 、 `foreground-read-bandwidth` 、および`max-delay-duration`です。                                                                           |
| TiFlash        | [`profiles.default.dt_compression_method`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                     | 新規追加   | TiFlashの圧縮アルゴリズムを指定します。オプションの値は`LZ4` 、 `zstd` 、および`LZ4HC`で、すべて大文字と小文字が区別されません。デフォルト値は`LZ4`です。                                                                                                                                                                                                                 |
| TiFlash        | [`profiles.default.dt_compression_level`](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)                                                                                                      | 新規追加   | TiFlashの圧縮レベルを指定します。デフォルト値は`1`です。                                                                                                                                                                                                                                                                             |
| DM             | [`loaders.&#x3C;name>.import-mode`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                               | 新規追加   | フル インポート フェーズ中のインポート モード。 v6.0 以降、DM は TiDB Lightning の TiDB バックエンド モードを使用して、フル インポート フェーズでデータをインポートします。以前のローダーコンポーネントは使用されなくなりました。これは内部交換であり、日常業務に明らかな影響はありません。<br/>デフォルト値は`sql`に設定されており、これは`tidb-backend`モードを使用することを意味します。まれに、 `tidb-backend`完全な互換性がない場合があります。このパラメーターを`loader`に設定すると、ローダー モードにフォールバックできます。 |
| DM             | [`loaders.&#x3C;name>.on-duplicate`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                                                                                              | 新規追加   | フル インポート フェーズ中に競合を解決する方法を指定します。デフォルト値は`replace`です。これは、新しいデータを使用して既存のデータを置き換えることを意味します。                                                                                                                                                                                                                        |
| TiCDC          | [`dial-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                     | 新規追加   | ダウンストリーム Kafka との接続を確立する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                              |
| TiCDC          | [`read-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                     | 新規追加   | ダウンストリーム Kafka から返された応答を取得する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                          |
| TiCDC          | [`write-timeout`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                                    | 新規追加   | ダウンストリーム Kafka にリクエストを送信する際のタイムアウト。デフォルト値は`10s`です。                                                                                                                                                                                                                                                            |

### その他 {#others}

-   データ配置ポリシーには、次の互換性の変更があります。
    -   バインディングはサポートされていません。直接配置オプションは構文から削除されました。
    -   `CREATE PLACEMENT POLICY`および`ALTER PLACEMENT POLICY`ステートメントは、 `VOTERS`および`VOTER_CONSTRAINTS`配置オプションをサポートしなくなりました。
    -   TiDB 移行ツール (TiDB Binlog、TiCDC、およびBR) が配置ルールと互換性を持つようになりました。配置オプションは TiDB Binlogの特別なコメントに移動されました。
    -   `information_schema.placement_rules`システム テーブルの名前が`information_schema.placement_policies`に変更されます。この表には、配置ポリシーに関する情報のみが表示されるようになりました。
    -   `placement_checks`システム変数は`tidb_placement_mode`に置き換えられます。
    -   TiFlashレプリカを持つテーブルに、配置ルールを持つパーティションを追加することは禁止されています。
    -   `INFORMATION_SCHEMA`テーブルから`TIDB_DIRECT_PLACEMENT`列を削除します。
-   SQL 計画管理 (SPM) バインディングの`status`値が変更されました。
    -   `using`を削除します。
    -   `enabled` (使用可能) を追加して`using`を置き換えます。
    -   `disabled` (使用不可) を追加します。
-   DM は OpenAPI インターフェイスを変更します
    -   内部機構の変更により、タスク管理に関連するインターフェイスは、以前の実験的バージョンと互換性がありません。適応のために新しい[DM OpenAPI ドキュメント](/dm/dm-open-api.md)を参照する必要があります。
-   DM は、フル インポート フェーズ中に競合を解決する方法を変更します。
    -   `loader.<name>.on-duplicate`パラメータが追加されます。デフォルト値は`replace`です。これは、新しいデータを使用して既存のデータを置き換えることを意味します。以前の動作を維持したい場合は、値を`error`に設定できます。このパラメータは、フル インポート フェーズ中の動作のみを制御します。
-   DM を使用するには、対応するバージョンの`dmctl`を使用する必要があります。
    -   内部メカニズムの変更により、DM を v6.0.0 にアップグレードした後、 `dmctl`も v6.0.0 にアップグレードする必要があります。
-   v5.4 (v5.4 のみ) では、TiDB は一部の noop システム変数に対して誤った値を許可します。 v6.0.0 以降、TiDB はシステム変数に誤った値を設定することを禁止しています。 [#31538](https://github.com/pingcap/tidb/issues/31538)

## 改良点 {#improvements}

-   TiDB

    -   `FLASHBACK`または`RECOVER`ステートメントを使用してテーブルを復元した後、テーブルの配置規則の設定を自動的にクリアする[#31668](https://github.com/pingcap/tidb/issues/31668)
    -   パフォーマンス概要ダッシュボードを追加して、典型的なクリティカル パスに関するコア パフォーマンス メトリックを表示し、TiDB でのメトリック分析を容易にします[#31676](https://github.com/pingcap/tidb/issues/31676)
    -   `LOAD DATA LOCAL INFILE`ステートメント[#24515](https://github.com/pingcap/tidb/issues/24515)での`REPLACE`キーワードの使用のサポート
    -   範囲パーティション テーブル[#26739](https://github.com/pingcap/tidb/issues/26739)の組み込み`IN`式のパーティション プルーニングをサポートします。
    -   MPP 集計クエリで潜在的に冗長な Exchange 操作を排除することにより、クエリの効率を向上させます[#31762](https://github.com/pingcap/tidb/issues/31762)
    -   `TRUNCATE PARTITION`と`DROP PARTITION`ステートメントで重複するパーティション名を許可することにより、MySQL との互換性を向上させます[#31681](https://github.com/pingcap/tidb/issues/31681)
    -   `ADMIN SHOW DDL JOBS`ステートメント[#23494](https://github.com/pingcap/tidb/issues/23494)の結果に`CREATE_TIME`情報を表示するサポート
    -   新しい組み込み関数のサポート`CHARSET()` [#3931](https://github.com/pingcap/tidb/issues/3931)
    -   ユーザー名によるベースライン キャプチャ ブロックリストのフィルタリングのサポート[#32558](https://github.com/pingcap/tidb/issues/32558)
    -   ベースライン キャプチャ ブロックリストでのワイルドカードの使用のサポート[#32714](https://github.com/pingcap/tidb/issues/32714)
    -   現在の`time_zone` [#26642](https://github.com/pingcap/tidb/issues/26642)に従って時間を表示することにより、 `ADMIN SHOW DDL JOBS`ステートメントと`SHOW TABLE STATUS`ステートメントの結果を最適化します。
    -   `DAYNAME()`および`MONTHNAME()`関数をTiFlash [#32594](https://github.com/pingcap/tidb/issues/32594)にプッシュダウンするサポート
    -   `REGEXP`機能のTiFlash [#32637](https://github.com/pingcap/tidb/issues/32637)へのプッシュダウンをサポート
    -   `DAYOFMONTH()`および`LAST_DAY()`関数をTiFlash [#33012](https://github.com/pingcap/tidb/issues/33012)にプッシュダウンするサポート
    -   `DAYOFWEEK()`および`DAYOFYEAR()`関数をTiFlash [#33130](https://github.com/pingcap/tidb/issues/33130)にプッシュダウンするサポート
    -   `IS_TRUE` 、 `IS_FALSE` 、および`IS_TRUE_WITH_NULL`関数のTiFlash [#33047](https://github.com/pingcap/tidb/issues/33047)へのプッシュダウンをサポート
    -   `GREATEST`および`LEAST`関数をTiFlash [#32787](https://github.com/pingcap/tidb/issues/32787)にプッシュダウンするサポート
    -   `UnionScan`オペレーターの実行の追跡をサポート[#32631](https://github.com/pingcap/tidb/issues/32631)
    -   `_tidb_rowid`列[#31543](https://github.com/pingcap/tidb/issues/31543)を読み取るクエリの PointGet プランを使用したサポート
    -   名前を小文字に変換せずに`EXPLAIN`ステートメントの出力に元のパーティション名を表示するサポート[#32719](https://github.com/pingcap/tidb/issues/32719)
    -   IN 条件および文字列型の列[#32626](https://github.com/pingcap/tidb/issues/32626)で RANGE COLUMNS パーティション分割のパーティション プルーニングを有効にする
    -   システム変数が NULL に設定されている場合にエラー メッセージを返す[#32850](https://github.com/pingcap/tidb/issues/32850)
    -   非 MPP モードから Broadcast Join を削除する[#31465](https://github.com/pingcap/tidb/issues/31465)
    -   動的プルーニング モード[#32347](https://github.com/pingcap/tidb/issues/32347)でのパーティション テーブルでの MPP プランの実行のサポート
    -   共通テーブル式 (CTE) の述語のプッシュ ダウンをサポート[#28163](https://github.com/pingcap/tidb/issues/28163)
    -   `Statement Summary`と`Capture Plan Baselines`の構成を簡素化して、グローバル ベースでのみ使用できるようにする[#30557](https://github.com/pingcap/tidb/issues/30557)
    -   gopsutil を v3.21.12 に更新して、macOS 12 でバイナリをビルドするときに報告されるアラームに対処します[#31607](https://github.com/pingcap/tidb/issues/31607)

-   TiKV

    -   多くのキー範囲を持つバッチのRaftstoreのサンプリング精度を向上させます[#12327](https://github.com/tikv/tikv/issues/12327)
    -   `debug/pprof/profile`の正しい「Content-Type」を追加して、プロファイルをより簡単に識別できるようにします[#11521](https://github.com/tikv/tikv/issues/11521)
    -   Raftstore がハートビートを持っているとき、またはレイテンシー要求を処理しているときに、リーダーのリース時間を無限に更新します[#11579](https://github.com/tikv/tikv/issues/11579)
    -   リーダーを切り替えるときにコストが最も低いストアを選択すると、パフォーマンスの安定性が向上します[#10602](https://github.com/tikv/tikv/issues/10602)
    -   Raftstoreをブロックすることによって引き起こされるパフォーマンスのジッターを減らすために、 Raftログを非同期的に取得します[#11320](https://github.com/tikv/tikv/issues/11320)
    -   ベクトル計算[#5751](https://github.com/tikv/tikv/issues/5751)で`QUARTER`関数をサポート
    -   `BIT`データ型の TiKV [#30738](https://github.com/pingcap/tidb/issues/30738)へのプッシュ ダウンをサポート
    -   `MOD`機能と`SYSDATE`機能をTiKV [#11916](https://github.com/tikv/tikv/issues/11916)に押し下げるサポート
    -   ロックの解決ステップ[#11993](https://github.com/tikv/tikv/issues/11993)を必要とするリージョンの数を減らすことで、TiCDC の回復時間を短縮します。
    -   動的変更のサポート`raftstore.raft-max-inflight-msgs` [#11865](https://github.com/tikv/tikv/issues/11865)
    -   動的プルーニング モード[#11888](https://github.com/tikv/tikv/issues/11888)を有効にするサポート`EXTRA_PHYSICAL_TABLE_ID_COL_ID`
    -   バケット[#11759](https://github.com/tikv/tikv/issues/11759)でのサポート計算
    -   RawKV API V2 のキーを`user-key` + `memcomparable-padding` + `timestamp` [#11965](https://github.com/tikv/tikv/issues/11965)としてエンコードします
    -   RawKV API V2 の値を`user-value` + `ttl` + `ValueMeta`としてエンコードし、 `delete` `ValueMeta` [#11965](https://github.com/tikv/tikv/issues/11965)でエンコードします
    -   動的変更のサポート`raftstore.raft-max-size-per-msg` [#12017](https://github.com/tikv/tikv/issues/12017)
    -   Grafana [#12014](https://github.com/tikv/tikv/issues/12014)でマルチ k8 の監視をサポート
    -   リーダーシップを CDC オブザーバーに移管し、レイテンシーのジッターを減らします[#12111](https://github.com/tikv/tikv/issues/12111)
    -   `raftstore.apply_max_batch_size`および`raftstore.store_max_batch_size` [#11982](https://github.com/tikv/tikv/issues/11982)の動的変更をサポート
    -   RawKV V2 は、 `raw_get`または`raw_scan`リクエストを受け取ると最新バージョンを返します[#11965](https://github.com/tikv/tikv/issues/11965)
    -   RCCheckTS 一貫性読み取りをサポート[#12097](https://github.com/tikv/tikv/issues/12097)
    -   動的変更のサポート`storage.scheduler-worker-pool-size` (Scheduler プールのスレッド数) [#12067](https://github.com/tikv/tikv/issues/12067)
    -   グローバル フォアグラウンド フロー コントローラーを使用して CPU と帯域幅の使用を制御し、TiKV [#11855](https://github.com/tikv/tikv/issues/11855)のパフォーマンスの安定性を向上させます。
    -   動的変更のサポート`readpool.unified.max-thread-count` (UnifyReadPool のスレッド数) [#11781](https://github.com/tikv/tikv/issues/11781)
    -   TiKV 内部パイプラインを使用して RocksDB パイプラインを置き換え、 `rocksdb.enable-multibatch-write`パラメータ[#12059](https://github.com/tikv/tikv/issues/12059)を非推奨にします

-   PD

    -   リーダーを削除するときに転送する最速のオブジェクトを自動的に選択することをサポートし、削除プロセスを高速化します[#4229](https://github.com/tikv/pd/issues/4229)
    -   リージョンが利用できなくなった場合に備えて、2 レプリカRaftグループから有権者を削除することを禁止する[#4564](https://github.com/tikv/pd/issues/4564)
    -   バランスリーダー[#4652](https://github.com/tikv/pd/issues/4652)のスケジューリングをスピードアップ

-   TiFlash

    -   TiFlashファイルの論理分割を禁止し (デフォルト値の`profiles.default.dt_enable_logical_split`から`false`を調整します。詳細については[ユーザー文書](/tiflash/tiflash-configuration.md#tiflash-configuration-parameters)参照してください)、 TiFlashカラムナstorageのスペース使用効率を改善して、 TiFlashに同期されたテーブルのスペース占有がスペースと同様になるようにします。 TiKVでのテーブルの占有
    -   以前のクラスタ管理モジュールを TiDB に統合することで、 TiFlashのクラスタ管理とレプリカ レプリケーション メカニズムを最適化し、小さなテーブルのレプリカ作成を高速化します[#29924](https://github.com/pingcap/tidb/issues/29924)

-   ツール

    -   バックアップと復元 (BR)

        -   バックアップ データの復元速度を向上させます。 BR が16 TB のデータを 15 ノード (各ノードには 16 CPU コアを持つ) の TiKV クラスターに復元するシミュレーション テストでは、スループットは 2.66 GiB/s に達します。 [#27036](https://github.com/pingcap/tidb/issues/27036)

        -   配置ルールのインポートとエクスポートをサポートします。データのインポート時に配置ルールを無視するかどうかを制御する`--with-tidb-placement-mode`パラメーターを追加します。 [#32290](https://github.com/pingcap/tidb/issues/32290)

    -   TiCDC

        -   Grafana [#4891](https://github.com/pingcap/tiflow/issues/4891)に`Lag analyze`パネルを追加する
        -   サポート配置ルール[#4846](https://github.com/pingcap/tiflow/issues/4846)
        -   HTTP API 処理の同期[#1710](https://github.com/pingcap/tiflow/issues/1710)
        -   changefeed [#3329](https://github.com/pingcap/tiflow/issues/3329)を再開するための指数バックオフ メカニズムを追加します。
        -   MySQL [#3589](https://github.com/pingcap/tiflow/issues/3589)のデッドロックを減らすために、MySQL シンクのデフォルトの分離レベルを read-committed に設定します
        -   作成時に変更フィード パラメータを検証し、エラー メッセージを改善する[#1716](https://github.com/pingcap/tiflow/issues/1716) [#1718](https://github.com/pingcap/tiflow/issues/1718) [#1719](https://github.com/pingcap/tiflow/issues/1719) [#4472](https://github.com/pingcap/tiflow/issues/4472)
        -   Kafka プロデューサーの構成パラメーターを公開して、TiCDC [#4385](https://github.com/pingcap/tiflow/issues/4385)で構成可能にする

    -   TiDB データ移行 (DM)

        -   上流のテーブル スキーマに一貫性がなく、楽観的モードの場合のタスクの開始のサポート[#3629](https://github.com/pingcap/tiflow/issues/3629) [#3708](https://github.com/pingcap/tiflow/issues/3708) [#3786](https://github.com/pingcap/tiflow/issues/3786)
        -   `stopped`状態でのタスクの作成をサポート[#4484](https://github.com/pingcap/tiflow/issues/4484)
        -   内部ファイルの書き込みに`/tmp`ではなく DM-worker の作業ディレクトリを使用し、タスクの停止後にディレクトリをクリーニングする Syncer をサポートします[#4107](https://github.com/pingcap/tiflow/issues/4107)
        -   事前チェックが改善されました。いくつかの重要なチェックがスキップされなくなりました。 [#3608](https://github.com/pingcap/tiflow/issues/3608)

    -   TiDB Lightning

        -   再試行可能なエラーの種類を追加する[#31376](https://github.com/pingcap/tidb/issues/31376)
        -   base64 形式のパスワード文字列[#31194](https://github.com/pingcap/tidb/issues/31194)をサポート
        -   エラーコードとエラー出力の標準化[#32239](https://github.com/pingcap/tidb/issues/32239)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `SCHEDULE = majority_in_primary`と`PrimaryRegion`と`Regions`が同じ値[#31271](https://github.com/pingcap/tidb/issues/31271)の場合、TiDB が配置規則を使用してテーブルを作成できないというバグを修正
    -   インデックス ルックアップ ジョイン[#30468](https://github.com/pingcap/tidb/issues/30468)を使用してクエリを実行するときの`invalid transaction`エラーを修正します。
    -   2 つ以上の権限が付与されている場合に`show grants`が誤った結果を返すバグを修正[#30855](https://github.com/pingcap/tidb/issues/30855)
    -   `INSERT INTO t1 SET timestamp_col = DEFAULT`がデフォルトの`CURRENT_TIMESTAMP` [#29926](https://github.com/pingcap/tidb/issues/29926)に設定されているフィールドのタイムスタンプをゼロのタイムスタンプに設定するというバグを修正します
    -   文字列型[#31721](https://github.com/pingcap/tidb/issues/31721)の最大値と最小非 null 値のエンコードを回避することで、結果の読み取りで報告されたエラーを修正します。
    -   データがエスケープ文字[#31589](https://github.com/pingcap/tidb/issues/31589)で壊れた場合のロード データpanicを修正
    -   照合順序を伴う`greatest`または`least`関数が間違った結果を取得する問題を修正します[#31789](https://github.com/pingcap/tidb/issues/31789)
    -   date_add および date_sub関数が誤ったデータ型を返す可能性があるバグを修正します[#31809](https://github.com/pingcap/tidb/issues/31809)
    -   挿入ステートメントを使用して仮想的に生成された列にデータを挿入するときに発生する可能性のあるpanicを修正します[#31735](https://github.com/pingcap/tidb/issues/31735)
    -   作成したリスト パーティション[#31784](https://github.com/pingcap/tidb/issues/31784)に重複する列が存在する場合にエラーが報告されないバグを修正
    -   `select for update union select`不適切なスナップショットを使用した場合に返される誤った結果を修正します[#31530](https://github.com/pingcap/tidb/issues/31530)
    -   復元操作の完了後にリージョンが不均一に分散される可能性があるという潜在的な問題を修正します[#31034](https://github.com/pingcap/tidb/issues/31034)
    -   COERCIBILITY が`json`タイプ[#31541](https://github.com/pingcap/tidb/issues/31541)で間違っているバグを修正
    -   この型が builtin-func [#31320](https://github.com/pingcap/tidb/issues/31320)を使用して処理されるときの`json`型の間違った照合順序を修正します
    -   TiFlashレプリカの数が 0 に設定されている場合に PD ルールが削除されないバグを修正します[#32190](https://github.com/pingcap/tidb/issues/32190)
    -   `alter column set default`テーブル スキーマを誤って更新する問題を修正します[#31074](https://github.com/pingcap/tidb/issues/31074)
    -   TiDB の`date_format`が MySQL と互換性のない方法で`'\n'`処理する問題を修正します[#32232](https://github.com/pingcap/tidb/issues/32232)
    -   結合[#31629](https://github.com/pingcap/tidb/issues/31629)を使用して分割されたテーブルを更新するとエラーが発生する可能性があるバグを修正
    -   Enum 値[#32428](https://github.com/pingcap/tidb/issues/32428)の Nulleq 関数の誤った範囲計算結果を修正
    -   関数`upper()`と機能`lower()`でpanicを修正[#32488](https://github.com/pingcap/tidb/issues/32488)
    -   他のタイプの列をタイムスタンプ タイプの列[#29585](https://github.com/pingcap/tidb/issues/29585)に変更するときに発生するタイム ゾーンの問題を修正します。
    -   ChunkRPC を使用してデータをエクスポートするときの TiDB OOM を修正[#31981](https://github.com/pingcap/tidb/issues/31981) [#30880](https://github.com/pingcap/tidb/issues/30880)
    -   動的パーティションプルーニングモード[#32516](https://github.com/pingcap/tidb/issues/32516)で、sub SELECT LIMIT が期待どおりに動作しないバグを修正
    -   `INFORMATION_SCHEMA.COLUMNS`テーブル[#32655](https://github.com/pingcap/tidb/issues/32655)のビット デフォルト値の間違った形式または矛盾した形式を修正します。
    -   サーバーの再起動後、パーティション テーブルの一覧表示でパーティション テーブルのプルーニングが機能しない可能性があるバグを修正します[#32416](https://github.com/pingcap/tidb/issues/32416)
    -   `add column`が`SET timestamp`の実行後に間違ったデフォルトのタイムスタンプを使用する可能性があるバグを修正します[#31968](https://github.com/pingcap/tidb/issues/31968)
    -   MySQL 5.5 または 5.6 クライアントから TiDB のパスワードなしアカウントへの接続が失敗する可能性があるバグを修正[#32334](https://github.com/pingcap/tidb/issues/32334)
    -   トランザクション[#29851](https://github.com/pingcap/tidb/issues/29851)の動的モードで分割されたテーブルを読み取るときの誤った結果を修正
    -   TiDB が重複したタスクをTiFlash [#32814](https://github.com/pingcap/tidb/issues/32814)にディスパッチする可能性があるバグを修正
    -   `timdiff`関数の入力にミリ秒[#31680](https://github.com/pingcap/tidb/issues/31680)含まれている場合に返される間違った結果を修正
    -   パーティションを明示的に読み取り、IndexJoin プラン[#32007](https://github.com/pingcap/tidb/issues/32007)を使用した場合の間違った結果を修正
    -   列の種類を同時に変更すると、列の名前変更が失敗するバグを修正します[#31075](https://github.com/pingcap/tidb/issues/31075)
    -   TiFlashプランの正味コストの計算式が TiKV プランと一致しないというバグを修正します[#30103](https://github.com/pingcap/tidb/issues/30103)
    -   `KILL TIDB`アイドル接続ですぐに有効にならないバグを修正[#24031](https://github.com/pingcap/tidb/issues/24031)
    -   生成された列を含むテーブルをクエリするときに発生する可能性のある誤った結果を修正します[#33038](https://github.com/pingcap/tidb/issues/33038)
    -   `left join` [#31321](https://github.com/pingcap/tidb/issues/31321)を使用して複数のテーブルのデータを削除したときの誤った結果を修正
    -   `SUBTIME`関数がオーバーフロー[#31868](https://github.com/pingcap/tidb/issues/31868)の場合に間違った結果を返すバグを修正
    -   集計クエリに`having`条件[#33166](https://github.com/pingcap/tidb/issues/33166)が含まれている場合、 `selection`演算子をプッシュダウンできないバグを修正
    -   クエリがエラーを報告したときに CTE がブロックされる可能性があるバグを修正します[#31302](https://github.com/pingcap/tidb/issues/31302)
    -   非厳密モードでテーブルを作成するときに varbinary または varchar 列が長すぎるとエラーが発生する可能性があるというバグを修正します[#30328](https://github.com/pingcap/tidb/issues/30328)
    -   フォロワーが指定されていない場合に間違ったフォロワー数を修正する`information_schema.placement_policies` [#31702](https://github.com/pingcap/tidb/issues/31702)
    -   インデックスの作成時に TiDB が列プレフィックス長を 0 に指定できる問題を修正します[#31972](https://github.com/pingcap/tidb/issues/31972)
    -   TiDB がスペース[#31535](https://github.com/pingcap/tidb/issues/31535)で終わるパーティション名を許可する問題を修正
    -   `RENAME TABLE`ステートメント[#29893](https://github.com/pingcap/tidb/issues/29893)のエラー メッセージを修正します。

-   TiKV

    -   ピア ステータスが`Applying` [#11746](https://github.com/tikv/tikv/issues/11746)のときにスナップショット ファイルを削除すると発生するpanicの問題を修正します。
    -   フロー制御が有効で、 `level0_slowdown_trigger`が明示的に設定され[#11424](https://github.com/tikv/tikv/issues/11424)いる場合の QPS ドロップの問題を修正します。
    -   ピアを破棄すると高レイテンシーが発生する可能性がある問題を修正します[#10210](https://github.com/tikv/tikv/issues/10210)
    -   GC ワーカーがビジー状態の場合、TiKV がデータの範囲を削除できない (つまり、内部コマンド`unsafe_destroy_range`が実行される) バグを修正します[#11903](https://github.com/tikv/tikv/issues/11903)
    -   一部のまれなケースで`StoreMeta`のデータが誤って削除されると、TiKV がパニックになるバグを修正します[#11852](https://github.com/tikv/tikv/issues/11852)
    -   ARM プラットフォームでプロファイリングを実行すると TiKV がパニックになるバグを修正[#10658](https://github.com/tikv/tikv/issues/10658)
    -   TiKVが2年以上稼働しているとpanicになることがあるバグを修正[#11940](https://github.com/tikv/tikv/issues/11940)
    -   SSE 命令セット[#12034](https://github.com/tikv/tikv/issues/12034)が欠落しているために発生した ARM64アーキテクチャでのコンパイルの問題を修正します。
    -   初期化されていないレプリカを削除すると、古いレプリカが再作成される可能性があるという問題を修正します[#10533](https://github.com/tikv/tikv/issues/10533)
    -   古いメッセージが原因で TiKV がpanicになるバグを修正[#12023](https://github.com/tikv/tikv/issues/12023)
    -   TsSet 変換で未定義の動作 (UB) が発生する可能性がある問題を修正します[#12070](https://github.com/tikv/tikv/issues/12070)
    -   レプリカの読み取りが線形化可能性に違反する可能性があるバグを修正します[#12109](https://github.com/tikv/tikv/issues/12109)
    -   TiKV が Ubuntu [#9765](https://github.com/tikv/tikv/issues/9765)でプロファイリングを実行するときに発生する潜在的なpanicの問題を修正します。
    -   間違った文字列の一致が原因で tikv-ctl が間違った結果を返す問題を修正します[#12329](https://github.com/tikv/tikv/issues/12329)
    -   メモリメトリック[#12160](https://github.com/tikv/tikv/issues/12160)のオーバーフローが原因で発生する断続的なパケット損失とメモリ不足 (OOM) の問題を修正します。
    -   TiKV [#12231](https://github.com/tikv/tikv/issues/12231)の終了時に TiKV パニックを誤って報告する潜在的な問題を修正

-   PD

    -   ジョイント コンセンサス[#4362](https://github.com/tikv/pd/issues/4362)の無意味な手順で PD が演算子を生成する問題を修正
    -   PD クライアント[#4549](https://github.com/tikv/pd/issues/4549)を閉じると、TSO 取り消しプロセスがスタックする可能性があるバグを修正します。
    -   リージョン scatterer スケジューリングで一部のピアが失われる問題を修正します[#4565](https://github.com/tikv/pd/issues/4565)
    -   `dr-autosync`のフィールドのうち`Duration`フィールドを動的に構成できないという問題を修正します[#4651](https://github.com/tikv/pd/issues/4651)

-   TiFlash

    -   メモリ制限が有効になっているときに発生するTiFlashpanicの問題を修正します[#3902](https://github.com/pingcap/tiflash/issues/3902)
    -   期限切れのデータがゆっくりとリサイクルされる問題を修正します[#4146](https://github.com/pingcap/tiflash/issues/4146)
    -   `Snapshot`が複数の DDL 操作と同時に適用された場合のTiFlashpanicの潜在的な問題を修正します[#4072](https://github.com/pingcap/tiflash/issues/4072)
    -   重い読み取りワークロードの下で列を追加した後の潜在的なクエリ エラーを修正します[#3967](https://github.com/pingcap/tiflash/issues/3967)
    -   負の引数を持つ`SQRT`関数が`Null` [#3598](https://github.com/pingcap/tiflash/issues/3598)ではなく`NaN`を返す問題を修正
    -   `INT`から`DECIMAL`をキャストするとオーバーフロー[#3920](https://github.com/pingcap/tiflash/issues/3920)が発生する可能性がある問題を修正
    -   多値式で`IN`の結果が正しくない問題を修正[#4016](https://github.com/pingcap/tiflash/issues/4016)
    -   日付形式が`'\n'`を無効な区切り文字として識別する問題を修正します[#4036](https://github.com/pingcap/tiflash/issues/4036)
    -   同時実行性の高いシナリオで学習者の読み取りプロセスに時間がかかりすぎる問題を修正します[#3555](https://github.com/pingcap/tiflash/issues/3555)
    -   `DATETIME`から`DECIMAL` [#4151](https://github.com/pingcap/tiflash/issues/4151)をキャストしたときに発生する誤った結果を修正します
    -   クエリがキャンセルされたときに発生するメモリリークの問題を修正します。 [#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   エラスティック スレッド プールを有効にするとメモリリークが発生する可能性があるバグを修正します[#4098](https://github.com/pingcap/tiflash/issues/4098)
    -   ローカル トンネルが有効になっている場合、MPP クエリをキャンセルすると、タスクが[#4229](https://github.com/pingcap/tiflash/issues/4229)にハングする可能性があるというバグを修正します。
    -   HashJoin ビルド側の障害により、MPP クエリが永久にハングする可能性があるというバグを修正します[#4195](https://github.com/pingcap/tiflash/issues/4195)
    -   MPP タスクがスレッドを永久にリークする可能性があるバグを修正します[#4238](https://github.com/pingcap/tiflash/issues/4238)

-   ツール

    -   バックアップと復元 (BR)

        -   復元操作がいくつかの回復不能なエラーに遭遇したときにBR がスタックするバグを修正します[#33200](https://github.com/pingcap/tidb/issues/33200)
        -   バックアップの再試行中に暗号化情報が失われると、復元操作が失敗する原因となるバグを修正します[#32423](https://github.com/pingcap/tidb/issues/32423)

    -   TiCDC

        -   `batch-replace-enable`が無効になっている場合、MySQL シンクが重複した`replace` SQL ステートメントを生成するバグを修正します[#4501](https://github.com/pingcap/tiflow/issues/4501)
        -   PD リーダーが強制終了されたときに TiCDC ノードが異常終了するバグを修正します[#4248](https://github.com/pingcap/tiflow/issues/4248)
        -   一部の MySQL バージョン[#4504](https://github.com/pingcap/tiflow/issues/4504)のエラー`Unknown system variable 'transaction_isolation'`を修正します。
        -   `Canal-JSON` `string` [#4635](https://github.com/pingcap/tiflow/issues/4635)を正しく処理しない場合に発生する可能性のある TiCDCpanicの問題を修正します。
        -   場合によってはシーケンスが正しく複製されないというバグを修正[#4563](https://github.com/pingcap/tiflow/issues/4552)
        -   `Canal-JSON`が nil [#4736](https://github.com/pingcap/tiflow/issues/4736)をサポートしていないために発生する可能性のある TiCDCpanicの問題を修正します。
        -   タイプ`Enum/Set`および`TinyText/MediumText/Text/LongText` [#4454](https://github.com/pingcap/tiflow/issues/4454)の avro コーデックの間違ったデータ マッピングを修正
        -   Avro が`NOT NULL`列を null 許容フィールド[#4818](https://github.com/pingcap/tiflow/issues/4818)に変換するバグを修正
        -   TiCDC が終了できない問題を修正[#4699](https://github.com/pingcap/tiflow/issues/4699)

    -   TiDB データ移行 (DM)

        -   ステータス[#4281](https://github.com/pingcap/tiflow/issues/4281)を照会した場合にのみ syncer メトリクスが更新される問題を修正します。
        -   セーフモードで update ステートメントの実行エラーが発生すると、DM-workerpanic[#4317](https://github.com/pingcap/tiflow/issues/4317)が発生する可能性がある問題を修正します。
        -   長い varchar がエラーを報告するバグを修正`Column length too big` [#4637](https://github.com/pingcap/tiflow/issues/4637)
        -   複数の DM ワーカーが同じアップストリーム[#3737](https://github.com/pingcap/tiflow/issues/3737)からデータを書き込むことによって発生する競合の問題を修正します。
        -   何百もの &quot;checkpoint has no change, skip sync flush checkpoint&quot; がログに出力され、レプリケーションが非常に遅いという問題を修正します[#4619](https://github.com/pingcap/tiflow/issues/4619)
        -   悲観的モード[#5002](https://github.com/pingcap/tiflow/issues/5002)でシャードをマージし、アップストリームから増分データをレプリケートするときの DML 損失の問題を修正します。

    -   TiDB Lightning

        -   一部のインポート タスクにソース ファイルが含まれていない場合、 TiDB Lightning がメタデータ スキーマを削除しないことがあるというバグを修正します[#28144](https://github.com/pingcap/tidb/issues/28144)
        -   ソース ファイルとターゲット クラスタのテーブル名が異なる場合に発生するpanicを修正します[#31771](https://github.com/pingcap/tidb/issues/31771)
        -   チェックサム エラー「GC ライフ タイムがトランザクション期間よりも短い」を修正します[#32733](https://github.com/pingcap/tidb/issues/32733)
        -   空のテーブルのチェックに失敗するとTiDB Lightningがスタックする問題を修正[#31797](https://github.com/pingcap/tidb/issues/31797)

    -   Dumpling

        -   `dumpling --sql $query` [#30532](https://github.com/pingcap/tidb/issues/30532)実行時に表示される進行状況が正確でない問題を修正
        -   Amazon S3 が圧縮データのサイズを正しく計算できない問題を修正[#30534](https://github.com/pingcap/tidb/issues/30534)

    -   TiDBBinlog

        -   大規模なアップストリーム書き込みトランザクションが Kafka [#1136](https://github.com/pingcap/tidb-binlog/issues/1136)にレプリケートされると、TiDB Binlogがスキップされる可能性がある問題を修正します

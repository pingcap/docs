---
title: TiDB 6.4.0 Release Notes
summary: TiDB 6.4.0-DMRでは、クラスタを特定の時点に復元する機能、線形ハッシュパーティショニング構文との互換性、高性能なAUTO_INCREMENT`モードなど、新機能と改善点が導入されています。また、障害リカバリ、メモリ使用量制御、統計情報の収集機能も強化されています。TiFlashは保存時の暗号化にSM4アルゴリズムをサポートし、TiCDCはKafkaへのデータレプリケートに対応しました。さらに、各種ツールやコンポーネントにおけるバグ修正と改善も含まれています。
---

# TiDB 6.4.0 リリースノート {#tidb-6-4-0-release-notes}

発売日：2022年11月17日

TiDBバージョン: 6.4.0-DMR

> **Note:**
>
> TiDB 6.4.0-DMR ドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.4/)です。 PingCAP は、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨します。

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v6.4/quick-start-with-tidb)

バージョン6.4.0-DMRの主な新機能と改善点は以下のとおりです。

-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) (実験的) を使用して、クラスターを特定の時点に復元することをサポートします。
-   TiDB インスタンスの[グローバルメモリ使用量の追跡](/configure-memory-usage.md)をサポートします (実験的)。
-   [線形ハッシュのパーティショニング構文](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)と互換性があります。
-   高性能かつグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode)サポートします (実験的)。
-   [JSON型](/data-type-json.md)の配列データの範囲選択をサポートします。
-   ディスク障害やI/Oスタックなどの極端な状況下での障害リカバリを加速します。
-   [動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)を追加して、テーブルの結合順序を決定します。
-   [新しいオプティマイザヒント`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)を導入して、相関サブクエリの非相関化を実行するかどうかを制御します。
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能が GA になります。
-   TiFlash は[保存時の暗号化](/encryption-at-rest.md#tiflash)のための SM4 アルゴリズムをサポートしています。
-   SQL ステートメントを使用して[テーブル内の指定されたパーティションのコンパクトなTiFlashレプリカを即座に](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)サポートします。
-   [EBSボリュームスナップショットを使用したTiDBクラスタのバックアップ](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)サポートします。
-   DM は[上流のデータソース情報を下流のマージ済みテーブルの拡張列に書き込む](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)サポートしています。

## 新機能 {#new-features}

### SQL {#sql}

-   SQL ステートメントを使用して、テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮するサポート [#5315](https://github.com/pingcap/tiflash/issues/5315) @[hehechen](https://github.com/hehechen)

    バージョン6.2.0以降、TiDBはTiFlashのフルテーブルレプリカに対して[物理データを即座に圧縮する](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact)機能をサポートしています。適切なタイミングでSQLステートメントを手動で実行してTiFlash内の物理データを即座に圧縮することで、ストレージ容量を削減し、クエリパフォーマンスを向上させることができます。バージョン6.4.0では、圧縮するTiFlashレプリカデータの粒度をさらに細かくし、テーブル内の指定されたパーティションのTiFlashレプリカを即座に圧縮できるようにしました。

    SQL ステートメント`ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`を実行すると、テーブル内の指定されたパーティションのTiFlashレプリカを即座に圧縮できます。

    詳細については、 [ユーザー向けドキュメント](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP`を使用した特定の時点へのクラスターの復元のサポート (実験的) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @[Defined2014](https://github.com/Defined2014) @[bb7133](https://github.com/bb7133) @[JmPotato](https://github.com/JmPotato) @[Connor1996](https://github.com/Connor1996) @[HuSharp](https://github.com/HuSharp) @[CalvinNeo](https://github.com/CalvinNeo)

    `FLASHBACK CLUSTER TO TIMESTAMP`構文を使用すると、ガベージコレクション（GC）の有効期間内に、クラスタを特定の時点に迅速に復元できます。この機能は、DML操作の誤りを簡単かつ迅速に取り消すのに役立ちます。たとえば、 `WHERE`句なしで誤って`DELETE`を実行した後、この構文を使用して数分で元のクラスタを復元できます。この機能はデータベースのバックアップに依存せず、異なる時点のデータをロールバックして、データが変更された正確な時刻を特定できます。 `FLASHBACK CLUSTER TO TIMESTAMP`はデータベースのバックアップの代わりにはならないことに注意してください。

    `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiCDC などのツールで実行されている PITR およびレプリケーション タスクを一時停止し、 `FLASHBACK`が完了した後に再開する必要があります。そうしないと、レプリケーション タスクが失敗する可能性があります。

    詳細については、 [ユーザー向けドキュメント](/sql-statements/sql-statement-flashback-cluster.md)を参照してください。

-   `FLASHBACK DATABASE` を使用して削除されたデータベースの復元をサポートします [#20463](https://github.com/pingcap/tidb/issues/20463) @[erwadba](https://github.com/erwadba)

    `FLASHBACK DATABASE`を使用すると、 `DROP`によってガベージコレクション(GC) の有効期間内に削除されたデータベースとそのデータを復元できます。この機能は外部ツールに依存しません。SQL ステートメントを使用して、データとメタデータを迅速に復元できます。

    詳細については、 [ユーザー向けドキュメント](/sql-statements/sql-statement-flashback-database.md)を参照してください。

### セキュリティ {#security}

-   TiFlashは保存時の暗号化にSM4アルゴリズムをサポートしています [#5953](https://github.com/pingcap/tiflash/issues/5953) @[lidezhu](https://github.com/lidezhu)

    TiFlashの保存時暗号化にSM4アルゴリズムを追加します。保存時暗号化を設定する際に、 `data-encryption-method`構成ファイル内の`sm4-ctr` 構成の値を`tiflash-learner.toml`暗号化機能を有効にできます。

    詳細については、[ユーザー向けドキュメント](/encryption-at-rest.md#tiflash)を参照してください。

### 可観測性 {#observability}

-   クラスタ診断が GA になります [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @[Hawkson-jee](https://github.com/Hawkson-jee)

    TiDB Dashboardの [クラスター診断](/dashboard/dashboard-diagnostics-access.md)は、指定された時間範囲内でクラスタに存在する可能性のある問題を診断し、診断結果とクラスタ関連の負荷監視情報を レポートにまとめます。この診断レポートはWeb [診断レポート](/dashboard/dashboard-diagnostics-report.md)形式です。ブラウザからページを保存した後、オフラインでページを閲覧したり、このページのリンクを共有したりできます。

    診断レポートを使用すると、負荷、コンポーネントの状態、処理時間、構成など、クラスタの基本的な状態情報をすばやく把握できます。クラスタに一般的な問題がある場合は、 [診断情報](/dashboard/dashboard-diagnostics-report.md#diagnostic-information)セクションにある組み込みの自動診断結果から原因を特定できます。

### パフォーマンス {#performance}

-   コプロセッサタスクの同時実行適応メカニズムを導入します [#37724](https://github.com/pingcap/tidb/issues/37724) @[you06](https://github.com/you06)

    TiKV の処理速度に基づいて、コプロセッサ タスクの数が増えると、TiDB は自動的に並列度を上げて ( [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の値を調整して)、コプロセッサ タスク キューを減らし、レイテンシーを削減します。

-   テーブル結合順序を決定するための動的計画アルゴリズムを追加 [#37825](https://github.com/pingcap/tidb/issues/37825) @[winoros](https://github.com/winoros)

    以前のバージョンでは、TiDB はテーブルの結合順序を決定するために貪欲アルゴリズムを使用していました。v6.4.0 では、TiDB オプティマイザに 計画 が導入されました。 [動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)計画アルゴリズムは、貪欲アルゴリズムよりも多くの可能な結合順序を列挙できるため、より良い実行計画を見つける可能性が高まり、一部のシナリオでは SQL 実行効率が向上します。

    動的計画法アルゴリズムは処理に時間がかかるため、TiDBの結合したテーブルの再配置アルゴリズムの選択は、 [`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)変数によって制御されます。Join 結合したテーブルの再配置に参加するノード数がこの閾値を超えると、TiDBは貪欲法アルゴリズムを使用します。そうでない場合は、動的計画法アルゴリズムを使用します。

    詳細については、[ユーザー向けドキュメント](/join-reorder.md)を参照してください。

-   プレフィックスインデックスは、null値のフィルタリングをサポートしています。 [#21145](https://github.com/pingcap/tidb/issues/21145) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    この機能は、プレフィックスインデックスの最適化です。テーブル内の列にプレフィックスインデックスが設定されている場合、SQL文内の列の`IS NULL`または`IS NOT NULL`条件をプレフィックスで直接フィルタリングできるため、この場合テーブル検索が不要になり、SQL実行のパフォーマンスが向上します。

    詳細については、 [ユーザー向けドキュメント](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)を参照してください。

-   TiDBチャンク再利用メカニズムの強化 [#38606](https://github.com/pingcap/tidb/issues/38606) @[keeplearning20221](https://github.com/keeplearning20221)

    以前のバージョンでは、TiDB は`writechunk`関数内でのみチャンクを再利用していました。TiDB v6.4.0 では、チャンク再利用メカニズムが Executor の演算子に拡張されました。チャンクを再利用することで、TiDB はメモリ解放を頻繁に要求する必要がなくなり、一部のシナリオでは SQL クエリの実行効率が向上します。システム変数[`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)使用して、チャンク オブジェクトを再利用するかどうかを制御できます。この機能はデフォルトで有効になっています。

    詳細については、 [ユーザー向けドキュメント](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)を参照してください。

-   相関サブクエリの非相関化を実行するかどうかを制御する新しいオプティマイザー ヒント`NO_DECORRELATE`を導入します [#37789](https://github.com/pingcap/tidb/issues/37789) @[time-and-fate](https://github.com/time-and-fate)

    TiDB はデフォルトでは、相関のあるサブクエリを書き換えて相関解除を実行しようとします。これにより、通常は実行効率が向上します。しかし、シナリオによっては相関解除によって実行効率が低下する場合があります。v6.4.0 では、オプティマイザヒント`NO_DECORRELATE`が導入され、特定のクエリブロックに対して相関解除を実行しないようにオプティマイザに指示することで、シナリオによってはクエリのパフォーマンスが向上します。

    詳細については、[ユーザー向けドキュメント](/optimizer-hints.md#no_decorrelate)を参照してください。

-   パーティション化されたテーブルの統計情報収集のパフォーマンスを改善する [#37977](https://github.com/pingcap/tidb/issues/37977) @[Yisaer](https://github.com/Yisaer)

    バージョン6.4.0では、TiDBはパーティションテーブルの統計情報を収集する戦略を最適化しました。システム変数[`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)を使用して、パーティションテーブルの統計情報を並列収集する際の同時実行数を設定することで、収集速度を向上させ、分析時間を短縮できます。

### 安定性 {#stability}

-   ディスク障害やI/Oスタックなどの極端な状況における障害リカバリを加速する [#13648](https://github.com/tikv/tikv/issues/13648) @[LykxSassinator](https://github.com/LykxSassinator)

    エンタープライズユーザーにとって、データベースの可用性は最も重要な指標の一つです。複雑なハードウェア環境では、障害を迅速に検知して復旧する方法が、データベース可用性における課題の一つとなっています。v6.4.0では、TiDBはTiKVノードの状態検出メカニズムを完全に最適化しました。ディスク障害やI/Oスタックといった極端な状況下でも、TiDBはノードの状態を迅速に報告し、アクティブウェイクアップメカニズムを使用してLeader選出を事前に開始することで、クラスタの自己修復を加速します。この最適化により、TiDBはディスク障害発生時のクラスタリカバリ時間を約50%短縮できます。

-   TiDBのメモリ使用量に関するグローバル制御 [#37816](https://github.com/pingcap/tidb/issues/37816) @[wshwsh12](https://github.com/wshwsh12)

    バージョン6.4.0では、TiDBインスタンスのグローバルメモリ使用量を追跡する実験的機能として、メモリ使用量のグローバル制御が導入されました。システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用して、グローバルメモリ使用量の上限を設定できます。メモリ使用量がしきい値に達すると、TiDBはより多くの空きメモリを解放しようとします。メモリ使用量がしきい値を超えると、TiDBはメモリ使用量が最も高いSQL操作を特定してキャンセルし、過剰なメモリ使用量によって引き起こされるシステムの問題を防ぎます。

    TiDBインスタンスのメモリ消費に潜在的なリスクがある場合、TiDBは事前に診断情報を収集し、指定されたディレクトリに書き込むことで、問題の診断を容易にします。同時に、TiDBはメモリ使用量と操作履歴を表示するシステムテーブルビュー[`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)と[`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)を提供し、メモリ使用状況をより深く理解できるようにします。

    グローバルメモリ制御は、TiDBのメモリ管理における画期的な機能です。インスタンスのグローバルな視点を導入し、メモリの体系的な管理を採用することで、より多くの重要なシナリオにおいてデータベースの安定性とサービスの可用性を大幅に向上させることができます。

    詳細については、[ユーザー向けドキュメント](/configure-memory-usage.md)を参照してください。

-   範囲構築オプティマイザのメモリ使用量を制御する [#37176](https://github.com/pingcap/tidb/issues/37176) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    バージョン6.4.0では、範囲を構築するオプティマイザの最大メモリ使用量を制限するために、システム変数[`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)が導入されました。メモリ使用量がこの制限を超えると、オプティマイザはメモリ消費量を削減するために、より正確な範囲ではなく、より粗い粒度の範囲を構築します。SQL文に`IN`条件が多数ある場合、この最適化によりコンパイル時のメモリ使用量を大幅に削減し、システムの安定性を確保できます。

    詳細については、 [ユーザー向けドキュメント](/system-variables.md#tidb_opt_range_max_size-new-in-v640)を参照してください。

-   統計情報の同期読み込みをサポート (GA) [#37434](https://github.com/pingcap/tidb/issues/37434) @[chrysan](https://github.com/chrysan)

    TiDB v6.4.0では、統計情報の同期読み込み機能がデフォルトで有効になっています。この機能により、SQL文の実行時に、ヒストグラム、TopN、Count-Min Sketch統計情報などの大規模な統計情報をメモリに同期的に読み込むことが可能になり、SQL最適化のための統計情報の網羅性が向上します。

    詳細については、 [ユーザー向けドキュメント](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)を参照してください。

-   バッチ書き込みリクエストが軽量トランザクション書き込みの応答時間に与える影響を軽減する [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

    一部のシステムのビジネスロジックでは、定期的なバッチ DML タスクが必要ですが、これらのバッチ書き込みタスクを処理すると、オンライン トランザクションのレイテンシーが増加します。v6.3.0 では、TiKV はハイブリッド ワークロード シナリオでの読み取り要求のスケジューリングを最適化するため、 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)構成項目を有効にすると、TiKV がすべての読み取り要求に対して UnifyReadPool スレッド プールのサイズを自動的に調整します。v6.4.0 では、TiKV は書き込み要求も動的に識別して優先順位を付け、1 回のポーリングで Apply スレッドが 1 つの FSM (有限状態機械) に対して書き込むことができる最大バイト数を制御できるため、バッチ書き込み要求がトランザクション書き込みの応答時間に与える影響を軽減できます。

### 使いやすさ {#ease-of-use}

-   TiKV API V2 が一般公開 (GA) [#11745](https://github.com/tikv/tikv/issues/11745) @[pingyu](https://github.com/pingyu)

    バージョン6.1.0より前のTiKVは、クライアントから渡された生データのみを保存するため、基本的なキーバリューの読み書き機能しか提供していませんでした。さらに、異なるコーディング方式とスコープのないデータ範囲のため、TiDB、トランザクションKV、およびRawKVを同じTiKVクラスタで同時に使用することはできません。そのため、複数のクラスタが必要となり、マシンコストと導入コストが増加します。

    TiKV API V2は、新しいRawKVストレージフォーマットとアクセスインターフェースを提供し、以下の利点をもたらします。

    -   MVCCにデータを保存する際に、記録されたデータの変更タイムスタンプを付加します。このタイムスタンプに基づいて変更データキャプチャ（CDC）が実装されます。この機能は実験的であり、詳細は[TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)に記載されています。
    -   データはさまざまな用途に応じて範囲が定められており、API V2では、単一のクラスタ内でTiDB、トランザクションKV、およびRawKVアプリケーションが共存することをサポートしています。
    -   マルチテナントなどの機能をサポートするために、キースペースフィールドを予約してください。

    TiKV API V2を有効にするには、TiKV設定ファイルの`api-version = 2`セクションに`[storage]` を設定します。

    詳細については、 [ユーザー向けドキュメント](/tikv-configuration-file.md#api-version-new-in-v610)を参照してください。

-   TiFlashデータ複製進捗状況の精度向上 [#4902](https://github.com/pingcap/tiflash/issues/4902) @[hehechen](https://github.com/hehechen)

    TiDBでは、 `PROGRESS`テーブルの`INFORMATION_SCHEMA.TIFLASH_REPLICA`フィールドは、TiKVの対応するテーブルからTiFlashレプリカへのデータレプリケーションの進行状況をTiFlashために使用されます。以前のTiDBバージョンでは、 `PROCESS`フィールドは、 TiFlashレプリカの作成中のデータレプリケーションの進行状況のみを提供していました。TiFlashレプリカが作成された後、TiKVの対応するテーブルに新しいデータがインポートされた場合、このフィールドは更新されず、新しいデータのTiKVからTiFlashへのレプリケーションの進行状況は表示されません。

    バージョン6.4.0では、TiDBはTiFlashレプリカのデータレプリケーション進捗状況の更新メカニズムを改善しました。TiFlashレプリカが作成された後、TiKVの対応するテーブルに新しいデータがインポートされると、 [`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)テーブルの`PROGRESS`値が更新され、新しいデータに対するTiKVからTiFlashへの実際のレプリケーション進捗状況が表示されます。この改善により、 TiFlashデータレプリケーションの実際の進捗状況を簡単に確認できます。

    詳細については、 [ユーザー向けドキュメント](/information-schema/information-schema-tiflash-replica.md)を参照してください。

### MySQLとの互換性 {#mysql-compatibility}

-   線形ハッシュパーティショニング構文との互換性を確保する [#38450](https://github.com/pingcap/tidb/issues/38450) @[mjonss](https://github.com/mjonss)

    以前のバージョンでは、TiDB はハッシュ、レンジ、List パーティショニングをサポートしていました。 v6.4.0 以降、TiDB は[MySQL 線形ハッシュパーティショニング](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)の構文とも互換性があります。

    TiDBでは、MySQLのリニアハッシュパーティションの既存のDDLステートメントを直接実行でき、TiDBは対応するハッシュパーティションテーブルを作成します（TiDB内部にはリニアハッシュパーティションは存在しません）。また、MySQLのリニアハッシュパーティションの既存のDMLステートメントを直接実行することもでき、TiDBは対応するTiDBハッシュパーティションのクエリ結果を正常に返します。この機能により、TiDBの構文とMySQLのリニアハッシュパーティションとの互換性が確保され、MySQLベースのアプリケーションからTiDBへのスムーズな移行が可能になります。

    パーティション数が2のべき乗である場合、TiDBハッシュパーティションテーブルの行は、MySQLリニアハッシュパーティションテーブルの行と同じように分散されます。そうでない場合、TiDBにおけるこれらの行の分散はMySQLとは異なります。

    詳細については、 [ユーザー向けドキュメント](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)を参照してください。

-   高性能かつグローバルに単調な`AUTO_INCREMENT` (実験的) をサポート [#38442](https://github.com/pingcap/tidb/issues/38442) @[tiancaiamao](https://github.com/tiancaiamao)

    TiDB v6.4.0 では`AUTO_INCREMENT` MySQL 互換モードが導入されました。このモードでは、すべての TiDB インスタンスで ID が単調増加することを保証する、集中型のAUTO_INCREMENT ID 割り当てサービスが導入されます。この機能により、AUTO_INCREMENT ID によるクエリ結果のソートが容易になります。MySQL 互換モードを使用するには、テーブルを作成する際に`AUTO_ID_CACHE`を`1`に設定する必要があります。以下に例を示します。

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    詳細については、[ユーザー向けドキュメント](/auto-increment.md#mysql-compatibility-mode)を参照してください。

-   JSON型における配列データの範囲選択のサポート [#13644](https://github.com/tikv/tikv/issues/13644) @[YangKeao](https://github.com/YangKeao)

    v6.4.0 以降、TiDB で MySQL 互換の[範囲選択構文](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths)を使用できるようになりました。

    -   キーワード`to`を使用すると、配列要素の開始位置と終了位置を指定したり、配列内の連続した範囲の要素を選択したりできます。 `0`を使用すると、配列の最初の要素の位置を指定できます。たとえば、 `$[0 to 2]`を使用すると、配列の最初の 3 つの要素を選択できます。

    -   キーワード`last`を使用すると、配列の最後の要素の位置を指定できます。これにより、右から左への位置設定が可能になります。たとえば、 `$[last-2 to last]`を使用すると、配列の最後の 3 つの要素を選択できます。

    この機能により、SQL文の記述プロセスが簡素化され、JSON型の互換性がさらに向上し、MySQLアプリケーションをTiDBに移行する際の難易度が軽減されます。

-   データベースユーザー向けの追加説明の追加をサポート [#38172](https://github.com/pingcap/tidb/issues/38172) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDB v6.4 では、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)を使用して、データベース ユーザーの追加の説明を追加できます。TiDB は 2 つの説明形式を提供します。 `COMMENT`を使用してテキスト コメントを追加したり、 `ATTRIBUTE`を使用して JSON 形式の構造化属性セットを追加したりできます。

    さらに、TiDB v6.4.0では[`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md)テーブルが追加され、ユーザーコメントやユーザー属性の情報を表示できるようになりました。

    ```sql
    CREATE USER 'newuser1'@'%' COMMENT 'This user is created only for test';
    CREATE USER 'newuser2'@'%' ATTRIBUTE '{"email": "user@pingcap.com"}';
    SELECT * FROM INFORMATION_SCHEMA.USER_ATTRIBUTES;
    ```

    ```sql
    +-----------+------+---------------------------------------------------+
    | USER      | HOST | ATTRIBUTE                                         |
    +-----------+------+---------------------------------------------------+
    | newuser1  | %    | {"comment": "This user is created only for test"} |
    | newuser1  | %    | {"email": "user@pingcap.com"}                     |
    +-----------+------+---------------------------------------------------+
    2 rows in set (0.00 sec)
    ```

    この機能により、TiDBとMySQL構文の互換性が向上し、TiDBをMySQLエコシステムのツールやプラットフォームに容易に統合できるようになります。

### バックアップと復元 {#backup-and-restore}

-   EBS ボリューム スナップショットを使用した TiDB クラスターのバックアップをサポート [#33849](https://github.com/pingcap/tidb/issues/33849) @[fengou1](https://github.com/fengou1)

    TiDB クラスターが EKS 上にデプロイされ、AWS EBS ボリュームを使用している場合、TiDB クラスター データのバックアップ時に以下の要件を満たす必要がある場合は、 TiDB Operatorを使用してボリューム スナップショットとメタデータによるデータを AWS S3 にバックアップできます。

    -   バックアップの影響を最小限に抑える。例えば、QPSとトランザクションレイテンシーへの影響を5%未満に抑え、クラスタのCPUとメモリを消費しないようにする。
    -   短時間でデータのバックアップと復元が可能です。例えば、1時間以内にバックアップを完了し、2時間以内にデータを復元できます。

    詳細については、 [ユーザー向けドキュメント](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)を参照してください。

### データ移行 {#data-migration}

-   DMは、下流のマージ済みテーブルの拡張列に上流のデータソース情報を書き込むことをサポートしています [#37797](https://github.com/pingcap/tidb/issues/37797) @[lichunzhu](https://github.com/lichunzhu)

    上流から TiDB へシャーディングされたスキーマとテーブルをマージする際、ターゲット テーブルに複数のフィールド (拡張列) を手動で追加し、DM タスクの設定時にその値を指定できます。たとえば、拡張列に上流のシャーディングされたスキーマとテーブルの名前を指定すると、DM によって下流に書き込まれるデータにはスキーマ名とテーブル名が含まれます。下流のデータが通常と異なる場合、この機能を使用して、スキーマ名やテーブル名など、ターゲット テーブル内のデータ ソース情報をすばやく特定できます。

    詳細については、 [テーブル、スキーマ、ソース情報を抽出し、マージされたテーブルに書き込みます](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)

-   DMは、必須チェック項目の一部をオプションに変更することで、事前チェックメカニズムを最適化します [#7333](https://github.com/pingcap/tiflow/issues/7333) @[lichunzhu](https://github.com/lichunzhu)

    データ移行タスクをスムーズに実行するために、DMはタスク開始時に自動的に[事前チェック](/dm/dm-precheck.md)トリガーし、チェック結果を返します。DMは事前チェックに合格した後にのみ移行を開始します。

    バージョン6.4.0では、DMは以下の3つのチェック項目を必須から任意に変更し、事前チェックの合格率を向上させました。

    -   上流のテーブルがTiDBと互換性のない文字セットを使用していないか確認してください。
    -   上流テーブルに主キー制約または一意キー制約があるかどうかを確認してください。
    -   プライマリ/セカンダリ構成で、アップストリームデータベースのデータベースID `server_id`が指定されているかどうかを確認してください。

-   DMは、増分移行タスクのオプションパラメータとしてbinlogの位置とGTIDを設定することをサポートします [#7393](https://github.com/pingcap/tiflow/issues/7393) @[GMHDBJD](https://github.com/GMHDBJD)

    バージョン6.4.0以降では、binlogの位置やGTIDを指定せずに、増分移行を直接実行できます。DMは、タスク開始後にアップストリームから生成されたbinlogファイルを自動的に取得し、これらの増分データをダウンストリームに移行します。これにより、ユーザーは面倒な理解や複雑な設定から解放されます。

    詳細については、 [DM 高度タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

-   DMが移行タスクのステータスインジケーターを追加 [#7343](https://github.com/pingcap/tiflow/issues/7343) @[okJiang](https://github.com/okJiang)

    バージョン6.4.0では、DMに移行タスクのパフォーマンスと進捗状況を示す指標がさらに追加され、移行のパフォーマンスと進捗状況をより直感的に把握できるようになり、トラブルシューティングの際の参考情報としても役立ちます。

    -   データインポートおよびエクスポートのパフォーマンスを示すステータスインジケーター（バイト/秒）を追加します。
    -   下流データベースへのデータ書き込みに関するパフォーマンス指標の名前を、TPSからRPS（行/秒）に変更します。
    -   DMの完全移行タスクにおけるデータエクスポートの進捗状況を示す進捗インジケーターを追加します。

    これらの指標の詳細については、 [TiDB Data Migrationにおけるクエリタスクステータス](/dm/dm-query-status.md)を参照してください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は`3.2.0`バージョンの Kafka へのデータのレプリケーションをサポートします。 [#7191](https://github.com/pingcap/tiflow/issues/7191) @[3AceShowHand](https://github.com/3AceShowHand)

    v6.4.0 以降、TiCDC は`3.2.0`バージョン以前のデータを[データをKafkaに複製する](/replicate-data-to-kafka.md)をサポートします。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                 | 変更の種類  | 説明                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`max_execution_time`](/system-variables.md#max_execution_time)                                                                     | 変更     | バージョン6.4.0より前は、この変数はすべての種類のステートメントに適用されていました。バージョン6.4.0以降は、この変数は読み取り専用ステートメントの最大実行時間のみを制御します。                                                                                                                                       |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)         | 変更     | グローバルスコープを削除し、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)設定項目を使用してデフォルト値を変更できるようにします。この変数は、TiDB が悲観的トランザクション内の一意制約をチェックするタイミングを制御します。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                 | 変更     | バージョン6.4.0以降で有効になり、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)の同時実行を制御します。デフォルト値は`64`です。                                                                                                |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)                                        | 変更     | デフォルト値を`INT_ONLY`から`ON`に変更します。これは、主キーがデフォルトでクラスター化インデックスとして作成されることを意味します。                                                                                                                                                        |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                                                         | 変更     | デフォルト値を`OFF`から`ON`に変更します。これは、コプロセッサ要求を送信するためのページング方式がデフォルトで使用されることを意味します。                                                                                                                                                           |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                               | 変更     | SESSION スコープを追加します。この変数は[プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを制御します。                                                                                                                                               |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)                                               | 変更     | デフォルト値を`0.8`から`0.7`に変更します。この変数は、tidb-server のメモリアラームをトリガーするメモリ使用率を制御します。                                                                                                                                                            |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)                                                             | 変更     | グローバルスコープを追加します。この変数は、オプティマイザが集計関数をJoin、Projection、およびUnionAllの前にプッシュダウンする最適化操作を実行するかどうかを制御します。                                                                                                                                     |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                   | 変更     | SESSIONスコープを追加します。この変数は、セッション内でキャッシュできるプランの最大数を制御します。                                                                                                                                                                               |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                           | 変更     | デフォルト値を`0`から`100`に変更します。これは、SQL 実行がデフォルトで最大 100 ミリ秒待機して、完全な列統計を同期的にロードできることを意味します。                                                                                                                                                  |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)                                 | 変更     | デフォルト値を`OFF`から`ON`に変更します。これは、完全な列統計を同期的に読み込むタイムアウトに達した後、SQL 最適化が擬似統計を使用するように戻ることを意味します。                                                                                                                                             |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640)                                                         | 新しく追加された | 前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用しているかどうかを示します。この変数は読み取り専用で、デフォルト値は`OFF`です。                                                                                                                                              |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)                 | 新しく追加された | パーティションテーブルを分析するときに TiDB が一度に[自動的に分析します](/statistics.md#automatic-update)できるパーティションの数を指定します (つまり、パーティションテーブルに関する統計を自動的に収集します)。デフォルト値は`1`です。                                                                                         |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)                                     | 新しく追加された | TiDB が[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取るかどうかを制御します。デフォルト値は`OFF`です。                                                                                                     |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640)                                                 | 新しく追加された | GOGC Tuner を有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                          |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)                                               | 新しく追加された | TiDB がチャンク オブジェクトのキャッシュを有効にするかどうかを制御します。デフォルト値は`ON`で、これは TiDB がキャッシュされたチャンク オブジェクトの使用を優先し、要求されたオブジェクトがキャッシュにない場合にのみシステムに要求することを意味します。値が`OFF`の場合、TiDB はシステムから直接チャンク オブジェクトを要求します。                                                    |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | 新しく追加された | プリペアドプランキャッシュにキャッシュされた実行プランによって消費されたメモリをカウントするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                             |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)                                                             | 新しく追加された | デフォルト値は`0`です。tidb_enable_external_ts_read [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) `ON`に設定されている場合、TiDB はこの変数で指定されたタイムスタンプを持つデータを読み取ります。                                      |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640)                                           | 新しく追加された | GOGC のチューニングにおける最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC Tuner は動作を停止します。デフォルト値は`0.6`です。                                                                                                                                                |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)               | 新しく追加された | tidb-serverのメモリ使用量がメモリアラームのしきい値を超えてアラームが発生した場合、TiDBはデフォルトでは直近5件のアラーム発生時に生成されたステータスファイルのみを保持します。この件数は、この変数で調整できます。                                                                                                                   |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)                           | 新しく追加された | TiDB オプティマイザが不要なテーブル検索を回避し、クエリのパフォーマンスを向上させるために、一部のフィルタ条件をプレフィックス インデックスにプッシュダウンするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                         |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)                                               | 新しく追加された | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を指定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                             | 新しく追加された | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を制御します（実験的）。デフォルト値は`0`で、メモリ制限がないことを意味します。                                                                                                                                                            |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)                       | 新しく追加された | TiDB が GC をトリガーしようとするしきい値を制御します (実験的)。デフォルト値は`70%`です。                                                                                                                                                                               |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)                 | 新しく追加された | メモリ制限を有効にすると、TiDB は現在のインスタンスで最もメモリ使用量の多い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。デフォルト値は`134217728` (128 MiB) です。                                                                                                   |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                                   | 変更の種類  | 説明                                                                                                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `tidb_memory_usage_alarm_ratio`                                                                                                                   | 削除済み     | この設定項目は無効になりました。                                                                                                                                                        |
| TiDB           | `memory-usage-alarm-ratio`                                                                                                                        | 削除済み     | システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)に置き換えられました。この設定項目が TiDB バージョン v6.4.0 より前のバージョンで設定されていた場合、アップグレード後には有効になりません。 |
| TiDB           | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)          | 新しく追加された | システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。デフォルト値は`true`です。         |
| TiDB           | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640)                                                            | 新しく追加された | チャンク割り当てのキャッシュされたチャンクオブジェクトの最大数を制御します。デフォルト値は`64`です。                                                                                                                    |
| TiDB           | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640)                                                          | 新しく追加された | チャンク割り当てのキャッシュされた列オブジェクトの最大数を制御します。デフォルト値は`256`です。                                                                                                                      |
| TiKV           | [`cdc.raw-min-ts-outlier-threshold`](https://docs-archive.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | 非推奨      | この設定項目は無効になりました。                                                                                                                                                        |
| TiKV           | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640)                                                      | 新しく追加された | 事前割り当て済みのTSOキャッシュサイズ（期間）。デフォルト値は`3s`です。                                                                                                                                 |
| TiKV           | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)                                                  | 新しく追加された | タイムスタンプ要求におけるTSOの最大数を制御します。デフォルト値は`8192`です。                                                                                                                             |
| TiKV           | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640)                                              | 新しく追加された | Applyスレッドが1回のポーリングで1つのFSM（有限状態機械）に対して書き込める最大バイト数を制御します。デフォルト値は`32KiB`です。これはソフトリミットです。                                                                                   |
| PD             | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)                                                          | 新しく追加された | バージョン6.4.0以降で有効になり、PDがTSOの物理時刻を更新する間隔を制御します。デフォルト値は`50ms`です。                                                                                                            |
| TiFlash        | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)                                              | 変更     | 新しい値オプション`sm4-ctr`が導入されました。この設定項目が`sm4-ctr`に設定されている場合、データは保存される前に SM4 を使用して暗号化されます。                                                                                     |
| DM             | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                              | 新しく追加された | オプション。シャーディングシナリオにおいて、シャーディングされたテーブルのソース情報を抽出するために使用します。抽出された情報は、ダウンストリームのマージ済みテーブルに書き込まれ、データソースを識別するために使用されます。このパラメータを設定する場合は、事前にダウンストリームにマージ済みテーブルを手動で作成する必要があります。    |
| DM             | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                             | 新しく追加された | オプション。シャーディングシナリオにおいて、シャーディングされたスキーマのソース情報を抽出するために使用します。抽出された情報は、ダウンストリームのマージ済みテーブルに書き込まれ、データソースを識別するために使用されます。このパラメータを設定する場合は、事前にダウンストリームにマージ済みテーブルを手動で作成する必要があります。    |
| DM             | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                             | 新しく追加された | オプション。シャーディングシナリオにおいて、ソースインスタンス情報を抽出するために使用します。抽出された情報は、ダウンストリームのマージ済みテーブルに書き込まれ、データソースを識別するために使用されます。このパラメータを設定する場合は、事前にダウンストリームにマージ済みテーブルを手動で作成する必要があります。             |
| TiCDC          | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)                                                     | 変更     | デフォルト値を`table`から`none`に変更します。この変更により、レプリケーションのレイテンシーとメモリ不足（OOM）のリスクが軽減されます。さらに、TiCDC はすべてのトランザクションを分割するのではなく、一部のトランザクション（単一のトランザクションのサイズが 1024 行を超える場合）のみを分割するようになります。  |

### その他 {#others}

-   v6.4.0 以降、 `mysql.user`テーブルには、 `User_attributes`と`Token_issuer`という 2 つの新しい列が追加されています。以前の TiDB バージョンのバックアップ データから TiDB v6.4.0 に[`mysql`スキーマ内のシステムテーブルを復元します](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)と、 BR は`column count mismatch`テーブルの`mysql.user`エラーを報告します。 `mysql`スキーマ内のシステム テーブルを復元しない場合、このエラーは報告されません。
-   名前が「 [Dumplingのエクスポートファイルの形式](/dumpling-overview.md#format-of-exported-files)一致するものの、末尾が非圧縮形式（例`test-schema-create.sql.origin`および`test.table-schema.sql.origin` ）で終わるファイルについては、 TiDB Lightning の処理方法が変更されました。v6.4.0 より前は、インポート対象ファイルにこのようなファイルが含まれている場合、TiDB Lightning はこれらのファイルのインポートをスキップしていました。v6.4.0 以降では、 TiDB Lightning TiDB Lightning はこれらのファイルがサポートされていない圧縮形式を使用しているとみなすため、インポート処理は失敗します。
-   バージョン6.4.0以降、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`の権限を持つチェンジフィードのみがTiCDC Syncpoint機能を使用できます。

## 改善点 {#improvements}

-   TiDB

    -   何もしない変数`lc_messages`の変更を許可する [#38231](https://github.com/pingcap/tidb/issues/38231) @[djshow832](https://github.com/djshow832)
    -   `AUTO_RANDOM`列をクラスター化複合インデックスの最初の列としてサポートする [#38572](https://github.com/pingcap/tidb/issues/38572) @[tangenta](https://github.com/tangenta)
    -   内部トランザクションの再試行では悲観的トランザクションを使用して、再試行の失敗を回避し、時間の消費を削減します [#38136](https://github.com/pingcap/tidb/issues/38136) @[jackysp](https://github.com/jackysp)

-   TiKV

    -   Applyスレッドが1回のポーリングで1つの有限状態マシンに対して書き込める最大バイト数を制御し、Applyスレッドが大量のデータを書き込む際のRaftstoreの混雑を緩和するために、新しい設定項目`apply-yield-write-size`を追加します。 [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)
    -   リージョンのリーダーを移行する前にエントリキャッシュをウォームアップして、リーダー転送プロセス中のQPSジッターを回避する [#13060](https://github.com/tikv/tikv/issues/13060) @[cosven](https://github.com/cosven)
    -   `json_constrains`演算子をコプロセッサーにプッシュダウンするサポート [#13592](https://github.com/tikv/tikv/issues/13592) @[lizhenhuan](https://github.com/lizhenhuan)
    -   `CausalTsProvider`に非同期関数を追加して、一部のシナリオでのフラッシュパフォーマンスを改善します [#13428](https://github.com/tikv/tikv/issues/13428) @[zeminzhou](https://github.com/zeminzhou)

-   PD

    -   ホットリージョンスケジューラのv2アルゴリズムがGAになります。一部のシナリオでは、v2アルゴリズムは、設定された両方の次元でより良いバランスを実現し、無効なスケジューリングを減らすことができます。 [#5021](https://github.com/tikv/pd/issues/5021) @[hundundm](https://github.com/hundundm)
    -   早期のタイムアウトを回避するためにオペレーター ステップのタイムアウト メカニズムを最適化します [#5596](https://github.com/tikv/pd/issues/5596) @[bufferflies](https://github.com/bufferflies)
    -   大規模クラスターでのスケジューラーのパフォーマンスを向上 [#5473](https://github.com/tikv/pd/issues/5473) @[bufferflies](https://github.com/bufferflies)
    -   PD で提供されていない外部タイムスタンプの使用をサポートする [#5637](https://github.com/tikv/pd/issues/5637) @[lhy1024](https://github.com/lhy1024)

-   TiFlash

    -   TiFlash MPP エラー処理ロジックをリファクタリングして、MPP の安定性をさらに向上させます。 [#5095](https://github.com/pingcap/tiflash/issues/5095) @[windtalker](https://github.com/windtalker)
    -   TiFlash計算プロセスのソートを最適化し、Joinと集計のキー処理を最適化します [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    -   デコード時のメモリ使用量を最適化し、冗長な転送列を削除して結合パフォーマンスを向上させる [#6157](https://github.com/pingcap/tiflash/issues/6157) @[yibin87](https://github.com/yibin87)

-   ツール

    -   TiDB Dashboard

        -   TiFlashのメトリクスをモニタリングページに表示できるようにし、そのページでのメトリクスの表示を最適化する [#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @[YiniXu9506](https://github.com/YiniXu9506)
        -   スロークエリリストとSQLステートメントリストの結果の行数を表示する [#1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @[baurine](https://github.com/baurine)
        -   Alertmanagerが存在しない場合にAlertmanagerエラーを報告しないようにダッシュボードを最適化する [#1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @[baurine](https://github.com/baurine)

    -   Backup & Restore (BR)

        -   メタデータの読み込みメカニズムを改善します。メタデータは必要な場合にのみメモリに読み込まれるため、PITR中のメモリ使用量が大幅に削減されます。 [#38404](https://github.com/pingcap/tidb/issues/38404) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   ExchangeパーティションDDLステートメントの複製をサポートする [#639](https://github.com/pingcap/tiflow/issues/639) @[asddongmen](https://github.com/asddongmen)
        -   MQ シンク モジュールの非バッチ送信パフォーマンスを向上 [#7353](https://github.com/pingcap/tiflow/issues/7353) @[Rustin170506](https://github.com/Rustin170506)
        -   テーブルに多数のリージョンがある場合の TiCDC プーラーのパフォーマンスを改善[#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @[sdojjy](https://github.com/sdojjy)
        -   Syncpointが有効になっている場合に`tidb_enable_external_ts_read`変数を使用して下流のTiDBの履歴データを読み取ることをサポートする [#7419](https://github.com/pingcap/tiflow/issues/7419) @[asddongmen](https://github.com/asddongmen)
        -   トランザクション分割を有効にし、デフォルトでセーフモードを無効にすることで、レプリケーションの安定性を向上させます [#7505](https://github.com/pingcap/tiflow/issues/7505) @[asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   役に立たない`operate-source update`コマンドを dmctl から削除します [#7246](https://github.com/pingcap/tiflow/issues/7246) @[buchuitoudegou](https://github.com/buchuitoudegou)
        -   上流データベースが TiDB と互換性のない DDL ステートメントを使用している場合に DM の完全インポートが失敗する問題を修正しました。TiDB でサポートされている DDL ステートメントを使用して、事前に TiDB でターゲット テーブルのスキーマを手動で作成することで、インポートの成功を確実にすることができます [#37984](https://github.com/pingcap/tidb/issues/37984) @[lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   スキーマファイルのスキャンを高速化するためにファイルスキャンロジックを最適化 [#38598](https://github.com/pingcap/tidb/issues/38598) @[dsdashun](https://github.com/dsdashun)

## バグ修正 {#bug-fixes}

-   TiDB

    -   新しいインデックスを作成した後に発生する可能性のあるインデックスの不整合の問題を修正します [#38165](https://github.com/pingcap/tidb/issues/38165) @[tangenta](https://github.com/tangenta)
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブルの権限の問題を修正しました [#38407](https://github.com/pingcap/tidb/issues/38407) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   `grantor`テーブルに`mysql.tables_priv`フィールドが欠落している問題を修正します [#38293](https://github.com/pingcap/tidb/issues/38293) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正 [#38170](https://github.com/pingcap/tidb/issues/38170) @[wjhuang2016](https://github.com/wjhuang2016)
    -   共通テーブル式の和集合の結果が間違っている可能性がある問題を修正 [#37928](https://github.com/pingcap/tidb/issues/37928) @[YangKeao](https://github.com/YangKeao)
    -   **トランザクション領域番号**監視パネルの情報が正しくない問題を修正 [#38139](https://github.com/pingcap/tidb/issues/38139) @[jackysp](https://github.com/jackysp)
    -   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)内部トランザクションに影響を与える可能性がある問題を修正しました。変数のスコープを SESSION に変更しました。 [#38766](https://github.com/pingcap/tidb/issues/38766) @[ekexium](https://github.com/ekexium)
    -   クエリ内の条件が誤ってプロジェクションにプッシュダウンされる問題を修正 [#35623](https://github.com/pingcap/tidb/issues/35623) @[Reminiscent](https://github.com/Reminiscent)
    -   `isNullRejected`および`OR` `AND`のチェック結果が間違っていたためにクエリ結果が間違っていた問題を修正しました [#38304](https://github.com/pingcap/tidb/issues/38304) @[Yisaer](https://github.com/Yisaer)
    -   外部結合が削除された際に`ORDER BY`内の`GROUP_CONCAT`が考慮されず、クエリ結果が誤る問題を修正しました [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    -   結合したテーブルの再配置により誤ってプッシュダウンされた条件が破棄された際に発生する、誤ったクエリ結果の問題を修正しました。 [#38736](https://github.com/pingcap/tidb/issues/38736) @[winoros](https://github.com/winoros)

-   TiKV

    -   複数の`cgroup`および`mountinfo`が存在する場合に Gitpod で TiDB が起動に失敗する問題を修正 [#13660](https://github.com/tikv/tikv/issues/13660) @[tabokie](https://github.com/tabokie)
    -   TiKV メトリクスの間違った式を修正`tikv_gc_compaction_filtered` [#13537](https://github.com/tikv/tikv/issues/13537) @[Defined2014](https://github.com/Defined2014)
    -   異常な`delete_files_in_range` によって引き起こされたパフォーマンスの問題を修正します [#13534](https://github.com/tikv/tikv/issues/13534) @[tabokie](https://github.com/tabokie)
    -   スナップショット取得中のリース期限切れによって引き起こされる異常なリージョン競合を修正 [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   `FLASHBACK`最初のバッチで失敗したときに発生したエラーを修正します[#13672](https://github.com/tikv/tikv/issues/13672) [#13704](https://github.com/tikv/tikv/issues/13704) [#13723](https://github.com/tikv/tikv/issues/13723) @[HuSharp](https://github.com/HuSharp)

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替えを加速します [#5207](https://github.com/tikv/pd/issues/5207) @[CabinfeverB](https://github.com/CabinfeverB)

-   TiFlash

    -   PageStorage GC がページ削除マーカーを適切にクリアしない場合に発生する、WAL ファイルのサイズ超過による OOM の問題を修正 [#6163](https://github.com/pingcap/tiflash/issues/6163) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   TiDB Dashboard

        -   特定の複雑なSQL文の実行プランを照会する際のTiDBのOOM問題を修正 [#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @[baurine](https://github.com/baurine)
        -   NgMonitoringがPDノードへの接続を失った場合にTop SQLスイッチが有効にならない可能性がある問題を修正しました [#164](https://github.com/pingcap/ng-monitoring/issues/164) @[zhongzc](https://github.com/zhongzc)

    -   Backup & Restore (BR)

        -   復元プロセス中にPDリーダーが切り替わったことが原因で発生する復元失敗の問題を修正しました [#36910](https://github.com/pingcap/tidb/issues/36910) @[MoCuishle28](https://github.com/MoCuishle28)
        -   ログバックアップタスクを一時停止できない問題を修正 [#38250](https://github.com/pingcap/tidb/issues/38250) @[joccau](https://github.com/joccau)
        -   BRがログバックアップデータを削除する際に、削除すべきでないデータを誤って削除してしまう問題を修正しました [#38939](https://github.com/pingcap/tidb/issues/38939) @[leavrth](https://github.com/leavrth)
        -   Azure Blob Storage または Google Cloud Storage に保存されているログバックアップデータを初めて削除する際にBR がデータ削除に失敗する問題を修正 [#38229](https://github.com/pingcap/tidb/issues/38229) @[leavrth](https://github.com/leavrth)

    -   TiCDC

        -   `sasl-password`の結果で`changefeed query`がマスクされない問題を修正 [#7182](https://github.com/pingcap/tiflow/issues/7182) @[dveeden](https://github.com/dveeden)
        -   etcdトランザクションで操作が多すぎるとTiCDCが利用できなくなる可能性がある問題を修正 [#7131](https://github.com/pingcap/tiflow/issues/7131) @[asddongmen](https://github.com/asddongmen)
        -   リドゥログが正しく削除されない可能性がある問題を修正 [#6413](https://github.com/pingcap/tiflow/issues/6413) @[asddongmen](https://github.com/asddongmen)
        -   Kafka Sink V2 でワイドテーブルを複製するときのパフォーマンスの低下を修正 [#7344](https://github.com/pingcap/tiflow/issues/7344) @[Rustin170506](https://github.com/Rustin170506)
        -   チェックポイントtsが正しく進まない可能性がある問題を修正 [#7274](https://github.com/pingcap/tiflow/issues/7274) @[Rustin170506](https://github.com/Rustin170506)
        -   マウンターモジュールのログレベルが不適切なため、大量のログが出力される問題を修正 [#7235](https://github.com/pingcap/tiflow/issues/7235) @[Rustin170506](https://github.com/Rustin170506)
        -   TiCDCクラスターに2人のオーナーが存在する可能性がある問題を修正 [#4051](https://github.com/pingcap/tiflow/issues/4051) @[asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   DM WebUI が間違った`allow-list`パラメータを生成する問題を修正 [#7096](https://github.com/pingcap/tiflow/issues/7096) @[zoubingwu](https://github.com/zoubingwu)
        -   DMワーカーが起動または停止時にデータ競合を引き起こす確率がある問題を修正します [#6401](https://github.com/pingcap/tiflow/issues/6401) @[liumengya94](https://github.com/liumengya94)
        -   DM が`UPDATE`または`DELETE`ステートメントを複製する際に、対応する行データが存在しない場合、DM がイベントをサイレントに無視する問題を修正します。 [#6383](https://github.com/pingcap/tiflow/issues/6383) @[GMHDBJD](https://github.com/GMHDBJD)
        -   `secondsBehindMaster`コマンドを実行した後、 `query-status`フィールドが表示されない問題を修正しました [#7189](https://github.com/pingcap/tiflow/issues/7189) @[GMHDBJD](https://github.com/GMHDBJD)
        -   チェックポイントの更新時に大きなトランザクションが発生する可能性がある問題を修正しました [#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        -   フルタスクモードで、タスクが同期段階に入ってすぐに失敗した場合、DMがアップストリームのテーブルスキーマ情報を失う可能性がある問題を修正します [#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        -   整合性チェックが有効になっている場合にデッドロックが発生する可能性がある問題を修正 [#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        -   タスクの事前チェックで`SELECT`テーブルに対する`INFORMATION_SCHEMA`権限が必要になる問題を修正します。 [#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        -   TLS設定が空の場合にエラーが発生する問題を修正しました [#7384](https://github.com/pingcap/tiflow/issues/7384) @[liumengya94](https://github.com/liumengya94)

    -   TiDB Lightning

        -   `binary`エンコード形式の文字列型列を含むターゲットテーブルに Apache Parquet ファイルをインポートする際のインポートパフォーマンスの低下を修正 [#38351](https://github.com/pingcap/tidb/issues/38351) @[dsdashun](https://github.com/dsdashun)

    -   TiDBDumpling

        -   多数のテーブルをエクスポートする際にDumpling がタイムアウトする可能性がある問題を修正しました [#36549](https://github.com/pingcap/tidb/issues/36549) @[lance6716](https://github.com/lance6716)
        -   整合性ロックが有効になっているが、アップストリームにターゲットテーブルがない場合に報告されるロックエラーを修正 [#38683](https://github.com/pingcap/tidb/issues/38683) @[lance6716](https://github.com/lance6716)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   @ [645775992](https://github.com/645775992)
-   [An-DJ](https://github.com/An-DJ)
-   [AndrewDi](https://github.com/AndrewDi)
-   [erwadba](https://github.com/erwadba)
-   [fuzhe1989](https://github.com/fuzhe1989)
-   [goldwind-ting](https://github.com/goldwind-ting) (初回貢献者)
-   [h3n4l](https://github.com/h3n4l)
-   [igxlin](https://github.com/igxlin) (初回貢献者)
-   [ihcsim](https://github.com/ihcsim)
-   [JigaoLuo](https://github.com/JigaoLuo)
-   [morgo](https://github.com/morgo)
-   [Ranxy](https://github.com/Ranxy)
-   [shenqidebaozi](https://github.com/shenqidebaozi) (初回貢献者)
-   [taofengliu](https://github.com/taofengliu) (初回貢献者)
-   [TszKitLo40](https://github.com/TszKitLo40)
-   [wxbty](https://github.com/wxbty) (初回貢献者)
-   [zgcbj](https://github.com/zgcbj)

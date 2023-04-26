---
title: TiDB 6.4.0 Release Notes
---

# TiDB 6.4.0 リリースノート {#tidb-6-4-0-release-notes}

発売日：2022年11月17日

TiDB バージョン: 6.4.0-DMR

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.4.0#version-list)

v6.4.0-DMR の主な新機能と改善点は次のとおりです。

-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) (実験的) を使用して、クラスターを特定の時点に復元することをサポートします。
-   [グローバルメモリ使用量の追跡](/configure-memory-usage.md)の TiDB インスタンスをサポート (実験的)。
-   [線形ハッシュ パーティショニング構文](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)と互換性があります。
-   高性能でグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) (実験的) をサポートします。
-   [JSON タイプ](/data-type-json.md)の配列データの範囲選択をサポートします。
-   ディスク障害やスタック I/O などの極端な状況での障害回復を加速します。
-   テーブルの結合順序を決定するには、 [動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)を追加します。
-   相関サブクエリの非相関を実行するかどうかを制御するには、 [新しいオプティマイザ ヒント`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)を導入します。
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能がGAになります。
-   TiFlash は[保存時の暗号化](/encryption-at-rest.md#tiflash)の SM4 アルゴリズムをサポートしています。
-   [テーブル内の指定されたパーティションのTiFlashレプリカを即座にコンパクト化](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)への SQL ステートメントの使用をサポートします。
-   サポート[EBS ボリュームのスナップショットを使用して TiDB クラスターをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) 。
-   DM は[アップストリーム データ ソース情報をダウンストリーム マージ テーブルの拡張列に書き込む](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   テーブル内の指定されたパーティションのTiFlashレプリカを即座に圧縮するための SQL ステートメントの使用をサポート[#5315](https://github.com/pingcap/tiflash/issues/5315) @ [へへへん](https://github.com/hehechen)

    v6.2.0 以降、TiDB はTiFlashのフル テーブル レプリカで[物理データをすぐに圧縮する](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact)の機能をサポートしています。 SQL ステートメントを手動で実行する適切なタイミングを選択して、 TiFlashの物理データをすぐに圧縮できます。これにより、storageスペースを削減し、クエリのパフォーマンスを向上させることができます。 v6.4.0 では、圧縮するTiFlashレプリカ データの粒度を調整し、テーブル内の指定されたパーティションのTiFlashレプリカの圧縮をすぐにサポートします。

    SQL ステートメント`ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`を実行すると、テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮できます。

    詳細については、 [ユーザー文書](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (実験的) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @ [定義済み2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [Jmポテト](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [ヒューシャープ](https://github.com/HuSharp) @ [カルバンネオ](https://github.com/CalvinNeo)を使用して、特定の時点へのクラスターの復元をサポートします。

    `FLASHBACK CLUSTER TO TIMESTAMP`構文を使用して、ガベージ コレクション (GC) の有効期間内にクラスターを特定の時点にすばやく復元できます。この機能により、DML の誤操作を簡単かつ迅速に元に戻すことができます。たとえば、この構文を使用して、 `WHERE`句なしで誤って`DELETE`実行した後、数分で元のクラスターを復元できます。この機能はデータベースのバックアップに依存せず、さまざまな時点でのデータのロールバックをサポートして、データが変更された正確な時刻を特定します。 `FLASHBACK CLUSTER TO TIMESTAMP`データベースのバックアップを置き換えることができないことに注意してください。

    `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiCDC などのツールで実行されている PITR およびレプリケーション タスクを一時停止し、 `FLASHBACK`完了後にそれらを再開する必要があります。そうしないと、複製タスクが失敗する可能性があります。

    詳細については、 [ユーザー文書](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

-   `FLASHBACK DATABASE` [#20463](https://github.com/pingcap/tidb/issues/20463) @ [エルワドバ](https://github.com/erwadba)を使用した削除済みデータベースの復元のサポート

    `FLASHBACK DATABASE`を使用すると、ガベージコレクション(GC) の有効期間内に`DROP`によって削除されたデータベースとそのデータを復元できます。この機能は、外部ツールに依存しません。 SQL ステートメントを使用して、データとメタデータをすばやく復元できます。

    詳細については、 [ユーザー文書](/sql-statements/sql-statement-flashback-database.md)を参照してください。

### Security {#security}

-   TiFlash は保存時の暗号化に SM4 アルゴリズムをサポートします[#5953](https://github.com/pingcap/tiflash/issues/5953) @ [リデジュ](https://github.com/lidezhu)

    保存時のTiFlash暗号化に SM4 アルゴリズムを追加します。保存時の暗号化を構成する場合、 `tiflash-learner.toml`構成ファイルで`data-encryption-method`構成の値を`sm4-ctr`に設定することで、SM4 暗号化機能を有効にすることができます。

    詳細については、 [ユーザー文書](/encryption-at-rest.md#tiflash)を参照してください。

### 可観測性 {#observability}

-   クラスタ診断は GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @ [ホークソンジー](https://github.com/Hawkson-jee)になります

    TiDB ダッシュボードの[クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能は、指定された時間範囲内でクラスターに存在する可能性がある問題を診断し、診断結果とクラスター関連の負荷監視情報を[診断レポート](/dashboard/dashboard-diagnostics-report.md)に要約します。この診断レポートは、Web ページの形式になっています。ブラウザからページを保存した後、オフラインでページを閲覧し、このページのリンクを循環させることができます。

    診断レポートを使用すると、負荷、コンポーネントのステータス、消費時間、構成など、クラスターの基本的な正常性情報をすばやく理解できます。クラスターにいくつかの一般的な問題がある場合は、 [診断情報](/dashboard/dashboard-diagnostics-report.md#diagnostic-information)セクションの組み込みの自動診断の結果で原因を特定できます。

### パフォーマンス {#performance}

-   コプロセッサー・タスク[#37724](https://github.com/pingcap/tidb/issues/37724) @ [あなた06](https://github.com/you06)に並行性適応メカニズムを導入する

    コプロセッサ タスクの数が増えると、TiKV の処理速度に基づいて、TiDB は自動的に同時実行数を増やし (値[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)を調整)、コプロセッサ タスク キューを減らし、レイテンシーを減らします。

-   テーブル結合順序[#37825](https://github.com/pingcap/tidb/issues/37825) @ [ウィノロス](https://github.com/winoros)を決定する動的計画アルゴリズムを追加します。

    以前のバージョンでは、TiDB は貪欲アルゴリズムを使用してテーブルの結合順序を決定していました。 v6.4.0 では、TiDB オプティマイザーに[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)が導入されました。動的計画アルゴリズムは貪欲アルゴリズムよりも多くの結合順序を列挙できるため、より適切な実行計画を見つける可能性が高くなり、シナリオによっては SQL 実行効率が向上します。

    動的計画法アルゴリズムはより多くの時間を消費するため、TiDB 結合したテーブルの再配置アルゴリズムの選択は[`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)変数によって制御されます。 結合したテーブルの再配置に参加しているノードの数がこのしきい値よりも多い場合、TiDB は貪欲なアルゴリズムを使用します。それ以外の場合、TiDB は動的計画法アルゴリズムを使用します。

    詳細については、 [ユーザー文書](/join-reorder.md)を参照してください。

-   プレフィックス インデックスは、null 値のフィルタリングをサポートしています。 [#21145](https://github.com/pingcap/tidb/issues/21145) @ [しゅいふぁんグリーンアイズ](https://github.com/xuyifangreeneyes)

    この機能は、プレフィックス インデックスの最適化です。テーブル内の列にプレフィックス インデックスがある場合、SQL ステートメント内の列の`IS NULL`または`IS NOT NULL`条件をプレフィックスで直接フィルター処理できます。これにより、この場合のテーブル ルックアップが回避され、SQL 実行のパフォーマンスが向上します。

    詳細については、 [ユーザー文書](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)を参照してください。

-   TiDB チャンク再利用メカニズムの強化[#38606](https://github.com/pingcap/tidb/issues/38606) @ [キープラーニング20221](https://github.com/keeplearning20221)

    以前のバージョンでは、TiDB は`writechunk`関数でのみチャンクを再利用します。 TiDB v6.4.0 は、チャンク再利用メカニズムを Executor のオペレーターに拡張します。チャンクを再利用することで、TiDB はメモリの解放を頻繁に要求する必要がなくなり、一部のシナリオでは SQL クエリがより効率的に実行されます。システム変数[`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)使用して、デフォルトで有効になっているチャンク オブジェクトを再利用するかどうかを制御できます。

    詳細については、 [ユーザー文書](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)を参照してください。

-   相関サブクエリの非相関を実行するかどうかを制御する新しいオプティマイザ ヒント`NO_DECORRELATE`を導入します[#37789](https://github.com/pingcap/tidb/issues/37789) @ [時間と運命](https://github.com/time-and-fate)

    デフォルトでは、TiDB は常に相関サブクエリを書き換えて非相関を実行しようとします。これにより、通常は実行効率が向上します。ただし、一部のシナリオでは、非相関化によって実行効率が低下します。 v6.4.0 では、TiDB はオプティマイザー ヒント`NO_DECORRELATE`を導入して、特定のクエリ ブロックに対して非相関を実行しないようにオプティマイザーに指示し、一部のシナリオでクエリのパフォーマンスを向上させます。

    詳細については、 [ユーザー文書](/optimizer-hints.md#no_decorrelate)を参照してください。

-   パーティション化されたテーブルでの統計収集のパフォーマンスを向上させます[#37977](https://github.com/pingcap/tidb/issues/37977) @ [イサール](https://github.com/Yisaer)

    v6.4.0 では、TiDB は分割されたテーブルの統計を収集する戦略を最適化します。システム変数[`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)を使用して、パーティション化されたテーブルの統計を並行して収集する同時実行性を設定し、収集を高速化し、分析時間を短縮できます。

### 安定性 {#stability}

-   ディスク障害やスタック I/O [#13648](https://github.com/tikv/tikv/issues/13648) @ [Lykxサシネーター](https://github.com/LykxSassinator)などの極端な状況での障害回復を加速

    企業ユーザーにとって、データベースの可用性は最も重要な指標の 1 つです。複雑なハードウェア環境において、障害を迅速に検出して回復する方法は、常にデータベースの可用性に関する課題の 1 つです。 v6.4.0 では、TiDB は TiKV ノードの状態検出メカニズムを完全に最適化します。ディスク障害やスタック I/O などの極端な状況でも、TiDB はノードの状態を迅速に報告し、アクティブ ウェイクアップ メカニズムを使用して事前にLeader選出を開始し、クラスターの自己修復を加速します。この最適化により、TiDB はディスク障害の場合にクラスターの復旧時間を約 50% 短縮できます。

-   TiDBメモリ使用量のグローバル制御[#37816](https://github.com/pingcap/tidb/issues/37816) @ [wshwsh12](https://github.com/wshwsh12)

    v6.4.0 では、TiDB は、TiDB インスタンスのグローバルメモリ使用量を追跡する実験的機能として、メモリ使用量のグローバル コントロールを導入します。システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用して、グローバルメモリ使用量の上限を設定できます。メモリ使用量がしきい値に達すると、TiDB はより多くの空きメモリを回収して解放しようとします。メモリ使用量がしきい値を超えると、TiDB はメモリ使用量が最も多い SQL 操作を特定してキャンセルし、過剰なメモリ使用量によって引き起こされるシステムの問題を回避します。

    TiDB インスタンスのメモリ消費に潜在的なリスクがある場合、TiDB は事前に診断情報を収集し、指定されたディレクトリに書き込み、問題の診断を容易にします。同時に、TiDB はシステム テーブル ビュー[`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)と[`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)を提供し、メモリ使用量と操作履歴を表示して、メモリ使用量をよりよく理解するのに役立ちます。

    グローバルメモリコントロールは、TiDBメモリ管理のマイルストーンです。インスタンスのグローバル ビューを導入し、メモリの体系的な管理を採用することで、より重要なシナリオでデータベースの安定性とサービスの可用性を大幅に向上させることができます。

    詳細については、 [ユーザー文書](/configure-memory-usage.md)を参照してください。

-   範囲構築オプティマイザ[#37176](https://github.com/pingcap/tidb/issues/37176) @ [しゅいふぁんグリーンアイズ](https://github.com/xuyifangreeneyes)のメモリ使用量を制御します

    v6.4.0 では、範囲を構築するオプティマイザの最大メモリ使用量を制限するために、システム変数[`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)が導入されました。メモリ使用量が制限を超えると、オプティマイザは、より正確な範囲ではなく、より粗い範囲を構築してメモリ消費を削減します。 SQL ステートメントに`IN`の条件が多数ある場合、この最適化により、コンパイルのメモリ使用量を大幅に削減し、システムの安定性を確保できます。

    詳細については、 [ユーザー文書](/system-variables.md#tidb_opt_range_max_size-new-in-v640)を参照してください。

-   統計の同期ロードをサポート (GA) [#37434](https://github.com/pingcap/tidb/issues/37434) @ [クリサン](https://github.com/chrysan)

    TiDB v6.4.0 では、統計の同期読み込み機能がデフォルトで有効になっています。この機能により、TiDB は、SQL ステートメントの実行時に大規模な統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期的にロードできるようになり、SQL 最適化のための統計の完全性が向上します。

    詳細については、 [ユーザー文書](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)を参照してください。

-   軽量トランザクション書き込みの応答時間に対するバッチ書き込み要求の影響を軽減する[#13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

    一部のシステムのビジネス ロジックでは、定期的なバッチ DML タスクが必要ですが、これらのバッチ書き込みタスクを処理すると、オンライン トランザクションのレイテンシーが長くなります。 v6.3.0 では、TiKV はハイブリッド ワークロード シナリオで読み取り要求のスケジューリングを最適化するため、 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)構成項目を有効にして、TiKV がすべての読み取り要求の UnifyReadPool スレッド プールのサイズを自動的に調整できるようにします。 v6.4.0 では、TiKV は書き込み要求も動的に識別して優先順位を付けることができ、適用スレッドが 1 回のポーリングで 1 つの FSM (有限状態マシン) に書き込むことができる最大バイト数を制御できるため、バッチ書き込み要求の影響を軽減できます。トランザクション書き込みの応答時間。

### 使いやすさ {#ease-of-use}

-   TiKV API V2 の一般提供 (GA) [#11745](https://github.com/tikv/tikv/issues/11745) @ [ピンギュ](https://github.com/pingyu)

    v6.1.0 より前の TiKV は、クライアントから渡された生データのみを保存するため、基本的なキー値の読み取りおよび書き込み機能のみを提供します。さらに、コーディング方法が異なり、データ範囲が限定されていないため、TiDB、Transactional KV、RawKV を同じ TiKV クラスターで同時に使用することはできません。代わりに、この場合は複数のクラスターが必要になるため、マシンと展開のコストが増加します。

    TiKV API V2 は、新しい RawKVstorage形式とアクセス インターフェイスを提供し、次の利点を提供します。

    -   変更データ キャプチャ (CDC) の実装に基づいて、記録されたデータの変更タイムスタンプと共にデータを MVCC に保存します。この機能は実験的であり、詳細は[TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)で説明されています。
    -   データはさまざまな用途に応じてスコープが設定され、API V2 は、単一のクラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
    -   マルチテナンシーなどの機能をサポートするために、キー スペース フィールドを予約します。

    TiKV API V2 を有効にするには、TiKV 構成ファイルの`[storage]`セクションに`api-version = 2`を設定します。

    詳細については、 [ユーザー文書](/tikv-configuration-file.md#api-version-new-in-v610)を参照してください。

-   TiFlashデータ レプリケーションの進行状況の精度を向上させる[#4902](https://github.com/pingcap/tiflash/issues/4902) @ [へへへん](https://github.com/hehechen)

    TiDB では、 `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの`PROGRESS`フィールドを使用して、TiKV の対応するテーブルからTiFlashレプリカへのデータ複製の進行状況を示します。以前の TiDB バージョンでは、 `PROCESS`フィールドは、 TiFlashレプリカの作成中のデータ複製の進行状況のみを提供します。 TiFlashレプリカが作成された後、新しいデータが TiKV の対応するテーブルにインポートされた場合、このフィールドは更新されず、新しいデータの TiKV からTiFlashへのレプリケーションの進行状況が表示されません。

    v6.4.0 では、TiDB はTiFlashレプリカのデータ複製進行状況の更新メカニズムを改善します。 TiFlashレプリカが作成された後、新しいデータが TiKV の対応するテーブルにインポートされると、 [`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)テーブルの`PROGRESS`値が更新され、新しいデータの TiKV からTiFlashへの実際のレプリケーションの進行状況が表示されます。この改善により、 TiFlashデータ複製の実際の進行状況を簡単に表示できます。

    詳細については、 [ユーザー文書](/information-schema/information-schema-tiflash-replica.md)を参照してください。

### MySQL の互換性 {#mysql-compatibility}

-   Linear Hash パーティショニング構文[#38450](https://github.com/pingcap/tidb/issues/38450) @ [ミヨンス](https://github.com/mjonss)と互換性がある

    以前のバージョンでは、TiDB は Hash、Range、およびList パーティショニングをサポートしていました。 v6.4.0 以降、TiDB は[MySQL 線形ハッシュ パーティショニング](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)の構文とも互換性があります。

    TiDB では、MySQL リニア ハッシュ パーティションの既存の DDL ステートメントを直接実行でき、TiDB は対応するハッシュ パーティション テーブルを作成します (TiDB 内にリニア ハッシュ パーティションがないことに注意してください)。また、MySQL Linear Hash パーティションの既存の DML ステートメントを直接実行することもできます。TiDB は、対応する TiDB Hash パーティションのクエリ結果を正常に返します。この機能により、TiDB 構文と MySQL Linear Hash パーティションとの互換性が確保され、MySQL ベースのアプリケーションから TiDB へのシームレスな移行が容易になります。

    パーティションの数が 2 の累乗である場合、TiDB ハッシュパーティションテーブルテーブルの行は、MySQL リニア ハッシュパーティションテーブルと同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は MySQL とは異なります。

    詳細については、 [ユーザー文書](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)を参照してください。

-   高性能でグローバルに単調な`AUTO_INCREMENT` (実験的) [#38442](https://github.com/pingcap/tidb/issues/38442) @ [ティアンカイマオ](https://github.com/tiancaiamao)をサポート

    TiDB v6.4.0 では、 `AUTO_INCREMENT` MySQL 互換モードが導入されています。このモードでは、すべての TiDB インスタンスで ID が単調に増加することを保証する集中自動インクリメント ID 割り当てサービスが導入されます。この機能により、クエリ結果を自動インクリメント ID で簡単に並べ替えることができます。 MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` ～ `1`を設定する必要があります。次に例を示します。

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    詳細については、 [ユーザー文書](/auto-increment.md#mysql-compatibility-mode)を参照してください。

-   JSON 型[#13644](https://github.com/tikv/tikv/issues/13644) @ [ヤンケアオ](https://github.com/YangKeao)の配列データの範囲選択をサポート

    v6.4.0 から、MySQL 互換の[範囲選択構文](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths) TiDB で使用できます。

    -   キーワード`to`を使用すると、配列要素の開始位置と終了位置を指定し、配列内の連続した範囲の要素を選択できます。 `0`を使用すると、配列内の最初の要素の位置を指定できます。たとえば、 `$[0 to 2]`を使用すると、配列の最初の 3 つの要素を選択できます。

    -   キーワード`last`を使用すると、配列内の最後の要素の位置を指定できます。これにより、位置を右から左に設定できます。たとえば、 `$[last-2 to last]`を使用すると、配列の最後の 3 つの要素を選択できます。

    この機能により、SQL ステートメントを記述するプロセスが簡素化され、JSON 型の互換性がさらに向上し、MySQL アプリケーションを TiDB に移行する際の困難が軽減されます。

-   データベース ユーザーの追加説明の追加をサポート[#38172](https://github.com/pingcap/tidb/issues/38172) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)

    TiDB v6.4 では、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)を使用してデータベース ユーザーの説明を追加できます。 TiDB は 2 つの記述形式を提供します。 `COMMENT`を使用してテキスト コメントを追加し、 `ATTRIBUTE`を使用して一連の構造化属性を JSON 形式で追加できます。

    さらに、TiDB v6.4.0 では、ユーザーのコメントとユーザー属性の情報を表示できる[`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md)テーブルが追加されています。

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

    この機能により、MySQL 構文との TiDB の互換性が向上し、TiDB を MySQL エコシステムのツールまたはプラットフォームに簡単に統合できるようになります。

### バックアップと復元 {#backup-and-restore}

-   EBS ボリューム スナップショット[#33849](https://github.com/pingcap/tidb/issues/33849) @ [fengou1](https://github.com/fengou1)を使用した TiDB クラスターのバックアップのサポート

    TiDB クラスターが EKS にデプロイされ、AWS EBS ボリュームを使用し、TiDB クラスター データをバックアップする際に次の要件がある場合、 TiDB Operator を使用して、ボリューム スナップショットとメタデータによってデータを AWS S3 にバックアップできます。

    -   バックアップの影響を最小限に抑えます。たとえば、QPS とトランザクションのレイテンシーへの影響を 5% 未満に保ち、クラスターの CPU とメモリを占有しないようにします。
    -   短時間でデータをバックアップおよび復元します。たとえば、バックアップを 1 時間以内に完了し、データを 2 時間以内に復元します。

    詳細については、 [ユーザー文書](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)を参照してください。

### データ移行 {#data-migration}

-   DM は、ダウンストリームのマージされたテーブル[#37797](https://github.com/pingcap/tidb/issues/37797) @ [リチュンジュ](https://github.com/lichunzhu)の拡張された列へのアップストリーム データ ソース情報の書き込みをサポートします。

    分割されたスキーマとテーブルをアップストリームから TiDB にマージする場合、ターゲット テーブルに複数のフィールド (拡張列) を手動で追加し、DM タスクを構成するときにそれらの値を指定できます。たとえば、拡張された列にアップストリームのシャード スキーマとテーブルの名前を指定すると、DM によってダウンストリームに書き込まれるデータには、スキーマ名とテーブル名が含まれます。ダウンストリーム データが異常に見える場合は、この機能を使用して、スキーマ名やテーブル名など、ターゲット テーブル内のデータ ソース情報をすばやく見つけることができます。

    詳細については、 [テーブル、スキーマ、およびソース情報を抽出し、マージされたテーブルに書き込みます](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)を参照してください。

-   DM は、一部の必須チェック項目をオプション項目に変更することで、事前チェック メカニズムを最適化します[#7333](https://github.com/pingcap/tiflow/issues/7333) @ [リチュンジュ](https://github.com/lichunzhu)

    データ移行タスクをスムーズに実行するために、DM はタスクの開始時に自動的に[事前チェック](/dm/dm-precheck.md)トリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみ移行を開始します。

    v6.4.0 では、DM は次の 3 つのチェック項目を必須からオプションに変更し、事前チェックの合格率を向上させます。

    -   アップストリーム テーブルが TiDB と互換性のない文字セットを使用しているかどうかを確認します。
    -   上流のテーブルに主キー制約または一意キー制約があるかどうかを確認します
    -   プライマリ-セカンダリ構成で、上流データベースのデータベース ID `server_id`が指定されているかどうかを確認してください。

-   DM は、増分移行タスク[#7393](https://github.com/pingcap/tiflow/issues/7393) @ [GMHDBJD](https://github.com/GMHDBJD)のオプションのパラメーターとしてbinlogの位置と GTID の構成をサポートします

    v6.4.0 以降、 binlog の位置や GTID を指定せずに増分移行を直接実行できます。 DM は、タスクの開始後に生成されたbinlogファイルをアップストリームから自動的に取得し、これらの増分データをダウンストリームに移行します。これにより、ユーザーは面倒な理解と複雑な設定から解放されます。

    詳細については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

-   DM は、移行タスクのステータス インジケーターを追加します[#7343](https://github.com/pingcap/tiflow/issues/7343) @ [オクジャン](https://github.com/okJiang)

    v6.4.0 では、DM は移行タスクのパフォーマンスと進行状況のインジケーターを追加します。これにより、移行のパフォーマンスと進行状況をより直感的に理解しやすくなり、トラブルシューティングの参照が提供されます。

    -   データのインポートとエクスポートのパフォーマンスを示すステータス インジケーター (バイト/秒) を追加します。
    -   ダウンストリーム データベースにデータを書き込むためのパフォーマンス インジケーターの名前を TPS から RPS (行/秒) に変更します。
    -   DM の完全移行タスクのデータ エクスポートの進行状況を示す進行状況インジケーターを追加します。

    これらのインジケーターの詳細については、 [TiDB データ移行でのクエリ タスク ステータス](/dm/dm-query-status.md)を参照してください。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、 `3.2.0`バージョン[#7191](https://github.com/pingcap/tiflow/issues/7191) @ [3AceShowHand](https://github.com/3AceShowHand)の Kafka へのデータの複製をサポートします

    v6.4.0 から、TiCDC は`3.2.0`のバージョンのうちの[データを Kafka に複製する](/replicate-data-to-kafka.md)それ以前をサポートします。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                 | タイプを変更 | 説明                                                                                                                                                                                                                                       |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)         | 修正済み   | GLOBAL スコープを削除し、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成アイテムを使用してデフォルト値を変更できるようにします。この変数は、悲観的トランザクションで TiDB が一意の制約をチェックするタイミングを制御します。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                 | 修正済み   | v6.4.0 から有効になり、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)の同時実行を制御します。デフォルト値は`64`です。                                                                                                    |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)                                        | 修正済み   | デフォルト値を`INT_ONLY`から`ON`に変更します。これは、主キーがデフォルトでクラスター化インデックスとして作成されることを意味します。                                                                                                                                                                |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                                                         | 修正済み   | デフォルト値を`OFF`から`ON`に変更します。これは、コプロセッサー要求を送信するページングの方法がデフォルトで使用されることを意味します。                                                                                                                                                                 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                               | 修正済み   | SESSION スコープを追加します。この変数は、 [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを制御します。                                                                                                                                                  |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)                                               | 修正済み   | デフォルト値を`0.8`から`0.7`に変更します。この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を制御します。                                                                                                                                                                   |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)                                                             | 修正済み   | GLOBAL スコープを追加します。この変数は、オプティマイザーが集約関数を Join、Projection、および UnionAll の前の位置にプッシュ ダウンする最適化操作を実行するかどうかを制御します。                                                                                                                                |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                   | 修正済み   | SESSION スコープを追加します。この変数は、セッションでキャッシュできるプランの最大数を制御します。                                                                                                                                                                                    |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                           | 修正済み   | デフォルト値を`0`から`100`に変更します。これは、完全な列統計を同期的にロードするために、SQL 実行がデフォルトで最大 100 ミリ秒待機できることを意味します。                                                                                                                                                    |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)                                 | 修正済み   | デフォルト値を`OFF`から`ON`に変更します。これは、完全な列統計を同期的にロードするタイムアウトに達した後、SQL 最適化が疑似統計の使用に戻ることを意味します。                                                                                                                                                     |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640)                                                         | 新規追加   | 前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用するかどうかを示します。この変数は読み取り専用で、デフォルト値は`OFF`です。                                                                                                                                                     |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)                 | 新規追加   | パーティションテーブルを分析するときに、TiDB が一度に[自動分析](/statistics.md#automatic-update)できるパーティションの数を指定します (これは、パーティションテーブルの統計を自動的に収集することを意味します)。デフォルト値は`1`です。                                                                                               |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)                                     | 新規追加   | TiDB が[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)で指定されたタイムスタンプでデータを読み取るかどうかを制御します。デフォルト値は`OFF`です。                                                                                                            |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640)                                                 | 新規追加   | GOGC チューナーを有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                                |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)                                               | 新規追加   | TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。デフォルト値は`ON`で、TiDB はキャッシュされたチャンク オブジェクトを優先して使用し、要求されたオブジェクトがキャッシュにない場合はシステムからの要求のみを使用することを意味します。値が`OFF`場合、TiDB はシステムからチャンク オブジェクトを直接要求します。                                                        |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | 新規追加   | プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                  |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)                                                             | 新規追加   | デフォルト値は`0`です。 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)が`ON`に設定されている場合、TiDB はこの変数で指定されたタイムスタンプでデータを読み取ります。                                                                         |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640)                                           | 新規追加   | GOGC を調整するための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC チューナーは動作を停止します。デフォルト値は`0.6`です。                                                                                                                                                         |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)               | 新規追加   | tidb サーバーのメモリ使用量がメモリアラームのしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この数値は、この変数で調整できます。                                                                                                                      |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)                           | 新規追加   | 不必要なテーブル ルックアップを回避し、クエリのパフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュ ダウンするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                     |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)                                               | 新規追加   | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を指定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                     |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                             | 新規追加   | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を制御します (実験的)。デフォルト値は`0`で、メモリ制限がないことを意味します。                                                                                                                                                                |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)                       | 新規追加   | TiDB が GC をトリガーしようとするしきい値を制御します (実験的)。デフォルト値は`70%`です。                                                                                                                                                                                    |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)                 | 新規追加   | メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も多い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。デフォルト値は`134217728` (128 MiB) です。                                                                                                        |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメーター                                                                                                                          | タイプを変更 | 説明                                                                                                                                                                  |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `tidb_memory_usage_alarm_ratio`                                                                                                           | 削除しました | この構成アイテムは有効ではなくなりました。                                                                                                                                               |
| TiDB           | `memory-usage-alarm-ratio`                                                                                                                | 削除しました | システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)に置き換えられます。この構成項目が v6.4.0 より前の TiDB バージョンで構成されている場合、アップグレード後に有効になりません。    |
| TiDB           | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)  | 新規追加   | システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。デフォルト値は`true`です。     |
| TiDB           | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640)                                                    | 新規追加   | チャンク割り当ての最大キャッシュ チャンク オブジェクトを制御します。デフォルト値は`64`です。                                                                                                                   |
| TiDB           | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640)                                                  | 新規追加   | チャンク割り当ての最大キャッシュ列オブジェクトを制御します。デフォルト値は`256`です。                                                                                                                       |
| TiKV           | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | 非推奨    | この構成アイテムは有効ではなくなりました。                                                                                                                                               |
| TiKV           | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640)                                              | 新規追加   | 事前に割り当てられた TSO キャッシュ サイズ (期間)。デフォルト値は`3s`です。                                                                                                                        |
| TiKV           | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)                                          | 新規追加   | タイムスタンプ要求での TSO の最大数を制御します。デフォルト値は`8192`です。                                                                                                                         |
| TiKV           | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640)                                      | 新規追加   | 1 回のポーリングで 1 つの FSM (Finite-state Machine) に対してアプライ スレッドが書き込める最大バイト数を制御します。デフォルト値は`32KiB`です。これはソフト制限です。                                                             |
| PD             | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)                                                  | 新規追加   | v6.4.0 から有効になり、PD が TSO の物理時刻を更新する間隔を制御します。デフォルト値は`50ms`です。                                                                                                         |
| TiFlash        | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)                                      | 修正済み   | 新しい値オプション`sm4-ctr`を導入します。この設定項目が`sm4-ctr`に設定されている場合、データは保存前に SM4 を使用して暗号化されます。                                                                                      |
| DM             | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                      | 新規追加   | オプション。シャード テーブルのソース情報を抽出するためのシャーディング シナリオで使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合、事前にダウンストリームでマージされたテーブルを手動で作成する必要があります。       |
| DM             | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新規追加   | オプション。シャード スキーマのソース情報を抽出するためのシャーディング シナリオで使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合、事前にダウンストリームでマージされたテーブルを手動で作成する必要があります。       |
| DM             | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新規追加   | オプション。ソース インスタンス情報を抽出するためのシャーディング シナリオで使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合、事前にダウンストリームでマージされたテーブルを手動で作成する必要があります。          |
| TiCDC          | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)                                             | 修正済み   | デフォルト値を`table`から`none`に変更します。この変更は、レプリケーションのレイテンシーと OOM のリスクを軽減するのに役立ちます。さらに、TiCDC は、すべてのトランザクションではなく、いくつかのトランザクション (1 つのトランザクションのサイズが 1024 行を超える) のみを分割するようになりました。 |

### その他 {#others}

-   v6.4.0 以降、 `mysql.user`テーブルに`User_attributes`と`Token_issuer`の 2 つの新しい列が追加されました。 [`mysql`スキーマのシステム テーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)以前の TiDB バージョンのバックアップ データから TiDB v6.4.0 に移行すると、 BR は`mysql.user`テーブルに対して`column count mismatch`エラーを報告します。 `mysql`スキーマのシステム テーブルを復元しない場合、このエラーは報告されません。
-   名前が[Dumplingエクスポート ファイルの形式](/dumpling-overview.md#format-of-exported-files)に一致するが圧縮されていない形式 ( `test-schema-create.sql.origin`や`test.table-schema.sql.origin`など) で終わるファイルの場合、 TiDB Lightning がそれらを処理する方法が変更されます。 v6.4.0 より前では、インポートするファイルにそのようなファイルが含まれている場合、 TiDB Lightning はそのようなファイルのインポートをスキップします。 v6.4.0 以降、 TiDB Lightning は、そのようなファイルがサポートされていない圧縮形式を使用していると想定するため、インポート タスクは失敗します。
-   v6.4.0 から、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`特権を持つ changefeed のみが TiCDC 同期点機能を使用できます。

## 改良点 {#improvements}

-   TiDB

    -   noop 変数の変更を許可する`lc_messages` [#38231](https://github.com/pingcap/tidb/issues/38231) @ [DJshow832](https://github.com/djshow832)
    -   クラスター化複合インデックス[#38572](https://github.com/pingcap/tidb/issues/38572) @ [接線](https://github.com/tangenta)の最初の列として`AUTO_RANDOM`列をサポートします。
    -   内部トランザクションの再試行で悲観的トランザクションを使用して、再試行の失敗を回避し、時間の消費を削減します[#38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキスプ](https://github.com/jackysp)

-   TiKV

    -   新しい構成項目`apply-yield-write-size`を追加して、1 回のポーリングで適用スレッドが 1 つの有限状態マシンに書き込むことができる最大バイト数を制御し、適用スレッドが大量のデータを書き込むときのRaftstore の輻輳を緩和します[#13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)
    -   リーダー転送プロセス中の QPS ジッターを回避するために、リージョンのリーダーを移行する前にエントリ キャッシュをウォームアップします[#13060](https://github.com/tikv/tikv/issues/13060) @ [コスヴェン](https://github.com/cosven)
    -   `json_constains`オペレーターのコプロセッサー[#13592](https://github.com/tikv/tikv/issues/13592) @ [立振歓](https://github.com/lizhenhuan)へのプッシュダウンをサポート
    -   `CausalTsProvider`の非同期関数を追加して、いくつかのシナリオでフラッシュのパフォーマンスを向上させます[#13428](https://github.com/tikv/tikv/issues/13428) @ [ゼミン州](https://github.com/zeminzhou)

-   PD

    -   ホットリージョンスケジューラの v2 アルゴリズムが GA になります。一部のシナリオでは、v2 アルゴリズムは、構成された両方のディメンションのバランスを改善し、無効なスケジューリング[#5021](https://github.com/tikv/pd/issues/5021) @ [HundunDM](https://github.com/hundundm)を減らすことができます。
    -   早期タイムアウト[#5596](https://github.com/tikv/pd/issues/5596) @ [バタフライ](https://github.com/bufferflies)を回避するために、オペレータ ステップのタイムアウト メカニズムを最適化します。
    -   大規模なクラスターでのスケジューラーのパフォーマンスを改善する[#5473](https://github.com/tikv/pd/issues/5473) @ [バタフライ](https://github.com/bufferflies)
    -   PD [#5637](https://github.com/tikv/pd/issues/5637) @ [lhy1024](https://github.com/lhy1024)によって提供されない外部タイムスタンプを使用したサポート

-   TiFlash

    -   TiFlash MPP エラー処理ロジックをリファクタリングして、MPP [#5095](https://github.com/pingcap/tiflash/issues/5095) @ [風の語り手](https://github.com/windtalker)の安定性をさらに向上させます。
    -   TiFlash計算プロセスのソートを最適化し、Join と集計 [#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロツグ](https://github.com/solotzg)のキー処理を最適化します。
    -   デコードのメモリ使用量を最適化し、冗長な転送列を削除して、結合のパフォーマンスを向上させます[#6157](https://github.com/pingcap/tiflash/issues/6157) @ [イビン87](https://github.com/yibin87)

-   ツール

    -   TiDB ダッシュボード

        -   監視ページでのTiFlashメトリックの表示をサポートし、そのページでのメトリックの表示を最適化します[#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @ [YiniXu9506](https://github.com/YiniXu9506)
        -   スロー クエリ リストと SQL ステートメント リストの結果の行数を表示します[#1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @ [バウリン](https://github.com/baurine)
        -   Alertmanager が存在しない場合に Alertmanager エラーを報告しないようにダッシュボードを最適化する[#1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @ [バウリン](https://github.com/baurine)

    -   バックアップと復元 (BR)

        -   メタデータをロードするメカニズムを改善します。メタデータは必要な場合にのみメモリにロードされるため、PITR [#38404](https://github.com/pingcap/tidb/issues/38404) @ [ユジュンセン](https://github.com/YuJuncen)中のメモリ使用量が大幅に削減されます。

    -   TiCDC

        -   Exchange パーティション DDL ステートメントの複製をサポート[#639](https://github.com/pingcap/tiflow/issues/639) @ [アスドンメン](https://github.com/asddongmen)
        -   MQ シンク モジュール[#7353](https://github.com/pingcap/tiflow/issues/7353) @ [ハイラスチン](https://github.com/hi-rustin)の非バッチ送信パフォーマンスを改善する
        -   テーブルに多数のリージョン[#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @ [スドジ](https://github.com/sdojjy)がある場合の TiCDC プルラーのパフォーマンスを向上させます
        -   同期点が有効な場合に`tidb_enable_external_ts_read`変数を使用して、下流の TiDB での履歴データの読み取りをサポートする[#7419](https://github.com/pingcap/tiflow/issues/7419) @ [アスドンメン](https://github.com/asddongmen)
        -   デフォルトでトランザクション分割を有効にし、セーフモードを無効にして、レプリケーションの安定性を向上させます[#7505](https://github.com/pingcap/tiflow/issues/7505) @ [アスドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   dmctl [#7246](https://github.com/pingcap/tiflow/issues/7246) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)から無駄な`operate-source update`コマンドを削除します
        -   アップストリーム データベースが TiDB と互換性のない DDL ステートメントを使用している場合、DM フル インポートが失敗する問題を修正します。 TiDB でサポートされている DDL ステートメントを使用して、事前に TiDB でターゲット テーブルのスキーマを手動で作成し、確実にインポートを成功させることができます[#37984](https://github.com/pingcap/tidb/issues/37984) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   ファイル スキャン ロジックを最適化して、スキーマ ファイルのスキャンを高速化します[#38598](https://github.com/pingcap/tidb/issues/38598) @ [dsdashun](https://github.com/dsdashun)

## バグの修正 {#bug-fixes}

-   TiDB

    -   新しいインデックス[#38165](https://github.com/pingcap/tidb/issues/38165) @ [接線](https://github.com/tangenta)を作成した後に発生するインデックスの不整合の潜在的な問題を修正します。
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブル[#38407](https://github.com/pingcap/tidb/issues/38407) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の権限の問題を修正
    -   `mysql.tables_priv`テーブル[#38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   共通テーブル式の結合結果が間違っている場合がある問題を修正[#38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[#37928](https://github.com/pingcap/tidb/issues/37928) @ [ヤンケアオ](https://github.com/YangKeao)
    -   **トランザクション領域数**監視パネルの情報が正しくない問題を修正[#38139](https://github.com/pingcap/tidb/issues/38139) @ [ジャッキスプ](https://github.com/jackysp)
    -   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が内部トランザクションに影響を与える可能性がある問題を修正します。変数のスコープは SESSION に変更されます。 [#38766](https://github.com/pingcap/tidb/issues/38766) @ [エキキシウム](https://github.com/ekexium)
    -   クエリの条件が間違ってプロジェクション[#35623](https://github.com/pingcap/tidb/issues/35623) @ [思い出す](https://github.com/Reminiscent)にプッシュされる問題を修正
    -   `AND`と`OR`の間違った`isNullRejected`チェック結果が間違ったクエリ結果[#38304](https://github.com/pingcap/tidb/issues/38304) @ [イサール](https://github.com/Yisaer)を引き起こす問題を修正します。
    -   外部結合が削除されたときに`ORDER BY` in `GROUP_CONCAT`が考慮されず、間違ったクエリ結果[#18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正します
    -   結合したテーブルの再配置 [#38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄されると、間違ったクエリ結果が発生する問題を修正

-   TiKV

    -   `cgroup`と`mountinfo`レコードが複数ある場合に Gitpod で TiDB の起動に失敗する問題を修正[#13660](https://github.com/tikv/tikv/issues/13660) @ [タボキー](https://github.com/tabokie)
    -   TiKV メトリクス`tikv_gc_compaction_filtered` [#13537](https://github.com/tikv/tikv/issues/13537) @ [定義済み2014](https://github.com/Defined2014)の間違った表現を修正
    -   異常な`delete_files_in_range` [#13534](https://github.com/tikv/tikv/issues/13534) @ [タボキー](https://github.com/tabokie)によって引き起こされるパフォーマンスの問題を修正します。
    -   スナップショット取得[#13553](https://github.com/tikv/tikv/issues/13553) @ [スペード・ア・タン](https://github.com/SpadeA-Tang)中のリース期限切れによる異常なリージョン競合を修正
    -   最初のバッチで`FLASHBACK`失敗したときに発生したエラーを修正[#13672](https://github.com/tikv/tikv/issues/13672) [#13704](https://github.com/tikv/tikv/issues/13704) [#13723](https://github.com/tikv/tikv/issues/13723) @ [ヒューシャープ](https://github.com/HuSharp)

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替えを高速化します[#5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

-   TiFlash

    -   PageStorage GC がページ削除マーカーを適切にクリアしない場合に発生する大きすぎる WAL ファイルによる OOM の問題を修正します[#6163](https://github.com/pingcap/tiflash/issues/6163) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiDB ダッシュボード

        -   特定の複雑な SQL ステートメントの実行プランを照会するときの TiDB OOM の問題を修正します[#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @ [バウリン](https://github.com/baurine)
        -   NgMonitoring が PD ノード[#164](https://github.com/pingcap/ng-monitoring/issues/164) @ [中津](https://github.com/zhongzc)への接続を失うと、 Top SQLスイッチが有効にならない可能性がある問題を修正します。

    -   バックアップと復元 (BR)

        -   復元プロセス中の PD リーダー スイッチによって引き起こされる復元失敗の問題を修正します[#36910](https://github.com/pingcap/tidb/issues/36910) @ [MoCuishle28](https://github.com/MoCuishle28)
        -   ログバックアップタスクが一時停止できない問題を修正[#38250](https://github.com/pingcap/tidb/issues/38250) @ [ジョッカウ](https://github.com/joccau)
        -   BRがログバックアップデータを削除すると、削除してはいけないデータを誤って削除してしまう問題を修正[#38939](https://github.com/pingcap/tidb/issues/38939) @ [レヴルス](https://github.com/leavrth)
        -   Azure Blob Storage または Google Cloud Storage に保存されているログ バックアップ データを初めて削除するときに、 BR がデータの削除に失敗する問題を修正[#38229](https://github.com/pingcap/tidb/issues/38229) @ [レヴルス](https://github.com/leavrth)

    -   TiCDC

        -   `changefeed query`結果の`sasl-password`が[#7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴィーデン](https://github.com/dveeden)でマスクされない問題を修正
        -   etcd トランザクションであまりにも多くの操作がコミットされた場合に TiCDC が使用できなくなる可能性がある問題を修正します[#7131](https://github.com/pingcap/tiflow/issues/7131) @ [アスドンメン](https://github.com/asddongmen)
        -   REDO ログが誤って削除される可能性がある問題を修正[#6413](https://github.com/pingcap/tiflow/issues/6413) @ [アスドンメン](https://github.com/asddongmen)
        -   Kafka Sink V2 [#7344](https://github.com/pingcap/tiflow/issues/7344) @ [ハイラスチン](https://github.com/hi-rustin)で幅の広いテーブルをレプリケートするときのパフォーマンスの低下を修正
        -   チェックポイント ts が正しく進められない可能性がある問題を修正[#7274](https://github.com/pingcap/tiflow/issues/7274) @ [ハイラスチン](https://github.com/hi-rustin)
        -   マウンタモジュール[#7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイラスチン](https://github.com/hi-rustin)のログレベルが不適切なため、ログが多く出力される問題を修正
        -   TiCDC クラスターに 2 人の所有者[#4051](https://github.com/pingcap/tiflow/issues/4051) @ [アスドンメン](https://github.com/asddongmen)が存在する可能性がある問題を修正します

    -   TiDB データ移行 (DM)

        -   DM WebUIが間違った`allow-list`パラメータ[#7096](https://github.com/pingcap/tiflow/issues/7096) @ [ズービングウ](https://github.com/zoubingwu)を生成する問題を修正
        -   DM-worker が開始または停止するときにデータ競合をトリガーする特定の確率があるという問題を修正します[#6401](https://github.com/pingcap/tiflow/issues/6401) @ [リウメンギャ94](https://github.com/liumengya94)
        -   DM が`UPDATE`または`DELETE`ステートメントをレプリケートするが、対応する行データが存在しない場合、DM がイベント[#6383](https://github.com/pingcap/tiflow/issues/6383) @ [GMHDBJD](https://github.com/GMHDBJD)を黙って無視する問題を修正します。
        -   `query-status`コマンド[#7189](https://github.com/pingcap/tiflow/issues/7189) @ [GMHDBJD](https://github.com/GMHDBJD)を実行した後、 `secondsBehindMaster`フィールドが表示されない問題を修正します。
        -   チェックポイントを更新すると大規模なトランザクション[#5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)がトリガーされる可能性があるという問題を修正します
        -   フル タスク モードで、タスクが同期ステージに入ってすぐに失敗すると、DM が上流のテーブル スキーマ情報を失う可能性があるという問題を修正します[#7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)
        -   整合性チェックを有効にするとデッドロックが発生する可能性がある問題を修正[#7241](https://github.com/pingcap/tiflow/issues/7241) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)
        -   タスクの事前チェックに`INFORMATION_SCHEMA`テーブル[#7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)に対する`SELECT`特権が必要であるという問題を修正します。
        -   TLS 構成が空の場合にエラー[#7384](https://github.com/pingcap/tiflow/issues/7384) @ [リウメンギャ94](https://github.com/liumengya94)が発生する問題を修正します。

    -   TiDB Lightning

        -   `binary`エンコード形式[#38351](https://github.com/pingcap/tidb/issues/38351) @ [dsdashun](https://github.com/dsdashun)の文字列型列を含むターゲット テーブルに Apache Parquet ファイルをインポートするときのインポート パフォーマンスの低下を修正します。

    -   TiDBDumpling

        -   大量のテーブル[#36549](https://github.com/pingcap/tidb/issues/36549) @ [ランス6716](https://github.com/lance6716)をエクスポートするとDumplingがタイムアウトすることがある問題を修正
        -   整合性ロックが有効になっているがアップストリームにターゲット テーブルがない場合に報告されるロック エラーを修正します[#38683](https://github.com/pingcap/tidb/issues/38683) @ [ランス6716](https://github.com/lance6716)

## 寄稿者 {#contributors}

TiDB コミュニティの次の貢献者に感謝します。

-   [645775992](https://github.com/645775992)
-   [アンDJ](https://github.com/An-DJ)
-   [アンドリューディ](https://github.com/AndrewDi)
-   [エルワドバ](https://github.com/erwadba)
-   [fuzhe1989](https://github.com/fuzhe1989)
-   [ゴールドウィンドティン](https://github.com/goldwind-ting) (初めての投稿者)
-   [h3n4l](https://github.com/h3n4l)
-   [イグスリン](https://github.com/igxlin) (初めての投稿者)
-   [ihcsim](https://github.com/ihcsim)
-   [ジガオルオ](https://github.com/JigaoLuo)
-   [モルゴ](https://github.com/morgo)
-   [ランシー](https://github.com/Ranxy)
-   [シェンキデバオジ](https://github.com/shenqidebaozi) (初めての投稿者)
-   [陶豊流](https://github.com/taofengliu) (初めての投稿者)
-   [TszKitLo40](https://github.com/TszKitLo40)
-   [wxbty](https://github.com/wxbty) (初めての投稿者)
-   [zgcbj](https://github.com/zgcbj)

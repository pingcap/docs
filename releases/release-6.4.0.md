---
title: TiDB 6.4.0 Release Notes
---

# TiDB 6.4.0 リリースノート {#tidb-6-4-0-release-notes}

発売日：2022年11月17日

TiDB バージョン: 6.4.0-DMR

> **注記：**
>
> TiDB 6.4.0-DMR のドキュメントは[アーカイブされた](https://docs-archive.pingcap.com/tidb/v6.4/)になりました。 PingCAP では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.4.0#version-list)

v6.4.0-DMR の主な新機能と改善点は次のとおりです。

-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md) (実験的) を使用して、特定の時点へのクラスターの復元をサポートします。
-   [グローバルメモリ使用量の追跡](/configure-memory-usage.md)の TiDB インスタンスをサポートします (実験的)。
-   [線形ハッシュ分割構文](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)と互換性があること。
-   高性能でグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) (実験的) をサポートします。
-   [JSON タイプ](/data-type-json.md)で配列データの範囲選択をサポートします。
-   ディスク障害や I/O スタックなどの極端な状況での障害回復を加速します。
-   [動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)を追加してテーブルの結合順序を決定します。
-   [新しいオプティマイザ ヒント`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)を導入して、相関サブクエリの非相関化を実行するかどうかを制御します。
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能が GA になります。
-   TiFlash は、 [保存時の暗号化](/encryption-at-rest.md#tiflash)の SM4 アルゴリズムをサポートしています。
-   [テーブル内の指定されたパーティションのコンパクトなTiFlashレプリカを直ちに作成します](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)への SQL ステートメントの使用をサポートします。
-   サポート[EBS ボリューム スナップショットを使用した TiDB クラスターのバックアップ](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) ．
-   DM は[アップストリーム データ ソース情報をダウンストリーム マージ テーブルの拡張列に書き込む](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)をサポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   SQL ステートメントを使用して、テーブル内の指定されたパーティションのTiFlashレプリカを即時に圧縮するサポート[#5315](https://github.com/pingcap/tiflash/issues/5315) @ [へへへん](https://github.com/hehechen)

    v6.2.0 以降、TiDB はTiFlashのフルテーブル レプリカで[物理データをただちに圧縮する](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact)の機能をサポートしています。 SQL ステートメントを手動で実行する適切なタイミングを選択して、 TiFlash内の物理データを即座に圧縮できます。これにより、storage領域が削減され、クエリのパフォーマンスが向上します。 v6.4.0 では、圧縮されるTiFlashレプリカ データの粒度が調整され、テーブル内の指定されたパーティションのTiFlashレプリカの即時圧縮がサポートされます。

    SQL ステートメント`ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`を実行すると、テーブル内の指定したパーティションのTiFlashレプリカをすぐに圧縮できます。

    詳細については、 [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)を参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (実験的) [#37197](https://github.com/pingcap/tidb/issues/37197) [#13303](https://github.com/tikv/tikv/issues/13303) @ [定義2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [Jmポテト](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [ヒューシャープ](https://github.com/HuSharp) @ [カルビンネオ](https://github.com/CalvinNeo)を使用してクラスターを特定の時点に復元することをサポートします。

    `FLASHBACK CLUSTER TO TIMESTAMP`構文を使用すると、ガベージ コレクション (GC) の有効期間内にクラスターを特定の時点にすばやく復元できます。この機能は、DML の誤った操作を簡単かつ迅速に元に戻すのに役立ちます。たとえば、この構文を使用すると、誤って`WHERE`句を指定せずに`DELETE`実行した後、数分で元のクラスターを復元できます。この機能はデータベースのバックアップに依存せず、さまざまな時点でのデータのロールバックをサポートし、データが変更された正確な時間を決定します。 `FLASHBACK CLUSTER TO TIMESTAMP`ではデータベースのバックアップを置き換えることはできないことに注意してください。

    `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiCDC などのツールで実行されている PITR タスクとレプリケーション タスクを一時停止し、 `FLASHBACK`完了後に再起動する必要があります。そうしないと、レプリケーション タスクが失敗する可能性があります。

    詳細については、 [ユーザードキュメント](/sql-statements/sql-statement-flashback-to-timestamp.md)を参照してください。

-   `FLASHBACK DATABASE` [#20463](https://github.com/pingcap/tidb/issues/20463) @ [エルワドバ](https://github.com/erwadba)を使用した削除されたデータベースの復元をサポート

    `FLASHBACK DATABASE`を使用すると、ガベージコレクション(GC) の有効期間内に`DROP`によって削除されたデータベースとそのデータを復元できます。この機能は外部ツールに依存しません。 SQL ステートメントを使用して、データとメタデータを迅速に復元できます。

    詳細については、 [ユーザードキュメント](/sql-statements/sql-statement-flashback-database.md)を参照してください。

### Security {#security}

-   TiFlash は、保存時の暗号化のための SM4 アルゴリズムをサポートしています[#5953](https://github.com/pingcap/tiflash/issues/5953) @ [リデジュ](https://github.com/lidezhu)

    保存時のTiFlash暗号化用の SM4 アルゴリズムを追加します。保存時の暗号化を構成する場合、 `tiflash-learner.toml`構成ファイルで`data-encryption-method`構成の値を`sm4-ctr`に設定することで、SM4 暗号化容量を有効にすることができます。

    詳細については、 [ユーザードキュメント](/encryption-at-rest.md#tiflash)を参照してください。

### 可観測性 {#observability}

-   クラスタ診断が GA [#1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @ [ホークソンジー](https://github.com/Hawkson-jee)になる

    TiDB ダッシュボードの[クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能は、指定された時間範囲内でクラスターに存在する可能性のある問題を診断し、診断結果とクラスター関連の負荷監視情報を[診断レポート](/dashboard/dashboard-diagnostics-report.md)に要約します。この診断レポートは Web ページの形式です。ブラウザからページを保存した後、オフラインでページを閲覧し、このページのリンクを回覧することができます。

    診断レポートを使用すると、負荷、コンポーネントのステータス、消費時間、構成などのクラスターの基本的な正常性情報をすぐに理解できます。クラスターに一般的な問題がある場合は、 [診断情報](/dashboard/dashboard-diagnostics-report.md#diagnostic-information)セクションの組み込みの自動診断の結果から原因を特定できます。

### パフォーマンス {#performance}

-   コプロセッサタスク[#37724](https://github.com/pingcap/tidb/issues/37724) @ [あなた06](https://github.com/you06)に同時実行性適応メカニズムを導入

    コプロセッサ タスクの数が増加すると、TiKV の処理速度に基づいて、TiDB は自動的に同時実行性を高め (値[`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)を調整)、コプロセッサ タスク キューを減らし、レイテンシーを短縮します。

-   動的計画アルゴリズムを追加して、テーブル結合順序[#37825](https://github.com/pingcap/tidb/issues/37825) @ [ウィノロス](https://github.com/winoros)を決定します。

    以前のバージョンでは、TiDB は貪欲アルゴリズムを使用してテーブルの結合順序を決定します。 v6.4.0 では、TiDB オプティマイザーに[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)導入されています。動的計画アルゴリズムは、貪欲アルゴリズムよりも多くの可能な結合順序を列挙できるため、より適切な実行計画を見つける可能性が高まり、一部のシナリオでは SQL 実行効率が向上します。

    動的プログラミング アルゴリズムはより多くの時間を消費するため、TiDB 結合したテーブルの再配置アルゴリズムの選択は[`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)変数によって制御されます。 結合したテーブルの再配置に参加しているノードの数がこのしきい値より大きい場合、TiDB は貪欲アルゴリズムを使用します。それ以外の場合、TiDB は動的プログラミング アルゴリズムを使用します。

    詳細については、 [ユーザードキュメント](/join-reorder.md)を参照してください。

-   接頭辞インデックスは、NULL 値のフィルタリングをサポートします。 [#21145](https://github.com/pingcap/tidb/issues/21145) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)

    この機能は、プレフィックス インデックスの最適化です。テーブル内の列に接頭辞インデックスがある場合、SQL ステートメント内の列の`IS NULL`または`IS NOT NULL`条件を接頭辞によって直接フィルタリングできます。これにより、この場合のテーブル検索が回避され、SQL 実行のパフォーマンスが向上します。

    詳細については、 [ユーザードキュメント](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)を参照してください。

-   TiDB チャンク再利用メカニズムの強化[#38606](https://github.com/pingcap/tidb/issues/38606) @ [キープラーニング20221](https://github.com/keeplearning20221)

    以前のバージョンでは、TiDB は`writechunk`関数内のチャンクのみを再利用します。 TiDB v6.4.0 は、チャンク再利用メカニズムを Executor のオペレーターに拡張します。チャンクを再利用することにより、TiDB はメモリ解放を頻繁に要求する必要がなくなり、一部のシナリオでは SQL クエリがより効率的に実行されます。システム変数[`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)使用して、チャンク オブジェクトを再利用するかどうかを制御できます。これはデフォルトで有効になっています。

    詳細については、 [ユーザードキュメント](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)を参照してください。

-   相関サブクエリの非相関化を実行するかどうかを制御する新しいオプティマイザ ヒント`NO_DECORRELATE`を導入します[#37789](https://github.com/pingcap/tidb/issues/37789) @ [時間と運命](https://github.com/time-and-fate)

    デフォルトでは、TiDB は常に相関サブクエリを書き換えて非相関化を実行しようとします。これにより、通常は実行効率が向上します。ただし、シナリオによっては、無相関化により実行効率が低下する場合があります。 v6.4.0 では、TiDB はオプティマイザー ヒント`NO_DECORRELATE`を導入し、一部のシナリオでクエリ パフォーマンスを向上させるために、指定されたクエリ ブロックの非相関化を実行しないようにオプティマイザーに指示します。

    詳細については、 [ユーザードキュメント](/optimizer-hints.md#no_decorrelate)を参照してください。

-   パーティションテーブル[#37977](https://github.com/pingcap/tidb/issues/37977) @ [イーサール](https://github.com/Yisaer)での統計収集のパフォーマンスを向上させます。

    v6.4.0 では、TiDB はパーティション化されたテーブルの統計を収集する戦略を最適化します。システム変数[`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)を使用して、パーティション化されたテーブルの統計を並行して収集する同時実行性を設定して、収集を高速化し、分析時間を短縮できます。

### 安定性 {#stability}

-   ディスク障害や I/O スタックなどの極端な状況での障害回復を加速します[#13648](https://github.com/tikv/tikv/issues/13648) @ [リククスサシネーター](https://github.com/LykxSassinator)

    企業ユーザーにとって、データベースの可用性は最も重要な指標の 1 つです。複雑なハードウェア環境では、障害を迅速に検出して回復する方法が、データベースの可用性に関する常に課題の 1 つです。 v6.4.0 では、TiDB は TiKV ノードの状態検出メカニズムを完全に最適化します。ディスク障害や I/O スタックなどの極端な状況でも、TiDB はノード状態を迅速に報告し、アクティブ ウェイクアップ メカニズムを使用して事前にLeader選出を開始することができ、これによりクラスターの自己修復が加速されます。この最適化により、TiDB はディスク障害が発生した場合のクラスターの回復時間を約 50% 短縮できます。

-   TiDBメモリ使用量のグローバル制御[#37816](https://github.com/pingcap/tidb/issues/37816) @ [wshwsh12](https://github.com/wshwsh12)

    v6.4.0 では、TiDB は、TiDB インスタンスのグローバルメモリ使用量を追跡する実験的機能として、メモリ使用量のグローバル コントロールを導入します。システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用して、グローバルメモリ使用量の上限を設定できます。メモリ使用量がしきい値に達すると、TiDB はより多くの空きメモリを再利用して解放しようとします。メモリ使用量がしきい値を超えると、過剰なメモリ使用量によって引き起こされるシステムの問題を回避するために、TiDB はメモリ使用量が最も高い SQL 操作を特定してキャンセルします。

    TiDB インスタンスのメモリ消費に潜在的なリスクがある場合、TiDB は問題の診断を容易にするために、事前に診断情報を収集し、指定されたディレクトリに書き込みます。同時に、TiDB はメモリ使用量と操作履歴を表示するシステム テーブル ビュー[`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)および[`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)を提供し、メモリ使用量をより深く理解できるようにします。

    グローバルメモリ制御は、TiDBメモリ管理におけるマイルストーンです。インスタンスのグローバル ビューを導入し、メモリの体系的な管理を採用することで、より重要なシナリオでデータベースの安定性とサービスの可用性を大幅に向上させることができます。

    詳細については、 [ユーザードキュメント](/configure-memory-usage.md)を参照してください。

-   範囲構築オプティマイザー[#37176](https://github.com/pingcap/tidb/issues/37176) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)のメモリ使用量を制御します。

    v6.4.0 では、範囲を構築するオプティマイザーの最大メモリ使用量を制限するために、システム変数[`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)が導入されました。メモリ使用量が制限を超えると、オプティマイザはメモリ消費量を削減するために、より正確な範囲ではなく、より粗い範囲を構築します。 SQL ステートメントに多くの`IN`条件がある場合、この最適化によりコンパイル時のメモリ使用量が大幅に削減され、システムの安定性が確保されます。

    詳細については、 [ユーザードキュメント](/system-variables.md#tidb_opt_range_max_size-new-in-v640)を参照してください。

-   統計の同期ロード (GA) [#37434](https://github.com/pingcap/tidb/issues/37434) @ [クリサン](https://github.com/chrysan)をサポート

    TiDB v6.4.0 では、統計の同期ロード機能がデフォルトで有効になっています。この機能により、SQL ステートメントの実行時に TiDB が大きなサイズの統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期してロードできるようになり、SQL 最適化のための統計の完全性が向上します。

    詳細については、 [ユーザードキュメント](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)を参照してください。

-   軽量トランザクション書き込みの応答時間に対するバッチ書き込みリクエストの影響を軽減します[#13313](https://github.com/tikv/tikv/issues/13313) @ [グロルフ](https://github.com/glorv)

    一部のシステムのビジネス ロジックでは、定期的なバッチ DML タスクが必要ですが、これらのバッチ書き込みタスクを処理すると、オンライン トランザクションのレイテンシーが増加します。 v6.3.0 では、TiKV はハイブリッド ワークロード シナリオにおける読み取りリクエストのスケジューリングを最適化するため、 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)構成項目を有効にして、TiKV がすべての読み取りリクエストに対して UnifyReadPool スレッド プールのサイズを自動的に調整できるようにします。 v6.4.0 では、TiKV は書き込みリクエストを動的に識別して優先順位を付けることもでき、適用スレッドがポーリングの 1 ラウンドで 1 つの FSM (有限状態マシン) に対して書き込むことができる最大バイト数を制御できるため、バッチ書き込みリクエストの影響が軽減されます。トランザクション書き込みの応答時間について。

### 使いやすさ {#ease-of-use}

-   TiKV API V2 が一般提供 (GA) [#11745](https://github.com/tikv/tikv/issues/11745) @ [ピンギュ](https://github.com/pingyu)に開始

    v6.1.0 より前では、TiKV はクライアントから渡された生データのみを保存するため、基本的なキー値の読み取りおよび書き込み機能のみを提供していました。さらに、コーディング方法とスコープ外のデータ範囲が異なるため、TiDB、トランザクション KV、および RawKV を同じ TiKV クラスター内で同時に使用することはできません。この場合、代わりに複数のクラスターが必要になるため、マシンと展開のコストが増加します。

    TiKV API V2 は、新しい RawKVstorage形式とアクセス インターフェイスを提供し、次の利点をもたらします。

    -   変更データ キャプチャ (CDC) の実装に基づいて、記録されたデータの変更タイムスタンプとともにデータを MVCC に保存します。この機能は実験的であり、 [TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)で詳しく説明されています。
    -   データはさまざまな用途に応じてスコープ設定されており、API V2 は、単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
    -   マルチテナントなどの機能をサポートするために、「キー スペース」フィールドを予約します。

    TiKV API V2 を有効にするには、TiKV 構成ファイルの`[storage]`セクションに`api-version = 2`を設定します。

    詳細については、 [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610)を参照してください。

-   TiFlashデータ複製の進行状況[#4902](https://github.com/pingcap/tiflash/issues/4902) @ [へへへん](https://github.com/hehechen)の精度を向上させます。

    TiDB では、 `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの`PROGRESS`フィールドは、TiKV 内の対応するテーブルからTiFlashレプリカへのデータ レプリケーションの進行状況を示すために使用されます。以前の TiDB バージョンでは、 `PROCESS`フィールドは、 TiFlashレプリカの作成中のデータ複製の進行状況のみを提供します。 TiFlashレプリカの作成後、新しいデータが TiKV の対応するテーブルにインポートされた場合、このフィールドは、新しいデータの TiKV からTiFlashへのレプリケーションの進行状況を示すように更新されません。

    v6.4.0 では、TiDB は、 TiFlashレプリカのデータ複製進行状況の更新メカニズムを改善します。 TiFlashレプリカの作成後、新しいデータが TiKV の対応するテーブルにインポートされると、 [`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)テーブルの`PROGRESS`値が更新され、新しいデータの TiKV からTiFlashへの実際のレプリケーションの進行状況が表示されます。この改善により、 TiFlashデータ レプリケーションの実際の進行状況を簡単に確認できるようになりました。

    詳細については、 [ユーザードキュメント](/information-schema/information-schema-tiflash-replica.md)を参照してください。

### MySQLの互換性 {#mysql-compatibility}

-   リニア ハッシュ パーティショニング構文[#38450](https://github.com/pingcap/tidb/issues/38450) @ [むじょん](https://github.com/mjonss)と互換性があること

    以前のバージョンでは、TiDB はハッシュ、レンジ、List パーティショニングをサポートしていました。 v6.4.0 以降、TiDB は[MySQL リニア ハッシュ パーティショニング](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)の構文とも互換性を持つようになりました。

    TiDB では、MySQL Linear Hash パーティションの既存の DDL ステートメントを直接実行でき、TiDB は対応する Hash パーティション テーブルを作成します (TiDB 内には Linear Hash パーティションがないことに注意してください)。 MySQL Linear Hash パーティションの既存の DML ステートメントを直接実行することもでき、TiDB は通常、対応する TiDB Hash パーティションのクエリ結果を返します。この機能により、TiDB 構文と MySQL Linear Hash パーティションとの互換性が保証され、MySQL ベースのアプリケーションから TiDB へのシームレスな移行が容易になります。

    パーティション数が 2 の累乗の場合、TiDB ハッシュパーティションテーブル内の行は、MySQL Linear Hashパーティションテーブル内の行と同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は MySQL とは異なります。

    詳細については、 [ユーザードキュメント](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)を参照してください。

-   高性能でグローバルに単調な`AUTO_INCREMENT` (実験的) [#38442](https://github.com/pingcap/tidb/issues/38442) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)をサポートします。

    TiDB v6.4.0 では、 `AUTO_INCREMENT` MySQL 互換モードが導入されています。このモードでは、すべての TiDB インスタンスで ID が単調増加することを保証する、集中型の自動インクリメント ID 割り当てサービスが導入されています。この機能により、クエリ結果を自動インクリメント ID で簡単に並べ替えることができます。 MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE` ～ `1`を設定する必要があります。以下は例です。

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    詳細については、 [ユーザードキュメント](/auto-increment.md#mysql-compatibility-mode)を参照してください。

-   JSON type [#13644](https://github.com/tikv/tikv/issues/13644) @ [ヤンケオ](https://github.com/YangKeao)の配列データの範囲選択をサポート

    v6.4.0 以降、TiDB で MySQL 互換[範囲選択の構文](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths)を使用できるようになります。

    -   キーワード`to`を使用すると、配列要素の開始位置と終了位置を指定し、配列内の連続した範囲の要素を選択できます。 `0`を使用すると、配列内の最初の要素の位置を指定できます。たとえば、 `$[0 to 2]`を使用すると、配列の最初の 3 つの要素を選択できます。

    -   キーワード`last`を使用すると、配列内の最後の要素の位置を指定できます。これにより、位置を右から左に設定できます。たとえば、 `$[last-2 to last]`を使用すると、配列の最後の 3 つの要素を選択できます。

    この機能により、SQL ステートメントを作成するプロセスが簡素化され、JSON タイプの互換性がさらに向上し、MySQL アプリケーションを TiDB に移行する難しさが軽減されます。

-   データベース ユーザー[#38172](https://github.com/pingcap/tidb/issues/38172) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の追加説明の追加をサポート

    TiDB v6.4 では、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)を使用してデータベース ユーザーに対する追加の説明を追加できます。 TiDB には 2 つの記述形式が用意されています。 `COMMENT`を使用してテキスト コメントを追加し、 `ATTRIBUTE`を使用して JSON 形式で一連の構造化属性を追加できます。

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

    この機能により、TiDB と MySQL 構文の互換性が向上し、TiDB を MySQL エコシステム内のツールまたはプラットフォームに簡単に統合できるようになります。

### バックアップと復元 {#backup-and-restore}

-   EBS ボリューム スナップショット[#33849](https://github.com/pingcap/tidb/issues/33849) @ [フェンゴウ1](https://github.com/fengou1)を使用した TiDB クラスターのバックアップのサポート

    TiDB クラスターが EKS にデプロイされ、AWS EBS ボリュームを使用しており、TiDB クラスターのデータをバックアップするときに次の要件がある場合、 TiDB Operator を使用して、ボリューム スナップショットとメタデータによってデータを AWS S3 にバックアップできます。

    -   バックアップの影響を最小限に抑えます。たとえば、QPS とトランザクションレイテンシーへの影響を 5% 未満に抑え、クラスターの CPU とメモリを占有しないようにします。
    -   データのバックアップと復元を短時間で実行します。たとえば、バックアップは 1 時間以内に完了し、データの復元は 2 時間以内に完了します。

    詳細については、 [ユーザードキュメント](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)を参照してください。

### データ移行 {#data-migration}

-   DM は、ダウンストリームのマージされたテーブル[#37797](https://github.com/pingcap/tidb/issues/37797) @ [リチュンジュ](https://github.com/lichunzhu)の拡張列へのアップストリーム データ ソース情報の書き込みをサポートします。

    シャードされたスキーマとテーブルをアップストリームから TiDB にマージする場合、ターゲット テーブルに複数のフィールド (拡張列) を手動で追加し、DM タスクの構成時にそれらの値を指定できます。たとえば、拡張列にアップストリームのシャード スキーマとテーブルの名前を指定すると、DM によってダウンストリームに書き込まれるデータにはスキーマ名とテーブル名が含まれます。ダウンストリーム データが異常であると思われる場合、この機能を使用すると、スキーマ名やテーブル名など、ターゲット テーブル内のデータ ソース情報をすばやく見つけることができます。

    詳細については、 [テーブル、スキーマ、ソース情報を抽出し、マージされたテーブルに書き込みます](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)を参照してください。

-   DM は、一部の必須チェック項目をオプション項目に変更することで、事前チェック メカニズムを最適化します[#7333](https://github.com/pingcap/tiflow/issues/7333) @ [リチュンジュ](https://github.com/lichunzhu)

    データ移行タスクをスムーズに実行するために、DM はタスクの開始時に自動的に[事前チェック](/dm/dm-precheck.md)トリガーし、チェック結果を返します。 DM は、事前チェックに合格した後にのみ移行を開始します。

    v6.4.0 では、DM は次の 3 つのチェック項目を必須からオプションに変更し、事前チェックの通過率を向上させます。

    -   上流のテーブルで TiDB と互換性のない文字セットが使用されていないか確認してください。
    -   上流テーブルに主キー制約または一意キー制約があるかどうかを確認する
    -   プライマリ-セカンダリ構成で上流データベースのデータベースID `server_id`が指定されているか確認してください。

-   DM は、増分移行タスク[#7393](https://github.com/pingcap/tiflow/issues/7393) @ [GMHDBJD](https://github.com/GMHDBJD)のオプション パラメーターとしてbinlogの位置と GTID の構成をサポートします。

    v6.4.0 以降、binlogの位置や GTID を指定せずに、増分移行を直接実行できるようになりました。 DM は、タスクの開始後に生成されるbinlogファイルをアップストリームから自動的に取得し、これらの増分データをダウンストリームに移行します。これにより、ユーザーは面倒な理解や複雑な設定から解放されます。

    詳細については、 [DM 拡張タスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)を参照してください。

-   DM は移行タスク[#7343](https://github.com/pingcap/tiflow/issues/7343) @ [オクジャン](https://github.com/okJiang)のステータス インジケーターを追加します

    v6.4.0 では、DM に移行タスクのパフォーマンスと進行状況のインジケーターがさらに追加されています。これにより、移行のパフォーマンスと進行状況をより直観的に理解できるようになり、トラブルシューティングの参照が提供されます。

    -   データのインポートおよびエクスポートのパフォーマンスを示すステータス インジケーター (バイト/秒) を追加します。
    -   ダウンストリーム データベースにデータを書き込むためのパフォーマンス インジケーターの名前を TPS から RPS (行数/秒) に変更します。
    -   DM 完全移行タスクのデータ エクスポートの進行状況を示す進行状況インジケーターを追加します。

    これらの指標の詳細については、 [TiDB データ移行でのタスク ステータスのクエリ](/dm/dm-query-status.md)を参照してください。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、バージョン`3.2.0` [#7191](https://github.com/pingcap/tiflow/issues/7191) @ [3エースショーハンド](https://github.com/3AceShowHand)の Kafka へのデータのレプリケーションをサポートします。

    v6.4.0 以降、TiCDC は`3.2.0`のバージョン以前の[Kafka へのデータの複製](/replicate-data-to-kafka.md)をサポートします。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                 | 種類の変更    | 説明                                                                                                                                                                                                                                  |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)         | 修正済み     | GLOBAL スコープを削除し、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成項目を使用してデフォルト値を変更できるようにします。この変数は、TiDB が悲観的トランザクションの一意の制約をいつチェックするかを制御します。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                 | 修正済み     | v6.4.0 から有効になり、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-to-timestamp.md)の同時実行性を制御します。デフォルト値は`64`です。                                                                                              |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)                                        | 修正済み     | デフォルト値を`INT_ONLY`から`ON`に変更します。これは、主キーがデフォルトでクラスター化インデックスとして作成されることを意味します。                                                                                                                                                           |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                                                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、コプロセッサ要求を送信するページング方式がデフォルトで使用されることを意味します。                                                                                                                                                              |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                               | 修正済み     | SESSION スコープを追加します。この変数は、 [プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを制御します。                                                                                                                                             |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)                                               | 修正済み     | デフォルト値を`0.8`から`0.7`に変更します。この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を制御します。                                                                                                                                                              |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)                                                             | 修正済み     | GLOBAL スコープを追加します。この変数は、オプティマイザが結合、射影、および UnionAll の前の位置に集約関数をプッシュダウンする最適化操作を実行するかどうかを制御します。                                                                                                                                        |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                   | 修正済み     | SESSION スコープを追加します。この変数は、セッション内にキャッシュできるプランの最大数を制御します。                                                                                                                                                                              |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                           | 修正済み     | デフォルト値を`0`から`100`に変更します。これは、完全な列統計を同期的にロードするために SQL 実行がデフォルトで最大 100 ミリ秒待機できることを意味します。                                                                                                                                               |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)                                 | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、完全な列統計の同期ロードのタイムアウトに達した後、SQL 最適化が擬似統計の使用に戻ることを意味します。                                                                                                                                                   |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640)                                                         | 新しく追加された | 前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用しているかどうかを示します。この変数は読み取り専用で、デフォルト値は`OFF`です。                                                                                                                                              |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)                 | 新しく追加された | パーティションテーブルを分析するときに TiDB が[自動的に分析します](/statistics.md#automatic-update)に実行できるパーティションの数を指定します (つまり、パーティションテーブルに関する統計を自動的に収集します)。デフォルト値は`1`です。                                                                                         |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)                                     | 新しく追加された | TiDB が[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)で指定されたタイムスタンプを持つデータを読み取るかどうかを制御します。デフォルト値は`OFF`です。                                                                                                     |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640)                                                 | 新しく追加された | GOGC チューナーを有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                           |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)                                               | 新しく追加された | TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。デフォルト値は`ON`です。これは、TiDB がキャッシュされたチャンク オブジェクトの使用を優先し、要求されたオブジェクトがキャッシュにない場合にのみシステムから要求することを意味します。値が`OFF`場合、TiDB はシステムからチャンク オブジェクトを直接要求します。                                                   |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | 新しく追加された | プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                             |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)                                                             | 新しく追加された | デフォルト値は`0`です。 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)が`ON`に設定されている場合、TiDB はこの変数で指定されたタイムスタンプを持つデータを読み取ります。                                                                  |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640)                                           | 新しく追加された | GOGC をチューニングするための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC チューナーは動作を停止します。デフォルト値は`0.6`です。                                                                                                                                                |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)               | 新しく追加された | tidb サーバーのメモリ使用量がメモリアラームしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この変数を使用してこの数値を調整できます。                                                                                                               |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)                           | 新しく追加された | TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュダウンして、不必要なテーブル ルックアップを回避し、クエリのパフォーマンスを向上させるかどうかを制御します。デフォルト値は`ON`です。                                                                                                                    |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)                                               | 新しく追加された | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を指定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                             | 新しく追加された | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を制御します (実験的)。デフォルト値は`0`で、メモリ制限がないことを意味します。                                                                                                                                                           |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)                       | 新しく追加された | TiDB が GC をトリガーしようとするしきい値を制御します (実験的)。デフォルト値は`70%`です。                                                                                                                                                                               |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)                 | 新しく追加された | メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も多い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。デフォルト値は`134217728` (128 MiB) です。                                                                                                   |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                           | 種類の変更    | 説明                                                                                                                                                                |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `tidb_memory_usage_alarm_ratio`                                                                                                           | 削除されました  | この設定項目は無効になりました。                                                                                                                                                  |
| TiDB           | `memory-usage-alarm-ratio`                                                                                                                | 削除されました  | システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)に置き換えられます。この構成項目が v6.4.0 より前の TiDB バージョンで構成されている場合、アップグレード後は有効になりません。  |
| TiDB           | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)  | 新しく追加された | システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。デフォルト値は`true`です。   |
| TiDB           | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640)                                                    | 新しく追加された | チャンク割り当てのキャッシュされたチャンク オブジェクトの最大数を制御します。デフォルト値は`64`です。                                                                                                             |
| TiDB           | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640)                                                  | 新しく追加された | チャンク割り当てのキャッシュされた列オブジェクトの最大数を制御します。デフォルト値は`256`です。                                                                                                                |
| TiKV           | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | 廃止されました  | この設定項目は無効になりました。                                                                                                                                                  |
| TiKV           | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640)                                              | 新しく追加された | 事前に割り当てられた TSO キャッシュ サイズ (期間内)。デフォルト値は`3s`です。                                                                                                                     |
| TiKV           | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)                                          | 新しく追加された | タイムスタンプ要求内の TSO の最大数を制御します。デフォルト値は`8192`です。                                                                                                                       |
| TiKV           | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640)                                      | 新しく追加された | 適用スレッドがポーリングの 1 ラウンドで 1 つの FSM (有限状態マシン) に対して書き込むことができる最大バイト数を制御します。デフォルト値は`32KiB`です。これはソフトリミットです。                                                                |
| PD             | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)                                                  | 新しく追加された | v6.4.0 から有効になり、PD が TSO の物理時間を更新する間隔を制御します。デフォルト値は`50ms`です。                                                                                                       |
| TiFlash        | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)                                      | 修正済み     | 新しい値のオプション`sm4-ctr`を導入します。この設定項目を`sm4-ctr`に設定すると、データは SM4 を使用して暗号化されて保存されます。                                                                                      |
| DM             | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                      | 新しく追加された | オプション。シャーディング テーブルのソース情報を抽出するためのシャーディング シナリオで使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。 |
| DM             | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディング スキーマのソース情報を抽出するためにシャーディング シナリオで使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。 |
| DM             | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディング シナリオでソース インスタンス情報を抽出するために使用されます。抽出された情報は、データ ソースを識別するためにダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。       |
| TiCDC          | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)                                             | 修正済み     | デフォルト値を`table`から`none`に変更します。この変更は、レプリケーションのレイテンシーと OOM のリスクを軽減するのに役立ちます。さらに、TiCDC は、すべてのトランザクションではなく、少数のトランザクションのみを分割するようになりました (単一トランザクションのサイズは 1024 行を超えます)。   |

### その他 {#others}

-   v6.4.0 以降、 `mysql.user`テーブルには`User_attributes`と`Token_issuer`という 2 つの新しい列が追加されます。以前の TiDB バージョンのバックアップ データから TiDB v6.4.0 にバックアップ[`mysql`スキーマ内のシステム テーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)と、 BR は`mysql.user`テーブルに対して`column count mismatch`エラーを報告します。 `mysql`スキーマのシステム テーブルを復元しない場合、このエラーは報告されません。
-   名前が[Dumplingエクスポート ファイルの形式](/dumpling-overview.md#format-of-exported-files)に一致するが、非圧縮形式で終わるファイル ( `test-schema-create.sql.origin`や`test.table-schema.sql.origin`など) の場合、 TiDB Lightningファイルの処理方法が変更されます。 v6.4.0 より前では、インポートされるファイルにそのようなファイルが含まれている場合、 TiDB Lightning はそのようなファイルのインポートをスキップします。 v6.4.0 以降、 TiDB Lightning は、そのようなファイルがサポートされていない圧縮形式を使用していると想定するため、インポート タスクは失敗します。
-   v6.4.0 以降、 `SYSTEM_VARIABLES_ADMIN`または`SUPER`権限を持つ変更フィードのみが TiCDC 同期ポイント機能を使用できます。

## 改善点 {#improvements}

-   TiDB

    -   noop 変数`lc_messages` [#38231](https://github.com/pingcap/tidb/issues/38231) @ [djshow832](https://github.com/djshow832)の変更を許可する
    -   クラスター化複合インデックス[#38572](https://github.com/pingcap/tidb/issues/38572) @ [タンジェンタ](https://github.com/tangenta)の最初の列として`AUTO_RANDOM`列をサポートします。
    -   内部トランザクションの再試行では悲観的トランザクションを使用して、再試行の失敗を回避し、時間の消費を削減します[#38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキースプ](https://github.com/jackysp)

-   TiKV

    -   新しい構成項目`apply-yield-write-size`を追加して、アプライ スレッドがポーリングの 1 ラウンドで 1 つの有限状態マシンに書き込むことができる最大バイト数を制御し、アプライ スレッドが大量のデータを書き込むときのRaftstore の輻輳を緩和します[#13313](https://github.com/tikv/tikv/issues/13313) @ [グロルフ](https://github.com/glorv)
    -   リージョンのリーダーを移行する前にエントリ キャッシュをウォームアップして、リーダー転送プロセス[#13060](https://github.com/tikv/tikv/issues/13060) @ [コスベン](https://github.com/cosven)中の QPS ジッターを回避します。
    -   `json_constains`オペレーターをコプロセッサー[#13592](https://github.com/tikv/tikv/issues/13592) @ [立振環](https://github.com/lizhenhuan)にプッシュダウンするサポート
    -   `CausalTsProvider`に非同期関数を追加して、一部のシナリオ[#13428](https://github.com/tikv/tikv/issues/13428) @ [沢民州](https://github.com/zeminzhou)でのフラッシュ パフォーマンスを向上させます。

-   PD

    -   ホットリージョンスケジューラの v2 アルゴリズムが GA になりました。一部のシナリオでは、v2 アルゴリズムは、構成された両方のディメンションでより適切なバランスを実現し、無効なスケジュール[#5021](https://github.com/tikv/pd/issues/5021) @ [フンドゥンDM](https://github.com/hundundm)を減らすことができます。
    -   早期タイムアウト[#5596](https://github.com/tikv/pd/issues/5596) @ [バッファフライ](https://github.com/bufferflies)を回避するために、オペレーター ステップのタイムアウト メカニズムを最適化します。
    -   大規模なクラスター[#5473](https://github.com/tikv/pd/issues/5473) @ [バッファフライ](https://github.com/bufferflies)でのスケジューラーのパフォーマンスを向上させます。
    -   PD [#5637](https://github.com/tikv/pd/issues/5637) @ [lhy1024](https://github.com/lhy1024)によって提供されない外部タイムスタンプの使用をサポート

-   TiFlash

    -   TiFlash MPP エラー処理ロジックをリファクタリングして、MPP [#5095](https://github.com/pingcap/tiflash/issues/5095) @ [ウィンドトーカー](https://github.com/windtalker)の安定性をさらに向上させます。
    -   TiFlash計算プロセスのソートを最適化し、結合および集計[#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツグ](https://github.com/solotzg)のキー処理を最適化します。
    -   デコード用のメモリ使用量を最適化し、冗長な転送列を削除して結合パフォーマンス[#6157](https://github.com/pingcap/tiflash/issues/6157) @ [イービン87](https://github.com/yibin87)を向上させます。

-   ツール

    -   TiDB ダッシュボード

        -   [モニタリング] ページでのTiFlashメトリクスの表示をサポートし、そのページでのメトリクスの表示を最適化します[#1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @ [イニシュ9506](https://github.com/YiniXu9506)
        -   スロー クエリ リストと SQL ステートメント リスト[#1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @ [バーリン](https://github.com/baurine)の結果の行数を表示します。
        -   Alertmanager が存在しない場合に Alertmanager エラーを報告しないようにダッシュボードを最適化します[#1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @ [バーリン](https://github.com/baurine)

    -   バックアップと復元 (BR)

        -   メタデータをロードするメカニズムを改善します。メタデータは必要な場合にのみメモリにロードされるため、PITR [#38404](https://github.com/pingcap/tidb/issues/38404) @ [ユジュンセン](https://github.com/YuJuncen)中のメモリ使用量が大幅に削減されます。

    -   TiCDC

        -   Exchange パーティション DDL ステートメントのレプリケートのサポート[#639](https://github.com/pingcap/tiflow/issues/639) @ [東門](https://github.com/asddongmen)
        -   MQ シンク モジュール[#7353](https://github.com/pingcap/tiflow/issues/7353) @ [こんにちはラスティン](https://github.com/hi-rustin)の非バッチ送信パフォーマンスを向上させます。
        -   テーブルに多数のリージョン[#7078](https://github.com/pingcap/tiflow/issues/7078) [#7281](https://github.com/pingcap/tiflow/issues/7281) @ [スドジ](https://github.com/sdojjy)がある場合の TiCDC プラーのパフォーマンスを向上させました。
        -   同期ポイントが有効な場合に`tidb_enable_external_ts_read`変数を使用して、ダウンストリーム TiDB での履歴データの読み取りをサポートします[#7419](https://github.com/pingcap/tiflow/issues/7419) @ [東門](https://github.com/asddongmen)
        -   レプリケーションの安定性を向上させるために、デフォルトでトランザクション分割を有効にし、セーフモードを無効にします[#7505](https://github.com/pingcap/tiflow/issues/7505) @ [東門](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   dmctl [#7246](https://github.com/pingcap/tiflow/issues/7246) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)から無駄な`operate-source update`コマンドを削除します。
        -   アップストリーム データベースが TiDB と互換性のない DDL ステートメントを使用している場合、DM の完全インポートが失敗する問題を修正します。 TiDB でサポートされている DDL ステートメントを使用して、事前に TiDB にターゲット テーブルのスキーマを手動で作成し、インポートを確実に成功させることができます[#37984](https://github.com/pingcap/tidb/issues/37984) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   ファイル スキャン ロジックを最適化して、スキーマ ファイル[#38598](https://github.com/pingcap/tidb/issues/38598) @ [dsダシュン](https://github.com/dsdashun)のスキャンを高速化します。

## バグの修正 {#bug-fixes}

-   TiDB

    -   新しいインデックス[#38165](https://github.com/pingcap/tidb/issues/38165) @ [タンジェンタ](https://github.com/tangenta)を作成した後に発生するインデックスの不一致の潜在的な問題を修正します。
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブル[#38407](https://github.com/pingcap/tidb/issues/38407) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の権限の問題を修正
    -   `mysql.tables_priv`テーブル[#38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   共通テーブル式の結合結果が間違っている場合がある問題を修正[#38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   共通テーブル式の結合結果が間違っている場合がある問題を修正[#37928](https://github.com/pingcap/tidb/issues/37928) @ [ヤンケオ](https://github.com/YangKeao)
    -   **トランザクション領域番号**監視パネルの情報が正しくない問題を修正[#38139](https://github.com/pingcap/tidb/issues/38139) @ [ジャッキースプ](https://github.com/jackysp)
    -   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が内部トランザクションに影響を与える可能性がある問題を修正します。変数のスコープは SESSION に変更されます。 [#38766](https://github.com/pingcap/tidb/issues/38766) @ [エキシウム](https://github.com/ekexium)
    -   クエリ内の条件が誤って投影[#35623](https://github.com/pingcap/tidb/issues/35623) @ [懐かしい](https://github.com/Reminiscent)にプッシュダウンされる問題を修正
    -   `AND`および`OR`に対する間違った`isNullRejected`チェック結果により、間違ったクエリ結果[#38304](https://github.com/pingcap/tidb/issues/38304) @ [イーサール](https://github.com/Yisaer)が発生する問題を修正します。
    -   外部結合が削除されると`GROUP_CONCAT`のうち`ORDER BY`が考慮されず、誤ったクエリ結果[#18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正します。
    -   結合したテーブルの再配置 [#38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)で誤ってプッシュダウンされた条件が破棄された場合に、間違ったクエリ結果が発生する問題を修正しました。

-   TiKV

    -   複数の`cgroup`および`mountinfo`レコード[#13660](https://github.com/tikv/tikv/issues/13660) @ [タボキー](https://github.com/tabokie)がある場合、Gitpod で TiDB が起動できない問題を修正
    -   TiKV メトリクスの間違った式を修正`tikv_gc_compaction_filtered` [#13537](https://github.com/tikv/tikv/issues/13537) @ [定義2014](https://github.com/Defined2014)
    -   異常な`delete_files_in_range` [#13534](https://github.com/tikv/tikv/issues/13534) @ [タボキー](https://github.com/tabokie)によって引き起こされるパフォーマンスの問題を修正
    -   スナップショット取得中のリース期限切れによって引き起こされる異常なリージョン競合を修正[#13553](https://github.com/tikv/tikv/issues/13553) @ [SpadeA-Tang](https://github.com/SpadeA-Tang)
    -   最初のバッチ[#13672](https://github.com/tikv/tikv/issues/13672) [#13704](https://github.com/tikv/tikv/issues/13704) [#13723](https://github.com/tikv/tikv/issues/13723) @ [ヒューシャープ](https://github.com/HuSharp)で`FLASHBACK`が失敗したときに発生するエラーを修正しました

-   PD

    -   不正確なストリーム タイムアウトを修正し、リーダーの切り替え[#5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)を高速化します。

-   TiFlash

    -   PageStorage GC がページ削除マーカーを適切にクリアしない場合に発生する、WAL ファイルのサイズが大きすぎることによる OOM の問題を修正します[#6163](https://github.com/pingcap/tiflash/issues/6163) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiDB ダッシュボード

        -   特定の複雑な SQL ステートメント[#1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @ [バーリン](https://github.com/baurine)の実行プランをクエリするときの TiDB OOM の問題を修正しました。
        -   NgMonitoring が PD ノード[#164](https://github.com/pingcap/ng-monitoring/issues/164) @ [ゾンズク](https://github.com/zhongzc)への接続を失った場合に、 Top SQLスイッチが有効にならない場合がある問題を修正します。

    -   バックアップと復元 (BR)

        -   復元プロセス[#36910](https://github.com/pingcap/tidb/issues/36910) @ [モクイシュル28](https://github.com/MoCuishle28)中に PD リーダー スイッチによって引き起こされる復元失敗の問題を修正します。
        -   ログ バックアップ タスクを一時停止できない問題を修正[#38250](https://github.com/pingcap/tidb/issues/38250) @ [ジョッカウ](https://github.com/joccau)
        -   BRがログバックアップデータを削除すると、削除すべきでないデータを誤って削除してしまう問題を修正[#38939](https://github.com/pingcap/tidb/issues/38939) @ [レヴルス](https://github.com/leavrth)
        -   Azure Blob Storage または Google Cloud Storage に保存されているログ バックアップ データを初めて削除するときに、 BR がデータの削除に失敗する問題を修正[#38229](https://github.com/pingcap/tidb/issues/38229) @ [レヴルス](https://github.com/leavrth)

    -   TiCDC

        -   `changefeed query`結果のうち`sasl-password`マスクされない問題を修正[#7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴィーデン](https://github.com/dveeden)
        -   etcd トランザクションでコミットされる操作が多すぎると TiCDC が使用できなくなる可能性がある問題を修正[#7131](https://github.com/pingcap/tiflow/issues/7131) @ [東門](https://github.com/asddongmen)
        -   REDO ログが誤って削除される場合がある問題を修正[#6413](https://github.com/pingcap/tiflow/issues/6413) @ [東門](https://github.com/asddongmen)
        -   Kafka Sink V2 [#7344](https://github.com/pingcap/tiflow/issues/7344) @ [こんにちはラスティン](https://github.com/hi-rustin)でワイド テーブルをレプリケートするときのパフォーマンスの低下を修正
        -   チェックポイント ts が正しく進められない可能性がある問題を修正[#7274](https://github.com/pingcap/tiflow/issues/7274) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   マウンターモジュール[#7235](https://github.com/pingcap/tiflow/issues/7235) @ [こんにちはラスティン](https://github.com/hi-rustin)のログレベルが不適切なため、ログが過剰に出力される問題を修正
        -   TiCDC クラスターに 2 人の所有者[#4051](https://github.com/pingcap/tiflow/issues/4051) @ [東門](https://github.com/asddongmen)が存在する可能性がある問題を修正

    -   TiDB データ移行 (DM)

        -   DM WebUIが間違った`allow-list`パラメータ[#7096](https://github.com/pingcap/tiflow/issues/7096) @ [ズービンウー](https://github.com/zoubingwu)を生成する問題を修正
        -   DM ワーカーが開始時または停止時に一定の確率でデータ競合を引き起こす問題を修正[#6401](https://github.com/pingcap/tiflow/issues/6401) @ [リウメンギャ94](https://github.com/liumengya94)
        -   DM が`UPDATE`または`DELETE`ステートメントをレプリケートするが、対応する行データが存在しない場合、DM はイベント[#6383](https://github.com/pingcap/tiflow/issues/6383) @ [GMHDBJD](https://github.com/GMHDBJD)をサイレントに無視する問題を修正します。
        -   `query-status`コマンド[#7189](https://github.com/pingcap/tiflow/issues/7189) @ [GMHDBJD](https://github.com/GMHDBJD)を実行した後に`secondsBehindMaster`フィールドが表示されない問題を修正します。
        -   チェックポイントを更新すると大規模なトランザクションがトリガーされる可能性がある問題を修正[#5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)
        -   フル タスク モードで、タスクが同期ステージに入ってすぐに失敗すると、DM がアップストリーム テーブル スキーマ情報[#7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)を失う可能性がある問題を修正します。
        -   整合性チェックが有効になっている場合にデッドロックが発生する可能性がある問題を修正[#7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)
        -   タスクの事前チェックに`INFORMATION_SCHEMA`テーブル[#7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)に対する`SELECT`権限が必要である問題を修正
        -   空の TLS 構成によりエラー[#7384](https://github.com/pingcap/tiflow/issues/7384) @ [リウメンギャ94](https://github.com/liumengya94)が発生する問題を修正

    -   TiDB Lightning

        -   `binary`エンコード形式[#38351](https://github.com/pingcap/tidb/issues/38351) @ [dsダシュン](https://github.com/dsdashun)の文字列型列を含むターゲット テーブルに Apache Parquet ファイルをインポートするときのインポート パフォーマンスの低下を修正しました。

    -   TiDBDumpling

        -   多数のテーブル[#36549](https://github.com/pingcap/tidb/issues/36549) @ [ランス6716](https://github.com/lance6716)をエクスポートするとDumpling がタイムアウトになる可能性がある問題を修正
        -   整合性ロックが有効になっているが、アップストリームにターゲット テーブル[#38683](https://github.com/pingcap/tidb/issues/38683) @ [ランス6716](https://github.com/lance6716)がない場合に報告されるロック エラーを修正しました。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [645775992](https://github.com/645775992)
-   [DJ](https://github.com/An-DJ)
-   [アンドリューディ](https://github.com/AndrewDi)
-   [エルワドバ](https://github.com/erwadba)
-   [ふざ1989](https://github.com/fuzhe1989)
-   [ゴールドウィンドティン](https://github.com/goldwind-ting) (初投稿者)
-   [h3n4l](https://github.com/h3n4l)
-   [イクスリン](https://github.com/igxlin) (初投稿者)
-   [イクシム](https://github.com/ihcsim)
-   [ジガオルオ](https://github.com/JigaoLuo)
-   [モルゴ](https://github.com/morgo)
-   [ランシー](https://github.com/Ranxy)
-   [シェンキデバオジ](https://github.com/shenqidebaozi) (初投稿者)
-   [桃峰流](https://github.com/taofengliu) (初投稿者)
-   [TszKitLo40](https://github.com/TszKitLo40)
-   [wxbty](https://github.com/wxbty) (初投稿者)
-   [zgcbj](https://github.com/zgcbj)

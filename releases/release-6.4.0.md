---
title: TiDB 6.4.0 Release Notes
summary: TiDB 6.4.0-DMR では、クラスターを特定の時点に復元するサポート、リニア ハッシュ パーティション構文との互換性、高性能な AUTO_INCREMENT` モードなどの新機能と改善が導入されています。また、障害回復、メモリ使用量の制御、統計収集も強化されています。TiFlashは保存時の暗号化に SM4 アルゴリズムをサポートするようになり、TiCDC は Kafka へのデータ複製をサポートしています。このリリースには、さまざまなツールとコンポーネントにわたるバグ修正と改善も含まれています。
---

# TiDB 6.4.0 リリースノート {#tidb-6-4-0-release-notes}

発売日: 2022年11月17日

TiDB バージョン: 6.4.0-DMR

> **注記：**
>
> TiDB 6.4.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.4/)になりました。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨しています。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb)

v6.4.0-DMR の主な新機能と改善点は次のとおりです。

-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) (実験的) を使用して、クラスターを特定の時点に復元することをサポートします。
-   TiDB インスタンス[グローバルメモリ使用量の追跡](/configure-memory-usage.md)をサポートします (実験的)。
-   [線形ハッシュ分割構文](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)と互換性があること。
-   高性能かつ全体的に単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) (実験的) をサポートします。
-   [JSON型](/data-type-json.md)配列データの範囲選択をサポートします。
-   ディスク障害やスタックした I/O などの極端な状況での障害回復を高速化します。
-   テーブルの結合順序を決定するには[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)追加します。
-   相関サブクエリに対して非相関化を実行するかどうかを制御するには[新しいオプティマイザヒント`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)導入します。
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能はGAになります。
-   TiFlash は[保存時の暗号化](/encryption-at-rest.md#tiflash)の SM4 アルゴリズムをサポートします。
-   [テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮します](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)への SQL ステートメントの使用をサポートします。
-   サポート[EBS ボリューム スナップショットを使用して TiDB クラスターをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) 。
-   DM は[上流のデータソース情報を下流のマージされたテーブルの拡張列に書き込む](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)サポートします。

## 新機能 {#new-features}

### 構文 {#sql}

-   SQL ステートメントを使用して、テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮する機能をサポート[＃5315](https://github.com/pingcap/tiflash/issues/5315) @ [ヘヘチェン](https://github.com/hehechen)

    v6.2.0 以降、TiDB はTiFlashのフルテーブルレプリカで[物理データを即座に圧縮する](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact)の機能をサポートしています。適切なタイミングで SQL 文を手動で実行してTiFlash内の物理データを即時に圧縮できるため、storageスペースの削減とクエリパフォーマンスの向上に役立ちます。v6.4.0 では、圧縮するTiFlashレプリカデータの粒度を細かく調整し、テーブル内の指定されたパーティションのTiFlashレプリカを即時に圧縮することをサポートします。

    SQL ステートメント`ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`を実行すると、テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮できます。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (実験的) [＃37197](https://github.com/pingcap/tidb/issues/37197) [＃13303](https://github.com/tikv/tikv/issues/13303) @ [定義2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [じゃがいも](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [ヒューシャープ](https://github.com/HuSharp) @ [カルビンネオ](https://github.com/CalvinNeo)を使用して、クラスターを特定の時点に復元する機能をサポートします。

    `FLASHBACK CLUSTER TO TIMESTAMP`構文を使用すると、ガベージ コレクション (GC) の有効期間内にクラスターを特定の時点にすばやく復元できます。この機能を使用すると、DML の誤った操作を簡単かつ迅速に元に戻すことができます。たとえば、この構文を使用すると、誤って`WHERE`句なしで`DELETE`を実行した後、数分で元のクラスターを復元できます。この機能はデータベース バックアップに依存せず、データが変更された正確な時間を特定するために、さまざまな時点でデータをロールバックすることをサポートします`FLASHBACK CLUSTER TO TIMESTAMP`データベース バックアップを置き換えることはできないことに注意してください。

    `FLASHBACK CLUSTER TO TIMESTAMP`を実行する前に、TiCDC などのツールで実行されている PITR およびレプリケーション タスクを一時停止し、 `FLASHBACK`完了後に再起動する必要があります。そうしないと、レプリケーション タスクが失敗する可能性があります。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   `FLASHBACK DATABASE` [＃20463](https://github.com/pingcap/tidb/issues/20463) @ [エルワドバ](https://github.com/erwadba)を使用して削除されたデータベースの復元をサポートします

    `FLASHBACK DATABASE`使用すると、ガベージコレクション(GC) の有効期間内に`DROP`によって削除されたデータベースとそのデータを復元できます。この機能は外部ツールに依存しません。SQL ステートメントを使用してデータとメタデータをすばやく復元できます。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-flashback-database.md)参照してください。

### Security {#security}

-   TiFlashは保存時の暗号化にSM4アルゴリズムをサポートしています[＃5953](https://github.com/pingcap/tiflash/issues/5953) @ [リデズ](https://github.com/lidezhu)

    保存時のTiFlash暗号化に SM4 アルゴリズムを追加します。保存時の暗号化を構成する場合、 `tiflash-learner.toml`構成ファイルで`data-encryption-method`構成の値を`sm4-ctr`に設定することで、SM4 暗号化機能を有効にすることができます。

    詳細については[ユーザードキュメント](/encryption-at-rest.md#tiflash)参照してください。

### 可観測性 {#observability}

-   クラスタ診断は GA [＃1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @ [ホークソンジー](https://github.com/Hawkson-jee)になります

    TiDB ダッシュボードの[クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能は、指定された時間範囲内でクラスターに存在する可能性のある問題を診断し、診断結果とクラスター関連の負荷監視情報を[診断レポート](/dashboard/dashboard-diagnostics-report.md)にまとめます。この診断レポートは Web ページの形式です。ブラウザーからページを保存した後、オフラインでページを参照したり、このページのリンクを循環させたりすることができます。

    診断レポートを使用すると、負荷、コンポーネントの状態、時間消費、構成など、クラスターの基本的な健全性情報をすばやく把握できます。クラスターに一般的な問題がある場合は、セクション[診断情報](/dashboard/dashboard-diagnostics-report.md#diagnostic-information)に組み込まれている自動診断の結果で原因を見つけることができます。

### パフォーマンス {#performance}

-   コプロセッサタスク[＃37724](https://github.com/pingcap/tidb/issues/37724) @ [あなた06](https://github.com/you06)の並行適応メカニズムを導入する

    コプロセッサ タスクの数が増えると、TiKV の処理速度に基づいて、TiDB は自動的に同時実行性を高め ( [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の値を調整)、コプロセッサ タスク キューを減らしてレイテンシーを減らします。

-   テーブル結合順序を決定するための動的計画アルゴリズムを追加する[＃37825](https://github.com/pingcap/tidb/issues/37825) @ [ウィノロス](https://github.com/winoros)

    以前のバージョンでは、TiDB は貪欲アルゴリズムを使用してテーブルの結合順序を決定します。v6.4.0 では、TiDB オプティマイザーに[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)導入されています。動的計画アルゴリズムは貪欲アルゴリズムよりも多くの可能な結合順序を列挙できるため、より適切な実行プランが見つかる可能性が高まり、一部のシナリオでは SQL 実行効率が向上します。

    動的プログラミング アルゴリズムはより多くの時間を消費するため、TiDB 結合したテーブルの再配置アルゴリズムの選択は[`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)変数によって制御されます。Join 結合したテーブルの再配置に参加するノードの数がこのしきい値より大きい場合、TiDB は貪欲アルゴリズムを使用します。それ以外の場合、TiDB は動的プログラミング アルゴリズムを使用します。

    詳細については[ユーザードキュメント](/join-reorder.md)参照してください。

-   プレフィックスインデックスは null 値のフィルタリングをサポートします[＃21145](https://github.com/pingcap/tidb/issues/21145) @ [翻訳者](https://github.com/xuyifangreeneyes)

    この機能はプレフィックス インデックスの最適化です。テーブル内の列にプレフィックス インデックスがある場合、SQL ステートメント内の列の`IS NULL`または`IS NOT NULL`条件をプレフィックスで直接フィルター処理できます。これにより、この場合のテーブル検索が回避され、SQL 実行のパフォーマンスが向上します。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)参照してください。

-   TiDB チャンク再利用メカニズム[＃38606](https://github.com/pingcap/tidb/issues/38606) @ [学習を続ける20221](https://github.com/keeplearning20221)を強化する

    以前のバージョンでは、TiDB は`writechunk`関数でのみチャンクを再利用していました。TiDB v6.4.0 では、チャンク再利用メカニズムが Executor の演算子に拡張されています。チャンクを再利用することで、TiDB は頻繁にメモリ解放を要求する必要がなくなり、一部のシナリオでは SQL クエリがより効率的に実行されます。システム変数[`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)を使用して、チャンク オブジェクトを再利用するかどうかを制御できます。これはデフォルトで有効になっています。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)参照してください。

-   相関サブクエリ[＃37789](https://github.com/pingcap/tidb/issues/37789) @ [時間と運命](https://github.com/time-and-fate)の相関解除を実行するかどうかを制御する新しいオプティマイザヒント`NO_DECORRELATE`を導入します。

    デフォルトでは、TiDB は常に相関サブクエリを書き換えて非相関化を実行しようとします。これにより、通常は実行効率が向上します。ただし、シナリオによっては、非相関化によって実行効率が低下することがあります。v6.4.0 では、TiDB はオプティマイザー ヒント`NO_DECORRELATE`を導入し、指定されたクエリ ブロックに対して非相関化を実行しないようにオプティマイザーに指示して、一部のシナリオでクエリ パフォーマンスを向上させます。

    詳細については[ユーザードキュメント](/optimizer-hints.md#no_decorrelate)参照してください。

-   パーティション化されたテーブル[＃37977](https://github.com/pingcap/tidb/issues/37977) @ [イサール](https://github.com/Yisaer)での統計収集のパフォーマンスを向上

    v6.4.0 では、TiDB はパーティション化されたテーブルでの統計収集戦略を最適化します。システム変数[`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)を使用して、パーティション化されたテーブルでの統計収集の同時実行性を並列に設定し、収集を高速化し、分析時間を短縮できます。

### 安定性 {#stability}

-   ディスク障害やスタックI/O [＃13648](https://github.com/tikv/tikv/issues/13648) @ [リクササシネーター](https://github.com/LykxSassinator)などの極端な状況での障害回復を高速化

    エンタープライズ ユーザーにとって、データベースの可用性は最も重要な指標の 1 つです。複雑なハードウェア環境では、障害を迅速に検出して回復する方法が常にデータベースの可用性の課題の 1 つとなっています。v6.4.0 では、TiDB は TiKV ノードの状態検出メカニズムを完全に最適化しています。ディスク障害や I/O スタックなどの極端な状況でも、TiDB はノードの状態を迅速に報告し、アクティブ ウェイクアップ メカニズムを使用して事前にLeader選出を開始することで、クラスターの自己修復を加速します。この最適化により、TiDB はディスク障害が発生した場合のクラスターの回復時間を約 50% 短縮できます。

-   TiDBメモリ使用量のグローバル制御[＃37816](https://github.com/pingcap/tidb/issues/37816) @ [うわー](https://github.com/wshwsh12)

    v6.4.0 では、TiDB インスタンスのグローバルメモリ使用量を追跡する実験的機能として、メモリ使用量のグローバル制御が導入されています。システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)を使用して、グローバルメモリ使用量の上限を設定できます。メモリ使用量がしきい値に達すると、TiDB は空きメモリを再利用して解放しようとします。メモリ使用量がしきい値を超えると、TiDB はメモリ使用量が最も高い SQL 操作を識別してキャンセルし、過剰なメモリ使用量によるシステムの問題を回避します。

    TiDB インスタンスのメモリ消費に潜在的なリスクがある場合、TiDB は事前に診断情報を収集し、指定されたディレクトリに書き込み、問題の診断を容易にします。同時に、TiDB はメモリ使用量と操作履歴を表示するシステム テーブル ビュー[`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)と[`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)を提供し、メモリ使用量をよりよく理解するのに役立ちます。

    グローバルメモリ制御は、TiDBメモリ管理におけるマイルストーンです。インスタンスのグローバル ビューを導入し、メモリの体系的な管理を採用することで、より多くの重要なシナリオでデータベースの安定性とサービスの可用性を大幅に向上できます。

    詳細については[ユーザードキュメント](/configure-memory-usage.md)参照してください。

-   範囲構築オプティマイザのメモリ使用量を制御する[＃37176](https://github.com/pingcap/tidb/issues/37176) @ [翻訳者](https://github.com/xuyifangreeneyes)

    v6.4.0 では、範囲を構築するオプティマイザの最大メモリ使用量を制限するために、システム変数[`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)が導入されました。メモリ使用量が制限を超えると、オプティマイザは、より正確な範囲ではなく、より粗い範囲を構築して、メモリ消費を削減します。SQL ステートメントに`IN`条件が多数ある場合、この最適化により、コンパイルのメモリ使用量が大幅に削減され、システムの安定性が確保されます。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_opt_range_max_size-new-in-v640)参照してください。

-   統計情報の同期読み込みをサポート (GA) [＃37434](https://github.com/pingcap/tidb/issues/37434) @ [クリサン](https://github.com/chrysan)

    TiDB v6.4.0 では、統計の同期ロード機能がデフォルトで有効になっています。この機能により、SQL ステートメントを実行するときに、TiDB は大規模な統計 (ヒストグラム、TopN、Count-Min Sketch 統計など) をメモリに同期的にロードできるため、SQL 最適化の統計の完全性が向上します。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)参照してください。

-   軽量トランザクション書き込みの応答時間に対するバッチ書き込み要求の影響を軽減する[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

    一部のシステムのビジネス ロジックでは、定期的なバッチ DML タスクが必要ですが、これらのバッチ書き込みタスクを処理すると、オンライン トランザクションのレイテンシーが長くなります。v6.3.0 では、TiKV はハイブリッド ワークロード シナリオでの読み取り要求のスケジュールを最適化するため、 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)構成項目を有効にすると、TiKV がすべての読み取り要求の UnifyReadPool スレッド プールのサイズを自動的に調整できるようになります。v6.4.0 では、TiKV は書き込み要求を動的に識別して優先順位を付けることもでき、1 回のポーリングで 1 つの FSM (有限状態マシン) に適用スレッドが書き込むことができる最大バイト数を制御できるため、バッチ書き込み要求がトランザクション書き込みの応答時間に与える影響が軽減されます。

### 使いやすさ {#ease-of-use}

-   TiKV API V2 が一般提供開始 (GA) [＃11745](https://github.com/tikv/tikv/issues/11745) @ [ピンギュ](https://github.com/pingyu)

    v6.1.0 より前の TiKV では、クライアントから渡された生データのみを保存するため、基本的なキー値の読み取りおよび書き込み機能のみが提供されます。さらに、コーディング方法の違いと範囲指定されていないデータ範囲のため、TiDB、トランザクション KV、および RawKV を同じ TiKV クラスターで同時に使用することはできません。代わりに、この場合は複数のクラスターが必要になり、マシンと展開のコストが増加します。

    TiKV API V2 は、新しい RawKVstorage形式とアクセス インターフェイスを提供し、次のような利点をもたらします。

    -   記録されたデータの変更タイムスタンプとともに MVCC にデータを保存し、それに基づいて変更データ キャプチャ (CDC) を実装します。この機能は実験的であり、 [ティKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)で詳しく説明されています。
    -   データはさまざまな用途に応じてスコープ設定され、API V2 は単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
    -   マルチテナントなどの機能をサポートするために、キー スペース フィールドを予約します。

    TiKV API V2 を有効にするには、TiKV 構成ファイルの`[storage]`セクションで`api-version = 2`設定します。

    詳細については[ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610)参照してください。

-   TiFlashデータ複製の進行状況[＃4902](https://github.com/pingcap/tiflash/issues/4902) @ [ヘヘチェン](https://github.com/hehechen)の精度を向上

    TiDB では、 `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの`PROGRESS`フィールドは、TiKV の対応するテーブルからTiFlashレプリカへのデータ複製の進行状況を示すために使用されます。以前のバージョンの TiDB では、 `PROCESS`フィールドはTiFlashレプリカの作成中のTiFlash複製の進行状況のみを示します。TiFlash レプリカの作成後、新しいデータが TiKV の対応するテーブルにインポートされた場合、このフィールドは更新されず、新しいデータの TiKV からTiFlashへの複製の進行状況は表示されません。

    v6.4.0 では、TiDB はTiFlashレプリカのデータ レプリケーションの進行状況の更新メカニズムを改善しました。TiFlash レプリカの作成後、新しいデータが TiKV の対応するテーブルにインポートされると、 [`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)テーブルの`PROGRESS`TiFlashが更新され、新しいデータの TiKV からTiFlashへの実際のレプリケーションの進行状況が表示されます。この改善により、 TiFlashデータ レプリケーションの実際の進行状況を簡単に確認できます。

    詳細については[ユーザードキュメント](/information-schema/information-schema-tiflash-replica.md)参照してください。

### MySQL 互換性 {#mysql-compatibility}

-   線形ハッシュパーティション構文[＃38450](https://github.com/pingcap/tidb/issues/38450) @ [ミョンス](https://github.com/mjonss)と互換性がある

    以前のバージョンでは、TiDB はハッシュ、範囲、およびList パーティショニングをサポートしていました。v6.4.0 以降では、TiDB は[MySQL リニアハッシュパーティショニング](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)の構文とも互換性があります。

    TiDB では、MySQL リニア ハッシュ パーティションの既存の DDL ステートメントを直接実行でき、TiDB は対応するハッシュ パーティション テーブルを作成します (TiDB 内にはリニア ハッシュ パーティションがないことに注意してください)。また、MySQL リニア ハッシュ パーティションの既存の DML ステートメントを直接実行することもできます。TiDB は対応する TiDB ハッシュ パーティションのクエリ結果を通常どおり返します。この機能により、MySQL リニア ハッシュ パーティションとの TiDB 構文の互換性が確保され、MySQL ベースのアプリケーションから TiDB へのシームレスな移行が容易になります。

    パーティション数が 2 の累乗の場合、TiDB ハッシュパーティションテーブルの行は、MySQL リニア ハッシュパーティションテーブルの行と同じように分散されます。それ以外の場合、TiDB でのこれらの行の分散は、MySQL とは異なります。

    詳細については[ユーザードキュメント](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)参照してください。

-   高性能かつ全体的に単調な`AUTO_INCREMENT` (実験的) [＃38442](https://github.com/pingcap/tidb/issues/38442) @ [天菜まお](https://github.com/tiancaiamao)をサポートする

    TiDB v6.4.0 では、 `AUTO_INCREMENT` MySQL 互換モードが導入されています。このモードでは、すべての TiDB インスタンスで ID が単調に増加するようにする集中型の自動増分 ID 割り当てサービスが導入されています。この機能により、自動増分 ID によるクエリ結果の並べ替えが容易になります。MySQL 互換モードを使用するには、テーブルの作成時に`AUTO_ID_CACHE`から`1`に設定する必要があります。次に例を示します。

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    詳細については[ユーザードキュメント](/auto-increment.md#mysql-compatibility-mode)参照してください。

-   JSON型[＃13644](https://github.com/tikv/tikv/issues/13644) @ [ヤンケオ](https://github.com/YangKeao)の配列データの範囲選択をサポート

    v6.4.0 以降では、TiDB で MySQL 互換[範囲選択構文](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths)使用できます。

    -   キーワード`to`を使用すると、配列要素の開始位置と終了位置を指定し、配列内の連続した範囲の要素を選択できます。 `0`を使用すると、配列の最初の要素の位置を指定できます。 たとえば、 `$[0 to 2]`を使用すると、配列の最初の 3 つの要素を選択できます。

    -   キーワード`last`を使用すると、配列の最後の要素の位置を指定できます。これにより、右から左への位置を設定できます。たとえば、 `$[last-2 to last]`使用すると、配列の最後の 3 つの要素を選択できます。

    この機能により、SQL ステートメントの記述プロセスが簡素化され、JSON 型の互換性がさらに向上し、MySQL アプリケーションを TiDB に移行する際の難易度が軽減されます。

-   データベースユーザー[＃38172](https://github.com/pingcap/tidb/issues/38172) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の追加説明の追加をサポート

    TiDB v6.4 では、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)使用して、データベース ユーザー向けの追加の説明を追加できます。TiDB には 2 つの説明形式があります。 `COMMENT`を使用してテキスト コメントを追加し、 `ATTRIBUTE`を使用して JSON 形式の構造化属性のセットを追加できます。

    さらに、TiDB v6.4.0 では、ユーザーコメントとユーザー属性の情報を表示できる[`USER_ATTRIBUTES`](/information-schema/information-schema-user-attributes.md)テーブルが追加されました。

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

    この機能により、TiDB と MySQL 構文の互換性が向上し、MySQL エコシステム内のツールやプラットフォームへの TiDB の統合が容易になります。

### バックアップと復元 {#backup-and-restore}

-   EBS ボリューム スナップショット[＃33849](https://github.com/pingcap/tidb/issues/33849) @ [フェンゴウ1](https://github.com/fengou1)を使用して TiDB クラスターのバックアップをサポート

    TiDB クラスターが EKS にデプロイされ、AWS EBS ボリュームを使用しており、TiDB クラスター データをバックアップする際に次の要件がある場合は、 TiDB Operator を使用してボリューム スナップショットとメタデータごとにデータを AWS S3 にバックアップできます。

    -   バックアップの影響を最小限に抑えます。たとえば、QPS とトランザクションのレイテンシーへの影響を 5% 未満に抑え、クラスターの CPU とメモリを占有しないようにします。
    -   短時間でデータをバックアップおよび復元します。たとえば、1 時間以内にバックアップを完了し、2 時間以内にデータを復元します。

    詳細については[ユーザードキュメント](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)参照してください。

### データ移行 {#data-migration}

-   DMは、下流のマージされたテーブル[＃37797](https://github.com/pingcap/tidb/issues/37797) @ [リチュンジュ](https://github.com/lichunzhu)の拡張列への上流データソース情報の書き込みをサポートします。

    上流から TiDB にシャードされたスキーマとテーブルをマージする場合、ターゲット テーブルに複数のフィールド (拡張列) を手動で追加し、DM タスクを構成するときにその値を指定できます。たとえば、拡張列に上流のシャードされたスキーマとテーブルの名前を指定すると、DM によって下流に書き込まれるデータにはスキーマ名とテーブル名が含まれます。下流のデータが異常な場合、この機能を使用して、スキーマ名やテーブル名などのターゲット テーブルのデータ ソース情報をすばやく見つけることができます。

    詳細については[テーブル、スキーマ、ソース情報を抽出し、マージされたテーブルに書き込みます。](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)参照してください。

-   DMは、いくつかの必須チェック項目をオプションのチェック項目に変更することで、事前チェックのメカニズムを最適化します[＃7333](https://github.com/pingcap/tiflow/issues/7333) @ [リチュンジュ](https://github.com/lichunzhu)

    データ移行タスクをスムーズに実行するために、DM はタスクの開始時に[事前チェック](/dm/dm-precheck.md)自動的にトリガーし、チェック結果を返します。DM は、事前チェックに合格した後にのみ移行を開始します。

    v6.4.0 では、DM は次の 3 つのチェック項目を必須からオプションに変更し、事前チェックの合格率を向上させます。

    -   アップストリーム テーブルが TiDB と互換性のない文字セットを使用しているかどうかを確認します。
    -   上流テーブルに主キー制約または一意キー制約があるかどうかを確認します。
    -   プライマリ/セカンダリ構成でアップストリーム データベースのデータベース ID `server_id`が指定されているかどうかを確認します。

-   DM は、増分移行タスク[＃7393](https://github.com/pingcap/tiflow/issues/7393) @ [GMHDBJD](https://github.com/GMHDBJD)のオプション パラメータとして、 binlog の位置と GTID の設定をサポートしています。

    v6.4.0 以降では、 binlog の位置や GTID を指定せずに直接増分移行を実行できます。DM は、タスク開始後に生成されたbinlogファイルを上流から自動的に取得し、これらの増分データを下流に移行します。これにより、ユーザーは面倒な理解や複雑な設定から解放されます。

    詳細については[DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)参照してください。

-   DM は移行タスク[＃7343](https://github.com/pingcap/tiflow/issues/7343) @ [ok江](https://github.com/okJiang)のステータス インジケーターを追加します

    v6.4.0 では、DM は移行タスクのパフォーマンスと進行状況のインジケーターをさらに追加しました。これにより、移行のパフォーマンスと進行状況をより直感的に理解できるようになり、トラブルシューティングの参照としても役立ちます。

    -   データのインポートとエクスポートのパフォーマンスを示すステータス インジケーター (バイト/秒単位) を追加します。
    -   ダウンストリーム データベースにデータを書き込むためのパフォーマンス インジケーターの名前を TPS から RPS (行数/秒) に変更します。
    -   DM 完全移行タスクのデータ エクスポートの進行状況を示す進行状況インジケーターを追加します。

    これらの指標の詳細については、 [TiDB データ移行におけるクエリタスクステータス](/dm/dm-query-status.md)参照してください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDCは、 `3.2.0`バージョン[＃7191](https://github.com/pingcap/tiflow/issues/7191) @ [3エースショーハンド](https://github.com/3AceShowHand)のKafkaへのデータのレプリケーションをサポートしています。

    v6.4.0 以降、TiCDC は`3.2.0`バージョンのうち[Kafka へのデータの複製](/replicate-data-to-kafka.md)それ以前のバージョンをサポートします。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)         | 修正済み     | GLOBAL スコープを削除し、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)構成項目を使用してデフォルト値を変更できるようにします。この変数は、TiDB が悲観的トランザクションで一意の制約をチェックするタイミングを制御します。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                 | 修正済み     | v6.4.0 から有効になり、 [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)の同時実行を制御します。デフォルト値は`64`です。                                                                                                      |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)                                        | 修正済み     | デフォルト値を`INT_ONLY`から`ON`に変更します。これは、主キーがデフォルトでクラスター化インデックスとして作成されることを意味します。                                                                                                                                                             |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                                                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、コプロセッサ要求を送信するためのページング方式がデフォルトで使用されることを意味します。                                                                                                                                                             |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                               | 修正済み     | SESSION スコープを追加します。この変数は[プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)を有効にするかどうかを制御します。                                                                                                                                                 |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)                                               | 修正済み     | デフォルト値を`0.8`から`0.7`に変更します。この変数は、tidb-serverメモリアラームをトリガーするメモリ使用率を制御します。                                                                                                                                                                |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)                                                             | 修正済み     | GLOBAL スコープを追加します。この変数は、オプティマイザーが集計関数を Join、Projection、および UnionAll の前の位置にプッシュダウンする最適化操作を実行するかどうかを制御します。                                                                                                                              |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                   | 修正済み     | SESSION スコープを追加します。この変数は、セッションでキャッシュできるプランの最大数を制御します。                                                                                                                                                                                 |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                           | 修正済み     | デフォルト値を`0`から`100`に変更します。つまり、SQL 実行は、完全な列統計を同期的にロードするために、デフォルトで最大 100 ミリ秒待機できます。                                                                                                                                                       |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)                                 | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、完全な列統計を同期的にロードするタイムアウトに達した後、SQL 最適化が疑似統計の使用に戻ることを意味します。                                                                                                                                                  |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640)                                                         | 新しく追加された | 前のステートメントがキャッシュされたチャンク オブジェクト (チャンク割り当て) を使用するかどうかを示します。この変数は読み取り専用で、デフォルト値は`OFF`です。                                                                                                                                                  |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)                 | 新しく追加された | パーティションテーブルを分析するときに TiDB が[自動的に分析する](/statistics.md#automatic-update)実行できるパーティションの数を指定します (つまり、パーティションテーブルの統計情報を自動的に収集します)。デフォルト値は`1`です。                                                                                              |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)                                     | 新しく追加された | TiDB が[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)で指定されたタイムスタンプでデータを読み取るかどうかを制御します。デフォルト値は`OFF`です。                                                                                                         |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640)                                                 | 新しく追加された | GOGC チューナーを有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                             |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)                                               | 新しく追加された | TiDB がチャンク オブジェクト キャッシュを有効にするかどうかを制御します。デフォルト値は`ON`です。これは、TiDB がキャッシュされたチャンク オブジェクトを優先して使用し、要求されたオブジェクトがキャッシュにない場合にのみシステムから要求することを意味します。値が`OFF`の場合、TiDB はシステムからチャンク オブジェクトを直接要求します。                                                   |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | 新しく追加された | プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                               |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)                                                             | 新しく追加された | デフォルト値は`0`です。3 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) `ON`設定すると、TiDB はこの変数で指定されたタイムスタンプでデータを読み取ります。                                                                          |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640)                                           | 新しく追加された | GOGC をチューニングするための最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC チューナーは動作を停止します。デフォルト値は`0.6`です。                                                                                                                                                  |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)               | 新しく追加された | tidb-server のメモリ使用量がメモリアラームしきい値を超えてアラームをトリガーすると、TiDB はデフォルトで最近の 5 つのアラーム中に生成されたステータス ファイルのみを保持します。この変数を使用してこの数を調整できます。                                                                                                                |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)                           | 新しく追加された | 不要なテーブル検索を回避し、クエリのパフォーマンスを向上させるために、TiDB オプティマイザーが一部のフィルター条件をプレフィックス インデックスにプッシュダウンするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                         |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)                                               | 新しく追加された | オプティマイザがスキャン範囲を構築するためのメモリ使用量の上限を指定します。デフォルト値は`67108864` (64 MiB) です。                                                                                                                                                                  |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                             | 新しく追加された | スキャン範囲を構築するためのオプティマイザのメモリ使用量の上限を制御します (実験的)。デフォルト値は`0`で、メモリ制限がないことを意味します。                                                                                                                                                             |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)                       | 新しく追加された | TiDB が GC をトリガーしようとするしきい値を制御します (実験的)。デフォルト値は`70%`です。                                                                                                                                                                                 |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)                 | 新しく追加された | メモリ制限を有効にすると、TiDB は現在のインスタンスでメモリ使用量が最も高い SQL ステートメントを終了します。この変数は、終了する SQL ステートメントの最小メモリ使用量を指定します。デフォルト値は`134217728` (128 MiB) です。                                                                                                     |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                           | タイプを変更   | 説明                                                                                                                                                                   |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | `tidb_memory_usage_alarm_ratio`                                                                                                           | 削除されました  | この構成項目は無効になりました。                                                                                                                                                     |
| ティビ            | `memory-usage-alarm-ratio`                                                                                                                | 削除されました  | システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)に置き換えられます。この構成項目が v6.4.0 より前のバージョンの TiDB で構成されている場合、アップグレード後に有効になりません。    |
| ティビ            | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)  | 新しく追加された | システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。デフォルト値は`true`です。      |
| ティビ            | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640)                                                    | 新しく追加された | チャンク割り当てのキャッシュされたチャンク オブジェクトの最大数を制御します。デフォルト値は`64`です。                                                                                                                |
| ティビ            | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640)                                                  | 新しく追加された | チャンク割り当てのキャッシュされた列オブジェクトの最大数を制御します。デフォルト値は`256`です。                                                                                                                   |
| ティクヴ           | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | 非推奨      | この構成項目は無効になりました。                                                                                                                                                     |
| ティクヴ           | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640)                                              | 新しく追加された | 事前に割り当てられた TSO キャッシュ サイズ (期間)。デフォルト値は`3s`です。                                                                                                                         |
| ティクヴ           | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)                                          | 新しく追加された | タイムスタンプ要求内の TSO の最大数を制御します。デフォルト値は`8192`です。                                                                                                                          |
| ティクヴ           | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640)                                      | 新しく追加された | 1 回のポーリングで 1 つの FSM (有限状態マシン) に適用スレッドが書き込むことができる最大バイト数を制御します。デフォルト値は`32KiB`です。これはソフト制限です。                                                                            |
| PD             | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)                                                  | 新しく追加された | v6.4.0 から有効になり、PD が TSO の物理時間を更新する間隔を制御します。デフォルト値は`50ms`です。                                                                                                          |
| TiFlash        | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)                                      | 修正済み     | 新しい値オプション`sm4-ctr`が導入されました。この構成項目が`sm4-ctr`に設定されている場合、データは保存される前に SM4 を使用して暗号化されます。                                                                                  |
| DM             | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                      | 新しく追加された | オプション。シャーディング シナリオで、シャーディングされたテーブルのソース情報を抽出するために使用します。抽出された情報は、データ ソースを識別するために、ダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。 |
| DM             | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディング シナリオで、シャーディングされたスキーマのソース情報を抽出するために使用します。抽出された情報は、データ ソースを識別するために、ダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。 |
| DM             | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディング シナリオでソース インスタンス情報を抽出するために使用します。抽出された情報は、データ ソースを識別するために、ダウンストリームのマージされたテーブルに書き込まれます。このパラメータが設定されている場合は、事前にダウンストリームにマージされたテーブルを手動で作成する必要があります。          |
| ティCDC          | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)                                             | 修正済み     | デフォルト値を`table`から`none`に変更します。この変更により、レプリケーションのレイテンシーと OOM のリスクが軽減されます。さらに、TiCDC は、すべてのトランザクションではなく、いくつかのトランザクション (1 つのトランザクションのサイズが 1024 行を超える) のみを分割するようになりました。     |

### その他 {#others}

-   v6.4.0 以降、 `mysql.user`テーブルに`User_attributes`と`Token_issuer` 2 つの新しい列が追加されます。以前の TiDB バージョンのバックアップ データを TiDB v6.4.0 に[`mysql`スキーマのシステムテーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)すると、 BR は`mysql.user`テーブルに対して`column count mismatch`エラーを報告します。13 スキーマでシステム テーブルを復元しないと、このエラーは報告されませ`mysql` 。
-   名前が[Dumplingエクスポートファイルの形式](/dumpling-overview.md#format-of-exported-files)に一致するが、非圧縮形式で終わるファイル ( `test-schema-create.sql.origin`や`test.table-schema.sql.origin`など) については、 TiDB Lightningによる処理方法が変更されました。v6.4.0 より前では、インポートするファイルにこのようなファイルが含まれている場合、 TiDB Lightning はそのようなファイルのインポートをスキップします。v6.4.0 以降では、 TiDB Lightningはそのようなファイルがサポートされていない圧縮形式を使用していると想定するため、インポート タスクは失敗します。
-   v6.4.0 以降では、権限`SYSTEM_VARIABLES_ADMIN`または`SUPER`を持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。

## 改善点 {#improvements}

-   ティビ

    -   noop変数の変更を許可する`lc_messages` [＃38231](https://github.com/pingcap/tidb/issues/38231) @ [翻訳者](https://github.com/djshow832)
    -   クラスター化複合インデックス[＃38572](https://github.com/pingcap/tidb/issues/38572) @ [タンジェンタ](https://github.com/tangenta)の最初の列として`AUTO_RANDOM`列をサポートします。
    -   内部トランザクション再試行で悲観的トランザクションを使用して再試行の失敗を回避し、時間の消費を削減する[＃38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキー](https://github.com/jackysp)

-   ティクヴ

    -   新しい構成項目`apply-yield-write-size`を追加して、Apply スレッドが 1 回のポーリングで 1 つの有限状態マシンに書き込むことができる最大バイト数を制御し、Apply スレッドが大量のデータを書き込むときにRaftstore の輻輳を緩和します[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)
    -   リーダー転送プロセス中の QPS ジッターを回避するために、リージョンのリーダーを移行する前にエントリ キャッシュをウォームアップします[＃13060](https://github.com/tikv/tikv/issues/13060) @ [コスベン](https://github.com/cosven)
    -   `json_constrains`演算子をコプロセッサー[＃13592](https://github.com/tikv/tikv/issues/13592) @ [李鎮歓](https://github.com/lizhenhuan)にプッシュダウンするサポート
    -   いくつかのシナリオでフラッシュパフォーマンスを向上させるために、 `CausalTsProvider`非同期関数を追加します[＃13428](https://github.com/tikv/tikv/issues/13428) @ [沢民州](https://github.com/zeminzhou)

-   PD

    -   ホットリージョンスケジューラのv2アルゴリズムがGAになります。いくつかのシナリオでは、v2アルゴリズムは両方の構成されたディメンションでよりよいバランスを実現し、無効なスケジューリング[＃5021](https://github.com/tikv/pd/issues/5021) @ [フンドゥンDM](https://github.com/hundundm)を減らすことができます。
    -   オペレータステップのタイムアウトメカニズムを最適化して、早期のタイムアウトを回避する[＃5596](https://github.com/tikv/pd/issues/5596) @ [バッファフライ](https://github.com/bufferflies)
    -   大規模クラスタのスケジューラのパフォーマンスを向上[＃5473](https://github.com/tikv/pd/issues/5473) @ [バッファフライ](https://github.com/bufferflies)
    -   PD [＃5637](https://github.com/tikv/pd/issues/5637) @ [翻訳者](https://github.com/lhy1024)で提供されていない外部タイムスタンプの使用をサポートします

-   TiFlash

    -   TiFlash MPP エラー処理ロジックをリファクタリングして、MPP [＃5095](https://github.com/pingcap/tiflash/issues/5095) @ [風の話し手](https://github.com/windtalker)の安定性をさらに向上します。
    -   TiFlash計算プロセスのソートを最適化し、結合と集計[＃5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツ](https://github.com/solotzg)のキー処理を最適化します。
    -   デコード時のメモリ使用量を最適化し、冗長な転送列を削除して結合パフォーマンスを向上させる[＃6157](https://github.com/pingcap/tiflash/issues/6157) @ [いいえ](https://github.com/yibin87)

-   ツール

    -   TiDBダッシュボード

        -   監視ページでのTiFlashメトリックの表示をサポートし、そのページでのメトリックの表示を最適化します[＃1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @ [宜尼Xu9506](https://github.com/YiniXu9506)
        -   スロークエリリストとSQLステートメントリストに結果の行数を表示します[＃1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @ [バウリン](https://github.com/baurine)
        -   Alertmanager が存在しない場合に Alertmanager エラーを報告しないようにダッシュボードを最適化します[＃1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @ [バウリン](https://github.com/baurine)

    -   バックアップと復元 (BR)

        -   メタデータをロードするメカニズムを改善しました。メタデータは必要な場合にのみメモリにロードされるため、PITR [＃38404](https://github.com/pingcap/tidb/issues/38404) @ [ユジュンセン](https://github.com/YuJuncen)中のメモリ使用量が大幅に削減されます。

    -   ティCDC

        -   交換パーティション DDL ステートメント[＃639](https://github.com/pingcap/tiflow/issues/639) @ [アズドンメン](https://github.com/asddongmen)の複製をサポート
        -   MQシンクモジュール[＃7353](https://github.com/pingcap/tiflow/issues/7353) @ [ハイラスティン](https://github.com/Rustin170506)の非バッチ送信パフォーマンスを向上
        -   テーブルに多数のリージョン[＃7078](https://github.com/pingcap/tiflow/issues/7078) [＃7281](https://github.com/pingcap/tiflow/issues/7281) @ [スドジ](https://github.com/sdojjy)がある場合の TiCDC プラーのパフォーマンスを向上
        -   同期ポイントが有効な場合、 `tidb_enable_external_ts_read`変数を使用して下流 TiDB の履歴データの読み取りをサポートします[＃7419](https://github.com/pingcap/tiflow/issues/7419) @ [アズドンメン](https://github.com/asddongmen)
        -   レプリケーションの安定性を向上させるために、トランザクション分割を有効にし、セーフモードをデフォルトで無効にします[＃7505](https://github.com/pingcap/tiflow/issues/7505) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   dmctl [＃7246](https://github.com/pingcap/tiflow/issues/7246) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)から不要な`operate-source update`コマンドを削除します
        -   上流データベースが TiDB と互換性のない DDL ステートメントを使用している場合に DM の完全インポートが失敗する問題を修正しました。TiDB でサポートされている DDL ステートメントを使用して、事前に TiDB でターゲット テーブルのスキーマを手動で作成し、インポートが成功するようにすることができます[＃37984](https://github.com/pingcap/tidb/issues/37984) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   ファイルスキャンロジックを最適化してスキーマファイルのスキャンを高速化します[＃38598](https://github.com/pingcap/tidb/issues/38598) @ [ダシュン](https://github.com/dsdashun)

## バグ修正 {#bug-fixes}

-   ティビ

    -   新しいインデックス[＃38165](https://github.com/pingcap/tidb/issues/38165) @ [タンジェンタ](https://github.com/tangenta)を作成した後に発生する可能性のあるインデックスの不整合の問題を修正します
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブル[＃38407](https://github.com/pingcap/tidb/issues/38407) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の権限問題を修正
    -   `mysql.tables_priv`テーブル[＃38293](https://github.com/pingcap/tidb/issues/38293) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃38170](https://github.com/pingcap/tidb/issues/38170) @ [翻訳:](https://github.com/wjhuang2016)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃37928](https://github.com/pingcap/tidb/issues/37928) @ [ヤンケオ](https://github.com/YangKeao)
    -   **トランザクションリージョン番号**監視パネルの情報が正しくない問題を修正[＃38139](https://github.com/pingcap/tidb/issues/38139) @ [ジャッキー](https://github.com/jackysp)
    -   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)が内部トランザクションに影響を与える可能性がある問題を修正しました。変数のスコープは SESSION に変更されました[＃38766](https://github.com/pingcap/tidb/issues/38766) @ [エキシウム](https://github.com/ekexium)
    -   クエリ内の条件が誤って投影[＃35623](https://github.com/pingcap/tidb/issues/35623) @ [思い出させる](https://github.com/Reminiscent)にプッシュダウンされる問題を修正しました
    -   `AND`と`OR`の間違った`isNullRejected`チェック結果が間違ったクエリ結果[＃38304](https://github.com/pingcap/tidb/issues/38304) @ [イサール](https://github.com/Yisaer)を引き起こす問題を修正しました
    -   外部結合が削除されるときに`ORDER BY` in `GROUP_CONCAT`が考慮されず、間違ったクエリ結果[＃18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正しました。
    -   誤ってプッシュダウンされた条件が結合したテーブルの再配置 [＃38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)によって破棄されたときに発生する間違ったクエリ結果の問題を修正しました。

-   ティクヴ

    -   `cgroup`と`mountinfo`レコードが複数ある場合に Gitpod で TiDB が起動に失敗する問題を修正[＃13660](https://github.com/tikv/tikv/issues/13660) @ [タボキ](https://github.com/tabokie)
    -   TiKV メトリックの誤った表現を修正`tikv_gc_compaction_filtered` [＃13537](https://github.com/tikv/tikv/issues/13537) @ [定義2014](https://github.com/Defined2014)
    -   異常な`delete_files_in_range` [＃13534](https://github.com/tikv/tikv/issues/13534) @ [タボキ](https://github.com/tabokie)によるパフォーマンスの問題を修正
    -   スナップショット取得中に期限切れのリースが原因で発生する異常なリージョン競合を修正[＃13553](https://github.com/tikv/tikv/issues/13553) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   最初のバッチで`FLASHBACK`失敗したときに発生したエラーを修正[＃13672](https://github.com/tikv/tikv/issues/13672) [＃13704](https://github.com/tikv/tikv/issues/13704) [＃13723](https://github.com/tikv/tikv/issues/13723) @ [ヒューシャープ](https://github.com/HuSharp)

-   PD

    -   不正確なストリームタイムアウトを修正し、リーダーの切り替えを高速化[＃5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

-   TiFlash

    -   PageStorage GC がページ削除マーカーを適切にクリアしない場合に発生する、WAL ファイルのサイズが大きすぎることによる OOM 問題を修正しました[＃6163](https://github.com/pingcap/tiflash/issues/6163) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiDBダッシュボード

        -   特定の複雑な SQL ステートメントの実行プランをクエリする際の TiDB OOM 問題を修正[＃1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @ [バウリン](https://github.com/baurine)
        -   NgMonitoring が PD ノード[＃164](https://github.com/pingcap/ng-monitoring/issues/164) @ [中文](https://github.com/zhongzc)への接続を失ったときに、 Top SQLスイッチが有効にならない可能性がある問題を修正しました。

    -   バックアップと復元 (BR)

        -   復元プロセス中の PD リーダー切り替えによって発生する復元失敗の問題を修正[＃36910](https://github.com/pingcap/tidb/issues/36910) @ [モクイシュル28](https://github.com/MoCuishle28)
        -   ログバックアップタスクを一時停止できない問題を修正[＃38250](https://github.com/pingcap/tidb/issues/38250) @ [ジョッカウ](https://github.com/joccau)
        -   BR がログバックアップデータを削除するときに、削除すべきでないデータを誤って削除してしまう問題を修正[＃38939](https://github.com/pingcap/tidb/issues/38939) @ [リーヴルス](https://github.com/leavrth)
        -   Azure Blob Storage または Google Cloud Storage に保存されたログ バックアップ データを初めて削除するときにBR がデータを削除できない問題を修正[＃38229](https://github.com/pingcap/tidb/issues/38229) @ [リーヴルス](https://github.com/leavrth)

    -   ティCDC

        -   `changefeed query`の結果のうち`sasl-password`がマスクされていない問題を修正[＃7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴェーデン](https://github.com/dveeden)
        -   etcd トランザクションでコミットされる操作が多すぎると TiCDC が利用できなくなる問題を修正[＃7131](https://github.com/pingcap/tiflow/issues/7131) @ [アズドンメン](https://github.com/asddongmen)
        -   REDOログが誤って削除される可能性がある問題を修正[＃6413](https://github.com/pingcap/tiflow/issues/6413) @ [アズドンメン](https://github.com/asddongmen)
        -   Kafka Sink V2 [＃7344](https://github.com/pingcap/tiflow/issues/7344) @ [ハイラスティン](https://github.com/Rustin170506)でワイド テーブルを複製する際のパフォーマンス低下を修正
        -   チェックポイント ts が誤って[＃7274](https://github.com/pingcap/tiflow/issues/7274) @ [ハイラスティン](https://github.com/Rustin170506)に進められる可能性がある問題を修正しました
        -   マウンタモジュール[＃7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイラスティン](https://github.com/Rustin170506)のログレベルが不適切であるためにログが多すぎるという問題を修正しました
        -   TiCDC クラスターに[＃4051](https://github.com/pingcap/tiflow/issues/4051) @ [アズドンメン](https://github.com/asddongmen)という 2 人の所有者が存在する可能性がある問題を修正しました。

    -   TiDB データ移行 (DM)

        -   DM WebUIが間違った`allow-list`パラメータ[＃7096](https://github.com/pingcap/tiflow/issues/7096) @ [ゾウビングウ](https://github.com/zoubingwu)を生成する問題を修正
        -   DM ワーカーが開始または停止するときに、一定の確率でデータ競合が発生する問題を修正[＃6401](https://github.com/pingcap/tiflow/issues/6401) @ [りゅうめんぎゃ](https://github.com/liumengya94)
        -   DM が`UPDATE`または`DELETE`ステートメントを複製しても対応する行データが存在しない場合、DM がイベント[＃6383](https://github.com/pingcap/tiflow/issues/6383) @ [GMHDBJD](https://github.com/GMHDBJD)を黙って無視する問題を修正しました。
        -   `query-status`コマンド[＃7189](https://github.com/pingcap/tiflow/issues/7189) @ [GMHDBJD](https://github.com/GMHDBJD)を実行した後に`secondsBehindMaster`フィールドが表示されない問題を修正しました
        -   チェックポイントを更新すると大規模なトランザクション[＃5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)がトリガーされる可能性がある問題を修正
        -   フルタスクモードで、タスクが同期ステージに入ってすぐに失敗すると、DM が上流のテーブルスキーマ情報[＃7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)を失う可能性がある問題を修正しました。
        -   整合性チェックが有効になっている場合にデッドロックが発生する可能性がある問題を修正[＃7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)
        -   タスクの事前チェックに`INFORMATION_SCHEMA`テーブル[＃7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要である問題を修正
        -   TLS 構成が空の場合にエラーが発生する問題を修正[＃7384](https://github.com/pingcap/tiflow/issues/7384) @ [りゅうめんぎゃ](https://github.com/liumengya94)

    -   TiDB Lightning

        -   `binary`エンコード形式[＃38351](https://github.com/pingcap/tidb/issues/38351) @ [ダシュン](https://github.com/dsdashun)の文字列型列を含むターゲット テーブルに Apache Parquet ファイルをインポートする際のインポート パフォーマンスの低下を修正しました。

    -   TiDBDumpling

        -   多数のテーブル[＃36549](https://github.com/pingcap/tidb/issues/36549) @ [ランス6716](https://github.com/lance6716)をエクスポートするときにDumpling がタイムアウトする可能性がある問題を修正しました
        -   一貫性ロックが有効になっているが、アップストリームにターゲット テーブル[＃38683](https://github.com/pingcap/tidb/issues/38683) @ [ランス6716](https://github.com/lance6716)がない場合に報告されるロック エラーを修正します。

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   [645775992](https://github.com/645775992)
-   [アンDJ](https://github.com/An-DJ)
-   [アンドリュー・ディ](https://github.com/AndrewDi)
-   [エルワドバ](https://github.com/erwadba)
-   [ふじぇ1989](https://github.com/fuzhe1989)
-   [ゴールドウィンド](https://github.com/goldwind-ting) (初めての投稿者)
-   [翻訳:](https://github.com/h3n4l)
-   [イグスリン](https://github.com/igxlin) (初めての投稿者)
-   [ihcsim](https://github.com/ihcsim)
-   [ジガオ・ルオ](https://github.com/JigaoLuo)
-   [モルゴ](https://github.com/morgo)
-   [ランキシー](https://github.com/Ranxy)
-   [神奇徳宝子](https://github.com/shenqidebaozi) (初めての投稿者)
-   [タオフェンリウ](https://github.com/taofengliu) (初めての投稿者)
-   [翻訳者](https://github.com/TszKitLo40)
-   [ウィックスブティ](https://github.com/wxbty) (初めての投稿者)
-   [翻訳](https://github.com/zgcbj)

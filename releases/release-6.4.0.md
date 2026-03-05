---
title: TiDB 6.4.0 Release Notes
summary: TiDB 6.4.0-DMRでは、クラスターを特定時点へのリストアのサポート、線形ハッシュパーティショニング構文との互換性、高性能な「AUTO_INCREMENT」モードなど、新機能と改善が導入されています。また、障害復旧、メモリ使用量の制御、統計情報収集も強化されています。TiFlashは保存時の暗号化にSM4アルゴリズムをサポートし、TiCDCはKafkaへのデータレプリケーションをサポートしています。このリリースには、さまざまなツールとコンポーネントのバグ修正と改善も含まれています。
---

# TiDB 6.4.0 リリースノート {#tidb-6-4-0-release-notes}

発売日：2022年11月17日

TiDB バージョン: 6.4.0-DMR

> **注記：**
>
> TiDB 6.4.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.4/)です。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.4/quick-start-with-tidb)

v6.4.0-DMR の主な新機能と改善点は次のとおりです。

-   [`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md) (実験的) を使用してクラスターを特定の時点に復元することをサポートします。
-   TiDB インスタンスの[グローバルメモリ使用量の追跡](/configure-memory-usage.md)サポートします (実験的)。
-   [線形ハッシュ分割構文](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)と互換性があること。
-   高性能かつグローバルに単調な[`AUTO_INCREMENT`](/auto-increment.md#mysql-compatibility-mode) (実験的) をサポートします。
-   [JSON型](/data-type-json.md)における配列データの範囲選択をサポートします。
-   ディスク障害や I/O のスタックなどの極端な状況での障害回復を高速化します。
-   テーブルの結合順序を決定するには[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)追加します。
-   相関サブクエリに対して非相関化を実行するかどうかを制御するには[新しいオプティマイザヒント`NO_DECORRELATE`](/optimizer-hints.md#no_decorrelate)導入します。
-   [クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能はGAになります。
-   TiFlash は[保存時の暗号化](/encryption-at-rest.md#tiflash)の SM4 アルゴリズムをサポートします。
-   [指定されたパーティションのTiFlashレプリカをテーブルにすぐに圧縮します](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)への SQL ステートメントの使用をサポートします。
-   サポート[EBSボリュームスナップショットを使用してTiDBクラスターをバックアップする](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot) 。
-   DMは[上流のデータソース情報を下流のマージされたテーブルの拡張列に書き込む](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)サポートします。

## 新機能 {#new-features}

### SQL {#sql}

-   SQL 文を使用して、テーブル内の指定されたパーティションのTiFlashレプリカを即時に圧縮する機能をサポート[＃5315](https://github.com/pingcap/tiflash/issues/5315) @ [ヘヘチェン](https://github.com/hehechen)

    TiDBはv6.2.0以降、 TiFlashのフルテーブルレプリカにおける[物理データを即座に圧縮する](/sql-statements/sql-statement-alter-table-compact.md#alter-table--compact)の機能をサポートしています。適切なタイミングでSQL文を手動で実行することで、 TiFlash内の物理データを即座に圧縮できるため、storage容量の削減とクエリパフォーマンスの向上につながります。v6.4.0では、圧縮対象となるTiFlashレプリカデータの粒度を改良し、テーブル内の特定のパーティションのTiFlashレプリカを即座に圧縮できるようになりました。

    SQL ステートメント`ALTER TABLE table_name COMPACT [PARTITION PartitionNameList] [engine_type REPLICA]`実行すると、テーブル内の指定されたパーティションのTiFlashレプリカをすぐに圧縮できます。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md#compact-tiflash-replicas-of-specified-partitions-in-a-table)参照してください。

-   `FLASHBACK CLUSTER TO TIMESTAMP` (実験的) [＃37197](https://github.com/pingcap/tidb/issues/37197) [＃13303](https://github.com/tikv/tikv/issues/13303) @ [定義2014](https://github.com/Defined2014) @ [bb7133](https://github.com/bb7133) @ [Jmポテト](https://github.com/JmPotato) @ [コナー1996](https://github.com/Connor1996) @ [HuSharp](https://github.com/HuSharp) @ [カルビンネオ](https://github.com/CalvinNeo)を使用して、クラスターを特定の時点に復元することをサポートします。

    `FLASHBACK CLUSTER TO TIMESTAMP`構文を使用すると、ガベージコレクション（GC）の有効期間内であれば、クラスターを特定の時点に迅速に復元できます。この機能は、DMLの誤った操作を簡単かつ迅速に元に戻すのに役立ちます。例えば、 `WHERE`句を指定せずに誤って`DELETE`実行してしまった場合でも、この構文を使用すれば数分で元のクラスターを復元できます。この機能はデータベースのバックアップに依存せず、異なる時点のデータのロールバックをサポートし、データが変更された正確な時刻を特定します。7 `FLASHBACK CLUSTER TO TIMESTAMP`データベースのバックアップを置き換えることはできませんのでご注意ください。

    `FLASHBACK CLUSTER TO TIMESTAMP`実行する前に、TiCDC などのツールで実行されている PITR およびレプリケーションタスクを一時停止し、 `FLASHBACK`完了後に再開する必要があります。そうしないと、レプリケーションタスクが失敗する可能性があります。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-flashback-cluster.md)参照してください。

-   `FLASHBACK DATABASE` [＃20463](https://github.com/pingcap/tidb/issues/20463) @ [エルワドバ](https://github.com/erwadba)を使用して削除されたデータベースの復元をサポートします

    `FLASHBACK DATABASE`使用すると、 `DROP`によって削除されたデータベースとそのデータを、ガベージコレクション（GC）の有効期間内に復元できます。この機能は外部ツールに依存しません。SQL文を使用して、データとメタデータを迅速に復元できます。

    詳細については[ユーザードキュメント](/sql-statements/sql-statement-flashback-database.md)参照してください。

### Security {#security}

-   TiFlashは保存時の暗号化にSM4アルゴリズムをサポートしています[＃5953](https://github.com/pingcap/tiflash/issues/5953) @ [リデジュ](https://github.com/lidezhu)

    TiFlash の保存時暗号化に SM4 アルゴリズムを追加します。保存時暗号化を設定する場合、設定ファイル`tiflash-learner.toml`の`data-encryption-method`設定の値を`sm4-ctr`に設定することで、SM4 暗号化機能を有効にできます。

    詳細については[ユーザードキュメント](/encryption-at-rest.md#tiflash)参照してください。

### 可観測性 {#observability}

-   クラスタ診断は GA [＃1438](https://github.com/pingcap/tidb-dashboard/issues/1438) @ [ホークソンジー](https://github.com/Hawkson-jee)になります

    TiDBダッシュボードの[クラスター診断](/dashboard/dashboard-diagnostics-access.md)機能は、指定された時間範囲内でクラスタに存在する可能性のある問題を診断し、診断結果とクラスタ関連の負荷監視情報を[診断レポート](/dashboard/dashboard-diagnostics-report.md)にまとめます。この診断レポートはウェブページ形式で提供されます。ブラウザからページを保存した後、オフラインでページを閲覧したり、このページのリンクを配布したりできます。

    診断レポートを使用すると、負荷、コンポーネントの状態、時間消費、構成など、クラスターの基本的な健全性情報を迅速に把握できます。クラスターに一般的な問題がある場合は、セクション[診断情報](/dashboard/dashboard-diagnostics-report.md#diagnostic-information)に組み込まれた自動診断の結果から原因を特定できます。

### パフォーマンス {#performance}

-   コプロセッサタスク[＃37724](https://github.com/pingcap/tidb/issues/37724) @ [あなた06](https://github.com/you06)同時実行適応メカニズムを導入する

    コプロセッサ タスクの数が増えると、TiKV の処理速度に基づいて、TiDB は自動的に同時実行性を高め ( [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)の値を調整)、コプロセッサ タスク キューを減らしてレイテンシーを減らします。

-   テーブル結合順序[＃37825](https://github.com/pingcap/tidb/issues/37825) @ [ウィノロス](https://github.com/winoros)を決定する動的計画アルゴリズムを追加します。

    以前のバージョンでは、TiDBはテーブルの結合順序を決定するために貪欲アルゴリズムを使用していました。v6.4.0では、TiDBオプティマイザーに[動的計画アルゴリズム](/join-reorder.md#example-the-dynamic-programming-algorithm-of-join-reorder)導入されました。動的計画アルゴリズムは貪欲アルゴリズムよりも多くの結合順序を列挙できるため、より適切な実行プランを見つける可能性が高まり、一部のシナリオではSQL実行効率が向上します。

    動的計画法アルゴリズムはより多くの時間を消費するため、TiDBの結合したテーブルの再配置アルゴリズムの選択は変数[`tidb_opt_join_reorder_threshold`](/system-variables.md#tidb_opt_join_reorder_threshold)によって制御されます。結合したテーブルの再配置に参加するノードの数がこのしきい値を超える場合、TiDBは貪欲アルゴリズムを使用します。それ以外の場合は、動的計画法アルゴリズムを使用します。

    詳細については[ユーザードキュメント](/join-reorder.md)参照してください。

-   プレフィックスインデックスは、null値のフィルタリングをサポートします[＃21145](https://github.com/pingcap/tidb/issues/21145) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    この機能はプレフィックスインデックスの最適化です。テーブル内の列にプレフィックスインデックスが設定されている場合、SQL文内の列の条件`IS NULL`または`IS NOT NULL`プレフィックスで直接フィルタリングできます。これにより、テーブル参照が回避され、SQL実行のパフォーマンスが向上します。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)参照してください。

-   TiDB チャンク再利用メカニズム[＃38606](https://github.com/pingcap/tidb/issues/38606) @ [キープラーニング20221](https://github.com/keeplearning20221)の強化

    以前のバージョンでは、TiDBはチャンクを`writechunk`関数内でのみ再利用していました。TiDB v6.4.0では、チャンク再利用メカニズムがExecutorの演算子にも拡張されています。チャンクを再利用することで、TiDBは頻繁にメモリ解放を要求する必要がなくなり、一部のシナリオではSQLクエリの実行効率が向上します。システム変数[`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)使用して、チャンクオブジェクトの再利用の有無を制御できます。これはデフォルトで有効になっています。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)参照してください。

-   相関サブクエリ[＃37789](https://github.com/pingcap/tidb/issues/37789) @ [時間と運命](https://github.com/time-and-fate)の相関解除を実行するかどうかを制御する新しいオプティマイザヒント`NO_DECORRELATE`を導入します。

    デフォルトでは、TiDB は常に相関サブクエリを書き換えてデコリレーションを実行しようとします。これにより、通常は実行効率が向上します。しかし、シナリオによっては、デコリレーションによって実行効率が低下する場合があります。v6.4.0 では、TiDB にオプティマイザーヒント`NO_DECORRELATE`が導入され、特定のクエリブロックに対してデコリレーションを実行しないようにオプティマイザーに指示することで、一部のシナリオにおけるクエリパフォーマンスが向上します。

    詳細については[ユーザードキュメント](/optimizer-hints.md#no_decorrelate)参照してください。

-   パーティションテーブル[＃37977](https://github.com/pingcap/tidb/issues/37977) @ [イーサール](https://github.com/Yisaer)での統計収集のパフォーマンスを向上

    v6.4.0では、TiDBはパーティションテーブルの統計収集戦略を最適化します。システム変数[`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)使用して、パーティションテーブルの統計収集の同時実行性を設定することで、収集速度を向上させ、分析時間を短縮できます。

### 安定性 {#stability}

-   ディスク障害やスタックI/O [＃13648](https://github.com/tikv/tikv/issues/13648) @ [LykxSassinator](https://github.com/LykxSassinator)などの極端な状況での障害回復を高速化します

    エンタープライズユーザーにとって、データベースの可用性は最も重要な指標の一つです。複雑なハードウェア環境において、いかに迅速に障害を検知し、復旧するかは、常にデータベースの可用性における課題の一つでした。v6.4.0では、TiDBはTiKVノードの状態検出メカニズムを完全に最適化しました。ディスク障害やI/Oスタックなどの極端な状況下でも、TiDBはノードの状態を迅速に報告し、アクティブウェイクアップメカニズムを用いて事前にLeader選出を開始することで、クラスターの自己修復を加速します。この最適化により、TiDBはディスク障害発生時のクラスター復旧時間を約50%短縮できます。

-   TiDBメモリ使用量のグローバル制御[＃37816](https://github.com/pingcap/tidb/issues/37816) @ [wshwsh12](https://github.com/wshwsh12)

    バージョン6.4.0では、TiDBインスタンスのグローバルメモリ使用量を追跡する実験的機能として、メモリメモリ量のグローバル制御が導入されました。システム変数[`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)使用して、グローバルメモリ使用量の上限を設定できます。メモリ使用量がしきい値に達すると、TiDBは空きメモリの回収と解放を試みます。メモリ使用量がしきい値を超えると、TiDBはメモリメモリ量によるシステムの問題を回避します。

    TiDBインスタンスのメモリ消費に潜在的なリスクがある場合、TiDBは事前に診断情報を収集し、指定されたディレクトリに書き込むことで、問題の診断を容易にします。同時に、メモリ使用量と操作履歴を表示するシステムテーブルビュー[`INFORMATION_SCHEMA.MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)と[`INFORMATION_SCHEMA.MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)提供し、メモリ使用量の理解を深めるのに役立ちます。

    グローバルメモリ制御は、TiDBのメモリ管理における画期的な技術です。インスタンスのグローバルビューを導入し、メモリを体系的に管理することで、より多くの重要なシナリオにおいてデータベースの安定性とサービスの可用性を大幅に向上させることができます。

    詳細については[ユーザードキュメント](/configure-memory-usage.md)参照してください。

-   範囲構築オプティマイザ[＃37176](https://github.com/pingcap/tidb/issues/37176) @ [xuyifangreeneyes](https://github.com/xuyifangreeneyes)のメモリ使用量を制御する

    バージョン6.4.0では、範囲を構築するオプティマイザの最大メモリ使用量を制限するシステム変数[`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)が導入されました。メモリ使用量が制限を超えると、オプティマイザはより正確な範囲ではなく、より粗い範囲を構築することでメモリ消費量を削減します。SQL文に`IN`の条件が多数含まれる場合、この最適化によりコンパイル時のメモリ使用量を大幅に削減し、システムの安定性を確保できます。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_opt_range_max_size-new-in-v640)参照してください。

-   統計情報の同期読み込みをサポート (GA) [＃37434](https://github.com/pingcap/tidb/issues/37434) @ [クリサン](https://github.com/chrysan)

    TiDB v6.4.0では、統計情報の同期ロード機能がデフォルトで有効になっています。この機能により、SQL文の実行時に、TiDBは大規模な統計情報（ヒストグラム、TopN、Count-Min Sketch統計情報など）をメモリに同期的にロードできるようになり、SQL最適化における統計情報の完全性が向上します。

    詳細については[ユーザードキュメント](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)参照してください。

-   軽量トランザクション書き込みの応答時間に対するバッチ書き込み要求の影響を軽減[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

    一部のシステムのビジネスロジックでは、定期的なバッチDMLタスクが必要ですが、これらのバッチ書き込みタスクの処理はオンライントランザクションのレイテンシーを増加させます。v6.3.0では、TiKVがハイブリッドワークロードシナリオにおける読み取り要求のスケジューリングを最適化するため、 [`readpool.unified.auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)構成項目を有効にすると、TiKVがすべての読み取り要求に対してUnifyReadPoolスレッドプールのサイズを自動的に調整できるようになります。v6.4.0では、TiKVは書き込み要求を動的に識別して優先順位付けするだけでなく、1回のポーリングで1つのFSM（有限状態マシン）に適用スレッドが書き込める最大バイト数を制御することができるため、バッチ書き込み要求がトランザクション書き込みの応答時間に与える影響を軽減できます。

### 使いやすさ {#ease-of-use}

-   TiKV API V2 が一般公開 (GA) される[＃11745](https://github.com/tikv/tikv/issues/11745) @ [ピンギュ](https://github.com/pingyu)

    v6.1.0より前のTiKVは、クライアントから渡された生データのみを保存するため、基本的なキー値の読み取りと書き込み機能しか提供していませんでした。さらに、コーディング方法の違いとスコープ外のデータ範囲のため、TiDB、Transactional KV、RawKVを同じTiKVクラスター内で同時に使用することはできません。同時に使用するには複数のクラスターが必要となり、マシンコストと導入コストが増加します。

    TiKV API V2 は、新しい RawKVstorage形式とアクセス インターフェイスを提供し、次のような利点をもたらします。

    -   MVCCに記録されたデータの変更タイムスタンプとともにデータを保存し、これに基づいて変更データキャプチャ（CDC）を実装します。この機能は実験的であり、詳細は[TiKV-CDC](https://github.com/tikv/migration/blob/main/cdc/README.md)に記載されています。
    -   データはさまざまな使用方法に応じてスコープが設定され、API V2 は単一クラスター内での TiDB、トランザクション KV、および RawKV アプリケーションの共存をサポートします。
    -   マルチテナントなどの機能をサポートするために、キー スペース フィールドを予約します。

    TiKV API V2 を有効にするには、TiKV 構成ファイルの`[storage]`セクションで`api-version = 2`設定します。

    詳細については[ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610)参照してください。

-   TiFlashデータ複製の進行状況[＃4902](https://github.com/pingcap/tiflash/issues/4902) @ [ヘヘチェン](https://github.com/hehechen)精度を向上

    TiDBでは、 `INFORMATION_SCHEMA.TIFLASH_REPLICA`テーブルの`PROGRESS`フィールドは、TiKV内の対応するテーブルからTiFlashレプリカへのデータレプリケーションの進行状況を示すために使用されます。以前のTiDBバージョンでは、 `PROCESS`フィールドはTiFlashレプリカの作成中のデータレプリケーションの進行状況のみを示します。TiFlashTiFlashの作成後、TiKV内の対応するテーブルに新しいデータがインポートされても、このフィールドは更新されず、新しいデータのTiKVからTiFlashへのレプリケーションの進行状況は表示されません。

    v6.4.0では、TiDBはTiFlashレプリカのデータレプリケーションの進行状況の更新メカニズムを改善しました。TiFlashTiFlashの作成後、TiKVの対応するテーブルに新しいデータがインポートされると、テーブル[`INFORMATION_SCHEMA.TIFLASH_REPLICA`](/information-schema/information-schema-tiflash-replica.md)の`PROGRESS`の値が更新され、新しいデータのTiKVからTiFlashへの実際のレプリケーション進行状況が表示されます。この改善により、 TiFlashデータレプリケーションの実際の進行状況を簡単に確認できます。

    詳細については[ユーザードキュメント](/information-schema/information-schema-tiflash-replica.md)参照してください。

### MySQLの互換性 {#mysql-compatibility}

-   線形ハッシュパーティション構文[＃38450](https://github.com/pingcap/tidb/issues/38450) @ [ミョンス](https://github.com/mjonss)と互換性がある

    以前のバージョンでは、TiDBはハッシュ、レンジ、List パーティショニングをサポートしていました。v6.4.0以降、TiDBは[MySQL 線形ハッシュパーティショニング](https://dev.mysql.com/doc/refman/5.7/en/partitioning-linear-hash.html)の構文にも対応しています。

    TiDBでは、MySQLリニアハッシュパーティションの既存のDDL文を直接実行できます。TiDBは対応するハッシュパーティションテーブルを作成します（TiDB内にはリニアハッシュパーティションは存在しないことに注意してください）。また、MySQLリニアハッシュパーティションの既存のDML文を直接実行することもできます。TiDBは対応するTiDBハッシュパーティションのクエリ結果を通常通り返します。この機能により、TiDBの構文とMySQLリニアハッシュパーティションの互換性が確保され、MySQLベースのアプリケーションからTiDBへのシームレスな移行が容易になります。

    パーティション数が2の累乗の場合、TiDBハッシュパーティションテーブルの行はMySQLリニアハッシュパーティションテーブルと同じように分散されます。それ以外の場合、TiDBにおける行の分散はMySQLとは異なります。

    詳細については[ユーザードキュメント](/partitioned-table.md#how-tidb-handles-linear-hash-partitions)参照してください。

-   高性能かつ全体的に単調な`AUTO_INCREMENT` (実験的) [＃38442](https://github.com/pingcap/tidb/issues/38442) @ [天菜まお](https://github.com/tiancaiamao)をサポート

    TiDB v6.4.0 では、MySQL 互換モード`AUTO_INCREMENT`が導入されました。このモードでは、すべての TiDB インスタンスで ID が単調に増加するようにする、集中型の自動インクリメント ID 割り当てサービスが導入されます。この機能により、自動インクリメント ID によるクエリ結果の並べ替えが容易になります。MySQL 互換モードを使用するには、テーブル作成時に`AUTO_ID_CACHE`から`1`設定する必要があります。以下は例です。

    ```sql
    CREATE TABLE t (a INT AUTO_INCREMENT PRIMARY KEY) AUTO_ID_CACHE = 1;
    ```

    詳細については[ユーザードキュメント](/auto-increment.md#mysql-compatibility-mode)参照してください。

-   JSON型[＃13644](https://github.com/tikv/tikv/issues/13644) @ [ヤンケオ](https://github.com/YangKeao)の配列データの範囲選択をサポート

    v6.4.0 以降では、TiDB で MySQL 互換[範囲選択構文](https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths)使用できるようになります。

    -   キーワード`to`使用すると、配列要素の開始位置と終了位置を指定し、配列内の連続した範囲の要素を選択できます。 `0`使用すると、配列の最初の要素の位置を指定できます。例えば、 `$[0 to 2]`使用すると、配列の最初の3つの要素を選択できます。

    -   キーワード`last`を使用すると、配列の最後の要素の位置を指定できます。これにより、右から左への位置を指定できます。例えば、 `$[last-2 to last]`使用すると、配列の最後の3つの要素を選択できます。

    この機能により、SQL ステートメントの記述プロセスが簡素化され、JSON 型の互換性がさらに向上し、MySQL アプリケーションを TiDB に移行する際の難易度が軽減されます。

-   データベースユーザー[＃38172](https://github.com/pingcap/tidb/issues/38172) @ [CbcWestwolf](https://github.com/CbcWestwolf)の追加説明の追加をサポート

    TiDB v6.4では、 [`CREATE USER`](/sql-statements/sql-statement-create-user.md)または[`ALTER USER`](/sql-statements/sql-statement-alter-user.md)使用してデータベースユーザー向けの説明を追加できます。TiDBは2つの説明形式を提供しています。5 `COMMENT`使用してテキストコメントを追加し、 `ATTRIBUTE`を使用してJSON形式の構造化属性セットを追加できます。

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

    この機能により、TiDB と MySQL 構文の互換性が向上し、TiDB を MySQL エコシステムのツールやプラットフォームに統合しやすくなります。

### バックアップと復元 {#backup-and-restore}

-   EBSボリュームスナップショット[＃33849](https://github.com/pingcap/tidb/issues/33849) @ [フェンゴウ1](https://github.com/fengou1)を使用したTiDBクラスターのバックアップをサポート

    TiDB クラスターが EKS にデプロイされ、AWS EBS ボリュームを使用しており、TiDB クラスター データをバックアップする際に次の要件がある場合は、 TiDB Operatorを使用してボリューム スナップショットとメタデータごとにデータを AWS S3 にバックアップできます。

    -   バックアップの影響を最小限に抑えます。たとえば、QPS とトランザクションのレイテンシーへの影響を 5% 未満に保ち、クラスターの CPU とメモリを占有しないようにします。
    -   短時間でデータのバックアップとリストアを行います。例えば、1時間以内にバックアップを完了し、2時間以内にデータをリストアします。

    詳細については[ユーザードキュメント](https://docs.pingcap.com/tidb-in-kubernetes/v1.4/backup-to-aws-s3-by-snapshot)参照してください。

### データ移行 {#data-migration}

-   DMは、上流のデータソース情報を下流のマージされたテーブル[＃37797](https://github.com/pingcap/tidb/issues/37797) @ [リチュンジュ](https://github.com/lichunzhu)の拡張列に書き込むことをサポートします。

    上流からTiDBにシャード化されたスキーマとテーブルをマージする際、ターゲットテーブルに複数のフィールド（拡張列）を手動で追加し、DMタスクの設定時にそれらの値を指定できます。例えば、拡張列に上流のシャード化されたスキーマとテーブルの名前を指定すると、DMによって下流に書き込まれるデータにはスキーマ名とテーブル名が含まれます。下流のデータが通常とは異なる場合、この機能を使用することで、ターゲットテーブル内のスキーマ名やテーブル名などのデータソース情報を素早く見つけることができます。

    詳細については[テーブル、スキーマ、ソース情報を抽出し、結合されたテーブルに書き込みます](/dm/dm-table-routing.md#extract-table-schema-and-source-information-and-write-into-the-merged-table)参照してください。

-   DMは、いくつかの必須チェック項目をオプションの項目に変更することで、事前チェックのメカニズムを最適化します[＃7333](https://github.com/pingcap/tiflow/issues/7333) @ [リチュンジュ](https://github.com/lichunzhu)

    データ移行タスクをスムーズに実行するために、DM はタスクの開始時に[事前チェック](/dm/dm-precheck.md)自動的にトリガーし、チェック結果を返します。DM は事前チェックに合格した後にのみ移行を開始します。

    v6.4.0 では、DM は次の 3 つのチェック項目を必須からオプションに変更し、事前チェックの合格率を向上させました。

    -   アップストリーム テーブルが TiDB と互換性のない文字セットを使用しているかどうかを確認します。
    -   上流のテーブルに主キー制約または一意キー制約があるかどうかを確認します
    -   プライマリ/セカンダリ構成で、アップストリーム データベースのデータベース ID `server_id`が指定されているかどうかを確認します。

-   DM は、増分移行タスク[＃7393](https://github.com/pingcap/tiflow/issues/7393) @ [GMHDBJD](https://github.com/GMHDBJD)オプション パラメータとして、binlogの位置と GTID を構成することをサポートしています。

    v6.4.0以降、binlogの位置やGTIDを指定せずに、直接増分マイグレーションを実行できるようになりました。DMは、タスク開始後に生成されたbinlogファイルを上流から自動的に取得し、これらの増分データを下流に移行します。これにより、ユーザーは煩雑な設定や理解の手間から解放されます。

    詳細については[DM 高度なタスクコンフィグレーションファイル](/dm/task-configuration-file-full.md)参照してください。

-   DM は移行タスク[＃7343](https://github.com/pingcap/tiflow/issues/7343) @ [okJiang](https://github.com/okJiang)ステータス インジケーターを追加します

    バージョン 6.4.0 では、DM により移行タスクのパフォーマンスと進行状況のインジケーターがさらに追加され、移行のパフォーマンスと進行状況をより直感的に理解できるようになり、トラブルシューティングの参照としても役立ちます。

    -   データのインポートおよびエクスポートのパフォーマンスを示すステータス インジケーター (バイト/秒単位) を追加します。
    -   ダウンストリーム データベースにデータを書き込むためのパフォーマンス インジケーターの名前を TPS から RPS (行数/秒) に変更します。
    -   DM 完全移行タスクのデータ エクスポートの進行状況を示す進行状況インジケーターを追加します。

    これらの指標の詳細については、 [TiDB データ移行におけるクエリタスクステータス](/dm/dm-query-status.md)参照してください。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDCは[＃7191](https://github.com/pingcap/tiflow/issues/7191) `3.2.0`のデータレプリケーションを[3エースショーハンド](https://github.com/3AceShowHand)サポートしています。

    v6.4.0 以降、TiCDC は`3.2.0`バージョンのうち[Kafkaへのデータの複製](/replicate-data-to-kafka.md)それ以前のバージョンをサポートします。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                 | タイプを変更   | 説明                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`max_execution_time`](/system-variables.md#max_execution_time)                                                                     | 修正済み     | バージョン6.4.0より前では、この変数はすべてのタイプのステートメントに適用されます。バージョン6.4.0以降では、この変数は読み取り専用ステートメントの最大実行時間のみを制御します。                                                                                                                                         |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)         | 修正済み     | GLOBALスコープを削除し、 [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)設定項目を使用してデフォルト値を変更できるようにします。この変数は、TiDBが悲観的トランザクションにおいて一意制約をチェックするタイミングを制御します。 |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                 | 修正済み     | バージョン6.4.0以降で有効になり、同時実行数を[`FLASHBACK CLUSTER TO TIMESTAMP`](/sql-statements/sql-statement-flashback-cluster.md)に制御します。デフォルト値は`64`です。                                                                                                  |
| [`tidb_enable_clustered_index`](/system-variables.md#tidb_enable_clustered_index-new-in-v50)                                        | 修正済み     | デフォルト値を`INT_ONLY`から`ON`に変更します。これは、主キーがデフォルトでクラスター化インデックスとして作成されることを意味します。                                                                                                                                                             |
| [`tidb_enable_paging`](/system-variables.md#tidb_enable_paging-new-in-v540)                                                         | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、コプロセッサ要求を送信するためのページング方式がデフォルトで使用されることを意味します。                                                                                                                                                             |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                               | 修正済み     | SESSIONスコープを追加します。この変数は[プリペアドプランキャッシュ](/sql-prepared-plan-cache.md)有効にするかどうかを制御します。                                                                                                                                                   |
| [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)                                               | 修正済み     | デフォルト値を`0.8`から`0.7`に変更します。この変数は、tidb-server のメモリアラームをトリガーするメモリ使用率を制御します。                                                                                                                                                              |
| [`tidb_opt_agg_push_down`](/system-variables.md#tidb_opt_agg_push_down)                                                             | 修正済み     | GLOBALスコープを追加します。この変数は、オプティマイザーが集計関数をJoin、Projection、UnionAllの前の位置までプッシュダウンする最適化操作を実行するかどうかを制御します。                                                                                                                                    |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                                   | 修正済み     | SESSIONスコープを追加します。この変数は、セッションでキャッシュできるプランの最大数を制御します。                                                                                                                                                                                  |
| [`tidb_stats_load_sync_wait`](/system-variables.md#tidb_stats_load_sync_wait-new-in-v540)                                           | 修正済み     | デフォルト値を`0`から`100`に変更します。これは、SQL 実行が完全な列統計を同期的にロードするために、デフォルトで最大 100 ミリ秒待機できることを意味します。                                                                                                                                                 |
| [`tidb_stats_load_pseudo_timeout`](/system-variables.md#tidb_stats_load_pseudo_timeout-new-in-v540)                                 | 修正済み     | デフォルト値を`OFF`から`ON`に変更します。これは、完全な列統計を同期的にロードするタイムアウトに達した後、SQL 最適化が疑似統計の使用に戻ることを意味します。                                                                                                                                                  |
| [`last_sql_use_alloc`](/system-variables.md#last_sql_use_alloc-new-in-v640)                                                         | 新しく追加された | 前の文がキャッシュされたチャンクオブジェクト（チャンク割り当て）を使用したかどうかを示します。この変数は読み取り専用で、デフォルト値は`OFF`です。                                                                                                                                                           |
| [`tidb_auto_analyze_partition_batch_size`](/system-variables.md#tidb_auto_analyze_partition_batch_size-new-in-v640)                 | 新しく追加された | パーティションテーブルを分析する際にTiDBが[自動的に分析する](/statistics.md#automatic-update)に処理できるパーティションの数を指定します（つまり、パーティションテーブルの統計情報を自動的に収集します）。デフォルト値は`1`です。                                                                                                 |
| [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)                                     | 新しく追加された | TiDBが[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)で指定されたタイムスタンプでデータを読み取るかどうかを制御します。デフォルト値は`OFF`です。                                                                                                          |
| [`tidb_enable_gogc_tuner`](/system-variables.md#tidb_enable_gogc_tuner-new-in-v640)                                                 | 新しく追加された | GOGCチューナーを有効にするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                                                              |
| [`tidb_enable_reuse_chunk`](/system-variables.md#tidb_enable_reuse_chunk-new-in-v640)                                               | 新しく追加された | TiDBがチャンクオブジェクトのキャッシュを有効にするかどうかを制御します。デフォルト値は`ON`で、これはTiDBがキャッシュされたチャンクオブジェクトを優先的に使用し、要求されたオブジェクトがキャッシュ内に存在しない場合にのみシステムから要求することを意味します。値が`OFF`場合、TiDBはシステムから直接チャンクオブジェクトを要求します。                                                        |
| [`tidb_enable_prepared_plan_cache_memory_monitor`](/system-variables.md#tidb_enable_prepared_plan_cache_memory_monitor-new-in-v640) | 新しく追加された | プリペアドプランキャッシュにキャッシュされた実行プランによって消費されるメモリをカウントするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                                                               |
| [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)                                                             | 新しく追加された | デフォルト値は`0`です。3 `ON` [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)設定すると、TiDB はこの変数で指定されたタイムスタンプでデータを読み取ります。                                                                          |
| [`tidb_gogc_tuner_threshold`](/system-variables.md#tidb_gogc_tuner_threshold-new-in-v640)                                           | 新しく追加された | GOGCチューニングの最大メモリしきい値を指定します。メモリがこのしきい値を超えると、GOGC Tunerは動作を停止します。デフォルト値は`0.6`です。                                                                                                                                                        |
| [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-new-in-v640)               | 新しく追加された | tidb-server のメモリ使用量がメモリアラームしきい値を超えてアラームがトリガーされると、TiDB はデフォルトで直近 5 件のアラーム中に生成されたステータスファイルのみを保持します。この変数でこの数を調整できます。                                                                                                                     |
| [`tidb_opt_prefix_index_single_scan`](/system-variables.md#tidb_opt_prefix_index_single_scan-new-in-v640)                           | 新しく追加された | TiDBオプティマイザが、不要なテーブル検索を回避し、クエリパフォーマンスを向上させるために、一部のフィルタ条件をプレフィックスインデックスにプッシュダウンするかどうかを制御します。デフォルト値は`ON`です。                                                                                                                             |
| [`tidb_opt_range_max_size`](/system-variables.md#tidb_opt_range_max_size-new-in-v640)                                               | 新しく追加された | オプティマイザがスキャン範囲を構築する際に使用するメモリの上限を指定します。デフォルト値は`67108864` （64MiB）です。                                                                                                                                                                    |
| [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640)                                             | 新しく追加された | スキャン範囲を構築するためのオプティマイザのメモリ使用量の上限を制御します（実験的）。デフォルト値は`0`で、メモリ制限がないことを意味します。                                                                                                                                                              |
| [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640)                       | 新しく追加された | TiDBがGCをトリガーしようとするしきい値を制御します（実験的）。デフォルト値は`70%`です。                                                                                                                                                                                     |
| [`tidb_server_memory_limit_sess_min_size`](/system-variables.md#tidb_server_memory_limit_sess_min_size-new-in-v640)                 | 新しく追加された | メモリ制限を有効にすると、TiDBは現在のインスタンスで最もメモリ使用量が多いSQL文を終了します。この変数は、終了するSQL文の最小メモリ使用量を指定します。デフォルト値は`134217728` （128MiB）です。                                                                                                                        |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーションパラメータ                                                                                                                           | タイプを変更   | 説明                                                                                                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `tidb_memory_usage_alarm_ratio`                                                                                                           | 削除済み     | この構成項目は無効になりました。                                                                                                                                                        |
| TiDB           | `memory-usage-alarm-ratio`                                                                                                                | 削除済み     | システム変数[`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)に置き換えられます。この構成項目が TiDB バージョン v6.4.0 より前のバージョンで構成されている場合には、アップグレード後に有効になりません。 |
| TiDB           | [`pessimistic-txn.constraint-check-in-place-pessimistic`](/tidb-configuration-file.md#constraint-check-in-place-pessimistic-new-in-v640)  | 新しく追加された | システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)のデフォルト値を制御します。デフォルト値は`true`です。         |
| TiDB           | [`tidb-max-reuse-chunk`](/tidb-configuration-file.md#tidb-max-reuse-chunk-new-in-v640)                                                    | 新しく追加された | チャンク割り当てにおけるキャッシュされたチャンクオブジェクトの最大数を制御します。デフォルト値は`64`です。                                                                                                                 |
| TiDB           | [`tidb-max-reuse-column`](/tidb-configuration-file.md#tidb-max-reuse-column-new-in-v640)                                                  | 新しく追加された | チャンク割り当てのキャッシュ列オブジェクトの最大数を制御します。デフォルト値は`256`です。                                                                                                                         |
| TiKV           | [`cdc.raw-min-ts-outlier-threshold`](https://docs.pingcap.com/tidb/v6.2/tikv-configuration-file#raw-min-ts-outlier-threshold-new-in-v620) | 非推奨      | この構成項目は無効になりました。                                                                                                                                                        |
| TiKV           | [`causal-ts.alloc-ahead-buffer`](/tikv-configuration-file.md#alloc-ahead-buffer-new-in-v640)                                              | 新しく追加された | 事前に割り当てられたTSOキャッシュサイズ（期間）。デフォルト値は`3s`です。                                                                                                                                |
| TiKV           | [`causal-ts.renew-batch-max-size`](/tikv-configuration-file.md#renew-batch-max-size-new-in-v640)                                          | 新しく追加された | タイムスタンプリクエストにおけるTSOの最大数を制御します。デフォルト値は`8192`です。                                                                                                                          |
| TiKV           | [`raftstore.apply-yield-write-size`](/tikv-configuration-file.md#apply-yield-write-size-new-in-v640)                                      | 新しく追加された | Applyスレッドが1回のポーリングで1つのFSM（有限状態機械）に書き込める最大バイト数を制御します。デフォルト値は`32KiB`です。これはソフトリミットです。                                                                                      |
| PD             | [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval)                                                  | 新しく追加された | バージョン6.4.0以降で有効になり、PDがTSOの物理時間を更新する間隔を制御します。デフォルト値は`50ms`です。                                                                                                            |
| TiFlash        | [`data-encryption-method`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)                                      | 修正済み     | 新しい値オプション`sm4-ctr`が導入されました。この設定項目を`sm4-ctr`に設定すると、データは保存前に SM4 を使用して暗号化されます。                                                                                            |
| DM             | [`routes.route-rule-1.extract-table`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                      | 新しく追加された | オプション。シャーディングシナリオにおいて、シャーディングされたテーブルのソース情報を抽出するために使用します。抽出された情報は、データソースを識別するために、下流のマージされたテーブルに書き込まれます。このパラメータを設定する場合は、事前に下流にマージされたテーブルを手動で作成する必要があります。                  |
| DM             | [`routes.route-rule-1.extract-schema`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディングシナリオにおいて、シャーディングされたスキーマのソース情報を抽出するために使用します。抽出された情報は、データソースを識別するために、下流のマージされたテーブルに書き込まれます。このパラメータを設定する場合は、事前に下流にマージされたテーブルを手動で作成する必要があります。                  |
| DM             | [`routes.route-rule-1.extract-source`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced)                     | 新しく追加された | オプション。シャーディングシナリオにおいて、ソースインスタンスの情報を抽出するために使用されます。抽出された情報は、データソースを識別するために、下流のマージテーブルに書き込まれます。このパラメータを設定する場合は、事前に下流にマージテーブルを手動で作成する必要があります。                               |
| TiCDC          | [`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)                                             | 修正済み     | デフォルト値を`table`から`none`に変更します。この変更により、レプリケーションのレイテンシーとOOMリスクが軽減されます。さらに、TiCDCはすべてのトランザクションではなく、一部のトランザクション（単一トランザクションのサイズが1024行を超える）のみを分割するようになりました。                     |

### その他 {#others}

-   v6.4.0以降、 `mysql.user`テーブルに`User_attributes`と`Token_issuer` 2つの新しい列が追加されます。以前のTiDBバージョン`mysql`バックアップデータからTiDB v6.4.0に[`mysql`スキーマ内のシステムテーブルを復元する](/br/br-snapshot-guide.md#restore-tables-in-the-mysql-schema)復元すると、 BRは`mysql.user`テーブルに対して`column count mismatch`エラーを報告します。13スキーマでシステムテーブルを復元しない場合、このエラーは報告されません。
-   名前が[Dumplingエクスポートファイルの形式](/dumpling-overview.md#format-of-exported-files)一致するものの、末尾が非圧縮形式（ `test-schema-create.sql.origin`や`test.table-schema.sql.origin`など）であるファイルについては、 TiDB Lightningによる処理方法が変更されました。v6.4.0 より前では、インポートするファイルにこれらのファイルが含まれている場合、 TiDB Lightning はそれらのファイルのインポートをスキップしていました。v6.4.0 以降では、 TiDB Lightning はこれらのファイルがサポートされていない圧縮形式を使用していると想定し、インポートタスクは失敗します。
-   v6.4.0 以降では、権限`SYSTEM_VARIABLES_ADMIN`または`SUPER`持つ changefeed のみが TiCDC Syncpoint 機能を使用できます。

## 改善点 {#improvements}

-   TiDB

    -   noop変数`lc_messages` [＃38231](https://github.com/pingcap/tidb/issues/38231) @ [djshow832](https://github.com/djshow832)変更を許可する
    -   `AUTO_RANDOM`列目をクラスター化複合インデックス[＃38572](https://github.com/pingcap/tidb/issues/38572) @ [接線](https://github.com/tangenta)の最初の列としてサポートします
    -   内部トランザクションの再試行で悲観的トランザクションを使用して再試行の失敗を回避し、時間の消費を削減します[＃38136](https://github.com/pingcap/tidb/issues/38136) @ [ジャッキーsp](https://github.com/jackysp)

-   TiKV

    -   新しい構成項目`apply-yield-write-size`追加して、Apply スレッドが 1 回のポーリングで 1 つの有限状態マシンに書き込むことができる最大バイト数を制御し、Apply スレッドが大量のデータ[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)を書き込むときにRaftstore の輻輳を緩和します。
    -   リーダー移行プロセス中のQPSジッターを回避するために、リージョンのリーダーを移行する前にエントリキャッシュをウォームアップします[＃13060](https://github.com/tikv/tikv/issues/13060) @ [コスベン](https://github.com/cosven)
    -   `json_constrains`演算子をコプロセッサー[＃13592](https://github.com/tikv/tikv/issues/13592) @ [立振環](https://github.com/lizhenhuan)にプッシュダウンする機能をサポート
    -   いくつかのシナリオでフラッシュパフォーマンスを向上させるために、 `CausalTsProvider`に非同期関数を追加します[＃13428](https://github.com/tikv/tikv/issues/13428) @ [沢民州](https://github.com/zeminzhou)

-   PD

    -   ホットリージョンスケジューラのv2アルゴリズムがGAになりました。一部のシナリオでは、v2アルゴリズムは両方の構成ディメンションでより適切なバランスを実現し、無効なスケジューリング[＃5021](https://github.com/tikv/pd/issues/5021) @ [フンドゥンDM](https://github.com/hundundm)を削減できます。
    -   オペレータステップのタイムアウトメカニズムを最適化して、早期のタイムアウト[＃5596](https://github.com/tikv/pd/issues/5596) @ [バッファフライ](https://github.com/bufferflies)を回避する
    -   大規模クラスタのスケジューラのパフォーマンスを向上[＃5473](https://github.com/tikv/pd/issues/5473) @ [バッファフライ](https://github.com/bufferflies)
    -   PD [＃5637](https://github.com/tikv/pd/issues/5637) @ [lhy1024](https://github.com/lhy1024)では提供されない外部タイムスタンプの使用をサポートします

-   TiFlash

    -   TiFlash MPPエラー処理ロジックをリファクタリングして、MPP [＃5095](https://github.com/pingcap/tiflash/issues/5095) @ [ウィンドトーカー](https://github.com/windtalker)の安定性をさらに向上します。
    -   TiFlash計算プロセスのソートを最適化し、結合と集計[＃5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロツグ](https://github.com/solotzg)キー処理を最適化します。
    -   デコード時のメモリ使用量を最適化し、冗長な転送列を削除して結合パフォーマンスを向上させる[＃6157](https://github.com/pingcap/tiflash/issues/6157) @ [イービン87](https://github.com/yibin87)

-   ツール

    -   TiDBダッシュボード

        -   監視ページでのTiFlashメトリックの表示をサポートし、そのページ[＃1440](https://github.com/pingcap/tidb-dashboard/issues/1440) @ [イニシュ9506](https://github.com/YiniXu9506)でのメトリックの表示を最適化します。
        -   スロークエリリストとSQLステートメントリストに結果の行数を表示します[＃1443](https://github.com/pingcap/tidb-dashboard/issues/1443) @ [バウリン](https://github.com/baurine)
        -   Alertmanager が存在しない場合に Alertmanager エラーを報告しないようにダッシュボードを最適化します[＃1444](https://github.com/pingcap/tidb-dashboard/issues/1444) @ [バウリン](https://github.com/baurine)

    -   バックアップと復元 (BR)

        -   メタデータのロードメカニズムを改善しました。メタデータは必要な場合にのみメモリにロードされるため、PITR [＃38404](https://github.com/pingcap/tidb/issues/38404) @ [ユジュンセン](https://github.com/YuJuncen)のメモリ使用量が大幅に削減されます。

    -   TiCDC

        -   交換パーティションDDLステートメント[＃639](https://github.com/pingcap/tiflow/issues/639) @ [アズドンメン](https://github.com/asddongmen)の複製をサポート
        -   MQシンクモジュール[＃7353](https://github.com/pingcap/tiflow/issues/7353) @ [ハイラスティン](https://github.com/Rustin170506)の非バッチ送信パフォーマンスを向上
        -   テーブルに多数のリージョン[＃7078](https://github.com/pingcap/tiflow/issues/7078) [＃7281](https://github.com/pingcap/tiflow/issues/7281) @ [スドジ](https://github.com/sdojjy)がある場合の TiCDC プラーのパフォーマンスを向上
        -   同期ポイントが有効な場合、 `tidb_enable_external_ts_read`変数を使用して下流 TiDB の履歴データの読み取りをサポートします[＃7419](https://github.com/pingcap/tiflow/issues/7419) @ [アズドンメン](https://github.com/asddongmen)
        -   レプリケーションの安定性を向上させるために、トランザクション分割を有効にし、セーフモードをデフォルトで無効にします[＃7505](https://github.com/pingcap/tiflow/issues/7505) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   dmctl [＃7246](https://github.com/pingcap/tiflow/issues/7246) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)から不要なコマンド`operate-source update`を削除します
        -   上流データベースがTiDBと互換性のないDDL文を使用している場合、DMの完全インポートが失敗する問題を修正しました。TiDBでサポートされているDDL文を使用して、事前にTiDBでターゲットテーブルのスキーマを手動で作成しておくことで、インポートを確実に成功させることができます[＃37984](https://github.com/pingcap/tidb/issues/37984) @ [ランス6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   ファイルスキャンロジックを最適化して、スキーマファイル[＃38598](https://github.com/pingcap/tidb/issues/38598) @ [dsdashun](https://github.com/dsdashun)のスキャンを高速化します。

## バグ修正 {#bug-fixes}

-   TiDB

    -   新しいインデックス[＃38165](https://github.com/pingcap/tidb/issues/38165) @ [接線](https://github.com/tangenta)を作成した後に発生する可能性のあるインデックスの不整合の問題を修正しました
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`テーブル[＃38407](https://github.com/pingcap/tidb/issues/38407) @ [CbcWestwolf](https://github.com/CbcWestwolf)の権限の問題を修正
    -   `mysql.tables_priv`テーブル[＃38293](https://github.com/pingcap/tidb/issues/38293) @ [CbcWestwolf](https://github.com/CbcWestwolf)で`grantor`フィールドが欠落している問題を修正しました
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃38170](https://github.com/pingcap/tidb/issues/38170) @ [wjhuang2016](https://github.com/wjhuang2016)
    -   共通テーブル式の結合結果が間違っている可能性がある問題を修正[＃37928](https://github.com/pingcap/tidb/issues/37928) @ [ヤンケオ](https://github.com/YangKeao)
    -   **トランザクションリージョン番号**監視パネルの情報が正しくない問題を修正[＃38139](https://github.com/pingcap/tidb/issues/38139) @ [ジャッキーsp](https://github.com/jackysp)
    -   システム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)内部トランザクションに影響を与える可能性がある問題を修正しました。変数のスコープはSESSIONに変更されました[＃38766](https://github.com/pingcap/tidb/issues/38766) @ [エキシウム](https://github.com/ekexium)
    -   クエリ内の条件が誤って投影[＃35623](https://github.com/pingcap/tidb/issues/35623) @ [思い出させる](https://github.com/Reminiscent)にプッシュダウンされる問題を修正しました
    -   `AND`と`OR`間違った`isNullRejected`チェック結果が間違ったクエリ結果[＃38304](https://github.com/pingcap/tidb/issues/38304) @ [イーサール](https://github.com/Yisaer)を引き起こす問題を修正しました
    -   外部結合が除去されるときに`ORDER BY` in `GROUP_CONCAT`が考慮されず、間違ったクエリ結果[＃18216](https://github.com/pingcap/tidb/issues/18216) @ [ウィノロス](https://github.com/winoros)が発生する問題を修正しました。
    -   結合したテーブルの再配置 [＃38736](https://github.com/pingcap/tidb/issues/38736) @ [ウィノロス](https://github.com/winoros)によって誤ってプッシュダウンされた条件が破棄されたときに発生する間違ったクエリ結果の問題を修正しました。

-   TiKV

    -   `cgroup`と`mountinfo`レコードが複数ある場合、TiDB が Gitpod で起動に失敗する問題を修正しました[＃13660](https://github.com/tikv/tikv/issues/13660) @ [タボキ](https://github.com/tabokie)
    -   TiKVメトリックの誤った表現を修正`tikv_gc_compaction_filtered` [＃13537](https://github.com/tikv/tikv/issues/13537) @ [定義2014](https://github.com/Defined2014)
    -   異常な`delete_files_in_range` [＃13534](https://github.com/tikv/tikv/issues/13534) @ [タボキ](https://github.com/tabokie)によって引き起こされるパフォーマンスの問題を修正
    -   スナップショット取得中に期限切れのリースが原因で発生する異常なリージョン競合を修正[＃13553](https://github.com/tikv/tikv/issues/13553) @ [スペードA-タン](https://github.com/SpadeA-Tang)
    -   最初のバッチ[＃13672](https://github.com/tikv/tikv/issues/13672) [＃13704](https://github.com/tikv/tikv/issues/13704) [＃13723](https://github.com/tikv/tikv/issues/13723) @ [HuSharp](https://github.com/HuSharp)で`FLASHBACK`失敗したときに発生したエラーを修正

-   PD

    -   不正確なストリームタイムアウトを修正し、リーダーのスイッチオーバーを高速化[＃5207](https://github.com/tikv/pd/issues/5207) @ [キャビンフィーバーB](https://github.com/CabinfeverB)

-   TiFlash

    -   PageStorage GC がページ削除マーカーを適切にクリアしない場合に発生する、WAL ファイルのサイズが大きすぎることによる OOM 問題を修正しました[＃6163](https://github.com/pingcap/tiflash/issues/6163) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)

-   ツール

    -   TiDBダッシュボード

        -   特定の複雑な SQL 文の実行プランをクエリする際の TiDB OOM 問題を修正[＃1386](https://github.com/pingcap/tidb-dashboard/issues/1386) @ [バウリン](https://github.com/baurine)
        -   NgMonitoring が PD ノード[＃164](https://github.com/pingcap/ng-monitoring/issues/164) @ [中zc](https://github.com/zhongzc)への接続を失ったときに、 Top SQLスイッチが有効にならない可能性がある問題を修正しました。

    -   バックアップと復元 (BR)

        -   復元プロセス中にPDリーダースイッチによって発生する復元失敗の問題を修正[＃36910](https://github.com/pingcap/tidb/issues/36910) @ [モクイシュル28](https://github.com/MoCuishle28)
        -   ログバックアップタスクを一時停止できない問題を修正[＃38250](https://github.com/pingcap/tidb/issues/38250) @ [ジョッカウ](https://github.com/joccau)
        -   BRがログバックアップデータを削除するときに、削除されるべきでないデータを誤って削除してしまう問題を修正[＃38939](https://github.com/pingcap/tidb/issues/38939) @ [リーヴルス](https://github.com/leavrth)
        -   Azure Blob Storage または Google Cloud Storage に保存されたログバックアップデータを初めて削除するときにBR がデータを削除できない問題を修正[＃38229](https://github.com/pingcap/tidb/issues/38229) @ [リーヴルス](https://github.com/leavrth)

    -   TiCDC

        -   `changefeed query`結果のうち`sasl-password`が[＃7182](https://github.com/pingcap/tiflow/issues/7182) @ [ドヴェーデン](https://github.com/dveeden)でマスクされない問題を修正しました
        -   etcdトランザクションでコミットされる操作が多すぎるとTiCDCが利用できなくなる問題を修正[＃7131](https://github.com/pingcap/tiflow/issues/7131) @ [アズドンメン](https://github.com/asddongmen)
        -   REDOログが誤って削除される可能性がある問題を修正[＃6413](https://github.com/pingcap/tiflow/issues/6413) @ [アズドンメン](https://github.com/asddongmen)
        -   Kafka Sink V2 [＃7344](https://github.com/pingcap/tiflow/issues/7344) @ [ハイラスティン](https://github.com/Rustin170506)でワイドテーブルを複製する際のパフォーマンス低下を修正
        -   チェックポイント ts が誤って[＃7274](https://github.com/pingcap/tiflow/issues/7274) @ [ハイラスティン](https://github.com/Rustin170506)に進められる可能性がある問題を修正しました
        -   マウンタモジュール[＃7235](https://github.com/pingcap/tiflow/issues/7235) @ [ハイラスティン](https://github.com/Rustin170506)のログレベルが不適切であるためにログが多すぎる問題を修正しました
        -   TiCDC クラスタに[＃4051](https://github.com/pingcap/tiflow/issues/4051) @ [アズドンメン](https://github.com/asddongmen)という 2 人の所有者が存在する可能性がある問題を修正しました

    -   TiDB データ移行 (DM)

        -   DM WebUIが間違った`allow-list`パラメータ[＃7096](https://github.com/pingcap/tiflow/issues/7096) @ [ズービンウー](https://github.com/zoubingwu)を生成する問題を修正しました
        -   DM ワーカーが開始または停止するときに、一定の確率でデータ競合が発生する問題を修正しました[＃6401](https://github.com/pingcap/tiflow/issues/6401) @ [liumengya94](https://github.com/liumengya94)
        -   DM が`UPDATE`または`DELETE`ステートメントを複製したが、対応する行データが存在しない場合、DM がイベント[＃6383](https://github.com/pingcap/tiflow/issues/6383) @ [GMHDBJD](https://github.com/GMHDBJD)を黙って無視する問題を修正しました。
        -   `query-status`コマンド[＃7189](https://github.com/pingcap/tiflow/issues/7189) @ [GMHDBJD](https://github.com/GMHDBJD)を実行した後に`secondsBehindMaster`フィールドが表示されない問題を修正しました
        -   チェックポイントの更新により大規模なトランザクション[＃5010](https://github.com/pingcap/tiflow/issues/5010) @ [ランス6716](https://github.com/lance6716)がトリガーされる可能性がある問題を修正しました
        -   フルタスクモードで、タスクが同期ステージに入ってすぐに失敗すると、DM が上流のテーブルスキーマ情報[＃7159](https://github.com/pingcap/tiflow/issues/7159) @ [ランス6716](https://github.com/lance6716)を失う可能性がある問題を修正しました。
        -   整合性チェックが有効になっているときにデッドロックが発生する可能性がある問題を修正[＃7241](https://github.com/pingcap/tiflow/issues/7241) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)
        -   タスクの事前チェックにテーブル`INFORMATION_SCHEMA` [＃7317](https://github.com/pingcap/tiflow/issues/7317) @ [ランス6716](https://github.com/lance6716)の`SELECT`権限が必要である問題を修正しました
        -   空のTLS構成によってエラー[＃7384](https://github.com/pingcap/tiflow/issues/7384) @ [liumengya94](https://github.com/liumengya94)が発生する問題を修正

    -   TiDB Lightning

        -   `binary`エンコード形式[＃38351](https://github.com/pingcap/tidb/issues/38351) @ [dsdashun](https://github.com/dsdashun)の文字列型列を含むターゲット テーブルに Apache Parquet ファイルをインポートする際のインポート パフォーマンスの低下を修正しました。

    -   TiDBDumpling

        -   Dumpling が多数のテーブル[＃36549](https://github.com/pingcap/tidb/issues/36549) @ [ランス6716](https://github.com/lance6716)をエクスポートするときにタイムアウトする可能性がある問題を修正しました
        -   一貫性ロックが有効になっているが、アップストリームにターゲットテーブル[＃38683](https://github.com/pingcap/tidb/issues/38683) @ [ランス6716](https://github.com/lance6716)がない場合に報告されるロックエラーを修正しました

## 寄稿者 {#contributors}

TiDB コミュニティからの以下の貢献者に感謝いたします。

-   [645775992](https://github.com/645775992)
-   [アンDJ](https://github.com/An-DJ)
-   [アンドリュー・ディ](https://github.com/AndrewDi)
-   [エルワドバ](https://github.com/erwadba)
-   [ふざ1989](https://github.com/fuzhe1989)
-   [ゴールドウィンド・ティング](https://github.com/goldwind-ting) (初回投稿者)
-   [h3n4l](https://github.com/h3n4l)
-   [イグスリン](https://github.com/igxlin) (初回投稿者)
-   [ihcsim](https://github.com/ihcsim)
-   [ジガオルオ](https://github.com/JigaoLuo)
-   [モルゴ](https://github.com/morgo)
-   [ランキシー](https://github.com/Ranxy)
-   [シェンキデバオジ](https://github.com/shenqidebaozi) (初回投稿者)
-   [桃峰流](https://github.com/taofengliu) (初回投稿者)
-   [TszKitLo40](https://github.com/TszKitLo40)
-   [wxbty](https://github.com/wxbty) (初回投稿者)
-   [zgcbj](https://github.com/zgcbj)

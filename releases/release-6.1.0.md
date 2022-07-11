---
title: TiDB 6.1.0 Release Notes
---

# TiDB6.1.0リリースノート {#tidb-6-1-0-release-notes}

発売日：2022年6月13日

TiDBバージョン：6.1.0

6.1.0では、主な新機能または改善点は次のとおりです。

-   List パーティショニングとリストのCOLUMNSパーティショニングがGAになり、 MySQL 5.7と互換性があります
-   TiFlashパーティションテーブル（動的プルーニング）がGAになります
-   MySQLと互換性のあるユーザーレベルのロック管理をサポートする
-   非トランザクションDMLステートメントをサポートします（ `DELETE`のみをサポートします）
-   TiFlashはオンデマンドデータ圧縮をサポートします
-   MPPはウィンドウ関数フレームワークを導入します
-   TiCDCは、Avroを介したKafkaへの変更ログの複製をサポートしています
-   シャードテーブルをマージおよび移行するための楽観的なモードはGAになります

## 新機能 {#new-features}

### SQL {#sql}

-   List パーティショニングとリストのCOLUMNSパーティショニングはGAになります。どちらもMySQL 5.7と互換性があります。

    ユーザー[List COLUMNS パーティショニング](/partitioned-table.md#list-columns-partitioning) ： [List パーティショニング](/partitioned-table.md#list-partitioning)

-   TiFlashは、コンパクトコマンドの開始をサポートしています。 （実験的）

    TiFlash v6.1.0では`ALTER TABLE ... COMPACT`ステートメントが導入されています。これは、既存のバックグラウンド圧縮メカニズムに基づいて物理データを手動で圧縮する方法を提供します。このステートメントを使用すると、以前の形式でデータを更新し、必要に応じていつでも読み取り/書き込みパフォーマンスを向上させることができます。クラスタをv6.1.0にアップグレードした後、このステートメントを実行してデータを圧縮することをお勧めします。このステートメントは標準SQL構文の拡張であるため、MySQLクライアントと互換性があります。 TiFlashアップグレード以外のシナリオでは、通常、このステートメントを使用する必要はありません。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md) [＃4145](https://github.com/pingcap/tiflash/issues/4145)

-   TiFlashはウィンドウ関数フレームワークを実装し、次のウィンドウ関数をサポートします。

    -   `RANK()`
    -   `DENSE_RANK()`
    -   `ROW_NUMBER()`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [＃33072](https://github.com/pingcap/tidb/issues/33072)

### 可観測性 {#observability}

-   連続プロファイリングは、ARMアーキテクチャとTiFlashをサポートします。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

-   Grafanaは、パフォーマンス概要ダッシュボードを追加して、全体的なパフォーマンス診断のためのシステムレベルのエントリを提供します。

    TiDBの視覚化された監視コンポーネントGrafanaの新しいダッシュボードとして、パフォーマンスの概要は、全体的なパフォーマンス診断のためのシステムレベルのエントリを提供します。トップダウンのパフォーマンス分析方法に従って、パフォーマンス概要ダッシュボードはデータベースの時間内訳に基づいてTiDBパフォーマンスメトリックを再編成し、これらのメトリックをさまざまな色で表示します。これらの色を確認することで、システム全体のパフォーマンスのボトルネックを一目で特定できます。これにより、パフォーマンスの診断時間が大幅に短縮され、パフォーマンスの分析と診断が簡素化されます。

    [ユーザードキュメント](/performance-tuning-overview.md)

### パフォーマンス {#performance}

-   カスタマイズされたリージョンサイズをサポート（実験的）

    リージョンをより大きなサイズに設定すると、リージョンの数を効果的に減らし、リージョンの管理を容易にし、クラスタのパフォーマンスと安定性を向上させることができます。この機能は、リージョン内のより小さな範囲であるバケットの概念を導入します。クエリユニットとしてバケットを使用すると、リージョンがより大きなサイズに設定されている場合に、同時クエリのパフォーマンスを最適化できます。バケットをクエリユニットとして使用すると、ホットリージョンのサイズを動的に調整して、スケジューリングの効率と負荷分散を確保することもできます。この機能は現在実験的中です。実稼働環境での使用はお勧めしません。

    [ユーザードキュメント](/tune-region-performance.md) [＃11515](https://github.com/tikv/tikv/issues/11515)

-   デフォルトのログストレージエンジンとしてRaft Engineを使用する

    v6.1.0以降、TiDBはログのデフォルトのストレージRaft EngineとしてRaftEngineを使用します。 RocksDBと比較して、 Raft EngineはTiKVI / O書き込みトラフィックを最大40％、CPU使用率を10％削減し、特定の負荷の下でフォアグラウンドスループットを約5％向上させ、テールレイテンシーを20％削減します。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine) [＃95](https://github.com/tikv/raft-engine/issues/95)

-   結合順序ヒント構文をサポートする

    -   `LEADING`ヒントは、結合操作のプレフィックスとして指定された順序を使用するようにオプティマイザに通知します。結合の適切なプレフィックスを使用すると、結合の初期段階でデータ量をすばやく削減し、クエリのパフォーマンスを向上させることができます。
    -   `STRAIGHT_JOIN`ヒントは、 `FROM`節のテーブルの順序と一致する順序でテーブルを結合するようにオプティマイザーに通知します。

    これは、テーブル結合の順序を修正するための方法を提供します。ヒントを適切に使用すると、SQLのパフォーマンスとクラスタの安定性を効果的に高めることができます。

    ユーザー[`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join) [＃29932](https://github.com/pingcap/tidb/issues/29932) [`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-)

-   TiFlashはさらに4つの関数をサポートしています。

    -   `FROM_DAYS`
    -   `TO_DAYS`
    -   `TO_SECONDS`
    -   `WEEKOFYEAR`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [＃4679](https://github.com/pingcap/tiflash/issues/4679) [＃4678](https://github.com/pingcap/tiflash/issues/4678) [＃4677](https://github.com/pingcap/tiflash/issues/4677)

-   TiFlashは、動的プルーニングモードでパーティションテーブルをサポートします。

    OLAPシナリオのパフォーマンスを向上させるために、パーティションテーブルで動的プルーニングモードがサポートされています。 TiDBをv6.0.0より前のバージョンからアップグレードする場合は、パフォーマンスを最大化するために、既存のパーティションテーブルの統計を手動で更新することをお勧めします（v6.1.0へのアップグレード後に作成された新しいインストールまたは新しいパーティションには必要ありません）。

    ユーザー[動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) [＃3873](https://github.com/pingcap/tiflash/issues/3873) [MPPモードでパーティションテーブルにアクセスする](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

### 安定性 {#stability}

-   SST破損からの自動回復

    RocksDBがバックグラウンドで破損したSSTファイルを検出すると、TiKVは影響を受けるピアをスケジュールし、他のレプリカを使用してそのデータを回復しようとします。 `background-error-recovery-window`パラメーターを使用して、リカバリーの最大許容時間を設定できます。時間枠内に回復操作が完了しない場合、TiKVはpanicになります。この機能は、回復可能な損傷したストレージを自動的に検出して回復するため、クラスタの安定性が向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610) [＃10578](https://github.com/tikv/tikv/issues/10578)

-   非トランザクションDMLステートメントをサポートする

    大規模なデータ処理のシナリオでは、大規模なトランザクションを伴う単一のSQLステートメントが、クラスタの安定性とパフォーマンスに悪影響を与える可能性があります。 v6.1.0以降、TiDBは、バッチ処理のために`DELETE`のステートメントを複数のステートメントに分割する構文の提供をサポートしています。分割ステートメントは、トランザクションのアトミック性と分離を損ないますが、クラスタの安定性を大幅に向上させます。詳細な構文については、 [`BATCH`](/sql-statements/sql-statement-batch.md)を参照してください。

    [ユーザードキュメント](/non-transactional-dml.md)

-   TiDBは、最大GC待機時間の構成をサポートします

    TiDBのトランザクションは、マルチバージョン同時実行制御（MVCC）メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。古いデータは、ガベージコレクション（GC）タスクによって定期的にクリーンアップされます。これは、ストレージスペースを再利用して、クラスタのパフォーマンスと安定性を向上させるのに役立ちます。 GCはデフォルトで10分ごとにトリガーされます。長時間実行されるトランザクションが対応する履歴データにアクセスできるようにするために、実行中のトランザクションがある場合、GCタスクは遅延されます。 GCタスクが無期限に遅延しないようにするために、TiDBはシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)を導入して、GCタスクの最大遅延時間を制御します。最大遅延時間を超えると、GCが強制的に実行されます。変数のデフォルト値は24時間です。この機能を使用すると、GCの待機時間と長時間実行されるトランザクションの関係を制御できるため、クラスタの安定性が向上します。

    [ユーザードキュメント](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

-   TiDBは、自動統計収集タスクの最大実行時間の構成をサポートしています

    データベースは、統計を収集することでデータの分散を効果的に理解できます。これにより、合理的な実行プランが生成され、SQL実行の効率が向上します。 TiDBは、バックグラウンドで頻繁に変更されるデータオブジェクトに関する統計を定期的に収集します。ただし、統計の収集はクラスタリソースを消費し、ビジネスのピーク時にビジネスの安定した運用に影響を与える可能性があります。

    v6.1.0以降、TiDBではバックグラウンド統計収集の最大実行時間を制御するために[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)が導入されています。これは、デフォルトでは12時間です。アプリケーションでリソースのボトルネックが発生しない場合は、TiDBがタイムリーに統計を収集できるように、この変数を変更しないことをお勧めします。

    [ユーザードキュメント](/system-variables.md)

### 使いやすさ {#ease-of-use}

-   複数のレプリカが失われた場合のワンストップオンラインデータリカバリをサポートする

    TiDB v6.1.0より前では、マシンの障害のために複数のリージョンレプリカが失われた場合、ユーザーはすべてのTiKVサーバーを停止し、 TiKV Controlを使用してTiKVを1つずつ回復する必要があります。 TiDB v6.1.0以降、リカバリプロセスは完全に自動化されており、TiKVを停止する必要がなく、オンラインの他のアプリケーションに影響を与えません。回復プロセスはPD Controlを使用してトリガーでき、よりユーザーフレンドリーな要約情報を提供します。

    [ユーザードキュメント](/online-unsafe-recovery.md) [＃10483](https://github.com/tikv/tikv/issues/10483)

-   履歴統計収集タスクの表示をサポート

    `SHOW ANALYZE STATUS`ステートメントを使用して、クラスターレベルの統計収集タスクを表示できます。 TiDB v6.1.0より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンスレベルのタスクのみを示し、履歴タスクレコードはTiDBの再起動後にクリアされます。したがって、履歴統計の収集時間と詳細を表示することはできません。 TiDB v6.1.0以降、統計収集タスクの履歴レコードは保持され、クラスタの再起動後にクエリを実行できます。これにより、統計の異常によって引き起こされるクエリパフォーマンスの問題をトラブルシューティングするためのリファレンスが提供されます。

    [ユーザードキュメント](/sql-statements/sql-statement-show-analyze-status.md)

-   オンラインでのTiDB、TiKV、およびTiFlash構成の変更のサポート

    以前のバージョンのTiDBでは、構成アイテムを変更した後、変更を有効にするためにクラスタを再起動する必要があります。これにより、オンラインサービスが中断される可能性があります。この問題に対処するために、TiDB v6.1.0にはオンライン構成機能が導入されており、クラスタを再起動せずにパラメーターの変更を検証できます。具体的な最適化は次のとおりです。

    -   一部のTiDB構成アイテムをシステム変数に変換して、オンラインで変更して永続化できるようにします。元の構成アイテムは、変換後に非推奨になることに注意してください。変換された構成アイテムの詳細なリストについては、 [Configuration / コンフィグレーションファイルのパラメーター](#configuration-file-parameters)を参照してください。
    -   一部のTiKVパラメーターのオンライン構成をサポートします。パラメータの詳細なリストについては、 [その他](#others)を参照してください。
    -   TiFlash構成アイテム`max_threads`をシステム変数`tidb_max_tiflash_threads`に変換して、構成をオンラインで変更して永続化できるようにします。元の構成アイテムは変換後も残ることに注意してください。

    以前のバージョンからアップグレードされたv6.1.0クラスター（オンラインおよびオフラインのアップグレードを含む）の場合、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成アイテムがすでに存在する場合、TiDBは、アップグレードプロセス中に、構成されたアイテムの値を対応するシステム変数の値に自動的に更新します。このように、アップグレード後、システムの動作はパラメーターの最適化の影響を受けません。
    -   上記の自動更新は、アップグレード中に1回だけ発生します。アップグレード後、廃止された構成アイテムは無効になります。

    この機能を使用すると、システムを再起動してサービスを中断する代わりに、パラメーターをオンラインで変更し、検証して永続化することができます。これにより、日常のメンテナンスが容易になります。

    [ユーザードキュメント](/dynamic-config.md)

-   クエリまたは接続の強制終了をグローバルにサポート

    `enable-global-kill`構成（デフォルトで有効）を使用して、グローバルキル機能を制御できます。

    TiDB v6.1.0より前では、操作が多くのリソースを消費し、クラスタの安定性の問題を引き起こす場合、ターゲットTiDBインスタンスに接続してから、 `KILL TIDB ${id};`コマンドを実行してターゲット接続と操作を終了する必要があります。多くのTiDBインスタンスの場合、この方法は使いやすくなく、間違った操作をする傾向があります。 v6.1.0以降、 `enable-global-kill`の構成が導入され、デフォルトで有効になっています。クライアントとTiDBの間にプロキシがある場合に、他のクエリやセッションを誤って誤って終了することを心配することなく、任意のTiDBインスタンスでkillコマンドを実行して、指定した接続と操作を終了できます。現在、TiDBはCtrl+Cを使用してクエリまたはセッションを終了することをサポートしていません。

    [ユーザードキュメント](/tidb-configuration-file.md#enable-global-kill-new-in-v610) [＃8854](https://github.com/pingcap/tidb/issues/8854)

-   TiKV API V2（実験的）

    v6.1.0より前では、TiKVがRaw Key Valueストレージとして使用される場合、TiKVは、クライアントから渡された生データのみを格納するため、基本的なKeyValue読み取りおよび書き込み機能のみを提供します。

    TiKV API V2は、次のような新しいRawKeyValueストレージ形式とアクセスインターフェイスを提供します。

    -   データはMVCCに保存され、データの変更タイムスタンプが記録されます。この機能は、変更データのキャプチャと増分バックアップおよび復元を実装するための基盤を築きます。
    -   データはさまざまな使用法に応じてスコープが設定され、単一のTiDBクラスタ、トランザクションKV、RawKVアプリケーションの共存をサポートします。

    <Warning>基盤となるストレージ形式が大幅に変更されたため、API V2を有効にした後、TiKVクラスタをv6.1.0より前のバージョンにロールバックすることはできません。 TiKVをダウングレードすると、データが破損する可能性があります。</Warning>

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [＃11745](https://github.com/tikv/tikv/issues/11745)

### MySQLの互換性 {#mysql-compatibility}

-   MySQLを使用したユーザーレベルのロック管理との互換性をサポート

    ユーザーレベルのロックは、組み込み関数を介してMySQLによって提供されるユーザー名のロック管理システムです。ロック関数は、ロックのブロック、待機、およびその他のロック管理機能を提供できます。ユーザーレベルのロックは、Rails、Elixir、EctoなどのORMフレームワークでも広く使用されています。 v6.1.0以降、TiDBはMySQL互換のユーザーレベルのロック管理をサポートし、 `GET_LOCK` 、および`RELEASE_LOCK`の関数をサポートして`RELEASE_ALL_LOCKS`ます。

    [ユーザードキュメント](/functions-and-operators/locking-functions.md) [＃14994](https://github.com/pingcap/tidb/issues/14994)

### データ移行 {#data-migration}

-   シャードテーブルをマージおよび移行するための楽観的なモードはGAになります

    DMは、毎日の使用シナリオの90％をカバーする楽観的なモードで、シャーディングされたテーブルからデータをマージおよび移行するタスクに対して、多数のシナリオテストを追加します。悲観的モードと比較して、楽観的モードはより簡単で効率的に使用できます。使用上の注意をよく理解した後で、楽観的なモードを使用することをお勧めします。

    [ユーザードキュメント](/dm/feature-shard-merge-optimistic.md#restrictions)

-   DM WebUIは、指定されたパラメーターに従ってタスクを開始することをサポートします

    移行タスクを開始するときに、開始時間とセーフモード期間を指定できます。これは、多数のソースを使用して増分移行タスクを作成する場合に特に役立ち、ソースごとにbinlogの開始位置を指定する必要がなくなります。

    [ユーザードキュメント](/dm/dm-webui-guide.md) [＃5442](https://github.com/pingcap/tiflow/issues/5442)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiDBは、さまざまなサードパーティのデータエコシステムとのデータ共有をサポートしています

    -   TiCDCは、TiDBインクリメンタルデータをAvro形式でKafkaに送信することをサポートし、Confluentを介してKSQLやSnowflakeなどのサードパーティとデータを共有できるようにします。

        [ユーザードキュメント](/ticdc/ticdc-avro-protocol.md) [＃5338](https://github.com/pingcap/tiflow/issues/5338)

    -   TiCDCは、テーブルごとにTiDBからさまざまなKafkaトピックへの増分データのディスパッチをサポートします。これをCanal-json形式と組み合わせると、Flinkと直接データを共有できます。

        [ユーザードキュメント](/ticdc/manage-ticdc.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink) [＃4423](https://github.com/pingcap/tiflow/issues/4423)

    -   TiCDCはSASLGSSAPI認証タイプをサポートし、Kafkaを使用したSASL認証の例を追加します。

        [ユーザードキュメント](/ticdc/manage-ticdc.md#ticdc-uses-the-authentication-and-authorization-of-kafka) [＃4423](https://github.com/pingcap/tiflow/issues/4423)

-   TiCDCは、 `charset=GBK`のテーブルの複製をサポートしています。

    [ユーザードキュメント](/character-set-gbk.md#component-compatibility) [＃4806](https://github.com/pingcap/tiflow/issues/4806)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                           | タイプを変更する   | 説明                                                                                                                                                   |
| ----------------------------------------------------------------------------------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                    | 変更         | デフォルト値は`OFF`から`ON`に変更されます。                                                                                                                           |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                           | 変更         | この変数はGLOBALスコープを追加し、変数値はクラスタに保持されます。                                                                                                                 |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)                                                       | 変更         | 可変スコープがINSTANCEからGLOBALに変更されました。変数値はクラスタに保持され、値の範囲は`[0, 1073741824]`に変更されます。                                                                         |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)                                       | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `security.require-secure-transport` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                    |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)                                   | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `performance.committer-concurrency` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                    |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                       | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `run-auto-analyze` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                                     |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)       | 新しく追加されました | この変数は、TiDBが`ONLY_FULL_GOUP_BY`チェックを実行するときの動作を制御します。                                                                                                  |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                           | 新しく追加されました | v6.1.0以降、TiDBの結合したテーブルの再配置再注文アルゴリズムは外部結合をサポートしています。この変数はサポート動作を制御し、デフォルト値は`ON`です。                                                                    |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                         | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.enabled` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                          |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)                                             | 新しく追加されました | この変数は、コミットされていないトランザクションによってブロックされるGCセーフポイントの最大時間を設定するために使用されます。                                                                                     |
| [tidb_max_auto_analyze_time](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                                     | 新しく追加されました | この変数は、auto analyzeの最大実行時間を指定するために使用されます。                                                                                                             |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)                                       | 新しく追加されました | この変数は、TiFlashがリクエストを実行するための最大同時実行性を設定するために使用されます。                                                                                                    |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)                                                 | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `oom-action` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                                           |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)                                           | 新しく追加されました | この変数は、TiDBが統計を更新するときの最大メモリ使用量を制御します。これには、ユーザーが手動で実行した[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)や、TiDBバックグラウンドでの自動分析タスクが含まれます。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)                   | 新しく追加されました | この変数は、非トランザクションDMLステートメントでエラーが発生したときにエラーをすぐに返すかどうかを指定します。                                                                                            |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-new-in-v610) | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.memory-guard-ratio` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                               |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                             | 新しく追加されました | この設定は、以前は`tidb.toml`オプション（ `prepared-plan-cache.capacity` ）でしたが、TiDBv6.1.0以降のシステム変数に変更されました。                                                         |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)                                   | 新しく追加されました | この変数は、TiDB統計キャッシュのメモリクォータを設定します。                                                                                                                     |

### Configuration / コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| Configuration / コンフィグレーションファイル | Configuration / コンフィグレーション                                                                                                                                                                             | タイプを変更する   | 説明                                                                                                                                                        |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB                           | `committer-concurrency`                                                                                                                                                                                | 削除         | システム変数`tidb_committer_concurrency`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                            |
| TiDB                           | `lower-case-table-names`                                                                                                                                                                               | 削除         | 現在、TiDBは`lower_case_table_name=2`のみをサポートしています。別の値が設定されている場合、クラスタがv6.1.0にアップグレードされた後、値は失われます。                                                              |
| TiDB                           | `mem-quota-query`                                                                                                                                                                                      | 削除         | システム変数`tidb_mem_quota_query`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                                  |
| TiDB                           | `oom-action`                                                                                                                                                                                           | 削除         | システム変数`tidb_mem_oom_action`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                                   |
| TiDB                           | `prepared-plan-cache.capacity`                                                                                                                                                                         | 削除         | システム変数`tidb_prepared_plan_cache_size`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                         |
| TiDB                           | `prepared-plan-cache.enabled`                                                                                                                                                                          | 削除         | システム変数`tidb_enable_prepared_plan_cache`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                       |
| TiDB                           | `query-log-max-len`                                                                                                                                                                                    | 削除         | システム変数`tidb_query_log_max_len`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                                |
| TiDB                           | `require-secure-transport`                                                                                                                                                                             | 削除         | システム変数`require_secure_transport`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                              |
| TiDB                           | `run-auto-analyze`                                                                                                                                                                                     | 削除         | システム変数`tidb_enable_auto_analyze`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                              |
| TiDB                           | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)                                                                                                                     | 新しく追加されました | グローバルキル（インスタンス間のクエリまたは接続の終了）機能を有効にするかどうかを制御します。値が`true`の場合、 `KILL`ステートメントと`KILL TIDB`ステートメントの両方でインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。 |
| TiDB                           | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                                                                                 | 新しく追加されました | 統計キャッシュのメモリクォータを有効にするかどうかを制御します。                                                                                                                          |
| TiKV                           | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1)                                                                                                                                           | 変更         | デフォルト値は`FALSE`から`TRUE`に変更されます。                                                                                                                            |
| TiKV                           | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys)                                                                                                                                       | 変更         | デフォルト値は1440000から`region-split-keys / 2 * 3`に変更されます。                                                                                                       |
| TiKV                           | [`region-max-size`](/tikv-configuration-file.md#region-max-size)                                                                                                                                       | 変更         | デフォルト値は144MBから`region-split-size / 2 * 3`に変更されます。                                                                                                         |
| TiKV                           | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)                                                                                                     | 新しく追加されました | リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。                                                                                                                      |
| TiKV                           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                                                                         | 新しく追加されました | `enable-region-bucket`が真の場合のバケットのサイズ。                                                                                                                     |
| TiKV                           | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size)                                                                                                                   | 新しく追加されました | ローカルにキャッシュされたタイムスタンプの最小数。                                                                                                                                 |
| TiKV                           | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval)                                                                                                                               | 新しく追加されました | ローカルにキャッシュされたタイムスタンプが更新される間隔。                                                                                                                             |
| TiKV                           | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-new-in-v610)                                                                                                     | 新しく追加されました | スナップショットファイルのサイズがこの値を超えると、スナップショットファイルは複数のファイルに分割されます。                                                                                                    |
| TiKV                           | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit)                                                                                                                                 | 新しく追加されました | Raft Engineのメモリ使用量の制限を指定します。                                                                                                                              |
| TiKV                           | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610)                                                                                 | 新しく追加されました | RocksDBが回復可能なバックグラウンドエラーを検出した後、最大回復時間が許可されます。                                                                                                             |
| TiKV                           | [`storage.api-version`](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                           | 新しく追加されました | TiKVが生のKey-Valueストアとして機能するときにTiKVによって使用されるストレージ形式とインターフェイスバージョン。                                                                                          |
| PD                             | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-new-in-v610)                                                                                                  | 新しく追加されました | ストアがオンラインになるまでの最大待機時間を制御します。                                                                                                                              |
| TiCDC                          | [`enable-tls`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)                                                                                                                                   | 新しく追加されました | TLSを使用してダウンストリームのKafkaインスタンスに接続するかどうか。                                                                                                                    |
| TiCDC                          | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新しく追加されました | KafkaのSASL/GSSAPI認証をサポートするために使用されます。詳細については、 [`kafka`を使用してシンクURIを構成する](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)を参照してください。                    |
| TiCDC                          | [`avro-decimal-handling-mode`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/manage-ticdc.md#configure-sink-uri-with-kafka)                  | 新しく追加されました | Avro形式の出力詳細を決定します。                                                                                                                                        |
| TiCDC                          | [`dispatchers.topic`](/ticdc/manage-ticdc.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                                    | 新しく追加されました | TiCDCがインクリメンタルデータをさまざまなKafkaトピックにディスパッチする方法を制御します。                                                                                                        |
| TiCDC                          | [`dispatchers.partition`](/ticdc/manage-ticdc.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                                | 新しく追加されました | `dispatchers.partition`は`dispatchers.dispatcher`のエイリアスです。 TiCDCがインクリメンタルデータをKafkaパーティションにディスパッチする方法を制御します。                                                |
| TiCDC                          | [`schema-registry`](/ticdc/manage-ticdc.md#integrate-ticdc-with-kafka-connect-confluent-platform)                                                                                                      | 新しく追加されました | Avroスキーマを格納するスキーマレジストリエンドポイントを指定します。                                                                                                                      |
| DM                             | `dmctl start-relay`コマンドの`worker`                                                                                                                                                                       | 削除         | このパラメーターの使用はお勧めしません。より簡単な実装を提供します。                                                                                                                        |
| DM                             | ソース構成ファイルの`relay-dir`                                                                                                                                                                                  | 削除         | ワーカー構成ファイル内の同じ構成項目に置き換えられました。                                                                                                                             |
| DM                             | タスク構成ファイルの`is-sharding`                                                                                                                                                                                | 削除         | `shard-mode`の構成アイテムに置き換えられました。                                                                                                                            |
| DM                             | タスク構成ファイルの`auto-fix-gtid`                                                                                                                                                                              | 削除         | v5.xで非推奨になり、v6.1.0で正式に削除されました。                                                                                                                            |
| DM                             | ソース構成ファイルの`meta-dir`と`charset`                                                                                                                                                                         | 削除         | v5.xで非推奨になり、v6.1.0で正式に削除されました。                                                                                                                            |

### その他 {#others}

-   プリペアドプランキャッシュをデフォルトで有効にする

    プリペアドプランキャッシュは、新しいクラスターでデフォルトで有効になっており、 `Prepare` / `Execute`リクエストの実行プランをキャッシュします。後続の実行では、クエリプランの最適化をスキップできるため、パフォーマンスが向上します。アップグレードされたクラスターは、構成ファイルから構成を継承します。新しいクラスターは新しいデフォルト値を使用します。つまり、 プリペアドプランキャッシュはデフォルトで有効になっており、各セッションは最大100のプランをキャッシュできます（ `capacity=100` ）。この機能のメモリ消費量については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)を参照してください。

-   TiDB v6.1.0より前では、 `SHOW ANALYZE STATUS`はインスタンスレベルのタスクを示し、タスクレコードはTiDBの再起動後にクリアされます。 TiDB v6.1.0以降、 `SHOW ANALYZE STATUS`はクラスターレベルのタスクを示し、タスクレコードは再起動後も保持されます。 `tidb_analyze_version = 2`の場合、 `Job_info`列に`analyze option`情報が追加されます。

-   TiKV内の破損したSSTファイルにより、TiKVプロセスがpanicになる可能性があります。 TiDB v6.1.0より前は、SSTファイルが破損しているため、TiKVはすぐにpanicに陥りました。 TiDB v6.1.0以降、SSTファイルが破損してから1時間後にTiKVプロセスがpanicになります。

-   次のTiKV構成アイテムは[オンラインで値を変更する](/dynamic-config.md#modify-tikv-configuration-online)をサポートします：

    -   `raftstore.raft-entry-max-size`
    -   `quota.foreground-cpu-time`
    -   `quota.foreground-write-bandwidth`
    -   `quota.foreground-read-bandwidth`
    -   `quota.max-delay-duration`
    -   `server.grpc-memory-pool-quota`
    -   `server.max-grpc-send-msg-len`
    -   `server.raft-msg-max-batch-size`

-   v6.1.0では、一部の構成ファイルのパラメーターがシステム変数に変換されます。以前のバージョンからアップグレードされたv6.1.0クラスター（オンラインおよびオフラインのアップグレードを含む）の場合、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成アイテムがすでに存在する場合、TiDBは、アップグレードプロセス中に、構成されたアイテムの値を対応するシステム変数の値に自動的に更新します。このように、アップグレード後、パラメータの最適化によってシステムの動作が変わることはありません。
    -   上記の自動更新は、アップグレード中に1回だけ発生します。アップグレード後、廃止された構成アイテムは無効になります。

-   ダッシュボードページがDM WebUIから削除されます。

-   `dispatchers.topic`と`dispatchers.partition`が有効になっている場合、TiCDCをv6.1.0より前のバージョンにダウングレードすることはできません。

-   Avroプロトコルを使用するTiCDC Changefeedは、v6.1.0より前のバージョンにダウングレードすることはできません。

## 改善 {#improvements}

-   TiDB

    -   `UnionScanRead`オペレーター[＃32433](https://github.com/pingcap/tidb/issues/32433)のパフォーマンスを向上させる
    -   `EXPLAIN`の出力でのタスクタイプの表示を改善します（MPPタスクタイプを追加します） [＃33332](https://github.com/pingcap/tidb/issues/33332)
    -   列[＃10377](https://github.com/pingcap/tidb/issues/10377)のデフォルト値として`rand()`を使用することをサポートします
    -   列[＃33870](https://github.com/pingcap/tidb/issues/33870)のデフォルト値として`uuid()`を使用することをサポートします
    -   列の文字セットを`latin1`から`utf8`に[＃34008](https://github.com/pingcap/tidb/issues/34008)することを`utf8mb4`

-   TiKV

    -   インメモリペシミスティックロックを使用する場合のCDCの古い値のヒット率を改善する[＃12279](https://github.com/tikv/tikv/issues/12279)
    -   ヘルスチェックを改善して、使用できないRaftstoreを検出し、TiKVクライアントが時間[＃12398](https://github.com/tikv/tikv/issues/12398)でリージョンキャッシュを更新できるようにします。
    -   Raft Engineでのメモリ制限の設定を[＃12255](https://github.com/tikv/tikv/issues/12255)
    -   TiKVは、損傷したSSTファイルを自動的に検出して削除し、製品の可用性を向上させます[＃10578](https://github.com/tikv/tikv/issues/10578)
    -   CDCはRawKV1をサポートし[＃11965](https://github.com/tikv/tikv/issues/11965)
    -   大きなスナップショットファイルを複数のファイルに分割することをサポート[＃11595](https://github.com/tikv/tikv/issues/11595)
    -   スナップショットガベージコレクションをRaftstoreからバックグラウンドスレッドに移動して、スナップショットGCがRaftstoreメッセージループをブロックしないようにします[＃11966](https://github.com/tikv/tikv/issues/11966)
    -   最大メッセージ長（ `max-grpc-send-msg-len` ）とgPRCメッセージの最大バッチサイズ（ `raft-msg-max-batch-size` ）の動的設定をサポート[＃12334](https://github.com/tikv/tikv/issues/12334)
    -   Raftを介しオンラインの安全でない復元計画の実行を[＃10483](https://github.com/tikv/tikv/issues/10483)

-   PD
    -   リージョンラベルの存続時間（TTL）をサポート[＃4694](https://github.com/tikv/pd/issues/4694)
    -   サポートリージョンバケット[＃4668](https://github.com/tikv/pd/issues/4668)
    -   デフォルトでSwaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

-   TiFlash

    -   マージフェーズ[＃4451](https://github.com/pingcap/tiflash/issues/4451)でより効率的なアルゴリズムが使用されるように、集計演算子のメモリ計算を最適化します。

-   ツール

    -   バックアップと復元（BR）

        -   空のデータベースのバックアップと復元のサポート[＃33866](https://github.com/pingcap/tidb/issues/33866)

    -   TiDB Lightning

        -   スキャッターリージョンプロセスの安定性を向上させるために、スキャッターリージョンをバッチモードに最適化する[＃33618](https://github.com/pingcap/tidb/issues/33618)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `in`関数が`bit`タイプのデータを処理するときに発生する可能性のあるpanicの問題を修正します[＃33070](https://github.com/pingcap/tidb/issues/33070)
    -   `UnionScan`演算子は順序[＃33175](https://github.com/pingcap/tidb/issues/33175)を維持できないため、誤ったクエリ結果の問題を修正します
    -   マージ結合演算子が特定の場合に間違った結果を得る問題を修正します[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   動的プルーニングモード[＃33231](https://github.com/pingcap/tidb/issues/33231)で`index join`の結果が間違っている可能性があるという問題を修正します。
    -   パーティションテーブルの一部のパーティションが削除されたときにデータがガベージコレクションされない可能性がある問題を修正します[＃33620](https://github.com/pingcap/tidb/issues/33620)
    -   クラスタのPDノードが置き換えられた後、一部のDDLステートメントが一定期間スタックする可能性がある問題を修正します[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`のテーブルが照会されたときにTiDBサーバーのメモリが不足する可能性がある問題を修正します。この問題は、Grafanaダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックしたときに発生する可能性があります
    -   システム変数`max_allowed_packet`が有効にならない問題を修正します[＃31422](https://github.com/pingcap/tidb/issues/31422)
    -   [＃34502](https://github.com/pingcap/tidb/issues/34502)モジュールのメモリリークの問題を修正します[＃34525](https://github.com/pingcap/tidb/issues/34525)
    -   PointGetプラン[＃32371](https://github.com/pingcap/tidb/issues/32371)でプランキャッシュが間違っている可能性がある問題を修正します
    -   プランキャッシュがRC分離レベル[＃34447](https://github.com/pingcap/tidb/issues/34447)で開始されたときに、クエリ結果が間違っている可能性がある問題を修正します。

-   TiKV

    -   TiKVインスタンスがオフラインになるとRaftログラグが増加する問題を修正します[＃12161](https://github.com/tikv/tikv/issues/12161)
    -   マージされるターゲットリージョンが無効であるためにTiKVがパニックになり、ピアを予期せず破壊する問題を修正します[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   v5.3.1またはv5.4.0からv6.0.0以降のバージョン[＃12269](https://github.com/tikv/tikv/issues/12269)にアップグレードするときにTiKVが`failed to load_latest_options`エラーを報告する問題を修正します。
    -   メモリリソースが不足しているときにRaftログを追加することによって引き起こされるOOMの問題を修正します[＃11379](https://github.com/tikv/tikv/issues/11379)
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされるTiKVpanicの問題を修正します
    -   `stats_monitor`がデッドループに陥った後、短時間でTiKVメモリ使用量が急増する問題を修正します[＃12416](https://github.com/tikv/tikv/issues/12416)
    -   FollowerRead3を使用するとTiKVが`invalid store ID 0`エラーを報告する問題を修正し[＃12478](https://github.com/tikv/tikv/issues/12478)

-   PD

    -   13の間違ったステータス`not leader`を修正し[＃4797](https://github.com/tikv/pd/issues/4797)
    -   一部のコーナーケースでのTSOフォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)
    -   PDリーダーの転送後に削除されたトゥームストーンストアが再び表示される問題を修正します[＃4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダーの転送直後にスケジューリングを開始できない問題を修正します[＃4769](https://github.com/tikv/pd/issues/4769)

-   TiDBダッシュボード

    -   Top SQL機能が有効になる前に実行されていたSQLステートメントのCPUオーバーヘッドをTop SQLが収集できないバグを修正します[＃33859](https://github.com/pingcap/tidb/issues/33859)

-   TiFlash

    -   多くのINSERTおよびDELETE操作後の潜在的なデータの不整合を修正します[＃4956](https://github.com/pingcap/tiflash/issues/4956)

-   ツール

    -   TiCDC

        -   DDLスキーマのバッファリング方法を最適化することにより、過剰なメモリ使用量を修正します[＃1386](https://github.com/pingcap/tiflow/issues/1386)
        -   大規模なトランザクションによって引き起こされるOOMを修正する[＃5280](https://github.com/pingcap/tiflow/issues/5280)
        -   特別なインクリメンタルスキャンシナリオで発生するデータ損失を修正する[＃5468](https://github.com/pingcap/tiflow/issues/5468)

    -   TiDBデータ移行（DM）

        -   `start-time`タイムゾーンの問題を修正し、DMの動作をダウンストリームタイムゾーンの使用からアップストリームタイムゾーン[＃5271](https://github.com/pingcap/tiflow/issues/5471)の使用に変更します。
        -   タスクが自動的に再開した後、DMがより多くのディスクスペースを占有する問題を修正します[＃3734](https://github.com/pingcap/tiflow/issues/3734) [＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   チェックポイントフラッシュにより、失敗した行のデータがスキップされる可能性がある問題を修正します[＃5279](https://github.com/pingcap/tiflow/issues/5279)
        -   場合によっては、ダウンストリームでフィルター処理されたDDLを手動で実行すると、タスクの再開が失敗する可能性があるという問題を修正します[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルを複製できない問題を修正します[＃5255](https://github.com/pingcap/tiflow/issues/5255)
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの最初に主キーがない場合に発生するDMワーカーのpanicの問題を修正します。
        -   GTIDを有効にした場合、またはタスクが自動的に再開された場合に、CPU使用率が増加し、大量のログが出力される可能性がある問題を修正します[＃5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM WebUIのオフラインオプションおよびその他の使用上の問題を修正し[＃4993](https://github.com/pingcap/tiflow/issues/4993)
        -   アップストリーム[＃3731](https://github.com/pingcap/tiflow/issues/3731)でGTIDが空の場合にインクリメンタルタスクを開始できない問題を修正します。
        -   空の構成によりdm-masterがpanicになる可能性がある問題を修正します[＃3732](https://github.com/pingcap/tiflow/issues/3732)

    -   TiDB Lightning

        -   事前チェックでローカルディスクリソースとクラスタの可用性がチェックされない問題を修正します[＃34213](https://github.com/pingcap/tidb/issues/34213)
        -   スキーマ[＃33381](https://github.com/pingcap/tidb/issues/33381)の誤ったルーティングの問題を修正します
        -   TiDB LightningがパニックになったときにPD構成が正しく復元されない問題を修正します[＃31733](https://github.com/pingcap/tidb/issues/31733)
        -   `auto_increment`列[＃29737](https://github.com/pingcap/tidb/issues/27937)の範囲外のデータが原因で発生するローカルバックエンドのインポートエラーの問題を修正します。
        -   `auto_random`列または`auto_increment`列がnullの場合のローカルバックエンドインポートの失敗の問題を修正します[＃34208](https://github.com/pingcap/tidb/issues/34208)

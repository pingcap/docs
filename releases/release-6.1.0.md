---
title: TiDB 6.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.0.
---

# TiDB 6.1.0 リリースノート {#tidb-6-1-0-release-notes}

発売日：2022年6月13日

TiDB バージョン: 6.1.0

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.1.0#version-list)

6.1.0 の主な新機能または改善点は次のとおりです。

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になり、 MySQL 5.7と互換性があります
-   TiFlashパーティションテーブル(動的プルーニング) が GA になりました
-   MySQLと互換性のあるユーザーレベルのロック管理をサポート
-   非トランザクション DML ステートメントをサポートする (サポートは`DELETE`のみ)
-   TiFlash はオンデマンドのデータ圧縮をサポート
-   MPP はウィンドウ関数フレームワークを導入します
-   TiCDC は、Avro を介した Kafka への変更ログのレプリケートをサポートしています
-   TiCDC は、レプリケーション中に大きなトランザクションを分割することをサポートしています。これにより、大きなトランザクションによって引き起こされるレプリケーションのレイテンシーが大幅に削減されます。
-   シャード テーブルをマージおよび移行するための楽観的モードが GA になる

## 新機能 {#new-features}

### SQL {#sql}

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になります。どちらもMySQL 5.7と互換性があります。

    ユーザー文書: [List パーティショニング](/partitioned-table.md#list-partitioning) 、 [List COLUMNS パーティショニング](/partitioned-table.md#list-columns-partitioning)

-   TiFlash は、コンパクト コマンドの開始をサポートしています。 (実験的)

    TiFlash v6.1.0 では`ALTER TABLE ... COMPACT`ステートメントが導入され、既存のバックグラウンド圧縮メカニズムに基づいて物理データを手動で圧縮する方法が提供されます。このステートメントを使用すると、必要に応じていつでも以前の形式のデータを更新し、読み取り/書き込みのパフォーマンスを向上させることができます。クラスターを v6.1.0 にアップグレードした後、このステートメントを実行してデータを圧縮することをお勧めします。このステートメントは標準 SQL 構文の拡張であるため、MySQL クライアントと互換性があります。 TiFlashアップグレード以外のシナリオでは、通常、このステートメントを使用する必要はありません。

    [ユーザー文書](/sql-statements/sql-statement-alter-table-compact.md) 、 [#4145](https://github.com/pingcap/tiflash/issues/4145)

-   TiFlash はウィンドウ関数フレームワークを実装し、次のウィンドウ関数をサポートします。

    -   `RANK()`
    -   `DENSE_RANK()`
    -   `ROW_NUMBER()`

    [ユーザー文書](/tiflash/tiflash-supported-pushdown-calculations.md) 、 [#33072](https://github.com/pingcap/tidb/issues/33072)

### 可観測性 {#observability}

-   継続的なプロファイリングは、ARMアーキテクチャとTiFlashをサポートしています。

    [ユーザー文書](/dashboard/continuous-profiling.md)

-   Grafana は、パフォーマンス概要ダッシュボードを追加して、全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。

    TiDB の視覚化された監視コンポーネントGrafana の新しいダッシュボードとして、Performance Overview は、全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。トップダウンのパフォーマンス分析方法に従って、パフォーマンス概要ダッシュボードは、データベース時間内訳に基づいて TiDB パフォーマンス メトリックを再編成し、これらのメトリックを異なる色で表示します。これらの色をチェックすることで、システム全体のパフォーマンスのボトルネックを一目で特定できるため、パフォーマンスの診断時間が大幅に短縮され、パフォーマンスの分析と診断が簡素化されます。

    [ユーザー文書](/performance-tuning-overview.md)

### パフォーマンス {#performance}

-   カスタマイズされたリージョンサイズをサポート (実験的)

    リージョンをより大きなサイズに設定すると、リージョンの数を効果的に減らし、リージョンを管理しやすくし、クラスターのパフォーマンスと安定性を向上させることができます。この機能は、 リージョン内のより小さな範囲であるバケットの概念を導入します。バケットをクエリ ユニットとして使用すると、リージョンがより大きなサイズに設定されている場合に同時クエリのパフォーマンスを最適化できます。クエリ ユニットとしてバケットを使用すると、ホット リージョンのサイズを動的に調整して、スケジューリングの効率と負荷バランスを確保することもできます。この機能は現在実験的です。本番環境で使用することはお勧めしません。

    [ユーザー文書](/tune-region-performance.md) 、 [#11515](https://github.com/tikv/tikv/issues/11515)

-   Raft Engine をデフォルトのログstorageエンジンとして使用する

    v6.1.0 以降、TiDB はRaft Engine をログのデフォルトのstorageエンジンとして使用します。 RocksDB と比較して、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40% 削減し、CPU 使用率を 10% 削減し、フォアグラウンド スループットを約 5% 向上させ、特定の負荷の下でテールレイテンシーを 20% 削減できます。

    [ユーザー文書](/tikv-configuration-file.md#raft-engine) 、 [#95](https://github.com/tikv/raft-engine/issues/95)

-   結合順序のヒント構文をサポート

    -   `LEADING`ヒントは、指定された順序を結合操作のプレフィックスとして使用することをオプティマイザに思い出させます。結合の適切なプレフィックスは、結合の初期段階でデータ量をすばやく削減し、クエリのパフォーマンスを向上させることができます。
    -   `STRAIGHT_JOIN`ヒントは、 `FROM`句のテーブルの順序と一致する順序でテーブルを結合するようオプティマイザに通知します。

    これにより、テーブル結合の順序を修正する方法が提供されます。ヒントを適切に使用すると、SQL のパフォーマンスとクラスターの安定性を効果的に向上させることができます。

    ユーザー文書: [`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-) 、 [`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join) 、 [#29932](https://github.com/pingcap/tidb/issues/29932)

-   TiFlash はさらに 4 つの関数をサポートしています。

    -   `FROM_DAYS`
    -   `TO_DAYS`
    -   `TO_SECONDS`
    -   `WEEKOFYEAR`

    [ユーザー文書](/tiflash/tiflash-supported-pushdown-calculations.md) 、 [#4679](https://github.com/pingcap/tiflash/issues/4679) 、 [#4678](https://github.com/pingcap/tiflash/issues/4678) 、 [#4677](https://github.com/pingcap/tiflash/issues/4677)

-   TiFlash は、動的プルーニング モードで分割されたテーブルをサポートします。

    OLAP シナリオでのパフォーマンスを向上させるために、パーティション分割されたテーブルで動的プルーニング モードがサポートされています。 TiDB が v6.0.0 より前のバージョンからアップグレードされた場合、パフォーマンスを最大化するために、既存のパーティション分割されたテーブルの統計を手動で更新することをお勧めします (v6.1.0 へのアップグレード後に作成された新しいインストールまたは新しいパーティションには必要ありません)。

    ユーザー文書: [MPP モードで分割されたテーブルにアクセスする](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode) 、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) 、 [#3873](https://github.com/pingcap/tiflash/issues/3873)

### 安定性 {#stability}

-   SST 破損からの自動回復

    RocksDB がバックグラウンドで破損した SST ファイルを検出すると、TiKV は影響を受けるピアをスケジュールし、他のレプリカを使用してそのデータを回復しようとします。 `background-error-recovery-window`パラメータを使用して、リカバリの最大許容時間を設定できます。回復操作が時間枠内に完了しない場合、TiKV はpanicになります。この機能は、回復可能な損傷したstorageを自動的に検出して回復するため、クラスターの安定性が向上します。

    [ユーザー文書](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610) 、 [#10578](https://github.com/tikv/tikv/issues/10578)

-   非トランザクション DML ステートメントのサポート

    大規模なデータ処理のシナリオでは、大規模なトランザクションを含む単一の SQL ステートメントがクラスターの安定性とパフォーマンスに悪影響を及ぼす可能性があります。 v6.1.0 以降、TiDB は、バッチ処理のために`DELETE`のステートメントを複数のステートメントに分割する構文の提供をサポートしています。 split ステートメントは、トランザクションの原子性と分離性を損ないますが、クラスターの安定性を大幅に向上させます。詳細な構文については、 [`BATCH`](/sql-statements/sql-statement-batch.md)を参照してください。

    [ユーザー文書](/non-transactional-dml.md)

-   TiDB は最大 GC 待機時間の構成をサポートしています

    TiDB のトランザクションは、Multi-Version Concurrency Control (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。古いデータはガベージ コレクション (GC) タスクによって定期的にクリーンアップされます。これにより、storageスペースが再利用され、クラスターのパフォーマンスと安定性が向上します。デフォルトでは、GC は 10 分ごとにトリガーされます。長期実行トランザクションが対応する履歴データにアクセスできるようにするために、実行中のトランザクションがある場合、GC タスクは遅延されます。 GC タスクが無期限に遅延しないようにするために、TiDB はシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)を導入して GC タスクの最大遅延時間を制御します。最大遅延時間を超えると、GC が強制的に実行されます。変数のデフォルト値は 24 時間です。この機能により、GC 待機時間と実行時間の長いトランザクションとの関係を制御できるようになり、クラスターの安定性が向上します。

    [ユーザー文書](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

-   TiDB は、自動統計収集タスクの最大実行時間の構成をサポートしています

    データベースは、統計を収集することでデータの分布を効果的に把握できます。これにより、合理的な実行計画が生成され、SQL 実行の効率が向上します。 TiDB は、バックグラウンドで頻繁に変更されるデータ オブジェクトに関する統計を定期的に収集します。ただし、統計の収集はクラスターのリソースを占有し、ビジネスのピーク時にビジネスの安定した運用に影響を与える可能性があります。

    v6.1.0 から、TiDB は[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)を導入してバックグラウンド統計収集の最大実行時間を制御します。これはデフォルトで 12 時間です。アプリケーションでリソースのボトルネックが発生しない場合は、TiDB がタイムリーに統計を収集できるように、この変数を変更しないことをお勧めします。

    [ユーザー文書](/system-variables.md)

### 使いやすさ {#ease-of-use}

-   複数のレプリカが失われた場合のワンストップのオンライン データ リカバリをサポート

    TiDB v6.1.0 より前では、マシンの障害により複数のリージョンレプリカが失われた場合、ユーザーはすべての TiKV サーバーを停止し、 TiKV Controlを使用して TiKV を 1 つずつ回復する必要がありました。 TiDB v6.1.0 以降、リカバリ プロセスは完全に自動化されており、TiKV を停止する必要がなく、オンラインの他のアプリケーションに影響を与えません。 PD Controlを使用して回復プロセスを開始し、よりユーザーフレンドリーな概要情報を提供します。

    [ユーザー文書](/online-unsafe-recovery.md) 、 [#10483](https://github.com/tikv/tikv/issues/10483)

-   履歴統計収集タスクの表示をサポート

    `SHOW ANALYZE STATUS`ステートメントを使用して、クラスター レベルの統計収集タスクを表示できます。 TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンス レベルのタスクのみを表示し、履歴タスク レコードは TiDB の再起動後にクリアされます。したがって、履歴統計の収集時間と詳細を表示することはできません。 TiDB v6.1.0 以降では、統計収集タスクの履歴レコードが保持され、クラスターの再起動後にクエリを実行できます。これは、統計の異常によって引き起こされるクエリ パフォーマンスの問題をトラブルシューティングするためのリファレンスを提供します。

    [ユーザー文書](/sql-statements/sql-statement-show-analyze-status.md)

-   TiDB、TiKV、およびTiFlash構成の動的な変更をサポート

    以前のバージョンの TiDB では、構成アイテムを変更した後、クラスターを再起動して変更を有効にする必要がありました。これにより、オンライン サービスが中断される場合があります。この問題に対処するために、TiDB v6.1.0 では動的構成機能が導入されています。これにより、クラスターを再起動せずにパラメーターの変更を検証できます。具体的な最適化は次のとおりです。

    -   一部の TiDB 構成項目をシステム変数に変換して、動的に変更して永続化できるようにします。元の構成アイテムは、変換後に非推奨になることに注意してください。変換された構成アイテムの詳細なリストについては、 [コンフィグレーションファイルのパラメーター](#configuration-file-parameters)を参照してください。
    -   一部の TiKV パラメータのオンライン設定をサポートします。パラメータの詳細なリストについては、 [その他](#others)を参照してください。
    -   TiFlash構成項目`max_threads`をシステム変数`tidb_max_tiflash_threads`に変換して、構成を動的に変更して永続化できるようにします。変換後も元の構成アイテムが残ることに注意してください。

    以前のバージョンからアップグレードされた v6.1.0 クラスター (オンラインおよびオフライン アップグレードを含む) については、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成項目が既に存在する場合、TiDB はアップグレード プロセス中に、構成された項目の値を対応するシステム変数の値に自動的に更新します。このように、アップグレード後、システムの動作はパラメーターの最適化の影響を受けません。
    -   上記の自動更新は、アップグレード中に 1 回だけ実行されます。アップグレード後、非推奨の構成アイテムは有効ではなくなります。

    この機能を使用すると、システムを再起動してサービスを中断する代わりに、パラメーターを動的に変更し、それらを検証して永続化できます。これにより、日常のメンテナンスが容易になります。

    [ユーザー文書](/dynamic-config.md)

-   クエリまたは接続の強制終了をグローバルにサポート

    `enable-global-kill`構成 (デフォルトで有効) を使用してグローバルキル機能を制御できます。

    TiDB v6.1.0 より前では、操作が大量のリソースを消費し、クラスターの安定性の問題を引き起こす場合、ターゲットの TiDB インスタンスに接続してから、 `KILL TIDB ${id};`コマンドを実行してターゲットの接続と操作を終了する必要があります。多くの TiDB インスタンスの場合、この方法は使いにくく、操作を誤る傾向があります。 v6.1.0 以降、 `enable-global-kill`構成が導入され、デフォルトで有効になります。クライアントと TiDB の間にプロキシがある場合、誤って他のクエリやセッションを誤って終了することを心配することなく、任意の TiDB インスタンスで kill コマンドを実行して、指定された接続と操作を終了できます。現在、TiDB は Ctrl+C を使用したクエリまたはセッションの終了をサポートしていません。

    [ユーザー文書](/tidb-configuration-file.md#enable-global-kill-new-in-v610) 、 [#8854](https://github.com/pingcap/tidb/issues/8854)

-   TiKV API V2 (実験的)

    v6.1.0 より前では、TiKV が未加工のキー値storageとして使用される場合、TiKV はクライアントから渡された未加工データのみを保存するため、基本的なキー値の読み取りおよび書き込み機能のみを提供します。

    TiKV API V2 は、次のような新しい Raw Key Valuestorage形式とアクセス インターフェイスを提供します。

    -   データは MVCC に保存され、データの変更タイムスタンプが記録されます。この機能は、変更データ キャプチャと増分バックアップおよび復元を実装するための基盤を築きます。
    -   データはさまざまな用途に応じてスコープが設定され、単一の TiDB クラスター、トランザクション KV、RawKV アプリケーションの共存がサポートされます。

    <Warning>基本的なstorage形式が大幅に変更されたため、API V2 を有効にした後、TiKV クラスターを v6.1.0 より前のバージョンにロールバックすることはできません。 TiKV をダウングレードすると、データが破損する可能性があります。</Warning>

    [ユーザー文書](/tikv-configuration-file.md#api-version-new-in-v610) 、 [#11745](https://github.com/tikv/tikv/issues/11745)

### MySQL の互換性 {#mysql-compatibility}

-   MySQL によるユーザーレベルのロック管理との互換性をサポート

    ユーザーレベルのロックは、MySQL が組み込み関数を通じて提供する、ユーザーが名前を付けたロック管理システムです。ロック関数は、ロックのブロック、待機、およびその他のロック管理機能を提供できます。ユーザーレベルのロックは、Rails、Elixir、Ecto などの ORM フレームワークでも広く使用されています。 v6.1.0 以降、TiDB は MySQL と互換性のあるユーザーレベルのロック管理をサポートしており、 `GET_LOCK` `RELEASE_LOCK`および`RELEASE_ALL_LOCKS`関数をサポートしています。

    [ユーザー文書](/functions-and-operators/locking-functions.md) 、 [#14994](https://github.com/pingcap/tidb/issues/14994)

### データ移行 {#data-migration}

-   シャード テーブルをマージおよび移行するための楽観的モードが GA になる

    DM は、楽観的モードでシャード テーブルからデータをマージおよび移行するタスクの多数のシナリオ テストを追加します。これは、毎日の使用シナリオの 90% をカバーします。悲観的モードと比較して、楽観的モードはよりシンプルで効率的に使用できます。使用上の注意をよく理解してから、できれば楽観的モードを使用することをお勧めします。

    [ユーザー文書](/dm/feature-shard-merge-optimistic.md#restrictions)

-   DM WebUI は、指定されたパラメーターに従ってタスクを開始することをサポートします

    移行タスクを開始するときに、開始時刻とセーフ モード期間を指定できます。これは、多数のソースを含む増分移行タスクを作成する場合に特に役立ち、ソースごとにbinlogの開始位置を指定する必要がなくなります。

    [ユーザー文書](/dm/dm-webui-guide.md) 、 [#5442](https://github.com/pingcap/tiflow/issues/5442)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiDB は、さまざまなサードパーティ データ エコシステムとのデータ共有をサポートしています

    -   TiCDC は TiDB の増分データを Avro 形式で Kafka に送信することをサポートしており、Confluent を介して KSQL や Snowflake などのサードパーティとデータを共有できます。

        [ユーザー文書](/ticdc/ticdc-avro-protocol.md) 、 [#5338](https://github.com/pingcap/tiflow/issues/5338)

    -   TiCDC は、テーブルによる TiDB からの増分データのさまざまな Kafka トピックへのディスパッチをサポートします。これを Canal-json 形式と組み合わせることで、Flink と直接データを共有できます。

        [ユーザー文書](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink) 、 [#4423](https://github.com/pingcap/tiflow/issues/4423)

    -   TiCDC は SASL GSSAPI 認証タイプをサポートし、Kafka を使用した SASL 認証の例を追加します。

        [ユーザー文書](/ticdc/ticdc-sink-to-kafka.md#ticdc-uses-the-authentication-and-authorization-of-kafka) 、 [#4423](https://github.com/pingcap/tiflow/issues/4423)

-   TiCDC は`charset=GBK`テーブルの複製をサポートしています。

    [ユーザー文書](/character-set-gbk.md#component-compatibility) 、 [#4806](https://github.com/pingcap/tiflow/issues/4806)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                           | タイプを変更 | 説明                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                    | 修正済み   | デフォルト値が`OFF`から`ON`に変更されました。                                                                                                                               |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                           | 修正済み   | この変数は GLOBAL スコープを追加し、変数値はクラスターに保持されます。                                                                                                                   |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)                                                       | 修正済み   | 変数のスコープが INSTANCE から GLOBAL に変更されます。変数値はクラスターに保持され、値の範囲は`[0, 1073741824]`に変更されます。                                                                         |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)                                       | 新規追加   | この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                       |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)                                   | 新規追加   | この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                       |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                       | 新規追加   | この設定は以前は`tidb.toml`オプション ( `run-auto-analyze` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                                        |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)       | 新規追加   | この変数は、TiDB が`ONLY_FULL_GOUP_BY`チェックを実行するときの動作を制御します。                                                                                                      |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                           | 新規追加   | v6.1.0 以降、TiDB の結合したテーブルの再配置アルゴリズムは Outer Join をサポートしています。この変数はサポートの動作を制御し、デフォルト値は`ON`です。                                                                 |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                         | 新規追加   | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                             |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)                                             | 新規追加   | この変数は、コミットされていないトランザクションによってブロックされる GC セーフ ポイントの最大時間を設定するために使用されます。                                                                                       |
| [tidb_max_auto_analyze_time](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                                     | 新規追加   | この変数は、auto analyzeの最大実行時間を指定するために使用されます。                                                                                                                  |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)                                       | 新規追加   | この変数は、 TiFlash がリクエストを実行する最大同時実行数を設定するために使用されます。                                                                                                          |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)                                                 | 新規追加   | この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                                              |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)                                           | 新規追加   | この変数は、TiDB が統計を更新するときの最大メモリ使用量を制御します。これには、ユーザーが手動で実行する[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)タスクや、TiDB バックグラウンドでの自動分析タスクが含まれます。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)                   | 新規追加   | この変数は、非トランザクション DML ステートメントでエラーが発生したときに、すぐにエラーを返すかどうかを指定します。                                                                                              |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-new-in-v610) | 新規追加   | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                  |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                             | 新規追加   | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 からシステム変数に変更されました。                                                            |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)                                   | 新規追加   | この変数は、TiDB 統計キャッシュのメモリクォータを設定します。                                                                                                                         |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                             | タイプを変更 | 説明                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `committer-concurrency`                                                                                                                                                                                | 削除しました | システム変数`tidb_committer_concurrency`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                       |
| TiDB           | `lower-case-table-names`                                                                                                                                                                               | 削除しました | 現在、TiDB は`lower_case_table_name=2`のみをサポートしています。別の値が設定されている場合、クラスターが v6.1.0 にアップグレードされた後、値は失われます。                                                         |
| TiDB           | `mem-quota-query`                                                                                                                                                                                      | 削除しました | システム変数`tidb_mem_quota_query`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                             |
| TiDB           | `oom-action`                                                                                                                                                                                           | 削除しました | システム変数`tidb_mem_oom_action`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                              |
| TiDB           | `prepared-plan-cache.capacity`                                                                                                                                                                         | 削除しました | システム変数`tidb_prepared_plan_cache_size`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                    |
| TiDB           | `prepared-plan-cache.enabled`                                                                                                                                                                          | 削除しました | システム変数`tidb_enable_prepared_plan_cache`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                  |
| TiDB           | `query-log-max-len`                                                                                                                                                                                    | 削除しました | システム変数`tidb_query_log_max_len`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                           |
| TiDB           | `require-secure-transport`                                                                                                                                                                             | 削除しました | システム変数`require_secure_transport`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                         |
| TiDB           | `run-auto-analyze`                                                                                                                                                                                     | 削除しました | システム変数`tidb_enable_auto_analyze`に置き換えられます。この構成アイテムは有効ではなくなりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                         |
| TiDB           | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)                                                                                                                     | 新規追加   | Global Kill (インスタンス間のクエリまたは接続の終了) 機能を有効にするかどうかを制御します。値が`true`の場合、 `KILL`と`KILL TIDB`ステートメントの両方がインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続を誤って終了することを心配する必要はありません。 |
| TiDB           | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                                                                                 | 新規追加   | 統計キャッシュのメモリクォータを有効にするかどうかを制御します。                                                                                                                         |
| TiKV           | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1)                                                                                                                                           | 修正済み   | デフォルト値が`FALSE`から`TRUE`に変更されました。                                                                                                                          |
| TiKV           | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys)                                                                                                                                       | 修正済み   | デフォルト値が 1440000 から`region-split-keys / 2 * 3`に変更されました。                                                                                                   |
| TiKV           | [`region-max-size`](/tikv-configuration-file.md#region-max-size)                                                                                                                                       | 修正済み   | デフォルト値が 144 MB から`region-split-size / 2 * 3`に変更されました。                                                                                                    |
| TiKV           | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)                                                                                                     | 新規追加   | リージョン をバケットと呼ばれる小さな範囲に分割するかどうかを決定します。                                                                                                                    |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                                                                         | 新規追加   | `enable-region-bucket`が true の場合のバケットのサイズ。                                                                                                               |
| TiKV           | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size)                                                                                                                   | 新規追加   | ローカルにキャッシュされたタイムスタンプの最小数。                                                                                                                                |
| TiKV           | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval)                                                                                                                               | 新規追加   | ローカルにキャッシュされたタイムスタンプが更新される間隔。                                                                                                                            |
| TiKV           | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-new-in-v610)                                                                                                     | 新規追加   | スナップショット ファイルのサイズがこの値を超えると、スナップショット ファイルは複数のファイルに分割されます。                                                                                                 |
| TiKV           | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit)                                                                                                                                 | 新規追加   | Raft Engineのメモリ使用量の制限を指定します。                                                                                                                             |
| TiKV           | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610)                                                                                 | 新規追加   | RocksDB が回復可能なバックグラウンド エラーを検出した後、最大回復時間が許可されます。                                                                                                          |
| TiKV           | [`storage.api-version`](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                           | 新規追加   | TiKV が未加工のキー値ストアとして機能するときに TiKV によって使用されるstorage形式とインターフェイス バージョン。                                                                                       |
| PD             | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-new-in-v610)                                                                                                  | 新規追加   | ストアがオンラインになるまでの最大待機時間を制御します。                                                                                                                             |
| TiCDC          | [`enable-tls`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                             | 新規追加   | TLS を使用してダウンストリームの Kafka インスタンスに接続するかどうか。                                                                                                                |
| TiCDC          | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新規追加   | Kafka の SASL/GSSAPI 認証をサポートするために使用されます。詳細については、 [`kafka`でシンク URI を構成する](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)を参照してください。            |
| TiCDC          | [`avro-decimal-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)      | 新規追加   | Avro 形式の出力の詳細を決定します。                                                                                                                                     |
| TiCDC          | [`dispatchers.topic`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                             | 新規追加   | TiCDC が増分データをさまざまな Kafka トピックにディスパッチする方法を制御します。                                                                                                          |
| TiCDC          | [`dispatchers.partition`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                         | 新規追加   | `dispatchers.partition`は`dispatchers.dispatcher`のエイリアスです。 TiCDC が増分データを Kafka パーティションにディスパッチする方法を制御します。                                                  |
| TiCDC          | [`schema-registry`](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-kafka-connect-confluent-platform)                                                                                               | 新規追加   | Avro スキーマを格納するスキーマ レジストリ エンドポイントを指定します。                                                                                                                  |
| DM             | `dmctl start-relay`コマンドで`worker`                                                                                                                                                                       | 削除しました | このパラメーターの使用はお勧めしません。より簡単な実装を提供します。                                                                                                                       |
| DM             | ソース構成ファイルの`relay-dir`                                                                                                                                                                                  | 削除しました | ワーカー構成ファイル内の同じ構成アイテムに置き換えられます。                                                                                                                           |
| DM             | タスク構成ファイルの`is-sharding`                                                                                                                                                                                | 削除しました | `shard-mode`の構成アイテムに置き換えられます。                                                                                                                            |
| DM             | タスク構成ファイルの`auto-fix-gtid`                                                                                                                                                                              | 削除しました | v5.x で廃止され、v6.1.0 で正式に削除されました。                                                                                                                           |
| DM             | ソース構成ファイルの`meta-dir`と`charset`                                                                                                                                                                         | 削除しました | v5.x で廃止され、v6.1.0 で正式に削除されました。                                                                                                                           |

### その他 {#others}

-   デフォルトでプリペアドプランキャッシュを有効にする

    新しいクラスターでは、 `Prepare` / `Execute`リクエストの実行プランをキャッシュするために、プリペアドプランキャッシュ がデフォルトで有効になっています。その後の実行では、クエリ プランの最適化をスキップできるため、パフォーマンスが向上します。アップグレードされたクラスターは、構成ファイルから構成を継承します。新しいクラスターは新しいデフォルト値を使用します。つまり、 プリペアドプランキャッシュ はデフォルトで有効になっており、各セッションは最大 100 個のプランをキャッシュできます ( `capacity=100` )。この機能のメモリ消費量については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)を参照してください。

-   TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`インスタンス レベルのタスクを示し、タスク レコードは TiDB の再起動後にクリアされます。 TiDB v6.1.0 以降、 `SHOW ANALYZE STATUS`クラスター レベルのタスクを示し、タスク レコードは再起動後も保持されます。 `tidb_analyze_version = 2`の場合、 `Job_info`列は`analyze option`情報を追加します。

-   TiKV 内の SST ファイルが破損していると、TiKV プロセスがpanicに陥る可能性があります。 TiDB v6.1.0 より前では、SST ファイルが破損していると、TiKV がすぐにpanicに陥りました。 TiDB v6.1.0 以降、SST ファイルが破損してから 1 時間後に TiKV プロセスがpanicになります。

-   次の TiKV 構成アイテムは[値を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)をサポートします。

    -   `raftstore.raft-entry-max-size`
    -   `quota.foreground-cpu-time`
    -   `quota.foreground-write-bandwidth`
    -   `quota.foreground-read-bandwidth`
    -   `quota.max-delay-duration`
    -   `server.grpc-memory-pool-quota`
    -   `server.max-grpc-send-msg-len`
    -   `server.raft-msg-max-batch-size`

-   v6.1.0 では、一部の構成ファイル パラメータがシステム変数に変換されます。以前のバージョンからアップグレードされた v6.1.0 クラスター (オンラインおよびオフライン アップグレードを含む) については、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成項目が既に存在する場合、TiDB はアップグレード プロセス中に、構成された項目の値を対応するシステム変数の値に自動的に更新します。このように、アップグレード後、パラメーターの最適化により、システムの動作は変わりません。
    -   上記の自動更新は、アップグレード中に 1 回だけ実行されます。アップグレード後、非推奨の構成アイテムは有効ではなくなります。

-   ダッシュボード ページはDM WebUIから削除されました。

-   `dispatchers.topic`と`dispatchers.partition`が有効になっている場合、TiCDC を v6.1.0 より前のバージョンにダウングレードすることはできません。

-   Avro プロトコルを使用するTiCDC Changefeed は、 v6.1.0 より前のバージョンにダウングレードできません。

## 改良点 {#improvements}

-   TiDB

    -   `UnionScanRead`オペレーターのパフォーマンスを向上させる[#32433](https://github.com/pingcap/tidb/issues/32433)
    -   `EXPLAIN`の出力におけるタスク タイプの表示を改善 (MPP タスク タイプを追加) [#33332](https://github.com/pingcap/tidb/issues/33332)
    -   列[#10377](https://github.com/pingcap/tidb/issues/10377)のデフォルト値として`rand()`を使用するサポート
    -   列[#33870](https://github.com/pingcap/tidb/issues/33870)のデフォルト値として`uuid()`を使用するサポート
    -   列の文字セットの`latin1`から`utf8` / `utf8mb4`への変更をサポート[#34008](https://github.com/pingcap/tidb/issues/34008)

-   TiKV

    -   インメモリ悲観的ロック[#12279](https://github.com/tikv/tikv/issues/12279)を使用する場合の CDC の古い値のヒット率を改善する
    -   TiKV クライアントがリージョンキャッシュを時間[#12398](https://github.com/tikv/tikv/issues/12398)に更新できるように、ヘルス チェックを改善して利用できないRaftstoreを検出します。
    -   Raft Engine [#12255](https://github.com/tikv/tikv/issues/12255)でのメモリ制限の設定をサポート
    -   TiKV は破損した SST ファイルを自動的に検出して削除し、製品の可用性を向上させます[#10578](https://github.com/tikv/tikv/issues/10578)
    -   CDC は RawKV [#11965](https://github.com/tikv/tikv/issues/11965)をサポート
    -   大きなスナップショット ファイルを複数のファイルに分割するサポート[#11595](https://github.com/tikv/tikv/issues/11595)
    -   スナップショットガベージコレクションをRaftstoreからバックグラウンド スレッドに移動して、スナップショット GC がRaftstoreメッセージ ループをブロックしないようにする[#11966](https://github.com/tikv/tikv/issues/11966)
    -   最大メッセージ長 ( `max-grpc-send-msg-len` ) と gPRC メッセージの最大バッチ サイズ ( `raft-msg-max-batch-size` ) の動的設定をサポート[#12334](https://github.com/tikv/tikv/issues/12334)
    -   Raft [#10483](https://github.com/tikv/tikv/issues/10483)によるオンラインの安全でない復元計画の実行をサポート

-   PD
    -   リージョン ラベルの有効期限 (TTL) をサポート[#4694](https://github.com/tikv/pd/issues/4694)
    -   サポートリージョンバケット[#4668](https://github.com/tikv/pd/issues/4668)
    -   デフォルトでswaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

-   TiFlash

    -   マージ フェーズ[#4451](https://github.com/pingcap/tiflash/issues/4451)でより効率的なアルゴリズムが使用されるように、集計演算子のメモリ計算を最適化します。

-   ツール

    -   バックアップと復元 (BR)

        -   空のデータベースのバックアップと復元のサポート[#33866](https://github.com/pingcap/tidb/issues/33866)

    -   TiDB Lightning

        -   分散リージョンをバッチ モードに最適化して、分散リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   TiCDC は、レプリケーション中の大規模なトランザクションの分割をサポートしています。これにより、大規模なトランザクションによって引き起こされるレプリケーションのレイテンシーが大幅に削減されます[#5280](https://github.com/pingcap/tiflow/issues/5280)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `in`関数が`bit`タイプのデータ[#33070](https://github.com/pingcap/tidb/issues/33070)を処理するときに発生する可能性があるpanicの問題を修正します。
    -   `UnionScan`演算子が順序[#33175](https://github.com/pingcap/tidb/issues/33175)を維持できないため、間違ったクエリ結果が返される問題を修正します。
    -   Merge Join 演算子が特定のケースで間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   動的枝刈りモード[#33231](https://github.com/pingcap/tidb/issues/33231)で`index join`の結果がおかしくなることがある問題を修正
    -   パーティションテーブルの一部のパーティションが削除されると、データがガベージ コレクションされない可能性がある問題を修正します[#33620](https://github.com/pingcap/tidb/issues/33620)
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリすると、TiDBサーバーがメモリ不足になることがある問題を修正します。この問題は、Grafana ダッシュボードでスロー クエリを確認すると発生する可能性があります[#33893](https://github.com/pingcap/tidb/issues/33893)
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[#31422](https://github.com/pingcap/tidb/issues/31422)
    -   TopSQL モジュールのメモリリークの問題を修正する[#34525](https://github.com/pingcap/tidb/issues/34525) [#34502](https://github.com/pingcap/tidb/issues/34502)
    -   PointGet プラン[#32371](https://github.com/pingcap/tidb/issues/32371)でプラン キャッシュが間違っている可能性がある問題を修正します。
    -   Plan Cache を RC 分離レベル[#34447](https://github.com/pingcap/tidb/issues/34447)で開始すると、クエリの結果が正しくない場合がある問題を修正します。

-   TiKV

    -   TiKV インスタンスがオフラインになるとRaftログのラグが増加する問題を修正します[#12161](https://github.com/tikv/tikv/issues/12161)
    -   マージする対象のリージョンが無効であるため、TiKV が予期せずパニックになり、ピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   v5.3.1 または v5.4.0 から v6.0.0 以降のバージョンにアップグレードすると、TiKV が`failed to load_latest_options`エラーを報告する問題を修正します[#12269](https://github.com/tikv/tikv/issues/12269)
    -   メモリリソースが不足している場合にRaftログを追加することによって引き起こされる OOM の問題を修正します[#11379](https://github.com/tikv/tikv/issues/11379)
    -   ピアの破棄とリージョン[#12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   `stats_monitor`デッド ループに陥った後、短時間で TiKV のメモリ使用量が急増する問題を修正します[#12416](https://github.com/tikv/tikv/issues/12416)
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)の使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正

-   PD

    -   `not leader` [#4797](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   一部のまれなケースでの TSO フォールバックのバグを修正します[#4884](https://github.com/tikv/pd/issues/4884)
    -   PDリーダーの転送後、削除されたトゥームストーンストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   PD リーダーの転送[#4769](https://github.com/tikv/pd/issues/4769)の直後にスケジュールを開始できない問題を修正します。

-   TiDB ダッシュボード

    -   Top SQL機能が有効になる前に実行されていた SQL ステートメントの CPU オーバーヘッドをTop SQL SQL が収集できないというバグを修正します[#33859](https://github.com/pingcap/tidb/issues/33859)

-   TiFlash

    -   多数の INSERT 操作と DELETE 操作の後に発生する可能性のあるデータの不整合を修正します[#4956](https://github.com/pingcap/tiflash/issues/4956)

-   ツール

    -   TiCDC

        -   DDL スキーマがバッファリングされる方法を最適化することにより、過剰なメモリ使用量を修正します[#1386](https://github.com/pingcap/tiflow/issues/1386)
        -   特別な増分スキャン シナリオで発生するデータ損失を修正します[#5468](https://github.com/pingcap/tiflow/issues/5468)

    -   TiDB データ移行 (DM)

        -   `start-time`タイム ゾーンの問題を修正し、DM の動作をダウンストリーム タイム ゾーンの使用からアップストリーム タイム ゾーンの使用に変更します[#5271](https://github.com/pingcap/tiflow/issues/5471)
        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正します[#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        -   チェックポイントのフラッシュにより、失敗した行のデータがスキップされる可能性がある問題を修正します[#5279](https://github.com/pingcap/tiflow/issues/5279)
        -   フィルタリングされた DDL をダウンストリームで手動で実行すると、タスクの再開に失敗する場合があるという問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `case-sensitive: true`が設定されていない場合に大文字のテーブルが複製されない問題を修正します[#5255](https://github.com/pingcap/tiflow/issues/5255)
        -   主キーが`SHOW CREATE TABLE`ステートメントによって返されるインデックスの先頭にない場合に発生する DM ワーカーpanicの問題を修正します[#5159](https://github.com/pingcap/tiflow/issues/5159)
        -   GTID有効時やタスク自動再開時にCPU使用率が上昇し、大量のログが出力されることがある問題を修正[#5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM WebUI [#4993](https://github.com/pingcap/tiflow/issues/4993)のオフライン オプションとその他の使用上の問題を修正します。
        -   アップストリーム[#3731](https://github.com/pingcap/tiflow/issues/3731)で GTID が空の場合、インクリメンタル タスクの開始に失敗する問題を修正します。
        -   空の構成により dm-master がpanicになる可能性がある問題を修正します[#3732](https://github.com/pingcap/tiflow/issues/3732)

    -   TiDB Lightning

        -   事前チェックでローカル ディスク リソースとクラスタの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)
        -   スキーマ[#33381](https://github.com/pingcap/tidb/issues/33381)の不適切なルーティングの問題を修正します。
        -   TiDB Lightningパニック時に PD 構成が正しく復元されない問題を修正[#31733](https://github.com/pingcap/tidb/issues/31733)
        -   `auto_increment`列[#29737](https://github.com/pingcap/tidb/issues/27937)の範囲外のデータが原因でローカル バックエンドのインポートが失敗する問題を修正します。
        -   `auto_random`または`auto_increment`列が null [#34208](https://github.com/pingcap/tidb/issues/34208)の場合にローカル バックエンドのインポートが失敗する問題を修正します。

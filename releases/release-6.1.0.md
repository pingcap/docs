---
title: TiDB 6.1.0 Release Notes
summary: Learn about the new features, compatibility changes, improvements, and bug fixes in TiDB 6.1.0.
---

# TiDB 6.1.0 リリースノート {#tidb-6-1-0-release-notes}

発売日：2022年6月13日

TiDB バージョン: 6.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.1.0#version-list)

6.1.0 の主な新機能または改善点は次のとおりです。

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になり、 MySQL 5.7と互換性があります。
-   TiFlashパーティションテーブル(動的プルーニング) が GA になりました
-   ユーザーレベルのロック管理をサポートし、MySQL と互換性があります。
-   非トランザクション DML ステートメントのサポート ( `DELETE`のみサポート)
-   TiFlash はオンデマンドのデータ圧縮をサポートします
-   MPP はウィンドウ関数フレームワークを導入します
-   TiCDC は、Avro を介した Kafka への変更ログのレプリケートをサポートします
-   TiCDC は、レプリケーション中の大規模なトランザクションの分割をサポートしており、大規模なトランザクションによって引き起こされるレプリケーションのレイテンシーを大幅に削減します。
-   シャードテーブルのマージおよび移行の楽観的モードが GA になりました

## 新機能 {#new-features}

### SQL {#sql}

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になりました。どちらもMySQL 5.7と互換性があります。

    ユーザードキュメント: [List パーティショニング](/partitioned-table.md#list-partitioning) 、 [List COLUMNS パーティショニング](/partitioned-table.md#list-columns-partitioning)

-   TiFlash は、コンパクト コマンドの開始をサポートしています。 (実験的)

    TiFlash v6.1.0 では、既存のバックグラウンド圧縮メカニズムに基づいて物理データを手動で圧縮する方法を提供する`ALTER TABLE ... COMPACT`ステートメントが導入されています。このステートメントを使用すると、必要に応じていつでも以前の形式でデータを更新し、読み取り/書き込みのパフォーマンスを向上させることができます。クラスターを v6.1.0 にアップグレードした後、このステートメントを実行してデータを圧縮することをお勧めします。このステートメントは標準 SQL 構文の拡張であるため、MySQL クライアントと互換性があります。 TiFlashアップグレード以外のシナリオでは、通常、このステートメントを使用する必要はありません。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md) [#4145](https://github.com/pingcap/tiflash/issues/4145)

-   TiFlash はウィンドウ関数フレームワークを実装し、次のウィンドウ関数をサポートします。

    -   `RANK()`
    -   `DENSE_RANK()`
    -   `ROW_NUMBER()`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [#33072](https://github.com/pingcap/tidb/issues/33072)

### 可観測性 {#observability}

-   継続的プロファイリングは、ARMアーキテクチャとTiFlashをサポートします。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

-   Grafana は、パフォーマンス概要ダッシュボードを追加して、全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。

    TiDB 視覚化モニタリングコンポーネントGrafana の新しいダッシュボードとして、パフォーマンス概要は、全体的なパフォーマンス診断のためのシステム レベルのエントリを提供します。トップダウンのパフォーマンス分析手法に従って、パフォーマンス概要ダッシュボードは、データベース時間の内訳に基づいて TiDB パフォーマンス メトリックを再編成し、これらのメトリックをさまざまな色で表示します。これらの色を確認することで、システム全体の性能ボトルネックを一目で特定することができ、性能診断時間を大幅に短縮し、性能解析と診断を簡素化します。

    [ユーザードキュメント](/performance-tuning-overview.md)

### パフォーマンス {#performance}

-   カスタマイズされたリージョンサイズのサポート (実験的)

    リージョンをより大きなサイズに設定すると、リージョンの数が効果的に減り、リージョンの管理が容易になり、クラスターのパフォーマンスと安定性が向上します。この機能では、リージョン内のより小さな範囲であるバケットの概念が導入されます。リージョンがより大きなサイズに設定されている場合、クエリ単位としてバケットを使用すると、同時クエリのパフォーマンスを最適化できます。バケットをクエリ単位として使用すると、ホット リージョンのサイズを動的に調整して、スケジューリングの効率と負荷バランスを確保することもできます。この機能は現在実験的です。本番環境での使用はお勧めできません。

    [ユーザードキュメント](/tune-region-performance.md) [#11515](https://github.com/tikv/tikv/issues/11515)

-   Raft Engine をデフォルトのログstorageエンジンとして使用する

    v6.1.0 以降、TiDB はログのデフォルトのstorageエンジンとしてRaft Engineを使用します。 RocksDB と比較して、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40% 削減し、CPU 使用率を 10% 削減すると同時に、特定の負荷の下でフォアグラウンドレイテンシーを約 5% 向上させ、テール レイテンシーを 20% 削減します。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine) [#95](https://github.com/tikv/raft-engine/issues/95)

-   結合順序ヒント構文のサポート

    -   `LEADING`ヒントは、指定された順序を結合操作のプレフィックスとして使用することをオプティマイザーに思い出させます。結合の適切なプレフィックスを使用すると、結合の初期段階でデータ量がすぐに削減され、クエリのパフォーマンスが向上します。
    -   `STRAIGHT_JOIN`ヒントは、オプティマイザに対し、 `FROM`節のテーブルの順序と一致する順序でテーブルを結合するように指示します。

    これにより、テーブル結合の順序を修正する方法が提供されます。ヒントを適切に使用すると、SQL のパフォーマンスとクラスターの安定性を効果的に向上させることができます。

    ユーザードキュメント: [`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-) 、 [`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join) 、 [#29932](https://github.com/pingcap/tidb/issues/29932)

-   TiFlash はさらに 4 つの関数をサポートします。

    -   `FROM_DAYS`
    -   `TO_DAYS`
    -   `TO_SECONDS`
    -   `WEEKOFYEAR`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [#4679](https://github.com/pingcap/tiflash/issues/4679) [#4678](https://github.com/pingcap/tiflash/issues/4678) [#4677](https://github.com/pingcap/tiflash/issues/4677)

-   TiFlash は、動的プルーニング モードでパーティション化されたテーブルをサポートします。

    OLAP シナリオのパフォーマンスを向上させるために、パーティション テーブルに対して動的プルーニング モードがサポートされています。 TiDB が v6.0.0 より前のバージョンからアップグレードされている場合は、パフォーマンスを最大化するために、既存のパーティション化されたテーブルの統計を手動で更新することをお勧めします (新規インストールまたは v6.1.0 へのアップグレード後に作成された新しいパーティションの場合は必要ありません)。

    ユーザードキュメント: [MPP モードでパーティション化されたテーブルにアクセスする](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode) 、 [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) 、 [#3873](https://github.com/pingcap/tiflash/issues/3873)

### 安定性 {#stability}

-   SST破損からの自動回復

    RocksDB がバックグラウンドで破損した SST ファイルを検出すると、TiKV は影響を受けるピアをスケジュールし、他のレプリカを使用してそのデータを回復しようとします。 `background-error-recovery-window`パラメータを使用して、回復の最大許容時間を設定できます。回復操作が時間枠内に完了しない場合、TiKV はpanicになります。この機能は、回復可能な破損したstorageを自動的に検出して回復するため、クラスターの安定性が向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610) [#10578](https://github.com/tikv/tikv/issues/10578)

-   非トランザクション DML ステートメントのサポート

    大規模なデータ処理のシナリオでは、大規模なトランザクションを含む 1 つの SQL ステートメントがクラスターの安定性とパフォーマンスに悪影響を与える可能性があります。 v6.1.0 以降、TiDB はバッチ処理用に`DELETE`のステートメントを複数のステートメントに分割する構文の提供をサポートしています。分割ステートメントはトランザクションの原子性と分離性を損ないますが、クラスターの安定性は大幅に向上します。詳細な構文については、 [`BATCH`](/sql-statements/sql-statement-batch.md)を参照してください。

    [ユーザードキュメント](/non-transactional-dml.md)

-   TiDB は最大 GC 待機時間の構成をサポートします

    TiDB のトランザクションは、Multi-Version Concurrency Control (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが保存されます。古いデータはガベージ コレクション (GC) タスクによって定期的にクリーンアップされ、storage領域を再利用してクラスターのパフォーマンスと安定性を向上させるのに役立ちます。 GC はデフォルトで 10 分ごとにトリガーされます。長時間実行されるトランザクションが対応する履歴データにアクセスできるようにするために、実行中のトランザクションがある場合、GC タスクは遅延されます。 GC タスクが無期限に遅延しないようにするために、TiDB ではシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)を導入して GC タスクの最大遅延時間を制御します。最大遅延時間を超えると強制的に GC が実行されます。変数のデフォルト値は 24 時間です。この機能により、GC 待機時間と長時間実行トランザクションとの関係を制御できるようになり、クラスターの安定性が向上します。

    [ユーザードキュメント](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

-   TiDB は、自動統計収集タスクの最大実行時間の構成をサポートします。

    データベースは統計を収集することでデータの分布を効果的に把握できるため、合理的な実行計画を生成し、SQL 実行の効率を向上させることができます。 TiDB は、頻繁に変更されるデータ オブジェクトに関する統計をバックグラウンドで定期的に収集します。ただし、統計の収集にはクラスターのリソースが消費されるため、ビジネスのピーク時のビジネスの安定した運用に影響を与える可能性があります。

    v6.1.0 以降、TiDB ではバックグラウンド統計収集の最大実行時間を制御するために[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)導入されており、デフォルトでは 12 時間です。アプリケーションでリソースのボトルネックが発生していない場合は、TiDB がタイムリーに統計を収集できるように、この変数を変更しないことをお勧めします。

    [ユーザードキュメント](/system-variables.md)

### 使いやすさ {#ease-of-use}

-   複数のレプリカが失われた場合のワンストップのオンラインデータリカバリをサポート

    TiDB v6.1.0 より前は、マシンの障害により複数のリージョンレプリカが失われた場合、ユーザーはすべての TiKV サーバーを停止し、 TiKV Controlを使用して TiKV を 1 つずつ復元する必要がありました。 TiDB v6.1.0 以降、リカバリ プロセスは完全に自動化されており、TiKV を停止する必要がなく、オンラインの他のアプリケーションにも影響を与えません。回復プロセスはPD Controlを使用してトリガーでき、よりユーザーフレンドリーな概要情報を提供します。

    [ユーザードキュメント](/online-unsafe-recovery.md) [#10483](https://github.com/tikv/tikv/issues/10483)

-   履歴統計収集タスクの表示をサポート

    `SHOW ANALYZE STATUS`ステートメントを使用すると、クラスターレベルの統計収集タスクを表示できます。 TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントにはインスタンス レベルのタスクのみが表示され、履歴タスク レコードは TiDB の再起動後にクリアされます。したがって、履歴統計の収集時間と詳細を表示することはできません。 TiDB v6.1.0 以降、統計収集タスクの履歴レコードは保持され、クラスターの再起動後にクエリできるようになりました。これは、統計の異常によって引き起こされるクエリ パフォーマンスの問題のトラブルシューティングの参考になります。

    [ユーザードキュメント](/sql-statements/sql-statement-show-analyze-status.md)

-   TiDB、TiKV、 TiFlash構成の動的変更のサポート

    以前の TiDB バージョンでは、構成項目を変更した後、変更を有効にするためにクラスターを再起動する必要がありました。これにより、オンライン サービスが中断される可能性があります。この問題に対処するために、TiDB v6.1.0 には動的構成機能が導入されており、クラスターを再起動せずにパラメーターの変更を検証できるようになります。具体的な最適化は次のとおりです。

    -   一部の TiDB 構成項目をシステム変数に変換して、動的に変更して永続化できるようにします。元の構成項目は変換後は非推奨になることに注意してください。変換された構成アイテムの詳細なリストについては、 [コンフィグレーションファイルのパラメータ](#configuration-file-parameters)を参照してください。
    -   一部の TiKV パラメーターのオンライン構成をサポートします。パラメータの詳細なリストについては、 [その他](#others)を参照してください。
    -   TiFlash構成項目`max_threads`をシステム変数`tidb_max_tiflash_threads`に変換して、構成を動的に変更して永続化できるようにします。変換後も元の構成アイテムが残ることに注意してください。

    以前のバージョンからアップグレードされた (オンラインおよびオフライン アップグレードを含む) v6.1.0 クラスターの場合は、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成項目がすでに存在する場合、TiDB はアップグレード プロセス中に、構成項目の値を対応するシステム変数の値に自動的に更新します。このようにして、アップグレード後のシステムの動作はパラメータの最適化による影響を受けません。
    -   上記の自動アップデートは、アップグレード中に 1 回だけ実行されます。アップグレード後、非推奨の構成項目は無効になります。

    この機能を使用すると、システムを再起動してサービスを中断する代わりに、パラメータを動的に変更し、検証して永続化することができます。これにより、日常のメンテナンスが容易になります。

    [ユーザードキュメント](/dynamic-config.md)

-   クエリまたは接続のグローバルな強制終了をサポート

    `enable-global-kill`構成 (デフォルトで有効) を使用して、Global Kill 機能を制御できます。

    TiDB v6.1.0 より前では、操作で大量のリソースが消費され、クラスターの安定性の問題が発生する場合、ターゲット TiDB インスタンスに接続し、 `KILL TIDB ${id};`コマンドを実行してターゲットの接続と操作を終了する必要がありました。多くの TiDB インスタンスの場合、この方法は使用が簡単ではなく、誤った操作が発生する傾向があります。 v6.1.0 以降、 `enable-global-kill`構成が導入され、デフォルトで有効になります。クライアントと TiDB の間にプロキシがある場合、他のクエリやセッションを誤って終了することを心配することなく、任意の TiDB インスタンスで kill コマンドを実行して、指定された接続と操作を終了できます。現在、TiDB は、Ctrl+C を使用したクエリまたはセッションの終了をサポートしていません。

    [ユーザードキュメント](/tidb-configuration-file.md#enable-global-kill-new-in-v610) [#8854](https://github.com/pingcap/tidb/issues/8854)

-   TiKV API V2 (実験的)

    v6.1.0 より前では、TiKV が Raw Key Valuestorageとして使用される場合、TiKV はクライアントから渡された Raw データのみを保存するため、基本的な Key Value の読み取りおよび書き込み機能のみを提供します。

    TiKV API V2 は、次のような新しい Raw Key Valuestorage形式とアクセス インターフェイスを提供します。

    -   データは MVCC に保存され、データの変更タイムスタンプが記録されます。この機能は、変更データ キャプチャと増分バックアップと復元を実装するための基盤を築きます。
    -   データはさまざまな用途に応じてスコープ設定され、単一の TiDB クラスター、トランザクション KV、RawKV アプリケーションの共存をサポートします。

    <Warning>

    基盤となるstorage形式が大幅に変更されたため、API V2 を有効にした後は、TiKV クラスターを v6.1.0 より前のバージョンにロールバックできません。 TiKV をダウングレードすると、データが破損する可能性があります。

    </Warning>

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [#11745](https://github.com/tikv/tikv/issues/11745)

### MySQLの互換性 {#mysql-compatibility}

-   MySQL によるユーザーレベルのロック管理との互換性をサポート

    ユーザーレベルのロックは、MySQL が組み込み関数を通じて提供するユーザー名付きのロック管理システムです。ロック関数は、ロックのブロック、待機、その他のロック管理機能を提供します。ユーザーレベルのロックは、Rails、Elixir、Ecto などの ORM フレームワークでも広く使用されています。 v6.1.0 以降、TiDB は MySQL と互換性のあるユーザーレベル`RELEASE_LOCK` `GET_LOCK`および`RELEASE_ALL_LOCKS`関数をサポートしています。

    [ユーザードキュメント](/functions-and-operators/locking-functions.md) [#14994](https://github.com/pingcap/tidb/issues/14994)

### データ移行 {#data-migration}

-   シャードテーブルのマージおよび移行の楽観的モードが GA になりました

    DM は、楽観的モードでシャード テーブルからデータをマージおよび移行するタスク用の多数のシナリオ テストを追加します。これは、日常使用シナリオの 90% をカバーします。悲観的モードと比較して、楽観的モードは使用が簡単で効率的です。使用上の注意をよく理解した上で、できれば楽観的モードを使用することをお勧めします。

    [ユーザードキュメント](/dm/feature-shard-merge-optimistic.md#restrictions)

-   DM WebUI は、指定されたパラメータに従ってタスクの開始をサポートします

    移行タスクを開始するときに、開始時刻とセーフ モードの期間を指定できます。これは、多数のソースを含む増分移行タスクを作成する場合に特に便利で、ソースごとにbinlogの開始位置を指定する必要がなくなります。

    [ユーザードキュメント](/dm/dm-webui-guide.md) [#5442](https://github.com/pingcap/tiflow/issues/5442)

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiDB は、さまざまなサードパーティ データ エコシステムとのデータ共有をサポートします

    -   TiCDC は、TiDB 増分データを Avro 形式で Kafka に送信することをサポートしており、Confluent を介して KSQL や Snowflake などのサードパーティとデータを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-avro-protocol.md) [#5338](https://github.com/pingcap/tiflow/issues/5338)

    -   TiCDC は、TiDB からの増分データをテーブルごとにさまざまな Kafka トピックにディスパッチすることをサポートしています。これを Canal-json 形式と組み合わせることで、Flink と直接データを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink) [#4423](https://github.com/pingcap/tiflow/issues/4423)

    -   TiCDC は SASL GSSAPI 認証タイプをサポートし、Kafka を使用した SASL 認証例を追加します。

        [ユーザードキュメント](/ticdc/ticdc-sink-to-kafka.md#ticdc-uses-the-authentication-and-authorization-of-kafka) [#4423](https://github.com/pingcap/tiflow/issues/4423)

-   TiCDC は`charset=GBK`テーブルの複製をサポートします。

    [ユーザードキュメント](/character-set-gbk.md#component-compatibility) [#4806](https://github.com/pingcap/tiflow/issues/4806)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                           | 種類の変更    | 説明                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                    | 修正済み     | デフォルト値が`OFF`から`ON`に変更されました。                                                                                                                 |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                           | 修正済み     | この変数は GLOBAL スコープを追加し、変数値はクラスターに保持されます。                                                                                                     |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)                                                       | 修正済み     | 変数のスコープが INSTANCE から GLOBAL に変更されます。変数値はクラスターに保持され、値の範囲は`[0, 1073741824]`に変更されます。                                                           |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)                                       | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                        |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)                                   | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                        |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                       | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `run-auto-analyze` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                                         |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)       | 新しく追加された | この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行するときの動作を制御します。                                                                                       |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                           | 新しく追加された | v6.1.0 以降、TiDB の結合したテーブルの再配置アルゴリズムは、Outer Join をサポートしています。この変数はサポート動作を制御します。デフォルト値は`ON`です。                                                  |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                         | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                              |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)                                             | 新しく追加された | この変数は、コミットされていないトランザクションによってブロックされる GC セーフ ポイントの最大時間を設定するために使用されます。                                                                         |
| [tidb_max_auto_analyze_time](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                                     | 新しく追加された | この変数は、auto analyzeの最大実行時間を指定するために使用されます。                                                                                                    |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)                                       | 新しく追加された | この変数は、リクエストを実行するためのTiFlash の最大同時実行数を設定するために使用されます。                                                                                          |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)                                                 | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                                               |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)                                           | 新しく追加された | この変数は[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)ユーザーによる手動実行や TiDB バックグラウンドでの自動分析タスクなど、TiDB が統計を更新するときの最大メモリ使用量を制御します。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)                   | 新しく追加された | この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、ただちにエラーを返すかどうかを指定します。                                                                               |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-new-in-v610) | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                   |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                             | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降はシステム変数に変更されました。                                             |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)                                   | 新しく追加された | この変数は、TiDB 統計キャッシュのメモリ割り当てを設定します。                                                                                                           |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                             | 種類の変更    | 説明                                                                                                                                                        |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `committer-concurrency`                                                                                                                                                                                | 削除されました  | システム変数`tidb_committer_concurrency`に置き換えられます。この構成項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                         |
| TiDB           | `lower-case-table-names`                                                                                                                                                                               | 削除されました  | 現在、TiDB は`lower_case_table_name=2`のみをサポートします。別の値が設定されている場合、クラスターを v6.1.0 にアップグレードすると、その値は失われます。                                                           |
| TiDB           | `mem-quota-query`                                                                                                                                                                                      | 削除されました  | システム変数`tidb_mem_quota_query`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                               |
| TiDB           | `oom-action`                                                                                                                                                                                           | 削除されました  | システム変数`tidb_mem_oom_action`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                                |
| TiDB           | `prepared-plan-cache.capacity`                                                                                                                                                                         | 削除されました  | システム変数`tidb_prepared_plan_cache_size`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                      |
| TiDB           | `prepared-plan-cache.enabled`                                                                                                                                                                          | 削除されました  | システム変数`tidb_enable_prepared_plan_cache`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                    |
| TiDB           | `query-log-max-len`                                                                                                                                                                                    | 削除されました  | システム変数`tidb_query_log_max_len`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                             |
| TiDB           | `require-secure-transport`                                                                                                                                                                             | 削除されました  | システム変数`require_secure_transport`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                           |
| TiDB           | `run-auto-analyze`                                                                                                                                                                                     | 削除されました  | システム変数`tidb_enable_auto_analyze`に置き換えられます。この設定項目はもう有効ではありません。値を変更したい場合は、対応するシステム変数を変更する必要があります。                                                           |
| TiDB           | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)                                                                                                                     | 新しく追加された | Global Kill (インスタンス間でのクエリまたは接続の終了) 機能を有効にするかどうかを制御します。値が`true`の場合、 `KILL`と`KILL TIDB`ステートメントの両方でインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続が誤って終了することを心配する必要はありません。 |
| TiDB           | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                                                                                 | 新しく追加された | 統計キャッシュのメモリ割り当てを有効にするかどうかを制御します。                                                                                                                          |
| TiKV           | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1)                                                                                                                                           | 修正済み     | デフォルト値が`FALSE`から`TRUE`に変更されました。                                                                                                                           |
| TiKV           | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys)                                                                                                                                       | 修正済み     | デフォルト値は 1440000 から`region-split-keys / 2 * 3`に変更されます。                                                                                                     |
| TiKV           | [`region-max-size`](/tikv-configuration-file.md#region-max-size)                                                                                                                                       | 修正済み     | デフォルト値が 144 MB から`region-split-size / 2 * 3`に変更されました。                                                                                                     |
| TiKV           | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)                                                                                                     | 新しく追加された | リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。                                                                                                                      |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                                                                         | 新しく追加された | `enable-region-bucket`が true の場合のバケットのサイズ。                                                                                                                |
| TiKV           | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size)                                                                                                                   | 新しく追加された | ローカルにキャッシュされたタイムスタンプの最小数。                                                                                                                                 |
| TiKV           | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval)                                                                                                                               | 新しく追加された | ローカルにキャッシュされたタイムスタンプが更新される間隔。                                                                                                                             |
| TiKV           | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-new-in-v610)                                                                                                     | 新しく追加された | スナップショット ファイルのサイズがこの値を超えると、スナップショット ファイルは複数のファイルに分割されます。                                                                                                  |
| TiKV           | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit)                                                                                                                                 | 新しく追加された | Raft Engineのメモリ使用量の制限を指定します。                                                                                                                              |
| TiKV           | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610)                                                                                 | 新しく追加された | RocksDB が回復可能なバックグラウンド エラーを検出した後、最大回復時間が許可されます。                                                                                                           |
| TiKV           | [`storage.api-version`](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                           | 新しく追加された | TiKV が生のキー/値ストアとして機能するときに TiKV によって使用されるstorage形式とインターフェイスのバージョン。                                                                                         |
| PD             | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-new-in-v610)                                                                                                  | 新しく追加された | ストアがオンラインになるまでの最大待ち時間を制御します。                                                                                                                              |
| TiCDC          | [`enable-tls`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                             | 新しく追加された | TLS を使用してダウンストリーム Kafka インスタンスに接続するかどうか。                                                                                                                  |
| TiCDC          | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新しく追加された | Kafka の SASL/GSSAPI 認証をサポートするために使用されます。詳細は[`kafka`を使用してシンク URI を構成する](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)を参照してください。               |
| TiCDC          | [`avro-decimal-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)      | 新しく追加された | Avro 形式の出力詳細を決定します。                                                                                                                                       |
| TiCDC          | [`dispatchers.topic`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                             | 新しく追加された | TiCDC が増分データをさまざまな Kafka トピックにディスパッチする方法を制御します。                                                                                                           |
| TiCDC          | [`dispatchers.partition`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                         | 新しく追加された | `dispatchers.partition`は`dispatchers.dispatcher`のエイリアスです。 TiCDC が増分データを Kafka パーティションにディスパッチする方法を制御します。                                                   |
| TiCDC          | [`schema-registry`](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-kafka-connect-confluent-platform)                                                                                               | 新しく追加された | Avro スキーマを保存するスキーマ レジストリ エンドポイントを指定します。                                                                                                                   |
| DM             | `dmctl start-relay`コマンドの`worker`                                                                                                                                                                       | 削除されました  | このパラメータの使用は推奨されません。よりシンプルな実装を提供します。                                                                                                                       |
| DM             | ソース構成ファイル内の`relay-dir`                                                                                                                                                                                 | 削除されました  | ワーカー構成ファイル内の同じ構成項目に置き換えられます。                                                                                                                              |
| DM             | タスク構成ファイル内の`is-sharding`                                                                                                                                                                               | 削除されました  | `shard-mode`の構成アイテムに置き換えられます。                                                                                                                             |
| DM             | タスク構成ファイル内の`auto-fix-gtid`                                                                                                                                                                             | 削除されました  | v5.x で非推奨となり、v6.1.0 で正式に削除されました。                                                                                                                          |
| DM             | ソース構成ファイルの`meta-dir`と`charset`                                                                                                                                                                         | 削除されました  | v5.x で非推奨となり、v6.1.0 で正式に削除されました。                                                                                                                          |

### その他 {#others}

-   デフォルトでプリペアドプランキャッシュを有効にする

    新しいクラスターでは、プリペアドプランキャッシュがデフォルトで有効になっており、 `Prepare` / `Execute`リクエストの実行プランをキャッシュします。以降の実行ではクエリ プランの最適化をスキップできるため、パフォーマンスの向上につながります。アップグレードされたクラスターは、構成ファイルから構成を継承します。新しいクラスターでは新しいデフォルト値が使用されます。これは、プリペアドプランキャッシュがデフォルトで有効になり、各セッションで最大 100 個のプランをキャッシュできることを意味します ( `capacity=100` )。この機能のメモリ消費量については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)を参照してください。

-   TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`インスタンス レベルのタスクを示し、タスク レコードは TiDB の再起動後にクリアされます。 TiDB v6.1.0 以降、 `SHOW ANALYZE STATUS`クラスター レベルのタスクを示し、タスク レコードは再起動後も保持されます。 `tidb_analyze_version = 2`の場合、 `Job_info`列に`analyze option`情報が追加されます。

-   TiKV 内の SST ファイルが破損していると、TiKV プロセスがpanicを引き起こす可能性があります。 TiDB v6.1.0 より前は、SST ファイルが破損すると、TiKV が即座にpanicを起こしました。 TiDB v6.1.0 以降、TiKV プロセスは、SST ファイルが破損してから 1 時間後にpanicになります。

-   次の TiKV 構成項目は[値を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)をサポートします。

    -   `raftstore.raft-entry-max-size`
    -   `quota.foreground-cpu-time`
    -   `quota.foreground-write-bandwidth`
    -   `quota.foreground-read-bandwidth`
    -   `quota.max-delay-duration`
    -   `server.grpc-memory-pool-quota`
    -   `server.max-grpc-send-msg-len`
    -   `server.raft-msg-max-batch-size`

-   v6.1.0 では、一部の構成ファイル パラメータがシステム変数に変換されます。以前のバージョンからアップグレードされた v6.1.0 クラスター (オンラインおよびオフライン アップグレードを含む) の場合は、次の点に注意してください。

    -   アップグレード前に構成ファイルで指定された構成項目がすでに存在する場合、TiDB はアップグレード プロセス中に、構成項目の値を対応するシステム変数の値に自動的に更新します。このように、パラメータの最適化により、アップグレード後もシステムの動作は変わりません。
    -   上記の自動アップデートは、アップグレード中に 1 回だけ実行されます。アップグレード後、非推奨の構成項目は無効になります。

-   ダッシュボード ページはDM WebUIから削除されました。

-   `dispatchers.topic`と`dispatchers.partition`が有効な場合、TiCDC を v6.1.0 より前のバージョンにダウングレードすることはできません。

-   Avro プロトコルを使用するTiCDC Changefeed は、 v6.1.0 より前のバージョンにダウングレードできません。

## 改善点 {#improvements}

-   TiDB

    -   `UnionScanRead`オペレーター[#32433](https://github.com/pingcap/tidb/issues/32433)のパフォーマンスの向上
    -   `EXPLAIN`の出力におけるタスク タイプの表示を改善します (MPP タスク タイプを追加) [#33332](https://github.com/pingcap/tidb/issues/33332)
    -   列[#10377](https://github.com/pingcap/tidb/issues/10377)のデフォルト値として`rand()`の使用をサポート
    -   列[#33870](https://github.com/pingcap/tidb/issues/33870)のデフォルト値として`uuid()`の使用をサポート
    -   `latin1`から`utf8` / `utf8mb4`までの列の文字セットの変更をサポート[#34008](https://github.com/pingcap/tidb/issues/34008)

-   TiKV

    -   インメモリ悲観的ロック[#12279](https://github.com/tikv/tikv/issues/12279)使用時のCDCの古い値ヒット率を改善
    -   ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[#12398](https://github.com/tikv/tikv/issues/12398)
    -   Raft Engine [#12255](https://github.com/tikv/tikv/issues/12255)でのメモリ制限の設定をサポート
    -   TiKV は、破損した SST ファイルを自動的に検出して削除し、製品の可用性を向上させます[#10578](https://github.com/tikv/tikv/issues/10578)
    -   CDC は RawKV [#11965](https://github.com/tikv/tikv/issues/11965)をサポートします
    -   大きなスナップショット ファイルを複数のファイルに分割するサポート[#11595](https://github.com/tikv/tikv/issues/11595)
    -   スナップショット GC がRaftstoreメッセージ ループをブロックしないように、スナップショットガベージコレクションをRaftstoreからバックグラウンド スレッドに移動します[#11966](https://github.com/tikv/tikv/issues/11966)
    -   gPRC メッセージの最大メッセージ長 ( `max-grpc-send-msg-len` ) と最大バッチ サイズ ( `raft-msg-max-batch-size` ) の動的設定をサポートします[#12334](https://github.com/tikv/tikv/issues/12334)
    -   Raft [#10483](https://github.com/tikv/tikv/issues/10483)を介したオンラインの安全でない復元計画の実行をサポート

-   PD
    -   リージョンラベル[#4694](https://github.com/tikv/pd/issues/4694)の有効期限 (TTL) をサポート
    -   サポートリージョンバケット[#4668](https://github.com/tikv/pd/issues/4668)
    -   Swaggerサーバーのコンパイルをデフォルトで無効にする[#4932](https://github.com/tikv/pd/issues/4932)

-   TiFlash

    -   マージ フェーズ[#4451](https://github.com/pingcap/tiflash/issues/4451)でより効率的なアルゴリズムが使用されるように、集計演算子のメモリ計算を最適化します。

-   ツール

    -   バックアップと復元 (BR)

        -   空のデータベースのバックアップと復元のサポート[#33866](https://github.com/pingcap/tidb/issues/33866)

    -   TiDB Lightning

        -   散乱リージョンをバッチ モードに最適化して、散乱リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   TiCDC は、レプリケーション中の大規模なトランザクションの分割をサポートしており、これにより、大規模なトランザクションによって発生するレプリケーションのレイテンシーが大幅に削減されます[#5280](https://github.com/pingcap/tiflow/issues/5280)

## バグの修正 {#bug-fixes}

-   TiDB

    -   `in`関数が`bit`種類のデータを処理するときにpanicが発生する可能性がある問題を修正します。 [#33070](https://github.com/pingcap/tidb/issues/33070)
    -   `UnionScan`演算子が順序[#33175](https://github.com/pingcap/tidb/issues/33175)を維持できないため、間違ったクエリ結果が表示される問題を修正
    -   特定の場合に Merge Join 演算子が間違った結果を取得する問題を修正します[#33042](https://github.com/pingcap/tidb/issues/33042)
    -   動的枝刈りモード[#33231](https://github.com/pingcap/tidb/issues/33231)において`index join`の結果が間違っている場合がある問題を修正
    -   パーティションテーブルの一部のパーティションが削除されると、データがガベージコレクションされない場合がある問題を修正します[#33620](https://github.com/pingcap/tidb/issues/33620)
    -   クラスターの PD ノードが交換された後、一部の DDL ステートメントが一定期間スタックすることがある問題を修正します[#33908](https://github.com/pingcap/tidb/issues/33908)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルがクエリされるときに TiDBサーバーがメモリ不足になる可能性がある問題を修正します。この問題は、Grafana ダッシュボード[#33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックすると発生する可能性があります。
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[#31422](https://github.com/pingcap/tidb/issues/31422)
    -   TopSQL モジュールのメモリリークの問題を修正[#34525](https://github.com/pingcap/tidb/issues/34525) [#34502](https://github.com/pingcap/tidb/issues/34502)
    -   PointGet プラン[#32371](https://github.com/pingcap/tidb/issues/32371)でプラン キャッシュが間違っている可能性がある問題を修正
    -   RC 分離レベル[#34447](https://github.com/pingcap/tidb/issues/34447)でプラン キャッシュを開始すると、クエリ結果が間違っていることがある問題を修正

-   TiKV

    -   TiKV インスタンスがオフラインになったときにRaftログラグが増加する問題を修正[#12161](https://github.com/tikv/tikv/issues/12161)
    -   マージ対象のターゲットリージョンが無効であるため、TiKV がパニックを起こして予期せずピアを破棄する問題を修正します[#12232](https://github.com/tikv/tikv/issues/12232)
    -   v5.3.1 または v5.4.0 から v6.0.0 以降のバージョン[#12269](https://github.com/tikv/tikv/issues/12269)にアップグレードするときに、TiKV が`failed to load_latest_options`エラーを報告する問題を修正します。
    -   メモリリソースが不足している場合にRaftログを追加することによって引き起こされる OOM の問題を修正します[#11379](https://github.com/tikv/tikv/issues/11379)
    -   ピアの破棄とリージョン[#12368](https://github.com/tikv/tikv/issues/12368)のバッチ分割の間の競合によって引き起こされる TiKVpanicの問題を修正します。
    -   `stats_monitor`デッド ループに陥った後、短時間で TiKVメモリ使用量が急増する問題を修正[#12416](https://github.com/tikv/tikv/issues/12416)
    -   Follower Read [#12478](https://github.com/tikv/tikv/issues/12478)を使用すると TiKV が`invalid store ID 0`エラーを報告する問題を修正

-   PD

    -   `not leader` [#4797](https://github.com/tikv/pd/issues/4797)の間違ったステータス コードを修正
    -   いくつかの特殊なケースにおける TSO フォールバックのバグを修正[#4884](https://github.com/tikv/pd/issues/4884)
    -   PDリーダー移転後、削除された墓石ストアが再び表示される問題を修正[#4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー転送[#4769](https://github.com/tikv/pd/issues/4769)直後にスケジューリングが開始できない問題を修正

-   TiDB ダッシュボード

    -   Top SQL機能が有効になる前に実行されていたSQL文のCPUオーバーヘッドをTop SQLが収集できないバグを修正[#33859](https://github.com/pingcap/tidb/issues/33859)

-   TiFlash

    -   多数の INSERT および DELETE 操作後の潜在的なデータの不整合を修正[#4956](https://github.com/pingcap/tiflash/issues/4956)

-   ツール

    -   TiCDC

        -   DDL スキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正します[#1386](https://github.com/pingcap/tiflow/issues/1386)
        -   特別な増分スキャン シナリオ[#5468](https://github.com/pingcap/tiflow/issues/5468)で発生するデータ損失を修正します。

    -   TiDB データ移行 (DM)

        -   `start-time`タイム ゾーンの問題を修正し、DM の動作をダウンストリーム タイム ゾーンの使用からアップストリーム タイム ゾーン[#5271](https://github.com/pingcap/tiflow/issues/5471)の使用に変更します。
        -   タスクが自動的に再開された後、DM がより多くのディスク領域を占有する問題を修正[#3734](https://github.com/pingcap/tiflow/issues/3734) [#5344](https://github.com/pingcap/tiflow/issues/5344)
        -   チェックポイントフラッシュにより失敗した行のデータがスキップされる場合がある問題を修正[#5279](https://github.com/pingcap/tiflow/issues/5279)
        -   場合によっては、ダウンストリームでフィルタリングされた DDL を手動で実行すると、タスクの再開が失敗する可能性がある問題を修正します[#5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `case-sensitive: true`が設定されていない場合、大文字のテーブルが複製できない問題を修正します[#5255](https://github.com/pingcap/tiflow/issues/5255)
        -   `SHOW CREATE TABLE`ステートメント[#5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーのpanic問題を修正します。
        -   GTID が有効になっている場合、またはタスクが自動的に再開された場合に、CPU 使用率が増加し、大量のログが出力される場合がある問題を修正します[#5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM WebUI [#4993](https://github.com/pingcap/tiflow/issues/4993)のオフライン オプションとその他の使用上の問題を修正
        -   アップストリーム[#3731](https://github.com/pingcap/tiflow/issues/3731)で GTID が空の場合、増分タスクの開始に失敗する問題を修正
        -   空の設定により dm-master がpanicを引き起こす可能性がある問題を修正[#3732](https://github.com/pingcap/tiflow/issues/3732)

    -   TiDB Lightning

        -   事前チェックでローカル ディスク リソースとクラスターの可用性がチェックされない問題を修正します[#34213](https://github.com/pingcap/tidb/issues/34213)
        -   スキーマ[#33381](https://github.com/pingcap/tidb/issues/33381)の誤ったルーティングの問題を修正
        -   TiDB Lightningパニック時に PD 設定が正しく復元されない問題を修正[#31733](https://github.com/pingcap/tidb/issues/31733)
        -   `auto_increment`列[#29737](https://github.com/pingcap/tidb/issues/27937)の範囲外データが原因でローカル バックエンドのインポートが失敗する問題を修正
        -   `auto_random`列または`auto_increment`列が null の場合にローカル バックエンドのインポートが失敗する問題を修正[#34208](https://github.com/pingcap/tidb/issues/34208)

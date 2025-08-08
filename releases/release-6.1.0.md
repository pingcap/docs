---
title: TiDB 6.1.0 Release Notes
summary: TiDB 6.1.0 の新機能、互換性の変更、改善点、バグ修正について説明します。
---

# TiDB 6.1.0 リリースノート {#tidb-6-1-0-release-notes}

発売日：2022年6月13日

TiDB バージョン: 6.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [本番環境への展開](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

6.1.0 の主な新機能または改善点は次のとおりです。

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になり、 MySQL 5.7と互換性があります
-   TiFlashパーティションテーブル（動的プルーニング）が GA になりました
-   ユーザーレベルのロック管理をサポートし、MySQLと互換性があります
-   非トランザクションDML文をサポート（ `DELETE`のみサポート）
-   TiFlashはオンデマンドのデータ圧縮をサポート
-   MPPはウィンドウ関数フレームワークを導入する
-   TiCDCはAvro経由でKafkaへの変更ログの複製をサポートします
-   TiCDCはレプリケーション中に大規模なトランザクションを分割することをサポートしており、これにより大規模なトランザクションによって発生するレプリケーションのレイテンシーが大幅に削減されます。
-   シャードテーブルのマージと移行の楽観的モードがGAになりました

## 新機能 {#new-features}

### SQL {#sql}

-   List パーティショニングとリストCOLUMNSパーティショニングがGAになりました。どちらもMySQL 5.7と互換性があります。

    ユーザー[List COLUMNS partitioning](/partitioned-table.md#list-columns-partitioning) : [List パーティショニング](/partitioned-table.md#list-partitioning)

-   TiFlash は、コンパクト コマンドの開始をサポートしています。(実験的)

    TiFlash v6.1.0 introduces the `ALTER TABLE ... COMPACT` statement, which provides a manual way to compact physical data based on the existing background compaction mechanism. With this statement, you can update data in earlier formats and improve read/write performance any time as appropriate. It is recommended that you execute this statement to compact data after upgrading your cluster to v6.1.0. This statement is an extension of the standard SQL syntax and therefore is compatible with MySQL clients. For scenarios other than TiFlash upgrade, usually there is no need to use this statement.

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md) [＃4145](https://github.com/pingcap/tiflash/issues/4145)

-   TiFlash はウィンドウ関数フレームワークを実装し、次のウィンドウ関数をサポートします。

    -   `RANK()`
    -   `DENSE_RANK()`
    -   `ROW_NUMBER()`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [＃33072](https://github.com/pingcap/tidb/issues/33072)

### 可観測性 {#observability}

-   継続的なプロファイリングは、ARMアーキテクチャとTiFlash をサポートします。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

-   Grafana は、全体的なパフォーマンス診断のためのシステム レベルのエントリを提供するパフォーマンス概要ダッシュボードを追加します。

    TiDB可視化監視コンポーネントGrafanaの新しいダッシュボードである「パフォーマンス概要」は、システム全体のパフォーマンス診断のためのエントリーを提供します。トップダウン型パフォーマンス分析手法に基づき、「パフォーマンス概要」ダッシュボードは、TiDBのパフォーマンスメトリクスをデータベース時間の内訳に基づいて整理し、異なる色で表示します。これらの色を確認することで、システム全体のパフォーマンスボトルネックを一目で特定できるため、パフォーマンス診断時間を大幅に短縮し、パフォーマンス分析と診断を簡素化します。

    [ユーザードキュメント](/performance-tuning-overview.md)

### パフォーマンス {#performance}

-   カスタマイズされたリージョンサイズをサポート

    v6.1.0以降では、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)設定することでリージョンのサイズを大きく設定できます。これにより、リージョンの数を効果的に削減し、リージョンの管理を容易にし、クラスターのパフォーマンスと安定性を向上させることができます。

    [ユーザードキュメント](/tune-region-performance.md#use-region-split-size-to-adjust-region-size) [＃11515](https://github.com/tikv/tikv/issues/11515)

-   同時実行性を高めるためにバケットの使用をサポート（実験的）

    リージョンのサイズを大きくした後でもクエリの同時実行性をさらに向上させるために、TiDB ではバケットという概念が導入されています。バケットとは、リージョン内のより小さな範囲を指します。バケットをクエリ単位として使用すると、リージョンのサイズを大きくした場合に同時実行クエリのパフォーマンスを最適化できます。また、バケットをクエリ単位として使用すると、ホットスポットリージョンのサイズを動的に調整して、スケジューリングの効率と負荷分散を確保することもできます。この機能は現在実験的です。本番環境での使用は推奨されません。

    [ユーザードキュメント](/tune-region-performance.md#use-bucket-to-increase-concurrency) [＃11515](https://github.com/tikv/tikv/issues/11515)

-   Use Raft Engine as the default log storage engine

    v6.1.0以降、TiDBはログのデフォルトstorageエンジンとしてRaft Engineを使用しています。RocksDBと比較して、 Raft EngineはTiKV I/O書き込みトラフィックを最大40%、CPU使用率を10%削減し、フォアグラウンドスループットを約5%向上させ、特定の負荷下ではテールレイテンシーを20%削減します。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine) [＃95](https://github.com/tikv/raft-engine/issues/95)

-   結合順序ヒント構文をサポートする

    -   The `LEADING` hint reminds the optimizer to use the specified order as the prefix of join operations. A good prefix of join can quickly reduce the amount of data at the early phase of join and improve the query performance.
    -   `STRAIGHT_JOIN`ヒントは、 `FROM`句内のテーブルの順序と一致する順序でテーブルを結合するようにオプティマイザーに通知します。

    これにより、テーブル結合の順序を固定することができます。ヒントを適切に使用することで、SQLパフォーマンスとクラスタの安定性を効果的に向上させることができます。

    [＃29932](https://github.com/pingcap/tidb/issues/29932) [`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join) : [`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-)

-   TiFlash はさらに 4 つの関数をサポートしています。

    -   `FROM_DAYS`
    -   `TO_DAYS`
    -   `TO_SECONDS`
    -   `WEEKOFYEAR`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [＃4679](https://github.com/pingcap/tiflash/issues/4679) [＃4678](https://github.com/pingcap/tiflash/issues/4678) [＃4677](https://github.com/pingcap/tiflash/issues/4677)

-   TiFlash は、動的プルーニング モードでパーティション化されたテーブルをサポートします。

    OLAPシナリオにおけるパフォーマンス向上のため、パーティションテーブルでは動的プルーニングモードがサポートされています。TiDBをv6.0.0より前のバージョンからアップグレードする場合は、パフォーマンスを最大限に高めるために、既存のパーティションテーブルの統計情報を手動で更新することをお勧めします（新規インストールの場合、またはv6.1.0へのアップグレード後に新しく作成されたパーティションの場合は必要ありません）。

    [＃3873](https://github.com/pingcap/tiflash/issues/3873) [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) : [MPP モードでパーティション テーブルにアクセスする](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

### 安定性 {#stability}

-   SST 破損からの自動回復

    RocksDBがバックグラウンドで破損したSSTファイルを検出すると、TiKVは影響を受けたピアのスケジュールを設定し、他のレプリカを使用してそのデータの復旧を試みます。パラメータ`background-error-recovery-window`を使用して、復旧の最大許容時間を設定できます。復旧操作が指定時間内に完了しない場合、TiKVはpanicになります。この機能は、復旧可能な破損storageを自動的に検出して復旧するため、クラスターの安定性が向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610) [＃10578](https://github.com/tikv/tikv/issues/10578)

-   非トランザクションDMLステートメントをサポートする

    大規模データ処理のシナリオでは、大規模なトランザクションを伴う単一のSQL文が、クラスタの安定性とパフォーマンスに悪影響を及ぼす可能性があります。TiDB v6.1.0以降、 `DELETE` SQL文を複数のSQL文に分割してバッチ処理する構文がサポートされています。分割文はトランザクションの原子性と独立性を損なう可能性がありますが、クラスタの安定性を大幅に向上させます。詳細な構文については、 [`BATCH`](/sql-statements/sql-statement-batch.md)参照してください。

    [User document](/non-transactional-dml.md)

-   TiDBは最大GC待機時間の設定をサポートしています

    TiDB のトランザクションは、マルチバージョン同時実行制御 (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが格納されます。古いデータはガベージコレクション (GC) タスクによって定期的にクリーンアップされ、storageスペースの再利用を促進してクラスターのパフォーマンスと安定性を向上させます。GC は、デフォルトでは 10 分ごとにトリガーされます。長時間実行トランザクションが対応する履歴データにアクセスできるようにするため、実行中のトランザクションがある場合は GC タスクが遅延されます。GC タスクが無期限に遅延されないように、TiDB は GC タスクの最大遅延時間を制御するシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)導入しています。最大遅延時間を超えると、GC は強制的に実行されます。変数のデフォルト値は 24 時間です。この機能により、GC の待機時間と長時間実行トランザクションの関係を制御でき、クラスターの安定性が向上します。

    [ユーザードキュメント](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

-   TiDBは自動統計収集タスクの最大実行時間の設定をサポートします

    データベースは統計情報を収集することでデータの分布を効果的に把握し、合理的な実行計画を生成してSQL実行の効率を向上させることができます。TiDBは、頻繁に変更されるデータオブジェクトの統計をバックグラウンドで定期的に収集します。しかし、統計の収集はクラスタリソースを消費するため、ビジネスピーク時にはビジネスの安定運用に影響を与える可能性があります。

    v6.1.0以降、TiDBはバックグラウンド統計収集の最大実行時間を制御するための[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)導入しました。これはデフォルトで12時間です。アプリケーションがリソースのボトルネックに遭遇しない場合は、TiDBがタイムリーに統計を収集できるように、この変数を変更しないことを推奨します。

    [ユーザードキュメント](/system-variables.md)

### 使いやすさ {#ease-of-use}

-   複数のレプリカが失われた場合のワンストップオンラインデータ復旧をサポート

    TiDB v6.1.0より前のバージョンでは、マシン障害により複数のリージョンレプリカが失われた場合、ユーザーはすべてのTiKVサーバーを停止し、 TiKV Controlを使用してTiKVを1つずつリカバリする必要がありました。TiDB v6.1.0以降では、リカバリプロセスは完全に自動化されており、TiKVを停止する必要がなく、他のオンラインアプリケーションに影響を与えることもありません。リカバリプロセスはPD Controlを使用して開始でき、よりユーザーフレンドリーな概要情報を提供します。

    [ユーザードキュメント](/online-unsafe-recovery.md) [＃10483](https://github.com/tikv/tikv/issues/10483)

-   履歴統計収集タスクの表示をサポート

    `SHOW ANALYZE STATUS`文を使用すると、クラスターレベルの統計収集タスクを表示できます。TiDB v6.1.0 より前のバージョンでは、 `SHOW ANALYZE STATUS`文はインスタンスレベルのタスクのみを表示し、履歴タスクの記録は TiDB の再起動後に消去されます。そのため、履歴統計収集の時間と詳細は表示できません。TiDB v6.1.0 以降では、統計収集タスクの履歴記録は保持され、クラスターの再起動後もクエリを実行できます。これにより、統計の異常によって発生するクエリパフォーマンスの問題をトラブルシューティングするための参考資料となります。

    [ユーザードキュメント](/sql-statements/sql-statement-show-analyze-status.md)

-   TiDB、TiKV、およびTiFlash構成の動的な変更をサポート

    以前のバージョンのTiDBでは、設定項目を変更した後、変更を有効にするにはクラスタを再起動する必要がありました。これにより、オンラインサービスが中断される可能性がありました。この問題に対処するため、TiDB v6.1.0では動的設定機能が導入され、クラスタを再起動せずにパラメータ変更を検証できるようになりました。具体的な最適化は以下の通りです。

    -   TiDBの一部の設定項目をシステム変数に変換し、動的に変更・保存できるようにします。変換後は元の設定項目は非推奨となることに注意してください。変換後の設定項目の詳細なリストについては、 [コンフィグレーションファイルのパラメータ](#configuration-file-parameters)参照してください。
    -   Support configuring some TiKV parameters online. For a detailed list of the parameters, see [その他](#others).
    -   TiFlash構成項目`max_threads`システム変数`tidb_max_tiflash_threads`に変換し、構成を動的に変更して永続化できるようにします。変換後も元の構成項目は保持されることに注意してください。

    以前のバージョンからアップグレードされた v6.1.0 クラスター (オンライン アップグレードとオフライン アップグレードを含む) については、次の点に注意してください。

    -   If the configuration items specified in the configuration file before the upgrade already exist, TiDB will automatically update the values of the configured items to those of the corresponding system variables during the upgrade process. In this way, after the upgrade, the system behavior is not affected by parameter optimization.
    -   上記の自動更新はアップグレード中に1回のみ実行されます。アップグレード後は、廃止された設定項目は無効になります。

    この機能により、システムを再起動したりサービスを中断したりすることなく、パラメータを動的に変更し、検証して永続化することができます。これにより、日々のメンテナンスが容易になります。

    [ユーザードキュメント](/dynamic-config.md)

-   クエリや接続をグローバルに強制終了する機能をサポート

    `enable-global-kill`構成 (デフォルトで有効) を使用して、グローバル キル機能を制御できます。

    TiDB v6.1.0より前のバージョンでは、操作が大量のリソースを消費し、クラスタの安定性に問題が発生する場合、対象のTiDBインスタンスに接続してから`KILL TIDB ${id};`のコマンドを実行して対象の接続と操作を終了する必要がありました。多くのTiDBインスタンスの場合、この方法は使いにくく、誤操作が発生しやすいという問題がありました。v6.1.0以降では、 `enable-global-kill`構成が導入され、デフォルトで有効になっています。クライアントとTiDBの間にプロキシがある場合、他のクエリやセッションを誤って終了してしまう心配なく、任意のTiDBインスタンスでkillコマンドを実行して、指定した接続と操作を終了できます。現在、TiDBはCtrl+Cを使用してクエリまたはセッションを終了することをサポートしていません。

    [ユーザードキュメント](/tidb-configuration-file.md#enable-global-kill-new-in-v610) [＃8854](https://github.com/pingcap/tidb/issues/8854)

-   TiKV API V2 (実験的)

    v6.1.0 より前では、TiKV が Raw Key Valuestorageとして使用される場合、TiKV はクライアントから渡された生データのみを保存するため、基本的な Key Value の読み取りおよび書き込み機能のみを提供します。

    TiKV API V2 は、次のような新しい Raw Key Valuestorage形式とアクセス インターフェイスを提供します。

    -   データはMVCCに保存され、データの変更タイムスタンプが記録されます。この機能は、変更データキャプチャ（CDC）と増分バックアップ・リストアの実装の基盤となります。
    -   データはさまざまな使用法に応じてスコープ設定され、単一の TiDB クラスター、トランザクション KV、RawKV アプリケーションの共存をサポートします。

    <Warning>

    基盤となるstorage形式に大幅な変更が加えられたため、API V2 を有効にすると、TiKV クラスターを v6.1.0 より前のバージョンにロールバックできなくなります。TiKV をダウングレードすると、データが破損する可能性があります。

    </Warning>

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) [＃11745](https://github.com/tikv/tikv/issues/11745)

### MySQLの互換性 {#mysql-compatibility}

-   MySQL のユーザーレベルロック管理との互換性をサポート

    User-level locks are a user-named lock management system provided by MySQL through built-in functions. The locking functions can provide lock blocking, waiting, and other lock management capabilities. User-level locks are also widely used in ORM frameworks, such as Rails, Elixir, and Ecto. Since v6.1.0, TiDB has supported MySQL-compatible user-level lock management, and supports `GET_LOCK`, `RELEASE_LOCK`, and `RELEASE_ALL_LOCKS` functions.

    [ユーザードキュメント](/functions-and-operators/locking-functions.md) [＃14994](https://github.com/pingcap/tidb/issues/14994)

### データ移行 {#data-migration}

-   シャードテーブルのマージと移行の楽観的モードがGAになりました

    DMは、シャードテーブルからデータをマージおよび移行するタスク向けに、楽観的モードに対応した多数のシナリオテストを追加しており、日常的な使用シナリオの90%をカバーしています。悲観的モードと比較して、楽観的モードはよりシンプルで効率的です。使用上の注意をよく理解した上で、楽観的モードを推奨します。

    [ユーザードキュメント](/dm/feature-shard-merge-optimistic.md#restrictions)

-   DM WebUIは指定されたパラメータに従ってタスクの開始をサポートします

    移行タスクを開始する際、開始時刻とセーフモードの継続時間を指定できます。これは、多数のソースを持つ増分移行タスクを作成する場合に特に便利です。これにより、ソースごとにbinlogの開始位置を個別に指定する必要がなくなります。

    [ユーザードキュメント](/dm/dm-webui-guide.md) [＃5442](https://github.com/pingcap/tiflow/issues/5442)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiDBは、さまざまなサードパーティのデータエコシステムとのデータ共有をサポートします。

    -   TiCDC は、TiDB 増分データを Avro 形式で Kafka に送信することをサポートしており、Confluent を介して KSQL や Snowflake などのサードパーティとデータを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-avro-protocol.md) [＃5338](https://github.com/pingcap/tiflow/issues/5338)

    -   TiCDC は、テーブルごとに TiDB からさまざまな Kafka トピックに増分データをディスパッチすることをサポートしており、これを Canal-json 形式と組み合わせることで、Flink と直接データを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink), [＃4423](https://github.com/pingcap/tiflow/issues/4423)

    -   TiCDC は SASL GSSAPI 認証タイプをサポートし、Kafka を使用した SASL 認証の例を追加します。

        [User document](/ticdc/ticdc-sink-to-kafka.md#ticdc-uses-the-authentication-and-authorization-of-kafka) [#4423](https://github.com/pingcap/tiflow/issues/4423)

-   TiCDC は`charset=GBK`テーブルの複製をサポートします。

    [ユーザードキュメント](/character-set-gbk.md#component-compatibility) [＃4806](https://github.com/pingcap/tiflow/issues/4806)

## Compatibility changes {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                           | タイプを変更      | 説明                                                                                                                                           |
| ----------------------------------------------------------------------------------------------------------------------------- | ----------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                    | 修正済み        | デフォルト値は`OFF`から`ON`に変更されます。                                                                                                                   |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                           | 修正済み        | この変数は GLOBAL スコープを追加し、変数の値はクラスターに保持されます。                                                                                                     |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)                                                       | Modified    | 変数のスコープがINSTANCEからGLOBALに変更されます。変数の値はクラスターに保持され、値の範囲は`[0, 1073741824]`に変更されます。                                                               |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)                                       | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                        |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)                                   | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                        |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                       | Newly added | この設定は以前は`tidb.toml`オプション ( `run-auto-analyze` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                                         |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)       | 新しく追加された    | この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行するときの動作を制御します。                                                                                        |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                           | 新しく追加された    | バージョン6.1.0以降、TiDBの結合したテーブルの再配置アルゴリズムは外部結合をサポートしています。この変数はサポートの動作を制御し、デフォルト値は`ON`です。                                                          |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                         | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                              |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)                                             | 新しく追加された    | この変数は、コミットされていないトランザクションによってブロックされる GC セーフ ポイントの最大時間を設定するために使用されます。                                                                          |
| [tidb_max_auto_analyze_time](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                                     | 新しく追加された    | This variable is used to specify the maximum execution time of auto analyze.                                                                 |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)                                       | 新しく追加された    | この変数は、 TiFlash がリクエストを実行するための最大同時実行性を設定するために使用されます。                                                                                          |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)                                                 | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                                               |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)                                           | 新しく追加された    | この変数は、ユーザーによる手動実行[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)や TiDB のバックグラウンドでの自動分析タスクなど、TiDB が統計を更新する際の最大メモリ使用量を制御します。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)                   | 新しく追加された    | この変数は、非トランザクション DML ステートメントでエラーが発生した場合に、すぐにエラーを返すかどうかを指定します。                                                                                 |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-new-in-v610) | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                   |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                             | 新しく追加された    | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                             |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)                                   | 新しく追加された    | この変数は、TiDB 統計キャッシュのメモリクォータを設定します。                                                                                                            |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                             | タイプを変更   | 説明                                                                                                                                            |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | `committer-concurrency`                                                                                                                                                                                | 削除済み     | システム変数`tidb_committer_concurrency`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                |
| TiDB           | `lower-case-table-names`                                                                                                                                                                               | 削除済み     | 現在、TiDBは`lower_case_table_name=2`のみをサポートしています。別の値が設定されている場合は、クラスターをv6.1.0にアップグレードした後にその値は失われます。                                               |
| TiDB           | `mem-quota-query`                                                                                                                                                                                      | 削除済み     | システム変数`tidb_mem_quota_query`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                      |
| TiDB           | `oom-action`                                                                                                                                                                                           | 削除済み     | システム変数`tidb_mem_oom_action`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                       |
| TiDB           | `prepared-plan-cache.capacity`                                                                                                                                                                         | 削除済み     | システム変数`tidb_prepared_plan_cache_size`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                             |
| TiDB           | `prepared-plan-cache.enabled`                                                                                                                                                                          | 削除済み     | システム変数`tidb_enable_prepared_plan_cache`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                           |
| TiDB           | `query-log-max-len`                                                                                                                                                                                    | 削除済み     | システム変数`tidb_query_log_max_len`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                    |
| TiDB           | `require-secure-transport`                                                                                                                                                                             | 削除済み     | システム変数`require_secure_transport`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                  |
| TiDB           | `run-auto-analyze`                                                                                                                                                                                     | 削除済み     | システム変数`tidb_enable_auto_analyze`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                  |
| TiDB           | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)                                                                                                                     | 新しく追加された | Global Kill（インスタンス間のクエリまたは接続の終了）機能を有効にするかどうかを制御します。値が`true`の場合、 `KILL`と`KILL TIDB`両方のステートメントでインスタンス間のクエリまたは接続を終了できるため、クエリや接続が誤って終了する心配はありません。 |
| TiDB           | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                                                                                 | 新しく追加された | 統計キャッシュのメモリクォータを有効にするかどうかを制御します。                                                                                                              |
| TiKV           | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1)                                                                                                                                           | 修正済み     | The default value is changed from `FALSE` to `TRUE`.                                                                                          |
| TiKV           | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys)                                                                                                                                       | 修正済み     | デフォルト値は 1440000 から`region-split-keys / 2 * 3`に変更されます。                                                                                         |
| TiKV           | [`region-max-size`](/tikv-configuration-file.md#region-max-size)                                                                                                                                       | 修正済み     | The default value is changed from 144 MB to `region-split-size / 2 * 3`.                                                                      |
| TiKV           | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)                                                                                                     | 新しく追加された | リージョンをバケットと呼ばれる小さな範囲に分割するかどうかを決定します。                                                                                                          |
| TiKV           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                                                                         | 新しく追加された | The size of a bucket when `enable-region-bucket` is true.                                                                                     |
| TiKV           | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size)                                                                                                                   | 新しく追加された | ローカルにキャッシュされるタイムスタンプの最小数。                                                                                                                     |
| TiKV           | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval)                                                                                                                               | 新しく追加された | The interval at which the locally cached timestamps are refreshed.                                                                            |
| TiKV           | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-new-in-v610)                                                                                                     | 新しく追加された | スナップショット ファイルのサイズがこの値を超えると、スナップショット ファイルは複数のファイルに分割されます。                                                                                      |
| TiKV           | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit)                                                                                                                                 | 新しく追加された | Raft Engineのメモリ使用量の制限を指定します。                                                                                                                  |
| TiKV           | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610)                                                                                 | 新しく追加された | The maximum recovery time is allowed after RocksDB detects a recoverable background error.                                                    |
| TiKV           | [`storage.api-version`](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                           | 新しく追加された | TiKV が生のキー値ストアとして機能するときに TiKV によって使用されるstorage形式とインターフェース バージョン。                                                                              |
| PD             | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-new-in-v610)                                                                                                  | 新しく追加された | ストアがオンラインになるまでの最大待機時間を制御します。                                                                                                                  |
| TiCDC          | [`enable-tls`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                             | 新しく追加された | ダウンストリーム Kafka インスタンスに接続するために TLS を使用するかどうか。                                                                                                  |
| TiCDC          | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新しく追加された | Kafka の SASL/GSSAPI 認証をサポートするために使用されます。詳細については[`kafka`でシンクURIを設定する](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)参照してください。      |
| TiCDC          | [`avro-decimal-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)      | 新しく追加された | Determines the output details of Avro format.                                                                                                 |
| TiCDC          | [`dispatchers.topic`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                             | 新しく追加された | TiCDC が増分データをさまざまな Kafka トピックに送信する方法を制御します。                                                                                                   |
| TiCDC          | [`dispatchers.partition`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                         | 新しく追加された | `dispatchers.partition`は`dispatchers.dispatcher`の別名です。TiCDC が増分データを Kafka パーティションに送信する方法を制御します。                                               |
| TiCDC          | [`schema-registry`](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-kafka-connect-confluent-platform)                                                                                               | 新しく追加された | Avro スキーマを保存するスキーマ レジストリ エンドポイントを指定します。                                                                                                       |
| DM             | `dmctl start-relay`コマンドの`worker`                                                                                                                                                                       | 削除済み     | このパラメータの使用は推奨されません。よりシンプルな実装を提供します。                                                                                                           |
| DM             | `relay-dir` in the source configuration file                                                                                                                                                           | 削除済み     | ワーカー構成ファイル内の同じ構成項目に置き換えられます。                                                                                                                  |
| DM             | タスク設定ファイル内の`is-sharding`                                                                                                                                                                               | 削除済み     | `shard-mode`構成項目に置き換えられました。                                                                                                                   |
| DM             | タスク設定ファイル内の`auto-fix-gtid`                                                                                                                                                                             | 削除済み     | v5.x では非推奨となり、v6.1.0 では正式に削除されました。                                                                                                            |
| DM             | ソース構成ファイルの`meta-dir`と`charset`                                                                                                                                                                         | 削除済み     | Deprecated in v5.x and officially deleted in v6.1.0.                                                                                          |

### その他 {#others}

-   プリペアドプランキャッシュをデフォルトで有効にする

    新しいクラスターでは、 プリペアドプランキャッシュがデフォルトで有効化され、リクエストの`Prepare` `Execute`実行プランをキャッシュします。以降の実行では、クエリプランの最適化をスキップできるため、パフォーマンスが向上します。アップグレードされたクラスターは、設定ファイルから設定を継承します。新しいクラスターは新しいデフォルト値を使用するため、 プリペアドプランキャッシュ はデフォルトで有効化され、各セッションで最大100プランをキャッシュできます ( `capacity=100` )。この機能のメモリ消費量については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)参照してください。

-   TiDB v6.1.0より前のバージョンでは、 `SHOW ANALYZE STATUS`インスタンスレベルのタスクを示し、タスクレコードはTiDBの再起動後に消去されます。TiDB v6.1.0以降では、 `SHOW ANALYZE STATUS`クラスタレベルのタスクを示し、タスクレコードは再起動後も保持されます。5 `tidb_analyze_version = 2`場合、 `Job_info`列に`analyze option`情報が追加されます。

-   TiKV内のSSTファイルが破損すると、TiKVプロセスがpanicになる可能性があります。TiDB v6.1.0より前では、SSTファイルが破損するとTiKVは直ちにpanic状態になりました。TiDB v6.1.0以降では、SSTファイルが破損してから1時間後にTiKVプロセスがpanicになります。

-   次の TiKV 構成項目は[値を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)サポートします。

    -   `raftstore.raft-entry-max-size`
    -   `quota.foreground-cpu-time`
    -   `quota.foreground-write-bandwidth`
    -   `quota.foreground-read-bandwidth`
    -   `quota.max-delay-duration`
    -   `server.grpc-memory-pool-quota`
    -   `server.max-grpc-send-msg-len`
    -   `server.raft-msg-max-batch-size`

-   v6.1.0では、一部の構成ファイルパラメータがシステム変数に変換されます。以前のバージョンからv6.1.0クラスターにアップグレード（オンラインおよびオフラインアップグレードを含む）する場合は、以下の点にご注意ください。

    -   アップグレード前に設定ファイルに指定された設定項目が既に存在する場合、TiDBはアップグレードプロセス中に、設定された項目の値を対応するシステム変数の値に自動的に更新します。これにより、パラメータの最適化により、アップグレード後もシステムの動作は変わりません。
    -   上記の自動更新はアップグレード中に1回のみ実行されます。アップグレード後は、廃止された設定項目は無効になります。

-   ダッシュボード ページはDM WebUIから削除されます。

-   `dispatchers.topic`と`dispatchers.partition`有効になっている場合、TiCDC を v6.1.0 より前のバージョンにダウングレードすることはできません。

-   Avro プロトコルを使用するTiCDC Changefeed は、v6.1.0 より前のバージョンにダウングレードできません。

## Improvements {#improvements}

-   TiDB

    -   `UnionScanRead`オペレータ[#32433](https://github.com/pingcap/tidb/issues/32433)のパフォーマンスを向上させる
    -   `EXPLAIN`の出力におけるタスクタイプの表示を改善（MPPタスクタイプを追加） [＃33332](https://github.com/pingcap/tidb/issues/33332)
    -   列[＃10377](https://github.com/pingcap/tidb/issues/10377)のデフォルト値として`rand()`使用することをサポートします
    -   列[＃33870](https://github.com/pingcap/tidb/issues/33870)のデフォルト値として`uuid()`使用することをサポートします
    -   Support modifying the character set of columns from `latin1` to `utf8`/`utf8mb4` [＃34008](https://github.com/pingcap/tidb/issues/34008)

-   TiKV

    -   インメモリ悲観的ロック[＃12279](https://github.com/tikv/tikv/issues/12279)使用時の CDC の古い値のヒット率を改善
    -   ヘルスチェックを改善して、利用できないRaftstoreを検出し、TiKV クライアントがリージョンキャッシュを時間内に更新できるようにします[＃12398](https://github.com/tikv/tikv/issues/12398)
    -   Raft Engine [＃12255](https://github.com/tikv/tikv/issues/12255)のメモリ制限設定をサポート
    -   TiKVは、破損したSSTファイルを自動的に検出して削除し、製品の可用性を向上させます[＃10578](https://github.com/tikv/tikv/issues/10578)
    -   CDCはRawKV [＃11965](https://github.com/tikv/tikv/issues/11965)をサポートしています
    -   Support splitting a large snapshot file into multiple files [＃11595](https://github.com/tikv/tikv/issues/11595)
    -   スナップショットGCがRaftstoreのメッセージループをブロックするのを防ぐために、スナップショットガベージコレクションをRaftstoreからバックグラウンドスレッドに移動します[＃11966](https://github.com/tikv/tikv/issues/11966)
    -   gPRCメッセージの最大メッセージ長（ `max-grpc-send-msg-len` ）と最大バッチサイズ（ `raft-msg-max-batch-size` ） [＃12334](https://github.com/tikv/tikv/issues/12334)の動的設定をサポート
    -   Raft [＃10483](https://github.com/tikv/tikv/issues/10483)によるオンラインの安全でない復元計画の実行をサポート

-   PD
    -   リージョンラベル[＃4694](https://github.com/tikv/pd/issues/4694)の Time-to-Live (TTL) をサポート
    -   サポートリージョンバケット[＃4668](https://github.com/tikv/pd/issues/4668)
    -   デフォルトでSwaggerサーバーのコンパイルを無効にする[#4932](https://github.com/tikv/pd/issues/4932)

-   TiFlash

    -   集約演算子のメモリ計算を最適化して、マージフェーズ[＃4451](https://github.com/pingcap/tiflash/issues/4451)でより効率的なアルゴリズムが使用されるようにします。

-   Tools

    -   バックアップと復元 (BR)

        -   空のデータベースのバックアップと復元をサポート[＃33866](https://github.com/pingcap/tidb/issues/33866)

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させます[#33618](https://github.com/pingcap/tidb/issues/33618)

    -   TiCDC

        -   TiCDCは、レプリケーション中に大規模なトランザクションを分割することをサポートしており、これにより、大規模なトランザクションによって発生するレプリケーションのレイテンシーが大幅に短縮されます[＃5280](https://github.com/pingcap/tiflow/issues/5280)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `in`関数が`bit`タイプのデータを処理する際に発生する可能性のあるpanicの問題を修正しました[＃33070](https://github.com/pingcap/tidb/issues/33070)
    -   `UnionScan`演算子が順序を維持できないために間違ったクエリ結果が発生する問題を修正[＃33175](https://github.com/pingcap/tidb/issues/33175)
    -   特定のケースで Merge Join 演算子が間違った結果を返す問題を修正[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   動的プルーニングモード[＃33231](https://github.com/pingcap/tidb/issues/33231)で`index join`結果が間違っている可能性がある問題を修正しました
    -   パーティションテーブルの一部のパーティションが削除されたときにデータがガベージコレクションされない可能性がある問題を修正[＃33620](https://github.com/pingcap/tidb/issues/33620)
    -   クラスターのPDノードが交換された後、一部のDDL文が一定期間スタックする可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルへのクエリ実行時に TiDBサーバーのメモリが発生する問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)でスロークエリをチェックすると発生する可能性があります。
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[＃31422](https://github.com/pingcap/tidb/issues/31422)
    -   TopSQLモジュール[＃34525](https://github.com/pingcap/tidb/issues/34525) [＃34502](https://github.com/pingcap/tidb/issues/34502)のメモリリークの問題を修正
    -   PointGetプラン[＃32371](https://github.com/pingcap/tidb/issues/32371)でプランキャッシュが間違っている可能性がある問題を修正しました
    -   RC分離レベル[＃34447](https://github.com/pingcap/tidb/issues/34447)でプランキャッシュが開始されるとクエリ結果が間違っている可能性がある問題を修正しました

-   TiKV

    -   TiKVインスタンスがオフラインになったときにRaftログの遅延が増加する問題を修正[＃12161](https://github.com/tikv/tikv/issues/12161)
    -   Fix the issue that TiKV panics and destroys peers unexpectedly because the target Region to be merged is invalid [＃12232](https://github.com/tikv/tikv/issues/12232)
    -   v5.3.1 または v5.4.0 から v6.0.0 以降のバージョンにアップグレードするときに TiKV が`failed to load_latest_options`エラーを報告する問題を修正しました[＃12269](https://github.com/tikv/tikv/issues/12269)
    -   メモリリソースが不足しているときにRaftログを追加することによって発生する OOM の問題を修正しました[#11379](https://github.com/tikv/tikv/issues/11379)
    -   Fix the issue of TiKV panic caused by the race between destroying peers and batch splitting Regions [＃12368](https://github.com/tikv/tikv/issues/12368)
    -   `stats_monitor`デッドループに陥った後、短時間で TiKVメモリ使用量が急増する問題を修正[＃12416](https://github.com/tikv/tikv/issues/12416)
    -   Follower Read [＃12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正しました

-   PD

    -   `not leader` [＃4797](https://github.com/tikv/pd/issues/4797)の間違ったステータスコードを修正
    -   Fix a bug of TSO fallback in some corner cases [＃4884](https://github.com/tikv/pd/issues/4884)
    -   PDリーダー移転後に削除した墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー移行後すぐにスケジュールを開始できない問題を修正[＃4769](https://github.com/tikv/pd/issues/4769)

-   TiDBダッシュボード

    -   Top SQL機能が有効になる前に実行されていた SQL 文の CPU オーバーヘッドをTop SQLが収集できないバグを修正[＃33859](https://github.com/pingcap/tidb/issues/33859)

-   TiFlash

    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータの不整合を修正[＃4956](https://github.com/pingcap/tiflash/issues/4956)

-   ツール

    -   TiCDC

        -   DDLスキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正[＃1386](https://github.com/pingcap/tiflow/issues/1386)
        -   特別な増分スキャンシナリオで発生するデータ損失を修正[＃5468](https://github.com/pingcap/tiflow/issues/5468)

    -   TiDB データ移行 (DM)

        -   `start-time`タイムゾーンの問題を修正し、DM の動作をダウンストリーム タイムゾーンの使用からアップストリーム タイムゾーンの使用に変更します[＃5471](https://github.com/pingcap/tiflow/issues/5471)
        -   タスクが自動的に再開された後にDMがより多くのディスクスペースを占有する問題を修正[＃3734](https://github.com/pingcap/tiflow/issues/3734) [＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   チェックポイントフラッシュにより失敗した行のデータがスキップされる可能性がある問題を修正[＃5279](https://github.com/pingcap/tiflow/issues/5279)
        -   Fix the issue that in some cases manually executing the filtered DDL in the downstream might cause task resumption failure [＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `case-sensitive: true`が設定されていない場合、大文字テーブルを複製できない問題を修正[＃5255](https://github.com/pingcap/tiflow/issues/5255)
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーpanicの問題を修正しました。
        -   GTID が有効になっているときやタスクが自動的に再開されたときに CPU 使用率が上昇し、大量のログが出力される問題を修正しました[＃5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM WebUI [＃4993](https://github.com/pingcap/tiflow/issues/4993)のオフライン オプションとその他の使用上の問題を修正しました
        -   アップストリーム[＃3731](https://github.com/pingcap/tiflow/issues/3731)でGTIDが空の場合に増分タスクの開始に失敗する問題を修正
        -   空の設定により dm-master がpanicを起こす可能性がある問題を修正[＃3732](https://github.com/pingcap/tiflow/issues/3732)

    -   TiDB Lightning

        -   事前チェックでローカルディスクリソースとクラスターの可用性がチェックされない問題を修正[＃34213](https://github.com/pingcap/tidb/issues/34213)
        -   スキーマ[＃33381](https://github.com/pingcap/tidb/issues/33381)ルーティングが正しくない問題を修正しました
        -   TiDB LightningがパニックになったときにPD構成が正しく復元されない問題を修正[＃31733](https://github.com/pingcap/tidb/issues/31733)
        -   Fix the issue of Local-backend import failure caused by out-of-bounds data in the `auto_increment` column [＃27937](https://github.com/pingcap/tidb/issues/27937)
        -   Fix the issue of local backend import failure when the `auto_random` or `auto_increment` column is null [＃34208](https://github.com/pingcap/tidb/issues/34208)

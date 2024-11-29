---
title: TiDB 6.1.0 Release Notes
summary: TiDB 6.1.0 の新機能、互換性の変更、改善、バグ修正について説明します。
---

# TiDB 6.1.0 リリースノート {#tidb-6-1-0-release-notes}

発売日: 2022年6月13日

TiDB バージョン: 6.1.0

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.1/quick-start-with-tidb) | [実稼働環境への導入](https://docs.pingcap.com/tidb/v6.1/production-deployment-using-tiup)

6.1.0 の主な新機能または改善点は次のとおりです。

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になり、 MySQL 5.7と互換性を持つようになりました。
-   TiFlashパーティションテーブル(動的プルーニング) が GA に
-   ユーザーレベルのロック管理をサポートし、MySQLと互換性があります
-   非トランザクションDMLステートメントをサポート（ `DELETE`のみサポート）
-   TiFlashはオンデマンドのデータ圧縮をサポート
-   MPPはウィンドウ関数フレームワークを導入する
-   TiCDC は Avro 経由で Kafka への変更ログの複製をサポートします
-   TiCDCはレプリケーション中に大規模なトランザクションを分割することをサポートしており、これにより大規模なトランザクションによって発生するレプリケーションのレイテンシーが大幅に短縮されます。
-   シャードされたテーブルをマージおよび移行するための楽観的モードが GA になりました

## 新機能 {#new-features}

### 構文 {#sql}

-   List パーティショニングとリスト COLUMNS パーティショニングが GA になりました。どちらもMySQL 5.7と互換性があります。

    ユーザードキュメント: [List パーティショニング](/partitioned-table.md#list-partitioning) 、 [List COLUMNS パーティショニング](/partitioned-table.md#list-columns-partitioning)

-   TiFlash は、コンパクト コマンドの開始をサポートしています。 (実験的)

    TiFlash v6.1.0 では、既存のバックグラウンド圧縮メカニズムに基づいて物理データを手動で圧縮する方法を提供する`ALTER TABLE ... COMPACT`ステートメントが導入されています。このステートメントを使用すると、以前の形式のデータを更新し、必要に応じていつでも読み取り/書き込みパフォーマンスを向上させることができます。クラスターを v6.1.0 にアップグレードした後、このステートメントを実行してデータを圧縮することをお勧めします。このステートメントは標準 SQL 構文の拡張であるため、MySQL クライアントと互換性があります。TiFlashのアップグレード以外のシナリオでは、通常、このステートメントを使用する必要はありません。

    [ユーザードキュメント](/sql-statements/sql-statement-alter-table-compact.md) , [＃4145](https://github.com/pingcap/tiflash/issues/4145)

-   TiFlash はウィンドウ関数フレームワークを実装し、次のウィンドウ関数をサポートします。

    -   `RANK()`
    -   `DENSE_RANK()`
    -   `ROW_NUMBER()`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) , [＃33072](https://github.com/pingcap/tidb/issues/33072)

### 可観測性 {#observability}

-   継続的なプロファイリングは、ARMアーキテクチャとTiFlash をサポートします。

    [ユーザードキュメント](/dashboard/continuous-profiling.md)

-   Grafana は、全体的なパフォーマンス診断のためのシステムレベルのエントリを提供するパフォーマンス概要ダッシュボードを追加します。

    TiDB 可視化監視コンポーネントGrafana の新しいダッシュボードであるパフォーマンス概要は、全体的なパフォーマンス診断のためのシステムレベルのエントリを提供します。トップダウンのパフォーマンス分析方法論に従って、パフォーマンス概要ダッシュボードは、データベース時間の内訳に基づいて TiDB パフォーマンス メトリックを再編成し、これらのメトリックを異なる色で表示します。これらの色を確認することで、システム全体のパフォーマンスのボトルネックを一目で特定できるため、パフォーマンス診断時間が大幅に短縮され、パフォーマンス分析と診断が簡素化されます。

    [ユーザードキュメント](/performance-tuning-overview.md)

### パフォーマンス {#performance}

-   カスタマイズされたリージョンサイズをサポート

    v6.1.0 以降では、 [`coprocessor.region-split-size`](/tikv-configuration-file.md#region-split-size)設定してリージョンをより大きなサイズに設定できます。これにより、リージョンの数を効果的に削減し、リージョンの管理を容易にし、クラスターのパフォーマンスと安定性を向上させることができます。

    [ユーザードキュメント](/tune-region-performance.md#use-region-split-size-to-adjust-region-size) , [＃11515](https://github.com/tikv/tikv/issues/11515)

-   同時実行性を高めるためにバケットの使用をサポート (実験的)

    リージョンをより大きなサイズに設定した後、クエリの同時実行性をさらに向上させるために、TiDB では、リージョン内のより小さな範囲であるバケットの概念を導入しています。バケットをクエリ単位として使用すると、リージョンをより大きなサイズに設定した場合に同時クエリのパフォーマンスを最適化できます。バケットをクエリ単位として使用すると、ホットスポット リージョンのサイズを動的に調整して、スケジュールの効率と負荷分散を確保することもできます。この機能は現在、実験的です。実本番環境での使用は推奨されません。

    [ユーザードキュメント](/tune-region-performance.md#use-bucket-to-increase-concurrency) , [＃11515](https://github.com/tikv/tikv/issues/11515)

-   デフォルトのログstorageエンジンとしてRaft Engineを使用する

    v6.1.0 以降、TiDB はログのデフォルトのstorageエンジンとしてRaft Engine を使用します。RocksDB と比較すると、 Raft Engine はTiKV I/O 書き込みトラフィックを最大 40%、CPU 使用率を 10% 削減し、フォアグラウンド スループットを約 5% 向上させ、特定の負荷下でテールレイテンシーを 20% 削減します。

    [ユーザードキュメント](/tikv-configuration-file.md#raft-engine) , [＃95](https://github.com/tikv/raft-engine/issues/95)

-   結合順序のヒント構文をサポートする

    -   `LEADING`ヒントは、指定された順序を結合操作のプレフィックスとして使用するようにオプティマイザーに通知します。結合のプレフィックスが適切であれば、結合の初期段階でデータ量を迅速に削減し、クエリのパフォーマンスを向上させることができます。
    -   `STRAIGHT_JOIN`ヒントは、 `FROM`句のテーブルの順序と一致する順序でテーブルを結合するようにオプティマイザーに通知します。

    これにより、テーブル結合の順序を修正する方法が提供されます。ヒントを適切に使用すると、SQL パフォーマンスとクラスターの安定性を効果的に向上できます。

    ユーザー[＃29932](https://github.com/pingcap/tidb/issues/29932) [`STRAIGHT_JOIN`](/optimizer-hints.md#straight_join) [`LEADING`](/optimizer-hints.md#leadingt1_name--tl_name-)

-   TiFlash はさらに 4 つの関数をサポートしています:

    -   `FROM_DAYS`
    -   `TO_DAYS`
    -   `TO_SECONDS`
    -   `WEEKOFYEAR`

    [ユーザードキュメント](/tiflash/tiflash-supported-pushdown-calculations.md) [＃4679](https://github.com/pingcap/tiflash/issues/4679) [＃4678](https://github.com/pingcap/tiflash/issues/4678) [＃4677](https://github.com/pingcap/tiflash/issues/4677)

-   TiFlash は、動的プルーニング モードでパーティション化されたテーブルをサポートします。

    OLAP シナリオでのパフォーマンスを向上させるために、パーティション テーブルでは動的プルーニング モードがサポートされています。TiDB を v6.0.0 より前のバージョンからアップグレードする場合は、パフォーマンスを最大化するために、既存のパーティション テーブルの統計を手動で更新することをお勧めします (新しいインストールや v6.1.0 へのアップグレード後に作成された新しいパーティションでは必要ありません)。

    [＃3873](https://github.com/pingcap/tiflash/issues/3873) [動的プルーニングモード](/partitioned-table.md#dynamic-pruning-mode) : [MPPモードでパーティションテーブルにアクセスする](/tiflash/use-tiflash-mpp-mode.md#access-partitioned-tables-in-the-mpp-mode)

### 安定性 {#stability}

-   SST 破損からの自動回復

    RocksDB がバックグラウンドで破損した SST ファイルを検出すると、TiKV は影響を受けたピアをスケジュールし、他のレプリカを使用してそのデータを回復しようとします。 `background-error-recovery-window`パラメータを使用して、回復の最大許容時間を設定できます。 回復操作が時間枠内に完了しない場合、TiKV はpanicになります。 この機能により、回復可能な破損したstorageが自動的に検出され、回復されるため、クラスターの安定性が向上します。

    [ユーザードキュメント](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610) , [＃10578](https://github.com/tikv/tikv/issues/10578)

-   非トランザクションDMLステートメントをサポート

    大規模データ処理のシナリオでは、大規模なトランザクションを伴う単一の SQL ステートメントが、クラスターの安定性とパフォーマンスに悪影響を及ぼす可能性があります。v6.1.0 以降、TiDB は、 `DELETE`ステートメントを複数のステートメントに分割してバッチ処理する構文をサポートしています。分割ステートメントはトランザクションの原子性と分離性を損ないますが、クラスターの安定性を大幅に向上させます。詳細な構文については、 [`BATCH`](/sql-statements/sql-statement-batch.md)参照してください。

    [ユーザードキュメント](/non-transactional-dml.md)

-   TiDBは最大GC待機時間の設定をサポートしています

    TiDB のトランザクションは、マルチバージョン同時実行制御 (MVCC) メカニズムを採用しています。新しく書き込まれたデータが古いデータを上書きする場合、古いデータは置き換えられず、両方のバージョンのデータが格納されます。古いデータはガベージ コレクション (GC) タスクによって定期的にクリーンアップされ、storageスペースを再利用してクラスターのパフォーマンスと安定性を向上させるのに役立ちます。GC は、デフォルトでは 10 分ごとにトリガーされます。長時間実行トランザクションが対応する履歴データにアクセスできるようにするために、実行中のトランザクションがある場合は、GC タスクが遅延されます。GC タスクが無期限に遅延されないようにするために、TiDB は GC タスクの最大遅延時間を制御するシステム変数[`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)を導入しています。最大遅延時間を超えると、GC が強制的に実行されます。変数のデフォルト値は 24 時間です。この機能により、GC 待機時間と長時間実行トランザクションの関係を制御でき、クラスターの安定性が向上します。

    [ユーザードキュメント](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)

-   TiDBは、自動統計収集タスクの最大実行時間の設定をサポートしています。

    データベースは統計を収集することでデータの分布を効果的に把握できるため、合理的な実行プランを生成し、SQL 実行の効率を向上させることができます。TiDB は、頻繁に変更されるデータ オブジェクトの統計をバックグラウンドで定期的に収集します。ただし、統計の収集にはクラスター リソースが消費されるため、ビジネス ピーク時にビジネスの安定した運用に影響を及ぼす可能性があります。

    v6.1.0 以降、TiDB はバックグラウンド統計収集の最大実行時間を制御する[`tidb_max_auto_analyze_time`](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)導入しました。これはデフォルトで 12 時間です。アプリケーションがリソースのボトルネックに遭遇しない場合は、TiDB がタイムリーに統計を収集できるように、この変数を変更しないことをお勧めします。

    [ユーザードキュメント](/system-variables.md)

### 使いやすさ {#ease-of-use}

-   複数のレプリカが失われた場合にワンストップのオンラインデータ復旧をサポート

    TiDB v6.1.0 より前では、マシン障害により複数のリージョンレプリカが失われた場合、ユーザーはすべての TiKV サーバーを停止し、 TiKV Controlを使用して TiKV を 1 つずつ回復する必要がありました。TiDB v6.1.0 以降では、回復プロセスは完全に自動化されており、TiKV を停止する必要がなく、オンラインの他のアプリケーションに影響を与えません。回復プロセスはPD Controlを使用してトリガーでき、よりユーザーフレンドリな概要情報が提供されます。

    [ユーザードキュメント](/online-unsafe-recovery.md) , [＃10483](https://github.com/tikv/tikv/issues/10483)

-   履歴統計収集タスクの表示をサポート

    `SHOW ANALYZE STATUS`ステートメントを使用して、クラスター レベルの統計収集タスクを表示できます。TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`ステートメントはインスタンス レベルのタスクのみを表示し、履歴タスク レコードは TiDB の再起動後にクリアされます。そのため、履歴統計収集時間と詳細を表示することはできません。TiDB v6.1.0 以降では、統計収集タスクの履歴レコードは保持され、クラスターの再起動後にクエリを実行できます。これにより、統計の異常によって発生するクエリ パフォーマンスの問題をトラブルシューティングするための参照が提供されます。

    [ユーザードキュメント](/sql-statements/sql-statement-show-analyze-status.md)

-   TiDB、TiKV、 TiFlash構成の動的な変更をサポート

    以前のバージョンの TiDB では、構成項目を変更した後、変更を有効にするためにクラスターを再起動する必要がありました。これにより、オンライン サービスが中断される可能性があります。この問題に対処するために、TiDB v6.1.0 では動的構成機能が導入され、クラスターを再起動せずにパラメーターの変更を検証できるようになりました。具体的な最適化は次のとおりです。

    -   一部の TiDB 構成項目をシステム変数に変換し、動的に変更して永続化できるようにします。変換後は元の構成項目は非推奨になることに注意してください。変換された構成項目の詳細なリストについては、 [コンフィグレーションファイルのパラメータ](#configuration-file-parameters)参照してください。
    -   一部の TiKV パラメータのオンライン設定をサポートします。パラメータの詳細なリストについては、 [その他](#others)参照してください。
    -   TiFlash構成項目`max_threads`システム変数`tidb_max_tiflash_threads`に変換して、構成を動的に変更し、永続化できるようにします。変換後も元の構成項目は残ることに注意してください。

    以前のバージョンからアップグレードされた v6.1.0 クラスター (オンラインおよびオフライン アップグレードを含む) の場合、次の点に注意してください。

    -   アップグレード前に設定ファイルに指定された設定項目がすでに存在する場合、TiDB はアップグレード プロセス中に、設定された項目の値を対応するシステム変数の値に自動的に更新します。これにより、アップグレード後のシステム動作は、パラメータの最適化の影響を受けません。
    -   上記の自動更新は、アップグレード中に 1 回だけ実行されます。アップグレード後は、非推奨の構成項目は有効ではなくなります。

    この機能を使用すると、システムを再起動したりサービスを中断したりすることなく、パラメータを動的に変更し、検証して保持することができます。これにより、日常のメンテナンスが容易になります。

    [ユーザードキュメント](/dynamic-config.md)

-   クエリや接続をグローバルに強制終了するサポート

    `enable-global-kill`構成 (デフォルトで有効) を使用して、グローバル キル機能を制御できます。

    TiDB v6.1.0 より前では、操作が大量のリソースを消費し、クラスターの安定性の問題を引き起こす場合、対象の TiDB インスタンスに接続してから`KILL TIDB ${id};`コマンドを実行して対象の接続と操作を終了する必要がありました。多くの TiDB インスタンスの場合、この方法は使いにくく、誤った操作が発生しやすいです。v6.1.0 以降では、 `enable-global-kill`構成が導入され、デフォルトで有効になっています。クライアントと TiDB の間にプロキシがある場合、誤って他のクエリやセッションを誤って終了することを心配することなく、任意の TiDB インスタンスで kill コマンドを実行して、指定した接続と操作を終了できます。現在、TiDB は Ctrl+C を使用してクエリまたはセッションを終了することをサポートしていません。

    [ユーザードキュメント](/tidb-configuration-file.md#enable-global-kill-new-in-v610) , [＃8854](https://github.com/pingcap/tidb/issues/8854)

-   TiKV API V2 (実験的)

    v6.1.0 より前では、TiKV が Raw Key Valuestorageとして使用される場合、TiKV はクライアントから渡された生データのみを保存するため、基本的な Key Value の読み取りおよび書き込み機能のみを提供します。

    TiKV API V2 は、次のような新しい Raw Key Valuestorage形式とアクセス インターフェイスを提供します。

    -   データは MVCC に保存され、データの変更タイムスタンプが記録されます。この機能は、変更データ キャプチャと増分バックアップおよび復元を実装するための基盤となります。
    -   データはさまざまな用途に応じてスコープ設定され、単一の TiDB クラスター、トランザクション KV、RawKV アプリケーションの共存をサポートします。

    <Warning>

    基盤となるstorage形式が大幅に変更されたため、API V2 を有効にした後は、TiKV クラスターを v6.1.0 より前のバージョンにロールバックすることはできません。TiKV をダウングレードすると、データが破損する可能性があります。

    </Warning>

    [ユーザードキュメント](/tikv-configuration-file.md#api-version-new-in-v610) , [＃11745](https://github.com/tikv/tikv/issues/11745)

### MySQL 互換性 {#mysql-compatibility}

-   MySQL のユーザーレベルロック管理との互換性をサポート

    ユーザーレベル ロックは、MySQL が組み込み関数を通じて提供する、ユーザーが命名するロック管理システムです。ロック関数は、ロックのブロック、待機、およびその他のロック管理機能を提供できます。ユーザーレベル ロックは、Rails、Elixir、Ecto などの ORM フレームワークでも広く使用されています。TiDB は、v6.1.0 以降、MySQL 互換のユーザーレベル ロック管理をサポートしており、 `GET_LOCK` 、および`RELEASE_ALL_LOCKS` `RELEASE_LOCK`をサポートしています。

    [ユーザードキュメント](/functions-and-operators/locking-functions.md) , [＃14994](https://github.com/pingcap/tidb/issues/14994)

### データ移行 {#data-migration}

-   シャードされたテーブルをマージおよび移行するための楽観的モードが GA になりました

    DM は、楽観的モードでシャード テーブルからデータをマージおよび移行するタスクのシナリオ テストを多数追加し、日常的な使用シナリオの 90% をカバーします。悲観的モードと比較すると、楽観的モードはよりシンプルで効率的に使用できます。使用上の注意をよく理解した上で、楽観的的モードを使用することをお勧めします。

    [ユーザードキュメント](/dm/feature-shard-merge-optimistic.md#restrictions)

-   DM WebUIは指定されたパラメータに従ってタスクを開始することをサポートします

    移行タスクを開始するときに、開始時刻とセーフ モードの期間を指定できます。これは、多数のソースを含む増分移行タスクを作成する場合に特に役立ち、ソースごとにbinlog の開始位置を指定する必要がなくなります。

    [ユーザードキュメント](/dm/dm-webui-guide.md) , [＃5442](https://github.com/pingcap/tiflow/issues/5442)

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiDBはさまざまなサードパーティのデータエコシステムとのデータ共有をサポートします

    -   TiCDC は、TiDB 増分データを Avro 形式で Kafka に送信することをサポートしており、Confluent を介して KSQL や Snowflake などのサードパーティとデータを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-avro-protocol.md) , [＃5338](https://github.com/pingcap/tiflow/issues/5338)

    -   TiCDC は、テーブルごとに TiDB からさまざまな Kafka トピックに増分データをディスパッチすることをサポートしており、Canal-json 形式と組み合わせることで、Flink と直接データを共有できます。

        [ユーザードキュメント](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink) , [＃4423](https://github.com/pingcap/tiflow/issues/4423)

    -   TiCDC は SASL GSSAPI 認証タイプをサポートし、Kafka を使用した SASL 認証の例を追加します。

        [ユーザードキュメント](/ticdc/ticdc-sink-to-kafka.md#ticdc-uses-the-authentication-and-authorization-of-kafka) , [＃4423](https://github.com/pingcap/tiflow/issues/4423)

-   TiCDC は`charset=GBK`テーブルの複製をサポートします。

    [ユーザードキュメント](/character-set-gbk.md#component-compatibility) , [＃4806](https://github.com/pingcap/tiflow/issues/4806)

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                           | タイプを変更   | 説明                                                                                                                                          |
| ----------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| [`tidb_enable_list_partition`](/system-variables.md#tidb_enable_list_partition-new-in-v50)                                    | 修正済み     | デフォルト値は`OFF`から`ON`に変更されます。                                                                                                                  |
| [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)                                                           | 修正済み     | この変数は GLOBAL スコープを追加し、変数の値はクラスターに保持されます。                                                                                                    |
| [`tidb_query_log_max_len`](/system-variables.md#tidb_query_log_max_len)                                                       | 修正済み     | 変数のスコープが INSTANCE から GLOBAL に変更されます。変数の値はクラスターに保持され、値の範囲は`[0, 1073741824]`に変更されます。                                                          |
| [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610)                                       | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `security.require-secure-transport` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                       |
| [`tidb_committer_concurrency`](/system-variables.md#tidb_committer_concurrency-new-in-v610)                                   | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `performance.committer-concurrency` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                       |
| [`tidb_enable_auto_analyze`](/system-variables.md#tidb_enable_auto_analyze-new-in-v610)                                       | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `run-auto-analyze` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                                        |
| [`tidb_enable_new_only_full_group_by_check`](/system-variables.md#tidb_enable_new_only_full_group_by_check-new-in-v610)       | 新しく追加された | この変数は、TiDB が`ONLY_FULL_GROUP_BY`チェックを実行するときの動作を制御します。                                                                                       |
| [`tidb_enable_outer_join_reorder`](/system-variables.md#tidb_enable_outer_join_reorder-new-in-v610)                           | 新しく追加された | v6.1.0 以降、TiDB の結合したテーブルの再配置アルゴリズムは外部結合をサポートしています。この変数はサポート動作を制御し、デフォルト値は`ON`です。                                                            |
| [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)                         | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.enabled` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                             |
| [`tidb_gc_max_wait_time`](/system-variables.md#tidb_gc_max_wait_time-new-in-v610)                                             | 新しく追加された | この変数は、コミットされていないトランザクションによってブロックされる GC セーフ ポイントの最大時間を設定するために使用されます。                                                                         |
| [tidb_max_auto_analyze_time](/system-variables.md#tidb_max_auto_analyze_time-new-in-v610)                                     | 新しく追加された | この変数は、auto analyzeの最大実行時間を指定するために使用されます。                                                                                                    |
| [`tidb_max_tiflash_threads`](/system-variables.md#tidb_max_tiflash_threads-new-in-v610)                                       | 新しく追加された | この変数は、 TiFlash がリクエストを実行するための最大同時実行数を設定するために使用されます。                                                                                         |
| [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-new-in-v610)                                                 | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `oom-action` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                                              |
| [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-new-in-v610)                                           | 新しく追加された | この変数は、ユーザーによる手動実行[`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md)や TiDB バックグラウンドでの自動分析タスクなど、TiDB が統計を更新する際の最大メモリ使用量を制御します。 |
| [`tidb_nontransactional_ignore_error`](/system-variables.md#tidb_nontransactional_ignore_error-new-in-v610)                   | 新しく追加された | この変数は、非トランザクション DML ステートメントでエラーが発生したときに、すぐにエラーを返すかどうかを指定します。                                                                                |
| [`tidb_prepared_plan_cache_memory_guard_ratio`](/system-variables.md#tidb_prepared_plan_cache_memory_guard_ratio-new-in-v610) | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.memory-guard-ratio` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                  |
| [`tidb_prepared_plan_cache_size`](/system-variables.md#tidb_prepared_plan_cache_size-new-in-v610)                             | 新しく追加された | この設定は以前は`tidb.toml`オプション ( `prepared-plan-cache.capacity` ) でしたが、TiDB v6.1.0 以降ではシステム変数に変更されました。                                            |
| [`tidb_stats_cache_mem_quota`](/system-variables.md#tidb_stats_cache_mem_quota-new-in-v610)                                   | 新しく追加された | この変数は、TiDB 統計キャッシュのメモリクォータを設定します。                                                                                                           |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                             | タイプを変更   | 説明                                                                                                                                                       |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | `committer-concurrency`                                                                                                                                                                                | 削除されました  | システム変数`tidb_committer_concurrency`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                           |
| ティビ            | `lower-case-table-names`                                                                                                                                                                               | 削除されました  | 現在、TiDB は`lower_case_table_name=2`のみをサポートしています。別の値が設定されている場合は、クラスターを v6.1.0 にアップグレードした後にその値は失われます。                                                       |
| ティビ            | `mem-quota-query`                                                                                                                                                                                      | 削除されました  | システム変数`tidb_mem_quota_query`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                                 |
| ティビ            | `oom-action`                                                                                                                                                                                           | 削除されました  | システム変数`tidb_mem_oom_action`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                                  |
| ティビ            | `prepared-plan-cache.capacity`                                                                                                                                                                         | 削除されました  | システム変数`tidb_prepared_plan_cache_size`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                        |
| ティビ            | `prepared-plan-cache.enabled`                                                                                                                                                                          | 削除されました  | システム変数`tidb_enable_prepared_plan_cache`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                      |
| ティビ            | `query-log-max-len`                                                                                                                                                                                    | 削除されました  | システム変数`tidb_query_log_max_len`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                               |
| ティビ            | `require-secure-transport`                                                                                                                                                                             | 削除されました  | システム変数`require_secure_transport`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                             |
| ティビ            | `run-auto-analyze`                                                                                                                                                                                     | 削除されました  | システム変数`tidb_enable_auto_analyze`に置き換えられました。この構成項目は無効になりました。値を変更する場合は、対応するシステム変数を変更する必要があります。                                                             |
| ティビ            | [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610)                                                                                                                     | 新しく追加された | Global Kill (インスタンス間のクエリまたは接続の終了) 機能を有効にするかどうかを制御します。値が`true`の場合、 `KILL`と`KILL TIDB`両方のステートメントでインスタンス間のクエリまたは接続を終了できるため、クエリまたは接続が誤って終了することを心配する必要はありません。 |
| ティビ            | [`enable-stats-cache-mem-quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-new-in-v610)                                                                                                 | 新しく追加された | 統計キャッシュのメモリクォータを有効にするかどうかを制御します。                                                                                                                         |
| ティクヴ           | [`raft-engine.enable`](/tikv-configuration-file.md#enable-1)                                                                                                                                           | 修正済み     | デフォルト値は`FALSE`から`TRUE`に変更されます。                                                                                                                           |
| ティクヴ           | [`region-max-keys`](/tikv-configuration-file.md#region-max-keys)                                                                                                                                       | 修正済み     | デフォルト値は 1440000 から`region-split-keys / 2 * 3`に変更されます。                                                                                                    |
| ティクヴ           | [`region-max-size`](/tikv-configuration-file.md#region-max-size)                                                                                                                                       | 修正済み     | デフォルト値は 144 MB から`region-split-size / 2 * 3`に変更されます。                                                                                                     |
| ティクヴ           | [`coprocessor.enable-region-bucket`](/tikv-configuration-file.md#enable-region-bucket-new-in-v610)                                                                                                     | 新しく追加された | リージョンをバケットと呼ばれるより小さな範囲に分割するかどうかを決定します。                                                                                                                   |
| ティクヴ           | [`coprocessor.region-bucket-size`](/tikv-configuration-file.md#region-bucket-size-new-in-v610)                                                                                                         | 新しく追加された | `enable-region-bucket`が true の場合のバケットのサイズ。                                                                                                               |
| ティクヴ           | [`causal-ts.renew-batch-min-size`](/tikv-configuration-file.md#renew-batch-min-size)                                                                                                                   | 新しく追加された | ローカルにキャッシュされるタイムスタンプの最小数。                                                                                                                                |
| ティクヴ           | [`causal-ts.renew-interval`](/tikv-configuration-file.md#renew-interval)                                                                                                                               | 新しく追加された | ローカルにキャッシュされたタイムスタンプが更新される間隔。                                                                                                                            |
| ティクヴ           | [`max-snapshot-file-raw-size`](/tikv-configuration-file.md#max-snapshot-file-raw-size-new-in-v610)                                                                                                     | 新しく追加された | スナップショット ファイルのサイズがこの値を超えると、スナップショット ファイルは複数のファイルに分割されます。                                                                                                 |
| ティクヴ           | [`raft-engine.memory-limit`](/tikv-configuration-file.md#memory-limit)                                                                                                                                 | 新しく追加された | Raft Engineのメモリ使用量の制限を指定します。                                                                                                                             |
| ティクヴ           | [`storage.background-error-recovery-window`](/tikv-configuration-file.md#background-error-recovery-window-new-in-v610)                                                                                 | 新しく追加された | RocksDB が回復可能なバックグラウンド エラーを検出した後、最大回復時間が許可されます。                                                                                                          |
| ティクヴ           | [`storage.api-version`](/tikv-configuration-file.md#api-version-new-in-v610)                                                                                                                           | 新しく追加された | TiKV が生のキー値ストアとして機能する場合に TiKV によって使用されるstorage形式とインターフェース バージョン。                                                                                         |
| PD             | [`schedule.max-store-preparing-time`](/pd-configuration-file.md#max-store-preparing-time-new-in-v610)                                                                                                  | 新しく追加された | ストアがオンラインになるまでの最大待機時間を制御します。                                                                                                                             |
| ティCDC          | [`enable-tls`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)                                                                                                                             | 新しく追加された | ダウンストリーム Kafka インスタンスに接続するために TLS を使用するかどうか。                                                                                                             |
| ティCDC          | `sasl-gssapi-user`<br/>`sasl-gssapi-password`<br/>`sasl-gssapi-auth-type`<br/>`sasl-gssapi-service-name`<br/>`sasl-gssapi-realm`<br/>`sasl-gssapi-key-tab-path`<br/>`sasl-gssapi-kerberos-config-path` | 新しく追加された | Kafka の SASL/GSSAPI 認証をサポートするために使用されます。詳細については、 [`kafka`でシンク URI を設定する](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)参照してください。             |
| ティCDC          | [`avro-decimal-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)<br/>[`avro-bigint-unsigned-handling-mode`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)      | 新しく追加された | Avro 形式の出力の詳細を決定します。                                                                                                                                     |
| ティCDC          | [`dispatchers.topic`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                             | 新しく追加された | TiCDC が増分データをさまざまな Kafka トピックに送信する方法を制御します。                                                                                                              |
| ティCDC          | [`dispatchers.partition`](/ticdc/ticdc-sink-to-kafka.md#customize-the-rules-for-topic-and-partition-dispatchers-of-kafka-sink)                                                                         | 新しく追加された | `dispatchers.partition`は`dispatchers.dispatcher`の別名です。TiCDC が増分データを Kafka パーティションに送信する方法を制御します。                                                          |
| ティCDC          | [`schema-registry`](/ticdc/ticdc-sink-to-kafka.md#integrate-ticdc-with-kafka-connect-confluent-platform)                                                                                               | 新しく追加された | Avro スキーマを保存するスキーマ レジストリ エンドポイントを指定します。                                                                                                                  |
| DM             | `dmctl start-relay`コマンドの`worker`                                                                                                                                                                       | 削除されました  | このパラメータの使用は推奨されません。より簡単な実装を提供します。                                                                                                                        |
| DM             | ソース構成ファイル内の`relay-dir`                                                                                                                                                                                 | 削除されました  | ワーカー構成ファイル内の同じ構成項目に置き換えられます。                                                                                                                             |
| DM             | タスク設定ファイル内の`is-sharding`                                                                                                                                                                               | 削除されました  | `shard-mode`の構成項目に置き換えられます。                                                                                                                              |
| DM             | タスク設定ファイル内の`auto-fix-gtid`                                                                                                                                                                             | 削除されました  | v5.x では非推奨となり、v6.1.0 では正式に削除されました。                                                                                                                       |
| DM             | ソース構成ファイルの`meta-dir`と`charset`                                                                                                                                                                         | 削除されました  | v5.x では非推奨となり、v6.1.0 では正式に削除されました。                                                                                                                       |

### その他 {#others}

-   プリペアドプランキャッシュをデフォルトで有効にする

    新しいクラスターでは、プリペアドプランキャッシュがデフォルトで有効になっており、 `Prepare` / `Execute`リクエストの実行プランをキャッシュします。後続の実行では、クエリ プランの最適化をスキップできるため、パフォーマンスが向上します。アップグレードされたクラスターは、構成ファイルから構成を継承します。新しいクラスターは新しいデフォルト値を使用するため、プリペアドプランキャッシュはデフォルトで有効になっており、各セッションで最大 100 のプランをキャッシュできます ( `capacity=100` )。この機能のメモリ消費量については、 [プリペアドプランキャッシュのメモリ管理](/sql-prepared-plan-cache.md#memory-management-of-prepared-plan-cache)参照してください。

-   TiDB v6.1.0 より前では、 `SHOW ANALYZE STATUS`インスタンス レベルのタスクを示し、タスク レコードは TiDB の再起動後にクリアされます。TiDB v6.1.0 以降では、 `SHOW ANALYZE STATUS`クラスター レベルのタスクを示し、タスク レコードは再起動後も保持されます。 `tidb_analyze_version = 2`の場合、 `Job_info`列に`analyze option`情報が追加されます。

-   TiKV 内の破損した SST ファイルにより、TiKV プロセスがpanicになる可能性があります。TiDB v6.1.0 より前では、破損した SST ファイルにより、TiKV は直ちにpanicになりました。TiDB v6.1.0 以降では、SST ファイルが破損してから 1 時間後に TiKV プロセスがpanicになります。

-   次の TiKV 構成項目は[値を動的に変更する](/dynamic-config.md#modify-tikv-configuration-dynamically)サポートします。

    -   `raftstore.raft-entry-max-size`
    -   `quota.foreground-cpu-time`
    -   `quota.foreground-write-bandwidth`
    -   `quota.foreground-read-bandwidth`
    -   `quota.max-delay-duration`
    -   `server.grpc-memory-pool-quota`
    -   `server.max-grpc-send-msg-len`
    -   `server.raft-msg-max-batch-size`

-   v6.1.0 では、一部の構成ファイル パラメータがシステム変数に変換されます。以前のバージョンからアップグレードされた v6.1.0 クラスタ (オンライン アップグレードとオフライン アップグレードを含む) の場合、次の点に注意してください。

    -   アップグレード前に構成ファイルに指定された構成項目がすでに存在する場合、TiDB はアップグレード プロセス中に、構成された項目の値を対応するシステム変数の値に自動的に更新します。このように、アップグレード後、パラメータの最適化によりシステムの動作は変わりません。
    -   上記の自動更新は、アップグレード中に 1 回だけ実行されます。アップグレード後は、非推奨の構成項目は有効ではなくなります。

-   ダッシュボード ページはDM WebUIから削除されます。

-   `dispatchers.topic`と`dispatchers.partition`が有効になっている場合、TiCDC を v6.1.0 より前のバージョンにダウングレードすることはできません。

-   Avro プロトコルを使用するTiCDC Changefeed は、 v6.1.0 より前のバージョンにダウングレードすることはできません。

## 改善点 {#improvements}

-   ティビ

    -   `UnionScanRead`オペレータ[＃32433](https://github.com/pingcap/tidb/issues/32433)のパフォーマンスを向上させる
    -   `EXPLAIN`の出力におけるタスクタイプの表示を改善（MPPタスクタイプを追加） [＃33332](https://github.com/pingcap/tidb/issues/33332)
    -   列[＃10377](https://github.com/pingcap/tidb/issues/10377)のデフォルト値として`rand()`使用をサポート
    -   列[＃33870](https://github.com/pingcap/tidb/issues/33870)のデフォルト値として`uuid()`使用をサポート
    -   列の文字セットを`latin1`から`utf8` `utf8mb4` [＃34008](https://github.com/pingcap/tidb/issues/34008)変更するサポート

-   ティクヴ

    -   インメモリ悲観的ロック[＃12279](https://github.com/tikv/tikv/issues/12279)使用時の CDC の古い値ヒット率の向上
    -   ヘルスチェックを改善して、利用できないRaftstore を検出し、TiKV クライアントが時間内にリージョンキャッシュを更新できるようにします[＃12398](https://github.com/tikv/tikv/issues/12398)
    -   Raft Engine [＃12255](https://github.com/tikv/tikv/issues/12255)のメモリ制限設定をサポート
    -   TiKVは破損したSSTファイルを自動的に検出して削除し、製品の可用性を向上させます[＃10578](https://github.com/tikv/tikv/issues/10578)
    -   CDCはRawKV [＃11965](https://github.com/tikv/tikv/issues/11965)をサポート
    -   大きなスナップショットファイルを複数のファイルに分割するサポート[＃11595](https://github.com/tikv/tikv/issues/11595)
    -   スナップショットGCがRaftstoreのメッセージループをブロックしないように、スナップショットガベージコレクションをRaftstoreからバックグラウンドスレッドに移動します[＃11966](https://github.com/tikv/tikv/issues/11966)
    -   gPRCメッセージの最大メッセージ長（ `max-grpc-send-msg-len` ）と最大バッチサイズ（ `raft-msg-max-batch-size` ） [＃12334](https://github.com/tikv/tikv/issues/12334)の動的設定をサポート
    -   Raft [＃10483](https://github.com/tikv/tikv/issues/10483)によるオンラインの安全でない復元プランの実行をサポート

-   PD
    -   リージョンラベルの存続時間 (TTL) をサポート[＃4694](https://github.com/tikv/pd/issues/4694)
    -   サポートリージョンバケット[＃4668](https://github.com/tikv/pd/issues/4668)
    -   デフォルトで Swaggerサーバーのコンパイルを無効にする[＃4932](https://github.com/tikv/pd/issues/4932)

-   TiFlash

    -   集約演算子のメモリ計算を最適化して、マージフェーズ[＃4451](https://github.com/pingcap/tiflash/issues/4451)でより効率的なアルゴリズムが使用されるようにします。

-   ツール

    -   バックアップと復元 (BR)

        -   空のデータベースのバックアップと復元をサポート[＃33866](https://github.com/pingcap/tidb/issues/33866)

    -   TiDB Lightning

        -   散布リージョンをバッチモードに最適化して、散布リージョンプロセスの安定性を向上させる[＃33618](https://github.com/pingcap/tidb/issues/33618)

    -   ティCDC

        -   TiCDCはレプリケーション中に大規模なトランザクションを分割することをサポートしており、これにより大規模なトランザクションによって発生するレプリケーションのレイテンシーが大幅に短縮されます[＃5280](https://github.com/pingcap/tiflow/issues/5280)

## バグ修正 {#bug-fixes}

-   ティビ

    -   `in`関数が`bit`型データ[＃33070](https://github.com/pingcap/tidb/issues/33070)処理するときに発生する可能性のあるpanicの問題を修正しました
    -   `UnionScan`演算子が順序を維持できないために間違ったクエリ結果が発生する問題を修正[＃33175](https://github.com/pingcap/tidb/issues/33175)
    -   特定のケースで Merge Join 演算子が間違った結果を返す問題を修正[＃33042](https://github.com/pingcap/tidb/issues/33042)
    -   動的プルーニングモード[＃33231](https://github.com/pingcap/tidb/issues/33231)で`index join`結果が間違っている可能性がある問題を修正
    -   パーティションテーブルの一部のパーティションが削除されたときにデータがガベージコレクションされない可能性がある問題を修正[＃33620](https://github.com/pingcap/tidb/issues/33620)
    -   クラスターの PD ノードが置き換えられた後、一部の DDL ステートメントが一定期間停止する可能性がある問題を修正しました[＃33908](https://github.com/pingcap/tidb/issues/33908)
    -   `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY`テーブルをクエリしたときに TiDBサーバーのメモリが不足する可能性がある問題を修正しました。この問題は、Grafana ダッシュボード[＃33893](https://github.com/pingcap/tidb/issues/33893)で遅いクエリをチェックしたときに発生する可能性があります。
    -   システム変数`max_allowed_packet`が有効にならない問題を修正[＃31422](https://github.com/pingcap/tidb/issues/31422)
    -   TopSQLモジュール[＃34525](https://github.com/pingcap/tidb/issues/34525) [＃34502](https://github.com/pingcap/tidb/issues/34502)のメモリリークの問題を修正
    -   PointGetプラン[＃32371](https://github.com/pingcap/tidb/issues/32371)でプランキャッシュが間違っている可能性がある問題を修正
    -   RC分離レベル[＃34447](https://github.com/pingcap/tidb/issues/34447)でプランキャッシュが開始されるとクエリ結果が間違っている可能性がある問題を修正しました

-   ティクヴ

    -   TiKVインスタンスがオフラインになったときにRaftログの遅延が増加する問題を修正[＃12161](https://github.com/tikv/tikv/issues/12161)
    -   マージ対象のリージョンが無効であるため、TiKV がパニックを起こしてピアを予期せず破棄する問題を修正[＃12232](https://github.com/tikv/tikv/issues/12232)
    -   v5.3.1 または v5.4.0 から v6.0.0 以降のバージョンにアップグレードするときに TiKV が`failed to load_latest_options`エラーを報告する問題を修正しました[＃12269](https://github.com/tikv/tikv/issues/12269)
    -   メモリリソースが不足しているときにRaftログを追加することで発生する OOM の問題を修正[＃11379](https://github.com/tikv/tikv/issues/11379)
    -   ピアの破壊とリージョン[＃12368](https://github.com/tikv/tikv/issues/12368)バッチ分割の競合によって発生する TiKVpanicの問題を修正しました。
    -   `stats_monitor`デッドループに陥った後、短時間で TiKVメモリ使用量が急増する問題を修正[＃12416](https://github.com/tikv/tikv/issues/12416)
    -   Follower Read [＃12478](https://github.com/tikv/tikv/issues/12478)使用時に TiKV が`invalid store ID 0`エラーを報告する問題を修正

-   PD

    -   `not leader` [＃4797](https://github.com/tikv/pd/issues/4797)の間違ったステータスコードを修正
    -   いくつかのコーナーケースでの TSO フォールバックのバグを修正[＃4884](https://github.com/tikv/pd/issues/4884)
    -   PDリーダーの移転後に削除された墓石ストアが再び表示される問題を修正[＃4941](https://github.com/tikv/pd/issues/4941)
    -   PDリーダー移行後すぐにスケジュールを開始できない問題を修正[＃4769](https://github.com/tikv/pd/issues/4769)

-   TiDBダッシュボード

    -   Top SQL機能を有効にする前に実行されていた SQL ステートメントの CPU オーバーヘッドをTop SQL が収集できないバグを修正[＃33859](https://github.com/pingcap/tidb/issues/33859)

-   TiFlash

    -   多数のINSERTおよびDELETE操作後に発生する可能性のあるデータの不整合を修正[＃4956](https://github.com/pingcap/tiflash/issues/4956)

-   ツール

    -   ティCDC

        -   DDLスキーマのバッファリング方法を最適化することで過剰なメモリ使用量を修正[＃1386](https://github.com/pingcap/tiflow/issues/1386)
        -   特別な増分スキャンシナリオで発生するデータ損失を修正[＃5468](https://github.com/pingcap/tiflow/issues/5468)

    -   TiDB データ移行 (DM)

        -   `start-time`タイムゾーンの問題を修正し、DM の動作をダウンストリーム タイムゾーンの使用からアップストリーム タイムゾーンの使用に変更します[＃5471](https://github.com/pingcap/tiflow/issues/5471)
        -   タスクが自動的に再開された後にDMがより多くのディスク領域を占有する問題を修正[＃3734](https://github.com/pingcap/tiflow/issues/3734) [＃5344](https://github.com/pingcap/tiflow/issues/5344)
        -   チェックポイントフラッシュにより失敗した行のデータがスキップされる可能性がある問題を修正[＃5279](https://github.com/pingcap/tiflow/issues/5279)
        -   下流でフィルタリングされた DDL を手動で実行すると、タスク再開が失敗する場合がある問題を修正しました[＃5272](https://github.com/pingcap/tiflow/issues/5272)
        -   `case-sensitive: true`が設定されていない場合、大文字テーブルを複製できない問題を修正[＃5255](https://github.com/pingcap/tiflow/issues/5255)
        -   `SHOW CREATE TABLE`ステートメント[＃5159](https://github.com/pingcap/tiflow/issues/5159)によって返されるインデックスの先頭に主キーがない場合に発生する DM ワーカーpanicの問題を修正しました。
        -   GTID が有効になっている場合やタスクが自動的に再開された場合に CPU 使用率が上昇し、大量のログが出力される問題を修正[＃5063](https://github.com/pingcap/tiflow/issues/5063)
        -   DM WebUI [＃4993](https://github.com/pingcap/tiflow/issues/4993)のオフライン オプションとその他の使用上の問題を修正
        -   アップストリーム[＃3731](https://github.com/pingcap/tiflow/issues/3731)でGTIDが空の場合に増分タスクの開始に失敗する問題を修正
        -   空の設定により dm-master がpanicを起こす可能性がある問題を修正[＃3732](https://github.com/pingcap/tiflow/issues/3732)

    -   TiDB Lightning

        -   事前チェックでローカルディスクリソースとクラスターの可用性がチェックされない問題を修正[＃34213](https://github.com/pingcap/tidb/issues/34213)
        -   スキーマ[＃33381](https://github.com/pingcap/tidb/issues/33381)のルーティングが正しくない問題を修正
        -   TiDB LightningがパニックになったときにPD構成が正しく復元されない問題を修正[＃31733](https://github.com/pingcap/tidb/issues/31733)
        -   `auto_increment`列目[＃27937](https://github.com/pingcap/tidb/issues/27937)の範囲外データによるローカルバックエンドインポート失敗の問題を修正
        -   `auto_random`列目または`auto_increment`列目が null の場合にローカル バックエンドのインポートが失敗する問題を修正しました[＃34208](https://github.com/pingcap/tidb/issues/34208)

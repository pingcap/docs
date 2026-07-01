---
title: TiDB 6.3.0 Release Notes
summary: 2022年9月30日にリリースされたTiDB 6.3.0-DMRでは、TiKVでのSM4アルゴリズムを使用した保存時の暗号化、TiDBでのSM3アルゴリズムを使用した認証、JSONデータ型と関数のサポートなど、新機能と改善点が導入されています。また、実行時間メトリクスをより細かい粒度で提供し、スローログと`TRACE`ステートメントの出力を強化し、TiDB Dashboardでデッドロック履歴情報をサポートします。さらに、TiDB v6.3.0では、新しいシステム変数と構成ファイルパラメータが導入され、さまざまなバグと問題が修正されています。このリリースには、TiKV、PD、 TiFlash、Backup & Restore (BR)、TiCDC、TiDB Binlog、TiDB Data Migration (DM)、およびTiDB Lightningの改善も含まれています。
---

# TiDB 6.3.0 リリースノート {#tidb-6-3-0-release-notes}

発売日：2022年9月30日

TiDBバージョン: 6.3.0-DMR

> **注記：**
>
> TiDB 6.3.0-DMR ドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.3/)です。 PingCAP は、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)を使用することを推奨します。

クイックアクセス: [クイックスタート](https://docs-archive.pingcap.com/tidb/v6.3/quick-start-with-tidb)

バージョン6.3.0-DMRの主な新機能と改善点は以下のとおりです。

-   TiKVは、SM4アルゴリズムを用いた保存データの暗号化をサポートしています。
-   TiDBはSM3アルゴリズムを用いた認証をサポートしています。
-   `CREATE USER`および`ALTER USER`ステートメントは`ACCOUNT LOCK/UNLOCK`オプションをサポートします。
-   JSONデータ型と関数が一般提供（GA）されます。
-   TiDBは、NULL値を考慮したアンチジョインをサポートしています。
-   TiDBは、より詳細な粒度で実行時間メトリクスを提供します。
-   範囲パーティションの定義を簡素化するために、新しい構文糖衣が追加されました。
-   範囲COLUMNSパーティショニングは、複数の列を定義することをサポートしています。
-   インデックス追加時のパフォーマンスが3倍に向上しました。
-   リソースを大量に消費するクエリが、軽量クエリの応答時間に与える影響を50%以上削減します。

## 新機能 {#new-features}

### SQL {#sql}

-   範囲パーティション定義を簡素化するための新しい構文糖衣（範囲INTERVALパーティショニング）を追加（実験的） [#35683](https://github.com/pingcap/tidb/issues/35683) @[mjonss](https://github.com/mjonss)

    TiDBは、範囲パーティションを定義する新しい方法として、 [区間分割](/partitioned-table.md#range-interval-partitioning)を提供します。すべてのパーティションを列挙する必要がないため、範囲パーティショニングのDDLステートメントの長さが大幅に短縮されます。構文は、従来の範囲パーティショニングと同じです。

-   範囲COLUMNSパーティショニングは、複数の列の定義をサポートします [#36636](https://github.com/pingcap/tidb/issues/36636) @[mjonss](https://github.com/mjonss)

    TiDB は[範囲列によるパーティション分割（列リスト）](/partitioned-table.md#range-columns-partitioning)をサポートしています。 `column_list`は単一列に制限されなくなりました。基本的な機能はMySQLと同じです。

-   [交換パーティション](/partitioned-table.md#partition-management)GA [#35996](https://github.com/pingcap/tidb/issues/35996) @[ymkzpx](https://github.com/ymkzpx)になります

-   TiFlashへのさらに 2 つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md)のプッシュダウンをサポート [#5579](https://github.com/pingcap/tiflash/issues/5579) @[SeaRise](https://github.com/SeaRise)

    -   `LEAD()`
    -   `LAG()`

-   DDL変更時のDML成功率を向上させるための軽量メタデータロックを提供する（実験的） [#37275](https://github.com/pingcap/tidb/issues/37275) @[wjhuang2016](https://github.com/wjhuang2016)

    TiDB は、変更されるメタデータ オブジェクトをサポートするために、オンライン非同期スキーマ変更アルゴリズムを使用します。トランザクションが実行されると、トランザクションの開始時に対応するメタデータ スナップショットを取得します。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。この問題を解決するために、TiDB v6.3.0 では、オンライン DDL アルゴリズムに[メタデータロック](/metadata-lock.md)が導入されました。可能な限り DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、実行中の DDL が古いメタデータを持つ DML のコミットを待つようにします。

-   インデックス追加のパフォーマンスを向上させ、DML トランザクションへの影響を軽減します (実験的) [#35983](https://github.com/pingcap/tidb/issues/35983) @[benjamin2037](https://github.com/benjamin2037)

    インデックス作成時のバックフィル処理速度を向上させるため、TiDB v6.3.0 では、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)システム変数が有効になっている場合、 `ADD INDEX`および`CREATE INDEX` DDL 操作が高速化されます。この機能が有効になっている場合、インデックス追加時のパフォーマンスは約 3 倍になります。

### セキュリティ {#security}

-   TiKV は保存時の暗号化に SM4 アルゴリズムをサポートしています [#13041](https://github.com/tikv/tikv/issues/13041) @[jiayang-zheng](https://github.com/jiayang-zheng)

    [SM4アルゴリズム](/encryption-at-rest.md)を追加します 保存時のTiKV暗号化用です。保存時の暗号化を設定する際に、 `data-encryption-method`構成の値を`sm4-ctr`に設定することで、SM4暗号化機能を有効にできます。

-   TiDBはSM3アルゴリズムによる認証をサポートします [#36192](https://github.com/pingcap/tidb/issues/36192) @[CbcWestwolf](https://github.com/CbcWestwolf)

    TiDBは、SM3アルゴリズムに基づいた認証プラグイン[`tidb_sm3_password`](/security-compatibility-with-mysql.md)を追加します。このプラグインが有効になっている場合、ユーザーパスワードはSM3アルゴリズムを使用して暗号化および検証されます。

-   TiDB JDBC は SM3 アルゴリズムによる認証をサポート [#25](https://github.com/pingcap/mysql-connector-j/issues/25) @[lastincisor](https://github.com/lastincisor)

    ユーザー パスワードの認証には、クライアント側のサポートが必要です。 [JDBCはSM3アルゴリズムをサポートしています](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)ので、TiDB-JDBC経由でSM3認証を使用してTiDBに接続できるようになります。

### 可観測性 {#observability}

-   TiDBはSQLクエリ実行時間の詳細なメトリクスを提供します [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 は[実行時間の詳細な観察](/latency-breakdown.md)のためのきめ細かいデータ メトリクスを提供します。完全でセグメント化されたメトリクスを通じて、SQL クエリの主な消費時間を明確に把握でき、主要な問題を迅速に見つけてトラブルシューティングの時間を節約できます。

-   スローログと`TRACE`ステートメントの出力強化 [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 では、スロー ログと`TRACE`の出力が強化されています。TiDB の解析から KV RocksDB によるディスクへの書き込みまでの SQL クエリの[フルリンク期間](/latency-breakdown.md)を観察できるため、診断機能がさらに強化されます。

-   TiDB Dashboardはデッドロック履歴情報を提供します [#34106](https://github.com/pingcap/tidb/issues/34106) @[cfzjywxk](https://github.com/cfzjywxk)

    バージョン6.3.0以降、TiDB Dashboardではデッドロック履歴が提供されます。TiDB Dashboardのスローログを確認し、一部のSQLステートメントのロック待機時間が極端に長い場合は、デッドロック履歴を確認することで根本原因を特定でき、診断が容易になります。

### パフォーマンス {#performance}

-   TiFlash がFastScan の使い方を変更 (実験的) [#5252](https://github.com/pingcap/tiflash/issues/5252) @[hongyunyan](https://github.com/hongyunyan)

    バージョン6.2.0では、 TiFlashにFastScan機能が導入されました。これにより、期待通りのパフォーマンス向上が実現しましたが、使用上の柔軟性に欠けていました。そのため、バージョン6.3.0では、 TiFlashは[FastScanの使い方](/tiflash/use-fastscan.md)変更します。 FastScanを有効または無効にするための`ALTER TABLE ... SET TIFLASH MODE ...`構文は非推奨となりました。代わりに、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して、FastScanを有効にするかどうかを簡単に制御できます。

    バージョン 6.2.0 からバージョン 6.3.0 にアップグレードすると、バージョン 6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。変数`tiflash_fastscan`を設定する必要があります。バージョン 6.2.0 またはそれ以前のバージョンからバージョン 6.3.0 にアップグレードすると、データの一貫性を維持するために、すべてのセッションで FastScan 機能がデフォルトで有効になりません。

-   TiFlashは、複数の同時実行タスクのシナリオにおけるデータスキャン性能を最適化します [#5376](https://github.com/pingcap/tiflash/issues/5376) @[JinheLin](https://github.com/JinheLin)

    TiFlash は、同じデータの読み取り操作を組み合わせることで、同じデータの重複読み取りを削減します。リソースのオーバーヘッドを最適化し、 [同時実行タスクの場合のデータスキャン性能を向上させる](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)。複数の同時タスクの場合、各タスクが同じデータを個別に読み取る必要がある状況を回避し、同じデータを同時に複数読み取る可能性を回避します。

    この機能はバージョン6.2.0では実験的に提供されており、バージョン6.3.0で正式リリースとなります。

-   TiFlashデータ レプリケーションのパフォーマンスが向上 [#5237](https://github.com/pingcap/tiflash/issues/5237) @[breezewish](https://github.com/breezewish)

    TiFlashは、TiKVからのデータレプリケーションにRaftプロトコルを使用します。v6.3.0より前は、大量のレプリカデータのレプリケーションに時間がかかることがよくありました。TiDB v6.3.0では、 TiFlashのデータレプリケーションメカニズムが最適化され、レプリケーション速度が大幅に向上しました。BRを使用してデータをリカバリする場合、 TiDB Lightningを使用してデータをインポートする場合、または新しいTiFlashレプリカを追加する場合、 TiFlashレプリカのレプリケーションがより迅速に行われます。TiFlashを使用したクエリもより迅速に実行できます。さらに、 TiFlashレプリカのスケールアップ、スケールダウン、またはレプリカ数の変更時にも、 TiFlashレプリカはより迅速に安全でバランスの取れた状態に到達します。

-   TiFlash は個々の`COUNT(DISTINCT)`の 3 段階集約をサポートしています [#37202](https://github.com/pingcap/tidb/issues/37202) @[fixdb](https://github.com/fixdb)

    TiFlashは`COUNT(DISTINCT)`を1つだけ含むクエリを[3段階集計](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)に書き換えることをサポートしています。 これにより、同時実行性とパフォーマンスが向上します。

-   TiKVはログのリサイクルをサポートしています [#214](https://github.com/tikv/raft-engine/issues/214) @[LykxSassinator](https://github.com/LykxSassinator)

    TiKV はRaft Engineの[リサイクルログファイル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)をサポートしています。これにより、 Raftログの追加中のネットワーク ディスクのロングテールレイテンシーが短縮され、書き込みワークロード時のパフォーマンスが向上します。

-   TiDB は null 認識アンチ結合をサポートします [#37525](https://github.com/pingcap/tidb/issues/37525) @[Arenatlx](https://github.com/Arenatlx)

    TiDB v6.3.0 では、新しい結合[ヌル値認識型アンチジョイン（NAAJ）](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)が導入されています。 NAAJ は、コレクション操作を処理するときに、コレクションが空であるか、 `NULL`であるかを認識できます。これにより`IN`や`= ANY`などの操作の実行効率が最適化され、SQL パフォーマンスが向上します。

-   ハッシュ結合のビルド終了を制御するオプティマイザー ヒントを追加 [#35439](https://github.com/pingcap/tidb/issues/35439) @[Reminiscent](https://github.com/Reminiscent)

    バージョン6.3.0では、TiDBオプティマイザに、ハッシュ結合、そのプローブ終了、および構築終了を指定するための2つのヒント、 `HASH_JOIN_BUILD()`と`HASH_JOIN_PROBE()`が導入されました。オプティマイザが最適な実行プランを選択できない場合、これらのヒントを使用してプランに介入できます。

-   セッションレベルの共通テーブル式 (CTE) インラインをサポート [#36514](https://github.com/pingcap/tidb/issues/36514) @[elsa0520](https://github.com/elsa0520)

    TiDB v6.2.0 では、オプティマイザに`MERGE`ヒントを導入し、CTE のインライン実行を可能にしました。これにより、CTE クエリ結果の利用者はTiFlashで並列実行できるようになりました。v6.3.0 では、セッション変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)導入され、セッション内での CTE のインライン実行が可能になりました。これにより、使いやすさが大幅に向上します。

### トランザクション {#transactions}

-   悲観的トランザクションにおける一意制約のチェックの延期をサポート [#36579](https://github.com/pingcap/tidb/issues/36579) @[ekexium](https://github.com/ekexium)

    TiDB が[固有の制約](/constraints.md#pessimistic-transactions)チェックを行うかを制御できるシステム変数[`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)を使用できます。悲観的トランザクションにおいて。この変数はデフォルトでは無効になっています。変数を有効にすると ( `ON`に設定)、TiDB は悲観的トランザクションにおけるロック操作と一意制約チェックを必要になるまで延期し、バルク DML 操作のパフォーマンスを向上させます。

-   Read-Committed 分離レベルで TSO を取得する方法を最適化します [#36812](https://github.com/pingcap/tidb/issues/36812) @[TonsnakeLin](https://github.com/TonsnakeLin)

    リードコミット分離レベルでは、システム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)導入され、TSOのフェッチ方法を制御します。プランキャッシュヒットの場合、TiDBはTSOのフェッチ頻度を減らすことでバッチDMLステートメントの実行効率を向上させ、バッチで実行されるタスクの実行時間を短縮します。

### 安定性 {#stability}

-   リソースを大量に消費するクエリが軽量クエリの応答時間に与える影響を軽減する [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

    リソースを大量に消費するクエリと軽量クエリが同時に実行されると、軽量クエリの応答時間に影響が出ます。この場合、トランザクションサービスの品質を確保するため、TiDBは軽量クエリを優先的に処理することが求められます。v6.3.0では、TiKVが読み取りリクエストのスケジューリングメカニズムを最適化し、各ラウンドにおけるリソースを大量に消費するクエリの実行時間が期待値を満たすようにしました。これにより、リソースを大量に消費するクエリが軽量クエリの応答時間に与える影響が大幅に軽減され、混合ワークロードシナリオにおけるP99レイテンシーが50%以上削減されます。

-   統計情報が古くなった場合に統計情報を読み込むデフォルトポリシーを変更する [#27601](https://github.com/pingcap/tidb/issues/27601) @[xuyifangreeneyes](https://github.com/xuyifangreeneyes)

    v5.3.0 では、統計情報が古くなったときのオプティマイザの動作を制御するために、システム変数[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)が導入されました。デフォルト値は`ON`で、これは旧バージョンの動作を維持することを意味します。つまり、SQL ステートメントに関係するオブジェクトの統計情報が古くなった場合、オプティマイザは (テーブルの総行数以外の) 統計情報はもはや信頼できないと判断し、代わりに擬似統計情報を使用します。実際のユーザー シナリオのテストと分析の結果、v6.3.0 以降、デフォルト値`tidb_enable_pseudo_for_outdated_stats`は`OFF`に変更されました。統計情報が古くなっても、オプティマイザはテーブル上の統計情報を使用するため、実行プランがより安定します。

-   Titan の無効化が GA に[タボキー](https://github.com/tabokie)

    オンライン TiKV ノードに対して[Titanを無効にする](/storage-engine/titan-configuration.md#disable-titan)ことができます。

-   グローバル統計が準備できていない場合は、 `static`パーティションプルーニングを使用します [#37535](https://github.com/pingcap/tidb/issues/37535) @[Yisaer](https://github.com/Yisaer)

    [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode)が有効になっている場合、オプティマイザは[世界の統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)に基づいて実行プランを選択します。グローバル統計が完全に収集される前に擬似統計を使用すると、パフォーマンスが低下する可能性があります。v6.3.0 では、グローバル統計の収集が完了する前に`dynamic`プルーニング モードを有効にすると、グローバル統計が完全に収集されるまで TiDB は`static`モードのままになります。これにより、パーティション プルーニングの設定を変更したときのパフォーマンスの安定性が確保されます。

### 使いやすさ {#ease-of-use}

-   SQLベースのデータ配置ルールとTiFlashレプリカ間の競合に対処する [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

    TiDB v6.0.0 は[SQLベースのデータ配置ルール](/placement-rules-in-sql.md)を提供します。ただし、実装上の問題により、この機能はTiFlashレプリカと競合します。 TiDB v6.3.0 は実装メカニズムを最適化し、SQL ベースのデータ配置ルールとTiFlashの間の競合を解決します。

### MySQLとの互換性 {#mysql-compatibility}

-   MySQL 8.0との互換性を向上させるため、4つの正規表現関数（ `REGEXP_INSTR()` 、 `REGEXP_LIKE()` 、 `REGEXP_REPLACE()` 、 `REGEXP_SUBSTR()` [#23881](https://github.com/pingcap/tidb/issues/23881) @[windtalker](https://github.com/windtalker)

    MySQL との互換性の詳細については、 [MySQLとの正規表現互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)を参照してください。

-   `CREATE USER`および`ALTER USER`ステートメントは`ACCOUNT LOCK/UNLOCK`オプション [#37051](https://github.com/pingcap/tidb/issues/37051)をサポートします @[CbcWestwolf](https://github.com/CbcWestwolf)

    [`CREATE USER`](/sql-statements/sql-statement-create-user.md)文を使用してユーザーを作成する際、 `ACCOUNT LOCK/UNLOCK`オプションを使用して、作成したユーザーがロックされているかどうかを指定できます。ロックされたユーザーはデータベースにログインできません。

    [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントの`ACCOUNT LOCK/UNLOCK`オプションを使用すると、既存ユーザーのロック状態を変更できます。

-   JSON データ型と JSON関数がGA になりました [#36993](https://github.com/pingcap/tidb/issues/36993) @[xiongjiwei](https://github.com/xiongjiwei)

    JSONは、多くのプログラムで採用されている一般的なデータ形式です。TiDBは、以前のバージョンから[JSONサポート](/data-type-json.md)実験的機能として導入しており、MySQLのJSONデータ型および一部のJSON関数と互換性があります。

    TiDB v6.3.0 では、JSON データ型と関数がGA になり、TiDB のデータ型が強化され、 [発現指数](/sql-statements/sql-statement-create-index.md#expression-index)および[生成された列](/generated-columns.md)での JSON関数の使用がサポートされ、TiDB と MySQL の互換性がさらに向上しました。

### バックアップと復元 {#backup-and-restore}

-   PITR はバックアップ ストレージとして[GCSとAzure Blob Storage](/br/backup-and-restore-storages.md)サポートしています @[joccau](https://github.com/joccau)

    TiDBクラスターがGoogle CloudまたはAzureにデプロイされている場合、クラスターをv6.3.0にアップグレードすると、PITR機能を使用できます。

-   BRは AWS S3 オブジェクト ロック [#13442](https://github.com/tikv/tikv/issues/13442) @[3pointer](https://github.com/3pointer)シュートをサポートします

    [S3オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)を有効にすることで、AWS 上のバックアップ データが改ざんまたは削除されないように保護できます。

### データ移行 {#data-migration}

-   TiDB Lightning は[Apache HiveによってエクスポートされたParquetファイルをTiDBにインポートする](/tidb-lightning/tidb-lightning-data-source.md#parquet)インポートする [#37536](https://github.com/pingcap/tidb/issues/37536) @[buchuitoudegou](https://github.com/buchuitoudegou)

-   DM に新しい設定項目`safe-mode-duration`が追加されました [#6224](https://github.com/pingcap/tiflow/issues/6224) @[okJiang](https://github.com/okJiang)

    この設定項目は、[タスク構成ファイル](/dm/task-configuration-file-full.md)ファイルに追加されます。DM が異常終了した後の自動セーフモードの継続時間を調整できます。デフォルト値は 60 秒です。 `safe-mode-duration` `"0s"`に設定すると、DM が異常再起動後にセーフモードに入ろうとしたときにエラーが報告されます。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDCは、地理的に分散した複数のデータソースからデータを複製できるデプロイメントトポロジーをサポートしています [#5301](https://github.com/pingcap/tiflow/issues/5301) @[sdojjy](https://github.com/sdojjy)

    v6.3.0 以降、単一の TiDB クラスターから複数の地理的に分散されたデータ システムへのデータの複製をサポートするために、 [TiCDCは複数のIDCに展開できます](/ticdc/deploy-ticdc.md) 。この機能は、地理的に分散されたデータ レプリケーションおよび展開トポロジの機能を提供するのに役立ちます。

-   TiCDCは、アップストリームとダウンストリーム間でスナップショットの一貫性を維持することをサポートしています（同期ポイント） [#6977](https://github.com/pingcap/tiflow/issues/6977) [asddongmen](https://github.com/asddongmen)

    ディザスタリカバリのためのデータ レプリケーションのシナリオでは、TiCDC は、ダウンストリーム スナップショットがアップストリーム スナップショットと一貫性を保つように [定期的に下流データのスナップショットを維持する](/ticdc/ticdc-upstream-downstream-check.md)をサポートします。この機能により、TiCDC は読み取りと書き込みが分離されるシナリオをより適切にサポートし、コストの削減に役立ちます。

-   TiCDC はグレースフル アップグレードをサポート [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus)@[3AceShowHand](https://github.com/3AceShowHand)

    TiCDCを[TiUP](/ticdc/deploy-ticdc.md#upgrade-cautions) （&gt;=v1.11.0）または[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) （&gt;=v1.3.8）を使用してデプロイする場合、TiCDCクラスタをスムーズにアップグレードできます。アップグレード中は、データレプリケーションのレイテンシーが30秒以下に抑えられます。これにより安定性が向上し、TiCDCはレイテンシに敏感なアプリケーションをより適切にサポートできるようになります。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                         | 変更の種類  | 説明                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                       | 変更     | 新しいオプション`tidb_sm3_password`を追加します。この変数を`tidb_sm3_password`に設定すると、暗号化アルゴリズムとして SM3 が使用されます。                                                                                                                                           |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630)                                       | 新しく追加された | テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。                                                                                                                                                   |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)             | 新しく追加された | [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合、TiDBサーバーが読み取り要求を TiDBサーバーと同じリージョンのレプリカに送信することを優先するしきい値を制御します。                                                                  |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | 新しく追加された | TiDB が悲観的トランザクションで[固有の制約](/constraints.md#pessimistic-transactions)いつチェックするかを制御します。                                                                                                                                                  |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)                                               | 新しく追加された | [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)有効になっている場合にのみ有効になります。インデックス作成時のバックフィル処理中にローカルストレージを使用する際の制限を設定します。                                                                      |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                 | 新しく追加された | インデックス作成時のバックフィル速度を向上させるために、 `ADD INDEX`および`CREATE INDEX` DDL 操作の高速化を有効にするかどうかを制御します。                                                                                                                                                |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                         | 新しく追加された | `flashback cluster`の同時実行を制御します。この変数で制御される機能は、TiDB v6.3.0 では完全には動作しません。デフォルト値を変更しないでください。                                                                                                                                             |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition)                                     | 非推奨      | [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、 `exchange partitions with tables`がデフォルトで有効になっています。                                                              |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                       | 新しく追加された | `FOREIGN KEY`機能を有効にするかどうかを制御します。この変数で制御される機能は、TiDB v6.3.0では完全には動作しません。デフォルト値を変更しないでください。                                                                                                                                             |
| `tidb_enable_general_plan_cache`                                                                                            | 新しく追加された | 一般プランキャッシュ機能を有効にするかどうかを制御します。この変数で制御される機能は、TiDB v6.3.0 では完全には動作しません。デフォルト値を変更しないでください。                                                                                                                                               |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                   | 新しく追加された | [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを指定します。                                                                                                                                                                                     |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                     | 新しく追加された | 特殊な集合演算子`NOT IN`および`!= ALL`を制御します。                                                                                                                                                                                                   |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)           | 変更     | 統計情報が古くなっている場合に、オプティマイザがテーブルの統計情報を使用する動作を制御します。デフォルト値は`ON`から`OFF`に変更されます。これは、テーブルの統計情報が古くなっている場合でも、オプティマイザが引き続きテーブルの統計情報を使用することを意味します。                                                                                               |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)                                       | 変更     | データを読み取るオペレータの動的メモリ制御機能を有効にするかどうかを制御します。この変数が`ON`に設定されている場合、メモリ使用量は[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制御下にない可能性があります。そのため、デフォルト値は`ON`から`OFF`に変更されます。                                                |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 新しく追加された | SQL書き込みステートメント内の読み取り要求をTiFlashにプッシュダウンするかどうかを制御します。この変数で制御される機能は、TiDB v6.3.0では完全には動作しません。デフォルト値は変更しないでください。                                                                                                                          |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 式を生成列に安全でない方法で置き換えるかどうかを制御します。                                                                                                                                                                                                       |
| `tidb_general_plan_cache_size`                                                                                              | 新しく追加された | 一般プランキャッシュでキャッシュできる実行プランの最大数を制御します。この変数で制御される機能は、TiDB v6.3.0 では完全には動作しません。デフォルト値を変更しないでください。                                                                                                                                         |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 読み取り専用であり、現在のセッションでの最後の`PLAN REPLAYER DUMP`実行の結果を取得するために使用されます。                                                                                                                                                                      |
| [tidb_max_paging_size](/system-variables.md#tidb_max_paging_size-new-in-v630)                                               | 新しく追加された | この変数は、コプロセッサのページング要求処理中に最小行数を設定するために使用されます。                                                                                                                                                                                          |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)                                   | 新しく追加された | セッション全体の共通テーブル式 (CTE) をインライン化するかどうかを制御します。デフォルト値は`OFF`で、これはデフォルトでは CTE のインライン化が強制されないことを意味します。                                                                                                                                       |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)                   | 新しく追加された | `COUNT(DISTINCT)`集計を MPP モードで 3 段階集計に書き換えるかどうかを指定します。デフォルト値は`ON`です。                                                                                                                                                                  |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)                                    | 変更     | 動的剪定を有効にするかどうかを指定します。v6.3.0 以降、デフォルト値は`dynamic`に変更されます。                                                                                                                                                                              |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                           | 変更     | タイムスタンプの取得を最適化するために使用され、読み取りコミット分離レベルのシナリオ（読み取りと書き込みの競合がまれなシナリオ）に適しています。この機能は特定のサービスワークロード向けに設計されており、他のシナリオではパフォーマンスが低下する可能性があります。そのため、v6.3.0以降、この変数の適用範囲が`GLOBAL \| SESSION`から`INSTANCE`に変更されました。つまり、特定のTiDBインスタンスに対してこの機能を有効にできます。 |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)                                         | 新しく追加された | タイムスタンプの取得を最適化するために使用され、悲観的トランザクションのRC分離レベルにおいてポイントライト競合が少ないシナリオに適しています。この変数を有効にすると、ポイントライトステートメントの実行中にグローバルタイムスタンプを取得する際に発生するレイテンシーとオーバーヘッドを回避できます。                                                                                 |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)                                                     | 新しく追加された | FastScanを有効にするかどうかを制御します。FastScan[ファストスキャン](/tiflash/use-fastscan.md)有効になっている場合（ `ON`に設定）、 TiFlashはより効率的なクエリパフォーマンスを提供しますが、クエリ結果の正確性やデータの一貫性は保証されません。                                                                                |

### コンフィグレーションファイルパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                            | 変更の種類  | 説明                                                                                                                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)                                        | 新しく追加された | TiDB が一時データを格納するために使用するファイルシステム上の場所を指定します。機能が TiDB ノードでローカルストレージを必要とする場合、TiDB は対応する一時データをこの場所に格納します。デフォルト値は`/tmp/tidb`です。                                                                                      |
| TiKV           | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)              | 新しく追加された | スレッドプールのサイズを自動的に調整するかどうかを制御します。有効にすると、現在のCPU使用率に基づいてUnifyReadPoolスレッドプールのサイズを自動的に調整することで、TiKVの読み取りパフォーマンスが最適化されます。                                                                                               |
| TiKV           | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method)                        | 変更     | 新しい値オプション`sm4-ctr`が導入されました。この設定項目が`sm4-ctr`に設定されている場合、データは保存される前に SM4 を使用して暗号化されます。                                                                                                                              |
| TiKV           | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                    | 新しく追加された | Raft Engineで古いログ ファイルを再利用するかどうかを決定します。有効にすると、論理的に削除されたログ ファイルは再利用のために予約されます。これにより、書き込みワークロードのロング テールレイテンシーが削減されます。この設定項目は[フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v630)が 2 以上の場合のみ使用できます。 |
| TiKV           | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                            | 新しく追加された | Raft Engineのログ ファイルのバージョンを指定します。デフォルトのログ ファイル バージョンは、TiKV v6.3.0 より前のバージョンでは`1`です。ログ ファイルは、TiKV &gt;= v6.1.0 で読み取ることができます。デフォルトのログ ファイル バージョンは、TiKV v6.3.0 以降では`2`です。TiKV v6.3.0 以降では、ログ ファイルを読み取ることができます。       |
| TiKV           | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620)                                 | 変更     | バージョン6.3.0以降、デフォルト値が`false`から`true`に変更されました。                                                                                                                                                                     |
| TiKV           | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620)         | 変更     | バージョン6.3.0以降、デフォルト値が`5min`から`3min`に変更されました。                                                                                                                                                                      |
| PD             | [診断を有効にする](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                   | 新しく追加された | 診断機能を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                           |
| TiFlash        | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)   | 非推奨      | バージョン6.3.0以降、この設定項目は非推奨となりました。デフォルトでは、スレッドプールがストレージエンジンからの読み取り要求を処理するために使用され、無効にすることはできません。                                                                                                                    |
| DM             | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | 自動セーフモードの継続時間を指定します。                                                                                                                                                                                             |
| TiCDC          | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | Syncpoint機能を有効にするかどうかを指定します。                                                                                                                                                                                     |
| TiCDC          | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)        | 新しく追加された | Syncpointがアップストリームとダウンストリームのスナップショットを同期させる間隔を指定します。                                                                                                                                                              |
| TiCDC          | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新しく追加された | Syncpointがダウンストリームテーブルにデータを保持する期間を指定します。この期間を超えると、データは削除されます。                                                                                                                                                    |
| TiCDC          | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters)                      | 非推奨      | `memory`ソートは非推奨です。いかなる状況でも使用することは推奨されません。                                                                                                                                                                        |

### その他 {#others}

-   ログバックアップは、バックアップストレージとしてGCSとAzure Blob Storageをサポートしています。
-   ログバックアップは`exchange partition` DDLと互換性を持つようになりました。
-   以前[ファストスキャン](/tiflash/use-fastscan.md)を有効にするために使用されていた SQL ステートメント`ALTER TABLE ...SET TiFLASH MODE ...`非推奨となり、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)に置き換えられました。v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。この場合、FastScan を有効または無効にするには、変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を設定する必要があります。以前のバージョンから v6.3.0 にアップグレードすると、データの一貫性を保つために、すべてのセッションで FastScan 機能はデフォルトで有効になりません。
-   TiFlashをLinux AMD64アーキテクチャにデプロイするには、CPUがAVX2命令セットをサポートしている必要があります。 `grep avx2 /proc/cpuinfo`に出力があることを確認してください。TiFlashをLinux ARM64アーキテクチャにデプロイするには、CPUがARMv8命令セットアーキテクチャをサポートしている必要があります。 `grep 'crc32' /proc/cpuinfo | grep 'asimd'`に出力があることを確認してください。命令セット拡張機能を使用することで、TiFlashのベクトル化エンジンはより優れたパフォーマンスを発揮できます。
-   TiDBと連携するHAProxyの最小バージョンはv1.5です。v1.5からv2.1までのHAProxyバージョンでは、 `post-41`に`mysql-check`設定オプションを設定する必要があります。HAProxy v2.2以降の使用をお勧めします。

## 削除された機能 {#removed-feature}

バージョン6.3.0以降、TiCDCはPulsarシンクの設定をサポートしなくなりました。StreamNativeが提供する[コップ](https://github.com/streamnative/kop)代替として使用できます。

## 改善点 {#improvements}

-   TiDB

    -   TiDB は、テーブルの存在を確認する際に、対象テーブル名の大文字小文字を区別しなくなりました [#34610](https://github.com/pingcap/tidb/issues/34610) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `init_connect`の値を設定する際に解析チェックを追加することで MySQL の互換性を向上させます [#35324](https://github.com/pingcap/tidb/issues/35324) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   新しい接続に対して生成されるログ警告を改善 [#34964](https://github.com/pingcap/tidb/issues/34964) @[xiongjiwei](https://github.com/xiongjiwei)
    -   DDL履歴ジョブのクエリ用HTTP APIを最適化し、 `start_job_id`パラメータのサポートを追加 [#35838](https://github.com/pingcap/tidb/issues/35838) @[tiancaiamao](https://github.com/tiancaiamao)
    -   JSON パスの構文が間違っている場合にエラーを報告する[#22525](https://github.com/pingcap/tidb/issues/22525) [#34959](https://github.com/pingcap/tidb/issues/34959) @[xiongjiwei](https://github.com/xiongjiwei)
    -   誤った共有の問題を修正することで、結合操作のパフォーマンスを向上させます [#37641](https://github.com/pingcap/tidb/issues/37641) @[gengliqi](https://github.com/gengliqi)
    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)を使用して複数のSQLステートメントの実行プラン情報を一度にエクスポートできるようにすることで、トラブルシューティングの効率化を図ります。 [#37798](https://github.com/pingcap/tidb/issues/37798) @[Yisaer](https://github.com/Yisaer)

-   TiKV

    -   ピアが到達不能になった後にRaftstore がメッセージを過剰にブロードキャストするのを回避するために`unreachable_backoff`アイテムの設定をサポートします [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    -   TSOサービスの耐障害性を向上させる [#12794](https://github.com/tikv/tikv/issues/12794) @[pingyu](https://github.com/pingyu)
    -   RocksDB で同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポートする ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @[ethercflow](https://github.com/ethercflow)
    -   空のリージョンをマージする際のパフォーマンスを最適化する [#12421](https://github.com/tikv/tikv/issues/12421) @[tabokie](https://github.com/tabokie)
    -   正規表現関数をさらにサポート [#13483](https://github.com/tikv/tikv/issues/13483) @[gengliqi](https://github.com/gengliqi)
    -   CPU使用率に基づいてスレッドプールサイズを自動的に調整する機能をサポート [#13313](https://github.com/tikv/tikv/issues/13313) @[glorv](https://github.com/glorv)

-   PD

    -   TiDB DashboardにおけるTiKV IO MBpsメトリックのクエリを改善する [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)
    -   TiDB DashboardのURLを`metrics`から`monitoring`に変更してください [#5366](https://github.com/tikv/pd/issues/5366) @[YiniXu9506](https://github.com/YiniXu9506)

-   TiFlash

    -   `elt`関数のTiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @[Willendless](https://github.com/Willendless)へのプッシュダウンをサポート
    -   TiFlashへの`leftShift`機能のプッシュダウンをサポートします [#5099](https://github.com/pingcap/tiflash/issues/5099) @[AnnieoftheStars](https://github.com/AnnieoftheStars)
    -   `castTimeAsDuration`関数のTiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @[AntiTopQuark](https://github.com/AntiTopQuark)へのプッシュダウンのサポート
    -   TiFlashへの`HexIntArg/HexStrArg`機能のプッシュダウンをサポートします [#5107](https://github.com/pingcap/tiflash/issues/5107) @[YangKeao](https://github.com/YangKeao)
    -   TiFlashのインタープリタをリファクタリングし、新しいインタープリタプランナー [#4739](https://github.com/pingcap/tiflash/issues/4739)をサポートする @[SeaRise](https://github.com/SeaRise)
    -   TiFlashのメモリトラッカーの精度を向上 [#5609](https://github.com/pingcap/tiflash/issues/5609) @[bestwoody](https://github.com/bestwoody)
    -   `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN`照合順序を使用した文字列列のパフォーマンスを改善 [#5294](https://github.com/pingcap/tiflash/issues/5294) @[solotzg](https://github.com/solotzg)
    -   ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401) , [#5091](https://github.com/pingcap/tiflash/issues/5091) @[Lloyd-Pottiger](https://github.com/Lloyd-Pottiger)ポティガーでバックグラウンドでI/Oスループットを計算

-   ツール

    -   Backup & Restore (BR)

        -   PITRはログバックアップで生成された小さなファイルをマージできるため、バックアップファイルの数を大幅に削減できます。 [#13232](https://github.com/tikv/tikv/issues/13232) @[Leavrth](https://github.com/Leavrth)
        -   PITRは、復元後にアップストリームクラスタ構成に基づいてTiFlashレプリカの数を自動的に構成することをサポートします [#37208](https://github.com/pingcap/tidb/issues/37208) @[YuJuncen](https://github.com/YuJuncen)

    -   TiCDC

        -   TiCDCと、上流のTiDBで導入された並行DDLフレームワークとの互換性を向上させる [#6506](https://github.com/pingcap/tiflow/issues/6506) @[lance6716](https://github.com/lance6716)
        -   MySQL シンクでエラー [#6460](https://github.com/pingcap/tiflow/issues/6460) @[overvenus](https://github.com/overvenus)ヴィーナスが発生した場合の DML ステートメントのロギング`start ts`のサポート
        -   `api/v1/health` API を強化して、TiCDC クラスターのより正確な正常性状態を返します [#4757](https://github.com/pingcap/tiflow/issues/4757) @[overvenus](https://github.com/overvenus)
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます [#5928](https://github.com/pingcap/tiflow/issues/5928) @[hicqu](https://github.com/hicqu)@[Rustin170506](https://github.com/Rustin170506)
        -   非推奨のPulsarシンク [#7087](https://github.com/pingcap/tiflow/issues/7087) @[Rustin170506](https://github.com/Rustin170506)を削除します
        -   変更フィードに関係のない DDL ステートメントを破棄することで、レプリケーションのパフォーマンスを向上させます [#6447](https://github.com/pingcap/tiflow/issues/6447) @[asddongmen](https://github.com/asddongmen)

    -   TiDB Data Migration (DM)

        -   MySQL 8.0をデータソースとして使用する際の互換性を向上させる [#6448](https://github.com/pingcap/tiflow/issues/6448) @[lance6716](https://github.com/lance6716)
        -   「無効な接続」が発生した場合にDDLを非同期で実行することでDDLを最適化する [#4689](https://github.com/pingcap/tiflow/issues/4689) @[lyzx2001](https://github.com/lyzx2001)

    -   TiDB Lightning

        -   S3外部ストレージURLのクエリパラメータを追加し、指定されたロールを引き受けることで別のアカウントのS3データにアクセスできるようにする [#36891](https://github.com/pingcap/tidb/issues/36891) @[dsdashun](https://github.com/dsdashun)

## バグ修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメントの権限チェックがスキップされる問題を修正 [#35784](https://github.com/pingcap/tidb/issues/35784) @[lcwangchao](https://github.com/lcwangchao)
    -   システム変数`tidb_enable_noop_variable`が`WARN`に設定できてしまう問題を修正しました [#36647](https://github.com/pingcap/tidb/issues/36647) @[lcwangchao](https://github.com/lcwangchao)
    -   式インデックスが定義されている場合、 `ORDINAL_POSITION`テーブルの`INFORMATION_SCHEMA.COLUMNS`列が正しくない可能性がある問題を修正します。 [#31200](https://github.com/pingcap/tidb/issues/31200) @[bb7133](https://github.com/bb7133)
    -   TiDB がタイムスタンプが`MAXINT32`より大きい場合にエラーを報告しない問題を修正 [#31585](https://github.com/pingcap/tidb/issues/31585) @[bb7133](https://github.com/bb7133)
    -   Enterpriseプラグイン使用時にTiDBサーバーが起動できない問題を修正 [#37319](https://github.com/pingcap/tidb/issues/37319) @[xhebox](https://github.com/xhebox)
    -   `SHOW CREATE PLACEMENT POLICY`の誤った出力を修正 [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
    -   一時テーブルでの予期しない`EXCHANGE PARTITION`動作を修正 [#37201](https://github.com/pingcap/tidb/issues/37201) @[lcwangchao](https://github.com/lcwangchao)
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`のクエリで誤った結果が返される問題を修正しました @[zimulala](https://github.com/zimulala)
    -   ビューに対する`EXPLAIN`クエリが権限をチェックしない問題を修正 [#34326](https://github.com/pingcap/tidb/issues/34326) @[hawkingrei](https://github.com/hawkingrei)
    -   JSON `null`を`NULL`に更新できない問題を修正 [#37852](https://github.com/pingcap/tidb/issues/37852) @[YangKeao](https://github.com/YangKeao)
    -   DDL ジョブの`row_count`が不正確である問題を修正 [#25968](https://github.com/pingcap/tidb/issues/25968) @[Defined2014](https://github.com/Defined2014)
    -   `FLASHBACK TABLE`が正しく動作しない問題を修正 [#37386](https://github.com/pingcap/tidb/issues/37386) @[tiancaiamao](https://github.com/tiancaiamao)
    -   標準的な MySQL プロトコルで`prepared`ステートメントフラグを処理できない問題を修正 [#36731](https://github.com/pingcap/tidb/issues/36731) @[dveeden](https://github.com/dveeden)
    -   一部の極端なケースで起動時に表示される可能性のある、TiDB ステータスの誤りに関する問題を修正しました [#36791](https://github.com/pingcap/tidb/issues/36791) @[xhebox](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.VARIABLES_INFO`がセキュリティ強化モード (SEM) に準拠していない問題を修正します [#37586](https://github.com/pingcap/tidb/issues/37586) @[CbcWestwolf](https://github.com/CbcWestwolf)
    -   `UNION`を含むクエリで文字列から文字列へのキャストが失敗する問題を修正 [#31678](https://github.com/pingcap/tidb/issues/31678) @[cbcwestwolf](https://github.com/cbcwestwolf)
    -   TiFlashのパーティションテーブルで動的モードを有効にした際に発生する誤った結果を修正 [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
    -   TiDBにおけるバイナリ文字列とJSON間のキャストおよび比較がMySQLと互換性がない問題を修正[#31918](https://github.com/pingcap/tidb/issues/31918) [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    -   TiDB の`JSON_OBJECTAGG`と`JSON_ARRAYAGG`がバイナリ値で MySQL と互換性がない問題を修正 [#25053](https://github.com/pingcap/tidb/issues/25053) @[YangKeao](https://github.com/YangKeao)
    -   JSONの不透明な値の比較でpanicが発生する問題を修正 [#37315](https://github.com/pingcap/tidb/issues/37315) @[YangKeao](https://github.com/YangKeao)
    -   JSON集計関数で単精度浮動小数点数が使用できない問題を修正 [#37287](https://github.com/pingcap/tidb/issues/37287) @[YangKeao](https://github.com/YangKeao)
    -   `UNION`演算子が予期しない空の結果を返す可能性がある問題を修正 [#36903](https://github.com/pingcap/tidb/issues/36903) @[tiancaiamao](https://github.com/tiancaiamao)
    -   `castRealAsTime`式の結果が MySQL と一致しない問題を修正します [#37462](https://github.com/pingcap/tidb/issues/37462) @[mengxin9014](https://github.com/mengxin9014)
    -   悲観的DML 操作が非一意インデックス キーをロックする問題を修正 [#36235](https://github.com/pingcap/tidb/issues/36235) @[ekexium](https://github.com/ekexium)
    -   `auto-commit`の変更がトランザクションコミットの動作に影響を与える問題を修正 [#36581](https://github.com/pingcap/tidb/issues/36581) @[cfzjywxk](https://github.com/cfzjywxk)
    -   DML実行エンジンを使用した`EXPLAIN ANALYZE`ステートメントがトランザクションコミットが完了する前に結果を返す可能性がある問題を修正しました [#37373](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)
    -   UPDATE文が場合によっては誤って投影を削除し、 `Can't find column`エラー [#37568](https://github.com/pingcap/tidb/issues/37568)が発生する問題を修正しました。@[AilinKid](https://github.com/AilinKid)
    -   結合したテーブルの再配置操作が誤って外部結合条件をプッシュダウンする問題を修正 [#37238](https://github.com/pingcap/tidb/issues/37238) @[AilinKid](https://github.com/AilinKid)
    -   一部のパターンで`IN`と`NOT IN`サブクエリが`Can't find column`エラー [#37032](https://github.com/pingcap/tidb/issues/37032)を報告する問題を修正しました。@[AilinKid](https://github.com/AilinKid)
    -   `Can't find column`ステートメントに共通テーブル式 (CTE) が含まれている場合に`UPDATE`が報告される問題を修正 [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)
    -   間違った`PromQL` [#35856](https://github.com/pingcap/tidb/issues/35856) @[Defined2014](https://github.com/Defined2014)修正

-   TiKV

    -   リージョンのハートビートが中断された後、PD が TiKV に再接続しない問題を修正 [#12934](https://github.com/tikv/tikv/issues/12934) @[bufferflies](https://github.com/bufferflies)
    -   Raftstoreがビジー状態のときにリージョンが重複する可能性がある問題を修正 [#13160](https://github.com/tikv/tikv/issues/13160) @[5kbpers](https://github.com/5kbpers)
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[#13191](https://github.com/tikv/tikv/issues/13191) @[bufferflies](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @[BurtonQin](https://github.com/BurtonQin)
    -   暗号化が無効になっている場合に TiKV がpanic可能性がある問題を修正 [#13081](https://github.com/tikv/tikv/issues/13081) @[jiayang-zheng](https://github.com/jiayang-zheng)
    -   ダッシュボードの`Unified Read Pool CPU`の誤った表現を修正 [#13086](https://github.com/tikv/tikv/issues/13086) @[glorv](https://github.com/glorv)
    -   TiKVインスタンスが隔離されたネットワーク環境にある場合、TiKVサービスが数分間利用できなくなる問題を修正します [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)
    -   TiKV が誤って`PessimisticLockNotFound`エラーを報告する問題を修正 [#13425](https://github.com/tikv/tikv/issues/13425) @[sticnarf](https://github.com/sticnarf)
    -   状況によってはPITRによりデータ損失が発生する可能性がある問題を修正 [#13281](https://github.com/tikv/tikv/issues/13281) @[YuJuncen](https://github.com/YuJuncen)
    -   長い悲観的トランザクションがある場合にチェックポイントが進まない問題を修正 [#13304](https://github.com/tikv/tikv/issues/13304) @[YuJuncen](https://github.com/YuJuncen)
    -   TiKV が JSON 内の datetime 型 ( `DATETIME` 、 `DATE` 、 `TIMESTAMP`および`TIME` ) と`STRING`型を区別しない問題を修正 [#13417](https://github.com/tikv/tikv/issues/13417) @[YangKeao](https://github.com/YangKeao)
    -   JSON boolと他のJSON値の比較におけるMySQLとの非互換性を修正[#13386](https://github.com/tikv/tikv/issues/13386) [#37481](https://github.com/pingcap/tidb/issues/37481) @[YangKeao](https://github.com/YangKeao)

-   PD

    -   `enable-forwarding`が有効になっている場合にgRPCがエラーを不適切に処理する問題によって発生するPDパニックを修正 [#5373](https://github.com/tikv/pd/issues/5373) @[bufferflies](https://github.com/bufferflies)
    -   不健康なリージョンがPDpanicを引き起こす可能性がある問題を修正 [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)
    -   TiFlash学習者レプリカが作成されない可能性がある問題を修正 [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)

-   TiFlash

    -   ウィンドウ関数がクエリのキャンセル時にTiFlashをクラッシュさせる可能性がある問題を修正 [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
    -   `CAST(value AS DATETIME)`への誤ったデータ入力が原因でTiFlashシステムの CPU 使用率が高くなる問題を修正しました [#5097](https://github.com/pingcap/tiflash/issues/5097) @[xzhangxian1008](https://github.com/xzhangxian1008)
    -   `CAST(Real/Decimal AS time)`の結果が MySQL と一致しない問題を修正します [#3779](https://github.com/pingcap/tiflash/issues/3779) @[mengxin9014](https://github.com/mengxin9014)
    -   ストレージ内の一部の古いデータが削除できない問題を修正 [#5570](https://github.com/pingcap/tiflash/issues/5570) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   ページ GC がテーブルの作成をブロックする可能性がある問題を修正 [#5697](https://github.com/pingcap/tiflash/issues/5697) @[JaySon-Huang](https://github.com/JaySon-Huang)
    -   `NULL`値を含む列でプライマリ インデックスを作成した後に発生するpanicを修正 [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

-   ツール

    -   Backup & Restore (BR)

        -   チェックポイントの情報が古くなる可能性がある問題を修正 [#36423](https://github.com/pingcap/tidb/issues/36423) @[YuJuncen](https://github.com/YuJuncen)
        -   復元中に同時実行数の設定が大きすぎるため、リージョンのバランスが取れていない問題を修正 [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        -   クラスター内に TiCDC が存在する場合にログバックアップチェックポイント TS が停止する可能性がある問題を修正します [#37822](https://github.com/pingcap/tidb/issues/37822) @[YuJuncen](https://github.com/YuJuncen)
        -   外部ストレージの認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正しました [#37469](https://github.com/pingcap/tidb/issues/37469) @[MoCuishle28](https://github.com/MoCuishle28)

    -   TiCDC

        -   TiCDCがgRPCサービスで誤ったPDアドレスに対して不正確なエラーを返す問題を修正 [#6458](https://github.com/pingcap/tiflow/issues/6458) @[crelax](https://github.com/crelax)
        -   `cdc cause cli changefeed list`コマンドが失敗した変更フィードを返さない問題を修正 [#6334](https://github.com/pingcap/tiflow/issues/6334) @[asddongmen](https://github.com/asddongmen)
        -   変更フィードの初期化に失敗した場合に TiCDC が利用できなくなる問題を修正 [#6859](https://github.com/pingcap/tiflow/issues/6859) @[asddongmen](https://github.com/asddongmen)

    -   TiDB Binlog

        -   コンプレッサーがgzipに設定されている場合に、 DrainerがPumpにリクエストを正しく送信できない問題を修正 [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @[lichunzhu](https://github.com/lichunzhu)

    -   TiDB Data Migration (DM)

        -   DMが`Specified key was too long`エラー [#5315](https://github.com/pingcap/tiflow/issues/5315)を報告する問題を修正しました @[lance6716](https://github.com/lance6716)
        -   リレーがエラーに遭遇した際のゴルーチンリークを修正 [#6193](https://github.com/pingcap/tiflow/issues/6193) @[lance6716](https://github.com/lance6716)
        -   `collation_compatible` `"strict"`に設定した場合に、DM が重複した照合順序を持つ SQL を生成する可能性がある問題を修正します [#6832](https://github.com/pingcap/tiflow/issues/6832) @[lance6716](https://github.com/lance6716)
        -   DM-workerログにおける警告メッセージ「 binlog status_varsからタイムゾーンを取得する際にエラーが発生しました」の表示を減らす [#6628](https://github.com/pingcap/tiflow/issues/6628) @[lyzx2001](https://github.com/lyzx2001)
        -   レプリケーション中にlatin1データが破損する可能性がある問題を修正 [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正しました [#36980](https://github.com/pingcap/tidb/issues/36980) @[D3Hunter](https://github.com/D3Hunter)

## 貢献者 {#contributors}

TiDBコミュニティの以下の貢献者の皆様に感謝申し上げます。

-   @[An-DJ](https://github.com/An-DJ)
-   [AnnieoftheStars](https://github.com/AnnieoftheStars)
-   @[AntiTopQuark](https://github.com/AntiTopQuark)
-   @[blacktear23](https://github.com/blacktear23)
-   @[BurtonQin](https://github.com/BurtonQin) (初回貢献者)
-   @[crelax](https://github.com/crelax)
-   @[eltociear](https://github.com/eltociear)
-   @[fuzhe1989](https://github.com/fuzhe1989)
-   @[erwadba](https://github.com/erwadba)
-   @[jianzhiyao](https://github.com/jianzhiyao)
-   @[joycse06](https://github.com/joycse06)
-   @[morgo](https://github.com/morgo)
-   @[onlyacat](https://github.com/onlyacat)
-   @[peakji](https://github.com/peakji)
-   [rzrymiak](https://github.com/rzrymiak)
-   @[tisonkun](https://github.com/tisonkun)
-   @[whitekeepwork](https://github.com/whitekeepwork)
-   @[Ziy1-Tan](https://github.com/Ziy1-Tan)

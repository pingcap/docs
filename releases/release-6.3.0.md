---
title: TiDB 6.3.0 Release Notes
---

# TiDB 6.3.0 リリースノート {#tidb-6-3-0-release-notes}

発売日：2022年9月30日

TiDB バージョン: 6.3.0-DMR

クイック アクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb) | [インストール パッケージ](https://www.pingcap.com/download/?version=v6.3.0#version-list)

v6.3.0-DMR の主な新機能と改善点は次のとおりです。

-   TiKV は、SM4 アルゴリズムを使用した保存時の暗号化をサポートしています。
-   TiDB は、SM3 アルゴリズムを使用した認証をサポートしています。
-   `CREATE USER`および`ALTER USER`ステートメントは`ACCOUNT LOCK/UNLOCK`オプションをサポートします。
-   JSON データ型と関数が一般提供 (GA) になりました。
-   TiDB は、null 認識アンチ結合をサポートしています。
-   TiDB は、より細かい粒度で実行時間メトリックを提供します。
-   範囲パーティションの定義を簡素化するために、新しい構文糖衣が追加されました。
-   範囲 COLUMNS パーティショニングは、複数の列の定義をサポートしています。
-   インデックスを追加するパフォーマンスは 3 倍になります。
-   リソースを消費するクエリが軽量クエリの応答時間に与える影響を 50% 以上削減します。

## 新機能 {#new-features}

### SQL {#sql}

-   新しいシンタックス シュガー (Range INTERVAL パーティショニング) を追加して、Range パーティションの定義を簡素化します (実験的) [#35683](https://github.com/pingcap/tidb/issues/35683) @ [ミヨンス](https://github.com/mjonss)

    TiDB は、Range パーティションを定義する新しい方法として[INTERVAL パーティショニング](/partitioned-table.md#range-interval-partitioning)を提供します。すべてのパーティションを列挙する必要がないため、Range パーティション分割 DDL ステートメントの長さが大幅に短縮されます。構文は、元の Range パーティショニングの構文と同等です。

-   範囲 COLUMNS パーティショニングは、複数の列[#36636](https://github.com/pingcap/tidb/issues/36636) @ [ミヨンス](https://github.com/mjonss)の定義をサポートします

    TiDB は[範囲列による分割 (column_list)](/partitioned-table.md#range-columns-partitioning)をサポートしています。 `column_list`は、単一の列に制限されなくなりました。基本的な機能はMySQLと同じです。

-   [交換パーティション](/partitioned-table.md#partition-management) GA [#35996](https://github.com/pingcap/tidb/issues/35996) @ [ymkzpx](https://github.com/ymkzpx)になります

-   TiFlash [#5579](https://github.com/pingcap/tiflash/issues/5579) @ [シーライズ](https://github.com/SeaRise)への 2 つ以上の[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md)のプッシュダウンをサポート

    -   `LEAD()`
    -   `LAG()`

-   DDL 変更中の DML 成功率を向上させるために、軽量のメタデータ ロックを提供します (実験的) [#37275](https://github.com/pingcap/tidb/issues/37275) @ [wjhuang2016](https://github.com/wjhuang2016)

    TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータ オブジェクトの変更をサポートします。トランザクションが実行されると、トランザクションの開始時に対応するメタデータ スナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。この問題を解決するために、TiDB v6.3.0 ではオンライン DDL アルゴリズムに[メタデータ ロック](/metadata-lock.md)が導入されています。可能な限り DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、実行中の DDL を古いメタデータを持つ DML がコミットされるまで待機させます。

-   インデックス追加のパフォーマンスを改善し、DML トランザクションへの影響を軽減します (実験的) [#35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037)

    インデックス作成時のバックフィルの速度を向上させるために、TiDB v6.3.0 は、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)システム変数が有効になっている場合に`ADD INDEX`および`CREATE INDEX` DDL 操作を高速化します。この機能を有効にすると、インデックスを追加するパフォーマンスが約 3 倍になります。

### Security {#security}

-   TiKV は保存時の暗号化に SM4 アルゴリズムをサポートします[#13041](https://github.com/tikv/tikv/issues/13041) @ [嘉陽正](https://github.com/jiayang-zheng)

    保存時の TiKV 暗号化の場合は[SM4 アルゴリズム](/encryption-at-rest.md)を追加します。保存時の暗号化を構成する場合、構成`data-encryption-method`の値を`sm4-ctr`に設定することにより、SM4 暗号化容量を有効にすることができます。

-   TiDB は SM3 アルゴリズム[#36192](https://github.com/pingcap/tidb/issues/36192) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)による認証をサポートします

    TiDB は、SM3 アルゴリズムに基づく認証プラグイン[`tidb_sm3_password`](/security-compatibility-with-mysql.md)を追加します。このプラグインを有効にすると、SM3 アルゴリズムを使用してユーザー パスワードが暗号化および検証されます。

-   TiDB JDBC は、SM3 アルゴリズム[#25](https://github.com/pingcap/mysql-connector-j/issues/25) @ [最後の切歯](https://github.com/lastincisor)による認証をサポートします。

    ユーザー パスワードの認証には、クライアント側のサポートが必要です。 [JDBC は SM3 アルゴリズムをサポートします](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)であるため、TiDB-JDBC 経由で SM3 認証を使用して TiDB に接続できます。

### 可観測性 {#observability}

-   TiDB は、SQL クエリの実行時間[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)の詳細なメトリクスを提供します

    TiDB v6.3.0 は、 [実行時間の詳細な観察](/latency-breakdown.md)のきめ細かいデータ メトリックを提供します。完全でセグメント化されたメトリクスにより、SQL クエリの主な時間消費を明確に理解し、重要な問題をすばやく見つけてトラブルシューティングの時間を節約できます。

-   スローログと`TRACE`ステートメントの拡張出力[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 では、スロー ログの出力が強化され、 `TRACE` . TiDB の解析から KV RocksDB のディスクへの書き込みまでの[フルリンク期間](/latency-breakdown.md)の SQL クエリを観察でき、診断機能がさらに強化されます。

-   TiDB ダッシュボードはデッドロックの履歴情報を提供します[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)

    v6.3.0 から、TiDB ダッシュボードはデッドロック履歴を提供します。 TiDB ダッシュボードでスロー ログを確認し、一部の SQL ステートメントのロック待機時間が長すぎることがわかった場合は、デッドロックの履歴を確認して根本原因を突き止めることができるため、診断が容易になります。

### パフォーマンス {#performance}

-   TiFlash はFastScan の使用方法を変更します (実験的) [#5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)

    v6.2.0 では、 TiFlashに FastScan 機能が導入されました。これにより、期待されるパフォーマンスの向上がもたらされますが、使用時の柔軟性に欠けます。したがって、v6.3.0 では、 TiFlash は[FastScanの使い方](/develop/dev-guide-use-fastscan.md)を変更します。FastScan を有効または無効にする`ALTER TABLE ... SET TIFLASH MODE ...`構文は非推奨です。代わりに、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して、FastScan を有効にするかどうかを簡単に制御できます。

    v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。変数`tiflash_fastscan`を設定する必要があります。 v6.2.0 以前のバージョンから v6.3.0 にアップグレードする場合、データの一貫性を保つために、デフォルトではすべてのセッションで FastScan 機能が有効になっていません。

-   TiFlash は、複数の同時実行タスクのシナリオでデータ スキャンのパフォーマンスを最適化します[#5376](https://github.com/pingcap/tiflash/issues/5376) @ [リン・ジンヘ](https://github.com/JinheLin)

    TiFlash は、同じデータの読み取り操作を組み合わせることで、同じデータの重複読み取りを減らします。リソースのオーバーヘッドと[同時タスクの場合のデータ スキャンのパフォーマンスが向上します。](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を最適化します。複数の同時タスクの場合、各タスクが同じデータを個別に読み取る必要がある状況を回避し、同じデータを同時に複数読み取る可能性を回避します。

    この機能は v6.2.0 で実験的であり、v6.3.0 で GA になります。

-   TiFlash はデータ複製のパフォーマンスを向上させます[#5237](https://github.com/pingcap/tiflash/issues/5237) @ [そよ風](https://github.com/breezewish)

    TiFlash は、 TiKV からのデータ複製にRaftプロトコルを使用します。 v6.3.0 より前のバージョンでは、大量のレプリカ データをレプリケートするには長い時間がかかることがよくありました。 TiDB v6.3.0 は、 TiFlashデータ複製メカニズムを最適化し、複製速度を大幅に改善します。 BRを使用してデータを回復したり、 TiDB Lightningを使用してデータをインポートしたり、新しいTiFlashレプリカを追加したりすると、 TiFlashレプリカをより迅速に複製できます。よりタイムリーにTiFlashを使用してクエリを実行できます。さらに、 TiFlashレプリカの数をスケールアップ、スケールダウン、または変更すると、 TiFlashレプリカは安全でバランスのとれた状態により速く到達します。

-   TiFlash は、個々の`COUNT(DISTINCT)` [#37202](https://github.com/pingcap/tidb/issues/37202) @ [fixdb](https://github.com/fixdb)の 3 段階の集約をサポートします。

    TiFlash は、 `COUNT(DISTINCT)`を 1 つだけ含むクエリを[三段集計](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)に書き換えることをサポートしています。これにより、同時実行性とパフォーマンスが向上します。

-   TiKV はログのリサイクルをサポートします[#214](https://github.com/tikv/raft-engine/issues/214) @ [Lykxサシネーター](https://github.com/LykxSassinator)

    TiKV はRaft Engineで[ログファイルのリサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)をサポートします。これにより、 Raftログの追加中のネットワーク ディスクのロング テールレイテンシーが減少し、書き込みワークロードでのパフォーマンスが向上します。

-   TiDB は null 認識のアンチ結合[#37525](https://github.com/pingcap/tidb/issues/37525) @ [アレナトルクス](https://github.com/Arenatlx)をサポートします

    TiDB v6.3.0 では、新しい結合タイプ[Null 認識アンチ結合 (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)が導入されました。 NAAJ は、コレクション操作を処理するときに、コレクションが空か`NULL`を認識することができます。これにより、 `IN`や`= ANY`などの操作の実行効率が最適化され、SQL のパフォーマンスが向上します。

-   Hash Join [#35439](https://github.com/pingcap/tidb/issues/35439) @ [思い出す](https://github.com/Reminiscent)のビルド終了を制御するためのオプティマイザー ヒントを追加します。

    v6.3.0 では、TiDB オプティマイザーは`HASH_JOIN_BUILD()`と`HASH_JOIN_PROBE()`の 2 つのヒントを導入して、ハッシュ結合、そのプローブ エンド、およびビルド エンドを指定します。オプティマイザが最適な実行計画の選択に失敗した場合、これらのヒントを使用して計画に介入できます。

-   セッション レベルの共通テーブル式 (CTE) インライン[#36514](https://github.com/pingcap/tidb/issues/36514) @ [エルザ0520](https://github.com/elsa0520)をサポート

    TiDB v6.2.0 では、オプティマイザーに`MERGE`ヒントを導入して CTE インラインを許可し、CTE クエリ結果のコンシューマーがTiFlashで並列に実行できるようにしました。 v6.3.0 では、セッション変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)が導入され、セッションで CTE インラインが可能になりました。これにより、使いやすさが大幅に向上します。

### 取引 {#transactions}

-   悲観的トランザクション[#36579](https://github.com/pingcap/tidb/issues/36579) @ [エキキシウム](https://github.com/ekexium)で一意制約の遅延チェックをサポート

    [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)システム変数を使用して、悲観的トランザクションで TiDB が[一意の制約](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御できます。この変数はデフォルトで無効になっています。変数が有効になっている ( `ON`に設定されている) 場合、TiDB は悲観的トランザクションのロック操作と一意制約チェックを必要になるまで延期するため、一括 DML 操作のパフォーマンスが向上します。

-   Read-Committed 分離レベル[#36812](https://github.com/pingcap/tidb/issues/36812) @ [トンスネークリン](https://github.com/TonsnakeLin)で TSO をフェッチする方法を最適化します。

    Read-Committed 分離レベルでは、システム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)が導入され、TSO のフェッチ方法が制御されます。 Plan Cache ヒットの場合、TiDB は TSO を取得する頻度を減らすことでバッチ DML ステートメントの実行効率を改善し、バッチで実行されているタスクの実行時間を短縮します。

### 安定性 {#stability}

-   リソースを消費するクエリが軽量クエリの応答時間に与える影響を軽減する[#13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

    リソースを消費するクエリと軽量クエリを同時に実行すると、軽量クエリの応答時間が影響を受けます。この場合、トランザクション サービスの品質を確保するために、軽量のクエリは TiDB によって最初に処理されることが期待されます。 v6.3.0 では、TiKV は読み取りリクエストのスケジューリング メカニズムを最適化し、各ラウンドでリソースを消費するクエリの実行時間が期待どおりになるようにします。これにより、リソースを消費するクエリが軽量クエリの応答時間に与える影響が大幅に減少し、混合ワークロード シナリオで P99レイテンシーが 50% 以上削減されます。

-   統計が古くなったときに統計をロードするデフォルトのポリシーを変更します[#27601](https://github.com/pingcap/tidb/issues/27601) @ [しゅいふぁんグリーンアイズ](https://github.com/xuyifangreeneyes)

    v5.3.0 で、TiDB はシステム変数[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)を導入して、統計が古くなったときのオプティマイザの動作を制御しました。デフォルト値は`ON`です。これは、古いバージョンの動作を維持することを意味します。SQL ステートメントに含まれるオブジェクトの統計が古い場合、オプティマイザーは統計 (テーブルの行の合計数以外) が無効であると見なします。より信頼性が高くなり、代わりに疑似統計を使用します。実際のユーザー シナリオのテストと分析の後、デフォルト値の`tidb_enable_pseudo_for_outdated_stats`は v6.3.0 以降`OFF`に変更されました。統計が古くなっても、オプティマイザはテーブルの統計を引き続き使用するため、実行計画がより安定します。

-   タイタンを無効化すると GA @ [タボキー](https://github.com/tabokie)になります

    オンラインの TiKV ノードに対して[タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan)を実行できます。

-   GlobalStats の準備ができていない場合は、 `static`パーティション プルーニングを使用する[#37535](https://github.com/pingcap/tidb/issues/37535) @ [イサール](https://github.com/Yisaer)

    [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode)が有効な場合、オプティマイザは[グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)に基づいて実行計画を選択します。 GlobalStats が完全に収集される前に、疑似統計を使用すると、パフォーマンスが低下する可能性があります。 v6.3.0 では、GlobalStats が収集される前に動的プルーニングを有効にする場合、 `static`モードを維持することでこの問題に対処しています。 GlobalStats が収集されるまで、TiDB は`static`モードのままです。これにより、パーティションのプルーニング設定を変更する際のパフォーマンスの安定性が確保されます。

### 使いやすさ {#ease-of-use}

-   SQL ベースのデータ配置ルールとTiFlashレプリカ間の競合に対処する[#37171](https://github.com/pingcap/tidb/issues/37171) @ [ルクァンチャオ](https://github.com/lcwangchao)

    TiDB v6.0.0 は、SQL ベースのデータ配置ルールを提供します。ただし、この機能は、実装上の問題により、 TiFlashレプリカと競合します。 TiDB v6.3.0 は実装メカニズムを最適化し、 [SQL ベースのデータ配置ルールとTiFlashの間の競合を解決します](/placement-rules-in-sql.md#known-limitations) .

### MySQL の互換性 {#mysql-compatibility}

-   `REGEXP_INSTR()` 、および`REGEXP_REPLACE()` `REGEXP_SUBSTR()` @ [風の語り手](https://github.com/windtalker)の 4 つの正規表現関数のサポート`REGEXP_LIKE()`追加することにより、MySQL 8.0 [#23881](https://github.com/pingcap/tidb/issues/23881)互換性を向上させます。

    MySQL との互換性の詳細については、 [MySQL との正規表現の互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)を参照してください。

-   `CREATE USER`および`ALTER USER`ステートメントは、 `ACCOUNT LOCK/UNLOCK`オプション[#37051](https://github.com/pingcap/tidb/issues/37051) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポートします。

    [`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを使用してユーザーを作成する場合、 `ACCOUNT LOCK/UNLOCK`オプションを使用して、作成したユーザーをロックするかどうかを指定できます。ロックされたユーザーはデータベースにログインできません。

    [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントの`ACCOUNT LOCK/UNLOCK`オプションを使用して、既存のユーザーのロック状態を変更できます。

-   JSON データ型と JSON関数はGA [#36993](https://github.com/pingcap/tidb/issues/36993) @ [ションジウェイ](https://github.com/xiongjiwei)になります

    JSON は、多数のプログラムで採用されている一般的なデータ形式です。 TiDB は、以前のバージョンから実験的機能として[JSON のサポート](/data-type-json.md)を導入しており、MySQL の JSON データ型および一部の JSON関数と互換性があります。

    TiDB v6.3.0 では、JSON データ型と関数がGA になり、TiDB のデータ型が充実し、 [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)と[生成列](/generated-columns.md)で JSON関数の使用がサポートされ、TiDB と MySQL との互換性がさらに向上します。

### バックアップと復元 {#backup-and-restore}

-   PITR はバックアップ ストレージとして[GCS と Azure Blob Storage](/br/backup-and-restore-storages.md)をサポート @ [ジョッカウ](https://github.com/joccau)

    TiDB クラスターが GCP または Azure にデプロイされている場合は、クラスターを v6.3.0 にアップグレードした後に PITR 機能を使用できます。

-   BR はAWS S3 オブジェクト ロック[#13442](https://github.com/tikv/tikv/issues/13442) @ [3ポインター](https://github.com/3pointer)をサポートします

    [S3 オブジェクト ロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)を有効にすることで、AWS 上のバックアップ データを改ざんや削除から保護できます。

### データ移行 {#data-migration}

-   TiDB Lightning は[Apache Hive によってエクスポートされた Parquet ファイルを TiDB にインポートする](/tidb-lightning/tidb-lightning-data-source.md#parquet) [#37536](https://github.com/pingcap/tidb/issues/37536) @ [ぶちゅとでごう](https://github.com/buchuitoudegou)をサポート

-   DM が新しい構成アイテムを追加します`safe-mode-duration` [#6224](https://github.com/pingcap/tiflow/issues/6224) @ [オクジャン](https://github.com/okJiang)

    この構成アイテムは[タスク構成ファイル](/dm/task-configuration-file-full.md)に追加されます。 DM が異常終了した後の自動セーフ モード期間を調整できます。デフォルト値は 60 秒です。 `safe-mode-duration`が`"0s"`に設定されている場合、異常な再起動後に DM がセーフ モードに入ろうとすると、エラーが報告されます。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、複数の地理的に分散されたデータ ソースからデータを複製できる展開トポロジをサポートします[#5301](https://github.com/pingcap/tiflow/issues/5301) @ [スドジ](https://github.com/sdojjy)

    v6.3.0 以降、単一の TiDB クラスターから複数の地理的[複数のIDCにTiCDCを展開できます](/ticdc/deploy-ticdc.md)分散されたデータ システムへのデータの複製をサポートするには、各 IDC のデータを複製します。この機能は、地理的に分散されたデータ レプリケーションおよび展開トポロジの機能を提供するのに役立ちます。

-   TiCDC は、アップストリームとダウンストリーム (同期ポイント) の間でスナップショットの一貫性を維持することをサポートします[#6977](https://github.com/pingcap/tiflow/issues/6977) @ [アスドンメン](https://github.com/asddongmen)

    ディザスター リカバリーのためのデータ レプリケーションのシナリオでは、TiCDC は[ダウンストリーム データのスナップショットを定期的に維持する](/sync-diff-inspector/upstream-downstream-diff.md#data-check-for-tidb-upstream-and-downstream-clusters)をサポートし、ダウンストリーム スナップショットがアップストリーム スナップショットと一致するようにします。この機能により、TiCDC は読み取りと書き込みが分離されているシナリオをより適切にサポートし、コストの削減に役立ちます。

-   TiCDC はグレースフル アップグレードをサポート[#4757](https://github.com/pingcap/tiflow/issues/4757) @ [大静脈](https://github.com/overvenus) @ [3AceShowHand](https://github.com/3AceShowHand)

    [TiUP](/ticdc/deploy-ticdc.md#upgrade-cautions) (&gt;=v1.11.0) または[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (&gt;=v1.3.8) を使用して TiCDC をデプロイすると、TiCDC クラスターを適切にアップグレードできます。アップグレード中、データ レプリケーションのレイテンシーは30 秒に抑えられます。これにより安定性が向上し、TiCDC がレイテンシーの影響を受けやすいアプリケーションをより適切にサポートできるようになります。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                         | タイプを変更 | 説明                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                       | 修正済み   | 新しいオプション`tidb_sm3_password`を追加します。この変数が`tidb_sm3_password`に設定されている場合、SM3 が暗号化アルゴリズムとして使用されます。                                                                                                                                                    |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630)                                       | 新規追加   | テーブルに主キーがあるという要件を強制するかどうかを制御します。この変数を有効にした後、主キーなしでテーブルを作成または変更しようとすると、エラーが発生します。                                                                                                                                                                 |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)             | 新規追加   | [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合に、TiDBサーバーがTiDBサーバーと同じリージョン内のレプリカに読み取り要求を送信することを好むしきい値を制御します。                                                                               |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | 新規追加   | 悲観的トランザクションで TiDB が[一意の制約](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御します。                                                                                                                                                          |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)                                               | 新規追加   | [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が有効な場合にのみ有効です。インデックス作成時のバックフィル時のローカルstorageの使用制限を設定します。                                                                                               |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                 | 新規追加   | `ADD INDEX`および`CREATE INDEX` DDL 操作のアクセラレーションを有効にして、インデックス作成時のバックフィルの速度を向上させるかどうかを制御します。                                                                                                                                                         |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                         | 新規追加   | `flashback cluster`の並行性を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                       |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition)                                     | 非推奨    | [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトで`exchange partitions with tables`が有効になっています。                                                                           |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                       | 新規追加   | `FOREIGN KEY`機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                     |
| [`tidb_enable_general_plan_cache`](/system-variables.md#tidb_enable_general_plan_cache-new-in-v630)                         | 新規追加   | 一般プラン キャッシュ機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                       |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                   | 新規追加   | [メタデータ ロック](/metadata-lock.md)機能を有効にするかどうかを指定します。                                                                                                                                                                                                |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                     | 新規追加   | Anti Join が特別なセット演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによって生成されるときに、TiDB が Null-Aware Hash Join を適用するかどうかを制御します。                                                                                                                                    |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)           | 修正済み   | 統計が古い場合にテーブルの統計を使用する際のオプティマイザの動作を制御します。デフォルト値は`ON`から`OFF`に変更されます。これは、このテーブルの統計が古くなっても、オプティマイザが引き続きテーブルの統計を使用し続けることを意味します。                                                                                                                        |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)                                       | 修正済み   | データを読み取るオペレーターの動的メモリ制御機能を有効にするかどうかを制御します。この変数が`ON`に設定されている場合、メモリ使用量は[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制御下にない可能性があります。したがって、デフォルト値は`ON`から`OFF`に変更されます。                                                          |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 新規追加   | SQL 書き込みステートメントの読み取り要求をTiFlashにプッシュするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                     |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新規追加   | 安全でない方法で式を生成された列に置き換えるかどうかを制御します。                                                                                                                                                                                                                |
| [`tidb_general_plan_cache_size`](/system-variables.md#tidb_general_plan_cache_size-new-in-v630)                             | 新規追加   | 一般プラン キャッシュでキャッシュできる実行プランの最大数を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                 |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新規追加   | 読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`回の実行の結果を取得するために使用されます。                                                                                                                                                                                   |
| [tidb_max_paging_size](/system-variables.md#tidb_max_paging_size-new-in-v630)                                               | 新規追加   | この変数は、コプロセッサーのページング要求プロセス中に行の最小数を設定するために使用されます。                                                                                                                                                                                                  |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)                                   | 新規追加   | セッション全体で共通テーブル式 (CTE) をインライン化するかどうかを制御します。デフォルト値は`OFF`です。これは、インライン CTE がデフォルトで強制されないことを意味します。                                                                                                                                                    |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)                   | 新規追加   | MPP モードで`COUNT(DISTINCT)`集約を 3 段階集約に書き換えるかどうかを指定します。デフォルト値は`ON`です。                                                                                                                                                                               |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)                                    | 修正済み   | 動的プルーニングを有効にするかどうかを指定します。 v6.3.0 以降、デフォルト値は`dynamic`に変更されました。                                                                                                                                                                                    |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                           | 修正済み   | タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれな読み取りコミット分離レベルのシナリオに適しています。この機能は、特定のサービス ワークロードを対象としており、他のシナリオでパフォーマンスの低下を引き起こす可能性があります。このため、v6.3.0 以降、この変数のスコープが`GLOBAL \| SESSION`から`INSTANCE`に変更されました。つまり、特定の TiDB インスタンスに対してこの機能を有効にできるということです。 |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)                                         | 新規追加   | タイムスタンプの取得を最適化するために使用され、悲観的トランザクションの RC 分離レベルでポイント書き込み競合がほとんどないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバル タイムスタンプを取得することによって生じるレイテンシーとオーバーヘッドを回避できます。                                                                                     |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)                                                     | 新規追加   | FastScan を有効にするかどうかを制御します。 [ファストスキャン](/develop/dev-guide-use-fastscan.md)が有効になっている ( `ON`に設定されている) 場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。                                                                               |

### コンフィグレーションファイルのパラメーター {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                            | タイプを変更 | 説明                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------- | ------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)                                        | 新規追加   | 一時データを格納するために TiDB が使用するファイル システムの場所を指定します。機能が TiDB ノードのローカルstorageを必要とする場合、TiDB は対応する一時データをこの場所に保存します。デフォルト値は`/tmp/tidb`です。                                                                                                |
| TiKV           | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)              | 新規追加   | スレッド プール サイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。                                                                                                   |
| TiKV           | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method)                        | 修正済み   | 新しい値オプション`sm4-ctr`を導入します。この設定項目が`sm4-ctr`に設定されている場合、データは保存前に SM4 を使用して暗号化されます。                                                                                                                                              |
| TiKV           | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                    | 新規追加   | Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。有効にすると、論理的にパージされたログ ファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが短縮されます。この構成アイテムは、 [フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v630)が &gt;= 2 の場合にのみ使用できます。 |
| TiKV           | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                            | 新規追加   | Raft Engineのログ ファイルのバージョンを指定します。デフォルトのログ ファイル バージョンは、v6.3.0 より前の TiKV では`1`です。ログ ファイルは、TiKV &gt;= v6.1.0 で読み取ることができます。デフォルトのログ ファイル バージョンは、TiKV v6.3.0 以降では`2`です。 TiKV v6.3.0 以降では、ログ ファイルを読み取ることができます。                     |
| TiKV           | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620)                                 | 修正済み   | v6.3.0 以降、デフォルト値が`false`から`true`に変更されました。                                                                                                                                                                                   |
| TiKV           | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620)         | 修正済み   | v6.3.0 以降、デフォルト値が`5min`から`3min`に変更されました。                                                                                                                                                                                    |
| PD             | [有効化診断](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                      | 新規追加   | 診断機能を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                      |
| TiFlash        | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)   | 非推奨    | v6.3.0 以降、この構成アイテムは廃止されました。スレッド プールは、デフォルトでstorageエンジンからの読み取り要求を処理するために使用され、無効にすることはできません。                                                                                                                                  |
| DM             | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新規追加   | 自動セーフ モードの期間を指定します。                                                                                                                                                                                                         |
| TiCDC          | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新規追加   | 同期点機能を有効にするかどうかを指定します。                                                                                                                                                                                                      |
| TiCDC          | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)        | 新規追加   | 同期点が上流と下流のスナップショットを調整する間隔を指定します。                                                                                                                                                                                            |
| TiCDC          | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新規追加   | 同期点がダウンストリーム テーブルにデータを保持する期間を指定します。この期間を超えると、データはクリーンアップされます。                                                                                                                                                               |
| TiCDC          | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters)                      | 非推奨    | `memory`ソートは非推奨です。どのような状況でも使用することはお勧めしません。                                                                                                                                                                                  |

### その他 {#others}

-   ログ バックアップは、GCS と Azure Blob Storage をバックアップstorageとしてサポートします。
-   ログ バックアップが`exchange partition` DDL と互換性を持つようになりました。
-   [ファストスキャン](/develop/dev-guide-use-fastscan.md)を有効にするために以前に使用された SQL ステートメント`ALTER TABLE ...SET TiFLASH MODE ...`廃止され、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)に置き換えられました。 v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。この場合、変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を構成して FastScan を有効または無効にする必要があります。以前のバージョンから v6.3.0 にアップグレードする場合、FastScan 機能は、データの一貫性を保つためにすべてのセッションに対してデフォルトで有効になっていません。
-   Linux AMD64アーキテクチャでTiFlashを展開するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを展開するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セットの拡張機能を使用することで、TiFlash のベクトル化エンジンはパフォーマンスを向上させることができます。
-   TiDB で動作する HAProxy の最小バージョンは v1.5 になりました。 v1.5 から v2.1 までの HAProxy バージョンでは、 `post-41`構成オプションを`mysql-check`に設定する必要があります。 HAProxy v2.2 以降を使用することをお勧めします。

## 削除された機能 {#removed-feature}

v6.3.0 以降、TiCDC は Pulsar シンクの構成をサポートしなくなりました。 StreamNative が提供する[コップ](https://github.com/streamnative/kop)代替として使用できます。

## 改良点 {#improvements}

-   TiDB

    -   TiDB は、テーブルの存在をチェックするときに、ターゲット テーブル名の大文字と小文字を区別しないようになりました[#34610](https://github.com/pingcap/tidb/issues/34610) @ [ティアンカイマオ](https://github.com/tiancaiamao)
    -   `init_connect` [#35324](https://github.com/pingcap/tidb/issues/35324) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の値を設定するときに解析チェックを追加して、MySQL の互換性を向上させます。
    -   新しい接続[#34964](https://github.com/pingcap/tidb/issues/34964) @ [ションジウェイ](https://github.com/xiongjiwei)に対して生成されるログ警告を改善
    -   DDL 履歴ジョブをクエリするために HTTP API を最適化し、 `start_job_id`パラメータ[#35838](https://github.com/pingcap/tidb/issues/35838) @ [ティアンカイマオ](https://github.com/tiancaiamao)のサポートを追加します。
    -   JSON パスの構文が間違っている場合にエラーを報告する[#22525](https://github.com/pingcap/tidb/issues/22525) [#34959](https://github.com/pingcap/tidb/issues/34959) @ [ションジウェイ](https://github.com/xiongjiwei)
    -   誤った共有の問題を修正して結合操作のパフォーマンスを改善する[#37641](https://github.com/pingcap/tidb/issues/37641) @ [ゲンリキ](https://github.com/gengliqi)
    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)を使用して、一度に複数の SQL ステートメントの実行計画情報をエクスポートすることをサポートします。これにより、トラブルシューティングがより効率的になります[#37798](https://github.com/pingcap/tidb/issues/37798) @ [イサール](https://github.com/Yisaer)

-   TiKV

    -   `unreachable_backoff`つのピアが到達不能になった後にRaftstore があまりにも多くのメッセージをブロードキャストするのを避けるために、1 つのアイテムの構成をサポートします[#13054](https://github.com/tikv/tikv/issues/13054) @ [5kbps](https://github.com/5kbpers)
    -   TSO サービス[#12794](https://github.com/tikv/tikv/issues/12794) @ [ピンギュ](https://github.com/pingyu)の耐障害性の向上
    -   RocksDB で同時に実行されるサブ圧縮操作の数を動的に変更するサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)
    -   空のリージョン[#12421](https://github.com/tikv/tikv/issues/12421) @ [タボキー](https://github.com/tabokie)をマージするパフォーマンスを最適化する
    -   より多くの正規表現関数をサポート[#13483](https://github.com/tikv/tikv/issues/13483) @ [ゲンリキ](https://github.com/gengliqi)
    -   CPU 使用率[#13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)に基づくスレッド プール サイズの自動調整のサポート

-   PD

    -   TiDB ダッシュボード[#5366](https://github.com/tikv/pd/issues/5366) @ [YiniXu9506](https://github.com/YiniXu9506)の TiKV IO MBps メトリックのクエリを改善
    -   TiDB ダッシュボードの URL を`metrics`から`monitoring` [#5366](https://github.com/tikv/pd/issues/5366) @ [YiniXu9506](https://github.com/YiniXu9506)に変更します

-   TiFlash

    -   `elt`機能をTiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @ [意志のない](https://github.com/Willendless)にプッシュダウンをサポート
    -   `leftShift`機能をTiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @ [星のアニー](https://github.com/AnnieoftheStars)にプッシュダウンをサポート
    -   `castTimeAsDuration`機能をTiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @ [アンチトップクォーク](https://github.com/AntiTopQuark)にプッシュダウンをサポート
    -   `HexIntArg/HexStrArg`機能をTiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107) @ [ヤンケアオ](https://github.com/YangKeao)にプッシュダウンをサポート
    -   TiFlash のインタープリターをリファクタリングし、新しいインタープリター Planner [#4739](https://github.com/pingcap/tiflash/issues/4739) @ [シーライズ](https://github.com/SeaRise)をサポートします。
    -   TiFlash [#5609](https://github.com/pingcap/tiflash/issues/5609) @ [最高のウッディ](https://github.com/bestwoody)のメモリトラッカーの精度を向上
    -   `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN`照合[#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロツグ](https://github.com/solotzg)を使用して文字列列のパフォーマンスを向上させる
    -   ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401) , [#5091](https://github.com/pingcap/tiflash/issues/5091) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でバックグラウンドでの I/O スループットを計算します。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR は、ログ バックアップで生成された小さなファイルをマージできるため、バックアップ ファイルの数が大幅に削減されます[#13232](https://github.com/tikv/tikv/issues/13232) @ [レヴルス](https://github.com/Leavrth)
        -   PITR は、復元後のアップストリーム クラスター構成に基づいて、 TiFlashレプリカの数を自動的に構成することをサポートします[#37208](https://github.com/pingcap/tidb/issues/37208) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   アップストリームの TiDB [#6506](https://github.com/pingcap/tiflow/issues/6506) @ [ランス6716](https://github.com/lance6716)で導入された並行 DDL フレームワークとの TiCDC の互換性を改善します。
        -   MySQL シンクがエラー[#6460](https://github.com/pingcap/tiflow/issues/6460) @ [大静脈](https://github.com/overvenus)を受け取ったときの DML ステートメントのログ`start ts`のサポート
        -   `api/v1/health` API を強化して、TiCDC クラスター[#4757](https://github.com/pingcap/tiflow/issues/4757) @ [大静脈](https://github.com/overvenus)のより正確な正常性状態を返します
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させる[#5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイラスチン](https://github.com/hi-rustin)
        -   非推奨のパルサー シンク[#7087](https://github.com/pingcap/tiflow/issues/7087) @ [ハイラスチン](https://github.com/hi-rustin)を削除します。
        -   changefeed [#6447](https://github.com/pingcap/tiflow/issues/6447) @ [アスドンメン](https://github.com/asddongmen)に関係のない DDL ステートメントを破棄することで、レプリケーションのパフォーマンスを向上させます

    -   TiDB データ移行 (DM)

        -   データ ソースとして MySQL 8.0 との互換性を向上[#6448](https://github.com/pingcap/tiflow/issues/6448) @ [ランス6716](https://github.com/lance6716)
        -   「無効な接続」が発生したときに DDL を非同期で実行することにより、DDL を最適化します[#4689](https://github.com/pingcap/tiflow/issues/4689) @ [lyzx2001](https://github.com/lyzx2001)

    -   TiDB Lightning

        -   S3 外部storageURL のクエリ パラメータを追加して、特定のロール[#36891](https://github.com/pingcap/tidb/issues/36891) @ [dsdashun](https://github.com/dsdashun)を引き受けることで、別のアカウントの S3 データへのアクセスをサポートします

## バグの修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメント[#35784](https://github.com/pingcap/tidb/issues/35784) @ [ルクァンチャオ](https://github.com/lcwangchao)で権限チェックがスキップされる問題を修正
    -   システム変数`tidb_enable_noop_variable`が`WARN` [#36647](https://github.com/pingcap/tidb/issues/36647) @ [ルクァンチャオ](https://github.com/lcwangchao)に設定できる問題を修正
    -   式インデックスが定義されている場合、 `INFORMAITON_SCHEMA.COLUMNS`テーブルの`ORDINAL_POSITION`列が正しくない可能性がある問題を修正します[#31200](https://github.com/pingcap/tidb/issues/31200) @ [bb7133](https://github.com/bb7133)
    -   タイムスタンプが`MAXINT32` [#31585](https://github.com/pingcap/tidb/issues/31585) @ [bb7133](https://github.com/bb7133)より大きい場合に TiDB がエラーを報告しない問題を修正
    -   エンタープライズプラグイン使用時にTiDBサーバーが起動できない問題を修正[#37319](https://github.com/pingcap/tidb/issues/37319) @ [xhebox](https://github.com/xhebox)
    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @ [xhebox](https://github.com/xhebox)の間違った出力を修正
    -   一時テーブル[#37201](https://github.com/pingcap/tidb/issues/37201) @ [ルクァンチャオ](https://github.com/lcwangchao)での予期しない`EXCHANGE PARTITION`の動作を修正します
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると間違った結果が返される問題を修正 @ [ジムラーラ](https://github.com/zimulala)
    -   ビューの`EXPLAIN`クエリが権限[#34326](https://github.com/pingcap/tidb/issues/34326) @ [ホーキングレイ](https://github.com/hawkingrei)をチェックしない問題を修正
    -   JSON `null` `NULL` [#37852](https://github.com/pingcap/tidb/issues/37852) @ [ヤンケアオ](https://github.com/YangKeao)に更新できない問題を修正
    -   DDL ジョブの`row_count`が不正確であるという問題を修正[#25968](https://github.com/pingcap/tidb/issues/25968) @ [定義済み2014](https://github.com/Defined2014)
    -   `FLASHBACK TABLE`が正しく動作しない問題を修正[#37386](https://github.com/pingcap/tidb/issues/37386) @ [ティアンカイマオ](https://github.com/tiancaiamao)
    -   一般的な MySQL プロトコル[#36731](https://github.com/pingcap/tidb/issues/36731) @ [ドヴィーデン](https://github.com/dveeden)で`prepared`ステートメント フラグの処理に失敗する問題を修正します。
    -   いくつかの極端なケースで、起動時に誤った TiDB ステータスが表示される問題を修正します[#36791](https://github.com/pingcap/tidb/issues/36791) @ [xhebox](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.VARIABLES_INFO`がセキュリティ強化モード (SEM) [#37586](https://github.com/pingcap/tidb/issues/37586) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)に準拠していない問題を修正
    -   `UNION` [#31678](https://github.com/pingcap/tidb/issues/31678) @ [cbcwestwolf](https://github.com/cbcwestwolf)のクエリで文字列から文字列へのキャストがうまくいかない問題を修正
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @ [wshwsh12](https://github.com/wshwsh12)のパーティション テーブルで動的モードを有効にしたときに発生する間違った結果を修正します。
    -   TiDB のバイナリ文字列と JSON のキャストと比較が MySQL と互換性がない問題を修正[#31918](https://github.com/pingcap/tidb/issues/31918) [#25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケアオ](https://github.com/YangKeao)
    -   TiDB の`JSON_OBJECTAGG`と`JSON_ARRAYAGG`バイナリ値[#25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケアオ](https://github.com/YangKeao)で MySQL と互換性がない問題を修正
    -   JSON opaque 値の比較でpanic[#37315](https://github.com/pingcap/tidb/issues/37315) @ [ヤンケアオ](https://github.com/YangKeao)が発生する問題を修正
    -   JSON集計関数[#37287](https://github.com/pingcap/tidb/issues/37287) @ [ヤンケアオ](https://github.com/YangKeao)で単精度浮動小数点が使えない問題を修正
    -   `UNION`演算子が予期しない空の結果[#36903](https://github.com/pingcap/tidb/issues/36903) @ [ティアンカイマオ](https://github.com/tiancaiamao)を返す可能性がある問題を修正します
    -   `castRealAsTime`式の結果がMySQL [#37462](https://github.com/pingcap/tidb/issues/37462) @ [mengxin9014](https://github.com/mengxin9014)と矛盾する問題を修正
    -   悲観的DML 操作が一意でないインデックス キー[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキキシウム](https://github.com/ekexium)をロックする問題を修正します。
    -   `auto-commit`変更がトランザクションのコミット動作に影響する問題を修正[#36581](https://github.com/pingcap/tidb/issues/36581) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   トランザクション コミットが完了する前に、DML executor を含む`EXPLAIN ANALYZE`ステートメントが結果を返す可能性があるという問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   UPDATE ステートメントが誤ってプロジェクションを除外する場合があり、これにより`Can't find column`エラー[#37568](https://github.com/pingcap/tidb/issues/37568) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正します。
    -   結合したテーブルの再配置操作が Outer Join 条件[#37238](https://github.com/pingcap/tidb/issues/37238) @ [アイリンキッド](https://github.com/AilinKid)を誤ってプッシュ ダウンする問題を修正します。
    -   一部のパターンで`IN`および`NOT IN`サブクエリが`Can't find column`エラー[#37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid)を報告する問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に`Can't find column`が報告される問題を修正します。
    -   間違った`PromQL` [#35856](https://github.com/pingcap/tidb/issues/35856) @ [定義済み2014](https://github.com/Defined2014)を修正

-   TiKV

    -   リージョンのハートビートが中断された後、PD が TiKV に再接続しない問題を修正します[#12934](https://github.com/tikv/tikv/issues/12934) @ [バタフライ](https://github.com/bufferflies)
    -   Raftstore が[#13160](https://github.com/tikv/tikv/issues/13160) @ [5kbps](https://github.com/5kbpers)でビジー状態の場合、リージョンが重複する可能性がある問題を修正
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正します[#13191](https://github.com/tikv/tikv/issues/13191) @ [バタフライ](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @ [バートンチン](https://github.com/BurtonQin)
    -   暗号化を無効にすると TiKV がpanicになることがある問題を修正[#13081](https://github.com/tikv/tikv/issues/13081) @ [嘉陽正](https://github.com/jiayang-zheng)
    -   ダッシュボード[#13086](https://github.com/tikv/tikv/issues/13086) @ [栄光](https://github.com/glorv)の`Unified Read Pool CPU`の間違った表現を修正
    -   TiKV インスタンスが隔離されたネットワーク環境にある場合、数分間 TiKV サービスが利用できない問題を修正します[#12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)
    -   TiKV が誤って`PessimisticLockNotFound`エラー[#13425](https://github.com/tikv/tikv/issues/13425) @ [スティックナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   状況によっては PITR がデータ損失を引き起こす可能性がある問題を修正します[#13281](https://github.com/tikv/tikv/issues/13281) @ [ユジュンセン](https://github.com/YuJuncen)
    -   長い悲観的トランザクション[#13304](https://github.com/tikv/tikv/issues/13304) @ [ユジュンセン](https://github.com/YuJuncen)がある場合にチェックポイントが進められない問題を修正します。
    -   TiKV が JSON [#13417](https://github.com/tikv/tikv/issues/13417) @ [ヤンケアオ](https://github.com/YangKeao)で datetime 型 ( `DATETIME` 、 `DATE` 、 `TIMESTAMP` 、 `TIME` ) と`STRING`型を区別しない問題を修正
    -   JSON bool と他の JSON 値との比較の MySQL との非互換性を修正[#13386](https://github.com/tikv/tikv/issues/13386) [#37481](https://github.com/pingcap/tidb/issues/37481) @ [ヤンケアオ](https://github.com/YangKeao)

-   PD

    -   `enable-forwarding`が有効な場合に gRPC がエラーを不適切に処理するという問題によって引き起こされる PD パニックを修正します[#5373](https://github.com/tikv/pd/issues/5373) @ [バタフライ](https://github.com/bufferflies)
    -   異常なリージョンが PDpanic[#5491](https://github.com/tikv/pd/issues/5491) @ [ノルーチ](https://github.com/nolouch)を引き起こす可能性がある問題を修正します
    -   TiFlash学習者のレプリカが作成されない場合がある問題を修正[#5401](https://github.com/tikv/pd/issues/5401) @ [フンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   ウィンドウ関数により、クエリがキャンセルされたときにTiFlashがクラッシュする可能性がある問題を修正します[#5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `CAST(value AS DATETIME)`の間違ったデータ入力が原因でTiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @ [xzhangxian1008](https://github.com/xzhangxian1008)が高くなる問題を修正
    -   `CAST(Real/Decimal AS time)`の結果がMySQL [#3779](https://github.com/pingcap/tiflash/issues/3779) @ [mengxin9014](https://github.com/mengxin9014)と矛盾する問題を修正
    -   storage内の一部の古いデータを削除できない問題を修正[#5570](https://github.com/pingcap/tiflash/issues/5570) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ページ GC がテーブル[#5697](https://github.com/pingcap/tiflash/issues/5697) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の作成をブロックする可能性がある問題を修正します
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   チェックポイントの情報が古い[#36423](https://github.com/pingcap/tidb/issues/36423) @ [ユジュンセン](https://github.com/YuJuncen)になる問題を修正
        -   復元時に同時実行数が大きすぎるため、リージョンのバランスが取れていない問題を修正します[#37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   クラスタ[#37822](https://github.com/pingcap/tidb/issues/37822) @ [ユジュンセン](https://github.com/YuJuncen)に TiCDC が存在する場合、ログ バックアップ チェックポイント TS が停止する可能性がある問題を修正します。
        -   外部storageの認証キーに特殊文字が含まれているとバックアップや復元に失敗することがある問題を修正[#37469](https://github.com/pingcap/tidb/issues/37469) [@MoCuishle28](https://github.com/MoCuishle28)

    -   TiCDC

        -   grpc サービス[#6458](https://github.com/pingcap/tiflow/issues/6458) @ [クレラックス](https://github.com/crelax)で間違った PD アドレスに対して TiCDC が不正確なエラーを返す問題を修正します。
        -   `cdc cause cli changefeed list`コマンドが失敗した変更フィード[#6334](https://github.com/pingcap/tiflow/issues/6334) @ [アスドンメン](https://github.com/asddongmen)を返さない問題を修正します。
        -   changefeed の初期化が失敗したときに TiCDC が使用できない問題を修正します[#6859](https://github.com/pingcap/tiflow/issues/6859) @ [アスドンメン](https://github.com/asddongmen)

    -   TiDBBinlog

        -   コンプレッサーが gzip [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合、 Drainer がリクエストをPumpに正しく送信できない問題を修正します。

    -   TiDB データ移行 (DM)

        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   リレーがエラー[#6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときのゴルーチン リークを修正
        -   `collation_compatible`が`"strict"`に設定されている場合、DM が重複した照合順序[#6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)で SQL を生成する可能性があるという問題を修正します。
        -   DM-worker ログ[#6628](https://github.com/pingcap/tiflow/issues/6628) @ [lyzx2001](https://github.com/lyzx2001)で「 binlog status_vars からタイムゾーンを取得するときにエラーが見つかりました」という警告メッセージの表示を減らします
        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正します。

    -   TiDB Lightning

        -   TiDB Lightning が、 Parquet ファイル[#36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしていないという問題を修正します

## 寄稿者 {#contributors}

TiDB コミュニティの次の貢献者に感謝します。

-   @ [アンDJ](https://github.com/An-DJ)
-   @ [星のアニー](https://github.com/AnnieoftheStars)
-   @ [アンチトップクォーク](https://github.com/AntiTopQuark)
-   @ [ブラックティア23](https://github.com/blacktear23)
-   @ [バートンチン](https://github.com/BurtonQin) (初投稿者)
-   @ [クレラックス](https://github.com/crelax)
-   @ [エルトシア](https://github.com/eltociear)
-   @ [fuzhe1989](https://github.com/fuzhe1989)
-   @ [エルワドバ](https://github.com/erwadba)
-   @ [ジャンジヤオ](https://github.com/jianzhiyao)
-   @ [joycse06](https://github.com/joycse06)
-   @ [モルゴ](https://github.com/morgo)
-   @ [猫のみ](https://github.com/onlyacat)
-   @ [ピークジー](https://github.com/peakji)
-   @ [ルズリミアク](https://github.com/rzrymiak)
-   @ [ティソンクン](https://github.com/tisonkun)
-   @ [ホワイトキープワーク](https://github.com/whitekeepwork)
-   @ [Ziy1タン](https://github.com/Ziy1-Tan)

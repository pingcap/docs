---
title: TiDB 6.3.0 Release Notes
summary: 2022 年 9 月 30 日にリリースされた TiDB 6.3.0-DMR では、TiKV での SM4 アルゴリズムを使用した保存時の暗号化、TiDB での SM3 アルゴリズムを使用した認証、JSON データ型と関数のサポートなど、新機能と改善が導入されています。また、より細かい粒度で実行時間メトリックを提供し、スロー ログと TRACE` ステートメントの出力を強化し、TiDB ダッシュボードでデッドロック履歴情報をサポートします。さらに、TiDB v6.3.0 では、新しいシステム変数と構成ファイル パラメーターが導入され、さまざまなバグと問題が修正されています。このリリースには、TiKV、PD、 TiFlash、バックアップと復元 (BR)、TiCDC、TiDB Binlog、TiDB データ移行 (DM)、およびTiDB Lightningの改善も含まれています。
---

# TiDB 6.3.0 リリースノート {#tidb-6-3-0-release-notes}

発売日: 2022年9月30日

TiDB バージョン: 6.3.0-DMR

> **注記：**
>
> TiDB 6.3.0-DMR のドキュメントは[アーカイブ済み](https://docs-archive.pingcap.com/tidb/v6.3/)になりました。PingCAP では、TiDB データベースの[最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)使用することを推奨しています。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb)

v6.3.0-DMR の主な新機能と改善点は次のとおりです。

-   TiKV は、SM4 アルゴリズムを使用した保存時の暗号化をサポートします。
-   TiDB は SM3 アルゴリズムを使用した認証をサポートしています。
-   `CREATE USER`および`ALTER USER`ステートメントは`ACCOUNT LOCK/UNLOCK`オプションをサポートします。
-   JSON データ型と関数が一般提供 (GA) されます。
-   TiDB は null 対応のアンチ結合をサポートします。
-   TiDB は、より細かい粒度で実行時間メトリックを提供します。
-   範囲パーティション定義を簡素化するために、新しい構文糖が追加されました。
-   範囲列パーティションは複数の列の定義をサポートします。
-   インデックス追加のパフォーマンスが 3 倍になります。
-   リソースを消費するクエリが軽量クエリの応答時間に与える影響を 50% 以上削減します。

## 新機能 {#new-features}

### 構文 {#sql}

-   範囲パーティション定義を簡素化するための新しい構文糖 (範囲 INTERVAL パーティション) を追加します (実験的) [＃35683](https://github.com/pingcap/tidb/issues/35683) @ [ミョンス](https://github.com/mjonss)

    TiDB は、範囲パーティションを定義する新しい方法として[INTERVALパーティション分割](/partitioned-table.md#range-interval-partitioning)提供します。すべてのパーティションを列挙する必要がないため、範囲パーティション分割の DDL ステートメントの長さが大幅に短縮されます。構文は、元の範囲パーティション分割の構文と同じです。

-   範囲列パーティションは、複数の列[＃36636](https://github.com/pingcap/tidb/issues/36636) @ [ミョンス](https://github.com/mjonss)の定義をサポートします。

    TiDB は[範囲列によるパーティション分割 (column_list)](/partitioned-table.md#range-columns-partitioning)サポートします。3 `column_list`単一の列に制限されなくなりました。基本的な機能は MySQL と同じです。

-   [交換パーティション](/partitioned-table.md#partition-management) GA [＃35996](https://github.com/pingcap/tidb/issues/35996) @ [ymkzpx](https://github.com/ymkzpx)になります

-   2つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md)から[シーライズ](https://github.com/SeaRise)までのTiFlash [＃5579](https://github.com/pingcap/tiflash/issues/5579)へのプッシュダウンをサポート

    -   `LEAD()`
    -   `LAG()`

-   DDL 変更時の DML 成功率を向上させるために軽量メタデータ ロックを提供する (実験的) [＃37275](https://github.com/pingcap/tidb/issues/37275) @ [翻訳:](https://github.com/wjhuang2016)

    TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータ オブジェクトの変更をサポートします。トランザクションが実行されると、トランザクションの開始時に対応するメタデータ スナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。この問題を解決するために、TiDB v6.3.0 では、オンライン DDL アルゴリズムに[メタデータロック](/metadata-lock.md)導入されました。可能な限り DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、実行中の DDL が古いメタデータを持つ DML がコミットされるまで待機するようにします。

-   インデックス追加のパフォーマンスを改善し、DML トランザクションへの影響を軽減します (実験的) [＃35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037)

    インデックス作成時のバックフィル速度を向上させるために、TiDB v6.3.0 では、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)システム変数を有効にすると`ADD INDEX`および`CREATE INDEX` DDL 操作が高速化されます。この機能を有効にすると、インデックス追加のパフォーマンスが約 3 倍になります。

### Security {#security}

-   TiKVは保存時の暗号化にSM4アルゴリズムをサポートしています[＃13041](https://github.com/tikv/tikv/issues/13041) @ [嘉陽鄭](https://github.com/jiayang-zheng)

    保存時の TiKV 暗号化の場合は[SM4アルゴリズム](/encryption-at-rest.md)追加します。保存時の暗号化を構成する場合、 `data-encryption-method`構成の値を`sm4-ctr`に設定することで、 SM4 暗号化容量を有効にすることができます。

-   TiDBはSM3アルゴリズム[＃36192](https://github.com/pingcap/tidb/issues/36192) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)による認証をサポートしています

    TiDB は、SM3 アルゴリズムに基づく認証プラグイン[`tidb_sm3_password`](/security-compatibility-with-mysql.md)を追加します。このプラグインを有効にすると、ユーザー パスワードは SM3 アルゴリズムを使用して暗号化され、検証されます。

-   TiDB JDBCはSM3アルゴリズム[＃25](https://github.com/pingcap/mysql-connector-j/issues/25) @ [最後の切歯](https://github.com/lastincisor)による認証をサポートしています

    ユーザー パスワードの認証にはクライアント側のサポートが必要です。1 [JDBCはSM3アルゴリズムをサポートしています](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)では、TiDB-JDBC 経由で SM3 認証を使用して TiDB に接続できます。

### 可観測性 {#observability}

-   TiDBはSQLクエリ実行時間の詳細なメトリクスを提供します[＃34106](https://github.com/pingcap/tidb/issues/34106) @ [翻訳](https://github.com/cfzjywxk)

    TiDB v6.3.0 は、 [実行時間の詳細な観察](/latency-breakdown.md)のきめ細かいデータ メトリックを提供します。完全かつセグメント化されたメトリックを通じて、SQL クエリの主な時間消費を明確に把握し、主要な問題を迅速に見つけてトラブルシューティングの時間を節約できます。

-   スローログと`TRACE`ステートメント[＃34106](https://github.com/pingcap/tidb/issues/34106) @ [翻訳](https://github.com/cfzjywxk)の出力が強化されました

    TiDB v6.3.0 では、スロー ログと`TRACE`の出力が強化されています。TiDB の解析から KV RocksDB のディスクへの書き込みまでの[フルリンク期間](/latency-breakdown.md)の SQL クエリを観察できるため、診断機能がさらに強化されます。

-   TiDBダッシュボードはデッドロック履歴情報を提供します[＃34106](https://github.com/pingcap/tidb/issues/34106) @ [翻訳](https://github.com/cfzjywxk)

    v6.3.0 以降、TiDB ダッシュボードはデッドロック履歴を提供します。TiDB ダッシュボードでスロー ログを確認し、一部の SQL ステートメントのロック待機時間が過度に長いことがわかった場合は、デッドロック履歴を確認して根本原因を特定できるため、診断が容易になります。

### パフォーマンス {#performance}

-   TiFlash はFastScan の使い方を変えます (実験的) [＃5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユンヤン](https://github.com/hongyunyan)

    v6.2.0 では、 TiFlashに FastScan 機能が導入されました。この機能は、期待どおりのパフォーマンス向上をもたらしますが、使用上の柔軟性に欠けます。そのため、v6.3.0 では、 TiFlash は[FastScanの使い方](/tiflash/use-fastscan.md)変更しました。FastScan を有効または無効にする`ALTER TABLE ... SET TIFLASH MODE ...`構文は非推奨になりました。代わりに、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)使用して、FastScan を有効にするかどうかを簡単に制御できます。

    v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。変数`tiflash_fastscan`を設定する必要があります。v6.2.0 またはそれ以前のバージョンから v6.3.0 にアップグレードすると、データの一貫性を保つために、すべてのセッションで FastScan 機能がデフォルトで有効になりません。

-   TiFlashは、複数の同時実行タスクのシナリオでデータスキャンのパフォーマンスを最適化します[＃5376](https://github.com/pingcap/tiflash/issues/5376) @ [ジンヘリン](https://github.com/JinheLin)

    TiFlash は、同じデータの読み取り操作を組み合わせることで、同じデータの重複読み取りを削減します。リソースのオーバーヘッド[同時タスクの場合のデータスキャンのパフォーマンスが向上します](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)最適化し、複数の同時タスクの場合、各タスクが同じデータを個別に読み取る必要がある状況を回避し、同じデータが同時に複数回読み取られる可能性を回避します。

    この機能は v6.2.0 では実験的であり、v6.3.0 で GA になります。

-   TiFlashはデータ複製のパフォーマンスを向上します[＃5237](https://github.com/pingcap/tiflash/issues/5237) @ [そよ風のような](https://github.com/breezewish)

    TiFlash は、 TiKV からのデータ レプリケーションにRaftプロトコルを使用します。v6.3.0 より前では、大量のレプリカ データをレプリケーションするのに長い時間がかかることがよくありました。TiDB v6.3.0 は、 TiFlashデータ レプリケーション メカニズムを最適化し、レプリケーション速度を大幅に向上させます。BRを使用してデータを回復したり、 TiDB Lightning を使用してデータをインポートしたり、新しいTiFlashレプリカを追加したりすると、 TiFlashレプリカをより迅速にレプリケーションできます。TiFlash でよりタイムリーにクエリを実行できます。さらに、 TiFlashレプリカのスケールアップ、スケールダウン、または数の変更を行った場合、 TiFlashレプリカはより速く安全でバランスの取れた状態に到達します。

-   TiFlashは、個々の`COUNT(DISTINCT)` [＃37202](https://github.com/pingcap/tidb/issues/37202) @ [修正DB](https://github.com/fixdb)の3段階の集約をサポートします。

    TiFlash は、 `COUNT(DISTINCT)`を 1 つだけ含むクエリを[3段階集約](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)に書き換えることをサポートしています。これにより、同時実行性とパフォーマンスが向上します。

-   TiKVはログリサイクル[＃214](https://github.com/tikv/raft-engine/issues/214) @ [リクササシネーター](https://github.com/LykxSassinator)をサポートします

    TiKV はRaft Engineで[ログファイルのリサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)サポートします。これにより、 Raftログ追加時のネットワーク ディスクのロングテールレイテンシーが短縮され、書き込みワークロードでのパフォーマンスが向上します。

-   TiDBはnull認識アンチ結合[＃37525](https://github.com/pingcap/tidb/issues/37525) @ [アレナトルクス](https://github.com/Arenatlx)をサポート

    TiDB v6.3.0 では、新しい結合タイプ[Null 認識アンチ結合 (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)が導入されました。NAAJ は、コレクション操作を処理するときに、コレクションが空であるか`NULL`あるかを認識できます。これにより、 `IN`や`= ANY`などの操作の実行効率が最適化され、SQL パフォーマンスが向上します。

-   ハッシュ結合[＃35439](https://github.com/pingcap/tidb/issues/35439) @ [思い出させる](https://github.com/Reminiscent)のビルド終了を制御するためのオプティマイザヒントを追加します。

    v6.3.0 では、TiDB オプティマイザーは、ハッシュ結合、そのプローブ終了、およびそのビルド終了を指定するためのヒント`HASH_JOIN_BUILD()`と`HASH_JOIN_PROBE()` 2 つを導入します。オプティマイザーが最適な実行プランを選択できない場合は、これらのヒントを使用してプランに介入できます。

-   セッションレベルの共通テーブル式 (CTE) インライン[＃36514](https://github.com/pingcap/tidb/issues/36514) @ [エルサ0520](https://github.com/elsa0520)をサポート

    TiDB v6.2.0 では、オプティマイザーに`MERGE`ヒントが導入され、CTE インラインが可能になり、CTE クエリ結果のコンシューマーがTiFlashで並列実行できるようになりました。v6.3.0 では、セッション変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)が導入され、セッションで CTE インラインが可能になりました。これにより、使いやすさが大幅に向上します。

### 取引 {#transactions}

-   悲観的トランザクションにおける一意制約のチェックの延期をサポート[＃36579](https://github.com/pingcap/tidb/issues/36579) @ [エキシウム](https://github.com/ekexium)

    [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)システム変数を使用して、TiDB が悲観的トランザクションで[一意制約](/constraints.md#pessimistic-transactions)チェックするタイミングを制御できます。この変数はデフォルトでは無効になっています。変数を有効にすると ( `ON`に設定)、TiDB は悲観的トランザクションでのロック操作と一意制約チェックを必要になるまで延期し、一括 DML 操作のパフォーマンスを向上させます。

-   Read-Committed分離レベル[＃36812](https://github.com/pingcap/tidb/issues/36812) @ [トンスネークリン](https://github.com/TonsnakeLin)でTSOを取得する方法を最適化する

    Read-Committed 分離レベルでは、TSO のフェッチ方法を制御するためにシステム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)が導入されています。プラン キャッシュ ヒットの場合、TiDB は TSO のフェッチ頻度を減らすことでバッチ DML ステートメントの実行効率を向上させ、バッチで実行中のタスクの実行時間を短縮します。

### 安定性 {#stability}

-   リソースを消費するクエリが軽量クエリの応答時間に与える影響を軽減する[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

    リソースを消費するクエリと軽量クエリが同時に実行されると、軽量クエリの応答時間に影響します。この場合、トランザクション サービスの品質を確保するために、軽量クエリは最初に TiDB によって処理されることが期待されます。v6.3.0 では、TiKV は読み取り要求のスケジュール メカニズムを最適化し、各ラウンドのリソースを消費するクエリの実行時間が期待どおりになるようにします。これにより、リソースを消費するクエリが軽量クエリの応答時間に与える影響が大幅に軽減され、混合ワークロード シナリオで P99レイテンシーが 50% 以上削減されます。

-   統計が古くなったときに統計をロードするデフォルトのポリシーを変更する[＃27601](https://github.com/pingcap/tidb/issues/27601) @ [翻訳者](https://github.com/xuyifangreeneyes)

    v5.3.0 では、TiDB は、統計が古くなった場合にオプティマイザがどのように動作するかを制御するシステム変数[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)を導入しました。デフォルト値は`ON`で、これは旧バージョンの動作を維持することを意味します。SQL ステートメントに関係するオブジェクトの統計が古くなった場合、オプティマイザは統計 (テーブルの合計行数以外) が信頼できないと見なし、代わりに疑似統計を使用します。実際のユーザー シナリオのテストと分析の結果、v6.3.0 以降ではデフォルト値`tidb_enable_pseudo_for_outdated_stats`が`OFF`に変更されました。統計が古くなっても、オプティマイザは引き続きテーブルの統計を使用するため、実行プランがより安定します。

-   タイタンを無効にするとGA @ [タボキ](https://github.com/tabokie)になる

    オンライン TiKV ノードは[タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan)することができます。

-   GlobalStatsが準備できていない場合は`static`パーティションプルーニングを使用する[＃37535](https://github.com/pingcap/tidb/issues/37535) @ [イサール](https://github.com/Yisaer)

    [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode)が有効になっている場合、オプティマイザは[グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)に基づいて実行プランを選択します。GlobalStats が完全に収集される前に疑似統計を使用すると、パフォーマンスが低下する可能性があります。v6.3.0 では、GlobalStats が収集される前に動的プルーニングを有効にすると、 `static`モードを維持することでこの問題に対処します。TiDB は GlobalStats が収集されるまで`static`モードのままです。これにより、パーティション プルーニング設定を変更してもパフォーマンスの安定性が確保されます。

### 使いやすさ {#ease-of-use}

-   SQLベースのデータ配置ルールとTiFlashレプリカ[＃37171](https://github.com/pingcap/tidb/issues/37171) @ [lcwangchao](https://github.com/lcwangchao)間の競合に対処する

    TiDB v6.0.0 は[SQLベースのデータ配置ルール](/placement-rules-in-sql.md)提供します。ただし、この機能は実装上の問題によりTiFlashレプリカと競合します。TiDB v6.3.0 は実装メカニズムを最適化し、SQL ベースのデータ配置ルールとTiFlash間の競合を解決します。

### MySQL 互換性 {#mysql-compatibility}

-   `REGEXP_SUBSTR()`つの正規表現関数のサポートを追加することで、MySQL 8.0との互換性が向上し[＃23881](https://github.com/pingcap/tidb/issues/23881)た: `REGEXP_INSTR()` `REGEXP_REPLACE()` `REGEXP_LIKE()` [風の話し手](https://github.com/windtalker)

    MySQLとの互換性の詳細については、 [MySQL との正規表現の互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)参照してください。

-   `CREATE USER`と`ALTER USER`文は`ACCOUNT LOCK/UNLOCK`オプション[＃37051](https://github.com/pingcap/tidb/issues/37051) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポートします

    [`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを使用してユーザーを作成する場合、 `ACCOUNT LOCK/UNLOCK`オプションを使用して、作成されたユーザーをロックするかどうかを指定できます。ロックされたユーザーはデータベースにログインできません。

    [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントの`ACCOUNT LOCK/UNLOCK`オプションを使用して、既存のユーザーのロック状態を変更できます。

-   JSON データ型と JSON関数がGA [＃36993](https://github.com/pingcap/tidb/issues/36993) @ [雄吉偉](https://github.com/xiongjiwei)になる

    JSON は、多数のプログラムで採用されている一般的なデータ形式です。TiDB は以前のバージョンから[JSONサポート](/data-type-json.md)実験的機能として導入しており、MySQL の JSON データ型および一部の JSON関数と互換性があります。

    TiDB v6.3.0 では、JSON データ型と関数がGA となり、TiDB のデータ型が充実し、 [表現インデックス](/sql-statements/sql-statement-create-index.md#expression-index)と[生成された列](/generated-columns.md)での JSON関数の使用がサポートされ、TiDB と MySQL の互換性がさらに向上しました。

### バックアップと復元 {#backup-and-restore}

-   PITRは[ジョッカウ](https://github.com/joccau)のバックアップストレージとして[GCS と Azure Blob ストレージ](/br/backup-and-restore-storages.md)サポートします

    TiDB クラスターが Google Cloud または Azure にデプロイされている場合は、クラスターを v6.3.0 にアップグレードした後、PITR 機能を使用できます。

-   BRはAWS S3オブジェクトロック[＃13442](https://github.com/tikv/tikv/issues/13442) @ [3ポインター](https://github.com/3pointer)をサポートします

    [S3 オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)有効にすることで、AWS 上のバックアップデータが改ざんされたり削除されたりするのを防ぐことができます。

### データ移行 {#data-migration}

-   TiDB Lightningは[Apache Hive によってエクスポートされた Parquet ファイルを TiDB にインポートする](/tidb-lightning/tidb-lightning-data-source.md#parquet) [＃37536](https://github.com/pingcap/tidb/issues/37536) @ [ブチュイトウデゴウ](https://github.com/buchuitoudegou)をサポートします

-   DMは新しい構成項目`safe-mode-duration` [＃6224](https://github.com/pingcap/tiflow/issues/6224) @ [ok江](https://github.com/okJiang)を追加します

    この設定項目は[タスク設定ファイル](/dm/task-configuration-file-full.md)に追加されます。DM が異常終了した後の自動セーフ モードの継続時間を調整できます。デフォルト値は 60 秒です。 `safe-mode-duration` `"0s"`に設定すると、DM が異常な再起動後にセーフ モードに入ろうとするとエラーが報告されます。

### TiDBデータ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDCは、複数の地理的に分散したデータソースからデータを複製できる展開トポロジをサポートしています[＃5301](https://github.com/pingcap/tiflow/issues/5301) @ [スドジ](https://github.com/sdojjy)

    単一の TiDB クラスターから複数の地理的に分散されたデータ システムへのデータのレプリケーションをサポートするために、v6.3.0 以降では、各 IDC のデータを[TiCDCを複数のIDCに導入できる](/ticdc/deploy-ticdc.md)ずつレプリケーションします。この機能は、地理的に分散されたデータのレプリケーションとデプロイメント トポロジの機能を提供するのに役立ちます。

-   TiCDCは、上流と下流（同期ポイント）間のスナップショットの一貫性を維持することをサポートします[＃6977](https://github.com/pingcap/tiflow/issues/6977) @ [アズドンメン](https://github.com/asddongmen)

    災害復旧のためのデータ レプリケーションのシナリオでは、TiCDC は[定期的に下流データのスナップショットを維持する](/ticdc/ticdc-upstream-downstream-check.md)サポートしているため、ダウンストリーム スナップショットがアップストリーム スナップショットと一貫性を保ちます。この機能により、TiCDC は読み取りと書き込みが分離されているシナリオをより適切にサポートし、コストを削減できます。

-   TiCDC は[＃4757](https://github.com/pingcap/tiflow/issues/4757) @ [金星の上](https://github.com/overvenus) @ [3エースショーハンド](https://github.com/3AceShowHand)の正常なアップグレードをサポートします

    TiCDC が[TiUP](/ticdc/deploy-ticdc.md#upgrade-cautions) (&gt;=v1.11.0) または[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (&gt;=v1.3.8) を使用して展開されている場合、TiCDC クラスターを正常にアップグレードできます。アップグレード中、データ レプリケーションのレイテンシーは30 秒まで短く抑えられます。これにより安定性が向上し、TiCDC は待ち時間の影響を受けやすいアプリケーションをより適切にサポートできるようになります。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                         | タイプを変更   | 説明                                                                                                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                       | 修正済み     | 新しいオプション`tidb_sm3_password`を追加します。この変数を`tidb_sm3_password`に設定すると、暗号化アルゴリズムとして SM3 が使用されます。                                                                                                                                                    |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630)                                       | 新しく追加された | テーブルに主キーが必要であるという要件を強制するかどうかを制御します。この変数を有効にすると、主キーのないテーブルを作成または変更しようとするとエラーが発生します。                                                                                                                                                            |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)             | 新しく追加された | [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)から`closest-adaptive`に設定されている場合、TiDBサーバーがTiDBサーバーと同じリージョン内のレプリカに読み取り要求を送信することを優先するしきい値を制御します。                                                                          |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | 新しく追加された | 悲観的トランザクションで TiDB が[一意制約](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御します。                                                                                                                                                        |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)                                               | 新しく追加された | [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が有効な場合にのみ有効になります。インデックス作成時のバックフィル中のローカルstorageの使用制限を設定します。                                                                                         |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                 | 新しく追加された | インデックス作成時のバックフィルの速度を向上させるために、 `ADD INDEX`および`CREATE INDEX` DDL 操作の高速化を有効にするかどうかを制御します。                                                                                                                                                        |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                         | 新しく追加された | `flashback cluster`の同時実行性を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                  |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition)                                     | 非推奨      | [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトでは`exchange partitions with tables`有効になっています。                                                                        |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                       | 新しく追加された | `FOREIGN KEY`機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                  |
| `tidb_enable_general_plan_cache`                                                                                            | 新しく追加された | 一般プラン キャッシュ機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                    |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                   | 新しく追加された | [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを指定します。                                                                                                                                                                                              |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                     | 新しく追加された | 特殊なセット演算子`NOT IN`と`!= ALL`によって導かれるサブクエリによって Anti Join が生成される場合に、TiDB が Null 対応ハッシュ結合を適用するかどうかを制御します。                                                                                                                                          |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)           | 修正済み     | 統計が古くなった場合に、テーブルの統計を使用する際のオプティマイザの動作を制御します。デフォルト値は`ON`から`OFF`に変更されます。これは、このテーブルの統計が古くなっても、オプティマイザがテーブルの統計を使用し続けることを意味します。                                                                                                                     |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)                                       | 修正済み     | データを読み取る演算子の動的メモリ制御機能を有効にするかどうかを制御します。この変数を`ON`に設定すると、メモリ使用量が[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制御下になくなる可能性があります。そのため、デフォルト値は`ON`から`OFF`に変更されます。                                                             |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 新しく追加された | SQL 書き込みステートメントの読み取り要求がTiFlashにプッシュダウンされるかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                              |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 式を生成された列に安全でない方法で置き換えるかどうかを制御します。                                                                                                                                                                                                             |
| `tidb_general_plan_cache_size`                                                                                              | 新しく追加された | 一般プラン キャッシュによってキャッシュできる実行プランの最大数を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                           |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行の結果を取得するために使用されます。                                                                                                                                                                                 |
| [tidb_max_paging_size](/system-variables.md#tidb_max_paging_size-new-in-v630)                                               | 新しく追加された | この変数は、コプロセッサ ページング要求プロセス中の最小行数を設定するために使用されます。                                                                                                                                                                                                 |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)                                   | 新しく追加された | セッション全体の共通テーブル式 (CTE) がインライン化されるかどうかを制御します。デフォルト値は`OFF`で、これは CTE のインライン化がデフォルトでは強制されないことを意味します。                                                                                                                                               |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)                   | 新しく追加された | MPP モードで`COUNT(DISTINCT)`集約を 3 段階の集約に書き換えるかどうかを指定します。デフォルト値は`ON`です。                                                                                                                                                                           |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)                                    | 修正済み     | 動的プルーニングを有効にするかどうかを指定します。v6.3.0 以降、デフォルト値は`dynamic`に変更されます。                                                                                                                                                                                   |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                           | 修正済み     | タイムスタンプ取得を最適化するために使用されます。これは、読み取り/書き込み競合がほとんど発生しない、読み取りコミット分離レベルのシナリオに適しています。この機能は特定のサービス ワークロード向けであり、他のシナリオではパフォーマンスの低下を引き起こす可能性があります。このため、v6.3.0 以降、この変数のスコープは`GLOBAL \| SESSION`から`INSTANCE`に変更されています。つまり、特定の TiDB インスタンスに対してこの機能を有効にできます。 |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)                                         | 新しく追加された | タイムスタンプの取得を最適化するために使用され、悲観的トランザクションのRC分離レベルでポイント書き込みの競合が少ないシナリオに適しています。この変数を有効にすると、ポイント書き込みステートメントの実行中にグローバルタイムスタンプを取得することによって生じるレイテンシーとオーバーヘッドを回避できます。                                                                                       |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)                                                     | 新しく追加された | FastScan を有効にするかどうかを制御します。1 が有効 ( [高速スキャン](/tiflash/use-fastscan.md)に設定) の場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の正確性やデータの一貫性は`ON`されません。                                                                                                  |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                            | タイプを変更   | 説明                                                                                                                                                                                                                      |
| -------------- | ----------------------------------------------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ティビ            | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)                                        | 新しく追加された | TiDB が一時データを保存するために使用するファイル システムの場所を指定します。機能が TiDB ノードにローカルstorageを必要とする場合、TiDB は対応する一時データをこの場所に保存します。デフォルト値は`/tmp/tidb`です。                                                                                             |
| ティクヴ           | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)              | 新しく追加された | スレッド プールのサイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プールのサイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。                                                                                               |
| ティクヴ           | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method)                        | 修正済み     | 新しい値オプション`sm4-ctr`が導入されました。この構成項目が`sm4-ctr`に設定されている場合、データは保存される前に SM4 を使用して暗号化されます。                                                                                                                                     |
| ティクヴ           | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                    | 新しく追加された | Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。有効にすると、論理的に消去されたログ ファイルはリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが削減されます。この構成項目は、 [フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。 |
| ティクヴ           | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                            | 新しく追加された | Raft Engineのログ ファイルのバージョンを指定します。TiKV v6.3.0 より前のバージョンの場合、デフォルトのログ ファイルのバージョンは`1`です。ログ ファイルは TiKV &gt;= v6.1.0 で読み取ることができます。TiKV v6.3.0 以降の場合、デフォルトのログ ファイルのバージョンは`2`です。TiKV v6.3.0 以降では、ログ ファイルを読み取ることができます。            |
| ティクヴ           | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620)                                 | 修正済み     | v6.3.0 以降、デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                |
| ティクヴ           | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620)         | 修正済み     | v6.3.0 以降、デフォルト値は`5min`から`3min`に変更されます。                                                                                                                                                                                 |
| PD             | [診断を有効にする](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                   | 新しく追加された | 診断機能を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                  |
| TiFlash        | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)   | 非推奨      | v6.3.0 以降、この構成項目は非推奨です。スレッド プールは、デフォルトでstorageエンジンからの読み取り要求を処理するために使用され、無効にすることはできません。                                                                                                                                  |
| DM             | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | 自動セーフ モードの期間を指定します。                                                                                                                                                                                                     |
| ティCDC          | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | 同期ポイント機能を有効にするかどうかを指定します。                                                                                                                                                                                               |
| ティCDC          | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)        | 新しく追加された | Syncpoint が上流スナップショットと下流スナップショットを揃える間隔を指定します。                                                                                                                                                                           |
| ティCDC          | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新しく追加された | ダウンストリーム テーブルで同期ポイントによってデータが保持される期間を指定します。この期間を超えると、データはクリーンアップされます。                                                                                                                                                    |
| ティCDC          | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters)                      | 非推奨      | `memory`ソートは非推奨です。いかなる状況でも使用することはお勧めしません。                                                                                                                                                                               |

### その他 {#others}

-   ログ バックアップは、バックアップstorageとして GCS と Azure Blob Storage をサポートします。
-   ログ バックアップは`exchange partition` DDL と互換性を持つようになりました。
-   [高速スキャン](/tiflash/use-fastscan.md)有効にするために以前使用されていた SQL 文`ALTER TABLE ...SET TiFLASH MODE ...`は非推奨となり、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)に置き換えられました。v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定が無効になりますが、データの通常の読み取りには影響しません。この場合、変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を構成して FastScan を有効または無効にする必要があります。以前のバージョンから v6.3.0 にアップグレードすると、データの一貫性を保つために、すべてのセッションで FastScan 機能がデフォルトで有効になりません。
-   Linux AMD64アーキテクチャでTiFlash を展開するには、CPU が AVX2 命令セットをサポートしている必要があります。1 `cat /proc/cpuinfo | grep avx2`出力されていることを確認してください。Linux ARM64アーキテクチャでTiFlashを展開するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。3 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`出力されていることを確認してください。命令セット拡張を使用することで、TiFlash のベクトル化エンジンはより優れたパフォーマンスを発揮できます。
-   TiDB で動作する HAProxy の最小バージョンは現在 v1.5 です。v1.5 から v2.1 までの HAProxy バージョンでは、 `mysql-check`に`post-41`構成オプションを設定する必要があります。HAProxy v2.2 以降を使用することをお勧めします。

## 削除された機能 {#removed-feature}

v6.3.0 以降、TiCDC は Pulsar シンクの構成をサポートしなくなりました。StreamNative が提供する[コップ](https://github.com/streamnative/kop)代替として使用できます。

## 改善点 {#improvements}

-   ティビ

    -   TiDB は、テーブルの存在を確認する際に、ターゲット テーブル名の大文字と小文字を区別しなくなりました[＃34610](https://github.com/pingcap/tidb/issues/34610) @ [天菜まお](https://github.com/tiancaiamao)
    -   `init_connect` [＃35324](https://github.com/pingcap/tidb/issues/35324) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の値を設定するときに解析チェックを追加することで、MySQL の互換性が向上しました。
    -   新しい接続[＃34964](https://github.com/pingcap/tidb/issues/34964) @ [雄吉偉](https://github.com/xiongjiwei)に対して生成されるログ警告を改善
    -   DDL履歴ジョブのクエリ用にHTTP APIを最適化し、 `start_job_id`パラメータ[＃35838](https://github.com/pingcap/tidb/issues/35838) @ [天菜まお](https://github.com/tiancaiamao)のサポートを追加します。
    -   JSON パスの構文が間違っている場合にエラーを報告する[＃22525](https://github.com/pingcap/tidb/issues/22525) [＃34959](https://github.com/pingcap/tidb/issues/34959) @ [雄吉偉](https://github.com/xiongjiwei)
    -   偽共有の問題を修正して結合操作のパフォーマンスを向上[＃37641](https://github.com/pingcap/tidb/issues/37641) @ [ゲンリキ](https://github.com/gengliqi)
    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)を使用して複数の SQL ステートメントの実行プラン情報を一度にエクスポートする機能をサポートし、トラブルシューティングの効率が向上します[＃37798](https://github.com/pingcap/tidb/issues/37798) @ [イサール](https://github.com/Yisaer)

-   ティクヴ

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストするのを回避するための`unreachable_backoff`項目の構成をサポートします[＃13054](https://github.com/tikv/tikv/issues/13054) @ [5kbpsの](https://github.com/5kbpers)
    -   TSOサービス[＃12794](https://github.com/tikv/tikv/issues/12794) @ [ピンギュ](https://github.com/pingyu)のフォールトトレランスを向上
    -   RocksDBで同時に実行されるサブコンパクション操作の数を動的に変更する機能をサポート ( `rocksdb.max-sub-compactions` ) [＃13145](https://github.com/tikv/tikv/issues/13145) @ [イーサフロー](https://github.com/ethercflow)
    -   空のリージョン[＃12421](https://github.com/tikv/tikv/issues/12421) @ [タボキ](https://github.com/tabokie)の結合のパフォーマンスを最適化します
    -   より多くの正規表現関数をサポート[＃13483](https://github.com/tikv/tikv/issues/13483) @ [ゲンリキ](https://github.com/gengliqi)
    -   CPU 使用率に基づいてスレッドプールのサイズを自動的に調整する機能をサポート[＃13313](https://github.com/tikv/tikv/issues/13313) @ [栄光](https://github.com/glorv)

-   PD

    -   TiDBダッシュボード[＃5366](https://github.com/tikv/pd/issues/5366) @ [宜尼Xu9506](https://github.com/YiniXu9506)のTiKV IO MBpsメトリックのクエリを改善
    -   TiDBダッシュボードのURLを`metrics`から`monitoring` [＃5366](https://github.com/tikv/pd/issues/5366) @ [宜尼Xu9506](https://github.com/YiniXu9506)に変更します

-   TiFlash

    -   `elt`機能をTiFlash [＃5104](https://github.com/pingcap/tiflash/issues/5104) @ [無限の意志](https://github.com/Willendless)に押し下げるサポート
    -   `leftShift`機能をTiFlash [＃5099](https://github.com/pingcap/tiflash/issues/5099) @ [星のアニー](https://github.com/AnnieoftheStars)に押し下げるサポート
    -   `castTimeAsDuration`機能をTiFlash [＃5306](https://github.com/pingcap/tiflash/issues/5306) @ [アンチトップクォーク](https://github.com/AntiTopQuark)に押し下げるサポート
    -   `HexIntArg/HexStrArg`機能をTiFlash [＃5107](https://github.com/pingcap/tiflash/issues/5107) @ [ヤンケオ](https://github.com/YangKeao)に押し下げるサポート
    -   TiFlash のインタープリタをリファクタリングし、新しいインタープリタ Planner [＃4739](https://github.com/pingcap/tiflash/issues/4739) @ [シーライズ](https://github.com/SeaRise)をサポートします
    -   TiFlash [＃5609](https://github.com/pingcap/tiflash/issues/5609) @ [ベストウッディ](https://github.com/bestwoody)のメモリトラッカーの精度を向上
    -   `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN`照合[＃5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツ](https://github.com/solotzg)で文字列列のパフォーマンスを向上
    -   ReadLimiter [＃5401](https://github.com/pingcap/tiflash/issues/5401) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でバックグラウンドでの I/O スループットを計算します[＃5091](https://github.com/pingcap/tiflash/issues/5091)

-   ツール

    -   バックアップと復元 (BR)

        -   PITRはログバックアップで生成された小さなファイルをマージできるため、バックアップファイルの数を大幅に削減できます[＃13232](https://github.com/tikv/tikv/issues/13232) @ [リーヴルス](https://github.com/Leavrth)
        -   PITRは、復元後の上流クラスタ構成に基づいてTiFlashレプリカの数を自動的に構成することをサポートします[＃37208](https://github.com/pingcap/tidb/issues/37208) @ [ユジュンセン](https://github.com/YuJuncen)

    -   ティCDC

        -   TiCDC とアップストリーム TiDB [＃6506](https://github.com/pingcap/tiflow/issues/6506) @ [ランス6716](https://github.com/lance6716)で導入された並行 DDL フレームワークとの互換性を向上
        -   MySQLシンクがエラー[＃6460](https://github.com/pingcap/tiflow/issues/6460) @ [金星の上](https://github.com/overvenus)を取得したときにDMLステートメントの`start ts`のログ記録をサポート
        -   `api/v1/health` API を強化して、TiCDC クラスター[＃4757](https://github.com/pingcap/tiflow/issues/4757) @ [金星の上](https://github.com/overvenus)のより正確なヘルス状態を返すようにしました
        -   シンクのスループットを向上させるために、非同期モードでMQシンクとMySQLシンクを実装する[＃5928](https://github.com/pingcap/tiflow/issues/5928) @ [ヒック](https://github.com/hicqu) @ [ハイラスティン](https://github.com/Rustin170506)
        -   廃止予定のパルサーシンク[＃7087](https://github.com/pingcap/tiflow/issues/7087) @ [ハイラスティン](https://github.com/Rustin170506)を削除します
        -   変更フィードに関係のない DDL ステートメントを破棄することでレプリケーションのパフォーマンスを向上します[＃6447](https://github.com/pingcap/tiflow/issues/6447) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   データソース[＃6448](https://github.com/pingcap/tiflow/issues/6448) @ [ランス6716](https://github.com/lance6716)として MySQL 8.0 との互換性を向上
        -   「無効な接続」に遭遇したときに DDL を非同期的に実行して DDL を最適化する[＃4689](https://github.com/pingcap/tiflow/issues/4689) @ [翻訳者](https://github.com/lyzx2001)

    -   TiDB Lightning

        -   特定のロール[＃36891](https://github.com/pingcap/tidb/issues/36891) @ [ダシュン](https://github.com/dsdashun)を引き受けて別のアカウントの S3 データにアクセスできるように、S3 外部storageURL のクエリ パラメータを追加します。

## バグ修正 {#bug-fixes}

-   ティビ

    -   `PREPARE`ステートメント[＃35784](https://github.com/pingcap/tidb/issues/35784) @ [lcwangchao](https://github.com/lcwangchao)で権限チェックがスキップされる問題を修正
    -   システム変数`tidb_enable_noop_variable` `WARN` [＃36647](https://github.com/pingcap/tidb/issues/36647) @ [lcwangchao](https://github.com/lcwangchao)に設定できる問題を修正
    -   式インデックスが定義されている場合、 `INFORMATION_SCHEMA.COLUMNS`テーブルの`ORDINAL_POSITION`列が正しくなくなる可能性がある問題を修正しました[#31200](https://github.com/pingcap/tidb/issues/31200) @ [bb7133](https://github.com/bb7133)
    -   タイムスタンプが`MAXINT32` [＃31585](https://github.com/pingcap/tidb/issues/31585) @ [bb7133](https://github.com/bb7133)より大きい場合に TiDB がエラーを報告しない問題を修正しました
    -   エンタープライズプラグイン使用時にTiDBサーバーを起動できない問題を修正[＃37319](https://github.com/pingcap/tidb/issues/37319) @ [xhebox](https://github.com/xhebox)
    -   `SHOW CREATE PLACEMENT POLICY` [＃37526](https://github.com/pingcap/tidb/issues/37526) @ [xhebox](https://github.com/xhebox)の誤った出力を修正
    -   一時テーブル[＃37201](https://github.com/pingcap/tidb/issues/37201) @ [lcwangchao](https://github.com/lcwangchao)の予期しない動作`EXCHANGE PARTITION`を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`クエリすると[ジムララ](https://github.com/zimulala)で誤った結果が返される問題を修正
    -   ビューに対する`EXPLAIN`クエリが権限[＃34326](https://github.com/pingcap/tidb/issues/34326) @ [ホーキングレイ](https://github.com/hawkingrei)をチェックしない問題を修正
    -   JSON `null` `NULL` [＃37852](https://github.com/pingcap/tidb/issues/37852) @ [ヤンケオ](https://github.com/YangKeao)に更新できない問題を修正
    -   DDLジョブの`row_count`が不正確であるという問題を修正[＃25968](https://github.com/pingcap/tidb/issues/25968) @ [定義2014](https://github.com/Defined2014)
    -   `FLASHBACK TABLE`正しく動作しない問題を修正[＃37386](https://github.com/pingcap/tidb/issues/37386) @ [天菜まお](https://github.com/tiancaiamao)
    -   典型的なMySQLプロトコル[＃36731](https://github.com/pingcap/tidb/issues/36731) @ [ドヴェーデン](https://github.com/dveeden)で`prepared`ステートメントフラグを処理できない問題を修正
    -   極端なケースで起動時に誤った TiDB ステータスが表示される問題を修正[＃36791](https://github.com/pingcap/tidb/issues/36791) @ [xhebox](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.VARIABLES_INFO`セキュリティ強化モード (SEM) [＃37586](https://github.com/pingcap/tidb/issues/37586) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)に準拠していない問題を修正
    -   `UNION` [＃31678](https://github.com/pingcap/tidb/issues/31678) @ [cbcwestwolf](https://github.com/cbcwestwolf)のクエリで文字列を文字列にキャストするとエラーが発生する問題を修正しました
    -   TiFlash [＃37254](https://github.com/pingcap/tidb/issues/37254) @ [うわー](https://github.com/wshwsh12)のパーティション テーブルで動的モードを有効にしたときに発生する誤った結果を修正しました。
    -   TiDB のバイナリ文字列と JSON 間のキャストおよび比較が MySQL [＃31918](https://github.com/pingcap/tidb/issues/31918) [＃25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケオ](https://github.com/YangKeao)と互換性がない問題を修正
    -   TiDB の`JSON_OBJECTAGG`と`JSON_ARRAYAGG`バイナリ値[＃25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケオ](https://github.com/YangKeao)で MySQL と互換性がない問題を修正しました。
    -   JSON の不透明値の比較でpanicが発生する問題を修正[＃37315](https://github.com/pingcap/tidb/issues/37315) @ [ヤンケオ](https://github.com/YangKeao)
    -   JSON集計関数[＃37287](https://github.com/pingcap/tidb/issues/37287) @ [ヤンケオ](https://github.com/YangKeao)で単精度浮動小数点が使用できない問題を修正
    -   `UNION`演算子が予期しない空の結果[＃36903](https://github.com/pingcap/tidb/issues/36903) @ [天菜まお](https://github.com/tiancaiamao)を返す可能性がある問題を修正しました
    -   `castRealAsTime`式の結果が MySQL [＃37462](https://github.com/pingcap/tidb/issues/37462) @ [メンシン9014](https://github.com/mengxin9014)と一致しない問題を修正
    -   悲観的DML操作が非一意のインデックスキー[＃36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)をロックする問題を修正
    -   `auto-commit`変更がトランザクションのコミット動作[＃36581](https://github.com/pingcap/tidb/issues/36581) @ [翻訳](https://github.com/cfzjywxk)に影響する問題を修正
    -   DMLエグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正しました[＃37373](https://github.com/pingcap/tidb/issues/37373) @ [翻訳](https://github.com/cfzjywxk)
    -   UPDATE ステートメントが場合によっては投影を誤って削除し、 `Can't find column`エラー[＃37568](https://github.com/pingcap/tidb/issues/37568) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正しました。
    -   結合したテーブルの再配置操作が誤って外部結合条件[＃37238](https://github.com/pingcap/tidb/issues/37238) @ [アイリンキッド](https://github.com/AilinKid)をプッシュダウンする問題を修正しました。
    -   一部のパターンの`IN`および`NOT IN`サブクエリが`Can't find column`エラー[＃37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid)を報告する問題を修正しました
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [＃35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれている場合に`Can't find column`が報告される問題を修正しました
    -   間違った`PromQL` [＃35856](https://github.com/pingcap/tidb/issues/35856) @ [定義2014](https://github.com/Defined2014)を修正

-   ティクヴ

    -   リージョンハートビートが中断された後にPDがTiKVに再接続しない問題を修正[＃12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)
    -   Raftstoreがビジー状態の場合にリージョンが重複する可能性がある問題を修正[＃13160](https://github.com/tikv/tikv/issues/13160) @ [5kbpsの](https://github.com/5kbpers)
    -   PDクライアントがデッドロックを引き起こす可能性がある問題を修正[＃13191](https://github.com/tikv/tikv/issues/13191) @ [バッファフライ](https://github.com/bufferflies) [＃12933](https://github.com/tikv/tikv/issues/12933) @ [バートンチン](https://github.com/BurtonQin)
    -   暗号化が無効になっている場合に TiKV がpanicになる可能性がある問題を修正[＃13081](https://github.com/tikv/tikv/issues/13081) @ [嘉陽鄭](https://github.com/jiayang-zheng)
    -   ダッシュボード[＃13086](https://github.com/tikv/tikv/issues/13086) @ [栄光](https://github.com/glorv)の`Unified Read Pool CPU`の誤った表現を修正
    -   TiKVインスタンスが隔離されたネットワーク環境にある場合、TiKVサービスが数分間利用できなくなる問題を修正[＃12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)
    -   TiKVが誤って`PessimisticLockNotFound`エラー[＃13425](https://github.com/tikv/tikv/issues/13425) @ [スティクナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   PITR が状況によってはデータ損失を引き起こす可能性がある問題を修正[＃13281](https://github.com/tikv/tikv/issues/13281) @ [ユジュンセン](https://github.com/YuJuncen)
    -   長い悲観的トランザクション[＃13304](https://github.com/tikv/tikv/issues/13304) @ [ユジュンセン](https://github.com/YuJuncen)がある場合にチェックポイントが進まない問題を修正しました
    -   TiKV が日付時刻型 ( `DATETIME` 、 `DATE` 、 `TIMESTAMP` 、 `TIME` ) と JSON [＃13417](https://github.com/tikv/tikv/issues/13417) @ [ヤンケオ](https://github.com/YangKeao)の`STRING`型を区別しない問題を修正しました
    -   JSON bool と他の JSON 値の比較における MySQL との非互換性を修正[＃13386](https://github.com/tikv/tikv/issues/13386) [＃37481](https://github.com/pingcap/tidb/issues/37481) @ [ヤンケオ](https://github.com/YangKeao)

-   PD

    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって発生する PD パニックを修正[＃5373](https://github.com/tikv/pd/issues/5373) @ [バッファフライ](https://github.com/bufferflies)
    -   不健全なリージョンがPDpanic[＃5491](https://github.com/tikv/pd/issues/5491) @ [ノルーシュ](https://github.com/nolouch)を引き起こす可能性がある問題を修正
    -   TiFlash学習レプリカが作成されない可能性がある問題を修正[＃5401](https://github.com/tikv/pd/issues/5401) @ [ハンダンDM](https://github.com/HunDunDM)

-   TiFlash

    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[＃5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `CAST(value AS DATETIME)`の誤ったデータ入力によりTiFlash sys CPU [＃5097](https://github.com/pingcap/tiflash/issues/5097) @ [翻訳者](https://github.com/xzhangxian1008)の負荷が高くなる問題を修正
    -   `CAST(Real/Decimal AS time)`の結果が MySQL [＃3779](https://github.com/pingcap/tiflash/issues/3779) @ [メンシン9014](https://github.com/mengxin9014)と一致しない問題を修正
    -   storage内の一部の古いデータを削除できない問題を修正[＃5570](https://github.com/pingcap/tiflash/issues/5570) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)
    -   ページGCがテーブル[＃5697](https://github.com/pingcap/tiflash/issues/5697) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)の作成をブロックする可能性がある問題を修正
    -   `NULL`値[＃5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   チェックポイントの情報が古くなる可能性がある問題を修正[＃36423](https://github.com/pingcap/tidb/issues/36423) @ [ユジュンセン](https://github.com/YuJuncen)
        -   復元中に同時実行性が大きすぎるために領域のバランスが取れない問題を修正[＃37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   クラスター[＃37822](https://github.com/pingcap/tidb/issues/37822) @ [ユジュンセン](https://github.com/YuJuncen)に TiCDC が存在する場合にログ バックアップ チェックポイント TS がスタックする可能性がある問題を修正しました。
        -   外部storage[＃37469](https://github.com/pingcap/tidb/issues/37469) @ [モクイシュル28](https://github.com/MoCuishle28)認証キーに特殊文字が含まれている場合にバックアップと復元が失敗する可能性がある問題を修正

    -   ティCDC

        -   TiCDC が grpc サービス[＃6458](https://github.com/pingcap/tiflow/issues/6458) @ [クレラックス](https://github.com/crelax)で間違った PD アドレスに対して不正確なエラーを返す問題を修正しました
        -   `cdc cause cli changefeed list`コマンドが失敗した変更フィード[＃6334](https://github.com/pingcap/tiflow/issues/6334) @ [アズドンメン](https://github.com/asddongmen)を返さない問題を修正
        -   チェンジフィードの初期化に失敗した場合に TiCDC が使用できなくなる問題を修正[＃6859](https://github.com/pingcap/tiflow/issues/6859) @ [アズドンメン](https://github.com/asddongmen)

    -   TiDBBinlog

        -   コンプレッサーが gzip [＃1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合に、 Drainer がPumpにリクエストを正しく送信できない問題を修正しました。

    -   TiDB データ移行 (DM)

        -   DMが`Specified key was too long`エラー[＃5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   リレーがエラー[＃6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   `collation_compatible` `"strict"`に設定すると、DM が重複した照合順序[＃6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)を持つ SQL を生成する可能性がある問題を修正しました。
        -   DM-worker ログ[＃6628](https://github.com/pingcap/tiflow/issues/6628) @ [翻訳者](https://github.com/lyzx2001)の警告メッセージ「 binlog status_vars からタイムゾーンを取得するときにエラーが発生しました」の表示を減らします。
        -   レプリケーション[＃7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正しました

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル内のスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正[＃36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)

## 寄稿者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   @ [アンDJ](https://github.com/An-DJ)
-   @ [星のアニー](https://github.com/AnnieoftheStars)
-   @ [アンチトップクォーク](https://github.com/AntiTopQuark)
-   @ [えり](https://github.com/blacktear23)
-   @ [バートンチン](https://github.com/BurtonQin) (初めての投稿者)
-   @ [クレラックス](https://github.com/crelax)
-   @ [エルトシア](https://github.com/eltociear)
-   @ [ふじぇ1989](https://github.com/fuzhe1989)
-   @ [エルワドバ](https://github.com/erwadba)
-   @ [江津矢](https://github.com/jianzhiyao)
-   @ [ジョイセ06](https://github.com/joycse06)
-   @ [モルゴ](https://github.com/morgo)
-   @ [猫のみ](https://github.com/onlyacat)
-   @ [ピークジ](https://github.com/peakji)
-   @ [ルズリミアク](https://github.com/rzrymiak)
-   @ [ティソンクン](https://github.com/tisonkun)
-   @ [ホワイトキープワーク](https://github.com/whitekeepwork)
-   @ [ジイタン](https://github.com/Ziy1-Tan)

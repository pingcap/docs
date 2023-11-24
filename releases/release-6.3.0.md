---
title: TiDB 6.3.0 Release Notes
---

# TiDB 6.3.0 リリースノート {#tidb-6-3-0-release-notes}

発売日：2022年9月30日

TiDB バージョン: 6.3.0-DMR

> **注記：**
>
> TiDB 6.3.0-DMR のドキュメントは[アーカイブされた](https://docs-archive.pingcap.com/tidb/v6.3/)になりました。 PingCAP では、 [最新のLTSバージョン](https://docs.pingcap.com/tidb/stable)の TiDB データベースを使用することをお勧めします。

クイックアクセス: [クイックスタート](https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb) | [インストールパッケージ](https://www.pingcap.com/download/?version=v6.3.0#version-list)

v6.3.0-DMR の主な新機能と改善点は次のとおりです。

-   TiKV は、SM4 アルゴリズムを使用した保存時の暗号化をサポートしています。
-   TiDB は、SM3 アルゴリズムを使用した認証をサポートしています。
-   `CREATE USER`および`ALTER USER`ステートメントは`ACCOUNT LOCK/UNLOCK`オプションをサポートします。
-   JSON データ型と関数が一般提供 (GA) になりました。
-   TiDB はヌル認識アンチ結合をサポートしています。
-   TiDB は、より細かい粒度で実行時間メトリクスを提供します。
-   範囲パーティションの定義を簡素化するために、新しい糖衣構文が追加されました。
-   範囲 COLUMNS パーティショニングは、複数の列の定義をサポートします。
-   インデックス追加のパフォーマンスは 3 倍になります。
-   リソースを消費するクエリが軽量クエリの応答時間に及ぼす影響を 50% 以上削減します。

## 新機能 {#new-features}

### SQL {#sql}

-   レンジ パーティションの定義を簡素化するために、新しい糖衣構文 (レンジ インターバル パーティショニング) を追加しました (実験的) [#35683](https://github.com/pingcap/tidb/issues/35683) @ [むじょん](https://github.com/mjonss)

    TiDB は、レンジ パーティションを定義する新しい方法として[間隔パーティショニング](/partitioned-table.md#range-interval-partitioning)を提供します。すべてのパーティションを列挙する必要がないため、範囲パーティション化 DDL ステートメントの長さが大幅に短縮されます。構文は、元の Range パーティショニングの構文と同等です。

-   範囲 COLUMNS パーティショニングは、複数の列[#36636](https://github.com/pingcap/tidb/issues/36636) @ [むじょん](https://github.com/mjonss)の定義をサポートします。

    TiDB は[範囲列によるパーティション化 (column_list)](/partitioned-table.md#range-columns-partitioning)をサポートします。 `column_list`は単一列に限定されなくなりました。基本的な機能はMySQLと同じです。

-   [交換パーティション](/partitioned-table.md#partition-management) GA [#35996](https://github.com/pingcap/tidb/issues/35996) @ [ymkzpx](https://github.com/ymkzpx)になります

-   TiFlash [#5579](https://github.com/pingcap/tiflash/issues/5579) @ [シーライズ](https://github.com/SeaRise)へのさらに 2 つの[ウィンドウ関数](/tiflash/tiflash-supported-pushdown-calculations.md)のプッシュダウンをサポート

    -   `LEAD()`
    -   `LAG()`

-   軽量メタデータ ロックを提供して、DDL 変更時の DML 成功率を向上させます (実験的) [#37275](https://github.com/pingcap/tidb/issues/37275) @ [wjhuang2016](https://github.com/wjhuang2016)

    TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータ オブジェクトの変更をサポートします。トランザクションが実行されると、トランザクションの開始時に対応するメタデータのスナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。この問題を解決するために、TiDB v6.3.0 ではオンライン DDL アルゴリズムに[メタデータロック](/metadata-lock.md)が導入されています。可能な限り DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、古いメタデータを持つ DML がコミットされるまで DDL の実行を待機させます。

-   インデックス追加のパフォーマンスを向上させ、DML トランザクションへの影響を軽減します (実験的) [#35983](https://github.com/pingcap/tidb/issues/35983) @ [ベンジャミン2037](https://github.com/benjamin2037)

    インデックス作成時のバックフィルの速度を向上させるために、TiDB v6.3.0 では、 [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)システム変数が有効な場合に`ADD INDEX`および`CREATE INDEX` DDL 操作が高速化されます。この機能を有効にすると、インデックス追加のパフォーマンスが約 3 倍になります。

### Security {#security}

-   TiKV は、保存時の暗号化のための SM4 アルゴリズムをサポートしています[#13041](https://github.com/tikv/tikv/issues/13041) @ [嘉陽鄭](https://github.com/jiayang-zheng)

    保存時の TiKV 暗号化の場合は[SM4アルゴリズム](/encryption-at-rest.md)を追加します。保存時の暗号化を構成する場合、構成`data-encryption-method`の値を`sm4-ctr`に設定することで SM4 暗号化容量を有効にできます。

-   TiDB は SM3 アルゴリズム[#36192](https://github.com/pingcap/tidb/issues/36192) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)による認証をサポートします

    TiDB は、SM3 アルゴリズムに基づいた認証プラグイン[`tidb_sm3_password`](/security-compatibility-with-mysql.md)を追加します。このプラグインを有効にすると、ユーザー パスワードは SM3 アルゴリズムを使用して暗号化され、検証されます。

-   TiDB JDBC は、SM3 アルゴリズム[#25](https://github.com/pingcap/mysql-connector-j/issues/25) @ [最後切歯](https://github.com/lastincisor)による認証をサポートします。

    ユーザー パスワードの認証には、クライアント側のサポートが必要です。 [JDBC は SM3 アルゴリズムをサポートします](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)なので、TiDB-JDBC 経由で SM3 認証を使用して TiDB に接続できるようになりました。

### 可観測性 {#observability}

-   TiDB は、SQL クエリ実行時間[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)の詳細なメトリクスを提供します。

    TiDB v6.3.0 は、 [実行時間の詳細な観察](/latency-breakdown.md)の詳細なデータ メトリックを提供します。完全でセグメント化されたメトリクスを通じて、SQL クエリの主な消費時間を明確に把握でき、主要な問題を迅速に見つけてトラブルシューティングの時間を節約できます。

-   遅いログと`TRACE`ステートメントの出力を強化[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)

    TiDB v6.3.0 では、低速ログと`TRACE`の出力が強化されています。 TiDB の解析から KV RocksDB のディスクへの書き込みまでの[フルリンク期間](/latency-breakdown.md)の SQL クエリを観察でき、診断機能がさらに強化されます。

-   TiDB ダッシュボードはデッドロック履歴情報を提供します[#34106](https://github.com/pingcap/tidb/issues/34106) @ [cfzjywxk](https://github.com/cfzjywxk)

    v6.3.0 以降、TiDB ダッシュボードはデッドロック履歴を提供します。 TiDB ダッシュボードで遅いログを確認し、一部の SQL ステートメントのロック待機時間が過度に長いことがわかった場合は、デッドロック履歴を確認して根本原因を特定できるため、診断が容易になります。

### パフォーマンス {#performance}

-   TiFlash はFastScan の使用方法を変更します (実験的) [#5252](https://github.com/pingcap/tiflash/issues/5252) @ [ホンユニャン](https://github.com/hongyunyan)

    v6.2.0 では、 TiFlashに FastScan 機能が導入されており、期待されるパフォーマンスの向上が得られますが、使用上の柔軟性が欠けています。したがって、v6.3.0 では、 TiFlash はFastScan を有効または無効にする[FastScanの使用方法](/tiflash/use-fastscan.md) : `ALTER TABLE ... SET TIFLASH MODE ...`構文を変更し、非推奨になりました。代わりに、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して、FastScan を有効にするかどうかを簡単に制御できます。

    v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定は無効になりますが、データの通常の読み取りには影響しません。変数`tiflash_fastscan`を設定する必要があります。 v6.2.0 以前のバージョンから v6.3.0 にアップグレードする場合、データの整合性を維持するために、FastScan 機能はデフォルトではすべてのセッションで有効になりません。

-   TiFlash は、複数の同時実行タスク[#5376](https://github.com/pingcap/tiflash/issues/5376) @ [ジンヘリン](https://github.com/JinheLin)のシナリオでデータ スキャン パフォーマンスを最適化します。

    TiFlash は、同じデータの読み取り操作を組み合わせることで、同じデータの重複読み取りを削減します。リソースのオーバーヘッドと[同時タスクの場合のデータ スキャンのパフォーマンスが向上します。](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を最適化します。複数の同時タスクの場合、各タスクが同じデータを個別に読み取る必要がある状況を回避し、同じデータを同時に複数読み取る可能性を回避します。

    この機能は v6.2.0 では実験的であり、v6.3.0 で GA になります。

-   TiFlash はデータ レプリケーション[#5237](https://github.com/pingcap/tiflash/issues/5237) @ [ブリーズウィッシュ](https://github.com/breezewish)のパフォーマンスを向上させます

    TiFlash は、 TiKV からのデータ複製にRaftプロトコルを使用します。 v6.3.0 より前は、大量のレプリカ データを複製するのに長い時間がかかることがよくありました。 TiDB v6.3.0 は、 TiFlashデータ レプリケーション メカニズムを最適化し、レプリケーション速度を大幅に向上させます。 BRを使用してデータをリカバリしたり、 TiDB Lightningを使用してデータをインポートしたり、新しいTiFlashレプリカを追加したりすると、 TiFlashレプリカをより迅速にレプリケートできます。 TiFlashを使用すると、よりタイムリーにクエリを実行できます。さらに、 TiFlashレプリカの数をスケールアップ、スケールダウン、または変更するときに、 TiFlashレプリカはより速く安全でバランスの取れた状態に到達します。

-   TiFlash は、個々の`COUNT(DISTINCT)` [#37202](https://github.com/pingcap/tidb/issues/37202) @ [修正データベース](https://github.com/fixdb)の 3 段階の集約をサポートします

    TiFlash は、 `COUNT(DISTINCT)` 1 つだけ含むクエリの[3段階集計](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)への書き換えをサポートしています。これにより、同時実行性とパフォーマンスが向上します。

-   TiKV はログのリサイクル[#214](https://github.com/tikv/raft-engine/issues/214) @ [リククスサシネーター](https://github.com/LykxSassinator)をサポートします

    TiKV はRaft Engineの[ログファイルのリサイクル](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)をサポートします。これにより、 Raftログの追加中のネットワーク ディスクのロングテールレイテンシーが短縮され、書き込みワークロード時のパフォーマンスが向上します。

-   TiDB は null 対応アンチ結合[#37525](https://github.com/pingcap/tidb/issues/37525) @ [アレナトゥス](https://github.com/Arenatlx)をサポートします

    TiDB v6.3.0 では、新しい結合タイプ[Null 認識アンチ結合 (NAAJ)](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)が導入されています。 NAAJ は、コレクション操作を処理するときに、コレクションが空であるか`NULL`であるかを認識できます。これにより、 `IN`や`= ANY`などの操作の実行効率が最適化され、SQL のパフォーマンスが向上します。

-   ハッシュ結合[#35439](https://github.com/pingcap/tidb/issues/35439) @ [懐かしい](https://github.com/Reminiscent)のビルド終了を制御するオプティマイザー ヒントを追加します。

    v6.3.0 では、TiDB オプティマイザーは、ハッシュ結合、そのプローブ終了、およびビルド終了を指定するための 2 つのヒント`HASH_JOIN_BUILD()`と`HASH_JOIN_PROBE()`を導入します。オプティマイザーが最適な実行計画を選択できない場合、これらのヒントを使用して計画に介入できます。

-   セッションレベルの共通テーブル式 (CTE) インライン[#36514](https://github.com/pingcap/tidb/issues/36514) @ [エルサ0520](https://github.com/elsa0520)をサポート

    TiDB v6.2.0 では、CTE インラインを可能にするオプティマイザーに`MERGE`ヒントが導入され、CTE クエリ結果のコンシューマがTiFlashで並列実行できるようになりました。 v6.3.0 では、セッション内で CTE インラインを許可するためにセッション変数[`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)が導入されました。これにより、使いやすさが大幅に向上します。

### トランザクション {#transactions}

-   悲観的トランザクション[#36579](https://github.com/pingcap/tidb/issues/36579) @ [エキシウム](https://github.com/ekexium)における一意制約のチェックの延期をサポート

    [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)システム変数を使用して、TiDB が悲観的トランザクションで[固有の制約](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御できます。この変数はデフォルトでは無効になっています。変数が有効 ( `ON`に設定) の場合、TiDB は必要になるまで悲観的トランザクションでのロック操作と一意の制約チェックを延期するため、一括 DML 操作のパフォーマンスが向上します。

-   Read-Committed 分離レベル[#36812](https://github.com/pingcap/tidb/issues/36812) @ [トンスネークリン](https://github.com/TonsnakeLin)で TSO をフェッチする方法を最適化します。

    Read-Committed 分離レベルでは、TSO のフェッチ方法を制御するためにシステム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)が導入されています。プラン キャッシュ ヒットの場合、TiDB は TSO をフェッチする頻度を減らすことでバッチ DML ステートメントの実行効率を向上させ、バッチでタスクを実行する実行時間を短縮します。

### 安定性 {#stability}

-   リソースを消費するクエリが軽量クエリの応答時間に及ぼす影響を軽減します[#13313](https://github.com/tikv/tikv/issues/13313) @ [グロルフ](https://github.com/glorv)

    リソースを消費するクエリと軽量のクエリが同時に実行されると、軽量のクエリの応答時間に影響します。この場合、トランザクション サービスの品質を確保するために、軽量のクエリが最初に TiDB によって処理されることが期待されます。 v6.3.0 では、TiKV は読み取りリクエストのスケジューリング メカニズムを最適化し、各ラウンドでのリソースを消費するクエリの実行時間が期待どおりになるようにします。これにより、リソースを消費するクエリが軽量クエリの応答時間に与える影響が大幅に軽減され、混合ワークロード シナリオで P99レイテンシーが 50% 以上削減されます。

-   統計が古くなった場合に統計をロードするデフォルトのポリシーを変更します[#27601](https://github.com/pingcap/tidb/issues/27601) @ [シュイファングリーンアイズ](https://github.com/xuyifangreeneyes)

    v5.3.0 では、TiDB は統計が古くなったときのオプティマイザーの動作を制御するシステム変数[`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)を導入しました。デフォルト値は`ON`で、これは古いバージョンの動作を維持することを意味します。SQL ステートメントに関係するオブジェクトの統計が古い場合、オプティマイザは統計 (テーブルの合計行数以外) が古いものであるとみなします。より信頼性が高く、代わりに疑似統計を使用します。実際のユーザー シナリオのテストと分析の後、v6.3.0 以降、デフォルト値の`tidb_enable_pseudo_for_outdated_stats`が`OFF`に変更されます。統計が古くなっても、オプティマイザはテーブル上の統計を引き続き使用するため、実行計画がより安定します。

-   Titan を無効化すると GA @ [タボキー](https://github.com/tabokie)になります

    オンライン TiKV ノードの場合は[タイタンを無効にする](/storage-engine/titan-configuration.md#disable-titan)を行うことができます。

-   GlobalStats の準備ができていない場合は`static`パーティション プルーニングを使用する[#37535](https://github.com/pingcap/tidb/issues/37535) @ [イーサール](https://github.com/Yisaer)

    [`dynamic pruning`](/partitioned-table.md#dynamic-pruning-mode)が有効な場合、オプティマイザは[グローバル統計](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)に基づいて実行プランを選択します。 GlobalStats が完全に収集される前に、疑似統計を使用すると、パフォーマンスの低下が発生する可能性があります。 v6.3.0 では、GlobalStats が収集される前に動的プルーニングを有効にした場合、この問題は`static`モードを維持することで解決されます。 TiDB は、GlobalStats が収集されるまで`static`モードのままです。これにより、パーティション プルーニング設定を変更するときのパフォーマンスの安定性が確保されます。

### 使いやすさ {#ease-of-use}

-   SQL ベースのデータ配置ルールとTiFlashレプリカ間の競合に対処します[#37171](https://github.com/pingcap/tidb/issues/37171) @ [ルクワンチャオ](https://github.com/lcwangchao)

    TiDB v6.0.0 は、SQL ベースのデータ配置ルールを提供します。ただし、実装上の問題により、この機能はTiFlashレプリカと競合します。 TiDB v6.3.0 は実装メカニズムを最適化します[SQL ベースのデータ配置ルールとTiFlashの間の競合を解決します。](/placement-rules-in-sql.md#known-limitations) .

### MySQLの互換性 {#mysql-compatibility}

-   4 つの正規表現関数( `REGEXP_INSTR()` `REGEXP_REPLACE()`および`REGEXP_SUBSTR()` [#23881](https://github.com/pingcap/tidb/issues/23881) @ [ウィンドトーカー](https://github.com/windtalker)のサポート`REGEXP_LIKE()`追加することにより、MySQL 8.0 の互換性が向上しました。

    MySQL との互換性の詳細については、 [MySQL との正規表現の互換性](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)を参照してください。

-   `CREATE USER`および`ALTER USER`ステートメントは、 `ACCOUNT LOCK/UNLOCK`オプション[#37051](https://github.com/pingcap/tidb/issues/37051) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)をサポートします。

    [`CREATE USER`](/sql-statements/sql-statement-create-user.md)ステートメントを使用してユーザーを作成する場合、 `ACCOUNT LOCK/UNLOCK`オプションを使用して、作成したユーザーをロックするかどうかを指定できます。ロックされたユーザーはデータベースにログインできません。

    [`ALTER USER`](/sql-statements/sql-statement-alter-user.md)ステートメントの`ACCOUNT LOCK/UNLOCK`オプションを使用して、既存のユーザーのロック状態を変更できます。

-   JSON データ型と JSON関数はGA [#36993](https://github.com/pingcap/tidb/issues/36993) @ [ションジウェイ](https://github.com/xiongjiwei)になります

    JSON は、多くのプログラムで採用されている一般的なデータ形式です。 TiDB は、以前のバージョンから実験的機能として[JSONのサポート](/data-type-json.md)を導入しており、MySQL の JSON データ型および一部の JSON関数と互換性があります。

    TiDB v6.3.0 では、JSON データ型と関数がGA になり、TiDB のデータ型が強化され、 [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index)と[生成された列](/generated-columns.md)での JSON関数の使用がサポートされ、TiDB と MySQL の互換性がさらに向上しました。

### バックアップと復元 {#backup-and-restore}

-   PITR はバックアップ ストレージとして[GCS と Azure Blob Storage](/br/backup-and-restore-storages.md) @ [ジョッカウ](https://github.com/joccau)をサポートします

    TiDB クラスターが Google Cloud または Azure にデプロイされている場合は、クラスターを v6.3.0 にアップグレードした後に PITR 機能を使用できます。

-   BR はAWS S3 オブジェクト ロック[#13442](https://github.com/tikv/tikv/issues/13442) @ [3ポインター](https://github.com/3pointer)をサポートします

    [S3 オブジェクトロック](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)を有効にすることで、AWS 上のバックアップ データが改ざんまたは削除されないように保護できます。

### データ移行 {#data-migration}

-   TiDB Lightning は[Apache Hive によってエクスポートされた Parquet ファイルを TiDB にインポート](/tidb-lightning/tidb-lightning-data-source.md#parquet) [#37536](https://github.com/pingcap/tidb/issues/37536) @ [ブチュイトデゴウ](https://github.com/buchuitoudegou)をサポートします

-   DM は新しい構成アイテムを追加します`safe-mode-duration` [#6224](https://github.com/pingcap/tiflow/issues/6224) @ [オクジャン](https://github.com/okJiang)

    この設定項目は[タスク構成ファイル](/dm/task-configuration-file-full.md)に追加されます。 DM が異常終了した後の自動セーフ モードの継続時間を調整できます。デフォルト値は 60 秒です。 `safe-mode-duration`が`"0s"`に設定されている場合、異常な再起動後に DM がセーフ モードに入ろうとするとエラーが報告されます。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、地理的に分散された複数のデータ ソース[#5301](https://github.com/pingcap/tiflow/issues/5301) @ [スドジ](https://github.com/sdojjy)からデータを複製できる展開トポロジをサポートします。

    v6.3.0 以降、単一の TiDB クラスターから複数の地理的に分散されたデータ システムへのデータの複製をサポートするには、IDC ごとにデータを複製する必要が[TiCDC を複数の IDC に導入できます](/ticdc/deploy-ticdc.md)ます。この機能は、地理的に分散されたデータ レプリケーションおよび展開トポロジの機能を提供するのに役立ちます。

-   TiCDC は、アップストリームとダウンストリーム (同期ポイント) [#6977](https://github.com/pingcap/tiflow/issues/6977) @ [東門](https://github.com/asddongmen)の間でスナップショットの一貫性を維持することをサポートします。

    災害復旧のためのデータ複製のシナリオでは、ダウンストリーム スナップショットがアップストリーム スナップショットと一貫性を保つように、TiCDC は[ダウンストリームデータのスナップショットを定期的に維持する](/ticdc/ticdc-upstream-downstream-check.md)をサポートします。この機能により、TiCDC は読み取りと書き込みが分離されるシナリオをより適切にサポートし、コストの削減に役立ちます。

-   TiCDC はグレースフル アップグレード[#4757](https://github.com/pingcap/tiflow/issues/4757) @ [オーバーヴィーナス](https://github.com/overvenus) @ [3エースショーハンド](https://github.com/3AceShowHand)をサポートします

    TiCDC が[TiUP](/ticdc/deploy-ticdc.md#upgrade-cautions) (&gt;=v1.11.0) または[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (&gt;=v1.3.8) を使用してデプロイされている場合、TiCDC クラスターを正常にアップグレードできます。アップグレード中のデータ レプリケーションのレイテンシーは30 秒程度に抑えられます。これにより安定性が向上し、TiCDC がレイテンシの影響を受けやすいアプリケーションをより適切にサポートできるようになります。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                         | 種類の変更    | 説明                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`default_authentication_plugin`](/system-variables.md#default_authentication_plugin)                                       | 修正済み     | 新しいオプション`tidb_sm3_password`を追加します。この変数を`tidb_sm3_password`に設定すると、暗号化アルゴリズムとして SM3 が使用されます。                                                                                                                                                       |
| [`sql_require_primary_key`](/system-variables.md#sql_require_primary_key-new-in-v630)                                       | 新しく追加された | テーブルに主キーがあるという要件を強制するかどうかを制御します。この変数を有効にした後、主キーなしでテーブルを作成または変更しようとすると、エラーが発生します。                                                                                                                                                                 |
| [`tidb_adaptive_closest_read_threshold`](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)             | 新しく追加された | [`tidb_replica_read`](/system-variables.md#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合、TiDBサーバーがTiDBサーバーと同じリージョン内のレプリカに読み取りリクエストを送信することを優先するしきい値を制御します。                                                                           |
| [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | 新しく追加された | TiDB が悲観的トランザクションで[固有の制約](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御します。                                                                                                                                                           |
| [`tidb_ddl_disk_quota`](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)                                               | 新しく追加された | [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が有効な場合にのみ有効になります。インデックス作成時のバックフィル中のローカルstorageの使用制限を設定します。                                                                                            |
| [`tidb_ddl_enable_fast_reorg`](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                 | 新しく追加された | インデックス作成時のバックフィルの速度を向上させるために、 `ADD INDEX`および`CREATE INDEX` DDL 操作の高速化を有効にするかどうかを制御します。                                                                                                                                                           |
| [`tidb_ddl_flashback_concurrency`](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                         | 新しく追加された | `flashback cluster`の同時実行性を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                     |
| [`tidb_enable_exchange_partition`](/system-variables.md#tidb_enable_exchange_partition)                                     | 廃止されました  | [`exchange partitions with tables`](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトで`exchange partitions with tables`が有効になります。                                                                             |
| [`tidb_enable_foreign_key`](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                       | 新しく追加された | `FOREIGN KEY`機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                     |
| `tidb_enable_general_plan_cache`                                                                                            | 新しく追加された | 一般プラン キャッシュ機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                       |
| [`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                   | 新しく追加された | [メタデータロック](/metadata-lock.md)機能を有効にするかどうかを指定します。                                                                                                                                                                                                 |
| [`tidb_enable_null_aware_anti_join`](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                     | 新しく追加された | 特別な集合演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによってアンチ結合が生成される場合に、TiDB が Null-Aware Hash Join を適用するかどうかを制御します。                                                                                                                                          |
| [`tidb_enable_pseudo_for_outdated_stats`](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)           | 修正済み     | 統計が古い場合に、テーブルの統計を使用する際のオプティマイザーの動作を制御します。デフォルト値は`ON`から`OFF`に変更されます。これは、このテーブルの統計が古くても、オプティマイザはテーブルの統計を引き続き使用することを意味します。                                                                                                                          |
| [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)                                       | 修正済み     | データを読み取るオペレータの動的メモリ制御機能を有効にするかどうかを制御します。この変数が`ON`に設定されている場合、メモリ使用量は[`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)の制御下にない可能性があります。したがって、デフォルト値は`ON`から`OFF`に変更されます。                                                           |
| [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)       | 新しく追加された | SQL 書き込みステートメントの読み取りリクエストをTiFlashにプッシュダウンするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                               |
| [`tidb_enable_unsafe_substitute`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 式を安全でない方法で生成された列に置き換えるかどうかを制御します。                                                                                                                                                                                                                |
| `tidb_general_plan_cache_size`                                                                                              | 新しく追加された | 一般プラン キャッシュによってキャッシュできる実行プランの最大数を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                              |
| [`tidb_last_plan_replayer_token`](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                           | 新しく追加された | 読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行結果を取得するために使用されます。                                                                                                                                                                                     |
| [tidb_max_paging_size](/system-variables.md#tidb_max_paging_size-new-in-v630)                                               | 新しく追加された | この変数は、コプロセッサーのページング要求プロセス中に最小行数を設定するために使用されます。                                                                                                                                                                                                   |
| [`tidb_opt_force_inline_cte`](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)                                   | 新しく追加された | セッション全体の共通テーブル式 (CTE) をインライン化するかどうかを制御します。デフォルト値は`OFF`です。これは、CTE のインライン化がデフォルトでは強制されないことを意味します。                                                                                                                                                  |
| [`tidb_opt_three_stage_distinct_agg`](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)                   | 新しく追加された | MPP モードで`COUNT(DISTINCT)`集計を 3 段階の集計に書き換えるかどうかを指定します。デフォルト値は`ON`です。                                                                                                                                                                              |
| [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)                                    | 修正済み     | 動的プルーニングを有効にするかどうかを指定します。 v6.3.0 以降、デフォルト値は`dynamic`に変更されます。                                                                                                                                                                                     |
| [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                           | 修正済み     | タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれな読み取りコミット分離レベルのシナリオに適しています。この機能は特定のサービス ワークロードを対象としているため、他のシナリオではパフォーマンスの低下を引き起こす可能性があります。このため、v6.3.0 以降、この変数のスコープは`GLOBAL \| SESSION`から`INSTANCE`に変更されます。つまり、特定の TiDB インスタンスに対してこの機能を有効にすることができます。 |
| [`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)                                         | 新しく追加された | タイムスタンプの取得を最適化するために使用され、悲観的トランザクションの RC 分離レベルでポイント書き込み競合がほとんどないシナリオに適しています。この変数を有効にすると、point-write ステートメントの実行中にグローバル タイムスタンプを取得することによってもたらされるレイテンシーとオーバーヘッドを回避できます。                                                                              |
| [`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)                                                     | 新しく追加された | FastScan を有効にするかどうかを制御します。 [ファストスキャン](/tiflash/use-fastscan.md)が有効になっている ( `ON`に設定されている) 場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。                                                                                         |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                            | 種類の変更    | 説明                                                                                                                                                                                                                          |
| -------------- | ----------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TiDB           | [`temp-dir`](/tidb-configuration-file.md#temp-dir-new-in-v630)                                        | 新しく追加された | TiDB が一時データを保存するために使用するファイル システムの場所を指定します。機能が TiDB ノードのローカルstorageを必要とする場合、TiDB は対応する一時データをこの場所に保存します。デフォルト値は`/tmp/tidb`です。                                                                                                 |
| TiKV           | [`auto-adjust-pool-size`](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)              | 新しく追加された | スレッド プール サイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。                                                                                                   |
| TiKV           | [`data-encryption-method`](/tikv-configuration-file.md#data-encryption-method)                        | 修正済み     | 新しい値のオプション`sm4-ctr`を導入します。この設定項目を`sm4-ctr`に設定すると、データは SM4 を使用して暗号化されて保存されます。                                                                                                                                                |
| TiKV           | [`enable-log-recycle`](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                    | 新しく追加された | Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。これを有効にすると、論理的にパージされたログ ファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが短縮されます。この設定項目は、 [フォーマットバージョン](/tikv-configuration-file.md#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。 |
| TiKV           | [`format-version`](/tikv-configuration-file.md#format-version-new-in-v630)                            | 新しく追加された | Raft Engineのログ ファイルのバージョンを指定します。 v6.3.0 より前の TiKV のデフォルトのログ ファイル バージョンは`1`です。ログ ファイルは TiKV v6.1.0 以上で読み取ることができます。 TiKV v6.3.0 以降のデフォルトのログ ファイル バージョンは`2`です。 TiKV v6.3.0 以降では、ログ ファイルを読み取ることができます。                           |
| TiKV           | [`log-backup.enable`](/tikv-configuration-file.md#enable-new-in-v620)                                 | 修正済み     | v6.3.0 以降、デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                    |
| TiKV           | [`log-backup.max-flush-interval`](/tikv-configuration-file.md#max-flush-interval-new-in-v620)         | 修正済み     | v6.3.0 以降、デフォルト値は`5min`から`3min`に変更されます。                                                                                                                                                                                     |
| PD             | [診断を有効にする](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                   | 新しく追加された | 診断機能を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                      |
| TiFlash        | [`dt_enable_read_thread`](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)   | 廃止されました  | v6.3.0 以降、この設定項目は非推奨になりました。スレッド プールは、デフォルトでstorageエンジンからの読み取りリクエストを処理するために使用され、無効にすることはできません。                                                                                                                               |
| DM             | [`safe-mode-duration`](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | 自動セーフモードの継続時間を指定します。                                                                                                                                                                                                        |
| TiCDC          | [`enable-sync-point`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)          | 新しく追加された | 同期ポイント機能を有効にするかどうかを指定します。                                                                                                                                                                                                   |
| TiCDC          | [`sync-point-interval`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)        | 新しく追加された | Syncpoint がアップストリームとダウンストリームのスナップショットを調整する間隔を指定します。                                                                                                                                                                         |
| TiCDC          | [`sync-point-retention`](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)       | 新しく追加された | 同期ポイントによってダウンストリーム テーブルにデータが保持される期間を指定します。この期間を超えると、データはクリーンアップされます。                                                                                                                                                        |
| TiCDC          | [`sink-uri.memory`](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters)                      | 廃止されました  | `memory`ソートは非推奨になりました。いかなる状況でも使用することはお勧めできません。                                                                                                                                                                              |

### その他 {#others}

-   ログ バックアップは、バックアップstorageとして GCS および Azure Blob Storage をサポートします。
-   ログ バックアップが`exchange partition` DDL と互換性を持つようになりました。
-   以前[高速スキャン](/tiflash/use-fastscan.md)有効にするために使用されていた SQL ステートメント`ALTER TABLE ...SET TiFLASH MODE ...`非推奨になり、システム変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)に置き換えられます。 v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定は無効になりますが、データの通常の読み取りには影響しません。この場合、変数[`tiflash_fastscan`](/system-variables.md#tiflash_fastscan-new-in-v630)を設定して FastScan を有効または無効にする必要があります。以前のバージョンから v6.3.0 にアップグレードする場合、データの一貫性を保つために、すべてのセッションに対して FastScan 機能がデフォルトで有効になりません。
-   Linux AMD64アーキテクチャでTiFlashを導入するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを導入するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セット拡張を使用することにより、TiFlash のベクトル化エンジンはより優れたパフォーマンスを実現できます。
-   TiDB で動作する HAProxy の最小バージョンは v1.5 になりました。 v1.5 と v2.1 の間の HAProxy バージョンでは、 `post-41`構成オプションを`mysql-check`に設定する必要があります。 HAProxy v2.2 以降を使用することをお勧めします。

## 削除された機能 {#removed-feature}

v6.3.0 以降、TiCDC は Pulsar シンクの構成をサポートしなくなりました。 StreamNative が提供する[コップ](https://github.com/streamnative/kop)代替として使用できます。

## 改善点 {#improvements}

-   TiDB

    -   TiDB は、テーブルの存在をチェックするときにターゲット テーブル名の大文字と小文字を区別しないようになりました[#34610](https://github.com/pingcap/tidb/issues/34610) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)
    -   `init_connect` [#35324](https://github.com/pingcap/tidb/issues/35324) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)の値を設定するときに解析チェックを追加することで、MySQL の互換性を向上させます。
    -   新しい接続に対して生成されるログ警告を改善[#34964](https://github.com/pingcap/tidb/issues/34964) @ [ションジウェイ](https://github.com/xiongjiwei)
    -   DDL 履歴ジョブをクエリするための HTTP API を最適化し、 `start_job_id`パラメーター[#35838](https://github.com/pingcap/tidb/issues/35838) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)のサポートを追加します。
    -   JSON パスの構文が間違っている場合にエラーを報告する[#22525](https://github.com/pingcap/tidb/issues/22525) [#34959](https://github.com/pingcap/tidb/issues/34959) @ [ションジウェイ](https://github.com/xiongjiwei)
    -   偽共有の問題[#37641](https://github.com/pingcap/tidb/issues/37641) @ [ゲンリキ](https://github.com/gengliqi)を修正して、結合操作のパフォーマンスを向上させます。
    -   [`PLAN REPLAYER`](/sql-plan-replayer.md)を使用して一度に複数の SQL ステートメントの実行計画情報をエクスポートすることをサポートします。これにより、トラブルシューティングがより効率的になります[#37798](https://github.com/pingcap/tidb/issues/37798) @ [イーサール](https://github.com/Yisaer)

-   TiKV

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポート[#13054](https://github.com/tikv/tikv/issues/13054) @ [5kbps](https://github.com/5kbpers)
    -   TSO サービス[#12794](https://github.com/tikv/tikv/issues/12794) @ [ピンギュ](https://github.com/pingyu)のフォールト トレランスを向上します。
    -   RocksDB で同時に実行されるサブコンパクション操作の数の動的変更をサポート ( `rocksdb.max-sub-compactions` ) [#13145](https://github.com/tikv/tikv/issues/13145) @ [エーテルフロー](https://github.com/ethercflow)
    -   空のリージョン[#12421](https://github.com/tikv/tikv/issues/12421) @ [タボキー](https://github.com/tabokie)をマージするパフォーマンスを最適化します。
    -   より多くの正規表現関数をサポート[#13483](https://github.com/tikv/tikv/issues/13483) @ [ゲンリキ](https://github.com/gengliqi)
    -   CPU 使用率[#13313](https://github.com/tikv/tikv/issues/13313) @ [グロルフ](https://github.com/glorv)に基づいてスレッド プール サイズを自動的に調整するサポート

-   PD

    -   TiDB ダッシュボード[#5366](https://github.com/tikv/pd/issues/5366) @ [イニシュ9506](https://github.com/YiniXu9506)での TiKV IO MBps メトリクスのクエリを改善しました。
    -   TiDB ダッシュボードの URL を`metrics`から`monitoring` [#5366](https://github.com/tikv/pd/issues/5366) @ [イニシュ9506](https://github.com/YiniXu9506)に変更します。

-   TiFlash

    -   `elt`機能をTiFlash [#5104](https://github.com/pingcap/tiflash/issues/5104) @ [ウィレンドレス](https://github.com/Willendless)にプッシュダウンするサポート
    -   `leftShift`機能をTiFlash [#5099](https://github.com/pingcap/tiflash/issues/5099) @ [アニー・オブ・ザ・スターズ](https://github.com/AnnieoftheStars)にプッシュダウンするサポート
    -   `castTimeAsDuration`機能をTiFlash [#5306](https://github.com/pingcap/tiflash/issues/5306) @ [アンチトップクワーク](https://github.com/AntiTopQuark)にプッシュダウンするサポート
    -   `HexIntArg/HexStrArg`機能をTiFlash [#5107](https://github.com/pingcap/tiflash/issues/5107) @ [ヤンケオ](https://github.com/YangKeao)にプッシュダウンするサポート
    -   TiFlash のインタープリタをリファクタリングし、新しいインタープリタ Planner [#4739](https://github.com/pingcap/tiflash/issues/4739) @ [シーライズ](https://github.com/SeaRise)をサポートします。
    -   TiFlash [#5609](https://github.com/pingcap/tiflash/issues/5609) @ [ベストウッディ](https://github.com/bestwoody)のメモリトラッカーの精度を向上
    -   `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN`照合順序[#5294](https://github.com/pingcap/tiflash/issues/5294) @ [ソロッツグ](https://github.com/solotzg)を使用して文字列列のパフォーマンスを向上させます。
    -   ReadLimiter [#5401](https://github.com/pingcap/tiflash/issues/5401) 、 [#5091](https://github.com/pingcap/tiflash/issues/5091) @ [ロイド・ポティガー](https://github.com/Lloyd-Pottiger)でバックグラウンドで I/O スループットを計算します。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR はログ バックアップで生成された小さなファイルをマージできるため、バックアップ ファイルの数が大幅に削減されます[#13232](https://github.com/tikv/tikv/issues/13232) @ [レヴルス](https://github.com/Leavrth)
        -   PITR は、復元後のアップストリーム クラスター構成に基づいたTiFlashレプリカの数の自動構成をサポートします[#37208](https://github.com/pingcap/tidb/issues/37208) @ [ユジュンセン](https://github.com/YuJuncen)

    -   TiCDC

        -   アップストリームの TiDB [#6506](https://github.com/pingcap/tiflow/issues/6506) @ [ランス6716](https://github.com/lance6716)で導入された同時 DDL フレームワークと TiCDC の互換性を向上させます。
        -   MySQL シンクでエラー[#6460](https://github.com/pingcap/tiflow/issues/6460) @ [オーバーヴィーナス](https://github.com/overvenus)が発生した場合の DML ステートメントのロギング`start ts`をサポートします。
        -   `api/v1/health` API を強化して、TiCDC クラスターのより正確な正常性状態を返す[#4757](https://github.com/pingcap/tiflow/issues/4757) @ [オーバーヴィーナス](https://github.com/overvenus)
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[#5928](https://github.com/pingcap/tiflow/issues/5928) @ [ひっくり返る](https://github.com/hicqu) @ [こんにちはラスティン](https://github.com/hi-rustin)
        -   非推奨のパルサー シンク[#7087](https://github.com/pingcap/tiflow/issues/7087) @ [こんにちはラスティン](https://github.com/hi-rustin)を削除します。
        -   変更フィードに無関係な DDL ステートメントを破棄することで、レプリケーションのパフォーマンスを向上させます[#6447](https://github.com/pingcap/tiflow/issues/6447) @ [東門](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   データソース[#6448](https://github.com/pingcap/tiflow/issues/6448) @ [ランス6716](https://github.com/lance6716)としての MySQL 8.0 との互換性の向上
        -   「無効な接続」が発生したときに DDL を非同期に実行することで DDL を最適化します[#4689](https://github.com/pingcap/tiflow/issues/4689) @ [lyzx2001](https://github.com/lyzx2001)

    -   TiDB Lightning

        -   S3 外部storageURL のクエリ パラメータを追加して、特定のロール[#36891](https://github.com/pingcap/tidb/issues/36891) @ [dsダシュン](https://github.com/dsdashun)を引き受けることで別のアカウントの S3 データへのアクセスをサポートします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメント[#35784](https://github.com/pingcap/tidb/issues/35784) @ [ルクワンチャオ](https://github.com/lcwangchao)で権限チェックがスキップされる問題を修正
    -   システム変数`tidb_enable_noop_variable`が`WARN` [#36647](https://github.com/pingcap/tidb/issues/36647) @ [ルクワンチャオ](https://github.com/lcwangchao)に設定できる問題を修正
    -   式インデックスが定義されている場合、 `INFORMAITON_SCHEMA.COLUMNS`テーブルの`ORDINAL_POSITION`列が正しくない可能性がある問題を修正します[#31200](https://github.com/pingcap/tidb/issues/31200) @ [bb7133](https://github.com/bb7133)
    -   タイムスタンプが`MAXINT32` [#31585](https://github.com/pingcap/tidb/issues/31585) @ [bb7133](https://github.com/bb7133)より大きい場合に TiDB がエラーを報告しない問題を修正
    -   エンタープライズプラグイン使用時にTiDBサーバーが起動できない問題を修正[#37319](https://github.com/pingcap/tidb/issues/37319) @ [ゼボックス](https://github.com/xhebox)
    -   `SHOW CREATE PLACEMENT POLICY` [#37526](https://github.com/pingcap/tidb/issues/37526) @ [ゼボックス](https://github.com/xhebox)の誤った出力を修正
    -   一時テーブル[#37201](https://github.com/pingcap/tidb/issues/37201) @ [ルクワンチャオ](https://github.com/lcwangchao)での予期しない動作`EXCHANGE PARTITION`を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると間違った結果 @ [ジムララ](https://github.com/zimulala)が返される問題を修正します。
    -   ビューに対する`EXPLAIN`クエリが権限[#34326](https://github.com/pingcap/tidb/issues/34326) @ [ホーキングレイ](https://github.com/hawkingrei)をチェックしない問題を修正します。
    -   JSON `null` `NULL` [#37852](https://github.com/pingcap/tidb/issues/37852) @ [ヤンケオ](https://github.com/YangKeao)に更新できない問題を修正
    -   DDL ジョブの`row_count`が不正確である問題を修正[#25968](https://github.com/pingcap/tidb/issues/25968) @ [定義2014](https://github.com/Defined2014)
    -   `FLASHBACK TABLE` [#37386](https://github.com/pingcap/tidb/issues/37386) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)が正常に動作しない問題を修正
    -   一般的な MySQL プロトコル[#36731](https://github.com/pingcap/tidb/issues/36731) @ [ドヴィーデン](https://github.com/dveeden)で`prepared`ステートメント フラグの処理に失敗する問題を修正
    -   一部の極端なケースで起動時に表示される可能性がある不正な TiDB ステータスの問題を修正します[#36791](https://github.com/pingcap/tidb/issues/36791) @ [ゼボックス](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.VARIABLES_INFO`がセキュリティ強化モード (SEM) [#37586](https://github.com/pingcap/tidb/issues/37586) @ [Cbcウェストウルフ](https://github.com/CbcWestwolf)に準拠していない問題を修正
    -   `UNION` [#31678](https://github.com/pingcap/tidb/issues/31678) @ [CBCウエストウルフ](https://github.com/cbcwestwolf)を使用したクエリで文字列から文字列へのキャストが失敗する問題を修正
    -   TiFlash [#37254](https://github.com/pingcap/tidb/issues/37254) @ [wshwsh12](https://github.com/wshwsh12)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   TiDB のバイナリ文字列と JSON 間のキャストと比較が MySQL [#31918](https://github.com/pingcap/tidb/issues/31918) [#25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケオ](https://github.com/YangKeao)と互換性がない問題を修正
    -   TiDB の`JSON_OBJECTAGG`と`JSON_ARRAYAGG`がバイナリ値[#25053](https://github.com/pingcap/tidb/issues/25053) @ [ヤンケオ](https://github.com/YangKeao)で MySQL と互換性がない問題を修正
    -   JSON の不透明な値間の比較でpanic[#37315](https://github.com/pingcap/tidb/issues/37315) @ [ヤンケオ](https://github.com/YangKeao)が発生する問題を修正
    -   JSON集計関数[#37287](https://github.com/pingcap/tidb/issues/37287) @ [ヤンケオ](https://github.com/YangKeao)で単精度浮動小数点数が使用できない問題を修正
    -   `UNION`演算子が予期しない空の結果[#36903](https://github.com/pingcap/tidb/issues/36903) @ [ティエンチャイアマオ](https://github.com/tiancaiamao)を返す可能性がある問題を修正します。
    -   `castRealAsTime`式の結果が MySQL [#37462](https://github.com/pingcap/tidb/issues/37462) @ [孟新9014](https://github.com/mengxin9014)と一致しない問題を修正
    -   悲観的DML 操作により、一意でないインデックス キー[#36235](https://github.com/pingcap/tidb/issues/36235) @ [エキシウム](https://github.com/ekexium)がロックされる問題を修正します。
    -   `auto-commit`変更がトランザクションのコミット動作[#36581](https://github.com/pingcap/tidb/issues/36581) @ [cfzjywxk](https://github.com/cfzjywxk)に影響を与える問題を修正
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[#37373](https://github.com/pingcap/tidb/issues/37373) @ [cfzjywxk](https://github.com/cfzjywxk)
    -   場合によっては UPDATE ステートメントが誤って投影を削除し、 `Can't find column`エラー[#37568](https://github.com/pingcap/tidb/issues/37568) @ [アイリンキッド](https://github.com/AilinKid)が発生する問題を修正します。
    -   結合したテーブルの再配置操作により誤って外部結合条件[#37238](https://github.com/pingcap/tidb/issues/37238) @ [アイリンキッド](https://github.com/AilinKid)がプッシュダウンされる問題を修正します。
    -   一部のパターンの`IN`および`NOT IN`サブクエリで`Can't find column`エラー[#37032](https://github.com/pingcap/tidb/issues/37032) @ [アイリンキッド](https://github.com/AilinKid)が報告される問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [#35758](https://github.com/pingcap/tidb/issues/35758) @ [アイリンキッド](https://github.com/AilinKid)が含まれる場合に`Can't find column`が報告される問題を修正
    -   間違った`PromQL` [#35856](https://github.com/pingcap/tidb/issues/35856) @ [定義2014](https://github.com/Defined2014)を修正

-   TiKV

    -   リージョンハートビートが中断された後、PD が TiKV に再接続しない問題を修正[#12934](https://github.com/tikv/tikv/issues/12934) @ [バッファフライ](https://github.com/bufferflies)
    -   Raftstore がビジー[#13160](https://github.com/tikv/tikv/issues/13160) @ [5kbps](https://github.com/5kbpers)の場合、リージョンが重複する可能性がある問題を修正
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[#13191](https://github.com/tikv/tikv/issues/13191) @ [バッファフライ](https://github.com/bufferflies) [#12933](https://github.com/tikv/tikv/issues/12933) @ [バートン秦](https://github.com/BurtonQin)
    -   暗号化が無効になっている場合に TiKV がpanicになる可能性がある問題を修正[#13081](https://github.com/tikv/tikv/issues/13081) @ [嘉陽鄭](https://github.com/jiayang-zheng)
    -   ダッシュボード[#13086](https://github.com/tikv/tikv/issues/13086) @ [グロルフ](https://github.com/glorv)の`Unified Read Pool CPU`の間違った式を修正
    -   TiKV インスタンスが隔離されたネットワーク環境[#12966](https://github.com/tikv/tikv/issues/12966) @ [コスベン](https://github.com/cosven)にある場合、TiKV サービスが数分間利用できなくなる問題を修正します。
    -   TiKV が誤って`PessimisticLockNotFound`エラー[#13425](https://github.com/tikv/tikv/issues/13425) @ [スティックナーフ](https://github.com/sticnarf)を報告する問題を修正
    -   状況によっては PITR によってデータ損失が発生する可能性がある問題を修正[#13281](https://github.com/tikv/tikv/issues/13281) @ [ユジュンセン](https://github.com/YuJuncen)
    -   長い悲観的トランザクション[#13304](https://github.com/tikv/tikv/issues/13304) @ [ユジュンセン](https://github.com/YuJuncen)があるときにチェックポイントが進められない問題を修正
    -   TiKV が JSON [#13417](https://github.com/tikv/tikv/issues/13417) @ [ヤンケオ](https://github.com/YangKeao)の datetime 型 ( `DATETIME` 、 `DATE` 、 `TIMESTAMP` 、 `TIME` ) と`STRING`型を区別しない問題を修正します。
    -   JSON bool と他の JSON 値[#13386](https://github.com/tikv/tikv/issues/13386) [#37481](https://github.com/pingcap/tidb/issues/37481) @ [ヤンケオ](https://github.com/YangKeao)の比較における MySQL との非互換性を修正

-   PD

    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって引き起こされる PD パニックを修正[#5373](https://github.com/tikv/pd/issues/5373) @ [バッファフライ](https://github.com/bufferflies)
    -   異常なリージョンにより PDpanic[#5491](https://github.com/tikv/pd/issues/5491) @ [ノールーシュ](https://github.com/nolouch)が発生する可能性がある問題を修正
    -   TiFlash学習者のレプリカが作成されないことがある問題を修正[#5401](https://github.com/tikv/pd/issues/5401) @ [フンドゥンDM](https://github.com/HunDunDM)

-   TiFlash

    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[#5814](https://github.com/pingcap/tiflash/issues/5814) @ [シーライズ](https://github.com/SeaRise)
    -   `CAST(value AS DATETIME)`の間違ったデータ入力によりTiFlash sys CPU [#5097](https://github.com/pingcap/tiflash/issues/5097) @ [xzhangxian1008](https://github.com/xzhangxian1008)のパフォーマンスが高くなる問題を修正
    -   `CAST(Real/Decimal AS time)`の結果がMySQL [#3779](https://github.com/pingcap/tiflash/issues/3779) @ [孟新9014](https://github.com/mengxin9014)と矛盾する問題を修正
    -   storage内の一部の古いデータが削除できない問題を修正[#5570](https://github.com/pingcap/tiflash/issues/5570) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)
    -   ページ GC がテーブル[#5697](https://github.com/pingcap/tiflash/issues/5697) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)の作成をブロックする可能性がある問題を修正
    -   `NULL`値[#5859](https://github.com/pingcap/tiflash/issues/5859) @ [ジェイ・ソン・ファン](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   チェックポイントの情報が古くなる可能性がある問題を修正[#36423](https://github.com/pingcap/tidb/issues/36423) @ [ユジュンセン](https://github.com/YuJuncen)
        -   復元中に同時実行数の設定が大きすぎるため、リージョンのバランスが取れない問題を修正[#37549](https://github.com/pingcap/tidb/issues/37549) @ [3ポインター](https://github.com/3pointer)
        -   TiCDC がクラスター[#37822](https://github.com/pingcap/tidb/issues/37822) @ [ユジュンセン](https://github.com/YuJuncen)に存在する場合に、ログ バックアップ チェックポイント TS がスタックする可能性がある問題を修正します。
        -   外部storage[#37469](https://github.com/pingcap/tidb/issues/37469) @ [モクイシュル28](https://github.com/MoCuishle28)の認証キーに特殊文字が存在する場合、バックアップと復元が失敗する可能性がある問題を修正

    -   TiCDC

        -   TiCDC が grpc サービス[#6458](https://github.com/pingcap/tiflow/issues/6458) @ [クレラックス](https://github.com/crelax)で間違った PD アドレスに対して不正確なエラーを返す問題を修正
        -   `cdc cause cli changefeed list`コマンドが失敗した変更フィード[#6334](https://github.com/pingcap/tiflow/issues/6334) @ [東門](https://github.com/asddongmen)を返さない問題を修正します。
        -   チェンジフィードの初期化が失敗した場合に TiCDC が利用できない問題を修正[#6859](https://github.com/pingcap/tiflow/issues/6859) @ [東門](https://github.com/asddongmen)

    -   TiDBBinlog

        -   コンプレッサーが gzip [#1152](https://github.com/pingcap/tidb-binlog/issues/1152) @ [リチュンジュ](https://github.com/lichunzhu)に設定されている場合、 Drainer がリクエストをPumpに正しく送信できない問題を修正

    -   TiDB データ移行 (DM)

        -   DM が`Specified key was too long`エラー[#5315](https://github.com/pingcap/tiflow/issues/5315) @ [ランス6716](https://github.com/lance6716)を報告する問題を修正
        -   リレーがエラー[#6193](https://github.com/pingcap/tiflow/issues/6193) @ [ランス6716](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   `collation_compatible`を`"strict"`に設定すると、DM が重複した照合順序[#6832](https://github.com/pingcap/tiflow/issues/6832) @ [ランス6716](https://github.com/lance6716)を含む SQL を生成する可能性がある問題を修正します。
        -   DM-worker ログ[#6628](https://github.com/pingcap/tiflow/issues/6628) @ [lyzx2001](https://github.com/lyzx2001)に表示される警告メッセージ「 binlog status_vars からタイムゾーンを取得するときにエラーが見つかりました」の表示を減らします。
        -   レプリケーション[#7028](https://github.com/pingcap/tiflow/issues/7028) @ [ランス6716](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル[#36980](https://github.com/pingcap/tidb/issues/36980) @ [D3ハンター](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正します。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   @ [DJ](https://github.com/An-DJ)
-   @ [アニー・オブ・ザ・スターズ](https://github.com/AnnieoftheStars)
-   @ [アンチトップクワーク](https://github.com/AntiTopQuark)
-   @ [ブラックティア23](https://github.com/blacktear23)
-   @ [バートン秦](https://github.com/BurtonQin) (初投稿者)
-   @ [クレラックス](https://github.com/crelax)
-   @ [エルトシア](https://github.com/eltociear)
-   @ [ふざ1989](https://github.com/fuzhe1989)
-   @ [エルワドバ](https://github.com/erwadba)
-   @ [ジャンジヤオ](https://github.com/jianzhiyao)
-   @ [ジョイセ06](https://github.com/joycse06)
-   @ [モルゴ](https://github.com/morgo)
-   @ [オンリーキャット](https://github.com/onlyacat)
-   @ [ピークジ](https://github.com/peakji)
-   @ [ルズリミアク](https://github.com/rzrymiak)
-   @ [てそくん](https://github.com/tisonkun)
-   @ [ホワイトキープワーク](https://github.com/whitekeepwork)
-   @ [Ziy1-Tan](https://github.com/Ziy1-Tan)

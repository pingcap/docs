---
title: TiDB 6.3.0 Release Notes
---

# TiDB 6.3.0 リリースノート {#tidb-6-3-0-release-notes}

発売日：2022年9月30日

TiDB バージョン: 6.3.0-DMR

クイックアクセス: [<a href="https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb">クイックスタート</a>](https://docs.pingcap.com/tidb/v6.3/quick-start-with-tidb) | [<a href="https://www.pingcap.com/download/?version=v6.3.0#version-list">インストールパッケージ</a>](https://www.pingcap.com/download/?version=v6.3.0#version-list)

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

-   レンジ パーティションの定義を簡素化するために、新しい糖衣構文 (レンジ インターバル パーティショニング) を追加しました (実験的) [<a href="https://github.com/pingcap/tidb/issues/35683">#35683</a>](https://github.com/pingcap/tidb/issues/35683) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)

    TiDB は、レンジ パーティションを定義する新しい方法として[<a href="/partitioned-table.md#range-interval-partitioning">間隔パーティショニング</a>](/partitioned-table.md#range-interval-partitioning)を提供します。すべてのパーティションを列挙する必要がないため、範囲パーティション化 DDL ステートメントの長さが大幅に短縮されます。構文は、元の Range パーティショニングの構文と同等です。

-   範囲 COLUMNS パーティショニングは、複数の列[<a href="https://github.com/pingcap/tidb/issues/36636">#36636</a>](https://github.com/pingcap/tidb/issues/36636) @ [<a href="https://github.com/mjonss">むじょん</a>](https://github.com/mjonss)の定義をサポートします。

    TiDB は[<a href="/partitioned-table.md#range-columns-partitioning">範囲列によるパーティション化 (column_list)</a>](/partitioned-table.md#range-columns-partitioning)をサポートします。 `column_list`は単一列に限定されなくなりました。基本的な機能はMySQLと同じです。

-   [<a href="/partitioned-table.md#partition-management">交換パーティション</a>](/partitioned-table.md#partition-management) GA [<a href="https://github.com/pingcap/tidb/issues/35996">#35996</a>](https://github.com/pingcap/tidb/issues/35996) @ [<a href="https://github.com/ymkzpx">ymkzpx</a>](https://github.com/ymkzpx)になります

-   TiFlash [<a href="https://github.com/pingcap/tiflash/issues/5579">#5579</a>](https://github.com/pingcap/tiflash/issues/5579) @ [<a href="https://github.com/SeaRise">シーライズ</a>](https://github.com/SeaRise)へのさらに 2 つの[<a href="/tiflash/tiflash-supported-pushdown-calculations.md">ウィンドウ関数</a>](/tiflash/tiflash-supported-pushdown-calculations.md)のプッシュダウンをサポート

    -   `LEAD()`
    -   `LAG()`

-   軽量メタデータ ロックを提供して、DDL 変更時の DML 成功率を向上させます (実験的) [<a href="https://github.com/pingcap/tidb/issues/37275">#37275</a>](https://github.com/pingcap/tidb/issues/37275) @ [<a href="https://github.com/wjhuang2016">wjhuang2016</a>](https://github.com/wjhuang2016)

    TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータ オブジェクトの変更をサポートします。トランザクションが実行されると、トランザクションの開始時に対応するメタデータのスナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。この問題を解決するために、TiDB v6.3.0 ではオンライン DDL アルゴリズムに[<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)が導入されています。可能な限り DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、古いメタデータを持つ DML がコミットされるまで DDL の実行を待機させます。

-   インデックス追加のパフォーマンスを向上させ、DML トランザクションへの影響を軽減します (実験的) [<a href="https://github.com/pingcap/tidb/issues/35983">#35983</a>](https://github.com/pingcap/tidb/issues/35983) @ [<a href="https://github.com/benjamin2037">ベンジャミン2037</a>](https://github.com/benjamin2037)

    インデックス作成時のバックフィルの速度を向上させるために、TiDB v6.3.0 では、 [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">`tidb_ddl_enable_fast_reorg`</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)システム変数が有効な場合に`ADD INDEX`および`CREATE INDEX` DDL 操作が高速化されます。この機能を有効にすると、インデックス追加のパフォーマンスが約 3 倍になります。

### Security {#security}

-   TiKV は、保存時の暗号化のための SM4 アルゴリズムをサポートしています[<a href="https://github.com/tikv/tikv/issues/13041">#13041</a>](https://github.com/tikv/tikv/issues/13041) @ [<a href="https://github.com/jiayang-zheng">嘉陽鄭</a>](https://github.com/jiayang-zheng)

    保存時の TiKV 暗号化の場合は[<a href="/encryption-at-rest.md">SM4アルゴリズム</a>](/encryption-at-rest.md)を追加します。保存時の暗号化を構成する場合、構成`data-encryption-method`の値を`sm4-ctr`に設定することで SM4 暗号化容量を有効にできます。

-   TiDB は SM3 アルゴリズム[<a href="https://github.com/pingcap/tidb/issues/36192">#36192</a>](https://github.com/pingcap/tidb/issues/36192) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)による認証をサポートします

    TiDB は、SM3 アルゴリズムに基づいた認証プラグイン[<a href="/security-compatibility-with-mysql.md">`tidb_sm3_password`</a>](/security-compatibility-with-mysql.md)を追加します。このプラグインを有効にすると、ユーザー パスワードは SM3 アルゴリズムを使用して暗号化され、検証されます。

-   TiDB JDBC は、SM3 アルゴリズム[<a href="https://github.com/pingcap/mysql-connector-j/issues/25">#25</a>](https://github.com/pingcap/mysql-connector-j/issues/25) @ [<a href="https://github.com/lastincisor">最後切歯</a>](https://github.com/lastincisor)による認証をサポートします。

    ユーザー パスワードの認証には、クライアント側のサポートが必要です。 [<a href="/develop/dev-guide-choose-driver-or-orm.md#java-drivers">JDBC は SM3 アルゴリズムをサポートします</a>](/develop/dev-guide-choose-driver-or-orm.md#java-drivers)なので、TiDB-JDBC 経由で SM3 認証を使用して TiDB に接続できるようになりました。

### 可観測性 {#observability}

-   TiDB は、SQL クエリ実行時間[<a href="https://github.com/pingcap/tidb/issues/34106">#34106</a>](https://github.com/pingcap/tidb/issues/34106) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)の詳細なメトリクスを提供します。

    TiDB v6.3.0 は、 [<a href="/latency-breakdown.md">実行時間の詳細な観察</a>](/latency-breakdown.md)の詳細なデータ メトリックを提供します。完全でセグメント化されたメトリクスを通じて、SQL クエリの主な消費時間を明確に把握でき、主要な問題を迅速に見つけてトラブルシューティングの時間を節約できます。

-   遅いログと`TRACE`ステートメントの出力を強化[<a href="https://github.com/pingcap/tidb/issues/34106">#34106</a>](https://github.com/pingcap/tidb/issues/34106) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)

    TiDB v6.3.0 では、低速ログと`TRACE`の出力が強化されています。 TiDB の解析から KV RocksDB のディスクへの書き込みまでの[<a href="/latency-breakdown.md">フルリンク期間</a>](/latency-breakdown.md)の SQL クエリを観察でき、診断機能がさらに強化されます。

-   TiDB ダッシュボードはデッドロック履歴情報を提供します[<a href="https://github.com/pingcap/tidb/issues/34106">#34106</a>](https://github.com/pingcap/tidb/issues/34106) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)

    v6.3.0 以降、TiDB ダッシュボードはデッドロック履歴を提供します。 TiDB ダッシュボードで遅いログを確認し、一部の SQL ステートメントのロック待機時間が過度に長いことがわかった場合は、デッドロック履歴を確認して根本原因を特定できるため、診断が容易になります。

### パフォーマンス {#performance}

-   TiFlash はFastScan の使用方法を変更します (実験的) [<a href="https://github.com/pingcap/tiflash/issues/5252">#5252</a>](https://github.com/pingcap/tiflash/issues/5252) @ [<a href="https://github.com/hongyunyan">ホンユニャン</a>](https://github.com/hongyunyan)

    v6.2.0 では、 TiFlashに FastScan 機能が導入されており、期待されるパフォーマンスの向上が得られますが、使用上の柔軟性が欠けています。したがって、v6.3.0 では、 TiFlash はFastScan を有効または無効にする[<a href="/tiflash/use-fastscan.md">FastScanの使用方法</a>](/tiflash/use-fastscan.md) : `ALTER TABLE ... SET TIFLASH MODE ...`構文を変更し、非推奨になりました。代わりに、システム変数[<a href="/system-variables.md#tiflash_fastscan-new-in-v630">`tiflash_fastscan`</a>](/system-variables.md#tiflash_fastscan-new-in-v630)を使用して、FastScan を有効にするかどうかを簡単に制御できます。

    v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定は無効になりますが、データの通常の読み取りには影響しません。変数`tiflash_fastscan`を設定する必要があります。 v6.2.0 以前のバージョンから v6.3.0 にアップグレードする場合、データの整合性を維持するために、FastScan 機能はデフォルトではすべてのセッションで有効になりません。

-   TiFlash は、複数の同時実行タスク[<a href="https://github.com/pingcap/tiflash/issues/5376">#5376</a>](https://github.com/pingcap/tiflash/issues/5376) @ [<a href="https://github.com/JinheLin">ジンヘリン</a>](https://github.com/JinheLin)のシナリオでデータ スキャン パフォーマンスを最適化します。

    TiFlash は、同じデータの読み取り操作を組み合わせることで、同じデータの重複読み取りを削減します。リソースのオーバーヘッドと[<a href="/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file">同時タスクの場合のデータ スキャンのパフォーマンスが向上します。</a>](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file)を最適化します。複数の同時タスクの場合、各タスクが同じデータを個別に読み取る必要がある状況を回避し、同じデータを同時に複数読み取る可能性を回避します。

    この機能は v6.2.0 では実験的であり、v6.3.0 で GA になります。

-   TiFlash はデータ レプリケーション[<a href="https://github.com/pingcap/tiflash/issues/5237">#5237</a>](https://github.com/pingcap/tiflash/issues/5237) @ [<a href="https://github.com/breezewish">ブリーズウィッシュ</a>](https://github.com/breezewish)のパフォーマンスを向上させます

    TiFlash は、 TiKV からのデータ複製にRaftプロトコルを使用します。 v6.3.0 より前は、大量のレプリカ データを複製するのに長い時間がかかることがよくありました。 TiDB v6.3.0 は、 TiFlashデータ レプリケーション メカニズムを最適化し、レプリケーション速度を大幅に向上させます。 BRを使用してデータをリカバリしたり、 TiDB Lightningを使用してデータをインポートしたり、新しいTiFlashレプリカを追加したりすると、 TiFlashレプリカをより迅速にレプリケートできます。 TiFlashを使用すると、よりタイムリーにクエリを実行できます。さらに、 TiFlashレプリカの数をスケールアップ、スケールダウン、または変更するときに、 TiFlashレプリカはより速く安全でバランスの取れた状態に到達します。

-   TiFlash は、個々の`COUNT(DISTINCT)` [<a href="https://github.com/pingcap/tidb/issues/37202">#37202</a>](https://github.com/pingcap/tidb/issues/37202) @ [<a href="https://github.com/fixdb">修正データベース</a>](https://github.com/fixdb)の 3 段階の集約をサポートします

    TiFlash は、 `COUNT(DISTINCT)` 1 つだけ含むクエリの[<a href="/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630">3段階集計</a>](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)への書き換えをサポートしています。これにより、同時実行性とパフォーマンスが向上します。

-   TiKV はログのリサイクル[<a href="https://github.com/tikv/raft-engine/issues/214">#214</a>](https://github.com/tikv/raft-engine/issues/214) @ [<a href="https://github.com/LykxSassinator">リククスサシネーター</a>](https://github.com/LykxSassinator)をサポートします

    TiKV はRaft Engineの[<a href="/tikv-configuration-file.md#enable-log-recycle-new-in-v630">ログファイルのリサイクル</a>](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)をサポートします。これにより、 Raftログの追加中のネットワーク ディスクのロングテールレイテンシーが短縮され、書き込みワークロード時のパフォーマンスが向上します。

-   TiDB は null 対応アンチ結合[<a href="https://github.com/pingcap/tidb/issues/37525">#37525</a>](https://github.com/pingcap/tidb/issues/37525) @ [<a href="https://github.com/Arenatlx">アレナトゥス</a>](https://github.com/Arenatlx)をサポートします

    TiDB v6.3.0 では、新しい結合タイプ[<a href="/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries">Null 認識アンチ結合 (NAAJ)</a>](/explain-subqueries.md#null-aware-anti-semi-join-not-in-and--all-subqueries)が導入されています。 NAAJ は、コレクション操作を処理するときに、コレクションが空であるか`NULL`であるかを認識できます。これにより、 `IN`や`= ANY`などの操作の実行効率が最適化され、SQL のパフォーマンスが向上します。

-   ハッシュ結合[<a href="https://github.com/pingcap/tidb/issues/35439">#35439</a>](https://github.com/pingcap/tidb/issues/35439) @ [<a href="https://github.com/Reminiscent">懐かしい</a>](https://github.com/Reminiscent)のビルド終了を制御するオプティマイザー ヒントを追加します。

    v6.3.0 では、TiDB オプティマイザーは、ハッシュ結合、そのプローブ終了、およびビルド終了を指定するための 2 つのヒント`HASH_JOIN_BUILD()`と`HASH_JOIN_PROBE()`を導入します。オプティマイザーが最適な実行計画を選択できない場合、これらのヒントを使用して計画に介入できます。

-   セッションレベルの共通テーブル式 (CTE) インライン[<a href="https://github.com/pingcap/tidb/issues/36514">#36514</a>](https://github.com/pingcap/tidb/issues/36514) @ [<a href="https://github.com/elsa0520">エルサ0520</a>](https://github.com/elsa0520)をサポート

    TiDB v6.2.0 では、CTE インラインを可能にするオプティマイザーに`MERGE`ヒントが導入され、CTE クエリ結果のコンシューマがTiFlashで並列実行できるようになりました。 v6.3.0 では、セッション内で CTE インラインを許可するためにセッション変数[<a href="/system-variables.md#tidb_opt_force_inline_cte-new-in-v630">`tidb_opt_force_inline_cte`</a>](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)が導入されました。これにより、使いやすさが大幅に向上します。

### 取引 {#transactions}

-   悲観的トランザクション[<a href="https://github.com/pingcap/tidb/issues/36579">#36579</a>](https://github.com/pingcap/tidb/issues/36579) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)における一意制約のチェックの延期をサポート

    [<a href="/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630">`tidb_constraint_check_in_place_pessimistic`</a>](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630)システム変数を使用して、TiDB が悲観的トランザクションで[<a href="/constraints.md#pessimistic-transactions">固有の制約</a>](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御できます。この変数はデフォルトでは無効になっています。変数が有効になっている ( `ON`に設定されている) 場合、TiDB は必要になるまで悲観的トランザクションでのロック操作と一意の制約チェックを延期するため、一括 DML 操作のパフォーマンスが向上します。

-   Read-Committed 分離レベル[<a href="https://github.com/pingcap/tidb/issues/36812">#36812</a>](https://github.com/pingcap/tidb/issues/36812) @ [<a href="https://github.com/TonsnakeLin">トンスネークリン</a>](https://github.com/TonsnakeLin)で TSO をフェッチする方法を最適化します。

    Read-Committed 分離レベルでは、TSO のフェッチ方法を制御するためにシステム変数[<a href="/system-variables.md#tidb_rc_write_check_ts-new-in-v630">`tidb_rc_write_check_ts`</a>](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)が導入されています。プラン キャッシュ ヒットの場合、TiDB は TSO をフェッチする頻度を減らすことでバッチ DML ステートメントの実行効率を向上させ、バッチでタスクを実行する実行時間を短縮します。

### 安定性 {#stability}

-   リソースを消費するクエリが軽量クエリの応答時間に及ぼす影響を軽減します[<a href="https://github.com/tikv/tikv/issues/13313">#13313</a>](https://github.com/tikv/tikv/issues/13313) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv)

    リソースを消費するクエリと軽量のクエリが同時に実行されると、軽量のクエリの応答時間に影響します。この場合、トランザクション サービスの品質を確保するために、軽量のクエリが最初に TiDB によって処理されることが期待されます。 v6.3.0 では、TiKV は読み取りリクエストのスケジューリング メカニズムを最適化し、各ラウンドでのリソースを消費するクエリの実行時間が期待どおりになるようにします。これにより、リソースを消費するクエリが軽量クエリの応答時間に与える影響が大幅に軽減され、混合ワークロード シナリオで P99レイテンシーが 50% 以上削減されます。

-   統計が古くなった場合に統計をロードするデフォルトのポリシーを変更します[<a href="https://github.com/pingcap/tidb/issues/27601">#27601</a>](https://github.com/pingcap/tidb/issues/27601) @ [<a href="https://github.com/xuyifangreeneyes">シュイファングリーンアイズ</a>](https://github.com/xuyifangreeneyes)

    v5.3.0 では、TiDB は統計が古くなったときのオプティマイザーの動作を制御するシステム変数[<a href="/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530">`tidb_enable_pseudo_for_outdated_stats`</a>](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)を導入しました。デフォルト値は`ON`で、これは古いバージョンの動作を維持することを意味します。 SQL ステートメントに関係するオブジェクトの統計が古い場合、オプティマイザは統計 (テーブルの合計行数以外) が古いものであるとみなします。より信頼性が高く、代わりに疑似統計を使用します。実際のユーザー シナリオのテストと分析の後、v6.3.0 以降、デフォルト値の`tidb_enable_pseudo_for_outdated_stats`が`OFF`に変更されます。統計が古くなっても、オプティマイザはテーブル上の統計を引き続き使用するため、実行計画がより安定します。

-   Titan を無効化すると GA @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)になります

    オンライン TiKV ノードの場合は[<a href="/storage-engine/titan-configuration.md#disable-titan">タイタンを無効にする</a>](/storage-engine/titan-configuration.md#disable-titan)を行うことができます。

-   GlobalStats の準備ができていない場合は`static`パーティション プルーニングを使用する[<a href="https://github.com/pingcap/tidb/issues/37535">#37535</a>](https://github.com/pingcap/tidb/issues/37535) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)

    [<a href="/partitioned-table.md#dynamic-pruning-mode">`dynamic pruning`</a>](/partitioned-table.md#dynamic-pruning-mode)が有効な場合、オプティマイザは[<a href="/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode">グローバル統計</a>](/statistics.md#collect-statistics-of-partitioned-tables-in-dynamic-pruning-mode)に基づいて実行プランを選択します。 GlobalStats が完全に収集される前に、疑似統計を使用すると、パフォーマンスの低下が発生する可能性があります。 v6.3.0 では、GlobalStats が収集される前に動的プルーニングを有効にした場合、この問題は`static`モードを維持することで解決されます。 TiDB は、GlobalStats が収集されるまで`static`モードのままです。これにより、パーティション プルーニング設定を変更するときのパフォーマンスの安定性が確保されます。

### 使いやすさ {#ease-of-use}

-   SQL ベースのデータ配置ルールとTiFlashレプリカ間の競合に対処します[<a href="https://github.com/pingcap/tidb/issues/37171">#37171</a>](https://github.com/pingcap/tidb/issues/37171) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)

    TiDB v6.0.0 は、SQL ベースのデータ配置ルールを提供します。ただし、実装上の問題により、この機能はTiFlashレプリカと競合します。 TiDB v6.3.0 は実装メカニズムを最適化します[<a href="/placement-rules-in-sql.md#known-limitations">SQL ベースのデータ配置ルールとTiFlashの間の競合を解決します。</a>](/placement-rules-in-sql.md#known-limitations) .

### MySQLの互換性 {#mysql-compatibility}

-   4 つの正規表現関数( `REGEXP_INSTR()` `REGEXP_REPLACE()`および`REGEXP_SUBSTR()` [<a href="https://github.com/pingcap/tidb/issues/23881">#23881</a>](https://github.com/pingcap/tidb/issues/23881) @ [<a href="https://github.com/windtalker">ウィンドトーカー</a>](https://github.com/windtalker)のサポート`REGEXP_LIKE()`追加することにより、MySQL 8.0 の互換性が向上しました。

    MySQL との互換性の詳細については、 [<a href="/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql">MySQL との正規表現の互換性</a>](/functions-and-operators/string-functions.md#regular-expression-compatibility-with-mysql)を参照してください。

-   `CREATE USER`および`ALTER USER`ステートメントは、 `ACCOUNT LOCK/UNLOCK`オプション[<a href="https://github.com/pingcap/tidb/issues/37051">#37051</a>](https://github.com/pingcap/tidb/issues/37051) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)をサポートします。

    [<a href="/sql-statements/sql-statement-create-user.md">`CREATE USER`</a>](/sql-statements/sql-statement-create-user.md)ステートメントを使用してユーザーを作成する場合、 `ACCOUNT LOCK/UNLOCK`オプションを使用して、作成したユーザーをロックするかどうかを指定できます。ロックされたユーザーはデータベースにログインできません。

    [<a href="/sql-statements/sql-statement-alter-user.md">`ALTER USER`</a>](/sql-statements/sql-statement-alter-user.md)ステートメントの`ACCOUNT LOCK/UNLOCK`オプションを使用して、既存のユーザーのロック状態を変更できます。

-   JSON データ型と JSON関数はGA [<a href="https://github.com/pingcap/tidb/issues/36993">#36993</a>](https://github.com/pingcap/tidb/issues/36993) @ [<a href="https://github.com/xiongjiwei">ションジウェイ</a>](https://github.com/xiongjiwei)になります

    JSON は、多くのプログラムで採用されている一般的なデータ形式です。 TiDB は、以前のバージョンから実験的機能として[<a href="/data-type-json.md">JSONのサポート</a>](/data-type-json.md)を導入しており、MySQL の JSON データ型および一部の JSON関数と互換性があります。

    TiDB v6.3.0 では、JSON データ型と関数がGA になり、TiDB のデータ型が強化され、 [<a href="/sql-statements/sql-statement-create-index.md#expression-index">式インデックス</a>](/sql-statements/sql-statement-create-index.md#expression-index)と[<a href="/generated-columns.md">生成された列</a>](/generated-columns.md)での JSON関数の使用がサポートされ、TiDB と MySQL の互換性がさらに向上しました。

### バックアップと復元 {#backup-and-restore}

-   PITR はバックアップ ストレージとして[<a href="/br/backup-and-restore-storages.md">GCS と Azure Blob Storage</a>](/br/backup-and-restore-storages.md) @ [<a href="https://github.com/joccau">ジョッカウ</a>](https://github.com/joccau)をサポートします

    TiDB クラスターが Google Cloud または Azure にデプロイされている場合は、クラスターを v6.3.0 にアップグレードした後に PITR 機能を使用できます。

-   BR はAWS S3 オブジェクト ロック[<a href="https://github.com/tikv/tikv/issues/13442">#13442</a>](https://github.com/tikv/tikv/issues/13442) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)をサポートします

    [<a href="https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html">S3 オブジェクトロック</a>](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)を有効にすることで、AWS 上のバックアップ データが改ざんまたは削除されないように保護できます。

### データ移行 {#data-migration}

-   TiDB Lightning は[<a href="/tidb-lightning/tidb-lightning-data-source.md#parquet">Apache Hive によってエクスポートされた Parquet ファイルを TiDB にインポート</a>](/tidb-lightning/tidb-lightning-data-source.md#parquet) [<a href="https://github.com/pingcap/tidb/issues/37536">#37536</a>](https://github.com/pingcap/tidb/issues/37536) @ [<a href="https://github.com/buchuitoudegou">ブチュイトデゴウ</a>](https://github.com/buchuitoudegou)をサポートします

-   DM は新しい構成アイテムを追加します`safe-mode-duration` [<a href="https://github.com/pingcap/tiflow/issues/6224">#6224</a>](https://github.com/pingcap/tiflow/issues/6224) @ [<a href="https://github.com/okJiang">オクジャン</a>](https://github.com/okJiang)

    この設定項目は[<a href="/dm/task-configuration-file-full.md">タスク構成ファイル</a>](/dm/task-configuration-file-full.md)に追加されます。 DM が異常終了した後の自動セーフ モードの継続時間を調整できます。デフォルト値は 60 秒です。 `safe-mode-duration`が`"0s"`に設定されている場合、異常な再起動後に DM がセーフ モードに入ろうとするとエラーが報告されます。

### TiDB データ共有サブスクリプション {#tidb-data-share-subscription}

-   TiCDC は、地理的に分散された複数のデータ ソース[<a href="https://github.com/pingcap/tiflow/issues/5301">#5301</a>](https://github.com/pingcap/tiflow/issues/5301) @ [<a href="https://github.com/sdojjy">スドジ</a>](https://github.com/sdojjy)からデータを複製できる展開トポロジをサポートします。

    v6.3.0 以降、単一の TiDB クラスターから複数の地理的に分散されたデータ システムへのデータの複製をサポートするには、IDC ごとにデータを複製する必要が[<a href="/ticdc/deploy-ticdc.md">TiCDC を複数の IDC に導入できます</a>](/ticdc/deploy-ticdc.md)ます。この機能は、地理的に分散されたデータ レプリケーションおよび展開トポロジの機能を提供するのに役立ちます。

-   TiCDC は、アップストリームとダウンストリーム (同期ポイント) [<a href="https://github.com/pingcap/tiflow/issues/6977">#6977</a>](https://github.com/pingcap/tiflow/issues/6977) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)の間でスナップショットの一貫性を維持することをサポートします。

    ディザスター リカバリーのためのデータ レプリケーションのシナリオでは、ダウンストリーム スナップショットがアップストリーム スナップショットと一致するように、TiCDC は[<a href="/sync-diff-inspector/upstream-downstream-diff.md#data-check-for-tidb-upstream-and-downstream-clusters">ダウンストリームデータのスナップショットを定期的に維持する</a>](/sync-diff-inspector/upstream-downstream-diff.md#data-check-for-tidb-upstream-and-downstream-clusters)をサポートします。この機能により、TiCDC は読み取りと書き込みが分離されるシナリオをより適切にサポートし、コストの削減に役立ちます。

-   TiCDC はグレースフル アップグレード[<a href="https://github.com/pingcap/tiflow/issues/4757">#4757</a>](https://github.com/pingcap/tiflow/issues/4757) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus) @ [<a href="https://github.com/3AceShowHand">3エースショーハンド</a>](https://github.com/3AceShowHand)をサポートします

    TiCDC が[<a href="/ticdc/deploy-ticdc.md#upgrade-cautions">TiUP</a>](/ticdc/deploy-ticdc.md#upgrade-cautions) (&gt;=v1.11.0) または[<a href="https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster">TiDB Operator</a>](https://docs.pingcap.com/tidb-in-kubernetes/v1.3/configure-a-tidb-cluster#configure-graceful-upgrade-for-ticdc-cluster) (&gt;=v1.3.8) を使用してデプロイされている場合、TiCDC クラスターを正常にアップグレードできます。アップグレード中のデータ レプリケーションのレイテンシーは30 秒程度に抑えられます。これにより安定性が向上し、TiCDC がレイテンシの影響を受けやすいアプリケーションをより適切にサポートできるようになります。

## 互換性の変更 {#compatibility-changes}

### システム変数 {#system-variables}

| 変数名                                                                                                                                                                                                                   | 種類の変更    | 説明                                                                                                                                                                                                                                               |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [<a href="/system-variables.md#default_authentication_plugin">`default_authentication_plugin`</a>](/system-variables.md#default_authentication_plugin)                                                                | 修正済み     | 新しいオプション`tidb_sm3_password`を追加します。この変数を`tidb_sm3_password`に設定すると、暗号化アルゴリズムとして SM3 が使用されます。                                                                                                                                                       |
| [<a href="/system-variables.md#sql_require_primary_key-new-in-v630">`sql_require_primary_key`</a>](/system-variables.md#sql_require_primary_key-new-in-v630)                                                          | 新しく追加された | テーブルに主キーがあるという要件を強制するかどうかを制御します。この変数を有効にした後、主キーなしでテーブルを作成または変更しようとすると、エラーが発生します。                                                                                                                                                                 |
| [<a href="/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630">`tidb_adaptive_closest_read_threshold`</a>](/system-variables.md#tidb_adaptive_closest_read_threshold-new-in-v630)                   | 新しく追加された | [<a href="/system-variables.md#tidb_replica_read-new-in-v40">`tidb_replica_read`</a>](/system-variables.md#tidb_replica_read-new-in-v40)が`closest-adaptive`に設定されている場合、TiDBサーバーがTiDBサーバーと同じリージョン内のレプリカに読み取りリクエストを送信することを優先するしきい値を制御します。           |
| [<a href="/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630">`tidb_constraint_check_in_place_pessimistic`</a>](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) | 新しく追加された | TiDB が悲観的トランザクションで[<a href="/constraints.md#pessimistic-transactions">固有の制約</a>](/constraints.md#pessimistic-transactions)をチェックするタイミングを制御します。                                                                                                    |
| [<a href="/system-variables.md#tidb_ddl_disk_quota-new-in-v630">`tidb_ddl_disk_quota`</a>](/system-variables.md#tidb_ddl_disk_quota-new-in-v630)                                                                      | 新しく追加された | [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">`tidb_ddl_enable_fast_reorg`</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)が有効な場合にのみ有効になります。インデックス作成時のバックフィル中のローカルstorageの使用制限を設定します。                  |
| [<a href="/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630">`tidb_ddl_enable_fast_reorg`</a>](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)                                                 | 新しく追加された | インデックス作成時のバックフィルの速度を向上させるために、 `ADD INDEX`および`CREATE INDEX` DDL 操作の高速化を有効にするかどうかを制御します。                                                                                                                                                           |
| [<a href="/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630">`tidb_ddl_flashback_concurrency`</a>](/system-variables.md#tidb_ddl_flashback_concurrency-new-in-v630)                                     | 新しく追加された | `flashback cluster`の同時実行性を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                     |
| [<a href="/system-variables.md#tidb_enable_exchange_partition">`tidb_enable_exchange_partition`</a>](/system-variables.md#tidb_enable_exchange_partition)                                                             | 廃止されました  | [<a href="/partitioned-table.md#partition-management">`exchange partitions with tables`</a>](/partitioned-table.md#partition-management)機能を有効にするかどうかを制御します。デフォルト値は`ON`です。つまり、デフォルトで`exchange partitions with tables`が有効になります。                    |
| [<a href="/system-variables.md#tidb_enable_foreign_key-new-in-v630">`tidb_enable_foreign_key`</a>](/system-variables.md#tidb_enable_foreign_key-new-in-v630)                                                          | 新しく追加された | `FOREIGN KEY`機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                     |
| `tidb_enable_general_plan_cache`                                                                                                                                                                                      | 新しく追加された | 一般プラン キャッシュ機能を有効にするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                                       |
| [<a href="/system-variables.md#tidb_enable_metadata_lock-new-in-v630">`tidb_enable_metadata_lock`</a>](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)                                                    | 新しく追加された | [<a href="/metadata-lock.md">メタデータロック</a>](/metadata-lock.md)機能を有効にするかどうかを指定します。                                                                                                                                                                 |
| [<a href="/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630">`tidb_enable_null_aware_anti_join`</a>](/system-variables.md#tidb_enable_null_aware_anti_join-new-in-v630)                               | 新しく追加された | 特別な集合演算子`NOT IN`および`!= ALL`によって導かれるサブクエリによってアンチ結合が生成される場合に、TiDB が Null-Aware Hash Join を適用するかどうかを制御します。                                                                                                                                          |
| [<a href="/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530">`tidb_enable_pseudo_for_outdated_stats`</a>](/system-variables.md#tidb_enable_pseudo_for_outdated_stats-new-in-v530)                | 修正済み     | 統計が古い場合に、テーブルの統計を使用する際のオプティマイザーの動作を制御します。デフォルト値は`ON`から`OFF`に変更されます。これは、このテーブルの統計が古くても、オプティマイザはテーブルの統計を引き続き使用することを意味します。                                                                                                                          |
| [<a href="/system-variables.md#tidb_enable_rate_limit_action">`tidb_enable_rate_limit_action`</a>](/system-variables.md#tidb_enable_rate_limit_action)                                                                | 修正済み     | データを読み取るオペレータの動的メモリ制御機能を有効にするかどうかを制御します。この変数が`ON`に設定されている場合、メモリ使用量は[<a href="/system-variables.md#tidb_mem_quota_query">`tidb_mem_quota_query`</a>](/system-variables.md#tidb_mem_quota_query)の制御下にない可能性があります。したがって、デフォルト値は`ON`から`OFF`に変更されます。   |
| [<a href="/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630">`tidb_enable_tiflash_read_for_write_stmt`</a>](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630)          | 新しく追加された | SQL 書き込みステートメントの読み取りリクエストをTiFlashにプッシュダウンするかどうかを制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                               |
| [<a href="/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630">`tidb_enable_unsafe_substitute`</a>](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                                        | 新しく追加された | 式を安全でない方法で生成された列に置き換えるかどうかを制御します。                                                                                                                                                                                                                |
| `tidb_general_plan_cache_size`                                                                                                                                                                                        | 新しく追加された | 一般プラン キャッシュによってキャッシュできる実行プランの最大数を制御します。この変数によって制御される機能は、TiDB v6.3.0 では完全には機能しません。デフォルト値を変更しないでください。                                                                                                                                              |
| [<a href="/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630">`tidb_last_plan_replayer_token`</a>](/system-variables.md#tidb_enable_unsafe_substitute-new-in-v630)                                        | 新しく追加された | 読み取り専用で、現在のセッションの最後の`PLAN REPLAYER DUMP`の実行結果を取得するために使用されます。                                                                                                                                                                                     |
| [<a href="/system-variables.md#tidb_max_paging_size-new-in-v630">tidb_max_paging_size</a>](/system-variables.md#tidb_max_paging_size-new-in-v630)                                                                     | 新しく追加された | この変数は、コプロセッサーのページング要求プロセス中に最小行数を設定するために使用されます。                                                                                                                                                                                                   |
| [<a href="/system-variables.md#tidb_opt_force_inline_cte-new-in-v630">`tidb_opt_force_inline_cte`</a>](/system-variables.md#tidb_opt_force_inline_cte-new-in-v630)                                                    | 新しく追加された | セッション全体の共通テーブル式 (CTE) をインライン化するかどうかを制御します。デフォルト値は`OFF`です。これは、CTE のインライン化がデフォルトでは強制されないことを意味します。                                                                                                                                                  |
| [<a href="/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630">`tidb_opt_three_stage_distinct_agg`</a>](/system-variables.md#tidb_opt_three_stage_distinct_agg-new-in-v630)                            | 新しく追加された | MPP モードで`COUNT(DISTINCT)`集計を 3 段階の集計に書き換えるかどうかを指定します。デフォルト値は`ON`です。                                                                                                                                                                              |
| [<a href="/system-variables.md#tidb_partition_prune_mode-new-in-v51">`tidb_partition_prune_mode`</a>](/system-variables.md#tidb_partition_prune_mode-new-in-v51)                                                      | 修正済み     | 動的プルーニングを有効にするかどうかを指定します。 v6.3.0 以降、デフォルト値は`dynamic`に変更されます。                                                                                                                                                                                     |
| [<a href="/system-variables.md#tidb_rc_read_check_ts-new-in-v600">`tidb_rc_read_check_ts`</a>](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)                                                                | 修正済み     | タイムスタンプの取得を最適化するために使用されます。これは、読み取りと書き込みの競合がまれな読み取りコミット分離レベルのシナリオに適しています。この機能は特定のサービス ワークロードを対象としているため、他のシナリオではパフォーマンスの低下を引き起こす可能性があります。このため、v6.3.0 以降、この変数のスコープは`GLOBAL \| SESSION`から`INSTANCE`に変更されます。つまり、特定の TiDB インスタンスに対してこの機能を有効にすることができます。 |
| [<a href="/system-variables.md#tidb_rc_write_check_ts-new-in-v630">`tidb_rc_write_check_ts`</a>](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)                                                             | 新しく追加された | タイムスタンプの取得を最適化するために使用され、悲観的トランザクションの RC 分離レベルでポイント書き込み競合がほとんどないシナリオに適しています。この変数を有効にすると、point-write ステートメントの実行中にグローバル タイムスタンプを取得することによってもたらされるレイテンシーとオーバーヘッドを回避できます。                                                                              |
| [<a href="/system-variables.md#tiflash_fastscan-new-in-v630">`tiflash_fastscan`</a>](/system-variables.md#tiflash_fastscan-new-in-v630)                                                                               | 新しく追加された | FastScan を有効にするかどうかを制御します。 [<a href="/tiflash/use-fastscan.md">ファストスキャン</a>](/tiflash/use-fastscan.md)が有効になっている ( `ON`に設定されている) 場合、 TiFlash はより効率的なクエリ パフォーマンスを提供しますが、クエリ結果の精度やデータの一貫性は保証されません。                                                  |

### コンフィグレーションファイルのパラメータ {#configuration-file-parameters}

| コンフィグレーションファイル | コンフィグレーション                                                                                                                                                                                        | 種類の変更    | 説明                                                                                                                                                                                                                                                                                               |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TiDB           | [<a href="/tidb-configuration-file.md#temp-dir-new-in-v630">`temp-dir`</a>](/tidb-configuration-file.md#temp-dir-new-in-v630)                                                                     | 新しく追加された | TiDB が一時データを保存するために使用するファイル システムの場所を指定します。機能が TiDB ノードのローカルstorageを必要とする場合、TiDB は対応する一時データをこの場所に保存します。デフォルト値は`/tmp/tidb`です。                                                                                                                                                                      |
| TiKV           | [<a href="/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630">`auto-adjust-pool-size`</a>](/tikv-configuration-file.md#auto-adjust-pool-size-new-in-v630)                              | 新しく追加された | スレッド プール サイズを自動的に調整するかどうかを制御します。有効にすると、現在の CPU 使用率に基づいて UnifyReadPool スレッド プール サイズを自動的に調整することで、TiKV の読み取りパフォーマンスが最適化されます。                                                                                                                                                                        |
| TiKV           | [<a href="/tikv-configuration-file.md#data-encryption-method">`data-encryption-method`</a>](/tikv-configuration-file.md#data-encryption-method)                                                   | 修正済み     | 新しい値のオプション`sm4-ctr`を導入します。この設定項目を`sm4-ctr`に設定すると、データは SM4 を使用して暗号化されて保存されます。                                                                                                                                                                                                                     |
| TiKV           | [<a href="/tikv-configuration-file.md#enable-log-recycle-new-in-v630">`enable-log-recycle`</a>](/tikv-configuration-file.md#enable-log-recycle-new-in-v630)                                       | 新しく追加された | Raft Engineで古いログ ファイルをリサイクルするかどうかを決定します。これを有効にすると、論理的にパージされたログ ファイルがリサイクル用に予約されます。これにより、書き込みワークロードのロングテールレイテンシーが短縮されます。この設定項目は、 [<a href="/tikv-configuration-file.md#format-version-new-in-v630">フォーマットバージョン</a>](/tikv-configuration-file.md#format-version-new-in-v630) &gt;= 2 の場合にのみ使用できます。 |
| TiKV           | [<a href="/tikv-configuration-file.md#format-version-new-in-v630">`format-version`</a>](/tikv-configuration-file.md#format-version-new-in-v630)                                                   | 新しく追加された | Raft Engineのログ ファイルのバージョンを指定します。 v6.3.0 より前の TiKV のデフォルトのログ ファイル バージョンは`1`です。ログ ファイルは TiKV v6.1.0 以上で読み取ることができます。 TiKV v6.3.0 以降のデフォルトのログ ファイル バージョンは`2`です。 TiKV v6.3.0 以降では、ログ ファイルを読み取ることができます。                                                                                                |
| TiKV           | [<a href="/tikv-configuration-file.md#enable-new-in-v620">`log-backup.enable`</a>](/tikv-configuration-file.md#enable-new-in-v620)                                                                | 修正済み     | v6.3.0 以降、デフォルト値は`false`から`true`に変更されます。                                                                                                                                                                                                                                                         |
| TiKV           | [<a href="/tikv-configuration-file.md#max-flush-interval-new-in-v620">`log-backup.max-flush-interval`</a>](/tikv-configuration-file.md#max-flush-interval-new-in-v620)                            | 修正済み     | v6.3.0 以降、デフォルト値は`5min`から`3min`に変更されます。                                                                                                                                                                                                                                                          |
| PD             | [<a href="/pd-configuration-file.md#enable-diagnostic-new-in-v630">診断を有効にする</a>](/pd-configuration-file.md#enable-diagnostic-new-in-v630)                                                         | 新しく追加された | 診断機能を有効にするかどうかを制御します。デフォルト値は`false`です。                                                                                                                                                                                                                                                           |
| TiFlash        | [<a href="/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file">`dt_enable_read_thread`</a>](/tiflash/tiflash-configuration.md#configure-the-tiflash-learnertoml-file)        | 廃止されました  | v6.3.0 以降、この設定項目は非推奨になりました。スレッド プールは、デフォルトでstorageエンジンからの読み取りリクエストを処理するために使用され、無効にすることはできません。                                                                                                                                                                                                    |
| DM             | [<a href="/dm/task-configuration-file-full.md#task-configuration-file-template-advanced">`safe-mode-duration`</a>](/dm/task-configuration-file-full.md#task-configuration-file-template-advanced) | 新しく追加された | 自動セーフモードの継続時間を指定します。                                                                                                                                                                                                                                                                             |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`enable-sync-point`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                  | 新しく追加された | 同期ポイント機能を有効にするかどうかを指定します。                                                                                                                                                                                                                                                                        |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sync-point-interval`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)                | 新しく追加された | Syncpoint がアップストリームとダウンストリームのスナップショットを調整する間隔を指定します。                                                                                                                                                                                                                                              |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters">`sync-point-retention`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)               | 新しく追加された | 同期ポイントによってダウンストリーム テーブルにデータが保持される期間を指定します。この期間を超えると、データはクリーンアップされます。                                                                                                                                                                                                                             |
| TiCDC          | [<a href="/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters">`sink-uri.memory`</a>](/ticdc/ticdc-changefeed-config.md#changefeed-cli-parameters)                                        | 廃止されました  | `memory`ソートは非推奨になりました。いかなる状況でも使用することはお勧めできません。                                                                                                                                                                                                                                                   |

### その他 {#others}

-   ログ バックアップは、バックアップstorageとして GCS および Azure Blob Storage をサポートします。
-   ログ バックアップが`exchange partition` DDL と互換性を持つようになりました。
-   以前[<a href="/tiflash/use-fastscan.md">高速スキャン</a>](/tiflash/use-fastscan.md)有効にするために使用されていた SQL ステートメント`ALTER TABLE ...SET TiFLASH MODE ...`非推奨になり、システム変数[<a href="/system-variables.md#tiflash_fastscan-new-in-v630">`tiflash_fastscan`</a>](/system-variables.md#tiflash_fastscan-new-in-v630)に置き換えられます。 v6.2.0 から v6.3.0 にアップグレードすると、v6.2.0 のすべての FastScan 設定は無効になりますが、データの通常の読み取りには影響しません。この場合、変数[<a href="/system-variables.md#tiflash_fastscan-new-in-v630">`tiflash_fastscan`</a>](/system-variables.md#tiflash_fastscan-new-in-v630)を設定して FastScan を有効または無効にする必要があります。以前のバージョンから v6.3.0 にアップグレードする場合、データの一貫性を保つために、すべてのセッションに対して FastScan 機能がデフォルトで有効になりません。
-   Linux AMD64アーキテクチャでTiFlashを導入するには、CPU が AVX2 命令セットをサポートしている必要があります。 `cat /proc/cpuinfo | grep avx2`に出力があることを確認します。 Linux ARM64アーキテクチャでTiFlashを導入するには、CPU が ARMv8 命令セットアーキテクチャをサポートしている必要があります。 `cat /proc/cpuinfo | grep 'crc32' | grep 'asimd'`に出力があることを確認します。命令セット拡張を使用することにより、TiFlash のベクトル化エンジンはより優れたパフォーマンスを実現できます。
-   TiDB で動作する HAProxy の最小バージョンは v1.5 になりました。 v1.5 と v2.1 の間の HAProxy バージョンでは、 `post-41`構成オプションを`mysql-check`に設定する必要があります。 HAProxy v2.2 以降を使用することをお勧めします。

## 削除された機能 {#removed-feature}

v6.3.0 以降、TiCDC は Pulsar シンクの構成をサポートしなくなりました。 StreamNative が提供する[<a href="https://github.com/streamnative/kop">コップ</a>](https://github.com/streamnative/kop)代替として使用できます。

## 改善点 {#improvements}

-   TiDB

    -   TiDB は、テーブルの存在をチェックするときにターゲット テーブル名の大文字と小文字を区別しないようになりました[<a href="https://github.com/pingcap/tidb/issues/34610">#34610</a>](https://github.com/pingcap/tidb/issues/34610) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)
    -   `init_connect` [<a href="https://github.com/pingcap/tidb/issues/35324">#35324</a>](https://github.com/pingcap/tidb/issues/35324) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)の値を設定するときに解析チェックを追加することで、MySQL の互換性を向上させます。
    -   新しい接続に対して生成されるログ警告を改善[<a href="https://github.com/pingcap/tidb/issues/34964">#34964</a>](https://github.com/pingcap/tidb/issues/34964) @ [<a href="https://github.com/xiongjiwei">ションジウェイ</a>](https://github.com/xiongjiwei)
    -   DDL 履歴ジョブをクエリするための HTTP API を最適化し、 `start_job_id`パラメーター[<a href="https://github.com/pingcap/tidb/issues/35838">#35838</a>](https://github.com/pingcap/tidb/issues/35838) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)のサポートを追加します。
    -   JSON パスの構文が間違っている場合にエラーを報告する[<a href="https://github.com/pingcap/tidb/issues/22525">#22525</a>](https://github.com/pingcap/tidb/issues/22525) [<a href="https://github.com/pingcap/tidb/issues/34959">#34959</a>](https://github.com/pingcap/tidb/issues/34959) @ [<a href="https://github.com/xiongjiwei">ションジウェイ</a>](https://github.com/xiongjiwei)
    -   偽共有の問題[<a href="https://github.com/pingcap/tidb/issues/37641">#37641</a>](https://github.com/pingcap/tidb/issues/37641) @ [<a href="https://github.com/gengliqi">ゲンリチ</a>](https://github.com/gengliqi)を修正して、結合操作のパフォーマンスを向上させます。
    -   [<a href="/sql-plan-replayer.md">`PLAN REPLAYER`</a>](/sql-plan-replayer.md)を使用して一度に複数の SQL ステートメントの実行計画情報をエクスポートすることをサポートします。これにより、トラブルシューティングがより効率的になります[<a href="https://github.com/pingcap/tidb/issues/37798">#37798</a>](https://github.com/pingcap/tidb/issues/37798) @ [<a href="https://github.com/Yisaer">イーサール</a>](https://github.com/Yisaer)

-   TiKV

    -   1 つのピアが到達不能になった後にRaftstore が大量のメッセージをブロードキャストすることを避けるための`unreachable_backoff`項目の設定をサポート[<a href="https://github.com/tikv/tikv/issues/13054">#13054</a>](https://github.com/tikv/tikv/issues/13054) @ [<a href="https://github.com/5kbpers">5kbps</a>](https://github.com/5kbpers)
    -   TSO サービス[<a href="https://github.com/tikv/tikv/issues/12794">#12794</a>](https://github.com/tikv/tikv/issues/12794) @ [<a href="https://github.com/pingyu">ピンギュ</a>](https://github.com/pingyu)のフォールト トレランスを向上します。
    -   RocksDB で同時に実行されるサブコンパクション操作の数の動的変更をサポート ( `rocksdb.max-sub-compactions` ) [<a href="https://github.com/tikv/tikv/issues/13145">#13145</a>](https://github.com/tikv/tikv/issues/13145) @ [<a href="https://github.com/ethercflow">エーテルフロー</a>](https://github.com/ethercflow)
    -   空のリージョン[<a href="https://github.com/tikv/tikv/issues/12421">#12421</a>](https://github.com/tikv/tikv/issues/12421) @ [<a href="https://github.com/tabokie">タボキー</a>](https://github.com/tabokie)をマージするパフォーマンスを最適化します。
    -   より多くの正規表現関数をサポート[<a href="https://github.com/tikv/tikv/issues/13483">#13483</a>](https://github.com/tikv/tikv/issues/13483) @ [<a href="https://github.com/gengliqi">ゲンリチ</a>](https://github.com/gengliqi)
    -   CPU 使用率[<a href="https://github.com/tikv/tikv/issues/13313">#13313</a>](https://github.com/tikv/tikv/issues/13313) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv)に基づいてスレッド プール サイズを自動的に調整するサポート

-   PD

    -   TiDB ダッシュボード[<a href="https://github.com/tikv/pd/issues/5366">#5366</a>](https://github.com/tikv/pd/issues/5366) @ [<a href="https://github.com/YiniXu9506">イニシュ9506</a>](https://github.com/YiniXu9506)での TiKV IO MBps メトリクスのクエリを改善しました。
    -   TiDB ダッシュボードの URL を`metrics`から`monitoring` [<a href="https://github.com/tikv/pd/issues/5366">#5366</a>](https://github.com/tikv/pd/issues/5366) @ [<a href="https://github.com/YiniXu9506">イニシュ9506</a>](https://github.com/YiniXu9506)に変更します。

-   TiFlash

    -   `elt`機能をTiFlash [<a href="https://github.com/pingcap/tiflash/issues/5104">#5104</a>](https://github.com/pingcap/tiflash/issues/5104) @ [<a href="https://github.com/Willendless">ウィレンドレス</a>](https://github.com/Willendless)にプッシュダウンするサポート
    -   `leftShift`機能をTiFlash [<a href="https://github.com/pingcap/tiflash/issues/5099">#5099</a>](https://github.com/pingcap/tiflash/issues/5099) @ [<a href="https://github.com/AnnieoftheStars">アニー・オブ・ザ・スターズ</a>](https://github.com/AnnieoftheStars)にプッシュダウンするサポート
    -   `castTimeAsDuration`機能をTiFlash [<a href="https://github.com/pingcap/tiflash/issues/5306">#5306</a>](https://github.com/pingcap/tiflash/issues/5306) @ [<a href="https://github.com/AntiTopQuark">アンチトップクワーク</a>](https://github.com/AntiTopQuark)にプッシュダウンするサポート
    -   `HexIntArg/HexStrArg`機能をTiFlash [<a href="https://github.com/pingcap/tiflash/issues/5107">#5107</a>](https://github.com/pingcap/tiflash/issues/5107) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)にプッシュダウンするサポート
    -   TiFlash のインタープリタをリファクタリングし、新しいインタープリタ Planner [<a href="https://github.com/pingcap/tiflash/issues/4739">#4739</a>](https://github.com/pingcap/tiflash/issues/4739) @ [<a href="https://github.com/SeaRise">シーライズ</a>](https://github.com/SeaRise)をサポートします。
    -   TiFlash [<a href="https://github.com/pingcap/tiflash/issues/5609">#5609</a>](https://github.com/pingcap/tiflash/issues/5609) @ [<a href="https://github.com/bestwoody">ベストウッディ</a>](https://github.com/bestwoody)のメモリトラッカーの精度を向上
    -   `UTF8_BIN/ASCII_BIN/LATIN1_BIN/UTF8MB4_BIN`照合順序[<a href="https://github.com/pingcap/tiflash/issues/5294">#5294</a>](https://github.com/pingcap/tiflash/issues/5294) @ [<a href="https://github.com/solotzg">ソロッツグ</a>](https://github.com/solotzg)を使用して文字列列のパフォーマンスを向上させます。
    -   ReadLimiter [<a href="https://github.com/pingcap/tiflash/issues/5401">#5401</a>](https://github.com/pingcap/tiflash/issues/5401) 、 [<a href="https://github.com/pingcap/tiflash/issues/5091">#5091</a>](https://github.com/pingcap/tiflash/issues/5091) @ [<a href="https://github.com/Lloyd-Pottiger">ロイド・ポティガー</a>](https://github.com/Lloyd-Pottiger)でバックグラウンドで I/O スループットを計算します。

-   ツール

    -   バックアップと復元 (BR)

        -   PITR はログ バックアップで生成された小さなファイルをマージできるため、バックアップ ファイルの数が大幅に削減されます[<a href="https://github.com/tikv/tikv/issues/13232">#13232</a>](https://github.com/tikv/tikv/issues/13232) @ [<a href="https://github.com/Leavrth">レヴルス</a>](https://github.com/Leavrth)
        -   PITR は、復元後のアップストリーム クラスター構成に基づいたTiFlashレプリカの数の自動構成をサポートします[<a href="https://github.com/pingcap/tidb/issues/37208">#37208</a>](https://github.com/pingcap/tidb/issues/37208) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)

    -   TiCDC

        -   アップストリームの TiDB [<a href="https://github.com/pingcap/tiflow/issues/6506">#6506</a>](https://github.com/pingcap/tiflow/issues/6506) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)で導入された同時 DDL フレームワークと TiCDC の互換性を向上させます。
        -   MySQL シンクでエラー[<a href="https://github.com/pingcap/tiflow/issues/6460">#6460</a>](https://github.com/pingcap/tiflow/issues/6460) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)が発生した場合の DML ステートメントのロギング`start ts`をサポートします。
        -   `api/v1/health` API を強化して、TiCDC クラスターのより正確な正常性状態を返す[<a href="https://github.com/pingcap/tiflow/issues/4757">#4757</a>](https://github.com/pingcap/tiflow/issues/4757) @ [<a href="https://github.com/overvenus">オーバーヴィーナス</a>](https://github.com/overvenus)
        -   MQ シンクと MySQL シンクを非同期モードで実装して、シンクのスループットを向上させます[<a href="https://github.com/pingcap/tiflow/issues/5928">#5928</a>](https://github.com/pingcap/tiflow/issues/5928) @ [<a href="https://github.com/hicqu">ひっくり返る</a>](https://github.com/hicqu) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)
        -   非推奨のパルサー シンク[<a href="https://github.com/pingcap/tiflow/issues/7087">#7087</a>](https://github.com/pingcap/tiflow/issues/7087) @ [<a href="https://github.com/hi-rustin">こんにちはラスティン</a>](https://github.com/hi-rustin)を削除します。
        -   変更フィードに無関係な DDL ステートメントを破棄することで、レプリケーションのパフォーマンスを向上させます[<a href="https://github.com/pingcap/tiflow/issues/6447">#6447</a>](https://github.com/pingcap/tiflow/issues/6447) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)

    -   TiDB データ移行 (DM)

        -   データソース[<a href="https://github.com/pingcap/tiflow/issues/6448">#6448</a>](https://github.com/pingcap/tiflow/issues/6448) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)としての MySQL 8.0 との互換性の向上
        -   「無効な接続」が発生したときに DDL を非同期に実行することで DDL を最適化します[<a href="https://github.com/pingcap/tiflow/issues/4689">#4689</a>](https://github.com/pingcap/tiflow/issues/4689) @ [<a href="https://github.com/lyzx2001">lyzx2001</a>](https://github.com/lyzx2001)

    -   TiDB Lightning

        -   S3 外部storageURL のクエリ パラメータを追加して、特定のロール[<a href="https://github.com/pingcap/tidb/issues/36891">#36891</a>](https://github.com/pingcap/tidb/issues/36891) @ [<a href="https://github.com/dsdashun">dsダシュン</a>](https://github.com/dsdashun)を引き受けることで別のアカウントの S3 データへのアクセスをサポートします。

## バグの修正 {#bug-fixes}

-   TiDB

    -   `PREPARE`ステートメント[<a href="https://github.com/pingcap/tidb/issues/35784">#35784</a>](https://github.com/pingcap/tidb/issues/35784) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)で権限チェックがスキップされる問題を修正
    -   システム変数`tidb_enable_noop_variable`が`WARN` [<a href="https://github.com/pingcap/tidb/issues/36647">#36647</a>](https://github.com/pingcap/tidb/issues/36647) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)に設定できる問題を修正
    -   式インデックスが定義されている場合、 `INFORMAITON_SCHEMA.COLUMNS`テーブルの`ORDINAL_POSITION`列が正しくない可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/31200">#31200</a>](https://github.com/pingcap/tidb/issues/31200) @ [<a href="https://github.com/bb7133">bb7133</a>](https://github.com/bb7133)
    -   タイムスタンプが`MAXINT32` [<a href="https://github.com/pingcap/tidb/issues/31585">#31585</a>](https://github.com/pingcap/tidb/issues/31585) @ [<a href="https://github.com/bb7133">bb7133</a>](https://github.com/bb7133)より大きい場合に TiDB がエラーを報告しない問題を修正
    -   エンタープライズプラグイン使用時にTiDBサーバーが起動できない問題を修正[<a href="https://github.com/pingcap/tidb/issues/37319">#37319</a>](https://github.com/pingcap/tidb/issues/37319) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)
    -   `SHOW CREATE PLACEMENT POLICY` [<a href="https://github.com/pingcap/tidb/issues/37526">#37526</a>](https://github.com/pingcap/tidb/issues/37526) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)の誤った出力を修正
    -   一時テーブル[<a href="https://github.com/pingcap/tidb/issues/37201">#37201</a>](https://github.com/pingcap/tidb/issues/37201) @ [<a href="https://github.com/lcwangchao">ルクワンチャオ</a>](https://github.com/lcwangchao)での予期しない動作`EXCHANGE PARTITION`を修正
    -   `INFORMATION_SCHEMA.TIKV_REGION_STATUS`をクエリすると間違った結果 @ [<a href="https://github.com/zimulala">ジムララ</a>](https://github.com/zimulala)が返される問題を修正します。
    -   ビューに対する`EXPLAIN`クエリが権限[<a href="https://github.com/pingcap/tidb/issues/34326">#34326</a>](https://github.com/pingcap/tidb/issues/34326) @ [<a href="https://github.com/hawkingrei">ホーキングレイ</a>](https://github.com/hawkingrei)をチェックしない問題を修正します。
    -   JSON `null` `NULL` [<a href="https://github.com/pingcap/tidb/issues/37852">#37852</a>](https://github.com/pingcap/tidb/issues/37852) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)に更新できない問題を修正
    -   DDL ジョブの`row_count`が不正確である問題を修正[<a href="https://github.com/pingcap/tidb/issues/25968">#25968</a>](https://github.com/pingcap/tidb/issues/25968) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)
    -   `FLASHBACK TABLE` [<a href="https://github.com/pingcap/tidb/issues/37386">#37386</a>](https://github.com/pingcap/tidb/issues/37386) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)が正常に動作しない問題を修正
    -   一般的な MySQL プロトコル[<a href="https://github.com/pingcap/tidb/issues/36731">#36731</a>](https://github.com/pingcap/tidb/issues/36731) @ [<a href="https://github.com/dveeden">ドヴィーデン</a>](https://github.com/dveeden)で`prepared`ステートメント フラグの処理に失敗する問題を修正
    -   一部の極端なケースで起動時に表示される可能性がある不正な TiDB ステータスの問題を修正します[<a href="https://github.com/pingcap/tidb/issues/36791">#36791</a>](https://github.com/pingcap/tidb/issues/36791) @ [<a href="https://github.com/xhebox">ゼボックス</a>](https://github.com/xhebox)
    -   `INFORMATION_SCHEMA.VARIABLES_INFO`がセキュリティ強化モード (SEM) [<a href="https://github.com/pingcap/tidb/issues/37586">#37586</a>](https://github.com/pingcap/tidb/issues/37586) @ [<a href="https://github.com/CbcWestwolf">Cbcウェストウルフ</a>](https://github.com/CbcWestwolf)に準拠していない問題を修正
    -   `UNION` [<a href="https://github.com/pingcap/tidb/issues/31678">#31678</a>](https://github.com/pingcap/tidb/issues/31678) @ [<a href="https://github.com/cbcwestwolf">CBCウエストウルフ</a>](https://github.com/cbcwestwolf)を使用したクエリで文字列から文字列へのキャストが失敗する問題を修正
    -   TiFlash [<a href="https://github.com/pingcap/tidb/issues/37254">#37254</a>](https://github.com/pingcap/tidb/issues/37254) @ [<a href="https://github.com/wshwsh12">wshwsh12</a>](https://github.com/wshwsh12)のパーティション化されたテーブルで動的モードを有効にしたときに発生する間違った結果を修正しました。
    -   TiDB のバイナリ文字列と JSON 間のキャストと比較が MySQL [<a href="https://github.com/pingcap/tidb/issues/31918">#31918</a>](https://github.com/pingcap/tidb/issues/31918) [<a href="https://github.com/pingcap/tidb/issues/25053">#25053</a>](https://github.com/pingcap/tidb/issues/25053) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)と互換性がない問題を修正
    -   TiDB の`JSON_OBJECTAGG`と`JSON_ARRAYAGG`がバイナリ値[<a href="https://github.com/pingcap/tidb/issues/25053">#25053</a>](https://github.com/pingcap/tidb/issues/25053) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)で MySQL と互換性がない問題を修正
    -   JSON の不透明な値間の比較でpanic[<a href="https://github.com/pingcap/tidb/issues/37315">#37315</a>](https://github.com/pingcap/tidb/issues/37315) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)が発生する問題を修正
    -   JSON集計関数[<a href="https://github.com/pingcap/tidb/issues/37287">#37287</a>](https://github.com/pingcap/tidb/issues/37287) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)で単精度浮動小数点数が使用できない問題を修正
    -   `UNION`演算子が予期しない空の結果[<a href="https://github.com/pingcap/tidb/issues/36903">#36903</a>](https://github.com/pingcap/tidb/issues/36903) @ [<a href="https://github.com/tiancaiamao">ティエンチャイアマオ</a>](https://github.com/tiancaiamao)を返す可能性がある問題を修正します。
    -   `castRealAsTime`式の結果が MySQL [<a href="https://github.com/pingcap/tidb/issues/37462">#37462</a>](https://github.com/pingcap/tidb/issues/37462) @ [<a href="https://github.com/mengxin9014">孟新9014</a>](https://github.com/mengxin9014)と一致しない問題を修正
    -   悲観的DML 操作により、一意でないインデックス キー[<a href="https://github.com/pingcap/tidb/issues/36235">#36235</a>](https://github.com/pingcap/tidb/issues/36235) @ [<a href="https://github.com/ekexium">エキシウム</a>](https://github.com/ekexium)がロックされる問題を修正します。
    -   `auto-commit`変更がトランザクションのコミット動作[<a href="https://github.com/pingcap/tidb/issues/36581">#36581</a>](https://github.com/pingcap/tidb/issues/36581) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)に影響を与える問題を修正
    -   DML エグゼキュータを使用した`EXPLAIN ANALYZE`ステートメントが、トランザクションのコミットが完了する前に結果を返す可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/issues/37373">#37373</a>](https://github.com/pingcap/tidb/issues/37373) @ [<a href="https://github.com/cfzjywxk">cfzjywxk</a>](https://github.com/cfzjywxk)
    -   場合によっては UPDATE ステートメントが誤って投影を削除し、 `Can't find column`エラー[<a href="https://github.com/pingcap/tidb/issues/37568">#37568</a>](https://github.com/pingcap/tidb/issues/37568) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)が発生する問題を修正します。
    -   結合したテーブルの再配置操作により誤って外部結合条件[<a href="https://github.com/pingcap/tidb/issues/37238">#37238</a>](https://github.com/pingcap/tidb/issues/37238) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)がプッシュダウンされる問題を修正します。
    -   一部のパターンの`IN`および`NOT IN`サブクエリで`Can't find column`エラー[<a href="https://github.com/pingcap/tidb/issues/37032">#37032</a>](https://github.com/pingcap/tidb/issues/37032) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)が報告される問題を修正します。
    -   `UPDATE`ステートメントに共通テーブル式 (CTE) [<a href="https://github.com/pingcap/tidb/issues/35758">#35758</a>](https://github.com/pingcap/tidb/issues/35758) @ [<a href="https://github.com/AilinKid">アイリンキッド</a>](https://github.com/AilinKid)が含まれる場合に`Can't find column`が報告される問題を修正
    -   間違った`PromQL` [<a href="https://github.com/pingcap/tidb/issues/35856">#35856</a>](https://github.com/pingcap/tidb/issues/35856) @ [<a href="https://github.com/Defined2014">定義2014</a>](https://github.com/Defined2014)を修正

-   TiKV

    -   リージョンハートビートが中断された後、PD が TiKV に再接続しない問題を修正[<a href="https://github.com/tikv/tikv/issues/12934">#12934</a>](https://github.com/tikv/tikv/issues/12934) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)
    -   Raftstore がビジー[<a href="https://github.com/tikv/tikv/issues/13160">#13160</a>](https://github.com/tikv/tikv/issues/13160) @ [<a href="https://github.com/5kbpers">5kbps</a>](https://github.com/5kbpers)の場合、リージョンが重複する可能性がある問題を修正
    -   PD クライアントがデッドロックを引き起こす可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/13191">#13191</a>](https://github.com/tikv/tikv/issues/13191) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies) [<a href="https://github.com/tikv/tikv/issues/12933">#12933</a>](https://github.com/tikv/tikv/issues/12933) @ [<a href="https://github.com/BurtonQin">バートン秦</a>](https://github.com/BurtonQin)
    -   暗号化が無効になっている場合に TiKV がpanicになる可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/13081">#13081</a>](https://github.com/tikv/tikv/issues/13081) @ [<a href="https://github.com/jiayang-zheng">嘉陽鄭</a>](https://github.com/jiayang-zheng)
    -   ダッシュボード[<a href="https://github.com/tikv/tikv/issues/13086">#13086</a>](https://github.com/tikv/tikv/issues/13086) @ [<a href="https://github.com/glorv">グロルフ</a>](https://github.com/glorv)の`Unified Read Pool CPU`の間違った式を修正
    -   TiKV インスタンスが隔離されたネットワーク環境[<a href="https://github.com/tikv/tikv/issues/12966">#12966</a>](https://github.com/tikv/tikv/issues/12966) @ [<a href="https://github.com/cosven">コスベン</a>](https://github.com/cosven)にある場合、TiKV サービスが数分間利用できなくなる問題を修正します。
    -   TiKV が誤って`PessimisticLockNotFound`エラー[<a href="https://github.com/tikv/tikv/issues/13425">#13425</a>](https://github.com/tikv/tikv/issues/13425) @ [<a href="https://github.com/sticnarf">スティックナーフ</a>](https://github.com/sticnarf)を報告する問題を修正
    -   状況によっては PITR によってデータ損失が発生する可能性がある問題を修正[<a href="https://github.com/tikv/tikv/issues/13281">#13281</a>](https://github.com/tikv/tikv/issues/13281) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)
    -   長い悲観的トランザクション[<a href="https://github.com/tikv/tikv/issues/13304">#13304</a>](https://github.com/tikv/tikv/issues/13304) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)があるときにチェックポイントが進められない問題を修正
    -   TiKV が JSON [<a href="https://github.com/tikv/tikv/issues/13417">#13417</a>](https://github.com/tikv/tikv/issues/13417) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)の datetime 型 ( `DATETIME` 、 `DATE` 、 `TIMESTAMP` 、 `TIME` ) と`STRING`型を区別しない問題を修正します。
    -   JSON bool と他の JSON 値[<a href="https://github.com/tikv/tikv/issues/13386">#13386</a>](https://github.com/tikv/tikv/issues/13386) [<a href="https://github.com/pingcap/tidb/issues/37481">#37481</a>](https://github.com/pingcap/tidb/issues/37481) @ [<a href="https://github.com/YangKeao">ヤンケオ</a>](https://github.com/YangKeao)との比較における MySQL との非互換性を修正

-   PD

    -   `enable-forwarding`が有効になっている場合に gRPC がエラーを不適切に処理する問題によって引き起こされる PD パニックを修正[<a href="https://github.com/tikv/pd/issues/5373">#5373</a>](https://github.com/tikv/pd/issues/5373) @ [<a href="https://github.com/bufferflies">バッファフライ</a>](https://github.com/bufferflies)
    -   異常なリージョンにより PDpanic[<a href="https://github.com/tikv/pd/issues/5491">#5491</a>](https://github.com/tikv/pd/issues/5491) @ [<a href="https://github.com/nolouch">ノールーシュ</a>](https://github.com/nolouch)が発生する可能性がある問題を修正
    -   TiFlash学習者のレプリカが作成されないことがある問題を修正[<a href="https://github.com/tikv/pd/issues/5401">#5401</a>](https://github.com/tikv/pd/issues/5401) @ [<a href="https://github.com/HunDunDM">フンドゥンDM</a>](https://github.com/HunDunDM)

-   TiFlash

    -   クエリがキャンセルされたときにウィンドウ関数によってTiFlashがクラッシュする可能性がある問題を修正[<a href="https://github.com/pingcap/tiflash/issues/5814">#5814</a>](https://github.com/pingcap/tiflash/issues/5814) @ [<a href="https://github.com/SeaRise">シーライズ</a>](https://github.com/SeaRise)
    -   `CAST(value AS DATETIME)`の間違ったデータ入力によりTiFlash sys CPU [<a href="https://github.com/pingcap/tiflash/issues/5097">#5097</a>](https://github.com/pingcap/tiflash/issues/5097) @ [<a href="https://github.com/xzhangxian1008">xzhangxian1008</a>](https://github.com/xzhangxian1008)のパフォーマンスが高くなる問題を修正
    -   `CAST(Real/Decimal AS time)`の結果がMySQL [<a href="https://github.com/pingcap/tiflash/issues/3779">#3779</a>](https://github.com/pingcap/tiflash/issues/3779) @ [<a href="https://github.com/mengxin9014">孟新9014</a>](https://github.com/mengxin9014)と矛盾する問題を修正
    -   storage内の一部の古いデータが削除できない問題を修正[<a href="https://github.com/pingcap/tiflash/issues/5570">#5570</a>](https://github.com/pingcap/tiflash/issues/5570) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)
    -   ページ GC がテーブル[<a href="https://github.com/pingcap/tiflash/issues/5697">#5697</a>](https://github.com/pingcap/tiflash/issues/5697) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)の作成をブロックする可能性がある問題を修正
    -   `NULL`値[<a href="https://github.com/pingcap/tiflash/issues/5859">#5859</a>](https://github.com/pingcap/tiflash/issues/5859) @ [<a href="https://github.com/JaySon-Huang">ジェイ・ソン・ファン</a>](https://github.com/JaySon-Huang)を含む列でプライマリ インデックスを作成した後に発生するpanicを修正します。

-   ツール

    -   バックアップと復元 (BR)

        -   チェックポイントの情報が古くなる可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/36423">#36423</a>](https://github.com/pingcap/tidb/issues/36423) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)
        -   復元中に同時実行数の設定が大きすぎるため、リージョンのバランスが取れない問題を修正[<a href="https://github.com/pingcap/tidb/issues/37549">#37549</a>](https://github.com/pingcap/tidb/issues/37549) @ [<a href="https://github.com/3pointer">3ポインター</a>](https://github.com/3pointer)
        -   TiCDC がクラスター[<a href="https://github.com/pingcap/tidb/issues/37822">#37822</a>](https://github.com/pingcap/tidb/issues/37822) @ [<a href="https://github.com/YuJuncen">ユジュンセン</a>](https://github.com/YuJuncen)に存在する場合に、ログ バックアップ チェックポイント TS がスタックする可能性がある問題を修正します。
        -   外部storageの認証キーに特殊文字が存在する場合、バックアップと復元が失敗する可能性がある問題を修正[<a href="https://github.com/pingcap/tidb/issues/37469">#37469</a>](https://github.com/pingcap/tidb/issues/37469) [<a href="https://github.com/MoCuishle28">@MouCuishle28</a>](https://github.com/MoCuishle28)

    -   TiCDC

        -   TiCDC が grpc サービス[<a href="https://github.com/pingcap/tiflow/issues/6458">#6458</a>](https://github.com/pingcap/tiflow/issues/6458) @ [<a href="https://github.com/crelax">クレラックス</a>](https://github.com/crelax)で間違った PD アドレスに対して不正確なエラーを返す問題を修正
        -   `cdc cause cli changefeed list`コマンドが失敗した変更フィード[<a href="https://github.com/pingcap/tiflow/issues/6334">#6334</a>](https://github.com/pingcap/tiflow/issues/6334) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)を返さない問題を修正します。
        -   チェンジフィードの初期化が失敗した場合に TiCDC が利用できない問題を修正[<a href="https://github.com/pingcap/tiflow/issues/6859">#6859</a>](https://github.com/pingcap/tiflow/issues/6859) @ [<a href="https://github.com/asddongmen">東門</a>](https://github.com/asddongmen)

    -   TiDBBinlog

        -   コンプレッサーが gzip [<a href="https://github.com/pingcap/tidb-binlog/issues/1152">#1152</a>](https://github.com/pingcap/tidb-binlog/issues/1152) @ [<a href="https://github.com/lichunzhu">リチュンジュ</a>](https://github.com/lichunzhu)に設定されている場合、 Drainer がリクエストをPumpに正しく送信できない問題を修正

    -   TiDB データ移行 (DM)

        -   DM が`Specified key was too long`エラー[<a href="https://github.com/pingcap/tiflow/issues/5315">#5315</a>](https://github.com/pingcap/tiflow/issues/5315) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を報告する問題を修正
        -   リレーがエラー[<a href="https://github.com/pingcap/tiflow/issues/6193">#6193</a>](https://github.com/pingcap/tiflow/issues/6193) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)に遭遇したときの goroutine リークを修正
        -   `collation_compatible`を`"strict"`に設定すると、DM が重複した照合順序[<a href="https://github.com/pingcap/tiflow/issues/6832">#6832</a>](https://github.com/pingcap/tiflow/issues/6832) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)を含む SQL を生成する可能性がある問題を修正します。
        -   DM-worker ログ[<a href="https://github.com/pingcap/tiflow/issues/6628">#6628</a>](https://github.com/pingcap/tiflow/issues/6628) @ [<a href="https://github.com/lyzx2001">lyzx2001</a>](https://github.com/lyzx2001)に表示される警告メッセージ「 binlog status_vars からタイムゾーンを取得するときにエラーが見つかりました」の表示を減らします。
        -   レプリケーション[<a href="https://github.com/pingcap/tiflow/issues/7028">#7028</a>](https://github.com/pingcap/tiflow/issues/7028) @ [<a href="https://github.com/lance6716">ランス6716</a>](https://github.com/lance6716)中に latin1 データが破損する可能性がある問題を修正

    -   TiDB Lightning

        -   TiDB Lightning がParquet ファイル[<a href="https://github.com/pingcap/tidb/issues/36980">#36980</a>](https://github.com/pingcap/tidb/issues/36980) @ [<a href="https://github.com/D3Hunter">D3ハンター</a>](https://github.com/D3Hunter)でスラッシュ、数字、または非 ASCII 文字で始まる列をサポートしない問題を修正します。

## 貢献者 {#contributors}

TiDB コミュニティの以下の貢献者に感謝いたします。

-   @ [<a href="https://github.com/An-DJ">DJ</a>](https://github.com/An-DJ)
-   @ [<a href="https://github.com/AnnieoftheStars">アニー・オブ・ザ・スターズ</a>](https://github.com/AnnieoftheStars)
-   @ [<a href="https://github.com/AntiTopQuark">アンチトップクワーク</a>](https://github.com/AntiTopQuark)
-   @ [<a href="https://github.com/blacktear23">ブラックティア23</a>](https://github.com/blacktear23)
-   @ [<a href="https://github.com/BurtonQin">バートン秦</a>](https://github.com/BurtonQin) (初投稿者)
-   @ [<a href="https://github.com/crelax">クレラックス</a>](https://github.com/crelax)
-   @ [<a href="https://github.com/eltociear">エルトシア</a>](https://github.com/eltociear)
-   @ [<a href="https://github.com/fuzhe1989">ふざ1989</a>](https://github.com/fuzhe1989)
-   @ [<a href="https://github.com/erwadba">エルワドバ</a>](https://github.com/erwadba)
-   @ [<a href="https://github.com/jianzhiyao">ジャンジヤオ</a>](https://github.com/jianzhiyao)
-   @ [<a href="https://github.com/joycse06">ジョイセ06</a>](https://github.com/joycse06)
-   @ [<a href="https://github.com/morgo">モルゴ</a>](https://github.com/morgo)
-   @ [<a href="https://github.com/onlyacat">オンリーキャット</a>](https://github.com/onlyacat)
-   @ [<a href="https://github.com/peakji">ピークジ</a>](https://github.com/peakji)
-   @ [<a href="https://github.com/rzrymiak">ルズリミアク</a>](https://github.com/rzrymiak)
-   @ [<a href="https://github.com/tisonkun">てそくん</a>](https://github.com/tisonkun)
-   @ [<a href="https://github.com/whitekeepwork">ホワイトキープワーク</a>](https://github.com/whitekeepwork)
-   @ [<a href="https://github.com/Ziy1-Tan">Ziy1-Tan</a>](https://github.com/Ziy1-Tan)

---
title: TiDB 3.0.8 Release Notes
summary: TiDB 3.0.8は2019年12月31日にリリースされました。SQLオプティマイザー、SQL実行エンジン、DDL、サーバー、トランザクション、モニター、TiKV、PD、TiDB Ansibleに関する様々な修正と改善が含まれています。主な変更点としては、SQLバインディングプランの修正、エラーメッセージの最適化、証明書ベースの認証のサポートなどが挙げられます。tidb_txn_mode`変数のデフォルト値が`"悲観的"`に更新されました。PDではパフォーマンスの最適化とバグ修正も行われました。TiDB Ansibleでは、様々なロジックの最適化とアップグレードが行われました。
---

# TiDB 3.0.8 リリースノート {#tidb-3-0-8-release-notes}

発売日：2019年12月31日

TiDB バージョン: 3.0.8

TiDB Ansible バージョン: 3.0.8

## TiDB {#tidb}

-   SQLオプティマイザー
    -   タイミングの悪いキャッシュ更新によって発生した間違ったSQLバインディングプランを修正[＃13891](https://github.com/pingcap/tidb/pull/13891)
    -   SQL文にシンボルリスト[＃14004](https://github.com/pingcap/tidb/pull/14004)が含まれている場合にSQLバインディングが無効になる可能性がある問題を修正しました
    -   SQL文が`;` [＃14113](https://github.com/pingcap/tidb/pull/14113)で終わるためSQLバインディングを作成または削除できない問題を修正しました
    -   `PhysicalUnionScan`演算子が間違った統計を設定するため、間違った SQL クエリ プランが選択される可能性がある問題を修正しました[＃14133](https://github.com/pingcap/tidb/pull/14133)
    -   `minAutoAnalyzeRatio`制限を解除して`autoAnalyze`をよりタイムリーにする[＃14015](https://github.com/pingcap/tidb/pull/14015)
-   SQL実行エンジン
    -   `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT`構文でエラーが報告される可能性があり、 `DEFAULT`の使用と仮想生成列を組み合わせるとエラーが報告される可能性がある問題を修正しました[＃13682](https://github.com/pingcap/tidb/pull/13682)
    -   `INSERT`文が文字列を浮動小数点数に変換するときにエラーを報告する可能性がある問題を修正しました[＃14011](https://github.com/pingcap/tidb/pull/14011)
    -   `HashAgg` Executor の同時実行値が正しく初期化されていないために集計操作の効率が低下することがある問題を修正しました[＃13811](https://github.com/pingcap/tidb/pull/13811)
    -   `group by item`節が括弧内にある場合に実行時にエラーが報告される問題を修正[＃13658](https://github.com/pingcap/tidb/pull/13658)
    -   TiDBが`group by item` [＃14014](https://github.com/pingcap/tidb/pull/14014)を誤って計算するため、 `OUTER JOIN`の実行でエラーが報告される可能性がある問題を修正しました。
    -   範囲を超えるデータが範囲パーティションテーブルに書き込まれたときにエラーメッセージが不正確になる問題を修正[＃14107](https://github.com/pingcap/tidb/pull/14107)
    -   MySQL 8では`PadCharToFullLength`すぐに破棄されることを考慮して、特殊なケースで予期しないクエリ結果を回避するために[PR #10124](https://github.com/pingcap/tidb/pull/10124)元に戻し、 `PadCharToFullLength`効果をキャンセルします[＃14157](https://github.com/pingcap/tidb/pull/14157)
    -   `ExplainExec` [＃14226](https://github.com/pingcap/tidb/pull/14226)の保証されていない`close()`呼び出しによって発生する`EXPLAIN ANALYZE`文の実行時のゴルーチン リークの問題を修正しました。
-   DDL
    -   `change column`のエラーメッセージ出力`modify column`最適化して理解しやすくする[＃13796](https://github.com/pingcap/tidb/pull/13796)
    -   パーティションテーブル[＃13929](https://github.com/pingcap/tidb/pull/13929)リージョン分割をサポートするために`SPLIT PARTITION TABLE`構文を追加します
    -   インデックス作成時にインデックスの長さが正しくチェックされないため、インデックスの長さが3072バイトを超えてもエラーが報告されない問題を修正しました[＃13779](https://github.com/pingcap/tidb/pull/13779)
    -   パーティションテーブル[＃14132](https://github.com/pingcap/tidb/pull/14132)にインデックスを追加するのに時間がかかりすぎるため、 `GC life time is shorter than transaction duration`エラーメッセージが報告される可能性がある問題を修正しました。
    -   `DROP COLUMN` / `MODIFY COLUMN` / `CHANGE COLUMN`実行時に外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`実行時にpanicする問題を修正しました[＃14105](https://github.com/pingcap/tidb/pull/14105)
-   サーバ
    -   ステートメントサマリーの改善:
        -   SQL文をより詳細に分析できるように[＃14168](https://github.com/pingcap/tidb/pull/14168)多数のSQLメトリックフィールドを追加します[＃14151](https://github.com/pingcap/tidb/pull/14151)
        -   `stmt-summary.refresh-interval`パラメータを追加して、古いデータを`events_statements_summary_by_digest`テーブルから`events_statements_summary_by_digest_history`テーブルに移動するかどうかを制御します (デフォルトの間隔: 30 分) [＃14161](https://github.com/pingcap/tidb/pull/14161)
        -   `events_statements_summary_by_digest` [＃14166](https://github.com/pingcap/tidb/pull/14166)の古いデータを保存するには、 `events_statements_summary_by_digest_history`テーブルを追加します。
    -   RBAC関連の内部SQL文実行時にbinlogが誤って出力される問題を修正[＃13890](https://github.com/pingcap/tidb/pull/13890)
    -   TiDBサーバーバージョン[＃13906](https://github.com/pingcap/tidb/pull/13906)変更する機能を制御するための`server-version`構成項目を追加します
    -   HTTPインターフェースを使用してTiDBbinlog[＃13892](https://github.com/pingcap/tidb/pull/13892)書き込みを回復する機能を追加
    -   MySQLの動作[＃13932](https://github.com/pingcap/tidb/pull/13932)との一貫性を保つために、 `GRANT roles TO user`に必要な権限を`GrantPriv`から`ROLE_ADMIN`または`SUPER`に更新します。
    -   MySQLの動作[＃13784](https://github.com/pingcap/tidb/pull/13784)の互換性を保つために、TiDBの動作を、現在のデータベースを使用する動作から、 `GRANT`文でデータベース名が指定されていない場合に`No database selected`エラーを報告する動作に変更しました。
    -   MySQLの動作[＃13306](https://github.com/pingcap/tidb/pull/13306)との一貫性を保つために、 `REVOKE`文の実行権限を`SuperPriv`から`REVOKE`変更し、対応するスキーマに対する権限を持つユーザーのみ実行できるようにします。
    -   `GRANT ALL`構文に`WITH GRANT OPTION` [＃13943](https://github.com/pingcap/tidb/pull/13943)が含まれていない場合に、対象ユーザーに`GrantPriv`が誤って付与される問題を修正しました。
    -   `LoadDataInfo` `addRecord` [＃13980](https://github.com/pingcap/tidb/pull/13980)呼び出しに失敗した場合、エラー メッセージに`LOAD DATA`ステートメントの誤った動作の原因が含まれていない問題を修正しました。
    -   クエリ内の複数のSQL文が同じ`StartTime` [＃13898](https://github.com/pingcap/tidb/pull/13898)を共有しているため、間違ったスロークエリ情報が出力される問題を修正しました。
    -   `batchClient`大規模なトランザクションを処理するときにメモリが発生する可能性がある問題を修正[＃14032](https://github.com/pingcap/tidb/pull/14032)
    -   `system_time_zone`が常に`CST`として表示され、TiDB の`system_time_zone` `mysql.tidb`テーブル[＃14086](https://github.com/pingcap/tidb/pull/14086)の`systemTZ`から取得される問題を修正しました。
    -   `GRANT ALL`構文がユーザーにすべての権限を付与しない問題を修正[＃14092](https://github.com/pingcap/tidb/pull/14092)
    -   `Priv_create_user`権限が`CREATE ROLE`と`DROP ROLE` [＃14088](https://github.com/pingcap/tidb/pull/14088)では無効になる問題を修正
    -   エラーコード`ErrInvalidFieldSize`を`1105(Unknow Error)`から`3013`に変更します[＃13737](https://github.com/pingcap/tidb/pull/13737)
    -   TiDBサーバーを停止するコマンド`SHUTDOWN`を追加し、権限`ShutdownPriv`を追加します[＃14104](https://github.com/pingcap/tidb/pull/14104)
    -   TiDBがステートメント[＃14130](https://github.com/pingcap/tidb/pull/14130)実行に失敗したときに一部のロールが予期せず削除されるのを回避するために、ステートメント`DROP ROLE`のアトミック性の問題を修正しました。
    -   TiDB バージョンが 3.0 にアップグレードされたときに、 `SHOW VARIABLE`結果の`tidb_enable_window_function`誤って`1`出力される問題を修正し、間違った結果を`0` [＃14131](https://github.com/pingcap/tidb/pull/14131)に置き換えます。
    -   TiKVノードがオフラインのときに`gcworker`継続的に再試行するため、goroutineがリークする可能性がある問題を修正しました[＃14106](https://github.com/pingcap/tidb/pull/14106)
    -   問題追跡の使いやすさを向上させるために、スロークエリログにbinlogを`Prewrite`回記録します[＃14138](https://github.com/pingcap/tidb/pull/14138)
    -   `tidb_enable_table_partition`変数を`GLOBAL SCOPE` [＃14091](https://github.com/pingcap/tidb/pull/14091)サポートする
    -   新しい権限が追加されたときに、新しく追加された権限が対応するユーザーに正しく付与されないため、ユーザー権限が欠落したり、誤って追加されたりする可能性がある問題を修正しました[＃14178](https://github.com/pingcap/tidb/pull/14178)
    -   TiKVサーバーが切断されたときに`rpcClient`閉じないために`CheckStreamTimeoutLoop`ゴルーチンがリークする可能性がある問題を修正しました[＃14227](https://github.com/pingcap/tidb/pull/14227)
    -   証明書ベースの認証をサポートする ( [ユーザードキュメント](/certificate-authentication.md) ) [＃13955](https://github.com/pingcap/tidb/pull/13955)
-   トランザクション
    -   新しいクラスターが作成されたときに、 `tidb_txn_mode`変数のデフォルト値を`""`から`"pessimistic"`に更新します[＃14171](https://github.com/pingcap/tidb/pull/14171)
    -   トランザクションが再試行されたときに単一のステートメントのロック待機時間がリセットされないため、悲観的トランザクションのロック待機時間が長すぎる問題を修正しました[＃13990](https://github.com/pingcap/tidb/pull/13990)
    -   悲観的トランザクションモード[＃14050](https://github.com/pingcap/tidb/pull/14050)で未変更データがロック解除されるため、誤ったデータが読み取られる可能性がある問題を修正しました。
    -   mocktikv [＃14175](https://github.com/pingcap/tidb/pull/14175)で事前書き込みを実行するときにトランザクション タイプが区別されないため、挿入値の制限チェックが繰り返される問題を修正しました。
    -   `session.TxnState`が`Invalid` [＃13988](https://github.com/pingcap/tidb/pull/13988)ときにトランザクションが正しく処理されないためpanicを修正
    -   mocktikvの`ErrConfclit`構造に`ConflictCommitTS` [＃14080](https://github.com/pingcap/tidb/pull/14080)が含まれていない問題を修正しました
    -   TiDBがロック[＃14083](https://github.com/pingcap/tidb/pull/14083)を解決した後にロックタイムアウトを正しくチェックしないため、トランザクションがブロックされる問題を修正しました。
-   モニター
    -   `LockKeys` [＃14194](https://github.com/pingcap/tidb/pull/14194)に`pessimistic_lock_keys_duration`監視項目を追加

## TiKV {#tikv}

-   コプロセッサー
    -   コプロセッサー[＃6051](https://github.com/tikv/tikv/pull/6051)でエラーが発生した場合の出力ログのレベルを`error`から`warn`に変更します
    -   統計サンプリングデータの更新動作を、行を直接更新するのではなく、挿入前に削除するように変更し、tidb-server [＃6069](https://github.com/tikv/tikv/pull/6096)の更新動作との一貫性を保ちます。
-   Raftstore
    -   `destroy`メッセージを`peerfsm`に繰り返し送信し、 `peerfsm`複数回破棄されることによって引き起こされるpanicを修正[＃6297](https://github.com/tikv/tikv/pull/6297)
    -   デフォルト値`split-region-on-table`を`true`から`false`に更新して、デフォルトでテーブルごとにリージョンを分割しないようにします[＃6253](https://github.com/tikv/tikv/pull/6253)
-   エンジン
    -   極端な状況でRocksDBイテレータエラーが正しく処理されないため、空のデータが返される可能性がある問題を修正しました[＃6326](https://github.com/tikv/tikv/pull/6326)
-   トランザクション
    -   悲観的ロックが誤ってクリーンアップされたために、TiKV がキーにデータを書き込むことができず、GC がブロックされる問題を修正しました[＃6354](https://github.com/tikv/tikv/pull/6354)
    -   ロック競合が深刻なシナリオでのパフォーマンスを向上させるために悲観的ロック待機メカニズムを最適化します[＃6296](https://github.com/tikv/tikv/pull/6296)
-   デフォルト値`tikv_alloc`を`tikv_alloc/default`から`jemalloc`に更新します[＃6206](https://github.com/tikv/tikv/pull/6206)

## PD {#pd}

-   クライアント
    -   `context`使用してクライアントを作成し、新しいクライアント[＃1994](https://github.com/pingcap/pd/pull/1994)を作成するときにタイムアウト期間を設定することをサポートします。
    -   `KeepAlive`接続[＃2035](https://github.com/pingcap/pd/pull/2035)作成をサポート
-   `/api/v1/regions` API [＃1986](https://github.com/pingcap/pd/pull/1986)のパフォーマンスを最適化
-   `tombstone`状態でストアを削除するとpanicが発生する可能性がある問題を修正[＃2038](https://github.com/pingcap/pd/pull/2038)
-   ディスク[#2011](https://github.com/pingcap/pd/issues/2011)からリージョン情報をロードするときに重複したリージョンが誤って削除される問題[＃2040](https://github.com/pingcap/pd/pull/2040)修正しました
-   etcdをv3.4.0からv3.4.3にアップグレードします（アップグレード後はpd-recoverを使用してetcdをデグレードすることしかできないことに注意してください） [＃2058](https://github.com/pingcap/pd/pull/2058)

## ツール {#tools}

-   TiDBBinlog
    -   PumpがコミットされたDDLbinlog[＃853](https://github.com/pingcap/tidb-binlog/pull/853)を受信しないため、binlogが無視される問題を修正しました。

## TiDB アンシブル {#tidb-ansible}

-   簡略化された構成項目[＃1053](https://github.com/pingcap/tidb-ansible/pull/1053)元に戻す
-   ローリングアップデートを実行する際にTiDBのバージョンをチェックするロジックを最適化します[＃1056](https://github.com/pingcap/tidb-ansible/pull/1056)
-   TiSparkをv2.1.8にアップグレード[＃1061](https://github.com/pingcap/tidb-ansible/pull/1061)
-   Grafana [＃1065](https://github.com/pingcap/tidb-ansible/pull/1065)で PD ロール監視項目が誤って表示される問題を修正
-   Grafana [＃1071](https://github.com/pingcap/tidb-ansible/pull/1071)のTiKV詳細ページで監視項目`Thread Voluntary Context Switches`と`Thread Nonvoluntary Context Switches`最適化

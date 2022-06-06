---
title: TiDB 3.0.8 Release Notes
---

# TiDB3.0.8リリースノート {#tidb-3-0-8-release-notes}

発売日：2019年12月31日

TiDBバージョン：3.0.8

TiDB Ansibleバージョン：3.0.8

## TiDB {#tidb}

-   SQLオプティマイザー
    -   タイムリーでないキャッシュ更新によって引き起こされた間違ったSQLバインディングプランを修正する[＃13891](https://github.com/pingcap/tidb/pull/13891)
    -   SQLステートメントにシンボルリストが含まれている場合にSQLバインディングが無効になる可能性がある問題を修正します[＃14004](https://github.com/pingcap/tidb/pull/14004)
    -   SQLステートメントが[＃14113](https://github.com/pingcap/tidb/pull/14113)で終わるため、SQLバインディングを作成または削除できない問題を修正し`;` 。
    -   `PhysicalUnionScan`演算子が間違った統計を設定するために間違ったSQLクエリプランが選択される可能性があるという問題を修正します[＃14133](https://github.com/pingcap/tidb/pull/14133)
    -   `minAutoAnalyzeRatio`の制限を削除して、 `autoAnalyze`をよりタイムリーに[＃14015](https://github.com/pingcap/tidb/pull/14015)にします。
-   SQL実行エンジン
    -   `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT`構文でエラーが報告され、 `DEFAULT`式の使用法を仮想生成列と組み合わせるとエラーが報告される可能性がある問題を修正します[＃13682](https://github.com/pingcap/tidb/pull/13682)
    -   文字列をfloat3に変換するときに`INSERT`ステートメントがエラーを報告する可能性がある問題を修正し[＃14011](https://github.com/pingcap/tidb/pull/14011)
    -   `HashAgg`エグゼキュータの同時実行値が正しく初期化されていないために集約操作の効果が低い場合がある問題を修正します[＃13811](https://github.com/pingcap/tidb/pull/13811)
    -   句が括弧内にある場合に`group by item`の実行でエラーが報告される問題を修正します[＃13658](https://github.com/pingcap/tidb/pull/13658)
    -   [＃14014](https://github.com/pingcap/tidb/pull/14014)が35を誤って計算するため、 `OUTER JOIN`を実行するとエラーが報告される可能性がある問題を修正し`group by item` 。
    -   Rangeを超えるデータがRangeパーティションテーブルに書き込まれるときにエラーメッセージが不正確になる問題を修正します[＃14107](https://github.com/pingcap/tidb/pull/14107)
    -   MySQL 8がすぐに`PadCharToFullLength`を破棄することを考慮して、特別な場合に予期しないクエリ結果を回避するために、 [PR＃10124](https://github.com/pingcap/tidb/pull/10124)を元に戻して`PadCharToFullLength`の効果をキャンセルします[＃14157](https://github.com/pingcap/tidb/pull/14157)
    -   57での無保証の`close()`呼び出しによって引き起こされた`EXPLAIN ANALYZE`ステートメントを実行するときの[＃14226](https://github.com/pingcap/tidb/pull/14226)ルーチンリークの問題を修正し`ExplainExec` 。
-   DDL
    -   理解し[＃13796](https://github.com/pingcap/tidb/pull/13796)ように`change column`のエラーメッセージ出力を最適化する`modify column`
    -   パーティションテーブルのリージョンの分割をサポートする`SPLIT PARTITION TABLE`の構文を追加します[＃13929](https://github.com/pingcap/tidb/pull/13929)
    -   インデックスの作成時にインデックスの長さが正しくチェックされないため、インデックスの長さが3072バイトを超え、エラーが報告されない問題を修正します[＃13779](https://github.com/pingcap/tidb/pull/13779)
    -   パーティションテーブルにインデックスを追加するのに時間がかかりすぎるため、 `GC life time is shorter than transaction duration`エラーメッセージが報告される可能性があるという問題を修正します[＃14132](https://github.com/pingcap/tidb/pull/14132)
    -   `DROP COLUMN`の実行時に外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`が実行されたときの[＃14105](https://github.com/pingcap/tidb/pull/14105)を修正し`MODIFY COLUMN` `CHANGE COLUMN`
-   サーバ
    -   ステートメントの要約の改善：
        -   多数のSQLメトリックフィールドを追加して、SQLステートメントの詳細な分析を容易にし[＃14168](https://github.com/pingcap/tidb/pull/14168) [＃14151](https://github.com/pingcap/tidb/pull/14151)
        -   `stmt-summary.refresh-interval`パラメーターを追加して、古いデータを`events_statements_summary_by_digest`テーブルから`events_statements_summary_by_digest_history`テーブルに移動するかどうかを制御します（デフォルトの間隔：30分） [＃14161](https://github.com/pingcap/tidb/pull/14161)
        -   `events_statements_summary_by_digest_history` [＃14166](https://github.com/pingcap/tidb/pull/14166)テーブルを追加して、古いデータを35に保存し`events_statements_summary_by_digest`
    -   RBAC関連の内部SQLステートメントが実行されたときにbinlogが誤って出力される問題を修正します[＃13890](https://github.com/pingcap/tidb/pull/13890)
    -   `server-version`の構成アイテムを追加して、TiDBサーバーバージョン[＃13906](https://github.com/pingcap/tidb/pull/13906)を変更する機能を制御します。
    -   HTTPインターフェイスを使用して[＃13892](https://github.com/pingcap/tidb/pull/13892)の書き込みを回復する機能を追加します。
    -   MySQLの動作との一貫性を保つために、 `GRANT roles TO user`に必要な特権を`GrantPriv`から`ROLE_ADMIN`または`SUPER`に更新します[＃13932](https://github.com/pingcap/tidb/pull/13932)
    -   MySQLの動作との互換性を維持するために、TiDBの動作を現在のデータベースの使用から`GRANT`ステートメントでデータベース名が指定されていない場合の`No database selected`エラーの報告に変更し[＃13784](https://github.com/pingcap/tidb/pull/13784) 。
    -   MySQLの動作との一貫性を保つために、ユーザーが対応するスキーマの特権を持っている場合にのみ実行可能な`REVOKE`ステートメントの実行特権を`SuperPriv`から`REVOKE`に変更します[＃13306](https://github.com/pingcap/tidb/pull/13306)
    -   `GRANT ALL`構文に[＃13943](https://github.com/pingcap/tidb/pull/13943)が含まれていない場合に、ターゲットユーザーに`GrantPriv`が誤って付与される問題を修正し`WITH GRANT OPTION` 。
    -   `LoadDataInfo`が[＃13980](https://github.com/pingcap/tidb/pull/13980)の呼び出しに失敗したときに、エラーメッセージに`LOAD DATA`ステートメントの誤った動作の原因が含まれていないという問題を修正し`addRecord` 。
    -   クエリ内の複数のSQLステートメントが同じ`StartTime`を共有するため、間違った遅いクエリ情報が出力される問題を修正し[＃13898](https://github.com/pingcap/tidb/pull/13898) 。
    -   `batchClient`が大規模なトランザクションを処理するときにメモリがリークする可能性がある問題を修正します[＃14032](https://github.com/pingcap/tidb/pull/14032)
    -   `system_time_zone`が常に`CST`として表示され、TiDBの`system_time_zone`が`mysql.tidb`テーブル[＃14086](https://github.com/pingcap/tidb/pull/14086)の`systemTZ`から取得されるという問題を修正します。
    -   `GRANT ALL`構文がユーザーにすべての特権を付与しないという問題を修正します[＃14092](https://github.com/pingcap/tidb/pull/14092)
    -   `Priv_create_user`特権が`CREATE ROLE`および[＃14088](https://github.com/pingcap/tidb/pull/14088)に対して無効であるという問題を修正し`DROP ROLE` 。
    -   `ErrInvalidFieldSize`のエラーコードを`1105(Unknow Error)`から[＃13737](https://github.com/pingcap/tidb/pull/13737)に変更し`3013`
    -   `SHUTDOWN`コマンドを追加してTiDBサーバーを停止し、 `ShutdownPriv`特権を追加します[＃14104](https://github.com/pingcap/tidb/pull/14104)
    -   `DROP ROLE`ステートメントのアトミック性の問題を修正して、TiDBがステートメント[＃14130](https://github.com/pingcap/tidb/pull/14130)の実行に失敗したときに一部のロールが予期せず削除されないようにします。
    -   TiDBバージョンを3.0にアップグレードすると、 `SHOW VARIABLE`の結果のうち`tidb_enable_window_function`つが誤って`1`を出力する問題を修正し、誤った結果を[＃14131](https://github.com/pingcap/tidb/pull/14131)に置き換え`0` 。
    -   1TiKVノードがオフラインのときに継続的に再試行するために`gcworker`がリークする可能性がある問題を修正します[＃14106](https://github.com/pingcap/tidb/pull/14106)
    -   問題追跡[＃14138](https://github.com/pingcap/tidb/pull/14138)の使いやすさを向上させるために、遅いクエリログにbinlogを`Prewrite`回記録します。
    -   `tidb_enable_table_partition` [＃14091](https://github.com/pingcap/tidb/pull/14091)をサポートする`GLOBAL SCOPE`
    -   新しい特権が追加されたときに、新しく追加された特権が対応するユーザーに正しく付与されないために、ユーザー特権が欠落しているか、誤って追加されている可能性がある問題を修正します[＃14178](https://github.com/pingcap/tidb/pull/14178)
    -   TiKVサーバーが切断されたときに`rpcClient`が閉じないため、 `CheckStreamTimeoutLoop`つのゴルーチンがリークする可能性がある問題を修正します[＃14227](https://github.com/pingcap/tidb/pull/14227)
    -   証明書ベースの認証をサポートする（ [ユーザードキュメント](/certificate-authentication.md) ） [＃13955](https://github.com/pingcap/tidb/pull/13955)
-   取引
    -   新しいクラスタが作成されたときに、 `tidb_txn_mode`変数のデフォルト値を`""`から`"pessimistic"`に更新します[＃14171](https://github.com/pingcap/tidb/pull/14171)
    -   トランザクションが再試行されたときに単一ステートメントのロック待機時間がリセットされないため、ペシミスティックトランザクションに対してロック待機時間が長すぎるという問題を修正します[＃13990](https://github.com/pingcap/tidb/pull/13990)
    -   悲観的なトランザクションモード[＃14050](https://github.com/pingcap/tidb/pull/14050)では、変更されていないデータのロックが解除されるため、間違ったデータが読み取られる可能性があるという問題を修正します。
    -   mocktikv [＃14175](https://github.com/pingcap/tidb/pull/14175)でプリライトが実行されるとトランザクションタイプが区別されないため、挿入値の制限チェックが繰り返される問題を修正しました。
    -   `session.TxnState`が[＃13988](https://github.com/pingcap/tidb/pull/13988)の場合、トランザクションが正しく処理されないため、パニックを修正し`Invalid` 。
    -   mocktikvの`ErrConfclit`構造に35が含まれて[＃14080](https://github.com/pingcap/tidb/pull/14080)ない問題を修正し`ConflictCommitTS`
    -   ロックを解決した後、TiDBがロックタイムアウトを正しくチェックしないためにトランザクションがブロックされる問題を修正します[＃14083](https://github.com/pingcap/tidb/pull/14083)
-   モニター
    -   35に`pessimistic_lock_keys_duration` [＃14194](https://github.com/pingcap/tidb/pull/14194)監視項目を追加し`LockKeys`

## TiKV {#tikv}

-   コプロセッサー
    -   コプロセッサー[＃6051](https://github.com/tikv/tikv/pull/6051)でエラーが発生した場合、出力ログのレベルを`error`から`warn`に変更します。
    -   tidb-server [＃6069](https://github.com/tikv/tikv/pull/6096)の更新動作との一貫性を保つために、統計サンプリングデータの更新動作を行の直接更新から挿入前の削除に変更します。
-   ラフトストア
    -   `destroy`のメッセージを`peerfsm`に繰り返し送信し、 `peerfsm`が複数回破壊されることによって引き起こされるパニックを修正します[＃6297](https://github.com/tikv/tikv/pull/6297)
    -   デフォルト値の`split-region-on-table`を`true`から`false`に更新して、デフォルトでリージョンをテーブルで分割できないようにします[＃6253](https://github.com/tikv/tikv/pull/6253)
-   エンジン
    -   RocksDBイテレータエラーが極端な条件で正しく処理されないために空のデータが返される可能性がある問題を修正します[＃6326](https://github.com/tikv/tikv/pull/6326)
-   取引
    -   TiKVがキーへのデータの書き込みに失敗し、悲観的なロックが誤ってクリーンアップされたためにGCがブロックされる問題を修正します[＃6354](https://github.com/tikv/tikv/pull/6354)
    -   悲観的なロック待機メカニズムを最適化して、ロックの競合が深刻なシナリオでのパフォーマンスを向上させます[＃6296](https://github.com/tikv/tikv/pull/6296)
-   デフォルト値の`tikv_alloc`を`tikv_alloc/default`から[＃6206](https://github.com/tikv/tikv/pull/6206)に更新し`jemalloc` 。

## PD {#pd}

-   クライアント
    -   `context`を使用してクライアントを作成し、新しいクライアントを作成するときにタイムアウト期間を設定することをサポートします[＃1994](https://github.com/pingcap/pd/pull/1994)
    -   `KeepAlive`の接続の作成をサポート[＃2035](https://github.com/pingcap/pd/pull/2035)
-   `/api/v1/regions`の[＃1986](https://github.com/pingcap/pd/pull/1986)を最適化する
-   `tombstone`の状態のストアを削除するとパニックが発生する可能性がある問題を修正します[＃2038](https://github.com/pingcap/pd/pull/2038)
-   ディスク[＃2011](https://github.com/pingcap/pd/issues/2011)からリージョン情報をロードするときに、オーバーラップしたリージョンが誤って削除される問題を修正し[＃2040](https://github.com/pingcap/pd/pull/2040) 。
-   etcdをv3.4.0からv3.4.3にアップグレードします（アップグレード後は、pd-recoverを使用してのみetcdを劣化させることができることに注意してください） [＃2058](https://github.com/pingcap/pd/pull/2058)

## ツール {#tools}

-   TiDB Binlog
    -   PumpがDDLコミットされたbinlog1を受信しないため、 [＃853](https://github.com/pingcap/tidb-binlog/pull/853)が無視される問題を修正します。

## TiDB Ansible {#tidb-ansible}

-   簡略化した構成項目を元に戻す[＃1053](https://github.com/pingcap/tidb-ansible/pull/1053)
-   ローリングアップデートを実行するときにTiDBバージョンをチェックするためのロジックを最適化する[＃1056](https://github.com/pingcap/tidb-ansible/pull/1056)
-   TiSparkをv2.1.81にアップグレードします[＃1061](https://github.com/pingcap/tidb-ansible/pull/1061)
-   PDの役割の監視項目がGrafana1に誤って表示される問題を修正し[＃1065](https://github.com/pingcap/tidb-ansible/pull/1065)
-   Grafana5の[＃1071](https://github.com/pingcap/tidb-ansible/pull/1071)詳細ページで`Thread Voluntary Context Switches`と`Thread Nonvoluntary Context Switches`の監視項目を最適化する

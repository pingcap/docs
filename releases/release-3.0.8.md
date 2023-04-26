---
title: TiDB 3.0.8 Release Notes
---

# TiDB 3.0.8 リリースノート {#tidb-3-0-8-release-notes}

発売日：2019年12月31日

TiDB バージョン: 3.0.8

TiDB アンシブル バージョン: 3.0.8

## TiDB {#tidb}

-   SQL オプティマイザー
    -   タイミングの悪いキャッシュ更新によって引き起こされた誤った SQL バインディング プランを修正する[#13891](https://github.com/pingcap/tidb/pull/13891)
    -   SQL ステートメントにシンボル リストが含まれている場合、SQL バインディングが無効になる可能性がある問題を修正します[#14004](https://github.com/pingcap/tidb/pull/14004)
    -   SQL ステートメントが`;` [#14113](https://github.com/pingcap/tidb/pull/14113)で終わるため、SQL バインディングを作成または削除できない問題を修正します。
    -   `PhysicalUnionScan`演算子が間違った統計を設定するため、間違った SQL クエリ プランが選択される可能性がある問題を修正します[#14133](https://github.com/pingcap/tidb/pull/14133)
    -   `minAutoAnalyzeRatio`制限を外して`autoAnalyze`をタイムリーに[#14015](https://github.com/pingcap/tidb/pull/14015)
-   SQL 実行エンジン
    -   `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT`構文でエラーが報告される可能性があり、 `DEFAULT`式の使用法を仮想生成列と組み合わせるとエラー[#13682](https://github.com/pingcap/tidb/pull/13682)が報告される可能性があるという問題を修正します。
    -   文字列を float に変換するときに`INSERT`ステートメントがエラーを報告する可能性がある問題を修正します[#14011](https://github.com/pingcap/tidb/pull/14011)
    -   `HashAgg` executor の同時実行値が正しく初期化されていないために集計操作の効果が低い場合がある問題を修正します[#13811](https://github.com/pingcap/tidb/pull/13811)
    -   句が括弧内にある場合、 `group by item`の実行でエラーが報告される問題を修正します[#13658](https://github.com/pingcap/tidb/pull/13658)
    -   TiDB が`group by item` [#14014](https://github.com/pingcap/tidb/pull/14014)を正しく計算しないため、 `OUTER JOIN`を実行するとエラーが報告される可能性がある問題を修正します。
    -   レンジ分割テーブルにレンジを超えるデータを書き込むとエラーメッセージが正しく表示されない問題を修正[#14107](https://github.com/pingcap/tidb/pull/14107)
    -   MySQL 8 がすぐに破棄されること`PadCharToFullLength`考慮して、 [広報番号 10124](https://github.com/pingcap/tidb/pull/10124)元に戻し、 `PadCharToFullLength`効果をキャンセルして、特殊なケースで予期しないクエリ結果を回避します[#14157](https://github.com/pingcap/tidb/pull/14157)
    -   `ExplainExec` [#14226](https://github.com/pingcap/tidb/pull/14226)での保証されていない`close()`呼び出しによって引き起こされる`EXPLAIN ANALYZE`ステートメントを実行するときのゴルーチン リークの問題を修正します。
-   DDL
    -   `change column`のエラーメッセージ出力を最適化`modify column`て分かりやすくする[#13796](https://github.com/pingcap/tidb/pull/13796)
    -   分割されたテーブルのリージョンの分割をサポートするために`SPLIT PARTITION TABLE`構文を追加します[#13929](https://github.com/pingcap/tidb/pull/13929)
    -   インデックスの作成時にインデックスの長さが正しくチェックされないため、インデックスの長さが[#13779](https://github.com/pingcap/tidb/pull/13779)バイトを超えてもエラーが報告されない問題を修正します。
    -   分割されたテーブルにインデックスを追加するのに時間がかかりすぎるため、 `GC life time is shorter than transaction duration`エラー メッセージが報告される場合がある問題を修正します[#14132](https://github.com/pingcap/tidb/pull/14132)
    -   `DROP COLUMN` / `MODIFY COLUMN` / `CHANGE COLUMN`実行時に外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`実行時のpanicを修正[#14105](https://github.com/pingcap/tidb/pull/14105)
-   サーバ
    -   ステートメントの概要の改善:
        -   多数の SQL メトリック フィールド[#14168](https://github.com/pingcap/tidb/pull/14168)追加して、SQL ステートメントをより詳細に分析しやすくする[#14151](https://github.com/pingcap/tidb/pull/14151)
        -   `stmt-summary.refresh-interval`パラメータを追加して、古いデータを`events_statements_summary_by_digest`テーブルから`events_statements_summary_by_digest_history`テーブルに移動するかどうかを制御します (デフォルトの間隔: 30 分) [#14161](https://github.com/pingcap/tidb/pull/14161)
        -   `events_statements_summary_by_digest_history`テーブルを追加して、古いデータを`events_statements_summary_by_digest` [#14166](https://github.com/pingcap/tidb/pull/14166)に保存します
    -   RBAC関連の内部SQL文実行時にbinlogが誤って出力される問題を修正[#13890](https://github.com/pingcap/tidb/pull/13890)
    -   TiDBサーバーバージョン[#13906](https://github.com/pingcap/tidb/pull/13906)を変更する機能を制御する`server-version`構成項目を追加します。
    -   HTTP インターフェイスを使用して TiDBbinlogの書き込みを回復する機能を追加します[#13892](https://github.com/pingcap/tidb/pull/13892)
    -   `GRANT roles TO user`で必要な権限を`GrantPriv`から`ROLE_ADMIN`または`SUPER`に更新して、MySQL の動作との一貫性を維持します[#13932](https://github.com/pingcap/tidb/pull/13932)
    -   MySQL の動作との互換性を維持するために、TiDB の動作を現在のデータベースの使用から`GRANT`ステートメントでデータベース名が指定されていない場合に`No database selected`エラーを報告するように変更します[#13784](https://github.com/pingcap/tidb/pull/13784)
    -   `REVOKE`ステートメントの実行権限を`SuperPriv`から`REVOKE`に変更して、ユーザーが対応するスキーマの権限を持っている場合にのみ実行できるようにし、MySQL の動作との一貫性を維持します[#13306](https://github.com/pingcap/tidb/pull/13306)
    -   `GRANT ALL`構文に`WITH GRANT OPTION` [#13943](https://github.com/pingcap/tidb/pull/13943)が含まれていない場合、ターゲット ユーザーに誤って`GrantPriv`が付与される問題を修正します。
    -   `LoadDataInfo`が`addRecord` [#13980](https://github.com/pingcap/tidb/pull/13980)の呼び出しに失敗した場合に、 `LOAD DATA`ステートメントの間違った動作の原因がエラー メッセージに含まれていない問題を修正します。
    -   クエリ内の複数の SQL ステートメントが同じ`StartTime` [#13898](https://github.com/pingcap/tidb/pull/13898)を共有するため、間違ったスロークエリ情報が出力される問題を修正します。
    -   `batchClient`大規模なトランザクションを処理するとメモリリークが発生する可能性がある問題を修正します[#14032](https://github.com/pingcap/tidb/pull/14032)
    -   `system_time_zone`が常に`CST`と表示され、TiDB の`system_time_zone` `mysql.tidb`テーブル[#14086](https://github.com/pingcap/tidb/pull/14086)の`systemTZ`から取得される問題を修正
    -   `GRANT ALL`構文がユーザー[#14092](https://github.com/pingcap/tidb/pull/14092)にすべての権限を付与しないという問題を修正します。
    -   `Priv_create_user`権限が`CREATE ROLE`と`DROP ROLE` [#14088](https://github.com/pingcap/tidb/pull/14088)で無効になる問題を修正
    -   `ErrInvalidFieldSize`のエラー コードを`1105(Unknow Error)`から`3013` [#13737](https://github.com/pingcap/tidb/pull/13737)に変更します。
    -   `SHUTDOWN`コマンドを追加して TiDBサーバーを停止し、 `ShutdownPriv`特権[#14104](https://github.com/pingcap/tidb/pull/14104)を追加します。
    -   `DROP ROLE`ステートメントの原子性の問題を修正して、TiDB がステートメントの実行に失敗したときに一部のロールが予期せず削除されないようにします[#14130](https://github.com/pingcap/tidb/pull/14130)
    -   TiDB のバージョンを 3.0 にアップグレードすると、 `SHOW VARIABLE`の結果の`tidb_enable_window_function`誤って`1`出力する問題を修正し、誤った結果を`0` [#14131](https://github.com/pingcap/tidb/pull/14131)に置き換えます。
    -   TiKV ノードがオフラインのときに`gcworker`継続的にリトライするため、ゴルーチンがリークする可能性がある問題を修正します[#14106](https://github.com/pingcap/tidb/pull/14106)
    -   問題追跡の使いやすさを向上させるために、スロー クエリ ログにbinlog を`Prewrite`回記録します[#14138](https://github.com/pingcap/tidb/pull/14138)
    -   `tidb_enable_table_partition`変数サポートを`GLOBAL SCOPE` [#14091](https://github.com/pingcap/tidb/pull/14091)にする
    -   新しい権限が追加されたときに、新しく追加された権限が対応するユーザーに正しく付与されないため、ユーザー権限が失われたり、誤って追加されたりする可能性がある問題を修正します[#14178](https://github.com/pingcap/tidb/pull/14178)
    -   TiKVサーバーが切断されたときに`rpcClient`閉じないため、 `CheckStreamTimeoutLoop`ゴルーチンがリークする可能性がある問題を修正[#14227](https://github.com/pingcap/tidb/pull/14227)
    -   証明書ベースの認証をサポート ( [ユーザー文書](/certificate-authentication.md) ) [#13955](https://github.com/pingcap/tidb/pull/13955)
-   トランザクション
    -   新しいクラスターが作成されるときに、 `tidb_txn_mode`変数のデフォルト値を`""`から`"pessimistic"`に更新します[#14171](https://github.com/pingcap/tidb/pull/14171)
    -   トランザクションの再試行時に単一ステートメントのロック待機時間がリセットされないため、悲観的トランザクションのロック待機時間が長すぎる問題を修正します[#13990](https://github.com/pingcap/tidb/pull/13990)
    -   悲観的トランザクションモード[#14050](https://github.com/pingcap/tidb/pull/14050)で変更されていないデータがロック解除されているため、間違ったデータが読み取られる可能性がある問題を修正します。
    -   [#14175](https://github.com/pingcap/tidb/pull/14175)でプリライトを行うとトランザクションの種類が区別されないため、挿入値の制限チェックが繰り返される問題を修正
    -   `session.TxnState`が`Invalid` [#13988](https://github.com/pingcap/tidb/pull/13988)の場合、トランザクションが正しく処理されないため、panicを修正します。
    -   mocktikv の`ErrConfclit`構造体に`ConflictCommitTS` [#14080](https://github.com/pingcap/tidb/pull/14080)含まれていない問題を修正
    -   ロックを解決した後、TiDB がロック タイムアウトを正しくチェックしないためにトランザクションがブロックされる問題を修正します[#14083](https://github.com/pingcap/tidb/pull/14083)
-   モニター
    -   `LockKeys` [#14194](https://github.com/pingcap/tidb/pull/14194)に`pessimistic_lock_keys_duration`監視項目を追加

## TiKV {#tikv}

-   コプロセッサー
    -   コプロセッサー[#6051](https://github.com/tikv/tikv/pull/6051)でエラーが発生した場合の出力ログのレベルを`error`から`warn`に変更します
    -   tidb-server [#6069](https://github.com/tikv/tikv/pull/6096)の更新動作との一貫性を保つために、統計サンプリング データの更新動作を、行を直接更新するから、挿入する前に削除するように変更します。
-   Raftstore
    -   `destroy`メッセージを`peerfsm`と`peerfsm`に繰り返し送信することによって引き起こされるpanicを修正します[#6297](https://github.com/tikv/tikv/pull/6297)
    -   デフォルト値`split-region-on-table`を`true`から`false`に更新して、デフォルトでテーブルごとのリージョンの分割を無効にします[#6253](https://github.com/tikv/tikv/pull/6253)
-   エンジン
    -   RocksDB イテレータ エラーが極端な状況で正しく処理されないため、空のデータが返される可能性がある問題を修正します[#6326](https://github.com/tikv/tikv/pull/6326)
-   トランザクション
    -   悲観的ロックが誤ってクリーンアップされるため、TiKV がキーにデータを書き込むことができず、GC がブロックされる問題を修正します[#6354](https://github.com/tikv/tikv/pull/6354)
    -   悲観的ロック待機メカニズムを最適化して、ロックの競合が深刻なシナリオでのパフォーマンスを向上させます[#6296](https://github.com/tikv/tikv/pull/6296)
-   デフォルト値の`tikv_alloc`を`tikv_alloc/default`から`jemalloc` [#6206](https://github.com/tikv/tikv/pull/6206)に更新します。

## PD {#pd}

-   クライアント
    -   `context`を使用してクライアントを作成し、新しいクライアントを作成するときにタイムアウト期間を設定することをサポートします[#1994](https://github.com/pingcap/pd/pull/1994)
    -   `KeepAlive`接続の作成をサポート[#2035](https://github.com/pingcap/pd/pull/2035)
-   `/api/v1/regions` API [#1986](https://github.com/pingcap/pd/pull/1986)のパフォーマンスを最適化する
-   `tombstone`状態のストアを削除するとpanicが発生する可能性がある問題を修正します[#2038](https://github.com/pingcap/pd/pull/2038)
-   ディスク[#2011](https://github.com/pingcap/pd/issues/2011) 、 [#2040](https://github.com/pingcap/pd/pull/2040)からリージョン情報をロードするときに、重複するリージョンが誤って削除される問題を修正します。
-   etcd を v3.4.0 から v3.4.3 にアップグレードします (アップグレード後は、pd-recover を使用してのみ etcd を劣化させることができることに注意してください) [#2058](https://github.com/pingcap/pd/pull/2058)

## ツール {#tools}

-   TiDBBinlog
    -   Pump がDDL コミットされたbinlog [#853](https://github.com/pingcap/tidb-binlog/pull/853)を受信しないため、 binlogが無視される問題を修正します。

## TiDB アンシブル {#tidb-ansible}

-   単純化された構成アイテム[#1053](https://github.com/pingcap/tidb-ansible/pull/1053)を元に戻す
-   ローリング更新時の TiDB のバージョン確認ロジックを最適化する[#1056](https://github.com/pingcap/tidb-ansible/pull/1056)
-   TiSpark を v2.1.8 にアップグレードする[#1061](https://github.com/pingcap/tidb-ansible/pull/1061)
-   Grafana [#1065](https://github.com/pingcap/tidb-ansible/pull/1065)で PD ロールの監視項目が誤って表示される問題を修正
-   Grafana [#1071](https://github.com/pingcap/tidb-ansible/pull/1071)の TiKV 詳細ページの最適化`Thread Voluntary Context Switches`と`Thread Nonvoluntary Context Switches`の監視項目

---
title: TiDB 3.0.8 Release Notes
---

# TiDB 3.0.8 リリースノート {#tidb-3-0-8-release-notes}

発売日：2019年12月31日

TiDB バージョン: 3.0.8

TiDB Ansible バージョン: 3.0.8

## TiDB {#tidb}

-   SQLオプティマイザー
    -   時期尚早のキャッシュ更新によって引き起こされる間違った SQL バインディング プランを修正する[#13891](https://github.com/pingcap/tidb/pull/13891)
    -   SQL ステートメントにシンボル リスト[#14004](https://github.com/pingcap/tidb/pull/14004)が含まれている場合、SQL バインディングが無効になる可能性がある問題を修正します。
    -   SQL ステートメントが`;` [#14113](https://github.com/pingcap/tidb/pull/14113)で終わるため、SQL バインディングを作成または削除できない問題を修正します。
    -   `PhysicalUnionScan`演算子が間違った統計[#14133](https://github.com/pingcap/tidb/pull/14133)を設定するため、間違った SQL クエリ プランが選択される可能性がある問題を修正します。
    -   `minAutoAnalyzeRatio`制限を削除すると、 `autoAnalyze`がよりタイムリーに[#14015](https://github.com/pingcap/tidb/pull/14015)になります
-   SQL実行エンジン
    -   `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT`構文でエラーが報告される可能性があり、 `DEFAULT`式の使用と仮想生成列を組み合わせるとエラーが報告される可能性があるという問題を修正します[#13682](https://github.com/pingcap/tidb/pull/13682)
    -   文字列を float [#14011](https://github.com/pingcap/tidb/pull/14011)に変換するときに`INSERT`ステートメントでエラーが報告される可能性がある問題を修正します。
    -   `HashAgg`エグゼキュータの同時実行値が正しく初期化されていないため、集計操作の効果が低い場合がある問題を修正します[#13811](https://github.com/pingcap/tidb/pull/13811)
    -   句が括弧内にある場合に`group by item`の実行でエラーが報告される問題を修正します[#13658](https://github.com/pingcap/tidb/pull/13658)
    -   TiDB が`group by item` [#14014](https://github.com/pingcap/tidb/pull/14014)を誤って計算するため、 `OUTER JOIN`を実行するとエラーが報告される可能性がある問題を修正
    -   範囲を超えるデータが範囲パーティション テーブル[#14107](https://github.com/pingcap/tidb/pull/14107)に書き込まれるときにエラー メッセージが不正確になる問題を修正します。
    -   MySQL 8 がすぐに`PadCharToFullLength`破棄することを考慮して、特殊な場合に予期しないクエリ結果を回避するために[PR #10124](https://github.com/pingcap/tidb/pull/10124)元に戻し、 `PadCharToFullLength`効果をキャンセルします[#14157](https://github.com/pingcap/tidb/pull/14157)
    -   `ExplainExec` [#14226](https://github.com/pingcap/tidb/pull/14226)での保証されていない`close()`呼び出しによって引き起こされる`EXPLAIN ANALYZE`ステートメントを実行するときの goroutine リークの問題を修正します。
-   DDL
    -   `change column` / `modify column`のエラーメッセージ出力を最適化して分かりやすくする[#13796](https://github.com/pingcap/tidb/pull/13796)
    -   パーティション テーブル[#13929](https://github.com/pingcap/tidb/pull/13929)のリージョンの分割をサポートする`SPLIT PARTITION TABLE`構文を追加します。
    -   インデックスの作成時にインデックスの長さが誤ってチェックされるため、インデックスの長さが 3072 バイトを超えてもエラーが報告されない問題を修正します[#13779](https://github.com/pingcap/tidb/pull/13779)
    -   パーティション テーブル[#14132](https://github.com/pingcap/tidb/pull/14132)にインデックスを追加するのに時間がかかりすぎるため、 `GC life time is shorter than transaction duration`エラー メッセージが報告される可能性がある問題を修正します。
    -   `DROP COLUMN` / `MODIFY COLUMN` / `CHANGE COLUMN`の実行時に外部キーがチェックされないため、 `SELECT * FROM information_schema.KEY_COLUMN_USAGE`の実行時にパニックが発生するpanicを修正[#14105](https://github.com/pingcap/tidb/pull/14105)
-   サーバ
    -   ステートメントの概要の改善:
        -   多数の SQL メトリック フィールドを追加して、SQL ステートメントをより詳細に分析し[#14168](https://github.com/pingcap/tidb/pull/14168)します[#14151](https://github.com/pingcap/tidb/pull/14151)
        -   `stmt-summary.refresh-interval`パラメータを追加して、古いデータを`events_statements_summary_by_digest`テーブルから`events_statements_summary_by_digest_history`テーブルに移動するかどうかを制御します (デフォルトの間隔: 30 分) [#14161](https://github.com/pingcap/tidb/pull/14161)
        -   `events_statements_summary_by_digest_history`テーブルを追加して、古いデータを`events_statements_summary_by_digest` [#14166](https://github.com/pingcap/tidb/pull/14166)に保存します
    -   RBAC 関連の内部 SQL ステートメントが実行されると、 binlogが誤って出力される問題を修正します[#13890](https://github.com/pingcap/tidb/pull/13890)
    -   TiDBサーバーバージョン[#13906](https://github.com/pingcap/tidb/pull/13906)を変更する機能を制御する`server-version`構成項目を追加します。
    -   HTTP インターフェースを使用して TiDBbinlogの書き込みを回復する機能を追加[#13892](https://github.com/pingcap/tidb/pull/13892)
    -   MySQL の動作との一貫性を保つために、 `GRANT roles TO user`で必要な権限を`GrantPriv`から`ROLE_ADMIN`または`SUPER`に更新します[#13932](https://github.com/pingcap/tidb/pull/13932)
    -   MySQL の動作[#13784](https://github.com/pingcap/tidb/pull/13784)の互換性を維持するために、TiDB の動作を現在のデータベースの使用から`GRANT`ステートメントでデータベース名が指定されていない場合に`No database selected`エラーを報告するように変更します。
    -   MySQL の動作[#13306](https://github.com/pingcap/tidb/pull/13306)の一貫性を保つために、ユーザーが対応するスキーマに対する権限を持っている場合にのみ実行可能となるように、 `REVOKE`ステートメントの実行権限を`SuperPriv`から`REVOKE`に変更します。
    -   `GRANT ALL`構文に`WITH GRANT OPTION` [#13943](https://github.com/pingcap/tidb/pull/13943)が含まれていない場合、対象ユーザーに誤って`GrantPriv`が付与されてしまう問題を修正
    -   `LoadDataInfo`が`addRecord` [#13980](https://github.com/pingcap/tidb/pull/13980)の呼び出しに失敗した場合の`LOAD DATA`ステートメントの誤った動作の原因がエラー メッセージに含まれていない問題を修正します。
    -   クエリ内の複数の SQL ステートメントが同じ`StartTime` [#13898](https://github.com/pingcap/tidb/pull/13898)を共有しているため、間違ったスロー クエリ情報が出力される問題を修正
    -   `batchClient`大きなトランザクションを処理するときにメモリが発生する可能性がある問題を修正[#14032](https://github.com/pingcap/tidb/pull/14032)
    -   `system_time_zone`が常に`CST`として表示され、TiDB の`system_time_zone` `mysql.tidb`テーブルの`systemTZ`から取得される問題を修正[#14086](https://github.com/pingcap/tidb/pull/14086)
    -   `GRANT ALL`構文ではユーザー[#14092](https://github.com/pingcap/tidb/pull/14092)にすべての権限が付与されないという問題を修正します。
    -   `Priv_create_user`権限が`CREATE ROLE`と`DROP ROLE`では無効になる問題を修正[#14088](https://github.com/pingcap/tidb/pull/14088)
    -   `ErrInvalidFieldSize`のエラーコードを`1105(Unknow Error)`から`3013`に変更します[#13737](https://github.com/pingcap/tidb/pull/13737)
    -   TiDBサーバーを停止する`SHUTDOWN`コマンドを追加し、 `ShutdownPriv`特権[#14104](https://github.com/pingcap/tidb/pull/14104)を追加します。
    -   TiDB がステートメント[#14130](https://github.com/pingcap/tidb/pull/14130)の実行に失敗したときに一部のロールが予期せず削除されるのを避けるために、ステートメント`DROP ROLE`のアトミック性の問題を修正しました。
    -   TiDB バージョンが 3.0 にアップグレードされると、 `SHOW VARIABLE`結果の`tidb_enable_window_function`誤って`1`出力する問題を修正し、間違った結果を`0` [#14131](https://github.com/pingcap/tidb/pull/14131)に置き換えます。
    -   TiKV ノードがオフラインのときに`gcworker`が継続的に再試行されるため、ゴルーチンがリークする可能性がある問題を修正します[#14106](https://github.com/pingcap/tidb/pull/14106)
    -   問題追跡の使いやすさを向上させるために、binlogをスロー クエリ ログに`Prewrite`回記録します[#14138](https://github.com/pingcap/tidb/pull/14138)
    -   `tidb_enable_table_partition`変数を`GLOBAL SCOPE` [#14091](https://github.com/pingcap/tidb/pull/14091)サポートにする
    -   新しい権限を追加するときに、新しく追加された権限が該当するユーザーに正しく付与されず、ユーザー権限が欠落しているか、誤って追加される可能性がある問題を修正します[#14178](https://github.com/pingcap/tidb/pull/14178)
    -   TiKVサーバーが切断されたときに`rpcClient`閉じないため、 `CheckStreamTimeoutLoop`ゴルーチンがリークする可能性がある問題を修正[#14227](https://github.com/pingcap/tidb/pull/14227)
    -   証明書ベースの認証をサポート ( [ユーザードキュメント](/certificate-authentication.md) ) [#13955](https://github.com/pingcap/tidb/pull/13955)
-   トランザクション
    -   新しいクラスターの作成時に`tidb_txn_mode`変数のデフォルト値を`""`から`"pessimistic"`に更新します[#14171](https://github.com/pingcap/tidb/pull/14171)
    -   トランザクションの再試行時に単一ステートメントのロック待機時間がリセットされないため、悲観的トランザクションに対してロック待機時間が長すぎる問題を修正します[#13990](https://github.com/pingcap/tidb/pull/13990)
    -   悲観的トランザクションモード[#14050](https://github.com/pingcap/tidb/pull/14050)で未変更データのロックが解除されるため、誤ったデータが読み込まれる可能性がある問題を修正
    -   mocktikv [#14175](https://github.com/pingcap/tidb/pull/14175)で事前書き込みが実行されるときにトランザクション タイプが区別されないため、挿入値の制限チェックが繰り返される問題を修正しました。
    -   `session.TxnState`が`Invalid` [#13988](https://github.com/pingcap/tidb/pull/13988)の場合にトランザクションが正しく処理されないため、panicを修正しました。
    -   mocktikv の`ErrConfclit`構造体に`ConflictCommitTS` [#14080](https://github.com/pingcap/tidb/pull/14080)含まれていない問題を修正
    -   TiDB がロック[#14083](https://github.com/pingcap/tidb/pull/14083)を解決した後にロック タイムアウトを正しくチェックしないため、トランザクションがブロックされる問題を修正します。
-   モニター
    -   `LockKeys` [#14194](https://github.com/pingcap/tidb/pull/14194)に監視項目を`pessimistic_lock_keys_duration`追加

## TiKV {#tikv}

-   コプロセッサー
    -   コプロセッサー[#6051](https://github.com/tikv/tikv/pull/6051)でエラーが発生した場合の出力ログのレベルを`error`から`warn`に変更
    -   tidb-server [#6069](https://github.com/tikv/tikv/pull/6096)の更新動作との一貫性を保つために、統計サンプリング データの更新動作を行の直接更新から挿入前の削除に変更しました。
-   Raftstore
    -   `destroy`メッセージを`peerfsm`に繰り返し送信し、 `peerfsm`複数回破棄されることによって引き起こされるpanicを修正[#6297](https://github.com/tikv/tikv/pull/6297)
    -   デフォルト値`split-region-on-table`を`true`から`false`に更新して、デフォルトでテーブルによるリージョンの分割を無効にします[#6253](https://github.com/tikv/tikv/pull/6253)
-   エンジン
    -   RocksDB イテレータエラーが極端な条件で正しく処理されないため、空のデータが返される可能性がある問題を修正します[#6326](https://github.com/tikv/tikv/pull/6326)
-   トランザクション
    -   悲観的ロックが誤ってクリーンアップされるため、TiKV がキーへのデータの書き込みに失敗し、GC がブロックされる問題を修正します[#6354](https://github.com/tikv/tikv/pull/6354)
    -   悲観的ロック待機メカニズムを最適化して、ロックの競合が深刻なシナリオでのパフォーマンスを向上させます[#6296](https://github.com/tikv/tikv/pull/6296)
-   デフォルト値`tikv_alloc`を`tikv_alloc/default`から`jemalloc` [#6206](https://github.com/tikv/tikv/pull/6206)に更新します。

## PD {#pd}

-   クライアント
    -   `context`を使用したクライアントの作成と、新しいクライアントの作成時のタイムアウト期間の設定をサポート[#1994](https://github.com/pingcap/pd/pull/1994)
    -   `KeepAlive`接続[#2035](https://github.com/pingcap/pd/pull/2035)の作成をサポート
-   `/api/v1/regions` API [#1986](https://github.com/pingcap/pd/pull/1986)のパフォーマンスを最適化する
-   `tombstone`状態でストアを削除するとpanic[#2038](https://github.com/pingcap/pd/pull/2038)が発生する可能性がある問題を修正
-   ディスク[#2011](https://github.com/pingcap/pd/issues/2011)からリージョン情報をロード[#2040](https://github.com/pingcap/pd/pull/2040)際に、重複したリージョンが誤って削除される問題を修正
-   etcd を v3.4.0 から v3.4.3 にアップグレードします (アップグレード後は、pd-recover を使用して etcd をデグレードすることしかできないことに注意してください) [#2058](https://github.com/pingcap/pd/pull/2058)

## ツール {#tools}

-   TiDBBinlog
    -   PumpがDDL によってコミットされたbinlog[#853](https://github.com/pingcap/tidb-binlog/pull/853)を受信しないため、binlogが無視される問題を修正します。

## TiDB Ansible {#tidb-ansible}

-   簡素化された構成項目[#1053](https://github.com/pingcap/tidb-ansible/pull/1053)を元に戻す
-   ローリング アップデート[#1056](https://github.com/pingcap/tidb-ansible/pull/1056)の実行時に TiDB バージョンをチェックするロジックを最適化します。
-   TiSpark を v2.1.8 にアップグレードする[#1061](https://github.com/pingcap/tidb-ansible/pull/1061)
-   Grafana [#1065](https://github.com/pingcap/tidb-ansible/pull/1065)でPDロール監視項目が誤って表示される問題を修正
-   Grafana [#1071](https://github.com/pingcap/tidb-ansible/pull/1071)の TiKV 詳細ページの監視項目`Thread Voluntary Context Switches`と`Thread Nonvoluntary Context Switches`を最適化する

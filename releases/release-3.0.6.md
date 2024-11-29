---
title: TiDB 3.0.6 Release Notes
summary: TiDB 3.0.6 は、さまざまな修正と最適化を伴って 2019 年 11 月 28 日にリリースされました。このリリースには、SQL オプティマイザー、SQL 実行エンジン、サーバー、DDL、TiKV、PD、TiDB Binlog、およびTiDB Lightningの改善が含まれています。修正には、ウィンドウ関数 AST の問題、STREAM AGG()` のプッシュダウン、SQL バインディングの引用符の処理などが含まれます。TiKV の改善には、正確な `lock_manager`、`innodb_lock_wait_timeout` のサポート、および `tikv-ctl` を使用した GC I/O 制限の動的な変更が含まれます。PD の機能強化には、クライアント ログ レベルの引き下げと、タイムスタンプを生成するための警告ログが含まれます。TiDB BinlogとTiDB Lightningにも修正と改善が加えられました。
---

# TiDB 3.0.6 リリースノート {#tidb-3-0-6-release-notes}

発売日: 2019年11月28日

TiDB バージョン: 3.0.6

TiDB Ansible バージョン: 3.0.6

## ティビ {#tidb}

-   SQL オプティマイザー
    -   ウィンドウ関数 AST が SQL テキストを復元した後に結果が正しくない (たとえば、 `over w`が誤って`over (w)` [＃12933](https://github.com/pingcap/tidb/pull/12933)に復元される) 問題を修正しました。
    -   `STREAM AGG()`から`doubleRead` [＃12690](https://github.com/pingcap/tidb/pull/12690)に押し下げる問題を修正
    -   SQLバインディング[＃13117](https://github.com/pingcap/tidb/pull/13117)で引用符が正しく処理されない問題を修正
    -   `select max(_tidb_rowid) from t`シナリオを最適化してテーブル全体のスキャンを回避する[＃13095](https://github.com/pingcap/tidb/pull/13095)
    -   クエリステートメントに変数割り当て式が含まれている場合にクエリ結果が正しくない問題を修正[＃13231](https://github.com/pingcap/tidb/pull/13231)
    -   `UPDATE`文にサブクエリと生成された列の両方が含まれている場合に結果が正しくない問題を修正します。この文に異なるソース データベースからの同じ名前のテーブルが 2 つ含まれている場合に`UPDATE`文の実行エラーが発生する問題を修正します[＃13350](https://github.com/pingcap/tidb/pull/13350)
    -   ポイントクエリ[＃13416](https://github.com/pingcap/tidb/pull/13416)のサポート`_tidb_rowid`
    -   パーティションテーブル統計の誤った使用により、生成されたクエリ実行プランが正しくない問題を修正しました[＃13628](https://github.com/pingcap/tidb/pull/13628)
-   SQL実行エンジン
    -   年型[＃12745](https://github.com/pingcap/tidb/pull/12745)の無効な値を処理するときにTiDBがMySQLと互換性がない問題を修正
    -   `INSERT ON DUPLICATE UPDATE`文で`Chunk`再利用してメモリオーバーヘッド[＃12998](https://github.com/pingcap/tidb/pull/12998)を削減する
    -   `JSON_VALID`組み込み関数[＃13133](https://github.com/pingcap/tidb/pull/13133)のサポートを追加
    -   パーティションテーブル[＃13140](https://github.com/pingcap/tidb/pull/13140)で`ADMIN CHECK TABLE`実行をサポート
    -   `FAST ANALYZE`が空のテーブル[＃13343](https://github.com/pingcap/tidb/pull/13343)で実行されたときに発生するpanic問題を修正
    -   複数列インデックス[＃13394](https://github.com/pingcap/tidb/pull/13394)含む空のテーブルで`FAST ANALYZE`実行するとpanic問題を修正
    -   `WHERE`句に一意のキー[＃13382](https://github.com/pingcap/tidb/pull/13382)の等号条件が含まれている場合に、推定行数が 1 より大きくなる問題を修正しました。
    -   TiDB [＃13254](https://github.com/pingcap/tidb/pull/13254)で`Streaming`が有効になっている場合に返されるデータが重複する可能性がある問題を修正
    -   推定精度を向上させるために、count-minスケッチから上位N個の値を抽出します[＃13429](https://github.com/pingcap/tidb/pull/13429)
-   サーバ
    -   gRPC ダイヤルがタイムアウトすると、TiKV に送信されたリクエストがすぐに失敗するようにします[＃12926](https://github.com/pingcap/tidb/pull/12926)
    -   次の仮想テーブルを追加します: [＃13009](https://github.com/pingcap/tidb/pull/13009)
        -   `performance_schema.tidb_profile_allocs`
        -   `performance_schema.tidb_profile_block`
        -   `performance_schema.tidb_profile_cpu`
        -   `performance_schema.tidb_profile_goroutines`
    -   クエリが悲観的ロック[＃12989](https://github.com/pingcap/tidb/pull/12989)を待機しているときに`kill`コマンドが機能しない問題を修正
    -   悲観的ロックの取得に失敗し、トランザクションが単一のキー[＃12707](https://github.com/pingcap/tidb/pull/12707)変更のみを伴う場合は、非同期ロールバックを実行しないでください。
    -   領域分割のリクエストに対する応答が空の場合にpanic問題を修正[＃13092](https://github.com/pingcap/tidb/pull/13092)
    -   `PessimisticLock`ロックエラーを返したときに不要なバックオフを回避する[＃13116](https://github.com/pingcap/tidb/pull/13116)
    -   認識されない構成オプション[＃13272](https://github.com/pingcap/tidb/pull/13272)警告ログを出力して構成をチェックするための TiDB の動作を変更します。
    -   `/info/all`インターフェース[＃13187](https://github.com/pingcap/tidb/pull/13187)を介してすべての TiDB ノードのbinlogステータスの取得をサポート
    -   TiDB が接続を切断したときに goroutine がリークする可能性がある問題を修正[＃13251](https://github.com/pingcap/tidb/pull/13251)
    -   悲観的トランザクションで`innodb_lock_wait_timeout`パラメータを機能させて、悲観的ロック[＃13165](https://github.com/pingcap/tidb/pull/13165)のロック待機タイムアウトを制御する
    -   悲観的トランザクションクエリが強制終了されたときに、他のトランザクションが不必要に待機するのを防ぐために、悲観的トランザクション TTL の更新を停止します[＃13046](https://github.com/pingcap/tidb/pull/13046)
-   DDL
    -   TiDBの`SHOW CREATE VIEW`の実行結果がMySQL [＃12912](https://github.com/pingcap/tidb/pull/12912)の結果と一致しない問題を修正
    -   `union`に基づいて`View`作成するサポート (例: `create view v as select * from t1 union select * from t2` [＃12955](https://github.com/pingcap/tidb/pull/12955)
    -   `slow_query`テーブルにトランザクション関連のフィールドを追加します: [＃13072](https://github.com/pingcap/tidb/pull/13072)
        -   `Prewrite_time`
        -   `Commit_time`
        -   `Get_commit_ts_time`
        -   `Commit_backoff_time`
        -   `Backoff_types`
        -   `Resolve_lock_time`
        -   `Local_latch_wait_time`
        -   `Write_key`
        -   `Write_size`
        -   `Prewrite_region`
        -   `Txn_retry`
    -   テーブルが作成され、テーブルに`COLLATE` [＃13174](https://github.com/pingcap/tidb/pull/13174)が含まれている場合、列のシステムのデフォルトの文字セットではなく、テーブルの`COLLATE`使用します。
    -   テーブル作成時にインデックス名の長さを制限する[＃13310](https://github.com/pingcap/tidb/pull/13310)
    -   テーブル名を変更するときにテーブル名の長さがチェックされない問題を修正[＃13346](https://github.com/pingcap/tidb/pull/13346)
    -   TiDB [＃13522](https://github.com/pingcap/tidb/pull/13522)で主キーの追加/削除をサポートするために、 `alter-primary-key`構成 (デフォルトでは無効) を追加します。

## ティクヴ {#tikv}

-   `acquire_pessimistic_lock`インターフェースが間違った`txn_size` [＃5740](https://github.com/tikv/tikv/pull/5740)を返す問題を修正
-   パフォーマンスへの影響を減らすために、GCワーカーの1秒あたりの書き込みを制限します[＃5735](https://github.com/tikv/tikv/pull/5735)
-   `lock_manager`正確に[＃5845](https://github.com/tikv/tikv/pull/5845)する
-   悲観的ロック[＃5848](https://github.com/tikv/tikv/pull/5848)のサポート`innodb_lock_wait_timeout`
-   Titan [＃5720](https://github.com/tikv/tikv/pull/5720)の設定チェックを追加
-   GC I/O制限を動的に変更するためのtikv-ctlの使用をサポート: `tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [＃5957](https://github.com/tikv/tikv/pull/5957)
-   無駄な`clean up`リクエストを減らしてデッドロック検出器[＃5965](https://github.com/tikv/tikv/pull/5965)への負荷を軽減する
-   悲観的ロックの事前書き込みリクエストでTTLを減らさないようにする[＃6056](https://github.com/tikv/tikv/pull/6056)
-   Titan [＃5968](https://github.com/tikv/tikv/pull/5968)でBLOBファイルが見つからない問題を修正
-   Titan [＃6009](https://github.com/tikv/tikv/pull/6009)で`RocksDBOptions`効かない問題を修正

## PD {#pd}

-   各フィルターに`ActOn`ディメンションを追加して、各スケジューラとチェッカーがフィルターの影響を受けることを示します。また、使用されていない 2 つのフィルター ( `disconnectFilter`と`rejectLeaderFilter` [＃1911](https://github.com/pingcap/pd/pull/1911)を削除します。
-   PD [＃1867](https://github.com/pingcap/pd/pull/1867)でタイムスタンプを生成するのに 5 ミリ秒以上かかる場合は警告ログを出力します。
-   利用できないエンドポイントをクライアントに渡すときにクライアントのログレベルを下げる[＃1856](https://github.com/pingcap/pd/pull/1856)
-   gRPCメッセージパッケージが`region_syncer`レプリケーションプロセス[＃1952](https://github.com/pingcap/pd/pull/1952)で最大サイズを超える可能性がある問題を修正

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [＃788](https://github.com/pingcap/tidb-binlog/pull/788)で`initial-commit-ts`が「-1」に設定されている場合、PDから初期レプリケーションタイムスタンプを取得します。
    -   Drainerの`Checkpoint`storageをダウンストリームから分離し、MySQLまたはローカルファイル[＃790](https://github.com/pingcap/tidb-binlog/pull/790)への保存`Checkpoint`サポートする
    -   レプリケーション データベース/テーブル フィルタリングを構成するときに空の値を使用することで発生するDrainerpanicの問題を修正しました[＃801](https://github.com/pingcap/tidb-binlog/pull/801)
    -   Drainer がbinlogファイルをダウンストリームに適用できないためにpanicが発生した後、プロセスが終了せずにデッドロック状態になる問題を修正しました[＃807](https://github.com/pingcap/tidb-binlog/pull/807)
    -   gRPC の`GracefulStop` [＃817](https://github.com/pingcap/tidb-binlog/pull/817)が原因でPump が終了するときにブロックされる問題を修正しました。
    -   TiDB (v3.0.6 以降) で`DROP COLUMN`ステートメントの実行中に列が欠落しているbinlogを受信するとDrainer が失敗する問題を修正しました[＃827](https://github.com/pingcap/tidb-binlog/pull/827)
-   TiDB Lightning
    -   TiDBバックエンド[＃248](https://github.com/pingcap/tidb-lightning/pull/248)に`max-allowed-packet`構成（デフォルトでは64M）を追加します。

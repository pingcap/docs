---
title: TiDB 3.0.6 Release Notes
summary: TiDB 3.0.6は、さまざまな修正と最適化を伴い、2019年11月28日にリリースされました。このリリースには、SQLオプティマイザー、SQL実行エンジン、サーバー、DDL、TiKV、PD、TiDB Binlog、およびTiDB Lightningの改善が含まれています。修正には、ウィンドウ関数ASTの問題、STREAM AGG()`のプッシュダウン、SQLバインディングの引用符の処理などが含まれます。TiKVの改善には、正確な`lock_manager`、`innodb_lock_wait_timeout`のサポート、`tikv-ctl`を使用したGC I/O制限の動的な変更が含まれます。PDの機能強化には、クライアントログレベルの引き下げと、タイムスタンプ生成のための警告ログが含まれます。TiDB BinlogとTiDB Lightningにも修正と改善が加えられました。
---

# TiDB 3.0.6 リリースノート {#tidb-3-0-6-release-notes}

発売日：2019年11月28日

TiDB バージョン: 3.0.6

TiDB Ansible バージョン: 3.0.6

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ウィンドウ関数 AST が SQL テキストを復元した後に結果が正しくない (たとえば、 `over w`が誤って`over (w)` に復元される) 問題を修正しました。 [＃12933](https://github.com/pingcap/tidb/pull/12933)
    -   `STREAM AGG()`から`doubleRead` プッシュダウンする問題を修正 [＃12690](https://github.com/pingcap/tidb/pull/12690)
    -   SQLバインディングで引用符が正しく処理されない問題を修正 [＃13117](https://github.com/pingcap/tidb/pull/13117)
    -   `select max(_tidb_rowid) from t`シナリオを最適化してテーブル全体のスキャンを回避する[＃13095](https://github.com/pingcap/tidb/pull/13095)
    -   クエリステートメントに変数代入式が含まれている場合にクエリ結果が正しくない問題を修正しました[＃13231](https://github.com/pingcap/tidb/pull/13231)
    -   `UPDATE`ステートメントにサブクエリと生成された列の両方が含まれている場合に結果が正しくない問題を修正しました。`UPDATE`ステートメントに異なるソース データベースからの同じ名前のテーブルが 2 つ含まれている場合に発生するステートメント実行エラーを修正しました[＃13350](https://github.com/pingcap/tidb/pull/13350)
    -   ポイントクエリのサポート`_tidb_rowid` [＃13416](https://github.com/pingcap/tidb/pull/13416)
    -   パーティションテーブル統計の不適切な使用により、生成されたクエリ実行プランが正しくない問題を修正しました[＃13628](https://github.com/pingcap/tidb/pull/13628)
-   SQL実行エンジン
    -   年型の無効な値を処理するときにTiDBがMySQLと互換性がない問題を修正しました [＃12745](https://github.com/pingcap/tidb/pull/12745)
    -   `INSERT ON DUPLICATE UPDATE`文で`Chunk`再利用してメモリオーバーヘッドを削減する [＃12998](https://github.com/pingcap/tidb/pull/12998)
    -   `JSON_VALID`組み込み関数のサポートを追加 [＃13133](https://github.com/pingcap/tidb/pull/13133)
    -   パーティションテーブルで`ADMIN CHECK TABLE`実行をサポート [＃13140](https://github.com/pingcap/tidb/pull/13140)
    -   空のテーブルで`FAST ANALYZE`実行したときに発生するpanic問題を修正 [＃13343](https://github.com/pingcap/tidb/pull/13343)
    -   複数列のインデックスを含む空のテーブルで`FAST ANALYZE`実行するとpanic問題を修正[＃13394](https://github.com/pingcap/tidb/pull/13394)
    -   `WHERE`句に一意キー等号条件が含まれている場合に推定行数が 1 より大きくなる問題を修正しました [＃13382](https://github.com/pingcap/tidb/pull/13382)
    -   TiDB で`Streaming`有効になっている場合に返されるデータが重複する可能性がある問題を修正しました [＃13254](https://github.com/pingcap/tidb/pull/13254)
    -   推定精度を向上させるために、count-minスケッチから上位N個の値を抽出します[＃13429](https://github.com/pingcap/tidb/pull/13429)
-   サーバ
    -   gRPC ダイヤルがタイムアウトすると、TiKV に送信されたリクエストがすぐに失敗するようにします[＃12926](https://github.com/pingcap/tidb/pull/12926)
    -   次の仮想テーブルを追加します: [＃13009](https://github.com/pingcap/tidb/pull/13009)
        -   `performance_schema.tidb_profile_allocs`
        -   `performance_schema.tidb_profile_block`
        -   `performance_schema.tidb_profile_cpu`
        -   `performance_schema.tidb_profile_goroutines`
    -   クエリが悲観的ロックを待機しているときにコマンド`kill`が機能しない問題を修正[＃12989](https://github.com/pingcap/tidb/pull/12989)
    -   悲観的ロックの取得に失敗し、トランザクションが単一のキー変更のみを伴う場合は、非同期ロールバックを実行しないでください。 [＃12707](https://github.com/pingcap/tidb/pull/12707)
    -   領域分割のリクエストに対する応答が空の場合にpanicする問題を修正[＃13092](https://github.com/pingcap/tidb/pull/13092)
    -   `PessimisticLock`ロックエラーを返したときに不要なバックオフを回避する[＃13116](https://github.com/pingcap/tidb/pull/13116)
    -   認識されない構成オプション警告ログを出力して構成をチェックする TiDB の動作を変更します。 [＃13272](https://github.com/pingcap/tidb/pull/13272)
    -   `/info/all`インターフェースを介してすべての TiDB ノードのbinlogステータスの取得をサポート [＃13187](https://github.com/pingcap/tidb/pull/13187)
    -   TiDB が接続を切断したときに goroutine がリークする可能性がある問題を修正[＃13251](https://github.com/pingcap/tidb/pull/13251)
    -   悲観的トランザクションで`innodb_lock_wait_timeout`パラメータを動作させて、悲観的ロックのロック待機タイムアウトを制御する [＃13165](https://github.com/pingcap/tidb/pull/13165)
    -   悲観的トランザクションクエリが強制終了されたときに、他のトランザクションが不必要に待機するのを防ぐために、悲観的トランザクション TTL の更新を停止します[＃13046](https://github.com/pingcap/tidb/pull/13046)
-   DDL
    -   TiDB の`SHOW CREATE VIEW`の実行結果が MySQL 結果と一致しない問題を修正しました [＃12912](https://github.com/pingcap/tidb/pull/12912)
    -   `union`に基づいて`View`を作成するサポート（例： `create view v as select * from t1 union select * from t2` [＃12955](https://github.com/pingcap/tidb/pull/12955)
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
    -   テーブルが作成され、テーブルに`COLLATE` が含まれている場合、列のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。 [＃13174](https://github.com/pingcap/tidb/pull/13174)
    -   テーブルを作成するときにインデックス名の長さを制限する [＃13310](https://github.com/pingcap/tidb/pull/13310)
    -   テーブル名を変更するときにテーブル名の長さがチェックされない問題を修正[＃13346](https://github.com/pingcap/tidb/pull/13346)
    -   TiDB で主キーの追加/削除をサポートするために、 `alter-primary-key`構成（デフォルトでは無効）を追加します。 [＃13522](https://github.com/pingcap/tidb/pull/13522)

## TiKV {#tikv}

-   `acquire_pessimistic_lock`インターフェースが間違った`txn_size` を返す問題を修正 [＃5740](https://github.com/tikv/tikv/pull/5740)
-   GCワーカーの1秒あたりの書き込み回数を制限して、パフォーマンスへの影響を軽減します[＃5735](https://github.com/tikv/tikv/pull/5735)
-   `lock_manager`正確にする [＃5845](https://github.com/tikv/tikv/pull/5845)
-   悲観的ロックのサポート`innodb_lock_wait_timeout` [＃5848](https://github.com/tikv/tikv/pull/5848)
-   Titan の構成チェックを追加 [＃5720](https://github.com/tikv/tikv/pull/5720)
-   tikv-ctl を使用して GC I/O 制限を動的に変更するサポート: `tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [＃5957](https://github.com/tikv/tikv/pull/5957)
-   デッドロック検出器への負荷を軽減するために、無駄な`clean up`リクエストを削減します。 [＃5965](https://github.com/tikv/tikv/pull/5965)
-   悲観的ロックの事前書き込みリクエストでTTLを減らさないようにする[＃6056](https://github.com/tikv/tikv/pull/6056)
-   Titan でBLOBファイルが見つからない問題を修正 [＃5968](https://github.com/tikv/tikv/pull/5968)
-   Titan で`RocksDBOptions`効力を発揮しない問題を修正 [＃6009](https://github.com/tikv/tikv/pull/6009)

## PD {#pd}

-   各フィルターに`ActOn`ディメンションを追加して、各スケジューラとチェッカーがフィルターの影響を受けることを示します。また、使用されていない2つのフィルター（ `disconnectFilter`と`rejectLeaderFilter` を削除します。 [＃1911](https://github.com/pingcap/pd/pull/1911)
-   PD でタイムスタンプを生成するのに 5 ミリ秒以上かかる場合は警告ログを出力します。 [＃1867](https://github.com/pingcap/pd/pull/1867)
-   利用できないエンドポイントをクライアントに渡すときにクライアントのログ レベルを下げる [＃1856](https://github.com/pingcap/pd/pull/1856)
-   gRPCメッセージパッケージが`region_syncer`レプリケーションプロセスで最大サイズを超える可能性がある問題を修正 [＃1952](https://github.com/pingcap/pd/pull/1952)

## ツール {#tools}

-   TiDB Binlog
    -   Drainer で`initial-commit-ts` 「-1」に設定されている場合にPDから初期レプリケーションタイムスタンプを取得します。 [＃788](https://github.com/pingcap/tidb-binlog/pull/788)
    -   Drainerの`Checkpoint`ストレージを下流から分離し、MySQLまたはローカルファイルへの保存`Checkpoint`サポートします。 [＃790](https://github.com/pingcap/tidb-binlog/pull/790)
    -   レプリケーションデータベース/テーブルフィルタリングを構成する際に空の値を使用することで発生するDrainer panicの問題を修正しました[＃801](https://github.com/pingcap/tidb-binlog/pull/801)
    -   Drainer が下流にbinlogファイルを適用できないためにpanicが発生した後、プロセスが終了せずにデッドロック状態になる問題を修正しました[＃807](https://github.com/pingcap/tidb-binlog/pull/807)
    -   gRPC の`GracefulStop` が原因で、Pumpが終了時にブロックされる問題を修正しました。 [＃817](https://github.com/pingcap/tidb-binlog/pull/817)
    -   TiDB (v3.0.6 以降) で`DROP COLUMN`の実行中に列が欠落しているbinlogを受信するとDrainer が失敗する問題を修正しました[＃827](https://github.com/pingcap/tidb-binlog/pull/827)
-   TiDB Lightning
    -   TiDBバックエンドに`max-allowed-packet`構成（デフォルトでは64MB）を追加します。 [＃248](https://github.com/pingcap/tidb-lightning/pull/248)

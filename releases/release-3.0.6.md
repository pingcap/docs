---
title: TiDB 3.0.6 Release Notes
---

# TiDB 3.0.6 リリースノート {#tidb-3-0-6-release-notes}

発売日：2019年11月28日

TiDB バージョン: 3.0.6

TiDB Ansible バージョン: 3.0.6

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ウィンドウ関数 AST が SQL テキストを復元した後の結果が正しくない問題を修正します。たとえば、 `over w`が誤って`over (w)` [<a href="https://github.com/pingcap/tidb/pull/12933">#12933</a>](https://github.com/pingcap/tidb/pull/12933)に復元されるなどです。
    -   `STREAM AGG()`から`doubleRead` [<a href="https://github.com/pingcap/tidb/pull/12690">#12690</a>](https://github.com/pingcap/tidb/pull/12690)まで押し下げられる問題を修正
    -   SQL バインディング[<a href="https://github.com/pingcap/tidb/pull/13117">#13117</a>](https://github.com/pingcap/tidb/pull/13117)で引用符が正しく処理されない問題を修正します。
    -   `select max(_tidb_rowid) from t`シナリオを最適化してテーブル全体のスキャンを回避する[<a href="https://github.com/pingcap/tidb/pull/13095">#13095</a>](https://github.com/pingcap/tidb/pull/13095)
    -   クエリ ステートメントに変数代入式[<a href="https://github.com/pingcap/tidb/pull/13231">#13231</a>](https://github.com/pingcap/tidb/pull/13231)含まれている場合、クエリ結果が正しくない問題を修正します。
    -   `UPDATE`ステートメントにサブクエリと生成された列の両方が含まれている場合、結果が正しくないという問題を修正します。このステートメントに異なるソース データベースの 2 `UPDATE`の同じ名前のテーブルが含まれている場合のステートメント実行エラーを修正します[<a href="https://github.com/pingcap/tidb/pull/13350">#13350</a>](https://github.com/pingcap/tidb/pull/13350)
    -   ポイントクエリ[<a href="https://github.com/pingcap/tidb/pull/13416">#13416</a>](https://github.com/pingcap/tidb/pull/13416)のサポート`_tidb_rowid`
    -   パーティションテーブル統計[<a href="https://github.com/pingcap/tidb/pull/13628">#13628</a>](https://github.com/pingcap/tidb/pull/13628)の誤った使用が原因で、生成されたクエリ実行プランが正しくない問題を修正します。
-   SQL実行エンジン
    -   年タイプ[<a href="https://github.com/pingcap/tidb/pull/12745">#12745</a>](https://github.com/pingcap/tidb/pull/12745)の無効な値を処理するときに TiDB が MySQL と互換性がないという問題を修正
    -   `INSERT ON DUPLICATE UPDATE`ステートメントの`Chunk`再利用してメモリのオーバーヘッドを削減します[<a href="https://github.com/pingcap/tidb/pull/12998">#12998</a>](https://github.com/pingcap/tidb/pull/12998)
    -   `JSON_VALID`組み込み関数[<a href="https://github.com/pingcap/tidb/pull/13133">#13133</a>](https://github.com/pingcap/tidb/pull/13133)のサポートを追加します。
    -   パーティション化されたテーブル[<a href="https://github.com/pingcap/tidb/pull/13140">#13140</a>](https://github.com/pingcap/tidb/pull/13140)での`ADMIN CHECK TABLE`の実行をサポート
    -   空のテーブル[<a href="https://github.com/pingcap/tidb/pull/13343">#13343</a>](https://github.com/pingcap/tidb/pull/13343)で`FAST ANALYZE`が実行されたときのpanicの問題を修正
    -   複数列インデックスを含む空のテーブルに対して`FAST ANALYZE`を実行するときのpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/13394">#13394</a>](https://github.com/pingcap/tidb/pull/13394)
    -   `WHERE`句に一意のキー[<a href="https://github.com/pingcap/tidb/pull/13382">#13382</a>](https://github.com/pingcap/tidb/pull/13382)に対する等しい条件が含まれている場合、推定行数が 1 より大きくなる問題を修正します。
    -   TiDB [<a href="https://github.com/pingcap/tidb/pull/13254">#13254</a>](https://github.com/pingcap/tidb/pull/13254)で`Streaming`を有効にすると返されるデータが重複する可能性がある問題を修正
    -   count-min スケッチから上位 N 個の値を抽出して、推定精度を向上させます[<a href="https://github.com/pingcap/tidb/pull/13429">#13429</a>](https://github.com/pingcap/tidb/pull/13429)
-   サーバ
    -   gRPC ダイヤルがタイムアウトすると、TiKV に送信されたリクエストがすぐに失敗するようにします[<a href="https://github.com/pingcap/tidb/pull/12926">#12926</a>](https://github.com/pingcap/tidb/pull/12926)
    -   次の仮想テーブルを追加します。 [<a href="https://github.com/pingcap/tidb/pull/13009">#13009</a>](https://github.com/pingcap/tidb/pull/13009)
        -   `performance_schema.tidb_profile_allocs`
        -   `performance_schema.tidb_profile_block`
        -   `performance_schema.tidb_profile_cpu`
        -   `performance_schema.tidb_profile_goroutines`
    -   クエリが悲観的ロックを待機しているときに`kill`コマンドが機能しない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/12989">#12989</a>](https://github.com/pingcap/tidb/pull/12989)
    -   悲観的ロックの取得が失敗し、トランザクションに単一のキーの変更のみが含まれる場合は、非同期ロールバックを実行しないでください[<a href="https://github.com/pingcap/tidb/pull/12707">#12707</a>](https://github.com/pingcap/tidb/pull/12707)
    -   リージョンの分割リクエストに対する応答が空の場合のpanicの問題を修正[<a href="https://github.com/pingcap/tidb/pull/13092">#13092</a>](https://github.com/pingcap/tidb/pull/13092)
    -   `PessimisticLock`ロック エラーを返した場合に不必要なバックオフを回避します[<a href="https://github.com/pingcap/tidb/pull/13116">#13116</a>](https://github.com/pingcap/tidb/pull/13116)
    -   認識されない構成オプション[<a href="https://github.com/pingcap/tidb/pull/13272">#13272</a>](https://github.com/pingcap/tidb/pull/13272)の警告ログを出力することで、構成をチェックするための TiDB の動作を変更します。
    -   `/info/all`インターフェイスを介したすべての TiDB ノードのbinlogステータスの取得をサポート[<a href="https://github.com/pingcap/tidb/pull/13187">#13187</a>](https://github.com/pingcap/tidb/pull/13187)
    -   TiDB が接続を強制終了するときに goroutine がリークする可能性がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/13251">#13251</a>](https://github.com/pingcap/tidb/pull/13251)
    -   `innodb_lock_wait_timeout`パラメータを悲観的トランザクションで機能させて、悲観的ロックのロック待機タイムアウトを制御します[<a href="https://github.com/pingcap/tidb/pull/13165">#13165</a>](https://github.com/pingcap/tidb/pull/13165)
    -   他のトランザクションが不必要に待機するのを防ぐために、悲観的トランザクション クエリが強制終了されたときに、悲観的トランザクション TTL の更新を停止します[<a href="https://github.com/pingcap/tidb/pull/13046">#13046</a>](https://github.com/pingcap/tidb/pull/13046)
-   DDL
    -   TiDBの`SHOW CREATE VIEW`の実行結果がMySQL [<a href="https://github.com/pingcap/tidb/pull/12912">#12912</a>](https://github.com/pingcap/tidb/pull/12912)の実行結果と一致しない問題を修正
    -   `union`に基づいた`View`の作成をサポート (例: `create view v as select * from t1 union select * from t2` [<a href="https://github.com/pingcap/tidb/pull/12955">#12955</a>](https://github.com/pingcap/tidb/pull/12955)
    -   `slow_query`テーブルにトランザクション関連フィールドをさらに追加します: [<a href="https://github.com/pingcap/tidb/pull/13072">#13072</a>](https://github.com/pingcap/tidb/pull/13072)
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
    -   テーブルが作成され、テーブルに`COLLATE` [<a href="https://github.com/pingcap/tidb/pull/13174">#13174</a>](https://github.com/pingcap/tidb/pull/13174)含まれている場合、列内のシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`使用します。
    -   テーブル作成時のインデックス名の長さを制限する[<a href="https://github.com/pingcap/tidb/pull/13310">#13310</a>](https://github.com/pingcap/tidb/pull/13310)
    -   テーブルの名前を変更するときにテーブル名の長さがチェックされない問題を修正[<a href="https://github.com/pingcap/tidb/pull/13346">#13346</a>](https://github.com/pingcap/tidb/pull/13346)
    -   TiDB [<a href="https://github.com/pingcap/tidb/pull/13522">#13522</a>](https://github.com/pingcap/tidb/pull/13522)での主キーの追加/削除をサポートするために`alter-primary-key`構成 (デフォルトでは無効) を追加します。

## TiKV {#tikv}

-   `acquire_pessimistic_lock`インターフェイスが間違った`txn_size` [<a href="https://github.com/tikv/tikv/pull/5740">#5740</a>](https://github.com/tikv/tikv/pull/5740)を返す問題を修正
-   パフォーマンスへの影響を軽減するために、1 秒あたりの GC ワーカーの書き込みを制限します[<a href="https://github.com/tikv/tikv/pull/5735">#5735</a>](https://github.com/tikv/tikv/pull/5735)
-   `lock_manager`を正確に[<a href="https://github.com/tikv/tikv/pull/5845">#5845</a>](https://github.com/tikv/tikv/pull/5845)
-   悲観的ロック[<a href="https://github.com/tikv/tikv/pull/5848">#5848</a>](https://github.com/tikv/tikv/pull/5848)のサポート`innodb_lock_wait_timeout`
-   Titan [<a href="https://github.com/tikv/tikv/pull/5720">#5720</a>](https://github.com/tikv/tikv/pull/5720)の構成チェックを追加
-   tikv-ctl を使用した GC I/O 制限の動的変更のサポート: `tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [<a href="https://github.com/tikv/tikv/pull/5957">#5957</a>](https://github.com/tikv/tikv/pull/5957)
-   無駄な`clean up`リクエストを減らしてデッドロック検出器の圧力を下げる[<a href="https://github.com/tikv/tikv/pull/5965">#5965</a>](https://github.com/tikv/tikv/pull/5965)
-   悲観的ロックの事前書き込みリクエストで TTL を削減しないようにする[<a href="https://github.com/tikv/tikv/pull/6056">#6056</a>](https://github.com/tikv/tikv/pull/6056)
-   Titan [<a href="https://github.com/tikv/tikv/pull/5968">#5968</a>](https://github.com/tikv/tikv/pull/5968)で BLOB ファイルの欠落が発生する可能性がある問題を修正
-   Titan [<a href="https://github.com/tikv/tikv/pull/6009">#6009</a>](https://github.com/tikv/tikv/pull/6009)で`RocksDBOptions`有効にならない場合がある問題を修正

## PD {#pd}

-   各フィルタに`ActOn`ディメンションを追加して、各スケジューラとチェッカーがフィルタの影響を受けることを示し、2 つの未使用フィルタ`disconnectFilter`と`rejectLeaderFilter` [<a href="https://github.com/pingcap/pd/pull/1911">#1911</a>](https://github.com/pingcap/pd/pull/1911)を削除します。
-   PD [<a href="https://github.com/pingcap/pd/pull/1867">#1867</a>](https://github.com/pingcap/pd/pull/1867)でタイムスタンプの生成に 5 ミリ秒以上かかる場合、警告ログを出力します。
-   使用できないエンドポイントをクライアント[<a href="https://github.com/pingcap/pd/pull/1856">#1856</a>](https://github.com/pingcap/pd/pull/1856)に渡すときにクライアントのログ レベルを下げる
-   gRPC メッセージ パッケージが`region_syncer`レプリケーション プロセスの最大サイズを超える可能性がある問題を修正[<a href="https://github.com/pingcap/pd/pull/1952">#1952</a>](https://github.com/pingcap/pd/pull/1952)

## ツール {#tools}

-   TiDBBinlog
    -   Drainer [<a href="https://github.com/pingcap/tidb-binlog/pull/788">#788</a>](https://github.com/pingcap/tidb-binlog/pull/788)で`initial-commit-ts`が「-1」に設定されている場合、PD から最初のレプリケーション タイムスタンプを取得します。
    -   Drainer の`Checkpoint`storageをダウンストリームから切り離し、MySQL またはローカル ファイルへの`Checkpoint`の保存をサポート[<a href="https://github.com/pingcap/tidb-binlog/pull/790">#790</a>](https://github.com/pingcap/tidb-binlog/pull/790)
    -   レプリケーション データベース/テーブル フィルタリング[<a href="https://github.com/pingcap/tidb-binlog/pull/801">#801</a>](https://github.com/pingcap/tidb-binlog/pull/801)を構成するときに空の値を使用することによって引き起こされるDrainerpanicの問題を修正します。
    -   Drainer がbinlogファイルをダウンストリーム[<a href="https://github.com/pingcap/tidb-binlog/pull/807">#807</a>](https://github.com/pingcap/tidb-binlog/pull/807)に適用できないため、panicが発生した後にプロセスが終了せずにデッドロック状態になる問題を修正します。
    -   gRPC `GracefulStop` [<a href="https://github.com/pingcap/tidb-binlog/pull/817">#817</a>](https://github.com/pingcap/tidb-binlog/pull/817)が原因で終了時にPumpがブロックされる問題を修正
    -   TiDB (v3.0.6 以降) `DROP COLUMN`ステートメントの実行中に列が欠落しているbinlogを受信すると、 Drainerが失敗する問題を修正します[<a href="https://github.com/pingcap/tidb-binlog/pull/827">#827</a>](https://github.com/pingcap/tidb-binlog/pull/827)
-   TiDB Lightning
    -   TiDB バックエンド[<a href="https://github.com/pingcap/tidb-lightning/pull/248">#248</a>](https://github.com/pingcap/tidb-lightning/pull/248)に`max-allowed-packet`構成 (デフォルトでは 64 M) を追加します。

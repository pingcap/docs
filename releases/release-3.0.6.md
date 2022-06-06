---
title: TiDB 3.0.6 Release Notes
---

# TiDB3.0.6リリースノート {#tidb-3-0-6-release-notes}

発売日：2019年11月28日

TiDBバージョン：3.0.6

TiDB Ansibleバージョン：3.0.6

## TiDB {#tidb}

-   SQLオプティマイザー
    -   ウィンドウ関数ASTがSQLテキストを復元した後、結果が正しくないという問題を修正し[＃12933](https://github.com/pingcap/tidb/pull/12933) 。たとえば、 `over w`が誤って35に復元され`over (w)` 。
    -   `STREAM AGG()`から[＃12690](https://github.com/pingcap/tidb/pull/12690)を押し下げる問題を修正し`doubleRead`
    -   SQLバインディング[＃13117](https://github.com/pingcap/tidb/pull/13117)で引用符が正しく処理されない問題を修正します
    -   全表スキャンを回避するために`select max(_tidb_rowid) from t`のシナリオを最適化する[＃13095](https://github.com/pingcap/tidb/pull/13095)
    -   クエリステートメントに変数代入式[＃13231](https://github.com/pingcap/tidb/pull/13231)が含まれている場合に、クエリ結果が正しくない問題を修正します。
    -   `UPDATE`ステートメントにサブクエリと生成された列の両方が含まれている場合に結果が正しくないという問題を修正します。このステートメントに異なるソースデータベースからの2つの同じ名前のテーブルが含まれている場合の`UPDATE`ステートメントの実行エラーを修正します[＃13350](https://github.com/pingcap/tidb/pull/13350)
    -   ポイントクエリ[＃13416](https://github.com/pingcap/tidb/pull/13416)のサポート`_tidb_rowid`
    -   パーティションテーブル統計の誤った使用が原因で、生成されたクエリ実行プランが正しくないという問題を修正します[＃13628](https://github.com/pingcap/tidb/pull/13628)
-   SQL実行エンジン
    -   年タイプ[＃12745](https://github.com/pingcap/tidb/pull/12745)の無効な値を処理するときに、TiDBがMySQLと互換性がないという問題を修正します
    -   `INSERT ON DUPLICATE UPDATE`ステートメントで`Chunk`を再利用して、メモリオーバーヘッドを削減します[＃12998](https://github.com/pingcap/tidb/pull/12998)
    -   `JSON_VALID`組み込み関数[＃13133](https://github.com/pingcap/tidb/pull/13133)のサポートを追加します
    -   パーティションテーブル[＃13140](https://github.com/pingcap/tidb/pull/13140)での`ADMIN CHECK TABLE`の実行をサポート
    -   空のテーブルで`FAST ANALYZE`が実行されたときのパニックの問題を修正します[＃13343](https://github.com/pingcap/tidb/pull/13343)
    -   複数列のインデックスを含む空のテーブルで`FAST ANALYZE`を実行するときのパニックの問題を修正します[＃13394](https://github.com/pingcap/tidb/pull/13394)
    -   `WHERE`句に一意キー[＃13382](https://github.com/pingcap/tidb/pull/13382)の等しい条件が含まれている場合に、推定行数が1より大きい問題を修正します。
    -   TiDB [＃13254](https://github.com/pingcap/tidb/pull/13254)で`Streaming`を有効にすると、返されるデータが重複する可能性がある問題を修正します。
    -   count-minスケッチから上位N値を抽出して、推定精度を向上させます[＃13429](https://github.com/pingcap/tidb/pull/13429)
-   サーバ
    -   gRPCダイヤルがタイムアウトしたときにTiKVに送信されたリクエストをすぐに失敗させる[＃12926](https://github.com/pingcap/tidb/pull/12926)
    -   次の仮想テーブルを追加します： [＃13009](https://github.com/pingcap/tidb/pull/13009)
        -   `performance_schema.tidb_profile_allocs`
        -   `performance_schema.tidb_profile_block`
        -   `performance_schema.tidb_profile_cpu`
        -   `performance_schema.tidb_profile_goroutines`
    -   クエリが悲観的なロックを待機しているときに`kill`コマンドが機能しない問題を修正します[＃12989](https://github.com/pingcap/tidb/pull/12989)
    -   悲観的ロックの取得が失敗し、トランザクションに単一のキーの変更のみが含まれる場合は、非同期ロールバックを実行しないでください[＃12707](https://github.com/pingcap/tidb/pull/12707)
    -   リージョンの分割リクエストに対する応答が空の場合のパニックの問題を修正します[＃13092](https://github.com/pingcap/tidb/pull/13092)
    -   `PessimisticLock`がロックエラーを返す場合の不要なバックオフを回避します[＃13116](https://github.com/pingcap/tidb/pull/13116)
    -   認識されない構成オプション[＃13272](https://github.com/pingcap/tidb/pull/13272)の警告ログを出力して、構成を確認するためのTiDBの動作を変更します。
    -   `/info/all`のインターフェース[＃13187](https://github.com/pingcap/tidb/pull/13187)を介したすべてのTiDBノードのbinlogステータスの取得をサポートします。
    -   TiDBが接続を切断したときにゴルーチンがリークする可能性がある問題を修正します[＃13251](https://github.com/pingcap/tidb/pull/13251)
    -   `innodb_lock_wait_timeout`パラメーターをペシミスティックトランザクションで機能させて、ペシミスティックロックのロック待機タイムアウトを制御します[＃13165](https://github.com/pingcap/tidb/pull/13165)
    -   他のトランザクションが不必要に待機するのを防ぐために、悲観的なトランザクションクエリが強制終了されたときに、悲観的なトランザクションTTLの更新を停止します[＃13046](https://github.com/pingcap/tidb/pull/13046)
-   DDL
    -   TiDBでの`SHOW CREATE VIEW`の実行結果がMySQL3での実行結果と矛盾する問題を修正し[＃12912](https://github.com/pingcap/tidb/pull/12912)
    -   `union`に基づく`View`の作成をサポートします（例： `create view v as select * from t1 union select * from t2` [＃12955](https://github.com/pingcap/tidb/pull/12955) ）
    -   `slow_query`のテーブルにトランザクション関連のフィールドをさらに追加します： [＃13072](https://github.com/pingcap/tidb/pull/13072)
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
    -   テーブルが作成され、テーブルに`COLLATE` [＃13174](https://github.com/pingcap/tidb/pull/13174)が含まれている場合は、列にシステムのデフォルトの文字セットの代わりにテーブルの`COLLATE`を使用します。
    -   テーブルを作成するときにインデックス名の長さを制限する[＃13310](https://github.com/pingcap/tidb/pull/13310)
    -   テーブルの名前が変更されたときにテーブル名の長さがチェックされない問題を修正します[＃13346](https://github.com/pingcap/tidb/pull/13346)
    -   TiDB [＃13522](https://github.com/pingcap/tidb/pull/13522)での主キーの追加/削除をサポートするために、 `alter-primary-key`の構成（デフォルトでは無効）を追加します。

## TiKV {#tikv}

-   `acquire_pessimistic_lock`インターフェイスが間違った[＃5740](https://github.com/tikv/tikv/pull/5740)を返す問題を修正し`txn_size`
-   パフォーマンスへの影響を減らすために、1秒あたりのGCワーカーの書き込みを制限します[＃5735](https://github.com/tikv/tikv/pull/5735)
-   `lock_manager`を正確にする[＃5845](https://github.com/tikv/tikv/pull/5845)
-   悲観的なロック[＃5848](https://github.com/tikv/tikv/pull/5848)のサポート`innodb_lock_wait_timeout`
-   Titan1の構成チェックを追加し[＃5720](https://github.com/tikv/tikv/pull/5720)
-   tikv-ctlを使用してGCI/ O制限を動的に変更することをサポートします： `tikv-ctl --host=ip:port modify-tikv-config -m server -n gc.max_write_bytes_per_sec -v 10MB` [＃5957](https://github.com/tikv/tikv/pull/5957)
-   無駄な`clean up`リクエストを減らして、デッドロック検出器[＃5965](https://github.com/tikv/tikv/pull/5965)への圧力を減らします。
-   悲観的なロックの事前書き込み要求でTTLを減らすことは避けてください[＃6056](https://github.com/tikv/tikv/pull/6056)
-   Titan1でblobファイルの欠落が発生する可能性がある問題を修正し[＃5968](https://github.com/tikv/tikv/pull/5968)
-   Titan3で`RocksDBOptions`が有効にならない可能性がある問題を修正し[＃6009](https://github.com/tikv/tikv/pull/6009)

## PD {#pd}

-   各フィルターに`ActOn`次元を追加して、各スケジューラーとチェッカーがフィルターの影響を受けることを示し、2つの未使用のフィルター（ `disconnectFilter`と`rejectLeaderFilter` [＃1911](https://github.com/pingcap/pd/pull/1911) ）を削除します。
-   PD [＃1867](https://github.com/pingcap/pd/pull/1867)でタイムスタンプを生成するのに5ミリ秒以上かかる場合は、警告ログを印刷します
-   使用できないエンドポイントをクライアントに渡すときに、クライアントのログレベルを下げる[＃1856](https://github.com/pingcap/pd/pull/1856)
-   gRPCメッセージパッケージが`region_syncer`レプリケーションプロセスで最大サイズを超える可能性があるという問題を修正します[＃1952](https://github.com/pingcap/pd/pull/1952)

## ツール {#tools}

-   TiDB Binlog
    -   Drainer [＃788](https://github.com/pingcap/tidb-binlog/pull/788)で`initial-commit-ts`が「-1」に設定されている場合、PDから初期レプリケーションタイムスタンプを取得します
    -   Drainerの`Checkpoint`のストレージをダウンストリームから切り離し、MySQLまたはローカルファイルへの`Checkpoint`の保存をサポートします[＃790](https://github.com/pingcap/tidb-binlog/pull/790)
    -   レプリケーションデータベース/テーブルフィルタリングを構成するときに空の値を使用することによって引き起こされるDrainerパニックの問題を修正します[＃801](https://github.com/pingcap/tidb-binlog/pull/801)
    -   Drainerがbinlogファイルをダウンストリームに適用できないためにパニックが発生した後にプロセスが終了するのではなくデッドロック状態になる問題を修正します[＃807](https://github.com/pingcap/tidb-binlog/pull/807)
    -   gRPCの`GracefulStop`が原因でPumpが終了するときにブロックする問題を修正し[＃817](https://github.com/pingcap/tidb-binlog/pull/817)
    -   TiDB（v3.0.6以降）で`DROP COLUMN`ステートメントの実行中に列を見逃したbinlogを受信すると、Drainerが失敗する問題を修正します[＃827](https://github.com/pingcap/tidb-binlog/pull/827)
-   TiDB Lightning
    -   TiDBバックエンド[＃248](https://github.com/pingcap/tidb-lightning/pull/248)の`max-allowed-packet`の構成（デフォルトでは64 M）を追加します

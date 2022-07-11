---
title: TiDB 2.1 RC5 Release Notes
---

<!-- markdownlint-disable MD032 -->

# TiDB2.1RC5リリースノート {#tidb-2-1-rc5-release-notes}

2018年11月12日、TiDB2.1RC5がリリースされました。このリリースでは、TiDB 2.1 RC4と比較して、安定性、SQLオプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `IndexReader`が間違ったハンドルを読み取る場合があるという問題を修正します[＃8132](https://github.com/pingcap/tidb/pull/8132)
    -   `IndexScan Prepared`ステートメントが[＃8055](https://github.com/pingcap/tidb/pull/8055)を使用しているときに発生した問題を修正し`Plan Cache`
    -   `Union`ステートメントの結果が不安定になる問題を修正します[＃8165](https://github.com/pingcap/tidb/pull/8165)
-   SQL実行エンジン
    -   ワイドテーブルの挿入または更新時のTiDBのパフォーマンスを向上させる[＃8024](https://github.com/pingcap/tidb/pull/8024)
    -   `Truncate`組み込み関数`int`でunsigned1フラグをサポートし[＃8068](https://github.com/pingcap/tidb/pull/8068) 。
    -   JSONデータを10進タイプ[＃8109](https://github.com/pingcap/tidb/pull/8109)に変換するときに発生したエラーを修正します
    -   `Update`フロートタイプ[＃8170](https://github.com/pingcap/tidb/pull/8170)のときに発生したエラーを修正します
-   統計
    -   場合によっては、ポイントクエリ中の誤った統計の問題を修正します[＃8035](https://github.com/pingcap/tidb/pull/8035)
    -   場合によっては、主キーの統計の選択性推定を修正します[＃8149](https://github.com/pingcap/tidb/pull/8149)
    -   削除されたテーブルの統計が長期間クリアされない問題を修正します[＃8182](https://github.com/pingcap/tidb/pull/8182)
-   サーバ
    -   ログの読みやすさを改善し、ログを改善します
        -   [＃8063](https://github.com/pingcap/tidb/pull/8063)
        -   [＃8053](https://github.com/pingcap/tidb/pull/8053)
        -   [＃8224](https://github.com/pingcap/tidb/pull/8224)

    <!---->

    -   [＃8096](https://github.com/pingcap/tidb/pull/8096)のテーブルデータを取得するときに発生したエラーを修正し`infoschema.profiling`
    -   UNIXソケットをpumpsクライアントに置き換えて、 [＃8098](https://github.com/pingcap/tidb/pull/8098)を書き込みます。
    -   `tidb_slow_log_threshold`の環境変数のしきい値を追加します。これにより、低速ログ[＃8094](https://github.com/pingcap/tidb/pull/8094)が動的に設定されます。
    -   `tidb_query_log_max_len`環境変数がログを動的に設定している間に切り捨てられたSQLステートメントの元の長さを追加します[＃8200](https://github.com/pingcap/tidb/pull/8200)
    -   `tidb_opt_write_row_id`の環境変数を追加して、書き込みを許可するかどうかを制御し`_tidb_rowid` [＃8218](https://github.com/pingcap/tidb/pull/8218)
    -   オーバーバウンドスキャンを回避するために、ticlientの`Scan`コマンドに上限を追加し[＃8247](https://github.com/pingcap/tidb/pull/8247) [＃8081](https://github.com/pingcap/tidb/pull/8081)
-   DDL
    -   トランザクションでDDLステートメントを実行するとエラーが発生する場合がある問題を修正します[＃8056](https://github.com/pingcap/tidb/pull/8056)
    -   パーティションテーブルで`truncate table`を実行しても[＃8103](https://github.com/pingcap/tidb/pull/8103)が有効にならない問題を修正します
    -   場合によってはキャンセルされた後、DDL操作が正しくロールバックされない問題を修正します[＃8057](https://github.com/pingcap/tidb/pull/8057)
    -   `admin show next_row_id`コマンドを追加して、次に使用可能な行[＃8268](https://github.com/pingcap/tidb/pull/8268)を返します。

## PD {#pd}

-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正します
    -   [＃1298](https://github.com/pingcap/pd/pull/1298)
    -   [＃1299](https://github.com/pingcap/pd/pull/1299)
    -   [＃1308](https://github.com/pingcap/pd/pull/1308)
-   `regions/check`が間違った結果を返す問題を修正します[＃1311](https://github.com/pingcap/pd/pull/1311)
-   PDの参加に失敗した後、PDが参加を再開できない問題を修正します[＃1279](https://github.com/pingcap/pd/pull/1279)
-   `watch leader`が場合によってはイベントを失う可能性があるという問題を修正します[＃1317](https://github.com/pingcap/pd/pull/1317)

## TiKV {#tikv}

-   `WriteConflict`のエラーメッセージを[＃3750](https://github.com/tikv/tikv/pull/3750)する
-   panicマークファイルを追加する[＃3746](https://github.com/tikv/tikv/pull/3746)
-   grpcioをダウングレードして、新しいバージョンのgRPC1によって引き起こされるセグメンテーション違反の問題を回避し[＃3650](https://github.com/tikv/tikv/pull/3650)
-   `kv_scan`のインターフェイスに上限を追加します[＃3749](https://github.com/tikv/tikv/pull/3749)

## ツール {#tools}

-   古いバージョンの[＃8093](https://github.com/pingcap/tidb/pull/8093)と互換性のないTiDB- [ドキュメンテーション](/tidb-binlog/tidb-binlog-overview.md)クラスタをサポートします。

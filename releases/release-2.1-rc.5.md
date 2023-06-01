---
title: TiDB 2.1 RC5 Release Notes
---

<!-- markdownlint-disable MD032 -->

# TiDB 2.1 RC5 リリースノート {#tidb-2-1-rc5-release-notes}

2018 年 11 月 12 日に、TiDB 2.1 RC5 がリリースされました。 TiDB 2.1 RC4 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `IndexReader`場合によっては間違ったハンドルを読み込む問題を修正[<a href="https://github.com/pingcap/tidb/pull/8132">#8132</a>](https://github.com/pingcap/tidb/pull/8132)
    -   `IndexScan Prepared`ステートメントが`Plan Cache` [<a href="https://github.com/pingcap/tidb/pull/8055">#8055</a>](https://github.com/pingcap/tidb/pull/8055)を使用しているときに発生した問題を修正します。
    -   `Union`ステートメントの結果が不安定になる問題を修正[<a href="https://github.com/pingcap/tidb/pull/8165">#8165</a>](https://github.com/pingcap/tidb/pull/8165)
-   SQL実行エンジン
    -   幅の広いテーブルの挿入または更新における TiDB のパフォーマンスを向上させる[<a href="https://github.com/pingcap/tidb/pull/8024">#8024</a>](https://github.com/pingcap/tidb/pull/8024)
    -   `Truncate`組み込み関数で unsigned `int`フラグをサポート[<a href="https://github.com/pingcap/tidb/pull/8068">#8068</a>](https://github.com/pingcap/tidb/pull/8068)
    -   JSONデータを10進数タイプ[<a href="https://github.com/pingcap/tidb/pull/8109">#8109</a>](https://github.com/pingcap/tidb/pull/8109)に変換する際に発生したエラーを修正
    -   float 型[<a href="https://github.com/pingcap/tidb/pull/8170">#8170</a>](https://github.com/pingcap/tidb/pull/8170)を`Update`すると発生するエラーを修正
-   統計
    -   場合によってはポイント クエリ中に発生する不正な統計の問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8035">#8035</a>](https://github.com/pingcap/tidb/pull/8035)
    -   場合によっては主キーの統計の選択性推定を修正しました[<a href="https://github.com/pingcap/tidb/pull/8149">#8149</a>](https://github.com/pingcap/tidb/pull/8149)
    -   削除されたテーブルの統計が長期間クリアされない問題を修正[<a href="https://github.com/pingcap/tidb/pull/8182">#8182</a>](https://github.com/pingcap/tidb/pull/8182)
-   サーバ
    -   ログの可読性を向上させ、ログをより適切なものにします
        -   [<a href="https://github.com/pingcap/tidb/pull/8063">#8063</a>](https://github.com/pingcap/tidb/pull/8063)
        -   [<a href="https://github.com/pingcap/tidb/pull/8053">#8053</a>](https://github.com/pingcap/tidb/pull/8053)
        -   [<a href="https://github.com/pingcap/tidb/pull/8224">#8224</a>](https://github.com/pingcap/tidb/pull/8224)

    <!---->

    -   `infoschema.profiling` [<a href="https://github.com/pingcap/tidb/pull/8096">#8096</a>](https://github.com/pingcap/tidb/pull/8096)のテーブルデータ取得時に発生するエラーを修正
    -   Unix ソケットをポンプ クライアントに置き換えて、バイナリ ログ[<a href="https://github.com/pingcap/tidb/pull/8098">#8098</a>](https://github.com/pingcap/tidb/pull/8098)を書き込みます。
    -   `tidb_slow_log_threshold`環境変数のしきい値を追加します。これにより、スロー ログが動的に設定されます[<a href="https://github.com/pingcap/tidb/pull/8094">#8094</a>](https://github.com/pingcap/tidb/pull/8094)
    -   `tidb_query_log_max_len`環境変数が動的にログを設定する間に、切り詰められた SQL ステートメントの元の長さを追加します[<a href="https://github.com/pingcap/tidb/pull/8200">#8200</a>](https://github.com/pingcap/tidb/pull/8200)
    -   `tidb_opt_write_row_id`環境変数を追加して、書き込みを許可するかどうかを制御します`_tidb_rowid` [<a href="https://github.com/pingcap/tidb/pull/8218">#8218</a>](https://github.com/pingcap/tidb/pull/8218)
    -   オーバーバウンドスキャンを避けるために、ticlient の`Scan`コマンドに上限を追加します[<a href="https://github.com/pingcap/tidb/pull/8081">#8081</a>](https://github.com/pingcap/tidb/pull/8081) 、 [<a href="https://github.com/pingcap/tidb/pull/8247">#8247</a>](https://github.com/pingcap/tidb/pull/8247)
-   DDL
    -   トランザクションで DDL ステートメントを実行すると、場合によってはエラーが発生する問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8056">#8056</a>](https://github.com/pingcap/tidb/pull/8056)
    -   パーティションテーブルで`truncate table`実行しても有効にならない問題を修正[<a href="https://github.com/pingcap/tidb/pull/8103">#8103</a>](https://github.com/pingcap/tidb/pull/8103)
    -   場合によっては DDL 操作がキャンセルされた後に正しくロールバックされない問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8057">#8057</a>](https://github.com/pingcap/tidb/pull/8057)
    -   `admin show next_row_id`コマンドを追加して、次に利用可能な行 ID [<a href="https://github.com/pingcap/tidb/pull/8268">#8268</a>](https://github.com/pingcap/tidb/pull/8268)を返します。

## PD {#pd}

-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正
    -   [<a href="https://github.com/pingcap/pd/pull/1298">#1298</a>](https://github.com/pingcap/pd/pull/1298)
    -   [<a href="https://github.com/pingcap/pd/pull/1299">#1299</a>](https://github.com/pingcap/pd/pull/1299)
    -   [<a href="https://github.com/pingcap/pd/pull/1308">#1308</a>](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` API が間違った結果を返す問題を修正[<a href="https://github.com/pingcap/pd/pull/1311">#1311</a>](https://github.com/pingcap/pd/pull/1311)
-   PD 参加失敗後に PD が参加を再開できない問題を修正[<a href="https://github.com/pingcap/pd/pull/1279">#1279</a>](https://github.com/pingcap/pd/pull/1279)
-   `watch leader`場合によってはイベントが失われる可能性がある問題を修正[<a href="https://github.com/pingcap/pd/pull/1317">#1317</a>](https://github.com/pingcap/pd/pull/1317)

## TiKV {#tikv}

-   `WriteConflict` [<a href="https://github.com/tikv/tikv/pull/3750">#3750</a>](https://github.com/tikv/tikv/pull/3750)のエラーメッセージを改善
-   panicマーク ファイル[<a href="https://github.com/tikv/tikv/pull/3746">#3746</a>](https://github.com/tikv/tikv/pull/3746)を追加します
-   gRPC [<a href="https://github.com/tikv/tikv/pull/3650">#3650</a>](https://github.com/tikv/tikv/pull/3650)の新しいバージョンによって引き起こされるセグメント障害の問題を回避するには、grpcio をダウングレードします。
-   `kv_scan`インターフェース[<a href="https://github.com/tikv/tikv/pull/3749">#3749</a>](https://github.com/tikv/tikv/pull/3749)に上限を追加します

## ツール {#tools}

-   TiDB-Binlog クラスターをサポートします。これは、 binlog [<a href="https://github.com/pingcap/tidb/pull/8093">#8093</a>](https://github.com/pingcap/tidb/pull/8093)の古いバージョンと互換性がありません[<a href="/tidb-binlog/tidb-binlog-overview.md">ドキュメンテーション</a>](/tidb-binlog/tidb-binlog-overview.md)

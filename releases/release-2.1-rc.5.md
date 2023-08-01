---
title: TiDB 2.1 RC5 Release Notes
---

<!-- markdownlint-disable MD032 -->

# TiDB 2.1 RC5 リリースノート {#tidb-2-1-rc5-release-notes}

2018 年 11 月 12 日に、TiDB 2.1 RC5 がリリースされました。 TiDB 2.1 RC4 と比較して、このリリースでは安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に向上しています。

## TiDB {#tidb}

-   SQLオプティマイザー
    -   `IndexReader`場合によっては間違ったハンドルを読み込む問題を修正[#8132](https://github.com/pingcap/tidb/pull/8132)
    -   `IndexScan Prepared`ステートメントが`Plan Cache` [#8055](https://github.com/pingcap/tidb/pull/8055)を使用しているときに発生した問題を修正します。
    -   `Union`ステートメントの結果が不安定になる問題を修正[#8165](https://github.com/pingcap/tidb/pull/8165)
-   SQL実行エンジン
    -   幅の広いテーブルの挿入または更新における TiDB のパフォーマンスを向上させる[#8024](https://github.com/pingcap/tidb/pull/8024)
    -   `Truncate`組み込み関数で unsigned `int`フラグをサポート[#8068](https://github.com/pingcap/tidb/pull/8068)
    -   JSONデータを10進数タイプ[#8109](https://github.com/pingcap/tidb/pull/8109)に変換する際に発生したエラーを修正
    -   float 型[#8170](https://github.com/pingcap/tidb/pull/8170)を`Update`すると発生するエラーを修正
-   統計
    -   場合によってはポイント クエリ中に発生する不正な統計の問題を修正します[#8035](https://github.com/pingcap/tidb/pull/8035)
    -   場合によっては主キーの統計の選択性推定を修正しました[#8149](https://github.com/pingcap/tidb/pull/8149)
    -   削除されたテーブルの統計が長期間クリアされない問題を修正[#8182](https://github.com/pingcap/tidb/pull/8182)
-   サーバ
    -   ログの可読性を向上させ、ログをより適切なものにします
        -   [#8063](https://github.com/pingcap/tidb/pull/8063)
        -   [#8053](https://github.com/pingcap/tidb/pull/8053)
        -   [#8224](https://github.com/pingcap/tidb/pull/8224)

    <!---->

    -   `infoschema.profiling` [#8096](https://github.com/pingcap/tidb/pull/8096)のテーブルデータ取得時に発生するエラーを修正
    -   Unix ソケットをポンプ クライアントに置き換えて、バイナリ ログ[#8098](https://github.com/pingcap/tidb/pull/8098)を書き込みます。
    -   `tidb_slow_log_threshold`環境変数のしきい値を追加します。これにより、スロー ログが動的に設定されます[#8094](https://github.com/pingcap/tidb/pull/8094)
    -   `tidb_query_log_max_len`環境変数が動的にログを設定する間に、切り詰められた SQL ステートメントの元の長さを追加します[#8200](https://github.com/pingcap/tidb/pull/8200)
    -   `tidb_opt_write_row_id`環境変数を追加して、書き込みを許可するかどうかを制御します`_tidb_rowid` [#8218](https://github.com/pingcap/tidb/pull/8218)
    -   オーバーバウンドスキャンを避けるために、ticlient の`Scan`コマンドに上限を追加します[#8081](https://github.com/pingcap/tidb/pull/8081) 、 [#8247](https://github.com/pingcap/tidb/pull/8247)
-   DDL
    -   トランザクションで DDL ステートメントを実行すると、場合によってはエラーが発生する問題を修正します[#8056](https://github.com/pingcap/tidb/pull/8056)
    -   パーティションテーブルで`truncate table`実行しても有効にならない問題を修正[#8103](https://github.com/pingcap/tidb/pull/8103)
    -   場合によっては DDL 操作がキャンセルされた後に正しくロールバックされない問題を修正します[#8057](https://github.com/pingcap/tidb/pull/8057)
    -   `admin show next_row_id`コマンドを追加して、次に利用可能な行 ID [#8268](https://github.com/pingcap/tidb/pull/8268)を返します。

## PD {#pd}

-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正
    -   [#1298](https://github.com/pingcap/pd/pull/1298)
    -   [#1299](https://github.com/pingcap/pd/pull/1299)
    -   [#1308](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` API が間違った結果を返す問題を修正[#1311](https://github.com/pingcap/pd/pull/1311)
-   PD 参加失敗後に PD が参加を再開できない問題を修正[#1279](https://github.com/pingcap/pd/pull/1279)
-   `watch leader`場合によってはイベントが失われる可能性がある問題を修正[#1317](https://github.com/pingcap/pd/pull/1317)

## TiKV {#tikv}

-   `WriteConflict` [#3750](https://github.com/tikv/tikv/pull/3750)のエラーメッセージを改善
-   panicマーク ファイル[#3746](https://github.com/tikv/tikv/pull/3746)を追加します
-   gRPC [#3650](https://github.com/tikv/tikv/pull/3650)の新しいバージョンによって引き起こされるセグメント障害の問題を回避するには、grpcio をダウングレードします。
-   `kv_scan`インターフェース[#3749](https://github.com/tikv/tikv/pull/3749)に上限を追加します

## ツール {#tools}

-   TiDB-Binlog クラスターをサポートします。これは、 binlog [#8093](https://github.com/pingcap/tidb/pull/8093)の古いバージョンと互換性がありません[ドキュメンテーション](/tidb-binlog/tidb-binlog-overview.md)

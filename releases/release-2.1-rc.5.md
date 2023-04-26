---
title: TiDB 2.1 RC5 Release Notes
---

<!-- markdownlint-disable MD032 -->

# TiDB 2.1 RC5 リリースノート {#tidb-2-1-rc5-release-notes}

2018 年 11 月 12 日に、TiDB 2.1 RC5 がリリースされました。 TiDB 2.1 RC4 と比較すると、このリリースでは、安定性、SQL オプティマイザー、統計情報、および実行エンジンが大幅に改善されています。

## TiDB {#tidb}

-   SQL オプティマイザー
    -   `IndexReader`場合によっては間違ったハンドルを読み取る問題を修正[#8132](https://github.com/pingcap/tidb/pull/8132)
    -   `IndexScan Prepared`ステートメントが`Plan Cache` [#8055](https://github.com/pingcap/tidb/pull/8055)を使用しているときに発生した問題を修正します。
    -   `Union`ステートメントの結果が不安定になる問題を修正[#8165](https://github.com/pingcap/tidb/pull/8165)
-   SQL 実行エンジン
    -   幅の広いテーブルを挿入または更新する際の TiDB のパフォーマンスを改善する[#8024](https://github.com/pingcap/tidb/pull/8024)
    -   `Truncate`組み込み関数[#8068](https://github.com/pingcap/tidb/pull/8068)で unsigned `int`フラグをサポート
    -   JSON データを 10 進数型に変換する際に発生したエラーを修正します[#8109](https://github.com/pingcap/tidb/pull/8109)
    -   float 型を`Update`にするとエラーが発生するのを修正[#8170](https://github.com/pingcap/tidb/pull/8170)
-   統計
    -   場合によっては、ポイント クエリ中の誤った統計の問題を修正します[#8035](https://github.com/pingcap/tidb/pull/8035)
    -   場合によっては、主キーの統計の選択性の推定を修正します[#8149](https://github.com/pingcap/tidb/pull/8149)
    -   削除されたテーブルの統計が長期間クリアされない問題を修正します[#8182](https://github.com/pingcap/tidb/pull/8182)
-   サーバ
    -   ログの読みやすさを改善し、ログをより良くします
        -   [#8063](https://github.com/pingcap/tidb/pull/8063)
        -   [#8053](https://github.com/pingcap/tidb/pull/8053)
        -   [#8224](https://github.com/pingcap/tidb/pull/8224)

    <!---->

    -   `infoschema.profiling` [#8096](https://github.com/pingcap/tidb/pull/8096)のテーブルデータ取得時にエラーが発生する問題を修正
    -   unix ソケットをポンプ クライアントに置き換えてバイナリログ[#8098](https://github.com/pingcap/tidb/pull/8098)を書き込みます。
    -   スローログ[#8094](https://github.com/pingcap/tidb/pull/8094)を動的に設定する`tidb_slow_log_threshold`環境変数のしきい値を追加します。
    -   `tidb_query_log_max_len`環境変数が動的にログを設定している間、切り捨てられた SQL ステートメントの元の長さを追加します[#8200](https://github.com/pingcap/tidb/pull/8200)
    -   `tidb_opt_write_row_id`環境変数を追加して、 `_tidb_rowid` [#8218](https://github.com/pingcap/tidb/pull/8218)の書き込みを許可するかどうかを制御します
    -   オーバーバウンド スキャンを回避するために、ticlient の`Scan`コマンドに上限を追加します[#8081](https://github.com/pingcap/tidb/pull/8081) , [#8247](https://github.com/pingcap/tidb/pull/8247)
-   DDL
    -   トランザクションで DDL ステートメントを実行すると、場合によってはエラーが発生する問題を修正します[#8056](https://github.com/pingcap/tidb/pull/8056)
    -   パーティションテーブルで`truncate table`実行しても有効にならない問題を修正[#8103](https://github.com/pingcap/tidb/pull/8103)
    -   場合によっては DDL 操作がキャンセルされた後、正しくロールバックされない問題を修正します[#8057](https://github.com/pingcap/tidb/pull/8057)
    -   `admin show next_row_id`コマンドを追加して、次に利用可能な行 ID [#8268](https://github.com/pingcap/tidb/pull/8268)を返します。

## PD {#pd}

-   `pd-ctl`リージョンキーの読み取りに関連する問題を修正します
    -   [#1298](https://github.com/pingcap/pd/pull/1298)
    -   [#1299](https://github.com/pingcap/pd/pull/1299)
    -   [#1308](https://github.com/pingcap/pd/pull/1308)
-   `regions/check` API が間違った結果を返す問題を修正[#1311](https://github.com/pingcap/pd/pull/1311)
-   PD の参加に失敗した後、PD が参加を再開できない問題を修正します[#1279](https://github.com/pingcap/pd/pull/1279)
-   `watch leader`場合によってはイベントが失われる可能性がある問題を修正します[#1317](https://github.com/pingcap/pd/pull/1317)

## TiKV {#tikv}

-   `WriteConflict` [#3750](https://github.com/tikv/tikv/pull/3750)のエラーメッセージを改善
-   panicマーク ファイル[#3746](https://github.com/tikv/tikv/pull/3746)を追加します。
-   grpcio をダウングレードして、gRPC [#3650](https://github.com/tikv/tikv/pull/3650)の新しいバージョンによって引き起こされるセグメント障害の問題を回避します
-   `kv_scan`インターフェースに上限を追加[#3749](https://github.com/tikv/tikv/pull/3749)

## ツール {#tools}

-   古いバージョンのbinlogと互換性がない TiDB-Binlog クラスターをサポートします[#8093](https://github.com/pingcap/tidb/pull/8093) 、 [ドキュメンテーション](/tidb-binlog/tidb-binlog-overview.md)

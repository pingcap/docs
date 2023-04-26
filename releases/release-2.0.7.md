---
title: TiDB 2.0.7 Release Notes
---

# TiDB 2.0.7 リリースノート {#tidb-2-0-7-release-notes}

2018 年 9 月 7 日に、TiDB 2.0.7 がリリースされました。 TiDB 2.0.6 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   `information_schema` [#7286](https://github.com/pingcap/tidb/pull/7286)に`PROCESSLIST`テーブルを追加
-   改善
    -   SQL ステートメントの実行に関する詳細を収集し、 `SLOW QUERY`ログに情報を出力します[#7364](https://github.com/pingcap/tidb/pull/7364)
    -   パーティション情報を`SHOW CREATE TABLE` [#7388](https://github.com/pingcap/tidb/pull/7388)にドロップします
    -   `ANALYZE`ステートメントを RC 分離レベルと低優先度[#7500](https://github.com/pingcap/tidb/pull/7500)に設定することで、ステートメントの実行効率を向上させます。
    -   一意のインデックスの追加を高速化する[#7562](https://github.com/pingcap/tidb/pull/7562)
    -   DDL 同時実行数を制御するオプションを追加します[#7563](https://github.com/pingcap/tidb/pull/7563)
-   バグの修正
    -   主キーが整数[#7298](https://github.com/pingcap/tidb/pull/7298)テーブルで`USE INDEX(PRIMARY)`を使用できない問題を修正
    -   内側の行が`NULL` [#7301](https://github.com/pingcap/tidb/pull/7301)の場合、 `Merge Join`と`Index Join`誤った結果を出力する問題を修正
    -   チャンクサイズの設定が小さすぎる場合に誤った結果を`Join`する問題を修正[#7315](https://github.com/pingcap/tidb/pull/7315)
    -   `range column` [#7379](https://github.com/pingcap/tidb/pull/7379)を含むテーブルを作成するステートメントによって引き起こされるpanicの問題を修正します。
    -   `admin check table`が時刻型の列のエラーを誤って報告する問題を修正[#7457](https://github.com/pingcap/tidb/pull/7457)
    -   デフォルト値`current_timestamp`のデータが`=`条件[#7467](https://github.com/pingcap/tidb/pull/7467)を使用してクエリできない問題を修正します
    -   `ComStmtSendLongData`コマンドを使用して挿入された長さ 0 のパラメーターが誤って NULL に解析される問題を修正します[#7508](https://github.com/pingcap/tidb/pull/7508)
    -   特定のシナリオで`auto analyze`が繰り返し実行される問題を修正[#7556](https://github.com/pingcap/tidb/pull/7556)
    -   改行文字で終わる単一行のコメントをパーサーが解析できない問題を修正します[#7635](https://github.com/pingcap/tidb/pull/7635)

## TiKV {#tikv}

-   改善
    -   スペース増幅を減らすために、デフォルトで空のクラスターで`dynamic-level-bytes`パラメーターを開きます
-   バグ修正
    -   リージョンのマージ後のリージョンの更新`approximate size`と`approximate keys count`

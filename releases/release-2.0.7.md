---
title: TiDB 2.0.7 Release Notes
---

# TiDB 2.0.7 リリースノート {#tidb-2-0-7-release-notes}

2018 年 9 月 7 日に、TiDB 2.0.7 がリリースされました。 TiDB 2.0.6 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   `information_schema` [#7286](https://github.com/pingcap/tidb/pull/7286)に`PROCESSLIST`テーブルを追加します
-   改善
    -   SQL ステートメントの実行に関する詳細を収集し、情報を`SLOW QUERY`ログ[#7364](https://github.com/pingcap/tidb/pull/7364)に出力します。
    -   `SHOW CREATE TABLE` [#7388](https://github.com/pingcap/tidb/pull/7388)にパーティション情報をドロップします
    -   `ANALYZE`ステートメントを RC 分離レベルおよび低優先度[#7500](https://github.com/pingcap/tidb/pull/7500)に設定することで、ステートメントの実行効率を向上させます。
    -   一意のインデックスの追加を高速化します[#7562](https://github.com/pingcap/tidb/pull/7562)
    -   DDL 同時実行性を制御するオプションを追加[#7563](https://github.com/pingcap/tidb/pull/7563)
-   バグの修正
    -   主キーが整数[#7298](https://github.com/pingcap/tidb/pull/7298)テーブルでは`USE INDEX(PRIMARY)`使用できない問題を修正
    -   内側の行が`NULL` [#7301](https://github.com/pingcap/tidb/pull/7301)の場合、 `Merge Join`と`Index Join`誤った結果を出力する問題を修正
    -   `Join`チャンクサイズが小さすぎると誤った結果が出力される問題を修正[#7315](https://github.com/pingcap/tidb/pull/7315)
    -   `range column` [#7379](https://github.com/pingcap/tidb/pull/7379)を含むテーブルを作成するステートメントによって引き起こされるpanicの問題を修正
    -   `admin check table`が誤って時刻型列[#7457](https://github.com/pingcap/tidb/pull/7457)のエラーを報告する問題を修正
    -   デフォルト値`current_timestamp`のデータを`=`条件[#7467](https://github.com/pingcap/tidb/pull/7467)を使用してクエリできない問題を修正します。
    -   `ComStmtSendLongData`コマンドを使用して挿入された長さゼロのパラメータが誤って NULL [#7508](https://github.com/pingcap/tidb/pull/7508)に解析される問題を修正
    -   特定のシナリオで`auto analyze`が繰り返し実行される問題を修正[#7556](https://github.com/pingcap/tidb/pull/7556)
    -   パーサーが改行文字で終わる 1 行のコメントを解析できない問題を修正します[#7635](https://github.com/pingcap/tidb/pull/7635)

## TiKV {#tikv}

-   改善
    -   スペースの増幅を減らすために、デフォルトで空のクラスターの`dynamic-level-bytes`パラメーターを開きます。
-   バグ修正
    -   リージョンの結合後のリージョンの`approximate size`と`approximate keys count`を更新する

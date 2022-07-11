---
title: TiDB 2.0.7 Release Notes
---

# TiDB2.0.7リリースノート {#tidb-2-0-7-release-notes}

2018年9月7日、TiDB2.0.7がリリースされました。 TiDB 2.0.6と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   35に`PROCESSLIST` [＃7286](https://github.com/pingcap/tidb/pull/7286)テーブルを追加し`information_schema`
-   改善
    -   SQLステートメントの実行に関する詳細を収集し、その情報を`SLOW QUERY`ログ[＃7364](https://github.com/pingcap/tidb/pull/7364)に出力します。
    -   [＃7388](https://github.com/pingcap/tidb/pull/7388)にパーティション情報をドロップし`SHOW CREATE TABLE`
    -   `ANALYZE`ステートメントをRC分離レベルおよび低優先度[＃7500](https://github.com/pingcap/tidb/pull/7500)に設定することにより、実行効率を向上させます。
    -   一意のインデックスの追加を高速化[＃7562](https://github.com/pingcap/tidb/pull/7562)
    -   DDL同時実行を制御するオプションを追加する[＃7563](https://github.com/pingcap/tidb/pull/7563)
-   バグの修正
    -   主キーが整数[＃7298](https://github.com/pingcap/tidb/pull/7298)であるテーブルで`USE INDEX(PRIMARY)`を使用できない問題を修正します。
    -   内側の行が[＃7301](https://github.com/pingcap/tidb/pull/7301)の場合、 `Merge Join`と`Index Join`が誤った結果を出力する問題を修正し`NULL` 。
    -   チャンクサイズの設定が小さすぎる場合に`Join`が誤った結果を出力する問題を修正します[＃7315](https://github.com/pingcap/tidb/pull/7315)
    -   `range column`を含むテーブルを作成するステートメントによって引き起こされるpanicの問題を修正し[＃7379](https://github.com/pingcap/tidb/pull/7379)
    -   `admin check table`が時間タイプの列[＃7457](https://github.com/pingcap/tidb/pull/7457)のエラーを誤って報告する問題を修正します
    -   デフォルト値`current_timestamp`のデータは、 `=`条件[＃7467](https://github.com/pingcap/tidb/pull/7467)を使用してクエリできないという問題を修正します。
    -   `ComStmtSendLongData`コマンドを使用して挿入された長さゼロのパラメーターが誤って[＃7508](https://github.com/pingcap/tidb/pull/7508)に解析される問題を修正します。
    -   `auto analyze`が特定のシナリオで繰り返し実行される問題を修正します[＃7556](https://github.com/pingcap/tidb/pull/7556)
    -   パーサーが改行文字[＃7635](https://github.com/pingcap/tidb/pull/7635)で終わる1行のコメントを解析できない問題を修正します

## TiKV {#tikv}

-   改善
    -   スペースの増幅を減らすために、デフォルトで空のクラスタで`dynamic-level-bytes`パラメーターを開きます
-   バグ修正
    -   リージョンのマージ後、リージョンの`approximate size`と`approximate keys count`を更新します

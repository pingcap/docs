---
title: TiDB 2.0.7 Release Notes
summary: TiDB 2.0.7 は、システムの互換性と安定性の向上を伴い、2018 年 9 月 7 日にリリースされました。新機能には、information_schema` の `PROCESSLIST` テーブルの追加が含まれます。バグ修正により、インデックスの使用、結合出力、およびクエリ条件に関する問題が対処されています。TiKV は、スペース増幅を減らすためにデフォルトで `dynamic-level-bytes` パラメータを開き、リージョンのマージ後におおよそのサイズとキー数を更新するようになりました。
---

# TiDB 2.0.7 リリースノート {#tidb-2-0-7-release-notes}

2018 年 9 月 7 日に、TiDB 2.0.7 がリリースされました。TiDB 2.0.6 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## ティビ {#tidb}

-   新機能
    -   `information_schema` [＃7286](https://github.com/pingcap/tidb/pull/7286)の`PROCESSLIST`テーブルを追加します
-   改善
    -   SQL文の実行に関する詳細を収集し、その情報を`SLOW QUERY`ログ[＃7364](https://github.com/pingcap/tidb/pull/7364)に出力します。
    -   `SHOW CREATE TABLE` [＃7388](https://github.com/pingcap/tidb/pull/7388)のパーティション情報をドロップします
    -   `ANALYZE`文を RC 分離レベルと低優先度[＃7500](https://github.com/pingcap/tidb/pull/7500)に設定して実行効率を向上させる
    -   ユニークインデックスの追加を高速化[＃7562](https://github.com/pingcap/tidb/pull/7562)
    -   DDL同時実行を制御するオプションを追加[＃7563](https://github.com/pingcap/tidb/pull/7563)
-   バグ修正
    -   主キーが整数[＃7298](https://github.com/pingcap/tidb/pull/7298)であるテーブルでは`USE INDEX(PRIMARY)`使用できない問題を修正
    -   内側の行が`NULL` [＃7301](https://github.com/pingcap/tidb/pull/7301)の場合に`Merge Join`と`Index Join`誤った結果を出力する問題を修正しました
    -   チャンクサイズが小さすぎると誤った結果が`Join`される問題を修正しました[＃7315](https://github.com/pingcap/tidb/pull/7315)
    -   `range column` [＃7379](https://github.com/pingcap/tidb/pull/7379)を含むテーブルを作成するステートメントによって発生するpanic問題を修正しました
    -   `admin check table`時刻型列のエラーを誤って報告する問題を修正[＃7457](https://github.com/pingcap/tidb/pull/7457)
    -   デフォルト値`current_timestamp`のデータを条件`=`を使用してクエリできない問題を修正[＃7467](https://github.com/pingcap/tidb/pull/7467)
    -   `ComStmtSendLongData`コマンドを使用して挿入された長さゼロのパラメータが誤って NULL [＃7508](https://github.com/pingcap/tidb/pull/7508)として解析される問題を修正
    -   特定のシナリオで`auto analyze`が繰り返し実行される問題を修正[＃7556](https://github.com/pingcap/tidb/pull/7556)
    -   パーサーが改行文字で終わる単一行コメントを解析できない問題を修正[＃7635](https://github.com/pingcap/tidb/pull/7635)

## ティクヴ {#tikv}

-   改善
    -   スペース増幅を減らすために、デフォルトで空のクラスターで`dynamic-level-bytes`パラメータを開きます。
-   バグ修正
    -   リージョン統合後のリージョンの更新`approximate size`と`approximate keys count`

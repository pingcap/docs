---
title: TiDB 2.0.7 Release Notes
summary: TiDB 2.0.7は2018年9月7日にリリースされ、システムの互換性と安定性が向上しました。新機能には、information_schema`への`PROCESSLIST`テーブルの追加が含まれます。バグ修正では、インデックスの使用、結合出力、クエリ条件に関する問題が修正されました。TiKVは、スペースの増幅を軽減するためにデフォルトで`dynamic-level-bytes`パラメータを開き、リージョンマージ後におおよそのサイズとキー数を更新するようになりました。
---

# TiDB 2.0.7 リリースノート {#tidb-2-0-7-release-notes}

2018年9月7日にTiDB 2.0.7がリリースされました。TiDB 2.0.6と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   新機能
    -   `information_schema` の`PROCESSLIST`テーブルを追加します [＃7286](https://github.com/pingcap/tidb/pull/7286)
-   改善
    -   SQL文の実行に関する詳細を収集し、その情報を`SLOW QUERY`ログに出力します。 [＃7364](https://github.com/pingcap/tidb/pull/7364)
    -   `SHOW CREATE TABLE` のパーティション情報をドロップします [＃7388](https://github.com/pingcap/tidb/pull/7388)
    -   `ANALYZE`文を RC 分離レベルと低優先度に設定して実行効率を改善します。 [＃7500](https://github.com/pingcap/tidb/pull/7500)
    -   一意インデックスの追加を高速化[＃7562](https://github.com/pingcap/tidb/pull/7562)
    -   DDL同時実行を制御するオプションを追加[＃7563](https://github.com/pingcap/tidb/pull/7563)
-   バグ修正
    -   主キーが整数であるテーブルでは`USE INDEX(PRIMARY)`を使用できない問題を修正 [＃7298](https://github.com/pingcap/tidb/pull/7298)
    -   内側の行が`NULL` の場合に`Merge Join`と`Index Join`が誤った結果を出力する問題を修正しました [＃7301](https://github.com/pingcap/tidb/pull/7301)
    -   チャンク`Join`が小さすぎると誤った結果が出力される問題を修正しました[＃7315](https://github.com/pingcap/tidb/pull/7315)
    -   `range column` を含むテーブルを作成するステートメントによって発生するpanic問題を修正しました [＃7379](https://github.com/pingcap/tidb/pull/7379)
    -   `admin check table`時刻型列のエラーを誤って報告する問題を修正[＃7457](https://github.com/pingcap/tidb/pull/7457)
    -   デフォルト値`current_timestamp`のデータが条件`=`を使用してクエリできない問題を修正しました。 [＃7467](https://github.com/pingcap/tidb/pull/7467)
    -   `ComStmtSendLongData`コマンドを使用して挿入された長さゼロのパラメータが誤って NULL として解析される問題を修正しました [＃7508](https://github.com/pingcap/tidb/pull/7508)
    -   特定のシナリオで`auto analyze`が繰り返し実行される問題を修正[＃7556](https://github.com/pingcap/tidb/pull/7556)
    -   改行文字で終わる1行コメントをパーサーが解析できない問題を修正[＃7635](https://github.com/pingcap/tidb/pull/7635)

## TiKV {#tikv}

-   改善
    -   スペース増幅を減らすために、デフォルトで空のクラスター内の`dynamic-level-bytes`パラメータを開きます。
-   バグ修正
    -   リージョン統合後のリージョンの更新`approximate size`と`approximate keys count`

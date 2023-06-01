---
title: TiDB 2.1.2 Release Notes
---

# TiDB 2.1.2 リリースノート {#tidb-2-1-2-release-notes}

2018 年 12 月 22 日に、TiDB 2.1.2 がリリースされました。対応する TiDB Ansible 2.1.2 もリリースされています。 TiDB 2.1.1 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   TiDB を Kafka バージョン[<a href="https://github.com/pingcap/tidb/pull/8747">#8747</a>](https://github.com/pingcap/tidb/pull/8747)の TiDB Binlogと互換性を持たせる
-   ローリング アップデート[<a href="https://github.com/pingcap/tidb/pull/8707">#8707</a>](https://github.com/pingcap/tidb/pull/8707)で TiDB の終了メカニズムを改善します。
-   場合によっては、生成された列のインデックスを追加することによって引き起こされるpanicの問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8676">#8676</a>](https://github.com/pingcap/tidb/pull/8676)
-   SQL ステートメントに`TIDB_SMJ Hint`が存在する場合、オプティマイザが最適なクエリ プランを見つけられない場合がある問題を修正します[<a href="https://github.com/pingcap/tidb/pull/8729">#8729</a>](https://github.com/pingcap/tidb/pull/8729)
-   `AntiSemiJoin`場合によっては不正な結果が返される問題を修正[<a href="https://github.com/pingcap/tidb/pull/8730">#8730</a>](https://github.com/pingcap/tidb/pull/8730)
-   `utf8`文字セット[<a href="https://github.com/pingcap/tidb/pull/8754">#8754</a>](https://github.com/pingcap/tidb/pull/8754)の有効文字チェックを改善
-   トランザクション[<a href="https://github.com/pingcap/tidb/pull/8746">#8746</a>](https://github.com/pingcap/tidb/pull/8746)で読み取り操作の前に書き込み操作が実行されると、時刻型のフィールドが誤った結果を返す可能性がある問題を修正します。

## PD {#pd}

-   リージョンマージ[<a href="https://github.com/pingcap/pd/pull/1377">#1377</a>](https://github.com/pingcap/pd/pull/1377)に関するリージョン情報更新の問題を修正

## TiKV {#tikv}

-   `DAY` ( `d` ) 単位の構成フォーマットをサポートし、構成互換性の問題を修正します[<a href="https://github.com/tikv/tikv/pull/3931">#3931</a>](https://github.com/tikv/tikv/pull/3931)
-   `Approximate Size Split` [<a href="https://github.com/tikv/tikv/pull/3942">#3942</a>](https://github.com/tikv/tikv/pull/3942)によって発生する可能性のpanicの問題を修正
-   リージョンのマージ[<a href="https://github.com/tikv/tikv/pull/3822">#3822</a>](https://github.com/tikv/tikv/pull/3822) 、 [<a href="https://github.com/tikv/tikv/pull/3873">#3873</a>](https://github.com/tikv/tikv/pull/3873)に関する 2 つの問題を修正

## ツール {#tools}

-   TiDB Lightning
    -   TiDB 2.1.0 を Lightning でサポートされる最小クラスタバージョンにする
    -   Lightning [<a href="https://github.com/pingcap/tidb-tools/issues/144">#144</a>](https://github.com/pingcap/tidb-tools/issues/144)の解析済み`JSON`データを含むファイルの内容エラーを修正
    -   Lightning を再起動するためにチェックポイントが使用された後に`Too many open engines`が発生する問題を修正
-   TiDBBinlog
    -   Drainer がKafka にデータを書き込む際のいくつかのボトルネックを解消します。
    -   TiDB Binlogの Kafka バージョンをサポートする

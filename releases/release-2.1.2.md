---
title: TiDB 2.1.2 Release Notes
---

# TiDB 2.1.2 リリースノート {#tidb-2-1-2-release-notes}

2018 年 12 月 22 日に、TiDB 2.1.2 がリリースされました。対応する TiDB Ansible 2.1.2 もリリースされています。 TiDB 2.1.1 と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   TiDB を Kafka バージョン[#8747](https://github.com/pingcap/tidb/pull/8747)の TiDB Binlogと互換性を持たせる
-   ローリング アップデート[#8707](https://github.com/pingcap/tidb/pull/8707)で TiDB の終了メカニズムを改善します。
-   場合によっては、生成された列のインデックスを追加することによって引き起こされるpanicの問題を修正します[#8676](https://github.com/pingcap/tidb/pull/8676)
-   SQL ステートメントに`TIDB_SMJ Hint`が存在する場合、オプティマイザが最適なクエリ プランを見つけられない場合がある問題を修正します[#8729](https://github.com/pingcap/tidb/pull/8729)
-   `AntiSemiJoin`場合によっては不正な結果が返される問題を修正[#8730](https://github.com/pingcap/tidb/pull/8730)
-   `utf8`文字セット[#8754](https://github.com/pingcap/tidb/pull/8754)の有効文字チェックを改善
-   トランザクション[#8746](https://github.com/pingcap/tidb/pull/8746)で読み取り操作の前に書き込み操作が実行されると、時刻型のフィールドが誤った結果を返す可能性がある問題を修正します。

## PD {#pd}

-   リージョンマージ[#1377](https://github.com/pingcap/pd/pull/1377)に関するリージョン情報更新の問題を修正

## TiKV {#tikv}

-   `DAY` ( `d` ) 単位の構成フォーマットをサポートし、構成互換性の問題を修正します[#3931](https://github.com/tikv/tikv/pull/3931)
-   `Approximate Size Split` [#3942](https://github.com/tikv/tikv/pull/3942)によって発生する可能性のpanicの問題を修正
-   リージョンの[#3873](https://github.com/tikv/tikv/pull/3873) [#3822](https://github.com/tikv/tikv/pull/3822) 2 つの問題を修正

## ツール {#tools}

-   TiDB Lightning
    -   TiDB 2.1.0 を Lightning でサポートされる最小クラスタバージョンにする
    -   Lightning [#144](https://github.com/pingcap/tidb-tools/issues/144)の解析済み`JSON`データを含むファイルの内容エラーを修正
    -   Lightning を再起動するためにチェックポイントが使用された後に`Too many open engines`が発生する問題を修正
-   TiDBBinlog
    -   Drainer がKafka にデータを書き込む際のいくつかのボトルネックを解消します。
    -   TiDB Binlogの Kafka バージョンをサポートする

---
title: TiDB 2.1.2 Release Notes
---

# TiDB 2.1.2 リリースノート {#tidb-2-1-2-release-notes}

2018 年 12 月 22 日に、TiDB 2.1.2 がリリースされました。対応する TiDB Ansible 2.1.2 もリリースされています。 TiDB 2.1.1 と比較すると、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   TiDB を Kafka バージョン[#8747](https://github.com/pingcap/tidb/pull/8747)の TiDB Binlogと互換性を持たせる
-   ローリング アップデートでの TiDB の終了メカニズムを改善する[#8707](https://github.com/pingcap/tidb/pull/8707)
-   場合によっては、生成された列のインデックスを追加することによって引き起こされるpanicの問題を修正します[#8676](https://github.com/pingcap/tidb/pull/8676)
-   SQL文に`TIDB_SMJ Hint`存在する場合、オプティマイザが最適なクエリプランを見つけられないことがある問題を修正[#8729](https://github.com/pingcap/tidb/pull/8729)
-   `AntiSemiJoin`場合によっては間違った結果を返す問題を修正[#8730](https://github.com/pingcap/tidb/pull/8730)
-   `utf8`文字セットの有効文字チェックを改善[#8754](https://github.com/pingcap/tidb/pull/8754)
-   トランザクション[#8746](https://github.com/pingcap/tidb/pull/8746)で、読み取り操作の前に書き込み操作が実行されると、時間型のフィールドが誤った結果を返すことがある問題を修正します。

## PD {#pd}

-   リージョン統合に関するリージョン情報の更新の問題を修正[#1377](https://github.com/pingcap/pd/pull/1377)

## TiKV {#tikv}

-   `DAY` ( `d` ) 単位の構成フォーマットをサポートし、構成の互換性の問題を修正します[#3931](https://github.com/tikv/tikv/pull/3931)
-   `Approximate Size Split` [#3942](https://github.com/tikv/tikv/pull/3942)によって引き起こされる可能性のあるpanicの問題を修正します
-   リージョンのマージに関する 2 つの問題を修正[#3822](https://github.com/tikv/tikv/pull/3822) 、 [#3873](https://github.com/tikv/tikv/pull/3873)

## ツール {#tools}

-   TiDB Lightning
    -   TiDB 2.1.0 を Lightning でサポートされる最小クラスター バージョンにする
    -   Lightning [#144](https://github.com/pingcap/tidb-tools/issues/144)で解析された`JSON`データを含むファイルのコンテンツ エラーを修正します。
    -   チェックポイントを使用してLightningを再起動した後に`Too many open engines`が発生する問題を修正
-   TiDBBinlog
    -   Drainer がKafka にデータを書き込む際のボトルネックを解消する
    -   TiDB Binlogの Kafka バージョンをサポート

---
title: TiDB 2.1.2 Release Notes
---

# TiDB2.1.2リリースノート {#tidb-2-1-2-release-notes}

2018年12月22日、TiDB2.1.2がリリースされました。対応するTiDBAnsible2.1.2もリリースされています。 TiDB 2.1.1と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   TiDBをKafkaバージョン[＃8747](https://github.com/pingcap/tidb/pull/8747)のTiDBBinlogと互換性を持たせる
-   ローリングアップデートでTiDBの終了メカニズムを改善する[＃8707](https://github.com/pingcap/tidb/pull/8707)
-   場合によっては、生成された列のインデックスを追加することによって引き起こされるパニックの問題を修正します[＃8676](https://github.com/pingcap/tidb/pull/8676)
-   SQLステートメントに`TIDB_SMJ Hint`が存在する場合、オプティマイザーが最適なクエリプランを見つけられない場合があるという問題を修正します[＃8729](https://github.com/pingcap/tidb/pull/8729)
-   `AntiSemiJoin`が誤った結果を返す場合があるという問題を修正します[＃8730](https://github.com/pingcap/tidb/pull/8730)
-   `utf8`文字セット[＃8754](https://github.com/pingcap/tidb/pull/8754)の有効な文字チェックを改善します
-   トランザクション[＃8746](https://github.com/pingcap/tidb/pull/8746)で読み取り操作の前に書き込み操作を実行すると、時間タイプのフィールドが誤った結果を返す可能性がある問題を修正します。

## PD {#pd}

-   リージョンマージ[＃1377](https://github.com/pingcap/pd/pull/1377)に関するリージョン情報の更新の問題を修正します

## TiKV {#tikv}

-   `DAY` （ `d` ）単位の構成形式をサポートし、構成の互換性の問題を修正します[＃3931](https://github.com/tikv/tikv/pull/3931)
-   `Approximate Size Split`によって引き起こされる可能性のあるパニックの問題を修正し[＃3942](https://github.com/tikv/tikv/pull/3942)
-   リージョンマージ[＃3822](https://github.com/tikv/tikv/pull/3822)に関する2つの問題を修正し[＃3873](https://github.com/tikv/tikv/pull/3873)

## ツール {#tools}

-   TiDB Lightning
    -   TiDB2.1.0をLightningでサポートされる最小クラスタバージョンにします
    -   [＃144](https://github.com/pingcap/tidb-tools/issues/144)で解析された`JSON`データを含むファイルのコンテンツエラーを修正しました
    -   チェックポイントを使用してLightningを再起動した後に`Too many open engines`が発生する問題を修正します
-   TiDB Binlog
    -   DrainerがKafkaにデータを書き込む際のボトルネックを解消します
    -   TiDBBinlogのKafkaバージョンをサポートする

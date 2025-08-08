---
title: TiDB 2.1.2 Release Notes
summary: TiDB 2.1.2およびTiDB Ansible 2.1.2は、2018年12月22日にリリースされました。このリリースでは、システムの互換性と安定性が向上しています。主なアップデートには、KafkaバージョンのTiDB Binlogとの互換性、ローリングアップデート中の終了メカニズムの改善、およびさまざまな問題の修正が含まれます。PDとTiKVにもアップデートが加えられ、リージョンマージの問題の修正や「DAY」単位の設定形式のサポートなどが行われました。さらに、 TiDB LightningとTiDB Binlogアップデートされ、新機能のサポートとボトルネックの解消が図られました。
---

# TiDB 2.1.2 リリースノート {#tidb-2-1-2-release-notes}

2018年12月22日にTiDB 2.1.2がリリースされました。対応するTiDB Ansible 2.1.2もリリースされました。TiDB 2.1.1と比較して、このリリースではシステムの互換性と安定性が大幅に向上しています。

## TiDB {#tidb}

-   TiDB を Kafka バージョン[＃8747](https://github.com/pingcap/tidb/pull/8747)の TiDB Binlogと互換性を持たせる
-   ローリングアップデート[＃8707](https://github.com/pingcap/tidb/pull/8707)におけるTiDBの終了メカニズムの改善
-   生成された列にインデックスを追加することで発生するpanic問題を修正[＃8676](https://github.com/pingcap/tidb/pull/8676)
-   一部のケースでSQL文に`TIDB_SMJ Hint`存在する場合にオプティマイザが最適なクエリプランを見つけられない問題を修正[＃8729](https://github.com/pingcap/tidb/pull/8729)
-   `AntiSemiJoin`場合によっては誤った結果が返される問題を修正[＃8730](https://github.com/pingcap/tidb/pull/8730)
-   `utf8`文字セット[＃8754](https://github.com/pingcap/tidb/pull/8754)の有効文字チェックの改善
-   トランザクション[＃8746](https://github.com/pingcap/tidb/pull/8746)で読み取り操作の前に書き込み操作を実行すると、時間型のフィールドが誤った結果を返す可能性がある問題を修正しました。

## PD {#pd}

-   リージョン統合[＃1377](https://github.com/pingcap/pd/pull/1377)に関するリージョン情報更新の問題を修正

## TiKV {#tikv}

-   `DAY` （ `d` ）単位の設定フォーマットをサポートし、設定の互換性の問題を修正しました[＃3931](https://github.com/tikv/tikv/pull/3931)
-   `Approximate Size Split` [＃3942](https://github.com/tikv/tikv/pull/3942)によって引き起こされる可能性のあるpanic問題を修正
-   リージョンマージ[＃3822](https://github.com/tikv/tikv/pull/3822)に関する2つの問題[＃3873](https://github.com/tikv/tikv/pull/3873)修正

## ツール {#tools}

-   TiDB Lightning
    -   Lightning でサポートされる最小のクラスタバージョンを TiDB 2.1.0 にする
    -   Lightning [＃144](https://github.com/pingcap/tidb-tools/issues/144)で解析された`JSON`データを含むファイルのコンテンツエラーを修正しました
    -   チェックポイントを使用してLightningを再起動した後に`Too many open engines`発生する問題を修正しました
-   TiDBBinlog
    -   Drainer がKafka にデータを書き込む際のボトルネックを解消
    -   TiDB Binlogの Kafka バージョンをサポート

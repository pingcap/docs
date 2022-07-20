---
title: TiDB 5.2.1 Release Notes
---

# TiDB5.2.1リリースノート {#tidb-5-2-1-release-notes}

発売日：2021年9月9日

TiDBバージョン：5.2.1

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行プランが原因で実行中に発生するエラーを修正します。誤った実行プランは、パーティションテーブルの集計演算子をプッシュダウンするときのスキーマ列の浅いコピーが原因で発生します。 [＃27797](https://github.com/pingcap/tidb/issues/27797) [＃26554](https://github.com/pingcap/tidb/issues/26554)

-   TiKV

    -   リージョンの移行時にRaftstoreのデッドロックが原因で発生するTiKVが利用できない問題を修正します。回避策は、スケジューリングを無効にして、使用できないTiKVを再起動することです。 [＃10909](https://github.com/tikv/tikv/issues/10909)

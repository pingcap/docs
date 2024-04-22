---
title: TiDB 5.2.1 Release Notes
summary: TiDB 5.2.1は2021年9月9日にリリースされました。このバージョンでは、TiDBとTiKVのバグが修正されています。TiDBの修正では、間違った実行計画が原因で発生するエラーが修正され、TiKVの修正では、リージョンの移行時にRaftstoreのデッドロックが原因でTiKVが利用できなくなる問題が修正されました。
---

# TiDB 5.2.1 リリースノート {#tidb-5-2-1-release-notes}

発売日：2021年9月9日

TiDB バージョン: 5.2.1

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行計画が原因で実行中に発生するエラーを修正します。間違った実行プランは、パーティション化されたテーブルで集計演算子をプッシュダウンするときにスキーマ列の浅いコピーが原因で発生します。 [#27797](https://github.com/pingcap/tidb/issues/27797) [#26554](https://github.com/pingcap/tidb/issues/26554)

-   TiKV

    -   リージョンの移行時にRaftstore のデッドロックが原因で TiKV が利用できなくなる問題を修正します。回避策は、スケジュールを無効にして、利用できない TiKV を再起動することです。 [#10909](https://github.com/tikv/tikv/issues/10909)

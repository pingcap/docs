---
title: TiDB 5.2.1 Release Notes
---

# TiDB 5.2.1 リリースノート {#tidb-5-2-1-release-notes}

発売日：2021年9月9日

TiDB バージョン: 5.2.1

## バグの修正 {#bug-fixes}

-   TiDB

    -   間違った実行計画が原因で実行中に発生するエラーを修正します。間違った実行プランは、パーティション化されたテーブルで集計演算子をプッシュダウンするときにスキーマ列の浅いコピーが原因で発生します。 [<a href="https://github.com/pingcap/tidb/issues/27797">#27797</a>](https://github.com/pingcap/tidb/issues/27797) [<a href="https://github.com/pingcap/tidb/issues/26554">#26554</a>](https://github.com/pingcap/tidb/issues/26554)

-   TiKV

    -   リージョンの移行時にRaftstore のデッドロックが原因で TiKV が利用できなくなる問題を修正します。回避策は、スケジュールを無効にして、利用できない TiKV を再起動することです。 [<a href="https://github.com/tikv/tikv/issues/10909">#10909</a>](https://github.com/tikv/tikv/issues/10909)

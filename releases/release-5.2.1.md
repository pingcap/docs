---
title: TiDB 5.2.1 Release Notes
summary: TiDB 5.2.1 は 2021 年 9 月 9 日にリリースされました。バグ修正には、誤った実行プランによって発生した TiDB のエラーの解決と、リージョンの移行時にRaftstoreデッドロックによって発生する TiKV が利用できなくなる問題の修正が含まれます。
---

# TiDB 5.2.1 リリースノート {#tidb-5-2-1-release-notes}

発売日: 2021年9月9日

TiDB バージョン: 5.2.1

## バグ修正 {#bug-fixes}

-   ティビ

    -   実行中に発生するエラーを修正します。実行プランが間違っているため、パーティション化されたテーブルで集計演算子[＃26554](https://github.com/pingcap/tidb/issues/26554)プッシュダウンするときにスキーマ列の浅いコピーによって間違った実行プランが発生します。1 [＃27797](https://github.com/pingcap/tidb/issues/27797)

-   ティクヴ

    -   リージョンの移行時にRaftstore のデッドロックによって TiKV が利用できなくなる問題を修正しました。回避策としては、スケジュールを無効にして、利用できない TiKV を再起動します[＃10909](https://github.com/tikv/tikv/issues/10909)

---
title: TiDB 3.0.13 Release Notes
summary: TiDB 3.0.13 は 2020 年 4 月 22 日にリリースされました。バグ修正には、INSERT ... ON DUPLICATE KEY UPDATE` ステートメントの問題の解決と、TiKV の `リージョン Merge` 中にシステムが停止して使用できなくなる問題の修正が含まれています。
---

# TiDB 3.0.13 リリースノート {#tidb-3-0-13-release-notes}

発売日：2020年4月22日

TiDB バージョン: 3.0.13

## バグ修正 {#bug-fixes}

-   TiDB

    -   ユーザーが重複するデータ[＃16690](https://github.com/pingcap/tidb/pull/16690)の複数行を挿入する必要がある場合に、トランザクション内で`INSERT ... ON DUPLICATE KEY UPDATE`ステートメントが誤って実行される可能性があるという、チェックされていない`MemBuffer`によって発生する問題を修正しました。

-   TiKV

    -   `Region Merge`繰り返し実行するとシステムが停止し、サービスが利用できなくなる問題を修正[＃7612](https://github.com/tikv/tikv/pull/7612)

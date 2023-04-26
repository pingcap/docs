---
title: TiDB 3.0.13 Release Notes
---

# TiDB 3.0.13 リリースノート {#tidb-3-0-13-release-notes}

発売日：2020年4月22日

TiDB バージョン: 3.0.13

## バグの修正 {#bug-fixes}

-   TiDB

    -   ユーザーが重複データの複数の行を挿入する必要がある場合、トランザクション内`INSERT ... ON DUPLICATE KEY UPDATE`ステートメントが正しく実行されない可能性があるという未チェック`MemBuffer`によって引き起こされる問題を修正します[#16690](https://github.com/pingcap/tidb/pull/16690)

-   TiKV

    -   `Region Merge`を繰り返し実行するとシステムがスタックしてサービスが利用できなくなる問題を修正[#7612](https://github.com/tikv/tikv/pull/7612)

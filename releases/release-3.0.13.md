---
title: TiDB 3.0.13 Release Notes
---

# TiDB3.0.13リリースノート {#tidb-3-0-13-release-notes}

発売日：2020年4月22日

TiDBバージョン：3.0.13

## バグの修正 {#bug-fixes}

-   TiDB

    -   チェックされていない`MemBuffer`によって引き起こされる問題を修正します。ユーザーが重複データの複数の行を挿入する必要がある場合、トランザクション内で`INSERT ... ON DUPLICATE KEY UPDATE`ステートメントが正しく実行されない可能性があります[＃16690](https://github.com/pingcap/tidb/pull/16690)

-   TiKV

    -   `Region Merge`を繰り返し実行すると、システムがスタックしてサービスが利用できなくなる可能性がある問題を修正します[＃7612](https://github.com/tikv/tikv/pull/7612)

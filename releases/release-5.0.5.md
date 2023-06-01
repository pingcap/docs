---
title: TiDB 5.0.5 Release Note
---

# TiDB 5.0.5 リリースノート {#tidb-5-0-5-release-note}

発売日：2021年12月3日

TiDB バージョン: 5.0.5

## バグ修正 {#bug-fix}

-   TiKV

    -   複数のキーで呼び出された場合に`GcKeys`タスクが動作しない問題を修正します。この問題が原因で、圧縮フィルター GC が MVCC 削除情報を削除しない可能性があります。 [#11217](https://github.com/tikv/tikv/issues/11217)

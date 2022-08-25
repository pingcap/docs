---
title: TiDB 5.2.3 Release Note
---

# TiDB 5.2.3 リリースノート {#tidb-5-2-3-release-note}

発売日：2021年12月3日

TiDB バージョン: 5.2.3

## バグ修正 {#bug-fix}

-   TiKV

    -   複数のキーで1つのタスクを呼び出すと、 `GcKeys`のタスクが動作しない問題を修正。この問題が原因で、コンパクション フィルター GC が MVCC 削除情報をドロップしない場合があります。 [#11217](https://github.com/tikv/tikv/issues/11217)

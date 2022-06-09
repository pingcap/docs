---
title: TiDB 5.0.5 Release Note
---

# TiDB5.0.5リリースノート {#tidb-5-0-5-release-note}

発売日：2021年12月3日

TiDBバージョン：5.0.5

## バグ修正 {#bug-fix}

-   TiKV

    -   複数のキーで呼び出されたときに`GcKeys`のタスクが機能しない問題を修正します。この問題が原因で、圧縮ファイラーGCがMVCC削除情報をドロップしない場合があります。 [＃11217](https://github.com/tikv/tikv/issues/11217)

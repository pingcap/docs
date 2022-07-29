---
title: TiDB 5.0.5 Release Note
---

# TiDB5.0.5リリースノート {#tidb-5-0-5-release-note}

発売日：2021年12月3日

TiDBバージョン：5.0.5

## バグ修正 {#bug-fix}

-   TiKV

    -   `GcKeys`のタスクが複数のキーによって呼び出されたときに機能しないという問題を修正します。この問題が原因で、圧縮ファイラーGCがMVCC削除情報をドロップしない場合があります。 [＃11217](https://github.com/tikv/tikv/issues/11217)

---
title: TiDB 4.0.4 Release Notes
---

# TiDB 4.0.4 リリースノート {#tidb-4-0-4-release-notes}

発売日：2020年7月31日

TiDB バージョン: 4.0.4

## バグの修正 {#bug-fixes}

-   TiDB

    -   `information_schema.columns` [#18849](https://github.com/pingcap/tidb/pull/18849)のクエリ時にスタックする問題を修正
    -   `PointGet`および`BatchPointGet`演算子が`in null` [#18848](https://github.com/pingcap/tidb/pull/18848)に遭遇したときに発生するエラーを修正しました。
    -   `BatchPointGet` [#18815](https://github.com/pingcap/tidb/pull/18815)の間違った結果を修正します
    -   `HashJoin`演算子が`set`または`enum`タイプ[#18859](https://github.com/pingcap/tidb/pull/18859)に遭遇したときに発生する誤ったクエリ結果の問題を修正します。

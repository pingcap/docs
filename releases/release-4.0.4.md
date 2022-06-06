---
title: TiDB 4.0.4 Release Notes
---

# TiDB4.0.4リリースノート {#tidb-4-0-4-release-notes}

発売日：2020年7月31日

TiDBバージョン：4.0.4

## バグの修正 {#bug-fixes}

-   TiDB

    -   `information_schema.columns`をクエリするときにスタックする問題を修正し[＃18849](https://github.com/pingcap/tidb/pull/18849)
    -   `PointGet`および`BatchPointGet`オペレーターが[＃18848](https://github.com/pingcap/tidb/pull/18848)に遭遇したときに発生するエラーを修正し`in null`
    -   [＃18815](https://github.com/pingcap/tidb/pull/18815)の間違った結果を修正し`BatchPointGet`
    -   `HashJoin`オペレーターが`set`または`enum`タイプ[＃18859](https://github.com/pingcap/tidb/pull/18859)に遭遇したときに発生する誤ったクエリ結果の問題を修正します

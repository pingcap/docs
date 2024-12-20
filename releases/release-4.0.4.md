---
title: TiDB 4.0.4 Release Notes
summary: TiDB 4.0.4 は 2020 年 7 月 31 日にリリースされました。バグ修正には、information_schema.columns` のクエリに関する問題、`PointGet` および `BatchPointGet` 演算子のエラー、`BatchPointGet` の誤った結果、`set` または `enum` 型に遭遇した `HashJoin` 演算子の誤ったクエリ結果が含まれます。
---

# TiDB 4.0.4 リリースノート {#tidb-4-0-4-release-notes}

発売日: 2020年7月31日

TiDB バージョン: 4.0.4

## バグ修正 {#bug-fixes}

-   ティビ

    -   クエリ実行時にスタックする問題を修正`information_schema.columns` [＃18849](https://github.com/pingcap/tidb/pull/18849)
    -   `PointGet`と`BatchPointGet`演算子が`in null` [＃18848](https://github.com/pingcap/tidb/pull/18848)に遭遇したときに発生するエラーを修正します
    -   `BatchPointGet` [＃18815](https://github.com/pingcap/tidb/pull/18815)の間違った結果を修正
    -   `HashJoin`演算子が`set`または`enum`型に遭遇したときに発生する不正なクエリ結果の問題を修正しました[＃18859](https://github.com/pingcap/tidb/pull/18859)

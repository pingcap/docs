---
title: TiDB 1.0.4 Release Notes
---

# TiDB1.0.4リリースノート {#tidb-1-0-4-release-notes}

2017年12月11日に、TiDB 1.0.4がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`tidb-server`を起動するときの統計のロードを高速化します](https://github.com/pingcap/tidb/pull/5362)
-   [`show variables`ステートメントのパフォーマンスを改善します](https://github.com/pingcap/tidb/pull/5363)
-   [`Add Index`ステートメントを使用して結合されたインデックスを処理する際の潜在的な問題を修正します](https://github.com/pingcap/tidb/pull/5323)
-   [`Rename Table`ステートメントを使用してテーブルを別のデータベースに移動するときに発生する可能性のある問題を修正します](https://github.com/pingcap/tidb/pull/5314)
-   [`Alter/Drop User`ステートメントの有効性を加速します](https://github.com/pingcap/tidb/pull/5226)

## TiKV {#tikv}

-   [スナップショットが適用されるときに発生する可能性のあるパフォーマンスの問題を修正します](https://github.com/pingcap/tikv/pull/2559)
-   [大量のデータを削除した後のリバーススキャンのパフォーマンスの問題を修正します](https://github.com/pingcap/tikv/pull/2559)
-   [特別な状況下でのDecimalタイプの誤ったエンコード結果を修正](https://github.com/pingcap/tikv/pull/2571)

1.0.3から1.0.4にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレード順序に従います。

---
title: TiDB 1.0.4 Release Notes
---

# TiDB 1.0.4 リリースノート {#tidb-1-0-4-release-notes}

2017 年 12 月 11 日に、TiDB 1.0.4 がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [`tidb-server`起動時の統計の読み込みを高速化](https://github.com/pingcap/tidb/pull/5362)
-   [`show variables`ステートメントのパフォーマンスを改善する](https://github.com/pingcap/tidb/pull/5363)
-   [`Add Index`ステートメントを使用して結合されたインデックスを処理する際の潜在的な問題を修正します。](https://github.com/pingcap/tidb/pull/5323)
-   [`Rename Table`ステートメントを使用してテーブルを別のデータベースに移動する際の潜在的な問題を修正します](https://github.com/pingcap/tidb/pull/5314)
-   [`Alter/Drop User`ステートメントの効果を加速](https://github.com/pingcap/tidb/pull/5226)

## TiKV {#tikv}

-   [スナップショットの適用時に発生する可能性があるパフォーマンスの問題を修正](https://github.com/pingcap/tikv/pull/2559)
-   [大量のデータを削除した後の逆スキャンのパフォーマンスの問題を修正](https://github.com/pingcap/tikv/pull/2559)
-   [特殊な状況下での Decimal 型の間違ったエンコード結果を修正](https://github.com/pingcap/tikv/pull/2571)

1.0.3 から 1.0.4 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従ってください。

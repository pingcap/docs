---
title: TiDB 1.0.4 Release Notes
summary: TiDB 1.0.4 は 2017 年 12 月 11 日にリリースされました。更新には、速度の向上、パフォーマンスの強化、および TiDB と TiKV の潜在的な問題の修正が含まれています。1.0.3 から 1.0.4 にアップグレードするには、PD、TiKV、および TiDB のローリング アップグレードの順序に従ってください。
---

# TiDB 1.0.4 リリースノート {#tidb-1-0-4-release-notes}

2017 年 12 月 11 日に、次の更新を含む TiDB 1.0.4 がリリースされました。

## ティビ {#tidb}

-   [`tidb-server`起動時に統計情報の読み込みを高速化します](https://github.com/pingcap/tidb/pull/5362)
-   [`show variables`ステートメントのパフォーマンスを向上する](https://github.com/pingcap/tidb/pull/5363)
-   [結合されたインデックスを処理するために`Add Index`ステートメントを使用するときに発生する可能性のある問題を修正しました。](https://github.com/pingcap/tidb/pull/5323)
-   [`Rename Table`ステートメントを使用してテーブルを別のデータベースに移動するときに発生する可能性のある問題を修正しました。](https://github.com/pingcap/tidb/pull/5314)
-   [`Alter/Drop User`ステートメントの有効性を加速する](https://github.com/pingcap/tidb/pull/5226)

## ティクヴ {#tikv}

-   [スナップショットを適用したときに発生する可能性のあるパフォーマンスの問題を修正](https://github.com/pingcap/tikv/pull/2559)
-   [大量のデータを削除した後のリバーススキャンのパフォーマンスの問題を修正](https://github.com/pingcap/tikv/pull/2559)
-   [特殊な状況下での Decimal 型の誤ったエンコード結果を修正](https://github.com/pingcap/tikv/pull/2571)

1.0.3 から 1.0.4 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレード順序に従います。

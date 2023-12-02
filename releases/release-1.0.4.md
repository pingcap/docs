---
title: TiDB 1.0.4 Release Notes
---

# TiDB 1.0.4 リリースノート {#tidb-1-0-4-release-notes}

2017 年 12 月 11 日に、次の更新を含む TiDB 1.0.4 がリリースされました。

## TiDB {#tidb}

-   [`tidb-server`の起動時の統計のロードを高速化します。](https://github.com/pingcap/tidb/pull/5362)
-   [`show variables`ステートメントのパフォーマンスを向上させる](https://github.com/pingcap/tidb/pull/5363)
-   [`Add Index`ステートメントを使用して結合インデックスを処理する場合の潜在的な問題を修正](https://github.com/pingcap/tidb/pull/5323)
-   [`Rename Table`ステートメントを使用してテーブルを別のデータベースに移動する場合の潜在的な問題を修正](https://github.com/pingcap/tidb/pull/5314)
-   [`Alter/Drop User`ステートメントの有効性を加速する](https://github.com/pingcap/tidb/pull/5226)

## TiKV {#tikv}

-   [スナップショットが適用されるときに発生する可能性のあるパフォーマンスの問題を修正します。](https://github.com/pingcap/tikv/pull/2559)
-   [大量のデータを削除した後の逆スキャンのパフォーマンスの問題を修正](https://github.com/pingcap/tikv/pull/2559)
-   [特殊な状況下で Decimal 型の間違ったエンコード結果を修正しました。](https://github.com/pingcap/tikv/pull/2571)

1.0.3 から 1.0.4 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。

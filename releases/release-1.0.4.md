---
title: TiDB 1.0.4 Release Notes
---

# TiDB 1.0.4 リリースノート {#tidb-1-0-4-release-notes}

2017 年 12 月 11 日に、次の更新を含む TiDB 1.0.4 がリリースされました。

## TiDB {#tidb}

-   [<a href="https://github.com/pingcap/tidb/pull/5362">`tidb-server`の起動時の統計のロードを高速化します。</a>](https://github.com/pingcap/tidb/pull/5362)
-   [<a href="https://github.com/pingcap/tidb/pull/5363">`show variables`ステートメントのパフォーマンスを向上させる</a>](https://github.com/pingcap/tidb/pull/5363)
-   [<a href="https://github.com/pingcap/tidb/pull/5323">`Add Index`ステートメントを使用して結合インデックスを処理する場合の潜在的な問題を修正</a>](https://github.com/pingcap/tidb/pull/5323)
-   [<a href="https://github.com/pingcap/tidb/pull/5314">`Rename Table`ステートメントを使用してテーブルを別のデータベースに移動する場合の潜在的な問題を修正</a>](https://github.com/pingcap/tidb/pull/5314)
-   [<a href="https://github.com/pingcap/tidb/pull/5226">`Alter/Drop User`ステートメントの有効性を加速する</a>](https://github.com/pingcap/tidb/pull/5226)

## TiKV {#tikv}

-   [<a href="https://github.com/pingcap/tikv/pull/2559">スナップショットが適用されるときに発生する可能性のあるパフォーマンスの問題を修正します。</a>](https://github.com/pingcap/tikv/pull/2559)
-   [<a href="https://github.com/pingcap/tikv/pull/2559">大量のデータを削除した後の逆スキャンのパフォーマンスの問題を修正</a>](https://github.com/pingcap/tikv/pull/2559)
-   [<a href="https://github.com/pingcap/tikv/pull/2571">特殊な状況下で Decimal 型の間違ったエンコード結果を修正しました。</a>](https://github.com/pingcap/tikv/pull/2571)

1.0.3 から 1.0.4 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。

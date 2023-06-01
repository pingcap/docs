---
title: TiDB 1.0.8 Release Notes
---

# TiDB 1.0.8 リリースノート {#tidb-1-0-8-release-notes}

2018 年 2 月 11 日に、次の更新を含む TiDB 1.0.8 がリリースされました。

## TiDB {#tidb}

-   [<a href="https://github.com/pingcap/tidb/pull/5712">一部のシナリオにおける`Outer Join`結果の問題を修正</a>](https://github.com/pingcap/tidb/pull/5712)
-   [<a href="https://github.com/pingcap/tidb/pull/5738">`InsertIntoIgnore`ステートメントのパフォーマンスを最適化します。</a>](https://github.com/pingcap/tidb/pull/5738)
-   [<a href="https://github.com/pingcap/tidb/pull/5751">`ShardRowID`オプションの問題を修正する</a>](https://github.com/pingcap/tidb/pull/5751)
-   [<a href="https://github.com/pingcap/tidb/pull/5754">トランザクション内の DML ステートメントの数に制限 (構成可能、デフォルト値は 5000) を追加します。</a>](https://github.com/pingcap/tidb/pull/5754)
-   [<a href="https://github.com/pingcap/tidb/pull/5776">`Prepare`ステートメントによって返されるテーブル/カラムのエイリアスの問題を修正</a>](https://github.com/pingcap/tidb/pull/5776)
-   [<a href="https://github.com/pingcap/tidb/pull/5787">統計デルタの更新の問題を修正</a>](https://github.com/pingcap/tidb/pull/5787)
-   [<a href="https://github.com/pingcap/tidb/pull/5805">`Drop Column`ステートメントのpanicエラーを修正</a>](https://github.com/pingcap/tidb/pull/5805)
-   [<a href="https://github.com/pingcap/tidb/pull/5818">`Add Column After`ステートメントを実行するときの DML の問題を修正する</a>](https://github.com/pingcap/tidb/pull/5818)
-   [<a href="https://github.com/pingcap/tidb/pull/5815">GC エラーのある領域を無視することで、GC プロセスの安定性を向上させます。</a>](https://github.com/pingcap/tidb/pull/5815)
-   [<a href="https://github.com/pingcap/tidb/pull/5850">GC を同時に実行して GC プロセスを高速化します</a>](https://github.com/pingcap/tidb/pull/5850)
-   [<a href="https://github.com/pingcap/tidb/pull/5853">`CREATE INDEX`ステートメントの構文サポートを提供します。</a>](https://github.com/pingcap/tidb/pull/5853)

## PD {#pd}

-   [<a href="https://github.com/pingcap/pd/pull/932">リージョンハートビートのロックオーバーヒートを軽減します。</a>](https://github.com/pingcap/pd/pull/932)
-   [<a href="https://github.com/pingcap/pd/pull/939">ホット リージョン スケジューラが間違ったLeaderを選択する問題を修正</a>](https://github.com/pingcap/pd/pull/939)

## TiKV {#tikv}

-   [<a href="https://github.com/pingcap/tikv/pull/2740">`DeleteFilesInRanges`を使用して古いデータをクリアし、TiKV の起動速度を向上させます</a>](https://github.com/pingcap/tikv/pull/2740)
-   [<a href="https://github.com/pingcap/tikv/pull/2754">コプロセッサーの合計で`Decimal`数を使用する</a>](https://github.com/pingcap/tikv/pull/2754)
-   [<a href="https://github.com/pingcap/tikv/pull/2758">受信したスナップショットのメタデータを強制的に同期し、安全性を確保します</a>](https://github.com/pingcap/tikv/pull/2758)

1.0.7 から 1.0.8 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。

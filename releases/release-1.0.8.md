---
title: TiDB 1.0.8 Release Notes
summary: TiDB 1.0.8 は、さまざまな問題の修正、パフォーマンスの最適化、安定性の向上などのアップデートとともにリリースされました。PD と TiKV にも、ロックの過熱の軽減、リーダー選択の問題の修正、起動速度の向上に関連するアップデートがあります。アップグレードするには、PD -> TiKV -> TiDB の順序に従ってください。
---

# TiDB 1.0.8 リリースノート {#tidb-1-0-8-release-notes}

2018 年 2 月 11 日に、次の更新を含む TiDB 1.0.8 がリリースされました。

## ティビ {#tidb}

-   [いくつかのシナリオにおける`Outer Join`結果の問題を修正](https://github.com/pingcap/tidb/pull/5712)
-   [`InsertIntoIgnore`ステートメントのパフォーマンスを最適化します](https://github.com/pingcap/tidb/pull/5738)
-   [`ShardRowID`オプションの問題を修正](https://github.com/pingcap/tidb/pull/5751)
-   [トランザクション内のDMLステートメント数に制限（設定可能、デフォルト値は5000）を追加します。](https://github.com/pingcap/tidb/pull/5754)
-   [`Prepare`ステートメントによって返されるテーブル/カラムのエイリアスの問題を修正しました。](https://github.com/pingcap/tidb/pull/5776)
-   [統計デルタの更新に関する問題を修正](https://github.com/pingcap/tidb/pull/5787)
-   [`Drop Column`ステートメントのpanicエラーを修正](https://github.com/pingcap/tidb/pull/5805)
-   [`Add Column After`ステートメントを実行する際の DML の問題を修正しました。](https://github.com/pingcap/tidb/pull/5818)
-   [GCエラーのある領域を無視することでGCプロセスの安定性を向上](https://github.com/pingcap/tidb/pull/5815)
-   [GCを並行して実行してGCプロセスを高速化する](https://github.com/pingcap/tidb/pull/5850)
-   [`CREATE INDEX`ステートメントの構文サポートを提供する](https://github.com/pingcap/tidb/pull/5853)

## PD {#pd}

-   [リージョンハートビートのロックオーバーヒートを軽減](https://github.com/pingcap/pd/pull/932)
-   [ホットリージョンスケジューラが間違ったLeaderを選択する問題を修正](https://github.com/pingcap/pd/pull/939)

## ティクヴ {#tikv}

-   [`DeleteFilesInRanges`を使用して古いデータを消去し、TiKV の起動速度を向上させます。](https://github.com/pingcap/tikv/pull/2740)
-   [コプロセッサーの合計で`Decimal`を使用する](https://github.com/pingcap/tikv/pull/2754)
-   [受信したスナップショットのメタデータを強制的に同期して安全性を確保します](https://github.com/pingcap/tikv/pull/2758)

1.0.7 から 1.0.8 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。

---
title: TiDB 1.0.8 Release Notes
---

# TiDB1.0.8リリースノート {#tidb-1-0-8-release-notes}

2018年2月11日に、TiDB 1.0.8がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [一部のシナリオでの`Outer Join`結果の問題を修正](https://github.com/pingcap/tidb/pull/5712)
-   [`InsertIntoIgnore`ステートメントのパフォーマンスを最適化する](https://github.com/pingcap/tidb/pull/5738)
-   [`ShardRowID`オプションの問題を修正します](https://github.com/pingcap/tidb/pull/5751)
-   [トランザクション内のDMLステートメント番号に制限（構成可能、デフォルト値は5000）を追加します](https://github.com/pingcap/tidb/pull/5754)
-   [`Prepare`ステートメントによって返されるテーブル/カラムエイリアスの問題を修正します](https://github.com/pingcap/tidb/pull/5776)
-   [統計デルタの更新に関する問題を修正します](https://github.com/pingcap/tidb/pull/5787)
-   [`Drop Column`ステートメントのpanicエラーを修正します](https://github.com/pingcap/tidb/pull/5805)
-   [`Add Column After`ステートメントを実行する際のDMLの問題を修正します](https://github.com/pingcap/tidb/pull/5818)
-   [GCエラーのある領域を無視することにより、GCプロセスの安定性を向上させます](https://github.com/pingcap/tidb/pull/5815)
-   [GCを同時に実行して、GCプロセスを加速します](https://github.com/pingcap/tidb/pull/5850)
-   [`CREATE INDEX`ステートメントの構文サポートを提供します](https://github.com/pingcap/tidb/pull/5853)

## PD {#pd}

-   [リージョンハートビートのロック過熱を減らします](https://github.com/pingcap/pd/pull/932)
-   [ホットリージョンスケジューラが間違ったリーダーを選択する問題を修正します](https://github.com/pingcap/pd/pull/939)

## TiKV {#tikv}

-   [`DeleteFilesInRanges`を使用して、古いデータをクリアし、TiKVの開始速度を向上させます](https://github.com/pingcap/tikv/pull/2740)
-   [コプロセッサーの合計で`Decimal`を使用する](https://github.com/pingcap/tikv/pull/2754)
-   [受信したスナップショットのメタデータを強制的に同期して、安全性を確保します](https://github.com/pingcap/tikv/pull/2758)

1.0.7から1.0.8にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレードの順序に従います。

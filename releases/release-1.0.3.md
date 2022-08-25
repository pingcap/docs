---
title: TiDB 1.0.3 Release Notes
---

# TiDB 1.0.3 リリースノート {#tidb-1-0-3-release-notes}

2017 年 11 月 28 日に、TiDB 1.0.3 がリリースされ、次の更新が行われました。

## TiDB {#tidb}

-   [トランザクション競合シナリオでのパフォーマンスを最適化する](https://github.com/pingcap/tidb/pull/5051)
-   [構成ファイルに`TokenLimit`オプションを追加します](https://github.com/pingcap/tidb/pull/5107)
-   [デフォルト データベースをスロー クエリ ログに出力する](https://github.com/pingcap/tidb/pull/5107)
-   [クエリ期間メトリックから DDL ステートメントを削除する](https://github.com/pingcap/tidb/pull/5107)
-   [クエリ コストの見積もりを最適化する](https://github.com/pingcap/tidb/pull/5140)
-   [テーブル作成時のインデックス接頭辞の問題を修正](https://github.com/pingcap/tidb/pull/5149)
-   [Float 型の式の TiKV へのプッシュ ダウンをサポート](https://github.com/pingcap/tidb/pull/5153)
-   [離散整数プライマリ インデックスを持つテーブルのインデックスを追加するのが遅いという問題を修正します。](https://github.com/pingcap/tidb/pull/5155)
-   [不要な統計更新を減らす](https://github.com/pingcap/tidb/pull/5164)
-   [トランザクションの再試行中の潜在的な問題を修正します](https://github.com/pingcap/tidb/pull/5219)

## PD {#pd}

-   API を使用してより多くのタイプのスケジューラを追加することをサポート

## TiKV {#tikv}

-   PD クライアントのデッドロックの問題を修正
-   間違った引出線の値が`NotLeader`と表示される問題を修正
-   コプロセッサーでチャンクサイズが大きすぎる問題を修正

1.0.2 から 1.0.3 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従ってください。

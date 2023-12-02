---
title: TiDB 1.0.3 Release Notes
---

# TiDB 1.0.3 リリースノート {#tidb-1-0-3-release-notes}

2017 年 11 月 28 日に、次の更新を含む TiDB 1.0.3 がリリースされました。

## TiDB {#tidb}

-   [トランザクション競合シナリオのパフォーマンスを最適化する](https://github.com/pingcap/tidb/pull/5051)
-   [構成ファイルに`TokenLimit`オプションを追加します。](https://github.com/pingcap/tidb/pull/5107)
-   [デフォルトのデータベースをスロークエリログに出力します。](https://github.com/pingcap/tidb/pull/5107)
-   [クエリ期間メトリクスから DDL ステートメントを削除する](https://github.com/pingcap/tidb/pull/5107)
-   [クエリのコスト見積もりを最適化する](https://github.com/pingcap/tidb/pull/5140)
-   [テーブル作成時のインデックスプレフィックスの問題を修正](https://github.com/pingcap/tidb/pull/5149)
-   [Float 型の式を TiKV にプッシュダウンするサポート](https://github.com/pingcap/tidb/pull/5153)
-   [離散整数のプライマリ インデックスを持つテーブルのインデックスの追加が遅いという問題を修正](https://github.com/pingcap/tidb/pull/5155)
-   [不必要な統計更新を削減する](https://github.com/pingcap/tidb/pull/5164)
-   [トランザクションの再試行中の潜在的な問題を修正する](https://github.com/pingcap/tidb/pull/5219)

## PD {#pd}

-   APIを使用してより多くの種類のスケジューラの追加をサポート

## TiKV {#tikv}

-   PDクライアントのデッドロック問題を修正
-   間違ったリーダー値`NotLeader`が表示される問題を修正
-   コプロセッサのチャンクサイズが大きすぎる問題を修正

1.0.2 から 1.0.3 にアップグレードするには、PD -&gt; TiKV -&gt; TiDB のローリング アップグレードの順序に従います。

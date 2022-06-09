---
title: TiDB 1.0.3 Release Notes
---

# TiDB1.0.3リリースノート {#tidb-1-0-3-release-notes}

2017年11月28日に、TiDB1.0.3が次のアップデートでリリースされます。

## TiDB {#tidb}

-   [トランザクション競合シナリオでのパフォーマンスを最適化する](https://github.com/pingcap/tidb/pull/5051)
-   [構成ファイルに`TokenLimit`オプションを追加します](https://github.com/pingcap/tidb/pull/5107)
-   [遅いクエリログにデフォルトのデータベースを出力する](https://github.com/pingcap/tidb/pull/5107)
-   [クエリ期間メトリックからDDLステートメントを削除します](https://github.com/pingcap/tidb/pull/5107)
-   [クエリコストの見積もりを最適化する](https://github.com/pingcap/tidb/pull/5140)
-   [テーブル作成時のインデックスプレフィックスの問題を修正](https://github.com/pingcap/tidb/pull/5149)
-   [Floatタイプの式をTiKVにプッシュダウンすることをサポート](https://github.com/pingcap/tidb/pull/5153)
-   [離散整数プライマリインデックスを持つテーブルのインデックスを追加するのが遅いという問題を修正します](https://github.com/pingcap/tidb/pull/5155)
-   [不要な統計の更新を減らす](https://github.com/pingcap/tidb/pull/5164)
-   [トランザクションの再試行中に発生する可能性のある問題を修正する](https://github.com/pingcap/tidb/pull/5219)

## PD {#pd}

-   APIを使用したスケジューラーのタイプの追加をサポート

## TiKV {#tikv}

-   PDクライアントのデッドロックの問題を修正します
-   間違ったリーダー値が`NotLeader`に対して要求される問題を修正します
-   コプロセッサーでチャンク・サイズが大きすぎるという問題を修正します

1.0.2から1.0.3にアップグレードするには、PD-&gt;TiKV-&gt;TiDBのローリングアップグレードの順序に従います。

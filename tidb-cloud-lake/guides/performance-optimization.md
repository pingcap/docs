---
title: パフォーマンス最適化
summary: "{{{ .lake }}} は、データクラスタリング、結果キャッシュ、専用インデックスなどの**さまざまなインデックス技術**を通じて、主にクエリパフォーマンスを高速化し、クエリ応答時間を大幅に改善します。"
---

# パフォーマンス最適化

{{{ .lake }}} は、データクラスタリング、結果キャッシュ、専用インデックスなどの**さまざまなインデックス技術**を通じて、主にクエリパフォーマンスを高速化し、クエリ応答時間を大幅に改善します。

## 最適化機能 {#optimization-features}

| 機能 | 目的 | 使用するタイミング |
|---------|---------|------------|
| [**Cluster Key**](/tidb-cloud-lake/sql/cluster-key.md) | 最適なクエリパフォーマンスのためにデータを物理的に自動整理する | 特定のカラムで頻繁にフィルタリングする大規模テーブルがある場合。特に時系列データやカテゴリデータに適しています |
| [**Table Partitioning**](/tidb-cloud-lake/guides/partition-by.md) | データを物理的に分離し、スキャン前にパーティションをプルーニングする | 大規模テーブルが時間、テナント、リージョン、またはバケット化された高カーディナリティキーで一般的にフィルタリングされる場合 |
| [**Query Result Cache**](/tidb-cloud-lake/guides/query-result-cache.md) | 同一クエリの結果を自動的に保存して再利用する | ダッシュボードや定期レポートなどで、アプリケーションが同じ分析クエリを繰り返し実行する場合 |
| [**Virtual Column**](/tidb-cloud-lake/guides/virtual-column.md) | JSON/VARIANT データ内のフィールドへのアクセスを自動的に高速化する | 半構造化データ内の特定パスを頻繁にクエリし、サブ秒の応答時間が必要な場合 |
| [**Aggregating Index**](/tidb-cloud-lake/guides/aggregating-index.md) | 一般的な集計結果を事前計算して保存する | 分析ワークロードで大規模データセットに対する SUM、COUNT、AVG クエリを頻繁に実行する場合 |
| [**Full-Text Index**](/tidb-cloud-lake/guides/full-text-index.md) | 非常に高速なセマンティックテキスト検索機能を有効にする | 関連度スコアリングやあいまい一致などの高度なテキスト検索機能が必要な場合 |
| [**Ngram Index**](/tidb-cloud-lake/guides/ngram-index.md) | ワイルドカードを使ったパターンマッチングを高速化する | 大規模なテキストカラムに対して、クエリでワイルドカード付きの LIKE 演算子（特に '%keyword%'）を使用する場合 |
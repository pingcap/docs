---
title: 集計インデックス
summary: 集計インデックスは、集計結果を事前計算して保存することで分析クエリを大幅に高速化し、一般的な分析処理のためにテーブル全体をスキャンする必要をなくします。
---

# 集計インデックス

集計インデックスは、集計結果を事前計算して保存することで分析クエリを大幅に高速化し、一般的な分析処理のためにテーブル全体をスキャンする必要をなくします。

## どのような問題を解決するのか {#what-problem-does-it-solve}

大規模データセットに対する分析クエリでは、パフォーマンス上の大きな課題があります。

| 問題 | 影響 | 集計インデックスによる解決策 |
|---------|--------|---------------------------|
| **フルテーブルスキャン** | SUM、COUNT、MIN、MAX クエリで数百万行をスキャンする | 事前計算済みの結果を即座に読み取る |
| **繰り返し計算** | 同じ集計を何度も計算する | 結果を一度保存し、何度も再利用する |
| **ダッシュボードクエリの低速化** | 分析ダッシュボードのロードに数分かかる | 一般的なメトリクスに対してサブ秒で応答する |
| **高い計算コスト** | 重い集計ワークロードがリソースを消費する | キャッシュ済み結果に対する計算を最小限に抑える |
| **ユーザー体験の低下** | ユーザーがレポートや分析結果を待たされる | ビジネスインテリジェンス向けに即時結果を返す |

**例**: 100M 行に対する売上分析クエリ `SELECT SUM(revenue), COUNT(*) FROM sales WHERE region = 'US'`。集計インデックスがない場合、US のすべての売上レコードをスキャンします。集計インデックスがある場合、事前計算済みの結果を即座に返します。

## 仕組み {#how-it-works}

1. **インデックス作成** → 事前計算する集計クエリを定義する
2. **結果の保存** → {{{ .lake }}} が集計結果を最適化されたブロックに保存する
3. **クエリマッチング** → 受信したクエリが自動的に事前計算済みの結果を使用する
4. **自動更新** → 基になるデータが変更されると結果が更新される

## クイックセットアップ {#quick-setup}

```sql
-- Create table with sample data
CREATE TABLE sales(region VARCHAR, product VARCHAR, revenue DECIMAL, quantity INT);

-- Create aggregating index for common analytics
CREATE AGGREGATING INDEX sales_summary AS
SELECT region, SUM(revenue), COUNT(*), AVG(quantity)
FROM sales
GROUP BY region;

-- Refresh the index (manual mode)
REFRESH AGGREGATING INDEX sales_summary;

-- Verify the index is used
EXPLAIN SELECT region, SUM(revenue) FROM sales GROUP BY region;
```

## サポートされる操作 {#supported-operations}

| ✅ サポート対象 | ❌ 非サポート |
|-------------|-----------------|
| SUM, COUNT, MIN, MAX, AVG | ウィンドウ関数 |
| GROUP BY 句 | GROUPING SETS |
| WHERE フィルター | ORDER BY, LIMIT |
| 単純な集計 | 複雑なサブクエリ |

## 更新戦略 {#refresh-strategies}

| 戦略 | 使用する場面 | 設定 |
|----------|-------------|---------------|
| **Automatic (SYNC)** | リアルタイム分析、小規模データセット | `CREATE AGGREGATING INDEX ... SYNC` |
| **Manual** | 大規模データセット、バッチ処理 | `CREATE AGGREGATING INDEX ...`（デフォルト） |
| **Background (Cloud)** | 本番ワークロード | {{{ .lake }}} で自動 |

### 自動更新と手動更新の比較 {#automatic-vs-manual-refresh}

```sql
-- Automatic refresh (updates with every data change)
CREATE AGGREGATING INDEX auto_summary AS
SELECT region, SUM(revenue) FROM sales GROUP BY region SYNC;

-- Manual refresh (update on demand)
CREATE AGGREGATING INDEX manual_summary AS
SELECT region, SUM(revenue) FROM sales GROUP BY region;

REFRESH AGGREGATING INDEX manual_summary;
```

## パフォーマンス例 {#performance-example}

この例は、パフォーマンスが大幅に向上することを示しています。

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;

-- Refresh the aggregating index
REFRESH AGGREGATING INDEX my_agg_index;

-- Verify if the aggregating index works
EXPLAIN SELECT MIN(a), MAX(c) FROM agg;

-- Key indicators in the execution plan:
-- ├── aggregating index: [SELECT MIN(a), MAX(c) FROM default.agg]
-- ├── rewritten query: [selection: [index_col_0 (#0), index_col_1 (#1)]]
-- This shows the query uses precomputed results instead of scanning raw data
```

## ベストプラクティス {#best-practices}

| プラクティス | 利点 |
|----------|---------|
| **一般的なクエリにインデックスを作成する** | 頻繁に実行される分析に集中できる |
| **手動更新を使用する** | 更新タイミングをより適切に制御できる |
| **インデックス使用状況を監視する** | EXPLAIN を使用してインデックス利用を確認できる |
| **未使用のインデックスをクリーンアップする** | 使用されていないインデックスを削除できる |
| **クエリパターンを一致させる** | インデックスのフィルターを実際のクエリに合わせられる |

## 管理コマンド {#management-commands}

| コマンド | 目的 |
|---------|---------|
| `CREATE AGGREGATING INDEX` | 新しい集計インデックスを作成する |
| `REFRESH AGGREGATING INDEX` | 最新データでインデックスを更新する |
| `DROP AGGREGATING INDEX` | インデックスを削除する（ストレージをクリーンアップするには VACUUM TABLE を使用） |
| `SHOW AGGREGATING INDEXES` | すべてのインデックスを一覧表示する |

## 重要な注意事項 {#important-notes}

**集計インデックスを使用すべき場面:**

- 頻繁な分析クエリ（ダッシュボード、レポート）
- 繰り返し集計を行う大規模データセット
- 安定したクエリパターン
- パフォーマンスが重要なアプリケーション

**使用すべきでない場面:**

- 頻繁に変更されるデータ
- 一度きりの分析クエリ
- 小さなテーブルに対する単純なクエリ

## 設定 {#configuration}

```sql
-- Enable/disable aggregating index feature
SET enable_aggregating_index_scan = 1;  -- Enable (default)
SET enable_aggregating_index_scan = 0;  -- Disable
```

---

*集計インデックスは、大規模データセットに対する反復的な分析ワークロードで最も効果を発揮します。まずは、最も一般的なダッシュボードおよびレポート用クエリから始めてください。*
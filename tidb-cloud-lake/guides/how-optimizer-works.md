---
title: TiDB Cloud Lake オプティマイザの仕組み
summary: "{{{ .lake }}} のクエリオプティマイザは、SQL テキストを実行可能なプランへ変換する一連の変換を統括します。オプティマイザはクエリの抽象表現を構築し、リアルタイム統計で補強し、ルールベースの書き換えを適用し、結合の代替案を探索し、最後に最もコストの低い物理演算子を選択します。"
---

# TiDB Cloud Lake オプティマイザの仕組み

{{{ .lake }}} のクエリオプティマイザは、SQL テキストを実行可能なプランへ変換する一連の変換を統括します。オプティマイザはクエリの抽象表現を構築し、リアルタイム統計で補強し、ルールベースの書き換えを適用し、結合の代替案を探索し、最後に最もコストの低い物理演算子を選択します。

同じオプティマイザパイプラインが、分析レポート、JSON 検索、ベクトル検索、地理空間検索を支えています。**{{{ .lake }}} は、保存するあらゆるデータ型を理解する単一のオプティマイザを管理します。**

## {{{ .lake }}} オプティマイザの特長 {#what-makes--lake-s-optimizer-tick}

- 統計情報は自動的に最新の状態に保たれます。データが書き込まれると、{{{ .lake }}} は行数、値の範囲、NDV を即座に管理するため、オプティマイザは選択率、結合順序、コスト計算に新しい情報を手動メンテナンスなしで利用できます。
- まずプランの形を整え、次にコストで選ぶ: パイプラインは、グローバル探索の前に相関を除去し、述語や limit をプッシュダウンし、集計を分割します。これにより探索空間を縮小し、処理をストレージ側へ移動します。
- DP + Cascades を併用: DPhpy が適切な結合順序を見つけ、memo ベースの Cascades パスが同じ SExpr memo 上で最もコストの低い物理演算子を選択します。
- 分散を考慮した設計: プランニングではローカル実行か分散実行かを決定し、ホットスポットを避けるためにブロードキャストをキーベースのシャッフルに書き換えます。

## クエリ例 {#example-query}

以下の分析クエリを使い、各ステージでどのように変換されるかを示します。

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
)
SELECT c.region,
       COUNT(*) AS order_count,
       COUNT(o.id) AS row_count,
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
FROM recent_orders o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
WHERE c.status = 'ACTIVE'
  AND o.total_amount > 0
  AND p.is_active = TRUE
  AND EXISTS (
        SELECT 1
        FROM support_tickets t
        WHERE t.customer_id = c.id
          AND t.created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
      )
GROUP BY c.region
HAVING COUNT(*) > 100
ORDER BY order_count DESC
LIMIT 10;
```

## フェーズ 1: 準備と統計情報 {#phase-1-prep--stats}

フェーズ 1 では、クエリを理解しやすい形に整え、コスト計算に必要なデータを付与します。この例では、オプティマイザは次の具体的な手順を実行します。

### 1. サブクエリをフラット化する {#1-flatten-the-subquery}

`EXISTS (...)` チェックを通常の結合に変換し、パイプラインの残りの部分が単一の結合ツリーとして扱えるようにします。

```
# Before (correlated)
customers ─┐
           ├─ JOIN ─ orders
support ───┘        │
                    └─ EXISTS (references customers)

# After (semi-join)
customers ─┐
support ───┴─ SEMI JOIN ─ orders
```

等価な SQL（意味は保持されます）:

```sql
FROM (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
) o
JOIN customers c ON o.customer_id = c.id
LEFT JOIN products p ON o.product_id = p.id
JOIN (
  SELECT DISTINCT customer_id
  FROM support_tickets
  WHERE created_at > DATE_TRUNC('month', today()) - INTERVAL '1' MONTH
) t ON t.customer_id = c.id
```

### 2. メタデータのショートカットを確認する {#2-check-metadata-shortcuts}

`MIN(o.total_amount)` のような集計にフィルタがない場合、オプティマイザはスキャンの代わりにテーブル統計からその値を取得します。

```
-- フィルタが適用されない場合の概念的な置き換え
SELECT MIN(total_amount)
FROM orders

# becomes

SELECT table_stats.min_total_amount
```

このクエリではフィルタが適用されるため、実際の計算を維持します。

### 3. 統計情報を付与する {#3-attach-statistics}

プランニング中に、{{{ .lake }}} はスキャン対象テーブルの行数、値の範囲、異なる値の数を収集します。SQL を変更する必要はなく、その後の選択率とコストの推定は、`ANALYZE` ジョブを実行しなくても正確に保たれます。

### 4. 集計を正規化する {#4-normalize-aggregates}

統計情報を付与した後、オプティマイザは共有できるカウンタを書き換えます。`COUNT(o.id)` は `COUNT(*)` に変換されるため、エンジンは両方の用途に対して単一のカウンタを管理します。変更されるのは SELECT リストだけです。

```sql
SELECT c.region,
       COUNT(*)            AS order_count,
       COUNT(*)            AS row_count,      -- was COUNT(o.id)
       COUNT(DISTINCT o.product_id) AS product_count,
       MIN(o.total_amount) AS min_amount,
       AVG(o.total_amount) AS avg_amount
...
```

## フェーズ 2: ロジックを洗練する {#phase-2-refine-the-logic}

フェーズ 2 では、実際に必要な処理だけを残すための対象を絞った書き換えを実行します。

### 1. フィルタと limit をプッシュダウンする {#1-push-filterslimits-down}

```
# Before
Filter (o.total_amount > 0)
└─ Scan (recent_orders)

# After
Scan (recent_orders, pushdown_predicates=[total_amount > 0])
```

limit を伴うソートも、より引き締められます。

```
# Before
Limit (10)
└─ Sort (order_count DESC)
   └─ Join (...)

# After
Sort (order_count DESC)
└─ Limit (10)
   └─ Join (...)
```

### 2. 冗長な処理を削除する {#2-drop-redundancies}

```
# Before
Filter (1 = 1 AND c.status = 'ACTIVE')
└─ ...

# After
Filter (c.status = 'ACTIVE')
└─ ...
```

### 3. 集計を分割する {#3-split-aggregates}

```
# Before
Aggregate (COUNT/AVG)
└─ Scan (recent_orders)

# After
Aggregate (final)
└─ Aggregate (partial)
   └─ Scan (recent_orders)
```

部分集計はデータの近くで実行され、その後 1 回の最終ステップで結果をマージします。

### 4. フィルタを CTE にプッシュダウンする {#4-push-filters-into-the-cte}

CTE のカラムだけを参照する述語は `recent_orders` の定義内にプッシュダウンされ、結合前にデータ量を削減します。

```sql
WITH recent_orders AS (
  SELECT *
  FROM orders
  WHERE order_date >= DATE_TRUNC('month', today()) - INTERVAL '3' MONTH
    AND fulfillment_status <> 'CANCELLED'
    AND total_amount > 0              -- pushed from outer query
)
```

## フェーズ 3: コストと物理プラン {#phase-3-cost--physical-plan}

論理プランが整理され、統計情報も最新になった段階で、オプティマイザは 3 つの判断を行います。

### 1. 結合順序を選択する {#1-choose-the-join-order}

統計情報に基づく動的計画法（`DPhpyOptimizer`）が、結合の順列を評価します。より小さくフィルタ済みのテーブル（`customers`、`products`、`support_tickets`）上にハッシュテーブルを構築し、大きなファクトテーブル（`recent_orders`）がそれらをプローブする構成を優先します。

```
    customers      products
           \      /
            HASH JOIN (build)
                 |
        recent_orders  (probe)
                 |
        SEMI JOIN support_tickets
```

### 2. 結合セマンティクスを厳密化する {#2-tighten-join-semantics}

ルールベースの処理により、上で見つかった結合が調整されます。

#### a. 安全な LEFT JOIN を INNER JOIN に変換する {#a-turn-safe-left-joins-into-inner-joins}

このクエリは `LEFT JOIN products p` で始まりますが、述語 `p.is_active = TRUE` により、一致する商品を持つ行だけが保持されることが保証されます。そのため、オプティマイザは結合の種類を切り替えます。

```
# Before
recent_orders ──⊗── products   (LEFT)
            filter: p.is_active = TRUE

# After
recent_orders ──⋈── products   (INNER)
```

#### b. 重複した述語を削除する {#b-drop-duplicate-predicates}

結合条件が重複している場合（たとえば `o.customer_id = c.id` が 2 回記載されている場合）、`DeduplicateJoinConditionOptimizer` は 1 つだけを残し、エグゼキューターが 1 回だけ評価するようにします。

#### c. 必要に応じて結合の左右を入れ替える {#c-optionally-swap-join-sides}

結合の並べ替えが引き続き有効な場合、`CommuteJoin` は結合の入力を反転できるため、オプティマイザは望ましいビルド/プローブの向きに合わせられます（たとえば、より小さいテーブルがハッシュテーブルを構築するようにしたり、分散戦略に一致させたりできます）。

```
# Before                     # After (smaller table builds)
customers ──⋈── recent_orders   recent_orders ──⋈── customers
```

### 3. 物理プランと分散方式を選択する {#3-pick-the-physical-plan-and-distribution}

`CascadesOptimizer` は、{{{ .lake }}} のコストモデルを使用して、ハッシュ結合、マージ結合、またはネステッドループ結合の実装から選択します。このパイプラインでは、プランをローカルのまま維持するかどうかも決定します。warehouse クラスターが利用可能で、結合の規模が大きい場合は、exchange の方式がブロードキャストからハッシュシャッフルに書き換えられ、処理が均等に分散されます。最後のクリーンアップでは、冗長な射影と未使用の CTE が削除されます。

## オブザーバビリティ {#observability}

- `EXPLAIN` は最終的に最適化されたプランを表示します。
- `EXPLAIN PIPELINE` は実行トポロジーを明らかにします。
- `SET enable_optimizer_trace = 1` は、すべてのオプティマイザのステップをクエリログに記録します。
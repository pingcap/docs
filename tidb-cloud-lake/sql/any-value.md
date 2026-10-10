---
title: ANY_VALUE
summary: 集約関数。
---

# ANY_VALUE

集約関数。

`ANY_VALUE()` 関数は、入力式から任意の非 NULL 値を返します。これは、グループ化も集約もされていないカラムを選択する必要がある `GROUP BY` クエリで使用されます。

> **Alias:** `ANY()` は `ANY_VALUE()` と同じ結果を返し、互換性のために引き続き利用できます。

## 構文 {#syntax}

```sql
ANY_VALUE(<expr>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|----------------|
| `<expr>`  | 任意の式 |

## 戻り値の型 {#return-type}

`<expr>` の型です。すべての値が NULL の場合、戻り値は NULL です。

> **Note:**
>
> - `ANY_VALUE()` は非決定的であり、実行ごとに異なる値を返す場合があります。
> - 予測可能な結果が必要な場合は、代わりに `MIN()` または `MAX()` を使用してください。

## 例 {#example}

**サンプルデータ:**

```sql
CREATE TABLE sales (
  region VARCHAR,
  manager VARCHAR,
  sales_amount DECIMAL(10, 2)
);

INSERT INTO sales VALUES
  ('North', 'Alice', 15000.00),
  ('North', 'Alice', 12000.00),
  ('South', 'Bob', 20000.00);
```

**問題:** このクエリは、`manager` が GROUP BY に含まれていないため失敗します。

```sql
SELECT region, manager, SUM(sales_amount)  -- ❌ Error
FROM sales GROUP BY region;
```

**従来の方法:** `manager` を GROUP BY に追加しますが、これにより必要以上にグループが増え、パフォーマンスが低下します。

```sql
SELECT region, manager, SUM(sales_amount)
FROM sales GROUP BY region, manager;  -- ❌ Poor performance due to extra grouping
```

**より良い解決策:** `ANY_VALUE()` を使用して manager を選択します。

```sql
SELECT
  region,
  ANY_VALUE(manager) AS manager,  -- ✅ Works
  SUM(sales_amount) AS total_sales
FROM sales
GROUP BY region;
```

**結果:**

```text
| region | manager | total_sales |
|--------|---------|-------------|
| North  | Alice   | 27000.00    |
| South  | Bob     | 20000.00    |
```
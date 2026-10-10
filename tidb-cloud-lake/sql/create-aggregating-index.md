---
title: CREATE AGGREGATING INDEX
summary: "{{{ .lake }}} で新しい集約インデックスを作成します。"
---

# CREATE AGGREGATING INDEX

{{{ .lake }}} で新しい集約インデックスを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] AGGREGATING INDEX <index_name> AS SELECT ...
```

- 集約インデックスを作成する際は、その用途を標準的な [Aggregate Functions](/tidb-cloud-lake/_index.md)（例: AVG、SUM、MIN、MAX、COUNT、および GROUP BY）に限定してください。GROUPING SETS、[Window Functions](/tidb-cloud-lake/_index.md)、[LIMIT](/tidb-cloud-lake/sql/select.md#limit-clause)、および [ORDER BY](/tidb-cloud-lake/sql/select.md#order-by-clause) は受け付けられず、使用すると次のエラーが返されます: `Currently create aggregating index just support simple query, like: SELECT ... FROM ... WHERE ... GROUP BY ...`.

- 集約インデックスの作成時に定義するクエリのフィルタ範囲は、実際のクエリの範囲と一致するか、それを包含している必要があります。

- 集約インデックスがクエリに対して有効に機能しているかを確認するには、[EXPLAIN](/tidb-cloud-lake/sql/explain.md) コマンドを使用してクエリを分析します。

## 例 {#examples}

この例では、クエリ "SELECT MIN(a), MAX(c) FROM agg" に対して、*my_agg_index* という名前の集約インデックスを作成します。

```sql
-- Prepare data
CREATE TABLE agg(a int, b int, c int);
INSERT INTO agg VALUES (1,1,4), (1,2,1), (1,2,4), (2,2,5);

-- Create an aggregating index
CREATE AGGREGATING INDEX my_agg_index AS SELECT MIN(a), MAX(c) FROM agg;
```
---
title: MIN_IF
summary: 接尾辞 `_IF` は任意の集約関数名の末尾に追加できます。この場合、集約関数は追加の引数である条件を受け取ります。
---

# MIN_IF

## MIN_IF {#min-if}

接尾辞 `_IF` は任意の集約関数名の末尾に追加できます。この場合、集約関数は追加の引数である条件を受け取ります。

```
MIN_IF(<column>, <cond>)
```

## 例 {#example}

**テーブルを作成してサンプルデータを挿入する**

```sql
CREATE TABLE project_budgets (
  id INT,
  project_id INT,
  department VARCHAR,
  budget FLOAT
);

INSERT INTO project_budgets (id, project_id, department, budget)
VALUES (1, 1, 'HR', 1000),
       (2, 1, 'IT', 2000),
       (3, 1, 'Marketing', 3000),
       (4, 2, 'HR', 1500),
       (5, 2, 'IT', 2500);
```

**クエリのデモ: IT 部門の最小予算を検索する**

```sql
SELECT MIN_IF(budget, department = 'IT') AS min_it_budget
FROM project_budgets;
```

**結果**

```sql
| min_it_budget |
|---------------|
|     2000      |
```
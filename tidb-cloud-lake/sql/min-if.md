---
title: MIN_IF
summary: 后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。
---

# MIN_IF

## MIN_IF {#min-if}

后缀 `_IF` 可以附加到任何聚合函数的名称后。在这种情况下，聚合函数会接受一个额外的参数——条件。

```
MIN_IF(<column>, <cond>)
```

## 示例 {#example}

**创建表并插入示例数据**

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

**查询示例：查找 IT 部门的最小预算**

```sql
SELECT MIN_IF(budget, department = 'IT') AS min_it_budget
FROM project_budgets;
```

**结果**

```sql
| min_it_budget |
|---------------|
|     2000      |
```
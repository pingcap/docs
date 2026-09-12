---
title: DROP ROW ACCESS POLICY
summary: "从 {{{ .lake }}} 中删除现有的行访问策略。在删除策略之前，请先将其从所有引用该策略的表中解绑。"
---

# DROP ROW ACCESS POLICY

从 {{{ .lake }}} 中删除现有的行访问策略。在删除策略之前，请先将其从所有引用该策略的表中解绑。

## 语法 {#syntax}

```sql
DROP ROW ACCESS POLICY [ IF EXISTS ] <policy_name>
```

## 访问控制要求 {#access-control-requirements}

| 权限 | 说明 |
|:----------|:------------|
| APPLY ROW ACCESS POLICY | 删除行访问策略所需的权限，除非你拥有该策略。 |

你必须具有全局 `APPLY ROW ACCESS POLICY` 权限，或者对目标策略具有 APPLY/OWNERSHIP。策略被删除后，{{{ .lake }}} 会自动从创建者角色回收 OWNERSHIP。

## 示例 {#examples}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN -> dept = 'Engineering';

CREATE TABLE employees(id INT, department STRING);
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

-- Detach the policy before dropping it.
ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;

DROP ROW ACCESS POLICY rap_engineering;
```
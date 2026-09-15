---
title: CREATE ROW ACCESS POLICY
summary: "在 {{{ .lake }}} 中创建新的行访问策略。行访问策略定义了一个布尔谓词，当该策略附加到表时，{{{ .lake }}} 会将其应用到行上。"
---

# CREATE ROW ACCESS POLICY

在 {{{ .lake }}} 中创建新的行访问策略。行访问策略定义了一个布尔谓词，当该策略附加到表时，{{{ .lake }}} 会将其应用到行上。

## 语法 {#syntax}

```sql
CREATE ROW ACCESS POLICY [ IF NOT EXISTS ] <policy_name> AS
    ( <arg_name> <arg_type> [ , <arg_name> <arg_type> ... ] )
    RETURNS BOOLEAN -> <predicate_expression>
    [ COMMENT = '<comment>' ]
```

| 参数 | 描述 |
|-----------|-------------|
| `policy_name` | 要创建的行访问策略名称。策略名称与 masking policies 共享同一个命名空间。 |
| `arg_name` | 在谓词表达式内部使用的策略参数名称。参数名称不需要与表列名匹配。 |
| `arg_type` | 参数的数据类型。附加策略时，列出的每个表列都必须与对应参数的类型匹配。 |
| `predicate_expression` | 用于决定某一行是否可见的布尔表达式。仅当该表达式计算结果为 `TRUE` 时，才会返回该行。 |
| `comment` | 可选注释，用于存储有关该策略的说明。 |

> **注意：**
>
> - 行访问策略当前仍处于实验阶段。可使用 `SET enable_experimental_row_access_policy = 1` 或 `SET GLOBAL enable_experimental_row_access_policy = 1` 启用。
> - 该策略必须返回 `BOOLEAN`。
> - `ALTER TABLE ... ADD ROW ACCESS POLICY ... ON (...)` 中列出的列会按位置绑定到策略参数。
> - 行访问策略定义中不支持子查询谓词。

## 访问控制要求 {#access-control-requirements}

| 权限 | 描述 |
|:----------|:------------|
| CREATE ROW ACCESS POLICY | 创建行访问策略所需的权限。通常授予在 `*.*` 上。 |

{{{ .lake }}} 会自动将新行访问策略的 OWNERSHIP 授予当前角色，以便其能够与其他对象一样管理该策略。

## 示例 {#examples}

以下示例创建了一个策略：仅暴露 `Engineering` 部门的行，除非当前角色为 `admin`。

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees (
    id INT,
    name STRING,
    department STRING
);

INSERT INTO employees VALUES
    (1, 'Alice', 'Engineering'),
    (2, 'Bob', 'Sales'),
    (3, 'Charlie', 'Engineering');

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN dept = 'Engineering' THEN true
    ELSE false
  END
  COMMENT = 'show engineering rows';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_engineering ON (department);

SELECT id, name, department FROM employees ORDER BY id;

┌────┬─────────┬─────────────┐
│ id │ name    │ department  │
├────┼─────────┼─────────────┤
│  1 │ Alice   │ Engineering │
│  3 │ Charlie │ Engineering │
└────┴─────────┴─────────────┘
```

`ON (department)` 子句将表列 `department` 映射到策略参数 `dept`。
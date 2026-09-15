---
title: POLICY_REFERENCES
summary: 返回安全策略（Masking Policy 或 Row Access Policy）与表/视图之间的关联。你可以按策略名称查询所有使用该策略的表，或按表名查询应用于该表的所有策略。
---

# POLICY_REFERENCES

返回安全策略（Masking Policy 或 Row Access Policy）与表/视图之间的关联。你可以按策略名称查询所有使用该策略的表，或按表名查询应用于该表的所有策略。

另请参阅：

- [MASKING POLICY](/tidb-cloud-lake/guides/masking-policy.md)
- [ROW ACCESS POLICY](/tidb-cloud-lake/guides/row-access-policy.md)

## 语法 {#syntax}

```sql
-- Find all tables/views using a specific policy
POLICY_REFERENCES(POLICY_NAME => '<policy_name>')

-- Find all policies applied to a specific table/view
POLICY_REFERENCES(
    REF_ENTITY_NAME => '[<database>.]<table_name>',
    REF_ENTITY_DOMAIN => 'TABLE' | 'VIEW'
)
```

## 输出列 {#output-columns}

| 列                  | 描述                                                               |
|----------------------|--------------------------------------------------------------------|
| policy_name          | 策略名称                                                           |
| policy_kind          | 策略类型：`MASKING POLICY` 或 `ROW ACCESS POLICY`                  |
| ref_database_name    | 包含被引用表/视图的数据库                                          |
| ref_entity_name      | 被引用的表或视图名称                                               |
| ref_entity_domain    | `TABLE` 或 `VIEW`                                                  |
| ref_column_name      | 应用该策略的列（适用于 masking policy）                            |
| ref_arg_column_names | 策略使用的参数列                                                   |
| policy_status        | 策略状态，通常为 `ACTIVE`                                          |

## 示例 {#examples}

### 查找使用某个 Row Access Policy 的表 {#find-tables-using-a-row-access-policy}

```sql
-- Create a row access policy
CREATE ROW ACCESS POLICY rap_employees AS (department STRING) RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN department = 'Engineering' THEN true
    ELSE false
  END;

-- Apply the policy to a table
CREATE TABLE employees(id INT, name STRING, department STRING);
ALTER TABLE employees ADD ROW ACCESS POLICY rap_employees ON (department);

-- Find all tables using this policy
SELECT * FROM policy_references(POLICY_NAME => 'rap_employees');

┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   policy_name   │    policy_kind    │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────────┼───────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ rap_employees   │ ROW ACCESS POLICY │ default           │ employees       │ TABLE             │ NULL            │ department           │ ACTIVE        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 查找应用于某个表的所有策略 {#find-all-policies-applied-to-a-table}

```sql
-- Create a masking policy
CREATE MASKING POLICY mask_salary AS (val INT) RETURNS INT ->
  CASE WHEN current_role() = 'admin' THEN val ELSE 0 END;

-- Apply both policies to the table
ALTER TABLE employees ADD COLUMN salary INT;
ALTER TABLE employees MODIFY COLUMN salary SET MASKING POLICY mask_salary;

-- Find all policies on this table
SELECT * FROM policy_references(
    REF_ENTITY_NAME => 'default.employees',
    REF_ENTITY_DOMAIN => 'TABLE'
);

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│   policy_name   │    policy_kind    │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────────┼───────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ mask_salary     │ MASKING POLICY    │ default           │ employees       │ TABLE             │ salary          │ NULL                 │ ACTIVE        │
│ rap_employees   │ ROW ACCESS POLICY │ default           │ employees       │ TABLE             │ NULL            │ department           │ ACTIVE        │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 查找使用带多个参数的 Masking Policy 的表 {#find-tables-using-a-masking-policy-with-multiple-arguments}

```sql
-- Create a masking policy with conditional arguments
CREATE MASKING POLICY mask_ssn AS (val STRING, user_role STRING) RETURNS STRING ->
  CASE
    WHEN user_role = current_role() THEN val
    ELSE '***-**-****'
  END;

-- Apply to multiple tables
CREATE TABLE employees1(id INT, ssn STRING, role STRING);
CREATE TABLE employees2(id INT, ssn STRING, role STRING);

ALTER TABLE employees1 MODIFY COLUMN ssn SET MASKING POLICY mask_ssn USING (ssn, role);
ALTER TABLE employees2 MODIFY COLUMN ssn SET MASKING POLICY mask_ssn USING (ssn, role);

-- Find all tables using this policy
SELECT * FROM policy_references(POLICY_NAME => 'mask_ssn') ORDER BY ref_entity_name;

┌───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ policy_name │   policy_kind  │ ref_database_name │ ref_entity_name │ ref_entity_domain │ ref_column_name │ ref_arg_column_names │ policy_status │
├─────────────┼────────────────┼───────────────────┼─────────────────┼───────────────────┼─────────────────┼──────────────────────┼───────────────┤
│ mask_ssn    │ MASKING POLICY │ default           │ employees1      │ TABLE             │ ssn             │ role                 │ ACTIVE        │
│ mask_ssn    │ MASKING POLICY │ default           │ employees2      │ TABLE             │ ssn             │ role                 │ ACTIVE        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
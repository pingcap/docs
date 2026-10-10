---
title: POLICY_REFERENCES
summary: セキュリティポリシー（Masking Policy または Row Access Policy）とテーブル/ビューの関連付けを返します。ポリシー名でクエリしてそのポリシーを使用しているすべてのテーブルを見つけることも、テーブル名でクエリしてそのテーブルに適用されているすべてのポリシーを見つけることもできます。
---

# POLICY_REFERENCES

セキュリティポリシー（Masking Policy または Row Access Policy）とテーブル/ビューの関連付けを返します。ポリシー名でクエリしてそのポリシーを使用しているすべてのテーブルを見つけることも、テーブル名でクエリしてそのテーブルに適用されているすべてのポリシーを見つけることもできます。

関連情報:

- [MASKING POLICY](/tidb-cloud-lake/guides/masking-policy.md)
- [ROW ACCESS POLICY](/tidb-cloud-lake/guides/row-access-policy.md)

## 構文 {#syntax}

```sql
-- Find all tables/views using a specific policy
POLICY_REFERENCES(POLICY_NAME => '<policy_name>')

-- Find all policies applied to a specific table/view
POLICY_REFERENCES(
    REF_ENTITY_NAME => '[<database>.]<table_name>',
    REF_ENTITY_DOMAIN => 'TABLE' | 'VIEW'
)
```

## 出力カラム {#output-columns}

| カラム               | 説明                                                               |
|----------------------|--------------------------------------------------------------------|
| policy_name          | ポリシーの名前                                                     |
| policy_kind          | ポリシーの種類: `MASKING POLICY` または `ROW ACCESS POLICY`       |
| ref_database_name    | 参照されるテーブル/ビューを含むデータベース                       |
| ref_entity_name      | 参照されるテーブルまたはビューの名前                              |
| ref_entity_domain    | `TABLE` または `VIEW`                                              |
| ref_column_name      | ポリシーが適用されるカラム（マスキングポリシーの場合）            |
| ref_arg_column_names | ポリシーで使用される引数カラム                                    |
| policy_status        | ポリシーのステータス。通常は `ACTIVE`                             |

## 例 {#examples}

### Row Access Policy を使用しているテーブルを見つける {#find-tables-using-a-row-access-policy}

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

### テーブルに適用されているすべてのポリシーを見つける {#find-all-policies-applied-to-a-table}

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

### 複数の引数を持つ Masking Policy を使用しているテーブルを見つける {#find-tables-using-a-masking-policy-with-multiple-arguments}

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
---
title: CREATE MASKING POLICY
summary: 在 {{{ .lake }}} 中创建新的 masking policy。
---

# CREATE MASKING POLICY

在 {{{ .lake }}} 中创建新的 masking policy。

## 语法 {#syntax}

```sql
CREATE MASKING POLICY [ IF NOT EXISTS ] <policy_name> AS
    ( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
    RETURNS <arg_type_to_mask> -> <expression_on_arg_name>
    [ COMMENT = '<comment>' ]
```

| 参数 | 描述 |
|------------------------|-------------|
| `policy_name`          | 要创建的 masking policy 名称。 |
| `arg_name_to_mask`     | 表示被脱敏列的参数。该参数必须放在第一位，并会自动绑定到 `SET MASKING POLICY` 中引用的列。 |
| `arg_type_to_mask`     | 被脱敏列的数据类型。它必须与应用该策略的列的数据类型一致。 |
| `arg_1 ... arg_n`      | 可选的额外参数，用于策略逻辑所依赖的其他列。附加策略时，通过 `USING` 子句提供这些列。 |
| `arg_type_1 ... arg_type_n` | 每个可选参数的数据类型。它们必须与 `USING` 子句中列出的列类型一致。 |
| `expression_on_arg_name` | 用于决定如何处理输入列以生成脱敏数据的表达式。 |
| `comment`              | 可选注释，用于存储有关 masking policy 的说明。 |

> **注意：**
>
> 请确保 *arg_type_to_mask* 与将要应用 masking policy 的列的数据类型一致。当策略定义了多个参数时，请在 `ALTER TABLE ... SET MASKING POLICY` 的 `USING` 子句中，按照相同顺序列出每个被引用的列。

## 访问控制要求 {#access-control-requirements}

| 权限 | 描述 |
|:----------|:------------|
| CREATE MASKING POLICY | 创建 masking policy 所需的权限。通常授予在 `*.*` 上。 |

{{{ .lake }}} 会自动将新 masking policy 的 OWNERSHIP 授予当前角色，以便其管理该策略并与其他人协作。

## 示例 {#examples}

本示例演示了如何设置 masking policy，以便根据用户角色有选择地显示或隐藏敏感数据。

```sql
-- Create a table and insert sample data
CREATE TABLE user_info (
    user_id INT,
    phone  VARCHAR,
    email VARCHAR
);

INSERT INTO user_info (user_id, phone, email) VALUES (1, '91234567', 'sue@example.com');
INSERT INTO user_info (user_id, phone, email) VALUES (2, '81234567', 'eric@example.com');

-- Create a role
CREATE ROLE 'MANAGERS';
GRANT ALL ON *.* TO ROLE 'MANAGERS';

-- Create a user and grant the role to the user
CREATE USER manager_user IDENTIFIED BY 'datalake';
GRANT ROLE 'MANAGERS' TO 'manager_user';

-- Create a masking policy that expects an extra column
CREATE MASKING POLICY contact_mask
AS
  (contact_val nullable(string), phone_ref nullable(string))
  RETURNS nullable(string) ->
  CASE
  WHEN current_role() IN ('MANAGERS') THEN
    contact_val
  WHEN phone_ref LIKE '91%'
  THEN
    contact_val
  ELSE
    '*********'
  END
  COMMENT = 'mask contact data with phone check';

-- Associate the masking policy with the 'email' column
ALTER TABLE user_info
MODIFY COLUMN email SET MASKING POLICY contact_mask USING (email, phone);

-- Associate the masking policy with the 'phone' column
ALTER TABLE user_info
MODIFY COLUMN phone SET MASKING POLICY contact_mask USING (phone, phone);

-- Query with the Root user
SELECT user_id, phone, email FROM user_info ORDER BY user_id;

     user_id     │        phone     │       email      │
 Nullable(Int32) │ Nullable(String) │ Nullable(String) │
─────────────────┼──────────────────┼──────────────────┤
               1 │ 91234567         │ sue@example.com  │
               2 │ *********        │ *********        │

```
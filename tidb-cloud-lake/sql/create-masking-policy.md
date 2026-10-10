---
title: CREATE MASKING POLICY
summary: "{{{ .lake }}} で新しいマスキングポリシーを作成します。"
---

# CREATE MASKING POLICY

{{{ .lake }}} で新しいマスキングポリシーを作成します。

## 構文 {#syntax}

```sql
CREATE MASKING POLICY [ IF NOT EXISTS ] <policy_name> AS
    ( <arg_name_to_mask> <arg_type_to_mask> [ , <arg_1> <arg_type_1> ... ] )
    RETURNS <arg_type_to_mask> -> <expression_on_arg_name>
    [ COMMENT = '<comment>' ]
```

| パラメータ               | 説明 |
|------------------------|-------------|
| `policy_name`          | 作成するマスキングポリシーの名前です。 |
| `arg_name_to_mask`     | マスク対象のカラムを表すパラメータです。この引数は先頭に指定する必要があり、`SET MASKING POLICY` で参照されるカラムに自動的にバインドされます。 |
| `arg_type_to_mask`     | マスク対象カラムのデータ型です。ポリシーを適用するカラムのデータ型と一致している必要があります。 |
| `arg_1 ... arg_n`      | ポリシーロジックが依存する追加カラム用の任意の追加パラメータです。ポリシーを関連付ける際に、`USING` 句を使ってこれらのカラムを指定します。 |
| `arg_type_1 ... arg_type_n` | 各任意パラメータのデータ型です。`USING` 句に列挙するカラムのデータ型と一致している必要があります。 |
| `expression_on_arg_name` | 入力カラムをどのように処理してマスク済みデータを生成するかを決定する式です。 |
| `comment`              | マスキングポリシーに関するメモを保存する任意のコメントです。 |

> **Note:**
>
> *arg_type_to_mask* が、マスキングポリシーを適用するカラムのデータ型と一致していることを確認してください。ポリシーで複数のパラメータを定義する場合は、参照する各カラムを `ALTER TABLE ... SET MASKING POLICY` の `USING` 句内に同じ順序で列挙してください。

## アクセス制御要件 {#access-control-requirements}

| Privilege | 説明 |
|:----------|:------------|
| CREATE MASKING POLICY | マスキングポリシーの作成に必要です。通常は `*.*` に対して付与されます。 |

{{{ .lake }}} は、新しいマスキングポリシーに対する OWNERSHIP を現在のロールに自動的に付与するため、そのロールで他のユーザーとポリシーを管理できます。

## 例 {#examples}

この例では、ユーザーロールに基づいて機密データを選択的に表示またはマスクするマスキングポリシーを設定する手順を示します。

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
---
title: CREATE ROW ACCESS POLICY
summary: "{{{ .lake }}} に新しい行アクセスポリシーを作成します。行アクセスポリシーは、ポリシーがテーブルにアタッチされたときに {{{ .lake }}} が行に適用する Boolean 述語を定義します。"
---

# CREATE ROW ACCESS POLICY

{{{ .lake }}} に新しい行アクセスポリシーを作成します。行アクセスポリシーは、ポリシーがテーブルにアタッチされたときに {{{ .lake }}} が行に適用する Boolean 述語を定義します。

## 構文 {#syntax}

```sql
CREATE ROW ACCESS POLICY [ IF NOT EXISTS ] <policy_name> AS
    ( <arg_name> <arg_type> [ , <arg_name> <arg_type> ... ] )
    RETURNS BOOLEAN -> <predicate_expression>
    [ COMMENT = '<comment>' ]
```

| パラメータ | 説明 |
|-----------|-------------|
| `policy_name` | 作成する行アクセスポリシーの名前です。ポリシー名は、マスキングポリシーと同じ名前空間を共有します。 |
| `arg_name` | 述語式の内部で使用されるポリシー引数名です。引数名はテーブルのカラム名と一致している必要はありません。 |
| `arg_type` | 引数のデータ型です。ポリシーがアタッチされると、列挙された各テーブルカラムは対応する引数型と一致している必要があります。 |
| `predicate_expression` | 行を表示するかどうかを決定する Boolean 式です。この式が `TRUE` と評価された場合にのみ行が返されます。 |
| `comment` | ポリシーに関するメモを保存するための任意のコメントです。 |

> **Note:**
>
> - 行アクセスポリシーは現在、実験的です。`SET enable_experimental_row_access_policy = 1` または `SET GLOBAL enable_experimental_row_access_policy = 1` で有効にします。
> - ポリシーは `BOOLEAN` を返す必要があります。
> - `ALTER TABLE ... ADD ROW ACCESS POLICY ... ON (...)` に列挙されたカラムは、位置によってポリシー引数にバインドされます。
> - 行アクセスポリシー定義では、サブクエリ述語はサポートされていません。

## アクセス制御要件 {#access-control-requirements}

| Privilege | 説明 |
|:----------|:------------|
| CREATE ROW ACCESS POLICY | 行アクセスポリシーを作成するために必要です。通常は `*.*` に対して付与されます。 |

{{{ .lake }}} は、新しい行アクセスポリシーに対する OWNERSHIP を現在のロールに自動的に付与するため、そのロールは他のユーザーとともにポリシーを管理できます。

## 例 {#examples}

この例では、現在のロールが `admin` でない限り、`Engineering` 部門の行のみを表示するポリシーを作成します。

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

`ON (department)` 句は、テーブルカラム `department` をポリシー引数 `dept` にマッピングします。
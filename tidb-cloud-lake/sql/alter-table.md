---
title: ALTER TABLE
summary: "`ALTER TABLE` を使用して、既存のテーブルの構造やプロパティを変更します。対象には、カラム、コメント、ストレージオプション、外部接続、さらには別のテーブルとのメタデータの入れ替えも含まれます。以下の各サブセクションでは、サポートされている各機能について説明します。"
---

# ALTER TABLE

`ALTER TABLE` を使用して、既存のテーブルの構造やプロパティを変更します。対象には、カラム、コメント、ストレージオプション、外部接続、さらには別のテーブルとのメタデータの入れ替えも含まれます。以下の各サブセクションでは、サポートされている各機能について説明します。

## カラム操作 {#column-operations}

カラムの追加、変換、名前変更、変更、削除によってテーブルを変更します。

### 構文 {#syntax}

```sql
-- Add a column to the end of the table
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
ADD [ COLUMN ] <column_name> <data_type> [ NOT NULL | NULL ] [ DEFAULT <constant_value> ]

-- Add a column to a specified position
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
ADD [ COLUMN ] <column_name> <data_type> [ NOT NULL | NULL ] [ DEFAULT <constant_value> ] [ FIRST | AFTER <column_name> ]

-- Add a virtual computed column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
ADD [ COLUMN ] <column_name> <data_type> AS (<expr>) VIRTUAL

-- Convert a stored computed column to a regular column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> DROP STORED

-- Rename a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
RENAME [ COLUMN ] <column_name> TO <new_column_name>

-- Change data type
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> <new_data_type> [ DEFAULT <constant_value> ]
       [ , [ COLUMN ] <column_name> <new_data_type> [ DEFAULT <constant_value> ] ]
       ...

-- Change comment
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> [ COMMENT '<comment>' ]
[ , [ COLUMN ] <column_name> [ COMMENT '<comment>' ] ]
...

-- Set / Unset masking policy for a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> SET MASKING POLICY <policy_name>
       [ USING ( <column_reference> [ , <column_reference> ... ] ) ]

ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
MODIFY [ COLUMN ] <column_name> UNSET MASKING POLICY

-- Remove a column
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
DROP [ COLUMN ] <column_name>
```

**Note:**

- カラムを追加または変更する際、デフォルト値として受け入れられるのは定数値のみです。非定数式を使用するとエラーになります。
- `ALTER TABLE` による stored computed column の追加は、まだサポートされていません。
- テーブルのカラムのデータ型を変更する場合、変換エラーのリスクがあります。たとえば、テキスト（String）を含むカラムを数値（Float）に変換しようとすると、問題が発生する可能性があります。
- カラムに masking policy を設定する場合は、ポリシーで定義されているデータ型（[CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md) の構文にあるパラメータ *arg_type_to_mask* を参照）がそのカラムと一致していることを確認してください。
- ポリシー定義が追加パラメータを想定している場合は、任意の `USING` 句を使用します。各ポリシー引数に対応するカラムを順番に列挙してください。最初の引数は常にマスク対象のカラムを表します。
- `USING` を含める場合は、少なくともマスク対象カラムと、ポリシーで必要な追加カラムを指定してください。`USING (...)` 内の最初の識別子は、変更対象のカラムと一致している必要があります。
- masking policy を関連付けられるのは通常のテーブルのみです。ビュー、stream、一時テーブルでは `SET MASKING POLICY` を使用できません。
- 1 つのカラムに関連付けられるセキュリティポリシー（masking または row-level）は最大 1 つです。新しいポリシーを関連付ける前に、既存のポリシーを削除してください。
- masking policy の関連付け、関連解除、表示、削除には、グローバルな `APPLY MASKING POLICY` 権限、または対象の masking policy に対する APPLY/OWNERSHIP が必要です。
- row access policy の追加または削除には、対象テーブルに対する `ALTER` 権限に加え、グローバルな `APPLY ROW ACCESS POLICY` 権限、またはそのポリシーに対する APPLY/OWNERSHIP が必要です。ポリシーの表示または削除にも同じポリシー権限が必要です。

> **Note:**
>
> カラム定義を変更したりカラムを削除したりする前に、必ず `ALTER TABLE ... MODIFY COLUMN <col> UNSET MASKING POLICY` を実行する必要があります。そうしないと、そのカラムはまだセキュリティポリシーで保護されているため、ステートメントは失敗します。

### 例 {#examples}

#### 例 1: カラムの追加、名前変更、削除 {#example-1-adding-renaming-and-removing-a-column}

この例では、`username`、`email`、`age` の各カラムを持つ `default.users` というテーブルを作成します。さらに、さまざまな制約付きで `id` と `middle_name` のカラムを追加します。また、`age` カラムの名前を変更し、その後削除する方法も示します。

```sql
-- Create a table
CREATE TABLE default.users (
  username VARCHAR(50) NOT NULL,
  email VARCHAR(255),
  age INT
);

-- Add a column to the end of the table
ALTER TABLE default.users
ADD COLUMN business_email VARCHAR(255) NOT NULL DEFAULT 'example@example.com';

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
username      |VARCHAR|NO  |''                   |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Add a column to the beginning of the table
ALTER TABLE default.users
ADD COLUMN id int NOT NULL FIRST;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Add a column after the column 'username'
ALTER TABLE default.users
ADD COLUMN middle_name VARCHAR(50) NULL AFTER username;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
age           |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Rename a column
ALTER TABLE default.users
RENAME COLUMN age TO new_age;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
new_age       |INT    |YES |NULL                 |     |
business_email|VARCHAR|NO  |'example@example.com'|     |

-- Remove a column
ALTER TABLE default.users
DROP COLUMN new_age;

DESC default.users;

Field         |Type   |Null|Default              |Extra|
--------------+-------+----+---------------------+-----+
id            |INT    |NO  |0                    |     |
username      |VARCHAR|NO  |''                   |     |
middle_name   |VARCHAR|YES |NULL                 |     |
email         |VARCHAR|YES |NULL                 |     |
```

#### 例 2: カラムの変更と Masking Policy {#example-2-modify-columns-and-masking-policies}

```sql
-- Change column types and defaults
ALTER TABLE users
MODIFY COLUMN age BIGINT DEFAULT 18,
       COLUMN email VARCHAR(320) DEFAULT '';

-- Add masking policy that expects extra arguments
ALTER TABLE users
MODIFY COLUMN email SET MASKING POLICY pii_email USING (email, username);

-- To drop or alter the column, remove the policy first
ALTER TABLE users
MODIFY COLUMN email UNSET MASKING POLICY;
```

## Row Access Policy 操作 {#row-access-policy-operations}

テーブルに row access policy を関連付ける、または関連解除します。row access policy は、クエリ実行時および DML の対象行マッチング時に行をフィルタリングします。

### 構文 {#syntax}

```sql
-- Add a row access policy to a table
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
ADD ROW ACCESS POLICY <policy_name> ON ( <column_name> [ , <column_name> ... ] )

-- Drop a specific row access policy from a table
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
DROP ROW ACCESS POLICY <policy_name>

-- Drop all row access policies from a table
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
DROP ALL ROW ACCESS POLICIES
```

> **Note:**
>
> - Row access policy は現在、実験的機能です。`SET enable_experimental_row_access_policy = 1` または `SET GLOBAL enable_experimental_row_access_policy = 1` で有効にします。
> - 1 つのテーブルに同時に設定できる row access policy は最大 1 つです。
> - `ON (...)` 内のカラムは、位置に基づいてポリシー引数にバインドされます。カラム数とそのデータ型は、ポリシーシグネチャと一致している必要があります。
> - Row access policy をアタッチできるのは通常のテーブルのみです。ビュー、stream、一時テーブルでは `ADD ROW ACCESS POLICY` は使用できません。
> - 1 つのカラムが属せる security policy は最大 1 つで、masking または row access のいずれかです。
> - Row access policy の追加または削除には、対象テーブルに対する `ALTER` 権限に加えて、グローバルな `APPLY ROW ACCESS POLICY` 権限、またはそのポリシーに対する APPLY/OWNERSHIP 権限が必要です。ポリシーの記述または削除にも同じポリシー権限が必要です。

> **Warning:**
>
> 保護されたカラムを変更または削除する前に、row access policy をデタッチする必要があります。そうしないと、そのカラムがまだ security policy から参照されているため、ステートメントは失敗します。

### 例 {#example}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE TABLE employees(id INT, name STRING, department STRING);

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN -> dept = 'Engineering';

ALTER TABLE employees
ADD ROW ACCESS POLICY rap_engineering ON (department);

ALTER TABLE employees
DROP ROW ACCESS POLICY rap_engineering;
```

## テーブルコメント {#table-comment}

テーブルのコメントを変更します。テーブルにまだコメントがない場合、このコマンドは指定したコメントをテーブルに追加します。

### 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
COMMENT = '<comment>'
```

### 例 {#examples}

```sql
-- Create a table with a comment
CREATE TABLE t(id INT) COMMENT ='original-comment';

SHOW CREATE TABLE t;

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  Table │                                 Create Table                                │
├────────┼─────────────────────────────────────────────────────────────────────────────┤
│ t      │ CREATE TABLE t (\n  id INT NULL\n) ENGINE=FUSE COMMENT = 'original-comment' │
└──────────────────────────────────────────────────────────────────────────────────────┘

-- Modify the comment
ALTER TABLE t COMMENT = 'new-comment';

SHOW CREATE TABLE t;

┌─────────────────────────────────────────────────────────────────────────────────┐
│  Table │                              Create Table                              │
├────────┼────────────────────────────────────────────────────────────────────────┤
│ t      │ CREATE TABLE t (\n  id INT NULL\n) ENGINE=FUSE COMMENT = 'new-comment' │
└─────────────────────────────────────────────────────────────────────────────────┘
```

```sql
-- Create a table without comment
CREATE TABLE t(id INT);

-- Add a comment later
ALTER TABLE t COMMENT = 'new-comment';
```

## Fuse Engine オプション {#fuse-engine-options}

テーブルの [Fuse Engine options](/tidb-cloud-lake/sql/fuse-engine-tables.md#fuse-engine-options) を設定または解除します。

### 構文 {#syntax}

```sql
-- Set Fuse Engine options
ALTER TABLE [ <database_name>. ]<table_name> SET OPTIONS (<options>)

-- Unset Fuse Engine options, reverting them to their default values
ALTER TABLE [ <database_name>. ]<table_name> UNSET OPTIONS (<options>)
```

解除できる Fuse Engine オプションは次のものだけです。

- `block_per_segment`
- `block_size_threshold`
- `data_retention_period_in_hours`
- `data_retention_num_snapshots_to_keep`
- `enable_schema_evolution`
- `row_avg_depth_threshold`
- `row_per_block`
- `row_per_page`

### 例 {#examples}

```sql
CREATE TABLE fuse_table (a int);

SET hide_options_in_show_create_table=0;

-- Show current options
SHOW CREATE TABLE fuse_table;

-- Change Fuse options
ALTER TABLE fuse_table SET OPTIONS (block_per_segment = 500, data_retention_period_in_hours = 240);

-- Show updated options
SHOW CREATE TABLE fuse_table;
```

```sql
-- Limit snapshots and enable auto vacuum
CREATE OR REPLACE TABLE t(c INT);
ALTER TABLE t SET OPTIONS(data_retention_num_snapshots_to_keep = 1);
SET enable_auto_vacuum = 1;
INSERT INTO t VALUES(1);
INSERT INTO t VALUES(2);
INSERT INTO t VALUES(3);

-- Revert options to defaults
ALTER TABLE fuse_table UNSET OPTIONS (block_per_segment, data_retention_period_in_hours);
```

## 外部テーブル接続 {#external-table-connection}

外部テーブルの接続設定を更新します。コマンド実行時に適用されるのは、認証情報関連のフィールド（`access_key_id`、`secret_access_key`、`role_arn`）のみです。`bucket`、`region`、`root` などのその他のプロパティは変更されません。

### 構文 {#syntax}

```sql
ALTER TABLE [ <database_name>. ]<table_name> CONNECTION = ( connection_name = '<connection_name>' )
```

| パラメータ | 説明 | 必須 |
|-----------|-------------|----------|
| connection_name | 外部テーブルで使用する接続の名前です。この接続はシステム内にすでに存在している必要があります。 | はい |

このコマンドは、認証情報をローテーションする必要がある場合や、IAM ロールが変更された場合に特に便利です。このコマンドで使用する前に、指定した接続がすでに存在している必要があります。

**セキュリティのベストプラクティス**

外部テーブルを扱う場合、AWS IAM ロールは access key と比べて大きなセキュリティ上の利点があります。

- 認証情報を保存しない: 設定内に access key を保存する必要がなくなります
- 自動ローテーション: 認証情報のローテーションを自動的に処理します
- きめ細かな制御: より正確なアクセス制御が可能です

{{{ .lake }}} で IAM ロールを使用する方法については、[AWS IAM Role による認証](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md) を参照してください。

### 例 {#examples}

```sql
-- Create connections
CREATE CONNECTION external_table_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE CONNECTION external_table_conn_new
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-new-access-key-id>'
    SECRET_ACCESS_KEY = '<your-new-secret-access-key>';

-- Create an external table using the first connection
CREATE OR REPLACE TABLE external_table_test (
    id INT,
    name VARCHAR,
    age INT
)
's3://testbucket/13_fuse_external_table/'
CONNECTION=(connection_name = 'external_table_conn');

-- Update to use the new connection
ALTER TABLE external_table_test CONNECTION=( connection_name = 'external_table_conn_new' );
```

```sql
-- Migrate to IAM role authentication
CREATE CONNECTION s3_access_key_conn
    STORAGE_TYPE = 's3'
    ACCESS_KEY_ID = '<your-access-key-id>'
    SECRET_ACCESS_KEY = '<your-secret-access-key>';

CREATE TABLE sales_data (
    order_id INT,
    product_name VARCHAR,
    quantity INT
)
's3://sales-bucket/data/'
CONNECTION=(connection_name = 's3_access_key_conn');

CREATE CONNECTION s3_role_conn
    STORAGE_TYPE = 's3'
    ROLE_ARN = 'arn:aws:iam::123456789012:role/lake-access';

ALTER TABLE sales_data CONNECTION=( connection_name = 's3_role_conn' );
```

## スナップショットタグ操作 {#snapshot-tag-operations}

<FunctionDescription description="Introduced or updated: v1.2.891"/>

特定の FUSE テーブルスナップショットを参照する名前付きスナップショットタグを作成または削除します。スナップショットタグを使用すると、テーブルのある時点の状態をブックマークでき、後で [AT](/tidb-cloud-lake/sql/at.md) 句を使ってクエリできます。

詳細については、以下を参照してください。

- [CREATE SNAPSHOT TAG](/tidb-cloud-lake/sql/create-snapshot-tag.md)
- [DROP SNAPSHOT TAG](/tidb-cloud-lake/sql/drop-snapshot-tag.md)

> **Note:**
>
> スナップショットタグは、[governance tags](#tag-operations) とは異なります。スナップショットタグはタイムトラベルのためにテーブルスナップショットをブックマークするものであり、governance tags は分類のためにオブジェクトへキーと値のメタデータを付与するものです。

## テーブルの入れ替え {#swap-tables}

1 つのトランザクション内で、2 つのテーブル間のすべてのテーブルメタデータとデータをアトミックに入れ替えます。この操作では、すべてのカラム、制約、データを含むテーブルスキーマが交換され、結果として各テーブルがもう一方のテーブルの実体を引き継ぎます。

### 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <source_table_name> SWAP WITH <target_table_name>
```

| パラメータ | 説明 |
|----------------------|------------------------------------------------|
| `source_table_name`  | 入れ替え元となる 1 つ目のテーブル名 |
| `target_table_name`  | 入れ替え先となる 2 つ目のテーブル名 |

### 使用上の注意 {#usage-notes}

- Fuse Engine テーブルでのみ使用できます。外部テーブル、システムテーブル、およびその他の非 Fuse テーブルはサポートされません。
- 一時テーブルは、永続テーブルまたは transient テーブルと入れ替えることはできません。
- 入れ替え操作を実行するには、現在のロールが両方のテーブルの所有者である必要があります。
- 両方のテーブルは同じデータベース内に存在する必要があります。データベースをまたぐ入れ替えはサポートされません。
- 入れ替え操作はアトミックです。両方のテーブルが正常に入れ替えられるか、どちらも変更されないかのいずれかです。
- 入れ替え中はすべてのデータとメタデータが保持されます。データが失われたり変更されたりすることはありません。

### 例 {#examples}

```sql
-- Create two tables with different schemas
CREATE OR REPLACE TABLE t1(a1 INT, a2 VARCHAR, a3 DATE);
CREATE OR REPLACE TABLE t2(b1 VARCHAR);

-- Check table schemas before swap
DESC t1;
DESC t2;

-- Swap the tables
ALTER TABLE t1 SWAP WITH t2;

-- After swapping, t1 now has t2's schema, and t2 has t1's schema
DESC t1;
DESC t2;
```

## タグ操作 {#tag-operations}

テーブルに governance tags を割り当てる、または削除します。governance tags は、分類とデータガバナンスのためのキーと値のメタデータです。タグは事前に [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) で作成しておく必要があります。詳細については、[SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md) を参照してください。

### 構文 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

### 例 {#examples}

```sql
ALTER TABLE default.users SET TAG env = 'prod', owner = 'team_a';
ALTER TABLE default.users UNSET TAG env, owner;
```
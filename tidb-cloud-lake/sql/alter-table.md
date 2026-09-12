---
title: ALTER TABLE
summary: 使用 ALTER TABLE 修改现有表的结构和属性，包括其列、注释、存储选项、外部连接，甚至与另一张表交换元信息。以下各小节介绍了每种受支持的功能。
---

# ALTER TABLE

使用 `ALTER TABLE` 修改现有表的结构和属性，包括其列、注释、存储选项、外部连接，甚至与另一张表交换元信息。以下各小节介绍了每种受支持的功能。

## 列操作 {#column-operations}

通过添加、转换、重命名、更改或删除列来修改表。

### 语法 {#syntax}

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

**注意：**

- 添加或修改列时，默认值只能接受常量值。如果使用非常量表达式，则会报错。
- 目前尚不支持使用 ALTER TABLE 添加 stored computed column。
- 更改表列的数据类型时，存在转换错误的风险。例如，如果尝试将包含文本（String）的列转换为数字（Float），可能会导致问题。
- 为列设置 masking policy 时，请确保策略中定义的数据类型（参见 [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md) 语法中的参数 *arg_type_to_mask*）与该列匹配。
- 当策略定义需要额外参数时，请使用可选的 `USING` 子句。按顺序列出映射到每个策略参数的列；第一个参数始终表示被脱敏的列。
- 如果包含 `USING`，则至少需要提供被脱敏的列，以及策略所需的其他附加列。`USING (...)` 中的第一个标识符必须与正在修改的列一致。
- masking policy 只能附加到普通表。视图、stream 和临时表不允许使用 `SET MASKING POLICY`。
- 一列最多只能属于一个安全策略（masking 或 row-level）。在附加新策略之前，请先移除现有策略。
- 附加、分离、描述或删除 masking policy 需要全局 `APPLY MASKING POLICY` 权限，或针对特定 masking policy 的 APPLY/OWNERSHIP 权限。
- 添加或删除 row access policy 需要目标表上的 `ALTER` 权限，以及全局 `APPLY ROW ACCESS POLICY` 权限，或该策略上的 APPLY/OWNERSHIP 权限。描述或删除策略需要相同的策略权限。

> **注意：**
>
> 在更改列定义或删除列之前，必须先执行 `ALTER TABLE ... MODIFY COLUMN <col> UNSET MASKING POLICY`；否则该语句会失败，因为该列仍受安全策略保护。

### 示例 {#examples}

#### 示例 1：添加、重命名和删除列 {#example-1-adding-renaming-and-removing-a-column}

本示例展示了如何创建名为 "default.users" 的表，其中包含 'username'、'email' 和 'age' 列。示例还演示了如何添加带有不同约束的 'id' 和 'middle_name' 列，以及如何重命名并随后删除 "age" 列。

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

#### 示例 2：修改列和 masking policy {#example-2-modify-columns-and-masking-policies}

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

## 行访问策略操作 {#row-access-policy-operations}

为表附加或分离行访问策略。行访问策略会在查询时以及 DML 目标行匹配期间过滤行。

### 语法 {#syntax}

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

> **注意：**
>
> - 行访问策略当前为实验特性。可使用 `SET enable_experimental_row_access_policy = 1` 或 `SET GLOBAL enable_experimental_row_access_policy = 1` 启用。
> - 一张表在同一时间最多只能有一个行访问策略。
> - `ON (...)` 中的列按位置绑定到策略参数。列的数量及其数据类型必须与策略签名匹配。
> - 行访问策略只能附加到普通表。视图、流和临时表不允许使用 `ADD ROW ACCESS POLICY`。
> - 一列最多只能属于一个安全策略，即脱敏策略或行访问策略中的一种。
> - 添加或移除行访问策略需要目标表上的 `ALTER` 权限，以及全局 `APPLY ROW ACCESS POLICY` 权限，或该策略上的 APPLY/OWNERSHIP 权限。描述或删除策略也需要相同的策略权限。

> **警告：**
>
> 在修改或删除受保护列之前，必须先解除关联的行访问策略。否则，由于该列仍被安全策略引用，语句会失败。

### 示例 {#example}

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

## 表注释 {#table-comment}

修改表的注释。如果该表尚未设置注释，此命令会为表添加指定的注释。

### 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
COMMENT = '<comment>'
```

### 示例 {#examples}

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

## Fuse Engine 选项 {#fuse-engine-options}

为表设置或取消设置 [Fuse Engine 选项](/tidb-cloud-lake/sql/fuse-engine-tables.md#fuse-engine-options)。

### 语法 {#syntax}

```sql
-- Set Fuse Engine options
ALTER TABLE [ <database_name>. ]<table_name> SET OPTIONS (<options>)

-- Unset Fuse Engine options, reverting them to their default values
ALTER TABLE [ <database_name>. ]<table_name> UNSET OPTIONS (<options>)
```

只有以下 Fuse Engine 选项可以取消设置：

- `block_per_segment`
- `block_size_threshold`
- `data_retention_period_in_hours`
- `data_retention_num_snapshots_to_keep`
- `enable_schema_evolution`
- `row_avg_depth_threshold`
- `row_per_block`
- `row_per_page`

### 示例 {#examples}

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

## 外部表连接 {#external-table-connection}

更新外部表的连接设置。命令执行时，仅会应用与凭证相关的字段（`access_key_id`、`secret_access_key`、`role_arn`）。其他属性（如 `bucket`、`region` 或 `root`）保持不变。

### 语法 {#syntax}

```sql
ALTER TABLE [ <database_name>. ]<table_name> CONNECTION = ( connection_name = '<connection_name>' )
```

| 参数 | 描述 | 必填 |
|-----------|-------------|----------|
| connection_name | 用于外部表的连接名称。该连接必须已存在于系统中。 | 是 |

当需要轮转凭证或 IAM 角色发生变化时，此命令特别有用。使用此命令前，指定的连接必须已存在。

**安全最佳实践**

在使用外部表时，相比 access keys，AWS IAM roles 具有显著的安全优势：

- 无需存储凭证：无需在配置中存储 access keys
- 自动轮转：自动处理凭证轮转
- 细粒度控制：可实现更精确的访问控制

如需在 {{{ .lake }}} 中使用 IAM roles，请参见[使用 AWS IAM Role 进行身份验证](/tidb-cloud-lake/guides/authenticate-with-aws-iam-role.md)。

### 示例 {#examples}

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

## 快照标签操作 {#snapshot-tag-operations}

<FunctionDescription description="Introduced or updated: v1.2.891"/>

创建或删除一个命名的快照标签，该标签引用特定的 FUSE 表快照。快照标签可让你为表的某个时间点状态添加书签，以便后续通过 [AT](/tidb-cloud-lake/sql/at.md) 子句进行查询。

完整详情请参见：

- [CREATE SNAPSHOT TAG](/tidb-cloud-lake/sql/create-snapshot-tag.md)
- [DROP SNAPSHOT TAG](/tidb-cloud-lake/sql/drop-snapshot-tag.md)

> **注意：**
>
> 快照标签不同于[治理标签](#tag-operations)。快照标签用于为表快照添加时间旅行书签，而治理标签则用于将键值元信息附加到对象上，以便进行分类。

## 交换表 {#swap-tables}

在单个事务中以原子方式交换两个表之间的所有表元信息和数据。此操作会交换表结构，包括所有列、约束和数据，从而使每个表实际上获得对方的身份。

### 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] <source_table_name> SWAP WITH <target_table_name>
```

| 参数 | 描述 |
|----------------------|------------------------------------------------|
| `source_table_name`  | 要交换的第一个表的名称 |
| `target_table_name`  | 要与之交换的第二个表的名称 |

### 使用说明 {#usage-notes}

- 仅适用于 Fuse Engine 表。不支持外部表、系统表以及其他非 Fuse 表。
- 临时表不能与永久表或 transient 表进行交换。
- 当前角色必须同时是这两个表的所有者，才能执行交换操作。
- 两个表必须位于同一个数据库中。不支持跨数据库交换。
- 交换操作是原子的。要么两个表都成功交换，要么都不会发生变化。
- 交换期间会保留所有数据和元信息。不会丢失或修改任何数据。

### 示例 {#examples}

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

## 标签操作 {#tag-operations}

为表分配或移除治理标签。治理标签是用于分类和数据治理的键值元信息。必须先使用 [CREATE TAG](/tidb-cloud-lake/sql/create-tag.md) 创建标签。完整详情请参见 [SET TAG / UNSET TAG](/tidb-cloud-lake/sql/set-tag.md)。

### 语法 {#syntax}

```sql
ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
    SET TAG <tag_name> = '<value>' [, <tag_name> = '<value>' ...]

ALTER TABLE [ IF EXISTS ] [ <database_name>. ]<table_name>
    UNSET TAG <tag_name> [, <tag_name> ...]
```

### 示例 {#examples}

```sql
ALTER TABLE default.users SET TAG env = 'prod', owner = 'team_a';
ALTER TABLE default.users UNSET TAG env, owner;
```
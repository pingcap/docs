---
title: CREATE TABLE
summary: 对于许多数据库来说，创建表是最复杂的操作之一，因为你可能需要。
---

# CREATE TABLE

对于许多数据库来说，创建表是最复杂的操作之一，因为你可能需要：

- 手动指定引擎
- 手动指定索引
- 甚至指定数据分区或数据分片

{{{ .lake }}} 的设计目标是易于使用，因此在创建表时**不需要**执行上述任何操作。此外，CREATE TABLE 语句还提供了以下选项，使你能够在各种场景下更轻松地创建表：

- [CREATE TABLE](#create-table)：从头开始创建表。
- [CREATE TABLE ... LIKE](#create-table--like)：使用与现有表相同的列定义创建表。
- [CREATE TABLE ... AS](#create-table--as)：创建表，并将 SELECT 查询的结果插入其中。

另请参阅：

- [CREATE TEMP TABLE](/tidb-cloud-lake/sql/create-temp-table.md)
- [CREATE TRANSIENT TABLE](/tidb-cloud-lake/sql/create-transient-table.md)
- [CREATE EXTERNAL TABLE](/tidb-cloud-lake/sql/create-external-table.md)

## CREATE TABLE {#create-table}

```sql
CREATE [ OR REPLACE ] TABLE [ IF NOT EXISTS ] [ <database_name>. ]<table_name>
(
    <column_name> <data_type> [ NOT NULL | NULL ]
                              [ { DEFAULT <expr>
                                | { AUTOINCREMENT | IDENTITY }
                                  [ { ( <start_num> , <step_num> )
                                    | START <num> INCREMENT <num> } ]
                                  [ { ORDER | NOORDER } ]
                                } ]
                              [ AS (<expr>) STORED | VIRTUAL ]
                              [ COMMENT '<comment>' ],
    <column_name> <data_type> ...
    ...
)
```

> **Note:**
>
> - 关于 {{{ .lake }}} 中可用的数据类型，请参阅 [数据类型](/tidb-cloud-lake/sql/data-types.md)。
>
> - {{{ .lake }}} 建议在命名列时尽量避免使用特殊字符。不过，如果在某些情况下必须使用特殊字符，则应将别名用反引号括起来，例如：CREATE TABLE price(\`$CA\` int);
>
> - {{{ .lake }}} 会自动将列名转换为小写。例如，如果你将某列命名为 _Total_，则它会在结果中显示为 _total_。

## CREATE TABLE ... LIKE {#create-table-like}

使用与现有表相同的列定义创建表。现有表的列名、数据类型及其非 NULL 约束将被复制到新表中。

语法：

```sql
CREATE TABLE [IF NOT EXISTS] [db.]table_name
LIKE [db.]origin_table_name
```

此命令不会包含原表中的任何数据或属性（例如 `CLUSTER BY`、`TRANSIENT` 和 `COMPRESSION`），而是使用系统默认设置创建一个新表。

> **Note:**
>
> - 使用此命令创建新表时，可以显式指定 `TRANSIENT` 和 `COMPRESSION`。例如：
>
> ```sql
> create transient table t_new like t_old;
>
> create table t_new compression='lz4' like t_old;
> ```

## CREATE TABLE ... AS {#create-table-as}

创建一个表，并使用 SELECT 命令计算得到的数据填充该表。

语法：

```sql
CREATE TABLE [IF NOT EXISTS] [db.]table_name
AS SELECT query
```

此命令不会包含原表中的任何属性（例如 CLUSTER BY、TRANSIENT 和 COMPRESSION），而是使用系统默认设置创建一个新表。

> **Note:**
>
> - 使用此命令创建新表时，可以显式指定 `TRANSIENT` 和 `COMPRESSION`。例如：
>
> ```sql
> create transient table t_new as select * from t_old;
>
> create table t_new compression='lz4' as select * from t_old;
> ```

## Column Nullable {#column-nullable}

默认情况下，{{{ .lake }}} 中的**所有列都允许为空（NULL）**。如果你需要某一列不允许 NULL 值，请使用 NOT NULL 约束。更多信息，请参阅 [NULL 值和 NOT NULL 约束](/tidb-cloud-lake/sql/data-types.md)。

## Column Default Values {#column-default-values}

`DEFAULT <expr>` 用于在未提供显式表达式时为列设置默认值。默认表达式可以是：

- 固定常量，例如下面示例中 `department` 列的 `Marketing`。
- 不带输入参数并返回标量值的表达式，例如 `1 + 1`、`NOW()` 或 `UUID()`。
- 由序列动态生成的值，例如下面示例中 `staff_id` 列的 `NEXTVAL(staff_id_seq)`。
    - NEXTVAL 必须作为独立的默认值使用；不支持 `NEXTVAL(seq1) + 1` 之类的表达式。
    - 用户必须遵循其已授予的序列使用权限要求，包括 [NEXTVAL](/tidb-cloud-lake/sql/nextval.md#access-control-requirements) 等操作

## Auto-Increment Columns {#auto-increment-columns}

`AUTOINCREMENT` 或 `IDENTITY` 可用于创建自增列，以自动生成连续的数值。这对于创建唯一标识符特别有用。

**语法：**

```sql
{ AUTOINCREMENT | IDENTITY }
  [ { ( <start_num> , <step_num> )
    | START <num> INCREMENT <num> } ]
  [ { ORDER | NOORDER } ]
```

**参数：**

- `start_num`：自增序列的初始值（默认值：1）
- `step_num`：每插入一行时的递增值（默认值：1）
- `ORDER`：保证值单调递增（可能存在间隔）
- `NOORDER`：不保证顺序（默认）

**要点：**

- 自增列在内部由序列支持
- 当删除带有 AUTOINCREMENT/IDENTITY 的列时，其关联的序列也会被删除
- 如果在插入时未提供显式值，则会自动生成下一个值
- `AUTOINCREMENT` 和 `IDENTITY` 是同义词，行为完全一致

**示例：**

```sql
-- Create a table with auto-increment columns
CREATE TABLE users (
    user_id BIGINT AUTOINCREMENT,
    order_id BIGINT AUTOINCREMENT START 100 INCREMENT 10,
    username VARCHAR
);

-- Insert data without specifying auto-increment columns
INSERT INTO users (username) VALUES ('alice'), ('bob'), ('charlie');

-- Query the table to see auto-generated values
SELECT * FROM users;

+----------+----------+----------+
| user_id  | order_id | username |
+----------+----------+----------+
|        0 |      100 | alice    |
|        1 |      110 | bob      |
|        2 |      120 | charlie  |
+----------+----------+----------+
```

## 计算列 {#computed-columns}

计算列使用标量表达式基于其他列生成。{{{ .lake }}} 支持两种类型：

- **STORED**：值会被实际存储，并在依赖列发生变化时自动修改
- **VIRTUAL**：值会在查询期间动态计算，从而节省存储空间

**语法：**

```sql
<column_name> <data_type> [ NOT NULL | NULL ] AS (<expr>) { STORED | VIRTUAL }
<column_name> <data_type> [ NOT NULL | NULL ] GENERATED ALWAYS AS (<expr>) { STORED | VIRTUAL }
```

**示例：**

```sql
-- Stored: physically stored, updates immediately
CREATE TABLE products (
  id INT,
  price FLOAT64,
  quantity INT,
  total_price FLOAT64 AS (price * quantity) STORED
);

-- Virtual: computed on query, no storage overhead
CREATE TABLE employees (
  id INT,
  first_name VARCHAR,
  last_name VARCHAR,
  full_name VARCHAR AS (CONCAT(first_name, ' ', last_name)) VIRTUAL
);
```

> **Tip:**
>
> 对于经常查询且性能很重要的列，请选择 **STORED**。如果计算成本可以接受，并且希望节省存储空间，请选择 **VIRTUAL**。

## MySQL 兼容性 {#mysql-compatibility}

{{{ .lake }}} 的语法与 MySQL 的差异主要体现在数据类型以及某些特定的索引提示上。

与 MySQL 不同，{{{ .lake }}} 默认遵循 PostgreSQL 风格的标识符大小写规则：未加引号的列名会被折叠为小写，而使用双引号的名称会保留原始大小写，并且是大小写敏感的。因此，使用带引号且保留大小写的列名（例如 `"Employee_ID"`）创建的表，执行 `SELECT *` 时可以返回行，但执行 `SELECT Employee_ID` 或 `SELECT employee_id` 时可能失败。有关标识符大小写规则、相关设置和故障排查的更多信息，请参见 [SQL 标识符](/tidb-cloud-lake/sql/sql-identifiers.md#identifier-casing-rules)。

## 访问控制要求 {#access-control-requirements}

| 权限 | 对象类型   | 描述            |
|:----------|:--------------|:-----------------------|
| CREATE    | 全局, Table | 创建表。       |

要创建表，执行该操作的用户或 [current_role](/tidb-cloud-lake/guides/roles.md) 必须具有 CREATE [权限](/tidb-cloud-lake/guides/privileges.md#table-privileges)。

## 示例 {#examples}

### 创建表 {#create-table}

创建一个表，并为某列设置默认值（在本例中，`genre` 列的默认值为 `'General'`）：

```sql
CREATE TABLE books (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
);
```

描述该表以确认表结构以及 `genre` 列的默认值：

```sql
DESC books;
+-------+-----------------+------+---------+-------+
| Field | Type            | Null | Default | Extra |
+-------+-----------------+------+---------+-------+
| id    | BIGINT UNSIGNED | YES  | 0       |       |
| title | VARCHAR         | YES  | ""      |       |
| genre | VARCHAR         | YES  | 'General'|       |
+-------+-----------------+------+---------+-------+
```

插入一行数据，不指定 `genre`：

```sql
INSERT INTO books(id, title) VALUES(1, 'Invisible Stars');
```

查询该表，可以看到默认值 `'General'` 已被设置到 `genre` 列：

```sql
SELECT * FROM books;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### 创建表 ... Like {#create-table-like}

创建一个新表（`books_copy`），其结构与现有表（`books`）相同：

```sql
CREATE TABLE books_copy LIKE books;
```

检查新表的结构：

```sql
DESC books_copy;
+-------+-----------------+------+---------+-------+
| Field | Type            | Null | Default | Extra |
+-------+-----------------+------+---------+-------+
| id    | BIGINT UNSIGNED | YES  | 0       |       |
| title | VARCHAR         | YES  | ""      |       |
| genre | VARCHAR         | YES  | 'General'|       |
+-------+-----------------+------+---------+-------+
```

向新表插入一行数据，可以看到 `genre` 列的默认值也被复制了：

```sql
INSERT INTO books_copy(id, title) VALUES(1, 'Invisible Stars');

SELECT * FROM books_copy;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### 创建表 ... As {#create-table-as}

创建一个新表（`books_backup`），其中包含现有表（`books`）中的数据：

```sql
CREATE TABLE books_backup AS SELECT * FROM books;
```

描述新表，可以看到 `genre` 列的默认值**不会**被复制：

```sql
DESC books_backup;
+-------+-----------------+------+---------+-------+
| Field | Type            | Null | Default | Extra |
+-------+-----------------+------+---------+-------+
| id    | BIGINT UNSIGNED | NO   | 0       |       |
| title | VARCHAR         | NO   | ""      |       |
| genre | VARCHAR         | NO   | NULL    |       |
+-------+-----------------+------+---------+-------+
```

查询新表，可以看到原表中的数据已被复制：

```sql
SELECT * FROM books_backup;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### Create Table ... Column As STORED | VIRTUAL {#create-table-column-as-stored-virtual}

以下示例演示了一个包含 stored 计算列的表，该列会在 `price` 或 `quantity` 列更新时自动重新计算：

```sql
-- Create the table with a stored computed column
CREATE TABLE IF NOT EXISTS products (
  id INT,
  price FLOAT64,
  quantity INT,
  total_price FLOAT64 AS (price * quantity) STORED
);

-- Insert data into the table
INSERT INTO products (id, price, quantity)
VALUES (1, 10.5, 3),
       (2, 15.2, 5),
       (3, 8.7, 2);

-- Query the table to see the computed column
SELECT id, price, quantity, total_price
FROM products;

---
+------+-------+----------+-------------+
| id   | price | quantity | total_price |
+------+-------+----------+-------------+
|    1 |  10.5 |        3 |        31.5 |
|    2 |  15.2 |        5 |        76.0 |
|    3 |   8.7 |        2 |        17.4 |
+------+-------+----------+-------------+
```

在此示例中，我们创建了一个名为 student*profiles 的表，其中包含一个名为 profile 的 Variant 类型列，用于存储 JSON 数据。我们还添加了一个名为 \_age* 的 virtual 计算列，用于从 profile 列中提取 age 属性并将其转换为整数型。

```sql
-- Create the table with a virtual computed column
CREATE TABLE student_profiles (
    id STRING,
    profile VARIANT,
    age INT NULL AS (profile['age']::INT) VIRTUAL
);

-- Insert data into the table
INSERT INTO student_profiles (id, profile) VALUES
    ('d78236', '{"id": "d78236", "name": "Arthur Read", "age": "16", "school": "PVPHS", "credits": 120, "sports": "none"}'),
    ('f98112', '{"name": "Buster Bunny", "age": "15", "id": "f98112", "school": "TEO", "credits": 67, "clubs": "MUN"}'),
    ('t63512', '{"name": "Ernie Narayan", "school" : "Brooklyn Tech", "id": "t63512", "sports": "Track and Field", "clubs": "Chess"}');

-- Query the table to see the computed column
SELECT * FROM student_profiles;

+--------+------------------------------------------------------------------------------------------------------------+------+
| id     | profile                                                                                                    | age  |
+--------+------------------------------------------------------------------------------------------------------------+------+
| d78236 | `{"age":"16","credits":120,"id":"d78236","name":"Arthur Read","school":"PVPHS","sports":"none"}`            |   16 |
| f98112 | `{"age":"15","clubs":"MUN","credits":67,"id":"f98112","name":"Buster Bunny","school":"TEO"}`                |   15 |
| t63512 | `{"clubs":"Chess","id":"t63512","name":"Ernie Narayan","school":"Brooklyn Tech","sports":"Track and Field"}` | NULL |
+--------+------------------------------------------------------------------------------------------------------------+------+
```
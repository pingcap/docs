---
title: CREATE TABLE
summary: テーブルの作成は、多くのデータベースにおいて最も複雑な操作の 1 つです。なぜなら、必要に応じてさまざまな指定を行う必要があるためです。
---

# CREATE TABLE

テーブルの作成は、多くのデータベースにおいて最も複雑な操作の 1 つです。たとえば、次のような指定が必要になることがあります。

- エンジンを手動で指定する
- インデックスを手動で指定する
- さらには、データパーティションやデータシャードを指定する

{{{ .lake }}} は、設計上使いやすさを重視しており、テーブル作成時にこれらの操作を必要としません。さらに、CREATE TABLE ステートメントには、さまざまなシナリオでより簡単にテーブルを作成できるよう、次のオプションが用意されています。

- [CREATE TABLE](#create-table): 新しいテーブルを一から作成します。
- [CREATE TABLE ... LIKE](#create-table--like): 既存のテーブルと同じカラム定義を持つテーブルを作成します。
- [CREATE TABLE ... AS](#create-table--as): テーブルを作成し、SELECT クエリの結果を使ってデータを挿入します。

関連情報:

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
> - {{{ .lake }}} で使用可能なデータ型については、[Data Types](/tidb-cloud-lake/sql/data-types.md) を参照してください。
>
> - {{{ .lake }}} では、カラム名に特殊文字をできるだけ使用しないことを推奨しています。ただし、場合によって特殊文字が必要な場合は、次のようにエイリアスをバッククォートで囲む必要があります: CREATE TABLE price(\`$CA\` int);
>
> - {{{ .lake }}} はカラム名を自動的に小文字に変換します。たとえば、カラム名を _Total_ とした場合、結果では _total_ と表示されます。

## CREATE TABLE ... LIKE {#create-table-like}

既存のテーブルと同じカラム定義を持つテーブルを作成します。既存テーブルのカラム名、データ型、および NOT NULL 制約が新しいテーブルにコピーされます。

構文:

```sql
CREATE TABLE [IF NOT EXISTS] [db.]table_name
LIKE [db.]origin_table_name
```

このコマンドには、元のテーブルのデータや属性（`CLUSTER BY`、`TRANSIENT`、`COMPRESSION` など）は含まれません。その代わり、デフォルトのシステム設定を使用して新しいテーブルを作成します。

> **Note:**
>
> - このコマンドで新しいテーブルを作成する際には、`TRANSIENT` と `COMPRESSION` を明示的に指定できます。例:
>
> ```sql
> create transient table t_new like t_old;
>
> create table t_new compression='lz4' like t_old;
> ```

## CREATE TABLE ... AS {#create-table-as}

テーブルを作成し、SELECT コマンドによって計算されたデータをそのテーブルに格納します。

構文:

```sql
CREATE TABLE [IF NOT EXISTS] [db.]table_name
AS SELECT query
```

このコマンドには、元のテーブルの属性（CLUSTER BY、TRANSIENT、COMPRESSION など）は含まれません。その代わり、デフォルトのシステム設定を使用して新しいテーブルを作成します。

> **Note:**
>
> - このコマンドで新しいテーブルを作成する際には、`TRANSIENT` と `COMPRESSION` を明示的に指定できます。例:
>
> ```sql
> create transient table t_new as select * from t_old;
>
> create table t_new compression='lz4' as select * from t_old;
> ```

## Column Nullable {#column-nullable}

{{{ .lake }}} では、デフォルトで **すべてのカラムが nullable(NULL)** です。NULL 値を許可しないカラムが必要な場合は、NOT NULL 制約を使用してください。詳細は [NULL Values and NOT NULL Constraint](/tidb-cloud-lake/sql/data-types.md) を参照してください。

## Column Default Values {#column-default-values}

`DEFAULT <expr>` は、明示的な式が指定されていない場合に、カラムのデフォルト値を設定します。デフォルト式には次のものを使用できます。

- 固定定数。たとえば、以下の例にある `department` カラムの `Marketing`。
- 入力引数を持たず、スカラー値を返す式。たとえば、`1 + 1`、`NOW()`、`UUID()`。
- シーケンスから動的に生成される値。たとえば、以下の例にある `staff_id` カラムの `NEXTVAL(staff_id_seq)`。
    - NEXTVAL は単独のデフォルト値として使用する必要があります。`NEXTVAL(seq1) + 1` のような式はサポートされていません。
    - ユーザーは、[NEXTVAL](/tidb-cloud-lake/sql/nextval.md#access-control-requirements) などの操作を含め、シーケンスの利用に関して付与された権限に従う必要があります。

## Auto-Increment Columns {#auto-increment-columns}

`AUTOINCREMENT` または `IDENTITY` を使用すると、自動インクリメントカラムを作成できます。これらのカラムは、連続した数値を自動生成します。これは、一意な識別子を作成する場合に特に便利です。

**構文:**

```sql
{ AUTOINCREMENT | IDENTITY }
  [ { ( <start_num> , <step_num> )
    | START <num> INCREMENT <num> } ]
  [ { ORDER | NOORDER } ]
```

**パラメータ:**

- `start_num`: 自動インクリメントのシーケンスの初期値（デフォルト: 1）
- `step_num`: 新しい各行に対する増分値（デフォルト: 1）
- `ORDER`: 単調増加する値を保証します（途中に欠番が生じる可能性があります）
- `NOORDER`: 順序を保証しません（デフォルト）

**重要なポイント:**

- 自動インクリメントカラムは、内部的にはシーケンスによって支えられています
- AUTOINCREMENT/IDENTITY を持つカラムを削除すると、関連付けられたシーケンスも削除されます
- 挿入時に明示的な値が指定されない場合、次の値が自動的に生成されます
- `AUTOINCREMENT` と `IDENTITY` は同義語であり、動作は同一です

**例:**

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

## 計算カラム {#computed-columns}

計算カラムは、スカラー式を使用して他のカラムから生成されます。{{{ .lake }}} は次の 2 種類をサポートしています。

- **STORED**: 値は物理的に保存され、依存するカラムが変更されると自動的に更新されます
- **VIRTUAL**: 値はクエリ実行時にその場で計算されるため、ストレージ容量を節約できます

**構文:**

```sql
<column_name> <data_type> [ NOT NULL | NULL ] AS (<expr>) { STORED | VIRTUAL }
<column_name> <data_type> [ NOT NULL | NULL ] GENERATED ALWAYS AS (<expr>) { STORED | VIRTUAL }
```

**例:**

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
> パフォーマンスが重要で、頻繁にクエリされるカラムには **STORED** を選択してください。計算コストを許容でき、ストレージ容量を節約したい場合は **VIRTUAL** を選択してください。

## MySQL 互換性 {#mysql-compatibility}

{{{ .lake }}} の構文は、主にデータ型と一部の特定のインデックスヒントにおいて MySQL と異なります。

MySQL とは異なり、{{{ .lake }}} はデフォルトで PostgreSQL スタイルの識別子の大文字・小文字規則に従います。引用符で囲まれていないカラム名は小文字に変換され、二重引用符で囲まれた名前は大文字・小文字が保持され、大文字・小文字が区別されます。その結果、引用符付きで大文字・小文字を保持したカラム名（たとえば `"Employee_ID"`）で作成されたテーブルは、`SELECT *` では行を返せても、`SELECT Employee_ID` や `SELECT employee_id` では失敗することがあります。識別子の大文字・小文字規則、関連設定、トラブルシューティングの詳細については、[SQL 識別子](/tidb-cloud-lake/sql/sql-identifiers.md#identifier-casing-rules) を参照してください。

## アクセス制御要件 {#access-control-requirements}

| 権限 | オブジェクトタイプ | 説明 |
|:----------|:--------------|:-----------------------|
| CREATE    | グローバル、テーブル | テーブルを作成します。       |

テーブルを作成するには、操作を実行するユーザー、または [current_role](/tidb-cloud-lake/guides/roles.md) に CREATE [権限](/tidb-cloud-lake/guides/privileges.md#table-privileges) が必要です。

## 例 {#examples}

### テーブルを作成する {#create-table}

カラムにデフォルト値を持つテーブルを作成します（この例では、`genre` カラムのデフォルト値は 'General' です）。

```sql
CREATE TABLE books (
    id BIGINT UNSIGNED,
    title VARCHAR,
    genre VARCHAR DEFAULT 'General'
);
```

テーブルの構造と `genre` カラムのデフォルト値を確認するために、テーブルの情報を表示します。

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

`genre` を指定せずに 1 行挿入します。

```sql
INSERT INTO books(id, title) VALUES(1, 'Invisible Stars');
```

テーブルをクエリすると、`genre` カラムにデフォルト値 'General' が設定されていることがわかります。

```sql
SELECT * FROM books;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### Create Table ... Like {#create-table-like}

既存のテーブル (`books`) と同じ構造を持つ新しいテーブル (`books_copy`) を作成します。

```sql
CREATE TABLE books_copy LIKE books;
```

新しいテーブルの構造を確認します。

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

新しいテーブルに 1 行挿入すると、`genre` カラムのデフォルト値もコピーされていることがわかります。

```sql
INSERT INTO books_copy(id, title) VALUES(1, 'Invisible Stars');

SELECT * FROM books_copy;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### Create Table ... As {#create-table-as}

既存のテーブル (`books`) のデータを含む新しいテーブル (`books_backup`) を作成します。

```sql
CREATE TABLE books_backup AS SELECT * FROM books;
```

新しいテーブルの情報を表示すると、`genre` カラムのデフォルト値がコピーされて**いない**ことがわかります。

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

新しいテーブルをクエリすると、元のテーブルのデータがコピーされていることがわかります。

```sql
SELECT * FROM books_backup;
+----+----------------+---------+
| id | title          | genre   |
+----+----------------+---------+
|  1 | Invisible Stars| General |
+----+----------------+---------+
```

### Create Table ... Column As STORED | VIRTUAL {#create-table-column-as-stored-virtual}

次の例は、"price" または "quantity" カラムの更新に基づいて自動的に再計算される、stored 計算カラムを持つテーブルを示しています。

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

この例では、JSON データを保存するために、profile という名前の Variant 型カラムを持つ student_profiles というテーブルを作成しています。また、profile カラムから age プロパティを抽出して整数にキャストする、_age_ という名前の virtual 計算カラムも追加しています。

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
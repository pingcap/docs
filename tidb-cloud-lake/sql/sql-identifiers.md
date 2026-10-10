---
title: SQL 識別子
summary: SQL 識別子は、テーブル、ビュー、データベースなど、{{{ .lake }}} 内のさまざまな要素に使用される名前です。
---

# SQL 識別子

SQL 識別子は、テーブル、ビュー、データベースなど、{{{ .lake }}} 内のさまざまな要素に使用される名前です。

## クォートなし識別子と二重引用符付き識別子 {#unquoted-double-quoted-identifiers}

クォートなし識別子は、文字 (A-Z, a-z) またはアンダースコア (`_`) で始まり、文字、アンダースコア、数字 (0-9)、またはドル記号 (`$`) で構成できます。

```text title='Examples:'
mydatalake
MyDatalake1
My$datalake
_my_datalake
```

二重引用符付き識別子には、数字 (0-9)、特殊文字（ピリオド (.)、シングルクォート ('), 感嘆符 (!), アットマーク (@), 番号記号 (#), ドル記号 ($), パーセント記号 (%), キャレット (^), アンパサンド (&) など）、拡張 ASCII および非 ASCII 文字、さらに空白文字を含めることができます。

```text title='Examples:'
"MyDatalake"
"my.datalake"
"my datalake"
"My 'Datalake'"
"1_datalake"
"$Datalake"
```

二重バッククォート (``) と二重引用符 (`"`) の使用は同等であることに注意してください。

```text title='Examples:'
`MyDatalake`
`my.datalake`
`my datalake`
`My 'Datalake'`
`1_datalake`
`$Datalake`
```

## 識別子の大文字・小文字ルール {#identifier-casing-rules}

{{{ .lake }}} は、デフォルトでクォートなし識別子を小文字で保存し、二重引用符付き識別子は入力されたとおりに保存します。言い換えると、{{{ .lake }}} はデータベース、テーブル、カラムなどのオブジェクト名を大文字・小文字を区別しないものとして扱います。これらを大文字・小文字を区別するものとして扱いたい場合は、二重引用符で囲んでください。

> **Note:**
>
> デフォルトでは、{{{ .lake }}} は PostgreSQL スタイルの識別子の大文字・小文字規則に従います。クォートなし識別子は小文字に正規化され、二重引用符付き識別子は元の大文字・小文字を保持し、大文字・小文字を区別します。この動作は次の 2 つの設定で制御されます。
>
> - `unquoted_ident_case_sensitive`: デフォルトは `0` で、クォートなし識別子は大文字・小文字を区別せず、小文字に正規化されます。`1` に設定すると、クォートなし識別子の大文字・小文字が保持され、大文字・小文字を区別するようになります。
> - `quoted_ident_case_sensitive`: デフォルトは `1` で、二重引用符付き識別子は文字の大文字・小文字を保持し、大文字・小文字を区別します。`0` に設定すると、二重引用符付き識別子は大文字・小文字を区別しなくなります。
>
> クォートの有無にかかわらず識別子を大文字・小文字を区別しないものとして扱う MySQL スタイルの動作を使用したい場合は、`unquoted_ident_case_sensitive` と `quoted_ident_case_sensitive` の両方を `0` に設定してください。

### `SELECT *` は動作するのに `SELECT <column>` が失敗する理由 {#why-select-works-but-select-fails}

よくある混乱の原因として、カラムが大文字・小文字を保持するクォート（二重引用符またはバッククォート）付きで作成されたテーブルがあります。たとえば `"Employee_ID"` のような場合です。デフォルト設定では、`SELECT *` はデータを返しますが、カラム名を指定して参照すると、大文字・小文字をどう書いても失敗します。

```sql
-- Columns created with the case preserved
CREATE TABLE xxxTable ("Employee_ID" INT, "Department" VARCHAR);
INSERT INTO xxxTable VALUES (1, 'Eng');

-- Works: no column is referenced by name
SELECT * FROM xxxTable;

-- Fails: unquoted names are folded to lowercase (employee_id / department),
-- which do not match the stored "Employee_ID" / "Department"
SELECT Employee_ID FROM xxxTable;
SELECT employee_id FROM xxxTable;

-- Works: double quotes preserve the case and match the stored column name
SELECT "Employee_ID" FROM xxxTable;
```

これは、`unquoted_ident_case_sensitive` のデフォルト値が `0` であるため、`Employee_ID` と `employee_id` の両方が `employee_id` として解決され、存在しない名前として扱われるためです。実際のカラムの大文字・小文字を確認するには、`DESC xxxTable;` または `SHOW CREATE TABLE xxxTable;` を実行してください。

これを避けるには、作成時と完全に同じ大文字・小文字で二重引用符を使ってカラムを参照するか、より望ましい方法として、データベース、テーブル、カラムの作成時には小文字、数字、アンダースコアのみを使用し（クォートは使わない）、命名してください。

次の例は、データベースの作成と一覧表示において、{{{ .lake }}} が識別子の大文字・小文字をどのように扱うかを示しています。

```sql
-- Create a database named "datalake"
CREATE DATABASE datalake;

-- Attempt to create a database named "Datalake"
CREATE DATABASE Datalake;

>> SQL Error [1105] [HY000]: DatabaseAlreadyExists. Code: 2301, Text = Database 'datalake' already exists.

-- Create a database named "Datalake"
CREATE DATABASE "Datalake";

-- List all databases
SHOW DATABASES;

databases_in_default|
--------------------+
Datalake            |
datalake            |
default             |
information_schema  |
system              |
```

この例は、テーブル名とカラム名に対して {{{ .lake }}} が識別子の大文字・小文字をどのように扱うかを示しており、デフォルトでの大文字・小文字の区別と、異なる大文字・小文字の識別子を区別するための二重引用符の使用を強調しています。

```sql
-- Create a table named "datalake"
CREATE TABLE datalake (a INT);
DESC datalake;

Field|Type|Null|Default|Extra|
-----+----+----+-------+-----+
a    |INT |YES |NULL   |     |

-- Attempt to create a table named "Datalake"
CREATE TABLE Datalake (a INT);

>> SQL Error [1105] [HY000]: TableAlreadyExists. Code: 2302, Text = Table 'datalake' already exists.

-- Attempt to create a table with one column named "a" and the other one named "A"
CREATE TABLE "Datalake" (a INT, A INT);

>> SQL Error [1105] [HY000]: BadArguments. Code: 1006, Text = Duplicated column name: a.

-- Double quote the column names
CREATE TABLE "Datalake" ("a" INT, "A" INT);
DESC "Datalake";

Field|Type|Null|Default|Extra|
-----+----+----+-------+-----+
a    |INT |YES |NULL   |     |
A    |INT |YES |NULL   |     |
```

## 文字列識別子 {#string-identifiers}

{{{ .lake }}} では、テキストや日付のような文字列項目を扱う際、標準的な方法としてシングルクォート (`'`) で囲む必要があります。

```sql
INSERT INTO weather VALUES ('San Francisco', 46, 50, 0.25, '1994-11-27');

SELECT 'Datalake';

'datalake'|
----------+
Datalake  |

SELECT "Datalake";

>> SQL Error [1105] [HY000]: SemanticError. Code: 1065, Text = error:
  --> SQL:1:73
  |
1 | /* ApplicationName=DBeaver 23.2.0 - SQLEditor <Script-12.sql> */ SELECT "Datalake"
  |                                                                         ^^^^^^^^^^ column Datalake doesn't exist, do you mean 'Datalake'?
```

デフォルトでは、{{{ .lake }}} の SQL dialect は `PostgreSQL` です。

```sql
SHOW SETTINGS LIKE '%sql_dialect%';

name       |value     |default   |level  |description                                                                      |type  |
-----------+----------+----------+-------+---------------------------------------------------------------------------------+------+
sql_dialect|PostgreSQL|PostgreSQL|SESSION|Sets the SQL dialect. Available values include "PostgreSQL", "MySQL", and "Hive".|String|
```

二重引用符 (`"`) を有効にするには、これを `MySQL` に変更できます。

```sql
SET sql_dialect='MySQL';

SELECT "demo";
+--------+
| 'demo' |
+--------+
| demo   |
+--------+
```
---
title: 字符集与排序规则
summary: 了解 TiDB 支持的字符集和排序规则。
---

# 字符集与排序规则

本文介绍了 TiDB 支持的字符集和排序规则。

## 概念

字符集是符号和编码的集合。TiDB 中的默认字符集是 `utf8mb4`，与 MySQL 8.0 及之后版本的默认字符集一致。

排序规则是一组用于比较字符的规则，以及字符的排序顺序。例如，在二进制排序规则中，`A` 和 `a` 不被视为相等：

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_bin;
SELECT 'A' = 'a';
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
SELECT 'A' = 'a';
```

```sql
SELECT 'A' = 'a';
```

```sql
+-----------+
| 'A' = 'a' |
+-----------+
|         0 |
+-----------+
1 行结果（0.00 秒）
```

```sql
SET NAMES utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
查询成功，影响行数：0（0.00 秒）
```

```sql
SELECT 'A' = 'a';
```

```sql
+-----------+
| 'A' = 'a' |
+-----------+
|         1 |
+-----------+
1 行结果（0.00 秒）
```

以下示例演示了不同 Unicode 排序规则如何比较德语字符 `ß` 和 `ss`。可以看到，只有更严格的 Unicode 排序规则会将它们视为相等，返回 `1`（表示 TRUE）：

```sql
SELECT
  'ss' COLLATE utf8mb4_general_ci = 'ß',
  'ss' COLLATE utf8mb4_unicode_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_ai_ci = 'ß',
  'ss' COLLATE utf8mb4_0900_bin = 'ß'
\G
```

```
*************************** 1. 行 ***************************
'ss' COLLATE utf8mb4_general_ci = 'ß': 0
'ss' COLLATE utf8mb4_unicode_ci = 'ß': 1
'ss' COLLATE utf8mb4_0900_ai_ci = 'ß': 1
  'ss' COLLATE utf8mb4_0900_bin = 'ß': 0
1 行结果（0.01 秒）
```

### 字符集和排序规则命名

一个字符集可以有多个排序规则，命名格式为 `<character_set>_<collation_properties>`。例如，`utf8mb4` 字符集有一个排序规则叫 `utf8mb4_bin`，这是 `utf8mb4` 的二进制排序规则。多个排序规则属性可以用下划线 `_` 分隔。

下表列出了常见的排序规则属性及其含义。

| 排序规则属性 | 含义 |
|---|---|
| `_bin` | 二进制 |
| `_ci` | 不区分大小写 |
| `_ai_ci` | 不区分重音符号，大小写不敏感 |
| `_0900_bin` | Unicode UCA 9.0.0，二进制 |
| `_unicode_ci` | （较旧）Unicode UCA 排序规则，大小写不敏感 |
| `_general_ci` | 较宽松的 Unicode 排序规则，大小写不敏感 |

## TiDB 支持的字符集和排序规则

目前，TiDB 支持以下字符集：

```sql
SHOW CHARACTER SET;
```

```sql
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| ascii   | US ASCII                            | ascii_bin         |      1 |
| binary  | 二进制                              | binary            |      1 |
| gbk     | 中文内码规范                        | gbk_chinese_ci    |      2 |
| latin1  | Latin1                              | latin1_bin        |      1 |
| utf8    | UTF-8 Unicode                        | utf8_bin          |      3 |
| utf8mb4 | UTF-8 Unicode                        | utf8mb4_bin       |      4 |
+---------+-------------------------------------+-------------------+--------+
```

TiDB 支持以下排序规则：

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | 是      | 是       |       1 | PAD SPACE     |
| binary             | binary  |  63 | 是      | 是       |       1 | NO PAD        |
| gbk_bin            | gbk     |  87 |         | 是       |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | 是      | 是       |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | 是      | 是       |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | 是      | 是       |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | 是       |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | 是       |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | 是       |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | 是       |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | 是      | 是       |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | 是       |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | 是       |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
```

> **Warning:**
>
> TiDB 错误地将 latin1 视为 utf8 的子集。这可能导致存储 latin1 和 utf8 编码字符时出现意外行为。强烈建议使用 utf8mb4 字符集。详见 [TiDB #18955](https://github.com/pingcap/tidb/issues/18955)。

> **Note:**
>
> TiDB 中的默认排序规则（二进制排序，后缀 `_bin`）与 [MySQL 中的默认排序规则](https://dev.mysql.com/doc/refman/8.0/en/charset-charsets.html)（通常是 general 排序，后缀 `_general_ci` 或 `_ai_ci`）不同。这可能导致在指定字符集但依赖隐式默认排序规则时出现不兼容行为。
>
> 不过，TiDB 的默认排序规则也会受到客户端的 [connection collation](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables) 设置的影响。例如，MySQL 8.x 客户端默认将 `utf8mb4` 的连接排序规则设置为 `utf8mb4_0900_ai_ci`。
>
> - 在 TiDB v7.4.0 之前，如果你的客户端使用 `utf8mb4_0900_ai_ci` 作为 [connection collation](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，TiDB 会回退使用服务器默认排序规则 `utf8mb4_bin`，因为 TiDB 不支持 `utf8mb4_0900_ai_ci` 排序规则。
> - 从 v7.4.0 开始，如果你的客户端使用 `utf8mb4_0900_ai_ci` 作为 [connection collation](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html#charset-connection-system-variables)，TiDB 会遵循客户端配置，使用 `utf8mb4_0900_ai_ci` 作为默认排序规则。

你可以使用以下语句查看对应字符集的排序规则（在 [新排序规则框架](#new-framework-for-collations) 下）：

```sql
SHOW COLLATION WHERE Charset = 'utf8mb4';
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | 是       |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | 是       |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | 是      | 是       |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | 是       |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | 是       |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
```

关于 TiDB 对 GBK 字符集的支持详情，请参见 [GBK](/character-set-gbk.md)。

## TiDB 中的 `utf8` 和 `utf8mb4`

在 MySQL 中，字符集 `utf8` 限制为最多三字节。这足以存储基本多语言平面（BMP）中的字符，但不足以存储如表情符号等字符。建议在新安装时使用 `utf8mb4`，并迁移 away from `utf8`。

在 MySQL 和 TiDB 中，`utf8` 和 `utf8mb3` 是同一字符集的别名。

默认情况下，TiDB 也将 `utf8` 限制为最多三字节，以确保在 TiDB 中创建的数据可以安全地在 MySQL 中还原。你可以通过修改系统变量 [`tidb_check_mb4_value_in_utf8`](/system-variables.md#tidb_check_mb4_value_in_utf8) 为 `OFF` 来禁用此限制。但强烈建议使用 `utf8mb4`，以获得完整的 Unicode 支持和更好的兼容性。

以下示例演示在表中插入 4 字节表情字符的默认行为。对于 `utf8` 字符集，`INSERT` 语句会失败；而对于 `utf8mb4`，会成功：

```sql
CREATE TABLE utf8_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8;
```

```
查询成功，影响行数：0（0.09 秒）
```

```sql
CREATE TABLE utf8m4_test (
     c char(1) NOT NULL
    ) CHARACTER SET utf8mb4;
```

```
查询成功，影响行数：0（0.09 秒）
```

```sql
INSERT INTO utf8_test VALUES ('😉');
```

```
错误 1366 (HY000): incorrect utf8 value f09f9889(😉) for column c
```

```sql
INSERT INTO utf8m4_test VALUES ('😉');
```

```
查询成功，影响行数：1（0.02 秒）
```

```sql
SELECT char_length(c), length(c), c FROM utf8_test;
```

```
空集（0.01 秒）
```

```sql
SELECT char_length(c), length(c), c FROM utf8m4_test;
```

```
+----------------+-----------+------+
| char_length(c) | length(c) | c    |
+----------------+-----------+------+
|              1 |         4 | 😉     |
+----------------+-----------+------+
1 行结果（0.00 秒）
```

## 不同层级的字符集和排序规则

字符集和排序规则可以在不同层级设置。

### 数据库字符集和排序规则

每个数据库都有字符集和排序规则。可以使用以下语句指定数据库的字符集和排序规则：

```sql
CREATE DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]

ALTER DATABASE db_name
    [[DEFAULT] CHARACTER SET charset_name]
    [[DEFAULT] COLLATE collation_name]
```

此处 `DATABASE` 可替换为 `SCHEMA`。

不同数据库可以使用不同的字符集和排序规则。使用 `character_set_database` 和 `collation_database` 查看当前数据库的字符集和排序规则：

```sql
CREATE SCHEMA test1 CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
查询成功，影响行数：0（0.09 秒）
```

```sql
USE test1;
```

```sql
数据库已切换
```

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| utf8mb4                  | utf8mb4_general_ci   |
+--------------------------|----------------------+
1 行结果（0.00 秒）
```

```sql
CREATE SCHEMA test2 CHARACTER SET latin1 COLLATE latin1_bin;
```

```sql
查询成功，影响行数：0（0.09 秒）
```

```sql
USE test2;
```

```sql
数据库已切换
```

```sql
SELECT @@character_set_database, @@collation_database;
```

```sql
+--------------------------|----------------------+
| @@character_set_database | @@collation_database |
+--------------------------|----------------------+
| latin1                   | latin1_bin           |
+--------------------------|----------------------+
1 行结果（0.00 秒）
```

你也可以在 `INFORMATION_SCHEMA` 中看到这两个值：

```sql
SELECT DEFAULT_CHARACTER_SET_NAME, DEFAULT_COLLATION_NAME
FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'db_name';
```

### 表字符集和排序规则

可以使用以下语句为表指定字符集和排序规则：

```sql
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
```

例如：

```sql
CREATE TABLE t1(a int) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

```sql
查询成功，影响行数：0（0.08 秒）
```

如果未指定表的字符集和排序规则，则使用数据库的默认值。如果只指定字符集为 `utf8mb4`，未指定排序规则，则排序规则由系统变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4-new-in-v740) 决定。

### 字段字符集和排序规则

可以使用以下语句为字段指定字符集和排序规则：

```sql
col_name {CHAR | VARCHAR | TEXT} (col_length)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]

col_name {ENUM | SET} (val_list)
    [CHARACTER SET charset_name]
    [COLLATE collation_name]
```

如果未指定字段的字符集和排序规则，则使用表的默认值。如果只指定字符集为 `utf8mb4`，未指定排序规则，则由系统变量 [`default_collation_for_utf8mb4`](/system-variables.md#default_collation_for_utf8mb4) 决定。

### 字符串的字符集和排序规则

每个字符串对应一个字符集和排序规则。当你使用字符串时，可以使用以下语法：

```sql
[_charset_name]'string' [COLLATE collation_name]
```

示例：

```sql
SELECT 'string';
SELECT _utf8mb4'string';
SELECT _utf8mb4'string' COLLATE utf8mb4_general_ci;
```

规则说明：

+ 规则 1：如果你指定 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用对应的字符集和排序规则。
+ 规则 2：如果你只指定 `CHARACTER SET charset_name`，未指定 `COLLATE collation_name`，则使用 `charset_name` 的字符集和其默认排序规则。
+ 规则 3：如果既未指定 `CHARACTER SET` 也未指定 `COLLATE`，则使用系统变量 `character_set_connection` 和 `collation_connection` 所定义的字符集和排序规则。

### 客户端连接的字符集和排序规则

+ 服务器的字符集和排序规则为系统变量 `character_set_server` 和 `collation_server` 的值。

+ 默认数据库的字符集和排序规则为系统变量 `character_set_database` 和 `collation_database` 的值。

你可以使用 `character_set_connection` 和 `collation_connection` 来为每个连接设置字符集和排序规则。`character_set_client` 变量用于设置客户端字符集。

在返回结果之前，系统变量 `character_set_results` 指示服务器返回查询结果给客户端时所用的字符集，包括结果的元数据。

你可以使用以下语句设置与客户端相关的字符集和排序规则：

+ `SET NAMES 'charset_name' [COLLATE 'collation_name']`

    `SET NAMES` 表示客户端用来向服务器发送 SQL 语句的字符集。`SET NAMES utf8mb4` 表示所有来自客户端的请求以及服务器返回的结果都使用 utf8mb4。

    `SET NAMES 'charset_name'` 等价于以下组合语句：

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection = charset_name;
    ```

    `COLLATE` 为可选项，若省略，则使用 `charset_name` 的默认排序规则设置 `collation_connection`。

+ `SET CHARACTER SET 'charset_name'`

    类似于 `SET NAMES`，`SET CHARACTER SET 'charset_name'` 等价于：

    ```sql
    SET character_set_client = charset_name;
    SET character_set_results = charset_name;
    SET character_set_connection=@@character_set_database;
    SET collation_connection = @@collation_database;
    ```

## 字符集和排序规则的选择优先级

String > Column > Table > Database > Server

## 选择字符集和排序规则的通用规则

+ 规则 1：如果你指定 `CHARACTER SET charset_name` 和 `COLLATE collation_name`，则直接使用对应的字符集和排序规则。
+ 规则 2：如果你只指定 `CHARACTER SET charset_name`，未指定 `COLLATE collation_name`，则使用 `charset_name` 的字符集和其默认排序规则。
+ 规则 3：如果既未指定 `CHARACTER SET` 也未指定 `COLLATE`，则使用排序规则优先级更高的字符集和排序规则。

## 字符有效性检查

如果指定的字符集为 `utf8` 或 `utf8mb4`，TiDB 仅支持有效的 `utf8` 字符。对于无效字符，TiDB 会报错 `incorrect utf8 value`。TiDB 中的字符有效性检查与 MySQL 8.0 兼容，但与 MySQL 5.7 及早期版本不兼容。

若要禁用此错误检测，可使用 `set @@tidb_skip_utf8_check=1;` 跳过字符检查。

> **Note:**
>
> 若跳过字符检查，TiDB 可能无法检测应用写入的非法 UTF-8 字符，执行 `ANALYZE` 时可能导致解码错误，并引入其他未知编码问题。如果你的应用无法保证写入字符串的有效性，不建议跳过字符检查。

## 排序规则支持框架

<CustomContent platform="tidb">

排序规则的语法支持和语义支持受到 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 配置项的影响。前者表示 TiDB 能解析和设置排序规则，后者表示 TiDB 能正确使用排序规则进行字符串比较。

</CustomContent>

在 v4.0 之前，TiDB 仅提供 [旧排序规则框架](#old-framework-for-collations)。在此框架下，TiDB 支持大部分 MySQL 排序规则的语法解析，但语义上将所有排序规则视为二进制排序。

自 v4.0 起，TiDB 支持 [新排序规则框架](#new-framework-for-collations)。在此框架下，TiDB 语义解析不同的排序规则，并在比较字符串时严格遵循排序规则。

### 旧排序规则框架

在 v4.0 之前，你可以在 TiDB 中指定大部分 MySQL 排序规则，这些排序规则按照默认排序规则处理，即字节顺序决定字符顺序。不同于 MySQL，TiDB 不处理字符末尾的空格，这导致以下行为差异：

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
查询成功，无影响行数
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
查询成功，影响行数：1
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
查询成功，影响行数：1
```

在 TiDB 中，上述语句执行成功。而在 MySQL 中，由于 `utf8mb4_general_ci` 是不区分大小写的，会报 `Duplicate entry 'a'` 错误。

```sql
INSERT INTO t1 VALUES ('a ');
```

```sql
查询成功，影响行数：1
```

在 TiDB 中，上述语句执行成功。而在 MySQL 中，由于比较是在填充空格后进行，会返回 `Duplicate entry 'a '` 错误。

### 新排序规则框架

自 TiDB v4.0 起，引入完整的排序规则框架。

<CustomContent platform="tidb">

此新框架支持语义解析排序规则，并引入 `new_collations_enabled_on_first_bootstrap` 配置项，用于决定在集群首次初始化时是否启用新框架。若要启用新框架，将 `new_collations_enabled_on_first_bootstrap` 设置为 `true`。详情请参见 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap)。

对于已初始化的 TiDB 集群，可以通过 `mysql.tidb` 表中的 `new_collation_enabled` 变量检查是否启用新排序规则：

> **Note:**
>
> 如果 `mysql.tidb` 表的查询结果与 `new_collations_enabled_on_first_bootstrap` 的值不同，则表中的结果为实际值。

```sql
SELECT VARIABLE_VALUE FROM mysql.tidb WHERE VARIABLE_NAME='new_collation_enabled';
```

```sql
+----------------+
| VARIABLE_VALUE |
+----------------+
| True           |
+----------------+
1 行结果（0.00 秒）
```

</CustomContent>

<CustomContent platform="tidb-cloud">

此新框架支持语义解析排序规则。TiDB 在集群首次初始化时默认启用新框架。

</CustomContent>

在新框架下，TiDB 支持 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_bin`、`utf8mb4_0900_ai_ci`、`gbk_chinese_ci` 和 `gbk_bin` 排序规则，与 MySQL 兼容。

当使用 `utf8_general_ci`、`utf8mb4_general_ci`、`utf8_unicode_ci`、`utf8mb4_unicode_ci`、`utf8mb4_0900_ai_ci` 和 `gbk_chinese_ci` 时，字符串比较为不区分大小写和不区分重音符号。同时，TiDB 也修正了排序规则的 `PADDING` 行为：

```sql
CREATE TABLE t(a varchar(20) charset utf8mb4 collate utf8mb4_general_ci PRIMARY KEY);
```

```sql
查询成功，影响行数：0（0.00 秒）
```

```sql
INSERT INTO t VALUES ('A');
```

```sql
查询成功，影响行数：1（0.00 秒）
```

```sql
INSERT INTO t VALUES ('a');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a' for key 't.PRIMARY' -- TiDB 兼容 MySQL 的不区分大小写排序规则。
```

```sql
INSERT INTO t VALUES ('a ');
```

```sql
ERROR 1062 (23000): Duplicate entry 'a ' for key 't.PRIMARY' -- TiDB 修改了 `PADDING` 行为以兼容 MySQL。
```

> **Note:**
>
> TiDB 中的 padding 实现方式与 MySQL 不同。在 MySQL 中，padding 通过填充空格实现；在 TiDB 中，padding 通过裁剪末尾空格实现。两者在大多数情况下效果相同，唯一例外是在字符串末尾包含小于空格（0x20）字符时。例如，`'a' < 'a\t'` 在 TiDB 中结果为 `1`，而在 MySQL 中，`'a' < 'a\t'` 等价于 `'a ' < 'a\t'`，结果为 `0`。

## 表达式中排序规则的 Coercibility 值

如果一个表达式涉及多个不同排序规则的子句，则需要推断所用的排序规则。规则如下：

+ 显式 `COLLATE` 子句的 coercibility 值为 `0`。
+ 如果两个字符串的排序规则不兼容，则两个不同排序规则的字符串拼接的 coercibility 值为 `1`。
+ 字段、`CAST()`、`CONVERT()` 或 `BINARY()` 的排序规则 coercibility 值为 `2`。
+ 系统常量（由 `USER()` 或 `VERSION()` 返回的字符串） coercibility 值为 `3`。
+ 常量的 coercibility 值为 `4`。
+ 数字或中间变量的 coercibility 值为 `5`。
+ `NULL` 或由 `NULL` 派生的表达式的 coercibility 值为 `6`。

在推断排序规则时，TiDB 优先使用 coercibility 值较低的表达式的排序规则。如果两个子句的 coercibility 值相同，则根据以下优先级确定排序规则：

binary > utf8mb4_bin > (utf8mb4_general_ci = utf8mb4_unicode_ci) > utf8_bin > (utf8_general_ci = utf8_unicode_ci) > latin1_bin > ascii_bin

TiDB 在以下情况下无法推断排序规则，并会报错：

- 两个子句的排序规则不同，且 coercibility 值均为 `0`。
- 两个子句的排序规则不兼容，且表达式的返回类型为 `String`。

## `COLLATE` 子句

TiDB 支持使用 `COLLATE` 子句指定表达式的排序规则。此表达式的 coercibility 值为 `0`，优先级最高。示例：

```sql
SELECT 'a' = _utf8mb4 'A' collate utf8mb4_general_ci;
```

```sql
+-----------------------------------------------+
| 'a' = _utf8mb4 'A' collate utf8mb4_general_ci |
+-----------------------------------------------+
|                                             1 |
+-----------------------------------------------+
1 行结果（0.00 秒）
```

更多详情请参见 [Connection Character Sets and Collations](https://dev.mysql.com/doc/refman/8.0/en/charset-connection.html)。
---
title: Schema Object Names
summary: Learn about schema object names in TiDB SQL statements.
---

# スキーマオブジェクト名 {#schema-object-names}

<!-- markdownlint-disable MD038 -->

このドキュメントでは、TiDBSQLステートメントのスキーマオブジェクト名を紹介します。

スキーマオブジェクト名は、データベース、テーブル、インデックス、列、エイリアスなど、TiDB内のすべてのスキーマオブジェクトに名前を付けるために使用されます。 SQLステートメントの識別子を使用してこれらのオブジェクトを引用できます。

バックティックを使用して識別子を囲むことができます。たとえば、 `SELECT * FROM t`は`` SELECT * FROM `t` ``と書くこともできます。ただし、識別子に1つ以上の特殊文字が含まれている場合、または予約済みキーワードである場合は、識別子が表すスキーマオブジェクトを引用するために、バッククォートで囲む必要があります。

{{< copyable "" >}}

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

SQLモードで`ANSI_QUOTES`を設定すると、TiDBは二重引用符`"`で囲まれた文字列を識別子として認識します。

{{< copyable "" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))"
```

{{< copyable "" >}}

```sql
SET SESSION sql_mode='ANSI_QUOTES';
```

```sql
Query OK, 0 rows affected (0.000 sec)
```

{{< copyable "" >}}

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
Query OK, 0 rows affected (0.012 sec)
```

引用符で囲まれた識別子にバックティック文字を使用する場合は、バックティックを2回繰り返します。たとえば、テーブルa`bを作成するには：

{{< copyable "" >}}

```sql
CREATE TABLE `a``b` (a int);
```

`SELECT`ステートメントでは、識別子または文字列を使用してエイリアスを指定できます。

{{< copyable "" >}}

```sql
SELECT 1 AS `identifier`, 2 AS 'string';
```

```sql
+------------+--------+
| identifier | string |
+------------+--------+
|          1 |      2 |
+------------+--------+
1 row in set (0.00 sec)
```

詳細については、 [MySQLスキーマオブジェクト名](https://dev.mysql.com/doc/refman/5.7/en/identifiers.html)を参照してください。

## 識別子修飾子 {#identifier-qualifiers}

オブジェクト名は、修飾されていない場合と修飾されている場合があります。たとえば、次のステートメントは、修飾名のないテーブルを作成します。

{{< copyable "" >}}

```sql
CREATE TABLE t (i int);
```

`USE`ステートメントまたは接続パラメーターを使用してデータベースを構成していない場合は、 `ERROR 1046 (3D000): No database selected`エラーが表示されます。このとき、データベース修飾名を指定できます。

{{< copyable "" >}}

```sql
CREATE TABLE test.t (i int);
```

空白は`.`の周りに存在できます。 `table_name.col_name`と`table_name . col_name`は同等です。

この識別子を引用するには、次を使用します。

{{< copyable "" >}}

```sql
`table_name`.`col_name`
```

それ以外の：

```sql
`table_name.col_name`
```

詳細については、 [MySQL識別子修飾子](https://dev.mysql.com/doc/refman/5.7/en/identifier-qualifiers.html)を参照してください。

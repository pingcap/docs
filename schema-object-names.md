---
title: Schema Object Names
summary: TiDB SQLステートメントのスキーマ オブジェクト名について学習します。
---

# Schema Object Names {#schema-object-names}

<!-- markdownlint-disable MD038 -->

このドキュメントでは、TiDB SQLステートメントのスキーマ オブジェクト名について説明します。

スキーマオブジェクト名は、データベース、テーブル、インデックス、列、エイリアスなど、TiDB内のすべてのスキーマオブジェクトの名前として使用されます。SQL文では、識別子を使用してこれらのオブジェクトを引用符で囲むことができます。

識別子をバッククォートで囲むことができます。例えば、 `SELECT * FROM t` `` SELECT * FROM `t` ``と表記することもできます。ただし、識別子に特殊文字が1つ以上含まれている場合、または予約語である場合は、それが表すスキーマオブジェクトを引用符で囲むために、バッククォートで囲む必要があります。

```sql
SELECT * FROM `table` WHERE `table`.id = 20;
```

SQL MODE に`ANSI_QUOTES`設定すると、TiDB は二重引用符`"`で囲まれた文字列を識別子として認識します。

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
ERROR 1064 (42000): You have an error in your SQL syntax; check the manual that corresponds to your TiDB version for the right syntax to use line 1 column 19 near ""test" (a varchar(10))" 
```

```sql
SET SESSION sql_mode='ANSI_QUOTES';
```

```sql
Query OK, 0 rows affected (0.000 sec)
```

```sql
CREATE TABLE "test" (a varchar(10));
```

```sql
Query OK, 0 rows affected (0.012 sec)
```

引用符で囲まれた識別子でバッククォート文字を使用する場合は、バッククォートを2回繰り返します。例えば、テーブル a`b を作成するには、次のようにします。

```sql
CREATE TABLE `a``b` (a int);
```

In a `SELECT` statement, you can use an identifier or a string to specify an alias:

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

詳細については[MySQLスキーマオブジェクト名](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html)参照してください。

## 識別子修飾子 {#identifier-qualifiers}

オブジェクト名は修飾名でも修飾名でも構いません。例えば、次の文は修飾名のないテーブルを作成します。

```sql
CREATE TABLE t (i int);
```

データベースの設定に`USE`ステートメントまたは接続パラメータを使用していない場合、 `ERROR 1046 (3D000): No database selected`エラーが表示されます。この場合、データベース修飾名を指定できます。

```sql
CREATE TABLE test.t (i int);
```

`.`周囲に空白が存在できます`table_name.col_name`と`table_name . col_name`同等です。

この識別子を引用するには、次のようにします。

```sql
`table_name`.`col_name`
```

の代わりに：

```sql
`table_name.col_name`
```

詳細については[MySQL 識別子修飾子](https://dev.mysql.com/doc/refman/8.0/en/identifier-qualifiers.html)参照してください。

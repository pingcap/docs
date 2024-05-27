---
title: Schema Object Names
summary: TiDB SQLステートメントのスキーマ オブジェクト名について学習します。
---

# スキーマオブジェクト名 {#schema-object-names}

<!-- markdownlint-disable MD038 -->

このドキュメントでは、 TiDB SQLステートメントのスキーマ オブジェクト名について説明します。

スキーマ オブジェクト名は、データベース、テーブル、インデックス、列、エイリアスなど、TiDB 内のすべてのスキーマ オブジェクトに名前を付けるために使用されます。SQL ステートメントでは、識別子を使用してこれらのオブジェクトを引用符で囲むことができます。

バックティックを使用して識別子を囲むことができます。たとえば、 `SELECT * FROM t` `` SELECT * FROM `t` ``と記述することもできます。ただし、識別子に 1 つ以上の特殊文字が含まれている場合、または識別子が予約キーワードである場合は、それが表すスキーマ オブジェクトを引用するためにバックティックで囲む必要があります。

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

引用符で囲まれた識別子でバックティック文字を使用する場合は、バックティックを 2 回繰り返します。たとえば、テーブル a`b を作成するには、次のようにします。

```sql
CREATE TABLE `a``b` (a int);
```

`SELECT`ステートメントでは、識別子または文字列を使用してエイリアスを指定できます。

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

詳細については[MySQL スキーマ オブジェクト名](https://dev.mysql.com/doc/refman/8.0/en/identifiers.html)参照してください。

## 識別子修飾子 {#identifier-qualifiers}

オブジェクト名は修飾されても修飾されてなくてもかまいません。たとえば、次のステートメントは修飾名のないテーブルを作成します。

```sql
CREATE TABLE t (i int);
```

データベースを構成するために`USE`ステートメントまたは接続パラメータを使用していない場合、 `ERROR 1046 (3D000): No database selected`エラーが表示されます。この時点で、データベース修飾名を指定できます。

```sql
CREATE TABLE test.t (i int);
```

`.`周りには空白が存在できます。3 `table_name.col_name` `table_name . col_name`同等です。

この識別子を引用するには、次のようにします。

```sql
`table_name`.`col_name`
```

の代わりに：

```sql
`table_name.col_name`
```

詳細については[MySQL 識別子修飾子](https://dev.mysql.com/doc/refman/8.0/en/identifier-qualifiers.html)参照してください。

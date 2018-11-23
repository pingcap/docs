---
title: TiDB Data Manipulation Language
summary: Use DML (Data Manipulation Language) to select, insert, delete and update the data.
category: user guide
---

# TiDB Data Manipulation Language

Data manipulation language (DML) is a family of syntax elements used for selecting, inserting, deleting and updating data in a database. 

## SELECT

`SELECT` is used to retrieve rows selected from one or more tables.

### Syntax

```sql
SELECT
  [ALL | DISTINCT | DISTINCTROW ]
    [HIGH_PRIORITY]
    [STRAIGHT_JOIN]
    [SQL_CACHE | SQL_NO_CACHE] [SQL_CALC_FOUND_ROWS]
  select_expr [, select_expr ...]
  [FROM table_references
  [WHERE where_condition]
  [GROUP BY {col_name | expr | position}
    [ASC | DESC], ...]
  [HAVING where_condition]
  [ORDER BY {col_name | expr | position}
    [ASC | DESC], ...]
  [LIMIT {[offset,] row_count | row_count OFFSET offset}]
  [FOR UPDATE | LOCK IN SHARE MODE]]
```

### Description of the syntax elements

|Syntax Element|Description|
| --------------------- | -------------------------------------------------- |
|`ALL`, `DISTINCT`, `DISTINCTROW` | The `ALL`, `DISTINCT`/`DISTINCTROW` modifiers specify whether duplicate rows should be returned. ALL (the default) specifies that all matching rows should be returned.|
|`HIGH_PRIORITY` | `HIGH_PRIORITY` gives the current statement higher priority than other statements. |
|`SQL_CACHE`, `SQL_NO_CACHE`, `SQL_CALC_FOUND_ROWS` | To guarantee compatibility with MySQL, TiDB parses these three modifiers, but will ignore them.|
| `STRAIGHT_JOIN` | `STRAIGHT_JOIN` forces the optimizer to execute a Join query in the order of the tables used in the `FROM` clause. You can use this syntax to speed up queries execution when the Join order chosen by the optimizer is not good. |
|`select_expr` | Each `select_expr` indicates a column to retrieve. including the column names and expressions. `\*` represents all the columns.|
\|`FROM table_references` | The `FROM table_references` clause indicates the table (such as `(select * from t;)`) , or tables(such as `select * from t1 join t2;)') or even 0 tables (such as `select 1+1 from dual;` (which is equivalent to `select 1+1;')) from which to retrieve rows.|
|`WHERE where_condition` | The `WHERE` clause, if given, indicates the condition or conditions that rows must satisfy to be selected. The result contains only the data that meets the condition(s).|
|`GROUP BY` | The `GROUP BY` statement is used to group the result-set.|
|`HAVING where_condition` |The `HAVING` clause and the `WHERE` clause are both used to filter the results. The `HAVING` clause filters the results of `GROUP BY`, while the `WHERE` clause filter the results before aggregationã|
|`ORDER BY` | The `ORDER BY` clause is used to sort the data in ascending or descending order, based on columns, expressions or items in the `select_expr` list.|
|`LIMIT` | The `LIMIT` clause can be used to constrain the number of rows. `LIMIT` takes one or two numeric arguments. With one argument, the argument specifies the maximum number of rows to return, the first row to return is the first row of the table by default; with two arguments, the first argument specifies the offset of the first row to return, and the second specifies the maximum number of rows to return.|
|`FOR UPDATE` | All the data in the result sets are read-locked, in order to detect the concurrent updates. TiDB uses the [Optimistic Transaction Model](mysql-compatibility.md#transaction). The transaction conflicts are detected in the commit phase instead of statement execution phase. while executing the `SELECT FOR UPDATE` statement, if there are other transactions trying to update relavant data, the `SELECT FOR UPDATE` transaction will fail.|
|`LOCK IN SHARE MODE` | To guarantee compatibility, TiDB parses these three modifiers, but will ignore them.|

## INSERT

`INSERT` inserts new rows into an existing table. TiDB is compatible with all the `INSERT` syntaxes of MySQL.

### Syntax

```sql
  Insert Statement:
  INSERT [LOW_PRIORITY | DELAYED | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    insert_values
    [ON DUPLICATE KEY UPDATE assignment_list]

  insert_values:
    [(col_name [, col_name] ...)]
    {VALUES | VALUE} (expr_list) [, (expr_list)] ...
|     SET assignment_list
|     [(col_name [, col_name] ...)]
    SELECT ...

  expr_list:
    expr [, expr] ...

  assignment:
    col_name = expr

  assignment_list:
    assignment [, assignment] ...
```

### Description of the syntax elements

| Syntax Elements | Description |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | `LOW_PRIORITY` gives the statement lower priority. TiDB lowers the priority of the current statement. |
| `DELAYED` | To guarantee compatibility, TiDB parses this modifier, but will ignore it. |
| `HIGH_PRIORITY` | `HIGH_PRIORITY` gives the current statement higher priority than other statements. TiDB raises the priority of the current statement.|
| `IGNORE` | If `IGNORE` modifier is specified and there is a duplicate key error, the data cannot be inserted without an error.  |
| `tbl_name` | `tbl_name` is the table into which the rows should be inserted.  |
| `insert_values` | The `insert_values` is the value to be inserted. For more information, see [insert_values](#insert_values). |
| `ON DUPLICATE KEY UPDATE assignment_list` | If `ON DUPLICATE KEY UPDATE` is specified, and there is a conflict in a `UNIQUE` index or `PRIMARY` KEY, the data cannot be inserted, instead, the existing row will be updated using `assignment_list`. |

### insert_values

You can use the following ways to specify the data set:

- Value List

  Place the values to be inserted in a Value List.

  ```sql
  CREATE TABLE tbl_name (
     a int,
     b int,
     c int
  );
  INSERT INTO tbl_name VALUES(1,2,3),(4,5,6),(7,8,9);
  ```
     
  In the example above, `(1,2,3),(4,5,6),(7,8,9)` are the Value Lists enclosed within parentheses and separated by commas. Each Values List means a row of data, in this example, 3 rows are inserted. You can also specify the `ColumnName List` to insert rows to some of the columns. 
  and contains exactly as many values as are to be inserted per row.  

  ```sql
  INSERT INTO tbl_name (a,c) VALUES(1,2),(4,5),(7,8);
  ```
  
  In the example above, only the `a` and `c` columns are listed, the the `b` of each row will be set to `Null`.

- Assignment List

  Insert the values by using Assignment Statements, for example:

  ```sql
  INSERT INTO tbl_name a=1, b=2, c=3;
  ```

  In this way, only one row of data can be inserted at a time, and the value of each column needs the assignment statement.

- Select Statement

  The data set to be inserted is obtained using a `SELECT` statement. The column to be inserted into is obtained from the Schema in the `SELECT` statement.
  ```sql
  CREATE TABLE tbl_name1 (
     a int,
     b int,
     c int
  );
  INSERT INTO tbl_name SELECT * from tbl_name1;
  ```
  In the example above, the data is selected from `tal_name1`, and then inserted into `tbl_name`.

## DELETE

`DELETE` is a DML statement that removes rows from a table. TiDB is compatible with all the `DELETE` syntaxes of MySQL except for `PARTITION`. There are two kinds of `DELETE`, [`Single-Table DELETE`](#single-table-delete-syntax) and [`Multiple-Table DELETE`](#multiple-table-delete-syntax).

### Single-Table DELETE syntax

The `Single_Table DELETE` syntax deletes rows from a single table. 

###  DELETE syntax

```sql
DELETE [LOW_PRIORITY] [QUICK] [IGNORE] FROM tbl_name
  [WHERE where_condition]
  [ORDER BY ...]
  [LIMIT row_count]
```

### Multiple-Table DELETE syntax

The `Multiple_Table DELETE` syntax deletes rows of multiple tables, and has the following two kinds of formats:

```sql
DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
  tbl_name[.*] [, tbl_name[.*]] ...
  FROM table_references
  [WHERE where_condition]

DELETE [LOW_PRIORITY] [QUICK] [IGNORE]
  FROM tbl_name[.*] [, tbl_name[.*]] ...
  USING table_references
  [WHERE where_condition]
```

Both of the two syntax formats can be used to delete multiple tables, or delete the selected results from multiple tables. There are still differences between the two formats. The first one will delete data of every table in the table list before `FROM`. The second one will delete the data of the tables in the table list which is after `FROM` and before `USING`.

### Description of the syntax elements

| Syntax Elements | Description|
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | `LOW_PRIORITY` gives the statement lower priority. TiDB lowers the priority of the current statement. |
| `QUICK` | To guarantee compatibility with MySQL, TiDB parses these three modifiers, but will ignore them. |
| `IGNORE` | To guarantee compatibility with MySQL, TiDB parses these three modifiers, but will ignore them.|
| `tbl_name` | the table names to be deleted|
| `WHERE where_condition` | the `Where` expression, which deletes rows that meets the expression |
| `ORDER BY` | To sort the data set which are to be deleted|
| `LIMIT row_count` | the top number of rows to be deleted as specified in`row_count` |

## Update

`UPDATE` is used to update data of the tables.

### Syntax

There are two kinds of `UPDATE` syntax, [Single-table UPDATE](#single-table-update) and [Multi-Table UPDATE](#multi-table-update).

###  Single-table UPDATE

```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_reference
  SET assignment_list
  [WHERE where_condition]
  [ORDER BY ...]
  [LIMIT row_count]

assignment:
  col_name = value

assignment_list:
  assignment [, assignment] ...
```

For the single-table syntax, the `UPDATE` statement updates columns of existing rows in the named table with new values. The `SET assignment_list` clause indicates which columns to modify and the values they should be given. The `WHERE/Orderby/Limit` clause, if given, specifies the conditions that identify which rows to update.

###  Multi-table UPDATE

```sql
UPDATE [LOW_PRIORITY] [IGNORE] table_references
  SET assignment_list
  [WHERE where_condition]
```

For the multiple-table syntax, `UPDATE` updates rows in each table named in `table_references` that satisfy the conditions. 

### Description of the syntax elements

| Syntax Elements | Description |
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | `LOW_PRIORITY` gives the statement lower priority. TiDB lowers the priority of the current statement. |
| `IGNORE` | To guarantee compatibility with MySQL, TiDB parses these three modifiers, but will ignore them.|
| `table_reference` | The Table Name to be updated |
| `table_references` | The Table Names to be updated |
| `SET assignment_list` | ColumnName and value to be updated |
| `WHERE where_condition` | The WHERE clause, if given, specifies the conditions that identify which rows to update.  |
| `ORDER BY` | $the rows are updated in the order that is specified$ |
| `LIMIT row_count` | $The LIMIT clause places a limit on the number of rows that can be updated.$ |

## REPLACE

`REPLACE` is a MySQL extension to the SQL standard. `REPLACE` works exactly like `INSERT`, except that if an old row in the table has the same value as a new row for a PRIMARY KEY or a UNIQUE index, the old row is deleted before the new row is inserted.

### Syntax

```sql
REPLACE [LOW_PRIORITY | DELAYED]
  [INTO] tbl_name
  [(col_name [, col_name] ...)]
  {VALUES | VALUE} (value_list) [, (value_list)] ...

REPLACE [LOW_PRIORITY | DELAYED]
  [INTO] tbl_name
  SET assignment_list

REPLACE [LOW_PRIORITY | DELAYED]
  [INTO] tbl_name
  [(col_name [, col_name] ...)]
  SELECT ...
```

### Description of the syntax elements

|Syntax Element|Description|
| -------------- | --------------------------------------------------------- |
| `LOW_PRIORITY` | `LOW_PRIORITY` gives the statement lower priority. TiDB lowers the priority of the current statement. |
| `DELAYED` | To guarantee compatibility with MySQL, TiDB parses these three modifiers, but will ignore them.|
| `tbl_name` | `tbl_name` is the table into which the rows should be inserted.  |
| `value_list` | data to be inserted |
| `SET assignment_list` | ColumnName and value to be updated |
| `SELECT ...` | results selected by 'SELECT' and to be inserted |

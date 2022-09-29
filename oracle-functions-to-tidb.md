---
title: Mappings between Functions and Syntax of Oracle and TiDB
summary: Learn the mappings between functions and syntax of Oracle and TiDB
---

# Mappings between Functions and Syntax of Oracle and TiDB

This document describes the mappings between functions and syntax of Oracle and TiDB. It helps you find the corresponding TiDB functions based on the Oracle functions, and understand the syntax differences between Oracle and TiDB.

> **Note:**
>
> The functions and syntax in this document are based on Oracle 12.2.0.1.0 and TiDB v5.4.0. They might be different in other versions.

## Mappings between some Oracle and TiDB functions

The following table shows the mappings between some Oracle and TiDB functions.

| Function | Oracle syntax | TiDB syntax | Note |
|---|---|---|---|
| Convert data types | <li>`TO_NUMBER(key)`</li><li>`TO_CHAR(key)`</li> | `CONVERT(key,dataType)` | TiDB supports converting `BINARY`, `CHAR`, `DATE`, `DATETIME`, `TIME`, `SIGNED INTEGER`, `UNSIGNED INTEGER` and `DECIMAL` types. |
| Convert a date type to a string type | <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd hh24:mi:ss')`</li> <li>`TO_CHAR(SYSDATE,'yyyy-MM-dd')`</li> | <li>`DATE_FORMAT(NOW(),'%Y-%m-%d %H:%i:%s')`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | TiDB format strings are case-sensitive. |
| Convert a string type to a date type | <li>`TO_DATE('2021-05-28 17:31:37','yyyy-MM-dd hh24:mi:ss')`</li><li>`TO_DATE('2021-05-28','yyyy-MM-dd hh24:mi:ss')`</li> | <li>`STR_TO_DATE('2021-05-28 17:31:37','%Y-%m-%d %H:%i:%s')`</li><li>`STR_TO_DATE('2021-05-28','%Y-%m-%d%T')` </li> | TiDB format strings are case-sensitive.  |
| Get the current system time (precision to the second) | `SYSDATE` | `NOW()` | |
| Get the number of days between `date1` and `date2` | `date1 - date2` | `DATEDIFF(date1, date2)` | |
| Increase or decrease date by `n` days  | `DATEVAL + n` | `DATE_ADD(dateVal,INTERVAL n DAY)` | `n` can be a negative value.|
| Increase or decrease date by `n` months | `ADD_MONTHS(dateVal,n)`| `DATE_ADD(dateVal,INTERVAL n MONTH)` | `n` can be a negative value. |
| Get the date (precision to the date) | `TRUNC(SYSDATE)` | <li>`CAST(NOW() AS DATE)`</li><li>`DATE_FORMAT(NOW(),'%Y-%m-%d')`</li> | In TiDB, `CAST` and  `DATE_FORMAT` return the same result. |
| Get the month of the date | `TRUNC(SYSDATE,'mm')` | `DATE_ADD(CURDATE(),interval - day(CURDATE()) + 1 day)`  | |
| Round down a value | `TRUNC(2.136) = 2`<br/> `TRUNC(2.136,2) = 2.14` | `TRUNCATE(2.136,0) = 2`<br/> `TRUNCATE(2.136,2) = 2.14` |  |
| Combine the strings `a` and `b` | `'a' || 'b'` | `CONCAT('a','b')` | |
| Get the next value in a sequence | `SEQUENCENAME.NEXTVAL` | `NEXTVAL(sequenceName)` | |
| Left join or right join | `SELECT * FROM a, b WHERE a.id = b.id(+);`<br/>`SELECT * FROM a, b WHERE a.id(+) = b.id;` | `SELECT * FROM a LEFT JOIN b ON a.id = b.id;`<br/>`SELECT * FROM a RIGHT JOIN b ON a.id = b.id;` | When correlating queries, TiDB does not support using (+) to left join or right join. You can use `LEFT JOIN` or `RIGHT JOIN` instead. |
| Get random sequence values | `SYS_GUID()` | `UUID()` | TiDB returns a Universal Unique Identifier (UUID).|
| `NVL()` | `NVL(key,val)` | `IFNULL(key,val)` | If the value of the field is `NULL`, it returns the value of `val`; otherwise, it returns the value of the field.  |
| `NVL2()` | `NVL2(key, val1, val2)`  | `IF(key is NULL, val1, val2)` | If the value of the field is not `NULL`, it returns the value of `val1`; otherwise, it returns the value of `val2`. |
| `DECODE()` | <li>`DECODE(key,val1,val2,val3)`</li><li>`DECODE(value,if1,val1,if2,val2,...,ifn,valn,val)`</li> | <li>`IF(key=val1,val2,val3)`</li><li>`CASE WHEN value=if1 THEN val1 WHEN value=if2 THEN val2,...,WHEN value=ifn THEN valn ELSE val END`</li> | <li>If the value of the field is equal to val1, then it returns val2; otherwise it returns val3.</li><li>When the field value satisfies the condition 1 (if1), it returns val1. When it satisfies the condition 2 (if2), it returns val2. When it satisfies the condition 3 (if3), it returns val3.</li> |
| Get the length of a string | `LENGTH(str)` | `CHAR_LENGTH(str)` | |
| Get sub strings | `SUBSTR('abcdefg',0,2) = 'ab'`<br/> `SUBSTR('abcdefg',1,2) = 'ab'` | `SUBSTRING('abcdefg',0,2) = ''`<br/>`SUBSTRING('abcdefg',1,2) = 'ab'` | <li>In Oracle, the starting position 0 has the same effect as 1. </li><li>In TiDB, the substring starting from 0 is null. If you need to start from the beginning of the string, you should start from 1.</li>|
| Search a string for substrings | `INSTR('abcdefg','b',1,1)` | `INSTR('abcdefg','b')` | Search from the first character of the string 'abcdefg' and return the position of the first occurrence of the 'b' string. |
| Search a string for substrings| `INSTR('stst','s',1,2)` | `LENGTH(SUBSTRING_INDEX('stst','s',2)) + 1` | Search from the first character of 'stst' and return the second occurrence of the 's' character. |
| Search a string for substrings | `INSTR('abcabc','b',2,1)` | `LOCATE('b','abcabc',2)` | Search from the second character of the string `abcabc` and return the first occurrence of the character `b`. |
| Get the interval months between dates | `MONTHS_BETWEEN(ENDDATE,SYSDATE)` | `TIMESTAMPDIFF(MONTH,SYSDATE,ENDDATE)` | The results of `MONTHS_BETWEEN()` in Oracle and `TIMESTAMPDIFF()` in TiDB are different. `TIMESTAMPDIFF()` keeps months only in integer. Note that the parameters in the two functions are in opposite positions. |
| Merge columns into rows | `LISTAGG(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME),'***') within GROUP(ORDER BY  DIMENSIONNAME)` | `GROUP_CONCAT(CONCAT(E.dimensionid,'---',E.DIMENSIONNAME) ORDER BY DIMENSIONNAME SEPARATOR '***')` | Combine a column of fields into one row and split them according to the `***` notation. |
| Get the current time (precision to the second) | `SYSTIMESTAMP` | `CURRENT_TIMESTAMP(6)` | |
| Convert ASCII values to corresponding characters | `CHR(n)` | `CHAR(n)` | The tab (`CHR(9)`), line feed (`CHR(10)`), and carriage return (`CHR(13)`) characters in Oracle correspond to `CHAR(9)`, `CHAR(10)`, and `CHAR(13)` in TiDB. |

## Syntax differences

This section describes some syntax differences between Oracle and TiDB.

### Add an alias for a table in the DELETE statement

Oracle supports adding an alias for a table in the DELETE statement. For example:

```sql
DELETE FROM test t WHERE t.xxx = xxx
```

TiDB does not support adding an alias for a table in the DELETE statement. For example:

```sql
DELETE FROM test WHERE xxx = xxx
```

### String syntax

- Oracle: strings can only be enclosed in single quotes (''). For example `'a'`
- TiDB: Strings can be enclosed in single quotes ('') or double quotes (""). For example, `'a'` and `"a"`

### Difference between `NULL` and an empty string

- Oracle does not distinguish between `NULL` and the empty string `''`, that is, `NULL` is equivalent to `''`.
- TiDB distinguishes between `NULL` and the empty string `''`. In TiDB, you need to convert `''` to `NULL`.

### Read and write to the same table in an `INSERT` statement

Oracle supports reading and writing to the same table in the `INSERT` statement. For example:

```sql
INSERT INTO table1 VALUES (feild1,(SELECT feild2 FROM table1 WHERE...))
```

TiDB does not support reading and writing to the same table in `INSERT` statements. For example:

```sql
INSERT INTO table1 VALUES（feild1,(SELECT T.fields2 FROM table1 T WHERE...)
```

### Get the first n pieces of data

- Oracle gets the first n pieces of data by `ROWNUM <= n`. For example `ROWNUM <= 10`.

- TiDB gets the first n pieces of data by `LIMIT n`. For example `LIMIT 10`. The Hibernate Query Language (HQL) running SQL statements with `LIMIT` results in an error. You need to change the Hibernate statements to SQL statements.

### `UPDATE` statement for multi-table updates

Oracle: it is not necessary to list the specific field update relationship when updating multiple tables. For example:

```sql
UPDATE test1 SET(test1.name,test1.age) = (SELECT test2.name,test2.age FROM test2 WHERE test2.id=test1.id)
```

TiDB: when updating multiple tables, you need to list all the specific field update relationships in `SET`. For example:

```sql
UPDATE test1,test2 SET test1.name=test2.name,test1.age=test2.age WHERE test1.id=test2.id
```

### Derived table alias

Oracle：when querying multiple tables, a derived table alias is not necessary. For example:

```sql
SELECT * FROM (SELECT * FROM test)
```

TiDB: when querying multiple tables, each derived table must have an alias of its own. For example:

```sql
SELECT * FROM (SELECT * FROM test) t
```

### Difference set operation

Oracle uses `MINUS` for difference set operations. For example:

```sql
SELECT * FROM t1 MINUS SELECT * FROM t2
```

TiDB does not support `MINUS`. You need to change it to `EXCEPT`. For example:

```sql
SELECT * FROM t1 EXCEPT SELECT * FROM t2
```

### Alias for `NULL` and `''`

Oracle: `NULL` is equivalent to `''`, and no special conversion is needed to alias a null value. For example

```sql
SELECT NULL AS ... FROM DUAL
```

TiDB: `NULL` is different from `''`. To alias a null value, you need to change `NULL` to `''`. For example:

```sql
SELECT '' AS ... FROM DUAL
```

### Comment syntax

- Oracle: `--Comment`. Oracle does not need a space after `--`.

- TiDB：`-- Comment`. TiDB needs a space after `--`.

### Paging queries

Oracle: `OFFSET m` means skipping `m` rows. `FETCH NEXT n ROWS ONLY` means taking `n` rows. For example:

```sql
SELECT * FROM tables OFFSET 0 ROWS FETCH NEXT 2000 ROWS ONLY
```

TiDB: Use `LIMIT n OFFSET m` to replace `OFFSET m ROWS FETCH NEXT n ROWS ONLY`. For example:

```sql
SELECT * FROM tables LIMIT 2000 OFFSET 0
```

### `ORDER BY` sorting rules for `NULL`

Rules for sorting `NULL` by the `ORDER BY` statement in Oracle.

- In `ORDER BY COLUM ASC`, `NULL` is placed last by default.

- In `ORDER BY COLUM DESC`, `NULL` is placed first by default.

- In `ORDER BY COLUM [ASC|DESC] NULLS FIRST`, `NULL` is forced to be placed first. Non-`NULL` values are still sorted by the declared order `ASC|DESC`.

- In `ORDER BY COLUM [ASC|DESC] NULLS LAST` , `NULL` is forced to be placed last. Non-`NULL` values are still sorted by the declared order `ASC|DESC`.

Rules for sorting `NULL` by the `ORDER BY` statement in TiDB.

- In `ORDER BY COLUM ASC`, `NULL` is placed first by default.

- `ORDER BY COLUM DESC`, `NULL` is placed last by default.

The following table shows some examples of equivalent `ORDER BY` statements in Oracle and TiDB:

| `ORDER BY` in Oracle | Equivalent in TiDB |
| :------------------- | :----------------- |
| `SELECT * FROM t1 ORDER BY name NULLS FIRST;`      |`SELECT * FROM t1 ORDER BY NAME ;`  |
| `SELECT * FROM t1 ORDER BY name DESC NULLS LAST;`  | `SELECT * FROM t1 ORDER BY NAME DESC;` |
| `SELECT * FROM t1 ORDER BY NAME DESC NULLS FIRST;` | `SELECT * FROM t1 ORDER BY ISNULL(name) DESC, name DESC;` |
|`SELECT * FROM t1 ORDER BY name ASC NULLS LAST;`    | `SELECT * FROM t1 ORDER BY ISNULL(name), name;` |

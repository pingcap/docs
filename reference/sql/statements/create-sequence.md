---
title: CREATE SEQUENCE
summary: An overview of the usage of CREATE SEQUENCE for the TiDB database.
category: reference
---

# CREATE SEQUENCE

The `CREATE SEQUENCE` statement creates sequence objects in TiDB. The sequence is a database object that is on a par with table and `View` objects. The sequence is used to generate customized and serialized IDs.

## Synopsis

**CreateSequenceStmt:**

![CreateSequenceStmt](/media/sqlgram-dev/CreateSequenceStmt.png)

**OptTemporary:**

![OptTemporary](/media/sqlgram-dev/OptTemporary.png)

**IfNotExists:**

![IfNotExists](/media/sqlgram-dev/IfNotExists.png)

**TableName:**

![TableName](/media/sqlgram-dev/TableName.png)

**CreateSequenceOptionListOpt:**

![CreateSequenceOptionListOpt](/media/sqlgram-dev/CreateSequenceOptionListOpt.png)

**SequenceOption:**

![SequenceOption](/media/sqlgram-dev/SequenceOption.png)

**CreateTableOptionListOpt:**

![CreateTableOptionListOpt](/media/sqlgram-dev/CreateTableOptionListOpt.png)

## Syntax

{{< copyable "sql" >}}

```sql
CREATE [TEMPORARY] SEQUENCE [IF NOT EXISTS] sequence_name
    [ INCREMENT [ BY | = ] increment ]
    [ MINVALUE [=] minvalue | NO MINVALUE | NOMINVALUE ]
    [ MAXVALUE [=] maxvalue | NO MAXVALUE | NOMAXVALUE ]
    [ START [ WITH | = ] start ]
    [ CACHE [=] cache | NOCACHE | NO CACHE]
    [ CYCLE | NOCYCLE | NO CYCLE]
    [ ORDER | NOORDER | NO ORDER]
    [table_options]
```

## Parameters

|Parameters | Default value | Description |
| :-- | :-- | :--|
| `INCREMENT` | `1` | The increment to use for values. Its positive or negative values can control the growth direction of the sequence. |
| `MINVALUE` | `1` or `-9223372036854775807` | Specifies the minimum value of a sequence. When `INCREMENT` > `0`, the default value is `1`. When `INCREMENT` < `0`, the default value is `-9223372036854775807`. |
| `MAXVALUE` | `9223372036854775806` or `-1` | Specifies the maximum value of a sequence. When `INCREMENT` > `0`, the default value is `9223372036854775806`. When `INCREMENT` < `0`, the default value is `1`. |
| `START` | `MINVALUE` or `MAXVALUE`| Specifies the initial value of a sequence. When `INCREMENT` > `0`, the default value is `MINVALUE`. When `INCREMENT` < `0`, the default value is `MAXVALUE`. |
| `CACHE` | `1000` | Specifies the size of the local cache sequence in TiDB. |
| `CYCLE` | `false` | Specifies whether a sequence restarts from the minimum value (or maximum for the descending sequence). When `INCREMENT` > `0`, the default value is `MINVALUE`. When `INCREMENT` < `0`, the default value is `MAXVALUE`. |

## `SEQUENCE` function

You can control a sequence through the following expression functions:

+ `NEXTVAL` or `NEXT VALUE FOR`

    Essentially, both are the `nextval()` function that gets the next valid value of the sequence object. The parameter of the `nextval()` function is the `identifier` of the sequence.

+ `LASTVAL`

    This function gets the last used value of this session. If the value does not exist, `NULL` is used. The parameter of this function is the `identifier` of the sequence.

+ `SETVAL`

    This function sets the next value to be returned for a sequence. The first parameter of this function is the `identifier` of the sequence; the second parameter is `num`.

> **Note:**
>
> In the implementation of TiDB `SEQUENCE`, the `SETVAL` function cannot change the initial progression or cycle progression of a sequence. This function only returns the next valid value based on this progression.

## Examples

{{< copyable "sql" >}}

```sql
CREATE SEQUENCE seq;
```

```
Query OK, 0 rows affected (0.06 sec)
```

{{< copyable "sql" >}}

```sql
SELECT nextval(seq);
```

```
+--------------+
| nextval(seq) |
+--------------+
|            1 |
+--------------+
1 row in set (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT lastval(seq);
```

```
+--------------+
| lastval(seq) |
+--------------+
|            1 |
+--------------+
1 row in set (0.02 sec)
```

{{< copyable "sql" >}}

```sql
SELECT setval(seq, 10);
```

```
+-----------------+
| setval(seq, 10) |
+-----------------+
|              10 |
+-----------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT next value for seq;
```

```
+--------------------+
| next value for seq |
+--------------------+
|                 11 |
+--------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
```

```
Query OK, 0 rows affected (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT lastval(seq2);
```

```
+---------------+
| lastval(seq2) |
+---------------+
|          NULL |
+---------------+
1 row in set (0.01 sec)
```

{{< copyable "sql" >}}

```sql
SELECT nextval(seq2);
```

```
+---------------+
| nextval(seq2) |
+---------------+
|             3 |
+---------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT setval(seq2, 6);
```

```
+-----------------+
| setval(seq2, 6) |
+-----------------+
|               6 |
+-----------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT next value for seq2;
```

```
+---------------------+
| next value for seq2 |
+---------------------+
|                   7 |
+---------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
CRATE table t(a int default next value for seq2);
```

```
Query OK, 0 rows affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
INSERT into t values();
```

```
Query OK, 1 row affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * from t;
```

```
+------+
| a    |
+------+
|    9 |
+------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
INSERT into t values();
```

```
ERROR 4135 (HY000): Sequence 'test.seq2' has run out
```

## MySQL compatibility

Currently, MySQL does not have the `SEQUENCE` option. TiDB `SEQUENCE` borrows from MariaDB. Except for the `SETVAL` function, all other functions have the same progressions with those functions of MariaDB.

Progression here means the arithmetic progression in a sequence after the numbers are defined. Although `SETVAL` can set the current value of a sequence, the subsequent values of the sequence still follows the progression.

For example:

```
1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
select setval(seq, 6)   // Sets the current value of a sequence to 6.
7, 9, 11, ...           // But the subsequent values still follow the progression.
```

In the `CYCLE` mode, the starting value of a sequence in the first round is `start`, and the starting value in the subsequent rounds is `MinValue` (increment > 0) or `MaxValue` (increment < 0).

## See also

* [DROP SEQUENCE](/reference/sql/statements/drop-sequence.md)
* [SHOW CREATE SEQUENCE](/reference/sql/statements/show-create-sequence.md)

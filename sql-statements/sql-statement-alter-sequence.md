---
title: ALTER SEQUENCE
summary: An overview of the usage of ALTER SEQUENCE for the TiDB database.
---

# ALTER SEQUENCE

The `ALTER SEQUENCE` statement alters sequence objects in TiDB. The sequence is a database object that is on a par with the `Table` and the `View` object. The sequence is used to generate serialized IDs in a customized way.

## Synopsis

```ebnf+diagram
CreateSequenceStmt ::=
    'ALTER' 'SEQUENCE' TableName CreateSequenceOptionListOpt

TableName ::=
    Identifier ('.' Identifier)?

CreateSequenceOptionListOpt ::=
    SequenceOption*

SequenceOptionList ::=
    SequenceOption

SequenceOption ::=
    ( 'INCREMENT' ( '='? | 'BY' ) | 'START' ( '='? | 'WITH' ) | ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' ) '='? ) SignedNum
|   'COMMENT' '='? stringLit
|   'NOMINVALUE'
|   'NO' ( 'MINVALUE' | 'MAXVALUE' | 'CACHE' | 'CYCLE' )
|   'NOMAXVALUE'
|   'NOCACHE'
|   'CYCLE'
|   'NOCYCLE'
|   'RESTART' ( ( '='? | 'WITH' ) SignedNum )?
```

## Syntax

```sql
ALTER SEQUENCE sequence_name
    [ INCREMENT [ BY | = ] increment ]
    [ MINVALUE [=] minvalue | NO MINVALUE | NOMINVALUE ]
    [ MAXVALUE [=] maxvalue | NO MAXVALUE | NOMAXVALUE ]
    [ START [ WITH | = ] start ]
    [ CACHE [=] cache | NOCACHE | NO CACHE]
    [ CYCLE | NOCYCLE | NO CYCLE]
    [table_options]
```

## Parameters

|Parameters | Default value | Description |
| :-- | :-- | :--|
| `INCREMENT` | `1` | Specifies the increment of a sequence. Its positive or negative values can control the growth direction of the sequence. |
| `MINVALUE` | `1` or `-9223372036854775807` | Specifies the minimum value of a sequence. When `INCREMENT` > `0`, the default value is `1`. When `INCREMENT` < `0`, the default value is `-9223372036854775807`. |
| `MAXVALUE` | `9223372036854775806` or `-1` | Specifies the maximum value of a sequence. When `INCREMENT` > `0`, the default value is `9223372036854775806`. When `INCREMENT` < `0`, the default value is `-1`. |
| `START` | `MINVALUE` or `MAXVALUE`| Specifies the initial value of a sequence. When `INCREMENT` > `0`, the default value is `MINVALUE`. When `INCREMENT` < `0`, the default value is `MAXVALUE`. |
| `CACHE` | `1000` | Specifies the local cache size of a sequence in TiDB. |
| `CYCLE` | `NO CYCLE` | Specifies whether a sequence restarts from the minimum value (or maximum for the descending sequence). When `INCREMENT` > `0`, the default value is `MINVALUE`. When `INCREMENT` < `0`, the default value is `MAXVALUE`. |

> **Note:**
>
> Changing the `START` value does not affect the generated values until you execute `ALTER SEQUENCE ... RESTART`.

## `SEQUENCE` function

You can control a sequence through the following expression functions:

+ `NEXTVAL` or `NEXT VALUE FOR`

    Essentially, both are the `NEXTVAL()` function that gets the next valid value of a sequence object. The parameter of the `NEXTVAL()` function is the `identifier` of the sequence.

+ `LASTVAL`

    This function gets the last used value of this session. If the value does not exist, `NULL` is used. The parameter of this function is the `identifier` of the sequence.

+ `SETVAL`

    This function sets the progression of the current value for a sequence. The first parameter of this function is the `identifier` of the sequence; the second parameter is `num`.

> **Note:**
>
> In the implementation of a sequence in TiDB, the `SETVAL` function cannot change the initial progression or cycle progression of this sequence. This function only returns the next valid value based on this progression.

## Examples

Create a sequence named `s1`:

```sql
CREATE SEQUENCE s1;
```

```
Query OK, 0 rows affected (0.15 sec)
```

Get the next two values from the sequence by executing the following SQL statement twice:

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|           1 |
+-------------+
1 row in set (0.01 sec)
```

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|           2 |
+-------------+
1 row in set (0.00 sec)
```

Change the increment of the sequence to `2`:

```sql
ALTER SEQUENCE s1 INCREMENT=2;
```

```
Query OK, 0 rows affected (0.18 sec)
```

Now, get the next two values from the sequence again:

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|        1001 |
+-------------+
1 row in set (0.02 sec)
```

```sql
SELECT NEXTVAL(s1);
```

```
+-------------+
| NEXTVAL(s1) |
+-------------+
|        1003 |
+-------------+
1 row in set (0.00 sec)
```

As you can see from the output, the values now increase by two, following the `ALTER SEQUENCE` statement.

You can also change other parameters of the sequence. For example, you can change the `MAXVALUE` of the sequence as follows:

```sql
CREATE SEQUENCE s2 MAXVALUE=10;
```

```
Query OK, 0 rows affected (0.17 sec)
```

```sql
ALTER SEQUENCE s2 MAXVALUE=100;
```

```
Query OK, 0 rows affected (0.15 sec)
```

```sql
SHOW CREATE SEQUENCE s2\G
```

```
*************************** 1. row ***************************
       Sequence: s2
Create Sequence: CREATE SEQUENCE `s2` start with 1 minvalue 1 maxvalue 100 increment by 1 cache 1000 nocycle ENGINE=InnoDB
1 row in set (0.00 sec)
```

## MySQL compatibility

This statement is a TiDB extension. The implementation is modeled on sequences available in MariaDB.

Except for the `SETVAL` function, all other functions have the same _progressions_ as MariaDB. Here "progression" means that the numbers in a sequence follow a certain arithmetic progression rule defined by the sequence. Although you can use `SETVAL` to set the current value of a sequence, the subsequent values of the sequence still follow the original progression rule.

For example:

```
1, 3, 5, ...            // The sequence starts from 1 and increments by 2.
SELECT SETVAL(seq, 6)   // Sets the current value of a sequence to 6.
7, 9, 11, ...           // Subsequent values still follow the progression rule.
```

In the `CYCLE` mode, the initial value of a sequence in the first round is the value of the `START` parameter, and the initial value in the subsequent rounds is the value of `MinValue` (`INCREMENT` > 0) or `MaxValue` (`INCREMENT` < 0).

## See also

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [Sequence Functions](/functions-and-operators/sequence-functions.md)

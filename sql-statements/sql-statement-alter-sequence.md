---
title: ALTER SEQUENCE
summary: 关于在 TiDB 数据库中使用 ALTER SEQUENCE 的概述。
---

# ALTER SEQUENCE

`ALTER SEQUENCE` 语句用于修改 TiDB 中的序列对象。序列是与 `Table` 和 `View` 对象同等地位的数据库对象。序列用于以定制化的方式生成有序的 ID。

## 概述

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

## 语法

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

## 参数

| 参数 | 默认值 | 描述 |
| :-- | :-- | :--|
| `INCREMENT` | `1` | 指定序列的增量。其正负值可以控制序列的增长方向。 |
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`。当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。 |
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`。当 `INCREMENT` < `0` 时，默认值为 `-1`。 |
| `START` | `MINVALUE` 或 `MAXVALUE` | 指定序列的初始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |
| `CACHE` | `1000` | 指定 TiDB 中序列的本地缓存大小。 |
| `CYCLE` | `NO CYCLE` | 指定序列是否在达到最大值（或最小值，递减序列）后重新循环。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |

> **Note:**
>
> 改变 `START` 值不会影响已生成的值，直到你执行 `ALTER SEQUENCE ... RESTART`。

## `SEQUENCE` 函数

你可以通过以下表达式函数控制序列：

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上，它们都是 `NEXTVAL()` 函数，用于获取序列对象的下一个有效值。`NEXTVAL()` 函数的参数是序列的 `identifier`。

+ `LASTVAL`

    该函数获取当前会话的上一个使用的值。如果不存在，则返回 `NULL`。参数为序列的 `identifier`。

+ `SETVAL`

    该函数设置序列的当前值。第一个参数为序列的 `identifier`，第二个参数为 `num`。

> **Note:**
>
> 在 TiDB 中实现序列时，`SETVAL` 函数不能改变序列的初始递增值或循环递增值。该函数仅返回基于当前递增规则的下一个有效值。

## 示例

创建一个名为 `s1` 的序列：

```sql
CREATE SEQUENCE s1;
```

```
Query OK, 0 rows affected (0.15 sec)
```

通过执行以下 SQL 语句两次，获取序列的下两个值：

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

将序列的增量改为 `2`：

```sql
ALTER SEQUENCE s1 INCREMENT=2;
```

```
Query OK, 0 rows affected (0.18 sec)
```

现在，再次获取序列的下两个值：

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

从输出可以看出，值现在按照 `ALTER SEQUENCE` 语句的设置以增量 2 递增。

你还可以修改序列的其他参数。例如，修改 `MAXVALUE`：

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

## MySQL 兼容性

该语句是 TiDB 的扩展功能。其实现借鉴了 MariaDB 中的序列。

除 `SETVAL` 函数外，其他所有函数的 _递增规则_ 与 MariaDB 相同。这里的“递增规则”指序列中的数字遵循由序列定义的某个算术递推规则。虽然你可以使用 `SETVAL` 来设置序列的当前值，但序列的后续值仍然遵循原有的递推规则。

例如：

```
1, 3, 5, ...            // 序列从 1 开始，递增 2。
SELECT SETVAL(seq, 6)   // 将序列的当前值设置为 6。
7, 9, 11, ...           // 后续值仍然遵循递推规则。
```

在 `CYCLE` 模式下，序列在第一轮的初始值为 `START` 参数的值，后续轮次的初始值为 `MinValue`（`INCREMENT` > 0）或 `MaxValue`（`INCREMENT` < 0）。

## 相关链接

* [CREATE SEQUENCE](/sql-statements/sql-statement-create-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [Sequence Functions](/functions-and-operators/sequence-functions.md)

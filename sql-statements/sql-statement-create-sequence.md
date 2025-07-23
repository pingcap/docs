---
title: CREATE SEQUENCE
summary: 关于在 TiDB 数据库中使用 CREATE SEQUENCE 的概述。
---

# CREATE SEQUENCE

`CREATE SEQUENCE` 语句在 TiDB 中创建序列对象。序列是与表和 `View` 对象同等地位的数据库对象。序列用于以定制化的方式生成序列化的 ID。

## 概述

```ebnf+diagram
CreateSequenceStmt ::=
    'CREATE' 'SEQUENCE' IfNotExists TableName CreateSequenceOptionListOpt

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

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
```

## 语法

```sql
CREATE [TEMPORARY] SEQUENCE [IF NOT EXISTS] sequence_name
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
| :-- | :-- | :-- |
| `TEMPORARY` | `false` | TiDB 目前不支持 `TEMPORARY` 选项，仅提供语法兼容性。 |
| `INCREMENT` | `1` | 指定序列的增量。其正负值可以控制序列的增长方向。 |
| `MINVALUE` | `1` 或 `-9223372036854775807` | 指定序列的最小值。当 `INCREMENT` > `0` 时，默认值为 `1`。当 `INCREMENT` < `0` 时，默认值为 `-9223372036854775807`。 |
| `MAXVALUE` | `9223372036854775806` 或 `-1` | 指定序列的最大值。当 `INCREMENT` > `0` 时，默认值为 `9223372036854775806`。当 `INCREMENT` < `0` 时，默认值为 `-1`。 |
| `START` | `MINVALUE` 或 `MAXVALUE` | 指定序列的起始值。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |
| `CACHE` | `1000` | 指定 TiDB 中序列的本地缓存大小。 |
| `CYCLE` | `NO CYCLE` | 指定序列是否在达到最大值（或最小值，递减序列时）后重新循环。当 `INCREMENT` > `0` 时，默认值为 `MINVALUE`。当 `INCREMENT` < `0` 时，默认值为 `MAXVALUE`。 |

## `SEQUENCE` 函数

你可以通过以下表达式函数控制序列：

+ `NEXTVAL` 或 `NEXT VALUE FOR`

    本质上，它们都是 `NEXTVAL()` 函数，用于获取序列对象的下一个有效值。`NEXTVAL()` 函数的参数是序列的 `identifier`。

+ `LASTVAL`

    该函数获取本会话中最后一次使用的值。如果不存在，则返回 `NULL`。参数为序列的 `identifier`。

+ `SETVAL`

    该函数设置序列的当前值（或当前位置）。第一个参数为序列的 `identifier`，第二个参数为 `num`。

> **Note:**
>
> 在 TiDB 中实现序列时，`SETVAL` 函数不能改变序列的初始递增值或循环递增值。此函数仅返回基于当前递增规则的下一个有效值。

## 示例

+ 创建一个使用默认参数的序列对象：

    
    ```sql
    CREATE SEQUENCE seq;
    ```

    ```
    Query OK, 0 rows affected (0.06 sec)
    ```

+ 使用 `NEXTVAL()` 函数获取序列对象的下一个值：

    
    ```sql
    SELECT NEXTVAL(seq);
    ```

    ```
    +--------------+
    | NEXTVAL(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

+ 使用 `LASTVAL()` 函数获取本会话中最后一次调用序列对象生成的值：

    
    ```sql
    SELECT LASTVAL(seq);
    ```

    ```
    +--------------+
    | LASTVAL(seq) |
    +--------------+
    |            1 |
    +--------------+
    1 row in set (0.02 sec)
    ```

+ 使用 `SETVAL()` 函数设置序列的当前值（或当前位置）：

    
    ```sql
    SELECT SETVAL(seq, 10);
    ```

    ```
    +-----------------+
    | SETVAL(seq, 10) |
    +-----------------+
    |              10 |
    +-----------------+
    1 row in set (0.01 sec)
    ```

+ 你也可以使用 `next value for` 语法获取序列的下一个值：

    
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

+ 创建一个具有默认自定义参数的序列对象：

    
    ```sql
    CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

+ 当在此会话中未使用过该序列对象时，`LASTVAL()` 函数返回 `NULL`。

    
    ```sql
    SELECT LASTVAL(seq2);
    ```

    ```
    +---------------+
    | LASTVAL(seq2) |
    +---------------+
    |          NULL |
    +---------------+
    1 row in set (0.01 sec)
    ```

+ `NEXTVAL()` 函数的第一个有效值为 `START` 参数的值。

    
    ```sql
    SELECT NEXTVAL(seq2);
    ```

    ```
    +---------------+
    | NEXTVAL(seq2) |
    +---------------+
    |             3 |
    +---------------+
    1 row in set (0.00 sec)
    ```

+ 虽然 `SETVAL()` 可以改变序列的当前值，但不能改变下一次值的算术递增规则。

    
    ```sql
    SELECT SETVAL(seq2, 6);
    ```

    ```
    +-----------------+
    | SETVAL(seq2, 6) |
    +-----------------+
    |               6 |
    +-----------------+
    1 row in set (0.00 sec)
    ```

+ 当你使用 `NEXTVAL()` 获取下一个值时，下一次的值将遵循序列定义的算术递增规则。

    
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

+ 你可以将序列的下一个值用作列的默认值，例如如下示例。

    
    ```sql
    CREATE table t(a int default next value for seq2);
    ```

    ```
    Query OK, 0 rows affected (0.02 sec)
    ```

+ 在以下示例中，没有指定值，因此使用 `seq2` 的默认值。

    
    ```sql
    INSERT into t values();
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

    
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

+ 在以下示例中，没有指定值，因此使用 `seq2` 的默认值。但 `seq2` 的下一个值不在上述定义的范围内（`CREATE SEQUENCE seq2 start 3 increment 2 minvalue 1 maxvalue 10 cache 3;`），因此会返回错误。

    
    ```sql
    INSERT into t values();
    ```

    ```
    ERROR 4135 (HY000): Sequence 'test.seq2' has run out
    ```

## MySQL 兼容性

此语句为 TiDB 扩展功能。其实现借鉴了 MariaDB 中的序列。

除 `SETVAL` 函数外，所有其他函数的 _递增_ 行为与 MariaDB 相同。这里的“递增”指序列中的数字遵循由序列定义的某个算术递增规则。虽然你可以使用 `SETVAL` 来设置序列的当前值，但序列的后续值仍然遵循原有的递增规则。

例如：

```
1, 3, 5, ...            // 序列从 1 开始，递增 2。
select SETVAL(seq, 6)   // 将序列的当前值设置为 6。
7, 9, 11, ...           // 后续值仍然遵循递增规则。
```

在 `CYCLE` 模式下，序列在第一轮的起始值为 `START` 参数的值，后续轮次的起始值为 `MinValue`（`INCREMENT` > 0）或 `MaxValue`（`INCREMENT` < 0）。

## 另请参见

* [ALTER SEQUENCE](/sql-statements/sql-statement-alter-sequence.md)
* [DROP SEQUENCE](/sql-statements/sql-statement-drop-sequence.md)
* [SHOW CREATE SEQUENCE](/sql-statements/sql-statement-show-create-sequence.md)
* [Sequence Functions](/functions-and-operators/sequence-functions.md)

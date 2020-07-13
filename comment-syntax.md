---
title: Comment Syntax
category: reference
summary: This document introduces the comment syntax supported by TiDB.
aliases: ['/docs/dev/comment-syntax/','/docs/dev/reference/sql/language-structure/comment-syntax/']
---

# Comment Syntax

This document describes the comment syntax supported by TiDB.
TiDB supports three comment styles:

- Use `#` to comment a line:

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     # comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```

- Use `--` to comment a line:

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+1;     -- comments
    ```

    ```
    +------+
    | 1+1  |
    +------+
    |    2 |
    +------+
    1 row in set (0.00 sec)
    ```
    
    And this style requires at least one whitespace after `--`:

   {{< copyable "sql" >}}

    ```sql
    SELECT 1+1--1;
    ```

    ```
    +--------+
    | 1+1--1 |
    +--------+
    |      3 |
    +--------+
    1 row in set (0.01 sec)
    ```

- Use `/* */` to comment a block or multiple lines:

   {{< copyable "sql" >}}

    ```sql
    SELECT 1 /* this is an in-line comment */ + 1;
    ```

    ```
    +--------+
    | 1  + 1 |
    +--------+
    |      2 |
    +--------+
    1 row in set (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    SELECT 1+
        -> /*
    /*> this is a
    /*> multiple-line comment
    /*> */
        -> 1;
    ```

    ```
    +-------+
    | 1+
    1 |
    +-------+
    |     2 |
    +-------+
    1 row in set (0.00 sec)
    ```

## Comment syntax compatible with MySQL

The same as MySQL, TiDB supports a variant of C comment style:

```
/*! Specific code */
```

or

```
/*!50110 Specific code */
```

In this style, TiDB runs the statements in the comment. This syntax is to make these SQLs ignored in other databases and executed in TiDB.

For example:

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

In TiDB, you can also use another version:

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

If the server version number is specified in the comment, for example, `/*!50110 KEY_BLOCK_SIZE=1024 */`, in MySQL it means that the contents in this comment is processed only when the MySQL version is or higher than 5.1.10. But in TiDB, the MySQL version number is ignored, resulting in `KEY_BLOCK_SIZE=1024`. 

## TiDB comment syntax

TiDB has its own comment syntax for the version number， which can be divided into the following two types:

* `/*T! Specific code */`: This syntax can only be parsed and executed by TiDB, and be ignored in other databases.
* `/*T![feature_id] Specific code */`: This syntax is used to ensure compatibility between different versions of TiDB. TiDB can parse the SQL fragment in this comment only if it implements the  corresponding feature of `feature_id` in the current version. For example, as the `AUTO_RANDOM` feature is introduced in v3.1.1, this version can parse `/*T![auto_rand] auto_random */` into `auto_random`. While the `AUTO_RANDOM` feature is not implemented in v3.0.0, the SQL statement fragment above is ignored.

## Optimizer comment syntax

Another type of comment is specially treated as the Hint optimizer:

{{< copyable "sql" >}}

```sql
SELECT /*+ hint */ FROM ...;
```

For details about the optimizer hints that TiDB supports, see [Optimizer hints](/optimizer-hints.md).

> **Note**
>
> TiDB comment syntax and optimizer comment syntax in MySQL client before 5.7.7 will be cleared as comments by default. So if you need to use these two syntaxes in the old client, add the --comments option when starting the client. For example, `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

For more information, see [Comment Syntax](https://dev.mysql.com/doc/refman/5.7/en/comments.html).

---
title: 注释语法
summary: 本文档介绍了 TiDB 支持的注释语法。
---

# 注释语法

本文档描述了 TiDB 支持的注释语法。

TiDB 支持三种注释风格：

- 使用 `#` 来注释一行：

    
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

- 使用 `--` 来注释一行：

    
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
    
    并且这种风格要求在 `--` 后至少有一个空格：

   
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

- 使用 `/* */` 来注释块或多行：

   
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

    
    ```sql
    SELECT 1+
    /*
    /*> this is a
    /*> multiple-line comment
    /*> */
        1;
    ```

    ```
    +-------------------+
    | 1+
            1 |
    +-------------------+
    |                 2 |
    +-------------------+
    1 row in set (0.001 sec)
    ```

## MySQL 兼容的注释语法

与 MySQL 相同，TiDB 支持一种变体的 C 注释风格：

```
/*! Specific code */
```

或

```
/*!50110 Specific code */
```

在这种风格中，TiDB 会执行注释中的语句。

例如：

```sql
SELECT /*! STRAIGHT_JOIN */ col1 FROM table1,table2 WHERE ...
```

在 TiDB 中，你还可以使用另一种版本：

```sql
SELECT STRAIGHT_JOIN col1 FROM table1,table2 WHERE ...
```

如果在注释中指定了服务器版本号，例如，`/*!50110 KEY_BLOCK_SIZE=1024 */`，在 MySQL 中意味着只有当 MySQL 版本为或高于 5.1.10 时，才会处理注释中的内容。但在 TiDB 中，MySQL 版本号不起作用，注释中的所有内容都会被处理。

## TiDB 特有的注释语法

TiDB 有自己的一套注释语法（即 TiDB 特有的注释语法），可以分为以下两类：

* `/*T! Specific code */`：这种语法只能被 TiDB 解析和执行，在其他数据库中会被忽略。
* `/*T![feature_id] Specific code */`：这种语法用于确保不同版本的 TiDB 之间的兼容性。只有当 TiDB 实现了对应的 `feature_id` 功能时，TiDB 才会解析该 SQL 片段。例如，随着 `AUTO_RANDOM` 功能在 v3.1.1 中引入，当前版本的 TiDB 可以将 `/*T![auto_rand] auto_random */` 解析为 `auto_random`。因为在 v3.0.0 中未实现 `AUTO_RANDOM` 功能，上述 SQL 片段会被忽略。**请勿在 `/*T![` 和 `]` 之间留空格**。

## 优化器注释语法

另一种特殊处理的注释是作为优化器提示（hint）：

```sql
SELECT /*+ hint */ FROM ...;
```

关于 TiDB 支持的优化器提示的详细信息，请参见 [Optimizer hints](/optimizer-hints.md)。

> **Note:**
>
> 在 MySQL 客户端中，TiDB 特有的注释语法会被视为普通注释并默认清除。在 5.7.7 之前的 MySQL 客户端中，提示也会被视为注释并默认清除。建议在启动客户端时使用 `--comments` 选项。例如，`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

更多信息请参见 [Comment Syntax](https://dev.mysql.com/doc/refman/8.0/en/comments.html)。
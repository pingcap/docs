---
title: 使用 `tidb_read_staleness` 系统变量读取历史数据
summary: 了解如何通过 `tidb_read_staleness` 系统变量读取历史数据。
---

# 使用 `tidb_read_staleness` 系统变量读取历史数据

为了支持读取历史数据，在 v5.4 版本中，TiDB 引入了一个新的系统变量 `tidb_read_staleness`。本文档描述了如何通过该系统变量读取历史数据，包括详细的操作流程。

## 功能描述

`tidb_read_staleness` 系统变量用于设置 TiDB 在当前会话中可以读取的历史数据的时间范围。该变量的数据类型为 int 类型，作用域为 `SESSION`。设置值后，TiDB 会在允许范围内选择一个尽可能新的时间戳，并以此时间戳进行后续的读取操作。例如，如果该变量的值设置为 `-5`，在 TiKV 存在对应历史版本数据的前提下，TiDB 会在 5 秒的时间范围内选择一个尽可能新的时间戳。

启用 `tidb_read_staleness` 后，你仍然可以执行以下操作：

- 在当前会话中插入、修改、删除数据或执行 DML 操作。这些操作不受 `tidb_read_staleness` 的影响。
- 在当前会话中开启交互式事务。事务中的查询仍然读取最新的数据。

在读取历史数据后，你可以通过以下两种方式读取最新数据：

- 开启一个新的会话。
- 使用 `SET` 语句将 `tidb_read_staleness` 变量的值设置为 `""`。

> **Note:**
>
> 为了减少延迟并提高 Stale Read 数据的时效性，你可以修改 TiKV 的 `advance-ts-interval` 配置项。详细信息请参见 [Reduce Stale Read latency](/stale-read.md#reduce-stale-read-latency)。

## 使用示例

本节通过示例介绍如何使用 `tidb_read_staleness`。

1. 创建一张表，并插入几行数据：

    
    ```sql
    create table t (c int);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    
    ```sql
    insert into t values (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查询表中的数据：

    
    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. 更新某一行的数据：

    
    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

4. 确认数据已被更新：

    
    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

5. 设置 `tidb_read_staleness` 系统变量。

    该变量的作用域为 `SESSION`。设置后，TiDB 会在设置的时间范围内选择一个尽可能新的时间戳，并以此时间戳读取历史数据。

    以下设置表示 TiDB 会在从 5 秒前到现在的时间范围内选择一个尽可能新的时间戳作为读取历史数据的时间点：

    
    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **Note:**
    >
    >  - 在 `tidb_read_staleness` 前使用 `@@`，而不是 `@`。`@@` 表示系统变量，`@` 表示用户变量。
    >  - 你需要根据第 3 步和第 4 步所花费的总时间，设置合适的历史时间范围（`tidb_read_staleness` 的值）。否则，查询结果会显示最新的数据，而不是历史数据。因此，你需要根据操作所花费的时间调整时间范围。例如，在此示例中，由于设置的时间范围为 5 秒，你需要在 5 秒内完成第 3 步和第 4 步。

    这里读取到的数据是更新之前的数据，即历史数据：

    
    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6. 取消设置该变量后，TiDB 可以读取最新的数据：

    
    ```sql
    set @@tidb_read_staleness="";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    
    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```
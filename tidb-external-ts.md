---
title: 使用 `tidb_external_ts` 变量读取历史数据
summary: 了解如何使用 `tidb_external_ts` 变量读取历史数据。
---

# 使用 `tidb_external_ts` 变量读取历史数据

为了支持读取历史数据，TiDB v6.4.0 引入了系统变量 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)。本文档描述了如何通过该系统变量读取历史数据，包括详细的使用示例。

## 场景

从指定时间点读取历史数据对于数据复制工具（如 TiCDC）非常有用。在数据复制工具完成某个时间点之前的数据复制后，你可以将下游 TiDB 的 `tidb_external_ts` 系统变量设置为该时间点之前的时间，从而读取该时间点之前的数据。这可以防止数据复制引起的数据不一致。

## 功能描述

当启用 `tidb_enable_external_ts_read` 时，系统变量 [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) 指定要读取的历史数据的时间戳。

系统变量 [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) 控制是否在当前会话或全局范围内读取历史数据。默认值为 `OFF`，表示禁用读取历史数据的功能，`tidb_external_ts` 的值会被忽略。当将 `tidb_enable_external_ts_read` 全局设置为 `ON` 时，所有查询会读取 `tidb_external_ts` 指定时间点之前的历史数据。如果只在某个会话中将 `tidb_enable_external_ts_read` 设置为 `ON`，则只有该会话中的查询会读取历史数据。

当启用 `tidb_enable_external_ts_read` 后，TiDB 将变为只读模式。所有写入查询将失败，并返回类似 `ERROR 1836 (HY000): Running in read-only mode` 的错误。

## 使用示例

本节介绍如何使用 `tidb_external_ts` 变量结合示例读取历史数据。

1. 创建表并插入一些行：

    ```sql
    CREATE TABLE t (c INT);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    ```sql
    INSERT INTO t VALUES (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. 查看表中的数据：

    ```sql
    SELECT * FROM t;
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

3. 将 `tidb_external_ts` 设置为 `@@tidb_current_ts`：

    ```sql
    START TRANSACTION;
    SET GLOBAL tidb_external_ts=@@tidb_current_ts;
    COMMIT;
    ```

4. 插入一行新数据，并确认已插入：

    ```sql
    INSERT INTO t VALUES (4);
    ```

    ```
    Query OK, 1 row affected (0.001 sec)
    ```

    ```sql
    SELECT * FROM t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    |    4 |
    +------+
    4 rows in set (0.00 sec)
    ```

5. 将 `tidb_enable_external_ts_read` 设置为 `ON`，然后查看表中的数据：

    ```sql
    SET tidb_enable_external_ts_read=ON;
    SELECT * FROM t;
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

    因为 `tidb_external_ts` 被设置为插入新行之前的时间戳，所以在启用 `tidb_enable_external_ts_read` 后，新增的那一行不会被返回。
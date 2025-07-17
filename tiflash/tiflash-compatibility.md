---
title: TiFlash 兼容性注意事项
summary: 了解与 TiFlash 不兼容的 TiDB 特性。
---

# TiFlash 兼容性注意事项

TiFlash 在以下情况下与 TiDB 不兼容：

* 在 TiFlash 计算层：
    * 不支持检查 [numerical values](/data-type-numeric.md) 是否溢出。例如，将两个最大值 `BIGINT` 类型的值 `9223372036854775807 + 9223372036854775807` 相加。在 TiDB 中，此计算的预期行为是返回 `ERROR 1690 (22003): BIGINT value is out of range` 错误。然而，在 TiFlash 中执行此计算时，会返回溢出值 `-2`，且没有任何错误提示。
    * 并非所有 [window functions](/functions-and-operators/window-functions.md) 都支持 [pushdown](/tiflash/tiflash-supported-pushdown-calculations.md)。
    * 不支持从 TiKV 读取数据。
    * 目前，TiFlash 中的 [`SUM`](/functions-and-operators/aggregate-group-by-functions.md#supported-aggregate-functions) 函数不支持字符串类型的参数。但在 TiDB 中，编译时无法判断是否传入字符串类型的参数到 `SUM` 函数中。因此，当你执行类似 `SELECT SUM(string_col) FROM t` 的语句时，TiFlash 会返回 `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.` 错误。为了避免此类错误，你需要将 SQL 语句修改为 `SELECT SUM(CAST(string_col AS double)) FROM t`。
    * 目前，TiFlash 的 decimal 除法计算方式与 TiDB 不兼容。例如，在进行 decimal 除法时，TiFlash 始终使用编译时推断的类型进行计算。而 TiDB 则使用比推断类型更高精度的类型进行计算。因此，涉及 decimal 除法的某些 SQL 语句在 TiDB + TiKV 和 TiDB + TiFlash 中执行时会返回不同的结果。例如：

        ```sql
        mysql> CREATE TABLE t (a DECIMAL(3,0), b DECIMAL(10, 0));
        Query OK, 0 rows affected (0.07 sec)
        mysql> INSERT INTO t VALUES (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)
        mysql> ALTER TABLE t SET TIFLASH REPLICA 1;
        Query OK, 0 rows affected (0.07 sec)
        mysql> SET SESSION tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)
        mysql> SELECT a/b, a/b + 0.0000000000001 FROM t WHERE a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)
        mysql> SET SESSION tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)
        mysql> SELECT a/b, a/b + 0.0000000000001 FROM t WHERE a/b;
        Empty set (0.01 sec)
        ```

        在上述示例中，`a/b` 在编译时推断的类型在 TiDB 和 TiFlash 中都是 `DECIMAL(7,4)`。由于受限于 `DECIMAL(7,4)`，`a/b` 返回的类型为 `0.0000`。在 TiDB 中，`a/b` 的运行时精度高于 `DECIMAL(7,4)`，因此原始表中的数据不会被 `WHERE a/b` 条件过滤。而在 TiFlash 中，`a/b` 的计算结果类型使用 `DECIMAL(7,4)`，因此原始表中的数据会被 `WHERE a/b` 条件过滤。

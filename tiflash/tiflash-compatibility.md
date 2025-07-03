---
title: TiFlash Compatibility Notes
summary: Learn the TiDB features that are incompatible with TiFlash.
---

# TiFlash Compatibility Notes

TiFlash is incompatible with TiDB in the following situations:

* In the TiFlash computation layer:
    * Checking overflowed [numerical values](/data-type-numeric.md) is not supported. For example, adding two maximum values of the `BIGINT` type `9223372036854775807 + 9223372036854775807`. The expected behavior of this calculation in TiDB is to return the `ERROR 1690 (22003): BIGINT value is out of range` error. However, if this calculation is performed in TiFlash, an overflow value of `-2` is returned without any error.
    * Not all [window functions](/functions-and-operators/window-functions.md) are supported for [pushdown](/tiflash/tiflash-supported-pushdown-calculations.md).
    * Reading data from TiKV is not supported.
    * Currently, the [`SUM`](/functions-and-operators/aggregate-group-by-functions.md#supported-aggregate-functions) function in TiFlash does not support the string-type argument. But TiDB cannot identify whether any string-type argument has been passed into the `SUM` function during the compiling. Therefore, when you execute statements similar to `SELECT SUM(string_col) FROM t`, TiFlash returns the `[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.` error. To avoid such an error in this case, you need to modify this SQL statement to `SELECT SUM(CAST(string_col AS double)) FROM t`.
    * Currently, TiFlash's decimal division calculation is incompatible with that of TiDB. For example, when dividing decimal, TiFlash performs the calculation always using the type inferred from the compiling. However, TiDB performs this calculation using a type that is more precise than that inferred from the compiling. Therefore, some SQL statements involving the decimal division return different execution results when executed in TiDB + TiKV and in TiDB + TiFlash. For example:

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

        In the preceding example, `a/b`'s inferred type from the compiling is `DECIMAL(7,4)` both in TiDB and in TiFlash. Constrained by `DECIMAL(7,4)`, `a/b`'s returned type is `0.0000`. In TiDB, `a/b`'s runtime precision is higher than `DECIMAL(7,4)`, so the original table data is not filtered by the `WHERE a/b` condition. However, in TiFlash, the calculation of `a/b` uses `DECIMAL(7,4)` as the result type, so the original table data is filtered by the `WHERE a/b` condition.

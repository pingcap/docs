---
title: TiFlash Compatibility Notes
summary: TiFlashと互換性のない TiDB 機能について説明します。
---

# TiFlash互換性に関する注意事項 {#tiflash-compatibility-notes}

次の状況では、 TiFlashは TiDB と互換性がありません。

-   TiFlash計算レイヤー:
    -   オーバーフローした[数値](/data-type-numeric.md)チェックはサポートされていません。例えば、 `BIGINT`の最大値2つを加算して`9223372036854775807 + 9223372036854775807` 。TiDBでは、この計算は`ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことが期待されます。しかし、この計算をTiFlashで実行すると、エラーなしでオーバーフロー値`-2`返されます。
    -   [ウィンドウ関数](/functions-and-operators/window-functions.md)すべてが[プッシュダウン](/tiflash/tiflash-supported-pushdown-calculations.md)でサポートされているわけではありません。
    -   TiKV からのデータの読み取りはサポートされていません。
    -   現在、 TiFlashの[`SUM`](/functions-and-operators/aggregate-group-by-functions.md#supported-aggregate-functions)関数は文字列型の引数をサポートしていません。しかし、TiDBはコンパイル時に`SUM`関数に文字列型の引数が渡されたかどうかを識別できません。そのため、 `SELECT SUM(string_col) FROM t`のような文を実行すると、 TiFlashは`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。このようなエラーを回避するには、このSQL文を`SELECT SUM(CAST(string_col AS double)) FROM t`に変更する必要があります。
    -   現在、TiFlash の小数除算計算は TiDB のものと互換性がありません。例えば、小数除算を行う場合、 TiFlash は常にコンパイルから推論された型を使用して計算を実行します。一方、TiDB はコンパイルから推論された型よりも精度の高い型を使用して計算を実行します。そのため、小数除算を含む一部の SQL 文は、TiDB + TiKV と TiDB + TiFlashで実行した場合で異なる実行結果を返します。例えば、次のようになります。

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

        上の例では、コンパイルから推論された`a/b`の型は、TiDB とTiFlashの両方で`DECIMAL(7,4)`です。 `DECIMAL(7,4)`制約により、 `a/b`の戻り型は`0.0000`なります。TiDB では、 `a/b`の実行時精度は`DECIMAL(7,4)`よりも高いため、元のテーブルデータは`WHERE a/b`条件によってフィルタリングされません。しかし、 TiFlashでは、 `a/b`の計算で結果の型として`DECIMAL(7,4)`使用されるため、元のテーブルデータは`WHERE a/b`条件によってフィルタリングされます。

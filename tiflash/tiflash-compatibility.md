---
title: TiFlash Compatibility Notes
summary: Learn the TiDB features that are incompatible with TiFlash.
---

# TiFlash互換性に関する注意事項 {#tiflash-compatibility-notes}

TiFlash は、次の状況では TiDB と互換性がありません。

-   TiFlash計算レイヤー内:
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`の 2 つの最大値を加算すると、 `9223372036854775807 + 9223372036854775807` 。 TiDB でのこの計算の予期される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算がTiFlashで実行される場合、エラーなしでオーバーフロー値`-2`が返されます。
    -   ウィンドウ機能はサポートされていません。
    -   TiKV からのデータの読み取りはサポートされていません。
    -   現在、 TiFlashの`sum`関数は文字列型の引数をサポートしていません。ただし、TiDB はコンパイル中に文字列型の引数が`sum`関数に渡されたかどうかを識別できません。したがって、 `select sum(string_col) from t`のようなステートメントを実行すると、 TiFlash は`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。この場合にこのようなエラーを回避するには、この SQL ステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlash の小数除算計算は TiDB のものと互換性がありません。たとえば、10 進数を除算する場合、 TiFlash は常にコンパイルから推測される型を使用して計算を実行します。ただし、TiDB は、コンパイルから推測される型よりも正確な型を使用してこの計算を実行します。したがって、小数除算を含む一部の SQL ステートメントは、 TiDB + TiKV と TiDB + TiFlashで実行すると異なる実行結果を返します。例えば：

        ```sql
        mysql> create table t (a decimal(3,0), b decimal(10, 0));
        Query OK, 0 rows affected (0.07 sec)
        mysql> insert into t values (43, 1044774912);
        Query OK, 1 row affected (0.03 sec)
        mysql> alter table t set tiflash replica 1;
        Query OK, 0 rows affected (0.07 sec)
        mysql> set session tidb_isolation_read_engines='tikv';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        +--------+-----------------------+
        | a/b    | a/b + 0.0000000000001 |
        +--------+-----------------------+
        | 0.0000 |       0.0000000410001 |
        +--------+-----------------------+
        1 row in set (0.00 sec)
        mysql> set session tidb_isolation_read_engines='tiflash';
        Query OK, 0 rows affected (0.00 sec)
        mysql> select a/b, a/b + 0.0000000000001 from t where a/b;
        Empty set (0.01 sec)
        ```

        上の例では、コンパイルから推測される`a/b`の型は、 TiDB とTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`による制約により、 `a/b`の戻り値の型は`0.0000`になる必要があります。 TiDB では、 `a/b`の実行時精度は`Decimal(7,4)`よりも高いため、元のテーブル データは`where a/b`条件によってフィルターされません。ただし、 TiFlashでは、 `a/b`の計算では結果のタイプとして`Decimal(7,4)`が使用されるため、元のテーブル データは`where a/b`条件によってフィルターされます。

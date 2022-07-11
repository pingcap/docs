---
title: TiFlash Compatibility Notes
summary: Learn the TiDB features that are incompatible with TiFlash.
---

# TiFlash互換性に関する注意事項 {#tiflash-compatibility-notes}

次の状況では、TiFlashはTiDBと互換性がありません。

-   TiFlash計算レイヤー：
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`タイプ`9223372036854775807 + 9223372036854775807`の2つの最大値を追加します。 TiDBでのこの計算の予想される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算をTiFlashで実行すると、オーバーフロー値`-2`がエラーなしで返されます。
    -   ウィンドウ関数はサポートされていません。
    -   TiKVからのデータの読み取りはサポートされていません。
    -   現在、TiFlashの`sum`関数は文字列型引数をサポートしていません。ただし、TiDBは、コンパイル中に文字列型の引数が`sum`関数に渡されたかどうかを識別できません。したがって、 `select sum(string_col) from t`と同様のステートメントを実行すると、TiFlashは`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。この場合のこのようなエラーを回避するには、このSQLステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlashの小数除算の計算はTiDBの計算と互換性がありません。たとえば、小数を除算する場合、TiFlashは常にコンパイルから推測されたタイプを使用して計算を実行します。ただし、TiDBは、コンパイルから推測されるタイプよりも正確なタイプを使用してこの計算を実行します。したがって、10進数の除算を含む一部のSQLステートメントは、TiDB+TiKVとTiDB+TiFlashで実行されたときに異なる実行結果を返します。例えば：

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

        上記の例では、コンパイルから推測される`a/b`の型は、TiDBとTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`によって制約され、 `a/b`の返されるタイプは`0.0000`である必要があります。 TiDBでは、 `a/b`の実行時精度は`Decimal(7,4)`よりも高いため、元のテーブルデータは`where a/b`条件によってフィルタリングされません。ただし、TiFlashでは、 `a/b`の計算では結果タイプとして`Decimal(7,4)`が使用されるため、元のテーブルデータは`where a/b`条件でフィルタリングされます。

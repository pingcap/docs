---
title: TiFlash Compatibility Notes
summary: TiFlashと互換性のない TiDB 機能について説明します。
---

# TiFlash互換性に関する注意事項 {#tiflash-compatibility-notes}

次の状況では、 TiFlash はTiDB と互換性がありません。

-   TiFlash計算レイヤーでは:
    -   オーバーフローした数値のチェックはサポートされていません。たとえば、 `BIGINT`型の`9223372036854775807 + 9223372036854775807`の最大値 2 つを加算します。TiDB でのこの計算の予想される動作は、 `ERROR 1690 (22003): BIGINT value is out of range`エラーを返すことです。ただし、この計算をTiFlashで実行すると、エラーなしでオーバーフロー値`-2`が返されます。
    -   ウィンドウ関数はサポートされていません。
    -   TiKV からのデータの読み取りはサポートされていません。
    -   現在、 TiFlashの`sum`関数は文字列型の引数をサポートしていません。しかし、TiDB はコンパイル時に`sum`関数に文字列型の引数が渡されたかどうかを識別できません。そのため、 `select sum(string_col) from t`のようなステートメントを実行すると、 TiFlash は`[FLASH:Coprocessor:Unimplemented] CastStringAsReal is not supported.`エラーを返します。この場合にこのようなエラーを回避するには、この SQL ステートメントを`select sum(cast(string_col as double)) from t`に変更する必要があります。
    -   現在、TiFlash の 10 進除算計算は TiDB のものと互換性がありません。たとえば、10 進除算を行う場合、 TiFlash は常にコンパイルから推測された型を使用して計算を実行します。ただし、TiDB はコンパイルから推測された型よりも正確な型を使用してこの計算を実行します。そのため、10 進除算を含む一部の SQL ステートメントは、TiDB + TiKV で実行した場合と TiDB + TiFlashで実行した場合で異なる実行結果を返します。たとえば、次のようになります。

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

        上記の例では、コンパイルから推論された`a/b`の型は、 TiDB とTiFlashの両方で`Decimal(7,4)`です。 `Decimal(7,4)`の制約により、 `a/b`の戻り型は`0.0000`になります。 TiDB では、 `a/b`の実行時精度は`Decimal(7,4)`よりも高いため、元のテーブル データは`where a/b`条件によってフィルタリングされません。 ただし、 TiFlashでは、 `a/b`の計算で結果の型として`Decimal(7,4)`使用されるため、元のテーブル データは`where a/b`条件によってフィルタリングされます。

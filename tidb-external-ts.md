---
title: Read Historical Data Using the `tidb_external_ts` Variable
summary: tidb_external_ts` 変数を使用して履歴データを読み取る方法を学びます。
---

# <code>tidb_external_ts</code>変数を使用して履歴データを読み取る {#read-historical-data-using-the-code-tidb-external-ts-code-variable}

履歴データの読み取りをサポートするために、TiDB v6.4.0 ではシステム変数[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)が導入されました。このドキュメントでは、このシステム変数を使用して履歴データを読み取る方法と、詳細な使用例について説明します。

## シナリオ {#scenarios}

指定した時点からの履歴データの読み取りは、TiCDCなどのデータレプリケーションツールにとって非常に便利です。データレプリケーションツールが特定の時点より前のデータレプリケーションを完了した後、下流TiDBのシステム変数`tidb_external_ts`設定することで、その時点より前のデータを読み取ることができます。これにより、データレプリケーションによるデータの不整合を防ぐことができます。

## 機能の説明 {#feature-description}

システム変数[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) 、 `tidb_enable_external_ts_read`が有効な場合に読み取る履歴データのタイムスタンプを指定します。

システム変数[`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) 、履歴データを現在のセッションで読み取るか、グローバルで読み取るかを制御します。デフォルト値は`OFF`で、履歴データの読み取り機能は無効であり、 `tidb_external_ts`は無視されます。7 `tidb_enable_external_ts_read`グローバルに`ON`に設定すると、すべてのクエリは`tidb_external_ts`で指定された時刻より前に履歴データを読み取ります。13 `tidb_enable_external_ts_read`特定のセッションのみ`ON`に設定すると、そのセッションのクエリのみが履歴データを読み取ります。

`tidb_enable_external_ts_read`有効にすると、TiDB は読み取り専用になります。すべての書き込みクエリは`ERROR 1836 (HY000): Running in read-only mode`ようなエラーで失敗します。

## 使用例 {#usage-examples}

このセクションでは、 `tidb_external_ts`変数を使用して履歴データを読み取る方法を例とともに説明します。

1.  テーブルを作成し、テーブルにいくつかの行を挿入します。

    ```sql
    CREATE TABLE t (c INT);
    ```

        Query OK, 0 rows affected (0.01 sec)

    ```sql
    INSERT INTO t VALUES (1), (2), (3);
    ```

        Query OK, 3 rows affected (0.00 sec)

2.  表内のデータをビュー。

    ```sql
    SELECT * FROM t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |    2 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

3.  セット`tidb_external_ts` ～ `@@tidb_current_ts` :

    ```sql
    START TRANSACTION;
    SET GLOBAL tidb_external_ts=@@tidb_current_ts;
    COMMIT;
    ```

4.  新しい行を挿入し、挿入されたことを確認します。

    ```sql
    INSERT INTO t VALUES (4);
    ```

        Query OK, 1 row affected (0.001 sec)

    ```sql
    SELECT * FROM t;
    ```

        +------+
        | id   |
        +------+
        |    1 |
        |    2 |
        |    3 |
        |    4 |
        +------+
        4 rows in set (0.00 sec)

5.  `tidb_enable_external_ts_read`を`ON`に設定し、表内のデータを表示します。

    ```sql
    SET tidb_enable_external_ts_read=ON;
    SELECT * FROM t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |    2 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

    新しい行が挿入される前にタイムスタンプに`tidb_external_ts`設定されるため、 `tidb_enable_external_ts_read`有効になった後は新しく挿入された行は返されません。

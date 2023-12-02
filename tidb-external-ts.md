---
title: Read Historical Data Using the `tidb_external_ts` Variable
summary: Learn how to read historical data using the `tidb_external_ts` variable.
---

# <code>tidb_external_ts</code>変数を使用した履歴データの読み取り {#read-historical-data-using-the-code-tidb-external-ts-code-variable}

履歴データの読み取りをサポートするために、TiDB v6.4.0 ではシステム変数[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)が導入されています。このドキュメントでは、このシステム変数を使用して履歴データを読み取る方法について、詳細な使用例を含めて説明します。

## シナリオ {#scenarios}

指定した時点からの履歴データの読み取りは、TiCDC などのデータ レプリケーション ツールで非常に役立ちます。データ レプリケーション ツールが特定の時点より前にデータ レプリケーションを完了した後、ダウンストリーム TiDB の`tidb_external_ts`システム変数を設定して、その時点より前のデータを読み取ることができます。これにより、データの複製によって生じるデータの不整合が防止されます。

## 機能の説明 {#feature-description}

システム変数[`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640)は、 `tidb_enable_external_ts_read`有効な場合に読み取られる履歴データのタイムスタンプを指定します。

システム変数[`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640)は、履歴データを現在のセッションで読み取るかグローバルに読み取るかを制御します。デフォルト値は`OFF`です。これは、履歴データの読み取り機能が無効であり、値`tidb_external_ts`は無視されることを意味します。 `tidb_enable_external_ts_read`がグローバルに`ON`に設定されている場合、すべてのクエリは`tidb_external_ts`で指定された時間より前の履歴データを読み取ります。特定のセッションに対してのみ`tidb_enable_external_ts_read` `ON`に設定されている場合、そのセッション内のクエリのみが履歴データを読み取ります。

`tidb_enable_external_ts_read`を有効にすると、TiDB は読み取り専用になります。すべての書き込みクエリは`ERROR 1836 (HY000): Running in read-only mode`のようなエラーで失敗します。

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

2.  テーブル内のデータをビュー。

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

3.  `tidb_external_ts` ～ `@@tidb_current_ts`を設定：

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

5.  `tidb_enable_external_ts_read`から`ON`を設定し、テーブル内のデータを表示します。

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

    新しい行が挿入される前にタイムスタンプに`tidb_external_ts`が設定されるため、 `tidb_enable_external_ts_read`が有効になった後は新しく挿入された行は返されません。

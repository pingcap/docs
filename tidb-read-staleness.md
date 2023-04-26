---
title: Read Historical Data Using the `tidb_read_staleness` System Variable
summary: Learn how to read historical data using the `tidb_read_staleness` system variable.
---

# <code>tidb_read_staleness</code>システム変数を使用して履歴データを読み取る {#read-historical-data-using-the-code-tidb-read-staleness-code-system-variable}

v5.4 では、履歴データの読み取りをサポートするために、TiDB は新しいシステム変数`tidb_read_staleness`を導入しています。このドキュメントでは、詳細な操作手順を含め、このシステム変数を使用して履歴データを読み取る方法について説明します。

## 機能説明 {#feature-description}

`tidb_read_staleness`システム変数は、現在のセッションで TiDB が読み取ることができる履歴データの時間範囲を設定するために使用されます。この変数のデータ型は int 型で、スコープは`SESSION`です。値を設定した後、TiDB はこの変数によって許可された範囲からできるだけ新しいタイムスタンプを選択し、その後のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKV に対応する履歴バージョンのデータがあるという条件で、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

`tidb_read_staleness`を有効にした後でも、次の操作を実行できます。

-   現在のセッションでデータを挿入、変更、削除するか、DML 操作を実行します。これらのステートメントは`tidb_read_staleness`の影響を受けません。
-   現在のセッションでインタラクティブ トランザクションを開始します。このトランザクション内のクエリは引き続き最新のデータを読み取ります。

履歴データを読み取った後、次の 2 つの方法で最新のデータを読み取ることができます。

-   新しいセッションを開始します。
-   `SET`ステートメントを使用して、変数`tidb_read_staleness`の値を`""`に設定します。

> **ノート：**
>
> レイテンシーを短縮し、ステイル読み取りデータの適時性を向上させるために、TiKV `advance-ts-interval`構成アイテムを変更できます。詳細は[ステイル読み取りのレイテンシーを減らす](/stale-read.md#reduce-stale-read-latency)参照してください。

## 使用例 {#usage-examples}

このセクションでは、例を使用して`tidb_read_staleness`を使用する方法について説明します。

1.  テーブルを作成し、数行のデータをテーブルに挿入します。

    {{< copyable "" >}}

    ```sql
    create table t (c int);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "" >}}

    ```sql
    insert into t values (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2.  テーブル内のデータを確認してください。

    {{< copyable "" >}}

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

3.  データを連続して更新します。

    {{< copyable "" >}}

    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

4.  データが更新されたことを確認します。

    {{< copyable "" >}}

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

5.  `tidb_read_staleness`システム変数を設定します。

    この変数のスコープは`SESSION`です。その値を設定した後、TiDB は、値によって設定された時刻の前に最新バージョンのデータを読み取ります。

    次の設定は、TiDB が 5 秒前から現在までの時間範囲内でできるだけ新しいタイムスタンプを選択し、それを履歴データを読み取るためのタイムスタンプとして使用することを示します。

    {{< copyable "" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **ノート：**
    >
    > -   `tidb_read_staleness`の前に`@`の代わりに`@@`使用します。 `@@`システム変数を意味し、 `@`ユーザー変数を意味します。
    > -   ステップ 3 とステップ 4 で費やした合計時間に従って、履歴時間範囲 (値`tidb_read_staleness` ) を設定する必要があります。そうしないと、履歴データではなく、最新のデータがクエリ結果に表示されます。したがって、操作に費やした時間に応じて、この時間範囲を調整する必要があります。たとえば、この例では、設定された時間範囲が 5 秒であるため、手順 3 と手順 4 を 5 秒以内に完了する必要があります。

    ここで読み取られるデータは、更新前のデータ、つまり履歴データです。

    {{< copyable "" >}}

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

6.  次のようにこの変数の設定を解除すると、TiDB は最新のデータを読み取ることができます。

    {{< copyable "" >}}

    ```sql
    set @@tidb_read_staleness="";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    {{< copyable "" >}}

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

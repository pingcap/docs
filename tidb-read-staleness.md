---
title: Read Historical Data Using the `tidb_read_staleness` System Variable
summary: Learn how to read historical data using the `tidb_read_staleness` system variable.
---

# <code>tidb_read_staleness</code>システム変数を使用して履歴データを読み取る {#read-historical-data-using-the-code-tidb-read-staleness-code-system-variable}

履歴データの読み取りをサポートするために、v5.4では、TiDBは新しいシステム変数`tidb_read_staleness`を導入しています。このドキュメントでは、詳細な操作手順を含め、このシステム変数を介して履歴データを読み取る方法について説明します。

## 機能の説明 {#feature-description}

`tidb_read_staleness`システム変数は、TiDBが現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。この変数のデータ型はint型であり、そのスコープは`SESSION`です。値を設定した後、TiDBはこの変数で許可されている範囲から可能な限り新しいタイムスタンプを選択し、以降のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKVに対応する履歴バージョンのデータがあることを条件として、TiDBは5秒の時間範囲内で可能な限り新しいタイムスタンプを選択します。

`tidb_read_staleness`を有効にした後でも、次の操作を実行できます。

-   現在のセッションでデータを挿入、変更、削除、またはDML操作を実行します。これらのステートメントは`tidb_read_staleness`の影響を受けません。
-   現在のセッションで対話型トランザクションを開始します。このトランザクション内のクエリは、引き続き最新のデータを読み取ります。

履歴データを読み取った後、次の2つの方法で最新のデータを読み取ることができます。

-   新しいセッションを開始します。
-   `SET`ステートメントを使用して、 `tidb_read_staleness`変数の値を`""`に設定します。

## 使用例 {#usage-examples}

このセクションでは、例を使用して`tidb_read_staleness`を使用する方法について説明します。

1.  テーブルを作成し、テーブルに数行のデータを挿入します。

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

2.  表のデータを確認してください。

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

3.  行のデータを更新します。

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

5.  `tidb_read_staleness`のシステム変数を設定します。

    この変数のスコープは`SESSION`です。値を設定した後、TiDBは値で設定された時間より前に最新バージョンのデータを読み取ります。

    次の設定は、TiDBが5秒前から現在までの時間範囲内で可能な限り新しいタイムスタンプを選択し、それを履歴データを読み取るためのタイムスタンプとして使用することを示しています。

    {{< copyable "" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **ノート：**
    >
    > -   `tidb_read_staleness`の前に`@`ではなく`@@`を使用します。 `@@`はシステム変数を意味し、 `@`はユーザー変数を意味します。
    > -   手順3と手順4で費やした合計時間に応じて、履歴時間範囲（値`tidb_read_staleness` ）を設定する必要があります。そうしないと、履歴データではなく、最新のデータがクエリ結果に表示されます。したがって、操作に費やした時間に応じて、この時間範囲を調整する必要があります。たとえば、この例では、設定された時間範囲が5秒であるため、5秒以内にステップ3とステップ4を完了する必要があります。

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

6.  この変数の設定を次のように解除すると、TiDBは最新のデータを読み取ることができます。

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

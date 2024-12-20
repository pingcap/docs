---
title: Read Historical Data Using the `tidb_read_staleness` System Variable
summary: tidb_read_staleness` システム変数を使用して履歴データを読み取る方法を学習します。
---

# <code>tidb_read_staleness</code>システム変数を使用して履歴データを読み取る {#read-historical-data-using-the-code-tidb-read-staleness-code-system-variable}

履歴データの読み取りをサポートするために、TiDB バージョン 5.4 では新しいシステム変数`tidb_read_staleness`が導入されています。このドキュメントでは、詳細な操作手順を含め、このシステム変数を使用して履歴データを読み取る方法について説明します。

## 機能の説明 {#feature-description}

`tidb_read_staleness`システム変数は、TiDB が現在のセッションで読み取ることができる履歴データの時間範囲を設定するために使用されます。この変数のデータ型は int 型で、スコープは`SESSION`です。値を設定すると、TiDB はこの変数で許可されている範囲からできるだけ新しいタイムスタンプを選択し、その後のすべての読み取り操作はこのタイムスタンプに対して実行されます。たとえば、この変数の値が`-5`に設定されている場合、TiKV に対応する履歴バージョンのデータがあるという条件で、TiDB は 5 秒の時間範囲内でできるだけ新しいタイムスタンプを選択します。

`tidb_read_staleness`有効にした後でも、次の操作を実行できます。

-   現在のセッションでデータを挿入、変更、削除したり、DML 操作を実行したりします。これらのステートメントは`tidb_read_staleness`の影響を受けません。
-   現在のセッションで対話型トランザクションを開始します。このトランザクション内のクエリは引き続き最新のデータを読み取ります。

履歴データを読み取った後、次の 2 つの方法で最新データを読み取ることができます。

-   新しいセッションを開始します。
-   `SET`ステートメントを使用して、変数`tidb_read_staleness`の値を`""`に設定します。

> **注記：**
>
> レイテンシーを減らし、ステイル読み取りデータの適時性を向上させるには、TiKV `advance-ts-interval`構成項目を変更します。詳細については[ステイル読み取りのレイテンシーを削減](/stale-read.md#reduce-stale-read-latency)参照してください。

## 使用例 {#usage-examples}

このセクションでは、 `tidb_read_staleness`使用方法を例とともに説明します。

1.  テーブルを作成し、テーブルに数行のデータを挿入します。

    ```sql
    create table t (c int);
    ```

        Query OK, 0 rows affected (0.01 sec)

    ```sql
    insert into t values (1), (2), (3);
    ```

        Query OK, 3 rows affected (0.00 sec)

2.  表のデータを確認してください:

    ```sql
    select * from t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |    2 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

3.  行内のデータを更新します。

    ```sql
    update t set c=22 where c=2;
    ```

        Query OK, 1 row affected (0.00 sec)

4.  データが更新されたことを確認します。

    ```sql
    select * from t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |   22 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

5.  システム変数`tidb_read_staleness`を設定します。

    この変数のスコープは`SESSION`です。値を設定すると、TiDB は値で設定された時間より前に最新バージョンのデータを読み取ります。

    次の設定は、TiDB が 5 秒前から現在までの時間範囲内で可能な限り新しいタイムスタンプを選択し、それを履歴データの読み取り用のタイムスタンプとして使用することを示しています。

    ```sql
    set @@tidb_read_staleness="-5";
    ```

        Query OK, 0 rows affected (0.00 sec)

    > **注記：**
    >
    > -   `tidb_read_staleness`前には`@`ではなく`@@`使用します。7 `@@`システム変数、 `@`ユーザー変数を意味します。
    > -   手順 3 と手順 4 に費やした合計時間に応じて、履歴時間範囲 (値`tidb_read_staleness` ) を設定する必要があります。そうしないと、履歴データではなく最新のデータがクエリ結果に表示されます。したがって、操作に費やした時間に応じてこの時間範囲を調整する必要があります。たとえば、この例では、設定された時間範囲は 5 秒であるため、手順 3 と手順 4 を 5 秒以内に完了する必要があります。

    ここで読み取られるデータは更新前のデータ、つまり履歴データです。

    ```sql
    select * from t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |    2 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

6.  次のようにこの変数を設定解除すると、TiDB は最新のデータを読み取ることができます。

    ```sql
    set @@tidb_read_staleness="";
    ```

        Query OK, 0 rows affected (0.00 sec)

    ```sql
    select * from t;
    ```

        +------+
        | c    |
        +------+
        |    1 |
        |   22 |
        |    3 |
        +------+
        3 rows in set (0.00 sec)

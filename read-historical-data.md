---
title: Read Historical Data Using the System Variable `tidb_snapshot`
summary: Learn about how TiDB reads data from history versions using the system variable `tidb_snapshot`.
---

# システム変数<code>tidb_snapshot</code>を使用して履歴データを読み取る {#read-historical-data-using-the-system-variable-code-tidb-snapshot-code}

このドキュメントでは、システム変数`tidb_snapshot`を使用して履歴バージョンからデータを読み取る方法について説明します。これには、履歴データを保存するための具体的な使用例と戦略が含まれます。

> **ノート：**
>
> [古い読み取り](/stale-read.md)機能を使用して履歴データを読み取ることもできます。これはより推奨されます。

## 機能の説明 {#feature-description}

TiDBは、特別なクライアントやドライバーを使用せずに、標準のSQLインターフェイスを使用して履歴データを直接読み取る機能を実装しています。

> **ノート：**
>
> -   データが更新または削除された場合でも、SQLインターフェイスを使用してその履歴バージョンを読み取ることができます。
> -   履歴データを読み取る場合、TiDBは、現在のテーブル構造が異なっていても、古いテーブル構造のデータを返します。

## TiDBが履歴バージョンからデータを読み取る方法 {#how-tidb-reads-data-from-history-versions}

[`tidb_snapshot`](/system-variables.md#tidb_snapshot)システム変数は、履歴データの読み取りをサポートするために導入されました。 `tidb_snapshot`の変数について：

-   変数は`SESSION`スコープで有効です。
-   その値は、 `SET`ステートメントを使用して変更できます。
-   変数のデータ型はテキストです。
-   この変数は、TSO（Timestamp Oracle）と日時を受け入れます。 TSOは、PDから取得する世界的にユニークなタイムサービスです。使用可能な日時の形式は「2016-10-0816：45：26.999」です。通常、日時は「2016-10-0816:45:26」のように2番目の精度で設定できます。
-   変数が設定されると、TiDBは、データ構造のためだけに、その値をタイムスタンプとして使用してスナップショットを作成し、オーバーヘッドはありません。その後、 `SELECT`の操作すべてがこのスナップショットからデータを読み取ります。

> **ノート：**
>
> TiDBトランザクションのタイムスタンプはPlacementDriver（PD）によって割り当てられるため、保存されたデータのバージョンもPDによって割り当てられたタイムスタンプに基づいてマークされます。スナップショットが作成されるとき、バージョン番号は`tidb_snapshot`変数の値に基づいています。 TiDBサーバーとPDサーバーの現地時間に大きな違いがある場合は、PDサーバーの時間を使用してください。

履歴バージョンからデータを読み取った後、現在のセッションを終了するか、 `SET`ステートメントを使用して`tidb_snapshot`変数の値を &quot;&quot;（空の文字列）に設定することにより、最新バージョンからデータを読み取ることができます。

## TiDBがデータバージョンを管理する方法 {#how-tidb-manages-the-data-versions}

TiDBは、データバージョンを管理するためにマルチバージョン同時実行制御（MVCC）を実装しています。データオブジェクトをインプレースで更新/削除するのではなく、更新/削除するたびに新しいバージョンのデータオブジェクトが作成されるため、データの履歴バージョンが保持されます。ただし、すべてのバージョンが保持されるわけではありません。バージョンが特定の時間より古い場合、それらは完全に削除され、ストレージの占有率と、履歴バージョンが多すぎるために発生するパフォーマンスのオーバーヘッドが削減されます。

TiDBでは、ガベージコレクション（GC）が定期的に実行され、廃止されたデータバージョンが削除されます。 GCの詳細については、 [TiDBガベージコレクション（GC）](/garbage-collection-overview.md)を参照してください。

次の点に特に注意してください。

-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) ：このシステム変数は、以前の変更の保持時間を構成するために使用されます（デフォルト： `10m0s` ）。
-   `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'`の出力。これは、最大の履歴データを読み取ることができる現在の`safePoint`です。ガベージコレクションプロセスが実行されるたびに更新されます。

## 例 {#example}

1.  初期段階で、テーブルを作成し、データのいくつかの行を挿入します。

    ```sql
    mysql> create table t (c int);
    Query OK, 0 rows affected (0.01 sec)

    mysql> insert into t values (1), (2), (3);
    Query OK, 3 rows affected (0.00 sec)
    ```

2.  表のデータを表示します。

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3.  テーブルのタイムスタンプを表示します。

    ```sql
    mysql> select now();
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4.  1行のデータを更新します。

    ```sql
    mysql> update t set c=22 where c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

5.  データが更新されていることを確認してください。

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6.  スコープがSessionである`tidb_snapshot`の変数を設定します。変数は、値の前の最新バージョンを読み取ることができるように設定されます。

    > **ノート：**
    >
    > この例では、値は更新操作の前の時間に設定されています。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **ノート：**
    >
    > `@@`はシステム変数を示し、 `@`はユーザー変数を示すために使用されるため、 `tidb_snapshot`の前に`@`ではなく`@@`を使用する必要があります。

    **結果：**次のステートメントからの読み取りは、更新操作前のデータであり、履歴データです。

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

7.  `tidb_snapshot`の変数を&quot;&quot;（空の文字列）に設定すると、最新バージョンからデータを読み取ることができます。

    ```sql
    mysql> set @@tidb_snapshot="";
    Query OK, 0 rows affected (0.00 sec)
    ```

    ```sql
    mysql> select * from t;
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

    > **ノート：**
    >
    > `@@`はシステム変数を示し、 `@`はユーザー変数を示すために使用されるため、 `tidb_snapshot`の前に`@`ではなく`@@`を使用する必要があります。

## 履歴データを復元する方法 {#how-to-restore-historical-data}

古いバージョンからデータを復元する前に、作業中にガベージコレクション（GC）が履歴データをクリアしないことを確認してください。これは、次の例に示すように`tidb_gc_life_time`変数を設定することで実行できます。復元後、変数を前の値に戻すことを忘れないでください。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **ノート：**
>
> GCの寿命をデフォルトの10分から30分以上に増やすと、追加のバージョンの行が保持され、より多くのディスク容量が必要になる場合があります。これは、データの読み取り中にTiDBが同じ行のこれらの追加バージョンをスキップする必要がある場合のスキャンなど、特定の操作のパフォーマンスにも影響を与える可能性があります。

古いバージョンからデータを復元するには、次のいずれかの方法を使用できます。

-   単純なケースでは、 `tidb_snapshot`変数を設定して出力をコピーアンドペーストした後に`SELECT`を使用するか、 `SELECT ... INTO LOCAL OUTFLE`を使用して後でデータをインポートするために`LOAD DATA`を使用します。

-   [Dumpling](/dumpling-overview.md#export-historical-data-snapshot-of-tidb)を使用して、履歴スナップショットをエクスポートします。Dumplingは、より大きなデータセットのエクスポートでうまく機能します。

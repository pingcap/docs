---
title: Read Historical Data Using the System Variable `tidb_snapshot`
summary: Learn about how TiDB reads data from history versions using the system variable `tidb_snapshot`.
---

# システム変数<code>tidb_snapshot</code>を使用した履歴データの読み取り {#read-historical-data-using-the-system-variable-code-tidb-snapshot-code}

このドキュメントでは、システム変数`tidb_snapshot`を使用して履歴バージョンからデータを読み取る方法について説明します。これには、履歴データを保存するための具体的な使用例や戦略も含まれます。

> **注記：**
>
> [ステイル読み取り](/stale-read.md)機能を使用して履歴データを読み取ることもできますが、これをお勧めします。

## 機能の説明 {#feature-description}

TiDB は、特別なクライアントやドライバーを使用せずに、標準 SQL インターフェイスを使用して履歴データを直接読み取る機能を実装しています。

> **注記：**
>
> -   データが更新または削除された場合でも、SQL インターフェイスを使用してその履歴バージョンを読み取ることができます。
> -   履歴データを読み取る場合、TiDB は、現在のテーブル構造が異なっていても、古いテーブル構造でデータを返します。

## TiDB が履歴バージョンからデータを読み取る方法 {#how-tidb-reads-data-from-history-versions}

[`tidb_snapshot`](/system-variables.md#tidb_snapshot)システム変数は、履歴データの読み取りをサポートするために導入されました。 `tidb_snapshot`変数について:

-   変数は`SESSION`スコープで有効です。
-   その値は`SET`ステートメントを使用して変更できます。
-   変数のデータ型はテキストです。
-   変数は TSO (Timestamp Oracle) と日時を受け入れます。 TSO は、PD から取得される、世界的に一意の時刻サービスです。受け入れられる日時形式は「2016-10-08 16:45:26.999」です。通常、日時は秒精度を使用して設定できます (例: &quot;2016-10-08 16:45:26&quot;)。
-   変数が設定されると、TiDB はその値をタイムスタンプとして使用して、データ構造のためだけにスナップショットを作成し、オーバーヘッドはありません。その後、すべての`SELECT`操作がこのスナップショットからデータを読み取ります。

> **注記：**
>
> TiDB トランザクションのタイムスタンプは配置Driver(PD) によって割り当てられるため、保存されたデータのバージョンも PD によって割り当てられたタイムスタンプに基づいてマークされます。スナップショットが作成されるとき、バージョン番号は`tidb_snapshot`変数の値に基づきます。 TiDBサーバーと PDサーバーのローカル時刻に大きな差がある場合は、PDサーバーの時刻を使用します。

履歴バージョンからデータを読み取った後、現在のセッションを終了するか、 `SET`ステートメントを使用して`tidb_snapshot`変数の値を &quot;&quot; (空の文字列) に設定することで、最新バージョンからデータを読み取ることができます。

## TiDB がデータ バージョンを管理する方法 {#how-tidb-manages-the-data-versions}

TiDB は、データ バージョンを管理するためにマルチバージョン同時実行制御 (MVCC) を実装しています。データ オブジェクトをその場で更新/削除するのではなく、更新/削除のたびにデータ オブジェクトの新しいバージョンが作成されるため、データの履歴バージョンが保持されます。ただし、すべてのバージョンが保存されているわけではありません。バージョンが特定の時点よりも古い場合、storage占有量と、履歴バージョンが多すぎることによって生じるパフォーマンスのオーバーヘッドを削減するために、バージョンは完全に削除されます。

TiDB では、ガベージ コレクション (GC) が定期的に実行され、古いデータ バージョンが削除されます。 GC の詳細については、 [TiDB ガベージ コレクション (GC)](/garbage-collection-overview.md)を参照してください。

以下の点に特に注意してください。

-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) : このシステム変数は、以前の変更の保持時間を構成するために使用されます (デフォルト: `10m0s` )。
-   `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'`の出力。過去のデータが読めるのは現在`safePoint`までです。ガベージコレクションプロセスが実行されるたびに更新されます。

## 例 {#example}

1.  最初の段階で、テーブルを作成し、いくつかのデータ行を挿入します。

    ```sql
    mysql> create table t (c int);
    Query OK, 0 rows affected (0.01 sec)

    mysql> insert into t values (1), (2), (3);
    Query OK, 3 rows affected (0.00 sec)
    ```

2.  テーブル内のデータをビュー。

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

3.  テーブルのタイムスタンプをビュー。

    ```sql
    mysql> select now();
    +---------------------+
    | now()               |
    +---------------------+
    | 2016-10-08 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)
    ```

4.  1 行のデータを更新します。

    ```sql
    mysql> update t set c=22 where c=2;
    Query OK, 1 row affected (0.00 sec)
    ```

5.  データが更新されていることを確認します。

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

6.  スコープがセッションである`tidb_snapshot`変数を設定します。変数はその値よりも前の最新バージョンを読み込めるように設定されています。

    > **注記：**
    >
    > この例では、値は更新操作前の時間に設定されます。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注記：**
    >
    > `@@`システム変数を表すのに使用され、 `@`はユーザー変数を表すために使用されるため、 `@` `tidb_snapshot`前に`@@`ではなく 1 を使用する必要があります。

    **結果:**次のステートメントから読み取られたデータは、更新操作前のデータ、つまり履歴データです。

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

7.  `tidb_snapshot`変数を &quot;&quot; (空の文字列) に設定すると、最新バージョンからデータを読み取ることができます。

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

    > **注記：**
    >
    > `@@`システム変数を表すのに使用され、 `@`はユーザー変数を表すために使用されるため、 `@` `tidb_snapshot`前に`@@`ではなく 1 を使用する必要があります。

## 履歴データを復元する方法 {#how-to-restore-historical-data}

古いバージョンからデータを復元する前に、作業中にガベージ コレクション (GC) によって履歴データが消去されないことを確認してください。これは、次の例に示すように`tidb_gc_life_time`変数を設定することで実行できます。復元後に変数を前の値に戻すことを忘れないでください。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **注記：**
>
> GC 存続時間をデフォルトの 10 分から 30 分以上に延長すると、行の追加バージョンが保持されることになり、より多くのディスク領域が必要になる可能性があります。これは、TiDB がデータ読み取り中に同じ行のこれらの追加バージョンをスキップする必要がある場合のスキャンなど、特定の操作のパフォーマンスにも影響を与える可能性があります。

古いバージョンからデータを復元するには、次のいずれかの方法を使用できます。

-   単純な場合は、変数`tidb_snapshot`設定した後に[`SELECT`](/sql-statements/sql-statement-select.md)使用して出力をコピー＆ペーストするか、 `SELECT ... INTO OUTFILE`を使用してから[`LOAD DATA`](/sql-statements/sql-statement-load-data.md)を使用して後でデータをインポートします。

-   履歴スナップショットをエクスポートするには[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-historical-data-snapshots-of-tidb)使用します。 Dumpling は、大規模なデータ セットのエクスポートに優れたパフォーマンスを発揮します。

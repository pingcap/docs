---
title: Read Historical Data Using the System Variable `tidb_snapshot`
summary: Learn about how TiDB reads data from history versions using the system variable `tidb_snapshot`.
---

# システム変数<code>tidb_snapshot</code>を使用して履歴データを読み取る {#read-historical-data-using-the-system-variable-code-tidb-snapshot-code}

このドキュメントでは、システム変数`tidb_snapshot`を使用して履歴バージョンからデータを読み取る方法について説明します。これには、具体的な使用例と履歴データを保存するための戦略が含まれます。

> **ノート：**
>
> [ステイル読み取り](/stale-read.md)機能を使用して履歴データを読み取ることもできますが、これはより推奨されます。

## 機能説明 {#feature-description}

TiDB は、特別なクライアントやドライバーを使用せずに、標準の SQL インターフェイスを直接使用して履歴データを読み取る機能を実装しています。

> **ノート：**
>
> -   データが更新または削除された場合でも、その履歴バージョンは SQL インターフェイスを使用して読み取ることができます。
> -   履歴データを読み取る場合、TiDB は、現在のテーブル構造が異なっていても、古いテーブル構造のデータを返します。

## TiDB が履歴バージョンからデータを読み取る方法 {#how-tidb-reads-data-from-history-versions}

履歴データの読み取りをサポートするために、 [`tidb_snapshot`](/system-variables.md#tidb_snapshot)システム変数が導入されました。 `tidb_snapshot`変数について:

-   変数は`SESSION`スコープで有効です。
-   その値は、 `SET`ステートメントを使用して変更できます。
-   変数のデータ型はテキストです。
-   この変数は、TSO (Timestamp Oracle) と日時を受け入れます。 TSO は、PD から取得されるグローバルに固有のタイム サービスです。許容される日時形式は「2016-10-08 16:45:26.999」です。通常、日時は秒精度を使用して設定できます (例: &quot;2016-10-08 16:45:26&quot;)。
-   変数が設定されると、TiDB はその値をタイムスタンプとして使用してスナップショットを作成します。これはデータ構造のためだけであり、オーバーヘッドはありません。その後、すべての`SELECT`操作がこのスナップショットからデータを読み取ります。

> **ノート：**
>
> TiDB トランザクションのタイムスタンプは Placement Driver (PD) によって割り当てられるため、格納されたデータのバージョンも、PD によって割り当てられたタイムスタンプに基づいてマークされます。スナップショットが作成されると、バージョン番号は`tidb_snapshot`変数の値に基づきます。 TiDBサーバーと PDサーバーのローカル時刻に大きな差がある場合は、PDサーバーの時刻を使用します。

履歴バージョンからデータを読み取った後、現在のセッションを終了するか、 `SET`ステートメントを使用して`tidb_snapshot`変数の値を &quot;&quot; (空の文字列) に設定することにより、最新バージョンからデータを読み取ることができます。

## TiDB がデータのバージョンを管理する方法 {#how-tidb-manages-the-data-versions}

TiDB は、Multi-Version Concurrency Control (MVCC) を実装して、データのバージョンを管理します。データ オブジェクトをその場で更新/削除するのではなく、更新/削除するたびに新しいバージョンのデータ オブジェクトが作成されるため、データの履歴バージョンが保持されます。ただし、すべてのバージョンが保持されるわけではありません。バージョンが特定の時間よりも古い場合、それらは完全に削除され、storageの占有率と、履歴バージョンが多すぎることによるパフォーマンスのオーバーヘッドが削減されます。

TiDB では、ガベージ コレクション (GC) が定期的に実行され、古いデータ バージョンが削除されます。 GC の詳細については、 [TiDB ガベージ コレクション (GC)](/garbage-collection-overview.md)を参照してください。

次の点に特に注意してください。

-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) : このシステム変数は、以前の変更の保持時間を構成するために使用されます (デフォルト: `10m0s` )。
-   `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'`の出力。これまでの履歴データを読み取ることができる現在の`safePoint`です。ガベージコレクションプロセスが実行されるたびに更新されます。

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

6.  スコープがセッションである`tidb_snapshot`変数を設定します。変数は、値の前の最新バージョンが読み取れるように設定されています。

    > **ノート：**
    >
    > この例では、値は更新操作の前の時間に設定されます。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **ノート：**
    >
    > `@@`システム変数を表すために使用され、 `@`はユーザー変数を表すために使用されるため、 `@` `tidb_snapshot`前に`@@`ではなく 1 を使用する必要があります。

    **結果:**次のステートメントから読み取られるのは、履歴データである更新操作の前のデータです。

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

    > **ノート：**
    >
    > `@@`システム変数を表すために使用され、 `@`はユーザー変数を表すために使用されるため、 `@` `tidb_snapshot`前に`@@`ではなく 1 を使用する必要があります。

## 履歴データを復元する方法 {#how-to-restore-historical-data}

古いバージョンからデータを復元する前に、作業中にガベージ コレクション (GC) が履歴データを消去しないことを確認してください。これは、次の例に示すように`tidb_gc_life_time`変数を設定することで実行できます。復元後に変数を以前の値に戻すことを忘れないでください。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **ノート：**
>
> GC の有効期間をデフォルトの 10 分から 30 分以上に増やすと、追加のバージョンの行が保持されるため、より多くのディスク領域が必要になる場合があります。これは、TiDB がデータ読み取り中に同じ行のこれらの追加バージョンをスキップする必要がある場合のスキャンなど、特定の操作のパフォーマンスにも影響を与える可能性があります。

古いバージョンからデータを復元するには、次のいずれかの方法を使用できます。

-   単純なケースでは、変数`tidb_snapshot`設定した後に`SELECT`使用して出力をコピー アンド ペーストするか、 `SELECT ... INTO LOCAL OUTFLE`使用して`LOAD DATA`を使用して後でデータをインポートします。

-   履歴スナップショットをエクスポートするには、 [Dumpling](/dumpling-overview.md#export-historical-data-snapshots-of-tidb)を使用します。 Dumpling は、より大きなデータ セットのエクスポートに適しています。

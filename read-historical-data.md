---
title: Read Historical Data Using the System Variable `tidb_snapshot`
summary: システム変数 tidb_snapshot` を使用して、TiDB が履歴バージョンからデータを読み取る方法について説明します。
---

# システム変数<code>tidb_snapshot</code>を使用して履歴データを読み取る {#read-historical-data-using-the-system-variable-code-tidb-snapshot-code}

このドキュメントでは、システム変数`tidb_snapshot`使用して履歴バージョンからデータを読み取る方法について説明します。これには、履歴データを保存するための具体的な使用例と戦略も含まれます。

> **注記：**
>
> [ステイル読み取り](/stale-read.md)機能を使用して履歴データを読み取ることもできます。こちらの方がより推奨されます。

## 機能の説明 {#feature-description}

TiDB は、特別なクライアントやドライバーを使用せずに、標準の SQL インターフェースを使用して履歴データを直接読み取る機能を実装しています。

> **注記：**
>
> -   データが更新または削除された場合でも、SQL インターフェースを使用してその履歴バージョンを読み取ることができます。
> -   履歴データを読み取る場合、TiDB は、現在のテーブル構造が異なっていても、古いテーブル構造を持つデータを返します。

## TiDBが履歴バージョンからデータを読み取る方法 {#how-tidb-reads-data-from-history-versions}

[`tidb_snapshot`](/system-variables.md#tidb_snapshot)のシステム変数は、履歴データの読み取りをサポートするために導入されました。3 `tidb_snapshot`の変数について：

-   変数は`SESSION`スコープ内で有効です。
-   その値は`SET`ステートメントを使用して変更できます。
-   変数のデータ型はテキストです。
-   この変数はTSO（Timestamp Oracle）とdatetimeを受け入れます。TSOはPDから取得される、グローバルに一意なタイムサービスです。受け入れられるdatetimeの形式は「2016-10-08 16:45:26.999」です。通常、datetimeは秒単位の精度で設定できます（例：「2016-10-08 16:45:26」）。
-   変数が設定されると、TiDBはその値をタイムスタンプとしてスナップショットを作成します。これはデータ構造のみを対象としており、オーバーヘッドは発生しません。その後、すべての`SELECT`操作はこのスナップショットからデータを読み取ります。

> **注記：**
>
> TiDBトランザクションのタイムスタンプはPlacement Driver （PD）によって割り当てられるため、保存されたデータのバージョンもPDによって割り当てられたタイムスタンプに基づいてマークされます。スナップショットが作成される際、バージョン番号は`tidb_snapshot`変数の値に基づいて決定されます。TiDBサーバーとPDサーバーのローカル時刻に大きな差がある場合は、PDサーバーの時刻を使用してください。

履歴バージョンからデータを読み取った後、現在のセッションを終了するか、 `SET`ステートメントを使用して`tidb_snapshot`変数の値を &quot;&quot; (空の文字列) に設定することで、最新バージョンからデータを読み取ることができます。

## TiDBがデータバージョンを管理する方法 {#how-tidb-manages-the-data-versions}

TiDBは、データのバージョン管理にマルチバージョン同時実行制御（MVCC）を実装しています。データの履歴バージョンは保持されます。これは、更新/削除のたびにデータオブジェクトの新しいバージョンが作成されるためです。データオブジェクトをその場で更新/削除するのではなく、新しいバージョンが作成されます。ただし、すべてのバージョンが保持されるわけではありません。特定の時間よりも古いバージョンは完全に削除され、履歴バージョンの過剰によって発生するstorageの占有量とパフォーマンスのオーバーヘッドを削減します。

TiDBでは、ガベージコレクション（GC）が定期的に実行され、古いデータバージョンが削除されます。GCの詳細については、 [TiDB ガベージコレクション (GC)](/garbage-collection-overview.md)参照してください。

以下の点に特に注意してください。

-   [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) : このシステム変数は、以前の変更の保持時間を構成するために使用されます (デフォルト: `10m0s` )。
-   `SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point'`の出力。これは、履歴データを読み取れる現在の`safePoint`です。ガベージコレクションプロセスが実行されるたびに更新されます。

## 例 {#example}

1.  初期段階では、テーブルを作成し、いくつかの行のデータを挿入します。

    ```sql
    mysql> create table t (c int);
    Query OK, 0 rows affected (0.01 sec)

    mysql> insert into t values (1), (2), (3);
    Query OK, 3 rows affected (0.00 sec)
    ```

2.  表内のデータをビュー。

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

6.  スコープがセッションである変数を`tidb_snapshot`設定します。この変数は、値の直前のバージョンを読み取れるように設定されます。

    > **注記：**
    >
    > この例では、値は更新操作前の時間に設定されます。

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **注記：**
    >
    > `@@`システム変数を示すのに使用され、 `@`ユーザー変数を示すのに使用されるため、 `tidb_snapshot`前に`@`ではなく`@@`使用する必要があります。

    **結果:**次のステートメントから読み取られるのは、更新操作前のデータ、つまり履歴データです。

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

7.  変数`tidb_snapshot` &quot;&quot; (空の文字列) に設定すると、最新バージョンからデータを読み取ることができます。

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
    > `@@`システム変数を示すのに使用され、 `@`ユーザー変数を示すのに使用されるため、 `tidb_snapshot`前に`@`ではなく`@@`使用する必要があります。

## 履歴データを復元する方法 {#how-to-restore-historical-data}

以前のバージョンからデータを復元する前に、作業中にガベージコレクション（GC）によって履歴データが消去されないように注意してください。これは、以下の例のように変数`tidb_gc_life_time`設定することで実現できます。復元後は、この変数を以前の値に戻すことを忘れないでください。

```sql
SET GLOBAL tidb_gc_life_time="60m";
```

> **注記：**
>
> GCの有効期間をデフォルトの10分から30分以上に延長すると、行の追加バージョンが保持されることになり、より多くのディスク容量が必要になる可能性があります。また、TiDBがデータ読み取り時に同じ行の追加バージョンをスキップする必要があるため、スキャンなどの特定の操作のパフォーマンスにも影響が出る可能性があります。

以前のバージョンからデータを復元するには、次のいずれかの方法を使用できます。

-   単純なケースでは、変数`tidb_snapshot`設定した後に[`SELECT`](/sql-statements/sql-statement-select.md)使用して出力をコピーして貼り付けるか、 `SELECT ... INTO OUTFILE`使用し、後で[`LOAD DATA`](/sql-statements/sql-statement-load-data.md)使用してデータをインポートします。

-   履歴スナップショットをエクスポートするには[Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview#export-historical-data-snapshots-of-tidb)使用します。Dumplingは、より大きなデータセットのエクスポートに適しています。

---
title: Read Historical Data Using the `AS OF TIMESTAMP` Clause
summary: AS OF TIMESTAMP` ステートメント句を使用して履歴データを読み取る方法を学習します。
---

# <code>AS OF TIMESTAMP</code>句を使用して履歴データを読み取る {#read-historical-data-using-the-code-as-of-timestamp-code-clause}

このドキュメントでは、 `AS OF TIMESTAMP`句を使用して[ステイル読み取り](/stale-read.md)機能を実行し、TiDB 内の履歴データを読み取る方法について説明します。具体的な使用例と履歴データを保存するための戦略も説明します。

TiDBは、特別なクライアントやドライバーを必要とせず、標準SQLインターフェース（ `AS OF TIMESTAMP` SQL句）を介して履歴データの読み取りをサポートします。データが更新または削除された後でも、このSQLインターフェースを使用して更新または削除前の履歴データを読み取ることができます。

> **注記：**
>
> 履歴データを読み取る場合、TiDB は、現在のテーブル構造が異なっていても、古いテーブル構造を持つデータを返します。

## 構文 {#syntax}

`AS OF TIMESTAMP`節は次の 3 つの方法で使用できます。

-   [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
-   [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
-   [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

正確な時刻を指定したい場合は、 `AS OF TIMESTAMP`節に datetime 値を設定するか、time 関数を使用します。datetime の形式は「2016-10-08 16:45:26.999」のように、最小の時間単位はミリ秒ですが、ほとんどの場合、datetime を指定するには「2016-10-08 16:45:26」のように秒単位で十分です。3 関数を使用して、現在時刻を`NOW(3)`秒単位で取得することもできます。数秒前のデータを読み取りたい場合は、 `NOW() - INTERVAL 10 SECOND`のような式を使用することを**お勧めします**。

時間範囲を指定する場合は、句内で[`TIDB_BOUNDED_STALENESS()`](/functions-and-operators/tidb-functions.md#tidb_bounded_staleness)関数を使用できます。この関数を使用すると、TiDB は指定された時間範囲内で適切なタイムスタンプを選択します。「適切」とは、このタイムスタンプより前に開始され、アクセス先のレプリカにコミットされていないトランザクションがないことを意味します。つまり、TiDB はアクセス先のレプリカに対して読み取り操作を実行でき、読み取り操作がブロックされていないことを意味します。この関数を呼び出すには`TIDB_BOUNDED_STALENESS(t1, t2)`使用する必要があります。5 と`t2` `t1`範囲の両端であり、datetime 値または時間関数を使用して指定できます。

`AS OF TIMESTAMP`節の例をいくつか示します。

-   `AS OF TIMESTAMP '2016-10-08 16:45:26'` : 2016 年 10 月 8 日 16:45:26 に保存された最新のデータを読み取るように TiDB に指示します。
-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` : TiDB に 10 秒前に保存された最新のデータを読み取るように指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` : 2016 年 10 月 8 日の 16:45:26 から 16:45:29 までの範囲内でできるだけ新しいデータを読み取るように TiDB に指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` : 20 秒前から現在までの時間範囲内で可能な限り新しいデータを読み取るように TiDB に指示します。

> **注記：**
>
> タイムスタンプの指定に加えて、 `AS OF TIMESTAMP`句の最も一般的な用途は、数秒前のデータを読み取ることです。この方法を使用する場合は、5秒より前の履歴データを読み取ることをお勧めします。
>
> ステイル読み取りを使用する場合は、TiDB ノードと PD ノードに NTP サービスを導入する必要があります。これにより、TiDB が使用する指定タイムスタンプが最新の TSO 割り当て進捗状況よりも先になる（数秒先になるなど）状況や、GC セーフポイントのタイムスタンプよりも後になる状況を回避できます。指定タイムスタンプがサービススコープを超える場合、TiDB はエラーを返します。
>
> レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させるには、TiKV `advance-ts-interval`設定項目を変更します。詳細は[ステイル読み取りのレイテンシーを削減](/stale-read.md#reduce-stale-read-latency)ご覧ください。

## 使用例 {#usage-examples}

このセクションでは、いくつかの例を用いて、 `AS OF TIMESTAMP`節の様々な使用方法を説明します。まず、リカバリ用のデータの準備方法を紹介し、次に`SELECT` 、 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 、 `SET TRANSACTION READ ONLY AS OF TIMESTAMP`でそれぞれ`AS OF TIMESTAMP`使用する方法を示します。

### データサンプルを準備する {#prepare-data-sample}

リカバリ用のデータを準備するには、まずテーブルを作成し、いくつかの行のデータを挿入します。

```sql
create table t (c int);
```

    Query OK, 0 rows affected (0.01 sec)

```sql
insert into t values (1), (2), (3);
```

    Query OK, 3 rows affected (0.00 sec)

表内のデータをビュー。

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

現在の時刻をビュー:

```sql
select now();
```

    +---------------------+
    | now()               |
    +---------------------+
    | 2021-05-26 16:45:26 |
    +---------------------+
    1 row in set (0.00 sec)

行内のデータを更新します。

```sql
update t set c=22 where c=2;
```

    Query OK, 1 row affected (0.00 sec)

行のデータが更新されていることを確認します。

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

### <code>SELECT</code>文を使用して履歴データを読み取る {#read-historical-data-using-the-code-select-code-statement}

[`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)ステートメントを使用すると、過去の時点からデータを読み取ることができます。

```sql
select * from t as of timestamp '2021-05-26 16:45:26';
```

    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)

> **注記：**
>
> `SELECT`ステートメントで複数のテーブルを読み取る場合、TIMESTAMP EXPRESSIONの形式が一貫していることを確認する必要があります。例えば、 `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;`ようになります。さらに、 `SELECT`ステートメントで関連するテーブルの`AS OF`情報を指定する必要があります。そうしないと、 `SELECT`ステートメントはデフォルトで最新のデータを読み取ります。

### <code>START TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取る {#read-historical-data-using-the-code-start-transaction-read-only-as-of-timestamp-code-statement}

[`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)ステートメントを使用すると、過去の特定の時点に基づいて読み取り専用トランザクションを開始できます。このトランザクションは、指定された時点の履歴データを読み取ります。

```sql
start transaction read only as of timestamp '2021-05-26 16:45:26';
```

    Query OK, 0 rows affected (0.00 sec)

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

```sql
commit;
```

    Query OK, 0 rows affected (0.00 sec)

トランザクションがコミットされた後、最新のデータを読み取ることができます。

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

> **注記：**
>
> ステートメント`START TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始すると、それは読み取り専用トランザクションになります。このトランザクションでは書き込み操作は拒否されます。

### <code>SET TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取る {#read-historical-data-using-the-code-set-transaction-read-only-as-of-timestamp-code-statement}

[`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)ステートメントを使用すると、次のトランザクションを過去の特定の時点に基づく読み取り専用トランザクションとして設定できます。このトランザクションは、指定された時点の履歴データを読み取ります。

```sql
set transaction read only as of timestamp '2021-05-26 16:45:26';
```

    Query OK, 0 rows affected (0.00 sec)

```sql
begin;
```

    Query OK, 0 rows affected (0.00 sec)

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

```sql
commit;
```

    Query OK, 0 rows affected (0.00 sec)

トランザクションがコミットされた後、最新のデータを読み取ることができます。

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

> **注記：**
>
> ステートメント`SET TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始すると、それは読み取り専用トランザクションになります。このトランザクションでは書き込み操作は拒否されます。

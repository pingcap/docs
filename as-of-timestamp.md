---
title: Read Historical Data Using the `AS OF TIMESTAMP` Clause
summary: Learn how to read historical data using the `AS OF TIMESTAMP` statement clause.
---

# <code>AS OF TIMESTAMP</code>句を使用した履歴データの読み取り {#read-historical-data-using-the-code-as-of-timestamp-code-clause}

このドキュメントでは、 `AS OF TIMESTAMP`句を使用して[ステイル読み取り](/stale-read.md)機能を実行し、TiDB で履歴データを読み取る方法について説明します。これには、履歴データを保存するための具体的な使用例や戦略も含まれます。

TiDB は、特別なクライアントやドライバーを必要とせず、標準 SQL インターフェイス ( `AS OF TIMESTAMP` SQL 句) を介した履歴データの読み取りをサポートします。データが更新または削除された後、この SQL インターフェイスを使用して、更新または削除前の履歴データを読み取ることができます。

> **注記：**
>
> 履歴データを読み取る場合、TiDB は、現在のテーブル構造が異なっていても、古いテーブル構造でデータを返します。

## 構文 {#syntax}

`AS OF TIMESTAMP`句は次の 3 つの方法で使用できます。

-   [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
-   [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
-   [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

正確な時点を指定する場合は、日時値を設定するか、 `AS OF TIMESTAMP`句で時刻関数を使用します。日時の形式は「2016-10-08 16:45:26.999」のようなもので、最小時間単位はミリ秒ですが、ほとんどの場合、「2016」のように日時を指定するには時間単位の秒で十分です。 -10-08 16:45:26」。 `NOW(3)`関数を使用して、現在時刻をミリ秒単位で取得することもできます。数秒前のデータを読みたい場合は、 `NOW() - INTERVAL 10 SECOND`などの式を使用することを**お勧めし**ます。

時間範囲を指定する場合は、句で`TIDB_BOUNDED_STALENESS()`関数を使用できます。この関数を使用すると、TiDB は指定された時間範囲内で適切なタイムスタンプを選択します。 「適切」とは、このタイムスタンプより前に開始され、アクセスされたレプリカでコミットされていないトランザクションがないことを意味します。つまり、TiDB はアクセスされたレプリカで読み取り操作を実行でき、読み取り操作はブロックされません。この関数を呼び出すには`TIDB_BOUNDED_STALENESS(t1, t2)`を使用する必要があります。 `t1`と`t2`は時間範囲の両端であり、日時値または時間関数を使用して指定できます。

`AS OF TIMESTAMP`節の例をいくつか示します。

-   `AS OF TIMESTAMP '2016-10-08 16:45:26'` : 2016 年 10 月 8 日の 16:45:26 に保存された最新のデータを読み取るように TiDB に指示します。
-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND` : 10 秒前に保存された最新のデータを読み取るように TiDB に指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` : 2016 年 10 月 8 日の 16:45:26 から 16:45:29 までの時間範囲内で、できるだけ新しいデータを読み取るように TiDB に指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())` : 20 秒前から現在までの時間範囲内で、できるだけ新しいデータを読み取るように TiDB に指示します。

> **注記：**
>
> タイムスタンプの指定に加えて、 `AS OF TIMESTAMP`句の最も一般的な使用法は、数秒前のデータを読み取ることです。このアプローチを使用する場合は、5 秒より古い履歴データを読み取ることをお勧めします。
>
> ステイル読み取りを使用する場合は、TiDB ノードおよび PD ノードに NTP サービスをデプロイする必要があります。これにより、TiDB によって使用される指定されたタイムスタンプが、最新の TSO 割り当て進行状況よりも進んでいる (タイムスタンプが数秒進んでいるなど)、または GC セーフ ポイントのタイムスタンプよりも遅いという状況が回避されます。指定されたタイムスタンプがサービスの範囲を超える場合、TiDB はエラーを返します。
>
> レイテンシーを短縮し、 ステイル読み取りデータの適時性を向上させるために、TiKV `advance-ts-interval`構成項目を変更できます。詳細は[ステイル読み取りレイテンシーを削減する](/stale-read.md#reduce-stale-read-latency)参照してください。

## 使用例 {#usage-examples}

このセクションでは、 `AS OF TIMESTAMP`句のさまざまな使用方法をいくつかの例とともに説明します。まず、リカバリ用にデータを準備する方法を紹介し、次に`SELECT` 、 `START TRANSACTION READ ONLY AS OF TIMESTAMP` 、および`SET TRANSACTION READ ONLY AS OF TIMESTAMP`の`AS OF TIMESTAMP`それぞれ使用する方法を示します。

### データサンプルの準備 {#prepare-data-sample}

リカバリ用のデータを準備するには、最初にテーブルを作成し、いくつかのデータ行を挿入します。

```sql
create table t (c int);
```

    Query OK, 0 rows affected (0.01 sec)

```sql
insert into t values (1), (2), (3);
```

    Query OK, 3 rows affected (0.00 sec)

テーブル内のデータをビュー。

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

データを連続して更新します。

```sql
update t set c=22 where c=2;
```

    Query OK, 1 row affected (0.00 sec)

行のデータが更新されたことを確認します。

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

### <code>SELECT</code>ステートメントを使用して履歴データを読み取る {#read-historical-data-using-the-code-select-code-statement}

[`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)ステートメントを使用すると、過去のある時点からデータを読み取ることができます。

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
> 1 つの`SELECT`ステートメントを使用して複数のテーブルを読み取る場合は、TIMESTAMP EXPRESSION の形式が一貫していることを確認する必要があります。たとえば、 `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;` 。さらに、 `SELECT`ステートメントで関連テーブルの`AS OF`情報を指定する必要があります。それ以外の場合、 `SELECT`ステートメントはデフォルトで最新のデータを読み取ります。

### <code>START TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取る {#read-historical-data-using-the-code-start-transaction-read-only-as-of-timestamp-code-statement}

[`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)ステートメントを使用すると、過去の時点に基づいて読み取り専用トランザクションを開始できます。トランザクションは、指定された時点の履歴データを読み取ります。

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
> ステートメント`START TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始すると、それは読み取り専用トランザクションになります。このトランザクションでは書き込み操作が拒否されます。

### <code>SET TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取る {#read-historical-data-using-the-code-set-transaction-read-only-as-of-timestamp-code-statement}

[`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)ステートメントを使用すると、過去の指定された時点に基づいて次のトランザクションを読み取り専用トランザクションとして設定できます。トランザクションは、指定された時点の履歴データを読み取ります。

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
> ステートメント`SET TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始すると、それは読み取り専用トランザクションになります。このトランザクションでは書き込み操作が拒否されます。

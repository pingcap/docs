---
title: Read Historical Data Using the `AS OF TIMESTAMP` Clause
summary: Learn how to read historical data using the `AS OF TIMESTAMP` statement clause.
---

# <code>AS OF TIMESTAMP</code>句を使用して履歴データを読み取る {#read-historical-data-using-the-code-as-of-timestamp-code-clause}

このドキュメントでは、 `AS OF TIMESTAMP`句を使用して[古い読み取り](/stale-read.md)機能を実行し、TiDBの履歴データを読み取る方法について説明します。これには、特定の使用例と履歴データを保存するための戦略が含まれます。

> **警告：**
>
> 現在、StaleReadをTiFlashと一緒に使用することはできません。 SQLクエリに`AS OF TIMESTAMP`句が含まれていて、TiDBがTiFlashレプリカからデータを読み取る可能性がある場合、 `ERROR 1105 (HY000): stale requests require tikv backend`のようなメッセージでエラーが発生する可能性があります。
>
> この問題を解決するには、StaleReadクエリのTiFlashレプリカを無効にします。これを行うには、次のいずれかの操作を実行します。
>
> -   `set session tidb_isolation_read_engines='tidb,tikv'`変数を使用します。
> -   [ヒント](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)を使用して、TiDBにTiKVからデータを読み取るように強制します。

TiDBは、特別なクライアントやドライバーを必要とせずに、 `AS OF TIMESTAMP`のSQL句である標準のSQLインターフェイスを介した履歴データの読み取りをサポートします。データが更新または削除された後、このSQLインターフェイスを使用して、更新または削除前の履歴データを読み取ることができます。

> **ノート：**
>
> TiDBは、履歴データを読み取るときに、現在のテーブル構造が異なっていても、古いテーブル構造のデータを返します。

## 構文 {#syntax}

`AS OF TIMESTAMP`句は、次の3つの方法で使用できます。

-   [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
-   [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
-   [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

正確な時点を指定する場合は、日時値を設定するか、 `AS OF TIMESTAMP`句で時間関数を使用できます。日時の形式は「2016-10-0816：45：26.999」のようで、最小時間単位はミリ秒ですが、「2016-10-08 16：45：26.999」のように、ほとんどの場合、秒の時間単位で十分です。 -10-0816:45:26&quot;。 `NOW(3)`関数を使用して、現在の時刻をミリ秒まで取得することもできます。数秒前のデータを読み取りたい場合は、 `NOW() - INTERVAL 10 SECOND`などの式を使用することを**お勧め**します。

時間範囲を指定する場合は、句で`TIDB_BOUNDED_STALENESS()`関数を使用できます。この関数を使用すると、TiDBは指定された時間範囲内で適切なタイムスタンプを選択します。 「適切」とは、このタイムスタンプより前に開始され、アクセスされたレプリカでコミットされていないトランザクションがないことを意味します。つまり、TiDBはアクセスされたレプリカで読み取り操作を実行でき、読み取り操作はブロックされません。この関数を呼び出すには、 `TIDB_BOUNDED_STALENESS(t1, t2)`を使用する必要があります。 `t1`と`t2`は時間範囲の両端であり、日時値または時間関数のいずれかを使用して指定できます。

`AS OF TIMESTAMP`句の例を次に示します。

-   `AS OF TIMESTAMP '2016-10-08 16:45:26'` ：2016年10月8日の16:45:26に保存された最新のデータを読み取るようにTiDBに指示します。
-   `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND`秒前に保存された最新のデータを読み取るようにTiDBに指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')` ：2016年10月8日の16:45:26から16:45:29の時間範囲内で可能な限り新しいデータを読み取るようにTiDBに指示します。
-   `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())`秒前から現在までの時間範囲内で可能な限り新しいデータを読み取るようにTiDBに指示します。

> **ノート：**
>
> タイムスタンプの指定に加えて、 `AS OF TIMESTAMP`句の最も一般的な使用法は、数秒前のデータを読み取ることです。このアプローチを使用する場合は、5秒より古い履歴データを読み取ることをお勧めします。
>
> Stale Readを使用する場合は、TiDBノードとPDノードにNTPサービスを展開する必要があります。これにより、TiDBによって使用される指定されたタイムスタンプが最新のTSO割り当ての進行状況（数秒先のタイムスタンプなど）よりも進んだり、GCセーフポイントのタイムスタンプよりも遅くなったりする状況を回避できます。指定されたタイムスタンプがサービススコープを超えると、TiDBはエラーを返します。

## 使用例 {#usage-examples}

このセクションでは、いくつかの例を使用して`AS OF TIMESTAMP`句を使用するさまざまな方法について説明します。最初に、リカバリ用にデータを準備する方法を紹介し、次に、それぞれ`SELECT` 、および`START TRANSACTION READ ONLY AS OF TIMESTAMP`で`AS OF TIMESTAMP`を使用する方法を示し`SET TRANSACTION READ ONLY AS OF TIMESTAMP` 。

### データサンプルを準備する {#prepare-data-sample}

リカバリ用のデータを準備するには、最初にテーブルを作成し、データのいくつかの行を挿入します。

```sql
create table t (c int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into t values (1), (2), (3);
```

```
Query OK, 3 rows affected (0.00 sec)
```

表のデータをビューします。

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

現在の時刻をビューします。

```sql
select now();
```

```
+---------------------+
| now()               |
+---------------------+
| 2021-05-26 16:45:26 |
+---------------------+
1 row in set (0.00 sec)
```

行のデータを更新します。

```sql
update t set c=22 where c=2;
```

```
Query OK, 1 row affected (0.00 sec)
```

行のデータが更新されていることを確認します。

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

### <code>SELECT</code>ステートメントを使用して履歴データを読み取ります {#read-historical-data-using-the-code-select-code-statement}

[`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)ステートメントを使用して、過去のある時点のデータを読み取ることができます。

```sql
select * from t as of timestamp '2021-05-26 16:45:26';
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

> **ノート：**
>
> 1つの`SELECT`ステートメントを使用して複数のテーブルを読み取る場合は、TIMESTAMPEXPRESSIONの形式が一貫していることを確認する必要があります。たとえば、 `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;` 。さらに、 `SELECT`ステートメントで関連するテーブルの`AS OF`情報を指定する必要があります。それ以外の場合、 `SELECT`ステートメントはデフォルトで最新のデータを読み取ります。

### <code>START TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取ります {#read-historical-data-using-the-code-start-transaction-read-only-as-of-timestamp-code-statement}

[`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)ステートメントを使用して、過去の時点に基づいて読み取り専用トランザクションを開始できます。トランザクションは、指定された時間の履歴データを読み取ります。

```sql
start transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

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

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

トランザクションがコミットされた後、最新のデータを読み取ることができます。

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

> **ノート：**
>
> ステートメント`START TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始する場合、それは読み取り専用トランザクションです。このトランザクションでは、書き込み操作は拒否されます。

### <code>SET TRANSACTION READ ONLY AS OF TIMESTAMP</code>ステートメントを使用して履歴データを読み取ります {#read-historical-data-using-the-code-set-transaction-read-only-as-of-timestamp-code-statement}

[`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)ステートメントを使用して、過去の指定された時点に基づいて、次のトランザクションを読み取り専用トランザクションとして設定できます。トランザクションは、指定された時間の履歴データを読み取ります。

```sql
set transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
begin;
```

```
Query OK, 0 rows affected (0.00 sec)
```

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

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

トランザクションがコミットされた後、最新のデータを読み取ることができます。

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

> **ノート：**
>
> ステートメント`SET TRANSACTION READ ONLY AS OF TIMESTAMP`でトランザクションを開始する場合、それは読み取り専用トランザクションです。このトランザクションでは、書き込み操作は拒否されます。

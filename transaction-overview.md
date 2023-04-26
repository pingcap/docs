---
title: Transactions
summary: Learn transactions in TiDB.
---

# 取引 {#transactions}

TiDB は、 [悲観的](/pessimistic-transaction.md)または[楽観的](/optimistic-transaction.md)トランザクション モードを使用する分散トランザクションをサポートします。 TiDB 3.0.8 以降、TiDB はデフォルトで悲観的トランザクション モードを使用します。

このドキュメントでは、一般的に使用されるトランザクション関連のステートメント、明示的および暗黙的なトランザクション、分離レベル、制約の遅延チェック、およびトランザクション サイズについて説明します。

一般的な変数には、 [`autocommit`](#autocommit) 、 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 、 [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 、および[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)が含まれます。

> **ノート：**
>
> [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)と[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit)変数は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

## 一般的なステートメント {#common-statements}

### 取引の開始 {#starting-a-transaction}

ステートメント[`BEGIN`](/sql-statements/sql-statement-begin.md)と[`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md)は、新しいトランザクションを明示的に開始するために同じ意味で使用できます。

構文：

{{< copyable "" >}}

```sql
BEGIN;
```

{{< copyable "" >}}

```sql
START TRANSACTION;
```

{{< copyable "" >}}

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

{{< copyable "" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

これらのステートメントのいずれかが実行されたときに現在のセッションがトランザクションの処理中である場合、TiDB は新しいトランザクションを開始する前に現在のトランザクションを自動的にコミットします。

> **ノート：**
>
> MySQL とは異なり、TiDB は上記のステートメントを実行した後に現在のデータベースのスナップショットを取得します。 MySQL の`BEGIN`と`START TRANSACTION` 、トランザクションの開始後に InnoDB からデータを読み取る最初の`SELECT`ステートメント ( `SELECT FOR UPDATE`ではない) を実行した後にスナップショットを取得します。 `START TRANSACTION WITH CONSISTENT SNAPSHOT`ステートメントの実行中にスナップショットを取得します。その結果、 `BEGIN` 、 `START TRANSACTION` 、および`START TRANSACTION WITH CONSISTENT SNAPSHOT` MySQL の`START TRANSACTION WITH CONSISTENT SNAPSHOT`に相当します。

### トランザクションのコミット {#committing-a-transaction}

ステートメント[`COMMIT`](/sql-statements/sql-statement-commit.md)は、現在のトランザクションで行われたすべての変更を適用するように TiDB に指示します。

構文：

{{< copyable "" >}}

```sql
COMMIT;
```

> **ヒント：**
>
> [楽観的取引](/optimistic-transaction.md)を有効にする前に、 `COMMIT`ステートメントがエラーを返す可能性があることをアプリケーションが正しく処理していることを確認してください。アプリケーションがこれをどのように処理するかわからない場合は、代わりにデフォルトの[悲観的取引](/pessimistic-transaction.md)を使用することをお勧めします。

### トランザクションのロールバック {#rolling-back-a-transaction}

ステートメント[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)はロールバックし、現在のトランザクションのすべての変更をキャンセルします。

構文：

{{< copyable "" >}}

```sql
ROLLBACK;
```

クライアント接続が中止またはクローズされた場合も、トランザクションは自動的にロールバックされます。

## 自動コミット {#autocommit}

MySQL との互換性のために必要なため、TiDB はデフォルトで、実行直後にステートメントを*自動コミット*します。

例えば：

```sql
mysql> CREATE TABLE t1 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.09 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> INSERT INTO t1 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM t1;
+----+------+
| id | pad1 |
+----+------+
|  1 | test |
+----+------+
1 row in set (0.00 sec)
```

上記の例では、 `ROLLBACK`ステートメントは効果がありません。これは、オートコミットで`INSERT`ステートメントが実行されるためです。つまり、次の単一ステートメントのトランザクションと同等でした。

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

トランザクションが明示的に開始されている場合、自動コミットは適用されません。次の例では、 `ROLLBACK`ステートメントが`INSERT`ステートメントを正常に元に戻します。

```sql
mysql> CREATE TABLE t2 (
    ->  id INT NOT NULL PRIMARY KEY auto_increment,
    ->  pad1 VARCHAR(100)
    -> );
Query OK, 0 rows affected (0.10 sec)

mysql> SELECT @@autocommit;
+--------------+
| @@autocommit |
+--------------+
| 1            |
+--------------+
1 row in set (0.00 sec)

mysql> START TRANSACTION;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t2 VALUES (1, 'test');
Query OK, 1 row affected (0.02 sec)

mysql> ROLLBACK;
Query OK, 0 rows affected (0.00 sec)

mysql> SELECT * FROM t2;
Empty set (0.00 sec)
```

グローバルまたはセッションベースの[`autocommit`](/system-variables.md#autocommit)システム変数[変更可能](/sql-statements/sql-statement-set-variable.md) 。

例えば：

{{< copyable "" >}}

```sql
SET autocommit = 0;
```

{{< copyable "" >}}

```sql
SET GLOBAL autocommit = 0;
```

## 明示的および暗黙的なトランザクション {#explicit-and-implicit-transaction}

> **ノート：**
>
> 一部のステートメントは暗黙的にコミットされます。たとえば、 `[BEGIN|START TRANSACTION]`を実行すると、最後のトランザクションが暗黙的にコミットされ、新しいトランザクションが開始されます。この動作は、MySQL との互換性のために必要です。詳細については、 [暗黙のコミット](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)を参照してください。

TiDB は、明示的なトランザクション (トランザクションの開始と終了を定義するために`[BEGIN|START TRANSACTION]`と`COMMIT`を使用) と暗黙的なトランザクション ( `SET autocommit = 1` ) をサポートしています。

`autocommit`の値を`1`に設定し、 `[BEGIN|START TRANSACTION]`ステートメントを使用して新しいトランザクションを開始すると、トランザクションが明示的になる`COMMIT`または`ROLLBACK`の前に自動コミットが無効になります。

DDL ステートメントの場合、トランザクションは自動的にコミットされ、ロールバックはサポートされません。現在のセッションがトランザクションの処理中に DDL ステートメントを実行すると、現在のトランザクションがコミットされた後に DDL ステートメントが実行されます。

## 制約の遅延チェック {#lazy-check-of-constraints}

デフォルトでは、楽観的トランザクションは、DML ステートメントの実行時に[主キー](/constraints.md#primary-key)または[一意の制約](/constraints.md#unique-key)をチェックしません。これらのチェックは、代わりにトランザクション`COMMIT`で実行されます。

例えば：

{{< copyable "" >}}

```sql
CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
INSERT INTO t1 VALUES (1);
BEGIN OPTIMISTIC;
INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
INSERT INTO t1 VALUES (2);
COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
```

```sql
mysql> CREATE TABLE t1 (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.10 sec)

mysql> INSERT INTO t1 VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> BEGIN OPTIMISTIC;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (1); -- MySQL returns an error; TiDB returns success.
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t1 VALUES (2);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT; -- It is successfully committed in MySQL; TiDB returns an error and the transaction rolls back.
ERROR 1062 (23000): Duplicate entry '1' for key 't1.PRIMARY'
mysql> SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

遅延チェックの最適化は、制約チェックをバッチ処理し、ネットワーク通信を削減することでパフォーマンスを向上させます。 [`tidb_constraint_check_in_place=ON`](/system-variables.md#tidb_constraint_check_in_place)を設定すると、この動作を無効にすることができます。

> **ノート：**
>
> -   この最適化は楽観的トランザクションにのみ適用されます。
> -   この最適化は、 `INSERT IGNORE`および`INSERT ON DUPLICATE KEY UPDATE`に対しては有効ではなく、通常の`INSERT`ステートメントに対してのみ有効です。

## ステートメントのロールバック {#statement-rollback}

TiDB は、ステートメントの実行が失敗した後のアトミックロールバックをサポートしています。ステートメントでエラーが発生した場合、その変更は有効になりません。トランザクションは開いたままになり、 `COMMIT`または`ROLLBACK`ステートメントを発行する前に追加の変更を行うことができます。

{{< copyable "" >}}

```sql
CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
BEGIN;
INSERT INTO test VALUES (1);
INSERT INTO tset VALUES (2);  -- Statement does not take effect because "test" is misspelled as "tset".
INSERT INTO test VALUES (1),(2);  -- Entire statement does not take effect because it violates a PRIMARY KEY constraint
INSERT INTO test VALUES (3);
COMMIT;
SELECT * FROM test;
```

```sql
mysql> CREATE TABLE test (id INT NOT NULL PRIMARY KEY);
Query OK, 0 rows affected (0.09 sec)

mysql> BEGIN;
Query OK, 0 rows affected (0.00 sec)

mysql> INSERT INTO test VALUES (1);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO tset VALUES (2);  -- Statement does not take effect because "test" is misspelled as "tset".
ERROR 1146 (42S02): Table 'test.tset' doesn't exist
mysql> INSERT INTO test VALUES (1),(2);  -- Entire statement does not take effect because it violates a PRIMARY KEY constraint
ERROR 1062 (23000): Duplicate entry '1' for key 'test.PRIMARY'
mysql> INSERT INTO test VALUES (3);
Query OK, 1 row affected (0.00 sec)

mysql> COMMIT;
Query OK, 0 rows affected (0.01 sec)

mysql> SELECT * FROM test;
+----+
| id |
+----+
|  1 |
|  3 |
+----+
2 rows in set (0.00 sec)
```

上記の例では、トランザクションは`INSERT`ステートメントが失敗した後も開いたままです。その後、最後の挿入ステートメントが成功し、変更がコミットされます。

## トランザクションサイズ制限 {#transaction-size-limit}

基盤となるstorageエンジンの制限により、TiDB では 1 行が 6 MB を超えないようにする必要があります。行のすべての列は、データ型に従ってバイトに変換され、合計されて 1 つの行のサイズが推定されます。

TiDB は楽観的トランザクションと悲観的トランザクションの両方をサポートしており、楽観的トランザクションは悲観的トランザクションの基礎です。楽観的トランザクションは最初に変更をプライベートメモリにキャッシュするため、TiDB は 1 つのトランザクションのサイズを制限します。

デフォルトでは、TiDB は 1 つのトランザクションの合計サイズを 100 MB 以下に設定します。このデフォルト値は、構成ファイルの`txn-total-size-limit`で変更できます。 `txn-total-size-limit`の最大値は 1 TB です。個々のトランザクション サイズの制限は、サーバーで使用可能な残りのメモリのサイズにも依存します。これは、トランザクションが実行されると、TiDB プロセスのメモリ使用量がトランザクション サイズと比較して、最大でトランザクション サイズの 2 ～ 3 倍以上になるためです。

TiDB は以前、1 つのトランザクションのキーと値のペアの総数を 300,000 に制限していました。この制限は TiDB v4.0 で削除されました。

> **ノート：**
>
> 通常、TiDB Binlog を有効にしてデータをダウンストリームに複製します。一部のシナリオでは、Kafka などのメッセージ ミドルウェアを使用して、ダウンストリームにレプリケートされるバイナリログを使用します。
>
> Kafka を例にとると、Kafka の単一メッセージ処理能力の上限は 1 GB です。したがって、 `txn-total-size-limit`が 1 GB を超える値に設定されている場合、TiDB でトランザクションが正常に実行されても、下流の Kafka がエラーを報告することがあります。このような状況を回避するには、最終消費者の制限に応じて`txn-total-size-limit`の実際の値を決定する必要があります。たとえば、Kafka がダウンストリームで使用される場合、 `txn-total-size-limit` 1 GB を超えてはなりません。

## 因果の一貫性 {#causal-consistency}

> **ノート：**
>
> 因果整合性のあるトランザクションは、非同期コミットおよび 1 フェーズ コミット機能が有効になっている場合にのみ有効になります。 2 つの機能の詳細については、 [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50)および[`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50)を参照してください。

TiDB は、トランザクションの因果的一貫性の有効化をサポートしています。因果関係のあるトランザクションは、コミット時に PD からタイムスタンプを取得する必要がなく、コミットレイテンシーが低くなります。因果的一貫性を有効にする構文は次のとおりです。

{{< copyable "" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

デフォルトでは、TiDB は線形一貫性を保証します。線形一貫性の場合、トランザクション 1 がコミットされた後にトランザクション 2 がコミットされる場合、論理的にはトランザクション 1 の後にトランザクション 2 が発生するはずです。因果的一貫性は線形一貫性よりも弱いです。因果的一貫性の場合、2 つのトランザクションのコミット順序と発生順序の一貫性が保証されるのは、トランザクション 1 とトランザクション 2 によってロックまたは書き込まれたデータに交差がある場合のみです。これは、2 つのトランザクションに因果関係があることを意味します。データベース。現在、TiDB は外部因果関係の受け渡しをサポートしていません。

因果整合性が有効になっている 2 つのトランザクションには、次の特徴があります。

-   [潜在的な因果関係があるトランザクションは、一貫した論理的順序と物理的コミット順序を持っています](#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order)
-   [因果関係のないトランザクションは、一貫した論理的順序と物理的コミット順序を保証しません](#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order)
-   [ロックなしの読み取りは因果関係を作成しません](#reads-without-lock-do-not-create-causal-relationship)

### 潜在的な因果関係があるトランザクションは、一貫した論理的順序と物理的コミット順序を持っています {#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order}

トランザクション 1 とトランザクション 2 の両方が因果整合性を採用し、次のステートメントを実行するとします。

| トランザクション1                                   | トランザクション2                       |
| ------------------------------------------- | ------------------------------- |
| 因果関係のみで取引を開始する                              | 因果関係のみで取引を開始する                  |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE |                                 |
| UPDATE t セット v = $(x + 1) WHERE id = 2      |                                 |
| 専念                                          |                                 |
|                                             | UPDATE t SET v = 2 WHERE id = 1 |
|                                             | 専念                              |

上記の例では、トランザクション 1 が`id = 1`レコードをロックし、トランザクション 2 が`id = 1`レコードを変更します。したがって、トランザクション 1 とトランザクション 2 には潜在的な因果関係があります。因果整合性が有効になっている場合でも、トランザクション 1 が正常にコミットされた後にトランザクション 2 がコミットされる限り、論理的には、トランザクション 2 はトランザクション`id = 1`の後に発生する必要があります。 `id = 2`レコードの 1 の変更。

### 因果関係のないトランザクションは、一貫した論理的順序と物理的コミット順序を保証しません {#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order}

`id = 1`と`id = 2`の初期値は両方とも`0`であるとします。トランザクション 1 とトランザクション 2 の両方が因果整合性を採用し、次のステートメントを実行するとします。

| トランザクション1                       | トランザクション2                       | トランザクション3                          |
| ------------------------------- | ------------------------------- | ---------------------------------- |
| 因果関係のみで取引を開始する                  | 因果関係のみで取引を開始する                  |                                    |
| UPDATE t セット v = 3 WHERE id = 2 |                                 |                                    |
|                                 | UPDATE t SET v = 2 WHERE id = 1 |                                    |
|                                 |                                 | 始める                                |
| 専念                              |                                 |                                    |
|                                 | 専念                              |                                    |
|                                 |                                 | SELECT v FROM t WHERE id IN (1, 2) |

上記の例では、トランザクション 1 は`id = 1`レコードを読み取っていないため、トランザクション 1 とトランザクション 2 には、データベースが認識している因果関係はありません。トランザクションの因果整合性が有効になっている場合、物理的な時間順でトランザクション 1 がコミットされた後にトランザクション 2 がコミットされたとしても、TiDB はトランザクション 2 がトランザクション 1 の後に論理的に発生することを保証しません。

トランザクション 1 がコミットされる前にトランザクション 3 が開始され、トランザクション 2 がコミットされた後にトランザクション 3 が`id = 1`と`id = 2`レコードを読み取る場合、トランザクション 3 は`id = 1`の値を`2`として読み取り、 `id = 2`の値を`0`として読み取る可能性があります。

### ロックなしの読み取りは因果関係を作成しません {#reads-without-lock-do-not-create-causal-relationship}

トランザクション 1 とトランザクション 2 の両方が因果整合性を採用し、次のステートメントを実行するとします。

| トランザクション1                       | トランザクション2                       |
| ------------------------------- | ------------------------------- |
| 因果関係のみで取引を開始する                  | 因果関係のみで取引を開始する                  |
|                                 | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1    |                                 |
| UPDATE t セット v = 3 WHERE id = 2 |                                 |
|                                 | 専念                              |
| 専念                              |                                 |

上記の例では、ロックなしの読み取りは因果関係を作成しません。トランザクション1 とトランザクション 2 は、書き込みスキューを作成しました。この場合、2 つのトランザクションにまだ因果関係があるとすれば、それは不合理なことです。したがって、因果整合性が有効になっている 2 つのトランザクションには、明確な論理順序はありません。

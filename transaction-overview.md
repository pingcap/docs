---
title: Transactions
summary: TiDB でのトランザクションについて学習します。
---

# 取引 {#transactions}

TiDBは、 [悲観的](/pessimistic-transaction.md)または[楽観的](/optimistic-transaction.md)トランザクションモードを使用した分散トランザクションをサポートします。TiDB 3.0.8以降では、デフォルトで悲観的トランザクションモードが使用されます。

このドキュメントでは、一般的に使用されるトランザクション関連のステートメント、明示的および暗黙的なトランザクション、分離レベル、制約の遅延チェック、およびトランザクション サイズについて説明します。

一般的な変数には、 [`autocommit`](#autocommit) 、 [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry) 、 [`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 、 [`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)などがあります。

> **注記：**
>
> 変数[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)と[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit)は楽観的トランザクションにのみ適用され、悲観的トランザクションには適用されません。

## よくある発言 {#common-statements}

### 取引の開始 {#starting-a-transaction}

ステートメント[`BEGIN`](/sql-statements/sql-statement-begin.md)と[`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) 、新しいトランザクションを明示的に開始するために互換的に使用できます。

構文：

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

```sql
START TRANSACTION WITH CONSISTENT SNAPSHOT;
```

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

これらのステートメントのいずれかが実行されたときに現在のセッションがトランザクションの処理中である場合、TiDB は新しいトランザクションを開始する前に現在のトランザクションを自動的にコミットします。

> **注記：**
>
> MySQLとは異なり、TiDBは上記のステートメントを実行した後に現在のデータベースのスナップショットを取得します。MySQLの`BEGIN`と`START TRANSACTION` 、トランザクション開始後、InnoDBからデータを読み取る最初の`SELECT`ステートメント（ `SELECT FOR UPDATE`ではありません）を実行した後にスナップショットを取得します。9 `START TRANSACTION WITH CONSISTENT SNAPSHOT` `START TRANSACTION`ステートメントの実行中にスナップショットを取得します。結果として、 `BEGIN` `START TRANSACTION WITH CONSISTENT SNAPSHOT` MySQLの`START TRANSACTION WITH CONSISTENT SNAPSHOT`に相当します。

### トランザクションのコミット {#committing-a-transaction}

ステートメント[`COMMIT`](/sql-statements/sql-statement-commit.md) 、現在のトランザクションで行われたすべての変更を適用するように TiDB に指示します。

構文：

```sql
COMMIT;
```

> **ヒント：**
>
> [楽観的取引](/optimistic-transaction.md)有効にする前に、アプリケーションが`COMMIT`ステートメントでエラーが返される可能性があることを正しく処理できることを確認してください。アプリケーションがこれをどのように処理するか不明な場合は、代わりにデフォルトの[悲観的取引](/pessimistic-transaction.md)使用することをお勧めします。

### トランザクションのロールバック {#rolling-back-a-transaction}

ステートメント[`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 、現在のトランザクション内のすべての変更をロールバックしてキャンセルします。

構文：

```sql
ROLLBACK;
```

クライアント接続が中止または閉じられた場合も、トランザクションは自動的にロールバックされます。

## 自動コミット {#autocommit}

MySQL との互換性のために必要なため、TiDB はデフォルトでステートメントを実行直後に*自動コミットし*ます。

例えば：

```sql
mysql> CREATE TABLE t1 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
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

上記の例では、 `ROLLBACK`文は効果がありません。これは、 `INSERT`文が自動コミットで実行されるためです。つまり、これは次の単一文のトランザクションと同等です。

```sql
START TRANSACTION;
INSERT INTO t1 VALUES (1, 'test');
COMMIT;
```

トランザクションが明示的に開始されている場合、自動コミットは適用されません。次の例では、 `ROLLBACK`文が`INSERT`文を正常に元に戻しています。

```sql
mysql> CREATE TABLE t2 (
     id INT NOT NULL PRIMARY KEY auto_increment,
     pad1 VARCHAR(100)
    );
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

グローバルまたはセッション ベースの[`autocommit`](/system-variables.md#autocommit)システム変数[変更可能](/sql-statements/sql-statement-set-variable.md) 。

例えば：

```sql
SET autocommit = 0;
```

```sql
SET GLOBAL autocommit = 0;
```

## 明示的トランザクションと暗黙的トランザクション {#explicit-and-implicit-transaction}

> **注記：**
>
> 一部の文は暗黙的にコミットされます。例えば、 `[BEGIN|START TRANSACTION]`実行すると、最後のトランザクションが暗黙的にコミットされ、新しいトランザクションが開始されます。この動作はMySQLとの互換性を保つために必要です。詳細は[暗黙のコミット](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)を参照してください。

TiDBは明示的なトランザクション（ `[BEGIN|START TRANSACTION]`と`COMMIT`使用してトランザクションの開始と終了を定義する）と暗黙的なトランザクション（ `SET autocommit = 1` ）をサポートしています。

`autocommit`の値を`1`に設定し、 `[BEGIN|START TRANSACTION]`ステートメントを通じて新しいトランザクションを開始すると、 `COMMIT`または`ROLLBACK`前に自動コミットが無効になり、トランザクションが明示的になります。

DDL文の場合、トランザクションは自動的にコミットされ、ロールバックはサポートされません。現在のセッションがトランザクション処理中である間にDDL文を実行した場合、DDL文は現在のトランザクションがコミットされた後に実行されます。

## 制約の遅延チェック {#lazy-check-of-constraints}

デフォルトでは、楽観的トランザクションはDML文の実行時に[主キー](/constraints.md#primary-key)と[一意制約](/constraints.md#unique-key)チェックしません。これらのチェックはトランザクション`COMMIT`で実行されます。

例えば：

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

遅延チェック最適化は、制約チェックをバッチ処理し、ネットワーク通信を削減することでパフォーマンスを向上させます。この動作は[`tidb_constraint_check_in_place=ON`](/system-variables.md#tidb_constraint_check_in_place)設定することで無効にできます。

> **注記：**
>
> -   この最適化は楽観的トランザクションにのみ適用されます。
> -   この最適化は`INSERT IGNORE`と`INSERT ON DUPLICATE KEY UPDATE`には適用されず、通常の`INSERT`ステートメントにのみ適用されます。

## ステートメントのロールバック {#statement-rollback}

TiDBは、ステートメント実行失敗後のアトミックロールバックをサポートしています。ステートメントがエラーになった場合、そのステートメントで行われた変更は有効になりません。トランザクションはオープンのままとなり、 `COMMIT`または`ROLLBACK`ステートメントを発行する前に追加の変更を加えることができます。

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

上記の例では、 `INSERT`ステートメントが失敗した後もトランザクションは開いたままです。その後、最後の挿入ステートメントが成功し、変更がコミットされます。

## トランザクションサイズの制限 {#transaction-size-limit}

基盤となるstorageエンジンの制限により、TiDBでは1行のサイズが6MB以下である必要があります。行内のすべての列は、それぞれのデータ型に応じてバイトに変換され、合計されて1行のサイズが推定されます。

TiDBは楽観的トランザクションと悲観的トランザクションの両方をサポートしており、楽観的トランザクションは悲観的トランザクションの基盤となります。楽観的トランザクションはまず変更をプライベートメモリにキャッシュするため、TiDBは単一トランザクションのサイズを制限します。

デフォルトでは、TiDB は単一トランザクションの合計サイズを 100 MB 以下に設定します。このデフォルト値は、設定ファイルで`txn-total-size-limit`設定することで変更できます。最大値は`txn-total-size-limit`で、1 TB です。個々のトランザクションのサイズ制限は、サーバーで使用可能なメモリの残り容量にも依存します。これは、トランザクションの実行時に、TiDB プロセスのメモリ使用量がトランザクションサイズと比較して、最大でトランザクションサイズの 2 ～ 3 倍以上にまで増加するためです。

TiDBでは以前、1トランザクションあたりのキーと値のペアの総数が300,000個に制限されていました。この制限はTiDB v4.0で削除されました。

## 因果関係の一貫性 {#causal-consistency}

> **注記：**
>
> 因果一貫性のあるトランザクションは、非同期コミット機能と1相コミット機能が有効な場合にのみ有効になります。これらの2つの機能の詳細については、 [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50)と[`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50)参照してください。

TiDBは、トランザクションの因果一貫性の有効化をサポートしています。因果一貫性のあるトランザクションは、コミット時にPDからタイムスタンプを取得する必要がなく、コミットレイテンシーが低くなります。因果一貫性を有効にする構文は次のとおりです。

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

TiDBはデフォルトで線形一貫性を保証します。線形一貫性の場合、トランザクション1がコミットされた後にトランザクション2がコミットされた場合、論理的にはトランザクション2はトランザクション1の後に発生するはずです。因果一貫性は線形一貫性よりも弱いです。因果一貫性の場合、2つのトランザクションのコミット順序と発生順序の一貫性が保証されるのは、トランザクション1とトランザクション2によってロックまたは書き込まれたデータが交差している場合のみです。つまり、2つのトランザクションはデータベースに既知の因果関係があることを意味します。現在、TiDBは外部因果関係の受け渡しをサポートしていません。

因果一貫性が有効になっている 2 つのトランザクションには、次の特性があります。

-   [潜在的な因果関係を持つトランザクションは、一貫した論理順序と物理的なコミット順序を持つ](#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order)
-   [因果関係のないトランザクションは、一貫した論理順序と物理的なコミット順序を保証しません。](#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order)
-   [ロックなしの読み取りでは因果関係は生まれない](#reads-without-lock-do-not-create-causal-relationship)

### 潜在的な因果関係を持つトランザクションは、一貫した論理順序と物理的なコミット順序を持つ {#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order}

トランザクション 1 とトランザクション 2 の両方が因果一貫性を採用し、次のステートメントを実行すると仮定します。

| トランザクション1                                   | トランザクション2                   |
| ------------------------------------------- | --------------------------- |
| 因果関係の一貫性のみで取引を開始する                          | 因果関係の一貫性のみで取引を開始する          |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE |                             |
| 更新 t set v = $(x + 1) WHERE id = 2          |                             |
| 専念                                          |                             |
|                                             | 更新 t SET v = 2 WHERE id = 1 |
|                                             | 専念                          |

上記の例では、トランザクション1がレコード`id = 1`をロックし、トランザクション2がレコード`id = 1`変更します。したがって、トランザクション1とトランザクション2には潜在的な因果関係があります。因果一貫性が有効になっている場合でも、トランザクション2がトランザクション1のコミット後にコミットされる限り、論理的にはトランザクション2はトランザクション1の後に発生する必要があります。したがって、トランザクション1によるレコード`id = 2`の変更を読み取らずに、トランザクション2によるレコード`id = 1`の変更を読み取るトランザクションは不可能です。

### 因果関係のないトランザクションは、一貫した論理順序と物理的なコミット順序を保証しません。 {#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order}

`id = 1`と`id = 2`の初期値はどちらも`0`あると仮定します。トランザクション 1 とトランザクション 2 の両方が因果一貫性を採用し、以下の文が実行されるものとします。

| トランザクション1                   | トランザクション2                   | トランザクション3                          |
| --------------------------- | --------------------------- | ---------------------------------- |
| 因果関係の一貫性のみで取引を開始する          | 因果関係の一貫性のみで取引を開始する          |                                    |
| 更新 t set v = 3 WHERE id = 2 |                             |                                    |
|                             | 更新 t SET v = 2 WHERE id = 1 |                                    |
|                             |                             | 始める                                |
| 専念                          |                             |                                    |
|                             | 専念                          |                                    |
|                             |                             | SELECT v FROM t WHERE id IN (1, 2) |

上記の例では、トランザクション1はレコード`id = 1`を読み取らないため、データベースはトランザクション1とトランザクション2の間に因果関係を認識していません。トランザクションの因果一貫性が有効になっている場合、物理的な時間順序でトランザクション2がトランザクション1のコミット後にコミットされたとしても、TiDBはトランザクション2が論理的にトランザクション1の後に発生することを保証しません。

トランザクション 3 がトランザクション 1 がコミットされる前に開始され、トランザクション 3 がトランザクション 2 がコミットされた後にレコード`id = 1`と`id = 2`読み取る場合、トランザクション 3 は`id = 1`の値を`2`と読み取りますが、 `id = 2`の値は`0`読み取る可能性があります。

### ロックなしの読み取りでは因果関係は生まれない {#reads-without-lock-do-not-create-causal-relationship}

トランザクション 1 とトランザクション 2 の両方が因果一貫性を採用し、次のステートメントを実行すると仮定します。

| トランザクション1                    | トランザクション2                   |
| ---------------------------- | --------------------------- |
| 因果関係の一貫性のみで取引を開始する           | 因果関係の一貫性のみで取引を開始する          |
|                              | 更新 t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1 |                             |
| 更新 t set v = 3 WHERE id = 2  |                             |
|                              | 専念                          |
| 専念                           |                             |

上記の例では、ロックなしの読み取りでは因果関係は発生しません。トランザクション1とトランザクション2は書き込みスキューを発生させています。この場合、2つのトランザクションに因果関係が残っているとしたら不合理です。したがって、因果一貫性が有効な2つのトランザクションには明確な論理的順序がありません。

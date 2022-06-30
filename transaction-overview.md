---
title: Transactions
summary: Learn transactions in TiDB.
---

# トランザクション {#transactions}

TiDBは、 [悲観的](/pessimistic-transaction.md)つまたは[楽観的](/optimistic-transaction.md)のトランザクションモードを使用した分散トランザクションをサポートします。 TiDB 3.0.8以降、TiDBはデフォルトで悲観的トランザクションモードを使用します。

このドキュメントでは、一般的に使用されるトランザクション関連のステートメント、明示的および暗黙的なトランザクション、分離レベル、制約の遅延チェック、およびトランザクションサイズを紹介します。

一般的な変数には、 [`autocommit`](#autocommit) 、および[`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)が[`tidb_txn_mode`](/system-variables.md#tidb_txn_mode)れ[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit) 。

> **ノート：**
>
> [`tidb_disable_txn_auto_retry`](/system-variables.md#tidb_disable_txn_auto_retry)変数と[`tidb_retry_limit`](/system-variables.md#tidb_retry_limit)変数は楽観的なトランザクションにのみ適用され、悲観的なトランザクションには適用されません。

## 一般的なステートメント {#common-statements}

### トランザクションの開始 {#starting-a-transaction}

ステートメント[`BEGIN`](/sql-statements/sql-statement-begin.md)と[`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md)は、新しいトランザクションを明示的に開始するために交換可能に使用できます。

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

これらのステートメントのいずれかが実行されたときに現在のセッションがトランザクションの処理中である場合、TiDBは新しいトランザクションを開始する前に現在のトランザクションを自動的にコミットします。

> **ノート：**
>
> MySQLとは異なり、TiDBは上記のステートメントを実行した後、現在のデータベースのスナップショットを取得します。 MySQLの`BEGIN`と`START TRANSACTION`は、トランザクションの開始後にInnoDBからデータを読み取る最初の`SELECT`のステートメント（ `SELECT FOR UPDATE`ではない）を実行した後にスナップショットを取得します。 `START TRANSACTION WITH CONSISTENT SNAPSHOT`は、ステートメントの実行中にスナップショットを取得します。その結果、 `BEGIN` 、および`START TRANSACTION`は、 `START TRANSACTION WITH CONSISTENT SNAPSHOT` `START TRANSACTION WITH CONSISTENT SNAPSHOT`相当します。

### トランザクションのコミット {#committing-a-transaction}

ステートメント[`COMMIT`](/sql-statements/sql-statement-commit.md)は、現在のトランザクションで行われたすべての変更を適用するようにTiDBに指示します。

構文：

{{< copyable "" >}}

```sql
COMMIT;
```

> **ヒント：**
>
> [楽観的なトランザクション](/optimistic-transaction.md)を有効にする前に、アプリケーションが`COMMIT`ステートメントがエラーを返す可能性があることを正しく処理していることを確認してください。アプリケーションがこれをどのように処理するかわからない場合は、代わりにデフォルトの[悲観的なトランザクション](/pessimistic-transaction.md)を使用することをお勧めします。

### トランザクションのロールバック {#rolling-back-a-transaction}

ステートメント[`ROLLBACK`](/sql-statements/sql-statement-rollback.md)はロールバックし、現在のトランザクションのすべての変更をキャンセルします。

構文：

{{< copyable "" >}}

```sql
ROLLBACK;
```

クライアント接続が中止または閉じられた場合も、トランザクションは自動的にロールバックされます。

## 自動コミット {#autocommit}

MySQLの互換性に必要な場合、TiDBはデフォルトで、実行直後にステートメントを*自動コミット*します。

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

上記の例では、 `ROLLBACK`ステートメントは効果がありません。これは、 `INSERT`ステートメントが自動コミットで実行されるためです。つまり、次の単一ステートメントトランザクションと同等でした。

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

グローバルベースまたはセッションベースのいずれかで[`autocommit`](/system-variables.md#autocommit)のシステム変数[変更可能](/sql-statements/sql-statement-set-variable.md) 。

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
> 一部のステートメントは暗黙的にコミットされます。たとえば、 `[BEGIN|START TRANSACTION]`を実行すると、最後のトランザクションが暗黙的にコミットされ、新しいトランザクションが開始されます。この動作は、MySQLとの互換性のために必要です。詳細については、 [暗黙のコミット](https://dev.mysql.com/doc/refman/8.0/en/implicit-commit.html)を参照してください。

TiDBは、明示的なトランザクション（ `[BEGIN|START TRANSACTION]`と`COMMIT`を使用してトランザクションの開始と終了を定義）と暗黙的なトランザクション（ `SET autocommit = 1` ）をサポートします。

`autocommit`から`1`の値を設定し、 `[BEGIN|START TRANSACTION]`ステートメントを使用して新しいトランザクションを開始すると、 `COMMIT`または`ROLLBACK`の前に自動コミットが無効になり、トランザクションが明示的になります。

DDLステートメントの場合、トランザクションは自動的にコミットされ、ロールバックをサポートしません。現在のセッションがトランザクションの処理中にDDLステートメントを実行すると、現在のトランザクションがコミットされた後にDDLステートメントが実行されます。

## 制約のレイジーチェック {#lazy-check-of-constraints}

デフォルトでは、楽観的なトランザクションは、DMLステートメントが実行されるときに[主キー](/constraints.md#primary-key)または[固有の制約](/constraints.md#unique-key)をチェックしません。これらのチェックは、代わりにトランザクション`COMMIT`で実行されます。

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
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
mysql> SELECT * FROM t1; -- MySQL returns 1 2; TiDB returns 1.
+----+
| id |
+----+
|  1 |
+----+
1 row in set (0.01 sec)
```

レイジーチェックの最適化は、制約チェックをバッチ処理し、ネットワーク通信を減らすことでパフォーマンスを向上させます。 [`tidb_constraint_check_in_place=TRUE`](/system-variables.md#tidb_constraint_check_in_place)を設定すると、この動作を無効にできます。

> **ノート：**
>
> -   この最適化は、楽観的なトランザクションにのみ適用されます。
> -   この最適化は、 `INSERT IGNORE`と`INSERT ON DUPLICATE KEY UPDATE`では有効になりませんが、通常の`INSERT`のステートメントでのみ有効になります。

## ステートメントのロールバック {#statement-rollback}

TiDBは、ステートメントの実行が失敗した後のアトミックロールバックをサポートします。ステートメントにエラーが発生した場合、ステートメントが行った変更は有効になりません。トランザクションは開いたままになり、 `COMMIT`または`ROLLBACK`ステートメントを発行する前に追加の変更を行うことができます。

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
ERROR 1062 (23000): Duplicate entry '1' for key 'PRIMARY'
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

上記の例では、 `INSERT`ステートメントが失敗した後もトランザクションは開いたままになります。その後、最後の挿入ステートメントが成功し、変更がコミットされます。

## トランザクションサイズの制限 {#transaction-size-limit}

基盤となるストレージエンジンの制限により、TiDBでは1行が6MB以下である必要があります。行のすべての列は、データ型に従ってバイトに変換され、合計されて1つの行のサイズが推定されます。

TiDBは、楽観的トランザクションと悲観的トランザクションの両方をサポートしており、楽観的トランザクションは悲観的トランザクションの基礎です。楽観的なトランザクションは最初にプライベートメモリに変更をキャッシュするため、TiDBは単一のトランザクションのサイズを制限します。

デフォルトでは、TiDBは単一トランザクションの合計サイズを100MB以下に設定します。このデフォルト値は、構成ファイルの`txn-total-size-limit`を介して変更できます。 `txn-total-size-limit`の最大値は1TBです。個々のトランザクションサイズの制限は、サーバーで使用可能な残りのメモリのサイズにも依存します。これは、トランザクションが実行されると、TiDBプロセスのメモリ使用量がトランザクションサイズと比較してスケールアップされ、トランザクションサイズの2〜3倍以上になるためです。

TiDBは以前、1つのトランザクションのキーと値のペアの総数を300,000に制限していました。この制限はTiDBv4.0で削除されました。

> **ノート：**
>
> 通常、TiDB Binlogは、データをダウンストリームに複製するために有効になっています。一部のシナリオでは、Kafkaなどのメッセージミドルウェアを使用して、ダウンストリームに複製されるbinlogを消費します。
>
> Kafkaを例にとると、Kafkaの単一メッセージ処理機能の上限は1GBです。したがって、 `txn-total-size-limit`が1 GBを超えるように設定されている場合、トランザクションはTiDBで正常に実行される可能性がありますが、ダウンストリームのKafkaはエラーを報告します。この状況を回避するには、最終消費者の制限に応じて実際の値`txn-total-size-limit`を決定する必要があります。たとえば、Kafkaをダウンストリームで使用する場合、 `txn-total-size-limit`は1GBを超えてはなりません。

## 因果整合性 {#causal-consistency}

> **ノート：**
>
> 因果整合性のあるトランザクションは、非同期コミットおよび1フェーズコミット機能が有効になっている場合にのみ有効になります。 2つの機能の詳細については、 [`tidb_enable_async_commit`](/system-variables.md#tidb_enable_async_commit-new-in-v50)と[`tidb_enable_1pc`](/system-variables.md#tidb_enable_1pc-new-in-v50)を参照してください。

TiDBは、トランザクションの因果整合性の有効化をサポートしています。因果整合性のあるトランザクションは、コミットされると、PDからタイムスタンプを取得する必要がなく、コミットの待ち時間が短くなります。因果整合性を有効にする構文は次のとおりです。

{{< copyable "" >}}

```sql
START TRANSACTION WITH CAUSAL CONSISTENCY ONLY;
```

デフォルトでは、TiDBは線形の一貫性を保証します。線形整合性の場合、トランザクション1がコミットされた後にトランザクション2がコミットされると、論理的には、トランザクション2はトランザクション1の後に発生するはずです。因果整合性は線形整合性よりも弱いです。因果整合性の場合、2つのトランザクションのコミット順序と発生順序は、トランザクション1とトランザクション2によってロックまたは書き込まれたデータに交差がある場合にのみ一貫性が保証されます。つまり、2つのトランザクションには因果関係があります。データベース。現在、TiDBは外部の因果関係の受け渡しをサポートしていません。

因果整合性が有効になっている2つのトランザクションには、次の特性があります。

-   [潜在的な因果関係を持つトランザクションには、一貫した論理順序と物理コミット順序があります](#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order)
-   [因果関係のないトランザクションは、一貫した論理順序と物理コミット順序を保証しません](#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order)
-   [ロックなしの読み取りは因果関係を作成しません](#reads-without-lock-do-not-create-causal-relationship)

### 潜在的な因果関係を持つトランザクションには、一貫した論理順序と物理コミット順序があります {#transactions-with-potential-causal-relationship-have-the-consistent-logical-order-and-physical-commit-order}

トランザクション1とトランザクション2の両方が因果整合性を採用し、次のステートメントが実行されていると想定します。

| トランザクション1                                   | トランザクション2                       |
| ------------------------------------------- | ------------------------------- |
| 因果整合性のみでトランザクションを開始する                       | 因果整合性のみでトランザクションを開始する           |
| x = SELECT v FROM t WHERE id = 1 FOR UPDATE |                                 |
| UPDATE t set v = $（x + 1）WHERE id = 2       |                                 |
| 専念                                          |                                 |
|                                             | UPDATE t SET v = 2 WHERE id = 1 |
|                                             | 専念                              |

上記の例では、トランザクション1が`id = 1`のレコードをロックし、トランザクション2が`id = 1`のレコードを変更します。したがって、トランザクション1とトランザクション2には潜在的な因果関係があります。因果整合性を有効にしても、トランザクション1が正常にコミットされた後にトランザクション2がコミットされる限り、論理的には、トランザクション2はトランザクション1の後に発生する必要があります。したがって、トランザクションがトランザクションを読み取らずに`id = 1`レコードのトランザクション2の変更を読み取ることはできません。 `id = 2`レコードの1の変更。

### 因果関係のないトランザクションは、一貫した論理順序と物理コミット順序を保証しません {#transactions-with-no-causal-relationship-do-not-guarantee-consistent-logical-order-and-physical-commit-order}

`id = 1`と`id = 2`の初期値は両方とも`0`であると仮定します。トランザクション1とトランザクション2の両方が因果整合性を採用し、次のステートメントが実行されていると想定します。

| トランザクション1                       | トランザクション2                       | トランザクション3                        |
| ------------------------------- | ------------------------------- | -------------------------------- |
| 因果整合性のみでトランザクションを開始する           | 因果整合性のみでトランザクションを開始する           |                                  |
| UPDATE t set v = 3 WHERE id = 2 |                                 |                                  |
|                                 | UPDATE t SET v = 2 WHERE id = 1 |                                  |
|                                 |                                 | 始める                              |
| 専念                              |                                 |                                  |
|                                 | 専念                              |                                  |
|                                 |                                 | SELECT v FROM t WHERE id IN（1、2） |

上記の例では、トランザクション1は`id = 1`レコードを読み取らないため、トランザクション1とトランザクション2にはデータベースに知られている因果関係はありません。トランザクションの因果整合性が有効になっている場合、物理的な時間順序でトランザクション1がコミットされた後にトランザクション2がコミットされたとしても、TiDBはトランザクション2がトランザクション1の後に論理的に発生することを保証しません。

トランザクション1がコミットされる前にトランザクション3が開始され、トランザクション2がコミットされた後にトランザクション3が`id = 1`および`id = 2`レコードを読み取る場合、トランザクション3は`id = 1`の値を`2`に読み取り、 `id = 2`の値を`0`に読み取る可能性があります。

### ロックなしの読み取りは因果関係を作成しません {#reads-without-lock-do-not-create-causal-relationship}

トランザクション1とトランザクション2の両方が因果整合性を採用し、次のステートメントが実行されていると想定します。

| トランザクション1                       | トランザクション2                       |
| ------------------------------- | ------------------------------- |
| 因果整合性のみでトランザクションを開始する           | 因果整合性のみでトランザクションを開始する           |
|                                 | UPDATE t SET v = 2 WHERE id = 1 |
| SELECT v FROM t WHERE id = 1    |                                 |
| UPDATE t set v = 3 WHERE id = 2 |                                 |
|                                 | 専念                              |
| 専念                              |                                 |

上記の例では、ロックなしの読み取りは因果関係を作成しません。トランザクション1とトランザクション2は書き込みスキューを作成しました。この場合、2つのトランザクションがまだ因果関係を持っていたとしたら、それは不合理だったでしょう。したがって、因果整合性が有効になっている2つのトランザクションには、明確な論理順序がありません。

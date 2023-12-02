---
title: Transaction overview
summary: A brief introduction to transactions in TiDB.
---

# トランザクション概要 {#transaction-overview}

TiDB は完全な分散トランザクションをサポートし、 [楽観的取引](/optimistic-transaction.md)と[悲観的取引](/pessimistic-transaction.md) (TiDB 3.0 で導入) を提供します。この記事では主に、トランザクション ステートメント、楽観的トランザクションと悲観的トランザクション、トランザクション分離レベル、楽観的トランザクションにおけるアプリケーション側のリトライとエラー処理について紹介します。

## 一般的なステートメント {#common-statements}

この章では、TiDB でのトランザクションの使用方法を紹介します。次の例は、単純なトランザクションのプロセスを示しています。

ボブはアリスに 20 ドルを送金したいと考えています。このトランザクションには次の 2 つの操作が含まれます。

-   ボブの口座は 20 ドル減額されます。
-   アリスのアカウントは 20 ドル増加しました。

トランザクションにより、上記の操作が両方とも正常に実行されるか、両方とも失敗するかを確認できます。

[書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`users`テーブルを使用して、サンプル データをテーブルに挿入します。

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

次のトランザクションを実行し、各ステートメントの意味を説明します。

```sql
BEGIN;
  UPDATE users SET balance = balance - 20 WHERE nickname = 'Bob';
  UPDATE users SET balance = balance + 20 WHERE nickname= 'Alice';
COMMIT;
```

上記のトランザクションが正常に実行されると、テーブルは次のようになります。

```
+----+--------------+---------+
| id | account_name | balance |
+----+--------------+---------+
|  1 | Alice        |  120.00 |
|  2 | Bob          |  180.00 |
+----+--------------+---------+

```

### 取引を開始する {#start-a-transaction}

新しいトランザクションを明示的に開始するには、 `BEGIN`または`START TRANSACTION`を使用できます。

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

TiDB のデフォルトのトランザクション モードは悲観的です。 [楽観的トランザクション モデル](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)明示的に指定することもできます。

```sql
BEGIN OPTIMISTIC;
```

[悲観的トランザクションモード](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)を有効にします。

```sql
BEGIN PESSIMISTIC;
```

上記のステートメントが実行されたときに現在のセッションがトランザクションの途中である場合、TiDB は最初に現在のトランザクションをコミットし、次に新しいトランザクションを開始します。

### トランザクションをコミットする {#commit-a-transaction}

`COMMIT`ステートメントを使用すると、現在のトランザクションで TiDB によって行われたすべての変更をコミットできます。

```sql
COMMIT;
```

楽観的トランザクションを有効にする前に、アプリケーションが`COMMIT`ステートメントによって返される可能性のあるエラーを適切に処理できることを確認してください。アプリケーションがそれをどのように処理するかわからない場合は、代わりに悲観的トランザクション モードを使用することをお勧めします。

### トランザクションをロールバックする {#roll-back-a-transaction}

`ROLLBACK`ステートメントを使用すると、現在のトランザクションの変更をロールバックできます。

```sql
ROLLBACK;
```

前の転送の例では、トランザクション全体をロールバックすると、アリスとボブの残高は変更されず、現在のトランザクションのすべての変更がキャンセルされます。

```sql
TRUNCATE TABLE `users`;

INSERT INTO `users` (`id`, `nickname`, `balance`) VALUES (1, 'Alice', 100), (2, 'Bob', 200);

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+

BEGIN;
  UPDATE `users` SET `balance` = `balance` - 20 WHERE `nickname`='Bob';
  UPDATE `users` SET `balance` = `balance` + 20 WHERE `nickname`='Alice';
ROLLBACK;

SELECT * FROM `users`;
+----+--------------+---------+
| id | nickname     | balance |
+----+--------------+---------+
|  1 | Alice        |  100.00 |
|  2 | Bob          |  200.00 |
+----+--------------+---------+
```

クライアント接続が停止または閉じられた場合にも、トランザクションは自動的にロールバックされます。

## トランザクション分離レベル {#transaction-isolation-levels}

トランザクション分離レベルは、データベース トランザクション処理の基礎です。 **ACID**の「I」（分離）は、トランザクションの分離を指します。

SQL-92 標準では、次の 4 つの分離レベルが定義されています。

-   コミットされていない読み取り ( `READ UNCOMMITTED` )
-   読み取りがコミットされました ( `READ COMMITTED` )
-   反復可能な読み取り ( `REPEATABLE READ` )
-   シリアル化可能 ( `SERIALIZABLE` )。

詳細については、以下の表を参照してください。

| 分離レベル            | ダーティライト | ダーティリード | ファジーリード | ファントム |
| ---------------- | ------- | ------- | ------- | ----- |
| READ UNCOMMITTED | ありえない   | 可能      | 可能      | 可能    |
| READ COMMITTED   | ありえない   | ありえない   | 可能      | 可能    |
| REPEATABLE READ  | ありえない   | ありえない   | ありえない   | 可能    |
| SERIALIZABLE     | ありえない   | ありえない   | ありえない   | ありえない |

TiDB は、次の分離レベル`READ COMMITTED`および`REPEATABLE READ`をサポートします。

```sql
mysql> SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
ERROR 8048 (HY000): The isolation level 'READ-UNCOMMITTED' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
mysql> SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
Query OK, 0 rows affected (0.00 sec)

mysql> SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;
ERROR 8048 (HY000): The isolation level 'SERIALIZABLE' is not supported. Set tidb_skip_isolation_level_check=1 to skip this error
```

TiDB は、MySQL との一貫性のために「反復読み取り」とも呼ばれるスナップショット分離 (SI) レベルの一貫性を実装しています。この分離レベルは[ANSI 反復読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)および[MySQL 反復読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)とは異なります。詳細については、 [TiDBトランザクション分離レベル](/transaction-isolation-levels.md)を参照してください。

---
title: Transaction overview
summary: A brief introduction to transactions in TiDB.
---

# 取引概要 {#transaction-overview}

TiDBは完全な分散トランザクションをサポートし、 [楽観的なトランザクション](/optimistic-transaction.md)と[悲観的なトランザクション](/pessimistic-transaction.md)を提供します（TiDB 3.0で導入）。この記事では、主にトランザクションステートメント、楽観的なトランザクションと悲観的なトランザクション、トランザクションの分離レベル、および楽観的なトランザクションでのアプリケーション側の再試行とエラー処理について説明します。

## 一般的なステートメント {#common-statements}

この章では、TiDBでトランザクションを使用する方法を紹介します。次の例は、単純なトランザクションのプロセスを示しています。

ボブは$20をアリスに送金したいと考えています。このトランザクションには、次の2つの操作が含まれます。

-   ボブのアカウントは$20削減されます。
-   アリスのアカウントは$20増加します。

トランザクションは、上記の操作の両方が正常に実行されるか、両方が失敗することを保証できます。

[書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`users`テーブルを使用して、いくつかのサンプルデータをテーブルに挿入します。

{{< copyable "" >}}

```sql
INSERT INTO users (id, nickname, balance)
  VALUES (2, 'Bob', 200);
INSERT INTO users (id, nickname, balance)
  VALUES (1, 'Alice', 100);
```

次のトランザクションを実行し、各ステートメントの意味を説明します。

{{< copyable "" >}}

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

### トランザクションを開始します {#start-a-transaction}

新しいトランザクションを明示的に開始するには、 `BEGIN`または`START TRANSACTION`のいずれかを使用できます。

{{< copyable "" >}}

```sql
BEGIN;
```

{{< copyable "" >}}

```sql
START TRANSACTION;
```

TiDBのデフォルトのトランザクションモードは悲観的です。 [楽観的なトランザクションモデル](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)を明示的に指定することもできます：

{{< copyable "" >}}

```sql
BEGIN OPTIMISTIC;
```

[悲観的なトランザクションモード](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)を有効にします：

{{< copyable "" >}}

```sql
BEGIN PESSIMISTIC;
```

上記のステートメントが実行されたときに現在のセッションがトランザクションの途中である場合、TiDBは最初に現在のトランザクションをコミットしてから、新しいトランザクションを開始します。

### トランザクションをコミットする {#commit-a-transaction}

`COMMIT`ステートメントを使用して、現在のトランザクションでTiDBによって行われたすべての変更をコミットできます。

{{< copyable "" >}}

```sql
COMMIT;
```

楽観的なトランザクションを有効にする前に、アプリケーションが`COMMIT`ステートメントによって返される可能性のあるエラーを適切に処理できることを確認してください。アプリケーションがそれをどのように処理するかわからない場合は、代わりにペシミスティックトランザクションモードを使用することをお勧めします。

### トランザクションをロールバックする {#roll-back-a-transaction}

`ROLLBACK`ステートメントを使用して、現在のトランザクションの変更をロールバックできます。

{{< copyable "" >}}

```sql
ROLLBACK;
```

前の転送の例では、トランザクション全体をロールバックすると、アリスとボブの残高は変更されず、現在のトランザクションのすべての変更がキャンセルされます。

{{< copyable "" >}}

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

クライアント接続が停止または閉じられた場合も、トランザクションは自動的にロールバックされます。

## トランザクション分離レベル {#transaction-isolation-levels}

トランザクション分離レベルは、データベーストランザクション処理の基礎です。 **ACID**の「I」（分離）は、トランザクションの分離を指します。

SQL-92標準では、次の4つの分離レベルが定義されています。

-   コミットされていない読み取り（ `READ UNCOMMITTED` ）
-   コミット済みの読み取り（ `READ COMMITTED` ）
-   繰り返し可能な読み取り（ `REPEATABLE READ` ）
-   シリアル化可能（ `SERIALIZABLE` ）。

詳細については、以下の表を参照してください。

| 分離レベル          | ダーティライト | ダーティリード | ファジーリード | ファントム |
| -------------- | ------- | ------- | ------- | ----- |
| コミットされていない読み取り | ありえない   | 可能      | 可能      | 可能    |
| コミット済みを読む      | ありえない   | ありえない   | 可能      | 可能    |
| 繰り返し読む         | ありえない   | ありえない   | ありえない   | 可能    |
| シリアル化可能        | ありえない   | ありえない   | ありえない   | ありえない |

TiDBは、次の分離レベルをサポートしています`READ COMMITTED`および`REPEATABLE READ` ：

{{< copyable "" >}}

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

TiDBは、MySQLとの整合性のために「反復可能読み取り」とも呼ばれるスナップショットアイソレーション（SI）レベルの整合性を実装します。この分離レベルは、 [ANSIの繰り返し可能な読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)および[MySQLの繰り返し可能な読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)とは異なります。詳細については、 [TiDBトランザクション分離レベル](/transaction-isolation-levels.md)を参照してください。

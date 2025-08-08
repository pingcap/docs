---
title: Transaction overview
summary: TiDB のトランザクションの簡単な紹介。
---

# トランザクションの概要 {#transaction-overview}

TiDBは完全な分散トランザクションをサポートし、 [楽観的取引](/optimistic-transaction.md)と[悲観的取引](/pessimistic-transaction.md) （TiDB 3.0で導入）を提供します。この記事では主に、トランザクションステートメント、楽観的トランザクションと悲観的トランザクション、トランザクション分離レベル、そして楽観的トランザクションにおけるアプリケーション側の再試行とエラー処理について紹介します。

## よくある発言 {#common-statements}

この章では、TiDBにおけるトランザクションの使い方を紹介します。以下の例は、単純なトランザクションの処理を示しています。

ボブはアリスに20ドルを送金したいと考えています。この取引には2つの操作が含まれます。

-   ボブの口座残高は 20 ドル減少します。
-   アリスの口座残高は 20 ドル増加しました。

トランザクションにより、上記の操作の両方が正常に実行されるか、または両方とも失敗するかを確認できます。

[書店](/develop/dev-guide-bookshop-schema-design.md)データベースの`users`テーブルを使用して、テーブルにサンプル データを挿入します。

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

新しいトランザクションを明示的に開始するには、 `BEGIN`または`START TRANSACTION`いずれかを使用できます。

```sql
BEGIN;
```

```sql
START TRANSACTION;
```

TiDBのデフォルトのトランザクションモードは悲観的です。1 [楽観的取引モデル](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)明示的に指定することもできます。

```sql
BEGIN OPTIMISTIC;
```

[悲観的トランザクションモード](/develop/dev-guide-optimistic-and-pessimistic-transaction.md)を有効にする:

```sql
BEGIN PESSIMISTIC;
```

上記のステートメントが実行されたときに現在のセッションがトランザクションの途中である場合、TiDB はまず現在のトランザクションをコミットし、次に新しいトランザクションを開始します。

### トランザクションをコミットする {#commit-a-transaction}

`COMMIT`ステートメントを使用すると、現在のトランザクションで TiDB によって行われたすべての変更をコミットできます。

```sql
COMMIT;
```

楽観的トランザクションを有効にする前に、アプリケーションが`COMMIT`文によって返される可能性のあるエラーを適切に処理できることを確認してください。アプリケーションがどのように処理するか不明な場合は、代わりに悲観的トランザクションモードを使用することをお勧めします。

### トランザクションをロールバックする {#roll-back-a-transaction}

`ROLLBACK`ステートメントを使用して、現在のトランザクションの変更をロールバックできます。

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

クライアント接続が停止または閉じられた場合も、トランザクションは自動的にロールバックされます。

## トランザクション分離レベル {#transaction-isolation-levels}

トランザクション分離レベルは、**ACID**のトランザクション処理の基礎となります。ACIDの「I」（Isolation）は、トランザクションの分離を意味します。

SQL-92 標準では、次の 4 つの分離レベルが定義されています。

-   コミットされていない読み取り ( `READ UNCOMMITTED` )
-   コミットされた読み取り ( `READ COMMITTED` )
-   繰り返し読み取り ( `REPEATABLE READ` )
-   シリアル化可能（ `SERIALIZABLE` ）。

詳細については、以下の表を参照してください。

| 分離レベル            | ダーティライト | ダーティリード | ファジーリード | ファントム |
| ---------------- | ------- | ------- | ------- | ----- |
| READ UNCOMMITTED | 不可能     | 可能      | 可能      | 可能    |
| READ COMMITTED   | 不可能     | 不可能     | 可能      | 可能    |
| REPEATABLE READ  | 不可能     | 不可能     | 不可能     | 可能    |
| SERIALIZABLE     | 不可能     | 不可能     | 不可能     | 不可能   |

TiDB は次の分離レベルをサポートしています: `READ COMMITTED`と`REPEATABLE READ` :

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

TiDBは、MySQLとの一貫性を保つため、スナップショット分離（SI）レベルの一貫性（「繰り返し読み取り」とも呼ばれます）を実装しています。この分離レベルは[ANSI繰り返し読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-ansi-repeatable-read)および[MySQL 繰り返し読み取り分離レベル](/transaction-isolation-levels.md#difference-between-tidb-and-mysql-repeatable-read)とは異なります。詳細については、 [TiDBトランザクション分離レベル](/transaction-isolation-levels.md)参照してください。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

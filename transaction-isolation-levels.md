---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
---

# TiDBトランザクション分離レベル {#tidb-transaction-isolation-levels}

<CustomContent platform="tidb">

トランザクション分離は、データベーストランザクション処理の基盤の1つです。分離は、トランザクションの4つの主要なプロパティの1つです（一般に[酸](/glossary.md#acid)と呼ばれます）。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション分離は、データベーストランザクション処理の基盤の1つです。分離は、トランザクションの4つの主要なプロパティの1つです（一般に[酸](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます）。

</CustomContent>

SQL-92標準では、トランザクション分離の4つのレベルが定義されています。コミットされていない読み取り、コミットされた読み取り、繰り返し可能な読み取り、およびシリアル化可能です。詳細については、次の表を参照してください。

| 分離レベル          | ダーティライト | ダーティリード | ファジーリード | ファントム |
| :------------- | :------ | :------ | :------ | :---- |
| コミットされていない読み取り | ありえない   | 可能      | 可能      | 可能    |
| コミット済みを読む      | ありえない   | ありえない   | 可能      | 可能    |
| 繰り返し読む         | ありえない   | ありえない   | ありえない   | 可能    |
| シリアル化可能        | ありえない   | ありえない   | ありえない   | ありえない |

TiDBは、MySQLとの互換性のために`REPEATABLE-READ`としてアドバタイズするスナップショットアイソレーション（SI）整合性を実装します。これは、 [ANSI反復可能読み取り分離レベル](#difference-between-tidb-and-ansi-repeatable-read)および[MySQLの繰り返し可能な読み取りレベル](#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

> **ノート：**
>
> TiDB v3.0以降、トランザクションの自動再試行はデフォルトで無効になっています。自動再試行を有効にすると**、トランザクション分離レベル**が損なわれる可能性があるため、お勧めしません。詳細は[トランザクションの再試行](/optimistic-transaction.md#automatic-retry)を参照してください。
>
> TiDB v3.0.8以降、新しく作成されたTiDBクラスターはデフォルトで[悲観的なトランザクションモード](/pessimistic-transaction.md)を使用します。現在の読み取り（ `for update`の読み取り）は**繰り返し不可能な読み取り**です。詳細は[悲観的なトランザクションモード](/pessimistic-transaction.md)を参照してください。

## 繰り返し可能な読み取り分離レベル {#repeatable-read-isolation-level}

繰り返し可能読み取り分離レベルは、トランザクションが開始する前にコミットされたデータのみを確認し、コミットされていないデータや、同時トランザクションによるトランザクション実行中にコミットされた変更を確認することはありません。ただし、トランザクションステートメントは、まだコミットされていなくても、自身のトランザクション内で実行された以前の更新の影響を確認します。

異なるノードで実行されているトランザクションの場合、開始とコミットの順序は、タイムスタンプがPDから取得される順序によって異なります。

繰り返し可能読み取り分離レベルのトランザクションは、同じ行を同時に更新することはできません。コミット時に、トランザクションが開始後に別のトランザクションによって行が更新されていることをトランザクションが検出した場合、トランザクションはロールバックします。例えば：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### TiDBとANSIの繰り返し可能な読み取りの違い {#difference-between-tidb-and-ansi-repeatable-read}

TiDBの反復可能読み取り分離レベルはANSI反復可能読み取り分離レベルとは異なりますが、同じ名前を共有しています。 [ANSISQL分離レベルの批評](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)のペーパーで説明されている標準に従って、TiDBはスナップショット分離レベルを実装します。この分離レベルでは、厳密なファントム（A3）は許可されませんが、広いファントム（P3）と書き込みスキューは許可されます。対照的に、ANSI反復可能読み取り分離レベルでは、ファントム読み取りは許可されますが、書き込みスキューは許可されません。

### TiDBとMySQLの繰り返し可能な読み取りの違い {#difference-between-tidb-and-mysql-repeatable-read}

TiDBのRepeatableRead分離レベルは、MySQLのそれとは異なります。 MySQLのRepeatableRead分離レベルは、更新時に現在のバージョンが表示されているかどうかをチェックしません。つまり、トランザクションの開始後に行が更新された場合でも、更新を続行できます。対照的に、トランザクションの開始後に行が更新された場合、TiDBオプティミスティックトランザクションはロールバックされて再試行されます。 TiDBの楽観的同時実行制御でのトランザクションの再試行が失敗し、トランザクションの最終的な失敗につながる可能性がありますが、TiDBの悲観的同時実行制御とMySQLでは、トランザクションの更新が成功する可能性があります。

## コミットされた分離レベルを読み取る {#read-committed-isolation-level}

TiDB v4.0.0-beta以降、TiDBはReadCommitted分離レベルをサポートしています。

歴史的な理由から、現在の主流データベースの読み取りコミット分離レベルは基本的に[Oracleによって定義された一貫性のある読み取り分離レベル](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)です。この状況に適応するために、TiDBペシミスティックトランザクションの読み取りコミット分離レベルも、本質的に一貫した読み取り動作です。

> **ノート：**
>
> 読み取りコミット分離レベルは、 [悲観的なトランザクションモード](/pessimistic-transaction.md)でのみ有効です。 [楽観的なトランザクションモード](/optimistic-transaction.md)では、トランザクション分離レベルを`Read Committed`に設定しても有効にならず、トランザクションは引き続き繰り返し可能読み取り分離レベルを使用します。

## TiDBとMySQLReadCommittedの違い {#difference-between-tidb-and-mysql-read-committed}

MySQL Read Committed分離レベルは、ほとんどの場合、一貫性のある読み取り機能と一致しています。 [半一貫性のある読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)などの例外もあります。この特別な動作は、TiDBではサポートされていません。

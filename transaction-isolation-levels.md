---
title: TiDB Transaction Isolation Levels
summary: TiDB のトランザクション分離レベルについて学習します。
---

# TiDBトランザクション分離レベル {#tidb-transaction-isolation-levels}

<CustomContent platform="tidb">

トランザクション分離は、データベーストランザクション処理の基盤の一つです。分離は、トランザクションの4つの主要な特性（一般的に[ACID](/glossary.md#acid)と呼ばれます）の一つです。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション分離は、データベーストランザクション処理の基盤の一つです。分離は、トランザクションの4つの主要な特性（一般的に[ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます）の一つです。

</CustomContent>

SQL-92標準では、トランザクション分離レベルとして、Read Uncommitted、Read Committed、Repeatable Read、Serializableの4つのレベルが定義されています。詳細については、次の表をご覧ください。

| 分離レベル            | ダーティライト | ダーティリード | ファジーリード | ファントム |
| :--------------- | :------ | :------ | :------ | :---- |
| READ UNCOMMITTED | 不可能     | 可能      | 可能      | 可能    |
| READ COMMITTED   | 不可能     | 不可能     | 可能      | 可能    |
| REPEATABLE READ  | 不可能     | 不可能     | 不可能     | 可能    |
| SERIALIZABLE     | 不可能     | 不可能     | 不可能     | 不可能   |

TiDBはスナップショット分離（SI）一貫性を実装しており、MySQLとの互換性のために`REPEATABLE-READ`として宣伝されています。これはSI [ANSI繰り返し読み取り分離レベル](#difference-between-tidb-and-ansi-repeatable-read)やSI [MySQL 繰り返し読み取りレベル](#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

> **注記：**
>
> TiDB v3.0以降、トランザクションの自動再試行はデフォルトで無効になっています。自動再試行を有効にすると**、トランザクション分離レベルが損なわれる**可能性があるため、有効にすることは推奨されません。詳細は[トランザクションの再試行](/optimistic-transaction.md#automatic-retry)を参照してください。
>
> TiDB v3.0.8以降、新規に作成されたTiDBクラスタはデフォルトで[悲観的トランザクションモード](/pessimistic-transaction.md)使用します。現在の読み取り（ `for update`読み取り）**は繰り返し不可能な読み取り**です。詳細は[悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

## 繰り返し読み取り分離レベル {#repeatable-read-isolation-level}

リピータブルリード分離レベルでは、トランザクション開始前にコミットされたデータのみが参照され、コミットされていないデータや、トランザクション実行中に同時実行トランザクションによってコミットされた変更は参照されません。ただし、トランザクション文は、自身のトランザクション内で実行された以前の更新の影響を参照します。これらの更新は、まだコミットされていない場合でも参照されます。

異なるノードで実行されているトランザクションの場合、開始順序とコミット順序は、PD からタイムスタンプが取得される順序によって異なります。

反復可能読み取り分離レベルのトランザクションは、同じ行を同時に更新できません。コミット時に、トランザクション開始後に別のトランザクションによってその行が更新されたことがわかった場合、トランザクションはロールバックされます。例：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### TiDBとANSI繰り返し読み取りの違い {#difference-between-tidb-and-ansi-repeatable-read}

TiDBのRepeatable Read分離レベルは、ANSIのRepeatable Read分離レベルとは同じ名前ですが、異なります。1番目の[ANSI SQL分離レベルの批評](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)に記載されている標準によると、TiDBはスナップショット分離レベルを実装しています。この分離レベルでは、厳密なファントム（A3）は許可されませんが、広範囲のファントム（P3）とライトスキューは許可されます。一方、ANSIのRepeatable Read分離レベルでは、ファントムリードは許可されますが、ライトスキューは許可されません。

### TiDBとMySQLの繰り返し読み取りの違い {#difference-between-tidb-and-mysql-repeatable-read}

TiDBのRepeatable Read分離レベルは、MySQLのそれとは異なります。MySQLのRepeatable Read分離レベルでは、更新時に現在のバージョンが可視かどうかがチェックされないため、トランザクション開始後に行が更新された場合でも更新を続行できます。一方、TiDBの楽観的トランザクションでは、トランザクション開始後に行が更新された場合、ロールバックされて再試行されます。TiDBの楽観的同時実行制御ではトランザクションの再試行が失敗し、最終的にトランザクションが失敗する可能性がありますが、TiDBの悲観的同時実行制御とMySQLでは、更新トランザクションが成功する可能性があります。

## コミット読み取り分離レベル {#read-committed-isolation-level}

TiDB v4.0.0-beta 以降、TiDB は Read Committed 分離レベルをサポートします。

歴史的な理由により、現在主流のデータベースのRead Committed分離レベルは基本的に[Oracleが定義する一貫性読み取り分離レベル](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)です。この状況に対応するため、TiDBの悲観的トランザクションにおけるRead Committed分離レベルも、本質的には一貫性のある読み取り動作となっています。

> **注記：**
>
> Read Committed 分離レベルは[悲観的トランザクションモード](/pessimistic-transaction.md)でのみ有効になります。 [楽観的トランザクションモード](/optimistic-transaction.md)では、トランザクション分離レベルを`Read Committed`に設定しても有効にならず、トランザクションは引き続き Repeatable Read 分離レベルを使用します。

v6.0.0以降、TiDBは、読み取り/書き込み競合が稀なシナリオにおいて、タイムスタンプ取得を最適化するためにシステム変数[`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)使用をサポートします。この変数を有効にすると、TiDBは`SELECT`実行時に、前回の有効なタイムスタンプを使用してデータを読み取ろうとします。この変数の初期値は、トランザクションの`start_ts`です。

-   TiDB は読み取りプロセス中にデータ更新が発生しなかった場合、結果をクライアントに返し、 `SELECT`ステートメントが正常に実行されます。
-   TiDB が読み取りプロセス中にデータ更新を検出した場合:
    -   TiDB がまだ結果をクライアントに送信していない場合、TiDB は新しいタイムスタンプを取得してこのステートメントを再試行します。
    -   TiDBが既に部分的なデータをクライアントに送信している場合、TiDBはクライアントにエラーを報告します。クライアントに送信されるデータの量は、 [`tidb_init_chunk_size`](/system-variables.md#tidb_init_chunk_size)と[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size)によって制御されます。

分離レベル`READ-COMMITTED`が使用され、ステートメントが`SELECT`多く、読み取り/書き込みの競合がまれなシナリオでは、この変数を有効にすると、グローバル タイムスタンプを取得する際のレイテンシーとコストを回避できます。

v6.3.0以降、TiDBはポイント書き込みの競合が少ないシナリオにおいて、システム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)有効にすることでタイムスタンプ取得の最適化をサポートします。この変数を有効にすると、ポイント書き込みステートメントの実行中に、TiDBは現在のトランザクションの有効なタイムスタンプを使用してデータの読み取りとロックを試みます。3 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)有効になっている場合も、TiDBは同様にデータを読み取ります。

現在、適用可能なポイント書き込みステートメントの種類は`UPDATE` 、 `DELETE` 、 `SELECT ...... FOR UPDATE`です。ポイント書き込みステートメントとは、主キーまたは一意キーをフィルター条件として使用し、最終実行演算子に`POINT-GET`含まれる書き込みステートメントを指します。現在、3種類のポイント書き込みステートメントに共通するのは、まずキー値に基づいてポイントクエリを実行することです。キーが存在する場合は、キーをロックします。キーが存在しない場合は、空のセットを返します。

-   ポイント書き込みステートメントの読み取りプロセス全体で更新されたデータ バージョンが検出されない場合、TiDB は引き続き現在のトランザクションのタイムスタンプを使用してデータをロックします。
    -   ロック取得プロセス中に古いタイムスタンプが原因で書き込み競合が発生した場合、TiDB は最新のグローバル タイムスタンプを取得してロック取得プロセスを再試行します。
    -   ロック取得プロセス中に書き込み競合やその他のエラーが発生しない場合、ロックは正常に取得されます。
-   読み取りプロセス中に更新されたデータ バージョンが検出されると、TiDB は新しいタイムスタンプを取得してこのステートメントを再試行します。

ポイント書き込みステートメントは多いが、分離レベル`READ-COMMITTED`でのポイント書き込み競合が少ないトランザクションでは、この変数を有効にすると、グローバル タイムスタンプの取得のレイテンシーとオーバーヘッドを回避できます。

## TiDBとMySQLのRead Committedの違い {#difference-between-tidb-and-mysql-read-committed}

MySQLのRead Committed分離レベルは、ほとんどの場合、Consistent Read機能と一致します。ただし、 [半一貫性読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)ような例外もあります。この特殊な動作はTiDBではサポートされていません。

## トランザクション分離レベルのビューと変更 {#view-and-modify-transaction-isolation-levels}

トランザクション分離レベルは次のように表示および変更できます。

現在のセッションのトランザクション分離レベルをビュー。

```sql
SHOW VARIABLES LIKE 'transaction_isolation';
```

現在のセッションのトランザクション分離レベルを変更します。

```sql
SET SESSION transaction_isolation = 'READ-COMMITTED';
```

トランザクション分離レベルの構成と使用の詳細については、次のドキュメントを参照してください。

-   [システム変数`transaction_isolation`](/system-variables.md#transaction_isolation)
-   [分離レベル](/pessimistic-transaction.md#isolation-level)
-   [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md)

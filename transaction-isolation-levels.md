---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
---

# TiDBトランザクション分離レベル {#tidb-transaction-isolation-levels}

<CustomContent platform="tidb">

トランザクション分離は、データベース トランザクション処理の基礎の 1 つです。分離は、トランザクションの 4 つの主要なプロパティ (一般に[ACID](/glossary.md#acid)と呼ばれます) の 1 つです。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション分離は、データベース トランザクション処理の基礎の 1 つです。分離は、トランザクションの 4 つの主要なプロパティ (一般に[ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます) の 1 つです。

</CustomContent>

SQL-92 標準では、非コミット読み取り、コミット読み取り、反復可能読み取り、シリアル化可能という 4 つのレベルのトランザクション分離が定義されています。詳細については、次の表を参照してください。

| 分離レベル            | ダーティライト | ダーティリード | ファジーリード | ファントム |
| :--------------- | :------ | :------ | :------ | :---- |
| READ UNCOMMITTED | ありえない   | 可能      | 可能      | 可能    |
| READ COMMITTED   | ありえない   | ありえない   | 可能      | 可能    |
| REPEATABLE READ  | ありえない   | ありえない   | ありえない   | 可能    |
| SERIALIZABLE     | ありえない   | ありえない   | ありえない   | ありえない |

TiDB はスナップショット分離 (SI) 整合性を実装しており、MySQL との互換性のために`REPEATABLE-READ`として宣伝されています。これは[ANSI リピータブルリード分離レベル](#difference-between-tidb-and-ansi-repeatable-read)や[MySQL 反復読み取りレベル](#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

> **注記：**
>
> TiDB v3.0 以降、トランザクションの自動再試行はデフォルトで無効になっています。自動再試行を有効にすると、**トランザクション分離レベルが破壊される**可能性があるため、これはお勧めできません。詳細は[トランザクションの再試行](/optimistic-transaction.md#automatic-retry)を参照してください。
>
> TiDB v3.0.8 以降、新しく作成された TiDB クラスターはデフォルトで[悲観的トランザクションモード](/pessimistic-transaction.md)を使用します。現在の読み取り ( `for update`読み取り) は**反復不可能な読み取り**です。詳細は[悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

## 反復読み取り分離レベル {#repeatable-read-isolation-level}

リピータブルリード分離レベルでは、トランザクションの開始前にコミットされたデータのみが参照され、コミットされていないデータや、同時トランザクションによるトランザクション実行中にコミットされた変更は決して参照されません。ただし、トランザクション ステートメントには、まだコミットされていない場合でも、自身のトランザクション内で実行された以前の更新の影響が表示されます。

異なるノードで実行されているトランザクションの場合、開始順序とコミット順序は、タイムスタンプが PD から取得される順序によって異なります。

反復可能読み取り分離レベルのトランザクションは、同じ行を同時に更新できません。コミット時に、トランザクションの開始後に行が別のトランザクションによって更新されたことが検出されると、トランザクションはロールバックされます。例えば：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### TiDB と ANSI リピータブル リードの違い {#difference-between-tidb-and-ansi-repeatable-read}

TiDB のリピータブル リード分離レベルは、同じ名前を共有していますが、ANSI リピータブル リード分離レベルとは異なります。 [ANSI SQL 分離レベルの批判](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)論文で説明されている標準に従って、TiDB はスナップショット分離レベルを実装します。この分離レベルでは、厳密なファントム (A3) は許可されませんが、ブロードなファントム (P3) と書き込みスキューは許可されます。対照的に、ANSI リピータブル リード分離レベルでは、ファントム読み取りは許可されますが、書き込みスキューは許可されません。

### TiDB と MySQL 反復読み取りの違い {#difference-between-tidb-and-mysql-repeatable-read}

TiDB のRepeatable Read 分離レベルは、MySQL の分離レベルとは異なります。 MySQL のRepeatable Read 分離レベルは、更新時に現在のバージョンが表示されるかどうかをチェックしません。つまり、トランザクションの開始後に行が更新された場合でも更新を続けることができます。対照的に、トランザクションの開始後に行が更新された場合、TiDB楽観的トランザクションはロールバックされ、再試行されます。 TiDB の楽観的ミスティック同時実行制御でのトランザクションの再試行は失敗し、トランザクションの最終的な失敗につながる可能性がありますが、TiDB の悲観的ミスティック同時実行制御と MySQL では、トランザクションの更新は成功する可能性があります。

## コミットされた分離レベルの読み取り {#read-committed-isolation-level}

TiDB v4.0.0 ベータ以降、TiDB は Read Committed 分離レベルをサポートします。

歴史的な理由により、現在の主流データベースの Read Committed 分離レベルは基本的に[Oracle によって定義された Consistent Read 分離レベル](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)です。この状況に適応するために、TiDB悲観的トランザクションの Read Committed 分離レベルも、本質的には一貫した読み取り動作となります。

> **注記：**
>
> Read Committed 分離レベルは[悲観的トランザクションモード](/pessimistic-transaction.md)でのみ有効です。 [楽観的トランザクションモード](/optimistic-transaction.md)では、トランザクション分離レベルを`Read Committed`に設定しても有効にならず、トランザクションは依然としてRepeatable Read分離レベルを使用します。

v6.0.0 以降、TiDB は、読み取り/書き込みの競合がまれなシナリオでタイムスタンプの取得を最適化するために[`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)システム変数の使用をサポートします。この変数を有効にすると、TiDB は`SELECT`の実行時に以前の有効なタイムスタンプを使用してデータを読み取ろうとします。この変数の初期値はトランザクションの`start_ts`です。

-   TiDB が読み取りプロセス中にデータ更新に遭遇しなかった場合、結果がクライアントに返され、 `SELECT`ステートメントは正常に実行されます。
-   TiDB が読み取りプロセス中にデータ更新を検出した場合:
    -   TiDB がまだ結果をクライアントに送信していない場合、TiDB は新しいタイムスタンプを取得してこのステートメントを再試行しようとします。
    -   TiDB がすでに部分的なデータをクライアントに送信している場合、TiDB はクライアントにエラーを報告します。毎回クライアントに送信されるデータの量は、 `tidb_init_chunk_size`と`tidb_max_chunk_size`によって制御されます。

`READ-COMMITTED`分離レベルが使用されるシナリオでは、 `SELECT`のステートメントが多く、読み取り/書き込み競合が発生することはまれであるため、この変数を有効にすると、グローバル タイムスタンプの取得にかかるレイテンシーとコストを回避できます。

v6.3.0 以降、TiDB は、ポイントと書き込みの競合が少ないシナリオでシステム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)を有効にすることにより、タイムスタンプの取得の最適化をサポートします。この変数を有効にすると、ポイント書き込みステートメントの実行中に、TiDB は現在のトランザクションの有効なタイムスタンプを使用してデータを読み取り、ロックしようとします。 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)が有効な場合、TiDB は同じ方法でデータを読み取ります。

現在、適用可能な point-write ステートメントのタイプには、 `UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE`が含まれます。 point-write ステートメントは、主キーまたは一意キーをフィルター条件として使用し、最終的な実行演算子に`POINT-GET`が含まれる write ステートメントを指します。現在、3 種類のポイント書き込みステートメントには次の共通点があります。まず、キー値に基づいてポイント クエリを実行します。キーが存在する場合は、キーをロックします。キーが存在しない場合は、空のセットが返されます。

-   point-write ステートメントの読み取りプロセス全体で更新されたデータ バージョンが発生しない場合、TiDB は引き続き現在のトランザクションのタイムスタンプを使用してデータをロックします。
    -   ロック取得プロセス中に古いタイムスタンプが原因で書き込み競合が発生した場合、TiDB は最新のグローバル タイムスタンプを取得してロック取得プロセスを再試行します。
    -   ロック取得プロセス中に書き込み競合やその他のエラーが発生しなければ、ロックは正常に取得されます。
-   読み取りプロセス中に更新されたデータ バージョンが発生した場合、TiDB は新しいタイムスタンプの取得を試み、このステートメントを再試行します。

分離レベル`READ-COMMITTED`で多くのポイント書き込みステートメントがあり、少数のポイント書き込み競合があるトランザクションでは、この変数を有効にすると、グローバル タイムスタンプの取得に伴うレイテンシーとオーバーヘッドを回避できます。

## TiDB と MySQL の Read Committed の違い {#difference-between-tidb-and-mysql-read-committed}

MySQL Read Committed 分離レベルは、ほとんどの場合、Consistent Read 機能と一致します。 [半一貫した読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)などの例外もあります。この特別な動作は TiDB ではサポートされていません。

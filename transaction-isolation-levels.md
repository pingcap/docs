---
title: TiDB Transaction Isolation Levels
summary: TiDB のトランザクション分離レベルについて学習します。
---

# TiDBトランザクション分離レベル {#tidb-transaction-isolation-levels}

<CustomContent platform="tidb">

トランザクション分離は、データベース トランザクション処理の基礎の 1 つです。分離は、トランザクションの 4 つの主要なプロパティの 1 つです (一般に[ACID](/glossary.md#acid)と呼ばれます)。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション分離は、データベース トランザクション処理の基礎の 1 つです。分離は、トランザクションの 4 つの主要なプロパティの 1 つです (一般に[ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます)。

</CustomContent>

SQL-92 標準では、トランザクション分離の 4 つのレベル (Read Uncommitted、Read Committed、Repeatable Read、Serializable) が定義されています。詳細については、次の表を参照してください。

| 分離レベル            | ダーティライト | ダーティリード | ファジーリード | ファントム |
| :--------------- | :------ | :------ | :------ | :---- |
| READ UNCOMMITTED | 不可能     | 可能      | 可能      | 可能    |
| READ COMMITTED   | 不可能     | 不可能     | 可能      | 可能    |
| REPEATABLE READ  | 不可能     | 不可能     | 不可能     | 可能    |
| SERIALIZABLE     | 不可能     | 不可能     | 不可能     | 不可能   |

TiDB は、MySQL との互換性のために`REPEATABLE-READ`として宣伝されているスナップショット分離 (SI) 一貫性を実装しています。これは[ANSI 繰り返し読み取り分離レベル](#difference-between-tidb-and-ansi-repeatable-read)および[MySQL 繰り返し読み取りレベル](#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

> **注記：**
>
> TiDB v3.0 以降では、トランザクションの自動再試行はデフォルトで無効になっています。自動再試行を有効にすると、**トランザクション分離レベルが破られる**可能性があるため、有効にすることは推奨されません。詳細については[トランザクションの再試行](/optimistic-transaction.md#automatic-retry)を参照してください。
>
> TiDB v3.0.8 以降、新しく作成された TiDB クラスターはデフォルトで[悲観的トランザクションモード](/pessimistic-transaction.md)使用します。現在の読み取り ( `for update`読み取り) は**繰り返し不可能な読み取り**です。詳細については[悲観的トランザクションモード](/pessimistic-transaction.md)を参照してください。

## 繰り返し読み取り分離レベル {#repeatable-read-isolation-level}

繰り返し読み取り分離レベルでは、トランザクションの開始前にコミットされたデータのみが表示され、コミットされていないデータや、同時トランザクションによってトランザクション実行中にコミットされた変更は表示されません。ただし、トランザクション ステートメントでは、まだコミットされていなくても、自身のトランザクション内で実行された以前の更新の影響が表示されます。

異なるノードで実行されているトランザクションの場合、開始順序とコミット順序は、PD からタイムスタンプが取得される順序によって異なります。

Repeatable Read 分離レベルのトランザクションは、同じ行を同時に更新できません。コミット時に、トランザクションの開始後に別のトランザクションによって行が更新されたことがトランザクションによって検出された場合、トランザクションはロールバックされます。例:

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### TiDB と ANSI 繰り返し読み取りの違い {#difference-between-tidb-and-ansi-repeatable-read}

TiDB の Repeatable Read 分離レベルは、同じ名前を共有していますが、ANSI Repeatable Read 分離レベルとは異なります。1 [ANSI SQL 分離レベルの批評](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)論文に記載されている標準によると、TiDB はスナップショット分離レベルを実装しています。この分離レベルでは、厳密なファントム (A3) は許可されませんが、広範なファントム (P3) と書き込みスキューは許可されます。対照的に、ANSI Repeatable Read 分離レベルでは、ファントム読み取りは許可されますが、書き込みスキューは許可されません。

### TiDB と MySQL の繰り返し読み取りの違い {#difference-between-tidb-and-mysql-repeatable-read}

TiDB の Repeatable Read 分離レベルは、MySQL のそれとは異なります。MySQL の Repeatable Read 分離レベルでは、更新時に現在のバージョンが可視かどうかがチェックされないため、トランザクションの開始後に行が更新された場合でも更新を続行できます。対照的に、トランザクションの開始後に行が更新された場合、TiDB の楽観的トランザクションはロールバックされ、再試行されます。TiDB の楽観的同時実行制御でのトランザクションの再試行は失敗し、最終的にトランザクションが失敗する可能性がありますが、TiDB の悲観的同時実行制御と MySQL では、更新トランザクションが成功する可能性があります。

## コミット読み取り分離レベル {#read-committed-isolation-level}

TiDB v4.0.0-beta 以降、TiDB は Read Committed 分離レベルをサポートします。

歴史的な理由により、現在の主流データベースの Read Committed 分離レベルは本質的に[Oracleによって定義された一貫性のある読み取り分離レベル](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)です。この状況に適応するために、TiDB悲観的トランザクションの Read Committed 分離レベルも本質的には一貫した読み取り動作です。

> **注記：**
>
> Read Committed 分離レベルは[悲観的トランザクションモード](/pessimistic-transaction.md)でのみ有効です。 [楽観的トランザクションモード](/optimistic-transaction.md)では、トランザクション分離レベルを`Read Committed`に設定しても有効にならず、トランザクションは引き続き Repeatable Read 分離レベルを使用します。

v6.0.0 以降、TiDB は、読み取り/書き込み競合がまれなシナリオでタイムスタンプの取得を最適化するために、 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)システム変数の使用をサポートしています。この変数を有効にすると、 `SELECT`実行されたときに、TiDB は以前の有効なタイムスタンプを使用してデータを読み取ろうとします。この変数の初期値は、トランザクションの`start_ts`です。

-   TiDB は読み取りプロセス中にデータ更新が発生しなかった場合、結果をクライアントに返し、 `SELECT`ステートメントが正常に実行されます。
-   TiDB が読み取りプロセス中にデータ更新を検出した場合:
    -   TiDB がまだ結果をクライアントに送信していない場合、TiDB は新しいタイムスタンプを取得してこのステートメントを再試行します。
    -   TiDB がすでに部分的なデータをクライアントに送信している場合、TiDB はクライアントにエラーを報告します。クライアントに送信されるデータの量は、 [`tidb_init_chunk_size`](/system-variables.md#tidb_init_chunk_size)と[`tidb_max_chunk_size`](/system-variables.md#tidb_max_chunk_size)によって制御されます。

`READ-COMMITTED`分離レベルが使用され、 `SELECT`ステートメントが多く、読み取り/書き込みの競合がまれなシナリオでは、この変数を有効にすると、グローバル タイムスタンプを取得する際のレイテンシーとコストを回避できます。

v6.3.0 以降、TiDB は、ポイント書き込みの競合が少ないシナリオでシステム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)を有効にすることで、タイムスタンプの取得を最適化することをサポートしています。この変数を有効にすると、ポイント書き込みステートメントの実行中に、TiDB は現在のトランザクションの有効なタイムスタンプを使用してデータを読み取り、ロックしようとします[`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)が有効になっている場合、TiDB は同じ方法でデータを読み取ります。

現在、適用可能なポイント書き込みステートメントのタイプには、 `UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE`があります。ポイント書き込みステートメントとは、主キーまたは一意のキーをフィルター条件として使用し、最終実行演算子に`POINT-GET`含まれる書き込みステートメントを指します。現在、3 種類のポイント書き込みステートメントには、最初にキー値に基づいてポイント クエリを実行するという共通点があります。キーが存在する場合は、キーをロックします。キーが存在しない場合は、空のセットを返します。

-   ポイント書き込みステートメントの読み取りプロセス全体で更新されたデータ バージョンが検出されない場合、TiDB は引き続き現在のトランザクションのタイムスタンプを使用してデータをロックします。
    -   ロック取得プロセス中に古いタイムスタンプが原因で書き込み競合が発生した場合、TiDB は最新のグローバル タイムスタンプを取得してロック取得プロセスを再試行します。
    -   ロック取得プロセス中に書き込み競合やその他のエラーが発生しない場合、ロックは正常に取得されます。
-   読み取りプロセス中に更新されたデータ バージョンが検出されると、TiDB は新しいタイムスタンプを取得してこのステートメントを再試行します。

ポイント書き込みステートメントは多いが、分離レベル`READ-COMMITTED`でのポイント書き込み競合が少ないトランザクションでは、この変数を有効にすると、グローバル タイムスタンプの取得のレイテンシーとオーバーヘッドを回避できます。

## TiDB と MySQL Read Committed の違い {#difference-between-tidb-and-mysql-read-committed}

MySQL の Read Committed 分離レベルは、ほとんどの場合、Consistent Read 機能と一致します。 [半一貫性のある読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)などの例外もあります。この特殊な動作は TiDB ではサポートされていません。

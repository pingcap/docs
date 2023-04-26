---
title: TiDB Transaction Isolation Levels
summary: Learn about the transaction isolation levels in TiDB.
---

# TiDBトランザクション分離レベル {#tidb-transaction-isolation-levels}

<CustomContent platform="tidb">

トランザクション分離は、データベース トランザクション処理の基盤の 1 つです。分離は、トランザクションの 4 つの主要なプロパティの 1 つです (一般に[ACID](/glossary.md#acid)と呼ばれます)。

</CustomContent>

<CustomContent platform="tidb-cloud">

トランザクション分離は、データベース トランザクション処理の基盤の 1 つです。分離は、トランザクションの 4 つの主要なプロパティの 1 つです (一般に[ACID](/tidb-cloud/tidb-cloud-glossary.md#acid)と呼ばれます)。

</CustomContent>

SQL-92 標準では、4 つのレベルのトランザクション分離が定義されています。Read Uncommitted、Read Committed、Repeatable Read、Serializable です。詳細については、次の表を参照してください。

| 分離レベル            | ダーティーライト | ダーティリード | ファジーリード | ファントム |
| :--------------- | :------- | :------ | :------ | :---- |
| READ UNCOMMITTED | ありえない    | 可能      | 可能      | 可能    |
| READ COMMITTED   | ありえない    | ありえない   | 可能      | 可能    |
| REPEATABLE READ  | ありえない    | ありえない   | ありえない   | 可能    |
| SERIALIZABLE     | ありえない    | ありえない   | ありえない   | ありえない |

TiDB は Snapshot Isolation (SI) 整合性を実装しており、MySQL との互換性のために`REPEATABLE-READ`として宣伝しています。これは[ANSI Repeatable Read 分離レベル](#difference-between-tidb-and-ansi-repeatable-read)および[MySQL 反復可能読み取りレベル](#difference-between-tidb-and-mysql-repeatable-read)とは異なります。

> **ノート：**
>
> TiDB v3.0 以降、トランザクションの自動再試行はデフォルトで無効になっています。自動再試行を有効にすることは、**トランザクション分離レベルを壊す**可能性があるためお勧めしません。詳細は[トランザクションの再試行](/optimistic-transaction.md#automatic-retry)を参照してください。
>
> TiDB v3.0.8 以降、新しく作成された TiDB クラスターはデフォルトで[悲観的トランザクション モード](/pessimistic-transaction.md)を使用します。現在の読み取り ( `for update`読み取り) は**繰り返し不可の読み取り**です。詳細は[悲観的トランザクション モード](/pessimistic-transaction.md)を参照してください。

## 反復可能読み取り分離レベル {#repeatable-read-isolation-level}

Repeatable Read 分離レベルでは、トランザクションの開始前にコミットされたデータのみが表示され、コミットされていないデータや同時トランザクションによるトランザクション実行中にコミットされた変更は表示されません。ただし、トランザクション ステートメントは、まだコミットされていなくても、自身のトランザクション内で実行された以前の更新の影響を確認します。

異なるノードで実行されているトランザクションの場合、開始およびコミットの順序は、タイムスタンプが PD から取得される順序によって異なります。

Repeatable Read 分離レベルのトランザクションは、同じ行を同時に更新できません。コミット時に、トランザクションの開始後に行が別のトランザクションによって更新されたことをトランザクションが検出すると、トランザクションはロールバックします。例えば：

```sql
create table t1(id int);
insert into t1 values(0);

start transaction;              |               start transaction;
select * from t1;               |               select * from t1;
update t1 set id=id+1;          |               update t1 set id=id+1; -- In pessimistic transactions, the `update` statement executed later waits for the lock until the transaction holding the lock commits or rolls back and releases the row lock.
commit;                         |
                                |               commit; -- The transaction commit fails and rolls back. Pessimistic transactions can commit successfully.
```

### TiDB と ANSI 反復可能読み取りの違い {#difference-between-tidb-and-ansi-repeatable-read}

TiDB の Repeatable Read 分離レベルは ANSI Repeatable Read 分離レベルとは異なりますが、同じ名前を共有しています。 [ANSI SQL 分離レベルの批判](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-95-51.pdf)論文で説明されている標準に従って、TiDB はスナップショット分離レベルを実装しています。この分離レベルでは、厳密なファントム (A3) は許可されませんが、幅広いファントム (P3) と書き込みスキューは許可されます。対照的に、ANSI Repeatable Read 分離レベルでは、ファントム読み取りは許可されますが、書き込みスキューは許可されません。

### TiDB と MySQL の反復可能読み取りの違い {#difference-between-tidb-and-mysql-repeatable-read}

TiDB の Repeatable Read 分離レベルは、MySQL とは異なります。 MySQL Repeatable Read 分離レベルは、更新時に現在のバージョンが表示されるかどうかをチェックしません。つまり、トランザクションの開始後に行が更新されていても、更新を続行できます。対照的に、トランザクションの開始後に行が更新された場合、TiDB楽観的トランザクションはロールバックされ、再試行されます。 TiDB の楽観的実行制御でのトランザクションの再試行は失敗し、トランザクションの最終的な失敗につながる可能性がありますが、TiDB の悲観的同時実行制御と MySQL では、更新トランザクションが成功する可能性があります。

## 読み取りコミット分離レベル {#read-committed-isolation-level}

TiDB v4.0.0-beta 以降、TiDB は Read Committed 分離レベルをサポートしています。

歴史的な理由から、現在のメインストリーム データベースの Read Committed 分離レベルは基本的に[Oracle によって定義された一貫性のある読み取り分離レベル](https://docs.oracle.com/cd/B19306_01/server.102/b14220/consist.htm)です。この状況に適応するために、TiDB悲観的トランザクションの Read Committed 分離レベルも本質的に一貫した読み取り動作です。

> **ノート：**
>
> Read Committed 分離レベルは[悲観的トランザクション モード](/pessimistic-transaction.md)でのみ有効です。 [楽観的トランザクション モード](/optimistic-transaction.md)では、トランザクション分離レベルを`Read Committed`に設定しても効果がなく、トランザクションは引き続き Repeatable Read 分離レベルを使用します。

v6.0.0 以降、TiDB は[`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)システム変数を使用して、読み取りと書き込みの競合がまれなシナリオでタイムスタンプの取得を最適化することをサポートしています。この変数を有効にした後、TiDB は`SELECT`が実行されたときに以前の有効なタイムスタンプを使用してデータを読み取ろうとします。この変数の初期値はトランザクションの`start_ts`です。

-   読み取りプロセス中に TiDB がデータ更新に遭遇しなかった場合、TiDB は結果をクライアントに返し、 `SELECT`ステートメントは正常に実行されます。
-   TiDB が読み取りプロセス中にデータ更新を検出した場合:
    -   TiDB がまだ結果をクライアントに送信していない場合、TiDB は新しいタイムスタンプを取得して、このステートメントを再試行しようとします。
    -   TiDB がすでに部分的なデータをクライアントに送信している場合、TiDB はクライアントにエラーを報告します。毎回クライアントに送信されるデータの量は、 `tidb_init_chunk_size`と`tidb_max_chunk_size`によって制御されます。

`READ-COMMITTED`分離レベルが使用され、 `SELECT`ステートメントが多く、読み取りと書き込みの競合がまれなシナリオでは、この変数を有効にすると、グローバル タイムスタンプを取得するためのレイテンシーとコストを回避できます。

v6.3.0 以降、TiDB は、ポイント書き込み競合がほとんどないシナリオでシステム変数[`tidb_rc_write_check_ts`](/system-variables.md#tidb_rc_write_check_ts-new-in-v630)を有効にすることにより、タイムスタンプの取得の最適化をサポートします。この変数を有効にした後、ポイント書き込みステートメントの実行中に、TiDB は現在のトランザクションの有効なタイムスタンプを使用してデータの読み取りとロックを試みます。 [`tidb_rc_read_check_ts`](/system-variables.md#tidb_rc_read_check_ts-new-in-v600)が有効な場合、TiDB は同じ方法でデータを読み取ります。

現在、適用可能なポイント書き込みステートメントのタイプには、 `UPDATE` 、 `DELETE` 、および`SELECT ...... FOR UPDATE`が含まれます。ポイント書き込みステートメントとは、主キーまたは一意キーをフィルター条件として使用し、最終実行演算子に`POINT-GET`を含む書き込みステートメントを指します。現在、3 種類のポイント書き込みステートメントには共通点があります。まず、キー値に基づいてポイント クエリを実行します。キーが存在する場合は、キーをロックします。キーが存在しない場合、空のセットを返します。

-   ポイントライト ステートメントの読み取りプロセス全体で更新されたデータ バージョンが検出されない場合、TiDB は引き続き現在のトランザクションのタイムスタンプを使用してデータをロックします。
    -   ロック取得プロセス中に古いタイムスタンプが原因で書き込み競合が発生した場合、TiDB は最新のグローバル タイムスタンプを取得してロック取得プロセスを再試行します。
    -   ロック取得プロセス中に書き込み競合やその他のエラーが発生しなければ、ロックは正常に取得されます。
-   読み取りプロセス中に更新されたデータ バージョンが検出された場合、TiDB は新しいタイムスタンプの取得を試み、このステートメントを再試行します。

多くのポイント書き込みステートメントがあり、分離レベル`READ-COMMITTED`でポイント書き込み競合がいくつかあるトランザクションでは、この変数を有効にすると、グローバル タイムスタンプを取得する際のレイテンシーとオーバーヘッドを回避できます。

## TiDB と MySQL Read Committed の違い {#difference-between-tidb-and-mysql-read-committed}

MySQL Read Committed 分離レベルは、ほとんどの場合、Consistent Read 機能と一致しています。 [半一貫性の読み取り](https://dev.mysql.com/doc/refman/8.0/en/innodb-transaction-isolation-levels.html)などの例外もあります。この特別な動作は TiDB ではサポートされていません。

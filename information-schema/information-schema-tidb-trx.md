---
title: TIDB_TRX
summary: Learn the `TIDB_TRX` INFORMATION_SCHEMA table.
---

# TIDB_TRX {#tidb-trx}

表`TIDB_TRX`は、TiDB ノード上で現在実行されているトランザクションに関する情報を提供します。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_TRX;
```

出力は次のとおりです。

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

`TIDB_TRX`テーブルの各列フィールドの意味は次のとおりです。

-   `ID` : トランザクション ID。トランザクションの`start_ts` (開始タイムスタンプ) です。
-   `START_TIME` : トランザクションの開始時刻。トランザクションの`start_ts`に対応する物理時間です。
-   `CURRENT_SQL_DIGEST` : トランザクション内で現在実行されている SQL ステートメントのダイジェスト。
-   `CURRENT_SQL_DIGEST_TEXT` : トランザクションによって現在実行されている SQL ステートメントの正規化された形式、つまり引数と形式のない SQL ステートメント。 `CURRENT_SQL_DIGEST`に相当します。
-   `STATE` : トランザクションの現在の状態。可能な値は次のとおりです。
    -   `Idle` : トランザクションはアイドル状態です。つまり、ユーザーがクエリを入力するのを待っています。
    -   `Running` : トランザクションはクエリを実行しています。
    -   `LockWaiting` : トランザクションは悲観的ロックの取得を待機しています。トランザクションは、他のトランザクションによってブロックされているかどうかに関係なく、悲観的ロック操作の開始時にこの状態になることに注意してください。
    -   `Committing` : トランザクションはコミット中です。
    -   `RollingBack` : トランザクションはロールバック中です。
-   `WAITING_START_TIME` : `STATE`の値が`LockWaiting`の場合、この列は待機の開始時刻を示します。
-   `MEM_BUFFER_KEYS` : 現在のトランザクションによってメモリバッファに書き込まれたキーの数。
-   `MEM_BUFFER_BYTES` : 現在のトランザクションによってメモリバッファに書き込まれたキーと値の合計バイト数。
-   `SESSION_ID` : このトランザクションが属するセッションの ID。
-   `USER` : トランザクションを実行するユーザーの名前。
-   `DB` : トランザクションが実行されるセッションの現在のデフォルトのデータベース名。
-   `ALL_SQL_DIGESTS` : トランザクションによって実行されたステートメントのダイジェスト リスト。リストは JSON 形式の文字列配列として表示されます。各トランザクションは最大で最初の 50 ステートメントを記録します。 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数を使用すると、この列の情報を、対応する正規化された SQL ステートメントのリストに変換できます。
-   `RELATED_TABLE_IDS` : トランザクションがアクセスするテーブル、ビュー、およびその他のオブジェクトの ID。

> **注記：**
>
> -   [プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみが、この表の完全な情報を取得できます。 PROCESS 権限を持たないユーザーは、現在のユーザーが実行したトランザクションの情報のみを照会できます。
> -   `CURRENT_SQL_DIGEST`目と`ALL_SQL_DIGESTS`列目の情報（SQLダイジェスト）は、正規化されたSQL文から計算されたハッシュ値です。 `CURRENT_SQL_DIGEST_TEXT`列の情報と`TIDB_DECODE_SQL_DIGESTS`関数から返された結果は、ステートメント概要テーブルから内部的にクエリされるため、対応するステートメントが内部で見つからない可能性があります。 SQL ダイジェストとステートメント概要テーブルの詳細については、 [ステートメント概要テーブル](/statement-summary-tables.md)を参照してください。
> -   [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数呼び出しにはオーバーヘッドが高くなります。多数のトランザクションの履歴 SQL ステートメントをクエリするために関数が呼び出された場合、クエリに時間がかかる可能性があります。クラスターが大きく、多くの同時トランザクションがある場合は、 `TIDB_TRX`のテーブル全体をクエリするときに、この関数を`ALL_SQL_DIGEST`列で直接使用することは避けてください。これは、 `SELECT *, tidb_decode_sql_digests(all_sql_digests) FROM TIDB_TRX`のような SQL ステートメントを避けることを意味します。
> -   現在、 `TIDB_TRX`テーブルは TiDB 内部トランザクションの情報の表示をサポートしていません。

## 例 {#example}

`TIDB_TRX`テーブルをビュー。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
                     ID: 426789913200689153
             START_TIME: 2021-08-04 10:51:54.883000
     CURRENT_SQL_DIGEST: NULL
CURRENT_SQL_DIGEST_TEXT: NULL
                  STATE: Idle
     WAITING_START_TIME: NULL
        MEM_BUFFER_KEYS: 1
       MEM_BUFFER_BYTES: 29
             SESSION_ID: 7
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
*************************** 2. row ***************************
                     ID: 426789921471332353
             START_TIME: 2021-08-04 10:52:26.433000
     CURRENT_SQL_DIGEST: 38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821
CURRENT_SQL_DIGEST_TEXT: update `t` set `v` = `v` + ? where `id` = ?
                  STATE: LockWaiting
     WAITING_START_TIME: 2021-08-04 10:52:35.106568
        MEM_BUFFER_KEYS: 0
       MEM_BUFFER_BYTES: 0
             SESSION_ID: 9
                   USER: root
                     DB: test
        ALL_SQL_DIGESTS: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
2 rows in set (0.01 sec)
```

この例のクエリ結果から、現在のノードには 2 つの進行中のトランザクションがあることがわかります。 1 つのトランザクションはアイドル状態 ( `STATE`は`Idle` 、 `CURRENT_SQL_DIGEST`は`NULL` ) にあり、このトランザクションは 3 つのステートメントを実行しました ( `ALL_SQL_DIGESTS`リストには 3 つのレコードがあり、これらは実行された 3 つの SQL ステートメントのダイジェストです)。別のトランザクションがステートメントを実行し、ロックを待機しています ( `STATE`は`LockWaiting` `WAITING_START_TIME`待機中のロックの開始時間を示します)。トランザクションは 2 つのステートメントを実行しました。現在実行中のステートメントは``"update `t` set `v` = `v` + ? where `id` = ?"``の形式です。

```sql
SELECT id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) AS all_sqls FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

出力は次のとおりです。

```sql
*************************** 1. row ***************************
             id: 426789913200689153
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","04fa858fa491c62d194faec2ab427261cc7998b3f1ccf8f6844febca504cb5e9","b83710fa8ab7df8504920e8569e48654f621cf828afbe7527fd003b79f48da9e"]
       all_sqls: ["begin","insert into `t` values ( ... )","update `t` set `v` = `v` + ?"]
*************************** 2. row ***************************
             id: 426789921471332353
all_sql_digests: ["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821"]
       all_sqls: ["begin","update `t` set `v` = `v` + ? where `id` = ?"]
```

このクエリは、 `TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列で[`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数を呼び出し、システム内部クエリを通じて SQL ダイジェスト配列を正規化された SQL ステートメントの配列に変換します。これは、トランザクションによって過去に実行されたステートメントの情報を視覚的に取得するのに役立ちます。ただし、前述のクエリは`TIDB_TRX`のテーブル全体をスキャンし、行ごとに`TIDB_DECODE_SQL_DIGESTS`関数を呼び出すことに注意してください。 `TIDB_DECODE_SQL_DIGESTS`関数の呼び出しには高いオーバーヘッドがかかります。したがって、クラスター内に多数の同時トランザクションが存在する場合は、このタイプのクエリを避けるようにしてください。

## CLUSTER_TIDB_TRX {#cluster-tidb-trx}

`TIDB_TRX`テーブルは、単一の TiDB ノードで実行されているトランザクションに関する情報のみを提供します。クラスター全体のすべての TiDB ノードで実行されているトランザクションの情報を表示したい場合は、 `CLUSTER_TIDB_TRX`テーブルをクエリする必要があります。 `TIDB_TRX`テーブルのクエリ結果と比較して、 `CLUSTER_TIDB_TRX`テーブルのクエリ結果には追加の`INSTANCE`フィールドが含まれています。 `INSTANCE`フィールドには、クラスター内の各ノードの IP アドレスとポートが表示されます。これは、トランザクションが存在する TiDB ノードを区別するために使用されます。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_TRX;
```

出力は次のとおりです。

```sql
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| Field                   | Type                                                            | Null | Key  | Default | Extra |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
| INSTANCE                | varchar(64)                                                     | YES  |      | NULL    |       |
| ID                      | bigint(21) unsigned                                             | NO   | PRI  | NULL    |       |
| START_TIME              | timestamp(6)                                                    | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST      | varchar(64)                                                     | YES  |      | NULL    |       |
| CURRENT_SQL_DIGEST_TEXT | text                                                            | YES  |      | NULL    |       |
| STATE                   | enum('Idle','Running','LockWaiting','Committing','RollingBack') | YES  |      | NULL    |       |
| WAITING_START_TIME      | timestamp(6)                                                    | YES  |      | NULL    |       |
| MEM_BUFFER_KEYS         | bigint(64)                                                      | YES  |      | NULL    |       |
| MEM_BUFFER_BYTES        | bigint(64)                                                      | YES  |      | NULL    |       |
| SESSION_ID              | bigint(21) unsigned                                             | YES  |      | NULL    |       |
| USER                    | varchar(16)                                                     | YES  |      | NULL    |       |
| DB                      | varchar(64)                                                     | YES  |      | NULL    |       |
| ALL_SQL_DIGESTS         | text                                                            | YES  |      | NULL    |       |
| RELATED_TABLE_IDS       | text                                                            | YES  |      | NULL    |       |
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
14 rows in set (0.00 sec)
```

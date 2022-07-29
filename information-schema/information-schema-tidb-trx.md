---
title: TIDB_TRX
summary: Learn the `TIDB_TRX` information_schema table.
---

# TIDB_TRX {#tidb-trx}

`TIDB_TRX`の表は、TiDBノードで現在実行されているトランザクションに関する情報を提供します。

{{< copyable "" >}}

```sql
USE information_schema;
DESC tidb_trx;
```

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
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

`TIDB_TRX`テーブルの各列フィールドの意味は次のとおりです。

-   `ID` ：トランザクションID。トランザクションの`start_ts` （開始タイムスタンプ）です。
-   `START_TIME` ：トランザクションの開始時刻。これは、トランザクションの`start_ts`に対応する物理的な時刻です。
-   `CURRENT_SQL_DIGEST` ：トランザクションで現在実行されているSQLステートメントのダイジェスト。
-   `CURRENT_SQL_DIGEST_TEXT` ：トランザクションによって現在実行されているSQLステートメントの正規化された形式、つまり、引数と形式のないSQLステートメント。 `CURRENT_SQL_DIGEST`に対応します。
-   `STATE` ：トランザクションの現在の状態。可能な値は次のとおりです：
    -   `Idle` ：トランザクションはアイドル状態です。つまり、ユーザーがクエリを入力するのを待っています。
    -   `Running` ：トランザクションはクエリを実行しています。
    -   `LockWaiting` ：トランザクションはペシミスティックロックが取得されるのを待っています。トランザクションは、他のトランザクションによってブロックされているかどうかに関係なく、ペシミスティックロック操作の開始時にこの状態になることに注意してください。
    -   `Committing` ：トランザクションはコミット中です。
    -   `RollingBack` ：トランザクションはロールバックされています。
-   `WAITING_START_TIME` ： `STATE`の値が`LockWaiting`の場合、この列には待機の開始時刻が表示されます。
-   `MEM_BUFFER_KEYS` ：現在のトランザクションによってメモリバッファに書き込まれたキーの数。
-   `MEM_BUFFER_BYTES` ：現在のトランザクションによってメモリバッファに書き込まれたKey-Valueバイトの総数。
-   `SESSION_ID` ：このトランザクションが属するセッションのID。
-   `USER` ：トランザクションを実行するユーザーの名前。
-   `DB` ：トランザクションが実行されるセッションの現在のデフォルトデータベース名。
-   `ALL_SQL_DIGESTS` ：トランザクションによって実行されたステートメントのダイジェストリスト。リストは、JSON形式の文字列配列として表示されます。各トランザクションは、最大で最初の50個のステートメントを記録します。 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数を使用すると、この列の情報を対応する正規化されたSQLステートメントのリストに変換できます。

> **ノート：**
>
> -   このテーブルの完全な情報を取得できるのは、 [処理する](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)の特権を持つユーザーのみです。 PROCESS権限を持たないユーザーは、現在のユーザーによって実行されたトランザクションの情報のみを照会できます。
> -   `CURRENT_SQL_DIGEST`列と`ALL_SQL_DIGESTS`列の情報（SQLダイジェスト）は、正規化されたSQLステートメントから計算されたハッシュ値です。 `CURRENT_SQL_DIGEST_TEXT`列の情報と`TIDB_DECODE_SQL_DIGESTS`関数から返される結果は、ステートメントの要約テーブルから内部的に照会されるため、対応するステートメントが内部で見つからない可能性があります。 SQLダイジェストとステートメントの要約テーブルの詳細については、 [ステートメント要約表](/statement-summary-tables.md)を参照してください。
> -   [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)の関数呼び出しには高いオーバーヘッドがあります。多数のトランザクションの履歴SQLステートメントを照会するために関数が呼び出されると、照会に長い時間がかかる場合があります。クラスタが大きく、同時トランザクションが多い場合は、 `TIDB_TRX`のテーブル全体を照会するときに、 `ALL_SQL_DIGEST`列でこの関数を直接使用しないでください。これは、 `select *, tidb_decode_sql_digests(all_sql_digests) from tidb_trx`のようなSQLステートメントを回避することを意味します。
> -   現在、 `TIDB_TRX`テーブルはTiDB内部トランザクションの情報の表示をサポートしていません。

## 例 {#example}

{{< copyable "" >}}

```sql
select * from information_schema.tidb_trx\G
```

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

この例のクエリ結果から、次のことがわかります。現在のノードには2つの進行中のトランザクションがあります。 1つのトランザクションはアイドル状態（ `STATE`は`Idle`は`NULL` ）であり、このトランザクションは3 `CURRENT_SQL_DIGEST`のステートメントを実行しました（ `ALL_SQL_DIGESTS`つのリストには実行された3つのSQLステートメントのダイジェストである3つのレコードがあります）。別のトランザクションは、ステートメントを実行してロックを待機しています（ `STATE`は`LockWaiting`で、 `WAITING_START_TIME`は待機中のロックの開始時刻を示します）。トランザクションは2つのステートメントを実行し、現在実行されているステートメントは``"update `t` set `v` = `v` + ? where `id` = ?"``の形式です。

{{< copyable "" >}}

```sql
select id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) as all_sqls from information_schema.tidb_trx\G
```

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

このクエリは、 `TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列で[`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数を呼び出し、システム内部クエリを介してSQLダイジェスト配列を正規化されたSQLステートメントの配列に変換します。これは、トランザクションによって過去に実行されたステートメントの情報を視覚的に取得するのに役立ちます。ただし、上記のクエリは`TIDB_TRX`のテーブル全体をスキャンし、各行に対して`TIDB_DECODE_SQL_DIGESTS`関数を呼び出すことに注意してください。 `TIDB_DECODE_SQL_DIGESTS`関数を呼び出すと、オーバーヘッドが高くなります。したがって、クラスタに多数の同時トランザクションが存在する場合は、このタイプのクエリを回避するようにしてください。

## CLUSTER_TIDB_TRX {#cluster-tidb-trx}

`TIDB_TRX`の表は、単一のTiDBノードで実行されているトランザクションに関する情報のみを提供します。クラスタ全体のすべてのTiDBノードで実行されているトランザクションの情報を表示する場合は、 `CLUSTER_TIDB_TRX`のテーブルをクエリする必要があります。 `TIDB_TRX`テーブルのクエリ結果と比較すると、 `CLUSTER_TIDB_TRX`テーブルのクエリ結果には追加の`INSTANCE`フィールドが含まれています。 `INSTANCE`フィールドには、クラスタの各ノードのIPアドレスとポートが表示されます。これは、トランザクションが配置されているTiDBノードを区別するために使用されます。

{{< copyable "" >}}

```sql
USE information_schema;
DESC cluster_tidb_trx;
```

```sql
mysql> desc cluster_tidb_trx;
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
+-------------------------+-----------------------------------------------------------------+------+------+---------+-------+
```

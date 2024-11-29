---
title: TIDB_TRX
summary: TIDB_TRX` INFORMATION_SCHEMA テーブルについて学習します。
---

# 翻訳元 {#tidb-trx}

`TIDB_TRX`テーブルには、TiDB ノードで現在実行されているトランザクションに関する情報が提供されます。

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_TRX;
```

出力は次のようになります。

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

`TIDB_TRX`表の各列フィールドの意味は次のとおりです。

-   `ID` : トランザクション ID。トランザクションの`start_ts` (開始タイムスタンプ) です。
-   `START_TIME` : トランザクションの開始時刻。これは、トランザクションの`start_ts`に対応する物理的な時間です。
-   `CURRENT_SQL_DIGEST` : トランザクションで現在実行されている SQL ステートメントのダイジェスト。
-   `CURRENT_SQL_DIGEST_TEXT` : トランザクションによって現在実行されている SQL 文の正規化された形式、つまり引数と形式のない SQL 文。 `CURRENT_SQL_DIGEST`に相当します。
-   `STATE` : トランザクションの現在の状態。可能な値は次のとおりです:
    -   `Idle` : トランザクションはアイドル状態です。つまり、ユーザーがクエリを入力するのを待機しています。
    -   `Running` : トランザクションはクエリを実行しています。
    -   `LockWaiting` : トランザクションは悲観的ロックの取得を待機しています。トランザクションは、他のトランザクションによってブロックされているかどうかに関係なく、悲観的ロック操作の開始時にこの状態になることに注意してください。
    -   `Committing` : トランザクションはコミット処理中です。
    -   `RollingBack` : トランザクションはロールバック中です。
-   `WAITING_START_TIME` : `STATE`の値が`LockWaiting`場合、この列には待機の開始時刻が表示されます。
-   `MEM_BUFFER_KEYS` : 現在のトランザクションによってメモリバッファーに書き込まれたキーの数。
-   `MEM_BUFFER_BYTES` : 現在のトランザクションによってメモリバッファーに書き込まれたキー値バイトの合計数。
-   `SESSION_ID` : このトランザクションが属するセッションの ID。
-   `USER` : トランザクションを実行するユーザーの名前。
-   `DB` : トランザクションが実行されるセッションの現在のデフォルトのデータベース名。
-   `ALL_SQL_DIGESTS` : トランザクションによって実行されたステートメントのダイジェスト リスト。リストは JSON 形式の文字列配列として表示されます。各トランザクションは最大で最初の 50 個のステートメントを記録します。2 [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)を使用すると、この列の情報を対応する正規化された SQL ステートメントのリストに変換できます。
-   `RELATED_TABLE_IDS` : トランザクションがアクセスするテーブル、ビュー、およびその他のオブジェクトの ID。

> **注記：**
>
> -   [プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみがこのテーブルの完全な情報を取得できます。PROCESS 権限を持たないユーザーは、現在のユーザーが実行したトランザクションの情報のみを照会できます。
> -   `CURRENT_SQL_DIGEST`列目と`ALL_SQL_DIGESTS`列目の情報 (SQL ダイジェスト) は、正規化された SQL 文から計算されたハッシュ値です。5 `CURRENT_SQL_DIGEST_TEXT`目の情報と`TIDB_DECODE_SQL_DIGESTS`関数から返される結果は、文の要約テーブルから内部的に照会されるため、対応する文が内部的に見つからない可能性があります。SQL ダイジェストと文の要約テーブルの詳細については、 [ステートメント要約表](/statement-summary-tables.md)参照してください。
> -   [`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数呼び出しには大きなオーバーヘッドがあります。この関数を呼び出して多数のトランザクションの履歴 SQL ステートメントを照会すると、照会に長い時間がかかる可能性があります。クラスターが大きく、同時トランザクションが多い場合は、 `TIDB_TRX`のテーブル全体を照会するときに、 `ALL_SQL_DIGEST`列でこの関数を直接使用しないでください。つまり、 `SELECT *, tidb_decode_sql_digests(all_sql_digests) FROM TIDB_TRX`のような SQL ステートメントを回避する必要があります。
> -   現在、 `TIDB_TRX`テーブルは TiDB 内部トランザクションの情報の表示をサポートしていません。

## 例 {#example}

`TIDB_TRX`テーブルをビュー。

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

出力は次のようになります。

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

この例のクエリ結果から、現在のノードには 2 つのトランザクションが進行中であることがわかります。 1 つのトランザクションはアイドル状態 ( `STATE`は`Idle` 、 `CURRENT_SQL_DIGEST`は`NULL` ) で、このトランザクションは 3 つのステートメントを実行しました ( `ALL_SQL_DIGESTS`リストには 3 つのレコードがあり、これは実行された 3 つの SQL ステートメントのダイジェストです)。 別のトランザクションはステートメントを実行してロックを待機しています ( `STATE`は`LockWaiting`で、 `WAITING_START_TIME`待機中のロックの開始時間を示しています)。 トランザクションは 2 つのステートメントを実行し、現在実行中のステートメントは``"update `t` set `v` = `v` + ? where `id` = ?"``の形式になっています。

```sql
SELECT id, all_sql_digests, tidb_decode_sql_digests(all_sql_digests) AS all_sqls FROM INFORMATION_SCHEMA.TIDB_TRX\G
```

出力は次のようになります。

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

このクエリは、 `TIDB_TRX`テーブルの`ALL_SQL_DIGESTS`列で[`TIDB_DECODE_SQL_DIGESTS`](/functions-and-operators/tidb-functions.md#tidb_decode_sql_digests)関数を呼び出し、システム内部クエリを通じて SQL ダイジェスト配列を正規化された SQL ステートメントの配列に変換します。これにより、トランザクションによって過去に実行されたステートメントの情報を視覚的に取得できます。ただし、前のクエリは`TIDB_TRX`のテーブル全体をスキャンし、各行に対して`TIDB_DECODE_SQL_DIGESTS`関数を呼び出すことに注意してください。11 関数`TIDB_DECODE_SQL_DIGESTS`呼び出しには大きなオーバーヘッドがあります。したがって、クラスター内に多数の同時トランザクションが存在する場合は、このタイプのクエリを避けるようにしてください。

## クラスター_TIDB_TRX {#cluster-tidb-trx}

`TIDB_TRX`テーブルは、単一の TiDB ノードで実行されているトランザクションに関する情報のみを提供します。クラスター全体のすべての`TIDB_TRX`ノードで実行されているトランザクションの情報を表示するには、 `CLUSTER_TIDB_TRX`テーブルをクエリする必要があります。5 テーブルのクエリ結果と比較すると、 `CLUSTER_TIDB_TRX`テーブルのクエリ結果には追加の`INSTANCE`フィールドが含まれます`INSTANCE`フィールドには、クラスター内の各ノードの IP アドレスとポートが表示され、トランザクションが配置されている TiDB ノードを区別するために使用されます。

```sql
USE INFORMATION_SCHEMA;
DESC CLUSTER_TIDB_TRX;
```

出力は次のようになります。

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

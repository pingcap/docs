---
title: TiDB Specific Functions
summary: TiDB 固有の関数の使用法について学習します。
---

# TiDB固有の機能 {#tidb-specific-functions}

次の関数はTiDB 拡張機能であり、MySQL には存在しません。

<CustomContent platform="tidb">

| 関数名                                                     | 機能説明                                                                                                                                                                                                                                                                |
| :------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)   | 現在のセッションがバインドされているリソース グループの名前を返します。 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)を参照してください。                                                                                                                                                                 |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness)   | 指定された時間範囲内の最新のデータを読み取るように TiDB に指示します。1 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)参照してください。                                                                                                                                                           |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso)               | 現在の[TiDB のタイムスタンプ Oracle (TSO)](/tso.md)返します。                                                                                                                                                                                                                       |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | バイナリプランをデコードします。                                                                                                                                                                                                                                                    |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key)                 | TiDB でエンコードされたキー エントリを、 `_tidb_rowid`と`table_id`含む JSON 構造にデコードします。これらのエンコードされたキーは、一部のシステム テーブルとログ出力にあります。                                                                                                                                                          |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan)               | TiDB 実行プランをデコードします。                                                                                                                                                                                                                                                 |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) を照会します。                                                                                                                                                                                                  |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest)   | クエリ文字列のダイジェストを取得します。                                                                                                                                                                                                                                                |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner)             | 接続している TiDB インスタンスが DDL 所有者であるかどうかを確認します。DDL 所有者は、クラスター内の他のすべてのノードに代わって DDL ステートメントを実行するタスクを割り当てられた TiDB インスタンスです。                                                                                                                                                  |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso)                   | TiDB TSO タイムスタンプから物理タイムスタンプを抽出します。 参照: [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 。                                                                                                                                                                  |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical)   | TiDB TSO タイムスタンプから論理タイムスタンプを抽出します。                                                                                                                                                                                                                                  |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum)             | 行のチェックサム値を照会します。この関数は、FastPlan プロセス内の`SELECT`ステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントを使用して照会できます。 [単一行データのデータ整合性検証](/ticdc/ticdc-integrity-check.md)も参照してください。 |
| [`TIDB_SHARD()`](#tidb_shard)                           | インデックス ホットスポットを分散するためにシャード インデックスを作成します。シャード インデックスは、プレフィックスとして`TIDB_SHARD`関数を持つ式インデックスです。                                                                                                                                                                          |
| [`TIDB_VERSION()`](#tidb_version)                       | 追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                                        |
| [`VITESS_HASH()`](#vitess_hash)                         | 数値のハッシュを返します。この関数は Vitess の`HASH`関数と互換性があり、Vitess からのデータ移行を支援することを目的としています。                                                                                                                                                                                         |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 関数名                                                     | 機能説明                                                                                                                                                                                                                                                                                           |
| :------------------------------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)   | 現在のセッションがバインドされているリソース グループ名を返します。 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)を参照してください。                                                                                                                                                                                              |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness)   | 指定された時間範囲内の最新のデータを読み取るように TiDB に指示します。1 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)参照してください。                                                                                                                                                                                      |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso)               | 現在の[TiDB のタイムスタンプ Oracle (TSO)](/tso.md)返します。                                                                                                                                                                                                                                                  |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | バイナリプランをデコードします。                                                                                                                                                                                                                                                                               |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key)                 | TiDB でエンコードされたキー エントリを、 `_tidb_rowid`と`table_id`含む JSON 構造にデコードします。これらのエンコードされたキーは、一部のシステム テーブルとログ出力にあります。                                                                                                                                                                                     |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan)               | TiDB 実行プランをデコードします。                                                                                                                                                                                                                                                                            |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) を照会します。                                                                                                                                                                                                                             |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest)   | クエリ文字列のダイジェストを取得します。                                                                                                                                                                                                                                                                           |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner)             | 接続している TiDB インスタンスが DDL 所有者であるかどうかを確認します。DDL 所有者は、クラスター内の他のすべてのノードに代わって DDL ステートメントを実行するタスクを割り当てられた TiDB インスタンスです。                                                                                                                                                                             |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso)                   | TiDB TSO タイムスタンプから物理タイムスタンプを抽出します。 参照: [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 。                                                                                                                                                                                             |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical)   | TiDB TSO タイムスタンプから論理タイムスタンプを抽出します。                                                                                                                                                                                                                                                             |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum)             | 行のチェックサム値を照会します。この関数は、FastPlan プロセス内の`SELECT`ステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントを使用して照会できます。 [単一行データのデータ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)も参照してください。 |
| [`TIDB_SHARD()`](#tidb_shard)                           | インデックス ホットスポットを分散するためにシャード インデックスを作成します。シャード インデックスは、プレフィックスとして`TIDB_SHARD`関数を持つ式インデックスです。                                                                                                                                                                                                     |
| [`TIDB_VERSION()`](#tidb_version)                       | 追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                                                                   |
| [`VITESS_HASH()`](#vitess_hash)                         | 数値のハッシュを返します。この関数は Vitess の`HASH`関数と互換性があり、Vitess からのデータ移行を支援することを目的としています。                                                                                                                                                                                                                    |

</CustomContent>

## 現在のリソースグループ {#current-resource-group}

`CURRENT_RESOURCE_GROUP()`機能は、現在[リソース管理](/tidb-resource-control.md)セッションがバインドされているリソース グループ名を表示するために使用されます。3 機能を有効にすると、SQL ステートメントで使用できるリソースは、バインドされたリソース グループのリソース クォータによって制限されます。

セッションが確立されると、TiDB は、ログイン ユーザーがデフォルトでバインドされているリソース グループにセッションをバインドします。ユーザーがどのリソース グループにもバインドされていない場合、セッションは`default`リソース グループにバインドされます。セッションが確立されると、ユーザーのバインドされているリソース グループが[ユーザーにバインドされたリソース グループを変更する](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information)で変更されたとしても、バインドされているリソース グループはデフォルトでは変更されません。現在のセッションのバインドされているリソース グループを変更するには、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)使用できます。

例:

ユーザー`user1`作成し、 2 つのリソース グループ`rg1`と`rg2`作成し、ユーザー`user1`リソース グループ`rg1`にバインドします。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP rg1 RU_PER_SEC = 1000;
CREATE RESOURCE GROUP rg2 RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

`user1`使用してログインし、現在のユーザーにバインドされているリソース グループを表示します。

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg1                      |
    +--------------------------+
    1 row in set (0.00 sec)

`SET RESOURCE GROUP`を実行して、現在のセッションのリソース グループを`rg2`に設定し、現在のユーザーにバインドされているリソース グループを表示します。

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg2                      |
    +--------------------------+
    1 row in set (0.00 sec)

## TIDB_BOUNDED_STALENESS {#tidb-bounded-staleness}

`TIDB_BOUNDED_STALENESS()`関数は[`AS OF TIMESTAMP`](/as-of-timestamp.md)構文の一部として使用されます。

## TIDB_CURRENT_TSO {#tidb-current-tso}

`TIDB_CURRENT_TSO()`関数は、現在のトランザクションの[TSO](/tso.md)返します。これは、 [`tidb_current_ts`](/system-variables.md#tidb_current_ts)システム変数に似ています。

```sql
BEGIN;
```

    Query OK, 0 rows affected (0.00 sec)

```sql
SELECT TIDB_CURRENT_TSO();
```

    +--------------------+
    | TIDB_CURRENT_TSO() |
    +--------------------+
    | 450456244814610433 |
    +--------------------+
    1 row in set (0.00 sec)

```sql
SELECT @@tidb_current_ts;
```

    +--------------------+
    | @@tidb_current_ts  |
    +--------------------+
    | 450456244814610433 |
    +--------------------+
    1 row in set (0.00 sec)

## TIDB_DECODE_BINARY_PLAN {#tidb-decode-binary-plan}

`TIDB_DECODE_BINARY_PLAN(binary_plan)`関数は、 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)の表の`BINARY_PLAN`列にあるようなバイナリ プランをデコードします。

バイナリ プランを使用できるようにするには、 [`tidb_generate_binary_plan`](/system-variables.md#tidb_generate_binary_plan-new-in-v620)変数を`ON`に設定する必要があります。

例：

```sql
SELECT BINARY_PLAN,TIDB_DECODE_BINARY_PLAN(BINARY_PLAN) FROM information_schema.STATEMENTS_SUMMARY LIMIT 1\G
```

    *************************** 1. row ***************************
                             BINARY_PLAN: lQLwPgqQAgoMUHJvamVjdGlvbl8zEngKDk1lbVRhYmxlU2Nhbl80KQAAAAAAiMNAMAM4AUABSioKKAoSaW5mb3JtYQU00HNjaGVtYRISU1RBVEVNRU5UU19TVU1NQVJZWhV0aW1lOjI5LjPCtXMsIGxvb3BzOjJw////CQIEAXgJCBD///8BIQFnDOCb+EA6cQCQUjlDb2x1bW4jOTIsIHRpZGJfZGVjb2RlX2JpbmFyeV9wbGFuKBUjCCktPg0MEDEwM1oWBYAIMTA4NoEAeGINQ29uY3VycmVuY3k6NXDIZXj///////////8BGAE=
    TIDB_DECODE_BINARY_PLAN(BINARY_PLAN):
    | id               | estRows  | estCost   | actRows | task | access object            | execution info                       | operator info                                             | memory  | disk  |
    | Projection_3     | 10000.00 | 100798.00 | 3       | root |                          | time:108.3µs, loops:2, Concurrency:5 | Column#92, tidb_decode_binary_plan(Column#92)->Column#103 | 12.7 KB | N/A   |
    | └─MemTableScan_4 | 10000.00 | 0.00      | 3       | root | table:STATEMENTS_SUMMARY | time:29.3µs, loops:2                 |                                                           | N/A     | N/A   |

    1 row in set (0.00 sec)

## TIDB_デコードキー {#tidb-decode-key}

`TIDB_DECODE_KEY()`関数は、TiDB でエンコードされたキー エントリを`_tidb_rowid`と`table_id`含む JSON 構造にデコードします。これらのエンコードされたキーは、一部のシステム テーブルとログ出力に存在します。

次の例では、テーブル`t1`に TiDB によって生成された非表示の`rowid`あります。ステートメントでは`TIDB_DECODE_KEY()`関数が使用されています。結果から、非表示の`rowid`がデコードされて出力されていることがわかります。これは、クラスター化されていない主キーの一般的な結果です。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

次の例では、テーブル`t2`に複合クラスター化主キーがあります。JSON 出力から、主キーの一部である両方の列の名前と値を含む`handle`確認できます。

```sql
SHOW CREATE TABLE t2\G
```

```sql
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` binary(36) NOT NULL,
  `a` tinyint unsigned NOT NULL,
  `v` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`a`,`id`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin
1 row in set (0.001 sec)
```

```sql
SELECT * FROM information_schema.tikv_region_status WHERE table_name='t2' LIMIT 1\G
```

```sql
*************************** 1. row ***************************
                REGION_ID: 48
                START_KEY: 7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9
                  END_KEY:
                 TABLE_ID: 62
                  DB_NAME: test
               TABLE_NAME: t2
                 IS_INDEX: 0
                 INDEX_ID: NULL
               INDEX_NAME: NULL
           EPOCH_CONF_VER: 1
            EPOCH_VERSION: 38
            WRITTEN_BYTES: 0
               READ_BYTES: 0
         APPROXIMATE_SIZE: 136
         APPROXIMATE_KEYS: 479905
  REPLICATIONSTATUS_STATE: NULL
REPLICATIONSTATUS_STATEID: NULL
1 row in set (0.005 sec)
```

```sql
SELECT tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9');
```

```sql
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

次の例では、テーブルの最初のリージョンは、テーブルの`table_id`のみを含むキーで始まります。テーブルの最後のリージョンは`table_id + 1`で終わります。その間にあるリージョンには、 `_tidb_rowid`または`handle`含む長いキーがあります。

```sql
SELECT
  TABLE_NAME,
  TIDB_DECODE_KEY(START_KEY),
  TIDB_DECODE_KEY(END_KEY)
FROM
  information_schema.TIKV_REGION_STATUS
WHERE
  TABLE_NAME='stock'
  AND IS_INDEX=0
ORDER BY
  START_KEY;
```

```sql
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| TABLE_NAME | TIDB_DECODE_KEY(START_KEY)                                | TIDB_DECODE_KEY(END_KEY)                                  |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
| stock      | {"table_id":143}                                          | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"32485","s_w_id":"3"},"table_id":143} | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"64964","s_w_id":"5"},"table_id":143} | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} |
| stock      | {"handle":{"s_i_id":"97451","s_w_id":"7"},"table_id":143} | {"table_id":145}                                          |
+------------+-----------------------------------------------------------+-----------------------------------------------------------+
4 rows in set (0.031 sec)
```

`TIDB_DECODE_KEY`成功した場合は有効な JSON を返し、デコードに失敗した場合は引数の値を返します。

## TIDB_デコードプラン {#tidb-decode-plan}

スロー クエリ ログには、エンコードされた形式の TiDB 実行プランが記録されています。1 関数`TIDB_DECODE_PLAN()` 、エンコードされたプランを人間が読める形式にデコードするために使用されます。

この関数は、ステートメントの実行時にプランがキャプチャされるため便利です。 `EXPLAIN`のステートメントを再実行すると、データの分布と統計が時間の経過とともに変化するため、異なる結果が生成される場合があります。

```sql
SELECT tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXzAJMwm2SGx0KHRlc3QudC5hLCAxMDAwMCkNuQRrdgmiAHsFbBQzMTMuOMIBmQnEDDk2MH0BUgEEGAoyCTQzXzUFVwX1oGFibGU6dCwga2VlcCBvcmRlcjpmYWxzZSwgc3RhdHM6cHNldWRvCTk2ISE2aAAIMTUzXmYA')\G
```

```sql
*************************** 1. row ***************************
  tidb_decode_plan('8QIYMAkzMV83CQEH8E85LjA0CWRhdGE6U2VsZWN0aW9uXzYJOTYwCXRpbWU6NzEzLjHCtXMsIGxvb3BzOjIsIGNvcF90YXNrOiB7bnVtOiAxLCBtYXg6IDU2OC41wgErRHByb2Nfa2V5czogMCwgcnBjXxEpAQwFWBAgNTQ5LglZyGNvcHJfY2FjaGVfaGl0X3JhdGlvOiAwLjAwfQkzLjk5IEtCCU4vQQoxCTFfNgkxXz:     id                     task         estRows    operator info                              actRows    execution info                                                                                                                         memory     disk
    TableReader_7          root         319.04     data:Selection_6                           960        time:713.1µs, loops:2, cop_task: {num: 1, max: 568.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 549.1µs, copr_cache_hit_ratio: 0.00}    3.99 KB    N/A
    └─Selection_6          cop[tikv]    319.04     lt(test.t.a, 10000)                        960        tikv_task:{time:313.8µs, loops:960}                                                                                                   N/A        N/A
      └─TableFullScan_5    cop[tikv]    960        table:t, keep order:false, stats:pseudo    960        tikv_task:{time:153µs, loops:960}                                                                                                     N/A        N/A
```

## TIDB_DECODE_SQL_DIGESTS {#tidb-decode-sql-digests}

`TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) を照会するために使用されます。この関数は、1 つまたは 2 つの引数を受け入れます。

-   `digests` : 文字列。このパラメータは JSON 文字列配列の形式であり、配列内の各文字列は SQL ダイジェストです。
-   `stmtTruncateLength` : 整数 (オプション)。返される結果内の各 SQL ステートメントの長さを制限するために使用されます。SQL ステートメントが指定された長さを超える場合、ステートメントは切り捨てられます。2 `0`長さが無制限であることを意味します。

この関数は、JSON 文字列配列の形式の文字列を返します。配列の*i*番目の項目は、 `digests`パラメータの*i*番目の要素に対応する正規化された SQL 文です。 `digests`パラメータの要素が有効な SQL ダイジェストでないか、システムが対応する SQL 文を見つけられない場合、返される結果の対応する項目は`null`です。切り捨て長が指定されている場合 ( `stmtTruncateLength > 0` )、返される結果のこの長さを超える各文について、最初の`stmtTruncateLength`文字が保持され、切り捨てを示すために末尾にサフィックス`"..."`が追加されます。 `digests`パラメータが`NULL`の場合、関数の戻り値は`NULL`です。

> **注記：**
>
> -   この機能を使用できるのは、権限[プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)を持つユーザーのみです。
> -   `TIDB_DECODE_SQL_DIGESTS`を実行すると、TiDB は各 SQL ダイジェストに対応するステートメントをステートメント サマリー テーブルから照会するため、どの SQL ダイジェストに対しても必ず対応するステートメントが見つかるという保証はありません。見つかるのはクラスター内で実行されたステートメントのみであり、これらの SQL ステートメントを照会できるかどうかは、ステートメント サマリー テーブルの関連設定にも影響されます。ステートメント サマリー テーブルの詳細な説明については、 [ステートメント要約表](/statement-summary-tables.md)参照してください。
> -   この関数には高いオーバーヘッドがあります。行数が多いクエリ (たとえば、大規模でビジーなクラスターで`information_schema.cluster_tidb_trx`のテーブル全体をクエリする) では、この関数を使用するとクエリの実行時間が長くなりすぎる可能性があります。注意して使用してください。
>     -   この関数は、呼び出されるたびに内部的に`STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、および`CLUSTER_STATEMENTS_SUMMARY_HISTORY`テーブルを照会し、その照会に`UNION`操作が含まれるため、オーバーヘッドが高くなります。この関数は現在ベクトル化をサポートしていません。つまり、複数行のデータに対してこの関数を呼び出すと、上記のクエリが各行に対して個別に実行されます。

```sql
SET @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

SELECT TIDB_DECODE_SQL_DIGESTS(@digests);
```

```sql
+------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

上記の例では、パラメータは 3 つの SQL ダイジェストを含む JSON 配列であり、対応する SQL 文はクエリ結果の 3 つの項目です。ただし、2 番目の SQL ダイジェストに対応する SQL 文はクラスターから見つからないため、結果の 2 番目の項目は`null`になります。

```sql
SELECT TIDB_DECODE_SQL_DIGESTS(@digests, 10);
```

```sql
+---------------------------------------+
| TIDB_DECODE_SQL_DIGESTS(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

上記の呼び出しでは、2 番目のパラメーター (つまり、切り捨ての長さ) が 10 に指定されていますが、クエリ結果の 3 番目のステートメントの長さは 10 を超えています。したがって、最初の 10 文字のみが保持され、最後に切り捨てを示す`"..."`追加されます。

参照:

-   [ステートメント要約表](/statement-summary-tables.md)
-   [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST {#tidb-encode-sql-digest}

`TIDB_ENCODE_SQL_DIGEST(query_str)`はクエリ文字列の SQL ダイジェストを返します。

次の例では、両方のクエリが同じクエリ ダイジェストを取得することがわかります。これは、両方のクエリのダイジェストが`select ?`になるためです。

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 1');
```

    +------------------------------------------------------------------+
    | TIDB_ENCODE_SQL_DIGEST('SELECT 1')                               |
    +------------------------------------------------------------------+
    | e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
    +------------------------------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT TIDB_ENCODE_SQL_DIGEST('SELECT 2');
```

    +------------------------------------------------------------------+
    | TIDB_ENCODE_SQL_DIGEST('SELECT 2')                               |
    +------------------------------------------------------------------+
    | e1c71d1661ae46e09b7aaec1c390957f0d6260410df4e4bc71b9c8d681021471 |
    +------------------------------------------------------------------+
    1 row in set (0.00 sec)

## TIDB_IS_DDL_OWNER {#tidb-is-ddl-owner}

接続しているインスタンスが DDL 所有者である場合、 `TIDB_IS_DDL_OWNER()`関数は`1`返します。

```sql
SELECT TIDB_IS_DDL_OWNER();
```

    +---------------------+
    | TIDB_IS_DDL_OWNER() |
    +---------------------+
    |                   1 |
    +---------------------+
    1 row in set (0.00 sec)

## TIDB_PARSE_TSO {#tidb-parse-tso}

`TIDB_PARSE_TSO()`関数は、TiDB TSO タイムスタンプから物理タイムスタンプを抽出します。3 [TSO](/tso.md) Time Stamp Oracle を表し、PD (Placement Driver) によってトランザクションごとに発行される単調に増加するタイムスタンプです。

TSO は 2 つの部分で構成される番号です。

-   物理的なタイムスタンプ
-   論理的なカウンター

```sql
BEGIN;
SELECT TIDB_PARSE_TSO(@@tidb_current_ts);
ROLLBACK;
```

```sql
+-----------------------------------+
| TIDB_PARSE_TSO(@@tidb_current_ts) |
+-----------------------------------+
| 2021-05-26 11:33:37.776000        |
+-----------------------------------+
1 row in set (0.0012 sec)
```

ここで`TIDB_PARSE_TSO` 、セッション変数`tidb_current_ts`で使用可能なタイムスタンプ番号から物理的なタイムスタンプを抽出するために使用されます。タイムスタンプはトランザクションごとに発行されるため、この関数はトランザクション内で実行されます。

## TIDB_PARSE_TSO_LOGICAL {#tidb-parse-tso-logical}

`TIDB_PARSE_TSO_LOGICAL(tso)`関数は、 [TSO](/tso.md)タイムスタンプの論理部分を返します。

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610433);
```

    +--------------------------------------------+
    | TIDB_PARSE_TSO_LOGICAL(450456244814610433) |
    +--------------------------------------------+
    |                                          1 |
    +--------------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT TIDB_PARSE_TSO_LOGICAL(450456244814610434);
```

    +--------------------------------------------+
    | TIDB_PARSE_TSO_LOGICAL(450456244814610434) |
    +--------------------------------------------+
    |                                          2 |
    +--------------------------------------------+
    1 row in set (0.00 sec)

## TIDB_ROW_CHECKSUM {#tidb-row-checksum}

`TIDB_ROW_CHECKSUM()`関数は、行のチェックサム値を照会するために使用されます。この関数は、FastPlan プロセス内の`SELECT`ステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`などのステートメントを通じて照会できます。

TiDB 内の単一行データのチェックサム機能を有効にするには (システム変数[`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)によって制御されます)、次のステートメントを実行します。

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

この構成は新しく作成されたセッションに対してのみ有効になるため、TiDB に再接続する必要があります。

テーブル`t`を作成し、データを挿入します。

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c CHAR(1));
INSERT INTO t VALUES (1, 10, 'a');
```

次のステートメントは、表`t`の行`id = 1`のチェックサム値を照会する方法を示しています。

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

出力は次のようになります。

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

## TIDB_シャード {#tidb-shard}

`TIDB_SHARD()`関数は、インデックス ホットスポットを分散するためのシャード インデックスを作成します。シャード インデックスは、 `TIDB_SHARD()`関数がプレフィックスとして付いた式インデックスです。

-   作成:

    インデックスフィールド`a`のシャードインデックスを作成するには、 `uk((tidb_shard(a)), a))`使用できます。一意のセカンダリインデックス`uk((tidb_shard(a)), a))`のインデックスフィールド`a`のデータが単調に増加または減少することによってホットスポットが発生した場合、インデックスのプレフィックス`tidb_shard(a)`によってホットスポットを分散させ、クラスターのスケーラビリティを向上させることができます。

-   シナリオ:

    -   一意のセカンダリ インデックス上のキーが単調に増加または減少することによって書き込みホットスポットが発生し、インデックスに整数型のフィールドが含まれています。
    -   SQL ステートメントは、セカンダリ インデックスのすべてのフィールドに基づいて、個別の`SELECT`として、または`UPDATE` 、 `DELETE`などで生成された内部クエリとして、等価クエリを実行します。等価クエリには、 `a = 1`または`a IN (1, 2, ......)` 2 つの方法があります。

-   制限事項:

    -   不等式クエリでは使用できません。
    -   `OR`最外部の`AND`演算子が混在するクエリでは使用できません。
    -   `GROUP BY`節では使用できません。
    -   `ORDER BY`節では使用できません。
    -   `ON`節では使用できません。
    -   `WHERE`サブクエリでは使用できません。
    -   整数フィールドのみの一意のインデックスを分散するために使用できます。
    -   複合インデックスでは効果がない可能性があります。
    -   FastPlan プロセスを実行できないため、オプティマイザーのパフォーマンスに影響します。
    -   実行プラン キャッシュの準備には使用できません。

次の例は、 `TIDB_SHARD()`関数の使用方法を示しています。

-   `TIDB_SHARD()`関数を使用して SHARD 値を計算します。

    次のステートメントは、 `TIDB_SHARD()`関数を使用して`12373743746`の SHARD 値を計算する方法を示しています。

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

-   SHARD 値は次のとおりです。

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

-   `TIDB_SHARD()`関数を使用してシャード インデックスを作成します。

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

## TIDB_バージョン {#tidb-version}

`TIDB_VERSION()`関数は、接続している TiDBサーバーのバージョンとビルドの詳細を取得するために使用されます。この関数は、GitHub で問題を報告するときに使用できます。

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v8.5.0
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2024-12-05 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## ハッシュ {#vitess-hash}

`VITESS_HASH(num)`関数は、Vitess と同じ方法で数値をハッシュするために使用されます。これは、Vitess から TiDB への移行を支援するためです。

例：

```sql
SELECT VITESS_HASH(123);
```

    +---------------------+
    | VITESS_HASH(123)    |
    +---------------------+
    | 1155070131015363447 |
    +---------------------+
    1 row in set (0.00 sec)

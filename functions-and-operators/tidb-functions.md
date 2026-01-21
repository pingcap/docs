---
title: TiDB Specific Functions
summary: TiDB 固有の関数の使用法について学習します。
---

# TiDB固有の機能 {#tidb-specific-functions}

次の関数は TiDB 拡張機能であり、MySQL には存在しません。

<CustomContent platform="tidb">

| 関数名                                                     | 機能の説明                                                                                                                                                                                                                                            |
| :------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)   | 現在のセッションがバインドされているリソースグループの名前を返します。1 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)参照してください。                                                                                                                           |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness)   | 指定された時間範囲内の最新のデータを読み取るようTiDBに指示します。1 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)参照してください。                                                                                                                                           |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso)               | 現在の[TiDB のタイムスタンプ Oracle (TSO)](/tso.md)を返します。                                                                                                                                                                                                   |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | バイナリ プランをデコードします。                                                                                                                                                                                                                                |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key)                 | TiDBエンコードされたキーエントリを、 `_tidb_rowid`と`table_id`含むJSON構造にデコードします。これらのエンコードされたキーは、一部のシステムテーブルやログ出力で確認できます。                                                                                                                                           |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan)               | TiDB 実行プランをデコードします。                                                                                                                                                                                                                              |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | クラスター内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (形式と引数のない形式) を照会します。                                                                                                                                                                                |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key)     | インデックス キーをエンコードします。                                                                                                                                                                                                                              |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key)   | レコード キーをエンコードします。                                                                                                                                                                                                                                |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest)   | クエリ文字列のダイジェストを取得します。                                                                                                                                                                                                                             |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner)             | 接続しているTiDBインスタンスがDDLオーナーであるかどうかを確認します。DDLオーナーとは、クラスター内の他のすべてのノードに代わってDDLステートメントを実行する役割を担うTiDBインスタンスです。                                                                                                                                           |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info)                   | キーに関する[MVCC (マルチバージョン同時実行制御)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc)情報を返します。                                                                                                                      |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso)                   | TiDB TSOタイムスタンプから物理タイムスタンプを抽出します。参照: [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 。                                                                                                                                                 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical)   | TiDB TSO タイムスタンプから論理タイムスタンプを抽出します。                                                                                                                                                                                                               |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum)             | 行のチェックサム値を照会します。この関数は、FastPlanプロセス内の`SELECT`文でのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のような文で照会できます[単一行データのデータ整合性検証](/ticdc/ticdc-integrity-check.md)も参照してください。 |
| [`TIDB_SHARD()`](#tidb_shard)                           | インデックスホットスポットを分散させるためにシャードインデックスを作成します。シャードインデックスは、プレフィックスに`TIDB_SHARD`関数が付いた式インデックスです。                                                                                                                                                          |
| [`TIDB_VERSION()`](#tidb_version)                       | 追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                     |
| [`VITESS_HASH()`](#vitess_hash)                         | 数値のハッシュを返します。この関数はVitessの`HASH`関数と互換性があり、Vitessからのデータ移行を支援することを目的としています。                                                                                                                                                                         |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 関数名                                                     | 機能の説明                                                                                                                                                                                                                                                                       |
| :------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`CURRENT_RESOURCE_GROUP()`](#current_resource_group)   | 現在のセッションがバインドされているリソースグループ名を返します。1 [リソース制御を使用してリソースグループの制限とフロー制御を実現する](/tidb-resource-control-ru-groups.md)参照してください。                                                                                                                                                        |
| [`TIDB_BOUNDED_STALENESS()`](#tidb_bounded_staleness)   | 指定された時間範囲内の最新のデータを読み取るようTiDBに指示します。1 [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)参照してください。                                                                                                                                                                      |
| [`TIDB_CURRENT_TSO()`](#tidb_current_tso)               | 現在の[TiDB のタイムスタンプ Oracle (TSO)](/tso.md)を返します。                                                                                                                                                                                                                              |
| [`TIDB_DECODE_BINARY_PLAN()`](#tidb_decode_binary_plan) | バイナリ プランをデコードします。                                                                                                                                                                                                                                                           |
| [`TIDB_DECODE_KEY()`](#tidb_decode_key)                 | TiDBエンコードされたキーエントリを、 `_tidb_rowid`と`table_id`含むJSON構造にデコードします。これらのエンコードされたキーは、一部のシステムテーブルやログ出力で確認できます。                                                                                                                                                                      |
| [`TIDB_DECODE_PLAN()`](#tidb_decode_plan)               | TiDB 実行プランをデコードします。                                                                                                                                                                                                                                                         |
| [`TIDB_DECODE_SQL_DIGESTS()`](#tidb_decode_sql_digests) | クラスター内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (形式と引数のない形式) を照会します。                                                                                                                                                                                                           |
| [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key)     | インデックス キーをエンコードします。                                                                                                                                                                                                                                                         |
| [`TIDB_ENCODE_RECORD_KEY()`](#tidb_encode_record_key)   | レコード キーをエンコードします。                                                                                                                                                                                                                                                           |
| [`TIDB_ENCODE_SQL_DIGEST()`](#tidb_encode_sql_digest)   | クエリ文字列のダイジェストを取得します。                                                                                                                                                                                                                                                        |
| [`TIDB_IS_DDL_OWNER()`](#tidb_is_ddl_owner)             | 接続しているTiDBインスタンスがDDLオーナーであるかどうかを確認します。DDLオーナーとは、クラスター内の他のすべてのノードに代わってDDLステートメントを実行する役割を担うTiDBインスタンスです。                                                                                                                                                                      |
| [`TIDB_PARSE_TSO()`](#tidb_parse_tso)                   | TiDB TSOタイムスタンプから物理タイムスタンプを抽出します。参照: [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 。                                                                                                                                                                            |
| [`TIDB_MVCC_INFO()`](#tidb_mvcc_info)                   | キーに関する[MVCC (マルチバージョン同時実行制御)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc)情報を返します。                                                                                                                                                 |
| [`TIDB_PARSE_TSO_LOGICAL()`](#tidb_parse_tso_logical)   | TiDB TSO タイムスタンプから論理タイムスタンプを抽出します。                                                                                                                                                                                                                                          |
| [`TIDB_ROW_CHECKSUM()`](#tidb_row_checksum)             | 行のチェックサム値を照会します。この関数は、FastPlanプロセス内の`SELECT`文でのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のような文で照会できます[単一行データのデータ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)も参照してください。 |
| [`TIDB_SHARD()`](#tidb_shard)                           | インデックスホットスポットを分散させるためにシャードインデックスを作成します。シャードインデックスは、プレフィックスに`TIDB_SHARD`関数が付いた式インデックスです。                                                                                                                                                                                     |
| [`TIDB_VERSION()`](#tidb_version)                       | 追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                                                |
| [`VITESS_HASH()`](#vitess_hash)                         | 数値のハッシュを返します。この関数はVitessの`HASH`関数と互換性があり、Vitessからのデータ移行を支援することを目的としています。                                                                                                                                                                                                    |

</CustomContent>

## 現在のリソースグループ {#current-resource-group}

`CURRENT_RESOURCE_GROUP()`機能は、現在のセッションがバインドされているリソースグループ名を表示するために使用されます。3 [リソース管理](/tidb-resource-control-ru-groups.md)機能を有効にすると、SQL ステートメントで使用できるリソースは、バインドされているリソースグループのリソースクォータによって制限されます。

セッションが確立されると、TiDB はログインユーザーがデフォルトでバインドされているリソースグループにセッションをバインドします。ユーザーがどのリソースグループにもバインドされていない場合、セッションは`default`リソースグループにバインドされます。セッションが確立されると、ユーザーのバインドされているリソースグループが[ユーザーにバインドされたリソースグループを変更する](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information)で変更されても、バインドされているリソースグループはデフォルトで変更されません。現在のセッションのバインドされているリソースグループを変更するには、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)使用します。

例:

ユーザー`user1`を作成し、リソース グループ`rg1`と`rg2` 2 つのリソース グループを作成し、ユーザー`user1`リソース グループ`rg1`にバインドします。

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

`SET RESOURCE GROUP`実行して、現在のセッションのリソース グループを`rg2`に設定し、現在のユーザーにバインドされているリソース グループを表示します。

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

`TIDB_CURRENT_TSO()`関数は、現在のトランザクションの[TSO](/tso.md)を返します。これはシステム変数[`tidb_current_ts`](/system-variables.md#tidb_current_ts)に似ています。

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

`TIDB_DECODE_BINARY_PLAN(binary_plan)`関数は、 [`STATEMENTS_SUMMARY`](/statement-summary-tables.md)表の`BINARY_PLAN`列目にあるようなバイナリ プランをデコードします。

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

## TIDB_デコード_キー {#tidb-decode-key}

`TIDB_DECODE_KEY()`関数は、TiDBでエンコードされたキーエントリを、 `_tidb_rowid`と`table_id`含むJSON構造にデコードします。これらのエンコードされたキーは、一部のシステムテーブルとログ出力に存在します。

次の例では、テーブル`t1`にTiDBによって生成された隠し`rowid`があります。ステートメントでは関数`TIDB_DECODE_KEY()`が使用されています。結果から、隠し`rowid`がデコードされて出力されていることがわかります。これは、非クラスター化主キーの典型的な結果です。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

次の例では、テーブル`t2`に複合クラスター化主キーがあります。JSON 出力を見ると、主キーを構成する両方の列の名前と値を含む`handle`が確認できます。

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

次の例では、テーブルの最初のリージョンは、テーブルの`table_id`を含むキーで始まります。テーブルの最後のリージョンは`table_id + 1`で終わります。その間にあるリージョンは、 `_tidb_rowid`または`handle`を含むより長いキーを持ちます。

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

## TIDB_デコード_プラン {#tidb-decode-plan}

TiDB実行プランは、スロークエリログにエンコードされた形式で保存されています。1関数`TIDB_DECODE_PLAN()` 、エンコードされたプランを人間が読める形式にデコードするために使用されます。

この関数は、ステートメント実行時にプランが取得されるため便利です。1 `EXPLAIN`ステートメントを再実行すると、データの分布と統計が時間の経過とともに変化するため、異なる結果が生成される可能性があります。

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

`TIDB_DECODE_SQL_DIGESTS()`関数は、クラスタ内のSQLダイジェストセットに対応する正規化されたSQL文（フォーマットと引数のない形式）を照会するために使用されます。この関数は1つまたは2つの引数を取ります。

-   `digests` : 文字列。このパラメータはJSON文字列配列の形式であり、配列内の各文字列はSQLダイジェストです。
-   `stmtTruncateLength` : 整数（オプション）。返される結果内の各SQL文の長さを制限するために使用されます。SQL文が指定された長さを超えた場合、文は切り捨てられます。2 `0`長さが無制限であることを意味します。

この関数は、JSON文字列配列形式の文字列を返します。配列の*i*番目の項目は、 `digests`パラメータの*i*番目の要素に対応する正規化されたSQL文です。 `digests`パラメータの要素が有効なSQLダイジェストでないか、システムが対応するSQL文を見つけられない場合、返される結果の対応する項目は`null`なります。切り捨て長が指定されている場合（ `stmtTruncateLength > 0` ）、返される結果のこの長さを超える各文については、最初の`stmtTruncateLength`文字が保持され、切り捨てを示すために末尾にサフィックス`"..."`が追加されます。 `digests`パラメータが`NULL`の場合、関数の戻り値は`NULL`なります。

> **注記：**
>
> -   この機能を使用できるのは、 [プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみです。
> -   `TIDB_DECODE_SQL_DIGESTS`実行すると、TiDB は各 SQL ダイジェストに対応するステートメントをステートメントサマリーテーブルから照会します。そのため、どの SQL ダイジェストに対しても、必ず対応するステートメントが見つかるとは限りません。見つかるのはクラスタ内で実行されたステートメントのみであり、これらの SQL ステートメントを照会できるかどうかは、ステートメントサマリーテーブルの関連設定にも影響されます。ステートメントサマリーテーブルの詳細については、 [明細書要約表](/statement-summary-tables.md)参照してください。
> -   この関数はオーバーヘッドが大きいため、行数の多いクエリ（例えば、大規模で高負荷なクラスターでテーブル`information_schema.cluster_tidb_trx`全体を検索するなど）では、この関数を使用するとクエリの実行時間が長くなりすぎる可能性があります。注意して使用してください。
>     -   この関数は、呼び出されるたびに内部的に`STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、 `CLUSTER_STATEMENTS_SUMMARY_HISTORY`テーブルを照会し、そのクエリに`UNION`演算が含まれるため、オーバーヘッドが大きくなります。この関数は現在ベクトル化をサポートしていません。つまり、複数行のデータに対してこの関数を呼び出す場合、上記のクエリは各行ごとに個別に実行されます。

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

上記の例では、パラメータは3つのSQLダイジェストを含むJSON配列であり、対応するSQL文はクエリ結果の3つの項目です。しかし、2番目のSQLダイジェストに対応するSQL文がクラスターから見つからないため、結果の2番目の項目は`null`なります。

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

上記の呼び出しでは、2 番目のパラメーター (つまり、切り捨ての長さ) を 10 に指定していますが、クエリ結果の 3 番目のステートメントの長さは 10 を超えています。したがって、最初の 10 文字のみが保持され、最後に切り捨てを示す`"..."`が追加されます。

参照:

-   [明細書要約表](/statement-summary-tables.md)
-   [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

## TIDB_ENCODE_SQL_DIGEST {#tidb-encode-sql-digest}

`TIDB_ENCODE_SQL_DIGEST(query_str)`クエリ文字列の SQL ダイジェストを返します。

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

TSO は次の 2 つの部分で構成される数値です。

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

ここで`TIDB_PARSE_TSO` 、セッション変数`tidb_current_ts`で利用可能なタイムスタンプ番号から物理タイムスタンプを抽出するために使用されています。タイムスタンプはトランザクションごとに発行されるため、この関数はトランザクション内で実行されます。

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

`TIDB_ROW_CHECKSUM()`関数は、行のチェックサム値を照会するために使用されます。この関数は、FastPlanプロセス内の`SELECT`ステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントで照会できます。

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

次のステートメントは、テーブル`t`の行`id = 1`のチェックサム値を照会する方法を示しています。

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

`TIDB_SHARD()`関数は、インデックスホットスポットを分散させるためのシャードインデックスを作成します。シャードインデックスは、 `TIDB_SHARD()`関数をプレフィックスとして持つ式インデックスです。

-   作成:

    インデックスフィールド`a`にシャードインデックスを作成するには、 `uk((tidb_shard(a)), a))`使用します。一意のセカンダリインデックス`uk((tidb_shard(a)), a))`内のインデックスフィールド`a`のデータが単調に増加または減少することでホットスポットが発生した場合、インデックスのプレフィックス`tidb_shard(a)`によってホットスポットを分散させることで、クラスターのスケーラビリティを向上させることができます。

-   シナリオ:

    -   一意のセカンダリ インデックス上のキーが単調に増加または減少することによって書き込みホットスポットが発生し、インデックスに整数型のフィールドが含まれています。
    -   このSQL文は、セカンダリインデックスの全フィールドに基づいて等価性クエリを実行します。これは、 `SELECT`独立したクエリとして、または`UPDATE` 、 `DELETE`などによって生成された内部クエリとして実行されます。等価性クエリには、 `a = 1`または`a IN (1, 2, ......)` 2つの方法があります。

-   制限事項:

    -   不等式クエリでは使用できません。
    -   `OR`と最外部の`AND`演算子が混在するクエリでは使用できません。
    -   `GROUP BY`節では使用できません。
    -   `ORDER BY`節では使用できません。
    -   `ON`節では使用できません。
    -   `WHERE`サブクエリでは使用できません。
    -   整数フィールドのみの一意のインデックスを分散させるために使用できます。
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
TIDB_VERSION(): Release Version: v8.5.5
Edition: Community
Git Commit Hash: 821e491a20fbab36604b36b647b5bae26a2c1418
Git Branch: HEAD
UTC Build Time: 2026-01-15 19:16:25
GoVersion: go1.21.10
Race Enabled: false
Check Table Before Drop: false
Store: tikv
1 row in set (0.00 sec)
```

## VITESS_ハッシュ {#vitess-hash}

`VITESS_HASH(num)`関数は、Vitess と同じ方法で数値をハッシュするために使用されます。これは、Vitess から TiDB への移行を容易にするためのものです。

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

## TIDB_ENCODE_INDEX_KEY {#tidb-encode-index-key}

`TIDB_ENCODE_INDEX_KEY()`関数は、指定されたインデックスキーを16進文字列にエンコードします。構文は次のとおりです。

```sql
TIDB_ENCODE_INDEX_KEY(<db_name>, <table_name>, <index_name>, <index_columns>..., <handle_columns>...)
```

パラメータの説明:

-   `<db_name>` : ターゲット インデックスを含むデータベースの名前。
-   `<table_name>` : ターゲットインデックスを含むテーブルの名前。パーティションテーブルの場合は、パーティション名（例： `'t(p0)'` ）を指定できます。
-   `<index_name>` : ターゲットインデックスの名前。
-   `<index_columns>...` : インデックス列の値。インデックスで定義されている順序と同じ順序で値を指定する必要があります。複合インデックスの場合は、すべてのインデックス列の値を指定する必要があります。
-   `<handle_columns>...` : 行のハンドル値。必要なハンドル値は、テーブルの主キーの種類によって異なります。

    -   テーブルに主キーがない場合、または主キーが`NONCLUSTERED`場合、ハンドル値は非表示の列`_tidb_rowid`の値になります。
    -   主キーが`CLUSTERED`で、単一列の整数の場合、ハンドル値は主キー列の値になります。
    -   主キーが`CLUSTERED`で、複合主キーまたは非整数型 (共通ハンドル) の場合、ハンドル値はすべての主キー列の値を順番に含んだものになります。

次の例は、異なる主キー タイプで複合セカンダリ インデックス`idx(c1, c2)`に対してこの関数を呼び出す方法を示しています。

```sql
-- For tables without a primary key or with a NONCLUSTERED primary key, use the _tidb_rowid column.
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <_tidb_rowid>
);

-- For tables with a CLUSTERED integer primary key (the primary key column is id), use the id column.
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <id>
);

-- For tables with a CLUSTERED composite primary key (the primary key columns are p1, p2), provide the values of p1 and p2 in their defined order.
SELECT TIDB_ENCODE_INDEX_KEY(
    '<db_name>', '<table_name>', '<index_name>', 
    <c1>, <c2>, <p1>, <p2>
);
```

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO t VALUES(1,2);
```

    Query OK, 1 row affected (0.00 sec)

```sql
SELECT TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 2, 1);
```

    +----------------------------------------------------------------------------+
    | TIDB_ENCODE_INDEX_KEY('test', 't', 'idx', 2, 1)                            |
    +----------------------------------------------------------------------------+
    | 7480000000000000b45f698000000000000001038000000000000002038000000000000001 |
    +----------------------------------------------------------------------------+
    1 row in set (0.00 sec)

## TIDB_ENCODE_RECORD_KEY {#tidb-encode-record-key}

`TIDB_ENCODE_RECORD_KEY()`関数は、指定された行レコードキーを16進文字列にエンコードします。関数の構文は次のとおりです。

```sql
TIDB_ENCODE_RECORD_KEY(<db_name>, <table_name>, <handle_columns>...)
```

パラメータの説明:

-   `<db_name>` : ターゲット テーブルを含むデータベースの名前。
-   `<table_name>` : 対象テーブルの名前。パーティションテーブルの場合は、 `<table_name>`にパーティション名を指定できます（例： `'t(p0)'` ）。
-   `<handle_columns>...` : 対応する行のハンドル（行キー）値。ハンドルの正確な構成は、テーブルの主キーの種類（例えば、主キーが`CLUSTERED` （共通ハンドル）であるか、非表示列`_tidb_rowid`を使用しているかなど）によって異なります。詳細については、 [`TIDB_ENCODE_INDEX_KEY()`](#tidb_encode_index_key)の`<handle_columns>...`の説明を参照してください。

```sql
CREATE TABLE t(id int PRIMARY KEY, a int, KEY `idx` (a));
```

    Query OK, 0 rows affected (0.00 sec)

```sql
INSERT INTO t VALUES(1,2);
```

    Query OK, 1 row affected (0.00 sec)

```sql
SELECT TIDB_ENCODE_RECORD_KEY('test', 't', 1);
```

    +----------------------------------------+
    | TIDB_ENCODE_RECORD_KEY('test', 't', 1) |
    +----------------------------------------+
    | 7480000000000000845f728000000000000001 |
    +----------------------------------------+
    1 row in set (0.00 sec)

```sql
SELECT TIDB_DECODE_KEY('7480000000000000845f728000000000000001');
```

    +-----------------------------------------------------------+
    | TIDB_DECODE_KEY('7480000000000000845f728000000000000001') |
    +-----------------------------------------------------------+
    | {"id":1,"table_id":"132"}                                 |
    +-----------------------------------------------------------+
    1 row in set (0.00 sec)

## TIDB_MVCC_INFO {#tidb-mvcc-info}

キーの[MVCC (マルチバージョン同時実行制御)](https://docs.pingcap.com/tidb/stable/glossary#multi-version-concurrency-control-mvcc)の情報を返します。キーを取得するには[`TIDB_ENCODE_INDEX_KEY`](#tidb_encode_index_key)関数を使用できます。

```sql
SELECT JSON_PRETTY(TIDB_MVCC_INFO('74800000000000007f5f698000000000000001038000000000000001038000000000000001')) AS info\G
```

    *************************** 1. row ***************************
    info: [
      {
        "key": "74800000000000007f5f698000000000000001038000000000000001038000000000000001",
        "mvcc": {
          "info": {
            "values": [
              {
                "start_ts": 454654803134119936,
                "value": "MA=="
              }
            ],
            "writes": [
              {
                "commit_ts": 454654803134119937,
                "short_value": "MA==",
                "start_ts": 454654803134119936
              }
            ]
          }
        }
      }
    ]
    1 row in set (0.00 sec)

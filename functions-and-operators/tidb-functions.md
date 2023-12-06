---
title: TiDB Specific Functions
summary: Learn about the usage of TiDB specific functions.
---

# TiDB 固有の機能 {#tidb-specific-functions}

次の関数はTiDB 拡張機能であり、MySQL には存在しません。

<CustomContent platform="tidb">

| 関数名                                                                                | 機能説明                                                                                                                                                                                                                                                                                                    |
| :--------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `TIDB_BOUNDED_STALENESS()`                                                         | `TIDB_BOUNDED_STALENESS`関数は、時間範囲内でできるだけ新しいデータを読み取るように TiDB に指示します。参照: [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)                                                                                                                                                                          |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key)                                         | `TIDB_DECODE_KEY`関数を使用すると、TiDB でエンコードされたキー エントリを`_tidb_rowid`と`table_id`を含む JSON 構造にデコードできます。これらのエンコードされたキーは、一部のシステム テーブルおよびログ出力に含まれています。                                                                                                                                                               |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan)                                       | `TIDB_DECODE_PLAN`関数は、TiDB 実行プランをデコードするために使用できます。                                                                                                                                                                                                                                                       |
| `TIDB_IS_DDL_OWNER()`                                                              | `TIDB_IS_DDL_OWNER`関数を使用すると、接続している TiDB インスタンスが DDL 所有者であるかどうかを確認できます。 DDL オーナーは、クラスター内の他のすべてのノードに代わって DDL ステートメントを実行する任務を負った TiDB インスタンスです。                                                                                                                                                            |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso)                                           | `TIDB_PARSE_TSO`関数を使用すると、TiDB TSO タイムスタンプから物理タイムスタンプを抽出できます。 [`tidb_current_ts`](/system-variables.md#tidb_current_ts)も参照してください。                                                                                                                                                                        |
| [`TIDB_VERSION()`](#tidb_version)                                                  | `TIDB_VERSION`関数は、追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                                                          |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | `TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) をクエリするために使用されます。                                                                                                                                                                                              |
| `VITESS_HASH(str)`                                                                 | `VITESS_HASH`関数は、Vitess の`HASH`関数と互換性のある文字列のハッシュを返します。これは、Vitess からのデータ移行を支援することを目的としています。                                                                                                                                                                                                              |
| `TIDB_SHARD()`                                                                     | `TIDB_SHARD`関数を使用すると、インデックス ホットスポットを分散するシャード インデックスを作成できます。シャード インデックスは、接頭辞として`TIDB_SHARD`関数が付いている式インデックスです。                                                                                                                                                                                            |
| `TIDB_ROW_CHECKSUM()`                                                              | `TIDB_ROW_CHECKSUM`関数は、行のチェックサム値をクエリするために使用されます。この関数は、FastPlan プロセス内の`SELECT`のステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントを通じてクエリを実行できます。 [単一行データのデータ整合性検証](/ticdc/ticdc-integrity-check.md)も参照してください。 |
| `CURRENT_RESOURCE_GROUP()`                                                         | `CURRENT_RESOURCE_GROUP`関数は、現在のセッションがバインドされているリソース グループ名を返すために使用されます。 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)も参照してください。                                                                                                                                                                    |

</CustomContent>

<CustomContent platform="tidb-cloud">

| 関数名                                                                                | 機能説明                                                                                                                                                                                                                                                                                                                               |
| :--------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `TIDB_BOUNDED_STALENESS()`                                                         | `TIDB_BOUNDED_STALENESS`関数は、時間範囲内でできるだけ新しいデータを読み取るように TiDB に指示します。参照: [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)                                                                                                                                                                                                     |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key)                                         | `TIDB_DECODE_KEY`関数を使用すると、TiDB でエンコードされたキー エントリを`_tidb_rowid`と`table_id`を含む JSON 構造にデコードできます。これらのエンコードされたキーは、一部のシステム テーブルおよびログ出力に含まれています。                                                                                                                                                                                          |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan)                                       | `TIDB_DECODE_PLAN`関数は、TiDB 実行プランをデコードするために使用できます。                                                                                                                                                                                                                                                                                  |
| `TIDB_IS_DDL_OWNER()`                                                              | `TIDB_IS_DDL_OWNER`関数を使用すると、接続している TiDB インスタンスが DDL 所有者であるかどうかを確認できます。 DDL オーナーは、クラスター内の他のすべてのノードに代わって DDL ステートメントを実行する任務を負った TiDB インスタンスです。                                                                                                                                                                                       |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso)                                           | `TIDB_PARSE_TSO`関数を使用すると、TiDB TSO タイムスタンプから物理タイムスタンプを抽出できます。 [`tidb_current_ts`](/system-variables.md#tidb_current_ts)も参照してください。                                                                                                                                                                                                   |
| [`TIDB_VERSION()`](#tidb_version)                                                  | `TIDB_VERSION`関数は、追加のビルド情報を含む TiDB バージョンを返します。                                                                                                                                                                                                                                                                                     |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | `TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) をクエリするために使用されます。                                                                                                                                                                                                                         |
| `VITESS_HASH(str)`                                                                 | `VITESS_HASH`関数は、Vitess の`HASH`関数と互換性のある文字列のハッシュを返します。これは、Vitess からのデータ移行を支援することを目的としています。                                                                                                                                                                                                                                         |
| `TIDB_SHARD()`                                                                     | `TIDB_SHARD`関数を使用すると、インデックス ホットスポットを分散するシャード インデックスを作成できます。シャード インデックスは、接頭辞として`TIDB_SHARD`関数が付いている式インデックスです。                                                                                                                                                                                                                       |
| `TIDB_ROW_CHECKSUM()`                                                              | `TIDB_ROW_CHECKSUM`関数は、行のチェックサム値をクエリするために使用されます。この関数は、FastPlan プロセス内の`SELECT`のステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントを通じてクエリを実行できます。 [単一行データのデータ整合性検証](https://docs.pingcap.com/tidb/stable/ticdc-integrity-check)も参照してください。 |
| `CURRENT_RESOURCE_GROUP()`                                                         | `CURRENT_RESOURCE_GROUP`関数は、現在のセッションがバインドされているリソース グループ名を返すために使用されます。 [リソース制御を使用してリソースの分離を実現する](/tidb-resource-control.md)も参照してください。                                                                                                                                                                                               |

</CustomContent>

## 例 {#examples}

このセクションでは、上記の関数のいくつかの例を示します。

### TIDB_DECODE_KEY {#tidb-decode-key}

次の例では、テーブル`t1`に TiDB によって生成された非表示の`rowid`があります。ステートメントでは`TIDB_DECODE_KEY`が使用されています。結果から、隠れた`rowid`がデコードされて出力されていることがわかります。これは、非クラスター化主キーの典型的な結果です。

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

次の例では、テーブル`t2`に複合クラスター化主キーがあります。 JSON 出力から、主キーの一部である両方の列の名前と値を含む`handle`が確認できます。

```sql
SHOW CREATE TABLE t2\G
```

```sql
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` binary(36) NOT NULL,
  `a` tinyint(3) unsigned NOT NULL,
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

テーブルの最初のリージョンは、テーブルの`table_id`のみを持つキーで始まります。テーブルの最後のリージョンは`table_id + 1`で終わります。間にあるリージョンには、 `_tidb_rowid`または`handle`を含む長いキーがあります。

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

`TIDB_DECODE_KEY`は、成功すると有効な JSON を返し、デコードに失敗した場合は引数の値を返します。

### TIDB_DECODE_PLAN {#tidb-decode-plan}

TiDB 実行プランは、スロー クエリ ログでエンコードされた形式で見つけることができます。次に、 `TIDB_DECODE_PLAN()`関数を使用して、エンコードされた計画を人間が読める形式にデコードします。

この関数は、ステートメントの実行時にプランが取得されるため便利です。データの分散と統計が時間の経過とともに進化するにつれて、 `EXPLAIN`のステートメントを再実行すると、異なる結果が生じる可能性があります。

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

### TIDB_PARSE_TSO {#tidb-parse-tso}

`TIDB_PARSE_TSO`関数を使用すると、TiDB TSO タイムスタンプから物理タイムスタンプを抽出できます。 TSO は Time Stamp Oracle の略で、トランザクションごとに PD (Placement Driver) によって与えられる単調増加するタイムスタンプです。

TSO は、次の 2 つの部分で構成される数値です。

-   物理的なタイムスタンプ
-   論理カウンター

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

ここで、 `TIDB_PARSE_TSO` `tidb_current_ts`セッション変数で使用可能なタイムスタンプ番号から物理タイムスタンプを抽出するために使用されます。タイムスタンプはトランザクションごとに発行されるため、この関数はトランザクション内で実行されます。

### TIDB_VERSION {#tidb-version}

`TIDB_VERSION`関数を使用すると、接続している TiDBサーバーのバージョンとビルドの詳細を取得できます。この機能は、GitHub で問題を報告するときに使用できます。

```sql
SELECT TIDB_VERSION()\G
```

```sql
*************************** 1. row ***************************
TIDB_VERSION(): Release Version: v5.1.0-alpha-13-gd5e0ed0aa-dirty
Edition: Community
Git Commit Hash: d5e0ed0aaed72d2f2dfe24e9deec31cb6cb5fdf0
Git Branch: master
UTC Build Time: 2021-05-24 14:39:20
GoVersion: go1.13
Race Enabled: false
TiKV Min Version: v3.0.0-60965b006877ca7234adaced7890d7b029ed1306
Check Table Before Drop: false
1 row in set (0.00 sec)
```

### TIDB_DECODE_SQL_DIGESTS {#tidb-decode-sql-digests}

`TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の SQL ダイジェストのセットに対応する正規化された SQL ステートメント (形式と引数のない形式) をクエリするために使用されます。この関数は 1 つまたは 2 つの引数を受け取ります。

-   `digests` : 文字列。このパラメータは JSON 文字列配列の形式であり、配列内の各文字列は SQL ダイジェストです。
-   `stmtTruncateLength` : 整数 (オプション)。これは、返される結果内の各 SQL ステートメントの長さを制限するために使用されます。 SQL ステートメントが指定された長さを超える場合、ステートメントは切り捨てられます。 `0`長さが無制限であることを意味します。

この関数は、JSON 文字列配列形式の文字列を返します。配列内の*i*番目の項目は、 `digests`パラメータの*i*番目の要素に対応する正規化された SQL ステートメントです。 `digests`パラメータの要素が有効な SQL ダイジェストではない場合、またはシステムが対応する SQL ステートメントを見つけられない場合、返される結果の対応する項目は`null`です。切り捨ての長さが指定されている場合 ( `stmtTruncateLength > 0` )、この長さを超える返された結果の各ステートメントについて、最初の`stmtTruncateLength`文字が保持され、切り捨てを示すサフィックス`"..."`が最後に追加されます。 `digests`パラメータが`NULL`の場合、関数の戻り値は`NULL`です。

> **注記：**
>
> -   この機能は[プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみが使用できます。
> -   `TIDB_DECODE_SQL_DIGESTS`が実行されると、TiDB はステートメント概要テーブルから各 SQL ダイジェストに対応するステートメントをクエリするため、対応するステートメントが SQL ダイジェストに対して常に見つかるという保証はありません。クラスター内で実行されたステートメントのみが検索され、これらの SQL ステートメントをクエリできるかどうかは、ステートメント サマリー テーブルの関連構成にも影響されます。ステートメント集計テーブルの詳細な説明については、 [ステートメント概要テーブル](/statement-summary-tables.md)を参照してください。
> -   この関数にはオーバーヘッドが高くなります。多数の行を含むクエリ (たとえば、大規模でビジーなクラスター上の`information_schema.cluster_tidb_trx`の完全なテーブルをクエリする場合) では、この関数を使用するとクエリの実行時間が長すぎる可能性があります。慎重に使用してください。
>     -   この関数は呼び出されるたびに`STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、および`CLUSTER_STATEMENTS_SUMMARY_HISTORY`テーブルを内部的にクエリし、クエリには`UNION`操作が含まれるため、オーバーヘッドが高くなります。この関数は現在、ベクトル化をサポートしていません。つまり、複数行のデータに対してこの関数を呼び出す場合、上記のクエリは行ごとに個別に実行されます。

```sql
set @digests = '["e6f07d43b5c21db0fbb9a31feac2dc599787763393dd5acbfad80e247eb02ad5","38b03afa5debbdf0326a014dbe5012a62c51957f1982b3093e748460f8b00821","e5796985ccafe2f71126ed6c0ac939ffa015a8c0744a24b7aee6d587103fd2f7"]';

select tidb_decode_sql_digests(@digests);
```

```sql
+------------------------------------+
| tidb_decode_sql_digests(@digests)  |
+------------------------------------+
| ["begin",null,"select * from `t`"] |
+------------------------------------+
1 row in set (0.00 sec)
```

上の例では、パラメーターは 3 つの SQL ダイジェストを含む JSON 配列であり、対応する SQL ステートメントはクエリ結果の 3 つの項目です。ただし、2 番目の SQL ダイジェストに対応する SQL ステートメントがクラスターから見つからないため、結果の 2 番目の項目は`null`になります。

```sql
select tidb_decode_sql_digests(@digests, 10);
```

```sql
+---------------------------------------+
| tidb_decode_sql_digests(@digests, 10) |
+---------------------------------------+
| ["begin",null,"select * f..."]        |
+---------------------------------------+
1 row in set (0.01 sec)
```

上記の呼び出しでは、2 番目のパラメーター (切り捨ての長さ) を 10 として指定し、クエリ結果の 3 番目のステートメントの長さが 10 を超えています。したがって、最初の 10 文字のみが保持され、最後に`"..."`が追加されます。 end は切り捨てを示します。

以下も参照してください。

-   [`Statement Summary Tables`](/statement-summary-tables.md)
-   [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### TIDB_SHARD {#tidb-shard}

`TIDB_SHARD`関数を使用すると、インデックス ホットスポットを分散するシャード インデックスを作成できます。シャード インデックスは、 `TIDB_SHARD`関数が接頭辞として付けられた式インデックスです。

-   作成:

    インデックス フィールド`a`のシャード インデックスを作成するには、 `uk((tidb_shard(a)), a))`使用できます。一意のセカンダリインデックス`uk((tidb_shard(a)), a))`のインデックスフィールド`a`上のデータが単調増加または減少することによって引き起こされるホットスポットがある場合、インデックスのプレフィックス`tidb_shard(a)`によってホットスポットを分散させ、クラスターのスケーラビリティを向上させることができます。

-   シナリオ:

    -   一意のセカンダリ インデックス上のキーが単調増加または減少することによって引き起こされる書き込みホットスポットがあり、インデックスには整数型のフィールドが含まれています。
    -   SQL ステートメントは、セカンダリ インデックスのすべてのフィールドに基づいて等価クエリを、個別の`SELECT`として、または`UPDATE` 、 `DELETE`などによって生成された内部クエリとして実行します。等価クエリには`a = 1`または`a IN (1, 2, ......)` 2 つの方法が含まれます。

-   制限事項:

    -   不等号クエリでは使用できません。
    -   `OR`と一番外側の`AND`演算子を組み合わせたクエリでは使用できません。
    -   `GROUP BY`項では使用できません。
    -   `ORDER BY`項では使用できません。
    -   `ON`項では使用できません。
    -   `WHERE`サブクエリでは使用できません。
    -   整数フィールドのみの一意のインデックスを分散するために使用できます。
    -   複合インデックスでは有効にならない場合があります。
    -   FastPlan プロセスを実行できないため、オプティマイザーのパフォーマンスに影響します。
    -   実行プラン キャッシュの準備には使用できません。

次の例は、 `TIDB_SHARD`関数の使用方法を示しています。

-   `TIDB_SHARD`関数を使用して SHARD 値を計算します。

    次のステートメントは、 `TIDB_SHARD`関数を使用して SHARD 値`12373743746`を計算する方法を示しています。

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

-   `TIDB_SHARD`関数を使用してシャード インデックスを作成します。

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

### TIDB_ROW_CHECKSUM {#tidb-row-checksum}

`TIDB_ROW_CHECKSUM`関数は、行のチェックサム値をクエリするために使用されます。この関数は、FastPlan プロセス内の`SELECT`のステートメントでのみ使用できます。つまり、 `SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id = ?`や`SELECT TIDB_ROW_CHECKSUM() FROM t WHERE id IN (?, ?, ...)`のようなステートメントを通じてクエリを実行できます。

TiDB の単一行データのチェックサム機能 (システム変数[`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)によって制御) を有効にするには、次のステートメントを実行します。

```sql
SET GLOBAL tidb_enable_row_level_checksum = ON;
```

テーブル`t`を作成し、データを挿入します。

```sql
USE test;
CREATE TABLE t (id INT PRIMARY KEY, k INT, c int);
INSERT INTO TABLE t values (1, 10, a);
```

次のステートメントは、テーブル`t`の`id = 1`である行のチェックサム値をクエリする方法を示しています。

```sql
SELECT *, TIDB_ROW_CHECKSUM() FROM t WHERE id = 1;
```

出力は次のとおりです。

```sql
+----+------+------+---------------------+
| id | k    | c    | TIDB_ROW_CHECKSUM() |
+----+------+------+---------------------+
|  1 |   10 | a    | 3813955661          |
+----+------+------+---------------------+
1 row in set (0.000 sec)
```

### CURRENT_RESOURCE_GROUP {#current-resource-group}

`CURRENT_RESOURCE_GROUP`関数は、現在のセッションがバインドされているリソース グループ名を表示するために使用されます。 [リソース制御](/tidb-resource-control.md)機能が有効になっている場合、SQL ステートメントで使用できる利用可能なリソースは、バインドされたリソース グループのリソース クォータによって制限されます。

セッションが確立されると、TiDB はログイン ユーザーがデフォルトでバインドされているリソース グループにセッションをバインドします。ユーザーがどのリソース グループにもバインドされていない場合、セッションは`default`リソース グループにバインドされます。セッションが確立されると、ユーザーのバインドされたリソース グループが[ユーザーにバインドされたリソース グループを変更する](/sql-statements/sql-statement-alter-user.md#modify-basic-user-information)によって変更されても、デフォルトではバインドされたリソース グループは変更されません。現在のセッションのバインドされたリソース グループを変更するには、 [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md)を使用できます。

#### 例 {#example}

ユーザー`user1`を作成し、2 つのリソース グループ`rg1`と`rg2`を作成し、ユーザー`user1`をリソース グループ`rg1`にバインドします。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
CREATE RESOURCE GROUP 'rg2' RU_PER_SEC = 2000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

`user1`を使用してログインし、現在のユーザーにバインドされているリソース グループを表示します。

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

    +--------------------------+
    | CURRENT_RESOURCE_GROUP() |
    +--------------------------+
    | rg1                      |
    +--------------------------+
    1 row in set (0.00 sec)

`SET RESOURCE GROUP`を実行して現在のセッションのリソース グループを`rg2`に設定し、現在のユーザーにバインドされているリソース グループを表示します。

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

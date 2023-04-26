---
title: TiDB Specific Functions
summary: Learn about the usage of TiDB specific functions.
---

# TiDB固有の機能 {#tidb-specific-functions}

次の関数はTiDB 拡張機能であり、MySQL には存在しません。

| 関数名                                                                                | 機能説明                                                                                                                                       |
| :--------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `TIDB_BOUNDED_STALENESS()`                                                         | `TIDB_BOUNDED_STALENESS`関数は、時間範囲内で可能な限り新しいデータを読み取るように TiDB に指示します。参照: [`AS OF TIMESTAMP`句を使用した履歴データの読み取り](/as-of-timestamp.md)             |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key)                                         | `TIDB_DECODE_KEY`関数を使用して、TiDB でエンコードされたキー エントリを`_tidb_rowid`と`table_id`を含む JSON 構造にデコードできます。これらのエンコードされたキーは、一部のシステム テーブルとログ出力で見つけることができます。 |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan)                                       | `TIDB_DECODE_PLAN`関数を使用して、TiDB 実行計画をデコードできます。                                                                                              |
| `TIDB_IS_DDL_OWNER()`                                                              | `TIDB_IS_DDL_OWNER`関数を使用して、接続している TiDB インスタンスが DDL 所有者であるかどうかを確認できます。 DDL 所有者は、クラスター内の他のすべてのノードに代わって DDL ステートメントを実行する役割を担う TiDB インスタンスです。  |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso)                                           | `TIDB_PARSE_TSO`関数を使用して、TiDB TSO タイムスタンプから物理タイムスタンプを抽出できます。参照: [`tidb_current_ts`](/system-variables.md#tidb_current_ts) .                 |
| [`TIDB_VERSION()`](#tidb_version)                                                  | `TIDB_VERSION`関数は、TiDB のバージョンと追加のビルド情報を返します。                                                                                               |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | `TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (形式と引数のないフォーム) を照会するために使用されます。                                 |
| `VITESS_HASH(str)`                                                                 | `VITESS_HASH`関数は、Vitess の`HASH`関数と互換性のある文字列のハッシュを返します。これは、Vitess からのデータ移行を支援することを目的としています。                                                 |
| `TIDB_SHARD()`                                                                     | `TIDB_SHARD`関数を使用してシャード インデックスを作成し、インデックス ホットスポットを分散させることができます。シャード インデックスは、プレフィックスとして`TIDB_SHARD`関数を持つ式インデックスです。                          |

## 例 {#examples}

このセクションでは、上記の関数のいくつかの例を示します。

### TIDB_DECODE_KEY {#tidb-decode-key}

次の例では、テーブル`t1`に TiDB によって生成された非表示の`rowid`があります。ステートメントでは`TIDB_DECODE_KEY`が使用されます。結果から、非クラスタ化主キーの典型的な結果である、非表示の`rowid`がデコードされて出力されていることがわかります。

{{< copyable "" >}}

```sql
SELECT START_KEY, TIDB_DECODE_KEY(START_KEY) FROM information_schema.tikv_region_status WHERE table_name='t1' AND REGION_ID=2\G
```

```sql
*************************** 1. row ***************************
                 START_KEY: 7480000000000000FF3B5F728000000000FF1DE3F10000000000FA
TIDB_DECODE_KEY(START_KEY): {"_tidb_rowid":1958897,"table_id":"59"}
1 row in set (0.00 sec)
```

次の例では、テーブル`t2`に複合クラスタ化された主キーがあります。 JSON 出力から、主キーの一部である両方の列の名前と値を含む`handle`を確認できます。

{{< copyable "" >}}

```sql
show create table t2\G
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

{{< copyable "" >}}

```sql
select * from information_schema.tikv_region_status where table_name='t2' limit 1\G
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

{{< copyable "" >}}

```sql
select tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9');
```

```sql
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| tidb_decode_key('7480000000000000FF3E5F720400000000FF0000000601633430FF3338646232FF2D64FF3531632D3131FF65FF622D386337352DFFFF3830653635303138FFFF61396265000000FF00FB000000000000F9') |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| {"handle":{"a":"6","id":"c4038db2-d51c-11eb-8c75-80e65018a9be"},"table_id":62}                                                                                                        |
+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.001 sec)
```

### TIDB_DECODE_PLAN {#tidb-decode-plan}

TiDB 実行計画は、スロー クエリ ログでエンコードされた形式で見つけることができます。 `TIDB_DECODE_PLAN()`関数は、エンコードされた計画を人間が読める形式にデコードするために使用されます。

この関数は、ステートメントの実行時に計画が取得されるため便利です。 `EXPLAIN`のステートメントを再実行すると、データの分散と統計が時間の経過とともに変化するため、異なる結果が生じる可能性があります。

{{< copyable "" >}}

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

`TIDB_PARSE_TSO`関数を使用して、TiDB TSO タイムスタンプから物理タイムスタンプを抽出できます。 TSO は Time Stamp Oracle の略で、トランザクションごとに PD (Placement Driver) によって単調に増加するタイムスタンプです。

TSO は、次の 2 つの部分で構成される数値です。

-   物理的なタイムスタンプ
-   論理カウンター

{{< copyable "" >}}

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

ここで`TIDB_PARSE_TSO` `tidb_current_ts`セッション変数で使用可能なタイムスタンプ番号から物理タイムスタンプを抽出するために使用されます。タイムスタンプはトランザクションごとに発行されるため、この関数はトランザクションで実行されます。

### TIDB_VERSION {#tidb-version}

`TIDB_VERSION`関数を使用して、接続している TiDBサーバーのバージョンとビルドの詳細を取得できます。 GitHub で問題を報告するときに、この機能を使用できます。

{{< copyable "" >}}

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

`TIDB_DECODE_SQL_DIGESTS()`関数は、クラスター内の一連の SQL ダイジェストに対応する正規化された SQL ステートメント (形式と引数のないフォーム) を照会するために使用されます。この関数は、1 つまたは 2 つの引数を受け入れます。

-   `digests` : 文字列。このパラメーターは JSON 文字列配列の形式であり、配列内の各文字列は SQL ダイジェストです。
-   `stmtTruncateLength` : 整数 (オプション)。返される結果の各 SQL ステートメントの長さを制限するために使用されます。 SQL ステートメントが指定された長さを超える場合、ステートメントは切り捨てられます。 `0` 、長さが無制限であることを意味します。

この関数は、JSON 文字列配列の形式の文字列を返します。配列の*i*番目の項目は、 `digests`パラメータの<em>i</em>番目の要素に対応する正規化された SQL ステートメントです。 `digests`パラメータの要素が有効な SQL ダイジェストでない場合、またはシステムが対応する SQL ステートメントを見つけられない場合、返される結果の対応する項目は`null`です。切り捨ての長さが指定されている場合 ( `stmtTruncateLength > 0` )、この長さを超える返される結果のステートメントごとに、最初の`stmtTruncateLength`文字が保持され、切り捨てを示すためにサフィックス`"..."`が末尾に追加されます。 `digests`パラメータが`NULL`の場合、関数の戻り値は`NULL`です。

> **ノート：**
>
> -   この機能を使用できるのは、 [プロセス](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)権限を持つユーザーのみです。
> -   `TIDB_DECODE_SQL_DIGESTS`を実行すると、TiDB は各 SQL ダイジェストに対応するステートメントをステートメント サマリー テーブルからクエリするため、どの SQL ダイジェストでも対応するステートメントが常に見つかるという保証はありません。クラスター内で実行されたステートメントのみを見つけることができ、これらの SQL ステートメントを照会できるかどうかは、ステートメント要約テーブルの関連する構成によっても影響を受けます。ステートメント要約表の詳細な説明については、 [ステートメント要約表](/statement-summary-tables.md)を参照してください。
> -   この関数には高いオーバーヘッドがあります。多数の行を含むクエリ (たとえば、大規模でビジーなクラスターで`information_schema.cluster_tidb_trx`のテーブル全体をクエリする場合) で、この関数を使用すると、クエリの実行時間が長くなりすぎる可能性があります。注意して使用してください。
>     -   この関数は、呼び出されるたびに`STATEMENTS_SUMMARY` 、 `STATEMENTS_SUMMARY_HISTORY` 、 `CLUSTER_STATEMENTS_SUMMARY` 、および`CLUSTER_STATEMENTS_SUMMARY_HISTORY`テーブルを内部的にクエリし、クエリには`UNION`操作が含まれるため、オーバーヘッドが高くなります。この関数は現在、ベクトル化をサポートしていません。つまり、複数行のデータに対してこの関数を呼び出す場合、上記のクエリは行ごとに個別に実行されます。

{{< copyable "" >}}

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

上記の例では、パラメーターは 3 つの SQL ダイジェストを含む JSON 配列であり、対応する SQL ステートメントはクエリ結果の 3 つの項目です。しかし、2 番目の SQL ダイジェストに対応する SQL ステートメントがクラスターから見つからないため、結果の 2 番目の項目は`null`になります。

{{< copyable "" >}}

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

上記の呼び出しでは、2 番目のパラメーター (つまり、切り捨ての長さ) を 10 に指定しており、クエリ結果の 3 番目のステートメントの長さが 10 を超えています。したがって、最初の 10 文字のみが保持され、最後に`"..."`が追加されます。切り捨てを示します。

以下も参照してください。

-   [`Statement Summary Tables`](/statement-summary-tables.md)
-   [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### TIDB_SHARD {#tidb-shard}

`TIDB_SHARD`関数を使用してシャード インデックスを作成し、インデックス ホットスポットを分散させることができます。シャード インデックスは、 `TIDB_SHARD`関数で始まる式インデックスです。

#### シャード インデックス {#shard-index}

-   作成:

    インデックス フィールド`a`のシャード インデックスを作成するには、 `uk((tidb_shard(a)), a))`使用できます。一意のセカンダリ インデックス`uk((tidb_shard(a)), a))`のインデックス フィールド`a`のデータが単調に増加または減少することによって発生するホットスポットがある場合、インデックスのプレフィックス`tidb_shard(a)`はホットスポットを分散させてクラスターのスケーラビリティを向上させることができます。

-   シナリオ:

    -   一意のセカンダリ インデックスで単調に増加または減少するキーによって発生する書き込みホットスポットがあり、インデックスに整数型フィールドが含まれています。
    -   SQL ステートメントは、セカンダリ インデックスのすべてのフィールドに基づいて、個別の`SELECT`または`UPDATE` 、 `DELETE`などによって生成された内部クエリとして等値クエリを実行します。等価クエリには`a = 1`または`a IN (1, 2, ......)` 2 つの方法が含まれます。

-   制限:

    -   不等式クエリでは使用できません。
    -   `OR`と outmost `AND`演算子が混在するクエリでは使用できません。
    -   `GROUP BY`節では使用できません。
    -   `ORDER BY`節では使用できません。
    -   `ON`節では使用できません。
    -   `WHERE`サブクエリでは使用できません。
    -   整数フィールドのみの一意のインデックスを分散させるために使用できます。
    -   複合インデックスでは有効にならない場合があります。
    -   オプティマイザーのパフォーマンスに影響する FastPlan プロセスを実行できません。
    -   実行計画キャッシュの準備には使用できません。

#### あらすじ {#synopsis}

```ebnf+diagram
TIDBShardExpr ::=
    "TIDB_SHARD" "(" expr ")"
```

#### 例 {#example}

-   `TIDB_SHARD`関数を使用して SHARD 値を計算します。

    次のステートメントは、 `TIDB_SHARD`関数を使用して`12373743746`の SHARD 値を計算する方法を示しています。

    {{< copyable "" >}}

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

-   シャード値は次のとおりです。

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

-   `TIDB_SHARD`関数を使用してシャード インデックスを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

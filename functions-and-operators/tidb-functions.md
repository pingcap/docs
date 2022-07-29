---
title: TiDB Specific Functions
summary: Learn about the usage of TiDB specific functions.
---

# TiDB固有の機能 {#tidb-specific-functions}

次の関数はTiDB拡張機能であり、MySQLには存在しません。

| 関数名                                                                                | 機能の説明                                                                                                                             |
| :--------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `TIDB_BOUNDED_STALENESS()`                                                         | `TIDB_BOUNDED_STALENESS`関数は、時間範囲内で可能な限り新しいデータを読み取るようにTiDBに指示します。参照： [`AS OF TIMESTAMP`句を使用して履歴データを読み取る](/as-of-timestamp.md)      |
| [`TIDB_DECODE_KEY(str)`](#tidb_decode_key)                                         | `TIDB_DECODE_KEY`関数を使用して、TiDBでエンコードされたキーエントリを`_tidb_rowid`と`table_id`を含むJSON構造にデコードできます。これらのエンコードされたキーは、一部のシステムテーブルおよびログ出力にあります。  |
| [`TIDB_DECODE_PLAN(str)`](#tidb_decode_plan)                                       | `TIDB_DECODE_PLAN`関数は、TiDB実行プランをデコードするために使用できます。                                                                                  |
| `TIDB_IS_DDL_OWNER()`                                                              | `TIDB_IS_DDL_OWNER`関数を使用して、接続しているTiDBインスタンスがDDL所有者であるかどうかを確認できます。 DDL所有者は、クラスタの他のすべてのノードに代わってDDLステートメントを実行するタスクを実行するTiDBインスタンスです。 |
| [`TIDB_PARSE_TSO(num)`](#tidb_parse_tso)                                           | `TIDB_PARSE_TSO`関数を使用して、TiDBTSOタイムスタンプから物理タイムスタンプを抽出できます。参照： [`tidb_current_ts`](/system-variables.md#tidb_current_ts) 。          |
| [`TIDB_VERSION()`](#tidb_version)                                                  | `TIDB_VERSION`関数は、追加のビルド情報を含むTiDBバージョンを返します。                                                                                      |
| [`TIDB_DECODE_SQL_DIGESTS(digests, stmtTruncateLength)`](#tidb_decode_sql_digests) | `TIDB_DECODE_SQL_DIGESTS()`関数は、クラスタのSQLダイジェストのセットに対応する正規化されたSQLステートメント（形式と引数のないフォーム）を照会するために使用されます。                               |
| `VITESS_HASH(str)`                                                                 | `VITESS_HASH`関数は、Vitessの`HASH`関数と互換性のある文字列のハッシュを返します。これは、Vitessからのデータ移行を支援することを目的としています。                                          |
| `TIDB_SHARD()`                                                                     | `TIDB_SHARD`関数を使用してシャードインデックスを作成し、インデックスのホットスポットを分散させることができます。シャードインデックスは、プレフィックスとして`TIDB_SHARD`関数を持つ式インデックスです。                   |

## 例 {#examples}

このセクションでは、上記のいくつかの関数の例を示します。

### TIDB_DECODE_KEY {#tidb-decode-key}

次の例では、テーブル`t1`にTiDBによって生成された非表示の`rowid`があります。ステートメントでは`TIDB_DECODE_KEY`が使用されています。結果から、非表示の`rowid`がデコードされて出力されていることがわかります。これは、クラスター化されていない主キーの一般的な結果です。

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

次の例では、テーブル`t2`に複合クラスター主キーがあります。 JSON出力から、主キーの一部である両方の列の名前と値を含む`handle`を確認できます。

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

TiDB実行プランは、エンコードされた形式で低速クエリログにあります。次に、 `TIDB_DECODE_PLAN()`関数を使用して、エンコードされた計画を人間が読める形式にデコードします。

この関数は、ステートメントの実行時にプランがキャプチャされるため便利です。 `EXPLAIN`でステートメントを再実行すると、データの分散と統計が時間の経過とともに変化するため、異なる結果が生成される可能性があります。

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

`TIDB_PARSE_TSO`関数を使用して、TiDBTSOタイムスタンプから物理タイムスタンプを抽出できます。 TSOはTimeStampOracleの略で、トランザクションごとにPD（Placement Driver）によって与えられる単調に増加するタイムスタンプです。

TSOは、次の2つの部分で構成される数値です。

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

ここで、 `TIDB_PARSE_TSO`は、 `tidb_current_ts`セッション変数で使用可能なタイムスタンプ番号から物理タイムスタンプを抽出するために使用されます。タイムスタンプはトランザクションごとに提供されるため、この関数はトランザクションで実行されます。

### TIDB_VERSION {#tidb-version}

`TIDB_VERSION`関数を使用して、接続しているTiDBサーバーのバージョンとビルドの詳細を取得できます。この関数は、GitHubで問題を報告するときに使用できます。

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

`TIDB_DECODE_SQL_DIGESTS()`関数は、クラスタのSQLダイジェストのセットに対応する正規化されたSQLステートメント（形式と引数のないフォーム）を照会するために使用されます。この関数は、1つまたは2つの引数を受け入れます。

-   `digests` ：文字列。このパラメーターはJSON文字列配列の形式であり、配列内の各文字列はSQLダイジェストです。
-   `stmtTruncateLength` ：整数（オプション）。これは、返される結果の各SQLステートメントの長さを制限するために使用されます。 SQLステートメントが指定された長さを超えると、ステートメントは切り捨てられます。 `0`は、長さが無制限であることを意味します。

この関数は、JSON文字列配列の形式の文字列を返します。配列の*i*番目の項目は、 `digests`パラメーターの<em>i</em>番目の要素に対応する正規化されたSQLステートメントです。 `digests`パラメーターの要素が有効なSQLダイジェストではない場合、またはシステムが対応するSQLステートメントを見つけられない場合、返される結果の対応する項目は`null`です。切り捨ての長さが指定されている場合（ `stmtTruncateLength > 0` ）、この長さを超える戻り結果の各ステートメントについて、最初の`stmtTruncateLength`文字が保持され、末尾に接尾辞`"..."`が追加されて切り捨てが示されます。 `digests`パラメータが`NULL`の場合、関数の戻り値は`NULL`です。

> **ノート：**
>
> -   この機能を使用できるのは、 [処理する](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)の権限を持つユーザーのみです。
> -   `TIDB_DECODE_SQL_DIGESTS`が実行されると、TiDBはステートメントサマリーテーブルから各SQLダイジェストに対応するステートメントをクエリするため、対応するステートメントがどのSQLダイジェストでも常に見つかるという保証はありません。クラスタで実行されたステートメントのみが検出され、これらのSQLステートメントを照会できるかどうかは、ステートメント要約テーブルの関連する構成によっても影響を受けます。ステートメント要約テーブルの詳細な説明については、 [ステートメント要約表](/statement-summary-tables.md)を参照してください。
> -   この関数はオーバーヘッドが高くなります。行数が多いクエリ（たとえば、大規模でビジーなクラスタで`information_schema.cluster_tidb_trx`のテーブル全体をクエリする）では、この関数を使用すると、クエリの実行時間が長すぎる可能性があります。注意して使用してください。
>     -   この関数は、呼び出されるたびに`STATEMENTS_SUMMARY` 、および`STATEMENTS_SUMMARY_HISTORY`のテーブルを内部的にクエリし、クエリには`CLUSTER_STATEMENTS_SUMMARY`の操作が含まれるため、オーバーヘッドが高く`UNION` `CLUSTER_STATEMENTS_SUMMARY_HISTORY` 。この関数は現在、ベクトル化をサポートしていません。つまり、データの複数の行に対してこの関数を呼び出すと、上記のクエリは行ごとに個別に実行されます。

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

上記の例では、パラメーターは3つのSQLダイジェストを含むJSON配列であり、対応するSQLステートメントはクエリ結果の3つの項目です。ただし、2番目のSQLダイジェストに対応するSQLステートメントがクラスタから見つからないため、結果の2番目の項目は`null`です。

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

上記の呼び出しでは、2番目のパラメーター（つまり、切り捨ての長さ）が10として指定され、クエリ結果の3番目のステートメントの長さが10より大きいため、最初の10文字のみが保持され、 `"..."`が追加されます。 end、これは切り捨てを示します。

参照：

-   [`Statement Summary Tables`](/statement-summary-tables.md)
-   [`INFORMATION_SCHEMA.TIDB_TRX`](/information-schema/information-schema-tidb-trx.md)

### TIDB_SHARD {#tidb-shard}

`TIDB_SHARD`関数を使用してシャードインデックスを作成し、インデックスのホットスポットを分散させることができます。シャードインデックスは、接頭辞`TIDB_SHARD`の関数が付いた式インデックスです。

#### シャードインデックス {#shard-index}

-   作成：

    インデックスフィールド`a`のシャードインデックスを作成するには、 `uk((tidb_shard(a)), a))`を使用できます。一意のセカンダリインデックス`uk((tidb_shard(a)), a))`のインデックスフィールド`a`のデータが単調に増加または減少することによってホットスポットが発生した場合、インデックスのプレフィックス`tidb_shard(a)`がホットスポットを分散させて、クラスタのスケーラビリティを向上させることができます。

-   シナリオ：

    -   一意のセカンダリインデックスのキーが単調に増加または減少することによって引き起こされる書き込みホットスポットがあり、インデックスには整数型のフィールドが含まれています。
    -   SQLステートメントは、セカンダリインデックスのすべてのフィールドに基づいて、個別の`SELECT`として、または`UPDATE`などによって生成された内部クエリとして等価クエリを実行し`DELETE` 。等式クエリには、 `a = 1`または`a IN (1, 2, ......)`の2つの方法があります。

-   制限：

    -   不等式クエリでは使用できません。
    -   `OR`と最上位の`AND`演算子が混在するクエリでは使用できません。
    -   `GROUP BY`節では使用できません。
    -   `ORDER BY`節では使用できません。
    -   `ON`節では使用できません。
    -   `WHERE`サブクエリでは使用できません。
    -   整数フィールドのみの一意のインデックスを分散するために使用できます。
    -   複合インデックスでは有効にならない場合があります。
    -   オプティマイザのパフォーマンスに影響するFastPlanプロセスを通過できません。
    -   実行プランキャッシュの準備には使用できません。

#### あらすじ {#synopsis}

```ebnf+diagram
TIDBShardExpr ::=
    "TIDB_SHARD" "(" expr ")"
```

#### 例 {#example}

-   `TIDB_SHARD`関数を使用して、SHARD値を計算します。

    次のステートメントは、 `TIDB_SHARD`関数を使用してSHARD値`12373743746`を計算する方法を示しています。

    {{< copyable "" >}}

    ```sql
    SELECT TIDB_SHARD(12373743746);
    ```

-   SHARD値は次のとおりです。

    ```sql
    +-------------------------+
    | TIDB_SHARD(12373743746) |
    +-------------------------+
    |                     184 |
    +-------------------------+
    1 row in set (0.00 sec)
    ```

-   `TIDB_SHARD`関数を使用してシャードインデックスを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE TABLE test(id INT PRIMARY KEY CLUSTERED, a INT, b INT, UNIQUE KEY uk((tidb_shard(a)), a));
    ```

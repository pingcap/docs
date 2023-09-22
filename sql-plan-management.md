---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
---

# SQL 計画管理 (SPM) {#sql-plan-management-spm}

SQL 計画管理は、SQL バインディングを実行して SQL 実行計画を手動で妨害する一連の関数です。これらの関数には、SQL バインディング、ベースライン キャプチャ、ベースライン展開が含まれます。

## SQLバインディング {#sql-binding}

SQL バインディングは SPM の基礎です。 [オプティマイザーのヒント](/optimizer-hints.md)ドキュメントでは、ヒントを使用して特定の実行プランを選択する方法が紹介されています。ただし、場合によっては、SQL ステートメントを変更せずに実行選択に干渉する必要がある場合があります。 SQL バインディングを使用すると、SQL ステートメントを変更せずに、指定した実行プランを選択できます。

<CustomContent platform="tidb">

> **注記：**
>
> SQL バインディングを使用するには、 `SUPER`権限が必要です。 TiDB が十分な権限を持っていないことを示すプロンプトを表示した場合は、 [権限管理](/privilege-management.md)を参照して必要な権限を追加してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> SQL バインディングを使用するには、 `SUPER`権限が必要です。 TiDB が十分な権限を持っていないことを示すプロンプトを表示した場合は、 [権限管理](https://docs.pingcap.com/tidb/stable/privilege-management)を参照して必要な権限を追加してください。

</CustomContent>

### バインディングを作成する {#create-a-binding}

SQL ステートメントまたは履歴実行計画に従って、SQL ステートメントのバインディングを作成できます。

#### SQL文に従ってバインディングを作成する {#create-a-binding-according-to-a-sql-statement}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

このステートメントは、SQL 実行プランを GLOBAL または SESSION レベルでバインドします。現在、TiDB でサポートされているバインド可能な SQL ステートメント (BindableStmt) には、 `SELECT`サブクエリを持つ`SELECT` 、 `DELETE` 、 `UPDATE` 、および`INSERT` / `REPLACE`が含まれます。

> **注記：**
>
> バインディングは、手動で追加されたヒントよりも優先されます。したがって、対応するバインディングが存在するときにヒントを含むステートメントを実行すると、オプティマイザーの動作を制御するヒントは有効になりません。ただし、他の種類のヒントも引き続き有効です。

具体的には、これらのステートメントの 2 種類は、構文の競合により実行プランにバインドできません。次の例を参照してください。

```sql
-- Type one: Statements that get the Cartesian product by using the `JOIN` keyword and not specifying the associated columns with the `USING` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2
USING
    SELECT * FROM t t1 JOIN t t2;

-- Type two: `DELETE` statements that contain the `USING` keyword.
CREATE GLOBAL BINDING for
    DELETE FROM t1 USING t1 JOIN t2 ON t1.a = t2.a
USING
    DELETE FROM t1 USING t1 JOIN t2 ON t1.a = t2.a;
```

同等のステートメントを使用すると、構文の競合を回避できます。たとえば、上記のステートメントは次のように書き換えることができます。

```sql
-- First rewrite of type one statements: Add a `USING` clause for the `JOIN` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1 JOIN t t2 USING (a)
USING
    SELECT * FROM t t1 JOIN t t2 USING (a);

-- Second rewrite of type one statements: Delete the `JOIN` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM t t1, t t2
USING
    SELECT * FROM t t1, t t2;

-- Rewrite of type two statements: Remove the `USING` keyword from the `delete` statement.
CREATE GLOBAL BINDING for
    DELETE t1 FROM t1 JOIN t2 ON t1.a = t2.a
using
    DELETE t1 FROM t1 JOIN t2 ON t1.a = t2.a;
```

> **注記：**
>
> `SELECT`のサブクエリを含む`INSERT` / `REPLACE`ステートメントの実行プラン バインディングを作成する場合、 `INSERT` / `REPLACE`キーワードの後ではなく、 `SELECT`サブクエリにバインドするオプティマイザ ヒントを指定する必要があります。そうしないと、オプティマイザのヒントが意図したとおりに有効になりません。

以下に 2 つの例を示します。

```sql
-- The hint takes effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
using
    INSERT INTO t1 SELECT /*+ use_index(@sel_1 t2, a) */ * FROM t2 WHERE a > 1 AND b = 1;

-- The hint cannot take effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1
using
    INSERT /*+ use_index(@sel_1 t2, a) */ INTO t1 SELECT * FROM t2 WHERE a > 1 AND b = 1;
```

実行計画バインディングの作成時にスコープを指定しない場合、デフォルトのスコープは SESSION です。 TiDB オプティマイザーは、バインドされた SQL ステートメントを正規化し、システム テーブルに保存します。 SQL クエリの処理時に、正規化されたステートメントがシステム テーブル内のバインドされた SQL ステートメントの 1 つと一致し、システム変数`tidb_use_plan_baselines`が`on` (デフォルト値は`on` ) に設定されている場合、TiDB はこのステートメントに対応するオプティマイザー ヒントを使用します。一致する実行プランが複数ある場合、オプティマイザはバインドするコストが最も低いものを選択します。

`Normalization`は、SQL文中の定数を可変パラメータに変換し、クエリで参照するテーブルのデータベースを明示的に指定する処理で、SQL文中のスペースや改行の処理が標準化されています。次の例を参照してください。

```sql
SELECT * FROM t WHERE a >    1
-- After normalization, the above statement is as follows:
SELECT * FROM test . t WHERE a > ?
```

> **注記：**
>
> カンマ`,`で結合された複数の定数は、 `?`ではなく`...`として正規化されます。
>
> 例えば：
>
> ```sql
> SELECT * FROM t limit 10
> SELECT * FROM t limit 10, 20
> SELECT * FROM t WHERE a IN (1)
> SELECT * FROM t WHERE a IN (1,2,3)
> -- After normalization, the above statements are as follows:
> SELECT * FROM test . t limit ?
> SELECT * FROM test . t limit ...
> SELECT * FROM test . t WHERE a IN ( ? )
> SELECT * FROM test . t WHERE a IN ( ... )
> ```
>
> バインディングが作成されると、TiDB は、単一の定数を含む SQL ステートメントと、コンマで結合された複数の定数を含む SQL ステートメントを異なる方法で処理します。したがって、2 つの SQL タイプのバインディングを個別に作成する必要があります。
>
> 例えば：
>
> ```sql
> CREATE TABLE t(a INT, b INT, KEY idx(a));
> CREATE SESSION BINDING for SELECT * FROM t WHERE a IN (?) USING SELECT /*+ use_index(t, idx) */ * FROM t WHERE a in (?);
> SHOW BINDINGS;
> +-----------------------------------------------+----------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                  | Bind_sql                                                             | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-----------------------------------------------+----------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | SELECT * FROM `test` . `t` WHERE `a` IN ( ? ) | SELECT /*+ use_index(`t` `idx`)*/ * FROM `test`.`t` WHERE `a` IN (?) | test       | enabled | 2023-08-23 14:15:31.472 | 2023-08-23 14:15:31.472 | utf8mb4 | utf8mb4_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-----------------------------------------------+----------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> SELECT * FROM t WHERE a IN (1);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> SELECT * FROM t WHERE a IN (1,2);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        0 |
> +--------------------------+
> CREATE SESSION BINDING for SELECT * FROM t WHERE a IN (?,?) USING SELECT /*+ use_index(t, idx) */ * FROM t WHERE a IN (?,?);
> show bindings;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | SELECT * FROM `test` . `t` WHERE `a` IN ( ... ) | SELECT /*+ use_index(`t` `idx`)*/ * FROM `test`.`t` WHERE `a` IN (?,?) | test       | enabled | 2023-08-23 14:16:30.762 | 2023-08-23 14:16:30.762 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> | SELECT * FROM `test` . `t` WHERE `a` IN ( ? )   | SELECT /*+ use_index(`t` `idx`)*/ * FROM `test`.`t` WHERE `a` IN (?)   | test       | enabled | 2023-08-23 14:15:31.472 | 2023-08-23 14:15:31.472 | utf8mb4 | utf8mb4_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> SELECT * FROM t WHERE a IN (1,2);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> SELECT * FROM t WHERE a IN (1,2,3);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> DROP SESSION BINDING for SELECT * FROM t WHERE a IN (?);
> SHOW BINDINGS;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | SELECT * FROM `test` . `t` WHERE `a` IN ( ... ) | SELECT /*+ use_index(`t` `idx`)*/ * FROM `test`.`t` WHERE `a` IN (?,?) | test       | enabled | 2023-08-23 14:16:30.762 | 2023-08-23 14:16:30.762 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> SELECT * FROM t WHERE a IN (1);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        0 |
> +--------------------------+
> ```

SQL ステートメントに GLOBAL スコープと SESSION スコープの両方でバインドされた実行プランがある場合、オプティマイザーは SESSION バインディングに遭遇すると GLOBAL スコープのバインドされた実行プランを無視するため、SESSION スコープ内のこのステートメントのバインドされた実行プランは、次の実行プランをシールドします。グローバルスコープ。

例えば：

```sql
--  Creates a GLOBAL binding and specifies using `sort merge join` in this binding.
CREATE GLOBAL BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ merge_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- The execution plan of this SQL statement uses the `sort merge join` specified in the GLOBAL binding.
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Creates another SESSION binding and specifies using `hash join` in this binding.
CREATE BINDING for
    SELECT * FROM t1, t2 WHERE t1.id = t2.id
USING
    SELECT /*+ hash_join(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;

-- In the execution plan of this statement, `hash join` specified in the SESSION binding is used, instead of `sort merge join` specified in the GLOBAL binding.
explain SELECT * FROM t1, t2 WHERE t1.id = t2.id;
```

最初の`SELECT`ステートメントが実行されると、オプティマイザは GLOBAL スコープのバインディングを通じて`sm_join(t1, t2)`ヒントをステートメントに追加します。 `explain`の結果の実行プランの最上位ノードは MergeJoin です。 2 番目の`SELECT`ステートメントが実行されるとき、オプティマイザは GLOBAL スコープのバインディングの代わりに SESSION スコープのバインディングを使用し、ステートメントに`hash_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行プランの最上位ノードは HashJoin です。

標準化された SQL ステートメントごとに、一度に`CREATE BINDING`を使用して作成できるバインディングは 1 つだけです。同じ標準化された SQL ステートメントに対して複数のバインディングが作成される場合、最後に作成されたバインディングは保持され、以前のすべてのバインディング (作成および展開されたバインディング) は削除済みとしてマークされます。ただし、セッション バインディングとグローバル バインディングは共存でき、このロジックの影響を受けません。

さらに、バインディングを作成する場合、TiDB ではセッションがデータベース コンテキスト内にあることが必要です。つまり、クライアントが接続されるとき、または`use ${database}`が実行されるときにデータベースが指定されます。

元の SQL ステートメントとバインドされたステートメントは、正規化とヒントの削除後に同じテキストを持つ必要があります。そうしないと、バインドが失敗します。次の例を考えてみましょう。

-   パラメータ化とヒントの削除の前後のテキストが同じであるため、このバインディングは正常に作成できます`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   元の SQL ステートメントは`SELECT * FROM test . t WHERE a > ?`として処理され、バインドされた SQL ステートメントは`SELECT * FROM test . t WHERE b > ?`として別の方法で処理されるため、このバインドは失敗します。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **注記：**
>
> `PREPARE` / `EXECUTE`ステートメントおよびバイナリ プロトコルで実行されるクエリの場合、 `PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントの実行プラン バインディングを作成する必要があります。

#### 過去の実行計画に従ってバインディングを作成する {#create-a-binding-according-to-a-historical-execution-plan}

SQL ステートメントの実行プランを履歴実行プランに固定するには、 `plan_digest`を使用してその履歴実行プランを SQL ステートメントにバインドできます。これは、SQL ステートメントに従ってバインドするよりも便利です。

現在、この機能には次の制限があります。

-   この機能は、履歴実行計画に従ってヒントを生成し、生成されたヒントをバインドに使用します。履歴実行プランは[ステートメント概要テーブル](/statement-summary-tables.md)に保存されるため、この機能を使用する前に、まず[`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304)システム変数を有効にする必要があります。
-   現在、この機能は、現在の TiDB ノードの`statements_summary`と`statements_summary_history`テーブルでの履歴実行プランのバインディングのみをサポートしています。 `can't find any plans`エラーが発生した場合は、クラスター内の別の TiDB ノードに接続して、バインドを再試行できます。

このバインド方法の SQL ステートメントは次のとおりです。

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST 'plan_digest';
```

このステートメントは、 `plan_digest`を使用して実行プランを SQL ステートメントにバインドします。デフォルトのスコープは SESSION です。作成されるバインディングの適用可能なSQL文、優先度、範囲、有効条件は[SQL ステートメントに従って作成されたバインディング](#create-a-binding-according-to-a-sql-statement)と同様です。

このバインド方法を使用するには、まず`statements_summary`でターゲットの履歴実行プランに対応する`plan_digest`取得し、次に`plan_digest`を使用してバインディングを作成する必要があります。詳細な手順は次のとおりです。

1.  `statements_summary`のターゲット実行計画に対応する`plan_digest`を取得します。

    例えば：

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY(a));
    SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1'\G;
    ```

    以下は、 `statements_summary`のクエリ結果の例の一部です。

        SUMMARY_BEGIN_TIME: 2022-12-01 19:00:00
        ...........
              DIGEST_TEXT: select * from `t` where `a` = ?
        ...........
              PLAN_DIGEST: 4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb
                     PLAN:  id                  task        estRows operator info                           actRows execution info                                                                                                                                             memory      disk
                            TableReader_7       root        10      data:Selection_6                        0       time:4.05ms, loops:1, cop_task: {num: 1, max: 598.6µs, proc_keys: 0, rpc_num: 2, rpc_time: 609.8µs, copr_cache_hit_ratio: 0.00, distsql_concurrency: 15}   176 Bytes   N/A
                            └─Selection_6       cop[tikv]   10      eq(test.t.a, 1)                         0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
                              └─TableFullScan_5 cop[tikv]   10000   table:t, keep order:false, stats:pseudo 0       tikv_task:{time:560.8µs, loops:0}                                                                                                                          N/A         N/A
              BINARY_PLAN: 6QOYCuQDCg1UYWJsZVJlYWRlcl83Ev8BCgtTZWxlY3Rpb25fNhKOAQoPBSJQRnVsbFNjYW5fNSEBAAAAOA0/QSkAAQHwW4jDQDgCQAJKCwoJCgR0ZXN0EgF0Uh5rZWVwIG9yZGVyOmZhbHNlLCBzdGF0czpwc2V1ZG9qInRpa3ZfdGFzazp7dGltZTo1NjAuOMK1cywgbG9vcHM6MH1w////CQMEAXgJCBD///8BIQFzCDhVQw19BAAkBX0QUg9lcSgBfCAudC5hLCAxKWrmYQAYHOi0gc6hBB1hJAFAAVIQZGF0YTo9GgRaFAW4HDQuMDVtcywgCbYcMWKEAWNvcF8F2agge251bTogMSwgbWF4OiA1OTguNsK1cywgcHJvY19rZXlzOiAwLCBycGNfBSkAMgkMBVcQIDYwOS4pEPBDY29wcl9jYWNoZV9oaXRfcmF0aW86IDAuMDAsIGRpc3RzcWxfY29uY3VycmVuY3k6IDE1fXCwAXj///////////8BGAE=

    この例では、 `plan_digest`に対応する実行計画は`4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`であることがわかります。

2.  バインディングを作成するには`plan_digest`を使用します。

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

作成したバインディングが有効かどうかを確認するには、 [バインディングを表示する](#view-bindings)を実行します。

```sql
SHOW BINDINGS\G;
```

    *************************** 1. row ***************************
    Original_sql: select * from `test` . `t` where `a` = ?
        Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t` ) ignore_index(`t` `a`)*/ * FROM `test`.`t` WHERE `a` = 1
           ...........
      Sql_digest: 6909a1bbce5f64ade0a532d7058dd77b6ad5d5068aee22a531304280de48349f
     Plan_digest:
    1 row in set (0.01 sec)

    ERROR:
    No query specified

```sql
SELECT * FROM t WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
```

    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)

### バインディングを削除する {#remove-a-binding}

SQL ステートメントまたは`sql_digest`に従ってバインディングを削除できます。

#### SQL文に従ってバインディングを削除します。 {#remove-a-binding-according-to-a-sql-statement}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

このステートメントは、指定された実行プラン バインディングを GLOBAL または SESSION レベルで削除します。デフォルトのスコープは SESSION です。

一般に、SESSION スコープのバインディングは主にテストまたは特殊な状況で使用されます。すべての TiDB プロセスでバインディングを有効にするには、GLOBAL バインディングを使用する必要があります。作成された SESSION バインディングは、セッションが閉じる前に SESSION バインディングが削除された場合でも、SESSION が終了するまで対応する GLOBAL バインディングを保護します。この場合、バインディングは有効にならず、プランはオプティマイザーによって選択されます。

次の例は、SESSION バインディングが GLOBAL バインディングをシールドする[バインディングを作成する](#create-a-binding)の例に基づいています。

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Views the SQL execution plan again.
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

上記の例では、SESSION スコープ内のドロップされたバインディングは、GLOBAL スコープ内の対応するバインディングをシールドします。オプティマイザはステートメントに`sm_join(t1, t2)`ヒントを追加しません。 `explain`結果の実行プランの最上位ノードは、このヒントでは MergeJoin に固定されません。代わりに、最上位ノードはコスト推定に従ってオプティマイザによって独立して選択されます。

#### <code>sql_digest</code>に従ってバインディングを削除します {#remove-a-binding-according-to-code-sql-digest-code}

SQL ステートメントに従ってバインディングを削除するだけでなく、 `sql_digest`に従ってバインディングを削除することもできます。

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST 'sql_digest';
```

このステートメントは、GLOBAL または SESSION レベルで`sql_digest`に対応する実行プラン バインディングを削除します。デフォルトのスコープは SESSION です。 `sql_digest` x [バインディングの表示](#view-bindings)を取得できます。

> **注記：**
>
> `DROP GLOBAL BINDING`を実行すると、現在の tidb-server インスタンス キャッシュ内のバインディングが削除され、システム テーブル内の対応する行のステータスが「削除」に変更されます。他の tidb-server インスタンスは、キャッシュ内の対応するバインディングを削除するために「削除済み」ステータスを読み取る必要があるため、このステートメントはシステム テーブル内のレコードを直接削除しません。これらのシステム テーブル内のステータスが「削除済み」のレコードについては、100 `bind-info-lease` (デフォルト値は`3s`で合計`300s` ) 間隔ごとに、バックグラウンド スレッドが 10 の前に`update_time`のバインディングを再利用およびクリアする操作をトリガーします。 `bind-info-lease` (すべての tidb-server インスタンスが「削除済み」ステータスを読み取り、キャッシュを更新したことを確認するため)。

### バインディングステータスの変更 {#change-binding-status}

#### SQL文に従ってバインディングステータスを変更する {#change-binding-status-according-to-a-sql-statement}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

このステートメントを実行すると、バインディングのステータスを変更できます。デフォルトのステータスは有効です。有効スコープはデフォルトでは GLOBAL であり、変更できません。

このステートメントを実行するときは、バインディングのステータスを`Disabled`から`Enabled`または`Enabled`から`Disabled`にのみ変更できます。ステータス変更に使用できるバインディングがない場合は、 `There are no bindings can be set the status. Please check the SQL text`という警告メッセージが返されます。 `Disabled`ステータスのバインディングはどのクエリでも使用されないことに注意してください。

#### <code>sql_digest</code>に従ってバインディングステータスを変更する {#change-binding-status-according-to-code-sql-digest-code}

SQL ステートメントに従ってバインド ステータスを変更するだけでなく、 `sql_digest`に従ってバインド ステータスを変更することもできます。

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

`sql_digest`で変更できるバインドステータスと効果は変更[SQL文によると](#change-binding-status-according-to-a-sql-statement)と同じです。ステータス変更に使用できるバインドがない場合は、警告メッセージ`can't find any binding for 'sql_digest'`が返されます。

### バインディングをビュー {#view-bindings}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

このステートメントは、バインディング更新時刻の新しいものから古いものまでの順序に従って、実行プランのバインディングを GLOBAL または SESSION レベルで出力します。デフォルトのスコープは SESSION です。以下に示すように、現在`SHOW BINDINGS` 11 列を出力します。

| カラム名         | 注記                                                                                                                                      |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------- |
| オリジナル_SQL    | パラメータ化後の元の SQL ステートメント                                                                                                                  |
| バインドSQL      | ヒントを含むバインドされた SQL ステートメント                                                                                                               |
| デフォルト_データベース | デフォルトのデータベース                                                                                                                            |
| 状態           | `enabled` (v6.0 の`using`ステータスを置き換え)、 `disabled` 、および`rejected` `deleted` `pending verify` `invalid`                                     |
| 作成時間         | 時間を創る                                                                                                                                   |
| 更新時間         | 更新時間                                                                                                                                    |
| 文字コード        | キャラクターセット                                                                                                                               |
| 照合順序         | 順序付けルール                                                                                                                                 |
| ソース          | バインディングの作成方法`manual` (SQL ステートメントに従って作成)、 `history` (過去の実行計画に従って作成)、 `capture` (TiDB によって自動的にキャプチャ)、 `evolve` (TiDB によって自動的に展開) が含まれます。 |
| sql_digest   | 正規化された SQL ステートメントのダイジェスト                                                                                                               |
| 計画ダイジェスト     | 実行計画のダイジェスト                                                                                                                             |

### バインディングのトラブルシューティングを行う {#troubleshoot-a-binding}

次のいずれかの方法を使用して、バインディングのトラブルシューティングを行うことができます。

-   システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)を使用して、最後に実行されたステートメントで使用された実行プランがバインディングからのものであるかどうかを示します。

    ```sql
    -- Create a global binding
    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    SELECT * FROM t;
    SELECT @@[SESSION.]last_plan_from_binding;
    ```

    ```sql
    +--------------------------+
    | @@last_plan_from_binding |
    +--------------------------+
    |                        1 |
    +--------------------------+
    1 row in set (0.00 sec)
    ```

-   SQL ステートメントのクエリ プランを表示するには、 `explain format = 'verbose'`ステートメントを使用します。 SQL ステートメントでバインディングが使用されている場合は、 `show warnings`実行して、SQL ステートメントでどのバインディングが使用されているかを確認できます。

    ```sql
    -- Create a global binding

    CREATE GLOBAL BINDING for
        SELECT * FROM t
    USING
        SELECT /*+ USE_INDEX(t, idx_a) */ * FROM t;

    -- Use explain format = 'verbose' to view the execution plan of a SQL statement

    explain format = 'verbose' SELECT * FROM t;

    -- Run `show warnings` to view the binding used in the query.

    show warnings;
    ```

    ```sql
    +-------+------+--------------------------------------------------------------------------+
    | Level | Code | Message                                                                  |
    +-------+------+--------------------------------------------------------------------------+
    | Note  | 1105 | Using the bindSQL: SELECT /*+ USE_INDEX(`t` `idx_a`)*/ * FROM `test`.`t` |
    +-------+------+--------------------------------------------------------------------------+
    1 row in set (0.01 sec)

    ```

### キャッシュバインディング {#cache-bindings}

各 TiDB インスタンスには、バインディング用に最も長く使用されていない (LRU) キャッシュがあります。キャッシュ容量はシステム変数[`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)によって制御されます。 TiDB インスタンスにキャッシュされたバインディングを表示できます。

バインディングのキャッシュ ステータスを表示するには、 `SHOW binding_cache status`ステートメントを実行します。このステートメントでは、有効スコープはデフォルトで GLOBAL であり、変更できません。このステートメントは、キャッシュ内で使用可能なバインディングの数、システム内で使用可能なバインディングの合計数、キャッシュされたすべてのバインディングのメモリ使用量、およびキャッシュの合計メモリを返します。

```sql

SHOW binding_cache status;
```

```sql
+-------------------+-------------------+--------------+--------------+
| bindings_in_cache | bindings_in_table | memory_usage | memory_quota |
+-------------------+-------------------+--------------+--------------+
|                 1 |                 1 | 159 Bytes    | 64 MB        |
+-------------------+-------------------+--------------+--------------+
1 row in set (0.00 sec)
```

## ベースラインのキャプチャ {#baseline-capturing}

[アップグレード中の実行計画の回帰を防止する](#prevent-regression-of-execution-plans-during-an-upgrade)に使用されるこの機能は、キャプチャ条件を満たすクエリをキャプチャし、これらのクエリのバインディングを作成します。

計画ベースラインは、オプティマイザが SQL ステートメントを実行するために使用できる、承認された計画のコレクションを指します。通常、TiDB は、プランが適切に実行されることを確認した後にのみ、プランをプラン ベースラインに追加します。このコンテキストにおけるプランには、オプティマイザーが実行プランを再現するために必要なプラン関連の詳細 (SQL プラン識別子、ヒント セット、バインド値、オプティマイザー環境など) がすべて含まれます。

### キャプチャを有効にする {#enable-capturing}

ベースラインのキャプチャを有効にするには、 `tidb_capture_plan_baselines` ～ `on`を設定します。デフォルト値は`off`です。

> **注記：**
>
> 自動バインド作成機能は[声明の概要](/statement-summary-tables.md)に依存しているため、自動バインドを使用する前に必ず Statement Summary を有効にしてください。

自動バインディング作成を有効にすると、ステートメント サマリー内の履歴 SQL ステートメントが`bind-info-lease` (デフォルト値は`3s` ) ごとに走査され、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。これらの SQL ステートメントの場合、TiDB はステートメントの概要に記録された実行計画を自動的にバインドします。

ただし、TiDB は、次のタイプの SQL ステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`と`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`など、TiDB の内部で実行される SQL ステートメント。
-   `Enabled`または`Disabled`のバインディングを含むステートメント。
-   キャプチャ条件によってフィルターで除外されたステートメント。

> **注記：**
>
> 現在、バインディングは、クエリ ステートメントによって生成された実行プランを修正するためのヒントのグループを生成します。このように、同じクエリの実行計画は変わりません。同じインデックスまたは結合アルゴリズム (HashJoin や IndexJoin など) を使用するクエリを含む、ほとんどの OLTP クエリについて、TiDB はバインドの前後でプランの一貫性を保証します。ただし、ヒントの制限により、TiDB は、3 つ以上のテーブルの結合、MPP クエリ、複雑な OLAP クエリなど、一部の複雑なクエリに対してプランの一貫性を保証できません。

`PREPARE` / `EXECUTE`ステートメントおよびバイナリ プロトコルで実行されるクエリの場合、TiDB は`PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントのバインディングを自動的にキャプチャします。

> **注記：**
>
> TiDB には一部の機能の正確性を保証するための SQL ステートメントが埋め込まれているため、ベースライン キャプチャはデフォルトでこれらの SQL ステートメントを自動的にシールドします。

### バインディングをフィルターで除外する {#filter-out-bindings}

この機能を使用すると、バインディングをキャプチャしたくないクエリを除外するブロックリストを構成できます。ブロックリストには、テーブル名、頻度、ユーザー名の 3 つの要素があります。

#### 使用法 {#usage}

フィルタリング条件をシステム テーブルに挿入します`mysql.capture_plan_baselines_blacklist` 。その後、フィルタリング条件はクラスタ全体に即座に有効になります。

```sql
-- Filter by table name
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.t');

-- Filter by database name and table name through wildcards
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'test.table_*');
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('table', 'db_*.table_*');

-- Filter by frequency
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('frequency', '2');

-- Filter by user name
 INSERT INTO mysql.capture_plan_baselines_blacklist(filter_type, filter_value) VALUES('user', 'user1');
```

| **次元名** | **説明**                                                                                                                                                       | 備考                                                                                                                                              |
| :------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| テーブル    | テーブル名でフィルターします。各フィルタリング ルールは`db.table`形式です。サポートされているフィルタリング構文には[プレーンなテーブル名](/table-filter.md#plain-table-names)と[ワイルドカード](/table-filter.md#wildcards)が含まれます。 | 大文字小文字を区別しません。テーブル名に不正な文字が含まれている場合、ログは警告メッセージ`[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`を返します。                           |
| 頻度      | 周波数でフィルタリングします。複数回実行された SQL ステートメントはデフォルトでキャプチャされます。頻繁に実行されるステートメントをキャプチャするために高い頻度を設定できます。                                                                   | 頻度を 1 より小さい値に設定すると、不正とみなされ、ログに警告メッセージ`[sql-bind] frequency threshold is less than 1, ignore it`が返されます。複数の周波数フィルター ルールが挿入された場合、最も高い周波数の値が優先されます。 |
| ユーザー    | ユーザー名でフィルターします。ブロックリストに登録されたユーザーによって実行されたステートメントはキャプチャされません。                                                                                                 | 複数のユーザーが同じステートメントを実行し、そのユーザー名がすべてブロックリストに含まれている場合、このステートメントはキャプチャされません。                                                                         |

> **注記：**
>
> -   ブロックリストを変更するにはスーパー権限が必要です。
>
> -   ブロックリストに不正なフィルターが含まれている場合、TiDB はログに警告メッセージ`[sql-bind] unknown capture filter type, ignore it`を返します。

### アップグレード中の実行計画の回帰を防止する {#prevent-regression-of-execution-plans-during-an-upgrade}

TiDB クラスターをアップグレードする前に、次の手順を実行することで、ベースライン キャプチャを使用して実行計画の回帰を防ぐことができます。

1.  ベースラインのキャプチャを有効にして機能し続けます。

    > **注記：**
    >
    > テスト データは、ベースライン キャプチャの長期作業がクラスター負荷のパフォーマンスにわずかな影響を与えることを示しています。したがって、重要な計画 (2 回以上表示される) がキャプチャされるように、ベースライン キャプチャをできるだけ長く有効にすることをお勧めします。

2.  TiDB クラスターをアップグレードします。アップグレード後、TiDB はそれらのキャプチャされたバインディングを使用して、実行計画の一貫性を確保します。

3.  アップグレード後、必要に応じてバインディングを削除します。

    -   [`SHOW GLOBAL BINDINGS`](#view-bindings)ステートメントを実行してバインディング ソースを確認します。

        出力の`Source`フィールドをチェックして、バインディングがキャプチャされたか ( `capture` )、手動で作成されたか ( `manual` ) を確認します。

    -   キャプチャされたバインディングを保持するかどうかを決定します。

            -- View the plan with the binding enabled
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

            -- View the plan with the binding disabled
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -   実行計画に一貫性がある場合は、バインディングを安全に削除できます。

        -   実行計画に矛盾がある場合は、統計情報を確認するなどして原因を特定する必要があります。この場合、計画の一貫性を確保するためにバインディングを保持する必要があります。

## ベースラインの進化 {#baseline-evolution}

ベースライン進化は、TiDB v4.0 で導入された SPM の重要な機能です。

データが更新されると、以前にバインドされた実行計画が最適でなくなる可能性があります。ベースライン進化機能は、バインドされた実行計画を自動的に最適化できます。

さらに、ベースラインの進化により、統計情報の変更によって引き起こされる実行計画にもたらされるジッターをある程度回避することもできます。

### 使用法 {#usage}

自動バインディング進化を有効にするには、次のステートメントを使用します。

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

デフォルト値の`tidb_evolve_plan_baselines`は`off`です。

<CustomContent platform="tidb">

> **警告：**
>
> -   ベースライン進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境で使用することは**お**勧めしません。
> -   この変数は、ベースライン進化機能が一般提供 (GA) されるまで、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。本番環境でこの機能をすでに使用している場合は、できるだけ早く無効にしてください。バインディング ステータスが期待どおりではない場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> -   ベースライン進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境で使用することは**お**勧めしません。
> -   この変数は、ベースライン進化機能が一般提供 (GA) されるまで、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。本番環境でこの機能をすでに使用している場合は、できるだけ早く無効にしてください。バインディングのステータスが期待どおりではない場合は、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md) .

</CustomContent>

自動バインディング展開機能が有効になった後、オプティマイザーによって選択された最適な実行プランがバインディング実行プランの中にない場合、オプティマイザーはそのプランを検証を待機する実行プランとしてマークします。 `bind-info-lease` (デフォルト値は`3s` ) 間隔ごとに、検証対象の実行プランが選択され、実際の実行時間の観点からコストが最小のバインディング実行プランと比較されます。検証対象のプランの実行時間が短い場合 (現在の比較基準は、検証対象のプランの実行時間がバインディング実行プランの 2/3 を超えないことです)、このプランは使用可能としてマークされます。バインディング。次の例では、上記のプロセスを説明します。

テーブル`t`が次のように定義されていると仮定します。

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

テーブル`t`に対して次のクエリを実行します。

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

上で定義したテーブルでは、条件`a < 100`を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザは、インデックス`a`を使用する最適な実行プランではなく、テーブル全体のスキャンを誤って選択します。まず、次のステートメントを使用してバインディングを作成できます。

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 using SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

上記のクエリが再度実行されると、オプティマイザはクエリ時間を短縮するためにインデックス`a` (上で作成したバインディングの影響を受ける) を選択します。

table `t`で挿入と削除が実行されると、条件`a < 100`満たす行の数が増加し、条件`b < 100`満たす行の数が減少すると仮定します。現時点では、バインディングの下で​​インデックス`a`を使用することは最適な計画ではなくなる可能性があります。

バインディングの進化により、この種の問題に対処できます。オプティマイザはテーブル内のデータ変更を認識すると、インデックス`b`を使用するクエリの実行プランを生成します。ただし、現行計画のバインディングが存在するため、この照会計画は採用されず、実行されません。代わりに、この計画はバックエンド進化リストに保存されます。展開プロセス中に、このプランの実行時間がインデックス`a`を使用する現在の実行プランよりも明らかに短いことが検証された場合、インデックス`b`が使用可能なバインディング リストに追加されます。この後、クエリが再度実行されると、オプティマイザはまずインデックス`b`を使用する実行プランを生成し、このプランがバインディング リストに含まれていることを確認します。次に、オプティマイザはこの計画を採用して実行し、データ変更後のクエリ時間を短縮します。

自動進化がクラスターに与える影響を軽減するには、次の構成を使用します。

-   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は`600s`です。実際の検証プロセスにおいても、最大実行時間は検証された実行計画の時間の 2 倍以下に制限されます。
-   時間枠を制限するには、 `tidb_evolve_plan_task_start_time` (デフォルトでは`00:00 +0000` ) と`tidb_evolve_plan_task_end_time` (デフォルトでは`23:59 +0000` ) を設定します。

### ノート {#notes}

ベースラインの進化により新しいバインディングが自動的に作成されるため、クエリ環境が変化すると、自動的に作成されたバインディングには複数の動作の選択肢がある可能性があります。次の注意事項に注意してください。

-   ベースラインの進化は、少なくとも 1 つのグローバル バインディングを持つ標準化された SQL ステートメントのみを進化させます。

-   新しいバインディングを作成すると、以前のバインディング (標準化された SQL ステートメントの場合) がすべて削除されるため、新しいバインディングを手動で作成した後、自動的に展開されたバインディングは削除されます。

-   計算プロセスに関連するすべてのヒントは進化中に保持されます。これらのヒントは次のとおりです。

    | ヒント                       | 説明                                               |
    | :------------------------ | :----------------------------------------------- |
    | `memory_quota`            | クエリに使用できる最大メモリ。                                  |
    | `use_toja`                | オプティマイザがサブクエリを結合に変換するかどうか。                       |
    | `use_cascades`            | カスケード オプティマイザーを使用するかどうか。                         |
    | `no_index_merge`          | オプティマイザがテーブルを読み取るためのオプションとしてインデックス マージを使用するかどうか。 |
    | `read_consistent_replica` | テーブルの読み取り時にFollower Readを強制的に有効にするかどうか。          |
    | `max_execution_time`      | クエリの最長期間。                                        |

-   `read_from_storage` 、テーブルを読み取るときに TiKV からデータを読み取るか、 TiFlashからデータを読み取るかを指定する特別なヒントです。 TiDB は分離読み取りを提供するため、分離条件が変化すると、このヒントは展開された実行計画に大きな影響を与えます。したがって、このヒントが最初に作成されたバインディングに存在する場合、TiDB はその進化したバインディングをすべて無視します。

## アップグレードのチェックリスト {#upgrade-checklist}

クラスターのアップグレード中に、SQL Plan Management (SPM) によって互換性の問題が発生し、アップグレードが失敗する可能性があります。アップグレードを確実に成功させるには、アップグレードの事前チェックに次のリストを含める必要があります。

-   v5.2.0 より前のバージョン (つまり、v4.0、v5.0、および v5.1) から現在のバージョンにアップグレードする場合は、アップグレード前に`tidb_evolve_plan_baselines`が無効になっていることを確認してください。この変数を無効にするには、次の手順を実行します。

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version.

    SELECT @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it.

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   v4.0 から現在のバージョンにアップグレードする前に、使用可能な SQL バインディングに対応するすべてのクエリの構文が新しいバージョンで正しいかどうかを確認する必要があります。構文エラーが存在する場合は、対応する SQL バインディングを削除します。これを行うには、次の手順を実行します。

    ```sql
    -- Check the query corresponding to the available SQL binding in the version to be upgraded.

    SELECT bind_sql FROM mysql.bind_info WHERE status = 'using';

    -- Verify the result from the above SQL query in the test environment of the new version.

    bind_sql_0;
    bind_sql_1;
    ...

    -- In the case of a syntax error (ERROR 1064 (42000): You have an error in your SQL syntax), delete the corresponding binding.
    -- For any other errors (for example, tables are not found), it means that the syntax is compatible. No other operation is needed.
    ```

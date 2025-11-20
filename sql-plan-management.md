---
title: SQL Plan Management (SPM)
summary: TiDB での SQL プラン管理について学習します。
---

# SQL プラン管理 (SPM) {#sql-plan-management-spm}

SQL計画管理は、SQLバインディングを実行してSQL実行計画を手動で操作する一連の関数です。これらの関数には、SQLバインディング、ベースラインキャプチャ、ベースラインエボリューションが含まれます。

## SQLバインディング {#sql-binding}

SQLバインディングはSPMの基盤です。1 [オプティマイザヒント](/optimizer-hints.md)ドキュメントでは、ヒントを用いて特定の実行プランを選択する方法を紹介しています。しかし、SQL文を変更せずに実行プランの選択を操作したい場合もあります。SQLバインディングを使用すれば、SQL文を変更せずに特定の実行プランを選択できます。

<CustomContent platform="tidb">

> **注記：**
>
> SQLバインディングを使用するには、 `SUPER`権限が必要です。TiDB から権限が不足しているというメッセージが表示された場合は、 [権限管理](/privilege-management.md)参照して必要な権限を追加してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> SQLバインディングを使用するには、 `SUPER`権限が必要です。TiDB から権限が不足しているというメッセージが表示された場合は、 [権限管理](https://docs.pingcap.com/tidb/stable/privilege-management)参照して必要な権限を追加してください。

</CustomContent>

### バインディングを作成する {#create-a-binding}

SQL ステートメントまたは履歴実行プランに従って、SQL ステートメントのバインディングを作成できます。

#### SQL文に従ってバインディングを作成する {#create-a-binding-according-to-a-sql-statement}

```sql
CREATE [GLOBAL | SESSION] BINDING [FOR BindableStmt] USING BindableStmt;
```

この文は`UPDATE` SQL実行プランをGLOBALまたはSESSIONレベルでバインドします。現在、TiDBでサポートされているバインド可能なSQL文（BindableStmt）には`DELETE` `SELECT` `INSERT` `REPLACE`あり、それぞれ`SELECT`サブクエリが含まれています。以下に例を示します。

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
CREATE GLOBAL BINDING FOR SELECT * FROM orders USING SELECT /*+ use_index(orders, orders_book_id_idx) */ * FROM orders;
```

> **注記：**
>
> バインディングは手動で追加されたヒントよりも優先されます。そのため、対応するバインディングが存在する状態でヒントを含む文を実行すると、オプティマイザの動作を制御するヒントは有効になりません。ただし、他の種類のヒントは引き続き有効です。

具体的には、これらのステートメントのうち2種類は、構文の競合のため実行プランにバインドできません。バインドの作成時に構文エラーが報告されます。次の例をご覧ください。

```sql
-- Type one: Statements that get the Cartesian product by using the `JOIN` keyword and not specifying the associated columns with the `USING` keyword.
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1 JOIN orders o2
USING
    SELECT * FROM orders o1 JOIN orders o2;

-- Type two: `DELETE` statements that contain the `USING` keyword.
CREATE GLOBAL BINDING for
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id
USING
    DELETE FROM users USING users JOIN orders ON users.id = orders.user_id;
```

同等の文を使用することで、構文の競合を回避できます。例えば、上記の文を次のように書き換えることができます。

```sql
-- Rewrite of type one statements: Delete the `JOIN` keyword. Replace it with a comma.
CREATE GLOBAL BINDING for
    SELECT * FROM orders o1, orders o2
USING
    SELECT * FROM orders o1, orders o2;

-- Rewrite of type two statements: Remove the `USING` keyword from the `DELETE` statement.
CREATE GLOBAL BINDING for
    DELETE users FROM users JOIN orders ON users.id = orders.user_id
USING
    DELETE users FROM users JOIN orders ON users.id = orders.user_id;
```

> **注記：**
>
> `REPLACE` `SELECT` `INSERT`実行プランバインディングを作成する場合、バインドするオプティマイザヒントを`INSERT`キーワードの後ではなく、 `SELECT` `REPLACE`に指定する必要があります。そうしないと、オプティマイザヒントは意図したとおりに機能しません。

ここに 2 つの例を示します。

```sql
-- The hint takes effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT INTO orders SELECT /*+ use_index(@sel_1 pre_orders, idx_created) */ * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);

-- The hint cannot take effect in the following statement.
CREATE GLOBAL BINDING for
    INSERT INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR)
USING
    INSERT /*+ use_index(@sel_1 pre_orders, idx_created) */ INTO orders SELECT * FROM pre_orders WHERE status = 'VALID' AND created <= (NOW() - INTERVAL 1 HOUR);
```

実行プランのバインディングを作成する際にスコープを指定しない場合、デフォルトのスコープはSESSIONです。TiDBオプティマイザーは、バインドされたSQL文を正規化し、システムテーブルに格納します。SQLクエリの処理時に、正規化された文がシステムテーブル内のバインドされたSQL文のいずれかと一致し、システム変数`tidb_use_plan_baselines`が`on` （デフォルト値は`on` ）に設定されている場合、TiDBはこの文に対応するオプティマイザーヒントを使用します。一致可能な実行プランが複数ある場合、オプティマイザーは最もコストの低いプランを選択してバインドします。

`Normalization` 、SQL文内の定数を変数パラメータに変換し、クエリで参照されるテーブルのデータベースを明示的に指定する処理です。SQL文内のスペースと改行は標準化された方法で処理されます。次の例をご覧ください。

```sql
SELECT * FROM users WHERE balance >    100
-- After normalization, the above statement is as follows:
SELECT * FROM bookshop . users WHERE balance > ?
```

> **注記：**
>
> 正規化プロセスでは、述語`IN`の`?` `...`として正規化されます。
>
> 例えば：
>
> ```sql
> SELECT * FROM books WHERE type IN ('Novel')
> SELECT * FROM books WHERE type IN ('Novel','Life','Education')
> -- After normalization, the above statements are as follows:
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> SELECT * FROM bookshop . books WHERE type IN ( ... )
> ```
>
> 正規化後、長さの異なる`IN`述語が同じステートメントとして認識されるため、これらすべての述語に適用される 1 つのバインディングを作成するだけで済みます。
>
> 例えば：
>
> ```sql
> CREATE TABLE t (a INT, KEY(a));
> CREATE BINDING FOR SELECT * FROM t WHERE a IN (?) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a in (?);
>
> SELECT * FROM t WHERE a IN (1);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
>
> SELECT * FROM t WHERE a IN (1, 2, 3);
> SELECT @@LAST_PLAN_FROM_BINDING;
> +--------------------------+
> | @@LAST_PLAN_FROM_BINDING |
> +--------------------------+
> |                        1 |
> +--------------------------+
> ```
>
> v7.4.0より前のTiDBクラスターで作成されたバインディングには`IN (?)`含まれている場合があります。v7.4.0以降のバージョンにアップグレードすると、これらのバインディングは`IN (...)`に変更されます。
>
> 例えば：
>
> ```sql
> -- Create a binding on v7.3.0
> mysql> CREATE GLOBAL BINDING FOR SELECT * FROM t WHERE a IN (1) USING SELECT /*+ use_index(t, idx_a) */ * FROM t WHERE a IN (1);
> mysql> SHOW GLOBAL BINDINGS;
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                  | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ? ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:39:02.695 | 2024-09-03 15:39:02.695 | utf8mb4 | utf8mb4_general_ci | manual | 8b9c4e6ab8fad5ba29b034311dcbfc8a8ce57dde2e2d5d5b65313b90ebcdebf7 |             |
> +-----------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
>
> -- After the upgrade to v7.4.0 or a later version
> mysql> SHOW GLOBAL BINDINGS;
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | Original_sql                                    | Bind_sql                                                               | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> | select * from `test` . `t` where `a` in ( ... ) | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` IN (1) | test       | enabled | 2024-09-03 15:35:59.861 | 2024-09-03 15:35:59.861 | utf8mb4 | utf8mb4_general_ci | manual | da38bf216db4a53e1a1e01c79ffa42306419442ad7238480bb7ac510723c8bdf |             |
> +-------------------------------------------------+------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
> ```

SQL ステートメントに GLOBAL スコープと SESSION スコープの両方のバインドされた実行プランがある場合、オプティマイザーは SESSION バインドを検出すると GLOBAL スコープのバインドされた実行プランを無視するため、SESSION スコープ内のこのステートメントのバインドされた実行プランは GLOBAL スコープの実行プランを保護します。

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

最初の`SELECT`番目の文が実行されると、オプティマイザはGLOBALスコープのバインディングを介して`sm_join(t1, t2)`ヒントを文に追加します。5 `explain`の結果における実行プランの最上位ノードはMergeJoinです。2番目の`SELECT`番目の文が実行されると、オプティマイザはGLOBALスコープのバインディングではなくSESSIONスコープのバインディングを使用し、 `hash_join(t1, t2)`ヒントを文に追加します。11 `explain`の結果における実行プランの最上位ノードはHashJoinです。

各標準化SQL文には、 `CREATE BINDING`ずつ作成できるバインディングが1つだけです。同じ標準化SQL文に複数のバインディングが作成された場合、最後に作成されたバインディングが保持され、それ以前に作成されたバインディング（作成済みおよび展開済み）はすべて削除済みとしてマークされます。ただし、セッションバインディングとグローバルバインディングは共存可能であり、このロジックの影響を受けません。

さらに、バインディングを作成する場合、TiDB ではセッションがデータベース コンテキスト内にあることが必要です。つまり、クライアントが接続されるか`use ${database}`が実行されるとき、データベースが指定されることになります。

正規化とヒントの削除後、元のSQL文とバインドされたSQL文のテキストは一致している必要があります。一致していない場合は、バインドは失敗します。次の例をご覧ください。

-   このバインディングは、パラメータ化とヒントの削除の前後のテキストが同じであるため、正常に作成できます`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   このバインディングは、元の SQL ステートメントが`SELECT * FROM test . t WHERE a > ?`として処理されるのに対し、バインドされた SQL ステートメントは`SELECT * FROM test . t WHERE b > ?`として異なる方法で処理されるため、失敗します。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **注記：**
>
> `PREPARE` `EXECUTE`およびバイナリ プロトコルで実行されるクエリの場合、 `PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントの実行プラン バインディングを作成する必要があります。

#### 履歴実行プランに従ってバインディングを作成する {#create-a-binding-according-to-a-historical-execution-plan}

SQL文の実行計画を過去の実行計画に固定するには、Plan Digestを使用して過去の実行計画をSQL文にバインドします。これは、SQL文ごとにバインドするよりも便利です。さらに、複数のSQL文の実行計画を一度にバインドすることも可能です。詳細と例については、 [`CREATE [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-create-binding.md)参照してください。

この機能を使用する場合、次の点に注意してください。

-   この機能は、過去の実行計画に基づいてヒントを生成し、生成されたヒントをバインディングに使用します。過去の実行計画は[明細書要約表](/statement-summary-tables.md)に保存されるため、この機能を使用する前に、 [`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304)システム変数を有効にする必要があります。
-   TiFlashクエリ、3つ以上のテーブルを含む結合クエリ、およびサブクエリを含むクエリの場合、自動生成されるヒントが適切ではないため、プランが完全にバインドされない可能性があります。このような場合、バインドの作成時に警告が表示されます。
-   履歴実行プランがヒント付きのSQL文用である場合、ヒントはバインディングに追加されます。例えば、 `SELECT /*+ max_execution_time(1000) */ * FROM t`実行した後、そのプランダイジェストで作成されたバインディングには`max_execution_time(1000)`含まれます。

このバインディング メソッドの SQL ステートメントは次のとおりです。

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST StringLiteralOrUserVariableList;
```

上記の文は、プランダイジェストを使用して実行プランをSQL文にバインドします。デフォルトのスコープはSESSIONです。作成されたバインドに適用されるSQL文、優先順位、スコープ、および有効条件は、 [SQL文に従って作成されたバインディング](#create-a-binding-according-to-a-sql-statement)と同じです。

このバインディング方法を使用するには、まず`statements_summary`で対象の履歴実行プランに対応するプランダイジェストを取得し、それを使用してバインディングを作成する必要があります。詳細な手順は以下のとおりです。

1.  `statements_summary`対象実行プランに対応するプランダイジェストを取得します。

    例えば：

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY idx_a(a));
    SELECT /*+ IGNORE_INDEX(t, idx_a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, idx_a) */ * FROM t WHERE a = 1'\G
    ```

    以下は`statements_summary`のクエリ結果例の一部です。

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

    この例では、 Plan Digest に対応する実行プランが`4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`あることがわかります。

2.  Plan Digest を使用してバインディングを作成します。

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

作成されたバインディングが有効かどうかを確認するには、 [ビューバインディング](#view-bindings)操作を実行します。

```sql
SHOW BINDINGS\G
```

    *************************** 1. row ***************************
    Original_sql: select * from `test` . `t` where `a` = ?
        Bind_sql: SELECT /*+ use_index(@`sel_1` `test`.`t` ) ignore_index(`t` `idx_a`)*/ * FROM `test`.`t` WHERE `a` = 1
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

SQL ステートメントまたは SQL ダイジェストに従ってバインドを削除できます。

#### SQL文に従ってバインドを削除する {#remove-a-binding-according-to-a-sql-statement}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

このステートメントは、GLOBAL レベルまたは SESSION レベルで指定された実行プランのバインドを削除します。デフォルトのスコープは SESSION です。

一般的に、SESSIONスコープ内のバインディングは、主にテストや特殊な状況で使用されます。バインディングをすべてのTiDBプロセスで有効にするには、GLOBALバインディングを使用する必要があります。作成されたSESSIONバインディングは、セッションが終了する前にSESSIONバインディングが削除された場合でも、対応するGLOBALバインディングをSESSIONの終了まで保護します。この場合、バインディングは有効にならず、オプティマイザによってプランが選択されます。

次の例は、SESSION バインディングが GLOBAL バインディングをシールドする[バインディングを作成する](#create-a-binding)の例に基づいています。

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Views the SQL execution plan again.
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

上記の例では、SESSIONスコープ内の削除されたバインディングが、GLOBALスコープ内の対応するバインディングを隠蔽しています。オプティマイザは、文に`sm_join(t1, t2)`ヒントを追加しません。3 `explain`の結果における実行プランのトップノードは、このヒントによってMergeJoinに固定されるわけではありません。代わりに、オプティマイザはコスト見積もりに基づいてトップノードを独自に選択します。

#### SQLダイジェストに従ってバインディングを削除する {#remove-a-binding-according-to-sql-digest}

SQL文に従ってバインドを削除するだけでなく、SQLダイジェストに従ってバインドを削除することもできます。詳細と例については、 [`DROP [GLOBAL|SESSION] BINDING`](/sql-statements/sql-statement-drop-binding.md)参照してください。

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST StringLiteralOrUserVariableList;
```

この文は、GLOBALまたはSESSIONレベルのSQLダイジェストに対応する実行プランのバインディングを削除します。デフォルトのスコープはSESSIONです。SQLダイジェストは[バインディングの表示](#view-bindings)で取得できます。

> **注記：**
>
> `DROP GLOBAL BINDING`実行すると、現在の tidb-server インスタンスのキャッシュ内のバインディングが削除され、システムテーブル内の対応する行のステータスが「削除済み」に変更されます。この文はシステムテーブル内のレコードを直接削除しません。これは、他の tidb-server インスタンスがキャッシュ内の対応するバインディングを削除するために「削除済み」ステータスを読み取る必要があるためです。これらのシステムテーブル内の「削除済み」ステータスのレコードについては、100 `bind-info-lease` (デフォルト値は`3s`で、合計`300s` ) 間隔ごとに、バックグラウンドスレッドが 10 `bind-info-lease`の前に`update_time`のバインディングの再利用とクリアの操作をトリガーします (すべての tidb-server インスタンスが「削除済み」ステータスを読み取り、キャッシュを更新できるようにするため)。

### バインディングステータスの変更 {#change-binding-status}

#### SQL文に従ってバインディングステータスを変更する {#change-binding-status-according-to-a-sql-statement}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

このステートメントを実行すると、バインディングのステータスを変更できます。デフォルトのステータスはENABLEDです。有効スコープはデフォルトでGLOBALに設定されており、変更できません。

このステートメントを実行すると、バインディングのステータスを`Disabled`から`Enabled`へ、または`Enabled`から`Disabled`へのみ変更できます。ステータス変更に使用できるバインディングがない場合、 `There are no bindings can be set the status. Please check the SQL text`という警告メッセージが返されます。ステータス`Disabled`のバインディングはどのクエリでも使用されないことに注意してください。

#### <code>sql_digest</code>に応じてバインディングステータスを変更する {#change-binding-status-according-to-code-sql-digest-code}

SQL ステートメントに従ってバインディング ステータスを変更するだけでなく、 `sql_digest`に従ってバインディング ステータスを変更することもできます。

```sql
SET BINDING [ENABLED | DISABLED] FOR SQL DIGEST 'sql_digest';
```

`sql_digest`で変更できるバインディングの状態と効果は[SQL文に従って](#change-binding-status-according-to-a-sql-statement)変更したものと同じです。状態変更に使用できるバインディングがない場合、警告メッセージ`can't find any binding for 'sql_digest'`が返されます。

### ビューバインディング {#view-bindings}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

この文は、GLOBALレベルまたはSESSIONレベルの実行プランバインディングを、バインディング更新時刻の最新から最古の順で出力します。デフォルトのスコープはSESSIONです。現在、 `SHOW BINDINGS`以下のように11列を出力します。

| カラム名        | 注記                                                                                                                                                    |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------- |
| オリジナルSQL    | パラメータ化後の元のSQL文                                                                                                                                        |
| バインドSQL     | ヒント付きのバインドされたSQL文                                                                                                                                     |
| デフォルトデータベース | デフォルトのデータベース                                                                                                                                          |
| 状態          | ステータスには`enabled` (v6.0 の`using`ステータスを置き換えます)、 `disabled` 、 `deleted` 、 `invalid` 、 `rejected` 、および`pending verify`が含まれます                              |
| 作成時間        | 時間を創る                                                                                                                                                 |
| 更新時間        | 更新時間                                                                                                                                                  |
| 文字セット       | 文字セット                                                                                                                                                 |
| 照合順序        | 順序付けルール                                                                                                                                               |
| ソース         | バインディングが作成される方法`manual` (SQL ステートメントに従って作成される)、 `history` (履歴実行プランに従って作成される)、 `capture` (TiDB によって自動的に取得される)、および`evolve` (TiDB によって自動的に展開される) が含まれます。 |
| sql_ダイジェスト  | 正規化されたSQL文のダイジェスト                                                                                                                                     |
| プランダイジェスト   | 実行計画のダイジェスト                                                                                                                                           |

### バインディングのトラブルシューティング {#troubleshoot-a-binding}

バインディングのトラブルシューティングには、次のいずれかの方法を使用できます。

-   最後に実行されたステートメントで使用された実行プランがバインディングからのものであるかどうかを表示するには、システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)使用します。

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

-   `explain format = 'verbose'`ステートメントを使用して、SQL ステートメントのクエリプランを表示します。SQL ステートメントでバインディングが使用されている場合は、 `show warnings`を実行して、SQL ステートメントで使用されているバインディングを確認できます。

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

各TiDBインスタンスには、バインディング用のLRU（Least Recently Used）キャッシュがあります。キャッシュ容量はシステム変数[`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)によって制御されます。TiDBインスタンスにキャッシュされているバインディングは、表示できます。

バインディングのキャッシュステータスを表示するには、 `SHOW binding_cache status`ステートメントを実行します。このステートメントの有効スコープはデフォルトで GLOBAL に設定されており、変更できません。このステートメントは、キャッシュ内の利用可能なバインディングの数、システム内の利用可能なバインディングの総数、キャッシュされたすべてのバインディングのメモリ使用量、およびキャッシュの合計メモリを返します。

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

## ステートメントサマリーテーブルを利用して、バインドする必要があるクエリを取得します。 {#utilize-the-statement-summary-table-to-obtain-queries-that-need-to-be-bound}

[声明の要約](/statement-summary-tables.md) 、レイテンシー、実行時間、対応するクエリプランなど、最近のSQL実行情報を記録します。ステートメントサマリーテーブルにクエリを実行すると、条件付き`plan_digest` 、そして[これらの履歴実行計画に従ってバインディングを作成する](/sql-plan-management.md#create-a-binding-according-to-a-historical-execution-plan)取得できます。

以下の例では、過去2週間に10回以上実行され、SQLバインディングのない複数の実行プランを持つ`SELECT`ステートメントをクエリします。クエリを実行時間でソートし、上位100件のクエリを最も高速なプランにバインドします。

```sql
WITH stmts AS (                                                -- Gets all information
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY
  UNION ALL
  SELECT * FROM INFORMATION_SCHEMA.CLUSTER_STATEMENTS_SUMMARY_HISTORY 
),
best_plans AS (
  SELECT plan_digest, `digest`, avg_latency, 
  CONCAT('create global binding from history using plan digest "', plan_digest, '"') as binding_stmt 
  FROM stmts t1
  WHERE avg_latency = (SELECT min(avg_latency) FROM stmts t2   -- The plan with the lowest query latency
                       WHERE t2.`digest` = t1.`digest`)
)

SELECT any_value(digest_text) as query, 
       SUM(exec_count) as exec_count, 
       plan_hint, binding_stmt
FROM stmts, best_plans
WHERE stmts.`digest` = best_plans.`digest`
  AND summary_begin_time > DATE_SUB(NOW(), interval 14 day)    -- Executed in the past 2 weeks
  AND stmt_type = 'Select'                                     -- Only consider select statements
  AND schema_name NOT IN ('INFORMATION_SCHEMA', 'mysql')       -- Not an internal query
  AND plan_in_binding = 0                                      -- No binding yet
GROUP BY stmts.`digest`
  HAVING COUNT(DISTINCT(stmts.plan_digest)) > 1                -- This query is unstable. It has more than 1 plan.
         AND SUM(exec_count) > 10                              -- High-frequency, and has been executed more than 10 times.
ORDER BY SUM(exec_count) DESC LIMIT 100;                       -- Top 100 high-frequency queries.
```

特定のフィルタリング条件を適用して基準を満たすクエリを取得することで、対応する`binding_stmt`列のステートメントを直接実行してバインディングを作成できます。

    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | query                                       | exec_count | plan_hint                                                                   | binding_stmt                                                                                                            |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+
    | select * from `t` where `a` = ? and `b` = ? |        401 | use_index(@`sel_1` `test`.`t` `a`), no_order_index(@`sel_1` `test`.`t` `a`) | create global binding from history using plan digest "0d6e97fb1191bbd08dddefa7bd007ec0c422b1416b152662768f43e64a9958a6" |
    | select * from `t` where `b` = ? and `c` = ? |        104 | use_index(@`sel_1` `test`.`t` `b`), no_order_index(@`sel_1` `test`.`t` `b`) | create global binding from history using plan digest "80c2aa0aa7e6d3205755823aa8c6165092c8521fb74c06a9204b8d35fc037dd9" |
    +---------------------------------------------+------------+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------------------------------------------------+

## データベース間のバインディング {#cross-database-binding}

バージョン7.6.0以降、TiDBでは、バインディング作成構文でワイルドカード`*`を使用してデータベース名を表すことで、データベース間バインディングを作成できます。データベース間バインディングを作成する前に、まずシステム変数「 [`tidb_opt_enable_fuzzy_binding`](/system-variables.md#tidb_opt_enable_fuzzy_binding-new-in-v760)を有効にする必要があります。

クロスデータベースバインディングを使用すると、データが異なるデータベースに分類・保存され、各データベースで同一のオブジェクト定義が維持され、類似のアプリケーションロジックが実行されるシナリオにおいて、実行プランの修正プロセスを簡素化できます。以下に、一般的なユースケースをいくつか示します。

-   SaaSまたはPaaSサービスをTiDBで実行すると、各テナントのデータが別々のデータベースに保存され、データの保守と管理が容易になります。
-   単一インスタンスでデータベースシャーディングを実行し、TiDBに移行した後も元のデータベーススキーマを保持した場合、つまり、元のインスタンスのデータはデータベースごとに分類され、保存されます。

このようなシナリオでは、クロスデータベースバインディングは、ユーザーデータとワークロードの不均一な分散や急激な変化によって引き起こされるSQLパフォーマンスの問題を効果的に軽減できます。SaaSプロバイダーは、クロスデータベースバインディングを使用することで、大容量データを扱うアプリケーションによって検証された実行プランを修正し、小容量データを扱うアプリケーションの急速な増加に起因する潜在的なパフォーマンス問題を回避できます。

データベース間のバインディングを作成するには、バインディングの作成時にデータベース名を表すために`*`を使用します。例:

```sql
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM t; -- Create a GLOBAL scope standard binding.
CREATE GLOBAL BINDING USING SELECT /*+ use_index(t, idx_a) */ * FROM *.t; -- Create a GLOBAL scope cross-database binding.
SHOW GLOBAL BINDINGS;
```

出力は次のようになります。

```sql
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                                          | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `test`.`t` | test       | enabled | 2023-12-29 14:19:01.332 | 2023-12-29 14:19:01.332 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
| select * from `*` . `t`    | SELECT /*+ use_index(`t` `idx_a`)*/ * FROM `*`.`t`    |            | enabled | 2023-12-29 14:19:02.232 | 2023-12-29 14:19:02.232 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+---------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
```

`SHOW GLOBAL BINDINGS`出力では、クロスデータベースバインディングの`Default_db`フィールド値が空で、 `Original_sql`フィールドと`Bind_sql`フィールドのデータベース名は`*`として表されています。このバインディングは、特定のデータベースだけでなく、すべてのデータベースの`select * from t`クエリに適用されます。

同じクエリに対して、クロスデータベース バインディングと標準バインディングの両方が共存できます。TiDB は、バインディングを次の順序で一致させます: SESSION スコープの標準バインディング &gt; SESSION スコープのクロスデータベース バインディング &gt; GLOBAL スコープの標準バインディング &gt; GLOBAL スコープのクロスデータベース バインディング。

作成構文を除き、クロスデータベースバインディングは標準バインディングと同じ削除構文とステータス変更構文を共有します。以下に詳細な使用例を示します。

1.  データベース`db1`と`db2`を作成し、各データベースに 2 つのテーブルを作成します。

    ```sql
    CREATE DATABASE db1;
    CREATE TABLE db1.t1 (a INT, KEY(a));
    CREATE TABLE db1.t2 (a INT, KEY(a));
    CREATE DATABASE db2;
    CREATE TABLE db2.t1 (a INT, KEY(a));
    CREATE TABLE db2.t2 (a INT, KEY(a));
    ```

2.  データベース間バインディング機能を有効にします。

    ```sql
    SET tidb_opt_enable_fuzzy_binding=1;
    ```

3.  データベース間バインディングを作成します。

    ```sql
    CREATE GLOBAL BINDING USING SELECT /*+ use_index(t1, idx_a), use_index(t2, idx_a) */ * FROM *.t1, *.t2;
    ```

4.  クエリを実行し、バインディングが使用されているかどうかを確認します。

    ```sql
    SELECT * FROM db1.t1, db1.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    SELECT * FROM db2.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    SELECT * FROM db1.t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+

    USE db1;
    SELECT * FROM t1, db2.t2;
    SELECT @@LAST_PLAN_FROM_BINDING;
    +--------------------------+
    | @@LAST_PLAN_FROM_BINDING |
    +--------------------------+
    |                        1 |
    +--------------------------+
    ```

5.  バインディングをビュー:

    ```sql
    SHOW GLOBAL BINDINGS;
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | Original_sql                                 | Bind_sql                                                                                 | Default_db | Status  | Create_time             | Update_time             | Charset | Collation          | Source | Sql_digest                                                       | Plan_digest |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    | select * from ( `*` . `t1` ) join `*` . `t2` | SELECT /*+ use_index(`t1` `idx_a`) use_index(`t2` `idx_a`)*/ * FROM (`*` . `t1`) JOIN `*` . `t2` |            | enabled | 2023-12-29 14:22:28.144 | 2023-12-29 14:22:28.144 | utf8    | utf8_general_ci    | manual | ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4 |             |
    +----------------------------------------------+------------------------------------------------------------------------------------------+------------+---------+-------------------------+-------------------------+---------+--------------------+--------+------------------------------------------------------------------+-------------+
    ```

6.  データベース間のバインディングを削除します。

    ```sql
    DROP GLOBAL BINDING FOR SQL DIGEST 'ea8720583e80644b58877663eafb3579700e5f918a748be222c5b741a696daf4';
    SHOW GLOBAL BINDINGS;
    Empty set (0.00 sec)
    ```

## ベースラインキャプチャ {#baseline-capturing}

[アップグレード中の実行計画の回帰を防ぐ](#prevent-regression-of-execution-plans-during-an-upgrade)に使用されるこの機能は、キャプチャ条件を満たすクエリをキャプチャし、これらのクエリのバインディングを作成します。

プラン・ベースラインとは、オプティマイザがSQL文の実行に使用できる承認済みのプランの集合を指します。通常、TiDBはプランが適切に実行されることを確認した後にのみ、プランをプラン・ベースラインに追加します。ここで言うプランとは、オプティマイザが実行プランを再現するために必要なすべてのプラン関連の詳細（SQLプラン識別子、ヒントセット、バインド値、オプティマイザ環境など）を包含するものです。

### キャプチャを有効にする {#enable-capturing}

ベースラインキャプチャを有効にするには、 `tidb_capture_plan_baselines`を`on`に設定します。デフォルト値は`off`です。

> **注記：**
>
> 自動バインディング作成機能は[声明の概要](/statement-summary-tables.md)に依存しているため、自動バインディングを使用する前にステートメント サマリーを有効にしてください。

自動バインディング作成を有効にすると、ステートメントサマリー内の過去のSQL文が`bind-info-lease`回（デフォルト値は`3s` ）ごとに走査され、2回以上出現するSQL文に対してバインディングが自動的に作成されます。これらのSQL文に対して、TiDBはステートメントサマリーに記録された実行プランを自動的にバインドします。

ただし、TiDB は次の種類の SQL ステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`と`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`クエリなど、TiDB 内で内部的に実行される SQL ステートメント。
-   `Enabled`または`Disabled`バインディングを含むステートメント。
-   キャプチャ条件によってフィルター処理されるステートメント。

> **注記：**
>
> 現在、バインディングは、クエリ文によって生成された実行プランを修正するためのヒント群を生成します。これにより、同じクエリに対しては実行プランは変更されません。同じインデックスや結合アルゴリズム（HashJoinやIndexJoinなど）を使用するクエリを含むほとんどのOLTPクエリでは、TiDBはバインディング前後のプランの一貫性を保証します。ただし、ヒントの制限により、2つ以上のテーブルの結合、MPPクエリ、複雑なOLAPクエリなど、一部の複雑なクエリではプランの一貫性を保証できません。

`PREPARE` `EXECUTE`およびバイナリ プロトコルで実行されたクエリの場合、TiDB は`PREPARE`ステートメントではなく、実際の`EXECUTE`ステートメントのバインディングを自動的にキャプチャします。

> **注記：**
>
> TiDB には一部の機能の正確性を確保するための SQL ステートメントが埋め込まれているため、ベースライン キャプチャではデフォルトでこれらの SQL ステートメントが自動的に保護されます。

### バインディングを除外する {#filter-out-bindings}

この機能を使用すると、キャプチャしたくないバインディングを持つクエリを除外するブロックリストを設定できます。ブロックリストには、テーブル名、頻度、ユーザー名の3つの要素があります。

#### 使用法 {#usage}

システムテーブル`mysql.capture_plan_baselines_blacklist`にフィルタリング条件を挿入します。すると、フィルタリング条件はクラスタ全体に即座に反映されます。

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

| **ディメンション名** | **説明**                                                                                                                                                      | 備考                                                                                                                                     |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| テーブル         | テーブル名でフィルタリングします。各フィルタリングルールは`db.table`形式です。サポートされているフィルタリング構文には[プレーンテーブル名](/table-filter.md#plain-table-names)と[ワイルドカード](/table-filter.md#wildcards)含まれます。 | 大文字と小文字は区別されません。テーブル名に無効な文字が含まれている場合、ログに警告メッセージ`[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`返されます。                |
| 頻度           | 頻度でフィルタリングします。複数回実行されたSQL文はデフォルトでキャプチャされます。頻繁に実行されるSQL文をキャプチャするには、高い頻度を設定することができます。                                                                         | 頻度を1未満の値に設定すると無効とみなされ、ログに警告メッセージ`[sql-bind] frequency threshold is less than 1, ignore it`が返されます。複数の頻度フィルタルールが挿入された場合、最も高い頻度の値が優先されます。 |
| ユーザー         | ユーザー名でフィルタリングします。ブロックリストに登録されたユーザーが実行したステートメントはキャプチャされません。                                                                                                  | 複数のユーザーが同じステートメントを実行し、そのユーザー名がすべてブロックリストに含まれている場合、このステートメントはキャプチャされません。                                                                |

> **注記：**
>
> -   ブロックリストを変更するには、スーパー権限が必要です。
>
> -   ブロックリストに無効なフィルターが含まれている場合、TiDB はログに警告メッセージ`[sql-bind] unknown capture filter type, ignore it`を返します。

### アップグレード中の実行計画の回帰を防ぐ {#prevent-regression-of-execution-plans-during-an-upgrade}

TiDB クラスターをアップグレードする前に、次の手順を実行して、ベースライン キャプチャを使用して実行プランの回帰を防ぐことができます。

1.  ベースラインキャプチャを有効にして動作を継続します。

    > **注記：**
    >
    > テストデータによると、ベースラインキャプチャを長期間実行すると、クラスター負荷のパフォーマンスにわずかな影響が出ることが示されています。そのため、重要なプラン（2回以上出現するプラン）をキャプチャできるよう、ベースラインキャプチャを可能な限り有効にすることをお勧めします。

2.  TiDB クラスターをアップグレードします。アップグレード後、TiDB はキャプチャされたバインディングを使用して実行プランの一貫性を確保します。

3.  アップグレード後、必要に応じてバインディングを削除します。

    -   [`SHOW GLOBAL BINDINGS`](#view-bindings)ステートメントを実行してバインディング ソースを確認します。

        出力では、 `Source`フィールドをチェックして、バインディングがキャプチャされたか（ `capture` ）、手動で作成されたか（ `manual` ）を確認します。

    -   キャプチャされたバインディングを保持するかどうかを決定します。

            -- View the plan with the binding enabled
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

            -- View the plan with the binding disabled
            SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
            EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -   実行プランに一貫性がある場合は、バインディングを安全に削除できます。

        -   実行プランに矛盾がある場合は、統計情報を確認するなどして原因を特定する必要があります。この場合、プランの一貫性を確保するために、バインドを保持する必要があります。

## ベースライン進化 {#baseline-evolution}

ベースライン進化は、TiDB v4.0 で導入された SPM の重要な機能です。

データが更新されると、以前にバインドされた実行プランが最適ではなくなる可能性があります。ベースライン進化機能は、バインドされた実行プランを自動的に最適化します。

さらに、ベースラインの進化により、統計情報の変更によって実行プランにもたらされるジッターをある程度回避することもできます。

### 使用法 {#usage}

自動バインディング進化を有効にするには、次のステートメントを使用します。

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

`tidb_evolve_plan_baselines`のデフォルト値は`off`です。

<CustomContent platform="tidb">

> **警告：**
>
> -   ベースライン進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境での使用は推奨され**ません**。
> -   この変数は、ベースラインエボリューション機能が一般提供（GA）されるまで強制的に`off`に設定されます。この機能を有効にしようとするとエラーが返されます。この機能を既に本番環境で使用している場合は、できるだけ早く無効にしてください。バインディングステータスが期待どおりでない場合は、PingCAPまたはコミュニティから[サポートを受ける](/support.md)お知らせください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> -   ベースライン進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境での使用は推奨され**ません**。
> -   この変数は、ベースラインエボリューション機能が一般提供（GA）されるまで強制的に`off`に設定されます。この機能を有効にしようとするとエラーが返されます。この機能を既に本番環境で使用している場合は、できるだけ早く無効にしてください。バインディングステータスが期待どおりでない場合は、 [TiDB Cloudサポートにお問い合わせください](/tidb-cloud/tidb-cloud-support.md)してください。

</CustomContent>

自動バインディング進化機能が有効になった後、オプティマイザによって選択された最適な実行プランがバインディング実行プランの中にない場合、オプティマイザはそのプランを検証待ちの実行プランとしてマークします。 `bind-info-lease`間隔（デフォルト値は`3s` ）ごとに、検証対象の実行プランが選択され、実際の実行時間の観点からコストが最小となるバインディング実行プランと比較されます。検証対象プランの実行時間が短い場合（現在の比較基準は、検証対象プランの実行時間がバインディング実行プランの 2/3 以下であること）、このプランは使用可能なバインディングとしてマークされます。次の例は、上記のプロセスを示しています。

表`t`が次のように定義されていると仮定します。

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

テーブル`t`に対して次のクエリを実行します。

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

上記で定義したテーブルでは、条件`a < 100`を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザはインデックス`a`を使用する最適な実行プランではなく、誤ってフルテーブルスキャンを選択します。まず、次のステートメントを使用してバインディングを作成します。

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 USING SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

上記のクエリが再度実行されると、オプティマイザーはインデックス`a` (上記で作成されたバインディングの影響を受けます) を選択して、クエリ時間を短縮します。

テーブル`t`で挿入と削除が実行されるにつれて、条件`a < 100`を満たす行の数が増加し、条件`b < 100`を満たす行の数が減少すると仮定します。この時点で、バインディングでインデックス`a`を使用することは、もはや最適なプランではない可能性があります。

バインディング進化は、このような問題に対処できます。オプティマイザは、テーブル内のデータ変更を認識すると、インデックス`b`を使用するクエリの実行プランを生成します。ただし、現在のプランのバインディングが存在するため、このクエリプランは採用されず、実行されません。代わりに、このプランはバックエンド進化リストに格納されます。進化プロセス中に、このプランの実行時間がインデックス`a`を使用する現在の実行プランよりも明らかに短いことが検証された場合、インデックス`b`が使用可能なバインディング リストに追加されます。その後、クエリが再度実行されると、オプティマイザはまずインデックス`b`を使用する実行プランを生成し、このプランがバインディング リストにあることを確認します。次に、オプティマイザはこのプランを採用して実行し、データ変更後のクエリ時間を短縮します。

自動進化がクラスターに与える影響を軽減するには、次の構成を使用します。

-   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`設定します。デフォルト値は`600s`です。実際の検証プロセスでは、最大実行時間も検証対象実行プランの2倍以内に制限されます。
-   時間ウィンドウを制限するには、 `tidb_evolve_plan_task_start_time` (デフォルトでは`00:00 +0000` ) と`tidb_evolve_plan_task_end_time` (デフォルトでは`23:59 +0000` ) を設定します。

### 注記 {#notes}

ベースライン進化により新しいバインディングが自動的に作成されるため、クエリ環境が変更されると、自動的に作成されたバインディングの動作が複数選択される場合があります。以下の点にご注意ください。

-   ベースライン進化では、少なくとも 1 つのグローバル バインディングを持つ標準化された SQL ステートメントのみが進化します。

-   新しいバインドを作成すると、以前のバインドがすべて削除されるため (標準化された SQL ステートメントの場合)、新しいバインドを手動で作成すると、自動的に進化したバインドは削除されます。

-   計算プロセスに関連するすべてのヒントは、進化の間も保持されます。これらのヒントは以下の通りです。

    | ヒント                       | 説明                                               |
    | :------------------------ | :----------------------------------------------- |
    | `memory_quota`            | クエリに使用できる最大メモリ。                                  |
    | `use_toja`                | オプティマイザーがサブクエリを結合に変換するかどうか。                      |
    | `use_cascades`            | カスケード オプティマイザーを使用するかどうか。                         |
    | `no_index_merge`          | オプティマイザーがテーブルを読み取るためのオプションとしてインデックスマージを使用するかどうか。 |
    | `read_consistent_replica` | テーブルの読み取り時にFollower Read を強制的に有効にするかどうか。         |
    | `max_execution_time`      | クエリの最長時間。                                        |

-   `read_from_storage`は、テーブル読み取り時に TiKV からデータを読み取るかTiFlashからデータを読み取るかを指定する特別なヒントです。TiDB は分離読み取りを提供するため、分離条件が変化すると、このヒントは進化型実行プランに大きな影響を与えます。したがって、最初に作成されたバインディングにこのヒントが存在する場合、TiDB はすべての進化型バインディングを無視します。

## アップグレードチェックリスト {#upgrade-checklist}

クラスタのアップグレード中に、SQL Plan Management (SPM) によって互換性の問題が発生し、アップグレードが失敗する可能性があります。アップグレードを成功させるには、アップグレードの事前チェックに以下の項目を含める必要があります。

-   v5.2.0より前のバージョン（v4.0、v5.0、v5.1）から現在のバージョンにアップグレードする場合は、アップグレード前に`tidb_evolve_plan_baselines`無効になっていることを確認してください。この変数を無効にするには、以下の手順を実行してください。

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version.

    SELECT @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it.

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   v4.0から現在のバージョンにアップグレードする前に、利用可能なSQLバインディングに対応するすべてのクエリの構文が新しいバージョンでも正しいかどうかを確認する必要があります。構文エラーがある場合は、対応するSQLバインディングを削除してください。これを行うには、以下の手順を実行してください。

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

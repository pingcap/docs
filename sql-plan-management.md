---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
---

# SQL 計画管理 (SPM) {#sql-plan-management-spm}

SQL Plan Management は、SQL バインディングを実行して手動で SQL 実行計画に干渉する関数のセットです。これらの関数には、SQL バインディング、ベースライン キャプチャ、およびベースライン展開が含まれます。

## SQL バインディング {#sql-binding}

SQL バインディングは SPM の基礎です。 [オプティマイザーのヒント](/optimizer-hints.md)ドキュメントでは、ヒントを使用して特定の実行プランを選択する方法を紹介します。ただし、SQL ステートメントを変更せずに実行の選択に干渉する必要がある場合があります。 SQL バインディングを使用すると、SQL ステートメントを変更せずに、指定された実行計画を選択できます。

<CustomContent platform="tidb">

> **ノート：**
>
> SQL バインディングを使用するには、 `SUPER`特権が必要です。 TiDB が十分な権限を持っていないというメッセージを表示した場合は、 [権限管理](/privilege-management.md)を参照して必要な権限を追加してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> SQL バインディングを使用するには、 `SUPER`特権が必要です。 TiDB が十分な権限を持っていないというメッセージを表示した場合は、 [権限管理](https://docs.pingcap.com/tidb/stable/privilege-management)を参照して必要な権限を追加してください。

</CustomContent>

### バインディングを作成する {#create-a-binding}

SQL ステートメントまたは履歴実行計画に従って、SQL ステートメントのバインドを作成できます。

#### SQL文に従ってバインディングを作成する {#create-a-binding-according-to-a-sql-statement}

{{< copyable "" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

このステートメントは、SQL 実行計画を GLOBAL または SESSION レベルでバインドします。現在、TiDB でサポートされているバインド可能な SQL ステートメント (BindableStmt) には、 `SELECT`サブクエリを持つ`SELECT` 、 `DELETE` 、 `UPDATE` 、および`INSERT` / `REPLACE`が含まれます。

> **ノート：**
>
> バインディングは、手動で追加されたヒントよりも優先されます。したがって、対応するバインディングが存在するときにヒントを含むステートメントを実行すると、オプティマイザーの動作を制御するヒントは有効になりません。ただし、他のタイプのヒントは引き続き有効です。

具体的には、これらの 2 つのタイプのステートメントは、構文の競合のために実行プランにバインドできません。次の例を参照してください。

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

同等のステートメントを使用して、構文の競合を回避できます。たとえば、上記のステートメントを次のように書き換えることができます。

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

> **ノート：**
>
> `SELECT`のサブクエリを持つ`INSERT` / `REPLACE`ステートメントの実行プラン バインディングを作成する場合、 `INSERT` / `REPLACE`キーワードの後ではなく、 `SELECT`サブクエリでバインドするオプティマイザ ヒントを指定する必要があります。そうしないと、オプティマイザーのヒントが意図したとおりに機能しません。

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

実行計画バインディングの作成時にスコープを指定しない場合、デフォルトのスコープは SESSION です。 TiDB オプティマイザーは、バインドされた SQL ステートメントを正規化し、システム テーブルに格納します。 SQL クエリを処理するときに、正規化されたステートメントがシステム テーブル内のバインドされた SQL ステートメントの 1 つと一致し、システム変数`tidb_use_plan_baselines`が`on` (デフォルト値は`on` ) に設定されている場合、TiDB はこのステートメントに対応するオプティマイザー ヒントを使用します。一致する実行計画が複数ある場合、オプティマイザは最もコストの低い実行計画を選択してバインドします。

`Normalization`は、SQL ステートメント内の定数を変数パラメーターに変換し、SQL ステートメント内のスペースと改行に関する標準化された処理を使用して、クエリで参照されるテーブルのデータベースを明示的に指定するプロセスです。次の例を参照してください。

```sql
SELECT * FROM t WHERE a >    1
-- After normalization, the above statement is as follows:
SELECT * FROM test . t WHERE a > ?
```

> **ノート：**
>
> コンマ`,`で結合された複数の定数は、 `?`ではなく`...`として正規化されます。
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
> バインディングが作成されると、TiDB は単一の定数を含む SQL ステートメントと、コンマで結合された複数の定数を含む SQL ステートメントを異なる方法で処理します。したがって、2 つの SQL タイプのバインディングを個別に作成する必要があります。

SQL ステートメントが GLOBAL スコープと SESSION スコープの両方でバインドされた実行計画を持っている場合、オプティマイザは SESSION バインディングに遭遇したときに GLOBAL スコープでバインドされた実行計画を無視するため、SESSION スコープでこのステートメントのバインドされた実行計画は実行計画を保護します。グローバルスコープ。

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

最初の`SELECT`ステートメントが実行されると、オプティマイザーは GLOBAL スコープのバインディングを介してステートメントに`sm_join(t1, t2)`ヒントを追加します。 `explain`番目の結果の実行計画の最上位ノードは MergeJoin です。 2 番目の`SELECT`ステートメントが実行されると、オプティマイザーは GLOBAL スコープのバインディングではなく SESSION スコープのバインディングを使用し、ステートメントに`hash_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行計画のトップノードはHashJoinです。

標準化された各 SQL ステートメントは、一度に`CREATE BINDING`を使用して作成されたバインディングを 1 つだけ持つことができます。同じ標準化された SQL ステートメントに対して複数のバインディングが作成されると、最後に作成されたバインディングが保持され、以前に作成されたすべてのバインディング (作成および展開されたもの) は削除済みとしてマークされます。ただし、セッション バインディングとグローバル バインディングは共存でき、このロジックの影響を受けません。

さらに、バインディングを作成するとき、TiDB はセッションがデータベース コンテキスト内にあることを要求します。つまり、クライアントが接続されたとき、または`use ${database}`が実行されたときにデータベースが指定されます。

元の SQL ステートメントとバインドされたステートメントは、正規化とヒントの削除後に同じテキストを持っている必要があります。そうでない場合、バインドは失敗します。次の例を見てください。

-   このバインドは、パラメーター化とヒントの削除の前後のテキストが同じであるため、正常に作成できます: `SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   元の SQL ステートメントは`SELECT * FROM test . t WHERE a > ?`として処理されるのに対し、バインドされた SQL ステートメントは`SELECT * FROM test . t WHERE b > ?`として異なる方法で処理されるため、このバインドは失敗します。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **ノート：**
>
> `PREPARE` / `EXECUTE`ステートメントおよびバイナリ プロトコルで実行されるクエリの場合、 `PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントに対して実行プラン バインディングを作成する必要があります。

#### 過去の実行計画に従ってバインディングを作成する {#create-a-binding-according-to-a-historical-execution-plan}

SQL ステートメントの実行計画を履歴実行計画に固定するには、 `plan_digest`を使用してその履歴実行計画を SQL ステートメントにバインドできます。これは、SQL ステートメントに従ってバインドするよりも便利です。

> **警告：**
>
> 現在、過去の実行計画に従ってバインディングを作成することは、リスクが不明な実験的機能です。本番環境では使用しないでください。

現在、この機能には次の制限があります。

-   この機能は、過去の実行計画に従ってヒントを生成し、生成されたヒントをバインディングに使用します。過去の実行計画は[ステートメント要約表](/statement-summary-tables.md)に保存されるため、この機能を使用する前に、最初に[`tidb_enable_stmt_summary`](/system-variables.md#tidb_enable_stmt_summary-new-in-v304)システム変数を有効にする必要があります。
-   現在、この機能は、現在の TiDB ノードの`statements_summary`および`statements_summary_history`テーブル内の過去の実行計画のバインドのみをサポートしています。 `can't find any plans`エラーが発生した場合は、クラスター内の別の TiDB ノードに接続して、バインドを再試行できます。
-   現在、この機能は、サブクエリを含むクエリ、 TiFlashにアクセスするクエリ、または 3 つ以上のテーブルを結合するクエリでは機能しません。

このバインディング メソッドの SQL ステートメントは次のとおりです。

```sql
CREATE [GLOBAL | SESSION] BINDING FROM HISTORY USING PLAN DIGEST 'plan_digest';
```

このステートメントは、 `plan_digest`を使用して実行計画を SQL ステートメントにバインドします。デフォルトのスコープは SESSION です。作成したバインディングの適用可能なSQL文、優先度、スコープ、有効条件は[SQL ステートメントに従って作成されたバインディング](#create-a-binding-according-to-a-sql-statement)と同じです。

このバインド方法を使用するには、最初に`statements_summary`でターゲットの履歴実行計画に対応する`plan_digest`取得し、次に`plan_digest`を使用してバインドを作成する必要があります。詳細な手順は次のとおりです。

1.  `statements_summary`で対象の実行計画に対応する`plan_digest`を取得します。

    例えば：

    ```sql
    CREATE TABLE t(id INT PRIMARY KEY , a INT, KEY(a));
    SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1;
    SELECT * FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE QUERY_SAMPLE_TEXT = 'SELECT /*+ IGNORE_INDEX(t, a) */ * FROM t WHERE a = 1'\G;
    ```

    以下は、 `statements_summary`のクエリ結果の例の一部です。

    ```
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
    ```

    この例では、 `plan_digest`に対応する実行計画が`4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb`であることがわかります。

2.  `plan_digest`を使用してバインディングを作成します。

    ```sql
    CREATE BINDING FROM HISTORY USING PLAN DIGEST '4e3159169cc63c14b139a4e7d72eae1759875c9a9581f94bb2079aae961189cb';
    ```

作成したバインディングが有効かどうかを確認するには、次のことができます[バインディングを表示](#view-bindings) :

```sql
SHOW BINDINGS\G;
```

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
```

```sql
SELECT * FROM t WHERE a = 1;
SELECT @@LAST_PLAN_FROM_BINDING;
```

```
+--------------------------+
| @@LAST_PLAN_FROM_BINDING |
+--------------------------+
|                        1 |
+--------------------------+
1 row in set (0.00 sec)
```

### バインディングを削除する {#remove-a-binding}

SQL ステートメントまたは`sql_digest`に従ってバインディングを削除できます。

#### SQL ステートメントに従ってバインディングを削除する {#remove-a-binding-according-to-a-sql-statement}

{{< copyable "" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

このステートメントは、GLOBAL または SESSION レベルで指定された実行計画バインディングを削除します。デフォルトのスコープは SESSION です。

一般に、SESSION スコープのバインディングは、主にテストまたは特別な状況で使用されます。すべての TiDB プロセスでバインディングを有効にするには、GLOBAL バインディングを使用する必要があります。作成された SESSION バインディングは、セッションが終了する前に SESSION バインディングが削除された場合でも、SESSION が終了するまで対応する GLOBAL バインディングを保護します。この場合、バインディングは有効ではなく、プランはオプティマイザによって選択されます。

次の例は、SESSION バインディングが GLOBAL バインディングを保護する[バインディングを作成する](#create-a-binding)の例に基づいています。

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Views the SQL execution plan again.
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

上記の例では、SESSION スコープで削除されたバインドにより、GLOBAL スコープの対応するバインドがシールドされます。オプティマイザーは、ステートメントに`sm_join(t1, t2)`ヒントを追加しません。 `explain`結果の実行計画の最上位ノードは、このヒントによって MergeJoin に固定されません。代わりに、最上位ノードは、コスト見積もりに従って最適化プログラムによって個別に選択されます。

#### <code>sql_digest</code>に従ってバインディングを削除する {#remove-a-binding-according-to-code-sql-digest-code}

SQL ステートメントに従ってバインドを削除するだけでなく、 `sql_digest`に従ってバインドを削除することもできます。

```sql
DROP [GLOBAL | SESSION] BINDING FOR SQL DIGEST 'sql_digest';
```

このステートメントは、GLOBAL または SESSION レベルで`sql_digest`に対応する実行計画バインディングを削除します。デフォルトのスコープは SESSION です。 `sql_digest` by [バインディングの表示](#view-bindings)を取得できます。

> **ノート：**
>
> `DROP GLOBAL BINDING`を実行すると、現在の tidb-server インスタンス キャッシュ内のバインディングが削除され、システム テーブル内の対応する行のステータスが「削除済み」に変更されます。このステートメントは、システム テーブル内のレコードを直接削除しません。他の tidb-server インスタンスは、キャッシュ内の対応するバインディングを削除するために「削除済み」ステータスを読み取る必要があるためです。これらのシステム テーブル内のステータスが「削除済み」のレコードの場合、100 `bind-info-lease` (デフォルト値は`3s`で、合計で`300s` ) の間隔ごとに、バックグラウンド スレッドは 10 より前に`update_time`のバインディングで回収およびクリアの操作をトリガーします。 `bind-info-lease` (すべての tidb-server インスタンスが「削除済み」ステータスを読み取り、キャッシュを更新したことを確認するため)。

### バインディング ステータスの変更 {#change-binding-status}

{{< copyable "" >}}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

このステートメントを実行して、バインディングのステータスを変更できます。デフォルトのステータスは ENABLED です。有効なスコープはデフォルトで GLOBAL であり、変更できません。

このステートメントを実行すると、バインディングのステータスを`Disabled`から`Enabled`または`Enabled`から`Disabled`にのみ変更できます。ステータス変更に使用できるバインディングがない場合は、 `There are no bindings can be set the status. Please check the SQL text`という警告メッセージが返されます。 `Disabled`ステータスのバインディングは、どのクエリでも使用されないことに注意してください。

### バインディングをビュー {#view-bindings}

{{< copyable "" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

このステートメントは、バインディングの更新時刻が新しいものから古いものへの順序に従って、GLOBAL または SESSION レベルで実行計画バインディングを出力します。デフォルトのスコープは SESSION です。以下に示すように、現在`SHOW BINDINGS` 11 列を出力します。

| カラム名         | ノート                                                                                                                                    |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| original_sql | パラメータ化後の元の SQL ステートメント                                                                                                                 |
| bind_sql     | ヒント付きのバインドされた SQL ステートメント                                                                                                              |
| default_db   | デフォルトのデータベース                                                                                                                           |
| スターテス        | `enabled` (v6.0 の`using`ステータスを置き換え)、 `disabled` 、 `deleted` 、 `invalid` 、 `rejected` 、および`pending verify`を含むステータス                      |
| create_time  | 時を創る                                                                                                                                   |
| update_time  | 更新時間                                                                                                                                   |
| 文字コード        | キャラクターセット                                                                                                                              |
| 照合順序         | 注文規則                                                                                                                                   |
| ソース          | `manual` (SQL ステートメントに従って作成)、 `history` (過去の実行計画に従って作成)、 `capture` (TiDB によって自動的に取得)、および`evolve` (TiDB によって自動的に進化) を含む、バインディングが作成される方法 |
| sql_digest   | 正規化された SQL ステートメントのダイジェスト                                                                                                              |
| plan_digest  | 実行計画のダイジェスト                                                                                                                            |

### バインディングのトラブルシューティング {#troubleshoot-a-binding}

バインディングのトラブルシューティングには、次のいずれかの方法を使用できます。

-   システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)を使用して、最後に実行されたステートメントで使用された実行プランがバインディングからのものかどうかを示します。

    {{< copyable "" >}}

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

-   `explain format = 'verbose'`ステートメントを使用して、SQL ステートメントのクエリ プランを表示します。 SQL ステートメントでバインディングが使用されている場合は、 `show warnings`実行して、SQL ステートメントで使用されているバインディングを確認できます。

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

### キャッシュ バインディング {#cache-bindings}

各 TiDB インスタンスには、バインディング用の LRU (Least Recent Used) キャッシュがあります。キャッシュ容量は、システム変数[`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)によって制御されます。 TiDB インスタンスにキャッシュされているバインディングを表示できます。

バインディングのキャッシュ ステータスを表示するには、 `SHOW binding_cache status`ステートメントを実行します。このステートメントでは、有効範囲はデフォルトで GLOBAL であり、変更できません。このステートメントは、キャッシュ内の使用可能なバインディングの数、システム内の使用可能なバインディングの合計数、キャッシュされたすべてのバインディングのメモリ使用量、およびキャッシュの合計メモリを返します。

{{< copyable "" >}}

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

[アップグレード中の実行計画の後退を防ぐ](#prevent-regression-of-execution-plans-during-an-upgrade)に使用されるこの機能は、キャプチャ条件を満たすクエリをキャプチャし、これらのクエリのバインディングを作成します。

### キャプチャを有効にする {#enable-capturing}

ベースラインのキャプチャを有効にするには、 `tidb_capture_plan_baselines`を`on`に設定します。デフォルト値は`off`です。

> **ノート：**
>
> 自動バインディング作成機能は[声明の要約](/statement-summary-tables.md)に依存しているため、自動バインディングを使用する前に必ず Statement Summary を有効にしてください。

バインディングの自動作成を有効にすると、Statement Summary の履歴 SQL ステートメントが`bind-info-lease`ごとにトラバースされ (デフォルト値は`3s` )、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。これらの SQL ステートメントの場合、TiDB は Statement Summary に記録された実行計画を自動的にバインドします。

ただし、TiDB は、次のタイプの SQL ステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`および`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`クエリなど、TiDB で内部的に実行される SQL ステートメント。
-   `Enabled`または`Disabled`のバインディングを含むステートメント。
-   条件を取得することによって除外されるステートメント。

> **ノート：**
>
> 現在、バインディングは、クエリ ステートメントによって生成された実行プランを修正するためのヒントのグループを生成します。このように、同じクエリの場合、実行計画は変更されません。同じインデックスまたは結合アルゴリズム (HashJoin や IndexJoin など) を使用するクエリを含むほとんどの OLTP クエリでは、TiDB はバインディングの前後でプランの一貫性を保証します。ただし、ヒントの制限により、TiDB は、3 つ以上のテーブルの結合、MPP クエリ、複雑な OLAP クエリなど、一部の複雑なクエリのプランの一貫性を保証できません。

`PREPARE` / `EXECUTE`ステートメントとバイナリ プロトコルで実行されるクエリの場合、TiDB は`PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントのバインディングを自動的にキャプチャします。

> **ノート：**
>
> TiDB には一部の機能の正確性を確保するために SQL ステートメントが埋め込まれているため、ベースライン キャプチャはデフォルトでこれらの SQL ステートメントを自動的に保護します。

### バインディングを除外する {#filter-out-bindings}

この機能を使用すると、ブロックリストを構成して、バインディングをキャプチャしたくないクエリを除外できます。ブロックリストには、テーブル名、頻度、およびユーザー名の 3 つのディメンションがあります。

#### 使用法 {#usage}

フィルタリング条件をシステム テーブルに挿入します`mysql.capture_plan_baselines_blacklist` 。その後、フィルター条件はクラスター全体ですぐに有効になります。

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

| **ディメンション名** | **説明**                                                                                                                                                           | 備考                                                                                                                                                      |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| テーブル         | テーブル名でフィルタリングします。各フィルタリング ルールは`db.table`形式です。サポートされているフィルタリング構文には、 [プレーンなテーブル名](/table-filter.md#plain-table-names)と[ワイルドカード](/table-filter.md#wildcards)が含まれます。 | 大文字小文字を区別しません。テーブル名に不正な文字が含まれている場合、ログは警告メッセージ`[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`を返します。                                   |
| 周波数          | 頻度でフィルタリングします。複数回実行された SQL ステートメントは、デフォルトでキャプチャされます。頻繁に実行されるステートメントをキャプチャするために、高い頻度を設定できます。                                                                      | frequency を 1 より小さい値に設定することは違法と見なされ、ログは警告メッセージ`[sql-bind] frequency threshold is less than 1, ignore it`を返します。複数の頻度フィルタ ルールが挿入されている場合は、頻度が最も高い値が優先されます。 |
| ユーザー         | ユーザー名でフィルタリングします。ブロックリストに登録されたユーザーによって実行されたステートメントはキャプチャされません。                                                                                                   | 複数のユーザーが同じステートメントを実行し、そのユーザー名がすべてブロックリストにある場合、このステートメントはキャプチャされません。                                                                                     |

> **ノート：**
>
> -   ブロックリストを変更するには、スーパー権限が必要です。
>
> -   ブロックリストに不正なフィルターが含まれている場合、TiDB はログに警告メッセージ`[sql-bind] unknown capture filter type, ignore it`を返します。

### アップグレード中の実行計画の後退を防ぐ {#prevent-regression-of-execution-plans-during-an-upgrade}

TiDB クラスターをアップグレードする前に、次の手順を実行することにより、ベースライン キャプチャを使用して実行計画の回帰を防ぐことができます。

1.  ベースラインのキャプチャを有効にして、引き続き機能させます。

    > **ノート：**
    >
    > テスト データは、ベースライン キャプチャの長期的な作業がクラスター負荷のパフォーマンスにわずかな影響を与えることを示しています。したがって、重要な計画 (2 回以上表示される) がキャプチャされるように、可能な限りベースラインのキャプチャを有効にすることをお勧めします。

2.  TiDB クラスターをアップグレードします。アップグレード後、TiDB はこれらのキャプチャされたバインディングを使用して、実行計画の一貫性を確保します。

3.  アップグレード後、必要に応じてバインディングを削除します。

    -   [`SHOW GLOBAL BINDINGS`](#view-bindings)ステートメントを実行してバインディング ソースを確認します。

        出力の`Source`フィールドをチェックして、バインディングがキャプチャされているか ( `capture` )、手動で作成されているか ( `manual` ) を確認します。

    -   キャプチャされたバインディングを保持するかどうかを決定します。

        ```
        -- View the plan with the binding enabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -- View the plan with the binding disabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;
        ```

        -   実行計画に一貫性がある場合は、バインディングを安全に削除できます。

        -   実行計画に一貫性がない場合は、統計を確認するなどして原因を特定する必要があります。この場合、計画の一貫性を確保するためにバインディングを保持する必要があります。

## ベースラインの進化 {#baseline-evolution}

ベースラインの進化は、TiDB v4.0 で導入された SPM の重要な機能です。

データが更新されると、以前にバインドされた実行計画が最適でなくなる可能性があります。ベースライン進化機能は、バインドされた実行計画を自動的に最適化できます。

さらに、ベースラインの進化は、統計情報の変更によって実行計画にもたらされるジッタをある程度回避することもできます。

### 使用法 {#usage}

自動バインディングの進化を有効にするには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

`tidb_evolve_plan_baselines`のデフォルト値は`off`です。

<CustomContent platform="tidb">

> **警告：**
>
> -   ベースラインの進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境で使用することは**お**勧めしません。
> -   この変数は、ベースライン進化機能が一般に利用可能 (GA) になるまで、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。この機能を本番環境ですでに使用している場合は、できるだけ早く無効にしてください。バインド ステータスが期待どおりではないことがわかった場合は、PingCAP またはコミュニティから[支持を得ます](/support.md) .

</CustomContent>

<CustomContent platform="tidb-cloud">

> **警告：**
>
> -   ベースラインの進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境で使用することは**お**勧めしません。
> -   この変数は、ベースライン進化機能が一般に利用可能 (GA) になるまで、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。この機能を本番環境ですでに使用している場合は、できるだけ早く無効にしてください。バインド ステータスが期待どおりではないことがわかった場合は、 [TiDB Cloudサポートに連絡する](/tidb-cloud/tidb-cloud-support.md) .

</CustomContent>

自動バインディング進化機能が有効になった後、オプティマイザによって選択された最適な実行計画がバインディング実行計画に含まれていない場合、オプティマイザはその計画を検証を待つ実行計画としてマークします。 `bind-info-lease` (デフォルト値は`3s` ) 間隔ごとに、検証する実行計画が選択され、実際の実行時間に関して最小のコストを持つバインディング実行計画と比較されます。検証対象の計画の実行時間が短い場合 (現在の比較基準は、検証対象の計画の実行時間が拘束力のある実行計画の実行時間の 2/3 を超えないことです)、この計画は使用可能としてマークされます。バインディング。次の例では、上記のプロセスについて説明します。

表`t`が次のように定義されているとします。

{{< copyable "" >}}

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

テーブル`t`に対して次のクエリを実行します。

{{< copyable "" >}}

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

上で定義した表では、 `a < 100`条件を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザーは、インデックス`a`を使用する最適な実行計画ではなく、誤って全テーブル スキャンを選択します。まず、次のステートメントを使用してバインディングを作成できます。

{{< copyable "" >}}

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 using SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

上記のクエリが再度実行されると、オプティマイザーはクエリ時間を短縮するためにインデックス`a` (上記で作成されたバインディングの影響を受ける) を選択します。

テーブル`t`で挿入と削除が実行されると、条件`a < 100`満たす行数が増加し、条件`b < 100`満たす行数が減少するとします。現時点では、バインディングでインデックス`a`を使用することは、最適な計画ではない可能性があります。

バインディングの進化は、この種の問題に対処できます。オプティマイザーは、テーブル内のデータの変更を認識すると、インデックス`b`を使用するクエリの実行プランを生成します。ただし、現在のプランのバインドが存在するため、このクエリ プランは採用されず、実行されません。代わりに、この計画はバックエンド進化リストに保存されます。展開プロセス中に、この計画がインデックス`a`を使用する現在の実行計画よりも明らかに短い実行時間であることが確認された場合、インデックス`b`が使用可能なバインディング リストに追加されます。この後、クエリが再度実行されると、オプティマイザーは最初にインデックス`b`を使用する実行プランを生成し、このプランがバインディング リストに含まれていることを確認します。次に、オプティマイザーはこの計画を採用して実行し、データ変更後のクエリ時間を短縮します。

自動進化がクラスターに与える影響を軽減するには、次の構成を使用します。

-   各実行計画の最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は`600s`です。実際の検証プロセスでは、最大実行時間も、検証済みの実行計画の時間の 2 倍を超えないように制限されます。
-   時間枠を制限するには、 `tidb_evolve_plan_task_start_time` (デフォルトでは`00:00 +0000` ) と`tidb_evolve_plan_task_end_time` (デフォルトでは`23:59 +0000` ) を設定します。

### ノート {#notes}

ベースラインの進化によって新しいバインディングが自動的に作成されるため、クエリ環境が変化すると、自動的に作成されたバインディングに複数の動作の選択肢が生じる場合があります。次の注意事項に注意してください。

-   ベースラインの進化は、少なくとも 1 つのグローバル バインディングを持つ標準化された SQL ステートメントのみを進化させます。

-   新しいバインディングを作成すると以前のすべてのバインディングが削除されるため (標準化された SQL ステートメントの場合)、新しいバインディングを手動で作成すると、自動的に展開されたバインディングが削除されます。

-   計算プロセスに関連するすべてのヒントは、進化中に保持されます。これらのヒントは次のとおりです。

    | ヒント                       | 説明                                                   |
    | :------------------------ | :--------------------------------------------------- |
    | `memory_quota`            | クエリに使用できる最大メモリ。                                      |
    | `use_toja`                | オプティマイザーがサブクエリを Join に変換するかどうか。                      |
    | `use_cascades`            | カスケード オプティマイザを使用するかどうか。                              |
    | `no_index_merge`          | オプティマイザーがテーブルを読み取るためのオプションとして Index Merge を使用するかどうか。 |
    | `read_consistent_replica` | テーブルの読み取り時に強制的にFollower Readを有効にするかどうか。              |
    | `max_execution_time`      | クエリの最長期間。                                            |

-   `read_from_storage`テーブルを読み取るときに TiKV からデータを読み取るか、 TiFlashからデータを読み取るかを指定するという点で、特別なヒントです。 TiDB は分離読み取りを提供するため、分離条件が変更された場合、このヒントは進化した実行計画に大きな影響を与えます。したがって、このヒントが最初に作成されたバインディングに存在する場合、TiDB はすべての進化したバインディングを無視します。

## アップグレードのチェックリスト {#upgrade-checklist}

クラスターのアップグレード中に、SQL Plan Management (SPM) が互換性の問題を引き起こし、アップグレードが失敗する可能性があります。アップグレードを確実に成功させるには、アップグレードの事前チェックに次のリストを含める必要があります。

-   v5.2.0 より前のバージョン (つまり、v4.0、v5.0、および v5.1) から現在のバージョンにアップグレードする場合は、アップグレードの前に`tidb_evolve_plan_baselines`が無効になっていることを確認してください。この変数を無効にするには、次の手順を実行します。

    {{< copyable "" >}}

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version.

    SELECT @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it.

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   v4.0 から現在のバージョンにアップグレードする前に、使用可能な SQL バインディングに対応するすべてのクエリの構文が新しいバージョンで正しいかどうかを確認する必要があります。構文エラーが存在する場合は、対応する SQL バインディングを削除します。これを行うには、次の手順を実行します。

    {{< copyable "" >}}

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

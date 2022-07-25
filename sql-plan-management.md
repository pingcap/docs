---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
---

# SQL計画管理（SPM） {#sql-plan-management-spm}

SQLプラン管理は、SQLバインディングを実行して、SQL実行プランに手動で干渉する一連の関数です。これらの関数には、SQLバインディング、ベースラインキャプチャ、およびベースライン進化が含まれます。

## SQLバインディング {#sql-binding}

SQLバインディングはSPMの基礎です。 [オプティマイザーのヒント](/optimizer-hints.md)のドキュメントでは、ヒントを使用して特定の実行プランを選択する方法を紹介しています。ただし、SQLステートメントを変更せずに実行の選択を妨害する必要がある場合があります。 SQLバインディングを使用すると、SQLステートメントを変更せずに指定された実行プランを選択できます。

### バインディングを作成する {#create-a-binding}

{{< copyable "" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

このステートメントは、SQL実行プランをGLOBALまたはSESSIONレベルでバインドします。現在、 `SELECT` `DELETE` `SELECT` `INSERT` `REPLACE`れて`UPDATE`ます。

> **ノート：**
>
> バインディングは、手動で追加されたヒントよりも優先されます。したがって、対応するバインディングが存在するときにヒントを含むステートメントを実行すると、オプティマイザーの動作を制御するヒントは有効になりません。ただし、他の種類のヒントは引き続き有効です。

具体的には、構文の競合のため、これらのステートメントの2つのタイプを実行プランにバインドすることはできません。次の例を参照してください。

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

同等のステートメントを使用することで、構文の競合を回避できます。たとえば、上記のステートメントを次のように書き直すことができます。

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
> `SELECT` `REPLACE`サブクエリを含む`INSERT`ステートメントの実行プランバインディングを作成する場合、 `INSERT` / `REPLACE`キーワードの後ではなく、 `SELECT`サブクエリでバインドするオプティマイザヒントを指定する必要があります。そうしないと、オプティマイザのヒントが意図したとおりに有効になりません。

次に2つの例を示します。

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

実行プランバインディングを作成するときにスコープを指定しない場合、デフォルトのスコープはSESSIONです。 TiDBオプティマイザは、バインドされたSQLステートメントを正規化し、それらをシステムテーブルに格納します。 SQLクエリを処理するときに、正規化されたステートメントがシステムテーブル内のバインドされたSQLステートメントの1つと一致し、システム変数`tidb_use_plan_baselines`が`on` （デフォルト値は`on` ）に設定されている場合、TiDBはこのステートメントに対応するオプティマイザーヒントを使用します。一致する実行プランが複数ある場合、オプティマイザーはバインドするのに最もコストのかからないプランを選択します。

`Normalization`は、SQLステートメントの定数を変数パラメーターに変換し、クエリで参照されるテーブルのデータベースを明示的に指定するプロセスです。SQLステートメントのスペースと改行の処理は標準化されています。次の例を参照してください。

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
> バインディングが作成されると、TiDBは、単一の定数を含むSQLステートメントと、コンマで結合された複数の定数を含むSQLステートメントを異なる方法で処理します。したがって、2つのSQLタイプのバインディングを別々に作成する必要があります。

SQLステートメントにGLOBALスコープとSESSIONスコープの両方で実行プランがバインドされている場合、オプティマイザーはSESSIONバインディングに遭遇すると、GLOBALスコープでバインドされた実行プランを無視するため、SESSIONスコープでのこのステートメントのバインドされた実行プランは、 GLOBALスコープ。

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

最初の`SELECT`ステートメントが実行されているとき、オプティマイザーはGLOBALスコープのバインディングを介してステートメントに`sm_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行プランの最上位ノードはMergeJoinです。 2番目の`SELECT`ステートメントが実行されているとき、オプティマイザーはGLOBALスコープのバインディングの代わりにSESSIONスコープのバインディングを使用し、ステートメントに`hash_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行プランの最上位ノードはHashJoinです。

標準化された各SQLステートメントは、一度に`CREATE BINDING`つを使用して作成されたバインディングを1つだけ持つことができます。同じ標準化されたSQLステートメントに対して複数のバインディングが作成されると、最後に作成されたバインディングが保持され、以前のすべてのバインディング（作成および展開）は削除済みとしてマークされます。ただし、セッションバインディングとグローバルバインディングは共存でき、このロジックの影響を受けません。

さらに、バインディングを作成する場合、TiDBではセッションがデータベースコンテキストにある必要があります。つまり、クライアントが接続されたとき、または`use ${database}`が実行されたときにデータベースが指定されます。

元のSQLステートメントとバインドされたステートメントは、正規化とヒントの削除後に同じテキストである必要があります。そうでない場合、バインドは失敗します。次の例を見てください。

-   パラメータ化とヒントの削除の前後のテキストが同じであるため、このバインディングは正常に作成できます`SELECT * FROM test . t WHERE a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   元のSQLステートメントは`SELECT * FROM test . t WHERE a > ?`として処理されるのに対し、バインドされたSQLステートメントは`SELECT * FROM test . t WHERE b > ?`として処理されるため、このバインドは失敗します。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **ノート：**
>
> `PREPARE`ステートメントおよびバイナリプロトコルで実行されるクエリの場合、 `EXECUTE` / `PREPARE`ステートメントではなく、実際のクエリステートメントの実行プランバインディングを作成する必要があり`EXECUTE` 。

### バインディングを削除します {#remove-binding}

{{< copyable "" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

このステートメントは、GLOBALまたはSESSIONレベルで指定された実行プランバインディングを削除します。デフォルトのスコープはSESSIONです。

一般に、SESSIONスコープのバインディングは、主にテストまたは特別な状況で使用されます。バインディングをすべてのTiDBプロセスで有効にするには、GLOBALバインディングを使用する必要があります。作成されたSESSIONバインディングは、セッションが閉じる前にSESSIONバインディングがドロップされた場合でも、SESSIONが終了するまで対応するGLOBALバインディングをシールドします。この場合、バインディングは有効にならず、プランはオプティマイザーによって選択されます。

次の例は、SESSIONバインディングがGLOBALバインディングをシールドする[バインディングを作成する](#create-a-binding)の例に基づいています。

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for SELECT * FROM t1, t2 WHERE t1.id = t2.id;

-- Views the SQL execution plan again.
explain SELECT * FROM t1,t2 WHERE t1.id = t2.id;
```

上記の例では、SESSIONスコープ内のドロップされたバインディングは、GLOBALスコープ内の対応するバインディングをシールドします。オプティマイザは、ステートメントに`sm_join(t1, t2)`のヒントを追加しません。 `explain`の結果の実行プランの最上位ノードは、このヒントによってMergeJoinに固定されていません。代わりに、コスト見積もりに従って、オプティマイザによって最上位ノードが個別に選択されます。

> **ノート：**
>
> `DROP GLOBAL BINDING`を実行すると、現在のtidb-serverインスタンスキャッシュのバインディングが削除され、システムテーブルの対応する行のステータスが「削除済み」に変更されます。他のtidb-serverインスタンスは、対応するバインディングをキャッシュにドロップするために「削除済み」ステータスを読み取る必要があるため、このステートメントはシステムテーブルのレコードを直接削除しません。ステータスが「削除済み」のこれらのシステムテーブルのレコードの場合、100 `bind-info-lease` （デフォルト値は`3s` 、合計`300s` ）間隔ごとに、バックグラウンドスレッドが10より前の`update_time`のバインディングを再利用およびクリアする操作をトリガーします。 `bind-info-lease` （すべてのtidb-serverインスタンスが「削除済み」ステータスを読み取り、キャッシュを更新したことを確認するため）。

## バインディングステータスの変更 {#change-binding-status}

{{< copyable "" >}}

```sql
SET BINDING [ENABLED | DISABLED] FOR BindableStmt;
```

このステートメントを実行して、バインディングのステータスを変更できます。デフォルトのステータスはENABLEDです。有効なスコープはデフォルトでGLOBALであり、変更できません。

このステートメントを実行するときは、バインディングのステータスを`Disabled`から`Enabled`または`Enabled`から`Disabled`にのみ変更できます。ステータス変更に使用できるバインディングがない場合は、 `There are no bindings can be set the status. Please check the SQL text`という警告メッセージが返されます。 `Disabled`ステータスのバインディングは、どのクエリでも使用されないことに注意してください。

### バインディングをビューする {#view-bindings}

{{< copyable "" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

このステートメントは、実行プランのバインディングを、最新から最早までのバインディング更新時間の順序に従って、GLOBALレベルまたはSESSIONレベルで出力します。デフォルトのスコープはSESSIONです。現在、以下に示すように、 `SHOW BINDINGS`は8つの列を出力します。

| カラム名         | ノート                                                                                                                                              |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| original_sql | パラメータ化後の元のSQLステートメント                                                                                                                             |
| bind_sql     | ヒント付きのバインドされたSQLステートメント                                                                                                                          |
| default_db   | デフォルトのデータベース                                                                                                                                     |
| 状態           | 有効（v6.0の使用ステータスを置き換える）、無効、削除、無効、拒否、保留中の検証を含むステータス                                                                                                |
| create_time  | 時間を作る                                                                                                                                            |
| update_time  | 更新時間                                                                                                                                             |
| 文字コード        | キャラクターセット                                                                                                                                        |
| 照合順序         | 注文ルール                                                                                                                                            |
| ソース          | `manual` （ `create [global] binding` SQLステートメントによって作成される）、 `capture` （TiDBによって自動的にキャプチャーされる）、および`evolve` （TiDBによって自動的に展開される）を含む、バインディングが作成される方法。 |

### バインディングのトラブルシューティング {#troubleshoot-a-binding}

次のいずれかの方法を使用して、バインディングのトラブルシューティングを行うことができます。

-   システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)を使用して、最後に実行されたステートメントで使用された実行プランがバインディングからのものであるかどうかを示します。

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

-   `explain format = 'verbose'`ステートメントを使用して、SQLステートメントのクエリプランを表示します。 SQLステートメントがバインディングを使用している場合は、 `show warnings`を実行して、SQLステートメントで使用されているバインディングを確認できます。

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

各TiDBインスタンスには、バインディングに使用頻度が最も低い（LRU）キャッシュがあります。キャッシュ容量は、システム変数[`tidb_mem_quota_binding_cache`](/system-variables.md#tidb_mem_quota_binding_cache-new-in-v600)によって制御されます。 TiDBインスタンスにキャッシュされているバインディングを表示できます。

バインディングのキャッシュステータスを表示するには、 `SHOW binding_cache status`ステートメントを実行します。このステートメントでは、有効なスコープはデフォルトでGLOBALであり、変更できません。このステートメントは、キャッシュで使用可能なバインディングの数、システムで使用可能なバインディングの総数、キャッシュされたすべてのバインディングのメモリ使用量、およびキャッシュの合計メモリを返します。

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

## ベースラインキャプチャ {#baseline-capturing}

[アップグレード中の実行プランのリグレッションの防止](#prevent-regression-of-execution-plans-during-an-upgrade)に使用されるこの機能は、キャプチャ条件を満たすクエリをキャプチャし、これらのクエリのバインディングを作成します。

### キャプチャを有効にする {#enable-capturing}

ベースラインキャプチャを有効にするには、 `tidb_capture_plan_baselines`を設定し`on` 。デフォルト値は`off`です。

> **ノート：**
>
> 自動バインディング作成機能は[ステートメントの要約](/statement-summary-tables.md)に依存しているため、自動バインディングを使用する前に、必ずステートメントの概要を有効にしてください。

自動バインディング作成を有効にすると、ステートメントの概要の履歴SQLステートメントが`bind-info-lease`ごとにトラバースされ（デフォルト値は`3s` ）、少なくとも2回出現するSQLステートメントのバインディングが自動的に作成されます。これらのSQLステートメントの場合、TiDBはステートメントの概要に記録されている実行プランを自動的にバインドします。

ただし、TiDBは、次のタイプのSQLステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`および`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`クエリなど、TiDBの内部で実行されるSQLステートメント。
-   `Enabled`つまたは`Disabled`のバインディングを含むステートメント。
-   条件をキャプチャすることによって除外されるステートメント。

> **ノート：**
>
> 現在、バインディングは、クエリステートメントによって生成された実行プランを修正するためのヒントのグループを生成します。このように、同じクエリに対して、実行プランは変更されません。同じインデックスまたは結合アルゴリズム（HashJoinやIndexJoinなど）を使用するクエリを含むほとんどのOLTPクエリでは、TiDBはバインディングの前後でプランの一貫性を保証します。ただし、ヒントの制限により、TiDBは、3つ以上のテーブルの結合、MPPクエリ、複雑なOLAPクエリなど、一部の複雑なクエリのプランの整合性を保証できません。

`PREPARE`ステートメントおよびバイナリプロトコルで実行されるクエリの場合、 `EXECUTE` `EXECUTE` `PREPARE`はなく、実際のクエリステートメントのバインディングを自動的にキャプチャします。

> **ノート：**
>
> TiDBにはいくつかの機能の正確さを保証するためにいくつかの埋め込みSQLステートメントがあるため、ベースラインキャプチャはデフォルトでこれらのSQLステートメントを自動的にシールドします。

### バインディングを除外する {#filter-out-bindings}

この機能を使用すると、ブロックリストを構成して、バインディングをキャプチャしたくないクエリを除外できます。ブロックリストには、テーブル名、頻度、およびユーザー名の3つのディメンションがあります。

#### 使用法 {#usage}

フィルタリング条件をシステムテーブル`mysql.capture_plan_baselines_blacklist`に挿入します。その後、フィルタリング条件はクラスタ全体ですぐに有効になります。

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

| **寸法名** | **説明**                                                                                                                                                                                                                           | 備考                                                                                                                                           |
| :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| テーブル    | テーブル名でフィルタリングします。各フィルタリングルールは`db.table`形式です。サポートされているフィルタリング構文には、 [プレーンテーブル名](https://docs.pingcap.com/tidb/stable/table-filter#plain-table-names)と[ワイルドカード](https://docs.pingcap.com/tidb/stable/table-filter#wildcards)が含まれます。 | 大文字小文字を区別しません。テーブル名に不正な文字が含まれている場合、ログは警告メッセージ`[sql-bind] failed to load mysql.capture_plan_baselines_blacklist`を返します。                        |
| 周波数     | 周波数でフィルタリングします。複数回実行されたSQLステートメントは、デフォルトでキャプチャされます。頻繁に実行されるステートメントをキャプチャするように高頻度を設定できます。                                                                                                                                         | 頻度を1より小さい値に設定すると、違法と見なされ、ログは警告メッセージ`[sql-bind] frequency threshold is less than 1, ignore it`を返します。複数の頻度フィルタールールが挿入されている場合は、頻度が最も高い値が優先されます。 |
| ユーザー    | ユーザー名でフィルタリングします。ブロックリストに登録されたユーザーによって実行されたステートメントはキャプチャされません。                                                                                                                                                                   | 複数のユーザーが同じステートメントを実行し、それらのユーザー名がすべてブロックリストに含まれている場合、このステートメントはキャプチャされません。                                                                    |

> **ノート：**
>
> -   ブロックリストを変更するには、スーパー特権が必要です。
>
> -   ブロックリストに不正なフィルターが含まれている場合、TiDBはログに警告メッセージ`[sql-bind] unknown capture filter type, ignore it`を返します。

### アップグレード中の実行プランのリグレッションを防止します {#prevent-regression-of-execution-plans-during-an-upgrade}

TiDBクラスタをアップグレードする前に、ベースラインキャプチャを使用して、次の手順を実行することにより、実行プランのリグレッションを防ぐことができます。

1.  ベースラインキャプチャを有効にして、機能し続けます。

    > **ノート：**
    >
    > テストデータは、ベースラインキャプチャの長期的な動作が、クラスタ負荷のパフォーマンスにわずかな影響を与えることを示しています。したがって、重要な計画（2回以上表示される）がキャプチャされるように、ベースラインキャプチャをできるだけ長く有効にすることをお勧めします。

2.  TiDBクラスタをアップグレードします。アップグレード後、TiDBはこれらのキャプチャされたバインディングを使用して、実行プランの一貫性を確保します。

3.  アップグレード後、必要に応じてバインディングを削除します。

    -   [`SHOW GLOBAL BINDINGS`](#view-bindings)ステートメントを実行して、バインディングソースを確認します。

        出力で、 `Source`フィールドをチェックして、バインディングがキャプチャされているか（ `capture` ）、手動で作成されているか（ `manual` ）を確認します。

    -   キャプチャされたバインディングを保持するかどうかを決定します。

        ```
        -- View the plan with the binding enabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = true;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;

        -- View the plan with the binding disabled
        SET @@SESSION.TIDB_USE_PLAN_BASELINES = false;
        EXPLAIN FORMAT='VERBOSE' SELECT * FROM t1 WHERE ...;
        ```

        -   実行プランに一貫性がある場合は、バインディングを安全に削除できます。

        -   実行プランに一貫性がない場合は、統計を確認するなどして原因を特定する必要があります。この場合、プランの一貫性を確保するためにバインディングを保持する必要があります。

## ベースラインの進化 {#baseline-evolution}

ベースラインの進化は、TiDBv4.0で導入されたSPMの重要な機能です。

データが更新されると、以前にバインドされた実行プランが最適でなくなる可能性があります。ベースライン進化機能は、バインドされた実行プランを自動的に最適化できます。

さらに、ベースラインの進化は、統計情報の変更によって引き起こされる実行プランにもたらされるジッターをある程度回避することもできます。

### 使用法 {#usage}

次のステートメントを使用して、自動バインディング展開を有効にします。

{{< copyable "" >}}

```sql
SET GLOBAL tidb_evolve_plan_baselines = ON;
```

デフォルト値の`tidb_evolve_plan_baselines`は`off`です。

> **警告：**
>
> -   ベースラインの進化は実験的特徴です。未知のリスクが存在する可能性があります。実稼働環境で使用することはお勧めし**ません**。
> -   この変数は、ベースライン進化機能が一般に利用可能になるまで（GA）、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。この機能を実稼働環境ですでに使用している場合は、できるだけ早く無効にしてください。バインディングステータスが期待どおりでない場合は、PingCAPのテクニカルサポートに問い合わせてください。

自動バインディング展開機能を有効にした後、オプティマイザーによって選択された最適な実行プランがバインディング実行プランに含まれていない場合、オプティマイザーはそのプランを検証を待機する実行プランとしてマークします。 `bind-info-lease` （デフォルト値は`3s` ）間隔ごとに、検証する実行プランが選択され、実際の実行時間の点でコストが最も低いバインディング実行プランと比較されます。検証対象のプランの実行時間が短い場合（現在の比較基準では、検証対象のプランの実行時間がバインディング実行プランの実行時間の2/3以下である）、このプランは使用可能としてマークされます。バインディング。次の例では、上記のプロセスについて説明します。

表`t`が次のように定義されていると仮定します。

{{< copyable "" >}}

```sql
CREATE TABLE t(a INT, b INT, KEY(a), KEY(b));
```

表`t`に対して次のクエリを実行します。

{{< copyable "" >}}

```sql
SELECT * FROM t WHERE a < 100 AND b < 100;
```

上で定義されたテーブルでは、 `a < 100`の条件を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザは、インデックス`a`を使用する最適な実行プランではなく、誤って全表スキャンを選択します。最初に次のステートメントを使用してバインディングを作成できます。

{{< copyable "" >}}

```sql
CREATE GLOBAL BINDING for SELECT * FROM t WHERE a < 100 AND b < 100 using SELECT * FROM t use index(a) WHERE a < 100 AND b < 100;
```

上記のクエリが再度実行されると、オプティマイザはインデックス`a` （上記で作成されたバインディングの影響を受けます）を選択して、クエリ時間を短縮します。

表`t`で挿入と削除が実行されると、 `a < 100`の条件を満たす行の数が増え、 `b < 100`の条件を満たす行の数が減ると仮定します。現時点では、バインディングの下でインデックス`a`を使用することは、もはや最適な計画ではない可能性があります。

拘束力のある進化は、この種の問題に対処することができます。オプティマイザは、テーブル内のデータの変更を認識すると、インデックス`b`を使用するクエリの実行プランを生成します。ただし、現在のプランのバインディングが存在するため、このクエリプランは採用および実行されません。代わりに、このプランはバックエンドの進化リストに保存されます。展開プロセス中に、このプランの実行時間が、インデックス`a`を使用する現在の実行プランよりも明らかに短いことが確認された場合、インデックス`b`が使用可能なバインディングリストに追加されます。この後、クエリが再度実行されると、オプティマイザは最初にインデックス`b`を使用する実行プランを生成し、このプランがバインディングリストに含まれていることを確認します。次に、オプティマイザーはこのプランを採用して実行し、データ変更後のクエリ時間を短縮します。

自動進化がクラスターに与える影響を減らすには、次の構成を使用します。

-   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は`600s`です。実際の検証プロセスでは、最大実行時間も検証された実行プランの2倍以下に制限されます。
-   時間枠を制限するには、 `tidb_evolve_plan_task_start_time` （デフォルトでは`00:00 +0000` ）と`tidb_evolve_plan_task_end_time` （デフォルトでは`23:59 +0000` ）を設定します。

### ノート {#notes}

ベースラインの進化により新しいバインディングが自動的に作成されるため、クエリ環境が変更されると、自動的に作成されたバインディングには複数の動作の選択肢がある場合があります。次の注意事項に注意してください。

-   ベースラインの進化は、少なくとも1つのグローバルバインディングを持つ標準化されたSQLステートメントのみを進化させます。

-   新しいバインディングを作成すると、以前のすべてのバインディングが削除されるため（標準化されたSQLステートメントの場合）、新しいバインディングを手動で作成した後、自動的に展開されたバインディングが削除されます。

-   計算プロセスに関連するすべてのヒントは、進化中に保持されます。これらのヒントは次のとおりです。

    | ヒント                       | 説明                                              |
    | :------------------------ | :---------------------------------------------- |
    | `memory_quota`            | クエリに使用できる最大メモリ。                                 |
    | `use_toja`                | オプティマイザがサブクエリをJoinに変換するかどうか。                    |
    | `use_cascades`            | カスケードオプティマイザを使用するかどうか。                          |
    | `no_index_merge`          | オプティマイザがテーブルを読み取るためのオプションとしてインデックスマージを使用するかどうか。 |
    | `read_consistent_replica` | テーブルの読み取り時にフォロワー読み取りを強制的に有効にするかどうか。             |
    | `max_execution_time`      | クエリの最長期間。                                       |

-   `read_from_storage`は、テーブルを読み取るときにTiKVからデータを読み取るかTiFlashからデータを読み取るかを指定するという点で特別なヒントです。 TiDBは分離読み取りを提供するため、分離条件が変更されると、このヒントは進化した実行プランに大きな影響を与えます。したがって、このヒントが最初に作成されたバインディングに存在する場合、TiDBはその進化したバインディングをすべて無視します。

## アップグレードチェックリスト {#upgrade-checklist}

クラスタのアップグレード中に、SQL Plan Management（SPM）によって互換性の問題が発生し、アップグレードが失敗する場合があります。アップグレードを成功させるには、アップグレードの事前チェックのために次のリストを含める必要があります。

-   v5.2.0より前のバージョン（つまり、v4.0、v5.0、およびv5.1）から現在のバージョンにアップグレードする場合は、アップグレードする前に`tidb_evolve_plan_baselines`が無効になっていることを確認してください。この変数を無効にするには、次の手順を実行します。

    {{< copyable "" >}}

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version.

    SELECT @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it.

    SET GLOBAL tidb_evolve_plan_baselines = OFF;
    ```

-   v4.0から現在のバージョンにアップグレードする前に、使用可能なSQLバインディングに対応するすべてのクエリの構文が新しいバージョンで正しいかどうかを確認する必要があります。構文エラーが存在する場合は、対応するSQLバインディングを削除します。これを行うには、次の手順を実行します。

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

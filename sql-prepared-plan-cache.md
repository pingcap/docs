---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
---

# SQL準備実行プランキャッシュ {#sql-prepare-execution-plan-cache}

TiDBは、 `Prepare`および`Execute`のクエリの実行プランキャッシュをサポートします。これには、準備されたステートメントの両方の形式が含まれます。

-   `COM_STMT_PREPARE`および`COM_STMT_EXECUTE`プロトコル機能を使用します。
-   SQLステートメント`PREPARE`および`EXECUTE`の使用。

TiDBオプティマイザーは、これら2つのタイプのクエリを同じ方法で処理します。準備時に、パラメーター化されたクエリがAST（抽象構文ツリー）に解析され、キャッシュされます。後の実行では、保存されたASTと特定のパラメータ値に基づいて実行プランが生成されます。

実行プランキャッシュが有効になっている場合、最初の実行で`Prepare`ステートメントごとに、現在のクエリが実行プランキャッシュを使用できるかどうかを確認し、クエリがそれを使用できる場合は、生成された実行プランをLRUによって実装されたキャッシュに配置します（最近使用済み）リンクリスト。後続の`Execute`のクエリでは、実行プランがキャッシュから取得され、可用性がチェックされます。チェックが成功した場合、実行プランを生成するステップはスキップされます。それ以外の場合、実行プランは再生成され、キャッシュに保存されます。

現在のバージョンのTiDBでは、 `Prepare`のステートメントが次の条件のいずれかを満たしている場合、クエリまたはプランはキャッシュされません。

-   `Union`には、 `SELECT` 、および`UPDATE` `Except`のSQL `Intersect`が含まれて`INSERT` `DELETE` 。
-   クエリは、パーティションテーブルまたは一時テーブル、あるいは生成された列を含むテーブルにアクセスします。
-   クエリには、 `select * from t where a > (select ...)`などのサブクエリが含まれています。
-   クエリには、 `select /*+ ignore_plan_cache() */ * from t`などの`ignore_plan_cache`のヒントが含まれています。
-   クエリには、 `select * from t where a>? and b>@x`などの`?`以外の変数（システム変数またはユーザー定義変数を含む）が含まれています。
-   `row_count`には、キャッシュできない関数が`version`れて`current_role` `current_user` `last_insert_id` `database()` `like` `connection_id` `user` 。
-   クエリには、 `Limit ?`や`Limit 10, ?`など、 `Limit`の後に`?`が含まれます。 `?`の特定の値はクエリのパフォーマンスに大きな影響を与えるため、このようなクエリはキャッシュされません。
-   クエリには、 `Order By ?`などの`Order By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータを並べ替えます。異なる列を対象とするクエリが同じ実行プランを使用している場合、結果は正しくありません。したがって、このようなクエリはキャッシュされません。ただし、クエリが`Order By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには、 `Group By?`などの`Group By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列を対象とするクエリが同じ実行プランを使用している場合、結果は正しくありません。したがって、このようなクエリはキャッシュされません。ただし、クエリが`Group By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには、 `(partition by year order by sale rows ? preceding)`などの`Window Frame`ウィンドウ関数の定義に`?`が含まれています。ウィンドウ関数の他の場所に`?`が表示されている場合、クエリはキャッシュされます。
-   クエリには、 `c_int >= ?`や`c_int in (?, ?)`などの`int`と`string`を比較するためのパラメータが含まれています。ここで、 `?`は`set @x='123'`などの文字列型を示します。クエリ結果がMySQLと互換性があることを確認するには、各クエリでパラメータを調整して、そのようなクエリがキャッシュされないようにする必要があります。
-   プランは`TiFlash`にアクセスしようとします。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメーターがない場合を除き、 `TableDual`を含むプランはキャッシュされません。

`Prepare`はセッション間で実行できないため、LRUリンクリストはセッションレベルのキャッシュとして設計されてい`Execute` 。 LRUリストの各要素は、キーと値のペアです。値は実行プランであり、キーは次の部分で構成されています。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`ステートメントのID、つまり`PREPARE`キーワードの後の名前
-   現在のスキーマバージョン。これは、DDLステートメントが正常に実行されるたびに更新されます。
-   `Execute`実行時のSQLモード
-   `time_zone`のシステム変数の値である現在のタイムゾーン
-   `sql_select_limit`のシステム変数の値

上記の情報の変更（たとえば、データベースの切り替え、 `Prepare`ステートメントの名前変更、DDLステートメントの実行、SQLモード/ `time_zone`の値の変更）、またはLRUキャッシュ除去メカニズムにより、実行時に実行プランのキャッシュミスが発生します。

実行プランキャッシュがキャッシュから取得された後、TiDBは最初に実行プランがまだ有効かどうかをチェックします。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照されたテーブルがトランザクションの事前注文ステートメントで変更された場合、このテーブルにアクセスするキャッシュされた実行プランに`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行プランのスキャン範囲が現在のパラメータ値に従って調整され、データクエリの実行に使用されます。

実行プランのキャッシュとクエリのパフォーマンスについては、注目に値するいくつかのポイントがあります。

-   実行プランがキャッシュされているかどうかに関係なく、SQLバインディングの影響を受けます。キャッシュされていない実行プラン（最初の`Execute` ）の場合、これらのプランは既存のSQLバインディングの影響を受けます。キャッシュされた実行プランの場合、新しいSQLバインディングが作成されると、これらのプランは無効になります。
-   キャッシュされたプランは、統計、最適化ルール、および式によるブロックリストのプッシュダウンの変更による影響を受けません。
-   `Execute`のパラメーターが異なることを考慮すると、実行プランキャッシュは、適応性を確保するために特定のパラメーター値に密接に関連するいくつかの積極的なクエリ最適化メソッドを禁止します。これにより、クエリプランが特定のパラメータ値に対して最適でない場合があります。たとえば、クエリのフィルター条件は`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメーターはそれぞれ`2`と`1`です。これらの2つのパラメーターが次の実行時に`1`と`2`になる可能性があることを考慮すると、オプティマイザーは現在のパラメーター値に固有の最適`TableDual`実行プランを生成しません。
-   キャッシュの無効化と削除が考慮されていない場合、実行プランキャッシュはさまざまなパラメータ値に適用され、理論的には特定の値に対して最適でない実行プランが発生します。たとえば、フィルター条件が`where a < ?`で、最初の実行に使用されるパラメーター値が`1`の場合、オプティマイザーは最適な`IndexScan`実行プランを生成し、それをキャッシュに入れます。その後の実行で、値が`10000`になった場合は、 `TableScan`プランの方が適している可能性があります。ただし、実行プランキャッシュのため、以前に生成された`IndexScan`が実行に使用されます。したがって、実行プランキャッシュは、クエリが単純で（コンパイルの比率が高い）、実行プランが比較的固定されているアプリケーションシナリオに適しています。

v6.1.0以降、実行プランキャッシュはデフォルトで有効になっています。準備された計画キャッシュは、システム変数[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を介して制御できます。

> **ノート：**
>
> 実行プランのキャッシュ機能は、 `Prepare` / `Execute`クエリにのみ適用され、通常のクエリでは有効になりません。

実行プランのキャッシュ機能を有効にした後、セッションレベルのシステム変数`last_plan_from_cache`を使用して、前の`Execute`のステートメントがキャッシュされた実行プランを使用したかどうかを確認できます。次に例を示します。

{{< copyable "" >}}

```sql
MySQL [test]> create table t(a int);
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> prepare stmt from 'select * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)

-- The first execution generates an execution plan and saves it in the cache.
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)

-- The second execution hits the cache.
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 1                      |
+------------------------+
1 row in set (0.00 sec)
```

実行プランキャッシュが原因で`Prepare`の特定のセットに予期しない動作が見られる場合は、 `Execute` SQLヒントを使用して、現在のステートメントの実行プランキャッシュの使用をスキップでき`ignore_plan_cache()` 。それでも、例として上記のステートメントを使用してください。

{{< copyable "" >}}

```sql
MySQL [test]> prepare stmt from 'select /*+ ignore_plan_cache() */ * from t where a = ?';
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> set @a = 1;
Query OK, 0 rows affected (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
MySQL [test]> execute stmt using @a;
Empty set (0.00 sec)
MySQL [test]> select @@last_plan_from_cache;
+------------------------+
| @@last_plan_from_cache |
+------------------------+
| 0                      |
+------------------------+
1 row in set (0.00 sec)
```

## プリペアドプランキャッシュのメモリ管理 {#memory-management-of-prepared-plan-cache}

プリペアドプランキャッシュを使用すると、メモリのオーバーヘッドが発生します。内部テストでは、キャッシュされた各プランは平均100KiBのメモリを消費します。プランキャッシュは現在`SESSION`レベルであるため、合計メモリ消費量は約`the number of sessions * the average number of cached plans in a session * 100 KiB`です。

たとえば、現在のTiDBインスタンスには50の同時実行セッションがあり、各セッションには約100のキャッシュされたプランがあります。合計メモリ消費量は約`50 * 100 * 100 KiB` = `512 MB`です。

システム変数`tidb_prepared_plan_cache_size`を構成することにより、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりです。

-   TiDBサーバーインスタンスのメモリしきい値が&lt;=64GiBの場合、 `tidb_prepared_plan_cache_size`を`50`に設定します。
-   TiDBサーバーインスタンスのメモリしきい値が&gt;64GiBの場合、 `tidb_prepared_plan_cache_size`を`100`に設定します。

TiDBサーバーの未使用メモリが特定のしきい値未満になると、プランキャッシュのメモリ保護メカニズムがトリガーされ、キャッシュされたプランの一部が削除されます。

システム変数`tidb_prepared_plan_cache_memory_guard_ratio`を構成することにより、しきい値を制御できます。デフォルトのしきい値は0.1です。これは、TiDBサーバーの未使用メモリが合計メモリの10％未満（メモリの90％が使用されている）になると、メモリ保護メカニズムがトリガーされることを意味します。

<CustomContent platform="tidb">

メモリ制限により、プランキャッシュが失われる場合があります。 Grafanaダッシュボードで[`Plan Cache Miss OPS`メトリック](/grafana-tidb-dashboard.md)を表示すると、ステータスを確認できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

メモリ制限により、プランキャッシュが失われる場合があります。

</CustomContent>

## 実行プランのキャッシュをクリアする {#clear-execution-plan-cache}

`ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE`ステートメントを実行すると、実行プランのキャッシュをクリアできます。

このステートメントで、 `[SESSION | INSTANCE]`は、現在のセッションまたはTiDBインスタンス全体のプランキャッシュをクリアするかどうかを指定します。スコープが指定されていない場合、上記のステートメントはデフォルトで`SESSION`キャッシュに適用されます。

以下は、 `SESSION`の実行プランのキャッシュをクリアする例です。

{{< copyable "" >}}

```sql
MySQL [test]> create table t (a int);
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> prepare stmt from 'select * from t';
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- Select the cached plan
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)

MySQL [test]> admin flush session plan_cache; -- Clear the cached plan of the current session
Query OK, 0 rows affected (0.00 sec)

MySQL [test]> execute stmt;
Empty set (0.00 sec)

MySQL [test]> select @@last_plan_from_cache; -- The cached plan cannot be selected again, because it has been cleared
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      0 |
+------------------------+
1 row in set (0.00 sec)
```

現在、TiDBは`GLOBAL`の実行プランキャッシュのクリアをサポートしていません。つまり、TiDBクラスタ全体のキャッシュされたプランをクリアすることはできません。 `GLOBAL`実行プランのキャッシュをクリアしようとすると、次のエラーが報告されます。

{{< copyable "" >}}

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## <code>COM_STMT_CLOSE</code>コマンドとDEALLOCATEPREPAREステートメントを無視し<code>DEALLOCATE PREPARE</code> {#ignore-the-code-com-stmt-close-code-command-and-the-code-deallocate-prepare-code-statement}

SQLステートメントの構文解析コストを削減するために、 `deallocate prepare`を実行する前に`prepare stmt`回実行し、次に`execute stmt`回実行することをお勧めします。

{{< copyable "" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;  -- Execute once
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- Execute multiple times
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

実際には、以下に示すように、 `execute stmt`を実行した後、毎回`deallocate prepare`を実行することに慣れている場合があります。

{{< copyable "" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
MySQL [test]> prepare stmt from '...'; -- Prepare twice
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

このような場合、最初に実行されたステートメントによって取得されたプランは、2番目に実行されたステートメントによって再利用することはできません。

この問題に対処するには、システム変数を[`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)から`ON`に設定して、TiDBが`prepare stmt`を閉じるコマンドを無視するようにします。

{{< copyable "" >}}

```sql
mysql> set @@tidb_ignore_prepared_cache_close_stmt=1;  -- Enable the variable
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- Prepare once
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- Execute once
Empty set (0.00 sec)

mysql> deallocate prepare stmt;             -- Release after the first execute
Query OK, 0 rows affected (0.00 sec)

mysql> prepare stmt from 'select * from t'; -- Prepare twice
Query OK, 0 rows affected (0.00 sec)

mysql> execute stmt;                        -- Execute twice
Empty set (0.00 sec)

mysql> select @@last_plan_from_cache;       -- Reuse the last plan
+------------------------+
| @@last_plan_from_cache |
+------------------------+
|                      1 |
+------------------------+
1 row in set (0.00 sec)
```

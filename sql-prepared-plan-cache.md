---
title: SQL Prepared Execution Plan Cache
summary: TiDB の SQL 準備実行プラン キャッシュについて学習します。
---

# SQL 準備済み実行プラン キャッシュ {#sql-prepared-execution-plan-cache}

TiDB は、 `Prepare`と`Execute`クエリの実行プラン キャッシュをサポートしています。これには、準備されたステートメントの両方の形式が含まれます。

-   プロトコル機能`COM_STMT_PREPARE`および`COM_STMT_EXECUTE`を使用します。
-   SQL ステートメント`PREPARE`と`EXECUTE`を使用します。

TiDB オプティマイザーは、これら 2 種類のクエリを同じ方法で処理します。準備時に、パラメーター化されたクエリは AST (抽象構文ツリー) に解析され、キャッシュされます。その後の実行時に、保存された AST と特定のパラメーター値に基づいて実行プランが生成されます。

実行プラン キャッシュを有効にすると、最初の実行では、 `Prepare`ステートメントごとに現在のクエリが実行プラン キャッシュを使用できるかどうかが確認され、使用できる場合は、生成された実行プランが LRU (Least Recently Used) リンク リストによって実装されたキャッシュに格納されます。後続の`Execute`のクエリでは、実行プランがキャッシュから取得され、使用可能かどうかがチェックされます。チェックが成功した場合、実行プランを生成する手順はスキップされます。それ以外の場合は、実行プランが再生成され、キャッシュに保存されます。

TiDB は、 `Prepare` / `Execute`ステートメントと同様に、一部の`PREPARE`以外のステートメントの実行プランのキャッシュもサポートしています。詳細については、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)を参照してください。

TiDB の現在のバージョンでは、 `Prepare`ステートメントが次のいずれかの条件を満たす場合、クエリまたはプランはキャッシュされません。

-   クエリには、 `SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `Union` 、 `Intersect` 、および`Except`以外の SQL ステートメントが含まれています。
-   クエリは一時テーブル、または生成された列を含むテーブルにアクセスします。
-   クエリには、 `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`などの相関のないサブクエリが含まれています。
-   クエリには、実行プランに`SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`などの`PhysicalApply`の演算子を持つ相関サブクエリが含まれています。
-   クエリには、 `SELECT /*+ ignore_plan_cache() */ * FROM t`や`SELECT /*+ set_var(max_execution_time=1) */ * FROM t`などの`ignore_plan_cache`または`set_var`ヒントが含まれています。
-   クエリには、 `select * from t where a>? and b>@x`などの`?`以外の変数 (システム変数またはユーザー定義変数を含む) が含まれています。
-   クエリには、キャッシュできない関数`database()` 、 `current_user` 、 `current_role` 、 `user` 、 `connection_id` 、 `last_insert_id` 、 `row_count` 、 `version` 、および`like`含まれています。
-   クエリでは、 `LIMIT`パラメータとして変数 ( `LIMIT ?`や`LIMIT 10, ?`など) が使用され、変数の値は 10000 を超えています。
-   クエリには`Order By ?`のように`Order By`の後に`?`含まれます。このようなクエリは`?`で指定された列に基づいてデータをソートします。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は間違ってしまいます。そのため、このようなクエリはキャッシュされません。ただし、 `Order By a+?`などの一般的なクエリの場合はキャッシュされます。
-   クエリには`Group By?`のように`Group By`の後に`?`含まれます。このようなクエリは`?`で指定された列に基づいてデータをグループ化します。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は間違ってしまいます。そのため、このようなクエリはキャッシュされません。ただし、 `Group By a+?`などの一般的なクエリの場合はキャッシュされます。
-   クエリには、 `Window Frame`ウィンドウ関数の定義に`(partition by year order by sale rows ? preceding)`などの`?`含まれています。ウィンドウ関数の他の場所に`?`出現する場合、クエリはキャッシュされます。
-   クエリには、 `int`と`string`比較するためのパラメータ（ `c_int >= ?`や`c_int in (?, ?)`など）が含まれており、 `?` `set @x='123'`などの文字列型を示します。クエリ結果が MySQL と互換性があることを保証するには、各クエリでパラメータを調整する必要があり、このようなクエリはキャッシュされません。
-   この計画は`TiFlash`にアクセスしようとします。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメータがない限り、 `TableDual`含むプランはキャッシュされません。
-   クエリは、 `information_schema.columns`などの TiDB システム ビューにアクセスします。システム ビューにアクセスするために`Prepare`および`Execute`ステートメントを使用することは推奨されません。

TiDB では、クエリ内の`?`の数に制限があります。クエリに 65535 を超える`?`が含まれている場合、エラー`Prepared statement contains too many placeholders`が報告されます。

LRU リンク リストは、 `Prepare`間で実行でき`Execute`ため、セッション レベルのキャッシュとして設計されています。LRU リストの各要素は、キーと値のペアです。値は実行プランであり、キーは次の部分で構成されます。

-   `Execute`実行されるデータベースの名前
-   `Prepare`番目のステートメントの識別子、つまり`PREPARE`のキーワードの後の名前
-   現在のスキーマバージョン。DDL文が正常に実行されるたびに更新されます。
-   `Execute`実行するときのSQLモード
-   現在のタイムゾーン（ `time_zone`システム変数の値）
-   `sql_select_limit`システム変数の値

前述の情報の変更 (たとえば、データベースの切り替え、 `Prepare`文の名前変更、DDL 文の実行、SQL モード/ `time_zone`の値の変更)、または LRU キャッシュ削除メカニズムにより、実行時に実行プランのキャッシュ ミスが発生します。

実行プラン キャッシュがキャッシュから取得された後、TiDB はまず実行プランがまだ有効かどうかを確認します。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照先のテーブルがトランザクション プリオーダー ステートメントで変更された場合、このテーブルにアクセスするキャッシュされた実行プランに`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行プランのスキャン範囲が現在のパラメータ値に応じて調整され、データクエリの実行に使用されます。

実行プランのキャッシュとクエリ パフォーマンスに関して注目すべき点がいくつかあります。

-   実行プランがキャッシュされているかどうかに関係なく、SQL バインディングの影響を受けます。キャッシュされていない実行プラン (最初の`Execute` ) の場合、これらのプランは既存の SQL バインディングの影響を受けます。キャッシュされている実行プランの場合、新しい SQL バインディングが作成されると、これらのプランは無効になります。
-   キャッシュされたプランは、統計、最適化ルール、および式によるブロックリストのプッシュダウンの変更の影響を受けません。
-   `Execute`のパラメータが異なることを考慮して、実行プラン キャッシュは、適応性を確保するために、特定のパラメータ値に密接に関連するいくつかの積極的なクエリ最適化方法を禁止します。これにより、クエリ プランが特定のパラメータ値に対して最適でない場合があります。たとえば、クエリのフィルタ条件が`where a > ? And a < ?`で、最初の`Execute`のステートメントのパラメータがそれぞれ`2`と`1`であるとします。次の実行時にこれらの 2 つのパラメータが`1`と`2`になる可能性があることを考慮すると、オプティマイザは現在のパラメータ値に固有の最適な`TableDual`実行プランを生成しません。
-   キャッシュの無効化と削除を考慮しない場合、実行プラン キャッシュはさまざまなパラメーター値に適用され、理論的には特定の値に対して最適でない実行プランが生成されます。たとえば、フィルター条件が`where a < ?`で、最初の実行に使用されたパラメーター値が`1`の場合、オプティマイザーは最適な`IndexScan`実行プランを生成し、それをキャッシュに格納します。後続の実行で値が`10000`になった場合、 `TableScan`プランの方が適している可能性があります。ただし、実行プラン キャッシュがあるため、実行には以前に生成された`IndexScan`が使用されます。したがって、実行プラン キャッシュは、クエリが単純 (コンパイル率が高い) で実行プランが比較的固定されているアプリケーション シナリオに適しています。

v6.1.0 以降では、実行プラン キャッシュがデフォルトで有効になっています。準備されたプラン キャッシュは、システム変数[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を介して制御できます。

> **注記：**
>
> [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)システム変数は、通常のクエリではなく、 `Prepare` / `Execute`クエリの実行プラン キャッシュのみを制御します。通常のクエリの実行プラン キャッシュについては、 [SQL 未準備実行プラン キャッシュ](/sql-non-prepared-plan-cache.md)を参照してください。

実行プラン キャッシュ機能を有効にすると、セッション レベルのシステム変数[`last_plan_from_cache`](/system-variables.md#last_plan_from_cache-new-in-v40)を使用して、前の`Execute`ステートメントでキャッシュされた実行プランが使用されたかどうかを確認できます。次に例を示します。

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

実行プラン キャッシュが原因で、特定の`Prepare`セットに予期しない動作があることがわかった場合は、 `ignore_plan_cache()` SQL ヒントを`Execute`して、現在のステートメントの実行プラン キャッシュの使用をスキップできます。それでも、前述のステートメントを例として使用します。

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

## プリペアドプランキャッシュの診断 {#diagnostics-of-prepared-plan-cache}

一部のクエリまたはプランはキャッシュできません。 `SHOW WARNINGS`ステートメントを使用して、クエリまたはプランがキャッシュされているかどうかを確認できます。 キャッシュされていない場合は、結果で失敗の理由を確認できます。 例:

```sql
mysql> PREPARE st FROM 'SELECT * FROM t WHERE a > (SELECT MAX(a) FROM t)';  -- The query contains a subquery and cannot be cached.

Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> show warnings;  -- Checks the reason why the query plan cannot be cached.

+---------+------+-----------------------------------------------+
| Level   | Code | Message                                       |
+---------+------+-----------------------------------------------+
| Warning | 1105 | skip plan-cache: sub-queries are un-cacheable |
+---------+------+-----------------------------------------------+
1 row in set (0.00 sec)

mysql> prepare st from 'select * from t where a<?';

Query OK, 0 rows affected (0.00 sec)

mysql> set @a='1';

Query OK, 0 rows affected (0.00 sec)

mysql> execute st using @a;  -- The optimization converts a non-INT type to an INT type, and the execution plan might change with the change of the parameter, so TiDB does not cache the plan.

Empty set, 1 warning (0.01 sec)

mysql> show warnings;

+---------+------+----------------------------------------------+
| Level   | Code | Message                                      |
+---------+------+----------------------------------------------+
| Warning | 1105 | skip plan-cache: '1' may be converted to INT |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)
```

## プリペアドプランキャッシュのメモリ管理 {#memory-management-of-prepared-plan-cache}

<CustomContent platform="tidb">

プリペアドプランキャッシュを使用すると、メモリのオーバーヘッドが発生します。各 TiDB インスタンスのすべてのセッションのキャッシュされた実行プランによる合計メモリ消費量を表示するには、Grafana の[**プランキャッシュメモリ使用量**監視パネル](/grafana-tidb-dashboard.md)使用します。

> **注記：**
>
> Golangのメモリ再利用メカニズムといくつかのカウントされないメモリ構造のため、Grafana に表示されるメモリは実際のヒープメモリ使用量と一致しません。Grafana に表示されるメモリと実際のヒープメモリ使用量の間には、約 ±20% の偏差があることがテストで判明しています。

各 TiDB インスタンスにキャッシュされている実行プランの合計数を表示するには、Grafana の[**プランキャッシュプラン番号**パネル](/grafana-tidb-dashboard.md)使用します。

以下は、Grafana の**Plan Cache Memory Usage**パネルと**Plan Cache Plan Num**パネルの例です。

![grafana\_panels](/media/planCache-memoryUsage-planNum-panels.png)

v7.1.0 以降では、システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を構成することで、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりで、監視パネルに応じて調整できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

プリペアドプランキャッシュを使用すると、メモリのオーバーヘッドが発生します。内部テストでは、キャッシュされたプランごとに平均 100 KiB のメモリが消費されます。プラン キャッシュは現在`SESSION`レベルであるため、合計メモリ消費量は約`the number of sessions * the average number of cached plans in a session * 100 KiB`です。

たとえば、現在の TiDB インスタンスには同時実行セッションが 50 あり、各セッションには約 100 のキャッシュされたプランがあります。合計メモリ消費量は約`50 * 100 * 100 KiB` = `512 MB`です。

システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を構成することで、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりです。

</CustomContent>

-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB 以下の場合は、 `tidb_session_plan_cache_size`を`50`に設定します。
-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB を超える場合は、 `tidb_session_plan_cache_size`を`100`に設定します。

v7.1.0 以降では、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用して、キャッシュできるプランの最大サイズを制御できます。デフォルト値は 2 MB です。プランのサイズがこの値を超えると、プランはキャッシュされません。

TiDBサーバーの未使用メモリが一定のしきい値を下回ると、プラン キャッシュのメモリ保護メカニズムがトリガーされ、キャッシュされたプランの一部が削除されます。

システム変数`tidb_prepared_plan_cache_memory_guard_ratio`を設定することでしきい値を制御できます。しきい値はデフォルトで 0.1 に設定されており、これは TiDBサーバーの未使用メモリが合計メモリの 10% 未満 (メモリの 90% が使用済み) になると、メモリ保護メカニズムがトリガーされることを意味します。

<CustomContent platform="tidb">

メモリ制限により、プラン キャッシュが失われる場合があります。Grafana ダッシュボードで[`Plan Cache Miss OPS`メトリック](/grafana-tidb-dashboard.md)表示してステータスを確認できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

メモリ制限により、プラン キャッシュが失われる場合があります。

</CustomContent>

## 実行プランのキャッシュをクリアする {#clear-execution-plan-cache}

`ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE`ステートメントを実行すると、実行プラン キャッシュをクリアできます。

このステートメントでは、 `[SESSION | INSTANCE]` 、現在のセッションまたは TiDB インスタンス全体のプラン キャッシュをクリアするかどうかを指定します。スコープが指定されていない場合、前述のステートメントはデフォルトで`SESSION`キャッシュに適用されます。

以下は、 `SESSION`実行プラン キャッシュをクリアする例です。

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

現在、TiDB は`GLOBAL`実行プラン キャッシュのクリアをサポートしていません。つまり、TiDB クラスター全体のキャッシュされたプランをクリアすることはできません。3 `GLOBAL`実行プラン キャッシュをクリアしようとすると、次のエラーが報告されます。

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## <code>COM_STMT_CLOSE</code>コマンドと<code>DEALLOCATE PREPARE</code>ステートメントを無視します。 {#ignore-the-code-com-stmt-close-code-command-and-the-code-deallocate-prepare-code-statement}

SQL ステートメントの構文解析コストを削減するには、 `prepare stmt`回実行し、次に`execute stmt`複数回実行してから`deallocate prepare`実行することをお勧めします。

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;  -- Execute once
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- Execute multiple times
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

実際の練習では、以下に示すように、 `execute stmt`実行した後、毎回`deallocate prepare`実行することに慣れているかもしれません。

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
MySQL [test]> prepare stmt from '...'; -- Prepare twice
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

このような方法では、最初に実行されたステートメントによって取得されたプランは、2 番目に実行されたステートメントでは再利用できません。

この問題を解決するには、システム変数[`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)を`ON`に設定して、TiDB が`prepare stmt`を閉じるコマンドを無視するようにします。

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

### 監視 {#monitoring}

<CustomContent platform="tidb">

**Executor**セクションの TiDB ページの[Grafanaダッシュボード](/grafana-tidb-dashboard.md)には、「プラン キャッシュ OPS を使用するクエリ」と「プラン キャッシュ ミス OPS」のグラフがあります。これらのグラフを使用して、TiDB とアプリケーションの両方が正しく構成され、SQL プラン キャッシュが正しく機能しているかどうかを確認できます。同じページの**Server**セクションには、「準備されたステートメントの数」のグラフがあります。アプリケーションが準備されたステートメントを使用している場合、このグラフにはゼロ以外の値が表示されます。これは、SQL プラン キャッシュが正しく機能するために必要なものです。

![sql\_plan\_cache](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB Cloudコンソール](https://tidbcloud.com/)の[**監視**](/tidb-cloud/built-in-monitoring.md)ページで、 `Queries Using Plan Cache OPS`メトリックをチェックして、すべての TiDB インスタンスで 1 秒あたりにプラン キャッシュを使用しているクエリまたはプラン キャッシュがないクエリの数を取得できます。

</CustomContent>

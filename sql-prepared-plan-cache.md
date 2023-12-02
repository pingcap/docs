---
title: SQL Prepared Execution Plan Cache
summary: Learn about SQL Prepared Execution Plan Cache in TiDB.
---

# SQL 準備済み実行プラン キャッシュ {#sql-prepared-execution-plan-cache}

TiDB は、 `Prepare`および`Execute`クエリの実行プラン キャッシュをサポートします。これには、準備されたステートメントの両方の形式が含まれます。

-   `COM_STMT_PREPARE`および`COM_STMT_EXECUTE`プロトコル機能を使用します。
-   SQL ステートメントの使用`PREPARE`および`EXECUTE` 。

TiDB オプティマイザは、これら 2 種類のクエリを同じ方法で処理します。準備時に、パラメータ化されたクエリは AST (抽象構文ツリー) に解析されてキャッシュされます。後の実行では、保存された AST と特定のパラメーター値に基づいて実行計画が生成されます。

実行プラン キャッシュが有効になっている場合、最初の実行で`Prepare`ステートメントごとに現在のクエリが実行プラン キャッシュを使用できるかどうかがチェックされ、クエリが実行プラン キャッシュを使用できる場合は、生成された実行プランが LRU (最も古いもの) によって実装されたキャッシュに置かれます。中古）リンクリスト。後続の`Execute`のクエリでは、実行プランがキャッシュから取得され、可用性がチェックされます。チェックが成功した場合、実行計画を生成するステップはスキップされます。それ以外の場合、実行計画は再生成され、キャッシュに保存されます。

TiDB は、 `Prepare` / `Execute`ステートメントと同様に、一部の非`PREPARE`ステートメントの実行プラン キャッシュもサポートしています。詳細については、 [準備されていないプラン キャッシュ](/sql-non-prepared-plan-cache.md)を参照してください。

TiDB の現在のバージョンでは、 `Prepare`ステートメントが次の条件のいずれかを満たしている場合、クエリまたはプランはキャッシュされません。

-   クエリには`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `Union` 、 `Intersect` 、および`Except`以外の SQL ステートメントが含まれています。
-   クエリは、パーティション化されたテーブル、一時テーブル、または生成された列を含むテーブルにアクセスします。
-   クエリには、 `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`などの相関のないサブクエリが含まれています。
-   クエリには、実行プランに演算子が`PhysicalApply`ある相関サブクエリ ( `SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`など) が含まれています。
-   クエリには、 `SELECT /*+ ignore_plan_cache() */ * FROM t`や`SELECT /*+ set_var(max_execution_time=1) */ * FROM t`などの`ignore_plan_cache`または`set_var`ヒントが含まれています。
-   クエリには、 `select * from t where a>? and b>@x`など、 `?`以外の変数 (システム変数またはユーザー定義変数を含む) が含まれています。
-   クエリには、キャッシュできない関数`database()` 、 `current_user` 、 `current_role` 、 `user` 、 `connection_id` 、 `last_insert_id` 、 `row_count` 、 `version` 、および`like`が含まれています。
-   クエリでは`LIMIT`パラメーターとして変数 ( `LIMIT ?`や`LIMIT 10, ?`など) が使用されており、変数値が 10000 より大きくなっています。
-   クエリには`Order By`後に`?`含まれます ( `Order By ?`など)。このようなクエリは、 `?`で指定された列に基づいてデータを並べ替えます。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Order By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには`Group By`後に`?`含まれます ( `Group By?`など)。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Group By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには`Window Frame`ウィンドウ関数の定義に`?`含まれています ( `(partition by year order by sale rows ? preceding)`など)。ウィンドウ関数の他の場所に`?`が表示される場合、クエリはキャッシュされます。
-   クエリには、 `c_int >= ?`や`c_int in (?, ?)`など、 `int`と`string`比較するためのパラメータが含まれており、 `?` `set @x='123'`などの文字列タイプを示します。クエリ結果が MySQL と互換性があることを確認するには、各クエリでパラメータを調整する必要があるため、そのようなクエリはキャッシュされません。
-   プランは`TiFlash`にアクセスしようとします。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメーターがない場合を除き、 `TableDual`を含むプランはキャッシュされません。
-   クエリは、 `information_schema.columns`などの TiDB システム ビューにアクセスします。システム ビューにアクセスするために`Prepare`と`Execute`ステートメントを使用することはお勧めできません。

TiDB では、クエリ内の`?`の数に制限があります。クエリに 65535 `?`を超える値が含まれる場合、エラー`Prepared statement contains too many placeholders`が報告されます。

`Prepare` / `Execute`はセッションをまたがって実行できないため、LRU リンク リストはセッション レベルのキャッシュとして設計されています。 LRU リストの各要素はキーと値のペアです。値は実行計画であり、キーは次の部分で構成されます。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`ステートメントの識別子、つまり`PREPARE`キーワードの後の名前
-   現在のスキーマのバージョン。DDL ステートメントが正常に実行されるたびに更新されます。
-   実行時のSQLモード`Execute`
-   現在のタイムゾーン`time_zone`システム変数の値です。
-   `sql_select_limit`システム変数の値

前述の情報の変更 (データベースの切り替え、 `Prepare`ステートメントの名前変更、DDL ステートメントの実行、SQL モード/ `time_zone`の値の変更など)、または LRU キャッシュ削除メカニズムにより、実行時に実行プランのキャッシュ ミスが発生します。

実行プラン キャッシュがキャッシュから取得された後、TiDB はまず実行プランがまだ有効かどうかを確認します。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照されるテーブルがトランザクション事前順序ステートメントで変更されている場合、このテーブルにアクセスするキャッシュされた実行プランに`UnionScan`演算子が含まれていない場合、そのステートメントは実行できません。

検証テストに合格すると、実行プランのスキャン範囲が現在のパラメータ値に従って調整され、データ クエリの実行に使用されます。

実行プランのキャッシュとクエリのパフォーマンスについては、注目に値する点がいくつかあります。

-   実行プランがキャッシュされるかどうかに関係なく、SQL バインディングの影響を受けます。キャッシュされていない実行プラン (最初の`Execute` ) の場合、これらのプランは既存の SQL バインディングの影響を受けます。キャッシュされた実行プランの場合、新しい SQL バインディングが作成されると、これらのプランは無効になります。
-   キャッシュされたプランは、統計、最適化ルール、式によるブロックリストのプッシュダウンの変更の影響を受けません。
-   `Execute`のパラメータが異なることを考慮して、実行プラン キャッシュは、適応性を確保するために、特定のパラメータ値に密接に関連する一部の積極的なクエリ最適化方法を禁止します。これにより、クエリ プランが特定のパラメーター値に対して最適ではなくなる可能性があります。たとえば、クエリのフィルター条件は`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメーターはそれぞれ`2`と`1`です。これら 2 つのパラメータが次回の実行時に`1`と`2`になる可能性が`TableDual`ことを考慮すると、オプティマイザは現在のパラメータ値に固有の最適な実行プランを生成しません。
-   キャッシュの無効化と削除が考慮されていない場合、実行プラン キャッシュはさまざまなパラメーター値に適用され、理論的には特定の値に対して実行プランが最適化されなくなります。たとえば、フィルター条件が`where a < ?`で、最初の実行に使用されるパラメーター値が`1`場合、オプティマイザーは最適な`IndexScan`実行プランを生成し、キャッシュに入れます。後続の実行で値が`10000`になった場合は、 `TableScan`計画の方が良い可能性があります。ただし、実行プラン キャッシュにより、以前に生成された`IndexScan`が実行に使用されます。したがって、実行プラン キャッシュは、クエリが単純で (コンパイル率が高く)、実行プランが比較的固定されているアプリケーション シナリオにより適しています。

v6.1.0 以降、実行プラン キャッシュはデフォルトで有効になります。準備されたプランのキャッシュは、システム変数[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を介して制御できます。

> **注記：**
>
> 実行プラン キャッシュ機能は`Prepare` / `Execute`クエリにのみ適用され、通常のクエリには効果がありません。

実行プラン キャッシュ機能を有効にすると、セッション レベルのシステム変数[`last_plan_from_cache`](/system-variables.md#last_plan_from_cache-new-in-v40)を使用して、前の`Execute`ステートメントがキャッシュされた実行プランを使用したかどうかを確認できます。次に例を示します。

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

実行プラン キャッシュが原因で、 `Prepare` / `Execute`の特定のセットが予期しない動作をしていることが判明した場合は、 `ignore_plan_cache()` SQL ヒントを使用して、現在のステートメントに対する実行プラン キャッシュの使用をスキップできます。ただし、前述のステートメントを例として使用します。

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

一部のクエリまたはプランはキャッシュできません。 `SHOW WARNINGS`ステートメントを使用して、クエリまたはプランがキャッシュされているかどうかを確認できます。キャッシュされていない場合は、結果で失敗の理由を確認できます。例えば：

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

プリペアドプランキャッシュを使用すると、メモリオーバーヘッドが発生します。各 TiDB インスタンスのすべてのセッションのキャッシュされた実行プランによる合計メモリ消費量を表示するには、Grafana の[**「プラン・キャッシュ・メモリー使用量」**モニター・パネル](/grafana-tidb-dashboard.md)を使用できます。

> **注記：**
>
> Golangのメモリ再利用メカニズムと一部のカウントされていないメモリ構造のため、Grafana に表示されるメモリは実際のヒープメモリ使用量と等しくありません。 Grafana で表示されるメモリと実際のヒープメモリ使用量の間には、±20% 程度の偏差があることがテストされています。

各 TiDB インスタンスにキャッシュされた実行プランの合計数を表示するには、Grafana の[**「プランキャッシュプラン番号」**パネル](/grafana-tidb-dashboard.md)を使用できます。

以下は、Grafana の**[プラン キャッシュ メモリ使用量]**パネルと**[プラン キャッシュ プラン数]**パネルの例です。

![grafana\_panels](/media/planCache-memoryUsage-planNum-panels.png)

v7.1.0 以降、システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を構成することで、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりで、監視パネルに応じて調整できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

プリペアドプランキャッシュを使用すると、ある程度のメモリオーバーヘッドが発生します。内部テストでは、キャッシュされた各プランは平均 100 KiB のメモリを消費します。プラン キャッシュは現在`SESSION`レベルであるため、合計メモリ消費量は約`the number of sessions * the average number of cached plans in a session * 100 KiB`です。

たとえば、現在の TiDB インスタンスには 50 の同時セッションがあり、各セッションには約 100 のキャッシュされたプランがあります。合計メモリ消費量は約`50 * 100 * 100 KiB` = `512 MB`です。

システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)を構成することで、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりです。

</CustomContent>

-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB 以下の場合は、 `tidb_session_plan_cache_size` ～ `50`を設定します。
-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB を超える場合は、 `tidb_session_plan_cache_size` ～ `100`を設定します。

v7.1.0 以降、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用してキャッシュできるプランの最大サイズを制御できます。デフォルト値は 2 MB です。プランのサイズがこの値を超える場合、プランはキャッシュされません。

TiDBサーバーの未使用メモリが特定のしきい値未満になると、プラン キャッシュのメモリ保護メカニズムがトリガーされ、キャッシュされたプランの一部が削除されます。

システム変数`tidb_prepared_plan_cache_memory_guard_ratio`を構成することで、しきい値を制御できます。デフォルトのしきい値は 0.1 です。これは、TiDBサーバーの未使用メモリが総メモリの 10% 未満になると (メモリの 90% が使用されている場合)、メモリ保護メカニズムがトリガーされることを意味します。

<CustomContent platform="tidb">

メモリ制限により、プラン キャッシュが失われる場合があります。 Grafana ダッシュボードの[`Plan Cache Miss OPS`メトリクス](/grafana-tidb-dashboard.md)を表示してステータスを確認できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

メモリ制限により、プラン キャッシュが失われる場合があります。

</CustomContent>

## 実行プランのキャッシュをクリアする {#clear-execution-plan-cache}

`ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE`ステートメントを実行すると、実行プランのキャッシュをクリアできます。

このステートメントでは、 `[SESSION | INSTANCE]`プラン キャッシュが現在のセッションに対してクリアされるか、TiDB インスタンス全体に対してクリアされるかを指定します。スコープが指定されていない場合、前述のステートメントはデフォルトで`SESSION`キャッシュに適用されます。

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

現在、TiDB は`GLOBAL`実行プラン キャッシュのクリアをサポートしていません。つまり、TiDB クラスター全体のキャッシュされたプランをクリアすることはできません。 `GLOBAL`実行プランのキャッシュをクリアしようとすると、次のエラーが報告されます。

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## <code>COM_STMT_CLOSE</code>コマンドと<code>DEALLOCATE PREPARE</code>ステートメントを無視します。 {#ignore-the-code-com-stmt-close-code-command-and-the-code-deallocate-prepare-code-statement}

SQL ステートメントの構文解析コストを削減するには、 `prepare stmt`を 1 回実行し、次に`execute stmt`複数回実行してから`deallocate prepare`を実行することをお勧めします。

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;  -- Execute once
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- Execute multiple times
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

実際には、以下に示すように、 `execute stmt`を実行した後に毎回`deallocate prepare`を実行することに慣れているかもしれません。

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
MySQL [test]> prepare stmt from '...'; -- Prepare twice
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

このような場合、最初に実行されたステートメントによって取得されたプランは、2 番目に実行されたステートメントによって再利用することはできません。

この問題に対処するには、システム変数[`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600) `ON`に設定して、TiDB が`prepare stmt`を閉じるコマンドを無視するようにします。

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

TiDB ページの**Executor**セクションの[Grafana ダッシュボード](/grafana-tidb-dashboard.md)には、「プラン キャッシュ OPS を使用したクエリ」グラフと「プラン キャッシュ ミス OPS」グラフがあります。これらのグラフを使用して、TiDB とアプリケーションの両方が SQL プラン キャッシュが正しく動作できるように正しく構成されているかどうかを確認できます。同じページの**サーバー**セクションには、「プリペアドステートメント数」グラフが表示されます。アプリケーションがプリペアド ステートメントを使用している場合、このグラフはゼロ以外の値を示します。これは、SQL プラン キャッシュが正しく機能するために必要です。

![sql\_plan\_cache](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB Cloudコンソール](https://tidbcloud.com/)の[**監視**](/tidb-cloud/built-in-monitoring.md)ページでは、 `Queries Using Plan Cache OPS`メトリクスをチェックして、すべての TiDB インスタンスで 1 秒あたりのプラン キャッシュを使用しているクエリまたは欠落しているクエリの数を取得できます。

</CustomContent>

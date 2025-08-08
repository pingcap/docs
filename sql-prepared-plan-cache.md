---
title: SQL Prepared Execution Plan Cache
summary: TiDB の SQL 準備実行プラン キャッシュについて学習します。
---

# SQL 準備済み実行プランキャッシュ {#sql-prepared-execution-plan-cache}

TiDBは、 `Prepare`と`Execute`クエリの実行プランのキャッシュをサポートしています。これには、以下の2つの形式のプリペアドステートメントが含まれます。

-   プロトコル機能`COM_STMT_PREPARE`および`COM_STMT_EXECUTE`使用。
-   SQL ステートメント`PREPARE`と`EXECUTE`使用します。

TiDB オプティマイザーは、これら 2 種類のクエリを同じ方法で処理します。準備時に、パラメータ化されたクエリは AST (抽象構文ツリー) に解析され、キャッシュされます。その後の実行時に、保存された AST と特定のパラメータ値に基づいて実行プランが生成されます。

実行プランキャッシュが有効な場合、最初の実行では、各`Prepare`ごとに現在のクエリが実行プランキャッシュを使用できるかどうかが確認され、使用できる場合は、生成された実行プランがLRU（Least Recently Used）リンクリストで実装されたキャッシュに格納されます。後続の`Execute`クエリでは、キャッシュから実行プランが取得され、その可用性が確認されます。確認が成功した場合、実行プラン生成のステップはスキップされます。そうでない場合は、実行プランが再生成され、キャッシュに保存されます。

TiDBは、 `Prepare` / `Execute`文と同様に、 `PREPARE`以外の文についても実行計画のキャッシュをサポートしています。詳細については、 [準備されていないプランキャッシュ](/sql-non-prepared-plan-cache.md)を参照してください。

TiDB の現在のバージョンでは、 `Prepare`ステートメントが次のいずれかの条件を満たす場合、クエリまたはプランはキャッシュされません。

-   クエリには、 `SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `Union` 、 `Intersect` 、 `Except`以外の SQL ステートメントが含まれています。
-   クエリは一時テーブル、または生成された列を含むテーブルにアクセスするか、静的モード (つまり、 [`tidb_partition_prune_mode`](/system-variables.md#tidb_partition_prune_mode-new-in-v51)が`static`に設定される) を使用してパーティション テーブルにアクセスします。
-   クエリには、 `SELECT * FROM t1 WHERE t1.a > (SELECT 1 FROM t2 WHERE t2.b < 1)`などの非相関サブクエリが含まれています。
-   クエリには、実行プランに`SELECT * FROM t1 WHERE t1.a > (SELECT a FROM t2 WHERE t1.b > t2.b)`などの`PhysicalApply`演算子を持つ相関サブクエリが含まれています。
-   クエリには、 `SELECT /*+ ignore_plan_cache() */ * FROM t`や`SELECT /*+ set_var(max_execution_time=1) */ * FROM t`などの`ignore_plan_cache`または`set_var`ヒントが含まれています。
-   クエリには、 `select * from t where a>? and b>@x`などの`?`以外の変数 (システム変数やユーザー定義変数を含む) が含まれています。
-   クエリには、キャッシュできない関数`database()` 、 `current_user` 、 `current_role` 、 `user` 、 `connection_id` 、 `last_insert_id` 、 `row_count` 、 `version` 、および`like`が含まれています。
-   クエリでは、 `LIMIT`のパラメータとして変数 ( `LIMIT ?`や`LIMIT 10, ?`など) が使用されており、変数の値は 10000 を超えています。
-   クエリには`Order By`後に`?`続きます（例： `Order By ?` ）。このようなクエリは、 `?`で指定された列に基づいてデータをソートします。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は正しくありません。そのため、このようなクエリはキャッシュされません。ただし、 `Order By a+?`ように一般的なクエリの場合はキャッシュされます。
-   クエリは`Group By`後に`?`含みます（例： `Group By?` ）。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列をターゲットとするクエリが同じ実行プランを使用すると、結果は正しくありません。そのため、このようなクエリはキャッシュされません。ただし、 `Group By a+?`ように一般的なクエリの場合はキャッシュされます。
-   クエリには、ウィンドウ関数`Window Frame`の定義に`?` （ `(partition by year order by sale rows ? preceding)`など）が含まれています。ウィンドウ関数の他の場所に`?`出現する場合、クエリはキャッシュされます。
-   このクエリには、 `int`と`string`比較するためのパラメータ`c_int >= ?`や`c_int in (?, ?)`など）が含まれています。ここで、 `?`文字列型（ `set @x='123'`など）を示します。クエリ結果がMySQLと互換性を持つようにするには、各クエリでパラメータを調整する必要があるため、このようなクエリはキャッシュされません。
-   このプランは`TiFlash`アクセスしようとします。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメータがない限り、 `TableDual`を含むプランはキャッシュされません。
-   このクエリは、 `information_schema.columns`などのTiDBシステムビューにアクセスします。システムビューにアクセスするために`Prepare`および`Execute`ステートメントを使用することは推奨されません。

TiDBでは、クエリ内の`?`の数に制限があります。クエリに`?` 65535 個以上含まれる場合、エラー`Prepared statement contains too many placeholders`が報告されます。

LRUリンクリストは、 `Prepare` / `Execute`セッションをまたいで実行できないため、セッションレベルのキャッシュとして設計されています。LRUリストの各要素はキーと値のペアです。値は実行計画であり、キーは以下の要素で構成されます。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`のステートメントの識別子、つまり`PREPARE`のキーワードの後の名前
-   現在のスキーマバージョン。DDL文が正常に実行されるたびに更新されます。
-   実行時のSQLモード`Execute`
-   現在のタイムゾーン（システム変数`time_zone`の値）
-   `sql_select_limit`システム変数の値

前述の情報に変更がある場合 (たとえば、データベースの切り替え、 `Prepare`文の名前変更、DDL 文の実行、SQL mode/ `time_zone`の値の変更)、または LRU キャッシュ削除メカニズムにより、実行時に実行プランのキャッシュ ミスが発生します。

実行計画キャッシュがキャッシュから取得された後、TiDBはまず実行計画がまだ有効かどうかを確認します。現在の`Execute`文が明示的なトランザクションで実行され、参照先のテーブルがトランザクションの事前順序付け文で変更された場合、このテーブルにアクセスするキャッシュされた実行計画に`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行プランのスキャン範囲が現在のパラメータ値に応じて調整され、データクエリの実行に使用されます。

実行プランのキャッシュとクエリ パフォーマンスに関して注目すべき点がいくつかあります。

-   実行プランは、キャッシュされているかどうかに関わらず、SQLバインディングの影響を受けます。キャッシュされていない実行プラン（最初の`Execute` ）は、既存のSQLバインディングの影響を受けます。キャッシュされている実行プランは、新しいSQLバインディングが作成されると無効になります。
-   キャッシュされたプランは、統計、最適化ルール、式によるブロックリストのプッシュダウンの変更の影響を受けません。
-   `Execute`のパラメータが異なることを考慮し、実行プランキャッシュは、適応性を確保するために、特定のパラメータ値に密接に関連する一部の積極的なクエリ最適化手法を禁止します。これにより、クエリプランが特定のパラメータ値に対して最適にならない可能性があります。例えば、クエリのフィルタ条件が`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメータがそれぞれ`2`と`1`あるとします。これらの 2 つのパラメータが次回の実行時に`1`と`2`なる可能性があることを考慮すると、オプティマイザは現在のパラメータ値に固有の最適な`TableDual`実行プランを生成しません。
-   キャッシュの無効化と削除を考慮しない場合、実行プラン キャッシュはさまざまなパラメーター値に適用され、理論上は特定の値に対して最適ではない実行プランが生成されます。たとえば、フィルター条件が`where a < ?`で、最初の実行に使用されたパラメーター値が`1`の場合、オプティマイザーは最適な`IndexScan`実行プランを生成し、それをキャッシュに格納します。後続の実行で値が`10000`になった場合、 `TableScan`プランの方が適している可能性があります。ただし、実行プラン キャッシュがあるため、以前に生成された`IndexScan`使用して実行されます。そのため、実行プラン キャッシュは、クエリが単純 (コンパイル率が高い) で実行プランが比較的固定されているアプリケーション シナリオに適しています。

バージョン6.1.0以降、実行プランキャッシュはデフォルトで有効になっています。準備済みプランキャッシュはシステム変数[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)介して制御できます。

> **注記：**
>
> [`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)システム変数は、 `Prepare` / `Execute`クエリの実行プランキャッシュのみを制御し、通常のクエリは制御しません。通常のクエリの実行プランキャッシュについては、 [SQL 非準備実行プランキャッシュ](/sql-non-prepared-plan-cache.md)参照してください。

実行プラン キャッシュ機能を有効にすると、セッション レベルのシステム変数[`last_plan_from_cache`](/system-variables.md#last_plan_from_cache-new-in-v40)使用して、前の`Execute`ステートメントがキャッシュされた実行プランを使用したかどうかを確認できます。次に例を示します。

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

実行計画キャッシュが原因で、特定の`Prepare` / `Execute`のセットで予期しない動作が発生する場合は、SQLヒント`ignore_plan_cache()`を使用して、現在のステートメントの実行計画キャッシュの使用をスキップできます。ただし、前述のステートメントを例として挙げます。

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

### <code>SHOW WARNINGS</code>を使用して診断する {#use-code-show-warnings-code-to-diagnose}

一部のクエリまたはプランはキャッシュできません。1 ステートメント`SHOW WARNINGS`使用して、クエリまたはプランがキャッシュされているかどうかを確認できます。キャッシュされていない場合は、結果で失敗の理由を確認できます。例:

```sql
mysql> PREPARE st FROM 'SELECT * FROM t WHERE a > (SELECT MAX(a) FROM t)';  -- The query contains a subquery and cannot be cached.

Query OK, 0 rows affected, 1 warning (0.01 sec)

mysql> SHOW WARNINGS;  -- Checks the reason why the query plan cannot be cached.

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

mysql> SHOW WARNINGS;

+---------+------+----------------------------------------------+
| Level   | Code | Message                                      |
+---------+------+----------------------------------------------+
| Warning | 1105 | skip plan-cache: '1' may be converted to INT |
+---------+------+----------------------------------------------+
1 row in set (0.00 sec)
```

### 診断には<code>Statements Summary</code>を使用する {#use-code-statements-summary-code-to-diagnose}

`Statements Summary`テーブルには`plan_cache_unqualified`と`plan_cache_unqualified_last_reason`という2つのフィールドがあり、それぞれ対応するクエリがプランキャッシュを使用できなかった回数とその理由を示します。これらの2つのフィールドは診断に使用できます。

```sql
mysql> SELECT digest_text, plan_cache_unqualified, plan_cache_unqualified_last_reason FROM information_schema.statements_summary WHERE plan_cache_unqualified > 0 ORDER BY plan_cache_unqualified DESC
LIMIT 10;

+---------------------------------+------------------------+----------------------------------------+
| digest_text                     | plan_cache_unqualified | plan_cache_unqualified_last_reason     |
+---------------------------------+------------------------+----------------------------------------+
| select * from `t` where `a` < ? |                     10 | '1' may be converted to INT            |
| select * from `t` order by ?    |                      4 | query has 'order by ?' is un-cacheable |
| select database ( ) from `t`    |                      2 | query has 'database()' is un-cacheable |
...
+---------------------------------+------------------------+----------------------------------------+
10 row in set (0.01 sec)
```

## プリペアドプランキャッシュのメモリ管理 {#memory-management-of-prepared-plan-cache}

<CustomContent platform="tidb">

プリペアドプランキャッシュを使用すると、メモリオーバーヘッドが発生します。各TiDBインスタンス内の全セッションのキャッシュされた実行プランによるメモリ消費量の合計を表示するには、Grafanaの[**プランキャッシュメモリ使用**量監視パネル](/grafana-tidb-dashboard.md)使用します。

> **注記：**
>
> Golangのメモリ回収メカニズムと一部の非カウントメモリ構造のため、Grafanaに表示されるメモリは実際のヒープメモリ使用量と一致しません。Grafanaに表示されるメモリと実際のヒープメモリ使用量の間には、約±20%の誤差があることがテストで確認されています。

各 TiDB インスタンスにキャッシュされている実行プランの合計数を表示するには、Grafana の[**プランキャッシュプラン番号**パネル](/grafana-tidb-dashboard.md)使用できます。

以下は、Grafana の**Plan Cache Memory Usage**パネルと**Plan Cache Plan Num**パネルの例です。

![grafana\_panels](/media/planCache-memoryUsage-planNum-panels.png)

バージョン7.1.0以降では、システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)設定することで、各セッションでキャッシュできるプランの最大数を制御できます。環境によって推奨値は以下のとおりです。監視パネルに応じて調整してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

プリペアドプランキャッシュを使用すると、メモリのオーバーヘッドが発生します。社内テストでは、キャッシュされたプランごとに平均100 KiBのメモリが消費されました。プランキャッシュは現在レベル`SESSION`であるため、合計メモリ消費量は約`the number of sessions * the average number of cached plans in a session * 100 KiB`です。

例えば、現在のTiDBインスタンスには50の同時セッションがあり、各セッションには約100のキャッシュプランがあります。この場合、メモリ消費量は約`50 * 100 * 100 KiB` = `512 MB`になります。

システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)設定することで、各セッションでキャッシュできるプランの最大数を制御できます。環境によって推奨される値は次のとおりです。

</CustomContent>

-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB 以下の場合は、 `tidb_session_plan_cache_size`を`50`に設定します。
-   TiDBサーバーインスタンスのメモリしきい値が 64 GiB を超える場合は、 `tidb_session_plan_cache_size`を`100`に設定します。

バージョン7.1.0以降では、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用して、キャッシュできるプランの最大サイズを制御できます。デフォルト値は2 MBです。プランのサイズがこの値を超える場合、プランはキャッシュされません。

TiDBサーバーの未使用メモリが一定のしきい値を下回ると、プラン キャッシュのメモリ保護メカニズムがトリガーされ、キャッシュされたプランの一部が削除されます。

システム変数`tidb_prepared_plan_cache_memory_guard_ratio`設定することで、しきい値を制御できます。しきい値はデフォルトで 0.1 に設定されており、TiDBサーバーの未使用メモリが総メモリの 10% 未満（メモリの 90% が使用済み）になると、メモリ保護メカニズムが起動します。

<CustomContent platform="tidb">

メモリ制限により、プランキャッシュが失われる場合があります。Grafanaダッシュボードの[`Plan Cache Miss OPS`メトリック](/grafana-tidb-dashboard.md)でステータスを確認できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

メモリ制限により、プラン キャッシュが失われる場合があります。

</CustomContent>

## 実行プランのキャッシュをクリアする {#clear-execution-plan-cache}

`ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE`ステートメントを実行すると、実行プラン キャッシュをクリアできます。

このステートメントでは、 `[SESSION | INSTANCE]`プランキャッシュを現在のセッションに対してクリアするか、TiDB インスタンス全体に対してクリアするかを指定します。スコープが指定されていない場合、上記のステートメントはデフォルトで`SESSION`キャッシュに適用されます。

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

現在、TiDBは`GLOBAL`実行計画キャッシュのクリアをサポートしていません。つまり、TiDBクラスタ全体のキャッシュされた計画をクリアすることはできません。3 `GLOBAL`実行計画キャッシュをクリアしようとすると、以下のエラーが報告されます。

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## <code>COM_STMT_CLOSE</code>コマンドと<code>DEALLOCATE PREPARE</code>ステートメントを無視します。 {#ignore-the-code-com-stmt-close-code-command-and-the-code-deallocate-prepare-code-statement}

SQL ステートメントの構文解析コストを削減するには、 `prepare stmt` 1 回実行し、次に`execute stmt`複数回実行してから`deallocate prepare`実行することをお勧めします。

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

この問題を解決するには、システム変数[`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)を`ON`に設定して、TiDB が`prepare stmt`閉じるコマンドを無視するようにします。

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

TiDBページの**Executor**セクションの[Grafanaダッシュボード](/grafana-tidb-dashboard.md)には、「プランキャッシュOPSを使用するクエリ」と「プランキャッシュミスOPS」のグラフがあります。これらのグラフは、TiDBとアプリケーションの両方がSQLプランキャッシュが正しく動作するように正しく設定されているかどうかを確認できます。同じページの**Server**セクションには、「準備済みステートメント数」のグラフがあります。アプリケーションが準備済みステートメントを使用している場合、このグラフは0以外の値を示します。これはSQLプランキャッシュが正しく機能するために必要なものです。

![sql\_plan\_cache](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB Cloudコンソール](https://tidbcloud.com/)の[**監視**](/tidb-cloud/built-in-monitoring.md)ページ目で`Queries Using Plan Cache OPS`メトリックをチェックして、すべての TiDB インスタンスで 1 秒あたりにプラン キャッシュを使用している、またはプラン キャッシュがないクエリの数を取得できます。

</CustomContent>

---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
---

# SQL 準備実行計画キャッシュ {#sql-prepare-execution-plan-cache}

TiDB は、 `Prepare`および`Execute`クエリの実行プランのキャッシュをサポートしています。これには、プリペアド ステートメントの両方の形式が含まれます。

-   `COM_STMT_PREPARE`および`COM_STMT_EXECUTE`プロトコル機能の使用。
-   SQL ステートメント`PREPARE`および`EXECUTE`を使用します。

TiDB オプティマイザは、これら 2 種類のクエリを同じ方法で処理します。準備時に、パラメータ化されたクエリは AST (Abstract Syntax Tree) に解析され、キャッシュされます。後の実行では、保存された AST と特定のパラメータ値に基づいて実行計画が生成されます。

実行プラン キャッシュが有効な場合、最初の実行で`Prepare`ステートメントごとに、現在のクエリが実行プラン キャッシュを使用できるかどうかがチェックされ、クエリがそれを使用できる場合は、生成された実行プランが LRU (Least Recent) によって実装されたキャッシュに入れられます。使用) リンクされたリスト。後続の`Execute`クエリでは、実行プランがキャッシュから取得され、可用性がチェックされます。チェックが成功した場合、実行計画を生成するステップはスキップされます。それ以外の場合は、実行計画が再生成され、キャッシュに保存されます。

現在のバージョンの TiDB では、 `Prepare`ステートメントが次の条件のいずれかを満たす場合、クエリまたはプランはキャッシュされません。

-   クエリに`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `Union` 、 `Intersect` 、および`Except`以外の SQL ステートメントが含まれています。
-   クエリは、パーティション テーブルまたは一時テーブル、または生成された列を含むテーブルにアクセスします。
-   クエリには、 `select * from t where a > (select ...)`などのサブクエリが含まれています。
-   クエリには、 `select /*+ ignore_plan_cache() */ * from t`などの`ignore_plan_cache`ヒントが含まれています。
-   クエリに、 `select * from t where a>? and b>@x`などの`?`以外の変数 (システム変数またはユーザー定義変数を含む) が含まれています。
-   クエリには、キャッシュできない関数が含まれています: `database()` 、 `current_user` 、 `current_role` 、 `user` 、 `connection_id` 、 `last_insert_id` 、 `row_count` 、 `version` 、および`like` 。
-   クエリには、 `Limit ?`や`Limit 10, ?`など、 `Limit`の後に`?`含まれます。特定の値`?`がクエリのパフォーマンスに大きな影響を与えるため、このようなクエリはキャッシュされません。
-   クエリには、 `Order By ?`など、 `Order By`後に`?`含まれます。このようなクエリは、 `?`で指定された列に基づいてデータを並べ替えます。異なる列をターゲットとするクエリが同じ実行プランを使用する場合、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Order By a+?`などの一般的なものである場合は、キャッシュされます。
-   クエリには、 `Group By?`など、 `Group By`後に`?`含まれます。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列をターゲットとするクエリが同じ実行プランを使用する場合、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Group By a+?`などの一般的なものである場合は、キャッシュされます。
-   クエリには、ウィンドウ関数`Window Frame`の定義に`(partition by year order by sale rows ? preceding)`などの`?`が含まれています。ウィンドウ関数の他の場所に`?`が表示される場合、クエリはキャッシュされます。
-   クエリには、 `int`と`string`比較するためのパラメーター ( `c_int >= ?`や`c_int in (?, ?)`など) が含まれ、 `?` `set @x='123'`などの文字列型を示します。クエリ結果が MySQL と互換性があることを確認するには、各クエリでパラメーターを調整する必要があるため、そのようなクエリはキャッシュされません。
-   プランは`TiFlash`へのアクセスを試みます。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメーターがない場合を除き、 `TableDual`を含むプランはキャッシュされません。

`Prepare` / `Execute`はセッション間で実行できないため、LRU リンク リストはセッション レベルのキャッシュとして設計されています。 LRU リストの各要素は、キーと値のペアです。値は実行計画で、キーは次の部分で構成されます。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`ステートメントの識別子、つまり`PREPARE`キーワードの後の名前
-   DDL ステートメントが正常に実行されるたびに更新される現在のスキーマ バージョン
-   実行時のSQLモード`Execute`
-   `time_zone`システム変数の値である現在のタイムゾーン
-   `sql_select_limit`システム変数の値

上記の情報の変更 (たとえば、データベースの切り替え、 `Prepare`ステートメントの名前変更、DDL ステートメントの実行、SQL モード / `time_zone`の値の変更)、または LRU キャッシュ除去メカニズムにより、実行時に実行プランのキャッシュ ミスが発生します。

実行計画キャッシュがキャッシュから取得された後、TiDB は最初に実行計画がまだ有効かどうかをチェックします。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照されるテーブルがトランザクションの pre-order ステートメントで変更された場合、このテーブルにアクセスするキャッシュされた実行プランには`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行計画のスキャン範囲が現在のパラメーター値に応じて調整され、データ クエリの実行に使用されます。

実行計画のキャッシュとクエリのパフォーマンスについて、注目すべき点がいくつかあります。

-   実行計画がキャッシュされているかどうかに関係なく、SQL バインディングの影響を受けます。キャッシュされていない実行計画 (最初の`Execute` ) の場合、これらの計画は既存の SQL バインディングの影響を受けます。キャッシュされた実行計画の場合、新しい SQL バインディングが作成されると、これらの計画は無効になります。
-   キャッシュされたプランは、統計、最適化ルール、および式によるブロックリスト プッシュダウンの変更の影響を受けません。
-   `Execute`のパラメーターが異なることを考慮して、実行プラン キャッシュは、適応性を確保するために、特定のパラメーター値に密接に関連するいくつかの積極的なクエリ最適化メソッドを禁止します。これにより、クエリ プランが特定のパラメーター値に対して最適でない場合があります。たとえば、クエリのフィルター条件は`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメーターはそれぞれ`2`と`1`です。これら 2 つのパラメーターが次回の実行時に`1`と`2`になる可能性があることを考慮すると、オプティマイザーは現在のパラメーター値に固有の最適な`TableDual`実行計画を生成しません。
-   キャッシュの無効化と削除が考慮されていない場合、実行計画のキャッシュがさまざまなパラメータ値に適用され、理論的には、特定の値に対して最適でない実行計画が発生します。たとえば、フィルタ条件が`where a < ?`で、最初の実行に使用されるパラメータ値が`1`の場合、オプティマイザは最適な`IndexScan`実行計画を生成してキャッシュに入れます。その後の実行で、値が`10000`になった場合は、 `TableScan`プランの方が優れている可能性があります。ただし、実行計画のキャッシュにより、以前に生成された`IndexScan`が実行に使用されます。したがって、実行プラン キャッシュは、クエリが単純で (コンパイルの比率が高く)、実行プランが比較的固定されているアプリケーション シナリオにより適しています。

v6.1.0 以降、実行プランのキャッシュはデフォルトで有効になっています。システム変数[`tidb_enable_prepared_plan_cache`](/system-variables.md#tidb_enable_prepared_plan_cache-new-in-v610)を介して、準備されたプランのキャッシュを制御できます。

> **ノート：**
>
> 実行プラン キャッシュ機能は、 `Prepare` / `Execute`クエリにのみ適用され、通常のクエリには影響しません。

実行計画キャッシュ機能を有効にした後、セッション レベルのシステム変数`last_plan_from_cache`を使用して、前の`Execute`ステートメントがキャッシュされた実行計画を使用したかどうかを確認できます。次に例を示します。

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

`Prepare` / `Execute`の特定のセットに実行計画キャッシュが原因で予期しない動作があることがわかった場合は、 `ignore_plan_cache()` SQL ヒントを使用して、現在のステートメントの実行計画キャッシュの使用をスキップできます。それでも、上記のステートメントを例として使用してください。

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

<CustomContent platform="tidb">

プリペアドプランキャッシュを使用すると、メモリオーバーヘッドが発生します。各 TiDB インスタンスのすべてのセッションのキャッシュされた実行プランによる合計メモリ消費量を表示するには、Grafana で[**Plan Cache Memory Usage**監視パネル](/grafana-tidb-dashboard.md)を使用できます。

> **ノート：**
>
> Golangのメモリ再利用メカニズムといくつかのカウントされないメモリ構造のため、Grafana に表示されるメモリは実際のヒープメモリ使用量と等しくありません。 Grafana で表示されるメモリと実際のヒープメモリ使用量との間に±20% 程度の偏差があることがテストされています。

各 TiDB インスタンスにキャッシュされた実行プランの総数を表示するには、Grafana で[**Plan Cache Plan Num**パネル](/grafana-tidb-dashboard.md)を使用できます。

以下は、Grafana の**Plan Cache Memory Usage**および<strong>Plan Cache Plan Num</strong>パネルの例です。

![grafana\_panels](/media/planCache-memoryUsage-planNum-panels.png)

システム変数`tidb_prepared_plan_cache_size`を構成することにより、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりであり、監視パネルに従って調整できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

プリペアドプランキャッシュを使用すると、メモリオーバーヘッドが発生します。内部テストでは、キャッシュされた各プランは平均 100 KiB のメモリを消費します。 Plan Cache は現在`SESSION`レベルであるため、合計メモリ消費量は約`the number of sessions * the average number of cached plans in a session * 100 KiB`です。

たとえば、現在の TiDB インスタンスには 50 の同時実行セッションがあり、各セッションには約 100 のキャッシュされたプランがあります。合計メモリ消費量は約`50 * 100 * 100 KiB` = `512 MB`です。

システム変数`tidb_prepared_plan_cache_size`を構成することにより、各セッションでキャッシュできるプランの最大数を制御できます。さまざまな環境での推奨値は次のとおりです。

</CustomContent>

-   TiDBサーバーインスタンスのメモリしきい値が &lt;= 64 GiB の場合、 `tidb_prepared_plan_cache_size`から`50`を設定します。
-   TiDBサーバーインスタンスのメモリしきい値が &gt; 64 GiB の場合は、 `tidb_prepared_plan_cache_size`を`100`に設定します。

TiDBサーバーの未使用メモリが特定のしきい値を下回ると、プラン キャッシュのメモリ保護メカニズムがトリガーされ、キャッシュされたプランの一部が削除されます。

システム変数`tidb_prepared_plan_cache_memory_guard_ratio`を構成することにより、しきい値を制御できます。しきい値はデフォルトで 0.1 です。これは、TiDBサーバーの未使用メモリが合計メモリの 10% 未満になると (メモリの 90% が使用される)、メモリ保護メカニズムがトリガーされることを意味します。

<CustomContent platform="tidb">

メモリの制限により、プラン キャッシュが失われることがあります。 Grafana ダッシュボードで[`Plan Cache Miss OPS`メトリック](/grafana-tidb-dashboard.md)を表示して、ステータスを確認できます。

</CustomContent>

<CustomContent platform="tidb-cloud">

メモリの制限により、プラン キャッシュが失われることがあります。

</CustomContent>

## 実行計画のキャッシュをクリアする {#clear-execution-plan-cache}

`ADMIN FLUSH [SESSION | INSTANCE] PLAN_CACHE`ステートメントを実行すると、実行プランのキャッシュをクリアできます。

このステートメントの`[SESSION | INSTANCE]` 、現在のセッションまたは TiDB インスタンス全体のプラン キャッシュをクリアするかどうかを指定します。スコープが指定されていない場合、上記のステートメントはデフォルトで`SESSION`キャッシュに適用されます。

以下は、 `SESSION`実行プランのキャッシュをクリアする例です。

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

現在、TiDB は`GLOBAL`実行プラン キャッシュのクリアをサポートしていません。つまり、TiDB クラスター全体のキャッシュされたプランをクリアすることはできません。 `GLOBAL`実行プランのキャッシュをクリアしようとすると、次のエラーが報告されます。

{{< copyable "" >}}

```sql
MySQL [test]> admin flush global plan_cache;
ERROR 1105 (HY000): Do not support the 'admin flush global scope.'
```

## <code>COM_STMT_CLOSE</code>コマンドと<code>DEALLOCATE PREPARE</code>ステートメントを無視する {#ignore-the-code-com-stmt-close-code-command-and-the-code-deallocate-prepare-code-statement}

SQL ステートメントの構文解析コストを削減するには、 `prepare stmt`を 1 回実行してから、 `deallocate prepare`を実行する前に`execute stmt`複数回実行することをお勧めします。

{{< copyable "" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;  -- Execute once
MySQL [test]> ...
MySQL [test]> execute stmt using ...;  -- Execute multiple times
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

実際には、以下に示すように、 `execute stmt`を実行した後に毎回`deallocate prepare`を実行することに慣れているかもしれません。

{{< copyable "" >}}

```sql
MySQL [test]> prepare stmt from '...'; -- Prepare once
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
MySQL [test]> prepare stmt from '...'; -- Prepare twice
MySQL [test]> execute stmt using ...;
MySQL [test]> deallocate prepare stmt; -- Release the prepared statement
```

このような場合、最初に実行されたステートメントによって取得されたプランは、2 番目に実行されたステートメントでは再利用できません。

この問題に対処するには、システム変数[`tidb_ignore_prepared_cache_close_stmt`](/system-variables.md#tidb_ignore_prepared_cache_close_stmt-new-in-v600)から`ON`を設定して、TiDB がコマンドを無視して`prepare stmt`を閉じるようにします。

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

### モニタリング {#monitoring}

<CustomContent platform="tidb">

**Executor**セクションの TiDB ページの[Grafana ダッシュボード](/grafana-tidb-dashboard.md)には、「プラン キャッシュ OPS を使用したクエリ」と「プラン キャッシュ ミス OPS」のグラフがあります。これらのグラフを使用して、TiDB とアプリケーションの両方が正しく構成され、SQL Plan Cache が正しく機能するかどうかを確認できます。同じページの<strong>サーバー</strong>セクションには、「Prepared Statement Count」グラフが表示されます。アプリケーションがプリペアド ステートメントを使用している場合、このグラフはゼロ以外の値を示します。これは、SQL プラン キャッシュが正しく機能するために必要です。

![sql\_plan\_cache](/media/performance/sql_plan_cache.png)

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB Cloudコンソール](https://tidbcloud.com/)の[**モニタリング**](/tidb-cloud/built-in-monitoring.md)ページで、 `Queries Using Plan Cache OPS`メトリクスをチェックして、すべての TiDB インスタンスで 1 秒あたりのプラン キャッシュを使用または欠落しているクエリの数を取得できます。

</CustomContent>

---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
aliases: ['/tidb/v5.4/sql-prepare-plan-cache','/tidb/stable/sql-prepare-plan-cache']
---

# SQL準備実行プランキャッシュ {#sql-prepare-execution-plan-cache}

TiDBは、 `Prepare`クエリと`Execute`クエリの実行プランのキャッシュをサポートしています。これには、準備されたステートメントの両方の形式が含まれます。

-   `COM_STMT_PREPARE`および`COM_STMT_EXECUTE`プロトコル機能を使用します。
-   SQLステートメント`PREPARE`および`EXECUTE`を使用します。

TiDBオプティマイザは、これら2つのタイプのクエリを同じ方法で処理します。準備時に、パラメータ化されたクエリがAST（抽象構文木）に解析され、キャッシュされます。後の実行では、保存されたASTと特定のパラメータ値に基づいて実行プランが生成されます。

実行プランキャッシュが有効になっている場合、最初の実行で`Prepare`ステートメントごとに、現在のクエリが実行プランキャッシュを使用できるかどうかを確認し、クエリで使用できる場合は、生成された実行プランをLRUによって実装されたキャッシュに配置します（最近使用済み）リンクリスト。後続の`Execute`のクエリでは、実行プランがキャッシュから取得され、可用性がチェックされます。チェックが成功すると、実行プランを生成するステップはスキップされます。それ以外の場合、実行プランは再生成され、キャッシュに保存されます。

現在のバージョンのTiDBでは、 `Prepare`のステートメントが次の条件のいずれかを満たす場合、クエリまたはプランはキャッシュされません。

-   `Union`には、 `SELECT` 、および`UPDATE` `Except`のSQL `Intersect`が含まれて`INSERT` `DELETE` 。
-   クエリは、パーティションテーブルまたは一時テーブル、あるいは生成された列を含むテーブルにアクセスします。
-   クエリには、 `select * from t where a > (select ...)`などのサブクエリが含まれています。
-   クエリには、 `select /*+ ignore_plan_cache() */ * from t`などの`ignore_plan_cache`のヒントが含まれています。
-   クエリには、 `select * from t where a>? and b>@x`などの`?`以外の変数（システム変数またはユーザー定義変数を含む）が含まれています。
-   `row_count`には、キャッシュできない関数が`version`れて`current_role` `current_user` `last_insert_id` `database()` `like` `connection_id` `user` 。
-   クエリには、 `Limit ?`や`Limit 10, ?`など、 `Limit`の後に`?`が含まれます。 `?`の特定の値はクエリのパフォーマンスに大きな影響を与えるため、このようなクエリはキャッシュされません。
-   クエリには、 `Order By ?`のように`Order By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータを並べ替えます。異なる列を対象とするクエリが同じ実行プランを使用している場合、結果は正しくありません。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Order By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには、 `Group By?`のように`Group By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列を対象とするクエリが同じ実行プランを使用している場合、結果は正しくありません。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Group By a+?`などの一般的なクエリである場合は、キャッシュされます。
-   クエリには、 `(partition by year order by sale rows ? preceding)`などの`Window Frame`ウィンドウ関数の定義に`?`が含まれています。ウィンドウ関数の他の場所に`?`が表示されている場合、クエリはキャッシュされます。
-   クエリには、 `c_int >= ?`や`c_int in (?, ?)`などの`int`と`string`を比較するためのパラメータが含まれています。ここで、 `?`は`set @x='123'`などの文字列タイプを示します。クエリ結果がMySQLと互換性があることを確認するには、各クエリでパラメータを調整して、そのようなクエリがキャッシュされないようにする必要があります。
-   プランは`TiFlash`にアクセスしようとします。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメーターがない場合を除き、 `TableDual`を含むプランはキャッシュされません。

`Prepare`はセッション間で実行できないため、LRUリンクリストはセッションレベルのキャッシュとして設計されてい`Execute` 。 LRUリストの各要素は、キーと値のペアです。値は実行プランであり、キーは次の部分で構成されています。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`ステートメントの識別子、つまり`PREPARE`キーワードの後の名前
-   現在のスキーマバージョン。これは、DDLステートメントが正常に実行されるたびに更新されます。
-   実行時のSQLモード`Execute`
-   `time_zone`システム変数の値である現在のタイムゾーン
-   `sql_select_limit`システム変数の値

上記の情報の変更（たとえば、データベースの切り替え、 `Prepare`ステートメントの名前変更、DDLステートメントの実行、SQLモード/ `time_zone`の値の変更）、またはLRUキャッシュ除去メカニズムにより、実行時に実行プランのキャッシュミスが発生します。

実行プランキャッシュがキャッシュから取得された後、TiDBは最初に実行プランがまだ有効かどうかをチェックします。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照されるテーブルがトランザクションのpre-orderステートメントで変更された場合、このテーブルにアクセスするキャッシュされた実行プランに`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行プランのスキャン範囲が現在のパラメータ値に従って調整され、データクエリの実行に使用されます。

実行プランのキャッシュとクエリのパフォーマンスについては、注目に値する点がいくつかあります。

-   実行プランがキャッシュされているかどうかに関係なく、SQLバインディングの影響を受けます。キャッシュされていない実行プラン（最初の`Execute` ）の場合、これらのプランは既存のSQLバインディングの影響を受けます。キャッシュされた実行プランの場合、新しいSQLバインディングが作成されると、これらのプランは無効になります。
-   キャッシュされたプランは、統計、最適化ルール、および式によるブロックリストのプッシュダウンの変更による影響を受けません。
-   `Execute`のパラメーターが異なることを考慮すると、実行プランキャッシュは、適応性を確保するために特定のパラメーター値に密接に関連するいくつかの積極的なクエリ最適化メソッドを禁止します。これにより、クエリプランが特定のパラメータ値に対して最適でない場合があります。たとえば、クエリのフィルター条件は`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメーターはそれぞれ`2`と`1`です。これらの2つのパラメーターが次の実行時に`1`と`2`になる可能性があることを考慮すると、オプティマイザーは現在のパラメーター値に固有の最適`TableDual`実行プランを生成しません。
-   キャッシュの無効化と削除が考慮されていない場合、実行プランキャッシュはさまざまなパラメータ値に適用され、理論的には特定の値に対して最適でない実行プランが発生します。たとえば、フィルター条件が`where a < ?`で、最初の実行に使用されるパラメーター値が`1`の場合、オプティマイザーは最適な`IndexScan`実行プランを生成し、それをキャッシュに入れます。以降の実行では、値が`10000`になった場合、 `TableScan`プランの方が適している可能性があります。ただし、実行プランキャッシュにより、以前に生成された`IndexScan`が実行に使用されます。したがって、実行プランキャッシュは、クエリが単純で（コンパイルの比率が高い）、実行プランが比較的固定されているアプリケーションシナリオに適しています。

現在、実行プランのキャッシュはデフォルトで無効になっています。この機能を有効にするには、TiDB構成ファイルで[`prepared-plan-cache`](/tidb-configuration-file.md#prepared-plan-cache)を有効にします。

> **ノート：**
>
> 実行プランのキャッシュ機能は`Prepare` `Execute`にのみ適用され、通常のクエリには有効になりません。

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

実行プランキャッシュが原因で`Prepare`の特定のセットが予期しない動作をすることがわかった場合は、 `Execute` SQLヒントを使用して、現在のステートメントの実行プランキャッシュの使用をスキップでき`ignore_plan_cache()` 。それでも、例として上記のステートメントを使用してください。

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

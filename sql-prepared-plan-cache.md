---
title: SQL Prepare Execution Plan Cache
summary: Learn about SQL Prepare Execution Plan Cache in TiDB.
aliases: ['/tidb/v5.4/sql-prepare-plan-cache','/tidb/stable/sql-prepare-plan-cache']
---

# SQL 準備実行計画キャッシュ {#sql-prepare-execution-plan-cache}

TiDB は、 `Prepare`および`Execute`クエリの実行プランのキャッシュをサポートしています。これには、プリペアド ステートメントの両方の形式が含まれます。

-   `COM_STMT_PREPARE`および`COM_STMT_EXECUTE`プロトコル機能の使用。
-   SQL ステートメント`PREPARE`および`EXECUTE`を使用します。

TiDB オプティマイザは、これら 2 種類のクエリを同じ方法で処理します。準備時に、パラメータ化されたクエリは AST (Abstract Syntax Tree) に解析され、キャッシュされます。後の実行では、保存された AST と特定のパラメータ値に基づいて実行計画が生成されます。

実行プラン キャッシュが有効な場合、最初の実行で`Prepare`ステートメントごとに、現在のクエリが実行プラン キャッシュを使用できるかどうかがチェックされ、クエリがそれを使用できる場合は、生成された実行プランが LRU (Least Recent) によって実装されたキャッシュに入れられます。使用) リンクされたリスト。後続の`Execute`のクエリでは、実行プランがキャッシュから取得され、可用性がチェックされます。チェックが成功した場合、実行計画を生成するステップはスキップされます。それ以外の場合は、実行計画が再生成され、キャッシュに保存されます。

現在のバージョンの TiDB では、 `Prepare`ステートメントが次の条件のいずれかを満たす場合、クエリまたはプランはキャッシュされません。

-   クエリに`SELECT` 、 `UPDATE` 、 `INSERT` 、 `DELETE` 、 `Union` 、 `Intersect` 、および`Except`以外の SQL ステートメントが含まれています。
-   クエリは、パーティション テーブルまたは一時テーブル、または生成された列を含むテーブルにアクセスします。
-   クエリには、 `select * from t where a > (select ...)`などのサブクエリが含まれています。
-   クエリには、 `select /*+ ignore_plan_cache() */ * from t`などの`ignore_plan_cache`ヒントが含まれています。
-   クエリに、 `select * from t where a>? and b>@x`などの`?`以外の変数 (システム変数またはユーザー定義変数を含む) が含まれています。
-   クエリには、キャッシュできない関数が含まれています: `database()` 、 `current_user` 、 `current_role` 、 `user` 、 `connection_id` 、 `last_insert_id` 、 `row_count` 、 `version` 、および`like` 。
-   クエリには、 `Limit ?`や`Limit 10, ?`など、 `Limit`の後に`?`が含まれます。特定の値`?`がクエリのパフォーマンスに大きな影響を与えるため、このようなクエリはキャッシュされません。
-   クエリには、 `Order By ?`など、 `Order By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータを並べ替えます。異なる列をターゲットとするクエリが同じ実行プランを使用する場合、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Order By a+?`などの一般的なものである場合は、キャッシュされます。
-   クエリには、 `Group By?`など、 `Group By`の後に`?`が含まれます。このようなクエリは、 `?`で指定された列に基づいてデータをグループ化します。異なる列をターゲットとするクエリが同じ実行プランを使用する場合、結果は間違ったものになります。したがって、そのようなクエリはキャッシュされません。ただし、クエリが`Group By a+?`などの一般的なものである場合は、キャッシュされます。
-   クエリには、ウィンドウ関数`Window Frame`の定義に`(partition by year order by sale rows ? preceding)`などの`?`が含まれています。ウィンドウ関数の他の場所に`?`が表示される場合、クエリはキャッシュされます。
-   クエリには、 `int`と`string`を比較するためのパラメーター ( `c_int >= ?`や`c_int in (?, ?)`など) が含まれ、 `?`は`set @x='123'`などの文字列型を示します。クエリ結果が MySQL と互換性があることを確認するには、各クエリでパラメーターを調整する必要があるため、そのようなクエリはキャッシュされません。
-   プランは`TiFlash`へのアクセスを試みます。
-   ほとんどの場合、現在の`Prepare`ステートメントにパラメーターがない場合を除き、 `TableDual`を含むプランはキャッシュされません。

`Prepare` / `Execute`はセッション間で実行できないため、LRU リンク リストはセッション レベルのキャッシュとして設計されています。 LRU リストの各要素は、キーと値のペアです。値は実行計画で、キーは次の部分で構成されます。

-   `Execute`が実行されるデータベースの名前
-   `Prepare`ステートメントの識別子、つまり`PREPARE`キーワードの後の名前
-   DDL ステートメントが正常に実行されるたびに更新される現在のスキーマ バージョン
-   実行時のSQLモード`Execute`
-   `time_zone`システム変数の値である現在のタイムゾーン
-   `sql_select_limit`システム変数の値

上記の情報の変更 (たとえば、データベースの切り替え、 `Prepare`のステートメントの名前変更、DDL ステートメントの実行、SQL モード / `time_zone`の値の変更)、または LRU キャッシュ除去メカニズムにより、実行時に実行プランのキャッシュ ミスが発生します。

実行計画キャッシュがキャッシュから取得された後、TiDB は最初に実行計画がまだ有効かどうかをチェックします。現在の`Execute`ステートメントが明示的なトランザクションで実行され、参照されるテーブルがトランザクションの pre-order ステートメントで変更された場合、このテーブルにアクセスするキャッシュされた実行プランには`UnionScan`演算子が含まれていないため、実行できません。

検証テストに合格すると、実行計画のスキャン範囲が現在のパラメーター値に応じて調整され、データ クエリの実行に使用されます。

実行計画のキャッシュとクエリのパフォーマンスについて、注目すべき点がいくつかあります。

-   実行計画がキャッシュされているかどうかに関係なく、SQL バインディングの影響を受けます。キャッシュされていない実行計画 (最初の`Execute` ) の場合、これらの計画は既存の SQL バインディングの影響を受けます。キャッシュされた実行計画の場合、新しい SQL バインディングが作成されると、これらの計画は無効になります。
-   キャッシュされたプランは、統計、最適化ルール、および式によるブロックリスト プッシュダウンの変更の影響を受けません。
-   `Execute`のパラメーターが異なることを考慮して、実行プラン キャッシュは、適応性を確保するために、特定のパラメーター値に密接に関連するいくつかの積極的なクエリ最適化メソッドを禁止します。これにより、クエリ プランが特定のパラメーター値に対して最適でない場合があります。たとえば、クエリのフィルター条件は`where a > ? And a < ?`で、最初の`Execute`ステートメントのパラメーターはそれぞれ`2`と`1`です。これら 2 つのパラメーターが次回の実行時に`1`と`2`になる可能性があることを考慮すると、オプティマイザーは現在のパラメーター値に固有の最適な`TableDual`実行計画を生成しません。
-   キャッシュの無効化と削除が考慮されていない場合、実行計画のキャッシュがさまざまなパラメータ値に適用され、理論的には、特定の値に対して最適でない実行計画が発生します。たとえば、フィルタ条件が`where a < ?`で、最初の実行に使用されるパラメータ値が`1`の場合、オプティマイザは最適な`IndexScan`実行計画を生成してキャッシュに入れます。その後の実行で、値が`10000`になった場合は、 `TableScan`のプランの方が優れている可能性があります。ただし、実行計画のキャッシュにより、以前に生成された`IndexScan`が実行に使用されます。したがって、実行プラン キャッシュは、クエリが単純で (コンパイルの比率が高く)、実行プランが比較的固定されているアプリケーション シナリオにより適しています。

<CustomContent platform="tidb">

現在、実行計画のキャッシュはデフォルトで無効になっています。この機能を有効にするには、TiDB 構成ファイルで[`prepared-plan-cache`](/tidb-configuration-file.md#prepared-plan-cache)を有効にします。

</CustomContent>

<CustomContent platform="tidb-cloud">

v6.1.0 以降、実行計画キャッシュはデフォルトで有効になっています。システム変数[`tidb_enable_prepared_plan_cache`](https://docs.pingcap.com/tidb/stable/system-variables#tidb_enable_prepared_plan_cache-new-in-v610)を介して、準備されたプランのキャッシュを制御できます。

TiDB v5.4 では、実行プランのキャッシュはデフォルトで無効になっています。 v5.4 でこの機能を使用するには、 [PingCAP テクニカル サポート](/tidb-cloud/tidb-cloud-support.md)に連絡する必要があります。

</CustomContent>

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

---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
---

# SQL計画管理（SPM） {#sql-plan-management-spm}

SQLプラン管理は、SQLバインディングを実行して、SQL実行プランを手動で妨害する一連の関数です。これらの機能には、SQLバインディング、ベースラインキャプチャ、およびベースライン進化が含まれます。

## SQLバインディング {#sql-binding}

SQLバインディングはSPMの基礎です。 [オプティマイザーのヒント](/optimizer-hints.md)のドキュメントでは、ヒントを使用して特定の実行プランを選択する方法を紹介しています。ただし、SQLステートメントを変更せずに実行の選択を妨害する必要がある場合があります。 SQLバインディングを使用すると、SQLステートメントを変更せずに指定された実行プランを選択できます。

### バインディングを作成する {#create-a-binding}

{{< copyable "" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

このステートメントは、SQL実行プランをGLOBALまたはSESSIONレベルでバインドします。現在、 `SELECT` `DELETE` `SELECT` `INSERT` `REPLACE`れて`UPDATE`ます。

具体的には、これらのステートメントの2つのタイプは、構文の競合のために実行プランにバインドできません。次の例を参照してください。

```sql
-- Type one: Statements that get the Cartesian product by using the `join` keyword and not specifying the associated columns with the `using` keyword.
create global binding for
    select * from t t1 join t t2
using
    select * from t t1 join t t2;

-- Type two: `DELETE` statements that contain the `using` keyword.
create global binding for
    delete from t1 using t1 join t2 on t1.a = t2.a
using
    delete from t1 using t1 join t2 on t1.a = t2.a;
```

同等のステートメントを使用することで、構文の競合を回避できます。たとえば、上記のステートメントを次のように書き直すことができます。

```sql
-- First rewrite of type one statements: Add a `using` clause for the `join` keyword.
create global binding for
    select * from t t1 join t t2 using (a)
using
    select * from t t1 join t t2 using (a);

-- Second rewrite of type one statements: Delete the `join` keyword.
create global binding for
    select * from t t1, t t2
using
    select * from t t1, t t2;

-- Rewrite of type two statements: Remove the `using` keyword from the `delete` statement.
create global binding for
    delete t1 from t1 join t2 on t1.a = t2.a
using
    delete t1 from t1 join t2 on t1.a = t2.a;
```

> **ノート：**
>
> `SELECT` `REPLACE`サブクエリを含む`INSERT`ステートメントの実行プランバインディングを作成する場合、 `INSERT` / `REPLACE`キーワードの後ではなく、 `SELECT`サブクエリでバインドするオプティマイザヒントを指定する必要があります。そうしないと、オプティマイザのヒントが意図したとおりに有効になりません。

次に2つの例を示します。

```sql
-- The hint takes effect in the following statement.
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert into t1 select /*+ use_index(@sel_1 t2, a) */ * from t2 where a > 1 and b = 1;

-- The hint cannot take effect in the following statement.
create global binding for
    insert into t1 select * from t2 where a > 1 and b = 1
using
    insert /*+ use_index(@sel_1 t2, a) */ into t1 select * from t2 where a > 1 and b = 1;
```

実行プランバインディングを作成するときにスコープを指定しない場合、デフォルトのスコープはSESSIONです。 TiDBオプティマイザは、バインドされたSQLステートメントを正規化し、それらをシステムテーブルに格納します。 SQLクエリを処理するときに、正規化されたステートメントがシステムテーブル内のバインドされたSQLステートメントの1つと一致し、システム変数`tidb_use_plan_baselines`が`on` （デフォルト値は`on` ）に設定されている場合、TiDBはこのステートメントに対応するオプティマイザーヒントを使用します。一致する実行プランが複数ある場合、オプティマイザーはバインドするのに最もコストのかからないプランを選択します。

`Normalization`は、SQLステートメントの定数を変数パラメーターに変換し、SQLステートメントのスペースと改行の標準化された処理を使用して、クエリで参照されるテーブルのデータベースを明示的に指定するプロセスです。次の例を参照してください。

```sql
select * from t where a >    1
-- After normalization, the above statement is as follows:
select * from test . t where a > ?
```

> **ノート：**
>
> コンマ`,`で結合された複数の定数は、 `?`ではなく`...`として正規化されます。
>
> 例えば：
>
> ```sql
> select * from t limit 10
> select * from t limit 10, 20
> select * from t where a in (1)
> select * from t where a in (1,2,3)
> -- After normalization, the above statements are as follows:
> select * from test . t limit ?
> select * from test . t limit ...
> select * from test . t where a in ( ? )
> select * from test . t where a in ( ... )
> ```
>
> バインディングが作成されると、TiDBは、単一の定数を含むSQLステートメントと、コンマで結合された複数の定数を含むSQLステートメントを異なる方法で処理します。したがって、2つのSQLタイプのバインディングを別々に作成する必要があります。

SQLステートメントがGLOBALスコープとSESSIONスコープの両方で実行プランをバインドしている場合、オプティマイザーはSESSIONバインディングに遭遇すると、GLOBALスコープでバインドされた実行プランを無視するため、SESSIONスコープでのこのステートメントのバインドされた実行プランは、 GLOBALスコープ。

例えば：

```sql
--  Creates a GLOBAL binding and specifies using `sort merge join` in this binding.
create global binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ merge_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- The execution plan of this SQL statement uses the `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;

-- Creates another SESSION binding and specifies using `hash join` in this binding.
create binding for
    select * from t1, t2 where t1.id = t2.id
using
    select /*+ hash_join(t1, t2) */ * from t1, t2 where t1.id = t2.id;

-- In the execution plan of this statement, `hash join` specified in the SESSION binding is used, instead of `sort merge join` specified in the GLOBAL binding.
explain select * from t1, t2 where t1.id = t2.id;
```

最初の`select`のステートメントが実行されているとき、オプティマイザーはGLOBALスコープのバインディングを介してステートメントに`sm_join(t1, t2)`のヒントを追加します。 `explain`の結果の実行プランの最上位ノードはMergeJoinです。 2番目の`select`ステートメントが実行されているとき、オプティマイザーはGLOBALスコープのバインディングの代わりにSESSIONスコープのバインディングを使用し、ステートメントに`hash_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行プランの最上位ノードはHashJoinです。

標準化された各SQLステートメントは、一度に`CREATE BINDING`つを使用して作成されたバインディングを1つだけ持つことができます。同じ標準化されたSQLステートメントに対して複数のバインディングが作成されると、最後に作成されたバインディングが保持され、以前のすべてのバインディング（作成および展開）は削除済みとしてマークされます。ただし、セッションバインディングとグローバルバインディングは共存でき、このロジックの影響を受けません。

さらに、バインディングを作成する場合、TiDBはセッションがデータベースコンテキストにあることを要求します。つまり、クライアントが接続されたとき、または`use ${database}`が実行されたときにデータベースが指定されます。

元のSQLステートメントとバインドされたステートメントは、正規化とヒントの削除後に同じテキストである必要があります。そうでない場合、バインドは失敗します。次の例を見てください。

-   パラメータ化とヒントの削除の前後のテキストが同じであるため、このバインディングは正常に作成できます`select * from test . t where a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   元のSQLステートメントは`select * from test . t where a > ?`として処理されるのに対し、バインドされたSQLステートメントは`select * from test . t where b > ?`として処理されるため、このバインドは失敗します。

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
drop session binding for select * from t1, t2 where t1.id = t2.id;

-- Views the SQL execution plan again.
explain select * from t1,t2 where t1.id = t2.id;
```

上記の例では、SESSIONスコープのドロップされたバインディングは、GLOBALスコープの対応するバインディングをシールドします。オプティマイザは、ステートメントに`sm_join(t1, t2)`のヒントを追加しません。 `explain`の結果の実行プランの最上位ノードは、このヒントによってMergeJoinに固定されていません。代わりに、コスト見積もりに従って、オプティマイザによって最上位ノードが個別に選択されます。

> **ノート：**
>
> `DROP GLOBAL BINDING`を実行すると、現在のtidb-serverインスタンスキャッシュのバインディングが削除され、システムテーブルの対応する行のステータスが「削除済み」に変更されます。他のtidb-serverインスタンスは、対応するバインディングをキャッシュにドロップするために「削除済み」ステータスを読み取る必要があるため、このステートメントはシステムテーブルのレコードを直接削除しません。ステータスが「削除済み」のこれらのシステムテーブルのレコードの場合、100 `bind-info-lease` （デフォルト値は`3s` 、合計`300s` ）間隔ごとに、バックグラウンドスレッドが10より前の`update_time`のバインディングを再利用およびクリアする操作をトリガーします。 `bind-info-lease` （すべてのtidb-serverインスタンスが「削除済み」ステータスを読み取り、キャッシュを更新したことを確認するため）。

### バインディングを表示 {#view-binding}

{{< copyable "" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

このステートメントは、実行プランのバインディングを、最新から最早までのバインディング更新時間の順序に従って、GLOBALまたはSESSIONレベルで出力します。デフォルトのスコープはSESSIONです。現在、以下に示すように、 `SHOW BINDINGS`は8つの列を出力します。

| 列名           | ノート                                                                                                                                             |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| original_sql | パラメータ化後の元のSQLステートメント                                                                                                                            |
| bind_sql     | ヒント付きのバインドされたSQLステートメント                                                                                                                         |
| default_db   | デフォルトのデータベース                                                                                                                                    |
| 状態           | 使用中、削除済み、無効、拒否済み、保留中の確認などのステータス                                                                                                                 |
| create_time  | 時間を作る                                                                                                                                           |
| update_time  | 更新時間                                                                                                                                            |
| 文字コード        | キャラクターセット                                                                                                                                       |
| 照合順序         | 注文ルール                                                                                                                                           |
| ソース          | `manual` （ `create [global] binding` SQLステートメントによって作成される）、 `capture` （TiDBによって自動的にキャプチャされる）、および`evolve` （TiDBによって自動的に展開される）を含む、バインディングが作成される方法。 |

### バインディングのトラブルシューティング {#troubleshoot-binding}

{{< copyable "" >}}

```sql
SELECT @@[SESSION.]last_plan_from_binding;
```

このステートメントは、システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)を使用して、最後に実行されたステートメントで使用された実行プランがバインディングからのものであるかどうかを示します。

さらに、 `explain format = 'verbose'`ステートメントを使用してSQLステートメントのクエリプランを表示するときに、SQLステートメントがバインディングを使用している場合、 `explain`ステートメントは警告を返します。この状況では、警告メッセージを確認して、SQLステートメントで使用されているバインディングを確認できます。

```sql
-- Create a global binding.

create global binding for
    select * from t
using
    select * from t;

-- Use the `explain format = 'verbose'` statement to check the SQL execution plan. Check the warning message to view the binding used in the query.

explain format = 'verbose' select * from t;
show warnings;
```

## ベースラインキャプチャ {#baseline-capturing}

ベースラインキャプチャを有効にするには、 `tidb_capture_plan_baselines`を設定し`on` 。デフォルト値は`off`です。

> **ノート：**
>
> 自動バインディング作成機能は[ステートメントの要約](/statement-summary-tables.md)に依存しているため、自動バインディングを使用する前に、必ずステートメントの概要を有効にしてください。

自動バインディング作成を有効にすると、ステートメントの概要の履歴SQLステートメントが`bind-info-lease`ごとにトラバースされ（デフォルト値は`3s` ）、少なくとも2回表示されるSQLステートメントのバインディングが自動的に作成されます。これらのSQLステートメントの場合、TiDBはステートメントの概要に記録されている実行プランを自動的にバインドします。

ただし、TiDBは、次のタイプのSQLステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`および`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`のクエリなど、TiDBで内部的に実行されるSQLステートメント。
-   手動で作成された実行プランにバインドされているSQLステートメント。

`PREPARE`ステートメントおよびバイナリプロトコルで実行されるクエリの場合、 `EXECUTE` `EXECUTE` `PREPARE`はなく、実際のクエリステートメントのバインディングを自動的にキャプチャします。

> **ノート：**
>
> TiDBにはいくつかの機能の正確さを保証するためにいくつかの埋め込みSQLステートメントがあるため、ベースラインキャプチャはデフォルトでこれらのSQLステートメントを自動的にシールドします。

## ベースラインの進化 {#baseline-evolution}

ベースラインの進化は、TiDBv4.0で導入されたSPMの重要な機能です。

データが更新されると、以前にバインドされた実行プランが最適でなくなる可能性があります。ベースライン進化機能は、バインドされた実行プランを自動的に最適化できます。

さらに、ベースラインの進化は、統計情報の変更によって引き起こされる実行計画にもたらされるジッターをある程度回避することもできます。

### 使用法 {#usage}

次のステートメントを使用して、自動バインディングエボリューションを有効にします。

{{< copyable "" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

デフォルト値の`tidb_evolve_plan_baselines`は`off`です。

> **警告：**
>
> -   ベースラインの進化は実験的特徴です。未知のリスクが存在する可能性があります。実稼働環境で使用することはお勧めし**ません**。
> -   この変数は、ベースライン進化機能が一般的に利用可能になるまで（GA）、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。この機能を実稼働環境ですでに使用している場合は、できるだけ早く無効にしてください。バインディングステータスが期待どおりでない場合は、PingCAPのテクニカルサポートに問い合わせてください。

自動バインディングエボリューション機能を有効にした後、オプティマイザーによって選択された最適な実行プランがバインディング実行プランに含まれていない場合、オプティマイザーはそのプランを検証を待機する実行プランとしてマークします。 `bind-info-lease` （デフォルト値は`3s` ）間隔ごとに、検証される実行プランが選択され、実際の実行時間の点でコストが最も低いバインディング実行プランと比較されます。検証対象のプランの実行時間が短い場合（現在の比較基準では、検証対象のプランの実行時間がバインディング実行プランの実行時間の2/3以下である）、このプランは使用可能としてマークされます。バインディング。次の例では、上記のプロセスについて説明します。

表`t`が次のように定義されていると仮定します。

{{< copyable "" >}}

```sql
create table t(a int, b int, key(a), key(b));
```

表`t`で次のクエリを実行します。

{{< copyable "" >}}

```sql
select * from t where a < 100 and b < 100;
```

上で定義されたテーブルでは、 `a < 100`の条件を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザは、インデックス`a`を使用する最適な実行プランではなく、誤って全表スキャンを選択します。最初に次のステートメントを使用してバインディングを作成できます。

{{< copyable "" >}}

```sql
create global binding for select * from t where a < 100 and b < 100 using select * from t use index(a) where a < 100 and b < 100;
```

上記のクエリが再度実行されると、オプティマイザはインデックス`a` （上記で作成されたバインディングの影響を受けます）を選択して、クエリ時間を短縮します。

表`t`で挿入と削除が実行されると、 `a < 100`の条件を満たす行の数が増え、 `b < 100`の条件を満たす行の数が減ると仮定します。現時点では、バインディングの下でインデックス`a`を使用することは、もはや最適な計画ではない可能性があります。

バインディングの進化は、この種の問題に対処できます。オプティマイザは、テーブル内のデータの変更を認識すると、インデックス`b`を使用するクエリの実行プランを生成します。ただし、現在のプランのバインディングが存在するため、このクエリプランは採用および実行されません。代わりに、このプランはバックエンドの進化リストに保存されます。展開プロセス中に、このプランの実行時間が、インデックス`a`を使用する現在の実行プランよりも明らかに短いことが確認された場合、インデックス`b`が使用可能なバインディングリストに追加されます。この後、クエリが再度実行されると、オプティマイザは最初にインデックス`b`を使用する実行プランを生成し、このプランがバインディングリストに含まれていることを確認します。次に、オプティマイザーはこのプランを採用して実行し、データ変更後のクエリ時間を短縮します。

自動進化がクラスターに与える影響を減らすには、次の構成を使用します。

-   各実行プランの最大実行時間を制限するには、 `tidb_evolve_plan_task_max_time`を設定します。デフォルト値は`600s`です。実際の検証プロセスでは、最大実行時間も検証された実行計画の2倍以下に制限されます。
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

    select @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it. 

    set global tidb_evolve_plan_baselines = off;
    ```

-   v4.0から現在のバージョンにアップグレードする前に、使用可能なSQLバインディングに対応するすべてのクエリの構文が新しいバージョンで正しいかどうかを確認する必要があります。構文エラーが存在する場合は、対応するSQLバインディングを削除します。これを行うには、次の手順を実行します。

    {{< copyable "" >}}

    ```sql
    -- Check the query corresponding to the available SQL binding in the version to be upgraded.

    select bind_sql from mysql.bind_info where status = 'using';

    -- Verify the result from the above SQL query in the test environment of the new version. 

    bind_sql_0;
    bind_sql_1;
    ...

    -- In the case of a syntax error (ERROR 1064 (42000): You have an error in your SQL syntax), delete the corresponding binding. 
    -- For any other errors (for example, tables are not found), it means that the syntax is compatible. No other operation is needed. 
    ```

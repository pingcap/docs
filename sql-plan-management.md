---
title: SQL Plan Management (SPM)
summary: Learn about SQL Plan Management in TiDB.
---

# SQL 計画管理 (SPM) {#sql-plan-management-spm}

SQL Plan Management は、SQL バインディングを実行して手動で SQL 実行計画に干渉する関数のセットです。これらの関数には、SQL バインディング、ベースライン キャプチャ、およびベースライン展開が含まれます。

## SQL バインディング {#sql-binding}

SQL バインディングは SPM の基礎です。 [オプティマイザーのヒント](/optimizer-hints.md)ドキュメントでは、ヒントを使用して特定の実行プランを選択する方法を紹介します。ただし、SQL ステートメントを変更せずに実行の選択に干渉する必要がある場合があります。 SQL バインディングを使用すると、SQL ステートメントを変更せずに、指定された実行計画を選択できます。

### バインディングを作成する {#create-a-binding}

{{< copyable "" >}}

```sql
CREATE [GLOBAL | SESSION] BINDING FOR BindableStmt USING BindableStmt
```

このステートメントは、SQL 実行計画を GLOBAL または SESSION レベルでバインドします。現在、TiDB でサポートされているバインド可能な SQL ステートメント (BindableStmt) には、 `SELECT`のサブクエリを持つ`SELECT` 、 `DELETE` 、 `UPDATE` 、および`INSERT` / `REPLACE`が含まれます。

具体的には、これらの 2 つのタイプのステートメントは、構文の競合のために実行プランにバインドできません。次の例を参照してください。

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

同等のステートメントを使用して、構文の競合を回避できます。たとえば、上記のステートメントを次のように書き換えることができます。

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
> `SELECT`のサブクエリを持つ`INSERT` / `REPLACE`ステートメントの実行プラン バインディングを作成する場合、 `INSERT` / `REPLACE`キーワードの後ではなく、 `SELECT`のサブクエリでバインドするオプティマイザ ヒントを指定する必要があります。そうしないと、オプティマイザーのヒントが意図したとおりに機能しません。

以下に 2 つの例を示します。

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

実行計画バインディングの作成時にスコープを指定しない場合、デフォルトのスコープは SESSION です。 TiDB オプティマイザーは、バインドされた SQL ステートメントを正規化し、システム テーブルに格納します。 SQL クエリを処理するときに、正規化されたステートメントがシステム テーブル内のバインドされた SQL ステートメントの 1 つと一致し、システム変数`tidb_use_plan_baselines`が`on` (デフォルト値は`on` ) に設定されている場合、TiDB はこのステートメントに対応するオプティマイザー ヒントを使用します。一致する実行計画が複数ある場合、オプティマイザは最もコストの低い実行計画を選択してバインドします。

`Normalization`は、SQL ステートメント内の定数を変数パラメーターに変換し、SQL ステートメント内のスペースと改行に関する標準化された処理を使用して、クエリで参照されるテーブルのデータベースを明示的に指定するプロセスです。次の例を参照してください。

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
> バインディングが作成されると、TiDB は単一の定数を含む SQL ステートメントと、コンマで結合された複数の定数を含む SQL ステートメントを異なる方法で扱います。したがって、2 つの SQL タイプのバインディングを個別に作成する必要があります。

SQL ステートメントが GLOBAL スコープと SESSION スコープの両方でバインドされた実行計画を持っている場合、オプティマイザは SESSION バインディングに遭遇したときに GLOBAL スコープでバインドされた実行計画を無視するため、SESSION スコープでこのステートメントのバインドされた実行計画は実行計画を保護します。グローバルスコープ。

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

最初の`select`ステートメントが実行されると、オプティマイザーは GLOBAL スコープのバインディングを介してステートメントに`sm_join(t1, t2)`ヒントを追加します。 `explain`番目の結果の実行計画の最上位ノードは MergeJoin です。 2 番目の`select`ステートメントが実行されると、オプティマイザーは GLOBAL スコープのバインディングではなく SESSION スコープのバインディングを使用し、ステートメントに`hash_join(t1, t2)`ヒントを追加します。 `explain`の結果の実行計画のトップノードはHashJoinです。

標準化された各 SQL ステートメントは、一度に`CREATE BINDING`つを使用して作成されたバインディングを 1 つだけ持つことができます。同じ標準化された SQL ステートメントに対して複数のバインディングが作成されると、最後に作成されたバインディングが保持され、以前に作成されたすべてのバインディング (作成および展開されたもの) は削除済みとしてマークされます。ただし、セッション バインディングとグローバル バインディングは共存でき、このロジックの影響を受けません。

さらに、バインディングを作成するとき、TiDB はセッションがデータベース コンテキスト内にあることを要求します。つまり、クライアントが接続されたとき、または`use ${database}`が実行されたときにデータベースが指定されます。

元の SQL ステートメントとバインドされたステートメントは、正規化とヒントの削除後に同じテキストを持っている必要があります。そうでない場合、バインドは失敗します。次の例を見てください。

-   このバインドは、パラメーター化とヒントの削除の前後のテキストが同じであるため、正常に作成できます: `select * from test . t where a > ?`

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index  (idx) WHERE a > 2
    ```

-   元の SQL ステートメントは`select * from test . t where a > ?`として処理されるのに対し、バインドされた SQL ステートメントは`select * from test . t where b > ?`として異なる方法で処理されるため、このバインドは失敗します。

    ```sql
    CREATE BINDING FOR SELECT * FROM t WHERE a > 1 USING SELECT * FROM t use index(idx) WHERE b > 2
    ```

> **ノート：**
>
> `PREPARE` / `EXECUTE`ステートメントおよびバイナリ プロトコルで実行されるクエリの場合、 `PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントに対して実行プラン バインディングを作成する必要があります。

### バインディングを削除 {#remove-binding}

{{< copyable "" >}}

```sql
DROP [GLOBAL | SESSION] BINDING FOR BindableStmt;
```

このステートメントは、GLOBAL または SESSION レベルで指定された実行計画バインディングを削除します。デフォルトのスコープは SESSION です。

一般に、SESSION スコープのバインディングは、主にテストまたは特別な状況で使用されます。すべての TiDB プロセスでバインディングを有効にするには、GLOBAL バインディングを使用する必要があります。作成された SESSION バインディングは、セッションが終了する前に SESSION バインディングが削除された場合でも、SESSION が終了するまで対応する GLOBAL バインディングを保護します。この場合、バインディングは有効ではなく、プランはオプティマイザによって選択されます。

次の例は、SESSION バインディングが GLOBAL バインディングを保護する[バインディングを作成する](#create-a-binding)の例に基づいています。

```sql
-- Drops the binding created in the SESSION scope.
drop session binding for select * from t1, t2 where t1.id = t2.id;

-- Views the SQL execution plan again.
explain select * from t1,t2 where t1.id = t2.id;
```

上記の例では、SESSION スコープで削除されたバインドにより、GLOBAL スコープの対応するバインドがシールドされます。オプティマイザーは、ステートメントに`sm_join(t1, t2)`ヒントを追加しません。 `explain`結果の実行計画の最上位ノードは、このヒントによって MergeJoin に固定されません。代わりに、最上位ノードは、コスト見積もりに従って最適化プログラムによって個別に選択されます。

> **ノート：**
>
> `DROP GLOBAL BINDING`を実行すると、現在の tidb-server インスタンス キャッシュ内のバインディングが削除され、システム テーブル内の対応する行のステータスが「削除済み」に変更されます。このステートメントは、システム テーブル内のレコードを直接削除しません。他の tidb-server インスタンスは、キャッシュ内の対応するバインディングを削除するために「削除済み」ステータスを読み取る必要があるためです。これらのシステム テーブル内のステータスが「削除済み」のレコードの場合、100 `bind-info-lease` (デフォルト値は`3s`で、合計で`300s` ) の間隔ごとに、バックグラウンド スレッドは、10 より前に`update_time`のバインディングで回収およびクリアの操作をトリガーします。 `bind-info-lease` (すべての tidb-server インスタンスが「削除済み」ステータスを読み取り、キャッシュを更新したことを確認するため)。

### バインディングをビュー {#view-binding}

{{< copyable "" >}}

```sql
SHOW [GLOBAL | SESSION] BINDINGS [ShowLikeOrWhere]
```

このステートメントは、バインディングの更新時刻が新しいものから古いものへの順序に従って、GLOBAL または SESSION レベルで実行計画バインディングを出力します。デフォルトのスコープは SESSION です。現在、以下に示すように、 `SHOW BINDINGS`は 8 つの列を出力します。

| カラム名         | ノート                                                                                                                                               |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| original_sql | パラメータ化後の元の SQL ステートメント                                                                                                                            |
| bind_sql     | ヒント付きのバインドされた SQL ステートメント                                                                                                                         |
| default_db   | デフォルトのデータベース                                                                                                                                      |
| スターテス        | `using` 、 `deleted` 、 `invalid` 、 `rejected` 、および`pending verify`を含むステータス                                                                         |
| create_time  | 時を創る                                                                                                                                              |
| update_time  | 更新時間                                                                                                                                              |
| 文字コード        | キャラクターセット                                                                                                                                         |
| 照合順序         | 注文規則                                                                                                                                              |
| ソース          | `manual` ( `create [global] binding` SQL ステートメントによって作成される)、 `capture` (TiDB によって自動的にキャプチャされる)、および`evolve` (TiDB によって自動的に展開される) を含むバインディングが作成される方法 |

### バインディングのトラブルシューティング {#troubleshoot-binding}

{{< copyable "" >}}

```sql
SELECT @@[SESSION.]last_plan_from_binding;
```

このステートメントは、システム変数[`last_plan_from_binding`](/system-variables.md#last_plan_from_binding-new-in-v40)を使用して、最後に実行されたステートメントで使用された実行計画がバインディングからのものかどうかを示します。

さらに、 `explain format = 'verbose'`ステートメントを使用して SQL ステートメントのクエリ プランを表示する場合、SQL ステートメントがバインドを使用している場合、 `explain`ステートメントは警告を返します。この場合、警告メッセージを確認して、SQL ステートメントで使用されているバインディングを確認できます。

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

## ベースラインのキャプチャ {#baseline-capturing}

ベースラインのキャプチャを有効にするには、 `tidb_capture_plan_baselines`を`on`に設定します。デフォルト値は`off`です。

> **ノート：**
>
> 自動バインディング作成機能は[声明の要約](/statement-summary-tables.md)に依存しているため、自動バインディングを使用する前に必ず Statement Summary を有効にしてください。

バインディングの自動作成を有効にすると、Statement Summary の履歴 SQL ステートメントが`bind-info-lease`ごとにトラバースされ (デフォルト値は`3s` )、少なくとも 2 回出現する SQL ステートメントに対してバインディングが自動的に作成されます。これらの SQL ステートメントの場合、TiDB は Statement Summary に記録された実行計画を自動的にバインドします。

ただし、TiDB は、次のタイプの SQL ステートメントのバインディングを自動的にキャプチャしません。

-   `EXPLAIN`および`EXPLAIN ANALYZE`ステートメント。
-   統計情報を自動的にロードするために使用される`SELECT`クエリなど、TiDB で内部的に実行される SQL ステートメント。
-   手動で作成された実行計画にバインドされた SQL ステートメント。

`PREPARE` / `EXECUTE`ステートメントとバイナリ プロトコルで実行されるクエリの場合、TiDB は`PREPARE` / `EXECUTE`ステートメントではなく、実際のクエリ ステートメントのバインディングを自動的にキャプチャします。

> **ノート：**
>
> TiDB には一部の機能の正確性を確保するために SQL ステートメントが埋め込まれているため、ベースライン キャプチャはデフォルトでこれらの SQL ステートメントを自動的に保護します。

## ベースラインの進化 {#baseline-evolution}

ベースラインの進化は、TiDB v4.0 で導入された SPM の重要な機能です。

データが更新されると、以前にバインドされた実行計画が最適でなくなる可能性があります。ベースライン進化機能は、バインドされた実行計画を自動的に最適化できます。

さらに、ベースラインの進化は、統計情報の変更によって実行計画にもたらされるジッタをある程度回避することもできます。

### 使用法 {#usage}

自動バインディングの進化を有効にするには、次のステートメントを使用します。

{{< copyable "" >}}

```sql
set global tidb_evolve_plan_baselines = on;
```

`tidb_evolve_plan_baselines`のデフォルト値は`off`です。

> **警告：**
>
> -   ベースラインの進化は実験的機能です。未知のリスクが存在する可能性があります。本番環境で使用することはお勧めし**ません**。
> -   この変数は、ベースライン進化機能が一般に利用可能 (GA) になるまで、強制的に`off`に設定されます。この機能を有効にしようとすると、エラーが返されます。この機能を本番環境ですでに使用している場合は、できるだけ早く無効にしてください。バインド ステータスが期待どおりではないことがわかった場合は、PingCAP のテクニカル サポートに連絡してください。

自動バインディング進化機能が有効になった後、オプティマイザによって選択された最適な実行計画がバインディング実行計画に含まれていない場合、オプティマイザはその計画を検証を待つ実行計画としてマークします。 `bind-info-lease` (デフォルト値は`3s` ) 間隔ごとに、検証する実行計画が選択され、実際の実行時間に関して最小のコストを持つバインディング実行計画と比較されます。検証対象の計画の実行時間が短い場合 (現在の比較基準は、検証対象の計画の実行時間が拘束力のある実行計画の実行時間の 2/3 を超えないことです)、この計画は使用可能としてマークされます。バインディング。次の例では、上記のプロセスについて説明します。

表`t`が次のように定義されているとします。

{{< copyable "" >}}

```sql
create table t(a int, b int, key(a), key(b));
```

テーブル`t`に対して次のクエリを実行します。

{{< copyable "" >}}

```sql
select * from t where a < 100 and b < 100;
```

上で定義した表では、 `a < 100`の条件を満たす行はほとんどありません。しかし、何らかの理由で、オプティマイザーは、インデックス`a`を使用する最適な実行計画ではなく、誤って全テーブル スキャンを選択します。まず、次のステートメントを使用してバインディングを作成できます。

{{< copyable "" >}}

```sql
create global binding for select * from t where a < 100 and b < 100 using select * from t use index(a) where a < 100 and b < 100;
```

上記のクエリが再度実行されると、オプティマイザーはクエリ時間を短縮するためにインデックス`a` (上記で作成されたバインディングの影響を受ける) を選択します。

テーブル`t`で挿入と削除が実行されると、条件`a < 100`を満たす行数が増加し、条件`b < 100`を満たす行数が減少するとします。現時点では、バインディングでインデックス`a`を使用することは、最適な計画ではない可能性があります。

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

-   `read_from_storage`は、テーブルを読み取るときにTiFlashからデータを読み取るか、TiFlash からデータを読み取るかを指定するという点で、特別なヒントです。 TiDB は分離読み取りを提供するため、分離条件が変更された場合、このヒントは進化した実行計画に大きな影響を与えます。したがって、このヒントが最初に作成されたバインディングに存在する場合、TiDB はすべての進化したバインディングを無視します。

## アップグレードのチェックリスト {#upgrade-checklist}

クラスターのアップグレード中に、SQL Plan Management (SPM) が互換性の問題を引き起こし、アップグレードが失敗する可能性があります。アップグレードを確実に成功させるには、アップグレードの事前チェックに次のリストを含める必要があります。

-   v5.2.0 より前のバージョン (つまり、v4.0、v5.0、および v5.1) から現在のバージョンにアップグレードする場合は、アップグレードの前に`tidb_evolve_plan_baselines`が無効になっていることを確認してください。この変数を無効にするには、次の手順を実行します。

    {{< copyable "" >}}

    ```sql
    -- Check whether `tidb_evolve_plan_baselines` is disabled in the earlier version. 

    select @@global.tidb_evolve_plan_baselines;

    -- If `tidb_evolve_plan_baselines` is still enabled, disable it. 

    set global tidb_evolve_plan_baselines = off;
    ```

-   v4.0 から現在のバージョンにアップグレードする前に、使用可能な SQL バインディングに対応するすべてのクエリの構文が新しいバージョンで正しいかどうかを確認する必要があります。構文エラーが存在する場合は、対応する SQL バインディングを削除します。これを行うには、次の手順を実行します。

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

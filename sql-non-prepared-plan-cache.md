---
title: SQL Non-Prepared Execution Plan Cache
summary: TiDB の SQL 非準備実行プラン キャッシュの原理、使用法、および例について学習します。
---

# SQL Non-Prepared Execution Plan Cache {#sql-non-prepared-execution-plan-cache}

TiDBは、 [ステートメント`Prepare` / `Execute`](/sql-prepared-plan-cache.md)と同様に、一部の`PREPARE`以外のステートメントに対して実行プランのキャッシュをサポートしています。この機能により、これらのステートメントは最適化フェーズをスキップし、パフォーマンスを向上させることができます。

非準備プランキャッシュを有効にすると、メモリとCPUのオーバーヘッドが増加する可能性があり、すべての状況に適しているとは限りません。この機能をシナリオで有効にするかどうかを判断するには、セクション[パフォーマンス上の利点](#performance-benefits)と[メモリ監視](#monitoring)を参照してください。

## 原理 {#principle}

非準備プランキャッシュは、 [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)とキャッシュを共有するセッションレベルの機能です。非準備プランキャッシュの基本原理は次のとおりです。

1.  非準備プランキャッシュを有効にすると、TiDBはまず抽象構文木（AST）に基づいてクエリをパラメータ化します。例えば、 `SELECT * FROM t WHERE b < 10 AND a = 1` `SELECT * FROM t WHERE b < ? and a = ?`としてパラメータ化されます。
2.  次に、TiDB はパラメータ化されたクエリを使用してプラン キャッシュを検索します。
3.  再利用可能なプランが見つかった場合は、それが直接使用され、最適化フェーズはスキップされます。
4.  それ以外の場合、オプティマイザーは新しいプランを生成し、それをキャッシュに戻して、後続のクエリで再利用します。

## 使用法 {#usage}

準備されていないプランのキャッシュを有効または無効にするには、システム変数[`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)設定します。また、システム変数[`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)使用して、準備されていないプランのキャッシュのサイズを制御することもできます。キャッシュされたプランの数が`tidb_session_plan_cache_size`を超えると、TiDB は LRU (Least Recently Used) 戦略を使用してプランを削除します。

バージョン7.1.0以降では、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用して、キャッシュできるプランの最大サイズを制御できます。デフォルト値は2 MBです。プランのサイズがこの値を超える場合、プランはキャッシュされません。

> **注記：**
>
> `tidb_session_plan_cache_size`で指定されたメモリは、準備済みプランキャッシュと準備されていないプランキャッシュで共有されます。現在のクラスターで準備済みプランキャッシュを有効にしている場合、準備されていないプランキャッシュを有効にすると、元の準備済みプランキャッシュのヒット率が低下する可能性があります。

## 例 {#example}

次の例は、準備されていないプラン キャッシュを使用する方法を示しています。

1.  テスト用にテーブル`t`を作成します。

    ```sql
    CREATE TABLE t (a INT, b INT, KEY(b));
    ```

2.  準備されていないプラン キャッシュを有効にします。

    ```sql
    SET tidb_enable_non_prepared_plan_cache = ON;
    ```

3.  次の 2 つのクエリを実行します。

    ```sql
    SELECT * FROM t WHERE b < 10 AND a = 1;
    SELECT * FROM t WHERE b < 5 AND a = 2;
    ```

4.  2 番目のクエリがキャッシュにヒットするかどうかを確認します。

    ```sql
    SELECT @@last_plan_from_cache;
    ```

    If the value of `last_plan_from_cache` in the output is `1`, it means that the execution plan of the second query comes from the cache:

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## 制限 {#restrictions}

### 最適でない計画をキャッシュする {#cache-suboptimal-plans}

TiDBは、パラメータ化されたクエリに対して1つのプランのみをキャッシュします。例えば、クエリ`SELECT * FROM t WHERE a < 1`と`SELECT * FROM t WHERE a < 100000`同じパラメータ化された形式（ `SELECT * FROM t WHERE a < ?` ）を共有しているため、同じプランを共有します。

これがパフォーマンスの問題を引き起こす場合は、 `ignore_plan_cache()`ヒントを使用してキャッシュ内のプランを無視し、オプティマイザが毎回SQLの新しい実行プランを生成するようにすることができます。SQLを変更できない場合は、バインディングを作成して問題を解決できます。例えば、 `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...`ように指定します。

### 使用制限 {#usage-restrictions}

上記のリスクと、実行プランキャッシュが大きなメリットをもたらすのは単純なクエリのみであるという事実（クエリが複雑で実行に時間がかかる場合、実行プランキャッシュの使用はあまり役に立たない可能性があります）を考慮し、TiDBでは非準備プランキャッシュのスコープに厳しい制限を設けています。制限は次のとおりです。

-   [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)でサポートされていないクエリまたはプランは、準備されていないプラン キャッシュでもサポートされません。
-   `Window`や`Having`などの複雑な演算子を含むクエリはサポートされていません。
-   3 つ以上の`Join`テーブルまたはサブクエリを含むクエリはサポートされていません。
-   `ORDER BY 1`や`GROUP BY a+1`など、 `ORDER BY`または`GROUP BY`直後に数字や式が含まれるクエリはサポートされていません`ORDER BY column_name`と`GROUP BY column_name`のみがサポートされています。
-   `SELECT * FROM t WHERE json_col = '{}'`など、 `JSON` 、 `ENUM` 、 `SET` 、または`BIT`タイプの列でフィルタリングするクエリはサポートされていません。
-   `SELECT * FROM t WHERE a is NULL`など、 `NULL`値でフィルタリングするクエリはサポートされていません。
-   パラメータ化後のパラメータ数が200を超えるクエリ（例： `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)` ）は、デフォルトではサポートされません。v7.3.0以降では、システム変数[`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)に[`44823`](/optimizer-fix-controls.md#44823-new-in-v730)を設定することで、この制限を変更できます。
-   仮想列、一時テーブル、ビュー、またはメモリテーブルにアクセスするクエリはサポートされていません (例: `SELECT * FROM INFORMATION_SCHEMA.COLUMNS` 、 `COLUMNS`は TiDBメモリテーブル)。
-   ヒントまたはバインディングを含むクエリはサポートされていません。
-   DML文、または`FOR UPDATE`句を含む`SELECT`文はデフォルトではサポートされていません。この制限を解除するには、 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`実行してください。

After you enable this feature, the optimizer quickly evaluates the query. If it does not meet the support conditions for non-prepared plan cache, the query falls back to the regular optimization process.

## パフォーマンス上の利点 {#performance-benefits}

社内テストでは、非準備プランキャッシュ機能を有効にすると、ほとんどのTPシナリオで大幅なパフォーマンス向上が見られました。例えば、TPC-Cテストでは約4%、一部の銀行業務ワークロードでは10%以上、Sysbench RangeScanでは15%のパフォーマンス向上が見られました。

ただし、この機能は、クエリがサポートされているかどうかの判断、クエリのパラメータ化、キャッシュ内のプランの検索など、メモリとCPUのオーバーヘッドを増加させます。ワークロード内のクエリの大部分をキャッシュで処理できない場合、この機能を有効にするとパフォーマンスに悪影響を与える可能性があります。

この場合、Grafanaの**「プランキャッシュを使用しているクエリOPS」**パネルの「 `non-prepared`メトリックと**「プランキャッシュミスOPS」**パネルの「 `non-prepared-unsupported`メトリックを確認する必要があります。ほとんどのクエリがサポートされておらず、プランキャッシュにヒットできるクエリがごくわずかである場合は、この機能を無効にできます。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 診断 {#diagnostics}

非準備プランキャッシュを有効にした後、 `EXPLAIN FORMAT='plan_cache' SELECT ...`ステートメントを実行して、クエリがキャッシュにヒットするかどうかを確認できます。キャッシュにヒットできないクエリの場合、システムは警告でその理由を返します。

`FORMAT='plan_cache'`追加しないと、 `EXPLAIN`ステートメントはキャッシュにヒットしないことに注意してください。

クエリがキャッシュにヒットするかどうかを確認するには、次の`EXPLAIN FORMAT='plan_cache'`ステートメントを実行します。

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t) t;
```

出力は次のようになります。

```sql
3 rows in set, 1 warning (0.00 sec)
```

キャッシュにヒットできないクエリを表示するには、 `SHOW warnings;`実行します。

```sql
SHOW warnings;
```

出力は次のようになります。

```sql
+---------+------+-------------------------------------------------------------------------------+
| Level   | Code | Message                                                                       |
+---------+------+-------------------------------------------------------------------------------+
| Warning | 1105 | skip non-prepared plan-cache: queries that have sub-queries are not supported |
+---------+------+-------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

前の例では、準備されていないプラン キャッシュが`+`操作をサポートしていないため、クエリはキャッシュにヒットできません。

## 監視 {#monitoring}

準備されていないプラン キャッシュを有効にすると、次のペインでメモリ使用量、キャッシュ内のプランの数、キャッシュ ヒット率を監視できます。

![non-prepare-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

`statements_summary`テーブルとスロークエリログでキャッシュヒット率を監視することもできます。以下は、 `statements_summary`テーブルでキャッシュヒット率を表示する方法を示しています。

1.  テーブル`t`を作成します。

    ```sql
    CREATE TABLE t (a int);
    ```

2.  準備されていないプラン キャッシュを有効にします。

    ```sql
    SET @@tidb_enable_non_prepared_plan_cache=ON;
    ```

3.  次の 3 つのクエリを実行します。

    ```sql
    SELECT * FROM t WHERE a<1;
    SELECT * FROM t WHERE a<2;
    SELECT * FROM t WHERE a<3;
    ```

4.  キャッシュヒット率を表示するには、 `statements_summary`テーブルをクエリします。

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    出力は次のようになります。

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    From the output, you can see that the query was executed three times and hit the cache twice.

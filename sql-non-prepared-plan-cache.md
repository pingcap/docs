---
title: SQL Non-Prepared Execution Plan Cache
summary: TiDB の SQL 非準備実行プラン キャッシュの原理、使用方法、および例について学習します。
---

# SQL 未準備実行プラン キャッシュ {#sql-non-prepared-execution-plan-cache}

TiDB は、 [ステートメントの`Prepare` / `Execute`](/sql-prepared-plan-cache.md)と同様に、一部の`PREPARE`以外のステートメントの実行プランのキャッシュをサポートしています。この機能により、これらのステートメントは最適化フェーズをスキップしてパフォーマンスを向上させることができます。

準備されていないプラン キャッシュを有効にすると、追加のメモリと CPU のオーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。シナリオでこの機能を有効にするかどうかを判断するには、セクション[パフォーマンス上の利点](#performance-benefits)と[メモリ監視](#monitoring)を参照してください。

## 原理 {#principle}

非準備プラン キャッシュは、 [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)とキャッシュを共有するセッション レベルの機能です。非準備プラン キャッシュの基本原理は次のとおりです。

1.  準備されていないプラン キャッシュを有効にすると、TiDB はまず抽象構文ツリー (AST) に基づいてクエリをパラメーター化します。たとえば、 `SELECT * FROM t WHERE b < 10 AND a = 1` `SELECT * FROM t WHERE b < ? and a = ?`としてパラメーター化されます。
2.  次に、TiDB はパラメータ化されたクエリを使用してプラン キャッシュを検索します。
3.  再利用可能なプランが見つかった場合は、それが直接使用され、最適化フェーズはスキップされます。
4.  それ以外の場合、オプティマイザーは新しいプランを生成し、それをキャッシュに戻して、後続のクエリで再利用します。

## 使用法 {#usage}

準備されていないプラン キャッシュを有効または無効にするには、 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)システム変数を設定します。また、 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)システム変数を使用して準備されていないプラン キャッシュのサイズを制御することもできます。キャッシュされたプランの数が`tidb_session_plan_cache_size`を超えると、TiDB は最も最近使用されていない (LRU) 戦略を使用してプランを削除します。

v7.1.0 以降では、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用して、キャッシュできるプランの最大サイズを制御できます。デフォルト値は 2 MB です。プランのサイズがこの値を超えると、プランはキャッシュされません。

> **注記：**
>
> `tidb_session_plan_cache_size`で指定されたメモリは、準備済みプラン キャッシュと準備されていないプラン キャッシュの間で共有されます。現在のクラスターに対して準備済みプラン キャッシュを有効にしている場合、準備されていないプラン キャッシュを有効にすると、元の準備済みプラン キャッシュのヒット率が低下する可能性があります。

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

    出力の`last_plan_from_cache`の値が`1`の場合、2 番目のクエリの実行プランはキャッシュから取得されることを意味します。

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

TiDB は、パラメータ化されたクエリに対して 1 つのプランのみをキャッシュします。たとえば、クエリ`SELECT * FROM t WHERE a < 1`と`SELECT * FROM t WHERE a < 100000`同じパラメータ化された形式`SELECT * FROM t WHERE a < ?`を共有しているため、同じプランを共有します。

これによりパフォーマンスの問題が発生する場合は、 `ignore_plan_cache()`ヒントを使用してキャッシュ内のプランを無視し、オプティマイザが毎回 SQL の新しい実行プランを生成するようにすることができます。SQL を変更できない場合は、バインディングを作成して問題を解決できます。たとえば、 `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...` 。

### 使用制限 {#usage-restrictions}

前述のリスクと、実行プラン キャッシュが大きなメリットをもたらすのは単純なクエリのみであるという事実 (クエリが複雑で実行に時間がかかる場合、実行プラン キャッシュを使用してもあまり役に立たない可能性があります) のため、TiDB では準備されていないプラン キャッシュの範囲に厳しい制限が設けられています。制限は次のとおりです。

-   [準備されたプランキャッシュ](/sql-prepared-plan-cache.md)でサポートされていないクエリまたはプランは、準備されていないプラン キャッシュでもサポートされません。
-   `Window`や`Having`などの複雑な演算子を含むクエリはサポートされていません。
-   3 つ以上の`Join`テーブルまたはサブクエリを含むクエリはサポートされていません。
-   `ORDER BY 1`や`GROUP BY a+1`など、 `ORDER BY`または`GROUP BY`の直後に数字または式が含まれるクエリはサポートされていません。 `ORDER BY column_name`と`GROUP BY column_name`のみがサポートされています。
-   `SELECT * FROM t WHERE json_col = '{}'`など、 `JSON` 、 `ENUM` 、 `SET` 、または`BIT`タイプの列でフィルタリングするクエリはサポートされていません。
-   `SELECT * FROM t WHERE a is NULL`など、 `NULL`値でフィルタリングするクエリはサポートされていません。
-   パラメータ化後のパラメータ数が 200 を超えるクエリ ( `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`など) は、デフォルトではサポートされません。v7.3.0 以降では、 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v653-and-v710)システム変数に[`44823`](/optimizer-fix-controls.md#44823-new-in-v730)修正を設定することで、この制限を変更できます。
-   仮想列、一時テーブル、ビュー、またはメモリテーブルにアクセスするクエリはサポートされていません (例: `SELECT * FROM INFORMATION_SCHEMA.COLUMNS` 、 `COLUMNS`は TiDBメモリテーブル)。
-   ヒントまたはバインディングを含むクエリはサポートされていません。
-   DML ステートメントまたは`FOR UPDATE`句を含む`SELECT`ステートメントは、デフォルトではサポートされていません。この制限を解除するには、 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`実行します。

この機能を有効にすると、オプティマイザーはクエリを迅速に評価します。準備されていないプラン キャッシュのサポート条件を満たしていない場合、クエリは通常の最適化プロセスに戻ります。

## パフォーマンス上の利点 {#performance-benefits}

内部テストでは、準備されていないプラン キャッシュ機能を有効にすると、ほとんどの TP シナリオでパフォーマンスが大幅に向上します。たとえば、TPC-C テストでは約 4%、一部の銀行業務ワークロードでは 10% 以上、Sysbench RangeScan では 15% のパフォーマンス向上が見られます。

ただし、この機能により、クエリがサポートされているかどうかの判断、クエリのパラメータ化、キャッシュ内のプランの検索など、追加のメモリと CPU のオーバーヘッドも発生します。ワークロード内のクエリの大部分をキャッシュで処理できない場合、キャッシュを有効にするとパフォーマンスに悪影響が出る可能性があります。

この場合、Grafana の**Queries Using Plan Cache OPS**パネルの`non-prepared`メトリックと**Plan Cache Miss OPS**パネルの`non-prepared-unsupported`メトリックを観察する必要があります。ほとんどのクエリがサポートされておらず、プラン キャッシュにヒットできるクエリが少数の場合は、この機能を無効にすることができます。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 診断 {#diagnostics}

準備されていないプラン キャッシュを有効にした後、 `EXPLAIN FORMAT='plan_cache' SELECT ...`ステートメントを実行して、クエリがキャッシュにヒットできるかどうかを確認できます。キャッシュにヒットできないクエリの場合、システムは警告で理由を返します。

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

`statements_summary`テーブルとスロー クエリ ログでキャッシュ ヒット率を監視することもできます。次に、 `statements_summary`テーブルでキャッシュ ヒット率を表示する方法を示します。

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

    出力から、クエリが 3 回実行され、キャッシュに 2 回ヒットしたことがわかります。

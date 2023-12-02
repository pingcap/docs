---
title: SQL Non-Prepared Execution Plan Cache
summary: Learn about the principle, usage, and examples of the SQL non-prepared execution plan cache in TiDB.
---

# SQL の未準備実行プラン キャッシュ {#sql-non-prepared-execution-plan-cache}

TiDB は、 [ステートメントの`Prepare` / `Execute`](/sql-prepared-plan-cache.md)と同様、一部の非`PREPARE`ステートメントの実行プラン キャッシュをサポートします。この機能により、これらのステートメントは最適化フェーズをスキップし、パフォーマンスを向上させることができます。

準備されていないプラン キャッシュを有効にすると、追加のメモリと CPU オーバーヘッドが発生する可能性があり、すべての状況に適しているとは限りません。シナリオでこの機能を有効にするかどうかを決定するには、 [パフォーマンス上の利点](#performance-benefits)セクションと[メモリ監視](#monitoring)セクションを参照してください。

## 原理 {#principle}

準備されていないプラン キャッシュは、 [準備されたプランのキャッシュ](/sql-prepared-plan-cache.md)とキャッシュを共有するセッション レベルの機能です。準備されていないプラン キャッシュの基本原理は次のとおりです。

1.  未準備プラン キャッシュを有効にすると、TiDB はまず抽象構文ツリー (AST) に基づいてクエリをパラメータ化します。たとえば、 `SELECT * FROM t WHERE b < 10 AND a = 1`は`SELECT * FROM t WHERE b < ? and a = ?`としてパラメータ化されます。
2.  次に、TiDB はパラメーター化されたクエリを使用してプラン キャッシュを検索します。
3.  再利用可能なプランが見つかった場合は、それが直接使用され、最適化フェーズはスキップされます。
4.  それ以外の場合、オプティマイザは新しいプランを生成し、後続のクエリで再利用できるようにそれをキャッシュに再度追加します。

## 使用法 {#usage}

準備されていないプラン キャッシュを有効または無効にするには、 [`tidb_enable_non_prepared_plan_cache`](/system-variables.md#tidb_enable_non_prepared_plan_cache)システム変数を設定します。 [`tidb_session_plan_cache_size`](/system-variables.md#tidb_session_plan_cache_size-new-in-v710)システム変数を使用して、準備されていないプラン キャッシュのサイズを制御することもできます。キャッシュされたプランの数が`tidb_session_plan_cache_size`を超えると、TiDB は最も最近使用されていない (LRU) 戦略を使用してプランを削除します。

v7.1.0 以降、システム変数[`tidb_plan_cache_max_plan_size`](/system-variables.md#tidb_plan_cache_max_plan_size-new-in-v710)を使用してキャッシュできるプランの最大サイズを制御できます。デフォルト値は 2 MB です。プランのサイズがこの値を超える場合、プランはキャッシュされません。

> **注記：**
>
> `tidb_session_plan_cache_size`で指定されたメモリは、準備済みプラン キャッシュと準備されていないプラン キャッシュ間で共有されます。現在のクラスターで準備済みプラン キャッシュを有効にしている場合、準備されていないプラン キャッシュを有効にすると、元の準備済みプラン キャッシュのヒット率が低下する可能性があります。

## 例 {#example}

次の例は、準備されていないプラン キャッシュの使用方法を示しています。

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

    出力の`last_plan_from_cache`の値が`1`の場合、2 番目のクエリの実行プランがキャッシュから取得されたことを意味します。

    ```sql
    +------------------------+
    | @@last_plan_from_cache |
    +------------------------+
    |                      1 |
    +------------------------+
    1 row in set (0.00 sec)
    ```

## 制限 {#restrictions}

### 次善のプランをキャッシュする {#cache-suboptimal-plans}

TiDB は、パラメーター化されたクエリに対して 1 つのプランのみをキャッシュします。たとえば、クエリ`SELECT * FROM t WHERE a < 1`と`SELECT * FROM t WHERE a < 100000`は同じパラメータ化された形式`SELECT * FROM t WHERE a < ?`を共有するため、同じプランを共有します。

これによりパフォーマンスの問題が発生する場合は、 `ignore_plan_cache()`ヒントを使用してキャッシュ内のプランを無視し、オプティマイザーが毎回 SQL の新しい実行プランを生成するようにすることができます。 SQL を変更できない場合は、バインディングを作成して問題を解決できます。たとえば、 `CREATE BINDING FOR SELECT ... USING SELECT /*+ ignore_plan_cache() */ ...` 。

### 使用制限 {#usage-restrictions}

前述のリスクと、実行プラン キャッシュは単純なクエリに対してのみ大きな利点を提供するという事実 (クエリが複雑で実行に時間がかかる場合、実行プラン キャッシュの使用はあまり役に立たない可能性があります) により、TiDB には厳しい制限があります。準備されていないプラン キャッシュの範囲について。制限事項は次のとおりです。

-   [準備されたプランのキャッシュ](/sql-prepared-plan-cache.md)でサポートされていないクエリまたはプランは、準備されていないプラン キャッシュでもサポートされません。
-   `Window`や`Having`などの複雑な演算子を含むクエリはサポートされていません。
-   3 つ以上の`Join`テーブルまたはサブクエリを含むクエリはサポートされていません。
-   `ORDER BY 1`や`GROUP BY a+1`など、 `ORDER BY`または`GROUP BY`直後に数値または式を含むクエリはサポートされていません。 `ORDER BY column_name`と`GROUP BY column_name`のみがサポートされます。
-   `JSON` 、 `ENUM` 、 `SET` 、または`BIT`タイプの列でフィルター処理するクエリ ( `SELECT * FROM t WHERE json_col = '{}'`など) はサポートされていません。
-   `SELECT * FROM t WHERE a is NULL`など、 `NULL`の値でフィルタリングするクエリはサポートされていません。
-   パラメータ化後のパラメータが 200 を超えるクエリ ( `SELECT * FROM t WHERE a in (1, 2, 3, ... 201)`など) は、デフォルトではサポートされていません。 v7.3.0 以降、 [`tidb_opt_fix_control`](/system-variables.md#tidb_opt_fix_control-new-in-v710)システム変数に[`44823`](/optimizer-fix-controls.md#44823-new-in-v730) fix を設定することで、この制限を変更できます。
-   パーティション化されたテーブル、仮想列、一時テーブル、ビュー、またはメモリテーブルにアクセスするクエリ ( `SELECT * FROM INFORMATION_SCHEMA.COLUMNS`など) はサポートされていません。ここで、 `COLUMNS`は TiDBメモリテーブルです。
-   ヒントまたはバインディングを含むクエリはサポートされていません。
-   DML ステートメントまたは`FOR UPDATE`句を含む`SELECT`ステートメントは、デフォルトではサポートされていません。この制限を解除するには、 `SET tidb_enable_non_prepared_plan_cache_for_dml = ON`を実行します。

この機能を有効にすると、オプティマイザーはクエリを迅速に評価します。準備されていないプラン キャッシュのサポート条件を満たさない場合、クエリは通常の最適化プロセスに戻ります。

## パフォーマンス上の利点 {#performance-benefits}

内部テストでは、準備されていないプラン キャッシュ機能を有効にすると、ほとんどの TP シナリオでパフォーマンスが大幅に向上します。たとえば、TPC-C テストでは約 4%、一部の銀行ワークロードでは 10% 以上、Sysbench RangeScan では 15% のパフォーマンス向上がありました。

ただし、この機能では、クエリがサポートされているかどうかの判断、クエリのパラメータ化、キャッシュ内のプランの検索など、追加のメモリと CPU のオーバーヘッドも発生します。キャッシュがワークロード内のクエリの大部分にヒットできない場合、キャッシュを有効にすると実際にパフォーマンスに悪影響を及ぼす可能性があります。

この場合、Grafana の**[プラン キャッシュ OPS を使用したクエリ]**パネルの`non-prepared`メトリックと、 **[プラン キャッシュ ミス OPS]**パネルの`non-prepared-unsupported`メトリックを観察する必要があります。ほとんどのクエリがサポートされておらず、プラン キャッシュにヒットできるクエリが少数しかない場合は、この機能を無効にすることができます。

![non-prepared-unsupported](/media/non-prepapred-plan-cache-unsupprot.png)

## 診断 {#diagnostics}

準備されていないプラン キャッシュを有効にした後、 `EXPLAIN FORMAT='plan_cache' SELECT ...`ステートメントを実行して、クエリがキャッシュにヒットできるかどうかを確認できます。キャッシュにヒットできないクエリの場合、システムは警告としてその理由を返します。

`FORMAT='plan_cache'`を追加しない場合、 `EXPLAIN`ステートメントはキャッシュにヒットしないことに注意してください。

クエリがキャッシュにヒットするかどうかを確認するには、次の`EXPLAIN FORMAT='plan_cache'`ステートメントを実行します。

```sql
EXPLAIN FORMAT='plan_cache' SELECT * FROM (SELECT a+1 FROM t1) t;
```

出力は次のとおりです。

```sql
3 rows in set, 1 warning (0.00 sec)
```

キャッシュにヒットできないクエリを表示するには、 `SHOW warnings;`を実行します。

```sql
SHOW warnings;
```

出力は次のとおりです。

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

未準備プラン キャッシュを有効にすると、次のペインでメモリ使用量、キャッシュ内のプラン数、キャッシュ ヒット率を監視できます。

![non-prepare-plan-cache](/media/tidb-non-prepared-plan-cache-metrics.png)

`statements_summary`テーブルのキャッシュ ヒット率やスロー クエリ ログも監視できます。以下に、 `statements_summary`の表でキャッシュ ヒット率を表示する方法を示します。

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

4.  `statements_summary`テーブルをクエリして、キャッシュ ヒット率を表示します。

    ```sql
    SELECT digest_text, query_sample_text, exec_count, plan_in_cache, plan_cache_hits FROM INFORMATION_SCHEMA.STATEMENTS_SUMMARY WHERE query_sample_text LIKE '%SELECT * FROM %';
    ```

    出力は次のとおりです。

    ```sql
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | digest_text                     | query_sample_text                        | exec_count | plan_in_cache | plan_cache_hits |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    | SELECT * FROM `t` WHERE `a` < ? | SELECT * FROM t WHERE a<1                |          3 |             1 |               2 |
    +---------------------------------+------------------------------------------+------------+---------------+-----------------+
    1 row in set (0.01 sec)
    ```

    出力から、クエリが 3 回実行され、キャッシュに 2 回ヒットしたことがわかります。

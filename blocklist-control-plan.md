---
title: The Blocklist of Optimization Rules and Expression Pushdown
summary: Learn about the blocklist to control the optimization rules and the behavior of expression pushdown.
---

# 最適化ルールと式のプッシュダウンのブロックリスト {#the-blocklist-of-optimization-rules-and-expression-pushdown}

このドキュメントでは、最適化ルールのブロックリストと式プッシュダウンのブロックリストを使用して、TiDBの動作を制御する方法を紹介します。

## 最適化ルールのブロックリスト {#the-blocklist-of-optimization-rules}

最適化ルールのブロックリストは、最適化ルールを調整する1つの方法であり、主に一部の最適化ルールを手動で無効にするために使用されます。

### 重要な最適化ルール {#important-optimization-rules}

| **最適化ルール**  | **ルール名**                | **説明**                                                                            |
| :---------- | :---------------------- | :-------------------------------------------------------------------------------- |
| カラムの剪定      | column_prune            | 上位のエグゼキュータが必要としない場合は、1人のオペレータが列を整理します。                                            |
| サブクエリを非相関化  | デコレレート                  | 相関サブクエリを非相関結合または集約に書き直そうとします。                                                     |
| 集計の除去       | Aggregation_eliminate   | 実行プランから不要な集計演算子を削除しようとします。                                                        |
| 突起物の除去      | Projection_eliminate    | 実行プランから不要な射影演算子を削除します。                                                            |
| 最大/最小除去     | max_min_eliminate       | 一部のmax/min関数を集約して`order by` + `limit 1`形式に書き換えます。                                 |
| 述語プッシュダウン   | predicate_push_down     | データソースに近い演算子に述語をプッシュしようとします。                                                      |
| アウタージョインの排除 | external_join_eliminate | 実行プランから不要な左結合または右結合を削除しようとします。                                                    |
| パーティションの剪定  | partition_processor     | 述部によって拒否されたパーティションを削除し、パーティションテーブルクエリを`UnionAll + Partition Datasource`形式に書き換えます。 |
| 集計プッシュダウン   | Aggregation_push_down   | アグリゲーションを子にプッシュしようとします。                                                           |
| TopNプッシュダウン | topn_push_down          | TopNオペレーターをデータソースに近い場所にプッシュしようとします。                                               |
| 再注文に参加      | join_reorder            | マルチテーブル結合の順序を決定します。                                                               |

### 最適化ルールを無効にする {#disable-optimization-rules}

一部のルールが特別なクエリの最適ではない実行プランにつながる場合は、最適化ルールのブロックリストを使用して、それらの一部を無効にすることができます。

#### 使用法 {#usage}

> **ノート：**
>
> 以下のすべての操作には、データベースの`super privilege`の特権が必要です。各最適化ルールには名前があります。たとえば、列プルーニングの名前は`column_prune`です。すべての最適化ルールの名前は、表[重要な最適化ルール](#important-optimization-rules)の2番目の列にあります。

-   一部のルールを無効にする場合は、その名前を`mysql.opt_rule_blacklist`テーブルに書き込みます。例えば：

    {{< copyable "" >}}

    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    次のSQLステートメントを実行すると、上記の操作をすぐに有効にすることができます。有効範囲には、対応するTiDBサーバーのすべての古い接続が含まれます。

    {{< copyable "" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **ノート：**
    >
    > `admin reload opt_rule_blacklist`は、上記のステートメントが実行されたTiDBサーバーでのみ有効です。クラスタのすべてのTiDBサーバーを有効にする場合は、各TiDBサーバーでこのコマンドを実行します。

-   ルールを再度有効にする場合は、テーブル内の対応するデータを削除してから、次の`admin reload`のステートメントを実行します。

    {{< copyable "" >}}

    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    ```

    {{< copyable "" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

## 式プッシュダウンのブロックリスト {#the-blocklist-of-expression-pushdown}

式のプッシュダウンのブロックリストは、式のプッシュダウンを調整する1つの方法であり、主に特定のデータ型の一部の式を手動で無効にするために使用されます。

### プッシュダウンがサポートされている式 {#expressions-which-are-supported-to-be-pushed-down}

| 式の分類                                                                                 | 具体的な操作                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :----------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [論理演算](/functions-and-operators/operators.md#logical-operators)                      | AND（&amp;&amp;）、OR（||）、NOT（！）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [比較関数と演算子](/functions-and-operators/operators.md#comparison-functions-and-operators) | &lt;、&lt;=、=、！=（ `<>` ）、&gt;、&gt; =、 [`&#x3C;=>`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#operator_equal-to) 、IS NULL、LIKE、IS TRUE、IS [`COALESCE()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_coalesce) 、 [`IN()`](https://dev.mysql.com/doc/refman/5.7/en/comparison-operators.html#function_in)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| [数値関数と演算子](/functions-and-operators/numeric-functions-and-operators.md)              | [`FLOOR()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_floor) 、-、 [`CEIL()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceil) 、 [`CEILING()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_ceiling) 、 [`ABS()`](https://dev.mysql.com/doc/refman/5.7/en/mathematical-functions.html#function_abs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| [制御フロー関数](/functions-and-operators/control-flow-functions.md)                        | [`CASE`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#operator_case) [`IF()`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_if) [`IFNULL()`](https://dev.mysql.com/doc/refman/5.7/en/flow-control-functions.html#function_ifnull)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| [JSON関数](/functions-and-operators/json-functions.md)                                 | [JSON_TYPE（json_val）](https://dev.mysql.com/doc/refman/5.7/en/json-attribute-functions.html#function_json-type) 、<br/> [JSON_EXTRACT（json_doc、path [、path] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-search-functions.html#function_json-extract) 、<br/> [JSON_UNQUOTE（json_val）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-unquote) 、<br/> [JSON_OBJECT（key、val [、key、val] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-object) 、<br/> [JSON_ARRAY（[val [、val] ...]）](https://dev.mysql.com/doc/refman/5.7/en/json-creation-functions.html#function_json-array) 、<br/> [JSON_MERGE（json_doc、json_doc [、json_doc] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-merge) 、<br/> [JSON_SET（json_doc、path、val [、path、val] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-set) 、<br/> [JSON_INSERT（json_doc、path、val [、path、val] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-insert) 、<br/> [JSON_REPLACE（json_doc、path、val [、path、val] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-replace) 、<br/> [JSON_REMOVE（json_doc、path [、path] ...）](https://dev.mysql.com/doc/refman/5.7/en/json-modification-functions.html#function_json-remove) |
| [日付と時刻の関数](/functions-and-operators/date-and-time-functions.md)                      | [`DATE_FORMAT()`](https://dev.mysql.com/doc/refman/5.7/en/date-and-time-functions.html#function_date-format)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |

### 特定の式のプッシュダウンを無効にする {#disable-the-pushdown-of-specific-expressions}

式のプッシュダウンが原因で間違った結果が得られた場合は、ブロックリストを使用してアプリケーションをすばやく回復できます。具体的には、サポートされている関数または演算子の一部を`mysql.expr_pushdown_blacklist`テーブルに追加して、特定の式のプッシュダウンを無効にすることができます。

`mysql.expr_pushdown_blacklist`のスキーマは次のように表示されます。

{{< copyable "" >}}

```sql
DESC mysql.expr_pushdown_blacklist;
```

```sql
+------------+--------------+------+------+-------------------+-------+
| Field      | Type         | Null | Key  | Default           | Extra |
+------------+--------------+------+------+-------------------+-------+
| name       | char(100)    | NO   |      | NULL              |       |
| store_type | char(100)    | NO   |      | tikv,tiflash,tidb |       |
| reason     | varchar(200) | YES  |      | NULL              |       |
+------------+--------------+------+------+-------------------+-------+
3 rows in set (0.00 sec)
```

上記の各フィールドの説明は次のとおりです。

-   `name` ：プッシュダウンが無効になっている関数の名前。
-   `store_type` ：計算のために関数がプッシュダウンされないようにするコンポーネントを指定します。使用可能なコンポーネントは`tidb` 、および`tikv` `tiflash` 。 `store_type`では大文字と小文字は区別されません。複数のコンポーネントを指定する必要がある場合は、コンマを使用して各コンポーネントを区切ります。
    -   `store_type`が`tidb`の場合、TiDBメモリテーブルの読み込み中に他のTiDBサーバーで機能を実行できるかどうかを示します。
    -   `store_type`が`tikv`の場合、TiKVサーバーのコプロセッサーコンポーネントで機能を実行できるかどうかを示します。
    -   `store_type`が`tiflash`の場合、TiFlashサーバーのコプロセッサーコンポーネントで機能を実行できるかどうかを示します。
-   `reason` ：この関数がブロックリストに追加された理由を記録します。

### 使用法 {#usage}

このセクションでは、式プッシュダウンのブロックリストの使用方法について説明します。

#### ブロックリストに追加 {#add-to-the-blocklist}

1つ以上の式（関数または演算子）をブロックリストに追加するには、次の手順を実行します。

1.  対応する関数名または演算子名、およびプッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`のテーブルに挿入します。

2.  `admin reload expr_pushdown_blacklist`を実行します。

### ブロックリストから削除する {#remove-from-the-blocklist}

ブロックリストから1つ以上の式を削除するには、次の手順を実行します。

1.  対応する関数名または演算子名、およびプッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`のテーブルから削除します。

2.  `admin reload expr_pushdown_blacklist`を実行します。

> **ノート：**
>
> `admin reload expr_pushdown_blacklist`は、このステートメントが実行されるTiDBサーバーでのみ有効です。クラスタのすべてのTiDBサーバーを有効にする場合は、各TiDBサーバーでこのコマンドを実行します。

## 式ブロックリストの使用例 {#expression-blocklist-usage-example}

次の例では、 `<`と`>`の演算子がブロックリストに追加され、次に`>`の演算子がブロックリストから削除されます。

ブロックリストが有効かどうかを判断するには、 `EXPLAIN`の結果を観察します（ [TiDBクエリ実行プランの概要](/explain-overview.md)を参照）。

1.  次のSQLステートメントの`WHERE`節の述語`a < 2`と`a > 2`は、TiKVにプッシュダウンできます。

    {{< copyable "" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | TableReader_7           | 0.00     | root      |               | data:Selection_6                   |
    | └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

2.  式を`mysql.expr_pushdown_blacklist`テーブルに挿入し、 `admin reload expr_pushdown_blacklist`を実行します。

    {{< copyable "" >}}

    ```sql
    INSERT INTO mysql.expr_pushdown_blacklist VALUES('<','tikv',''), ('>','tikv','');
    ```

    ```sql
    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    ```

    {{< copyable "" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3.  実行プランをもう一度観察すると、 `<`と`>`の両方のオペレーターがTiKVコプロセッサーにプッシュダウンされていないことがわかります。

    {{< copyable "" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 and a > 2;
    ```

    ```sql
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | id                      | estRows  | task      | access object | operator info                      |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    | Selection_7             | 10000.00 | root      |               | gt(ssb_1.t.a, 2), lt(ssb_1.t.a, 2) |
    | └─TableReader_6         | 10000.00 | root      |               | data:TableFullScan_5               |
    |   └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo     |
    +-------------------------+----------+-----------+---------------+------------------------------------+
    3 rows in set (0.00 sec)
    ```

4.  ブロックリストから1つの式（ここでは`>` ）を削除し、 `admin reload expr_pushdown_blacklist`を実行します。

    {{< copyable "" >}}

    ```sql
    DELETE FROM mysql.expr_pushdown_blacklist WHERE name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    {{< copyable "" >}}

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

5.  実行プランをもう一度観察すると、 `>`がTiKVコプロセッサーにプッシュダウンされている間、 `<`はプッシュダウンされていないことがわかります。

    {{< copyable "" >}}

    ```sql
    EXPLAIN SELECT * FROM t WHERE a < 2 AND a > 2;
    ```

    ```sql
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | id                        | estRows  | task      | access object | operator info                  |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    | Selection_8               | 0.00     | root      |               | lt(ssb_1.t.a, 2)               |
    | └─TableReader_7           | 0.00     | root      |               | data:Selection_6               |
    |   └─Selection_6           | 0.00     | cop[tikv] |               | gt(ssb_1.t.a, 2)               |
    |     └─TableFullScan_5     | 10000.00 | cop[tikv] | table:t       | keep order:false, stats:pseudo |
    +---------------------------+----------+-----------+---------------+--------------------------------+
    4 rows in set (0.00 sec)
    ```

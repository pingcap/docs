---
title: The Blocklist of Optimization Rules and Expression Pushdown
summary: Learn about the blocklist to control the optimization rules and the behavior of expression pushdown.
---

# 最適化ルールのブロックリストと式のプッシュダウン {#the-blocklist-of-optimization-rules-and-expression-pushdown}

このドキュメントでは、最適化ルールのブロックリストと式プッシュダウンのブロックリストを使用して、TiDB の動作を制御する方法を紹介します。

## 最適化ルールのブロックリスト {#the-blocklist-of-optimization-rules}

最適化ルールのブロックリストは、最適化ルールを調整する 1 つの方法であり、主にいくつかの最適化ルールを手動で無効にするために使用されます。

### 重要な最適化ルール {#important-optimization-rules}

| **最適化ルール**      | **ルール名**             | **説明**                                                                            |
| :-------------- | :------------------- | :-------------------------------------------------------------------------------- |
| カラムの剪定          | column_prune         | 上位エグゼキューターが列を必要としない場合、1 人のオペレーターが列を整理します。                                         |
| サブクエリの関連付けを解除する | 関連付けを解除する            | 相関サブクエリを非相関結合または集約に書き換えようとします。                                                    |
| 集計除去            | アグリゲーション_エリミネート      | 実行計画から不要な集計演算子を削除しようとします。                                                         |
| 突起除去            | プロジェクション_エリミネート      | 実行計画から不要な射影演算子を削除します。                                                             |
| 最大/最小除去         | max_min_eliminate    | 集計の一部の max/min関数を`order by` + `limit 1`形式に書き換えます。                                 |
| 述語のプッシュダウン      | predicate_push_down  | データ ソースに近い演算子に述語を押し下げようとします。                                                      |
| 外部結合の削除         | outer_join_eliminate | 不要な左結合または右結合を実行計画から削除しようとします。                                                     |
| パーティションの剪定      | partition_processor  | 述語によって拒否されたパーティションを削除し、パーティションテーブルクエリを`UnionAll + Partition Datasource`形式に書き換えます。 |
| 集計プッシュダウン       | アグリゲーション_プッシュ_ダウン    | 集計を子にプッシュしようとします。                                                                 |
| TopN プッシュダウン    | topn_push_down       | TopN オペレーターをデータ ソースに近い場所にプッシュしようとします。                                             |
| 再注文に参加          | join_reorder         | 複数テーブルの結合の順序を決定します。                                                               |

### 最適化ルールを無効にする {#disable-optimization-rules}

最適化ルールのブロックリストを使用して、いくつかのルールが特別なクエリの最適でない実行計画につながる場合、それらの一部を無効にすることができます。

#### 使用法 {#usage}

> **ノート：**
>
> 以下のすべての操作には、データベースの`super privilege`権限が必要です。各最適化ルールには名前があります。たとえば、列のプルーニングの名前は`column_prune`です。すべての最適化ルールの名前は、表[重要な最適化ルール](#important-optimization-rules)の 2 番目の列に記載されています。

-   一部のルールを無効にする場合は、その名前を`mysql.opt_rule_blacklist`テーブルに書き込みます。例えば：

    {{< copyable "" >}}

    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    次の SQL ステートメントを実行すると、上記の操作がすぐに有効になります。有効な範囲には、対応する TiDBサーバーのすべての古い接続が含まれます。

    {{< copyable "" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **ノート：**
    >
    > `admin reload opt_rule_blacklist`上記のステートメントが実行された TiDBサーバーでのみ有効です。クラスターのすべての TiDB サーバーを有効にする場合は、各 TiDBサーバーでこのコマンドを実行します。

-   ルールを再度有効にする場合は、テーブル内の対応するデータを削除してから、 `admin reload`ステートメントを実行します。

    {{< copyable "" >}}

    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    ```

    {{< copyable "" >}}

    ```sql
    admin reload opt_rule_blacklist;
    ```

## 式プッシュダウンのブロックリスト {#the-blocklist-of-expression-pushdown}

式プッシュダウンのブロックリストは、式プッシュダウンを調整する 1 つの方法であり、主に特定のデータ型の式を手動で無効にするために使用されます。

### プッシュ ダウンがサポートされている式 {#expressions-that-are-supported-to-be-pushed-down}

プッシュ ダウンがサポートされている式の詳細については、 [TiKV へのプッシュダウンでサポートされている式](/functions-and-operators/expressions-pushed-down.md#supported-expressions-for-pushdown-to-tikv)を参照してください。

### 特定の式のプッシュダウンを無効にする {#disable-the-pushdown-of-specific-expressions}

式のプッシュダウンが原因で間違った結果が得られた場合は、ブロックリストを使用してアプリケーションの迅速な回復を行うことができます。具体的には、サポートされている関数または演算子の一部を`mysql.expr_pushdown_blacklist`テーブルに追加して、特定の式のプッシュダウンを無効にすることができます。

`mysql.expr_pushdown_blacklist`のスキーマは次のように示されます。

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

-   `name` : プッシュダウンが無効になっている関数の名前。
-   `store_type` : 関数が計算のためにプッシュダウンされないようにするコンポーネントを指定します。使用可能なコンポーネントは`tidb` 、 `tikv` 、および`tiflash`です。 `store_type`は大文字と小文字を区別しません。複数のコンポーネントを指定する必要がある場合は、コンマを使用して各コンポーネントを区切ります。
    -   `store_type`が`tidb`の場合、TiDBメモリテーブルの読み取り中に他の TiDB サーバーで関数を実行できるかどうかを示します。
    -   `store_type`が`tikv`の場合、機能が TiKV サーバーのコプロセッサーコンポーネントで実行できるかどうかを示します。
    -   `store_type`が`tiflash`の場合、関数がTiFlashサーバーのコプロセッサーコンポーネントで実行できるかどうかを示します。
-   `reason` : この関数がブロックリストに追加された理由を記録します。

### 使用法 {#usage}

このセクションでは、式プッシュダウンのブロックリストの使用方法について説明します。

#### ブロックリストに追加 {#add-to-the-blocklist}

1 つ以上の式 (関数または演算子) をブロックリストに追加するには、次の手順を実行します。

1.  対応する関数名または演算子名、およびプッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`テーブルに挿入します。

2.  `admin reload expr_pushdown_blacklist`を実行します。

### ブロックリストから削除 {#remove-from-the-blocklist}

ブロックリストから 1 つ以上の式を削除するには、次の手順を実行します。

1.  対応する関数名または演算子名、およびプッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`テーブルから削除します。

2.  `admin reload expr_pushdown_blacklist`を実行します。

> **ノート：**
>
> `admin reload expr_pushdown_blacklist`は、このステートメントが実行される TiDBサーバーでのみ有効です。クラスターのすべての TiDB サーバーを有効にする場合は、各 TiDBサーバーでこのコマンドを実行します。

## 式ブロックリストの使用例 {#expression-blocklist-usage-example}

次の例では、 `<`と`>`演算子がブロックリストに追加され、 `>`演算子がブロックリストから削除されます。

ブロックリストが有効かどうかを判断するには、 `EXPLAIN`の結果を観察します ( [TiDB クエリ実行計画の概要](/explain-overview.md)を参照)。

1.  次の SQL ステートメントの`WHERE`句の述語`a < 2`と`a > 2`は、TiKV にプッシュ ダウンできます。

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

3.  実行計画をもう一度観察すると、 `<`と`>`の演算子の両方が TiKV コプロセッサーにプッシュされていないことがわかります。

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

4.  ブロックリストから 1 つの式 (ここでは`>` ) を削除し、 `admin reload expr_pushdown_blacklist`を実行します。

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

5.  実行計画を再度観察すると、 `<`はプッシュ ダウンされていませんが、 `>`は TiKV コプロセッサーにプッシュ ダウンされていることがわかります。

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

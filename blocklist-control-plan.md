---
title: The Blocklist of Optimization Rules and Expression Pushdown
summary: 最適化ルールと式プッシュダウンの動作を制御するブロックリストについて学習します。
---

# 最適化ルールのブロックリストと式のプッシュダウン {#the-blocklist-of-optimization-rules-and-expression-pushdown}

このドキュメントでは、最適化ルールのブロックリストと式プッシュダウンのブロックリストを使用して TiDB の動作を制御する方法を紹介します。

## 最適化ルールのブロックリスト {#the-blocklist-of-optimization-rules}

最適化ルールのブロックリストは、最適化ルールを調整する 1 つの方法であり、主に一部の最適化ルールを手動で無効にするために使用されます。

### 重要な最適化ルール {#important-optimization-rules}

| **最適化ルール**                 | **ルール名**         | **説明**                                                                                |
| :------------------------- | :--------------- | :------------------------------------------------------------------------------------ |
| カラムの剪定                     | 列プルーン            | 上位の実行者が列を必要としない場合、1 つの演算子がその列を削除します。                                                  |
| サブクエリの非相関化                 | 相関関係をなくす         | 相関サブクエリを非相関結合または集計に書き換えようとします。                                                        |
| 集計の除去                      | 集約を排除する          | 実行プランから不要な集計演算子を削除しようとします。                                                            |
| 投影の除去                      | 投影を排除する          | 実行プランから不要な投影演算子を削除します。                                                                |
| 最大/最小の排除                   | 最大最小排除           | 集計におけるいくつかの最大/最小関数を`order by` + `limit 1`形式に書き換えます。                                   |
| 述語プッシュダウン                  | 述語プッシュダウン        | 述語をデータ ソースに近い演算子にプッシュダウンしようとします。                                                      |
| 外部結合の除去                    | 外部結合の除去          | 実行プランから不要な左結合または右結合を削除しようとします。                                                        |
| パーティションの整理                 | パーティションプロセッサ     | 述語によって拒否されたパーティションをプルーニングし、パーティションテーブルクエリを`UnionAll + Partition Datasource`形式に書き換えます。 |
| 集計プッシュダウン                  | 集約プッシュダウン        | 集約をその子にプッシュダウンしようとします。                                                                |
| TopNプッシュダウン                | トップn_プッシュダウン     | TopN 演算子をデータ ソースに近い場所にプッシュしようとします。                                                    |
| 参加順序の変更                    | 結合順序変更           | 複数テーブルの結合の順序を決定します。                                                                   |
| ウィンドウ関数からTopNまたはLimitを導出する | ウィンドウからトップnを取得する | ウィンドウ関数から TopN または Limit 演算子を導出します。                                                   |

### 最適化ルールを無効にする {#disable-optimization-rules}

一部のルールが特殊なクエリに対して最適ではない実行プランにつながる場合は、最適化ルールのブロックリストを使用して、その一部を無効にすることができます。

#### 使用法 {#usage}

> **注記：**
>
> 以下のすべての操作には、データベースの`super privilege`権限が必要です。各最適化ルールには名前があります。たとえば、列プルーニングの名前は`column_prune`です。すべての最適化ルールの名前は、表[重要な最適化ルール](#important-optimization-rules)の 2 番目の列にあります。

-   いくつかのルールを無効にする場合は、その名前を`mysql.opt_rule_blacklist`テーブルに書き込みます。例:

    ```sql
    INSERT INTO mysql.opt_rule_blacklist VALUES("join_reorder"), ("topn_push_down");
    ```

    次の SQL 文を実行すると、上記の操作がすぐに有効になります。有効範囲には、対応する TiDBサーバーの古い接続がすべて含まれます。

    ```sql
    admin reload opt_rule_blacklist;
    ```

    > **注記：**
    >
    > `admin reload opt_rule_blacklist` 、上記のステートメントが実行された TiDBサーバーにのみ有効になります。クラスターのすべての TiDB サーバーに有効にする場合は、各 TiDBサーバーでこのコマンドを実行します。

-   ルールを再度有効にする場合は、テーブル内の対応するデータを削除してから、 `admin reload`ステートメントを実行します。

    ```sql
    DELETE FROM mysql.opt_rule_blacklist WHERE name IN ("join_reorder", "topn_push_down");
    ```

    ```sql
    admin reload opt_rule_blacklist;
    ```

## 表現プッシュダウンのブロックリスト {#the-blocklist-of-expression-pushdown}

式プッシュダウンのブロックリストは、式プッシュダウンを調整する 1 つの方法であり、主に特定のデータ型の式を手動で無効にするために使用されます。

### プッシュダウンがサポートされている式 {#expressions-that-are-supported-to-be-pushed-down}

プッシュダウンがサポートされている式の詳細については、 [TiKVへのプッシュダウンでサポートされている式](/functions-and-operators/expressions-pushed-down.md#supported-expressions-for-pushdown-to-tikv)参照してください。

### 特定の式のプッシュダウンを無効にする {#disable-the-pushdown-of-specific-expressions}

式のプッシュダウンによって間違った結果が返された場合、ブロックリストを使用してアプリケーションを迅速に回復できます。具体的には、サポートされている関数または演算子の一部を`mysql.expr_pushdown_blacklist`テーブルに追加して、特定の式のプッシュダウンを無効にすることができます。

`mysql.expr_pushdown_blacklist`のスキーマは次のようになります。

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
-   `store_type` : 計算のために関数がプッシュダウンされないようにするコンポーネントを指定します。使用可能なコンポーネントは`tidb` 、 `tikv` 、および`tiflash`です。 `store_type`は大文字と小文字を区別しません。複数のコンポーネントを指定する必要がある場合は、各コンポーネントをコンマで区切ります。
    -   `store_type`が`tidb`の場合、TiDBメモリテーブルの読み取り中に他の TiDB サーバーで関数を実行できるかどうかを示します。
    -   `store_type`が`tikv`の場合、関数が TiKV サーバーのコプロセッサーコンポーネントで実行できるかどうかを示します。
    -   `store_type`が`tiflash`場合、関数がTiFlash Server のコプロセッサーコンポーネントで実行できるかどうかを示します。
-   `reason` : この関数がブロックリストに追加された理由を記録します。

### 使用法 {#usage}

このセクションでは、式プッシュダウンのブロックリストの使用方法について説明します。

#### ブロックリストに追加 {#add-to-the-blocklist}

ブロックリストに 1 つ以上の式 (関数または演算子) を追加するには、次の手順を実行します。

1.  対応する関数名または演算子名と、プッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`テーブルに挿入します。

2.  `admin reload expr_pushdown_blacklist`実行します。

### ブロックリストから削除 {#remove-from-the-blocklist}

ブロックリストから 1 つ以上の式を削除するには、次の手順を実行します。

1.  対応する関数名または演算子名、およびプッシュダウンを無効にするコンポーネントのセットを`mysql.expr_pushdown_blacklist`テーブルから削除します。

2.  `admin reload expr_pushdown_blacklist`実行します。

> **注記：**
>
> `admin reload expr_pushdown_blacklist` 、このステートメントが実行された TiDBサーバーにのみ有効になります。クラスターのすべての TiDB サーバーに有効にするには、各 TiDBサーバーでこのコマンドを実行します。

## 表現ブロックリストの使用例 {#expression-blocklist-usage-example}

次の例では、 `<`および`>`演算子がブロックリストに追加され、 `>`演算子がブロックリストから削除されます。

ブロックリストが有効かどうかを判断するには、 `EXPLAIN`の結果を観察します（ [TiDB クエリ実行プランの概要](/explain-overview.md)参照）。

1.  次の SQL ステートメントの`WHERE`番目の句の述語`a < 2`と`a > 2` 、TiKV にプッシュダウンできます。

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

2.  式を`mysql.expr_pushdown_blacklist`テーブルに挿入し、 `admin reload expr_pushdown_blacklist`実行します。

    ```sql
    INSERT INTO mysql.expr_pushdown_blacklist VALUES('<','tikv',''), ('>','tikv','');
    ```

    ```sql
    Query OK, 2 rows affected (0.01 sec)
    Records: 2  Duplicates: 0  Warnings: 0
    ```

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

3.  実行プランをもう一度観察すると、演算子`<`と`>`両方が TiKVコプロセッサーにプッシュダウンされていないことがわかります。

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

4.  ブロックリストから 1 つの式 (ここでは`>` ) を削除し、 `admin reload expr_pushdown_blacklist`実行します。

    ```sql
    DELETE FROM mysql.expr_pushdown_blacklist WHERE name = '>';
    ```

    ```sql
    Query OK, 1 row affected (0.01 sec)
    ```

    ```sql
    admin reload expr_pushdown_blacklist;
    ```

    ```sql
    Query OK, 0 rows affected (0.00 sec)
    ```

5.  実行プランをもう一度観察すると、 `<`​​プッシュダウンされていないのに対し、 `>` TiKVコプロセッサーにプッシュダウンされていることがわかります。

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

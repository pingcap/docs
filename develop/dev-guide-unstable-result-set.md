---
title: Unstable Result Set
summary: Learn how to handle the error of an unstable result set.
---

# 不安定な結果セット {#unstable-result-set}

このドキュメントでは、不安定な結果セットエラーを解決する方法について説明します。

## GROUP BY {#group-by}

便宜上、MySQLは`GROUP BY`構文を「拡張」して、 `SELECT`句が`GROUP BY`句で宣言されていない非集約フィールド、つまり`NON-FULL GROUP BY`構文を参照できるようにします。他のデータベースでは、これは不安定な結果セットを引き起こすため、構文***エラー***と見なされます。

たとえば、次の2つのテーブルがあります。

-   `stu_info`は学生情報を保存します
-   `stu_score`は学生のテストスコアを保存します。

次に、次のようなSQLクエリステートメントを記述できます。

{{< copyable "" >}}

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`,
    `a`.`stuname`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

結果：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
| 2018_CS_03 | SpongeBob    |             95.0 |
+------------+--------------+------------------+
3 rows in set (0.00 sec)
```

`a` 。 `class`と`a` 。 `GROUP BY`ステートメントで`stuname`のフィールドが指定され、選択された列は`a`です。 `class` `a` `stuname`と`b` 。 `courscore` 。 `GROUP BY`の状態にない唯一の列、 `b` 。 `courscore`は、 `max()`関数を使用して一意の値で指定されます。 `FULL GROUP BY`構文と呼ばれる、あいまいさのないこのSQLステートメントを***満たす***結果は1つだけです。

反例は`NON-FULL GROUP BY`構文です。たとえば、これら2つのテーブルに、次のSQLクエリを記述します（ `GROUP BY`の`stuname`を削除し`a` ）。

{{< copyable "" >}}

```sql
SELECT
    `a`.`class`,
    `a`.`stuname`,
    max( `b`.`courscore` )
FROM
    `stu_info` `a`
    JOIN `stu_score` `b` ON `a`.`stuno` = `b`.`stuno`
GROUP BY
    `a`.`class`
ORDER BY
    `a`.`class`,
    `a`.`stuname`;
```

次に、このSQLに一致する2つの値が返されます。

最初の戻り値：

```sql
+------------+--------------+------------------------+
| class      | stuname      | max( `b`.`courscore` ) |
+------------+--------------+------------------------+
| 2018_CS_01 | MonkeyDLuffy |                   95.5 |
| 2018_CS_03 | PatrickStar  |                   99.0 |
+------------+--------------+------------------------+
```

2番目の戻り値：

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
```

`a`の値を取得する***方法***を指定しなかったため、2つの結果があります。 SQLの`stuname`フィールド、および2つの結果は両方ともSQLセマンティクスによって満たされます。結果セットが不安定になります。したがって、 `GROUP BY`ステートメントの結果セットの安定性を保証する場合は、 `FULL GROUP BY`構文を使用してください。

MySQLには、構文をチェックするかどうかを制御するための`sql_mode`スイッチ`ONLY_FULL_GROUP_BY`が用意されて`FULL GROUP BY`ます。 TiDBはこの`sql_mode`スイッチとも互換性があります。

{{< copyable "" >}}

```sql
mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | PatrickStar  |             99.0 |
+------------+--------------+------------------+
2 rows in set (0.01 sec)

mysql> set @@sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION,ONLY_FULL_GROUP_BY';
Query OK, 0 rows affected (0.01 sec)

mysql> select a.class, a.stuname, max(b.courscore) from stu_info a join stu_score b on a.stuno=b.stuno group by a.class order by a.class, a.stuname;
ERROR 1055 (42000): Expression #2 of ORDER BY is not in GROUP BY clause and contains nonaggregated column '' which is not functionally dependent on columns in GROUP BY clause; this is incompatible with sql_mode=only_full_group_by
```

**実行結果**：上記の例は、 `ONLY_FULL_GROUP_BY`を`sql_mode`に設定した場合の効果を示しています。

## 注文者 {#order-by}

SQLセマンティクスでは、 `ORDER BY`構文が使用されている場合にのみ、結果セットが順番に出力されます。シングルインスタンスデータベースの場合、データは1つのサーバーに保存されるため、複数の実行の結果は、データを再編成しなくても安定していることがよくあります。一部のデータベース（特にMySQL InnoDBストレージエンジン）は、主キーまたはインデックスの順序で結果セットを出力することもできます。

分散データベースとして、TiDBは複数のサーバーにデータを保存します。さらに、TiDBレイヤーはデータページをキャッシュしないため、 `ORDER BY`がないSQLステートメントの結果セットの順序は不安定であると簡単に認識されます。順次結果セットを出力するには、SQLセマンティクスに準拠するorderフィールドを`ORDER BY`句に明示的に追加する必要があります。

次の例では、 `ORDER BY`句に1つのフィールドのみが追加され、TiDBはその1つのフィールドで結果のみを並べ替えます。

{{< copyable "" >}}

```sql
mysql> select a.class, a.stuname, b.course, b.courscore from stu_info a join stu_score b on a.stuno=b.stuno order by a.class;
+------------+--------------+-------------------------+-----------+
| class      | stuname      | course                  | courscore |
+------------+--------------+-------------------------+-----------+
| 2018_CS_01 | MonkeyDLuffy | PrinciplesofDatabase    |      60.5 |
| 2018_CS_01 | MonkeyDLuffy | English                 |      43.0 |
| 2018_CS_01 | MonkeyDLuffy | OpSwimming              |      67.0 |
| 2018_CS_01 | MonkeyDLuffy | OpFencing               |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | FundamentalsofCompiling |      88.0 |
| 2018_CS_01 | MonkeyDLuffy | OperatingSystem         |      90.5 |
| 2018_CS_01 | MonkeyDLuffy | PrincipleofStatistics   |      69.0 |
| 2018_CS_01 | MonkeyDLuffy | ProbabilityTheory       |      76.0 |
| 2018_CS_01 | MonkeyDLuffy | Physics                 |      63.5 |
| 2018_CS_01 | MonkeyDLuffy | AdvancedMathematics     |      95.5 |
| 2018_CS_01 | MonkeyDLuffy | LinearAlgebra           |      92.5 |
| 2018_CS_01 | MonkeyDLuffy | DiscreteMathematics     |      89.0 |
| 2018_CS_03 | SpongeBob    | PrinciplesofDatabase    |      88.0 |
| 2018_CS_03 | SpongeBob    | English                 |      79.0 |
| 2018_CS_03 | SpongeBob    | OpBasketball            |      92.0 |
| 2018_CS_03 | SpongeBob    | OpTennis                |      94.0 |
| 2018_CS_03 | PatrickStar  | LinearAlgebra           |       6.5 |
| 2018_CS_03 | PatrickStar  | AdvancedMathematics     |       5.0 |
| 2018_CS_03 | SpongeBob    | DiscreteMathematics     |      72.0 |
| 2018_CS_03 | PatrickStar  | ProbabilityTheory       |      12.0 |
| 2018_CS_03 | PatrickStar  | PrincipleofStatistics   |      20.0 |
| 2018_CS_03 | PatrickStar  | OperatingSystem         |      36.0 |
| 2018_CS_03 | PatrickStar  | FundamentalsofCompiling |       2.0 |
| 2018_CS_03 | PatrickStar  | DiscreteMathematics     |      14.0 |
| 2018_CS_03 | PatrickStar  | PrinciplesofDatabase    |       9.0 |
| 2018_CS_03 | PatrickStar  | English                 |      60.0 |
| 2018_CS_03 | PatrickStar  | OpTableTennis           |      12.0 |
| 2018_CS_03 | PatrickStar  | OpPiano                 |      99.0 |
| 2018_CS_03 | SpongeBob    | FundamentalsofCompiling |      43.0 |
| 2018_CS_03 | SpongeBob    | OperatingSystem         |      95.0 |
| 2018_CS_03 | SpongeBob    | PrincipleofStatistics   |      90.0 |
| 2018_CS_03 | SpongeBob    | ProbabilityTheory       |      87.0 |
| 2018_CS_03 | SpongeBob    | Physics                 |      65.0 |
| 2018_CS_03 | SpongeBob    | AdvancedMathematics     |      55.0 |
| 2018_CS_03 | SpongeBob    | LinearAlgebra           |      60.5 |
| 2018_CS_03 | PatrickStar  | Physics                 |       6.0 |
+------------+--------------+-------------------------+-----------+
36 rows in set (0.01 sec)

```

`ORDER BY`の値が同じ場合、結果は不安定になります。ランダム性を減らすには、 `ORDER BY`の値が一意である必要があります。一意性を保証できない場合は、 `ORDER BY`の`ORDER BY`のフィールドの組み合わせが一意になるまで、さらに`ORDER BY`のフィールドを追加する必要があります。そうすると、結果は安定します。

## <code>GROUP_CONCAT()</code>でorder byが使用されていないため、結果セットは不安定です。 {#the-result-set-is-unstable-because-order-by-is-not-used-in-code-group-concat-code}

TiDBはストレージレイヤーからデータを並行して読み取るため、結果セットは不安定です。したがって、 `ORDER BY`なしで`GROUP_CONCAT()`によって返される結果セットの順序は、不安定であると簡単に認識されます。

`GROUP_CONCAT()`が結果セットの出力を順番に取得できるようにするには、SQLセマンティクスに準拠する`ORDER BY`句に並べ替えフィールドを追加する必要があります。次の例では、 `ORDER BY`なしで`customer_id`をスプライスする`GROUP_CONCAT()`は、不安定な結果セットを引き起こします。

1.  除外`ORDER BY`

    最初のクエリ：

    {{< copyable "" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
    +-------------------------------------------------------------------------+
    ```

    2番目のクエリ：

    {{< copyable "" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
    +-------------------------------------------------------------------------+
    ```

2.  `ORDER BY`を含む

    最初のクエリ：

    {{< copyable "" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

    2番目のクエリ：

    {{< copyable "" >}}

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

## 不安定な結果は<code>SELECT * FROM T LIMIT N</code> TLIMITNになります {#unstable-results-in-code-select-from-t-limit-n-code}

返される結果は、ストレージノード（TiKV）でのデータの分散に関連しています。複数のクエリが実行されると、ストレージノード（TiKV）の異なるストレージユニット（Regions）が異なる速度で結果を返し、不安定な結果を引き起こす可能性があります。

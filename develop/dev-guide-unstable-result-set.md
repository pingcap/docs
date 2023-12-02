---
title: Unstable Result Set
summary: Learn how to handle the error of an unstable result set.
---

# 不安定な結果セット {#unstable-result-set}

このドキュメントでは、不安定な結果セット エラーを解決する方法について説明します。

## グループ化 {#group-by}

便宜上、MySQL は`GROUP BY`構文を「拡張」して、 `SELECT`句が`GROUP BY`句で宣言されていない非集計フィールド、つまり`NON-FULL GROUP BY`構文を参照できるようにします。他のデータベースでは、結果セットが不安定になるため、これは構文***エラー***とみなされます。

たとえば、次の 2 つのテーブルがあるとします。

-   `stu_info`学生情報を保存します
-   `stu_score`は学生のテストのスコアが保存されます。

次に、次のような SQL クエリ ステートメントを作成できます。

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

`a` ． `class`と`a` 。 `GROUP BY`ステートメントでは`stuname`フィールドが指定されており、選択された列は`a`です。 `class` `a` `stuname`および`b` 。 `courscore` ． `GROUP BY`条件にない唯一の列`b` 。 `courscore`は、 `max()`関数を使用して一意の値でも指定されます。この SQL ステートメントを曖昧さなく満たす結果は***1 つだけ***あり、これは`FULL GROUP BY`構文と呼ばれます。

反例は`NON-FULL GROUP BY`構文です。たとえば、これら 2 つのテーブルに次の SQL クエリを記述します (delete `a` . `stuname` in `GROUP BY` )。

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

次に、この SQL に一致する 2 つの値が返されます。

最初の戻り値:

```sql
+------------+--------------+------------------------+
| class      | stuname      | max( `b`.`courscore` ) |
+------------+--------------+------------------------+
| 2018_CS_01 | MonkeyDLuffy |                   95.5 |
| 2018_CS_03 | PatrickStar  |                   99.0 |
+------------+--------------+------------------------+
```

2 番目の戻り値:

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
```

`a`の値を取得する方法を指定***し***なかったため、結果は 2 つになります。 SQL の`stuname`フィールドと 2 つの結果は両方とも SQL セマンティクスによって満たされます。結果セットが不安定になります。したがって、 `GROUP BY`ステートメントの結果セットの安定性を保証したい場合は、 `FULL GROUP BY`構文を使用してください。

MySQL には、 `FULL GROUP BY`構文をチェックするかどうかを制御する`sql_mode`スイッチ`ONLY_FULL_GROUP_BY`用意されています。 TiDB はこの`sql_mode`スイッチにも対応しています。

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

**実行結果**: 上記の例は、 `sql_mode`を`ONLY_FULL_GROUP_BY`に設定した場合の効果を示しています。

## 注文方法 {#order-by}

SQL セマンティクスでは、 `ORDER BY`構文が使用されている場合にのみ、結果セットが順番に出力されます。単一インスタンスのデータベースの場合、データは 1 つのサーバーに保存されるため、複数の実行結果はデー​​タを再編成しなくても安定していることがよくあります。一部のデータベース (特に MySQL InnoDBstorageエンジン) は、主キーまたはインデックスの順序で結果セットを出力することもできます。

分散データベースとして、TiDB は複数のサーバーにデータを保存します。さらに、TiDBレイヤーはデータ ページをキャッシュしないため、 `ORDER BY`のない SQL ステートメントの結果セットの順序は不安定であると認識されやすくなります。順次結果セットを出力するには、SQL セマンティクスに準拠した order フィールドを`ORDER BY`句に明示的に追加する必要があります。

次の例では、フィールドが 1 つだけ`ORDER BY`句に追加され、TiDB はその 1 つのフィールドによってのみ結果を並べ替えます。

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

`ORDER BY`値が同じ場合、結果は不安定になります。ランダム性を減らすために、 `ORDER BY`値は一意である必要があります。一意性が保証できない場合は、 `ORDER BY`フィールドの`ORDER BY`の組み合わせが一意になるまで、さらに`ORDER BY`フィールドを追加する必要があります。そうすれば、結果は安定します。

## <code>GROUP_CONCAT()</code>で order by が使用されていないため、結果セットは不安定です {#the-result-set-is-unstable-because-order-by-is-not-used-in-code-group-concat-code}

TiDB はstorageレイヤーから並行してデータを読み取るため、結果セットが不安定になります。そのため、 `ORDER BY`なしで`GROUP_CONCAT()`によって返される結果セットの順序は、不安定であると認識されやすいです。

`GROUP_CONCAT()`が結果セット出力を順番に取得できるようにするには、SQL セマンティクスに準拠したソート フィールドを`ORDER BY`句に追加する必要があります。次の例では、 `ORDER BY`を使用せずに`customer_id`を接合する`GROUP_CONCAT()`により、結果セットが不安定になります。

1.  除外`ORDER BY`

    最初のクエリ:

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200992,20000200993,20000200994,20000200995,20000200996,20000200... |
    +-------------------------------------------------------------------------+
    ```

    2 番目のクエリ:

    ```sql
    mysql>  select GROUP_CONCAT( customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000203040,20000203041,20000203042,20000203043,20000203044,20000203... |
    +-------------------------------------------------------------------------+
    ```

2.  `ORDER BY`を含む

    最初のクエリ:

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

    2 番目のクエリ:

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

## <code>SELECT * FROM T LIMIT N</code>の結果が不安定になる {#unstable-results-in-code-select-from-t-limit-n-code}

返された結果は、storageノード (TiKV) 上のデータの分散に関連しています。複数のクエリが実行される場合、storageノード (TiKV) の異なるstorageユニット (リージョン) が異なる速度で結果を返すため、結果が不安定になる可能性があります。

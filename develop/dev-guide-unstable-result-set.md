---
title: Unstable Result Set
summary: 不安定な結果セットのエラーを処理する方法を学習します。
---

# 不安定な結果セット {#unstable-result-set}

このドキュメントでは、不安定な結果セットのエラーを解決する方法について説明します。

## グループ化 {#group-by}

便宜上、MySQL は`GROUP BY`構文を「拡張」して、 `SELECT`句が`GROUP BY`句で宣言されていない非集約フィールド、つまり`NON-FULL GROUP BY`構文を参照できるようにします。他のデータベースでは、結果セットが不安定になるため、これは構文***エラー***と見なされます。

たとえば、次の 2 つのテーブルがあるとします。

-   `stu_info`学生情報を保存します
-   `stu_score`生徒のテストのスコアが格納されます。

次に、次のような SQL クエリ ステートメントを記述します。

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

`a` . `class`および`a` . `stuname`フィールドは`GROUP BY`ステートメントで指定され、選択された列は`a` . `class` 、 `a` . `stuname`および`b` . `courscore`です。 `GROUP BY`条件にない唯一の列`b` . `courscore`も、 `max()`関数を使用して一意の値で指定されます。 この SQL ステートメントを曖昧さなく満たす結果は***1 つだけ***あり、これを`FULL GROUP BY`構文と呼びます。

反例は`NON-FULL GROUP BY`構文です。たとえば、これら 2 つのテーブルでは、次の SQL クエリ (delete `a` . `stuname` in `GROUP BY` ) を記述します。

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

すると、この SQL に一致する 2 つの値が返されます。

最初に返される値:

```sql
+------------+--------------+------------------------+
| class      | stuname      | max( `b`.`courscore` ) |
+------------+--------------+------------------------+
| 2018_CS_01 | MonkeyDLuffy |                   95.5 |
| 2018_CS_03 | PatrickStar  |                   99.0 |
+------------+--------------+------------------------+
```

2 番目に返される値:

```sql
+------------+--------------+------------------+
| class      | stuname      | max(b.courscore) |
+------------+--------------+------------------+
| 2018_CS_01 | MonkeyDLuffy |             95.5 |
| 2018_CS_03 | SpongeBob    |             99.0 |
+------------+--------------+------------------+
```

`a`フィールドの値を SQL で取得する方法を指定しておら***ず***、2 つの結果が両方とも SQL セマンティクスによって満たされているため、結果が 2 つあります。その結果、結果セットが不安定に`stuname`ます。したがって、 `GROUP BY`ステートメントの結果セットの安定性を保証する場合は、 `FULL GROUP BY`構文を使用します。

MySQL は、 `FULL GROUP BY`構文をチェックするかどうかを制御する`sql_mode`スイッチ`ONLY_FULL_GROUP_BY`を提供します。TiDB もこの`sql_mode`スイッチと互換性があります。

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

**実行結果**: 上記の例は、 `sql_mode`に`ONLY_FULL_GROUP_BY`設定した場合の効果を示しています。

## 注文する {#order-by}

SQL セマンティクスでは、 `ORDER BY`構文が使用されている場合にのみ、結果セットが順番に出力されます。単一インスタンス データベースの場合、データは 1 つのサーバーに保存されるため、複数回実行した結果は、データの再編成なしで安定していることがよくあります。一部のデータベース (特に MySQL InnoDBstorageエンジン) では、主キーまたはインデックスの順序で結果セットを出力することもできます。

分散データベースである TiDB は、複数のサーバーにデータを格納します。また、TiDBレイヤーはデータ ページをキャッシュしないため、 `ORDER BY`のない SQL ステートメントの結果セットの順序は不安定であると認識されやすくなります。連続した結果セットを出力するには、SQL セマンティクスに準拠する`ORDER BY`節に order フィールドを明示的に追加する必要があります。

次の例では、 `ORDER BY`句に 1 つのフィールドのみが追加され、TiDB はその 1 つのフィールドのみで結果を並べ替えます。

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

`ORDER BY`値が同じ場合、結果は不安定になります。ランダム性を減らすには、 `ORDER BY`値が一意である必要があります。一意性を保証できない場合は、 `ORDER BY`のフィールドの`ORDER BY`の組み合わせが一意になるまで、さらに`ORDER BY`フィールドを追加する必要があります。そうすれば、結果は安定します。

## <code>GROUP_CONCAT()</code>で order by が使用されていないため、結果セットは不安定です。 {#the-result-set-is-unstable-because-order-by-is-not-used-in-code-group-concat-code}

TiDB はstorageレイヤーからデータを並列に読み取るため、結果セットは不安定になり、 `ORDER BY`なしで`GROUP_CONCAT()`によって返される結果セットの順序は不安定であると簡単に認識されます。

`GROUP_CONCAT()`結果セット出力を順序どおりに取得できるようにするには、SQL セマンティクスに準拠する`ORDER BY`句にソート フィールドを追加する必要があります。次の例では、 `ORDER BY`なしで`customer_id`結合する`GROUP_CONCAT()`によって、不安定な結果セットが発生します。

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

    2番目のクエリ:

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

    2番目のクエリ:

    ```sql
    mysql>  select GROUP_CONCAT( customer_id order by customer_id SEPARATOR ',' ) FROM customer where customer_id like '200002%';
    +-------------------------------------------------------------------------+
    | GROUP_CONCAT(customer_id  SEPARATOR ',')                                |
    +-------------------------------------------------------------------------+
    | 20000200000,20000200001,20000200002,20000200003,20000200004,20000200... |
    +-------------------------------------------------------------------------+
    ```

## <code>SELECT * FROM T LIMIT N</code>で結果が不安定になる {#unstable-results-in-code-select-from-t-limit-n-code}

返される結果は、storageノード (TiKV) 上のデータの分散に関係します。複数のクエリを実行すると、storageノード (TiKV) の異なるstorageユニット (リージョン) が異なる速度で結果を返すため、結果が不安定になる可能性があります。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

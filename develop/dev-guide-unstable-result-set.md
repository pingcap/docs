---
title: Unstable Result Set
summary: 不安定な結果セットのエラーを処理する方法を学習します。
aliases: ['/ja/tidb/stable/dev-guide-unstable-result-set/','/ja/tidbcloud/dev-guide-unstable-result-set/']
---

# 不安定な結果セット {#unstable-result-set}

このドキュメントでは、不安定な結果セットのエラーを解決する方法について説明します。

## グループ化 {#group-by}

便宜上、MySQLは`GROUP BY`構文を「拡張」し、 `SELECT`番目の句で`GROUP BY`番目の句で宣言されていない非集約フィールドを参照できるようにしています。つまり、 `NON-FULL GROUP BY`構文です。他のデータベースでは、これは不安定な結果セットを引き起こすため、構文***エラー***とみなされます。

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

`a` . `class`および`a` . `stuname`フィールドは`GROUP BY`文で指定されており、選択された列は`a` . `class` 、 `a` . `stuname` 、 `b` . `courscore`です。23 `GROUP BY`条件に含まれない唯一の列である`b` . `courscore`も、 `max()`関数を使用して一意の値で指定されています。このSQL文を曖昧さなく満たす結果は***1つだけ***あり、これを`FULL GROUP BY`構文と呼びます。

反例として、構文`NON-FULL GROUP BY`があります。例えば、この2つのテーブルに次のSQLクエリを記述します (delete `a` . `stuname` in `GROUP BY` )。

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

結果が2つあるのは`stuname` SQLで`a`フィールドの値を取得する方法を指定しておら***ず***、2つの結果がどちらもSQLセマンティクスを満たしているためです。そのため、結果セットは不安定になります。したがって、 `GROUP BY`文の結果セットの安定性を保証したい場合は、 `FULL GROUP BY`構文を使用してください。

MySQLは、 `FULL GROUP BY`チェックを行うかどうかを制御するスイッチ`sql_mode`スイッチ`ONLY_FULL_GROUP_BY`を提供しています。TiDBもこのスイッチ`sql_mode`と互換性があります。

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

## 注文方法 {#order-by}

SQLセマンティクスでは、 `ORDER BY`構文が使用されている場合にのみ結果セットが順序通りに出力されます。単一インスタンスのデータベースでは、データが1つのサーバーに保存されるため、複数回実行してもデータの再編成なしで結果が安定することがよくあります。一部のデータベース（特にMySQL InnoDBstorageエンジン）では、主キーまたはインデックスの順序で結果セットを出力することも可能です。

分散データベースであるTiDBは、複数のサーバーにデータを保存しています。また、TiDBレイヤーはデータページをキャッシュしないため、 `ORDER BY`を含まないSQL文の結果セットの順序は不安定であると認識されやすくなります。連続した結果セットを出力するには、SQLセマンティクスに準拠した`ORDER BY`節に明示的に順序フィールドを追加する必要があります。

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

`ORDER BY`値が同じ場合、結果は不安定になります。ランダム性を低減するには、 `ORDER BY`値が一意である必要があります。一意性を保証できない場合は、 `ORDER BY`のフィールドのうち`ORDER BY`フィールドの組み合わせが一意になるまで、さらに`ORDER BY`フィールドを追加する必要があります。そうすれば、結果は安定します。

## <code>GROUP_CONCAT()</code>で order by が使用されていないため、結果セットは不安定です。 {#the-result-set-is-unstable-because-order-by-is-not-used-in-code-group-concat-code}

TiDB はstorageレイヤーからデータを並列に読み取るため、結果セットは不安定になります。そのため、 `ORDER BY`なしで`GROUP_CONCAT()`によって返される結果セットの順序は不安定であると簡単に認識されます。

`GROUP_CONCAT()`結果セットの出力を順序通りにするには、SQLセマンティクスに準拠した`ORDER BY`節にソートフィールドを追加する必要があります。次の例では、 `ORDER BY`を除いた`customer_id`を連結する`GROUP_CONCAT()`によって、結果セットが不安定になります。

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

2.  `ORDER BY`含む

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

返される結果は、storageノード（TiKV）上のデータの分散状況に関係します。複数のクエリを実行すると、storageノード（TiKV）の異なるstorageユニット（リージョン）から異なる速度で結果が返されるため、結果が不安定になる可能性があります。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)

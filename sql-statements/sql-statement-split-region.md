---
title: Split Region
summary: An overview of the usage of Split Region for the TiDB database.
---

# スプリットリージョン {#split-region}

TiDBで作成された新しいテーブルごとに、このテーブルのデータを格納するためにデフォルトで[領域](/tidb-storage.md#region)つがセグメント化されます。このデフォルトの動作は、TiDB構成ファイルの`split-table`によって制御されます。このリージョンのデータがデフォルトのリージョンサイズ制限を超えると、リージョンは2つに分割され始めます。

上記の場合、最初にリージョンが1つしかないため、すべての書き込み要求は、リージョンが配置されているTiKVで発生します。新しく作成されたテーブルへの書き込みが多い場合、ホットスポットが発生します。

上記のシナリオでのホットスポットの問題を解決するために、TiDBは事前分割機能を導入します。この関数は、指定されたパラメーターに従って特定のテーブルの複数のリージョンを事前分割し、それらを各TiKVノードに分散させることができます。

## あらすじ {#synopsis}

**SplitRegionStmt：**

![SplitRegionStmt](/media/sqlgram/SplitRegionStmt.png)

**SplitSyntaxOption：**

![SplitSyntaxOption](/media/sqlgram/SplitSyntaxOption.png)

**TableName：**

![TableName](/media/sqlgram/TableName.png)

**PartitionNameListOpt：**

![PartitionNameListOpt](/media/sqlgram/PartitionNameListOpt.png)

**SplitOption：**

![SplitOption](/media/sqlgram/SplitOption.png)

**RowValue：**

![RowValue](/media/sqlgram/RowValue.png)

**Int64Num：**

![Int64Num](/media/sqlgram/Int64Num.png)

## 分割領域の使用 {#usage-of-split-region}

分割領域の構文には、次の2つのタイプがあります。

-   偶数分割の構文：

    {{< copyable "" >}}

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num`は、上限、下限、およびリージョンの量を定義します。次に、現在の領域が、上限と下限の間の領域の数（ `region_num`で指定）に均等に流出します。

-   不均一な分割の構文：

    {{< copyable "" >}}

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…`は、現在のリージョンがスピルトされることに基づいて、一連のポイントを手動で指定します。データが不均一に分散しているシナリオに適しています。

次の例は、 `SPLIT`ステートメントの結果を示しています。

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

-   `TOTAL_SPLIT_REGION` ：新しく分割されたリージョンの数。
-   `SCATTER_FINISH_RATIO` ：新しく分割されたリージョンの散乱の完了率。 `1.0`は、すべてのリージョンが分散していることを意味します。 `0.5`は、リージョンの半分だけが分散され、残りが分散されていることを意味します。

> **ノート：**
>
> 次の2つのセッション変数は、 `SPLIT`ステートメントの動作に影響を与える可能性があります。
>
> -   `tidb_wait_split_region_finish` ：リージョンを分散させるのに時間がかかる場合があります。この期間は、PDスケジューリングとTiKV負荷によって異なります。この変数は、 `SPLIT REGION`ステートメントを実行するときに、すべてのリージョンが分散するまで結果をクライアントに返すかどうかを制御するために使用されます。その値が`1` （デフォルト）に設定されている場合、TiDBはスキャッタリングが完了した後にのみ結果を返します。その値が`0`に設定されている場合、TiDBは散乱状態に関係なく結果を返します。
> -   `tidb_wait_split_region_timeout` ：この変数は、 `SPLIT REGION`ステートメントの実行タイムアウトを秒単位で設定します。デフォルト値は300秒です。 `split`の操作が期間内に完了しない場合、TiDBはタイムアウトエラーを返します。

### 分割テーブル領域 {#split-table-region}

各テーブルの行データのキーは、 `table_id`と`row_id`でエンコードされます。形式は次のとおりです。

```go
t[table_id]_r[row_id]
```

たとえば、 `table_id`が22で、 `row_id`が11の場合：

```go
t22_r11
```

同じテーブルの行データには同じ`table_id`がありますが、各行には、リージョン分割に使用できる一意の`row_id`があります。

#### スプリットさえ {#even-split}

`row_id`は整数であるため、分割するキーの値は、指定した`lower_value` 、および`upper_value`に従って計算でき`region_num` 。 TiDBは最初にステップ値（ `step = (upper_value - lower_value)/region_num` ）を計算します。次に、 `lower_value`から`upper_value`までの各「ステップ」ごとに均等に分割が行われ、 `region_num`で指定された数のリージョンが生成されます。

たとえば、テーブルtのキー範囲`minInt64`から16の均等に分割されたリージョンが必要な場合は、次のステートメントを使用でき`maxInt64` 。

{{< copyable "" >}}

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブルtをminInt64とmaxInt64の間の16のリージョンに分割します。指定された主キーの範囲が指定された範囲よりも小さい場合（たとえば、0〜1000000000）、minInt64とmaxInt64の代わりに0と1000000000を使用して、リージョンを分割できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不均一な分割 {#uneven-split}

既知のデータが不均一に分散されており、リージョンをキー範囲-inf〜10000、10000〜90000、および90000〜 + infにそれぞれ分割する場合は、以下に示すように、固定小数点を設定することでこれを実現できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t BY (10000), (90000);
```

### スプリットインデックスリージョン {#split-index-region}

テーブル内のインデックスデータのキーは、 `table_id` 、およびインデックス列の`index_id`によってエンコードされます。形式は次のとおりです。

```go
t[table_id]_i[index_id][index_value]
```

たとえば、 `table_id`が22の場合、 `index_id`は5であり、 `index_value`はabcです。

```go
t22_i5abc
```

1つのテーブル内の同じインデックスデータの`table_id`と`index_id`は同じです。インデックスリージョンを分割するには、 `index_value`に基づいてリージョンを分割する必要があります。

#### こぼれたとしても {#even-spilt}

インデックスを均等に分割する方法は、データを均等に分割するのと同じように機能します。ただし、 `index_value`は整数ではない可能性があるため、stepの値の計算はより複雑です。

`upper`と`lower`の値は、最初にバイト配列にエンコードされます。 `lower`バイトと`upper`バイトの配列の最長の共通プレフィックスを削除した後、 `lower`バイトと`upper`バイトの最初の8バイトがuint64形式に変換されます。次に、 `step = (upper - lower)/num`が計算されます。その後、計算されたステップはバイト配列にエンコードされ、インデックス分割のために`lower`バイト配列と`upper`バイト配列の最長の共通プレフィックスに追加されます。次に例を示します。

`idx`インデックスの列が整数型の場合、次のSQLステートメントを使用してインデックスデータを分割できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブルtのインデックスidxのリージョンを`minInt64`から`maxInt64`までの16のリージョンに分割します。

インデックスidx1の列がvarcharタイプであり、インデックスデータをプレフィックス文字で分割する場合。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

このステートメントは、インデックスidx1をa〜zから25のリージョンに分割します。リージョン1の範囲は`[minIndexValue, b)`です。リージョン2の範囲は`[b, c)`です。 …リージョン25の範囲は`[y, minIndexValue]`です。 `idx`インデックスの場合、プレフィックスが`a`のデータはリージョン1に書き込まれ、プレフィックスが`b`のデータはリージョン2に書き込まれます。

上記のsplitメソッドでは、上限が`z`ではなく`{` （ASCIIでは`z`の隣の文字）であるため、プレフィックスが`y`と`z`の両方のデータがリージョン25に書き込まれます。したがって、より正確な分割方法は次のとおりです。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

このステートメントは、テーブル`t`のインデックスidx1をa〜3から26のリージョンに分割し`{` 。リージョン1の範囲は`[minIndexValue, b)`です。リージョン2の範囲は`[b, c)`です。 …リージョン25の範囲は`[y, z)`で、リージョン26の範囲は`[z, maxIndexValue)`です。

インデックス`idx2`の列がtimestamp/datetimeのような時間タイプであり、インデックスRegionを年ごとに分割する場合：

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

このステートメントは、表`t`のインデックス`idx2`のリージョンを`2010-01-01 00:00:00`から`2020-01-01 00:00:00`までの10のリージョンに分割します。リージョン1の範囲は`[minIndexValue,  2011-01-01 00:00:00)`です。リージョン2の範囲は`[2011-01-01 00:00:00, 2012-01-01 00:00:00)`などです。

インデックスリージョンを日ごとに分割する場合は、次の例を参照してください。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

このステートメントは、表`t`のインデックス`idex2`の2020年6月のデータを30のリージョンに分割し、各リージョンは1日を表します。

他のタイプのインデックス列の領域分割方法も同様です。

ジョイントインデックスのデータ領域分割の場合、唯一の違いは、複数の列の値を指定できることです。

たとえば、インデックス`idx3 (a, b)`には2つの列があり、列`a`はタイムスタンプタイプで、列`b`はintです。列`a`に従って時間範囲を分割するだけの場合は、SQLステートメントを使用して単一の列の時間インデックスを分割できます。この場合、 `lower_value`列と`upper_velue`列の列`b`の値を指定しないでください。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

同じ時間範囲内で、列bの列に従ってもう1つ分割を実行する場合。分割するときは、列bの値を指定するだけです。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

このステートメントは、列aと同じ時間プレフィックスを使用して、列bの値に従ってa〜zの範囲の10個の領域を分割します。列aに指定された値が異なる場合、この場合、列bの値は使用されない可能性があります。

#### 不均一な分割 {#uneven-split}

インデックスデータは、指定したインデックス値で分割することもできます。

たとえば、varchar型の列`a`とtimestamp型の列`b`を持つ`idx4 (a,b)`があります。

{{< copyable "" >}}

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

このステートメントは、4つのリージョンを分割するための3つの値を指定します。各地域の範囲は次のとおりです。

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

### パーティション化されたテーブルの分割領域 {#split-regions-for-partitioned-tables}

パーティション化されたテーブルのリージョンの分割は、通常のテーブルのリージョンの分割と同じです。唯一の違いは、すべてのパーティションに対して同じ分割操作が実行されることです。

-   偶数分割の構文：

    {{< copyable "" >}}

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

-   不均一な分割の構文：

    {{< copyable "" >}}

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### パーティション化されたテーブルの分割領域の例 {#examples-of-split-regions-for-partitioned-tables}

1.  パーティションテーブルを作成します`t` 。 2つのパーティションに分割されたハッシュテーブルを作成するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    create table t (a int,b int,index idx(a)) partition by hash(a) partitions 2;
    ```

    テーブル`t`を作成した後、リージョンはパーティションごとに分割されます。このテーブルのリージョンを表示するには、次の`SHOW TABLE REGIONS`の構文を使用します。

    {{< copyable "" >}}

    ```sql
    show table t regions;
    ```

    ```sql
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 1978      | t_1400_   | t_1401_ | 1979      | 4               | 1979, 1980, 1981 | 0          | 0             | 0          | 1                    | 0                |
    | 6         | t_1401_   |         | 17        | 4               | 17, 18, 21       | 0          | 223           | 0          | 1                    | 0                |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

2.  `SPLIT`構文を使用して、パーティションごとにリージョンを分割します。各パーティションの`[0,10000]`の範囲のデータを4つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上記のステートメントで、 `0`と`10000`はそれぞれ、分散するホットスポットデータに対応する上限と下限の`row_id`を表します。

    > **ノート：**
    >
    > この例は、ホットスポットデータが均等に分散されているシナリオにのみ適用されます。ホットスポットデータが指定されたデータ範囲に不均一に分散している場合は、 [パーティション化されたテーブルの分割領域](#split-regions-for-partitioned-tables)の不均一な分割の構文を参照してください。

3.  `SHOW TABLE REGIONS`構文を使用して、このテーブルのリージョンを再度表示します。このテーブルには10個のリージョンがあり、各パーティションには5つのリージョンがあり、そのうち4つは行データで、1つはインデックスデータであることがわかります。

    {{< copyable "" >}}

    ```sql
    show table t regions;
    ```

    ```sql
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY     | END_KEY       | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 1998      | t_1400_r      | t_1400_r_2500 | 2001      | 5               | 2000, 2001, 2015 | 0          | 132           | 0          | 1                    | 0                |
    | 2006      | t_1400_r_2500 | t_1400_r_5000 | 2016      | 1               | 2007, 2016, 2017 | 0          | 35            | 0          | 1                    | 0                |
    | 2010      | t_1400_r_5000 | t_1400_r_7500 | 2012      | 2               | 2011, 2012, 2013 | 0          | 35            | 0          | 1                    | 0                |
    | 1978      | t_1400_r_7500 | t_1401_       | 1979      | 4               | 1979, 1980, 1981 | 0          | 621           | 0          | 1                    | 0                |
    | 1982      | t_1400_       | t_1400_r      | 2014      | 3               | 1983, 1984, 2014 | 0          | 35            | 0          | 1                    | 0                |
    | 1990      | t_1401_r      | t_1401_r_2500 | 1992      | 2               | 1991, 1992, 2020 | 0          | 120           | 0          | 1                    | 0                |
    | 1994      | t_1401_r_2500 | t_1401_r_5000 | 1997      | 5               | 1996, 1997, 2021 | 0          | 129           | 0          | 1                    | 0                |
    | 2002      | t_1401_r_5000 | t_1401_r_7500 | 2003      | 4               | 2003, 2023, 2022 | 0          | 141           | 0          | 1                    | 0                |
    | 6         | t_1401_r_7500 |               | 17        | 4               | 17, 18, 21       | 0          | 601           | 0          | 1                    | 0                |
    | 1986      | t_1401_       | t_1401_r      | 1989      | 5               | 1989, 2018, 2019 | 0          | 123           | 0          | 1                    | 0                |
    +-----------+---------------+---------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

4.  各パーティションのインデックスのリージョンを分割することもできます。たとえば、 `idx`のインデックスの`[1000,10000]`つの範囲を2つのリージョンに分割できます。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t index idx between (1000) and (10000) regions 2;
    ```

#### 単一パーティションの分割領域の例 {#examples-of-split-region-for-a-single-partition}

分割するパーティションを指定できます。

1.  パーティションテーブルを作成します。 3つのパーティションに分割されたRangeパーティションテーブルを作成するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    create table t ( a int, b int, index idx(b)) partition by range( a ) (
        partition p1 values less than (10000),
        partition p2 values less than (20000),
        partition p3 values less than (MAXVALUE) );
    ```

2.  `p1`のパーティションの`[0,10000]`つの範囲のデータを2つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t partition (p1) between (0) and (10000) regions 2;
    ```

3.  `p2`のパーティションの`[10000,20000]`つの範囲のデータを2つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t partition (p2) between (10000) and (20000) regions 2;
    ```

4.  `SHOW TABLE REGIONS`構文を使用して、このテーブルのリージョンを表示できます。

    {{< copyable "" >}}

    ```sql
    show table t regions;
    ```

    ```sql
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY      | END_KEY        | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 2040      | t_1406_        | t_1406_r_5000  | 2045      | 3               | 2043, 2045, 2044 | 0          | 0             | 0          | 1                    | 0                |
    | 2032      | t_1406_r_5000  | t_1407_        | 2033      | 4               | 2033, 2034, 2035 | 0          | 0             | 0          | 1                    | 0                |
    | 2046      | t_1407_        | t_1407_r_15000 | 2048      | 2               | 2047, 2048, 2050 | 0          | 35            | 0          | 1                    | 0                |
    | 2036      | t_1407_r_15000 | t_1408_        | 2037      | 4               | 2037, 2038, 2039 | 0          | 0             | 0          | 1                    | 0                |
    | 6         | t_1408_        |                | 17        | 4               | 17, 18, 21       | 0          | 214           | 0          | 1                    | 0                |
    +-----------+----------------+----------------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

5.  `p1`パーティションと`p2`パーティションの`idx`インデックスの`[0,20000]`の範囲を2つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t partition (p1,p2) index idx between (0) and (20000) regions 2;
    ```

## pre_split_regions {#pre-split-regions}

テーブルの作成時にリージョンを均等に分割するには、 `SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`を一緒に使用することをお勧めします。テーブルが正常に作成されると、 `PRE_SPLIT_REGIONS`は、 `2^(PRE_SPLIT_REGIONS)`で指定された数のリージョンにテーブルを事前にスピルします。

> **ノート：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`の値以下でなければなりません。

`tidb_scatter_region`グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響します。この変数は、テーブルの作成後に結果を返す前に、リージョンが事前に分割および分散されるのを待つかどうかを制御します。テーブルの作成後に集中的な書き込みがある場合は、この変数の値を`1`に設定する必要があります。そうすると、すべてのリージョンが分割されて分散されるまで、TiDBは結果をクライアントに返しません。そうしないと、TiDBはスキャッタリングが完了する前にデータを書き込みます。これは、書き込みパフォーマンスに大きな影響を及ぼします。

### pre_split_regionsの例 {#examples-of-pre-split-regions}

{{< copyable "" >}}

```sql
create table t (a int, b int,index idx1(a)) shard_row_id_bits = 4 pre_split_regions=2;
```

テーブルを作成した後、このステートメントはテーブルtの`4 + 1`のリージョンを分割します。 `4 (2^2)`のリージョンはテーブルの行データを保存するために使用され、1つのリージョンは`idx1`のインデックスデータを保存するために使用されます。

4つのテーブルリージョンの範囲は次のとおりです。

```
region1:   [ -inf      ,  1<<61 )
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

## ノート {#notes}

Split Regionステートメントによって分割されたRegionは、PDの[リージョンマージ](/best-practices/pd-scheduling-best-practices.md#region-merge)スケジューラーによって制御されます。 PDがすぐに新しく分割されたリージョンを再マージしないようにするには、リージョンマージ機能に関連する[動的に変更する](/pd-control.md)の構成アイテムを作成する必要があります。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。

## も参照してください {#see-also}

-   [テーブルの地域を表示する](/sql-statements/sql-statement-show-table-regions.md)
-   セッション[`tidb_wait_split_region_finish`](/system-variables.md#tidb_wait_split_region_finish) [`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout) [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) 。

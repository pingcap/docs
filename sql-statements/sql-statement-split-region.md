---
title: Split Region
summary: An overview of the usage of Split Region for the TiDB database.
---

# 分割リージョン {#split-region}

TiDB で作成された新しいテーブルごとに、デフォルトで 1 つの[リージョン](/tidb-storage.md#region)がセグメント化され、このテーブルのデータが格納されます。このデフォルトの動作は、TiDB 構成ファイルの`split-table`によって制御されます。このリージョンのデータがデフォルトのリージョンサイズ制限を超えると、リージョンは2 つに分割され始めます。

上記の場合、先頭にリージョンが1 つしかないため、すべての書き込み要求はリージョンが配置されている TiKV で発生します。新しく作成されたテーブルに大量の書き込みがあると、ホットスポットが発生します。

上記のシナリオのホットスポットの問題を解決するために、TiDB は pre-split 機能を導入します。これは、指定されたパラメーターに従って特定のテーブルの複数のリージョンを事前に分割し、それらを各 TiKV ノードに分散させることができます。

## あらすじ {#synopsis}

**SplitRegionStmt:**

![SplitRegionStmt](/media/sqlgram/SplitRegionStmt.png)

**分割構文オプション:**

![SplitSyntaxOption](/media/sqlgram/SplitSyntaxOption.png)

**テーブル名:**

![TableName](/media/sqlgram/TableName.png)

**PartitionNameListOpt:**

![PartitionNameListOpt](/media/sqlgram/PartitionNameListOpt.png)

**分割オプション:**

![SplitOption](/media/sqlgram/SplitOption.png)

**行値:**

![RowValue](/media/sqlgram/RowValue.png)

**Int64Num:**

![Int64Num](/media/sqlgram/Int64Num.png)

## スプリットリージョンの使い方 {#usage-of-split-region}

分割リージョンの構文には次の 2 種類があります。

-   偶数分割の構文:

    {{< copyable "" >}}

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num` 、上限、下限、およびリージョン量を定義します。次に、現在の領域は、上限と下限の間の領域数 ( `region_num`で指定) に均等にスピルされます。

-   不等分割の構文:

    {{< copyable "" >}}

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…`現在のリージョンが分割されることに基づいて、一連のポイントを手動で指定します。これは、データが不均一に分散されているシナリオに適しています。

次の例は、 `SPLIT`ステートメントの結果を示しています。

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

-   `TOTAL_SPLIT_REGION` : 新しく分割されたリージョンの数。
-   `SCATTER_FINISH_RATIO` : 新しく分割されたリージョンの分散の完了率。 `1.0` 、すべてのリージョンが分散していることを意味します。 `0.5` 、領域の半分のみが分散され、残りは分散されていることを意味します。

> **ノート：**
>
> 次の 2 つのセッション変数は、 `SPLIT`ステートメントの動作に影響を与える可能性があります。
>
> -   `tidb_wait_split_region_finish` : リージョンの分散に時間がかかる場合があります。この期間は、PD のスケジューリングと TiKV の負荷によって異なります。この変数は、 `SPLIT REGION`ステートメントの実行時に、すべてのリージョンが分散されるまで結果をクライアントに返すかどうかを制御するために使用されます。その値が`1`に設定されている場合 (デフォルト)、TiDB は分散が完了した後にのみ結果を返します。その値が`0`に設定されている場合、TiDB は分散ステータスに関係なく結果を返します。
> -   `tidb_wait_split_region_timeout` : この変数は、 `SPLIT REGION`ステートメントの実行タイムアウトを秒単位で設定します。デフォルト値は 300 秒です。 `split`操作が期間内に完了しない場合、TiDB はタイムアウト エラーを返します。

### 分割表リージョン {#split-table-region}

各テーブルの行データのキーは`table_id`と`row_id`でエンコードされます。形式は次のとおりです。

```go
t[table_id]_r[row_id]
```

たとえば、 `table_id`が 22 で`row_id`が 11 の場合:

```go
t22_r11
```

同じテーブルの行データには同じ`table_id`ありますが、各行にはリージョン分割に使用できる一意の`row_id`があります。

#### 偶数分割 {#even-split}

`row_id`は整数であるため、分割するキーの値は、指定された`lower_value` 、 `upper_value` 、および`region_num`に従って計算できます。 TiDB は最初にステップ値 ( `step = (upper_value - lower_value)/region_num` ) を計算します。次に、 `lower_value`と`upper_value`の間の「ステップ」ごとに均等に分割され、 `region_num`で指定された数のリージョンが生成されます。

たとえば、テーブル t のキー範囲`minInt64` ~ `maxInt64`から 16 の均等に分割されたリージョンが必要な場合は、次のステートメントを使用できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t を minInt64 と maxInt64 の間の 16 のリージョンに分割します。指定された主キー範囲が指定された範囲よりも小さい場合 (たとえば、0 ~ 1000000000)、0 と 1000000000 をそれぞれ minInt64 と maxInt64 の代わりに使用して、リージョンを分割できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不等分割 {#uneven-split}

既知のデータが不均一に分布しており、リージョンをそれぞれキー範囲 -inf ~ 10000、10000 ~ 90000、および 90000 ~ +inf で分割する場合は、以下に示すように固定ポイントを設定することでこれを実現できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t BY (10000), (90000);
```

### スプリット インデックスリージョン {#split-index-region}

テーブル内のインデックス データのキーは、 `table_id` 、 `index_id` 、およびインデックス列の値によってエンコードされます。形式は次のとおりです。

```go
t[table_id]_i[index_id][index_value]
```

たとえば、 `table_id`が 22、3 `index_id` `index_value`が abc の場合:

```go
t22_i5abc
```

1 つのテーブル内の同じインデックス データの`table_id`と`index_id`は同じです。インデックスのリージョンを分割するには、 `index_value`に基づいてリージョンを分割する必要があります。

#### こぼれた {#even-spilt}

インデックスを均等に分割する方法は、データを均等に分割するのと同じように機能します。ただし、 `index_value`整数ではない可能性があるため、step の値の計算はより複雑になります。

`upper`と`lower`の値は、最初にバイト配列にエンコードされます。 `lower`および`upper`バイト配列の最も長い共通プレフィックスを削除した後、 `lower`および`upper`の最初の 8 バイトが uint64 形式に変換されます。次に、 `step = (upper - lower)/num`が計算されます。その後、計算されたステップはバイト配列にエンコードされ、インデックス分割のために`lower`および`upper`バイト配列の最長の共通プレフィックスに追加されます。次に例を示します。

`idx`インデックスの列が整数型の場合、次の SQL ステートメントを使用してインデックス データを分割できます。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t のインデックス idx のリージョン を`minInt64`から`maxInt64`までの 16 の Region に分割します。

インデックス idx1 の列が varchar 型で、インデックス データをプレフィックス文字で分割する場合。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

このステートメントは、インデックス idx1 を a~z の 25 のリージョンに分割します。リージョン1 の範囲は`[minIndexValue, b)`です。リージョン2 の範囲は`[b, c)`です。 …リージョン25 の範囲は`[y, minIndexValue]`です。 `idx`インデックスの場合、プレフィックス`a`のデータはリージョン1 に書き込まれ、プレフィックス`b`のデータはリージョン2 に書き込まれます。

上記の分割方法では、上限が`z`ではなく`{` (ASCII の`z`の隣の文字) であるため、接頭辞`y`と`z`持つ両方のデータがリージョン25 に書き込まれます。したがって、より正確な分割方法は次のとおりです。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

このステートメントは、テーブル`t`のインデックス idx1 を a~ `{`から 26 のリージョンに分割します。リージョン1 の範囲は`[minIndexValue, b)`です。リージョン2 の範囲は`[b, c)`です。 …リージョン25 の範囲は`[y, z)`で、リージョン26 の範囲は`[z, maxIndexValue)`です。

インデックス`idx2`の列がタイムスタンプ/日時のような時間型で、インデックスのリージョンを年ごとに分割する場合:

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

このステートメントは、テーブル`t`のインデックス`idx2`のリージョン を`2010-01-01 00:00:00`から`2020-01-01 00:00:00`までの 10 の Region に分割します。リージョン1 の範囲は`[minIndexValue, 2011-01-01 00:00:00)`です。リージョン2 の範囲は`[2011-01-01 00:00:00, 2012-01-01 00:00:00)`です。

インデックスリージョン を日ごとに分割する場合は、次の例を参照してください。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

このステートメントは、表`t`のインデックス`idex2`の 2020 年 6 月のデータを 30 の地域に分割します。各リージョンは1 日を表します。

他のタイプのインデックス列のリージョン分割方法も同様です。

結合インデックスのデータリージョン分割の場合、唯一の違いは、複数の列の値を指定できることです。

たとえば、インデックス`idx3 (a, b)`は 2 つの列が含まれ、列`a`はタイムスタンプ タイプ、列`b`は int です。列`a`に従って時間範囲を分割したいだけの場合は、単一列の時間インデックスを分割するための SQL ステートメントを使用できます。この場合、 `lower_value`と`upper_velue`に`b`列目の値を指定しないでください。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

同じ時間の範囲内で、列 b の列に従って、もう 1 つの分割を行う場合。分割時に列 b の値を指定するだけです。

{{< copyable "" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

このステートメントは、列 a と同じ時間プレフィックスを使用して、列 b の値に従って a~z の範囲の 10 の地域を分割します。 a列に指定した値が異なる場合、この場合、b列の値が使用されないことがあります。

テーブルの主キーが[非クラスター化インデックス](/clustered-indexes.md)の場合、リージョンを分割するときにバッククォート`` ` ``使用して`PRIMARY`キーワードをエスケープする必要があります。例えば：

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 不等分割 {#uneven-split}

インデックス データは、指定したインデックス値で分割することもできます。

たとえば、 `idx4 (a,b)`があり、列`a`が varchar 型で、列`b`がタイムスタンプ型です。

{{< copyable "" >}}

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

このステートメントは、4 つのリージョンを分割するために 3 つの値を指定します。各リージョンの範囲は次のとおりです。

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

### 分割されたテーブルの分割リージョン {#split-regions-for-partitioned-tables}

分割されたテーブルのリージョンの分割は、通常のテーブルのリージョンの分割と同じです。唯一の違いは、すべてのパーティションに対して同じ分割操作が実行されることです。

-   偶数分割の構文:

    {{< copyable "" >}}

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

-   不等分割の構文:

    {{< copyable "" >}}

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### 分割されたテーブルの分割領域の例 {#examples-of-split-regions-for-partitioned-tables}

1.  パーティションテーブルを作成する`t` . 2 つのパーティションに分割されたハッシュ テーブルを作成するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    create table t (a int,b int,index idx(a)) partition by hash(a) partitions 2;
    ```

    テーブル`t`を作成した後、パーティションごとにリージョンが分割されます。 `SHOW TABLE REGIONS`構文を使用して、このテーブルのリージョンを表示します。

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

2.  `SPLIT`構文を使用して、パーティションごとにリージョンを分割します。各パーティションの`[0,10000]`範囲のデータを 4 つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上記のステートメントで、 `0`と`10000`はそれぞれ、散布するホットスポット データに対応する上限と下限の`row_id`つの境界を表します。

    > **ノート：**
    >
    > この例は、ホットスポット データが均等に分散されているシナリオにのみ適用されます。指定したデータ範囲内でホットスポット データが不均等に分散している場合は、 [分割されたテーブルの分割リージョン](#split-regions-for-partitioned-tables)の不均等な分割の構文を参照してください。

3.  `SHOW TABLE REGIONS`構文を使用して、このテーブルの地域を再度表示します。このテーブルには 10 のリージョンがあり、各パーティションには 5 つのリージョンがあり、そのうちの 4 つは行データで、1 つはインデックス データです。

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

4.  各パーティションのインデックスに対してリージョンを分割することもできます。たとえば、 `idx`インデックスの`[1000,10000]`範囲を 2 つのリージョンに分割できます。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t index idx between (1000) and (10000) regions 2;
    ```

#### 単一パーティションの分割リージョンの例 {#examples-of-split-region-for-a-single-partition}

分割するパーティションを指定できます。

1.  パーティションテーブルを作成します。 3 つのパーティションに分割された範囲パーティションテーブルを作成するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    create table t ( a int, b int, index idx(b)) partition by range( a ) (
        partition p1 values less than (10000),
        partition p2 values less than (20000),
        partition p3 values less than (MAXVALUE) );
    ```

2.  `p1`のパーティションの`[0,10000]`範囲のデータを 2 つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t partition (p1) between (0) and (10000) regions 2;
    ```

3.  `p2`のパーティションの`[10000,20000]`範囲のデータを 2 つのリージョンに分割するとします。ステートメントの例は次のとおりです。

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

5.  `p1`および`p2`パーティションの`idx`のインデックスの`[0,20000]`の範囲を 2 つのリージョンに分割するとします。ステートメントの例は次のとおりです。

    {{< copyable "" >}}

    ```sql
    split partition table t partition (p1,p2) index idx between (0) and (20000) regions 2;
    ```

## pre_split_regions {#pre-split-regions}

テーブルの作成時にリージョンを均等に分割するには、 `SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`を一緒に使用することをお勧めします。テーブルが正常に作成されると、 `PRE_SPLIT_REGIONS`テーブルを`2^(PRE_SPLIT_REGIONS)`で指定された数のリージョンに分割します。

> **ノート：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`の値以下でなければなりません。

`tidb_scatter_region`グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響します。この変数は、テーブルの作成後に結果を返す前に、領域が事前に分割および分散されるのを待つかどうかを制御します。テーブルの作成後に書き込みが集中する場合は、この変数の値を`1`に設定する必要があります。そうすると、すべてのリージョンが分割され分散されるまで、TiDB はクライアントに結果を返しません。そうしないと、分散が完了する前に TiDB がデータを書き込むため、書き込みパフォーマンスに大きな影響を与えます。

### pre_split_regions の例 {#examples-of-pre-split-regions}

{{< copyable "" >}}

```sql
create table t (a int, b int,index idx1(a)) shard_row_id_bits = 4 pre_split_regions=2;
```

テーブルを構築した後、このステートメントはテーブル t の`4 + 1`のリージョンを分割します。 `4 (2^2)`リージョンはテーブルの行データを保存するために使用され、1 つのリージョンは`idx1`のインデックス データを保存するために使用されます。

4 つのテーブル リージョンの範囲は次のとおりです。

```
region1:   [ -inf      ,  1<<61 )
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

<CustomContent platform="tidb">

> **ノート：**
>
> Split リージョンステートメントによって分割されたリージョンは、PD の[リージョンのマージ](/best-practices/pd-scheduling-best-practices.md#region-merge)スケジューラによって制御されます。 PD が新しく分割されたリージョンをすぐに再マージしないようにするには、リージョンマージ機能に関連する[動的に変更する](/pd-control.md)構成項目が必要です。

</CustomContent>

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## こちらもご覧ください {#see-also}

-   [テーブル領域を表示](/sql-statements/sql-statement-show-table-regions.md)
-   セッション変数: [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) 、 [`tidb_wait_split_region_finish`](/system-variables.md#tidb_wait_split_region_finish) 、および[`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout) 。

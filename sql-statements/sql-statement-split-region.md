---
title: Split Region
summary: TiDBデータベースにおけるスプリットリージョンの使用概要。
---

# 分割リージョン {#split-region}

TiDBで新しいテーブルを作成するたびに、デフォルトで1つの[リージョン](/tidb-storage.md#region)が分割され、そのテーブルのデータが格納されます。このデフォルトの動作は、TiDB構成ファイルの`split-table`によって制御されます。このリージョン内のデータがデフォルトのリージョンサイズ制限を超えると、リージョンは2つに分割され始めます。

上記の場合、初期状態ではリージョンが1つしかないため、すべての書き込み要求はリージョンが配置されているTiKV上で発生します。新しく作成されたテーブルへの書き込みが大量に発生すると、ホットスポットが発生します。

上記シナリオにおけるホットスポット問題を解決するために、TiDBは事前分割機能を導入しました。この機能は、指定されたパラメータに従って特定のテーブルに対して複数のリージョンを事前に分割し、それらを各TiKVノードに分散させることができます。

> **注記：**
>
> この機能は、 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter)および[TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)インスタンスではご利用いただけません。

## あらすじ {#synopsis}

```ebnf+diagram
SplitRegionStmt ::=
    "SPLIT" SplitSyntaxOption "TABLE" TableName PartitionNameList? ("INDEX" IndexName)? SplitOption

SplitSyntaxOption ::=
    ("REGION" "FOR")? "PARTITION"?

TableName ::=
    (SchemaName ".")? Identifier

PartitionNameList ::=
    "PARTITION" "(" PartitionName ("," PartitionName)* ")"

SplitOption ::=
    ("BETWEEN" RowValue "AND" RowValue "REGIONS" NUM
|   "BY" RowValue ("," RowValue)* )

RowValue ::=
    "(" ValuesOpt ")"
```

## 分割リージョンの使用 {#usage-of-split-region}

分割リージョン構文には2種類あります。

-   均等分割の構文：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num`上限、下限、およびリージョン数を定義します。すると、現在の領域は、上限と下限の間で、指定された数の領域（ `region_num`で指定）に均等に分割されます。

-   不均等分割の構文:

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…` 、現在のリージョンを分割するための基準となる一連のポイントを手動で指定します。これは、データが不均一に分布しているシナリオに適しています。

次の例は`SPLIT`ステートメントの実行結果を示しています。

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

-   `TOTAL_SPLIT_REGION` : 新たに分割された地域の数。
-   `SCATTER_FINISH_RATIO` : 新しく分割された領域の分散完了率。 `1.0`すべての領域が分散されたことを意味します。 `0.5`は、領域の半分のみが分散され、残りは分散中であることを意味します。

> **注記：**
>
> 以下の2つのセッション変数は`SPLIT`ステートメントの動作に影響を与える可能性があります。
>
> -   `tidb_wait_split_region_finish` : リージョンの分散には時間がかかる場合があります。この期間は、PD スケジューリングと TiKV の負荷によって異なります。この変数は、 `SPLIT REGION`ステートメントの実行時に、すべてのリージョンが分散されるまで結果をクライアントに返すかどうかを制御するために使用されます。値が`1` (デフォルト) に設定されている場合、TiDB は分散が完了した後にのみ結果を返します。値が`0`に設定されている場合、TiDB は分散状態に関係なく結果を返します。
> -   `tidb_wait_split_region_timeout` : この変数は、 `SPLIT REGION`ステートメントの実行タイムアウトを秒単位で設定します。デフォルト値は 300 秒です。 `split`操作が指定された時間内に完了しない場合、TiDB はタイムアウト エラーを返します。

### 分割テーブルリージョン {#split-table-region}

各テーブルの行データのキーは、 `table_id`と`row_id`でエンコードされます。フォーマットは以下のとおりです。

```go
t[table_id]_r[row_id]
```

例えば、 `table_id`が22で、 `row_id`が11の場合：

```go
t22_r11
```

同じテーブル内の行データには同じ`table_id`がありますが、各行にはリージョン分割に使用できる固有の`row_id`があります。

#### 均等に {#even-split}

`row_id`は整数であるため、分割するキーの値は、指定された`lower_value` 、 `upper_value` 、および`region_num`に従って計算できます。TiDB は最初にステップ値 ( `step = (upper_value - lower_value)/region_num` ) を計算します。次に、 `lower_value`と`upper_value`の間で各「ステップ」ごとに均等に分割して`region_num`で指定された数のリージョンを生成します。

例えば、テーブル t のキー範囲`minInt64` ~ `maxInt64`から均等に分割された 16 個の領域を作成したい場合は、次のステートメントを使用できます。

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t を minInt64 と maxInt64 の間の 16 個の領域に分割します。指定された主キーの範囲が、例えば 0~1000000000 のように、指定された範囲よりも小さい場合は、minInt64 と maxInt64 の代わりにそれぞれ 0 と 1000000000 を使用して領域を分割できます。

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不均等分割 {#uneven-split}

既知のデータが不均等に分布している場合、リージョンをそれぞれキー範囲 -inf ~ 10000、10000 ~ 90000、90000 ~ +inf に分割したい場合は、以下に示すように固定点を設定することで実現できます。

```sql
SPLIT TABLE t BY (10000), (90000);
```

### スプリットインデックスリージョン {#split-index-region}

テーブル内のインデックスデータのキーは`table_id` 、 `index_id` 、およびインデックス列の値によってエンコードされます。形式は次のとおりです。

```go
t[table_id]_i[index_id][index_value]
```

例えば、 `table_id`が 22、 `index_id`が 5、 `index_value`が abc の場合：

```go
t22_i5abc
```

1 つのテーブル内の同じインデックス データの`table_id`と`index_id`は同じです。インデックス領域を分割するには、 `index_value`に基づいて領域を分割する必要があります。

#### 均等に分割 {#even-spilt}

インデックスを均等に分割する方法は、データを均等に分割する方法と同じです。ただし、 `index_value`整数にならない可能性があるため、ステップの値を計算するのはより複雑になります。

`upper`と`lower`の値は、まずバイト配列にエンコードされます。 `lower`と`upper`のバイト配列の最長共通プレフィックスを削除した後、 `lower`と`upper`の最初の 8 バイトが uint64 形式に変換されます。次に、 `step = (upper - lower)/num`が計算されます。その後、計算されたステップはバイト配列にエンコードされ、インデックス分割のために`lower`と`upper`バイト配列の最長共通プレフィックスに追加されます。以下に例を示します。

`idx`インデックスの列が整数型の場合、次の SQL ステートメントを使用してインデックスデータを分割できます。

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t のインデックス idx のリージョンを`minInt64`から`maxInt64`までの 16 の領域に分割します。

インデックス idx1 の列が varchar 型で、インデックスデータを接頭辞文字で分割したい場合。

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

このステートメントは、インデックス idx1 を a~z の 25 個の領域に分割します。リージョン1 の範囲は`[minIndexValue, b)`です。リージョン2 の範囲は`[b, c)`です。…リージョン25 の範囲は`[y, minIndexValue]`です。 `idx`インデックスの場合、 `a`接頭辞を持つデータはリージョン1 に書き込まれ、 `b`接頭辞を持つデータはリージョン2 に書き込まれます。

上記の分割方法では、 `y`と`z`の接頭辞が付いたデータの両方がリージョン25 に書き込まれます。これは、上限が`z`ではなく`{` (ASCII で`z`の次の文字) であるためです。したがって、より正確な分割方法は次のようになります。

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

このステートメントは、テーブル`t`のインデックス idx1 を`{`から 26 の領域に分割します。リージョン1 の範囲は`[minIndexValue, b)`です。リージョン2 の範囲は`[b, c)`です。…リージョン25 の範囲は`[y, z)`であり、リージョン26 の範囲は`[z, maxIndexValue)`です。

インデックス`idx2`の列がタイムスタンプ/日時などの時間型であり、インデックスリージョン を年ごとに分割したい場合：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

このステートメントは、テーブル`idx2`内のインデックス`t`のリージョンを`2010-01-01 00:00:00`から`2020-01-01 00:00:00`までの 10 個の領域に分割します。リージョン1 の範囲は`[minIndexValue, 2011-01-01 00:00:00)`です。リージョン2 の範囲は`[2011-01-01 00:00:00, 2012-01-01 00:00:00)`です。

インデックスリージョンを日ごとに分割したい場合は、次の例を参照してください。

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

このステートメントは、テーブル`idex2`のインデックス`t` } の 2020 年 6 月のデータを 30 の領域に分割します。各リージョンは1 日を表します。

他のタイプのインデックス列に対するリージョン分割方法も同様です。

結合インデックスのデータリージョン分割の場合、唯一の違いは、複数の列の値を指定できる点です。

例えば、インデックス`idx3 (a, b)`には 2 つの列が含まれており、列`a`はタイムスタンプ型、列`b`は int 型です。列`a`に基づいて時間範囲を分割するだけであれば、単一列の時間インデックスを分割する SQL ステートメントを使用できます。この場合、列`b`と`lower_value`では列`upper_velue`でください。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

同じ時間範囲内で、列bに基づいてさらに分割を行いたい場合は、分割時に列bの値を指定するだけです。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

このステートメントは、列aと同じ時間接頭辞を持つ列bの値に基づいて、a～zの範囲にある10個の領域を分割します。列aに指定された値が異なる場合、列bの値は使用されない可能性があります。

テーブルの主キーが[非クラスター化インデックス](/clustered-indexes.md)の場合、リージョンを分割するときにバックティック`` ` ``を使用して`PRIMARY`キーワードをエスケープする必要があります。例えば：

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 不均等分割 {#uneven-split}

インデックスデータは、指定されたインデックス値によって分割することもできます。

例えば、 `idx4 (a,b)`があり、列`a`は varchar 型、列`b`は timestamp 型です。

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

このステートメントは、4つの領域を分割するための3つの値を指定します。各リージョンの範囲は次のとおりです。

    region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
    region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
    region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
    region4  [("c", "")                    , maxIndexValue               )

### パーティション化されたテーブルの領域を分割する {#split-regions-for-partitioned-tables}

パーティション化されたテーブルの領域分割は、通常のテーブルの領域分割と同じです。唯一の違いは、すべてのパーティションに対して同じ分割操作が実行される点です。

-   均等分割の構文：

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

-   不均等分割の構文:

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### パーティション化されたテーブルの分割領域の例 {#examples-of-split-regions-for-partitioned-tables}

1.  パーティションテーブル`t`を作成します。ハッシュテーブルを 2 つのパーティションに分割して作成したいとします。例のステートメントは次のとおりです。

    ```sql
    CREATE TABLE t (a INT, b INT, INDEX idx(a)) PARTITION BY HASH(a) PARTITIONS 2;
    ```

    テーブル`t`を作成すると、パーティションごとにリージョンが分割されます。このテーブルのリージョンを表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)構文を使用します。

    ```sql
    SHOW TABLE t REGIONS;
    ```

    ```sql
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | REGION_ID | START_KEY | END_KEY | LEADER_ID | LEADER_STORE_ID | PEERS            | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    | 1978      | t_1400_   | t_1401_ | 1979      | 4               | 1979, 1980, 1981 | 0          | 0             | 0          | 1                    | 0                |
    | 6         | t_1401_   |         | 17        | 4               | 17, 18, 21       | 0          | 223           | 0          | 1                    | 0                |
    +-----------+-----------+---------+-----------+-----------------+------------------+------------+---------------+------------+----------------------+------------------+
    ```

2.  `SPLIT`構文を使用して、パーティションごとにリージョンを分割します。たとえば、各パーティションの`[0,10000]`範囲のデータを4つの領域に分割したいとします。例のステートメントは次のとおりです。

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上記の記述において、 `0`と`10000`はそれぞれ、散布したいホットスポットデータに対応する上側境界と下側境界の`row_id`を表します。

    > **注記：**
    >
    > この例は、ホットスポット データが均等に分散されているシナリオにのみ適用されます。ホットスポット データが指定されたデータ範囲内で不均等に分散している場合は、[パーティション化されたテーブルの領域を分割する](#split-regions-for-partitioned-tables)不均等分割の構文を参照してください。

3.  `SHOW TABLE REGIONS`構文を使用して、このテーブルのリージョンを再度表示します。このテーブルには10個のリージョンがあり、各パーティションには5つのリージョンがあり、そのうち4つが行データ、1つがインデックスデータであることがわかります。

    ```sql
    SHOW TABLE t REGIONS;
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

4.  各パーティションのインデックスごとにリージョンを分割することもできます。たとえば、 `[1000,10000]`インデックスの`idx`範囲を 2 つのリージョンに分割できます。例のステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t INDEX idx BETWEEN (1000) AND (10000) REGIONS 2;
    ```

#### 単一パーティションの分割リージョンの例 {#examples-of-split-region-for-a-single-partition}

分割するパーティションを指定できます。

1.  パーティションテーブルを作成します。たとえば、3つのパーティションに分割された範囲パーティションテーブルを作成するとします。例となるステートメントは次のとおりです。

    ```sql
    CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
        PARTITION p1 VALUES LESS THAN (10000),
        PARTITION p2 VALUES LESS THAN (20000),
        PARTITION p3 VALUES LESS THAN (MAXVALUE) );
    ```

2.  `[0,10000]`パーティションの`p1`範囲のデータを2つの領域に分割したいとします。例となるステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1) BETWEEN (0) AND (10000) REGIONS 2;
    ```

3.  `[10000,20000]`パーティションの`p2`範囲のデータを2つの領域に分割したいとします。例となるステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p2) BETWEEN (10000) AND (20000) REGIONS 2;
    ```

4.  `SHOW TABLE REGIONS`構文を使用すると、このテーブルのリージョンを表示できます。

    ```sql
    SHOW TABLE t REGIONS;
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

5.  `[0,20000]`および`idx`インデックスの`p1` `p2`範囲を 2 つの領域に分割したいとします。例となるステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1,p2) INDEX idx BETWEEN (0) AND (20000) REGIONS 2;
    ```

## 分割前領域 {#pre-split-regions}

`AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性を使用してテーブルを作成する場合、テーブル作成直後にテーブルをリージョンに均等に事前分割したい場合は`PRE_SPLIT_REGIONS`オプションを指定することもできます。テーブルの事前分割リージョンの数は`2^(PRE_SPLIT_REGIONS)`です。

> **注記：**
>
> `PRE_SPLIT_REGIONS`の値は、 `SHARD_ROW_ID_BITS`または`AUTO_RANDOM`の値以下でなければなりません。

[`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響します。この変数は、テーブル作成後に結果を返す前に、リージョンが事前に分割され分散されるまで待機するかどうかを制御します。テーブル作成後に書き込みが集中する場合は、この変数の値を`global`に設定する必要があります。そうすると、TiDB はクラスタ全体のデータ分布に従って、新しく作成されたテーブルのリージョンを分散します。そうでない場合、TiDB は分散が完了する前にデータを書き込み、書き込みパフォーマンスに大きな影響を与えます。

### pre_split_regionsの例 {#examples-of-pre-split-regions}

```sql
CREATE TABLE t (a INT, b INT, INDEX idx1(a)) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=2;
```

テーブルを作成した後、このステートメントはテーブル t の`4 + 1`領域を分割します。 `4 (2^2)`領域はテーブルの行データを保存するのに使用され、1 つのリージョンは`idx1`のインデックス データを保存するために使用されます。

4つの表領域の範囲は以下のとおりです。

    region1:   [ -inf      ,  1<<61 )
    region2:   [ 1<<61     ,  2<<61 )
    region3:   [ 2<<61     ,  3<<61 )
    region4:   [ 3<<61     ,  +inf  )

<CustomContent platform="tidb">

> **注記：**
>
> Split リージョンステートメントによって分割されたリージョンは、PD の[リージョンの統合](/best-practices/pd-scheduling-best-practices.md#region-merge)スケジューラーによって制御されます。 PD が新しく分割されたリージョンをすぐに再マージしないようにするには、[テーブル属性](/table-attributes.md)プロパティ[動的に変更する](/pd-control.md)に変更するリージョンマージ機能に関連する構成アイテムを使用する必要があります。

</CustomContent>

## MySQLとの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文に対するTiDBの拡張機能です。

## 関連項目 {#see-also}

-   [テーブル領域を表示する](/sql-statements/sql-statement-show-table-regions.md)
-   セッション変数: [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) 、 [`tidb_wait_split_region_finish`](/system-variables.md#tidb_wait_split_region_finish) 、 [`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout) 。

---
title: Split Region
summary: TiDB データベースの Split リージョンの使用法の概要。
---

# 分割リージョン {#split-region}

TiDBに新しいテーブルが作成されると、デフォルトで[リージョン](/tidb-storage.md#region)つのセグメントが分割され、そのテーブルのデータが保存されます。このデフォルトの動作は、TiDB設定ファイルの`split-table`によって制御されます。このリージョン内のデータがデフォルトのリージョンサイズ制限を超えると、リージョンは2つに分割され始めます。

上記のケースでは、開始時にリージョンが1つしかないため、すべての書き込みリクエストは、そのリージョンが配置されているTiKV上で発生します。新しく作成されたテーブルへの書き込みが大量に発生すると、ホットスポットが発生します。

上記のシナリオのホットスポット問題を解決するために、TiDB は事前分割機能を導入しました。この機能は、指定されたパラメータに従って特定のテーブルの複数のリージョンを事前に分割し、各 TiKV ノードに分散させることができます。

> **注記：**
>
> この機能は、クラスター[TiDB Cloudスターター](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)および[TiDB Cloudエッセンシャル](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)では利用できません。

## 概要 {#synopsis}

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

分割リージョン構文には 2 つの種類があります。

-   均等分割の構文:

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num`上限、下限、およびリージョンの量を定義します。これにより、現在の領域は、上限と下限の間の領域数（ `region_num`で指定）に均等に分割されます。

-   不均等分割の構文:

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…` 、現在のリージョンを分割するポイントの系列を手動で指定します。データが不均一に分散しているシナリオに適しています。

次の例は、 `SPLIT`のステートメントの結果を示しています。

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

-   `TOTAL_SPLIT_REGION` : 新しく分割されたリージョンの数。
-   `SCATTER_FINISH_RATIO` : 新しく分割された領域の分散の完了率。2 `1.0`すべての領域が分散されていることを意味します。4 `0.5`領域の半分だけが分散され、残りは分散中であることを意味します。

> **注記：**
>
> 次の 2 つのセッション変数は、 `SPLIT`ステートメントの動作に影響を与える可能性があります。
>
> -   `tidb_wait_split_region_finish` : リージョンの分散には時間がかかる場合があります。この時間はPDスケジューリングとTiKVの負荷に依存します。この変数は、 `SPLIT REGION`ステートメントを実行する際に、すべてのリージョンが分散されるまで結果をクライアントに返すかどうかを制御するために使用されます。値が`1` （デフォルト）に設定されている場合、TiDBは分散が完了した後にのみ結果を返します。値が`0`に設定されている場合、TiDBは分散状態に関係なく結果を返します。
> -   `tidb_wait_split_region_timeout` : この変数は、 `SPLIT REGION`のステートメントの実行タイムアウトを秒単位で設定します。デフォルト値は300秒です。4 `split`操作が指定時間内に完了しない場合、TiDBはタイムアウトエラーを返します。

### テーブルリージョンを分割 {#split-table-region}

各テーブルの行データのキーは`table_id`と`row_id`でエンコードされます。形式は以下のとおりです。

```go
t[table_id]_r[row_id]
```

たとえば、 `table_id`が 22 で`row_id`が 11 の場合:

```go
t22_r11
```

同じテーブル内の行データには同じ`table_id`含まれますが、各行にはリージョン分割に使用できる固有の`row_id`含まれます。

#### 均等分割 {#even-split}

`row_id`整数なので、分割するキーの値は指定された`lower_value` 、 `upper_value` 、 `region_num`に従って計算できます。TiDBはまずステップ値（ `step = (upper_value - lower_value)/region_num` ）を計算します。次に、 `lower_value`から`upper_value`までの各「ステップ」ごとに均等に分割し、 `region_num`で指定された数のリージョンを生成します。

たとえば、テーブル t のキー範囲`minInt64` ～ `maxInt64`から 16 個の均等に分割された領域が必要な場合は、次のステートメントを使用できます。

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t を minInt64 から maxInt64 までの 16 個の Region に分割します。指定された主キーの範囲が、例えば 0~1000000000 のように、指定された範囲よりも小さい場合は、minInt64 と maxInt64 の代わりにそれぞれ 0 と 1000000000 を指定して Region を分割できます。

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不平等な分割 {#uneven-split}

既知のデータが不均一に分布していて、リージョンをキー範囲 -inf ~ 10000、10000 ~ 90000、90000 ~ +inf にそれぞれ分割したい場合は、以下に示すように固定ポイントを設定することでこれを実現できます。

```sql
SPLIT TABLE t BY (10000), (90000);
```

### 分割インデックスリージョン {#split-index-region}

テーブル内のインデックスデータのキーは、 `table_id` `index_id`およびインデックス列の値でエンコードされます。形式は次のとおりです。

```go
t[table_id]_i[index_id][index_value]
```

たとえば、 `table_id`が`index_id`が`index_value`が abc の場合:

```go
t22_i5abc
```

同じテーブル内の同じインデックスデータの`table_id`と`index_id`同じです。インデックスの Region を分割するには、 `index_value`に基づいて Region を分割する必要があります。

#### こぼしても {#even-spilt}

インデックスを均等に分割する方法は、データを均等に分割する方法と同じです。ただし、 `index_value`整数ではない可能性があるため、ステップの値の計算はより複雑になります。

まず、 `upper`と`lower`の値がバイト配列にエンコードされます。5と`upper`バイト配列の最長共通プレフィックス`lower`削除した後、 `lower`と`upper`の最初の8バイトがuint64形式に変換されます。次に`step = (upper - lower)/num`計算されます。その後、計算されたステップがバイト配列にエンコードされ、 `lower`と`upper`バイト配列の最長共通プレフィックスに追加されてインデックス分割が行われます。以下に例を示します。

`idx`インデックスの列が整数型の場合、次の SQL 文を使用してインデックス データを分割できます。

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

このステートメントは、テーブル t のインデックス idx のリージョンを`minInt64`から`maxInt64`までの 16 の Region に分割します。

インデックス idx1 の列が varchar 型であり、インデックス データをプレフィックス文字で分割する場合。

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

この文は、インデックス idx1 を a～z の 25 個のリージョンに分割します。リージョン1 の範囲は`[minIndexValue, b)` 、リージョン2 の範囲は`[b, c)` 、…リージョン25 の範囲は`[y, minIndexValue]`です。インデックス`idx`場合、プレフィックスが`a`データはリージョン1 に書き込まれ、プレフィックスが`b`のデータはリージョン2 に書き込まれます。

上記の分割方法では、 `y`と`z`プレフィックスを持つデータは両方ともリージョン25に書き込まれます。これは、上限が`z`ではなく`{` （ASCIIコードで`z`次の文字）であるためです。したがって、より正確な分割方法は次のとおりです。

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

この文は、テーブル`t`のインデックス idx1 を a~ `{`の26の領域に分割します。リージョン1 の範囲は`[minIndexValue, b)` 、リージョン2 の範囲は`[b, c)` 、…リージョン25 の範囲は`[y, z)` 、リージョン26 の範囲は`[z, maxIndexValue)`です。

インデックス`idx2`の列がタイムスタンプ/日付時刻のような時間型で、インデックスのリージョンを年ごとに分割する場合:

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

この文は、表`t`のインデックス`idx2`のリージョンを`2010-01-01 00:00:00`から`2020-01-01 00:00:00`までの10のRegionに分割します。Region 1のリージョンは`[minIndexValue, 2011-01-01 00:00:00)` 、 リージョン 2の範囲は`[2011-01-01 00:00:00, 2012-01-01 00:00:00)`です。

インデックスリージョンを日ごとに分割する場合は、次の例を参照してください。

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

このステートメントは、表`t`のインデックス`idex2`の 2020 年 6 月のデータを 30 の地域に分割します。各リージョンは1 日を表します。

他のタイプのインデックス列のリージョン分割方法も同様です。

結合インデックスのデータリージョン分割の場合、唯一の違いは複数の列の値を指定できることです。

例えば、インデックス`idx3 (a, b)`は2つの列があり、列`a`はタイムスタンプ型、列`b` int 型です。列`a`に基づいて時間範囲を分割したいだけの場合は、単一列の時間インデックスを分割するSQL文を使用できます。この場合、列`b`の値を`lower_value`と`upper_velue`に指定しないでください。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

同じ時間範囲内で、列bの値に基づいてさらに分割したい場合は、分割時に列bの値を指定するだけです。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

このステートメントは、列bの値に基づいて、列aと同じ時刻プレフィックスを持つa～zの範囲にある10個のリージョンを分割します。列aに指定された値が異なる場合、この場合、列bの値は使用されない可能性があります。

テーブルの主キーが[非クラスター化インデックス](/clustered-indexes.md)の場合、リージョンを分割する際に`PRIMARY`キーワードをエスケープするためにバッククォート`` ` ``使用する必要があります。例:

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 不平等な分割 {#uneven-split}

インデックス データは、指定されたインデックス値によって分割することもできます。

たとえば、列`a`が varchar 型で列`b`が timestamp 型の`idx4 (a,b)`あります。

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

このステートメントは、4つの領域を分割するための3つの値を指定します。各リージョンの範囲は次のとおりです。

    region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
    region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
    region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
    region4  [("c", "")                    , maxIndexValue               )

### パーティションテーブルの分割領域 {#split-regions-for-partitioned-tables}

パーティションテーブルのリージョン分割は、通常のテーブルのリージョン分割と同じです。唯一の違いは、すべてのパーティションに対して同じ分割操作が実行される点です。

-   均等分割の構文:

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

-   不均等分割の構文:

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### パーティションテーブルの分割領域の例 {#examples-of-split-regions-for-partitioned-tables}

1.  パーティションテーブル`t`を作成します。2つのパーティションに分割されたハッシュテーブルを作成するとします。例のステートメントは次のとおりです。

    ```sql
    CREATE TABLE t (a INT, b INT, INDEX idx(a)) PARTITION BY HASH(a) PARTITIONS 2;
    ```

    テーブル`t`作成した後、各パーティションにリージョンが分割されます。このテーブルのリージョンを表示するには、 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md)構文を使用します。

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

2.  各パーティションのリージョンを分割するには、 `SPLIT`構文を使用します。各パーティションの`[0,10000]`範囲のデータを 4 つのリージョンに分割するとします。例のステートメントは次のとおりです。

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上記のステートメントでは、 `0`と`10000`それぞれ、散布するホットスポット データに対応する上限と下限の`row_id`表します。

    > **注記：**
    >
    > この例は、ホットスポットデータが均等に分散されているシナリオにのみ適用されます。指定されたデータ範囲内でホットスポットデータが不均等に分散されている場合は、 [パーティションテーブルの分割領域](#split-regions-for-partitioned-tables)の不均等分割の構文を参照してください。

3.  `SHOW TABLE REGIONS`構文を使用して、このテーブルのRegionを再度表示します。テーブルには10個のRegionがあり、各パーティションには5個のRegionが含まれています。そのうち4個は行データ、1個はインデックスデータです。

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

4.  各パーティションのインデックスのRegionを分割することもできます。例えば、インデックス`idx`の`[1000,10000]`の範囲を2つのRegionに分割できます。例のステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t INDEX idx BETWEEN (1000) AND (10000) REGIONS 2;
    ```

#### 単一パーティションの分割リージョンの例 {#examples-of-split-region-for-a-single-partition}

分割するパーティションを指定できます。

1.  パーティションテーブルを作成します。3つのパーティションに分割された範囲パーティションテーブルを作成するとします。例のステートメントは次のとおりです。

    ```sql
    CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
        PARTITION p1 VALUES LESS THAN (10000),
        PARTITION p2 VALUES LESS THAN (20000),
        PARTITION p3 VALUES LESS THAN (MAXVALUE) );
    ```

2.  パーティション`p1`の`[0,10000]`の範囲のデータを2つのリージョンに分割するとします。例のステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1) BETWEEN (0) AND (10000) REGIONS 2;
    ```

3.  パーティション`p2`の`[10000,20000]`の範囲のデータを2つのリージョンに分割するとします。例のステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p2) BETWEEN (10000) AND (20000) REGIONS 2;
    ```

4.  `SHOW TABLE REGIONS`構文を使用して、このテーブルの地域を表示できます。

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

5.  パーティション`p1`と`p2`インデックス番号`idx`の`[0,20000]`の範囲を2つのリージョンに分割するとします。例のステートメントは次のとおりです。

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1,p2) INDEX idx BETWEEN (0) AND (20000) REGIONS 2;
    ```

## 事前分割領域 {#pre-split-regions}

`AUTO_RANDOM`または`SHARD_ROW_ID_BITS`属性でテーブルを作成する際に、テーブル作成直後に均等にリージョンに事前分割したい場合は、 `PRE_SPLIT_REGIONS`オプションも指定できます。テーブルごとに事前分割されるリージョンの数は`2^(PRE_SPLIT_REGIONS)`です。

> **注記：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`または`AUTO_RANDOM`の値以下でなければなりません。

グローバル変数[`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) `PRE_SPLIT_REGIONS`動作に影響します。この変数は、テーブル作成後に結果を返す前に、リージョンが事前に分割され、分散されるまで待機するかどうかを制御します。テーブル作成後に書き込みが集中する場合は、この変数の値を`global`に設定する必要があります。そうしないと、TiDBはクラスター全体のデータ分布に従って、新しく作成されたテーブルのリージョンを分散します。そうでない場合、TiDBは分散が完了する前にデータを書き込んでしまい、書き込みパフォーマンスに大きな影響を与えます。

### pre_split_regionsの例 {#examples-of-pre-split-regions}

```sql
CREATE TABLE t (a INT, b INT, INDEX idx1(a)) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=2;
```

テーブルを構築した後、このステートメントはテーブル t の`4 + 1`領域を分割します。3 `4 (2^2)`領域はテーブル行データを保存するために使用され、1 つのリージョンは`idx1`のインデックス データを保存するために使用されます。

4 つのテーブル領域の範囲は次のとおりです。

    region1:   [ -inf      ,  1<<61 )
    region2:   [ 1<<61     ,  2<<61 )
    region3:   [ 2<<61     ,  3<<61 )
    region4:   [ 3<<61     ,  +inf  )

<CustomContent platform="tidb">

> **注記：**
>
> Split リージョンステートメントによって分割されたリージョンは、PDの[リージョンの統合](/best-practices/pd-scheduling-best-practices.md#region-merge)のスケジューラによって制御されます。PDが分割されたリージョンをすぐに再マージすることを避けるには、リージョンマージ機能に関連する[テーブル属性](/table-attributes.md)または[動的に変更する](/pd-control.md)設定項目を使用する必要があります。

</CustomContent>

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。

## 参照 {#see-also}

-   [テーブル領域を表示](/sql-statements/sql-statement-show-table-regions.md)
-   セッション[`tidb_wait_split_region_timeout`](/system-variables.md#tidb_wait_split_region_timeout) : [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) [`tidb_wait_split_region_finish`](/system-variables.md#tidb_wait_split_region_finish)

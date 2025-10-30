---
title: Split Region
summary: TiDB 数据库 Split Region 的用法概述。
---

# Split Region

在 TiDB 中，每创建一张新表，默认会为该表的数据分配一个 [Region](/tidb-storage.md#region)。该默认行为由 TiDB 配置文件中的 `split-table` 控制。当该 Region 中的数据超过默认的 Region 大小限制时，该 Region 会被拆分成两个。

在上述情况下，由于一开始只有一个 Region，所有写入请求都会集中到该 Region 所在的 TiKV 上。如果对新建表有大量写入操作，就会产生热点问题。

为了解决上述场景下的热点问题，TiDB 引入了预拆分功能，可以根据指定参数为某张表预先拆分出多个 Region，并将它们分散到各个 TiKV 节点上。

> **Note:**
>
> 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

## 语法说明

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

## Split Region 的用法

Split Region 语法分为两种类型：

- 均匀拆分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num` 用于定义上下边界和 Region 数量。然后当前 Region 会在上下边界之间，均匀拆分为 `region_num` 个 Region。

- 非均匀拆分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…` 用于手动指定一系列拆分点，当前 Region 会根据这些点进行拆分。适用于数据分布不均的场景。

以下示例展示了 `SPLIT` 语句的执行结果：

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

* `TOTAL_SPLIT_REGION`：新拆分出来的 Region 数量。
* `SCATTER_FINISH_RATIO`：新拆分 Region 的分散完成率。`1.0` 表示所有 Region 已分散；`0.5` 表示只有一半 Region 已分散，剩余的还在分散中。

> **Note:**
>
> 以下两个会话变量可能会影响 `SPLIT` 语句的行为：
>
> - `tidb_wait_split_region_finish`：Region 分散可能需要一段时间，具体取决于 PD 调度和 TiKV 负载。该变量用于控制执行 `SPLIT REGION` 语句时，是否等所有 Region 分散完成后再将结果返回给客户端。若值为 `1`（默认），TiDB 会在分散完成后返回结果；若值为 `0`，则无论分散是否完成都会立即返回结果。
> - `tidb_wait_split_region_timeout`：该变量用于设置 `SPLIT REGION` 语句的执行超时时间，单位为秒，默认值为 300 秒。如果在该时间内拆分操作未完成，TiDB 会返回超时错误。

### 拆分表 Region

每张表的行数据的 key 由 `table_id` 和 `row_id` 编码，格式如下：

```go
t[table_id]_r[row_id]
```

例如，当 `table_id` 为 22，`row_id` 为 11 时：

```go
t22_r11
```

同一张表的行数据具有相同的 `table_id`，但每行有唯一的 `row_id`，可用于 Region 拆分。

#### 均匀拆分

由于 `row_id` 是整数，可以根据指定的 `lower_value`、`upper_value` 和 `region_num` 计算出要拆分的 key 值。TiDB 首先计算步长（`step = (upper_value - lower_value)/region_num`），然后在 `lower_value` 和 `upper_value` 之间，每隔一个步长均匀拆分，生成 `region_num` 个 Region。

例如，如果你想将表 t 的 key 范围 `minInt64`~`maxInt64` 均匀拆分为 16 个 Region，可以使用如下语句：

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

该语句会将表 t 在 minInt64 到 maxInt64 之间拆分为 16 个 Region。如果主键范围比上述范围小，例如 0~1000000000，可以用 0 和 1000000000 替换 minInt64 和 maxInt64 进行拆分：

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 非均匀拆分

如果已知数据分布不均，想要分别在 key 范围 -inf ~ 10000、10000 ~ 90000、90000 ~ +inf 各拆分一个 Region，可以通过设置固定拆分点实现，如下所示：

```sql
SPLIT TABLE t BY (10000), (90000);
```

### 拆分索引 Region

表中索引数据的 key 由 `table_id`、`index_id` 和索引列的值编码，格式如下：

```go
t[table_id]_i[index_id][index_value]
```

例如，`table_id` 为 22，`index_id` 为 5，`index_value` 为 abc 时：

```go
t22_i5abc
```

同一张表的同一个索引数据具有相同的 `table_id` 和 `index_id`。拆分索引 Region 时，需要根据 `index_value` 进行拆分。

#### 均匀拆分

索引均匀拆分的方式与数据均匀拆分类似。但由于 `index_value` 可能不是整数，步长的计算更为复杂。

`upper` 和 `lower` 的值首先会被编码为字节数组。去除 `lower` 和 `upper` 字节数组的最长公共前缀后，将剩余部分的前 8 个字节分别转为 uint64 格式，然后计算 `step = (upper - lower)/num`。之后，将计算出的步长编码为字节数组，并拼接回最长公共前缀，作为索引拆分点。示例如下：

如果 `idx` 索引的列为整型，可以用如下 SQL 拆分索引数据：

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

该语句会将表 t 的 idx 索引 Region 在 `minInt64` 到 `maxInt64` 之间拆分为 16 个 Region。

如果 idx1 索引的列为 varchar 类型，想按前缀字母拆分索引数据：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

该语句会将 idx1 索引在 a~z 之间拆分为 25 个 Region。Region 1 的范围为 `[minIndexValue, b)`，Region 2 的范围为 `[b, c)`，……，Region 25 的范围为 `[y, minIndexValue]`。对于 idx 索引，前缀为 a 的数据写入 Region 1，前缀为 b 的数据写入 Region 2。

在上述拆分方式中，前缀为 y 和 z 的数据都会写入 Region 25，因为上界不是 z，而是 `{`（ASCII 中 z 的下一个字符）。因此，更精确的拆分方式如下：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

该语句会将表 t 的 idx1 索引在 a~`{` 之间拆分为 26 个 Region。Region 1 的范围为 `[minIndexValue, b)`，Region 2 的范围为 `[b, c)`，……，Region 25 的范围为 `[y, z)`，Region 26 的范围为 `[z, maxIndexValue)`。

如果 idx2 索引的列为时间类型（如 timestamp/datetime），想按年份拆分索引 Region：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

该语句会将表 t 的 idx2 索引 Region 在 `2010-01-01 00:00:00` 到 `2020-01-01 00:00:00` 之间拆分为 10 个 Region。Region 1 的范围为 `[minIndexValue, 2011-01-01 00:00:00)`，Region 2 的范围为 `[2011-01-01 00:00:00, 2012-01-01 00:00:00)`。

如果想按天拆分索引 Region，示例如下：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

该语句会将表 t 的 idx2 索引 2020 年 6 月的数据拆分为 30 个 Region，每个 Region 表示一天。

其他类型索引列的数据 Region 拆分方式类似。

对于联合索引的数据 Region 拆分，唯一的区别是可以指定多列的值。

例如，索引 `idx3 (a, b)` 包含 2 列，a 为 timestamp 类型，b 为 int。如果只想按 a 列的时间范围拆分，可以直接使用单列时间索引的拆分 SQL，此时不需要在 `lower_value` 和 `upper_value` 中指定 b 列的值：

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

在同一时间范围内，如果还想按 b 列再拆分一次，只需在拆分时为 b 列指定值：

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

该语句会在 a 列为同一时间前缀的情况下，按 b 列的值 a~z 拆分为 10 个 Region。如果 a 列指定的值不同，则 b 列的值可能不会被使用。

如果表的主键为 [非聚簇索引](/clustered-indexes.md)，在拆分 Region 时需要用反引号 ``` ` ``` 转义 `PRIMARY` 关键字。例如：

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 非均匀拆分

索引数据也可以通过指定索引值进行拆分。

例如，有 `idx4 (a,b)`，a 为 varchar 类型，b 为 timestamp 类型。

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

该语句指定 3 个值，将数据拆分为 4 个 Region。每个 Region 的范围如下：

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

### 拆分分区表的 Region

分区表的 Region 拆分方式与普通表相同，唯一的区别是每个分区都会执行相同的拆分操作。

+ 均匀拆分的语法：

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

+ 非均匀拆分的语法：

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### 分区表拆分 Region 的示例

1. 创建分区表 `t`。假设要创建一个分为两个分区的 Hash 表，示例如下：

    ```sql
    CREATE TABLE t (a INT, b INT, INDEX idx(a)) PARTITION BY HASH(a) PARTITIONS 2;
    ```

    创建表 t 后，每个分区会拆分出一个 Region。可以使用 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 语法查看该表的 Region：

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

2. 使用 `SPLIT` 语法为每个分区拆分 Region。假设要将每个分区 `[0,10000]` 范围的数据拆分为 4 个 Region，示例如下：

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上述语句中，`0` 和 `10000` 分别代表你想要分散的热点数据的上下边界 `row_id`。

    > **Note:**
    >
    > 该示例仅适用于热点数据均匀分布的场景。如果热点数据在指定数据范围内分布不均，请参考 [分区表拆分 Region](#split-regions-for-partitioned-tables) 中的非均匀拆分语法。

3. 再次使用 `SHOW TABLE REGIONS` 语法查看该表的 Region，可以看到该表现在有 10 个 Region，每个分区有 5 个 Region，其中 4 个为行数据，1 个为索引数据。

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

4. 你还可以为每个分区的索引拆分 Region。例如，可以将 `idx` 索引的 `[1000,10000]` 范围拆分为 2 个 Region，示例如下：

    ```sql
    SPLIT PARTITION TABLE t INDEX idx BETWEEN (1000) AND (10000) REGIONS 2;
    ```

#### 单个分区拆分 Region 的示例

你可以指定要拆分的分区。

1. 创建分区表。假设要创建一个分为 3 个分区的 Range 分区表，示例如下：

    ```sql
    CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
        PARTITION p1 VALUES LESS THAN (10000),
        PARTITION p2 VALUES LESS THAN (20000),
        PARTITION p3 VALUES LESS THAN (MAXVALUE) );
    ```

2. 假设要将 `p1` 分区 `[0,10000]` 范围的数据拆分为 2 个 Region，示例如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1) BETWEEN (0) AND (10000) REGIONS 2;
    ```

3. 假设要将 `p2` 分区 `[10000,20000]` 范围的数据拆分为 2 个 Region，示例如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p2) BETWEEN (10000) AND (20000) REGIONS 2;
    ```

4. 可以使用 `SHOW TABLE REGIONS` 语法查看该表的 Region：

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

5. 假设要将 `p1` 和 `p2` 分区的 `idx` 索引 `[0,20000]` 范围拆分为 2 个 Region，示例如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1,p2) INDEX idx BETWEEN (0) AND (20000) REGIONS 2;
    ```

## pre_split_regions

当创建带有 `AUTO_RANDOM` 或 `SHARD_ROW_ID_BITS` 属性的表时，如果希望在建表后立即将表均匀预拆分为多个 Region，可以指定 `PRE_SPLIT_REGIONS` 选项。表的预拆分 Region 数量为 `2^(PRE_SPLIT_REGIONS)`。

> **Note:**
>
> `PRE_SPLIT_REGIONS` 的值必须小于等于 `SHARD_ROW_ID_BITS` 或 `AUTO_RANDOM` 的值。

[`tidb_scatter_region`](/system-variables.md#tidb_scatter_region) 全局变量会影响 `PRE_SPLIT_REGIONS` 的行为。该变量用于控制建表后是否等待 Region 预拆分并分散完成后再返回结果。如果建表后有大量写入操作，需要将该变量设置为 `global`，此时 TiDB 会根据整个集群的数据分布分散新建表的 Region。否则，TiDB 会在分散完成前写入数据，这会对写入性能产生较大影响。

### pre_split_regions 示例

```sql
CREATE TABLE t (a INT, b INT, INDEX idx1(a)) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=2;
```

建表后，该语句会为表 t 拆分出 `4 + 1` 个 Region。`4 (2^2)` 个 Region 用于存储表行数据，1 个 Region 用于存储 `idx1` 的索引数据。

4 个表 Region 的范围如下：

```
region1:   [ -inf      ,  1<<61 )
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

<CustomContent platform="tidb">

> **Note:**
>
> 通过 Split Region 语句拆分出来的 Region 受 PD 中 [Region merge](/best-practices/pd-scheduling-best-practices.md#region-merge) 调度器控制。为避免 PD 在短时间内重新合并新拆分的 Region，建议使用 [表属性](/table-attributes.md) 或 [动态修改](/pd-control.md) 与 Region merge 相关的配置项。

</CustomContent>

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [SHOW TABLE REGIONS](/sql-statements/sql-statement-show-table-regions.md)
* 会话变量：[tidb_scatter_region](/system-variables.md#tidb_scatter_region)、[tidb_wait_split_region_finish](/system-variables.md#tidb_wait_split_region_finish) 和 [tidb_wait_split_region_timeout](/system-variables.md#tidb_wait_split_region_timeout)
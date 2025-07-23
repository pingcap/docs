---
title: Split Region
summary: 关于在 TiDB 数据库中使用 Split Region 的概述。
---

# Split Region

对于在 TiDB 中创建的每个新表，默认会以一个 [Region](/tidb-storage.md#region) 来存储该表的数据。此默认行为由 TiDB 配置文件中的 `split-table` 控制。当该 Region 中的数据超过默认的 Region 大小限制时，Region 会开始拆分成两个。

在上述情况下，由于一开始只有一个 Region，所有写请求都发生在该 Region 所在的 TiKV 上。如果新创建的表有大量写入操作，就会造成热点。

为了解决上述场景中的热点问题，TiDB 引入了预拆分功能，可以根据指定参数为某个表预先拆分多个 Region，并将它们分散到每个 TiKV 节点。

> **Note:**
>
> 该功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 概要

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

Split Region 有两种语法形式：

- 均匀拆分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

    `BETWEEN lower_value AND upper_value REGIONS region_num` 定义了上边界、下边界和 Region 数量。然后当前 Region 会在上下边界之间均匀拆分成指定的 `region_num` 个 Region。

- 不均匀拆分的语法：

    ```sql
    SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

    `BY value_list…` 指定一系列手动点，根据这些点拆分当前 Region。适用于数据分布不均的场景。

以下示例展示了 `SPLIT` 语句的结果：

```sql
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 4                  | 1.0                  |
+--------------------+----------------------+
```

* `TOTAL_SPLIT_REGION`：新拆分的 Region 数量。
* `SCATTER_FINISH_RATIO`：新拆分 Region 的散布完成率。`1.0` 表示所有 Region 已散布完毕，`0.5` 表示只有一半的 Region 已散布，其余的正在散布中。

> **Note:**
>
> 下面两个会话变量可能会影响 `SPLIT` 语句的行为：
>
> - `tidb_wait_split_region_finish`：散布 Region 可能需要一段时间。此时长取决于 PD 调度和 TiKV 负载。此变量用于控制执行 `SPLIT REGION` 时，是否在所有 Region 散布完成后才返回结果给客户端。若其值设为 `1`（默认），TiDB 仅在散布完成后返回结果；若设为 `0`，无论散布状态如何，TiDB 都会返回结果。
> - `tidb_wait_split_region_timeout`：设置 `SPLIT REGION` 语句的执行超时时间（秒），默认值为 300 秒。如果在此时间内拆分未完成，TiDB 会返回超时错误。

### Split Table Region

每个表中行数据的 key 由 `table_id` 和 `row_id` 编码，格式如下：

```go
t[table_id]_r[row_id]
```

例如，当 `table_id` 为 22，`row_id` 为 11 时：

```go
t22_r11
```

同一表中的行数据具有相同的 `table_id`，但每行有唯一的 `row_id`，可用于 Region 拆分。

#### 均匀拆分

由于 `row_id` 为整数，拆分的 key 值可以根据指定的 `lower_value`、`upper_value` 和 `region_num` 计算。TiDB 首先计算步长（`step = (upper_value - lower_value)/region_num`），然后在 `lower_value` 和 `upper_value` 之间每个“步长”均匀拆分，生成 `region_num` 个 Region。

例如，若要将表 t 在 key 范围 `minInt64`~`maxInt64` 内均匀拆分成 16 个 Region，可以使用如下语句：

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

此语句会将表 t 在 `minInt64` 和 `maxInt64` 之间拆分成 16 个 Region。如果实际主键范围较小，例如 0~1000000000，可以用 0 和 1000000000 代替 `minInt64` 和 `maxInt64` 进行拆分：

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### 不均匀拆分

如果已知数据分布不均，且希望在 `-inf ~ 10000`、`10000 ~ 90000` 和 `90000 ~ +inf` 的区间内拆分 Region，可以通过设置固定点实现，如下所示：

```sql
SPLIT TABLE t BY (10000), (90000);
```

### Split index Region

表中索引数据的 key 由 `table_id`、`index_id` 和索引列的值编码，格式如下：

```go
t[table_id]_i[index_id][index_value]
```

例如，当 `table_id` 为 22，`index_id` 为 5，`index_value` 为 abc 时：

```go
t22_i5abc
```

同一索引在同一表中的 `table_id` 和 `index_id` 相同。拆分索引 Region 时，需要根据 `index_value` 进行拆分。

#### 均匀拆分

均匀拆分索引的方法与数据均匀拆分相同，但计算步长更复杂，因为 `index_value` 可能不是整数。

首先将 `upper` 和 `lower` 的值编码为字节数组。去除 `lower` 和 `upper` 字节数组的最长公共前缀后，将 `lower` 和 `upper` 的前 8 字节转换为 uint64 格式。然后计算 `step = (upper - lower)/num`。之后将计算得到的步长编码为字节数组，附加到 `lower` 和 `upper` 字节数组的最长公共前缀后，用于索引拆分。示例如下：

如果 `idx` 索引列为整数类型，可以使用如下 SQL 语句拆分索引数据：

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

此语句会将表 t 中索引 idx 的 Region 在 `minInt64` 和 `maxInt64` 之间拆分成 16 个 Region。

如果索引列为 varchar 类型，且希望按前缀字母拆分索引数据，可以使用：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 25;
```

此语句会将索引 idx1 拆分成 25 个 Region，从 a 到 z。每个 Region 的范围如下：

- Region 1：`[minIndexValue, b)`
- Region 2：`[b, c)`
- ...
- Region 25：`[y, minIndexValue]`

对于 `idx` 索引，前缀为 `a` 的数据写入 Region 1，前缀为 `b` 的数据写入 Region 2。

在上述拆分方法中，前缀为 `y` 和 `z` 的数据都写入第 25 个 Region，因为上界不是 `z`，而是 `{`（ASCII 中 `z` 后的字符）。因此，更精确的拆分方法如下：

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("{") REGIONS 26;
```

此语句会将表 t 中索引 idx1 拆分成 26 个 Region，从 a 到 `{`。每个 Region 的范围如下：

- Region 1：`[minIndexValue, b)`
- Region 2：`[b, c)`
- ...
- Region 25：`[y, z)`
- Region 26：`[z, maxIndexValue)`

如果索引 `idx2` 的列为时间类型（如 timestamp/datetime），且希望按年份拆分索引 Region：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

此语句会将表 t 中索引 `idx2` 的 Region 在 `"2010-01-01 00:00:00"` 到 `"2020-01-01 00:00:00"` 之间拆分成 10 个 Region，范围如下：

- Region 1：`[minIndexValue, 2011-01-01 00:00:00)`
- Region 2：`[2011-01-01 00:00:00, 2012-01-01 00:00:00)`
- 以此类推。

如果希望按天拆分索引 Region，示例如下：

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2020-06-01 00:00:00") AND ("2020-07-01 00:00:00") REGIONS 30;
```

此语句会将索引 `idx2` 在 2020 年 6 月的范围内拆分成 30 个 Region，每个代表 1 天。

其他类型索引列的 Region 拆分方法类似。

对于联合索引的 Region 拆分，唯一的区别是可以指定多个列的值。

例如，索引 `idx3 (a, b)` 包含 2 列，列 `a` 为时间类型，列 `b` 为 int。如果只想根据列 `a` 的时间范围拆分，可以使用单列时间索引的拆分语法，不在 `lower_value` 和 `upper_value` 中指定列 `b` 的值。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

在相同时间范围内，如果还想根据列 `b` 进行拆分，只需在拆分时为列 `b` 指定值即可。

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

此语句会在列 `a` 的时间范围内，将索引拆分成 10 个 Region，且每个 Region 内列 `b` 的值范围相同。如果列 `a` 的值不同，列 `b` 的值可能不会被用到。

如果表的主键为 [non-clustered index](/clustered-indexes.md)，在拆分 Region 时需要用反引号 ``` ` ``` 转义 `PRIMARY` 关键字，例如：

```sql
SPLIT TABLE t INDEX `PRIMARY` BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

#### 不均匀拆分

索引数据也可以通过指定索引值进行拆分。

例如，有 `idx4 (a,b)`，列 `a` 为 varchar 类型，列 `b` 为 timestamp 类型。

```sql
SPLIT TABLE t1 INDEX idx4 BY ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");
```

此语句指定 3 个值，将索引拆分成 4 个 Region。每个 Region 的范围如下：

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

### Partitioned 表的 Region 拆分

对分区表进行 Region 拆分与普通表相同，唯一的区别是对每个分区都执行相同的拆分操作。

+ 均匀拆分的语法：

    ```sql
    SPLIT [PARTITION] TABLE t [PARTITION] [(partition_name_list...)] [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
    ```

+ 不均匀拆分的语法：

    ```sql
    SPLIT [PARTITION] TABLE table_name [PARTITION (partition_name_list...)] [INDEX index_name] BY (value_list) [, (value_list)] ...
    ```

#### 分区表的 Region 拆分示例

1. 创建一个分区表 `t`。假设你想创建一个哈希分区表，分成两个分区，示例语句如下：

    ```sql
    CREATE TABLE t (a INT, b INT, INDEX idx(a)) PARTITION BY HASH(a) PARTITIONS 2;
    ```

    创建表 `t` 后，会为每个分区拆分出一个 Region。可以使用 [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) 查看该表的 Region：

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

2. 使用 `SPLIT` 语法对每个分区的 Region 进行拆分。例如，想将每个分区 `[0,10000]` 范围内的数据拆分成 4 个 Region，示例语句如下：

    ```sql
    split partition table t between (0) and (10000) regions 4;
    ```

    上述语句中的 `0` 和 `10000` 分别代表对应热点数据的上、下边界的 `row_id`。

    > **Note:**
    >
    > 该示例仅适用于热点数据均匀分布的场景。如果热点数据在指定数据范围内分布不均，参考 [Split Regions for partitioned tables](#split-regions-for-partitioned-tables) 中的不均匀拆分语法。

3. 再次使用 `SHOW TABLE REGIONS` 查看表的 Region，可以看到该表现在有十个 Region，每个分区有五个 Region，其中四个是行数据，一个是索引数据。

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

4. 你也可以对每个分区的索引 Region 进行拆分。例如，将 `idx` 索引在 `[1000, 10000]` 范围内拆分成两个 Region，示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t INDEX idx BETWEEN (1000) AND (10000) REGIONS 2;
    ```

#### 单个分区的 Region 拆分示例

你可以指定要拆分的分区。

1. 创建一个分区表。假设你要创建一个 Range 分区表，拆分成三个分区，示例语句如下：

    ```sql
    CREATE TABLE t ( a INT, b INT, INDEX idx(b)) PARTITION BY RANGE( a ) (
        PARTITION p1 VALUES LESS THAN (10000),
        PARTITION p2 VALUES LESS THAN (20000),
        PARTITION p3 VALUES LESS THAN (MAXVALUE) );
    ```

2. 假设你要将 `p1` 分区的 `[0,10000]` 范围内的数据拆分成两个 Region，示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1) BETWEEN (0) AND (10000) REGIONS 2;
    ```

3. 假设你要将 `p2` 分区的 `[10000,20000]` 范围内的数据拆分成两个 Region，示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p2) BETWEEN (10000) AND (20000) REGIONS 2;
    ```

4. 使用 `SHOW TABLE REGIONS` 查看该表的 Region：

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

5. 假设你想将 `p1` 和 `p2` 分区的 `[0, 20000]` 范围内的索引 `idx` 拆分成两个 Region，示例语句如下：

    ```sql
    SPLIT PARTITION TABLE t PARTITION (p1,p2) INDEX idx BETWEEN (0) AND (20000) REGIONS 2;
    ```
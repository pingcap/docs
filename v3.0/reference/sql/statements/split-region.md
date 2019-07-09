---
title: Split Region | TiDB SQL Statement Reference 
summary: An overview of the usage of Split Region for the TiDB database.
category: reference
---

# Split Region

When creating a new table in TiDB, 1 Region will be split to store the data of this table by default. This default behavior is controlled by `split-table` in the configuration file. When the data in this Region exceeds the default Region size limit, the Region will start splitting into 2 Regions.

In the above case, if a large number of writes occur on the newly created table, it will cause a hot spot. Because there is only one Region at the beginning, and all wirte requests occur on the TiKV where the Region is located.

To solve the porblem above, TiDB introduces the pre-split function, which can pre-split mutiple Regions for a certain table accroding to the parameters specified by the user and break them to each TiKV.

## Usage of Split Region 

There are two types of Split Region grammar:

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

`BETWEEN lower_value AND upper_value REGIONS region_num` can be used to define the Upper bundary, lower boundary and Region amount. Then the region will be evenly spilt into several regions between the upper and lower budaries according to these parameters.

{{< copyable "sql" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)] ...
```

`BY value_list…` can be used to specify a series of points manually, then the Region will be spilt according to them. It is suitable for a scenario which data is unevenly distributed.

### Split Table Region

Key of row data in each table is consist of encoding`table_id` and `row_id`. The format is as follows:

```go
t[table_id]_r[row_id]
```

For example, when `table_id` is 22 and `row_id` is 11:

```go
t22_r11
```

Each row data in the same table has the same `table_id` but their `row_id` of them is definitely different which could be used for splitting Region.

#### Evenly Split

Because `row_id` is integer, the value of key can be cacualted easily according to `lower_value`,`upper_value` and `region_num` defined by user. It will start with step (`step = (upper_value - lower_value)/num`). Then cut every step between `lower_value` 和 `upper_value` util there are  `num` Regions.

For example: For table t, if you want 16 evenly splitted Regions from `minInt64`~`maxInt64`, you can use this statement:

{{< copyable "sql" >}}

```sql
SPLIT TABLE t BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

This statement will cut the region from minInt64 to maxInt64 in table t into 16 Regions. If the range of known primary key is smaller than that, like between 0~1000000000, you can use 0 and 1000000000 instead of minInt64 and maxInt64 to split Region.

{{< copyable "sql" >}}

```sql
SPLIT TABLE t BETWEEN (0) AND (1000000000) REGIONS 16;
```

#### Unevenly Split

What to do when the known data is unevenly distributed? For example, you want to get spliited regions in -inf ~ 10000, 10000 ~ 90000 and 90000 ~ +inf. You can do this by setting fixed points as follows:

{{< copyable "sql" >}}

```sql
SPLIT TABLE t BY (10000), (90000);
```

### Split Index Region

The key of each index data in table is consist by encoding `table_id`,`index_id` and value of Index Value. The format is as follows:

```go
t[table_id]_i[index_id][index_value]
```

For example, when `table_id` is 22, `index_id` is 5 and `index_value` is abc:

```go
t22_i5abc
```

The `table_id` and `index_id` of same index data in the same table is the same, so you need to split the index Region by `index_value

#### Evenly Spilt

The way to split index evenly is the same as splitting data evenly. However calculating the value of step may be complicated, because the `index_value` may not be an integer.

The value of `upper` and `lower` will be encoded into byte array firstly. After deleting the longest common prefix of `lower` and `upper` byte array, the first 8 bytes of `lower` and `upper` will be transformed into uint64 format. Then `step = (upper - lower)/num` will be calculated. After calculating, step will be encoded into byte array, which will be added to the back of the longest common prefix to build a key for spliting. Here is the example:

If the row of index idx is an integer, you can use the following SQL statements to split index data:

{{< copyable "sql" >}}

```sql
SPLIT TABLE t INDEX idx BETWEEN (-9223372036854775808) AND (9223372036854775807) REGIONS 16;
```

This statement will split the region of index data idx in table t into 16 Regions from `minInt64` to `maxInt64`.

If the volume of index data idx1 is varchar type, it is suggested to split index data by prefix letter.

{{< copyable "sql" >}}

```sql
SPLIT TABLE t INDEX idx1 BETWEEN ("a") AND ("z") REGIONS 26;
```

This statement will split index data idx1 into 26 Regions from a~z. The range of region1 is [minIndexValue, b), region2 is [b, c),……,region26 is [z, minIndexValue]. For index idx, data whose prefix is a will be written into region1, b will be written into region2 and so on.

If the column of index idx2 is time type like timestamp/datetime, it is suggested to split by time interval:

{{< copyable "sql" >}}

```sql
SPLIT TABLE t INDEX idx2 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

This statemnt will spilt the region of index data idx2 in table t into 10 Regions from  `2010-01-01 00:00:00` tp  `2020-01-01 00:00:00`. The range of region1 is `[minIndexValue,  2011-01-01 00:00:00)`, region2 is `[2011-01-01 00:00:00, 2012-01-01 00:00:00)`……

Other splitting ways for index column are similar to that.

For splitting data Regions of joint index, the only one different thing is you can specific the value of several columns.

For example, index `idx3 (a, b)` contains 2 columns, a for timestamp and b for int. If you just want to split time range according to a column, you can use SQL statement for single time index, just don't specify the value of b column in `lower_value` and `upper_velue`.

{{< copyable "sql" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00") AND ("2020-01-01 00:00:00") REGIONS 10;
```

If you want to do one more split according to b column at the same time, you need to specify the value of b column when spilting.

{{< copyable "sql" >}}

```sql
SPLIT TABLE t INDEX idx3 BETWEEN ("2010-01-01 00:00:00", "a") AND ("2010-01-01 00:00:00", "z") REGIONS 10;
```

With the same time prefix of a column, this statement split out 10 regions according to the value of b column. If the value of speciied a column is different, you don't need to use the value of b column.

#### Unevenly Split

Index data can also be splited by index value specified by user.

For example, there is idx4 (a,b) whose a column is varchar and b colun is timestamp.

{{< copyable "sql" >}}

```sql
SPLIT TABLE t1 INDEX idx4 ("a", "2000-01-01 00:00:01"), ("b", "2019-04-17 14:26:19"), ("c", "");  
```

This statement specifies 3 value and cuts out 4 Regions. The range of each Region are shown as follows:

```
region1  [ minIndexValue               , ("a", "2000-01-01 00:00:01"))
region2  [("a", "2000-01-01 00:00:01") , ("b", "2019-04-17 14:26:19"))
region3  [("b", "2019-04-17 14:26:19") , ("c", "")                   )
region4  [("c", "")                    , maxIndexValue               )
```

## pre_split_regions

When using table with `shard_row_id_bits`, it is suggested to use with `pre_split_regions` if you want to spilt Region evenly at the start of building table. `pre_split_regions` spilt `2^(pre_split_regions-1)` Region evenly after the table is built.

> **Note:**
>
> `pre_split_regions` must amount to less than or equal to `shard_row_id_bits`.

### Example

{{< copyable "sql" >}}

```sql
create table t (a int, b int,index idx1(a)) shard_row_id_bits = 4 pre_split_regions=3;
```

After building that table, this statement will cut out 4 + 1  Regions form table t. 4 (2^(3-1)) Regions for saving table row data,1 Region for saving idx1 index data.

The range of 4 table Region are shown as follows:

```
region1:   [ -inf      ,  1<<61 )  
region2:   [ 1<<61     ,  2<<61 )
region3:   [ 2<<61     ,  3<<61 )
region4:   [ 3<<61     ,  +inf  )
```

Why the amount of Region is 2^(pre_split_regions-1)? Because when using shard_row_id_bits, only positive numbers will be assigned to `_tidb_rowid`, so there is no need to do Spilt Region for the negative interval.

## Related session variable

There are two `SPLIT REGION` related session variables: `tidb_wait_split_region_finish` and `tidb_wait_split_region_timeout`. See[TiDB specific system variables and syntax](/dev/reference/configuration/tidb-server/tidb-specific-variables.md).

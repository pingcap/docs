---
title: SHOW TABLE REGIONS
summary: Learn how to use SHOW TABLE REGIONS in TiDB.
aliases: ['/docs/v2.1/sql-statements/sql-statement-show-table-regions/','/docs/v2.1/reference/sql/statements/show-table-regions/']
---

# SHOW TABLE REGIONS

The `SHOW TABLE REGIONS` statement is used to show the Region information of a table in TiDB.

## Synopsis

```sql
SHOW TABLE [table_name] REGIONS [WhereClauseOptional];

SHOW TABLE [table_name] INDEX [index_name] REGIONS [WhereClauseOptional];
```

Executing `SHOW TABLE REGIONS` returns the following columns:

* `REGION_ID`: The Region ID.
* `START_KEY`: The start key of the Region.
* `END_KEY`: The end key of the Region.
* `LEADER_ID`: The Leader ID of the Region.
* `LEADER_STORE_ID`: The ID of the store (TiKV) where the Region leader is located.
* `PEERS`: The IDs of all Region replicas.
* `SCATTERING`: Whether the Region is being scheduled. `1` means true.

## Examples

Create an example table with enough data that fills a few Regions:

{{< copyable "sql" >}}

```sql
CREATE TABLE t1 (
 id INT NOT NULL PRIMARY KEY auto_increment,
 b INT NOT NULL,
 pad1 VARBINARY(1024),
 pad2 VARBINARY(1024),
 pad3 VARBINARY(1024)
);
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM dual;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
INSERT INTO t1 SELECT NULL, FLOOR(RAND()*1000), RANDOM_BYTES(1024), RANDOM_BYTES(1024), RANDOM_BYTES(1024) FROM t1 a JOIN t1 b JOIN t1 c LIMIT 10000;
SELECT SLEEP(5);
SHOW TABLE t1 REGIONS;
```

The output should show that the table is split into Regions. The `REGION_ID`, `START_KEY` and `END_KEY` may not match exactly:

```sql
<<<<<<< HEAD
test> show table t regions;
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| REGION_ID | START_KEY | END_Key | LEADER_ID | LEADER_STORE_ID | PEERS     | SCATTERING |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
| 5         | t_43_     |         | 8         | 2               | 8, 14, 93 | 0          |
+-----------+-----------+---------+-----------+-----------------+-----------+------------+
1 row in set
```

In the above example, `t_43_` is the value of `START_KEY` row. In this value, `t` is the table prefix and `43` is the table ID. The value of `END_KEY` row is empty (""), which means that it is an infinite value.
=======
...
mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |
|        96 | t_75_r_31717 | t_75_r_63434 |        97 |               1 | 97    |          0 |             0 |          0 |                   97 |                0 |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |     269323514 |   66346110 |                  245 |           162020 |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
3 rows in set (0.00 sec)
```

In the output above, a `START_KEY` of `t_75_r_31717` and `END_KEY` of `t_75_r_63434` shows that data with a PRIMARY KEY between `31717` and `63434` is stored in this Region. The prefix `t_75_` indicates that this is the Region for a table (`t`) which has an internal table ID of `75`. An empty key value for `START_KEY` or `END_KEY` indicates negative infinity or positive infinity respectively.
>>>>>>> c5acf0a... sql-statements: improve SHOW TABLE REGIONS examples (#3389)

TiDB automatically rebalances Regions as needed. For manual rebalancing, use the `SPLIT TABLE REGION` statement:

```sql
mysql> SPLIT TABLE t1 BETWEEN (31717) AND (63434) REGIONS 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
|                  1 |                    1 |
+--------------------+----------------------+
<<<<<<< HEAD
1 row in set
```

```sql
test> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
| 98        | t_43_r       | t_43_r_20000 | 100       | 4               | 100, 101, 102 | 0          |
| 103       | t_43_r_20000 | t_43_r_40000 | 108       | 5               | 104, 108, 107 | 0          |
| 109       | t_43_r_40000 | t_43_r_60000 | 110       | 1               | 110, 111, 112 | 0          |
| 113       | t_43_r_60000 | t_43_r_80000 | 117       | 6               | 116, 117, 118 | 0          |
| 2         | t_43_r_80000 |              | 3         | 1               | 3, 91, 92     | 0          |
| 68        | t_43_        | t_43_r       | 90        | 6               | 69, 90, 97    | 0          |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+
=======
1 row in set (42.34 sec)

mysql> SHOW TABLE t1 REGIONS;
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
|        94 | t_75_        | t_75_r_31717 |        95 |               1 | 95    |          0 |             0 |          0 |                  112 |           207465 |
|        98 | t_75_r_31717 | t_75_r_47575 |        99 |               1 | 99    |          0 |          1325 |          0 |                   53 |            12052 |
|        96 | t_75_r_47575 | t_75_r_63434 |        97 |               1 | 97    |          0 |          1526 |          0 |                   48 |                0 |
|         2 | t_75_r_63434 |              |         3 |               1 | 3     |          0 |             0 |   55752049 |                   60 |                0 |
+-----------+--------------+--------------+-----------+-----------------+-------+------------+---------------+------------+----------------------+------------------+
4 rows in set (0.00 sec)
```

The above output shows that Region 96 was split, with a new Region 98 being created. The remaining Regions in the table were unaffected by the split operation. This is confirmed by the output statistics:

* `TOTAL_SPLIT_REGION` indicates the number of newly split Regions. In this example, the number is 1.
* `SCATTER_FINISH_RATIO` indicates the rate at which the newly split Regions are successfully scattered. `1.0` means that all Regions are scattered.

For a more detailed example:

```sql
mysql> show table t regions;
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| REGION_ID | START_KEY    | END_KEY      | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
| 102       | t_43_r       | t_43_r_20000 | 118       | 7               | 105, 118, 119 | 0          | 0             | 0          | 1                    | 0                |
| 106       | t_43_r_20000 | t_43_r_40000 | 120       | 7               | 107, 108, 120 | 0          | 23            | 0          | 1                    | 0                |
| 110       | t_43_r_40000 | t_43_r_60000 | 112       | 9               | 112, 113, 121 | 0          | 0             | 0          | 1                    | 0                |
| 114       | t_43_r_60000 | t_43_r_80000 | 122       | 7               | 115, 122, 123 | 0          | 35            | 0          | 1                    | 0                |
| 3         | t_43_r_80000 |              | 93        | 8               | 5, 73, 93     | 0          | 0             | 0          | 1                    | 0                |
| 98        | t_43_        | t_43_r       | 99        | 1               | 99, 100, 101  | 0          | 0             | 0          | 1                    | 0                |
+-----------+--------------+--------------+-----------+-----------------+---------------+------------+---------------+------------+----------------------+------------------+
>>>>>>> c5acf0a... sql-statements: improve SHOW TABLE REGIONS examples (#3389)
6 rows in set
```

In the above example:

* Table t corresponds to six Regions. In these Regions, `98`, `103`, `109`, `113`, and `2` store the row data. `68` stores the index data.
* For `START_KEY` and `END_KEY` of Region `98`, `t_43` indicates the table prefix and ID. `_r` is the prefix of the record data in table t. `_i` is the prefix of the index data.
* In Region `98`, `START_KEY` and `END_KEY` mean that record data in the range of `[-inf, 20000)` is stored. In similar way, the ranges of data storage in Regions (`103`, `109`, `113`, `2`) can also be calculated.
* Region `68` stores the index data. The start key of table t's index data is `t_43_i`, which is in the range of Region `68`.

Use `SPLIT TABLE REGION` to split the index data into Regions. In the following example, the index data `name` of table t is split into two Regions in the range of `[a,z]`.

```sql
test> split table t index name between ("a") and ("z") regions 2;
+--------------------+----------------------+
| TOTAL_SPLIT_REGION | SCATTER_FINISH_RATIO |
+--------------------+----------------------+
| 2                  | 1.0                  |
+--------------------+----------------------+
1 row in set
```

Now table t corresponds to seven Regions. Five of them (`98`, `103`, `109`, `113`, `2`) store the record data of table t and another two (`125`, `68`) store the index data `name`.

```sql
test> show table t regions;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| 98        | t_43_r                      | t_43_r_20000                | 100       | 4               | 100, 101, 102 | 0          |
| 103       | t_43_r_20000                | t_43_r_40000                | 108       | 5               | 104, 108, 107 | 0          |
| 109       | t_43_r_40000                | t_43_r_60000                | 110       | 1               | 110, 111, 112 | 0          |
| 113       | t_43_r_60000                | t_43_r_80000                | 117       | 6               | 116, 117, 118 | 0          |
| 2         | t_43_r_80000                |                             | 3         | 1               | 3, 91, 92     | 0          |
| 125       | t_43_i_1_                   | t_43_i_1_016d80000000000000 | 127       | 6               | 127, 128, 129 | 0          |
| 68        | t_43_i_1_016d80000000000000 | t_43_r                      | 90        | 6               | 69, 90, 97    | 0          |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
7 rows in set
```

<<<<<<< HEAD
To check the Region that corresponds to table t in store 1, use the `WHERE` clause:

```sql
test> show table t regions where leader_store_id =1;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS         | SCATTERING |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
| 109       | t_43_r_40000                | t_43_r_60000                | 110       | 1               | 110, 111, 112 | 0          |
| 2         | t_43_r_80000                |                             | 3         | 1               | 3, 91, 92     | 0          |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------+------------+
2 rows in set
```
=======
## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
>>>>>>> c5acf0a... sql-statements: improve SHOW TABLE REGIONS examples (#3389)

## See also

* [SPLIT REGION](/sql-statements/sql-statement-split-region.md)
* [CREATE TABLE](/sql-statements/sql-statement-create-table.md)

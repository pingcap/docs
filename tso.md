---
title: TimeStamp Oracle
summary: Learn about TSO timestamps in TiDB.
---

One of the tasks of the Placement Driver (PD) is to hand out timestamps to other components of the cluster. Transactions and data get timestamps assigned and this allows the [Percolator](https://research.google.com/pubs/pub36726.html) model in TiDB to work, which is used for MVCC and [transactions](/transaction-overview.md).

Let's get a TSO timestamp:

```
mysql> BEGIN; SET @ts := @@tidb_current_ts; ROLLBACK;
Query OK, 0 rows affected (0.0007 sec)
Query OK, 0 rows affected (0.0002 sec)
Query OK, 0 rows affected (0.0001 sec)

sql> SELECT @ts;
+--------------------+
| @ts                |
+--------------------+
| 443852055297916932 |
+--------------------+
1 row in set (0.00 sec)
```

Note that this is done in a transction with (`BEGIN; ...; ROLLBACK`) as TSO timestamps are assigned to transactions.

There are two SQL function which helps us to inspect the number that we got back: [`TIDB_PARSE_TSO()`](/functions-and-operators/tidb-functions.md#tidb_parse_tso) and [`TIDB_PARSE_TSO_LOGICAL()`]((/functions-and-operators/tidb-functions.md#tidb_parse_tso_logical).

```
mysql> SELECT TIDB_PARSE_TSO(443852055297916932);
+------------------------------------+
| TIDB_PARSE_TSO(443852055297916932) |
+------------------------------------+
| 2023-08-27 20:33:41.687000         |
+------------------------------------+
1 row in set (0.00 sec)

mysql> SELECT TIDB_PARSE_TSO_LOGICAL(443852055297916932);
+--------------------------------------------+
| TIDB_PARSE_TSO_LOGICAL(443852055297916932) |
+--------------------------------------------+
|                                          4 |
+--------------------------------------------+
1 row in set (0.00 sec)
```

Let's now dive a bit deeper into what a TSO timestamp looks like:

```
0000011000101000111000010001011110111000110111000000000000000100  ← This is 443852055297916932, but in binary
0000011000101000111000010001011110111000110111                    ← The first 46 bits are the physical timestamp
                                              000000000000000100  ← The last 18 bits are the logical timestamp
```

There are two parts to the TSO timestamp:

- The *Physical timestamp*: This is a UNIX timestamp in milliseconds since 1 January 1970.
- The *Logical timestamp*: This is an increasing counter. This is used when there are multiple timestamps needed within the same millisecond or if there is a change that makes the clock go backwards, in that case the physical timestamp is kept the same while the logical timestamp increases. This is done as the TSO timestamp is guaranteed to never go back.

With this knowledge we can inspect the TSO timestamp a bit more in SQL:

```
mysql> SELECT @ts, UNIX_TIMESTAMP(NOW(6)), (@ts >> 18)/1000, FROM_UNIXTIME((@ts >> 18)/1000), NOW(6), @ts-((@ts >> 18) << 18)\G
*************************** 1. row ***************************
                            @ts: 443852055297916932
         UNIX_TIMESTAMP(NOW(6)): 1693161835.502954
               (@ts >> 18)/1000: 1693161221.6870
FROM_UNIXTIME((@ts >> 18)/1000): 2023-08-27 20:33:41.6870
                         NOW(6): 2023-08-27 20:43:55.502954
        @ts-((@ts >> 18) << 18): 4
1 row in set (0.00 sec)
```

The `>> 18` is to [shift right](/functions-and-operators/bit-functions-and-operators.md) by 18 bits, which is used to filter out the physical timestamp. As the physical timestamp is in milliseconds and not in seconds as is more usual for UNIX timestamps we need to divide by 1000 to get it in the format that [`FROM_UNIXTIME()`](/functions-and-operators/date-and-time-functions.md) understands. This is basically the same as what `TIDB_PARSE_TSO()` does for us.

Then we also filter out the logical timestamp: `000000000000000100` in binary, which is 4 in decimals.

And let's do the same via the CLI tools:

```
$ tiup ctl pd tso 443852055297916932                                                              
Starting component `ctl`: /home/dvaneeden/.tiup/components/ctl/v7.3.0/ctl pd tso 443852055297916932
system:  2023-08-27 20:33:41.687 +0200 CEST
logic:   4
```

Here you can see the same physical timestamp in the line that starts with `system:` and the logical timestamp in the line that starts with `logic:`.

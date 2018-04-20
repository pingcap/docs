---
title: TiDB Garbage Collection (GC)
category: advanced
---

# TiDB Garbage Collection (GC)

TiDB uses MVCC to control concurrency. When you update or delete data, the data is not deleted immediately and it is saved for a period during which it can be read. Thus the write operation and the read operation are not mutually exclusive and it is possible to read the previous data.

The data versions whose duration exceeds a specific time and that are not used any more will be cleared, or they will occupy the disk space, affecting the system performance. TiDB uses Garbage Collection (GC) to clear the obsolete data. 

## Working mechanism

GC runs periodically on TiDB. When a TiDB server is started, a `gc_worker` is enabled in the background. In a TiDB cluster, one `gc_worker` is elected to be the leader which is used to maintain the GC status and send GC commands to all the TiKV Region leaders. 

## Configuration and monitor

The GC configuration and operation status are recorded in the `mysql.tidb` system table, which can be monitored and configured using the following SQL statement:

```sql
mysql> select VARIABLE_NAME, VARIABLE_VALUE from mysql.tidb;
+-----------------------+------------------------------------------------------------------------------------------------+
| VARIABLE_NAME         | VARIABLE_VALUE                                                                                 |
+-----------------------+------------------------------------------------------------------------------------------------+
| bootstrapped          | True                                                                                           |
| tidb_server_version   | 18                                                                                             |
| tikv_gc_leader_uuid   | 58accebfa7c0004                                                                                |
| tikv_gc_leader_desc   | host:ip-172-16-30-5, pid:95472, start at 2018-04-11 13:43:30.73076656 +0800 CST m=+0.068873865 |
| tikv_gc_leader_lease  | 20180418-11:02:30 +0800 CST                                                                    |
| tikv_gc_run_interval  | 10m0s                                                                                          |
| tikv_gc_life_time     | 10m0s                                                                                          |
| tikv_gc_last_run_time | 20180418-10:59:30 +0800 CST                                                                    |
| tikv_gc_safe_point    | 20180418-10:58:30 +0800 CST                                                                    |
| tikv_gc_concurrency   | 1                                                                                              |
+-----------------------+------------------------------------------------------------------------------------------------+
10 rows in set (0.02 sec)
```

In the table above, `tikv_gc_run_interval`, `tikv_gc_life_time` and `tikv_gc_concurrency` can be configured manually. Other `tikv_gc`- variables record the current status, which are automatically updated by TiDB. Do not modify these variables.

`tikv_gc_run_interval` (10 min by default) indicates the interval of GC work. `tikv_gc_life_time` (10 min by default) indicates the retaining time of data versions. When GC works, the outdated data is cleared. The `tikv_gc_run_interval` and `tikv_gc_life_time` should be not less than 10 minutes. You can set them using SQL statements. For example, if you want to retain the data within a day, you can execute the operation as below:

```sql
update mysql.tidb set VARIABLE_VALUE = '24h' where VARIABLE_NAME = 'tikv_gc_life_time';
```

The duration strings are a sequence of a number with the time unit, such as `24h`, `2h30m` and `2.5h`. The time units you can use include "h", "m" and "s".

> **Note**: When you set `tikv_gc_life_time` to a large number (like days or even months) in a data updated frequently scenario, some problems as follows may occur: 

    - The more versions of the data, the more disk storage space is occupied.
    - A large number of history versions might slow down the query. They may affect range queries like `select count(*) from t`.
    - If `tikv_gc_life_time` is suddenly turned to a smaller value during operation, a great deal of old data may be deleted in a short time, causing I/O pressure.

`tikv_gc_concurrency` indicates the GC concurrency. It is set to `1` by default. In this case, a single thread operates and threads send request to each Region and wait for the response one by one. You can set the variable value larger to improve the system performance, but keep the value smaller than 128. 

`tikv_gc_leader_uuid`, `tikv_gc_leader_desc`, `tikv_gc_leader_lease` indicate the current GC leader information. `tikv_gc_last_run_time` indicates the last time GC works.

`tikv_gc_safe_point` indicates the time, versions before which are cleared by GC and versions after which are readable.

## Implementation details

The GC implementation process is complex. Clearing the data that is not used any more should be on the premise that data consistency is guaranteed. The process of doing GC is as below:

### 1. Resolve locks

The TiDB transaction is based on Google Percolator. The transaction committing is a two-phase committing process. When the first phase is finished, all the related keys are locked. Among these locks, one is the primary lock and the others are secondary locks which contain a pointer of the primary locks; in the secondary phase, the key with the primary lock gets a write record and its lock is removed. The write record indicates the write or delete operation in the history or the transactional rollback record of this key. Replacing the primary lock by which write record indicates whether the corresponding transaction is committed successfully. Then all the secondary locks are replaced successively. If the threads to replace the secondary locks fail, these locks are retained. During GC, locks whose timestamp is before the safe point will be replaced by the corresponding write record based on the transaction committing status.

This step is necessary, because you are not informed whether this transaction is successful if GC has cleared the write record of the primary lock, thus data consistency cannot be guaranteed.

### 2. Delete ranges

The `DeleteRanges` operation is usually necessary after the operation such as `drop table`. It is used to delete a range which may be very large. If the `use_delete_range` option of TiKV is not enabled, TiKV deletes the keys in the range.

### 3. Do GC

Clear the data before the safe point of each key and the write record. 
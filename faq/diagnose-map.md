---
title: TiDB Common Issue Diagnose Map
summary:
category: faq
---

# TiDB Common Issue Diagnose Map

## 6. Ecosystem tools

### 6.1 Binlog

### 6.2 DM

### 6.3 TiDB lightning

- 6.3.1: TiDB lightning is a tool for fast full import of large amounts of data into a TiDB cluster. See [TiDB Lightning Github](https://github.com/pingcap/tidb-lightning).

- 6.3.2: Import is slow.

    - `region-concurrency` is set too high. This causes different threads to compete for resources, which reduces efficiency. Three ways to troubleshoot:

        - Search `region-concurrency` from the start of the log to see the parameter TiDB Lightning reads.
        - If TiDB Lightning shares a server with other services such as Importer, you must manually set `region-concurrency` to 75% of the CPU units on that server.
        - If the CPU has set a limit (such as an upper limit specified by Kubernetes), TiDB Lightning might not be able to find the limit. You need to manually modify `region-concurrency`.

    - The table schema is complicated. Each index adds extra Key-Value pairs. If there are N indexes, the actually data being imported is around N+1 times of the Mydumper file size. Therefore, if the index is not important, you might remove the index from the schema and add it back by using CREATE INDEX after the import is completed.
    - The version of TiDB Lightning is old. Try the latest version, which might improve this issue.

6.3.3: `"checksum failed: checksum mismatched remote vs local"`.

    - Reason 1: This table 

## 7. Common log analysis

### 7.1 TiDB

- 7.1.1: "GC life time is shorter than transaction duration".

    The transaction duration exceeds the GC lifetime (10 minutes by default).
    
    You can increase the GC lifetime by modifying the `mysql.tidb` table. Generally, it is not recommended to modify this parameter, because it might cause many old versions to pile up if this transaction has a large number of update and delete statements.

- 7.1.2: "txn takes too much time".

    This error is returned when you commit a transaction that has not been committed for a long time (over 590 seconds).

    If your application needs to execute a transaction of such a long time, you can increase the `[tikv-client] max-txn-time-use = 590` parameter and the GC lifetime to avoid this issue.

- 7.1.3: `coprocessor.go` reports `"request outdated"`.

    This error is returned when the coprocessor request sent to TiKV waits in a queue at TiKV for over 60 seconds.

    You need to investigate why the TiKV coprocessor is in a long queue.

- 7.1.4: `region_cache.go` reports a large number of `"switch region peer to next due to send request fail"`, and the error message is `"context deadline exceeded"`.

    The request for TiKV timed out and triggers the region cache to switch the request to other nodes. You can continue to run the `grep "<addr> cancelled` command to the `addr` field in the log and take the following steps according to the `grep` results:

    - `"send request is cancelled"`: The request timed out during the sending phase. You can investigate the monitoring grafana -> TiDB -> Batch Client/Pending Request Count by TiKV and see whether the Pending Request Count is greater than 128:

        - If the value is greater than 128, the sending goes beyond the processing capacity of KV, so the sending piles up.
        - If the value is not greater than 128, check the log to see if the report is caused by the operation and maintenance changes of the corresponding KV; otherwise, this error is unexpected, and you need to report a bug.

    - `"wait response is cancelled"`: The request timed out after it is sent to TiKV. You need to check the response time of the corresponding TiKV address and the Region logs in PD and KV at that time.

- 7.1.5: `distsql.go` reports `"inconsistent index"`.

    The data index seems to be inconsistent. Run the `admin check table <TableName>` command on the table where the reported index is. If the check fails, close GC by running the following command, and report a bug:

    ```sql
    begin;
    update mysql.tidb set variable_value='72h' where variable_name='tikv_gc_life_time';
    commit;
    ```

### 7.2 TiKV

- 7.2.1: `"key is locked"`.

    The read and write have conflict. The read request encounters data that has not been committed and needs to wait until the data is committed.

    A small number of this error has no impact on the business, but a large number of this error indicates that the read-write conflict is severe in your business.

- 7.2.2: `"write conflict"`.

    This is the write-write conflict in optimistic transactions. If multiple transactions modify the same key, only one transaction succeed and other transactions automatically obtain the timestamp again and retry the operation, with no impact on the business.

    If the conflict is severe, it might cause transaction failure after multiple retries. In this case, it is recommended to use the pessimistic lock.

- 7.2.3: `"TxnLockNotFound"`.

    This transaction commit is too slow, which is rolled back by other transactions after TTL (3 seconds for a small transaction by default). This transaction will automatically retry, so the business is usually not affected.

- 7.2.4: `"PessimisticLockNotFound"`. 

    Similar to `"TxnLockNotFound"`. The pessimistic transaction commit is too slow and thus rolled back by other transactions.

- 7.2.5: `"stale_epoch"`.

    The request epoch is outdated, so TiDB re-sends the request after updating the routing. The business is not affected. Epoch changes when Region has a split/merge operation or a replica is migrated.

- 7.2.6: `"peer is not leader"`.

    The request is sent to a replica that is not Leader. If the error response indicates which replica is the latest Leader, TiDB updates the local routing according the error and sends a new request to the latest Leader. Usually, the business is not affected.

    In v3.0 and later versions, TiDB tries other peers if the request to the previous Leader fails, which might lead to frequent `"peer is not leader"` in TiKV log. You can check the `"switch region peer to next due to send request fail"` log of the corresponding Region in TiDB to determine the root cause of the sending failure. For details, refer to 7.1.4.

    This error might also be returned if a Region has no Leader due to other reasons. For details, see 4.4.

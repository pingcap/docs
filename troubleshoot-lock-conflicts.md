---
title: TiDB Lock Conflict Handling
summary: How to analyze lock conflicts and solutions for that.
category: troubleshoot
---

# TiDB Lock Conflict Handling
 
TiDB can support complete distributed transactions. As of version of v3.0, TiDB provides optimistic transaction mode and pessimistic transaction mode. This document introduces how to troubleshooting and resolve when TiDB has usually lock conflict.

## Optimistic Transaction Mode

In the transaction of TiDB which has two-phase commit (2PC) that included the Prewrite phase and the Commit phase. The procedure is as follows:

![two-phase of optimistic transaction mode](/media/troubleshooting-lock-pic-01.png)
 
More than details information about Percolator and  TiDB’s algorithm of transaction, see them in [Google's Percolator](https://ai.google/research/pubs/pub36726)。

### Prewrite Pharse
 
As a 2PC of the Prewrite phase, TiDB will add primary lock and secondary lock to target keys. At the too much add locks request from clients, TiDB will feedback such as write conflict or the key has been locked error to the TiDB log and client. There are some details errors and treatment suggestion below a part of introduced.
 
#### Read-write Conflict
 
As TiDB Server receives a read data request from a client, that will get unique of a timestamp is start_ts at the physical time. When the transaction is waiting for reading data of the start_ts that is later than the key of the commit_ts version.  Because the latest transaction knows which is add a lock of the other transactions on this key,  but it doesn't know which is a phase of this transaction between the Prewrite phase and the Commit phase.The procedure is as follows:

![read-write conflict](/media/troubleshooting-lock-pic-04.png)

If Txn0 of a transaction has been completed for the Prewrite Phase to the target key, and then which is the status of the Commit Phase right now. At the same time, the Txn1 is reading to the same target key. Txn1 needs to read start_ts which is later than the commit_ts of the latest version of the target key. When the Txn1’s  start_ts is later than the Txn0's lock_ts, the Txn1 must be waiting for the target key 's lock has been cleanup, but it hasn’t done. As a result, The Txn1 can’t confirm the Txn0 has been committed or not. That scene is a read-write conflict between the Txn1 and the Txn0.

You can  use two way for analyses to confirm read-write conflict in the TiDB:

1.  Metrics and Logs on the TiDB

* Monitoring data through TiDB Server

The panel of `KV Errors` in the TiDB dashboard has two monitored metrics are `Lock Resolve OPS` and `KV Backoff OPS` which can check read-write conflict in the transactions. If too many read-write conflicts in the current situation, the monitoring value both of `not_expired `and `resolve` in the `Lock Resolve OPS` plane which have an obvious upward trend. The `not_expired` means that before the one of the transaction's lock hasn't timeout. The `resolve` metric means that the other transaction will try to resolve lock operation. The other monitoring value of ` txnLockFast` in the `KV Backoff OPS` plane will have the same upward trend which represents read-write conflict peer of operation.

![KV-backoff-txnLockFast-optimistic](/media/troubleshooting-lock-pic-09.png)
![KV-Errors-resolve-optimistic](/media/troubleshooting-lock-pic-08.png)

* Through TiDB Server logs

If among transactions is read-write conflict, the tidb log has below message: 

      ```log
       [INFO] [coprocessor.go:743] ["[TIME_COP_PROCESS] resp_time:406.038899ms txnStartTS:416643508703592451 region_id:8297 store_addr:10.8.1.208:20160 backoff_ms:255 backoff_types:[txnLockFast,txnLockFast] kv_process_ms:333 scan_total_write:0 scan_processed_write:0 scan_total_data:0 scan_processed_data:0 scan_total_lock:0 scan_processed_lock:0"]
      ```


       * txnStartTS: The transaction is reading request which start timestamp is start_ts, for example, the start_ts is 416643508703592451
       * txnStartTS: If read-write conflict has happened, when the current transaction of reading request will try to backoff. TxnLockFast is one of the backoff types.
       * backoff_ms: This value is the time that the read request transaction attempts to backoff, and the time unit is milliseconds. The message is 255 milliseconds to try to backoff.
       * region_id: Region ID corresponding to the target key of the read request.

1. Logs on the TiKV

If among transactions is read-write conflict, the tikv log has below message: 

   ```log
   [ERROR] [endpoint.rs:454] [error-response] [err=""locked primary_lock:7480000000000004D35F6980000000000000010380000000004C788E0380000000004C0748 lock_version: 411402933858205712 key: 7480000000000004D35F7280000000004C0748 lock_ttl: 3008 txn_size: 1""]
   ```

When the read-write conflict in the TiDB, the read request to target key which has been blocked by the other transaction. These locks include the optimistic transaction mode is uncommit and the pessimistic transaction mode after uncommitted prewrite phase.

   * primary_lock：This value represents the target key is locked by the primary lock.
   * lock_version：This value is the target key is locked by a version of the transaction's start_ts.
   * key：The target key of information.
   * lock_ttl: The lock’s TTL (Time To Live)
   * txn_size：The region of keys counts at which locks in the transaction.

Treatment suggestions:

* If read-write conflict in the TiDB, TiDB Server will trigger an automatic backoff and retry. As in the above example, the Txn1 will perform a backoff and retry, the first time will retry to execute after 100 ms, the longest retry for 3000 ms, the total retry maximum time is 20000 ms.

* You can use the subcommand [decoder](/tidb-control.md#decoder-subcommand) of TiDB Control to view the table id and rowid of the row corresponding to the specified key:

   ```sh
   ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
  
   table_id: -9223372036854775780
   row_id: -9223372036854775558
   ```

#### KeyIsLocked Error

If the 2PC transaction status of the commit phase. And status is the prewrite phase right now. The first step is to check the write-write conflict, and then check whether the target key has been locked by other transactions. The TiKV server will output a log about "KeyIsLocked". At present, the error message is not printed in the logs of TiDB and TiKV. As with read-write conflicts, when "KeyIsLocked" occurs, the background will automatically perform backoff and retry again.

You can check "KeyIsLocked" error in the TiDB monitoring on Grafana:

The panel of "KV Errors" in the TiDB dashboard has two monitored metrics are "Lock Resolve OPS" and "KV Backoff OPS" which can check write-write conflict in the transaction. If too many write-write conflicts in the current situation, the "resolve" metric means that the other transaction will try to resolve lock operation. And the "txnLock" monitoring value in the "KV Backoff OPS" plane will have the same upward trend, indicating the number of write-write conflicts per second of the operation.

![KV-backoff-txnLockFast-optimistic-01](/media/troubleshooting-lock-pic-07.png)
![KV-Errors-resolve-optimistic-01](/media/troubleshooting-lock-pic-08.png)

Treatment suggestions:

* We don’t need to more take care of less number of operation "txnLock" in the `KV Backoff OPS`. Because the background process will try to backoff the transaction for the commit phase. the first time will retry after 200 ms,  the total retry maximum time is 3000 ms.
* If there are too many “txnLock” operation records in the “KV Backooff OPS”, we recommend analyzing to write conflicts at the application level.
* If this application is a write-write conflict scenario, it is strongly recommended to use the pessimistic transaction mode.

### Commit Phase

When the transaction states of the prewrite phase which has been completed. The client will be obtained commit_ts, and then the transaction is going to the next phase of 2PC. 

#### The error of "LockNotFound"

The error log of "TxnLockNotFound" means that transaction commit time is longer than TTL  time. and then when the transaction is going to commit, its lock has been rollbacked by other transactions. If the TiDB server enables transaction commit retry, this transaction is re-executed according to [tidb_retry_limit](/tidb-specific-system-variables.md). But take care of the difference between explicit and implicit transactions.

If you find a "LockNotFound" error, there are two ways to analyze and deal with the suggestions:

1.Through TiDB Server logs

If the metric has "TxnLockNotFound" error, the log of TiDB Server is outputting theses message:

   ```log
   [WARN] [session.go:446] ["commit failed"] [conn=149370] ["finished txn"="Txn{state=invalid}"] [error="[kv:6]Error: KV error safe to retry tikv restarts txn: Txn(Mvcc(TxnLockNotFound{ start_ts: 412720515987275779, commit_ts: 412720519984971777, key: [116, 128, 0, 0, 0, 0, 1, 111, 16, 95, 114, 128, 0, 0, 0, 0, 0, 0, 2] })) [try again later]"]
   ```

* start_ts: The transaction’s start_ts which its lock has been rollbacked by other transactions that are outputting error  `TxnLockNotFound`, such as 412720515987275779 is start_ts.
* commit_ts: The commit_ts is the same as start_ts’s transaction, such as the number is 412720519984971777 is commit_ts.

2.Through TiKV Server logs

If the metric has `TxnLockNotFound` error, the log of TiKV Server is outputting theses message:

   ```log
   Error: KV error safe to retry restarts txn: Txn(Mvcc(TxnLockNotFound)) [ERROR [Kv.rs:708] ["KvService::batch_raft send response fail"] [err=RemoteStoped]
   ```
 
Treatment suggestions:

 * By checking the time interval between start_ts and commit_ts, you can confirm whether the replacement TTL time is exceeded.

   checking the time interval use the PD control tool. 

  ```shell
   ./pd-ctl tso [start_ts]
   ./pd-ctl tso [commit_ts]
   ```

## Pessimistic Transaction Mode

Before the version of v3.0.8, The TiDB default transaction mode is Optimistic Transaction. If there has transaction conflict, the latest transaction will commit failed. So the application needs to supporting transactions retry to execute. The Pessimistic Transaction Mode can resolve this question, and the application doesn’t need to modify any logic for the workaround.

The commit phase of the pessimistic transaction mode and the optimistic transaction mode in TiDB is the same logic, and both commits are the 2PC mode. The important innovation of pessimistic transactions is DML.

![TiDB pessimistic transaction commit logic](/media/troubleshooting-lock-pic-05.png)
 
The pessimistic transaction adds ` Acquire Pessimistic Lock ` phase before 2PC, which its logic look at below introduction:

1. (same as the optimistic transaction mode) Receive the request from the client, the current timestamp is this transaction’s start_ts.
2. When the TiDB Server receives an update data request from the client, TiDB Server initiates a pessimistic lock request to TiKV Server, which is persisted to TiKV Server.
3. (same as the optimistic transaction mode) When the client executes commit request, TiDB starts to perform the 2PC mode similar to the optimistic transaction mode. 

![Pessimistic transactions in TiDB](/media/troubleshooting-lock-pic-06.png)

Relevant details will not be repeated in this section, you can see [The Pessimistic transaction mode](/pessimistic-transaction.md)

### Prewrite Phase

At the transaction pessimistic mode, the commit phase always two-phase commit(2PC). Therefore, the read-write conflict also exists as the optimistic transaction mode.

#### read-write conflict

See the above method for a detailed introduction in the optimistic transaction mode.

### Commit Phase

The error of “TxnLockNotFound” 

In the pessimistic transaction mode, there will be no `TxnLockNotFound` error. However, the pessimistic lock will automatically update the TTL of the transaction through `txnheartbeat` to ensure that the second transaction will not clear the lock of the first transaction.

### Other errors about lock

In a scenario where the transaction conflict is very serious, or when a write conflict occurs. The optimistic transaction will be terminated directly, but the pessimistic transaction will retry the statement with the latest data from storage until there is no write conflict. 
Because TiDB's lock operation is a write operation, and the operation process is to read first and then write, there is two RPC requests time. If a write conflict occurs in the middle of transactions, it will try again to lock the target keys, the operation of trying it which will print the TiDB log without special attention. The number of retries is determined by [pessimistic-txn.max-retry-count](/tidb-configuration-file.md#max-retry-count) .

Check the error by viewing the TiDB log:

In the pessimistic transaction mode, if a write conflict occurs and the number of retries reaches the upper limit, an error message containing the following keywords will appear in the TiDB log. as follows:

```log
err="pessimistic lock retry limit reached"
```

Treatment suggestions:

* If the above error occurs frequently, it is recommended to adjust it from an application level.

#### Lock wait timeout exceeded
 
In the pessimistic transaction mode, there will be waiting for locks between transactions. The timeout for wait locks is defined by the [innodb_lock_wait_timeout](/pessimistic-transaction.md/###behavior) parameter of TiDB. This is the maximum allowable wait lock time at the SQL statement level, which is the expectation of a SQL statement Locking, but the lock has never been acquired. After this time, TiDB will not try to lock again and will return the corresponding error message to the client.

You can view the error information by the TiDB log:

When a wait lock timeout occurs, the following error message will be returned to the client: 

```log
ERROR 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
```
 
Treatment suggestions:

* If the number of reported errors is very frequent, it is recommended to adjust from the perspective of application logic.

#### TTL manager has timed out
 
In addition to the transaction executes time can not exceed the GC time limit, the TTL time of pessimistic transactions has an upper limit, the default value is 10 minutes. Therefore, a pessimistic transaction with an execution time of more than 10 minutes will fail to commit. This timeout threshold is controlled by the TiDB parameter.

You can view the error information by the TiDB log:

```log
TTL manager has timed out, pessimistic locks may expire, please commit or rollback this transaction
```

Treatment suggestions: 

* When encountering this error, it is recommended to confirm whether the application logic can be optimized. For example, large transactions may trigger TiDB's transaction size limit, which can be split into multiple small transactions. Or adjust the TiDB transaction size limit [large transaction](/tidb-configuration-file.md#txn-total-size-limit),
* It is recommended to adjust the relevant parameters appropriately to meet the application transaction logic.

#### Deadlock found when trying to get lock
 
Due to resource competition between two or more transactions, a deadlock will occur. If you do not handle it manually, transactions that block each other cannot be executed successfully and will wait for each other. So you need to manually terminate one of the transactions to resume other transaction requests.

In a scenario where a pessimistic transaction has a deadlock, one of the transactions must be terminated to unlock the deadlock. The client will return the same Error 1213 error as MySQL, for example

```log
[err="[executor:1213]Deadlock found when trying to get lock; try restarting transaction"]
```
 
Treatment suggestions: 

The application needs to adjust transaction request logic when there too many more deadlocks. 

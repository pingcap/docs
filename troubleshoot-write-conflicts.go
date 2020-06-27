---
title: TiDB Write Conflict In Optimistic Transaction Troubleshooting
summary: Learn about common errors and solutions of write conflict in optimistic transaction.
category: how-to
---

# TiDB Write Conflict In Optimistic Transaction Troubleshooting

This article is an introduction to the reason and solutions of write conflict in optimistic transaction.

Before TiDB v3.0.8, optimistic transaction is the defalut transaction model in TiDB. The transaction won't check the conflict during the execution. The transaction will check the conflict in the 2PC committing stage. If the write conflict is exists when committing transaction, the transaction will be auto-retry in TiDB internal when the TiDB has enabled the auto-retry and the retry count has not exceeded the limie. Then, TiDB will return the result of transaction to the client. Therefore, the write latency of TiDB cluster will be higher when there are a lot of write conflict exists.

## The reason of write conflict

TiDB use [Percolator](https://www.usenix.org/legacy/event/osdi10/tech/full_papers/Peng.pdf) transaction model to implement the transaction. And `percolator` is generally an implementation of 2PC. Please refer to [optimistic transaction document](/optimistic-transaction.md) for the specific 2PC process.

After the client send a `COMMIT` request to TiDB, TiDB starts the 2PC process:

1. TiDB chooses one key from all keys as the primary key of the transaction.
2. TiDB sends `prewrite` requests to the TiKV regions which contain the keys of the transaction.
3. After all `prewrite` requests return successfully, process to the next step.
4. TiDB gets the `commit_ts` from PD.
5. TiDB sends `commit` request to the TiKV region which contain the primary key of the transaction. When TiKV executes `commit` request, TiKV checks the validity of the data and clear the lock left in `prewrite` request.
6. After the `commit` request returns successfully, TiDB return success to the client.

The write conflict occurs in the `prewrite` stage. When the transaction found a new version of the key (key.commit_ts > txn.start_ts), that's write conflict.

## How to check the write conflict exists in the cluster?

You can check the following monitoring metrics under **KV Errors** in the **TiDB Grafana** panel:

* **KV Backoff OPS** indicates the count of error that return by TiKV.

    ![kv-backoff-ops](/media/troubleshooting-write-conflict-kv-backoff-ops.png)

    `txnlock` metric indicates the write conflict. `txnLockFast` metric indicates the read-write conflict.

* **Lock Resolve OPS** indicates the count of resolve locks which cause by transaction conflict:

    ![lock-resolve-ops](/media/troubleshooting-write-conflict-lock-resolve-ops.png)

    `not_expired` means the TTL of lock was not expired, Then the conflict transaction can't resolve locks until the TTL was expired.
    `wait_expire` means the transaction needs to wait the lock expired.
    `expired` means the TTL of lock was expired, Then the conflict transaction can resolve this lock now.

* **KV Retry Duration** indicates the duration of re-sends the KV request:

     ![kv-retry-duration](/media/troubleshooting-write-conflict-kv-retry-duration.png)

You can also use `[kv:9007]Write conflict` as the key word to search in the TiDB log. The key word also indicates the write conflict exists in the cluster.

## How to resolve the write-conflict?

If there were many write conflict in the cluster, you can find out the write conflict key and the reason, then try to change the application logic to avoid write conflict. When the write conflict exists, you can see the similar log in TiDB log file:

```log
[2020/05/12 15:17:01.568 +08:00] [WARN] [session.go:446] ["commit failed"] [conn=3] ["finished txn"="Txn{state=invalid}"] [error="[kv:9007]Write conflict, txnStartTS=416617006551793665, conflictStartTS=416617018650001409, conflictCommitTS=416617023093080065, key={tableID=47, indexID=1, indexValues={string, }} primary={tableID=47, indexID=1, indexValues={string, }} [try again later]"]
```

The explaination of upper log as below:

* `[kv:9007]Write conflict`: indicates the write conflict.
* `txnStartTS=416617006551793665`：indicates the `start_ts` of the current transaction. You can use `pd-ctl` tool to convert the `start_ts` to physical time.
* `conflictStartTS=416617018650001409`: indicates the `start_ts` of the write conflict transaction.
* `conflictCommitTS=416617023093080065`: indicates the `commit_ts` of the write conflict transaction.
* `key={tableID=47, indexID=1, indexValues={string, }}`：indicates the write conflict key. `tableID` indicates the ID of the write conflict table. `indexID` indicates the ID of write conflict index. If the write conflict key is a record key, the log will print `handle=x`, indicates which record(row) was conflict. `indexValues` indicates the conflict index value.
* `primary={tableID=47, indexID=1, indexValues={string, }}`: indicates the primary key information of the current transaction.

You can use `pd-ctl` tool to convert the ts, such as below:

{{< copyable "" >}}

```shell
./pd-ctl -u https://127.0.0.1:2379 tso {TIMESTAMP}
```

You can use `tableID` to look up the related table:

{{< copyable "" >}}

```shell
curl http://{TiDBIP}:10080/db-table/{tableID}
```

You can use `indexID` and table name to look up the related index:

{{< copyable "sql" >}}

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEXES WHERE TABLE_SCHEMA='{table_name}' AND TABLE_NAME='{table_name}' AND INDEX_ID={indexID};
```

In addition, in TiDB v3.0.8 and later versions, the defalut transaction model was changed to pessimistic transaction. Pessimistic transaction model can avoid write conflict during the transaction prewrite stage, so no need to modify the application. In the pessimistic transaction mode, each DML statement will write a pessimistic lock to the related keys during execution. The pessimistic lock is used to prevent other transactions from modifying the same key, thus ensuring that there will be no writing conflict in the `prewrite` stage of the transaction 2PC.

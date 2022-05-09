---
title: Transaction Error Handling
summary: Describes how to handle transaction error.
---

# Transaction Error Handling

This section introduce deadlock and transaction error handing.

## Deadlock

If the application encounters the following error, it indicates a deadlock issue:

```sql
ERROR 1213: Deadlock found when trying to get lock; try restarting transaction
```

A deadlock occurs when two or more transactions are waiting for each other to release the lock they already hold, or because the lock order is inconsistent, resulting in a loop waiting for the lock resources.

Here is an example of a deadlock using the table `books` in the [bookshop](/develop/bookshop-schema-design.md) database:

First insert 2 rows data into the table `books`:

```sql
INSERT INTO books (id, title, stock, published_at) VALUES (1, 'book-1', 10, now()), (2, 'book-2', 10, now());
```

In TiDB pessimistic transaction mode, if two clients execute the following statements respectively, a deadlock will be encountered:

| Client-A                                                      | Client-B                                                            |
| --------------------------------------------------------------| --------------------------------------------------------------------|
| BEGIN;                                                        |                                                                     |
|                                                               | BEGIN;                                                              |
| UPDATE books SET stock=stock-1 WHERE id=1;                    |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=2;                          |
| UPDATE books SET stock=stock-1 WHERE id=2; -- will be blocked |                                                                     |
|                                                               | UPDATE books SET stock=stock-1 WHERE id=1; -- arise deadlock error  |

After client-B encounters deadlock error, TiDB will automatically `ROLLBACK` the transaction in client-B, and then update `id=2` in client-A will be executed successfully.

### Solution 1：Avoid Deadlock

For getting better performance, you should try to avoid deadlock at the application level by adjusting the business logic or schema design. In the example above, if client-B also uses the same update order as client-A, that is, they update `books` with `id=1` first, and then `update` books with `id=2`, so that deadlocks can be avoided:

| 客户端-A                                                    | 客户端-B                                                         |
| ---------------------------------------------------------- | ----------------------------------------------------------------|
| BEGIN;                                                     |                                                                 |
|                                                            | BEGIN;                                                          |
| UPDATE books SET stock=stock-1 WHERE id=1;                 |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=1;  -- will be blocked  |
| UPDATE books SET stock=stock-1 WHERE id=2;                 |                                                                 |
| COMMIT;                                                    |                                                                 |
|                                                            | UPDATE books SET stock=stock-1 WHERE id=2;                      |
|                                                            | COMMIT;                                                         |

Or update 2 books with 1 SQL, which can also avoid deadlock and execute more efficiently:

```sql
UPDATE books SET stock=stock-1 WHERE id IN (1, 2);
```

### Solution 2: Reduce transaction granularity

If you only update 1 book in each transaction, you can also avoid deadlock. However, the trade-off is that too small transaction granularity may affect performance.

### Solution 3: Use Optimistic Transactions

In TiDB optimistic transaction model, there is no deadlock problem, but the application needs to add the optimistic transaction retry logic after failure. For details, see [Application Retry and Error Handling](#Application-Retry-And-Error-Handling).

### Solution 4: Retry

As suggested in the error message, just add retry logic in the application code. For details, see [Application Retry and Error Handling](#Application-Retry-And-Error-Handling).

## Application Retry And Error Handling

Although TiDB is as compatible as possible with MySQL, the nature of its distributed system leads to certain differences, one of them is the transaction model.

The Adapters and ORMs that developers use to connect with databases are tailored to traditional databases such as MySQL and Oracle, where transaction commit rarely fail at the default isolation level, so no retry mechanism is required. For these clients, when a transaction commit fails, they abort due to an error, as this is presented as a rare exception in these databases.

Different from traditional databases such as MySQL, in TiDB optimistic transaction model, if you want to avoid commit failure, you need to add mechanism to handle related exceptions in your application code.

The following Python pseudocode shows how to implement application-level retries. It does not require your driver or ORM to implement advanced retry logic, so it can be used in any programming language or environment. Your retry logic must follow the following points:

- Throws an error if the number of failed retries reaches the `max_retries` limit.
- Use `try ... catch ...` to catch SQL execution exception，Retry on failure when encountering the following errors, and rollback when encountering other errors. More error code detail, see [Error Codes and Troubleshooting](https://docs.pingcap.com/tidb/stable/error-codes).
  - `Error 8002: can not retry select for update statement`: SELECT FOR UPDATE write conflict error
  - `Error 8022: Error: KV error safe to retry`: transaction commit failed error.
  - `Error 8028: Information schema is changed during the execution of the statement`: Table schema has been changed by DDL operation, resulting in an error in the transaction commit.
  - `Error 9007: Write conflict`: Write conflict error, cause by multiple transactions modify the same row of data when the optimistic transaction mode is used.
- COMMIT the transaction at the end of the try block.

```python
while True:
    n++
    if n == max_retries:
        raise("did not succeed within #{n} retries")
    try:
        connection.execute("your sql statement here")
        connection.exec('COMMIT')
        break
    catch error:
        if (error.code != "9007" && error.code != "8028" && error.code != "8002" && error.code != "8022"):
            raise error
        else:
            connnection.exec('ROLLBACK');
            
            # Capture the error types that require application-side retry,
            # wait for a short period of time,
            # and exponentially increase the wait time for each transaction failure
            sleep_ms = int(((1.5 ** n) + rand) * 100)
            sleep(sleep_ms) # make sure your sleep() takes milliseconds
```

> Note:
>
> If you frequently encounter `Error 9007: Write conflict` error, you may need to check your schema design and the data access patterns of your workload to find the source of conflicts and avoid conflicts by design.
> About how to troubleshoot and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts).

## See Also

- [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)
- [Troubleshoot Write Conflicts in Optimistic Transactions](https://docs.pingcap.com/tidb/stable/troubleshoot-write-conflicts)
---
title: DM Safe Mode
summary: Introduces the DM safe mode, its purpose, working principles and how to use it.
---

# DM Safe Mode

Safe mode is an operation mode for DM to perform incremental replication. In safe mode, when the DM's incremental replication component replicates binlog events, it forcibly rewrites all the `INSERT` and `UPDATE` statements before executing them in the downstream.

In safe mode, the same binlog event can be replicated repeatedly to the downstream and the result is guaranteed to be idempotent. Thus, the incremental replication is ensured to be *safe*.

After DM resumes a data replication task from the checkpoint, it might repeatedly execute some binlog events, which leads to the following issues:

1. During incremental replication, the operation of executing DML and the operation of writing checkpoint are not silmultaneous. The operation of writing checkpoint and writing data into the downstream database are not atomic. Therefore, **when DM exits abnormally, checkpoint might only record to a recovery point before the exit moment**.
2. When DM restarts a task and resumes incremental replication from the checkpoint, some data between the checkpoint and the exit moment might already be processed before the abnormal exit. This causes **some SQL statements to be repeatedly executed**.
3. If the `INSERT` statement is executed for more than once, the primary key or the unique index might encounter conflict and cause the replication to fail. If the `UPDATE` statement is executed for more than once, the fitler condition might not be able to locate the updated records.

In safe mode, DM can resolve the above issues by rewriting SQL statements.

## Working principle

Safe mode guarantees the idempotency of binlog events by rewriting SQL statements. Specifically, the following SQL statements are rewritten:

* `INSERT` is rewritten to `REPLACE`.
* `UPDATE` is analyzed to obtain the value of the primary key or the unique index of the row updated. `UPDATE` is then rewritten to `DELETE` + `REPLACE` in the following two steps: DM deletes the old record using the primary key or unique index, and insert the new record using the `REPLACE` statement.

`REPLACE` is a MySQL-specific data insertion syntax. When you insert data with `REPLACE`, if the new data and existing data has a primary key or unique constraint conflict, MySQL deletes all the conflicting records and executes the insert operation, which is equivalent to "force insert". For details, see [`REPLACE` statement](https://dev.mysql.com/doc/refman/8.0/en/replace.html) in MySQL documentation.

For example, a `dummydb.dummytbl` table has a primary key `id`. Execute the following SQL statements repeatedly on this table:

```sql
INSERT INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
UPDATE dummydb.dummytbl SET int_value = 888999 WHERE int_value = 999；   -- If there is no other record with int_value = 999
UPDATE dummydb.dummytbl SET id = 999 WHERE id = 888；    -- Update the primary key
```

With safe mode enabled, when the preceding SQL statement is executed again in the downstream, it is rewritten as follows:

```sql
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 123;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (123, 888999, 'abc');
DELETE FROM dummydb.dummytbl WHERE id = 888;
REPLACE INTO dummydb.dummytbl (id, int_value, str_value) VALUES (999, 888888, 'abc888');
```

In the preceding statement, `UPDATE` is rewritten as `DELETE` + `REPLACE`, rather than `DELETE` + `INSERT`. If `INSERT` is used here, when you insert a duplicate record with `id = 999`, the database reports a primary key conflict. This is why `REPLACE` is used instead. The new record will replace the existing record.

By rewriting SQL statements, before duplicate insert or update operations, DM uses the new row data to overwrite the existing row data. This guarantees that insert and update operations can be executed repeatedly.

## Enable safe mode

### Automatically enable

When DM resumes an incremental replication task from the checkpoint (DM worker restart or network reconnection), DM automatically enables safe mode for a period.

Whether to enable safe mode is related to the `safemode_exit_point` in the checkpoint. When an incremental replication task is paused abnormally, DM tries to replicate all DML statements in the memory to the downstream and records the latest binlog position in the memory pulled from the upstream as `safemode_exit_point`. The `safemode_exit_point` is saved in the last checkpoint before the abnormal pause.

When DM resumes an incremental replication task from the checkpoint, it determines whether to enable safe mode based on the following logic:

- If the checkpoint contains `safemode_exit_point`, the incremental replication task is paused abnormally. When DM resumes the task, if DM detects that the binlog position of the checkpoint to be resumed is earlier than `safemode_exit_point`, it means that the binlog events between the checkpoint and the `safemode_exit_point` might have been processed in the downstream. When the task is resumed, some binlog events might be executed repeatedly. Therefore, DM determines that safe mode should be enabled for these binlog positions. After the binlog position exceeds the `safemode_exit_point`, if safe mode is not manually enabled, DM automatically disables safe mode.

- If the checkpoint does not contain `safemode_exit_point`, there are two cases:

    1. This is a new task, or this task is paused as expected.
    2. This task is paused abnormally and it fails to record `safemode_exit_point`, or the DM process exits abnormally.

    In the second case, DM does not know which binlog events after the checkpoint are executed in the downstream. To be safe, if DM does not find `safemode_exit_point` in the checkpoint, it automatically enables safe mode between the preceding two checkpoints to ensure that repeatedly executed binlog events do not cause any problems. The default interval between two checkpoints is 30 seconds, which means when a normal incremental replication task starts, safe mode is enforced for the first 60 seconds (2 * 30 seconds).

    You can change the checkpoint interval by setting the `checkpoint-flush-interval` item in syncer configuration and thereby adjust the safe mode period at the beginning of the incremental replication task. It is not recommended to adjust this setting. If necessary, you can [manually enable safe mode](#manually-enable).

### Manually enable

You can control whether to enable safe mode throughout by setting the `safe-mode` item in the syncer configuration. `safe-mode` is a bool type parameter and `false` by default. If it is set to `true`, DM enables safe mode for the whole incremental replication process. The following is a task configuration example with safe mode enabled:

```
syncers:                              # The running configurations of the sync processing unit.
  global:                            # Configuration name.
    # Other configuration items are ignored.
    safe-mode: true                  # Enables safe mode for the whole incremental replication process.
    # Other configuration items are ignored.
# ----------- Instance configuration -----------
mysql-instances:
  -
    source-id: "mysql-replica-01"
    # Other configuration items are ignored.
    syncer-config-name: "global"            # Name of the syncers configuration.
```

## Notes for safe mode

If you want to enable safe mode throughout for safety reasons, you must be aware of the following:

- **Safe mode has extra overhead for incremental replication.** Frequent `DELETE` + `REPLACE` operations result in frequent changes to primary keys or unique indexes, which creates a greater performance overhead than a simple `UPDATE` statement.
- **Safe mode forces the replacement of records with the same primary key, which might result in data loss in the downstream.** When you merge and migrate shards from the upstream to the downstream, incorrect configuration might lead to a large number of primary key or unique key conflicts. If safe mode is enabled, the downstream might lose lots of data. The task might not show any exception, resulting in severe data inconsistency.
- **Safe mode relies on the primary key or unique index to detect conflicts.** if the downstream table has no primary key or unique index, DM cannot use `REPLACE` to replace and insert records. In such case, even if DM rewrites `INSERT` to `REPLACE`, duplicate records are still inserted into the downstream.

In summary, if the upstream database has data with duplicate primary keys, and the application can tolerate loss of duplicate records and performance overhead, you can enable safe mode to ignore data duplication.

---
title: Performance Tuning Best Practices
---

# Performance Tuning Best Practices

This section introduce some best practices for using TiDB databases.

## DML Best Practices

### Use multi-row statement

When you need to modify multiple rows of table, it is recommended to use multi-row statement:

```sql
INSERT INTO t VALUES (1, 'a'), (2, 'b'), (3, 'c');

DELETE FROM t WHERE id IN (1, 2, 3);
```

Not recommended to use multiple single-row statements:

```sql
INSERT INTO t VALUES (1, 'a');
INSERT INTO t VALUES (2, 'b');
INSERT INTO t VALUES (3, 'c');

DELETE FROM t WHERE id = 1;
DELETE FROM t WHERE id = 2;
DELETE FROM t WHERE id = 3;
```

### Use PREPARE

When you need to execute a SQL statement multiple times, it is recommended to use the `PREPARE` statement to avoid the overhead of repeatedly parse the SQL syntax.

<SimpleTab>
<div label="Golang">

```go
func BatchInsert(db *sql.DB) error {
	stmt, err := db.Prepare("INSERT INTO t (id) VALUES (?), (?), (?), (?), (?)")
	if err != nil {
		return err
	}
	for i := 0; i < 1000; i += 5 {
		values := []interface{}{i, i + 1, i + 2, i + 3, i + 4}
		_, err = stmt.Exec(values...)
		if err != nil {
			return err
		}
	}
	return nil
}
```

</div>

<div label="Java">

```java
public void batchInsert(Connection connection) throws SQLException {
	PreparedStatement statement = connection.prepareStatement(
			"INSERT INTO `t` (`id`) VALUES (?), (?), (?), (?), (?)");
	for (int i = 0; i < 1000; i ++) {
		statement.setInt(i % 5 + 1, i);

		if (i % 5 == 4) {
			statement.executeUpdate();
		}
	}
}
```

</div>
</SimpleTab>

Do not execute the `PREPARE` statement repeatedly. Otherwise, the execution efficiency cannot be improved.

### Only query the columns you need

Don't always use `SELECT *` to return all columns data if you don't have to; the following query is inefficient

```sql
SELECT * FROM books WHERE title = 'Marian Yost';
```

You should only query the columns you need, for example:

```sql
SELECT title, price FROM books WHERE title = 'Marian Yost';
```

### Use Batch Delete

When a large amount of data needs to be deleted, it is recommended to use [Batch Delete](/delete-data.md#bulk-delete)

### Use Batch Update

When a large amount of data needs to be update, it is recommended to use [Batch Update](/delete-data.md#bulk-delete)

### Use TRUNCATE instead of DELETE full table data

When you need to delete all data from a table, it is recommended to use the `TRUNCATE` statement:

```sql
TRUNCATE TABLE t;
```

Not recommended to use `DELETE` full table data:

```sql
DELETE FROM t;
```

## DDL Best Practices

### Primary Key Best Practices

See [Primary Key Best Practices](/create-table.md#best-practices-for-select-primary-key)

### Index Best Practices

See [Index Best Practice](/index-best-practice.md)

### Add Index Best Practices

TiDB supports the online `ADD INDEX` operation and does not block data reads and writes in the table. The speed of `ADD INDEX` can be adjusted by modify the following system variable:

* [tidb_ddl_reorg_worker_cnt](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_worker_cnt)
* [tidb_ddl_reorg_batch_size](https://docs.pingcap.com/tidb/stable/system-variables#tidb_ddl_reorg_batch_size)

To reduce the impact on online business, the default speed of `ADD INDEX` is conservative. When the target column of `ADD INDEX` only involves read load or is not directly related to online load, the above variable can be appropriately increased to speed up `ADD INDEX`:

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 16;
SET @@global.tidb_ddl_reorg_batch_size = 4096;
```

When the target column of `ADD INDEX` is updated frequently (including `UPDATE`, `INSERT` and `DELETE`), increase the above variable will cause more write conflicts, resulting in impact online business load; at the same time, `ADD INDEX` may take a long time to complete due to constant retries. In this case, it is recommended to reduce the above variable to avoid write conflicts with online load:

```sql
SET @@global.tidb_ddl_reorg_worker_cnt = 4;
SET @@global.tidb_ddl_reorg_batch_size = 128;
```

## Transaction Conflicts

About how to locate and resolve transaction conflicts, see [Troubleshoot Lock Conflicts](https://docs.pingcap.com/tidb/stable/troubleshoot-lock-conflicts)

## Best Practices for Developing Java Applications with TiDB

See [Best Practices for Developing Java Applications with TiDB](https://docs.pingcap.com/tidb/stable/java-app-best-practices)

### See Also

- [Highly Concurrent Write Best Practices](https://docs.pingcap.com/tidb/stable/high-concurrency-best-practices)

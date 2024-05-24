# SQL Statement Overview

TiDB uses SQL statements that aim to follow ISO/IEC SQL standards, with extensions for MySQL and TiDB-specific statements where necessary.

## Schema management / Data definition statements (DDL)

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER DATABASE`](/sql-statements/sql-statement-alter-database.md) | Modifies a database. |
| [`ALTER SEQUENCE`](/sql-statements/sql-statement-alter-sequence.md) | Modifies a sequence. |
| [`ALTER TABLE ... ADD COLUMN`](/sql-statements/sql-statement-add-column.md) | Adds a column to an existing table. |
| [`ALTER TABLE ... ADD INDEX`](/sql-statements/sql-statement-add-index.md) | Adds an index to an existing table. |
| [`ALTER TABLE ... ALTER INDEX`](/sql-statements/sql-statement-alter-index.md) | Changes an index definition. |
| [`ALTER TABLE ... CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md) | Changes a column definition. |
| [`ALTER TABLE ... COMPACT`](/sql-statements/sql-statement-alter-table-compact.md) | Compacts a table. |
| [`ALTER TABLE ... DROP COLUMN`](/sql-statements/sql-statement-drop-column.md) | Drops a column from a table. |
| [`ALTER TABLE ... MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md) | Modifies a column definition. |
| [`ALTER TABLE ... RENAME INDEX`](/sql-statements/sql-statement-rename-index.md) | Renames an index. |
| [`ALTER TABLE`](/sql-statements/sql-statement-alter-table.md) | Changes a table definition. |
| [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md) | Creates a new database. |
| [`CREATE INDEX`](/sql-statements/sql-statement-create-index.md) | Creates a new index on a table. |
| [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md) | Creates a new sequence object. |
| [`CREATE TABLE LIKE`](/sql-statements/sql-statement-create-table-like.md) | Copies the definition of an existing table, without copying any data. |
| [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) | Creates a new table. |
| [`CREATE VIEW`](/sql-statements/sql-statement-create-view.md) | Creates a new view. |
| [`DROP DATABASE`](/sql-statements/sql-statement-drop-database.md) | Drops an existing database. |
| [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md) | Drops an index from a table. |
| [`DROP SEQUENCE`](/sql-statements/sql-statement-drop-sequence.md) | Drops a sequence object. |
| [`DROP TABLE`](/sql-statements/sql-statement-drop-table.md) | Drops an existing table. |
| [`DROP VIEW`](/sql-statements/sql-statement-drop-view.md) | Drops an existing view. |
| [`RENAME TABLE`](/sql-statements/sql-statement-rename-table.md) | Renames a table. |
| [`SHOW COLUMNS FROM`](/sql-statements/sql-statement-show-columns-from.md) | Shows the columns from a table. |
| [`SHOW CREATE DATABASE`](/sql-statements/sql-statement-show-create-database.md) | Shows the CREATE statement for a database. |
| [`SHOW CREATE SEQUENCE`](/sql-statements/sql-statement-show-create-sequence.md) | Shows the CREATE statement for a sequence. |
| [`SHOW CREATE TABLE`](/sql-statements/sql-statement-show-create-table.md) | Shows the CREATE statement for a table. |
| [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) | Shows a list of databases that the current user has privileges to. |
| [`SHOW FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md) | Shows columns of a table. |
| [`SHOW INDEXES`](/sql-statements/sql-statement-show-indexes.md) | Shows indexes of a table. |
| [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md) | An alias to `SHOW DATABASES`, which shows a list of databases that the current user has privileges to. |
| [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) | Shows the next row ID for a table. |
| [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) | Shows the Region information of a table in TiDB. |
| [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md) | Shows various statistics about tables in TiDB. |
| [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md) | Shows tables in a database. |
| [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) | Truncates all data from a table. |

## Data manipulation statements (DML)

| SQL Statement | Description |
|---------------|-------------|
| [`BATCH`](/sql-statements/sql-statement-batch.md) | Splits a DML statement into multiple statements in TiDB for execution. |
| [`DELETE`](/sql-statements/sql-statement-delete.md) | Deletes rows from a table. |
| [`INSERT`](/sql-statements/sql-statement-insert.md) | Inserts new rows into a table. |
| [`REPLACE`](/sql-statements/sql-statement-replace.md) | Replaces existing rows or inserts new rows. |
| [`SELECT`](/sql-statements/sql-statement-select.md) | Reads data from a table. |
| [`TABLE`](/sql-statements/sql-statement-table.md) | Retrieves rows from a table. |
| [`UPDATE`](/sql-statements/sql-statement-update.md) | Updates existing rows in a table. |
| [`WITH`](/sql-statements/sql-statement-with.md) | Defines common table expressions. |

## Transaction statements

| SQL Statement | Description |
|---------------|-------------|
| [`BEGIN`](/sql-statements/sql-statement-begin.md) | Begins a new transaction. |
| [`COMMIT`](/sql-statements/sql-statement-commit.md) | Commits the current transaction. |
| [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) | Rolls back the current transaction. |
| [`SAVEPOINT`](/sql-statements/sql-statement-savepoint.md) | Sets a savepoint within a transaction. |
| [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) | Changes the current isolation level on a `GLOBAL` or `SESSION` basis. |
| [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) | Starts a new transaction. |

## Prepared statements

| SQL Statement | Description |
|---------------|-------------|
| [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md) | Deallocates a prepared statement, freeing associated resources. |
| [`EXECUTE`](/sql-statements/sql-statement-execute.md) | Executes a prepared statement with specific parameter values. |
| [`PREPARE`](/sql-statements/sql-statement-prepare.md) | Creates a prepared statement with placeholders. |

## Administrative statements

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | Cancels a DDL job. |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | Checks the integrity of a table or index. |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | Computes the checksum of a table. |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | Cleans up indexes from a table. |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | Pauses DDL operations. |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | Resumes DDL operations. |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | Shows DDL jobs or job queries. |
| [`ADMIN SHOW TELEMETRY`](/sql-statements/sql-statement-admin-show-telemetry.md) | Shows telemetry data. |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | Performs various administrative tasks. |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) |  Included for [MySQL compatibility](/mysql-compatibility.md). It has no effective usage in TiDB. |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | Modifies a system variable or user variable. |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | Set a character set and collation. |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | Splits a Region into smaller Regions. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | Cancels a DDL job. |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | Checks the integrity of a table or index. |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | Computes the checksum of a table. |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | Cleans up indexes from a table. |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | Pauses DDL operations. |
| [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md) | Recovers the consistency based on the redundant indexes. |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | Resumes DDL operations. |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | Shows DDL jobs or job queries. |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | Performs various administrative tasks. |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) |  Included for [MySQL compatibility](/mysql-compatibility.md). It has no effective usage in TiDB. |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | Modifies a system variable or user variable. |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | Set a character set and collation. |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | Splits a Region into smaller Regions. |

</CustomContent>

## Data import and export

| SQL Statement | Description |
|---------------|-------------|
| [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md) | Cancels an ongoing import job. |
| [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) | Imports data into a table via the [Physical Import Mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode) of TiDB Lightning. |
| [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) | Loads data into a table from Amazon S3 or Google Cloud Storage. |
| [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md) | Shows the status of an import job. |

## Backup & restore

| SQL Statement | Description |
|---------------|-------------|
| [`BACKUP`](/sql-statements/sql-statement-backup.md) | Perform a distributed backup of the TiDB cluster. |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) | Restores the cluster to a specific snapshot. |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | Restores a database and its data that are deleted by the `DROP` statement. |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) | Restore the tables and data dropped by the `DROP` or `TRUNCATE` operation. |
| [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md) | Recovers a deleted table and the data on it. |
| [`RESTORE`](/sql-statements/sql-statement-restore.md) | Restores a database from a backup. |
| [`SHOW BACKUPS`](/sql-statements/sql-statement-show-backups.md) | Shows backup tasks. |
| [`SHOW RESTORES`](/sql-statements/sql-statement-show-backups.md) | Shows restore tasks. |

## Placement policy

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) | Modifies a placement policy. |
| [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) | Modifies the range of a placement policy. |
| [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) | Creates a new placement policy. |
| [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) | Drops an existing placement policy. |
| [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) | Shows the `CREATE` statement for a placement policy. |
| [`SHOW PLACEMENT FOR`](/sql-statements/sql-statement-show-placement-for.md) | Shows placement rules for a specific table. |
| [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) | Shows available placement labels. |
| [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) | Shows placement rules. |

## Resource groups

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | Modifies a resource group. |
| [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) | Estimates and outputs the [Request Unit (RU)](/tidb-resource-control.md#what-is-request-unit-ru) capacity of the current cluster. |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | Creates a new resource group. |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | Drops a resource group. |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | Manage runaway query watch list. |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | Sets a resource group. |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | Shows the `CREATE` statement for a resource group. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | Modifies a resource group. |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | Creates a new resource group. |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | Drops a resource group. |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | Manage runaway query watch list. |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | Sets a resource group. |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | Shows the `CREATE` statement for a resource group. |

</CustomContent>

## Utility statements

| SQL Statement | Description |
|---------------|-------------|
| [`DESC`](/sql-statements/sql-statement-desc.md) | An alias to `DESCRIBE`, which shows the structure of a table. |
| [`DESCRIBE`](/sql-statements/sql-statement-describe.md) | Shows the structure of a table. |
| [`DO`](/sql-statements/sql-statement-do.md) | Executes an expression but does not return any results. |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md) | Shows the execution plan of a query. |
| [`TRACE`](/sql-statements/sql-statement-trace.md) | Provides detailed information about query execution. |
| [`USE`](/sql-statements/sql-statement-use.md) | Sets the current database. |

## Show statements

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) | Lists builtin functions. |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | Lists character sets. |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md) | Lists collations. |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md) | Shows errors from previously executed statements. |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md) | Included for [compatibility with MySQL](/mysql-compatibility.md). TiDB uses [Prometheus and Grafana](/tidb-monitoring-framework.md) for centralized metrics collection instead of `SHOW STATUS` for most metrics. |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md) | Shows system variables. |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) | Shows warnings and notes from previously executed statements. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) | Lists builtin functions. |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | Lists character sets. |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md) | Lists collations. |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md) | Shows errors from previously executed statements. |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md) | Included for [compatibility with MySQL](/mysql-compatibility.md). TiDB Cloud provides [Monitoring](/tidb-cloud/monitor-tidb-cluster.md) for centralized metrics collection instead of `SHOW STATUS` for most metrics. |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md) | Shows system variables. |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) | Shows warnings and notes from previously executed statements. |

</CustomContent>

## Instance management

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | Modifies an instance. |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) | Included for [compatibility with MySQL](/mysql-compatibility.md). TiDB uses [Prometheus and Grafana](/tidb-monitoring-framework.md) for centralized metrics collection instead of `SHOW STATUS` for most metrics. |
| [`KILL`](/sql-statements/sql-statement-kill.md) | Kills a connection in any TiDB instance in the current TiDB cluster. |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | Shows the configuration of various components of TiDB. |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | Shows available storage engines. |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | Shows installed plugins. |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | Shows the current sessions connected to the same TiDB server. |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) | Shows query profiles. Included for [compatibility with MySQL](/mysql-compatibility.md). Currently, it only returns an empty result. |
| [`SHUTDOWN`](/sql-statements/sql-statement-shutdown.md) | Stops the client-connected TiDB instance, not the entire TiDB cluster. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | Modifies an instance. |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) | Included for [compatibility with MySQL](/mysql-compatibility.md). TiDB Cloud provides [Monitoring](/tidb-cloud/monitor-tidb-cluster.md) for centralized metrics collection instead of `SHOW STATUS` for most metrics. |
| [`KILL`](/sql-statements/sql-statement-kill.md) | Kills a connection in any TiDB instance in the current TiDB cluster. |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | Shows available storage engines. |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | Shows the latest TSO in the cluster. |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | Shows installed plugins. |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | Shows the current sessions connected to the same TiDB server. |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) | Shows query profiles. Included for [compatibility with MySQL](/mysql-compatibility.md). Currently only returns an empty result. |

</CustomContent>

## Locking statements

| SQL Statement | Description |
|---------------|-------------|
| [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) | Locks statistics of tables or partitions. |
| [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | Locks tables for the current session. |
| [`UNLOCK STATS`](/sql-statements/sql-statement-unlock-stats.md) | Unlocks statistics of tables or partitions. |
| [`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | Unlocks tables. |

## Account management / Data Control Language

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) | Modifies a user. |
| [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md) | Creates a role. |
| [`CREATE USER`](/sql-statements/sql-statement-create-user.md) | Creates a new user. |
| [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md) | Drops an existing role. |
| [`DROP USER`](/sql-statements/sql-statement-drop-user.md) | Drops an existing user. |
| [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) | Reloads the in-memory copy of privileges from the privilege tables. |
| [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md) | Grants privileges. |
| [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md) | Grants a role. |
| [`RENAME USER`](/sql-statements/sql-statement-rename-user.md) | Renames an existing user. |
| [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md) | Revokes privileges. |
| [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md) | Revokes a role. |
| [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md) | Sets a default role. |
| [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md) | Changes a password. |
| [`SET ROLE`](/sql-statements/sql-statement-set-role.md) | Enables roles in the current session. |
| [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) | Shows the `CREATE` statement for a user. |
| [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md) | Shows privileges associated with a user. |
| [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md) | Shows available privileges. |

<CustomContent platform="tidb">

## TiDB Binlog & TiCDC

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN [SET\|SHOW\|UNSET] BDR ROLE`](/sql-statements/sql-statement-admin-bdr-role.md) | Manages BDR roles. |
| [`CHANGE DRAINER`](/sql-statements/sql-statement-change-drainer.md) | Modifies the status information for Drainer in the cluster. |
| [`CHANGE PUMP`](/sql-statements/sql-statement-change-pump.md) | Modifies the status information for Pump in the cluster. |
| [`SHOW DRAINER STATUS`](/sql-statements/sql-statement-show-drainer-status.md) | Shows the status for all Drainer nodes in the cluster. |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | Shows the latest TSO in the cluster. |
| [`SHOW PUMP STATUS`](/sql-statements/sql-statement-show-pump-status.md) | Shows the status information for all Pump nodes in the cluster. |

</CustomContent>

## Statistics and plan management

| SQL Statement | Description |
|---------------|-------------|
| [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) | Collects statistics about a table. |
| [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md) | Creates an execution plan binding for a SQL statement. |
| [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md) | Drops an execution plan binding from a SQL statement. |
| [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) | Drops statistics from a table. |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) | Works similar to `EXPLAIN`, with the major difference that it will execute the statement. |
| [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md) | Load statistics into TiDB. |
| [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md) | Show statistics collection tasks. |
| [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md) | Show created SQL bindings. |
| [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) | Shows an estimation of how accurate statistics are believed to be. |
| [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) | Shows the histogram information in statistics. |
| [`SHOW STATS_LOCKED`](/sql-statements/sql-statement-show-stats-locked.md) | Shows the tables whose statistics are locked. |
| [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) | Shows how many rows are in a table and how many rows are changed in that table. |

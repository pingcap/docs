# SQL Statement Overview

TiDB uses SQL statements that try to follow the ISO/IEC SQL standards and are extended with MySQL and TiDB specific statements where required.

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
| [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md) | Shows all databases. |
| [`SHOW FIELDS FROM`](/sql-statements/sql-statement-show-fields-from.md) | Shows columns of a table. |
| [`SHOW INDEXES`](/sql-statements/sql-statement-show-indexes.md) | Shows indexes of a table. |
| [`SHOW SCHEMAS`](/sql-statements/sql-statement-show-schemas.md) | An alias to `SHOW DATABASES`, which shows a list of databases that the current user has privileges to. |
| [`SHOW TABLE NEXT_ROW_ID`](/sql-statements/sql-statement-show-table-next-rowid.md) | Shows the next row ID for a table. |
| [`SHOW TABLE REGIONS`](/sql-statements/sql-statement-show-table-regions.md) | Shows regions of a table. |
| [`SHOW TABLE STATUS`](/sql-statements/sql-statement-show-table-status.md) | Shows the status of tables. |
| [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md) | Shows tables in a database. |
| [`TRUNCATE`](/sql-statements/sql-statement-truncate.md) | Truncates all data from a table. |

## Data manipulation statements (DML)

| SQL Statement | Description |
|---------------|-------------|
| [`BATCH`](/sql-statements/sql-statement-batch.md) | Batches DML operations on a table. |
| [`DELETE`](/sql-statements/sql-statement-delete.md) | Deletes rows from a table. |
| [`INSERT`](/sql-statements/sql-statement-insert.md) | Inserts new rows into a table. |
| [`REPLACE`](/sql-statements/sql-statement-replace.md) | Replaces existing rows or inserts new rows. |
| [`SELECT`](/sql-statements/sql-statement-select.md) | Retrieves rows from a table. |
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
| [`SET TRANSACTION`](/sql-statements/sql-statement-set-transaction.md) | Sets the characteristics of the current transaction. |
| [`START TRANSACTION`](/sql-statements/sql-statement-start-transaction.md) | Starts a new transaction. |

## Prepared statements

| SQL Statement | Description |
|---------------|-------------|
| [`DEALLOCATE`](/sql-statements/sql-statement-deallocate.md) | Deallocates a previously prepared statement. |
| [`EXECUTE`](/sql-statements/sql-statement-execute.md) | Executes a previously prepared statement. |
| [`PREPARE`](/sql-statements/sql-statement-prepare.md) | Prepares a statement for execution. |

## Administrative statements

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | Cancels a DDL job. |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | Checks the integrity of a table or index. |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | Computes and checks the checksum of a table. |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | Cleans up indexes from a table. |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | Pauses DDL operations. |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | Resumes DDL operations. |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | Shows DDL jobs or job queries. |
| [`ADMIN SHOW TELEMETRY`](/sql-statements/sql-statement-admin-show-telemetry.md) | Shows telemetry data. |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | Performs various administrative tasks. |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) | Flushes a table. |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | Sets a variable. |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | Set a character set and collation. |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | Splits a region into smaller regions. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN CANCEL DDL`](/sql-statements/sql-statement-admin-cancel-ddl.md) | Cancels a DDL job. |
| [`ADMIN CHECK [TABLE\|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) | Checks the integrity of a table or index. |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md) | Computes and checks the checksum of a table. |
| [`ADMIN CLEANUP INDEX`](/sql-statements/sql-statement-admin-cleanup.md) | Cleans up indexes from a table. |
| [`ADMIN PAUSE DDL`](/sql-statements/sql-statement-admin-pause-ddl.md) | Pauses DDL operations. |
| [`ADMIN RESUME DDL`](/sql-statements/sql-statement-admin-resume-ddl.md) | Resumes DDL operations. |
| [`ADMIN SHOW DDL [JOBS\|JOB QUERIES]`](/sql-statements/sql-statement-admin-show-ddl.md) | Shows DDL jobs or job queries. |
| [`ADMIN`](/sql-statements/sql-statement-admin.md) | Performs various administrative tasks. |
| [`FLUSH TABLES`](/sql-statements/sql-statement-flush-tables.md) | Flushes a table. |
| [`SET <variable>`](/sql-statements/sql-statement-set-variable.md) | Sets a variable. |
| [`SET [NAMES\|CHARACTER SET]`](/sql-statements/sql-statement-set-names.md) | Set a character set and collation. |
| [`SPLIT REGION`](/sql-statements/sql-statement-split-region.md) | Splits a region into smaller regions. |

</CustomContent>

## Data import and export

| SQL Statement | Description |
|---------------|-------------|
| [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md) | Cancels an ongoing import job. |
| [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) | Imports data into a table from an external source. |
| [`LOAD DATA`](/sql-statements/sql-statement-load-data.md) | Loads data into a table from a file. |
| [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md) | Shows the status of an import job. |

## Backup & restore

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN RECOVER INDEX`](/sql-statements/sql-statement-admin-recover.md) | Recovers a damaged index. |
| [`BACKUP`](/sql-statements/sql-statement-backup.md) | Creates a backup of the database. |
| [`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md) | Restores the cluster to a previous state. |
| [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md) | Restores the database to a previous state. |
| [`FLASHBACK TABLE`](/sql-statements/sql-statement-flashback-table.md) | Restores a table to a previous state. |
| [`RECOVER TABLE`](/sql-statements/sql-statement-recover-table.md) | Recovers a table. |
| [`RESTORE`](/sql-statements/sql-statement-restore.md) | Restores a database from a backup. |
| [`SHOW BACKUPS`](/sql-statements/sql-statement-show-backups.md) | Shows backups. |

## Placement policy

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER PLACEMENT POLICY`](/sql-statements/sql-statement-alter-placement-policy.md) | Modifies a placement policy. |
| [`ALTER RANGE`](/sql-statements/sql-statement-alter-range.md) | Modifies the range of a placement policy. |
| [`CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-create-placement-policy.md) | Creates a new placement policy. |
| [`DROP PLACEMENT POLICY`](/sql-statements/sql-statement-drop-placement-policy.md) | Drops an existing placement policy. |
| [`SHOW CREATE PLACEMENT POLICY`](/sql-statements/sql-statement-show-create-placement-policy.md) | Shows the CREATE statement for a placement policy. |
| [`SHOW PLACEMENT FOR`](/sql-statements/sql-statement-show-placement-for.md) | Shows placement rules for a specific table. |
| [`SHOW PLACEMENT LABELS`](/sql-statements/sql-statement-show-placement-labels.md) | Shows available placement labels. |
| [`SHOW PLACEMENT`](/sql-statements/sql-statement-show-placement.md) | Shows placement rules. |

## Resource groups

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | Modifies a resource group. |
| [`CALIBRATE RESOURCE`](/sql-statements/sql-statement-calibrate-resource.md) | Calibrates system resources. |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | Creates a new resource group. |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | Drops a resource group. |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | Manage runaway query watch list. |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | Sets a resource group. |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | Shows the CREATE statement for a resource group. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER RESOURCE GROUP`](/sql-statements/sql-statement-alter-resource-group.md) | Modifies a resource group. |
| [`CREATE RESOURCE GROUP`](/sql-statements/sql-statement-create-resource-group.md) | Creates a new resource group. |
| [`DROP RESOURCE GROUP`](/sql-statements/sql-statement-drop-resource-group.md) | Drops a resource group. |
| [`QUERY WATCH`](/sql-statements/sql-statement-query-watch.md) | Manage runaway query watch list. |
| [`SET RESOURCE GROUP`](/sql-statements/sql-statement-set-resource-group.md) | Sets a resource group. |
| [`SHOW CREATE RESOURCE GROUP`](/sql-statements/sql-statement-show-create-resource-group.md) | Shows the CREATE statement for a resource group. |

</CustomContent>

## Utility statements

| SQL Statement | Description |
|---------------|-------------|
| [`DESC`](/sql-statements/sql-statement-desc.md) | Describes the structure of a table. |
| [`DESCRIBE`](/sql-statements/sql-statement-describe.md) | Describes the structure of a table. |
| [`DO`](/sql-statements/sql-statement-do.md) | Executes an expression. |
| [`EXPLAIN`](/sql-statements/sql-statement-explain.md) | Shows the execution plan of a query. |
| [`TRACE`](/sql-statements/sql-statement-trace.md) | Traces query execution. |
| [`USE`](/sql-statements/sql-statement-use.md) | Sets the current database. |

## Show statements

| SQL Statement | Description |
|---------------|-------------|
| [`SHOW BUILTINS`](/sql-statements/sql-statement-show-builtins.md) | Lists builtin functions. |
| [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md) | Lists character sets. |
| [`SHOW COLLATIONS`](/sql-statements/sql-statement-show-collation.md) | Lists collations. |
| [`SHOW ERRORS`](/sql-statements/sql-statement-show-errors.md) | Shows error messages. |
| [`SHOW STATUS`](/sql-statements/sql-statement-show-status.md) | Shows server status. |
| [`SHOW VARIABLES`](/sql-statements/sql-statement-show-variables.md) | Shows system variables. |
| [`SHOW WARNINGS`](/sql-statements/sql-statement-show-warnings.md) | Shows warning messages. |

## Instance management

<CustomContent platform="tidb">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | Modifies an instance. |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) | Resets status variables. |
| [`KILL`](/sql-statements/sql-statement-kill.md) | Kills a process. |
| [`SHOW CONFIG`](/sql-statements/sql-statement-show-config.md) | Shows the configuration. |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | Shows available storage engines. |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | Shows installed plugins. |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | Shows active threads. |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) | Shows query profiles. |
| [`SHUTDOWN`](/sql-statements/sql-statement-shutdown.md) | Shuts down the database server. |

</CustomContent>

<CustomContent platform="tidb-cloud">

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER INSTANCE`](/sql-statements/sql-statement-alter-instance.md) | Modifies an instance. |
| [`FLUSH STATUS`](/sql-statements/sql-statement-flush-status.md) | Resets status variables. |
| [`KILL`](/sql-statements/sql-statement-kill.md) | Kills a process. |
| [`SHOW ENGINES`](/sql-statements/sql-statement-show-engines.md) | Shows available storage engines. |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | Shows the status of the master server. |
| [`SHOW PLUGINS`](/sql-statements/sql-statement-show-plugins.md) | Shows installed plugins. |
| [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) | Shows active threads. |
| [`SHOW PROFILES`](/sql-statements/sql-statement-show-profiles.md) | Shows query profiles. |

</CustomContent>

## Locking statements

| SQL Statement | Description |
|---------------|-------------|
| [`LOCK STATS`](/sql-statements/sql-statement-lock-stats.md) | Locks statistics for a table. |
| [`LOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | Locks tables for the current session. |
| [`UNLOCK STATS`](/sql-statements/sql-statement-unlock-stats.md) | Unlocks statistics for a table. |
| [`UNLOCK TABLES`](/sql-statements/sql-statement-lock-tables-and-unlock-tables.md) | Unlocks tables. |

## Account management / Data Control Language

| SQL Statement | Description |
|---------------|-------------|
| [`ALTER USER`](/sql-statements/sql-statement-alter-user.md) | Modifies a user. |
| [`CREATE ROLE`](/sql-statements/sql-statement-create-role.md) | Creates a role. |
| [`CREATE USER`](/sql-statements/sql-statement-create-user.md) | Creates a new user. |
| [`DROP ROLE`](/sql-statements/sql-statement-drop-role.md) | Drops an existing role. |
| [`DROP USER`](/sql-statements/sql-statement-drop-user.md) | Drops an existing user. |
| [`FLUSH PRIVILEGES`](/sql-statements/sql-statement-flush-privileges.md) | Activates privilege changes. |
| [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md) | Grants privileges. |
| [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md) | Grants a role. |
| [`RENAME USER`](/sql-statements/sql-statement-rename-user.md) | Renames an existing user. |
| [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md) | Revokes privileges. |
| [`REVOKE <role>`](/sql-statements/sql-statement-revoke-role.md) | Revokes a role. |
| [`SET DEFAULT ROLE`](/sql-statements/sql-statement-set-default-role.md) | Sets a default role. |
| [`SET PASSWORD`](/sql-statements/sql-statement-set-password.md) | Changes a password. |
| [`SET ROLE`](/sql-statements/sql-statement-set-role.md) | Sets a role. |
| [`SHOW CREATE USER`](/sql-statements/sql-statement-show-create-user.md) | Shows the CREATE statement for a user. |
| [`SHOW GRANTS`](/sql-statements/sql-statement-show-grants.md) | Shows grants for a user. |
| [`SHOW PRIVILEGES`](/sql-statements/sql-statement-show-privileges.md) | Shows available privileges. |

<CustomContent platform="tidb">

## TiDB Binlog & TiCDC

| SQL Statement | Description |
|---------------|-------------|
| [`ADMIN [SET\|SHOW\|UNSET] BDR ROLE`](/sql-statements/sql-statement-admin-bdr-role.md) | Manages BDR roles. |
| [`CHANGE DRAINER`](/sql-statements/sql-statement-change-drainer.md) | Changes drainer. |
| [`CHANGE PUMP`](/sql-statements/sql-statement-change-pump.md) | Changes pump. |
| [`SHOW DRAINER STATUS`](/sql-statements/sql-statement-show-drainer-status.md) | Shows the status of the drainer. |
| [`SHOW MASTER STATUS`](/sql-statements/sql-statement-show-master-status.md) | Shows the status of the master server. |
| [`SHOW PUMP STATUS`](/sql-statements/sql-statement-show-pump-status.md) | Shows the status of the pump. |

</CustomContent>

## Statistics and plan management

| SQL Statement | Description |
|---------------|-------------|
| [`ANALYZE TABLE`](/sql-statements/sql-statement-analyze-table.md) | Collects statistics about a table. |
| [`CREATE BINDING`](/sql-statements/sql-statement-create-binding.md) | Creates a plan binding. |
| [`DROP BINDING`](/sql-statements/sql-statement-drop-binding.md) | Drops a plan binding. |
| [`DROP STATS`](/sql-statements/sql-statement-drop-stats.md) | Drops statistics from a table. |
| [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md) | Analyze query execution. |
| [`LOAD STATS`](/sql-statements/sql-statement-load-stats.md) | Load statistics. |
| [`SHOW ANALYZE STATUS`](/sql-statements/sql-statement-show-analyze-status.md) | Show analyze status. |
| [`SHOW BINDINGS`](/sql-statements/sql-statement-show-bindings.md) | Show bindings. |
| [`SHOW STATS_HEALTHY`](/sql-statements/sql-statement-show-stats-healthy.md) | Shows the health of statistics. |
| [`SHOW STATS_HISTOGRAMS`](/sql-statements/sql-statement-show-stats-histograms.md) | Shows statistics histograms. |
| [`SHOW STATS_LOCKED`](/sql-statements/sql-statement-show-stats-locked.md) | Shows locked statistics. |
| [`SHOW STATS_META`](/sql-statements/sql-statement-show-stats-meta.md) | Shows metadata statistics. |
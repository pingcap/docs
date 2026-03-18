---
title: Administration Commands
summary: This page provides reference information for the system administration commands in Databend.
---
This page provides reference information for the system administration commands in Databend.

## System Monitoring

| Command | Description |
|---------|-------------|
| **[SHOW PROCESSLIST](/tidb-cloud-lake/sql/show-processlist.md)** | Display active queries and connections |
| **[SHOW METRICS](/tidb-cloud-lake/sql/show-metrics.md)** | View system performance metrics |
| **[KILL](/tidb-cloud-lake/sql/kill.md)** | Terminate running queries or connections |
| **[RUST BACKTRACE](/tidb-cloud-lake/sql/system-enable-disable-exception-backtrace.md)** | Debug Rust stack traces |

## Access Control

| Command | Description |
|---------|-------------|
| **[FLUSH PRIVILEGES](/tidb-cloud-lake/guides/privileges.md)** | Force every query node to reload role and privilege metadata |

## Configuration Management

| Command | Description |
|---------|-------------|
| **[SET](/tidb-cloud-lake/sql/set.md)** | Set global configuration parameters |
| **[UNSET](/tidb-cloud-lake/sql/unset.md)** | Remove configuration settings |
| **[SET VARIABLE](/tidb-cloud-lake/sql/set-var.md)** | Manage user-defined variables |
| **[SHOW SETTINGS](/tidb-cloud-lake/sql/show-settings.md)** | Display current system settings |

## Function Management

| Command | Description |
|---------|-------------|
| **[SHOW FUNCTIONS](/tidb-cloud-lake/sql/show-functions.md)** | List built-in functions |
| **[SHOW USER FUNCTIONS](/tidb-cloud-lake/sql/show-user-functions.md)** | List user-defined functions |
| **[SHOW TABLE FUNCTIONS](/tidb-cloud-lake/sql/show-table-functions.md)** | List table-valued functions |

## Storage Maintenance

| Command | Description |
|---------|-------------|
| **[VACUUM TABLE](/tidb-cloud-lake/sql/vacuum-table.md)** | Reclaim storage space from tables |
| **[VACUUM DROP TABLE](/tidb-cloud-lake/sql/vacuum-drop-table.md)** | Clean up dropped table data |
| **[VACUUM TEMP FILES](/tidb-cloud-lake/sql/vacuum-temporary-files.md)** | Remove temporary files |
| **[SHOW INDEXES](/tidb-cloud-lake/sql/show-indexes.md)** | Display table indexes |

## Dynamic Execution

| Command | Description |
|---------|-------------|
| **[EXECUTE IMMEDIATE](/tidb-cloud-lake/sql/execute-immediate.md)** | Execute dynamically constructed SQL statements |

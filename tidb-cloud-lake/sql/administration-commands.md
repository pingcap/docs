---
title: Administration Commands
---

This page provides reference information for the system administration commands in Databend.

## System Monitoring

| Command | Description |
|---------|-------------|
| **[SHOW PROCESSLIST](07-show-processlist.md)** | Display active queries and connections |
| **[SHOW METRICS](08-show-metrics.md)** | View system performance metrics |
| **[KILL](01-kill.md)** | Terminate running queries or connections |
| **[RUST BACKTRACE](rust-backtrace.md)** | Debug Rust stack traces |

## Access Control

| Command | Description |
|---------|-------------|
| **[FLUSH PRIVILEGES](flush-privileges.md)** | Force every query node to reload role and privilege metadata |

## Configuration Management

| Command | Description |
|---------|-------------|
| **[SET](02-set-global.md)** | Set global configuration parameters |
| **[UNSET](02-unset.md)** | Remove configuration settings |
| **[SET VARIABLE](03-set-var.md)** | Manage user-defined variables |
| **[SHOW SETTINGS](03-show-settings.md)** | Display current system settings |

## Function Management

| Command | Description |
|---------|-------------|
| **[SHOW FUNCTIONS](04-show-functions.md)** | List built-in functions |
| **[SHOW USER FUNCTIONS](05-show-user-functions.md)** | List user-defined functions |
| **[SHOW TABLE FUNCTIONS](06-show-table-functions.md)** | List table-valued functions |

## Storage Maintenance

| Command | Description |
|---------|-------------|
| **[VACUUM TABLE](09-vacuum-table.md)** | Reclaim storage space from tables |
| **[VACUUM DROP TABLE](09-vacuum-drop-table.md)** | Clean up dropped table data |
| **[VACUUM TEMP FILES](09-vacuum-temp-files.md)** | Remove temporary files |
| **[SHOW INDEXES](show-indexes.md)** | Display table indexes |

## Dynamic Execution

| Command | Description |
|---------|-------------|
| **[EXECUTE IMMEDIATE](execute-immediate.md)** | Execute dynamically constructed SQL statements |

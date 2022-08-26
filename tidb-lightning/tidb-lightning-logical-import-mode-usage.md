---
title: Use Logical Import Mode
summary: Learn how to use logical import mode in TiDB Lightning.
---

# Use Logical Import Mode

This document introduces how to use the logical import mode in TiDB Lightning, including writing the configuration file and tuning performance.

## Configure and use the logical import mode

You can use the following configuration file to execute data import using logical import mode:

```toml
[lightning]
# log
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# Checks the cluster minimum requirements before start.
check-requirements = true

[mydumper]
# The local data source directory or the external storage URL.
data-source-dir = "/data/my_database"

[tikv-importer]
# Import mode. "tidb" means using the logical import mode.
backend = "tidb"

# The operation of inserting duplicate data in logical import mode.
# - replace: replace existing data with new data
# - ignore: keep existing data and ignore new data
# - error: pause the import and report an error
on-duplicate = "replace"

[tidb]
# The information of the target cluster. The address of any tidb-server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. Either plaintext or Base64 encoded.
password = ""
# tidb-lightning imports the TiDB library, and generates some logs.
# Set the log level of the TiDB library.
log-level = "error"
```

For the complete configuration file, refer to [the configuration file and command line parameters](/tidb-lightning/tidb-lightning-configuration.md).

## Conflict detection

Conflicting data refers to two or more records with the same PK/UK column data. When the data source contains conflicting data, the actual number of rows in the table is different from the total number of rows returned by the query using unique index.

In logical import mode, you can configure the strategy for resolving conflicting data by setting the `on-duplicate` configuration item. Based on the strategy, TiDB Lightning imports data with different SQL statements.

| Configuration | Default behavior of conflicting data | The corresponding SQL statement |
| :-- | :-- | :-- |
| `replace` | Replace existing data with new data. | `REPLACE INTO ...` |
| `ignore` | Keep existing data and ignore new data. | `INSERT IGNORE INTO ...` |
| `error` | Pause the import and report an error. | `INSERT INTO ...` |

## Performance tuning

- In logical import mode, the performance of TiDB Lightning largely depends on the write performance of the target TiDB cluster. If the cluster hits a performance bottleneck, refer to [Highly Concurrent Write Best Practices](/best-practices/high-concurrency-best-practices.md).

- If the target TiDB cluster does not hit a write bottleneck, consider increasing the value of `region-concurrency` in TiDB Lightning configuration. The default value of `region-concurrency` is the number of CPU cores. The meaning of `region-concurrency` is different between physical import mode and logical import mode. In logical import mode, `region-concurrency` is the write concurrency.

    Example configuration:

    ```toml
    [lightning]
    region-concurrency = 32
    ```

- Adjusting the `raftstore.apply-pool-size` and `raftstore.store-pool-size` configuration items in the target TiDB cluster might improve the import speed.

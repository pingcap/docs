---
title: TiDB Lightning Configuration
summary: Learn about the CLI usage and sample configuration in TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-configuration/','/docs/dev/reference/tools/tidb-lightning/config/']
---

# TiDB Lightning Configuration

This document provides samples for global configuration and task configuration, and describes the usage of command-line parameters. You can find a sample configuration file in [`lightning/tidb-lightning.toml`](https://github.com/pingcap/tidb/blob/master/lightning/tidb-lightning.toml).

TiDB Lightning has two configuration classes: "global" and "task", and they have compatible structures. Their distinction arises only when the [server mode](/tidb-lightning/tidb-lightning-web-interface.md) is enabled. When server mode is disabled (the default), TiDB Lightning will only execute one task, and the same configuration file is used for both global and task configurations.

## TiDB Lightning (Global)

### lightning

#### `status-addr`

- The HTTP port for displaying the task progress on the web interface, pulling Prometheus metrics, exposing debug data, and submitting import tasks (in server mode).
- Setting it to `0` disables the port.

<!-- Example: `:8289` -->

#### `server-mode`

- Sets the server mode.
- Default value: `false`
- Value options:
    - `false`: an import task starts immediately after you execute the command.
    - `true`: after you execute the command, TiDB Lightning waits until you submit an import task in the web interface. For more information, see [TiDB Lightning Web Interface](/tidb-lightning/tidb-lightning-web-interface.md).

#### `level`

- Example: `"info"`

#### `file`

- Example: `"tidb-lightning.log"`

#### `max-size`

- Example: `128` <!-- MB -->

#### `max-days`

- Example: `28`

#### `max-backups`

- Example: `14`

#### `enable-diagnose-logs` <span class="version-mark">New in v7.3.0</span>

- Controls whether to enable the diagnostic logs.
- Default value: `false`
- Value options:
    - `false`: only the logs related to the import are output, and the logs of other dependent components are not output.
    - `true`: logs from both the import process and other dependent components are output, and GRPC debugging is enabled, which can be used for diagnosis.

## TiDB Lightning (Task)

### lightning

#### `check-requirements`

- Checks whether the cluster meets the minimum requirement before starting the task, and checks whether TiKV has more than 10% free space left during running time.

<!-- Example: `true` -->

#### `index-concurrency`

- The maximum number of index engines to be opened concurrently. Each table is split into one "index engine" to store indices, and multiple "data engines" to store row data. `index-concurrency` and `table-concurrency` settings control the maximum concurrent number for each type of engines. Generally, use the default value.

<!-- Example: `2` -->

#### `table-concurrency`

- The maximum number of data engines to be opened concurrently. Each table is split into one "index engine" to store indices, and multiple "data engines" to store row data. `index-concurrency` and `table-concurrency` settings control the maximum concurrent number for each type of engines. Generally, use the default value.

<!-- Example: `6` -->

#### `region-concurrency`

- The concurrency number of data. When deploying together with other components, you can set it to 75% of the size of logical CPU cores to limit the CPU usage.
- Default value: the number of logical CPU cores

#### `io-concurrency`

- The maximum I/O concurrency. Excessive I/O concurrency causes an increase in I/O latency because the disk's internal buffer is frequently refreshed, which causes the cache miss and slows down the read speed. Depending on the storage medium, this value might need to be adjusted for optimal performance.

<!-- Example: `5` -->

#### `max-error`

- The maximum number of non-fatal errors to tolerate before stopping TiDB Lightning.
- Non-fatal errors are localized to a few rows, and ignoring those rows allows the import process to continue.
- Setting this to N means that TiDB Lightning will stop as soon as possible when the (N+1)-th error is encountered.
- The skipped rows will be inserted into tables inside the `task info` schema on the target TiDB.
- Default value: `MaxInt64` bytes, that is, `9223372036854775807` bytes.

#### `task-info-schema-name`

- Specifies the name of the schema or database that stores TiDB Lightning execution results.
- To disable error recording, set this to an empty string.

<!-- Example: `'lightning_task_info'` -->

#### `meta-schema-name`

- In [parallel import mode](/tidb-lightning/tidb-lightning-distributed-import.md), the schema name that stores the meta information for each TiDB Lightning instance in the target cluster. Configure this parameter only if parallel import is enabled.
- The value set for this parameter must be the same for each TiDB Lightning instance that participates in the same parallel import; otherwise, the correctness of the imported data cannot be ensured.
- If parallel import mode is enabled, make sure that the user used for import (for the `tidb.user` configuration) has permissions to create and access the databases corresponding to this configuration.
- TiDB Lightning removes this schema after the import is completed. So do not use any existing schema name to configure this parameter.
- Default value: `"lightning_metadata"`

### security

The `security` section specifies certificates and keys for TLS connections within the cluster.

#### `ca-path`

- Specifies the public certificate of the CA. Leave it empty if you want to disable TLS.

<!-- Example: `"/path/to/ca.pem"` -->

#### `cert-path`

- Specifies the public certificate of this service.

<!-- Example: `"/path/to/lightning.pem"` -->

#### `key-path`

- Specifies the private key of this service.

<!-- Example: `"/path/to/lightning.key"` -->

### checkpoint

#### `enable`

- Controls whether to enable checkpoints.
- While importing data, TiDB Lightning records which tables have been imported, so even if TiDB Lightning or another component crashes, you can start from a known good state instead of restarting from scratch.

<!-- Example: `true` -->

#### `schema`

- Specifies the schema name (database name) to store the checkpoints.

<!-- Example: `"tidb_lightning_checkpoint"` -->

#### `driver`

- Where to store the checkpoints.
- Value options:
    - `"file"`: store as a local file.
    - `"mysql"`: store into a remote MySQL-compatible database.

#### `dsn`

- The data source name (DSN) indicating the location of the checkpoint storage.
- For the `file` driver, the DSN is a path. If the path is not specified, TiDB Lightning uses the default value `/tmp/CHECKPOINT_SCHEMA.pb`.
- For the `mysql` driver, the DSN is a URL in the form of `USER:PASS@tcp(HOST:PORT)/`.
- If the URL is not specified, the TiDB server from the `[tidb]` section is used to store the checkpoints.
- It is recommended that you specify a different MySQL-compatible database server to reduce the load of the target TiDB cluster.

<!-- Example: `"/tmp/tidb_lightning_checkpoint.pb"` -->

#### `keep-after-success`

- Controls whether to keep the checkpoints after all data are imported. If `false`, the checkpoints will be deleted.
- Keeping the checkpoints can aid debugging but will leak metadata about the data source.

<!-- Example: `false` -->

### conflict

#### `strategy`

- Starting from v7.3.0, a new version of strategy is introduced to handle conflicting data. Starting from v8.0.0, TiDB Lightning optimizes the conflict strategy for both physical and logical import modes.
- Default value: `""`
- Value options:
    - `""`:
        - In the physical import mode, TiDB Lightning does not detect or handle conflicting data. If the source file contains conflicting primary or unique key records, the subsequent step reports an error.
        - In the logical import mode, TiDB Lightning converts the `""` strategy to the `"error"` strategy for processing.
    - `"error"`: when detecting conflicting primary or unique key records in the imported data, TiDB Lightning terminates the import and reports an error.
    - `"replace"`: when encountering conflicting primary or unique key records, TiDB Lightning retains the latest data and overwrites the old data.
        - When you use the physical import mode, the conflicting data are recorded in the `lightning_task_info.conflict_view` view of the target TiDB cluster.
        - In the `lightning_task_info.conflict_view` view, if the `is_precheck_conflict` field for a row is `0`, it means that the conflicting data recorded in that row is detected by postprocess conflict detection; if the `is_precheck_conflict` field for a row is `1`, it means that conflicting data recorded in that row is detected by pre-import conflict detection. You can manually insert the correct records into the target table based on your application requirements.
        - Note that the target TiKV must be v5.2.0 or later versions.
    - `"ignore"`: when encountering conflicting primary or unique key records, TiDB Lightning retains the old data and ignores the new data. This option can only be used in the logical import mode.

#### `precheck-conflict-before-import`

- Controls whether to enable pre-import conflict detection, which checks conflicts in data before importing it to TiDB. This parameter can be used only in the physical import mode.
- In scenarios where the number of conflict records is greater than 1,000,000, it is recommended to set `precheck-conflict-before-import = true` for better performance in conflict detection.
- In other scenarios, it is recommended to disable it.
- Default value: `false`
- Value options:
    - `false`: TiDB Lightning only checks conflicts after the import.
    - `true`: TiDB Lightning checks conflicts both before and after the import.

#### `threshold`

- Controls the maximum number of conflict errors that can be handled when [`strategy`](#strategy) is `"replace"` or `"ignore"`. You can set it only when `strategy` is `"replace"` or `"ignore"`.
- If you set a value larger than `10000`, the import process might experience performance degradation.
- Default value: `10000`

#### `max-record-rows`

- Controls the maximum number of records in the `conflict_records` table.
- Starting from v8.1.0, there is no need to configure `max-record-rows` manually, because TiDB Lightning automatically assigns the value of `max-record-rows` with the value of [`threshold`](#threshold), regardless of the user input.
- `max-record-rows` will be deprecated in a future release.
- In the physical import mode, if the strategy is `"replace"`, the conflict records that are overwritten are recorded.
- In the logical import mode, if the strategy is `"ignore"`, the conflict records that are ignored are recorded; if the strategy is `"replace"`, the conflict records are not recorded.
- Default value: `10000`

### tikv-importer

#### `backend`

- Specifies the import mode of TiDB Lightning.
- Default value: `"local"`
- Value options:
    - `"local"`: [Physical import mode](/tidb-lightning/tidb-lightning-physical-import-mode.md), used by default. It applies to large dataset import, for example, greater than 1 TiB. However, during the import, downstream TiDB is not available to provide services.
    - `"tidb"`: [Logical import mode](/tidb-lightning/tidb-lightning-logical-import-mode.md). You can use this mode for small dataset import, for example, smaller than 1 TiB. During the import, downstream TiDB is available to provide services.

#### `parallel-import`

- Controls whether to enable multiple TiDB Lightning instances (in physical import mode) to import data to one or more target tables [in parallel](/tidb-lightning/tidb-lightning-distributed-import.md). Note that this parameter is only used in scenarios where the target table is empty.
- Default value: `false`
- Value options: `true`, `false`
- When you use parallel import mode, you must set the parameter to `true`, but the premise is that no data exists in the target table, that is, all data can only be imported by TiDB Lightning.

#### `duplicate-resolution`

> **Warning:**
>
> Starting from v8.0.0, the `duplicate-resolution` parameter is deprecated and will be removed in a future release. For more information, see [The old version of conflict detection](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#the-old-version-of-conflict-detection-deprecated-in-v800).

- Controls whether to detect and resolve duplicate records (unique key conflict) in the physical import mode.
- Default value: `'none'`
- Value options:
    - `'none'`: does not detect duplicate records. If there are duplicate records in the data source, it might lead to inconsistent data in the target TiDB. If you set `duplicate-resolution = 'none'` and do not set `conflict.strategy`, TiDB Lightning will automatically assign `""` to `conflict.strategy`.
    - `'remove'`: if you set `duplicate-resolution = 'remove'` and do not set `conflict.strategy`, TiDB Lightning will automatically assign "replace" to `conflict.strategy` and enable the new version of conflict detection.

#### `send-kv-pairs`

> **Warning:**
>
> Starting from v7.2.0, this parameter is deprecated and no longer takes effect after it is set. If you want to adjust the amount of data sent to TiKV in one request, use the [`send-kv-size`](#send-kv-size-new-in-v720) parameter instead.

- Specifies the maximum number of KV pairs in one request when sending data to TiKV in physical import mode.

<!-- Example: 32768 -->

#### `send-kv-size` <span class="version-mark">New in v7.2.0</span>

- Specifies the maximum size of one request when sending data to TiKV in physical import mode.
- Default value: `"16K"`

#### `compress-kv-pairs`

- Controls whether to enable compression when sending KV pairs to TiKV in the physical import mode.
- Currently, only the Gzip compression algorithm is supported. To use this algorithm, you can fill in either `"gzip"` or `"gz"` for this parameter.
- Default value: `""`, which means the compression is not enabled.
- Value options: `""`, `"gzip"`, `"gz"`

#### `sorted-kv-dir`

- Specifies the directory of local KV sorting in the physical import mode. If the disk performance is low (such as in HDD), it is recommended to set the directory on a different disk from `data-source-dir` to improve import speed.

#### `range-concurrency`

- Specifies the concurrency that TiKV writes KV data in the physical import mode.
- When the network transmission speed between TiDB Lightning and TiKV exceeds 10 Gigabit, you can increase this value accordingly.
- Default value: `16`

#### `store-write-bwlimit`

- Limits the bandwidth in which TiDB Lightning writes data into each TiKV node in the physical import mode.
- Default value: `0`, which means no limit.

#### `disk-quota`

- Specifies the disk quota for local temporary files when physical import mode is used.
- When the disk quota is insufficient, TiDB Lightning stops reading source data and writing temporary files, but prioritizes writing the already sorted key-value pairs to TiKV. After TiDB Lightning deletes the local temporary files, the import process continues.
- This option takes effect only when you set the [`backend`](#backend) option to `local`.
- Default value: `MaxInt64` bytes, that is, 9223372036854775807 bytes.

#### `add-index-by-sql`

- Specifies whether to add indexes via SQL in physical import mode.
- This mechanism is consistent with that of the historical versions. The benefit of adding indexes via SQL is that you can separately import data and import indexes, and import data more quickly. After the data is imported, even if the indexes fail to be added, it does not affect the consistency of the imported data.
- Default value: `false`
- Value options:
    - `false`: TiDB Lightning will encode both row data and index data into KV pairs and import them into TiKV together.
    - `true`: TiDB Lightning adds indexes via the `ADD INDEX` SQL statement after importing the row data.

#### `keyspace-name`

- When you use TiDB Lightning to import a multi-tenant TiDB cluster, use this parameter to specify the corresponding key space name.
- Default value: `""`, which means TiDB Lightning will automatically get the key space name of the corresponding tenant to import data.
- If you specify a value, the specified key space name will be used to import data.

#### `pause-pd-scheduler-scope` <span class="version-mark">New in v7.1.0</span>

- In Physical Import Mode, this parameter controls the scope in which TiDB Lightning stops PD scheduling.
- Default value: `"table"`
- Value options:
    - `"table"`: pause scheduling only for the Region that stores the target table data.
    - `"global"`: pause global scheduling. When importing data to a cluster without any business traffic, it is recommended to set this parameter to `"global"` to avoid interference from other scheduling.

#### `region-split-batch-size` <span class="version-mark">New in v7.1.0</span>

- In Physical Import Mode, this parameter controls the number of Regions when splitting Regions in a batch.
- The maximum number of Regions that can be split at the same time per TiDB Lightning instance is: `region-split-batch-size * region-split-concurrency * table-concurrency`
- Default value: `4096`

#### `region-split-concurrency` <span class="version-mark">New in v7.1.0</span>

- In Physical Import Mode, this parameter controls the concurrency when splitting Regions.
- Default value: the number of CPU cores

#### `region-check-backoff-limit` <span class="version-mark">New in v7.1.0</span>

- In Physical Import Mode, this parameter controls the number of retries to wait for the Region to come online after the split and scatter operations.
- The maximum retry interval is two seconds. The number of retries will not be increased if any Region becomes online between retries.
- Default value: `1800`

#### `block-size` <span class="version-mark">New in v7.6.0</span>

- In Physical Import Mode, this parameter controls the I/O block size for sorting local files. When the disk IOPS is a bottleneck, you can increase this value to improve data import performance.
- The value must be greater than or equal to `1B`. Note that if you only specify a number (for example, `16`), the unit is Byte instead of KiB.
- Default value: `"16KiB"`

#### `logical-import-batch-size` <span class="version-mark">New in v8.0.0</span>

- In Logical Import Mode, this parameter controls the size of each SQL statement executed on the downstream TiDB server.
- It specifies the expected size of the `VALUES` part of each `INSERT` or `REPLACE` statement in a single transaction.
- This parameter is not a hard limit. The actual SQL executed might be longer or shorter, depending on the actual content imported.
- Default value: `"96KiB"`, which is optimized for import speed when TiDB Lightning is the only client of the cluster.
- Due to the implementation details of TiDB Lightning, the value is capped at 96 KiB. Setting a larger value will not take effect. You can decrease this value to reduce the stress on the cluster due to large transactions.

#### `logical-import-batch-rows` <span class="version-mark">New in v8.0.0</span>

- In Logical Import Mode, this parameter controls the maximum number of rows inserted per transaction.
- When you specify both [`logical-import-batch-size`](#logical-import-batch-size-new-in-v800) and `logical-import-batch-rows`, the parameter whose value reaches its threshold first will take effect.
- You can decrease this value to reduce the stress on the cluster due to large transactions.
- Default value: `65536`

#### `logical-import-prep-stmt`

- In Logical Import Mode, this parameter controls whether to use [prepared statements](/sql-statements/sql-statement-prepare.md) and statement cache to improve performance.
- Default value: `false`

### mydumper

#### `read-block-size`

- Specifies the block size for file reading. Keep it longer than the longest string of the data source.
- Default value: `"64KiB"`

#### `batch-import-ratio`

- The engine file needs to be imported sequentially. Due to parallel processing, multiple data engines will be imported at nearly the same time, and this creates a queue and wastes resources. Therefore, TiDB Lightning slightly increases the size of the first few batches to properly distribute resources.
- The scale up factor is controlled by this parameter, which expresses the ratio of duration between the "import" and "write" steps with full concurrency. This can be calculated by using the ratio (import duration/write duration) of a single table of size around 1 GiB. The exact timing can be found in the log.
- If "import" is faster, the batch size variance is smaller, and a ratio of zero means a uniform batch size.
- Range: `[0, 1)`

<!-- Example: `0.75` -->

#### `data-source-dir`

- Specifies the local source data directory or the URI of the external storage. For more information about the URI of the external storage, see [URI format](/br/backup-and-restore-storages.md#uri-format).

<!-- Example: `"/data/my_database"` -->

#### `character-set`

- Specifies the character set of the schema files that contains the `CREATE TABLE` statements.
- Default value: `"auto"`
- Value options:
    - `"auto"`: automatically detects whether the schema is UTF-8 or GB-18030. An error is reported if the encoding is neither.
    - `"utf8mb4"`: the schema files must be encoded as UTF-8; otherwise, an error is reported.
    - `"gb18030"`: the schema files must be encoded as GB-18030; otherwise, an error is reported
    - `"latin1"`: the schema files use MySQL latin1 encoding, also known as Code Page 1252.
    - `"binary"`: do not try to decode the schema files

#### `data-character-set`

- Specifies the character set of the source data file. TiDB Lightning converts the source file from the specified character set to UTF-8 encoding when importing.
- Currently, this configuration only specifies the character set of the CSV files with the following options supported. If left blank, the default value `"binary"` is used, that is to say, Lightning does not convert the encoding.
- TiDB Lightning does not predict about the character set of the source data file and only converts the source file and import the data based on this configuration.
- If the value of this configuration is not the same as the actual encoding of the source data file, a failed import, data loss or data disorder might appear.
- Default value: `"binary"`
- Value options:
    - `"binary"`: indicates that TiDB Lightning does not convert the encoding (by default).
    - `"utf8mb4"`: indicates that the source data file uses UTF-8 encoding.
    - `"GB18030"`: indicates that the source data file uses the GB-18030 encoding.
    - `"GBK"`: the source data file uses GBK encoding (GBK encoding is an extension of the GB-2312 character set, also known as Code Page 936).
    - `"latin1"`: the source data file uses MySQL latin1 encoding, also known as Code Page 1252.

#### `data-invalid-char-replace`

- Specifies the replacement character in case of incompatible characters during the character set conversion of the source data file.
- This configuration must not be duplicated with field separators, quote definers, and line breaks. Changing the default value might result in potential degradation of parsing performance for the source data file.
- Default value: `"\uFFFD"`, which is the "error" Rune or Unicode replacement character in UTF-8 encoding.

#### `strict-format`

- Specifies the input data in a [strict format](/tidb-lightning/tidb-lightning-data-source.md#strict-format) to speed up processing. The default value is `false` for safety instead of speed.
- Default value: `false`
- Value options: `true`, `false`
- `strict-format = true` requires that:
    - In CSV, every value cannot contain literal new lines (`U+000A` and `U+000D`, or `\r` and `\n`) even when quoted, which means new lines are strictly used to separate rows.
    - The strict format allows TiDB Lightning to quickly locate split positions of a large file for parallel processing. However, if the input data is not "strict", it might split a valid data in half and corrupt the result.

#### `max-region-size`

- If [`strict-format`](#strict-format) is `true`, TiDB Lightning splits large CSV files into multiple chunks to process in parallel. `max-region-size` is the maximum size of each chunk after splitting.
- Default value: `"256MiB"`

#### `filter`

- Only imports tables that match these wildcard rules.

<!-- Example: `['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']` -->

### mydumper.csv

Configures how CSV files are parsed.

#### `separator`

- Specifies the separator between fields. It supports one or more characters.
- Default value: `','`

#### `delimiter`

- Specifies the quoting delimiter. Empty value means no quoting.
- Default value: `'"'`

#### `terminator`

- Specifies the line terminator.
- Default value: `""`, which means both `"\n"` (LF) and `"\r\n"` (CRLF) are line terminators.

#### `header`

- Controls whether the CSV files contain a header.
- Value options:
    - `true`: TiDB Lightning treats the first row as a table header and does not import it as data.
    - `false`: the first row is also imported as CSV data.

#### `header-schema-match`

- Controls whether the column names in the CSV file header are matched to those defined in the target table.
- The default value is `true`, which means that you have confirmed that the column names in the CSV header are consistent with those in the target table, so that even if the order of the columns is different between the two, TiDB Lightning can still import the data successfully by mapping the column names.
- If the column names between the CSV table header and the target table do not match (for example, some column names in the CSV table header cannot be found in the target table) but the column order is the same, set this configuration to `false`. In this scenario, TiDB Lightning will ignore the CSV header to avoid errors and import the data directly in the order of the columns in the target table. Therefore, if the columns are not in the same order, you need to manually adjust the order of the columns in the CSV file to be consistent with that in the target table before importing; otherwise data discrepancies might occur.
- Default value: `true`
- Value options: `true`, `false`

> **Note:**
>
> This parameter only applies if the `header` parameter is set to `true`. If `header` is set to `false`, it means that the CSV file does not contain a header, so this parameter is not relevant.

#### `not-null`

- Controls whether the CSV contains any NULL value.
- Value options:
    - `true`: all columns from CSV cannot be NULL.
    - `false`: CSV can contain NULL values.

#### `null`

- When `not-null` is `false` (that is, CSV can contain NULL), fields equal to this value will be treated as NULL.

<!-- Example: `'\N'` -->

#### `backslash-escape`

- Controls whether to interpret backslash escapes inside fields.

<!-- Example: `true` -->

#### `trim-last-separator`

- Controls whether to remove it if a line ends with a separator.

<!-- Example: `false` -->

### mydumper.files

#### `pattern`

- Expression used for parsing AWS Aurora parquet files.
- Example: `'(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'`

#### `schema`

- Example: `'$1'`

#### `table`

- Example: `'$2'`

#### `type`

- Example: `'$3'`

### tidb

#### `host`

- Configuration of any TiDB server from the cluster.

<!-- Example: `"172.16.31.1"` -->

#### `port`

- Example: `4000`

#### `user`

- Example: `"root"`

#### `password`

- Configure the password to connect to TiDB. The password can either be plaintext or Base64 encoded.

#### `status-port`

- Fetches the table schema information from TiDB.

<!-- Example: `10080` -->

#### `pd-addr`

- Specifies the address of any PD server from the cluster. Starting from v7.6.0, TiDB supports setting multiple PD addresses.

<!-- Example: `"172.16.31.4:2379,56.78.90.12:3456"` -->

#### `log-level`

- Controls the log level of the TiDB library. TiDB Lightning imports TiDB as a library and generates some logs itself.

<!-- Example: `"error"` -->

#### `build-stats-concurrency`

- Sets the TiDB session variable to speed up the Checksum and Analyze operations. For more information, see [Control `ANALYZE` concurrency](/statistics.md#control-analyze-concurrency).

<!-- Example: `20` -->

#### `distsql-scan-concurrency`

- Sets the TiDB session variable to speed up the Checksum and Analyze operations. For more information, see [Control `ANALYZE` concurrency](/statistics.md#control-analyze-concurrency).
- If [`checksum-via-sql`](#checksum-via-sql) is set to `"true"`, TiDB Lightning will execute the `ADMIN CHECKSUM TABLE <table>` SQL statement to perform the Checksum operation on TiDB. In this case, the following parameters `distsql-scan-concurrency` and `checksum-table-concurrency` will not take effect.

<!-- Example: `15` -->

#### `index-serial-scan-concurrency`

- Sets the TiDB session variable to speed up the Checksum and Analyze operations. For more information, see [Control `ANALYZE` concurrency](/statistics.md#control-analyze-concurrency).

<!-- Example: `20` -->

#### `checksum-table-concurrency`

- Sets the TiDB session variable to speed up the Checksum and `ANALYZE` operations. For more information, see [Control `ANALYZE` concurrency](/statistics.md#control-analyze-concurrency).
- If [`checksum-via-sql`](#checksum-via-sql) is set to `"true"`, TiDB Lightning will execute the `ADMIN CHECKSUM TABLE <table>` SQL statement to perform the Checksum operation on TiDB. In this case, the following parameters `distsql-scan-concurrency` and `checksum-table-concurrency` will not take effect.

<!-- Example: `2` -->

#### `sql-mode`

- Specifies the default SQL mode used to parse and execute the SQL statements.

<!-- Example: `"ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"` -->

#### `max-allowed-packet`

- Sets maximum packet size allowed for SQL connections.
- Set this to `0` to automatically fetch the `max_allowed_packet` variable from server on every connection.

<!-- Example: `67_108_864` -->

#### `tls`

- Controls whether to use TLS for SQL connections.
- Value options:
    * `""`: forces TLS (the same as "cluster") if the [`[tidb.security]`](#tidbsecurity) section is populated. Otherwise, the same as `"false"`.
    * `"false"`: disables TLS.
    * `"cluster"`: forces TLS and verifies the server's certificate with the CA specified in the [`[tidb.security]`](#tidbsecurity) section.
    * `"skip-verify"`: forces TLS but does not verify the server's certificate. Note that this setting is insecure.
    * `"preferred"`: the same as `"skip-verify"`, but if the server does not support TLS, fall back to the unencrypted connection.

### tidb.security

- Specifies certificates and keys for TLS-enabled MySQL connections.
- Default value: the copy of the [`security`](#security) section.

#### `ca-path`

- Specifies the public certificate of the CA. Set to the empty string if you want to disable TLS for SQL.

<!-- Example: `"/path/to/ca.pem"` -->

#### `cert-path`

- Specifies the public certificate of this service.
- Default value: the copy of [`security.cert-path`](#cert-path).

<!-- Example: `"/path/to/lightning.pem"` -->

#### `key-path`

- Specifies the private key of this service.
- Default value: the copy of [`security.key-path`](#key-path).

<!-- Example: `"/path/to/lightning.key"` -->

### tidb.session-vars

Specifies other TiDB session variables.

<!-- tidb_enable_clustered_index = "OFF" -->

### post-restore

- In the physical import mode, when data importing is complete, TiDB Lightning can automatically perform the Checksum and `ANALYZE` operations.
- It is recommended to leave these as true in the production environment.
- The execution order: Checksum -> `ANALYZE`.
- Note that in the logical import mode, Checksum and `ANALYZE` operations are not needed, and they are always skipped in the actual operation.

#### `checksum`

- Specifies whether to perform `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after importing.
- Default value: `"required"`. Starting from v4.0.8, the default value is changed from `"true"` to `"required"`.
- Value options:
    - `"required"`: Perform admin checksum. If checksum fails, TiDB Lightning will exit with failure.
    - `"optional"`: Perform admin checksum. If checksum fails, TiDB Lightning will report a WARN log but ignore any error.
    - `"off"`: Do not perform checksum.
- Checksum failure usually means import exception (data loss or inconsistency). It is recommended to always enable checksum.
- For backward compatibility, bool values `true` and `false` are also allowed for this field. `true` is equivalent to `required` and `false` is equivalent to `off`.

#### `checksum-via-sql`

- Specifies whether the `ADMIN CHECKSUM TABLE <table>` operation is executed via TiDB.
- Default value: `"false"`
- Value options:
    - `"false"`: the `ADMIN CHECKSUM TABLE <table>` command is sent to TiKV for execution via TiDB Lightning.
    - `"true"`: if you want to adjust concurrency when this value is `"true"`, you need to set the [`tidb_checksum_table_concurrency`](/system-variables.md#tidb_checksum_table_concurrency) variable in TiDB.
- It is recommended that you set this value to `"true"` to make it easier to locate the problem if checksum fails.

#### `analyze`

- Specifies whether to perform `ANALYZE TABLE <table>` for each table after checksum is done.
- Default value: `"optional"`
- Value options: `"required"`, `"optional"`, `"off"`

### cron

- Configures the background periodic actions.
- Supported units: h (hour), m (minute), s (second).

#### `switch-mode`

- Specifies the duration between which TiDB Lightning automatically refreshes the import mode status. Should be shorter than the corresponding TiKV setting.

<!-- Example: `"5m"` -->

#### `log-progress`

- Specifies the duration between which an import progress is printed to the log.

<!-- Example: `"5m"` -->

#### `check-disk-quota`

- Specifies the time interval for checking the local disk quota when you use the physical import mode.
- Default value: `"60s"`, which means 60 seconds.

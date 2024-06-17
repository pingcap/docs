---
title: TiDB Lightning Configuration
summary: Learn about the CLI usage and sample configuration in TiDB Lightning.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-configuration/','/docs/dev/reference/tools/tidb-lightning/config/']
---

# TiDB Lightning Configuration

This document provides samples for global configuration and task configuration, and describes the usage of command-line parameters.

## Configuration files

TiDB Lightning has two configuration classes: "global" and "task", and they have compatible structures. Their distinction arises only when the [server mode](/tidb-lightning/tidb-lightning-web-interface.md) is enabled. When server mode is disabled (the default), TiDB Lightning will only execute one task, and the same configuration file is used for both global and task configurations.

### TiDB Lightning (Global)

```toml
### tidb-lightning global configuration

[lightning]
# The HTTP port for displaying the web interface, pulling Prometheus metrics, exposing debug data,
# and submitting import tasks (in server mode). Setting it to 0 disables the port.
status-addr = ':8289'

# Server mode. Defaults to false, which means an import task starts immediately after you execute the command.
# If this value is set to true, after you execute the command,
# TiDB Lightning waits until you submit an import task in the web interface.
# See the "TiDB Lightning Web Interface" section for details.
server-mode = false

# Logging
level = "info"
file = "tidb-lightning.log"
max-size = 128 # MB
max-days = 28
max-backups = 14

# Controls whether to enable the diagnostic logs. The default value is false, that is, only the logs related to the import are output, and the logs of other dependent components are not output.
# When you set it to true, logs from both the import process and other dependent components are output, and GRPC debugging is enabled, which can be used for diagnosis.
# This parameter is introduced in v7.3.0.
enable-diagnose-logs = false
```

### TiDB Lightning (Task)

```toml
### tidb-lightning task configuration

[lightning]
# Checks whether the cluster satisfies the minimum requirement before starting the task, and check whether TiKV has more than 10% free space left during running time.
#check-requirements = true

# The maximum number of engines to be opened concurrently.
# Each table is split into one "index engine" to store indices, and multiple
# "data engines" to store row data. These settings control the maximum
# concurrent number for each type of engines. Generally, you can use the following two default values.
index-concurrency = 2
table-concurrency = 6

# The concurrency number of data. It is set to the number of logical CPU
# cores by default. When deploying together with other components, you can
# set it to 75% of the size of logical CPU cores to limit the CPU usage.
# region-concurrency =

# The maximum I/O concurrency. Excessive I/O concurrency causes an increase in
# I/O latency because the disk's internal buffer is frequently refreshed,
# which causes the cache miss and slows down the read speed. Depending on the storage
# medium, this value might need to be adjusted for optimal performance.
io-concurrency = 5

# The maximum number of non-fatal errors to tolerate before stopping TiDB Lightning.
# Non-fatal errors are localized to a few rows, and ignoring those rows allows the import process to continue.
# Setting this to N means that TiDB Lightning will stop as soon as possible when the (N+1)-th error is encountered.
# The skipped rows will be inserted into tables inside the "task info" schema on the target TiDB, which can be configured below.
# The default value is `MaxInt64` bytes, that is, 9223372036854775807 bytes.
max-error = 0
# task-info-schema-name is the name of the schema or database that stores TiDB Lightning execution results.
# To disable error recording, set this to an empty string.
# task-info-schema-name = 'lightning_task_info'

# In parallel import mode, the schema name that stores the meta information for each TiDB Lightning instance in the target cluster.
# By default, the value is "lightning_metadata".
# Configure this parameter only if parallel import is enabled.
# **Note:**
# - The value set for this parameter must be the same for each TiDB Lightning instance
#   that participates in the same parallel import; otherwise, the correctness of the imported data cannot be ensured.
# - If parallel import mode is enabled, make sure that the user used for import (for the tidb.user configuration)
#   has permissions to create and access the databases corresponding to this configuration.
# - TiDB Lightning removes this schema after the import is completed.
#   So do not use any existing schema name to configure this parameter.
meta-schema-name = "lightning_metadata"

[security]
# Specifies certificates and keys for TLS connections within the cluster.
# Public certificate of the CA. Leave empty to disable TLS.
# ca-path = "/path/to/ca.pem"
# Public certificate of this service.
# cert-path = "/path/to/lightning.pem"
# Private key of this service.
# key-path = "/path/to/lightning.key"

[checkpoint]
# Whether to enable checkpoints.
# While importing data, TiDB Lightning records which tables have been imported, so
# even if TiDB Lightning or another component crashes, you can start from a known
# good state instead of restarting from scratch.
enable = true
# The schema name (database name) to store the checkpoints.
schema = "tidb_lightning_checkpoint"
# Where to store the checkpoints.
#  - file:  store as a local file.
#  - mysql: store into a remote MySQL-compatible database
driver = "file"
# The data source name (DSN) indicating the location of the checkpoint storage.
# For the "file" driver, the DSN is a path. If the path is not specified, TiDB Lightning would
# default to "/tmp/CHECKPOINT_SCHEMA.pb".
# For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
# If the URL is not specified, the TiDB server from the [tidb] section is used to
# store the checkpoints. You should specify a different MySQL-compatible
# database server to reduce the load of the target TiDB cluster.
# dsn = "/tmp/tidb_lightning_checkpoint.pb"
# Whether to keep the checkpoints after all data are imported. If false, the
# checkpoints will be deleted. Keeping the checkpoints can aid debugging but
# will leak metadata about the data source.
# keep-after-success = false

[conflict]
# Starting from v7.3.0, a new version of strategy is introduced to handle conflicting data. The default value is "". Starting from v8.0.0, TiDB Lightning optimizes the conflict strategy for both physical and logical import modes.
# - "": in the physical import mode, TiDB Lightning does not detect or handle conflicting data. If the source file contains conflicting primary or unique key records, the subsequent step reports an error. In the logical import mode, TiDB Lightning converts the "" strategy to the "error" strategy for processing.
# - "error": when detecting conflicting primary or unique key records in the imported data, TiDB Lightning terminates the import and reports an error.
# - "replace": when encountering conflicting primary or unique key records, TiDB Lightning retains the latest data and overwrites the old data.
#              The conflicting data are recorded in the `lightning_task_info.conflict_error_v2` table (recording conflicting data detected by post-import conflict detection in the physical import mode) and the `conflict_records` table (recording conflicting data detected by preprocess conflict detection in both logical and physical import modes) of the target TiDB cluster.
#              If you set `conflict.strategy = "replace"` in physical import mode, the conflicting data can be checked in the `lightning_task_info.conflict_view` view.
#              You can manually insert the correct records into the target table based on your application requirements. Note that the target TiKV must be v5.2.0 or later versions.
# - "ignore": when encountering conflicting primary or unique key records, TiDB Lightning retains the old data and ignores the new data. This option can only be used in the logical import mode.
strategy = ""
# Controls whether to enable preprocess conflict detection, which checks conflicts in data before importing it to TiDB. The default value is false, indicating that TiDB Lightning only checks conflicts after the import. If you set it to true, TiDB Lightning checks conflicts both before and after the import. This parameter can be used only in the physical import mode. In scenarios where the number of conflict records is greater than 1,000,000, it is recommended to set `precheck-conflict-before-import = true` for better performance in conflict detection. In other scenarios, it is recommended to disable it.
# precheck-conflict-before-import = false
# Controls the maximum number of conflict errors that can be handled when strategy is "replace" or "ignore". You can set it only when the strategy is "replace" or "ignore". The default value is 10000. If you set a value larger than 10000, the import process might experience performance degradation.
# threshold = 10000
# Controls the maximum number of records in the `conflict_records` table. The default value is 10000. 
# Starting from v8.1.0, there is no need to configure `max-record-rows` manually, because TiDB Lightning automatically assigns the value of `max-record-rows` with the value of `threshold`, regardless of the user input. `max-record-rows` will be deprecated in a future release.
# In the physical import mode, if the strategy is "replace", the conflict records that are overwritten are recorded.
# In the logical import mode, if the strategy is "ignore", the conflict records that are ignored are recorded; if the strategy is "replace", the conflict records are not recorded.
# max-record-rows = 10000

[tikv-importer]
# "local": Physical import mode, used by default. It applies to large dataset import,
# for example, greater than 1 TiB. However, during the import, downstream TiDB is not available to provide services.
# "tidb": Logical import mode. You can use this mode for small dataset import,
# for example, smaller than 1 TiB. During the import, downstream TiDB is available to provide services.
# backend = "local"
# Whether to enable multiple TiDB Lightning instances (in physical import mode) to import data to one or more target tables in parallel.
# The default value is `false`.
# When you use parallel import mode, you must set the parameter to `true`,
# but the premise is that no data exists in the target table, that is, all data can only be imported by TiDB Lightning.
# Note that this parameter is only used in scenarios where the target table is empty.
# parallel-import = false

# The `duplicate-resolution` parameter is deprecated starting from v8.0.0 and will be removed in a future release. For more information, see <https://docs.pingcap.com/tidb/dev/tidb-lightning-physical-import-mode-usage#the-old-version-of-conflict-detection-deprecated-in-v800>.
# Whether to detect and resolve duplicate records (unique key conflict) in the physical import mode.
# The following resolution algorithms are supported:
#  - none: does not detect duplicate records, which has the best performance of the two algorithms.
#          But if there are duplicate records in the data source, it might lead to inconsistent data in the target TiDB.
#  - remove: if there are primary key or unique key conflicts between the inserting data A and B,
#            A and B will be removed from the target table and recorded
#            in the `lightning_task_info.conflict_error_v1` table in the target TiDB.
#            You can manually insert the correct records into the target table based on your business requirements.
#            Note that the target TiKV must be v5.2.0 or later versions; otherwise it falls back to 'none'.
# The default value is 'none'.
# duplicate-resolution = 'none'
# The maximum number of KV pairs in one request when sending data to TiKV in physical import mode.
# Starting from v7.2.0, this parameter is deprecated and no longer takes effect after it is set.
# If you want to adjust the amount of data sent to TiKV in one request, use the `send-kv-size` parameter instead.
# send-kv-pairs = 32768
# The maximum size of one request when sending data to TiKV in physical import mode.
# The default value is "16K". It is not recommended to adjust this parameter.
# This parameter is introduced in v7.2.0.
# send-kv-size = "16K"
# Whether to enable compression when sending KV pairs to TiKV in the physical import mode.
# Currently, only the Gzip compression algorithm is supported.
# To use this algorithm, you can fill in either "gzip" or "gz" for this parameter.
# By default, the compression is not enabled.
# compress-kv-pairs = ""
# The directory of local KV sorting in the physical import mode. If the disk
# performance is low (such as in HDD), it is recommended to set the directory
# on a different disk from `data-source-dir` to improve import speed.
# sorted-kv-dir = ""
# The concurrency that TiKV writes KV data in the physical import mode.
# When the network transmission speed between TiDB Lightning and TiKV
# exceeds 10 Gigabit, you can increase this value accordingly.
# range-concurrency = 16
# Limits the bandwidth in which TiDB Lightning writes data into each TiKV
# node in the physical import mode. 0 by default, which means no limit.
# store-write-bwlimit = "128MiB"

# Specifies the disk quota for local temporary files when physical import mode is used.
# When the disk quota is insufficient, TiDB Lightning stops reading source data and writing temporary files,
# but prioritizes writing the already sorted key-value pairs to TiKV.
# After TiDB Lightning deletes the local temporary files, the import process continues.
# This option takes effect only when you set the `backend` option to `local`.
# The default value is `MaxInt64` bytes, that is, 9223372036854775807 bytes.
# disk-quota = "10GB"

# Specifies whether Physical Import Mode adds indexes via SQL.
# The default value is `false`, which means that TiDB Lightning will encode both row data and index data
# into KV pairs and import them into TiKV together.
# This mechanism is consistent with that of the historical versions.
# If you set it to `true`, it means that TiDB Lightning adds indexes via SQL after importing the row data.
# The benefit of adding indexes via SQL is that you can separately import data and import indexes,
# and import data more quickly. After the data is imported, even if the indexes fail to be added,
# it does not affect the consistency of the imported data.
# add-index-by-sql = false

# When you use TiDB Lightning to import a multi-tenant TiDB cluster, use this parameter to specify the corresponding key space name.
# The default value is an empty string, which means TiDB Lightning will automatically get the key space name of the corresponding tenant to import data.
# If you specify a value, the specified key space name will be used to import data.
# keyspace-name = ""

# In Physical Import Mode, this parameter controls the scope in which TiDB Lightning stops PD scheduling.
# The value options are as follows:
# - "table": pause scheduling only for the Region that stores the target table data. The default value is "table".
# - "global": pause global scheduling. When importing data to a cluster without any business traffic,
#   it is recommended to set this parameter to "global" to avoid interference from other scheduling.
# pause-pd-scheduler-scope = "table"

# In Physical Import Mode, this parameter controls the number of Regions when splitting Regions in a batch.
# The maximum number of Regions that can be split at the same time per TiDB Lightning instance is:
# region-split-batch-size * region-split-concurrency * table-concurrency
# This parameter is introduced in v7.1.0. The default value is `4096`.
# region-split-batch-size = 4096

# In Physical Import Mode, this parameter controls the concurrency when splitting Regions.
# The default value is the number of CPU cores.
# This parameter is introduced in v7.1.0.
# region-split-concurrency =

# In Physical Import Mode, this parameter controls the number of retries to wait for the Region to come online
# after the split and scatter operations.
# The default value is `1800` and the maximum retry interval is two seconds.
# The number of retries will not be increased if any Region becomes online between retries.
# This parameter is introduced in v7.1.0.
# region-check-backoff-limit = 1800

# In Physical Import Mode, this parameter controls the I/O block size for sorting local files. When the disk IOPS is a bottleneck, you can increase this value to improve data import performance.
# This parameter is introduced in v7.6.0. The default value is "16KiB". The value must be greater than or equal to `1B`. Note that if you only specify a number (for example, `16`), the unit is Byte instead of KiB.
# block-size = "16KiB"

# In Logical Import Mode, this parameter controls the size of each SQL statement executed on the downstream TiDB server.
# This parameter is introduced in v8.0.0.
# It specifies the expected size of the VALUES part of each INSERT or REPLACE statement in a single transaction.
# This parameter is not a hard limit. The actual SQL executed might be longer or shorter, depending on the actual content imported.
# The default value is "96KiB", which is optimized for import speed when TiDB Lightning is the only client of the cluster.
# Due to the implementation details of TiDB Lightning, the value is capped at 96 KiB. Setting a larger value will not take effect.
# You can decrease this value to reduce the stress on the cluster due to large transactions.
# logical-import-batch-size = "96KiB"

# In Logical Import Mode, this parameter controls the maximum number of rows inserted per transaction.
# This parameter is introduced in v8.0.0. The default value is `65536` rows.
# When both `logical-import-batch-size` and `logical-import-batch-rows` are specified, the parameter whose value reaches its threshold first will take effect.
# You can decrease this value to reduce the stress on the cluster due to large transactions.
# logical-import-batch-rows = 65536

[mydumper]
# Block size for file reading. Keep it longer than the longest string of the data source.
read-block-size = "64KiB" # default value

# The engine file needs to be imported sequentially. Due to parallel processing,
# multiple data engines will be imported at nearly the same time, and this
# creates a queue and wastes resources. Therefore, TiDB Lightning slightly
# increases the size of the first few batches to properly distribute
# resources. The scale up factor is controlled by this parameter, which
# expresses the ratio of duration between the "import" and "write" steps
# with full concurrency. This can be calculated by using the ratio
# (import duration/write duration) of a single table of size around 1 GiB.
# The exact timing can be found in the log. If "import" is faster, the batch
# size variance is smaller, and a ratio of zero means a uniform batch size.
# This value should be in the range (0 <= batch-import-ratio < 1).
batch-import-ratio = 0.75

# Local source data directory or the URI of the external storage.
# For more information about the URI of the external storage, see https://docs.pingcap.com/tidb/v6.6/backup-and-restore-storages#uri-format.
data-source-dir = "/data/my_database"

# The character set of the schema files, containing CREATE TABLE statements;
# only supports one of:
#  - utf8mb4: the schema files must be encoded as UTF-8; otherwise, an error is reported.
#  - gb18030: the schema files must be encoded as GB-18030; otherwise,
#             an error is reported
#  - auto:    (default) automatically detects whether the schema is UTF-8 or
#             GB-18030. An error is reported if the encoding is neither.
#  - latin1:  the schema files use MySQL latin1 encoding, also known as Code Page 1252.
#  - binary:  do not try to decode the schema files
character-set = "auto"

# Specifies the character set of the source data file.
# Lightning converts the source file from the specified character set to UTF-8 encoding when importing.
# Currently, this configuration only specifies the character set of the CSV files with the following options supported:
# - utf8mb4: Indicates that the source data file uses UTF-8 encoding.
# - GB18030: Indicates that the source data file uses the GB-18030 encoding.
# - GBK: The source data file uses GBK encoding (GBK encoding is an extension of the GB-2312 character set, also known as Code Page 936).
# - latin1: The source data file uses MySQL latin1 encoding, also known as Code Page 1252.
# - binary: Indicates that Lightning does not convert the encoding (by default).
# If left blank, the default value "binary" is used, that is to say, Lightning does not convert the encoding.
# Note that Lightning does not predict about the character set of the source data file
# and only converts the source file and import the data based on this configuration.
# If the value of this configuration is not the same as the actual encoding of the source data file,
# a failed import, data loss or data disorder might appear.
data-character-set = "binary"
# Specifies the replacement character in case of incompatible characters during the character set conversion of the source data file.
# This configuration must not be duplicated with field separators, quote definers, and line breaks.
# The default value is "\uFFFD", which is the "error" Rune or Unicode replacement character in UTF-8 encoding.
# Changing the default value might result in potential degradation of parsing performance for the source data file.
data-invalid-char-replace = "\uFFFD"

# the input data in a "strict" format speeds up processing.
# "strict-format = true" requires that:
# in CSV, every value cannot contain literal new lines (U+000A and U+000D, or \r and \n) even
# when quoted, which means new lines are strictly used to separate rows.
# "Strict" format allows TiDB Lightning to quickly locate split positions of a large file for parallel processing.
# However, if the input data is not "strict", it may split a valid data in half and
# corrupt the result.
# The default value is false for safety instead of speed.
strict-format = false

# If strict-format is true, TiDB Lightning splits large CSV files into multiple chunks to process in
# parallel. max-region-size is the maximum size of each chunk after splitting.
# max-region-size = "256MiB" # default value

# Only import tables if these wildcard rules are matched. See the corresponding section for details.
filter = ['*.*', '!mysql.*', '!sys.*', '!INFORMATION_SCHEMA.*', '!PERFORMANCE_SCHEMA.*', '!METRICS_SCHEMA.*', '!INSPECTION_SCHEMA.*']

# Configures how CSV files are parsed.
[mydumper.csv]
# Separator between fields. Must not be empty.
separator = ','
# Quoting delimiter. Empty value means no quoting.
delimiter = '"'
# Line terminator. Empty value means both "\n" (LF) and "\r\n" (CRLF) are line terminators.
terminator = ''
# Whether the CSV files contain a header.
# If `header` is true, TiDB Lightning treats the first row as a table header and does not import it as data.
# If `header` is false, the first row is also imported as CSV data.
header = true
# Whether the column names in the CSV file header are matched to those defined in the target table.
# The default value is `true`, which means that you have confirmed that the column names in the CSV header
# are consistent with those in the target table, so that even if the order of the columns is different between the two,
# TiDB Lightning can still import the data successfully by mapping the column names.
# If the column names between the CSV table header and the target table do not match
# (for example, some column names in the CSV table header cannot be found in the target table)
# but the column order is the same, set this configuration to `false`.
# In this scenario, TiDB Lightning will ignore the CSV header to avoid errors and import the data
# directly in the order of the columns in the target table.
# Therefore, if the columns are not in the same order,
# you need to manually adjust the order of the columns in the CSV file to be consistent with that
# in the target table before importing;
# otherwise data discrepancies might occur.
# It is important to note that this parameter only applies if the `header` parameter is set to `true`.
# If `header` is set to `false`, it means that the CSV file does not contain a header,
# so this parameter is not relevant.
header-schema-match = true
# Whether the CSV contains any NULL value.
# If `not-null` is true, all columns from CSV cannot be NULL.
not-null = false
# When `not-null` is false (that is, CSV can contain NULL),
# fields equal to this value will be treated as NULL.
null = '\N'
# Whether to interpret backslash escapes inside fields.
backslash-escape = true
# If a line ends with a separator, remove it.
trim-last-separator = false

# [[mydumper.files]]
# Expression used for parsing AWS Aurora parquet files
# pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
# schema = '$1'
# table = '$2'
# type = '$3'

[tidb]
# Configuration of any TiDB server from the cluster.
host = "172.16.31.1"
port = 4000
user = "root"
# Configure the password to connect to TiDB. The password can either be plaintext or Base64 encoded.
password = ""
# Table schema information is fetched from TiDB via this status-port.
status-port = 10080
# Address of any PD server from the cluster. Starting from v7.6.0, TiDB supports setting multiple PD addresses.
pd-addr = "172.16.31.4:2379,56.78.90.12:3456"
# tidb-lightning imports TiDB as a library and generates some logs itself.
# This setting controls the log level of the TiDB library.
log-level = "error"

# Sets the TiDB session variable to speed up the Checksum and Analyze operations. Note that if checksum-via-sql is set to "true", TiDB Lightning will execute the ADMIN CHECKSUM TABLE <table> SQL statement to perform the Checksum operation on TiDB. In this case, the following parameters `distsql-scan-concurrency` and `checksum-table-concurrency` will not take effect.
# See https://docs.pingcap.com/tidb/stable/statistics#control-analyze-concurrency
# for the meaning of each setting
build-stats-concurrency = 20
distsql-scan-concurrency = 15
index-serial-scan-concurrency = 20
checksum-table-concurrency = 2

# Sets other TiDB session variables
# [tidb.session-vars]
# tidb_enable_clustered_index = "OFF"

# The default SQL mode used to parse and execute the SQL statements.
sql-mode = "ONLY_FULL_GROUP_BY,NO_AUTO_CREATE_USER"
# Sets maximum packet size allowed for SQL connections.
# Set this to 0 to automatically fetch the `max_allowed_packet` variable from server on every connection.
max-allowed-packet = 67_108_864

# Whether to use TLS for SQL connections. Valid values are:
#  * ""            - force TLS (same as "cluster") if [tidb.security] section is populated, otherwise same as "false"
#  * "false"       - disable TLS
#  * "cluster"     - force TLS and verify the server's certificate with the CA specified in the [tidb.security] section
#  * "skip-verify" - force TLS but do not verify the server's certificate (insecure!)
#  * "preferred"   - same as "skip-verify", but if the server does not support TLS, fallback to unencrypted connection
# tls = ""

# Specifies certificates and keys for TLS-enabled MySQL connections.
# Defaults to a copy of the [security] section.
# [tidb.security]
# Public certificate of the CA. Set to empty string to disable TLS for SQL.
# ca-path = "/path/to/ca.pem"
# Public certificate of this service. Default to copy of `security.cert-path`
# cert-path = "/path/to/lightning.pem"
# Private key of this service. Default to copy of `security.key-path`
# key-path = "/path/to/lightning.key"

# In the physical import mode, when data importing is complete, TiDB Lightning can
# automatically perform the Checksum and Analyze operations. It is recommended
# to leave these as true in the production environment.
# The execution order: Checksum -> Analyze.
# Note that in the logical import mode, Checksum and Analyze is not needed, and they are always
# skipped in the actual operation.
[post-restore]
# Specifies whether to perform `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity after importing.
# The following options are available:
# - "required" (default value): Perform admin checksum. If checksum fails, TiDB Lightning will exit with failure.
# - "optional": Perform admin checksum. If checksum fails, TiDB Lightning will report a WARN log but ignore any error.
# - "off": Do not perform checksum.
# Note that since v4.0.8, the default value has changed from "true" to "required".
# Note:
# 1. Checksum failure usually means import exception (data loss or inconsistency). It is recommended to always enable checksum.
# 2. For backward compatibility, bool values "true" and "false" are also allowed for this field.
# "true" is equivalent to "required" and "false" is equivalent to "off".
checksum = "required"
# Specifies whether the ADMIN CHECKSUM TABLE <table> operation is executed via TiDB.
# The default value is "false", which means that the ADMIN CHECKSUM TABLE <table> command is sent to TiKV for execution via TiDB Lightning.
# It is recommended that you set this value to "true" to make it easier to locate the problem if checksum fails.
# Meanwhile, if you want to adjust concurrency when this value is "true", you need to set the `tidb_checksum_table_concurrency` variable in TiDB (https://docs.pingcap.com/tidb/stable/system-variables#tidb_checksum_table_concurrency).
checksum-via-sql = "false"
# Specifies whether to perform `ANALYZE TABLE <table>` for each table after checksum is done.
# Options available for this field are the same as `checksum`. However, the default value for this field is "optional".
analyze = "optional"

# Configures the background periodic actions.
# Supported units: h (hour), m (minute), s (second).
[cron]
# Duration between which TiDB Lightning automatically refreshes the import mode
# status. Should be shorter than the corresponding TiKV setting.
switch-mode = "5m"
# Duration between which an import progress is printed to the log.
log-progress = "5m"
# The time interval for checking the local disk quota when you use the physical import mode.
# The default value is 60 seconds.
# check-disk-quota = "60s"
```

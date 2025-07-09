---
title: BACKUP | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 BACKUP 的概述。
---

# BACKUP

此语句用于对 TiDB 集群进行分布式备份。

> **Warning:**
>
> - 该功能为实验性特性。不建议在生产环境中使用。此功能可能在未提前通知的情况下被更改或移除。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`BACKUP` 语句使用的引擎与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 相同，但备份过程由 TiDB 自身驱动，而非单独的 BR 工具。BR 的所有优点和警告也适用于此语句。

执行 `BACKUP` 需要拥有 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点和集群中的所有 TiKV 节点必须对目标存储具有读写权限。在启用 [Security Enhanced Mode](/system-variables.md#tidb_enable_enhanced_security) 时，不允许使用本地存储（存储路径以 `local://` 开头）。

`BACKUP` 语句会阻塞，直到整个备份任务完成、失败或被取消。建议准备长连接以执行 `BACKUP`。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消任务。

一次只能执行一个 `BACKUP` 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。如果在同一台 TiDB 服务器上已在执行 `BACKUP` 或 `RESTORE`，新发起的 `BACKUP` 将等待直到前一个任务完成。

`BACKUP` 仅能与 "tikv" 存储引擎配合使用。使用 "unistore" 引擎时，`BACKUP` 将失败。

## 概要

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "SNAPSHOT" '='? ( BackupTSO | LengthNum TimestampUnit "AGO" )

Boolean ::=
    NUM | "TRUE" | "FALSE"

BackupTSO ::=
    LengthNum | stringLit
```

## 示例

### 备份数据库

```sql
BACKUP DATABASE `test` TO 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+-----------------+---------------------+---------------------+
| Destination                  | Size      | BackupTS        | Queue Time          | Execution Time      |
+------------------------------+-----------+-----------------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 416099531454472 | 2020-04-12 23:09:48 | 2020-04-12 23:09:48 |
+------------------------------+-----------+-----------------+---------------------+---------------------+
1 row in set (58.453 sec)
```

上述示例中，`test` 数据库被备份到本地文件系统。数据以 SST 文件形式存储在 `/mnt/backup/2020/04/` 目录中，分布在所有 TiDB 和 TiKV 节点上。

第一行结果的描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 目标 URL |
| `Size` |  备份归档的总大小（字节） |
| `BackupTS` | 备份创建时的快照 TSO（对 [增量备份](#incremental-backup) 有用） |
| `Queue Time` | `BACKUP` 任务排队的时间（当前时区） |
| `Execution Time` | `BACKUP` 任务开始执行的时间（当前时区） |

### 备份表

```sql
BACKUP TABLE `test`.`sbtest01` TO 'local:///mnt/backup/sbtest01/';
```

```sql
BACKUP TABLE sbtest02, sbtest03, sbtest04 TO 'local:///mnt/backup/sbtest/';
```

### 备份整个集群

```sql
BACKUP DATABASE * TO 'local:///mnt/backup/full/';
```

注意，系统表（`mysql.*`、`INFORMATION_SCHEMA.*`、`PERFORMANCE_SCHEMA.*` 等）不会包含在备份中。

### 外部存储

BR 支持将数据备份到 S3 或 GCS：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 语法在 [外部存储服务的 URI 格式](/external-storage-uri.md) 中有详细说明。

在云环境中，若不希望分发凭证，可以将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 限制每个 TiKV 节点的平均上传速度，以减少网络带宽压力。

在备份完成之前，`BACKUP` 会对集群中的数据进行校验和（checksum）以确保正确性。如果你确信不需要此验证，可以通过将 `CHECKSUM` 参数设置为 `FALSE` 来禁用。

若要指定 BR 执行备份表和索引的并发任务数，可以使用 `CONCURRENCY` 参数。该参数控制 BR 内部的线程池大小，从而优化备份操作的性能和效率。

一个任务代表一个表范围或一个索引范围。对于一个有一个索引的表，使用两个任务来备份此表。`CONCURRENCY` 的默认值为 `4`。如果需要备份大量表或索引，可以增加其值。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### 快照

指定时间戳、TSO 或相对时间以备份历史数据。

```sql
-- 相对时间
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;

-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';

-- 时间戳 Oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

支持的相对时间单位有：

* MICROSECOND
* SECOND
* MINUTE
* HOUR
* DAY
* WEEK

注意，按照 SQL 标准，单位始终为单数。

### 增量备份

提供 `LAST_BACKUP` 选项，只备份自上次备份以来的变更数据。

```sql
-- 时间戳（当前时区）
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- 时间戳 Oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL 兼容性

此语句为 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)
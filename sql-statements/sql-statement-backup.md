---
title: BACKUP | TiDB SQL 语句参考
summary: TiDB 数据库 BACKUP 语句用法概述。
---

# BACKUP

该语句用于对 TiDB 集群执行分布式备份。

> **Warning:**
>
> - 该功能为实验性功能。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下更改或移除。如果你发现了 bug，可以在 GitHub 上提交一个 [issue](https://github.com/pingcap/tidb/issues)。
> - 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

`BACKUP` 语句使用与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 相同的引擎，不同之处在于备份过程由 TiDB 自身驱动，而不是由独立的 BR 工具驱动。BR 的所有优点和注意事项同样适用于该语句。

执行 `BACKUP` 需要 `BACKUP_ADMIN` 或 `SUPER` 权限。此外，执行备份的 TiDB 节点以及集群中的所有 TiKV 节点都必须对目标路径具有读写权限。当启用 [安全增强模式](/system-variables.md#tidb_enable_enhanced_security) 时，不允许使用本地存储（以 `local://` 开头的存储路径）。

`BACKUP` 语句会被阻塞，直到整个备份任务完成、失败或被取消。建议为执行 `BACKUP` 准备一个长时间保持的连接。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消该任务。

同一时间只能执行一个 `BACKUP` 和 [`RESTORE`](/sql-statements/sql-statement-restore.md) 任务。如果同一个 TiDB 服务器上已经有 `BACKUP` 或 `RESTORE` 语句在执行，新的 `BACKUP` 执行会等待所有之前的任务完成。

`BACKUP` 只能用于 "tikv" 存储引擎。使用 "unistore" 引擎执行 `BACKUP` 会失败。

## 语法

```ebnf+diagram
BackupStmt ::=
    "BACKUP" BRIETables "TO" stringLit BackupOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

BackupOption ::=
    "CHECKSUM" '='? Boolean
|   "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "COMPRESSION_LEVEL" '='? LengthNum
|   "COMPRESSION_TYPE" '='? stringLit
|   "CONCURRENCY" '='? LengthNum
|   "IGNORE_STATS" '='? Boolean
|   "LAST_BACKUP" '='? BackupTSO
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
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

在上面的示例中，`test` 数据库被备份到本地文件系统。数据以 SST 文件的形式保存在分布于所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录下。

上述结果的第一行各列说明如下：

| 列名 | 说明 |
| :-------- | :--------- |
| `Destination` | 目标 URL |
| `Size` |  备份归档的总大小，单位为字节 |
| `BackupTS` | 创建备份时快照的 TSO（对 [增量备份](#incremental-backup) 有用） |
| `Queue Time` | `BACKUP` 任务进入队列的时间戳（当前时区） |
| `Execution Time` | `BACKUP` 任务开始执行的时间戳（当前时区） |

### 备份数据表

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

注意，系统表（`mysql.*`、`INFORMATION_SCHEMA.*`、`PERFORMANCE_SCHEMA.*` 等）不会被包含在备份中。

### 外部存储

BR 支持将数据备份到 S3 或 GCS：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/?access-key={YOUR_ACCESS_KEY}&secret-access-key={YOUR_SECRET_KEY}';
```

URL 语法详见 [外部存储服务的 URI 格式](/external-storage-uri.md)。

在云环境下，如果不希望分发凭证，可以将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 可以限制每个 TiKV 节点的平均上传速度，以减少网络带宽占用。

在备份完成前，`BACKUP` 默认会对集群上的数据进行校验（checksum），以验证数据正确性。单表校验任务的默认并发数为 4，可以通过 `CHECKSUM_CONCURRENCY` 参数进行调整。如果你确信无需数据校验，可以将 `CHECKSUM` 参数设置为 `FALSE` 以关闭校验。

如需指定 BR 备份表和索引时可执行的并发任务数，可使用 `CONCURRENCY` 参数。该参数控制 BR 内部的线程池大小，从而优化备份操作的性能和效率。

根据备份的 schema，一个任务代表一个表范围或一个索引范围。例如，一个带有一个索引的表会使用两个任务进行备份。`CONCURRENCY` 的默认值为 `4`。如果需要备份大量表或索引，可以适当增加该值。

统计信息默认不会被备份。如需备份统计信息，需要将 `IGNORE_STATS` 参数设置为 `FALSE`。

默认情况下，备份生成的 SST 文件使用 `zstd` 压缩算法。如果需要，可以通过 `COMPRESSION_TYPE` 参数指定其他压缩算法。支持的算法包括 `lz4`、`zstd` 和 `snappy`。你还可以通过 `COMPRESSION_LEVEL` 参数调整压缩级别，级别数值越高，压缩比越高，但 CPU 消耗也越大。

```sql
BACKUP DATABASE `test` TO 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 8
    CHECKSUM = FALSE;
```

### 快照

可以指定时间戳、TSO 或相对时间来备份历史数据。

```sql
-- relative time
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist01'
    SNAPSHOT = 36 HOUR AGO;

-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    SNAPSHOT = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    SNAPSHOT = 415685305958400;
```

相对时间支持的单位有：

* MICROSECOND
* SECOND
* MINUTE
* HOUR
* DAY
* WEEK

注意，按照 SQL 标准，单位始终为单数形式。

### 增量备份

通过指定 `LAST_BACKUP` 选项，仅备份上次备份到当前快照之间的变更数据。

```sql
-- timestamp (in current time zone)
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist02'
    LAST_BACKUP = '2020-04-01 12:00:00';

-- timestamp oracle
BACKUP DATABASE `test` TO 'local:///mnt/backup/hist03'
    LAST_BACKUP = 415685305958400;
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [RESTORE](/sql-statements/sql-statement-restore.md)
* [SHOW BACKUPS](/sql-statements/sql-statement-show-backups.md)

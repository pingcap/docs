---
title: RESTORE | TiDB SQL 语句参考
summary: 关于 TiDB 数据库中 RESTORE 的用法概述。
---

# RESTORE

此语句执行从之前由 [`BACKUP` 语句](/sql-statements/sql-statement-backup.md) 生成的备份归档的分布式还原。

> **Warning:**
>
> - 此功能为实验性功能。不建议在生产环境中使用。此功能可能在未提前通知的情况下被更改或移除。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 此功能在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群中不可用。

`RESTORE` 语句使用与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 相同的引擎，但还原过程由 TiDB 自身驱动，而非单独的 BR 工具。BR 的所有优点和注意事项也适用于此。在此特别强调，**`RESTORE` 目前不符合 ACID**。在运行 `RESTORE` 之前，请确保满足以下条件：

* 集群处于“离线”状态，当前 TiDB 会话是唯一访问所有待还原表的活跃 SQL 连接。
* 执行全量还原时，待还原的表不应已存在，因为可能会覆盖已有数据，导致数据与索引不一致。
* 执行增量还原时，表应处于创建备份时的 `LAST_BACKUP` 时间戳的完全相同状态。

运行 `RESTORE` 需要具有 `RESTORE_ADMIN` 或 `SUPER` 权限。此外，执行还原的 TiDB 节点和集群中的所有 TiKV 节点都必须对目标具有读取权限。

`RESTORE` 是阻塞操作，只有在整个还原任务完成、失败或取消后才会结束。建议准备长连接以执行 `RESTORE`。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消任务。

每次只能执行一个 `BACKUP` 和 `RESTORE` 任务。如果在同一 TiDB 服务器上已有 `BACKUP` 或 `RESTORE` 任务在运行，新发起的 `RESTORE` 将等待所有之前的任务完成。

`RESTORE` 仅支持 "tikv" 存储引擎。使用 "unistore" 引擎执行 `RESTORE` 将失败。

## 概要语法

```ebnf+diagram
RestoreStmt ::=
    "RESTORE" BRIETables "FROM" stringLit RestoreOption*

BRIETables ::=
    "DATABASE" ( '*' | DBName (',' DBName)* )
|   "TABLE" TableNameList

RestoreOption ::=
    "CHECKSUM_CONCURRENCY" '='? LengthNum
|   "CONCURRENCY" '='? LengthNum
|   "CHECKSUM" '='? Boolean
|   "LOAD_STATS" '='? Boolean
|   "RATE_LIMIT" '='? LengthNum "MB" '/' "SECOND"
|   "SEND_CREDENTIALS_TO_TIKV" '='? Boolean
|   "WAIT_TIFLASH_READY" '='? Boolean
|   "WITH_SYS_TABLE" '='? Boolean

Boolean ::=
    NUM | "TRUE" | "FALSE"
```

## 示例

### 从备份归档还原

```sql
RESTORE DATABASE * FROM 'local:///mnt/backup/2020/04/';
```

```sql
+------------------------------+-----------+----------+---------------------+---------------------+
| Destination                  | Size      | BackupTS | Queue Time          | Execution Time      |
+------------------------------+-----------+----------+---------------------+---------------------+
| local:///mnt/backup/2020/04/ | 248665063 | 0        | 2020-04-21 17:16:55 | 2020-04-21 17:16:55 |
+------------------------------+-----------+----------+---------------------+---------------------+
1 row in set (28.961 sec)
```

上述示例中，所有数据从本地文件系统的备份归档中还原。数据以 SST 文件的形式，从 `/mnt/backup/2020/04/` 目录中读取，目录分布在所有 TiDB 和 TiKV 节点上。

第一行结果的描述如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 读取的目标 URL |
| `Size` |  备份归档的总大小（字节） |
| `BackupTS` | （未使用） |
| `Queue Time` | 以当前时区为准，`RESTORE` 任务排队的时间戳 |
| `Execution Time` | 以当前时区为准，`RESTORE` 任务开始执行的时间戳 |

### 部分还原

你可以指定要还原的数据库或表。如果备份归档中缺少某些数据库或表，它们将被忽略，`RESTORE` 将不执行任何操作而完成。

```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```

```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部存储

BR 支持从 S3 或 GCS 还原数据：

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 语法详见 [URI Formats of External Storage Services](/external-storage-uri.md)。

在云环境中，如果不希望分发凭证，可以将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 限制每个 TiKV 节点的平均下载速度，以减少网络带宽压力。

在还原完成之前，`RESTORE` 默认会对备份文件中的数据进行校验和验证，以确保正确性。单个表的校验和任务默认并发数为 4，可以通过 `CHECKSUM_CONCURRENCY` 参数调整。如果你确信数据验证不必要，可以将 `CHECKSUM` 参数设置为 `FALSE` 来禁用校验。

如果已备份统计信息，默认会在还原过程中一并还原统计信息。如果不需要还原统计信息，可以将 `LOAD_STATS` 参数设置为 `FALSE`。

<CustomContent platform="tidb">

系统 [privilege tables](/privilege-management.md#privilege-table) 默认会被还原。如果不需要还原系统权限表，可以将 `WITH_SYS_TABLE` 参数设置为 `FALSE`。

</CustomContent>

<CustomContent platform="tidb-cloud">

系统 [privilege tables](https://docs.pingcap.com/tidb/stable/privilege-management#privilege-table) 默认会被还原。如果不需要还原系统权限表，可以将 `WITH_SYS_TABLE` 参数设置为 `FALSE`。

</CustomContent>

默认情况下，还原任务在完成前不会等待 TiFlash 副本完全创建。如果需要等待，可以将 `WAIT_TIFLASH_READY` 参数设置为 `TRUE`。

```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 增量还原

没有专门的语法用于执行增量还原。TiDB 会自动识别备份归档是全量还是增量，并采取相应措施。你只需按正确的顺序应用每个增量还原。

例如，如果备份任务如下创建：

```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

那么在还原时也应按相同顺序执行：

```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)
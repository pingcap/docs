---
title: RESTORE | TiDB SQL 语句参考
summary: TiDB 数据库中 RESTORE 的用法概述。
---

# RESTORE

该语句用于从之前由 [`BACKUP` 语句](/sql-statements/sql-statement-backup.md) 生成的备份归档中执行分布式恢复操作。

> **Warning:**
>
> - 该功能为实验性功能。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下更改或移除。如果你发现了 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。
> - 该功能在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群中不可用。

`RESTORE` 语句使用与 [BR 工具](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview) 相同的引擎，不同之处在于恢复过程由 TiDB 自身驱动，而不是单独的 BR 工具。BR 的所有优点和注意事项在此同样适用。特别地，**`RESTORE` 目前不符合 ACID**。在运行 `RESTORE` 之前，请确保满足以下要求：

* 集群处于“离线”状态，当前 TiDB 会话是唯一访问所有被恢复表的活跃 SQL 连接。
* 当执行全量恢复时，被恢复的表不应已存在，否则现有数据可能会被覆盖，导致数据与索引之间不一致。
* 当执行增量恢复时，表应与创建备份时的 `LAST_BACKUP` 时间戳处于完全相同的状态。

运行 `RESTORE` 需要 `RESTORE_ADMIN` 或 `SUPER` 权限。此外，执行恢复的 TiDB 节点以及集群中的所有 TiKV 节点都必须拥有目标存储的读取权限。

`RESTORE` 语句为阻塞型，只有在整个恢复任务完成、失败或被取消后才会结束。建议为 `RESTORE` 准备一个长时间保持的连接。可以使用 [`KILL TIDB QUERY`](/sql-statements/sql-statement-kill.md) 语句取消该任务。

同一时间只能执行一个 `BACKUP` 或 `RESTORE` 任务。如果同一 TiDB 服务器上已有 `BACKUP` 或 `RESTORE` 任务在运行，新的 `RESTORE` 执行将会等待直到所有前序任务完成。

`RESTORE` 只能与 "tikv" 存储引擎配合使用。若与 "unistore" 引擎配合使用将会失败。

## 语法

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

### 从备份归档恢复


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

在上面的示例中，所有数据都从本地文件系统的备份归档中恢复。数据以 SST 文件的形式从分布在所有 TiDB 和 TiKV 节点的 `/mnt/backup/2020/04/` 目录中读取。

上述结果的第一行各列含义如下：

| 列名 | 描述 |
| :-------- | :--------- |
| `Destination` | 读取数据的目标 URL |
| `Size` | 备份归档的总大小，单位为字节 |
| `BackupTS` | （未使用） |
| `Queue Time` | `RESTORE` 任务进入队列的时间戳（当前时区） |
| `Execution Time` | `RESTORE` 任务开始执行的时间戳（当前时区） |

### 部分恢复

你可以指定要恢复的数据库或表。如果备份归档中缺少某些数据库或表，它们会被忽略，因此 `RESTORE` 会直接完成而不做任何操作。


```sql
RESTORE DATABASE `test` FROM 'local:///mnt/backup/2020/04/';
```


```sql
RESTORE TABLE `test`.`sbtest01`, `test`.`sbtest02` FROM 'local:///mnt/backup/2020/04/';
```

### 外部存储

BR 支持从 S3 或 GCS 恢复数据：


```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/';
```

URL 语法详见 [外部存储服务的 URI 格式](/external-storage-uri.md)。

在云环境下，如果不希望分发凭证，可以将 `SEND_CREDENTIALS_TO_TIKV` 选项设置为 `FALSE`：


```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-05/'
    SEND_CREDENTIALS_TO_TIKV = FALSE;
```

### 性能调优

使用 `RATE_LIMIT` 可以限制每个 TiKV 节点的平均下载速度，以减少网络带宽占用。

在恢复完成前，`RESTORE` 默认会对备份文件中的数据进行校验（checksum），以验证数据的正确性。单表校验任务的默认并发度为 4，你可以通过 `CHECKSUM_CONCURRENCY` 参数进行调整。如果你确信无需数据校验，可以将 `CHECKSUM` 参数设置为 `FALSE` 以关闭校验。

如果统计信息已被备份，恢复时默认会一并恢复。如果你不需要恢复统计信息，可以将 `LOAD_STATS` 参数设置为 `FALSE`。

<CustomContent platform="tidb">

系统 [权限表](/privilege-management.md#privilege-table) 默认会被恢复。如果你不需要恢复系统权限表，可以将 `WITH_SYS_TABLE` 参数设置为 `FALSE`。

</CustomContent>

<CustomContent platform="tidb-cloud">

系统 [权限表](https://docs.pingcap.com/tidb/stable/privilege-management#privilege-table) 默认会被恢复。如果你不需要恢复系统权限表，可以将 `WITH_SYS_TABLE` 参数设置为 `FALSE`。

</CustomContent>

默认情况下，恢复任务不会等待 TiFlash 副本完全创建后才完成。如果你需要恢复任务等待 TiFlash 副本就绪，可以将 `WAIT_TIFLASH_READY` 参数设置为 `TRUE`。


```sql
RESTORE DATABASE * FROM 's3://example-bucket-2020/backup-06/'
    RATE_LIMIT = 120 MB/SECOND
    CONCURRENCY = 64
    CHECKSUM = FALSE;
```

### 增量恢复

执行增量恢复无需特殊语法。TiDB 会自动识别备份归档是全量还是增量，并采取相应操作。你只需按正确顺序依次应用每个增量恢复。

例如，若备份任务如下创建：


```sql
BACKUP DATABASE `test` TO 's3://example-bucket/full-backup'  SNAPSHOT = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-1' SNAPSHOT = 414971854848000 LAST_BACKUP = 413612900352000;
BACKUP DATABASE `test` TO 's3://example-bucket/inc-backup-2' SNAPSHOT = 416353458585600 LAST_BACKUP = 414971854848000;
```

则恢复时应按相同顺序执行：


```sql
RESTORE DATABASE * FROM 's3://example-bucket/full-backup';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-1';
RESTORE DATABASE * FROM 's3://example-bucket/inc-backup-2';
```

## MySQL 兼容性

该语句为 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [BACKUP](/sql-statements/sql-statement-backup.md)
* [SHOW RESTORES](/sql-statements/sql-statement-show-backups.md)

---
title: IMPORT INTO
summary: TiDB 中 IMPORT INTO 的用法概述。
---

# IMPORT INTO

`IMPORT INTO` 语句允许你通过 TiDB Lightning 的 [物理导入模式](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode) 向 TiDB 导入数据。你可以通过以下两种方式使用 `IMPORT INTO`：

- `IMPORT INTO ... FROM FILE`：将 `CSV`、`SQL`、`PARQUET` 等格式的数据文件导入到 TiDB 的空表中。
- `IMPORT INTO ... FROM SELECT`：将 `SELECT` 语句的查询结果导入到 TiDB 的空表中。你也可以用它导入通过 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

<CustomContent platform="tidb">

> **Note:**
>
> 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 相比，`IMPORT INTO` 可以直接在 TiDB 节点上执行，支持自动化分布式任务调度和 [TiDB Global Sort](/tidb-global-sort.md)，在部署、资源利用率、任务配置便捷性、调用与集成易用性、高可用性和可扩展性等方面有显著提升。建议你在合适的场景下优先考虑使用 `IMPORT INTO` 替代 TiDB Lightning。

</CustomContent>

## 限制

- `IMPORT INTO` 仅支持向数据库中已存在的空表导入数据。
- 如果同一张表的其他分区已经有数据，`IMPORT INTO` 不支持向空分区导入数据。目标表必须完全为空才能进行导入操作。
- `IMPORT INTO` 不支持向 [临时表](/temporary-tables.md) 或 [缓存表](/cached-tables.md) 导入数据。
- `IMPORT INTO` 不支持事务或回滚。在显式事务（`BEGIN`/`END`）中执行 `IMPORT INTO` 会返回错误。
- `IMPORT INTO` 不能与 [备份与恢复](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)、[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)、[加速添加索引](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)、TiDB Lightning 数据导入、TiCDC 数据同步或 [时间点恢复（PITR）](https://docs.pingcap.com/tidb/stable/br-log-architecture) 等功能同时使用。更多兼容性信息，参见 [TiDB Lightning 和 `IMPORT INTO` 与 TiCDC 及日志备份的兼容性](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios)。
- 在数据导入过程中，不要对目标表执行 DDL 或 DML 操作，也不要对目标数据库执行 [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)。这些操作可能导致导入失败或数据不一致。此外，**不**建议在导入过程中进行读操作，因为读取到的数据可能不一致。请在导入完成后再进行读写操作。
- 导入过程会大量消耗系统资源。对于 TiDB 自建集群，为获得更好的性能，建议使用至少 32 核 CPU 和 64 GiB 内存的 TiDB 节点。TiDB 在导入过程中会将排序后的数据写入 TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)，因此建议为 TiDB 自建集群配置高性能存储介质，如闪存。更多信息参见 [物理导入模式限制](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions)。
- 对于 TiDB 自建集群，TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 需至少有 90 GiB 可用空间。建议分配的存储空间大于或等于待导入数据的体积。
- 一次导入任务仅支持向一个目标表导入数据。
- TiDB 集群升级期间不支持 `IMPORT INTO`。
- 确保待导入数据中不包含任何主键或非空唯一索引冲突的记录，否则会导致导入任务失败。
- 已知问题：如果 TiDB 节点配置文件中的 PD 地址与当前集群的 PD 拓扑不一致，`IMPORT INTO` 任务可能会失败。例如，PD 曾经缩容但 TiDB 配置文件未同步更新，或配置文件更新后未重启 TiDB 节点。

### `IMPORT INTO ... FROM FILE` 限制

- 对于 TiDB 自建集群，每个 `IMPORT INTO` 任务支持导入 10 TiB 以内的数据。如果启用 [Global Sort](/tidb-global-sort.md) 功能，每个任务支持导入 40 TiB 以内的数据。
- 对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，如果待导入数据超过 500 GiB，建议使用至少 16 核的 TiDB 节点并启用 [Global Sort](/tidb-global-sort.md) 功能，此时每个任务支持导入 40 TiB 以内的数据。如果数据量在 500 GiB 以内或 TiDB 节点核数小于 16，则不建议启用 [Global Sort](/tidb-global-sort.md)。
- 执行 `IMPORT INTO ... FROM FILE` 时会阻塞当前连接，直到导入完成。若需异步执行，可添加 `DETACHED` 选项。
- 每个集群最多可同时运行 16 个 `IMPORT INTO` 任务（参见 [TiDB 分布式执行框架（DXF）使用限制](/tidb-distributed-execution-framework.md#limitation)）。当集群资源不足或任务数已达上限时，新提交的导入任务会排队等待执行。
- 使用 [Global Sort](/tidb-global-sort.md) 功能导入数据时，`THREAD` 选项的值必须至少为 `8`。
- 使用 [Global Sort](/tidb-global-sort.md) 功能导入数据时，单行编码后的数据大小不得超过 32 MiB。
- 在未启用 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 时创建的所有 `IMPORT INTO` 任务，均直接在提交任务的节点上运行，即使后续启用 DXF，这些任务也不会被调度到其他 TiDB 节点。启用 DXF 后，只有新创建的、从 S3 或 GCS 导入数据的 `IMPORT INTO` 任务才会自动调度或故障转移到其他 TiDB 节点执行。

### `IMPORT INTO ... FROM SELECT` 限制

- `IMPORT INTO ... FROM SELECT` 只能在当前用户连接的 TiDB 节点上执行，并且会阻塞当前连接直到导入完成。
- `IMPORT INTO ... FROM SELECT` 仅支持两种 [导入选项](#withoptions)：`THREAD` 和 `DISABLE_PRECHECK`。
- `IMPORT INTO ... FROM SELECT` 不支持 `SHOW IMPORT JOB(s)`、`CANCEL IMPORT JOB <job-id>` 等任务管理语句。
- TiDB 的 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 需要有足够空间存储 `SELECT` 语句的完整查询结果（目前不支持配置 `DISK_QUOTA` 选项）。
- 不支持使用 [`tidb_snapshot`](/read-historical-data.md) 导入历史数据。
- 由于 `SELECT` 子句语法复杂，`IMPORT INTO` 的 `WITH` 参数可能与其冲突并导致解析错误，如 `GROUP BY ... [WITH ROLLUP]`。建议对于复杂的 `SELECT` 语句，先创建视图，再通过 `IMPORT INTO ... FROM SELECT * FROM view_name` 导入。或者，可以用括号明确 `SELECT` 子句的范围，如 `IMPORT INTO ... FROM (SELECT ...) WITH ...`。

## 导入前提条件

在使用 `IMPORT INTO` 导入数据前，请确保满足以下要求：

- 目标表已在 TiDB 中创建且为空表。
- 目标集群有足够空间存储待导入数据。
- 对于 TiDB 自建集群，当前会话连接的 TiDB 节点的 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 至少有 90 GiB 可用空间。如果已启用 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 且导入数据来自 S3 或 GCS，还需确保集群中每个 TiDB 节点的临时目录磁盘空间充足。

## 所需权限

执行 `IMPORT INTO` 需要对目标表拥有 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。若需导入 TiDB 本地存储的文件，还需拥有 `FILE` 权限。

## 语法

```ebnf+diagram
ImportIntoStmt ::=
    'IMPORT' 'INTO' TableName ColumnNameOrUserVarList? SetClause? FROM fileLocation Format? WithOptions?
    |
    'IMPORT' 'INTO' TableName ColumnNameList? FROM SelectStatement WithOptions?

ColumnNameOrUserVarList ::=
    '(' ColumnNameOrUserVar (',' ColumnNameOrUserVar)* ')'

ColumnNameList ::=
    '(' ColumnName (',' ColumnName)* ')'

SetClause ::=
    'SET' SetItem (',' SetItem)*

SetItem ::=
    ColumnName '=' Expr

Format ::=
    'CSV' | 'SQL' | 'PARQUET'

WithOptions ::=
    'WITH' OptionItem (',' OptionItem)*

OptionItem ::=
    optionName '=' optionVal | optionName
```

## 参数说明

### ColumnNameOrUserVarList

用于指定数据文件中每个字段与目标表列的对应关系。你也可以用它将字段映射到变量，以跳过某些字段的导入，或在 `SetClause` 中使用。

- 如果未指定该参数，则数据文件每行的字段数必须与目标表的列数一致，字段将按顺序导入到对应列。
- 如果指定了该参数，则指定的列或变量数量必须与数据文件每行的字段数一致。

### SetClause

用于指定目标列的值如何计算。在 `SET` 表达式右侧，可以引用 `ColumnNameOrUserVarList` 中指定的变量。

在 `SET` 表达式左侧，只能引用未包含在 `ColumnNameOrUserVarList` 中的列名。如果目标列名已在 `ColumnNameOrUserVarList` 中出现，则该 `SET` 表达式无效。

### fileLocation

用于指定数据文件的存储位置，可以是 Amazon S3 或 GCS 的 URI 路径，也可以是 TiDB 本地文件路径。

- Amazon S3 或 GCS URI 路径：URI 配置详情参见 [外部存储服务的 URI 格式](/external-storage-uri.md)。

- TiDB 本地文件路径：必须为绝对路径，文件扩展名需为 `.csv`、`.sql` 或 `.parquet`。确保该路径对应的文件存储在当前用户连接的 TiDB 节点上，且该用户拥有 `FILE` 权限。

> **Note:**
>
> 如果目标集群启用了 [SEM](/system-variables.md#tidb_enable_enhanced_security)，则 `fileLocation` 不能指定为本地文件路径。

在 `fileLocation` 参数中，你可以指定单个文件，也可以使用 `*` 和 `[]` 通配符匹配多个文件进行导入。注意，通配符只能用于文件名部分，不能匹配目录或递归匹配子目录下的文件。以存储在 Amazon S3 的文件为例，参数配置如下：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下所有 `.csv` 后缀文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 开头的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下所有以 `foo` 开头且以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`
- 导入指定路径下的 `1.csv` 和 `2.csv`：`s3://<bucket-name>/path/to/data/[12].csv`

### Format

`IMPORT INTO` 语句支持三种数据文件格式：`CSV`、`SQL` 和 `PARQUET`。如未指定，默认格式为 `CSV`。

### WithOptions

你可以使用 `WithOptions` 指定导入选项，控制数据导入过程。例如，为了在后台异步执行数据文件导入，可以在 `IMPORT INTO` 语句中添加 `WITH DETACHED` 选项启用 `DETACHED` 模式。

支持的选项说明如下：

| 选项名 | 支持的数据源和格式 | 说明 |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | 指定数据文件的字符集。默认字符集为 `utf8mb4`。支持的字符集包括 `binary`、`utf8`、`utf8mb4`、`gb18030`、`gbk`、`latin1` 和 `ascii`。|
| `FIELDS_TERMINATED_BY='<string>'` | CSV | 指定字段分隔符。默认分隔符为 `,`。|
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | 指定字段定界符。默认定界符为 `"`。|
| `FIELDS_ESCAPED_BY='<char>'` | CSV | 指定字段的转义字符。默认转义字符为 `\`。|
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | 指定字段中表示 `NULL` 的值。默认值为 `\N`。|
| `LINES_TERMINATED_BY='<string>'` | CSV | 指定行终止符。默认情况下，`IMPORT INTO` 会自动识别 `\n`、`\r` 或 `\r\n` 作为行终止符。如果行终止符为这三者之一，无需显式指定该选项。|
| `SKIP_ROWS=<number>` | CSV | 指定跳过的行数。默认值为 `0`。可用于跳过 CSV 文件的表头。如果使用通配符指定导入源文件，该选项会应用于 `fileLocation` 匹配到的所有源文件。|
| `SPLIT_FILE` | CSV | 将单个 CSV 文件拆分为多个约 256 MiB 的小块并并行处理，以提升导入效率。该参数仅对**非压缩**的 CSV 文件生效，且使用限制与 TiDB Lightning 的 [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format) 相同。注意，需显式指定 `LINES_TERMINATED_BY`。|
| `DISK_QUOTA='<string>'` | 所有文件格式 | 指定数据排序过程中可用的磁盘空间阈值。默认值为 TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 磁盘空间的 80%。若无法获取总磁盘大小，默认值为 50 GiB。显式指定 `DISK_QUOTA` 时，确保该值不超过 TiDB 临时目录磁盘空间的 80%。|
| `DISABLE_TIKV_IMPORT_MODE` | 所有文件格式 | 指定是否在导入过程中禁用 TiKV 切换为导入模式。默认不禁用 TiKV 切换为导入模式。如果集群中有读写操作进行中，可启用该选项以避免导入过程的影响。|
| `THREAD=<number>` | 所有文件格式及 `SELECT` 查询结果 | 指定导入并发度。对于 `IMPORT INTO ... FROM FILE`，`THREAD` 默认值为 TiDB 节点 CPU 核数的 50%，最小值为 `1`，最大值为 CPU 核数。对于 `IMPORT INTO ... FROM SELECT`，默认值为 `2`，最小值为 `1`，最大值为 TiDB 节点 CPU 核数的两倍。若向新集群导入数据，建议适当提高并发度以提升导入性能。若目标集群已在生产环境使用，建议根据业务需求调整并发度。|
| `MAX_WRITE_SPEED='<string>'` | 所有文件格式 | 控制写入 TiKV 节点的速度。默认无限制。例如，可指定为 `1MiB`，限制写入速度为 1 MiB/s。|
| `CHECKSUM_TABLE='<string>'` | 所有文件格式 | 配置导入完成后是否对目标表进行校验以验证导入完整性。支持的值包括 `"required"`（默认）、`"optional"` 和 `"off"`。`"required"` 表示导入后进行校验，校验失败则返回错误并退出导入；`"optional"` 表示导入后进行校验，若出错则返回警告并忽略错误；`"off"` 表示不进行校验。|
| `DETACHED` | 所有文件格式 | 控制是否异步执行 `IMPORT INTO`。启用后，执行 `IMPORT INTO` 会立即返回导入任务信息（如 `Job_ID`），任务在后台异步执行。|
| `CLOUD_STORAGE_URI` | 所有文件格式 | 指定 [Global Sort](/tidb-global-sort.md) 编码 KV 数据的目标存储地址。未指定时，`IMPORT INTO` 会根据系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 的值判断是否启用 Global Sort。如果该系统变量指定了目标存储地址，则使用该地址进行 Global Sort。若 `CLOUD_STORAGE_URI` 显式指定非空值，则使用该值作为目标存储地址。若指定为空值，则强制本地排序。目前目标存储地址仅支持 S3。URI 配置详情参见 [Amazon S3 URI 格式](/external-storage-uri.md#amazon-s3-uri-format)。使用该功能时，所有 TiDB 节点需具备目标 S3 bucket 的读写权限，包括但不限于：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject`、`s3:PutObject`、`s3:AbortMultipartUpload`。|
| `DISABLE_PRECHECK` | 所有文件格式及 `SELECT` 查询结果 | 设置该选项可禁用非关键项的预检查，如检查是否存在 CDC 或 PITR 任务。|

<CustomContent platform="tidb-cloud" plan="premium">

> **Note:**
>
> 对于 TiDB Cloud Premium，以下四个选项 — `DISK_QUOTA`、`THREAD`、`MAX_WRITE_SPEED` 和 `CLOUD_STORAGE_URI` — 会自动调整为合适的值，用户无法修改。如需调整这些设置，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。

</CustomContent>

## `IMPORT INTO ... FROM FILE` 用法

对于 TiDB 自建集群，`IMPORT INTO ... FROM FILE` 支持从 Amazon S3、GCS 及 TiDB 本地存储的文件导入数据。对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，支持从 Amazon S3 和 GCS 导入。对于 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential)，支持从 Amazon S3 和阿里云 OSS 导入。

- 对于存储在 Amazon S3 或 GCS 的数据文件，`IMPORT INTO ... FROM FILE` 支持在 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 下运行。

    - 启用 DXF（[`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 为 `ON`）时，`IMPORT INTO` 会将数据导入任务拆分为多个子任务，并分发到不同 TiDB 节点并行执行，以提升导入效率。
    - 未启用 DXF 时，`IMPORT INTO ... FROM FILE` 仅支持在当前用户连接的 TiDB 节点上运行。

- 对于 TiDB 本地存储的数据文件，`IMPORT INTO ... FROM FILE` 仅支持在当前用户连接的 TiDB 节点上运行。因此，数据文件需放置在该 TiDB 节点上。如果你通过代理或负载均衡访问 TiDB，则无法导入本地存储的数据文件。

### 压缩文件

`IMPORT INTO ... FROM FILE` 支持导入压缩的 `CSV` 和 `SQL` 文件。可根据文件扩展名自动识别文件是否压缩及压缩格式：

| 扩展名 | 压缩格式 |
|:---|:---|
| `.gz`, `.gzip` | gzip 压缩格式 |
| `.zstd`, `.zst` | ZStd 压缩格式 |
| `.snappy` | snappy 压缩格式 |

> **Note:**
>
> - Snappy 压缩文件必须为 [官方 Snappy 格式](https://github.com/google/snappy)，不支持其他变体。
> - 由于 TiDB Lightning 无法并发解压单个大型压缩文件，压缩文件的大小会影响导入速度。建议单个源文件解压后不超过 256 MiB。

### Global Sort

> **Note:**
>
> Global Sort 不支持在 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#starter) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 集群上使用。

`IMPORT INTO ... FROM FILE` 会将源数据文件的导入任务拆分为多个子任务，每个子任务独立编码和排序数据后导入。如果这些子任务编码后的 KV 范围有大量重叠（关于 TiDB 如何将数据编码为 KV，参见 [TiDB 计算](/tidb-computing.md)），则 TiKV 在导入过程中需要持续进行 compaction，导致导入性能和稳定性下降。

以下场景可能导致 KV 范围重叠较多：

- 如果分配给各子任务的数据文件行的主键范围有重叠，则每个子任务编码生成的数据 KV 也会重叠。
    - `IMPORT INTO` 按数据文件的遍历顺序拆分子任务，通常按文件名字典序排序。
- 如果目标表有大量索引，或索引列值在数据文件中分布较散，则每个子任务编码生成的索引 KV 也会重叠。

启用 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 后，你可以通过在 `IMPORT INTO` 语句中指定 `CLOUD_STORAGE_URI` 选项，或通过系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 指定编码 KV 数据的目标存储地址来启用 [Global Sort](/tidb-global-sort.md)。目前 Global Sort 仅支持使用 Amazon S3 作为存储地址。启用 Global Sort 后，`IMPORT INTO` 会将编码后的 KV 数据写入云存储，在云存储中进行全局排序，然后并行将全局排序后的索引和表数据导入 TiKV，从而避免 KV 重叠带来的问题，提升导入的稳定性和性能。

Global Sort 会消耗大量内存资源。导入数据前，建议配置 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 变量，避免频繁触发 golang GC 影响导入效率。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **Note:**
>
> - 如果源数据文件的 KV 范围重叠较低，启用 Global Sort 可能会降低导入性能。因为启用 Global Sort 后，TiDB 需要等待所有子任务本地排序完成，才能进行全局排序及后续导入操作。
> - 使用 Global Sort 的导入任务完成后，云存储中用于 Global Sort 的文件会在后台线程中异步清理。

### 输出

当 `IMPORT INTO ... FROM FILE` 导入完成或启用 `DETACHED` 模式时，TiDB 会在输出中返回当前任务信息，示例如下。各字段说明参见 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)。

`IMPORT INTO ... FROM FILE` 导入完成时，输出示例如下：

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

启用 `DETACHED` 模式时，执行 `IMPORT INTO ... FROM FILE` 语句会立即返回任务信息。从输出中可以看到任务状态为 `pending`，表示等待执行。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### 查看和管理导入任务

对于启用 `DETACHED` 模式的导入任务，你可以使用 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) 查看其当前进度。

导入任务启动后，可以通过 [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md) 取消任务。

### 示例

#### 导入带表头的 CSV 文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 以 `DETACHED` 模式异步导入文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### 跳过导入数据文件中的某个字段

假设你的数据文件为 CSV 格式，内容如下：

```
id,name,age
1,Tom,23
2,Jack,44
```

假设目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100))`。若要跳过将数据文件中的 `age` 字段导入表 `t`，可执行如下 SQL：

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 使用通配符导入多个数据文件

假设 `/path/to/` 目录下有 `file-01.csv`、`file-02.csv` 和 `file-03.csv` 三个文件。要将这三个文件导入目标表 `t`，可执行如下 SQL：

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

如果只需导入 `file-01.csv` 和 `file-03.csv`，可执行如下 SQL：

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### 从 Amazon S3 或 GCS 导入数据文件

- 从 Amazon S3 导入数据文件：

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- 从 GCS 导入数据文件：

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

关于 Amazon S3 或 GCS 的 URI 路径配置，参见 [外部存储服务的 URI 格式](/external-storage-uri.md)。

#### 使用 SetClause 计算列值

假设你的数据文件为 CSV 格式，内容如下：

```
id,name,val
1,phone,230
2,book,440
```

假设目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100), val int)`。如果你希望在导入时将 `val` 列的值乘以 100，可执行如下 SQL：

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 导入 SQL 格式的数据文件

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### 限制写入 TiKV 的速度

若要将写入 TiKV 节点的速度限制为 10 MiB/s，可执行如下 SQL：

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## `IMPORT INTO ... FROM SELECT` 用法

`IMPORT INTO ... FROM SELECT` 允许你将 `SELECT` 语句的查询结果导入 TiDB 的空表。你也可以用它导入通过 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

### 导入 `SELECT` 查询结果

要将 `UNION` 结果导入目标表 `t`，并指定导入并发度为 `8`，禁用非关键项预检查，可执行如下 SQL：

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### 导入指定时间点的历史数据

要将指定时间点的历史数据导入目标表 `t`，可执行如下 SQL：

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQL 兼容性

该语句为 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md)

---
title: IMPORT INTO
summary: 关于在 TiDB 中使用 IMPORT INTO 的概述。
---

# IMPORT INTO

`IMPORT INTO` 语句允许你通过 TiDB Lightning 的 [Physical Import Mode](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode) 将数据导入到 TiDB。你可以通过以下两种方式使用 `IMPORT INTO`：

- `IMPORT INTO ... FROM FILE`：将支持 `CSV`、`SQL` 和 `PARQUET` 格式的数据文件导入到空的 TiDB 表中。
- `IMPORT INTO ... FROM SELECT`：将 `SELECT` 语句的查询结果导入到空的 TiDB 表中。你也可以用它导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

<CustomContent platform="tidb">

> **Note:**
>
> 相较于 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)，`IMPORT INTO` 可以直接在 TiDB 节点上执行，支持自动化的分布式任务调度和 [TiDB Global Sort](/tidb-global-sort.md)，在部署、资源利用率、任务配置便利性、调用和集成的简便性、高可用性以及扩展性方面有显著提升。建议在适用场景下考虑使用 `IMPORT INTO` 代替 TiDB Lightning。

</CustomContent>

## 限制条件

- `IMPORT INTO` 仅支持将数据导入到数据库中已存在且为空的表。
- 如果同一表的其他分区已存在数据，则不支持将数据导入到空的分区中。目标表必须完全为空才能进行导入操作。
- `IMPORT INTO` 不支持导入到 [临时表](/temporary-tables.md) 或 [缓存表](/cached-tables.md)。
- `IMPORT INTO` 不支持事务或回滚。在显式事务（`BEGIN`/`END`）中执行 `IMPORT INTO` 会返回错误。
- `IMPORT INTO` 不支持与 [备份与还原](https://docs.pingcap.com/tidb/stable/backup-and-restore-overview)、[`FLASHBACK CLUSTER`](/sql-statements/sql-statement-flashback-cluster.md)、[加速添加索引](/system-variables.md#tidb_ddl_enable_fast_reorg-new-in-v630)、TiDB Lightning 数据导入、TiCDC 数据复制或 [Point-in-Time Recovery (PITR)](https://docs.pingcap.com/tidb/stable/br-log-architecture) 等功能同时使用。更多兼容性信息，请参见 [TiDB Lightning 与 `IMPORT INTO` 在 TiCDC 和 Log Backup 场景下的兼容性](https://docs.pingcap.com/tidb/stable/tidb-lightning-compatibility-and-scenarios)。
- 在数据导入过程中，不要对目标表执行 DDL 或 DML 操作，也不要对目标数据库执行 [`FLASHBACK DATABASE`](/sql-statements/sql-statement-flashback-database.md)。这些操作可能导致导入失败或数据不一致。此外，**不建议** 在导入过程中进行读操作，因为读取的数据可能不一致。应在导入完成后再进行读写操作。
- 导入过程会大量消耗系统资源。对于 TiDB 自托管环境，为获得更好的性能，建议使用至少 32 核心和 64 GiB 内存的 TiDB 节点。导入时，TiDB 会将排序后的数据写入 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630)，因此建议配置高性能存储介质（如闪存）。更多信息请参见 [Physical Import Mode 限制](https://docs.pingcap.com/tidb/stable/tidb-lightning-physical-import-mode#requirements-and-restrictions)。
- 对于 TiDB 自托管环境，建议为 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 分配至少 90 GiB 的可用空间。建议存储空间不少于待导入数据的体积。
- 一个导入任务仅支持导入到一个目标表。
- 在 TiDB 集群升级期间，不支持 `IMPORT INTO`。
- 确保待导入数据不包含主键或非空唯一索引冲突的记录，否则冲突可能导致导入任务失败。
- 已知问题：如果 TiDB 节点配置文件中的 PD 地址与集群当前的 PD 拓扑不一致，`IMPORT INTO` 任务可能失败。这种不一致可能发生在之前扩容 PD 后未更新配置文件，或配置文件更新后未重启 TiDB 节点的情况下。

### `IMPORT INTO ... FROM FILE` 限制

- 对于 TiDB 自托管环境，每个 `IMPORT INTO` 任务支持导入数据在 10 TiB 以内。如果启用 [Global Sort](/tidb-global-sort.md)，每个 `IMPORT INTO` 任务支持导入数据在 40 TiB 以内。
- 对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，如果待导入数据超过 500 GiB，建议使用至少 16 核的 TiDB 节点并启用 [Global Sort](/tidb-global-sort.md)，此时每个 `IMPORT INTO` 任务支持导入数据在 40 TiB 以内。如果数据在 500 GiB 以内或 TiDB 节点核数少于 16，不建议启用 [Global Sort](/tidb-global-sort.md)。
- `IMPORT INTO ... FROM FILE` 的执行会阻塞当前连接，直到导入完成。若希望异步执行，可以添加 `DETACHED` 选项。
- 每个集群最多可同时运行 16 个 `IMPORT INTO` 任务（详见 [TiDB 分布式执行框架（DXF）使用限制](/tidb-distributed-execution-framework.md#limitation)）。当资源不足或达到最大任务数时，新提交的导入任务会排队等待执行。
- 使用 [Global Sort](/tidb-global-sort.md) 进行数据导入时，`THREAD` 选项的值必须至少为 `8`。
- 使用 [Global Sort](/tidb-global-sort.md) 进行数据导入时，单行编码后数据大小不得超过 32 MiB。
- 在未启用 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 时，所有创建的 `IMPORT INTO` 任务会直接在提交任务的节点上运行，即使后续启用 DXF，也不会调度到其他 TiDB 节点。启用 DXF 后，只有从 S3 或 GCS 导入数据的 `IMPORT INTO` 新任务会自动调度或故障转移到其他 TiDB 节点。

### `IMPORT INTO ... FROM SELECT` 限制

- `IMPORT INTO ... FROM SELECT` 只能在当前用户连接的 TiDB 节点上执行，且会阻塞当前连接直到导入完成。
- `IMPORT INTO ... FROM SELECT` 仅支持两个 [import options](#withoptions)：`THREAD` 和 `DISABLE_PRECHECK`。
- `IMPORT INTO ... FROM SELECT` 不支持 `SHOW IMPORT JOB(s)` 和 `CANCEL IMPORT JOB <job-id>` 等任务管理语句。
- TiDB 的 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 需要有足够空间存放 `SELECT` 语句的全部查询结果（目前不支持配置 `DISK_QUOTA` 选项）。
- 不支持使用 [`tidb_snapshot`](/read-historical-data.md) 导入历史数据。
- 由于 `SELECT` 子句的语法较复杂，`IMPORT INTO` 中的 `WITH` 参数可能与其冲突，导致解析错误，例如 `GROUP BY ... [WITH ROLLUP]`。建议为复杂的 `SELECT` 语句创建视图，然后用 `IMPORT INTO ... FROM SELECT * FROM view_name` 进行导入。或者用括号明确 `SELECT` 子句的范围，例如 `IMPORT INTO ... FROM (SELECT ...) WITH ...`。

## 导入前提条件

在使用 `IMPORT INTO` 导入数据前，请确保满足以下条件：

- 目标表已在 TiDB 中创建且为空。
- 目标集群有足够的空间存放待导入的数据。
- 对于 TiDB 自托管，连接当前会话的 TiDB 节点的 [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 至少有 90 GiB 可用空间。如果启用 [`tidb_enable_dist_task`](/system-variables.md#tidb_enable_dist_task-new-in-v710) 且数据来自 S3 或 GCS，还需确保集群中每个 TiDB 节点的临时目录有足够的磁盘空间。

## 所需权限

执行 `IMPORT INTO` 需要对目标表拥有 `SELECT`、`UPDATE`、`INSERT`、`DELETE` 和 `ALTER` 权限。若要导入 TiDB 本地存储的文件，还需拥有 `FILE` 权限。

## 概要

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

它指定每个数据文件中的字段与目标表中的列的对应关系。你也可以用它将字段映射到变量，以跳过某些字段，或在 `SetClause` 中使用。

- 如果未指定此参数，则每行数据文件中的字段数必须与目标表的列数相匹配，字段将按顺序导入对应的列。
- 如果指定了此参数，所列列或变量的数量必须与每行数据文件中的字段数相匹配。

### SetClause

它指定目标列的值如何计算。在 `SET` 表达式的右侧，可以引用在 `ColumnNameOrUserVarList` 中定义的变量。

在 `SET` 表达式的左侧，只能引用未包含在 `ColumnNameOrUserVarList` 中的列名。如果目标列名已在 `ColumnNameOrUserVarList` 中存在，则 `SET` 表达式无效。

### fileLocation

它指定数据文件的存储位置，可以是 Amazon S3 或 GCS 的 URI 路径，也可以是 TiDB 本地文件路径。

- Amazon S3 或 GCS URI 路径：有关 URI 配置详情，请参见 [URI Formats of External Storage Services](/external-storage-uri.md)。

- TiDB 本地文件路径：必须是绝对路径，文件扩展名必须为 `.csv`、`.sql` 或 `.parquet`。确保对应此路径的文件存储在当前用户连接的 TiDB 节点上，且用户拥有 `FILE` 权限。

> **Note:**
>
> 如果在目标集群启用了 [SEM](/system-variables.md#tidb_enable_enhanced_security)，则不能将 `fileLocation` 指定为本地文件路径。

在 `fileLocation` 参数中，可以指定单个文件，也可以使用 `*` 和 `[]` 通配符匹配多个文件进行导入。注意，通配符只能用于文件名，不能匹配目录或递归匹配子目录中的文件。例如，存储在 Amazon S3 上的文件，可以配置如下：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下所有 `.csv` 后缀的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 前缀的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下所有以 `foo` 前缀且后缀为 `.csv` 的文件：`s3://<bucket-name>/path/to/data/foo*.csv`
- 导入指定路径下 `1.csv` 和 `2.csv` 文件：`s3://<bucket-name>/path/to/data/[12].csv`

### Format

`IMPORT INTO` 语句支持三种数据文件格式：`CSV`、`SQL` 和 `PARQUET`。如果未指定，默认格式为 `CSV`。

### WithOptions

你可以使用 `WithOptions` 来指定导入选项，控制数据导入过程。例如，为了在后台异步执行数据文件的导入，可以启用 `DETACHED` 模式，只需在 `IMPORT INTO` 语句中添加 `WITH DETACHED` 选项。

支持的选项如下表所示：

| 选项名 | 支持的数据源和格式 | 描述 |
|:---|:---|:---|
| `CHARACTER_SET='<string>'` | CSV | 指定数据文件的字符集，默认字符集为 `utf8mb4`。支持的字符集包括 `binary`、`utf8`、`utf8mb4`、`gb18030`、`gbk`、`latin1` 和 `ascii`。 |
| `FIELDS_TERMINATED_BY='<string>'` | CSV | 指定字段分隔符，默认为 `,`。 |
| `FIELDS_ENCLOSED_BY='<char>'` | CSV | 指定字段定界符，默认为 `"`。 |
| `FIELDS_ESCAPED_BY='<char>'` | CSV | 指定字段的转义字符，默认为 `\`。 |
| `FIELDS_DEFINED_NULL_BY='<string>'` | CSV | 指定字段中表示 `NULL` 的值，默认为 `\N`。 |
| `LINES_TERMINATED_BY='<string>'` | CSV | 指定行终止符，默认情况下，`IMPORT INTO` 会自动识别 `\n`、`\r` 或 `\r\n` 作为行终止符。如果行终止符是这三者之一，则无需显式指定此选项。 |
| `SKIP_ROWS=<number>` | CSV | 指定跳过的行数，默认值为 `0`。可用于跳过 CSV 文件的表头。如果使用通配符指定源文件，此选项适用于所有匹配的源文件。 |
| `SPLIT_FILE` | CSV | 将单个 CSV 文件拆分成多个约 256 MiB 的块，以实现并行处理，从而提升导入效率。此参数仅适用于**非压缩**的 CSV 文件，且使用限制与 TiDB Lightning 的 [`strict-format`](https://docs.pingcap.com/tidb/stable/tidb-lightning-data-source#strict-format) 相同。注意，必须显式指定 `LINES_TERMINATED_BY`。 |
| `DISK_QUOTA='<string>'` | 所有文件格式 | 指定在数据排序过程中可用的磁盘空间阈值，默认值为 TiDB [临时目录](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#temp-dir-new-in-v630) 磁盘空间的 80%。如果无法获取总磁盘大小，则默认值为 50 GiB。显式指定 `DISK_QUOTA` 时，确保其值不超过临时目录磁盘空间的 80%。 |
| `DISABLE_TIKV_IMPORT_MODE` | 所有文件格式 | 指定是否在导入过程中禁用 TiKV 切换到导入模式，默认不禁用。如果集群中存在正在进行的读写操作，可以启用此选项以避免导入过程带来的影响。 |
| `THREAD=<number>` | 所有文件格式和 `SELECT` 查询结果 | 指定导入的并发度。对于 `IMPORT INTO ... FROM FILE`，`THREAD` 的默认值为 TiDB 节点 CPU 核数的 50%，最小值为 `1`，最大值为 CPU 核数。对于 `IMPORT INTO ... FROM SELECT`，默认值为 `2`，最小值为 `1`，最大值为 TiDB 节点 CPU 核数的两倍。若在新集群中无数据导入，建议适当增加此并发度以提升导入性能；若在生产环境中使用，建议根据应用需求调整。 |
| `MAX_WRITE_SPEED='<string>'` | 所有文件格式 | 控制写入 TiKV 节点的速度，默认无限制。例如，可配置为 `1MiB` 限制写入速度为 1 MiB/s。 |
| `CHECKSUM_TABLE='<string>'` | 所有文件格式 | 配置导入后是否对目标表进行校验和，以验证导入完整性。支持值包括 `"required"`（默认）、`"optional"` 和 `"off"`。`"required"` 表示导入后进行校验和，若校验失败，TiDB 返回错误并退出。`"optional"` 表示导入后进行校验和，若出错，TiDB 返回警告并忽略错误。`"off"` 表示不进行校验和。 |
| `DETACHED` | 所有文件格式 | 控制是否异步执行 `IMPORT INTO`。启用后，执行 `IMPORT INTO` 会立即返回导入任务信息（如 `Job_ID`），任务在后台异步执行。 |
| `CLOUD_STORAGE_URI` | 所有文件格式 | 指定存储编码的 KV 数据用于 [Global Sort](/tidb-global-sort.md) 的目标地址。当未指定 `CLOUD_STORAGE_URI` 时，`IMPORT INTO` 会根据系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 的值判断是否使用 Global Sort。如果该系统变量指定了目标存储地址，`IMPORT INTO` 会使用此地址进行 Global Sort。当 `CLOUD_STORAGE_URI` 被配置且非空时，`IMPORT INTO` 使用该值作为目标存储地址；若配置为空值，则强制本地排序。目前仅支持 S3。有关 URI 配置的详细信息，请参见 [Amazon S3 URI 格式](/external-storage-uri.md#amazon-s3-uri-format)。启用此功能后，所有 TiDB 节点必须具有对目标 S3 存储桶的读写权限，包括至少以下权限：`s3:ListBucket`、`s3:GetObject`、`s3:DeleteObject`、`s3:PutObject`、`s3: AbortMultipartUpload`。 |
| `DISABLE_PRECHECK` | 所有文件格式和 `SELECT` 查询结果 | 设置后，将禁用对非关键项的预检查，例如检查是否存在 CDC 或 PITR 任务。 |

## `IMPORT INTO ... FROM FILE` 使用示例

对于 TiDB 自托管环境，`IMPORT INTO ... FROM FILE` 支持导入存储在 Amazon S3、GCS 和 TiDB 本地存储中的数据文件。对于 [TiDB Cloud Dedicated](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-dedicated)，`IMPORT INTO ... FROM FILE` 支持导入存储在 Amazon S3 和 GCS 中的数据文件。对于 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless)，支持导入存储在 Amazon S3 和阿里云 OSS 中的数据文件。

- 存储在 Amazon S3 或 GCS 上的数据文件，`IMPORT INTO ... FROM FILE` 支持在 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 中运行。

    - 当启用 DXF（`tidb_enable_dist_task` /system-variables.md#tidb_enable_dist_task-new-in-v710 为 `ON`）时，`IMPORT INTO` 会将数据导入任务拆分成多个子任务，并将这些子任务分发到不同的 TiDB 节点执行，以提升导入效率。
    - 当禁用 DXF 时，`IMPORT INTO ... FROM FILE` 仅支持在当前用户连接的 TiDB 节点上运行。

- 存储在 TiDB 本地的文件，`IMPORT INTO ... FROM FILE` 仅支持在当前用户连接的 TiDB 节点上运行。因此，数据文件必须放在当前用户连接的 TiDB 节点上。如果通过代理或负载均衡器访问 TiDB，则无法导入存储在本地的文件。

### 压缩文件

`IMPORT INTO ... FROM FILE` 支持导入压缩的 `CSV` 和 `SQL` 文件。它可以根据文件扩展名自动判断文件是否压缩及压缩格式：

| 扩展名 | 压缩格式 |
|:---|:---|
| `.gz`, `.gzip` | gzip 压缩格式 |
| `.zstd`, `.zst` | ZStd 压缩格式 |
| `.snappy` | snappy 压缩格式 |

> **Note:**
>
> - Snappy 压缩文件必须为 [官方 Snappy 格式](https://github.com/google/snappy)，不支持其他变体。
> - 由于 TiDB Lightning 不能同时解压单个大压缩文件，压缩文件的大小会影响导入速度。建议源文件解压后不超过 256 MiB。

### Global Sort

> **Note:**
>
> Global Sort 在 [{{{ .starter }}}](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

`IMPORT INTO ... FROM FILE` 会将源数据文件的导入任务拆分成多个子任务，每个子任务在导入前会独立进行编码和排序。如果这些子任务的编码 KV 范围存在较大重叠（详见 [TiDB 编码数据到 KV](/tidb-computing.md)），则在导入过程中需要保持压缩 KV 的合并，可能导致导入性能下降和稳定性问题。

以下场景可能导致 KV 范围存在显著重叠：

- 如果每个子任务分配到的数据文件中的行具有重叠的主键范围，则每个子任务编码生成的 KV 也会重叠。
    - `IMPORT INTO` 根据数据文件的遍历顺序拆分子任务，通常按文件名的字典序排序。
- 如果目标表有许多索引，或索引列的值在数据文件中分散，则每个子任务编码生成的索引 KV 也会重叠。

启用 [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md) 后，可以通过在 `IMPORT INTO` 语句中指定 `CLOUD_STORAGE_URI` 选项，或通过系统变量 [`tidb_cloud_storage_uri`](/system-variables.md#tidb_cloud_storage_uri-new-in-v740) 指定编码 KV 数据的目标存储地址，来启用 [Global Sort](/tidb-global-sort.md)。目前，Global Sort 仅支持使用 Amazon S3 作为存储地址。当启用 Global Sort 时，`IMPORT INTO` 会将编码的 KV 数据写入云存储，在云端进行 Global Sort，然后并行导入全局排序后的索引和表数据到 TiKV。这可以避免 KV 重叠带来的问题，提升导入的稳定性和性能。

Global Sort 会消耗大量内存资源。建议在导入前配置 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-new-in-v640) 和 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-new-in-v640) 变量，以避免 Golang 垃圾回收频繁触发，从而影响导入效率。

```sql
SET GLOBAL tidb_server_memory_limit_gc_trigger=1;
SET GLOBAL tidb_server_memory_limit='75%';
```

> **Note:**
>
> - 如果源数据文件中的 KV 范围重叠较少，启用 Global Sort 可能会降低导入性能。这是因为启用后，TiDB 需要等待所有子任务完成本地排序后，才能进行全局排序和后续导入。
> - 使用 Global Sort 完成的导入任务结束后，存储在云端的 Global Sort 文件会在后台异步清理。

### 输出信息

当 `IMPORT INTO ... FROM FILE` 完成导入或启用 `DETACHED` 模式后，TiDB 会在输出中返回当前任务信息，示例如下。每个字段的说明请参见 [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)。

当 `IMPORT INTO ... FROM FILE` 完成导入时，示例输出如下：

```sql
IMPORT INTO t FROM '/path/to/small.csv';
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|  60002 | /path/to/small.csv | `test`.`t`   |      363 |       | finished | 16B              |             2 |                | 2023-06-08 16:01:22.095698 | 2023-06-08 16:01:22.394418 | 2023-06-08 16:01:26.531821 | root@%     |
+--------+--------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
```

当启用 `DETACHED` 模式后，执行 `IMPORT INTO ... FROM FILE` 会立即返回任务信息。可以从输出中看到任务状态为 `pending`，表示等待执行。

```sql
IMPORT INTO t FROM '/path/to/small.csv' WITH DETACHED;
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
```

### 查看和管理导入任务

对于启用 `DETACHED` 模式的导入任务，可以使用 [`SHOW IMPORT`](/sql-statements/sql-statement-show-import-job.md) 查看其当前进度。

任务启动后，可以用 [`CANCEL IMPORT JOB <job-id>`](/sql-statements/sql-statement-cancel-import-job.md) 取消。

### 示例

#### 导入带表头的 CSV 文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 异步以 `DETACHED` 模式导入文件

```sql
IMPORT INTO t FROM '/path/to/file.csv' WITH DETACHED;
```

#### 跳过数据文件中的某个字段导入

假设你的数据文件为 CSV 格式，内容如下：

```
id,name,age
1,Tom,23
2,Jack,44
```

目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100))`。若要跳过导入 `age` 字段到表 `t`，可以执行：

```sql
IMPORT INTO t(id, name, @1) FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 使用通配符导入多个数据文件

假设 `/path/to/` 目录下有 `file-01.csv`、`file-02.csv` 和 `file-03.csv` 三个文件。要导入这些文件到目标表 `t`，可以执行：

```sql
IMPORT INTO t FROM '/path/to/file-*.csv';
```

只导入 `file-01.csv` 和 `file-03.csv` 时，执行：

```sql
IMPORT INTO t FROM '/path/to/file-0[13].csv';
```

#### 从 Amazon S3 或 GCS 导入数据文件

- 从 Amazon S3 导入：

    ```sql
    IMPORT INTO t FROM 's3://bucket-name/test.csv?access-key=XXX&secret-access-key=XXX';
    ```

- 从 GCS 导入：

    ```sql
    IMPORT INTO t FROM 'gs://import/test.csv?credentials-file=${credentials-file-path}';
    ```

有关 Amazon S3 或 GCS URI 配置的详细信息，请参见 [URI Formats of External Storage Services](/external-storage-uri.md)。

#### 使用 SetClause 计算列值

假设数据文件为 CSV 格式，内容如下：

```
id,name,val
1,phone,230
2,book,440
```

目标表结构为 `CREATE TABLE t(id int primary key, name varchar(100), val int)`。若在导入时希望将 `val` 列的值乘以 100，可以执行：

```sql
IMPORT INTO t(id, name, @1) SET val=@1*100 FROM '/path/to/file.csv' WITH skip_rows=1;
```

#### 导入 SQL 格式的数据文件

```sql
IMPORT INTO t FROM '/path/to/file.sql' FORMAT 'sql';
```

#### 限制写入 TiKV 的速度

要将写入 TiKV 节点的速度限制为 10 MiB/s，执行：

```sql
IMPORT INTO t FROM 's3://bucket/path/to/file.parquet?access-key=XXX&secret-access-key=XXX' FORMAT 'parquet' WITH MAX_WRITE_SPEED='10MiB';
```

## `IMPORT INTO ... FROM SELECT` 使用示例

`IMPORT INTO ... FROM SELECT` 允许你将 `SELECT` 语句的查询结果导入到 TiDB 中的空表。你也可以用它导入使用 [`AS OF TIMESTAMP`](/as-of-timestamp.md) 查询的历史数据。

### 导入 `SELECT` 查询结果

将 `UNION` 结果导入目标表 `t`，并将导入并发度设为 `8`，同时禁用非关键项的预检查，执行：

```sql
IMPORT INTO t FROM SELECT * FROM src UNION SELECT * FROM src2 WITH THREAD = 8, DISABLE_PRECHECK;
```

### 在指定时间点导入历史数据

将指定时间点的历史数据导入目标表 `t`，执行：

```sql
IMPORT INTO t FROM SELECT * FROM src AS OF TIMESTAMP '2024-02-27 11:38:00';
```

## MySQL 兼容性

此语句为 TiDB 对 MySQL 语法的扩展。

## 相关链接

* [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
* [`SHOW IMPORT JOB(s)`](/sql-statements/sql-statement-show-import-job.md)
* [TiDB 分布式执行框架（DXF）](/tidb-distributed-execution-framework.md)
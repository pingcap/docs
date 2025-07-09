---
title: LOAD DATA | TiDB SQL 语句参考
summary: 关于在 TiDB 数据库中使用 LOAD DATA 的概述。
---

# LOAD DATA

`LOAD DATA` 语句批量将数据加载到 TiDB 表中。

从 TiDB v7.0.0 版本开始，`LOAD DATA` SQL 语句支持以下功能：

- 支持从 S3 和 GCS 导入数据
- 新增参数 `FIELDS DEFINED NULL BY`

> **Warning:**
>
> 新的参数 `FIELDS DEFINED NULL BY` 以及对从 S3 和 GCS 导入数据的支持为实验性功能。建议不要在生产环境中使用此功能。此功能可能在未提前通知的情况下被更改或移除。如发现 bug，可以在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 对于 `LOAD DATA INFILE` 语句，TiDB Cloud Dedicated 支持 `LOAD DATA LOCAL INFILE`，以及从 Amazon S3 或 Google Cloud Storage 导入 `LOAD DATA INFILE`，而 {{{ .starter }}} 仅支持 `LOAD DATA LOCAL INFILE`。

</CustomContent>

## 概要

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## 参数

### `LOCAL`

你可以使用 `LOCAL` 来指定在客户端要导入的数据文件，其中文件参数必须是客户端的文件系统路径。

如果你使用 TiDB Cloud，要使用 `LOAD DATA` 语句加载本地数据文件，连接时需要添加 `--local-infile` 选项。

- 以下是 {{{ .starter }}} 的示例连接字符串：

    ```
    mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile
    ```

- 以下是 TiDB Cloud Dedicated 的示例连接字符串：

    ```
    mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile
    ```

### S3 和 GCS 存储

<CustomContent platform="tidb">

如果未指定 `LOCAL`，文件参数必须是有效的 S3 或 GCS 路径，详细信息请参见 [external storage](/br/backup-and-restore-storages.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果未指定 `LOCAL`，文件参数必须是有效的 S3 或 GCS 路径，详细信息请参见 [external storage](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)。

</CustomContent>

当数据文件存储在 S3 或 GCS 上时，你可以导入单个文件或使用通配符 `*` 来匹配多个文件进行导入。注意，通配符不支持递归处理子目录中的文件。以下是一些示例：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 开头的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下所有以 `foo` 开头并以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### `Fields`、`Lines` 和 `Ignore Lines`

你可以使用 `Fields` 和 `Lines` 参数来指定数据格式的处理方式。

- `FIELDS TERMINATED BY`：指定字段分隔符。
- `FIELDS ENCLOSED BY`：指定字段的包裹字符。
- `LINES TERMINATED BY`：指定行结束符，如果你希望以特定字符结束一行。

你可以使用 `DEFINED NULL BY` 来指定数据文件中 NULL 值的表示方式。

- 与 MySQL 行为一致，如果 `ESCAPED BY` 不为空，例如使用默认值 `\`，那么 `\N` 会被视为 NULL。
- 如果使用 `DEFINED NULL BY`，例如 `DEFINED NULL BY 'my-null'`，那么 `'my-null'` 会被视为 NULL。
- 如果使用 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，例如 `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`，那么 `'my-null'` 和 `"my-null"`（假设 `ENCLOSED BY '"'`）都会被视为 NULL。
- 如果不使用 `DEFINED NULL BY` 或 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，但使用 `ENCLOSED BY`，例如 `ENCLOSED BY '"'`，那么空值会被视为 NULL。这与 MySQL 的行为一致。
- 在其他情况下，不会被视为 NULL。

以下是一个示例数据格式：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果你想提取 `bob`、`20` 和 `street 1`，可以将字段分隔符设置为 `','`，包裹字符设置为 `'\"'`：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

如果不指定上述参数，默认导入的数据会被处理为：

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

你可以通过配置 `IGNORE <number> LINES` 参数来忽略文件的前 `<number>` 行。例如，配置 `IGNORE 1 LINES` 时，文件的第一行会被忽略。

## 示例

以下示例使用 `LOAD DATA` 导入数据。字段分隔符为逗号，数据包裹在双引号中，忽略文件的第一行。

<CustomContent platform="tidb">

如果你看到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version`，请参考 [ERROR 1148 (42000): the used command is not allowed with this TiDB version](/error-codes.md#mysql-native-error-messages) 进行排查。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果你看到 `ERROR 1148 (42000): the used command is not allowed with this TiDB version`，请参考 [ERROR 1148 (42000): the used command is not allowed with this TiDB version](https://docs.pingcap.com/tidb/stable/error-codes#mysql-native-error-messages) 进行排查。

</CustomContent>

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

```sql
Query OK, 815264 rows affected (39.63 sec)
Records: 815264  Deleted: 0  Skipped: 0  Warnings: 0
```

`LOAD DATA` 还支持使用十六进制 ASCII 字符表达式或二进制 ASCII 字符表达式作为 `FIELDS ENCLOSED BY` 和 `FIELDS TERMINATED BY` 的参数。示例如下：

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

在上述示例中，`x'2c'` 是逗号 `,` 的十六进制表示，`b'100010'` 是双引号 `"` 的二进制表示。

<CustomContent platform="tidb-cloud">

以下示例演示如何通过 `LOAD DATA INFILE` 语句，将数据从 Amazon S3 导入到 TiDB Cloud Dedicated 集群：

```sql
LOAD DATA INFILE 's3://<your-bucket-name>/your-file.csv?role_arn=<你为 TiDB Cloud 导入创建的 IAM 角色的 ARN>&external_id=<TiDB Cloud 外部 ID（可选）>'
INTO TABLE <your-db-name>.<your-table-name>
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

</CustomContent>

## MySQL 兼容性

`LOAD DATA` 语句的语法与 MySQL 兼容，但字符集选项会被解析但忽略。如果你发现任何语法兼容性差异，可以 [提交 bug](https://docs.pingcap.com/tidb/stable/support)。

<CustomContent platform="tidb">

> **Note:**
>
> - 在 TiDB v4.0.0 之前的版本中，`LOAD DATA` 每提交 20000 行，且无法配置。
> - 在 TiDB v4.0.0 至 v6.6.0 版本中，TiDB 默认在一个事务中提交所有行。但如果你希望 `LOAD DATA` 每次提交固定数量的行，可以设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 为所需的行数。
> - 从 TiDB v7.0.0 开始，`tidb_dml_batch_size` 不再对 `LOAD DATA` 生效，TiDB 会在一个事务中提交所有行。
> - 从 TiDB v4.0.0 或更早版本升级后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` 错误。解决此问题的推荐方法是增加 `tidb.toml` 文件中的 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 配置项的值。
> - 在 TiDB v7.6.0 之前的版本中，无论事务中提交了多少行，`LOAD DATA` 不会被 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - 在 TiDB v7.6.0 之前的版本中，`LOAD DATA` 语句始终在乐观事务模式下执行，不受 TiDB 事务模式配置影响。
> - 从 v7.6.0 开始，TiDB 以与其他 DML 语句相同的方式在事务中处理 `LOAD DATA`：
>     - `LOAD DATA` 不会提交当前事务，也不会开启新事务。
>     - `LOAD DATA` 受 TiDB 事务模式设置（乐观或悲观事务）影响。
>     - 事务中的 `LOAD DATA` 可以通过事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - 在 TiDB v4.0.0 之前的版本中，`LOAD DATA` 每提交 20000 行，且无法配置。
> - 在 TiDB v4.0.0 至 v6.6.0 版本中，TiDB 默认在一个事务中提交所有行。但如果你希望 `LOAD DATA` 每次提交固定数量的行，可以设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 为所需的行数。
> - 从 v7.0.0 开始，`tidb_dml_batch_size` 不再对 `LOAD DATA` 生效，TiDB 会在一个事务中提交所有行。
> - 升级自 TiDB v4.0.0 或更早版本后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058` 错误。解决方案是联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 增加 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 配置项的值。
> - 在 TiDB v7.6.0 之前的版本中，无论事务中提交了多少行，`LOAD DATA` 不会被 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - 在 TiDB v7.6.0 之前的版本中，`LOAD DATA` 语句始终在乐观事务模式下执行，不受 TiDB 事务模式配置影响。
> - 从 v7.6.0 开始，TiDB 以与其他 DML 语句相同的方式在事务中处理 `LOAD DATA`：
>     - `LOAD DATA` 不会提交当前事务，也不会开启新事务。
>     - `LOAD DATA` 受 TiDB 事务模式设置（乐观或悲观事务）影响。
>     - 事务中的 `LOAD DATA` 可以通过事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

## 另见

<CustomContent platform="tidb">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [INSERT](/sql-statements/sql-statement-insert.md)
* [TiDB 乐观事务模型](/optimistic-transaction.md)
* [TiDB 悲观事务模式](/pessimistic-transaction.md)

</CustomContent>
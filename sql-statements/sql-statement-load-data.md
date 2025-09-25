---
title: LOAD DATA | TiDB SQL Statement Reference
summary: TiDB 数据库中 LOAD DATA 的用法概述。
---

# LOAD DATA

`LOAD DATA` 语句用于批量将数据加载到 TiDB 表中。

从 TiDB v7.0.0 开始，`LOAD DATA` SQL 语句支持以下功能：

- 支持从 S3 和 GCS 导入数据
- 新增参数 `FIELDS DEFINED NULL BY`

> **Warning:**
>
> 新参数 `FIELDS DEFINED NULL BY` 以及从 S3 和 GCS 导入数据的功能目前为实验性特性。不建议在生产环境中使用。该功能可能会在没有提前通知的情况下变更或移除。如果你发现了 bug，可以在 GitHub 上[提交 issue](https://github.com/pingcap/tidb/issues)。

<CustomContent platform="tidb-cloud">

> **Note:**
>
> 对于 `LOAD DATA INFILE` 语句，TiDB Cloud Dedicated 支持 `LOAD DATA LOCAL INFILE`，以及从 Amazon S3 或 Google Cloud Storage 加载数据，而 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 和 [TiDB Cloud Essential](https://docs.pingcap.com/tidbcloud/select-cluster-tier#essential) 仅支持 `LOAD DATA LOCAL INFILE`。

</CustomContent>

## 语法

```ebnf+diagram
LoadDataStmt ::=
    'LOAD' 'DATA' LocalOpt 'INFILE' stringLit DuplicateOpt 'INTO' 'TABLE' TableName CharsetOpt Fields Lines IgnoreLines ColumnNameOrUserVarListOptWithBrackets LoadDataSetSpecOpt

LocalOpt ::= ('LOCAL')?

DuplicateOpt ::=
    ( 'IGNORE' | 'REPLACE' )?

Fields ::=
    ('TERMINATED' 'BY' stringLit
    | ('OPTIONALLY')? 'ENCLOSED' 'BY' stringLit
    | 'ESCAPED' 'BY' stringLit
    | 'DEFINED' 'NULL' 'BY' stringLit ('OPTIONALLY' 'ENCLOSED')?)?
```

## 参数说明

### `LOCAL`

你可以使用 `LOCAL` 指定要导入的客户端本地数据文件，此时文件参数必须为客户端文件系统路径。

如果你在使用 TiDB Cloud，想通过 `LOAD DATA` 语句加载本地数据文件，连接 TiDB Cloud 时需要在连接字符串中添加 `--local-infile` 选项。

- 以下是 TiDB Cloud Starter 的连接字符串示例：

    ```
    mysql --connect-timeout 15 -u '<user_name>' -h <host_name> -P 4000 -D test --ssl-mode=VERIFY_IDENTITY --ssl-ca=/etc/ssl/cert.pem -p<your_password> --local-infile
    ```

- 以下是 TiDB Cloud Dedicated 的连接字符串示例：

    ```
    mysql --connect-timeout 15 --ssl-mode=VERIFY_IDENTITY --ssl-ca=<CA_path> --tls-version="TLSv1.2" -u root -h <host_name> -P 4000 -D test -p<your_password> --local-infile
    ```

### `REPLACE` 和 `IGNORE`

你可以使用 `REPLACE` 和 `IGNORE` 指定如何处理重复数据。

- `REPLACE`：覆盖已存在的数据。
- `IGNORE`：忽略重复行，保留已存在的数据。

默认情况下，重复数据会导致报错。

### S3 和 GCS 存储

<CustomContent platform="tidb">

如果未指定 `LOCAL`，文件参数必须为合法的 S3 或 GCS 路径，具体格式详见 [外部存储](/br/backup-and-restore-storages.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

如果未指定 `LOCAL`，文件参数必须为合法的 S3 或 GCS 路径，具体格式详见 [外部存储](https://docs.pingcap.com/tidb/stable/backup-and-restore-storages)。

</CustomContent>

当数据文件存储在 S3 或 GCS 上时，你可以导入单个文件，也可以使用通配符 `*` 匹配多个文件进行导入。注意，通配符不会递归处理子目录下的文件。以下是一些示例：

- 导入单个文件：`s3://<bucket-name>/path/to/data/foo.csv`
- 导入指定路径下的所有文件：`s3://<bucket-name>/path/to/data/*`
- 导入指定路径下所有以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/*.csv`
- 导入指定路径下所有以 `foo` 开头的文件：`s3://<bucket-name>/path/to/data/foo*`
- 导入指定路径下所有以 `foo` 开头且以 `.csv` 结尾的文件：`s3://<bucket-name>/path/to/data/foo*.csv`

### `Fields`、`Lines` 和 `Ignore Lines`

你可以通过 `Fields` 和 `Lines` 参数指定数据格式的处理方式。

- `FIELDS TERMINATED BY`：指定字段分隔符。
- `FIELDS ENCLOSED BY`：指定字段包裹字符。
- `LINES TERMINATED BY`：指定行结束符，如果你希望以某个字符结尾。

你可以使用 `DEFINED NULL BY` 指定数据文件中 NULL 值的表示方式。

- 与 MySQL 行为一致，如果 `ESCAPED BY` 不为 null，例如使用默认值 `\`，则 `\N` 会被视为 NULL 值。
- 如果你使用 `DEFINED NULL BY`，如 `DEFINED NULL BY 'my-null'`，则 `my-null` 会被视为 NULL 值。
- 如果你使用 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，如 `DEFINED NULL BY 'my-null' OPTIONALLY ENCLOSED`，则 `my-null` 和 `"my-null"`（假设 `ENCLOSED BY '"'`）都会被视为 NULL 值。
- 如果你未使用 `DEFINED NULL BY` 或 `DEFINED NULL BY ... OPTIONALLY ENCLOSED`，但使用了 `ENCLOSED BY`，如 `ENCLOSED BY '"'`，则 `NULL` 会被视为 NULL 值。此行为与 MySQL 一致。
- 其他情况下，不会被视为 NULL 值。

以如下数据格式为例：

```
"bob","20","street 1"\r\n
"alice","33","street 1"\r\n
```

如果你想提取 `bob`、`20` 和 `street 1`，需要将字段分隔符指定为 `','`，包裹字符指定为 `'\"'`：

```sql
FIELDS TERMINATED BY ',' ENCLOSED BY '\"' LINES TERMINATED BY '\r\n'
```

如果你未指定上述参数，导入数据时默认按如下方式处理：

```sql
FIELDS TERMINATED BY '\t' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY ''
```

你可以通过配置 `IGNORE <number> LINES` 参数忽略文件的前 `number` 行。例如，配置 `IGNORE 1 LINES` 时，文件的第一行会被忽略。

## 示例

以下示例使用 `LOAD DATA` 导入数据。字段分隔符为逗号，数据包裹的双引号会被忽略，文件的第一行会被忽略。

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

`LOAD DATA` 还支持使用十六进制 ASCII 字符表达式或二进制 ASCII 字符表达式作为 `FIELDS ENCLOSED BY` 和 `FIELDS TERMINATED BY` 的参数。如下示例：

```sql
LOAD DATA LOCAL INFILE '/mnt/evo970/data-sets/bikeshare-data/2017Q4-capitalbikeshare-tripdata.csv' INTO TABLE trips FIELDS TERMINATED BY x'2c' ENCLOSED BY b'100010' LINES TERMINATED BY '\r\n' IGNORE 1 LINES (duration, start_date, end_date, start_station_number, start_station, end_station_number, end_station, bike_number, member_type);
```

在上述示例中，`x'2c'` 是字符 `,` 的十六进制表示，`b'100010'` 是字符 `"` 的二进制表示。

<CustomContent platform="tidb-cloud">

以下示例展示了如何使用 `LOAD DATA INFILE` 语句从 Amazon S3 向 TiDB Cloud Dedicated 集群导入数据：

```sql
LOAD DATA INFILE 's3://<your-bucket-name>/your-file.csv?role_arn=<The ARN of the IAM role you created for TiDB Cloud import>&external_id=<TiDB Cloud external ID (optional)>'
INTO TABLE <your-db-name>.<your-table-name>
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;
```

</CustomContent>

## MySQL 兼容性

`LOAD DATA` 语句的语法与 MySQL 兼容，字符集相关选项会被解析但会被忽略。如果你发现任何语法兼容性差异，可以[提交 bug](https://docs.pingcap.com/tidb/stable/support)。

<CustomContent platform="tidb">

> **Note:**
>
> - TiDB v4.0.0 之前的版本，`LOAD DATA` 每 20000 行提交一次，且不可配置。
> - TiDB v4.0.0 到 v6.6.0 版本，默认情况下 TiDB 会将所有行在一个事务中提交。但如果你需要 `LOAD DATA` 语句每固定行数提交一次，可以设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 为期望的行数。
> - 从 TiDB v7.0.0 开始，`tidb_dml_batch_size` 对 `LOAD DATA` 不再生效，TiDB 会将所有行在一个事务中提交。
> - 从 TiDB v4.0.0 或更早版本升级后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`。推荐的解决方法是增加 `tidb.toml` 文件中的 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 配置值。
> - TiDB v7.6.0 之前的版本，无论每个事务提交多少行，`LOAD DATA` 在显式事务中都不会被 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - TiDB v7.6.0 之前的版本，`LOAD DATA` 语句始终以乐观事务模式执行，无论 TiDB 的事务模式配置如何。
> - 从 v7.6.0 开始，TiDB 处理 `LOAD DATA` 事务的方式与其他 DML 语句一致：
>     - `LOAD DATA` 语句不会提交当前事务，也不会开启新事务。
>     - `LOAD DATA` 语句会受到 TiDB 事务模式（乐观或悲观事务）的影响。
>     - 事务中的 `LOAD DATA` 语句可以被该事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **Note:**
>
> - TiDB v4.0.0 之前的版本，`LOAD DATA` 每 20000 行提交一次，且不可配置。
> - TiDB v4.0.0 到 v6.6.0 版本，默认情况下 TiDB 会将所有行在一个事务中提交。但如果你需要 `LOAD DATA` 语句每固定行数提交一次，可以设置 [`tidb_dml_batch_size`](/system-variables.md#tidb_dml_batch_size) 为期望的行数。
> - 从 v7.0.0 开始，`tidb_dml_batch_size` 对 `LOAD DATA` 不再生效，TiDB 会将所有行在一个事务中提交。
> - 从 TiDB v4.0.0 或更早版本升级后，可能会出现 `ERROR 8004 (HY000) at line 1: Transaction is too large, size: 100000058`。如需解决该错误，可以联系 [TiDB Cloud Support](https://docs.pingcap.com/tidbcloud/tidb-cloud-support) 增加 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 配置值。
> - TiDB v7.6.0 之前的版本，无论每个事务提交多少行，`LOAD DATA` 在显式事务中都不会被 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。
> - TiDB v7.6.0 之前的版本，`LOAD DATA` 语句始终以乐观事务模式执行，无论 TiDB 的事务模式配置如何。
> - 从 v7.6.0 开始，TiDB 处理 `LOAD DATA` 事务的方式与其他 DML 语句一致：
>     - `LOAD DATA` 语句不会提交当前事务，也不会开启新事务。
>     - `LOAD DATA` 语句会受到 TiDB 事务模式（乐观或悲观事务）的影响。
>     - 事务中的 `LOAD DATA` 语句可以被该事务中的 [`ROLLBACK`](/sql-statements/sql-statement-rollback.md) 语句回滚。

</CustomContent>

## 相关内容

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

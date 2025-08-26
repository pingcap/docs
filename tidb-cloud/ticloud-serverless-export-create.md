---
title: ticloud serverless export create
summary: The reference of `ticloud serverless export create`.
---

# ticloud serverless export create

从 TiDB Cloud Serverless 集群导出数据：

```shell
ticloud serverless export create [flags]
```

## 示例

以交互模式从 TiDB Cloud Serverless 集群导出数据：

```shell
ticloud serverless export create
```

以非交互模式将 TiDB Cloud Serverless 集群的数据导出到本地文件：

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

以非交互模式将 TiDB Cloud Serverless 集群的数据导出到 Amazon S3：

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

以非交互模式将 TiDB Cloud Serverless 集群的数据导出到 Google Cloud Storage：

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

以非交互模式将 TiDB Cloud Serverless 集群的数据导出到 Azure Blob Storage：

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

以非交互模式将 TiDB Cloud Serverless 集群的数据导出到阿里云 OSS：

```shell
ticloud serverless export create -c <cluster-id> --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter <database.table>
```

以非交互模式将数据导出为 Parquet 文件并使用 `SNAPPY` 压缩：

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

以非交互模式通过 SQL 语句导出数据：

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## 参数

在非交互模式下，你需要手动输入所需的参数。在交互模式下，你只需按照 CLI 提示填写即可。

| 参数                             | 描述                                                                                                                                                                   | 是否必需 | 备注                                                 |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string          | 指定你要导出数据的集群 ID。                                                                                                      | 是       | 仅在非交互模式下生效。                              |
| --file-type string               | 指定导出文件类型。可选值为 ["SQL" "CSV" "PARQUET"]。（默认值为 "CSV"）                                                                                                 | 否       | 仅在非交互模式下生效。                              |
| --target-type string             | 指定导出目标。可选值为 [`"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` `"OSS"`]。默认值为 `"LOCAL"`。                                    | 否       | 仅在非交互模式下生效。                              |
| --s3.uri string                  | 指定 S3 URI，格式为 `s3://<bucket>/<file-path>`。当目标类型为 S3 时必填。                                                        | 否       | 仅在非交互模式下生效。                              |
| --s3.access-key-id string        | 指定 Amazon S3 的访问密钥 ID。你只需设置 s3.role-arn 和 [s3.access-key-id, s3.secret-access-key] 其中之一。                      | 否       | 仅在非交互模式下生效。                              |
| --s3.secret-access-key string    | 指定 Amazon S3 的访问密钥 Secret。你只需设置 s3.role-arn 和 [s3.access-key-id, s3.secret-access-key] 其中之一。                   | 否       | 仅在非交互模式下生效。                              |
| --s3.role-arn string             | 指定 Amazon S3 的角色 ARN。你只需设置 s3.role-arn 和 [s3.access-key-id, s3.secret-access-key] 其中之一。                         | 否       | 仅在非交互模式下生效。                              |
| --gcs.uri string                 | 指定 GCS URI，格式为 `gcs://<bucket>/<file-path>`。当目标类型为 GCS 时必填。                                                     | 否       | 仅在非交互模式下生效。                              |
| --gcs.service-account-key string | 指定 GCS 的 base64 编码服务账号密钥。                                                                                            | 否       | 仅在非交互模式下生效。                              |
| --azblob.uri string              | 指定 Azure Blob URI，格式为 `azure://<account>.blob.core.windows.net/<container>/<file-path>`。当目标类型为 AZURE_BLOB 时必填。 | 否       | 仅在非交互模式下生效。                              |
| --azblob.sas-token string        | 指定 Azure Blob 的 SAS token。                                                                                                   | 否       | 仅在非交互模式下生效。                              |
| --oss.uri string                 | 指定阿里云 OSS URI，格式为 `oss://<bucket>/<file-path>`。当导出 `target-type` 为 `"OSS"` 时必填。                                | 否       | 仅在非交互模式下生效。                              |
| --oss.access-key-id string       | 指定访问阿里云 OSS 的 AccessKey ID。                                                                                            | 否       | 仅在非交互模式下生效。                              |
| --oss.access-key-secret string   | 指定访问阿里云 OSS 的 AccessKey Secret。                                                                                        | 否       | 仅在非交互模式下生效。                              |
| --csv.delimiter string           | 指定 CSV 文件中字符串类型变量的定界符。（默认值为 "\""）                                                                         | 否       | 仅在非交互模式下生效。                              |
| --csv.null-value string          | 指定 CSV 文件中 null 值的表示方式。（默认值为 "\\N"）                                                                           | 否       | 仅在非交互模式下生效。                              |
| --csv.separator string           | 指定 CSV 文件中每个值的分隔符。（默认值为 ","）                                                                                  | 否       | 仅在非交互模式下生效。                              |
| --csv.skip-header                | 导出表的 CSV 文件时不包含表头。                                                                                                 | 否       | 仅在非交互模式下生效。                              |
| --parquet.compression string     | 指定 Parquet 的压缩算法。可选值为 [`"GZIP"` `"SNAPPY"` `"ZSTD"` `"NONE"`]。默认值为 `"ZSTD"`。                                   | 否       | 仅在非交互模式下生效。                              |
| --filter strings                 | 通过表过滤模式指定要导出的表。不要与 --sql 一起使用。更多信息参见 [Table Filter](/table-filter.md)。                             | 否       | 仅在非交互模式下生效。                              |
| --sql string                     | 通过 `SQL SELECT` 语句过滤导出数据。                                                                                            | 否       | 仅在非交互模式下生效。                              |
| --where string                   | 通过 `WHERE` 条件过滤导出表。不要与 --sql 一起使用。                                                                            | 否       | 仅在非交互模式下生效。                              |
| --compression string             | 指定导出文件的压缩算法。支持的算法包括 `GZIP`、`SNAPPY`、`ZSTD` 和 `NONE`。默认值为 `GZIP`。                                    | 否       | 仅在非交互模式下生效。                              |
| --force                          | 无需确认直接创建导出任务。当你在非交互模式下导出整个集群时需要确认。                                                            | 否       | 仅在非交互模式下生效。                              |
| -h, --help                       | 显示该命令的帮助信息。                                                                                                          | 否       | 在非交互和交互模式下均可用。                        |

## 继承参数

| 参数                 | 描述                                                                                          | 是否必需 | 备注                                                                                                             |
|----------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | 禁用输出中的颜色。                                                                            | 否       | 仅在非交互模式下生效。在交互模式下，禁用颜色可能会影响部分 UI 组件的显示。                                       |
| -P, --profile string | 指定该命令使用的活动 [用户配置文件](/tidb-cloud/cli-reference.md#user-profile)。              | 否       | 在非交互和交互模式下均可用。                                                                                     |
| -D, --debug          | 启用调试模式。                                                                                | 否       | 在非交互和交互模式下均可用。                                                                                     |

## 反馈

如果你对 TiDB Cloud CLI 有任何问题或建议，欢迎创建 [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose)。我们也欢迎任何贡献。
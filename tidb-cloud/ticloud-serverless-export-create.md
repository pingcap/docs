---
title: ticloud serverless export create
summary: The reference of `ticloud serverless export create`.
---

# ticloud serverless export create

Export data from a TiDB Cloud cluster:

```shell
ticloud serverless export create [flags]
```

## Examples

Export data from a TiDB Cloud cluster in interactive mode:

```shell
ticloud serverless export create
```

Export data from a TiDB Cloud cluster to a local file in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

Export data from a TiDB Cloud cluster to Amazon S3 in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

Export data from a TiDB Cloud cluster to Google Cloud Storage in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

Export data from a TiDB Cloud cluster to Azure Blob Storage in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

Export data from a TiDB Cloud cluster to Alibaba Cloud OSS in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --oss.uri <uri> --oss.access-key-id <access-key-id> --oss.access-key-secret <access-key-secret> --filter <database.table>
```

Export data to a Parquet file and compress it with `SNAPPY` in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

Export data with SQL statements in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                             | Description                                                                                                                                                                   | Required | Note                                                 |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string          | Specifies the ID of the cluster, from which you want to export data.                                                                                                          | Yes      | Only works in non-interactive mode.                  |
| --file-type string               | Specifies the export file type. One of ["SQL" "CSV" "PARQUET"]. (default "CSV")                                                                                                         | No       | Only works in non-interactive mode.                  |
| --target-type string             | Specifies the export target. One of [`"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"` `"OSS"`]. The default value is `"LOCAL"`.                                                                                                | No       | Only works in non-interactive mode.                  |
| --s3.uri string                  | Specifies the S3 URI in `s3://<bucket>/<file-path>` format. Required when the target type is S3.                                                                                            | No       | Only works in non-interactive mode.                  |
| --s3.access-key-id string        | Specifies the access key ID of Amazon S3. You only need to set one of the s3.role-arn and [s3.access-key-id, s3.secret-access-key].                                                        | NO       | Only works in non-interactive mode.                  |
| --s3.secret-access-key string    | Specifies the secret access key of Amazon S3. You only need to set one of the s3.role-arn and [s3.access-key-id, s3.secret-access-key].                                                   | No       | Only works in non-interactive mode.                  |
| --s3.role-arn string             | Specifies the role ARN of Amazon S3. You only need to set one of the s3.role-arn and [s3.access-key-id, s3.secret-access-key].                                                             | No       | Only works in non-interactive mode.                  |
| --gcs.uri string                 | Specifies the GCS URI in `gcs://<bucket>/<file-path>` format. Required when the target type is GCS.                                                                                         | No       | Only works in non-interactive mode.                  |
| --gcs.service-account-key string | Specifies the base64 encoded service account key of GCS.                                                                                                                                | No       | Only works in non-interactive mode.                  |
| --azblob.uri string              | Specifies the Azure Blob URI in `azure://<account>.blob.core.windows.net/<container>/<file-path>` format. Required when the target type is AZURE_BLOB.                                      | No       | Only works in non-interactive mode.                  |
| --azblob.sas-token string        | Specifies the SAS token of Azure Blob.                                                                                                                                                  | No       | Only works in non-interactive mode.                  |
| --oss.uri string        | Specifies the Alibaba Cloud OSS URI in `oss://<bucket>/<file-path>` format. Required when the export `target-type` is `"OSS"`.                                                                                                                                            | No       | Only works in non-interactive mode.                  |
| --oss.access-key-id string        | Specifies the AccessKey ID to access Alibaba Cloud OSS.                                                                                                                                     | No       | Only works in non-interactive mode.                  |
| --oss.access-key-secret string        | Specifies the AccessKey secret to access Alibaba Cloud OSS.                                                                                                                                     | No       | Only works in non-interactive mode.                   |
| --csv.delimiter string           | Specifies the delimiter of string type variables in CSV files. (default "\"")                                                                                                         | No       | Only works in non-interactive mode.                  |
| --csv.null-value string          | Specifies the representation of null values in CSV files. (default "\\N")                                                                                                                   | No       | Only works in non-interactive mode.                  |
| --csv.separator string           | Specifies the separator of each value in CSV files. (default ",")                                                                                                                           | No       | Only works in non-interactive mode.                  |
| --csv.skip-header                | Exports CSV files of the tables without header.                                                                                                                                | No       | Only works in non-interactive mode.                  |
| --parquet.compression string     | Specifies the Parquet compression algorithm. One of [`"GZIP"` `"SNAPPY"` `"ZSTD"` `"NONE"`]. The default value is `"ZSTD"`.                                                                                   | No       | Only works in non-interactive mode.                  |
| --filter strings                 | Specifies the exported tables with table filter patterns. Do not use it with --sql. For more information, see [Table Filter](/table-filter.md). | No       | Only works in non-interactive mode.                  |
| --sql string                     | Filters the exported data with the `SQL SELECT` statement.                                                                                                                           | No       | Only works in non-interactive mode.                  |
| --where string                   | Filters the exported tables with the `WHERE` condition. Do not use it with --sql.                                                                                         | No       | Only works in non-interactive mode.                  |
| --compression string             | Specifies the compression algorithm of the export file. The supported algorithms include `GZIP`, `SNAPPY`, `ZSTD`, and `NONE`. The default value is `GZIP`.                   | No       | Only works in non-interactive mode.                  |
| --force                          | Creates the export task without confirmation. You need to confirm when you want to export the whole cluster in non-interactive mode.                                                           | No       | Only works in non-interactive mode.                  |
| -h, --help                       | Shows help information for this command.                                                                                                                                      | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless export create
summary: The reference of `ticloud serverless export create`.
---

# ticloud serverless export create

Export data from a TiDB Cloud Serverless cluster:

```shell
ticloud serverless export create [flags]
```

## Examples

Export data from a TiDB Cloud Serverless cluster in interactive mode:

```shell
ticloud serverless export create
```

Export data from a TiDB Cloud Serverless cluster to a local file in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --filter <database.table>
```

Export data from a TiDB Cloud Serverless cluster to Amazon S3 in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --s3.uri <bucket-uri> --s3.access-key-id <access-key-id> --s3.secret-access-key <secret-access-key> --filter <database.table>
```

Export data from a TiDB Cloud Serverless cluster to Google Cloud Storage in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --gcs.uri <uri> --gcs.service-account-key <service-account-key> --filter <database.table>
```

Export data from a TiDB Cloud Serverless cluster to Azure Blob Storage in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --azblob.uri <uri> --azblob.sas-token <sas-token> --filter <database.table>
```

Export data to a Parquet file in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --file-type parquet --parquet.compression SNAPPY --filter <database.table>
```

Export data with SQL statements in non-interactive mode:

```shell
ticloud serverless export create -c <cluster-id> --sql 'select * from database.table'
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                             | Description                                                                                                                                                 | Required | Note                                                 |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string          | Specifies the ID of the cluster, from which you want to export data.                                                                                        | Yes      | Only works in non-interactive mode.                  |
| --file-type string               | Specifies the format of the exported file. The supported formats include `CSV` and `SQL`. The default value is `SQL`.                                       | No       | Only works in non-interactive mode.                  |
| --target-type string             | Specifies the exported location. The supported location includes `LOCAL` and `S3`. The default value is `LOCAL`.                                            | No       | Only works in non-interactive mode.                  |
| --s3.uri string                  | Specifies the URI of the S3. This flag is required when you export data to Amazon S3.                                                                       | No       | Only works in non-interactive mode.                  |
| --s3.access-key-id string        | Specifies the access key ID of the S3 bucket. This flag is required when you export data to Amazon S3.                                                      | NO       | Only works in non-interactive mode.                  |
| --s3.secret-access-key string    | Specifies the secret access key of the S3 bucket. This flag is required when you export data to Amazon S3.                                                  | No       | Only works in non-interactive mode.                  |
| --s3.role-arn string             | The role arn of the S3. You only need to set one of the s3.role-arn and [s3.access-key-id, s3.secret-access-key].                                           | No       | Only works in non-interactive mode.                  |
| --gcs.uri string                 | The GCS URI in gcs://<bucket>/<path> format. Required when target type is GCS.                                                                              | No       | Only works in non-interactive mode.                  |
| --gcs.service-account-key string | The base64 encoded service account key of GCS.                                                                                                              | No       | Only works in non-interactive mode.                  |
| --azblob.uri string              | The Azure Blob URI in azure://<account>.blob.core.windows.net/<container>/<path> format. Required when target type is AZURE_BLOB.                           | No       | Only works in non-interactive mode.                  |
| --azblob.sas-token string        | The SAS token of Azure Blob.                                                                                                                                | No       | Only works in non-interactive mode.                  |
| --csv.delimiter string           | Delimiter of string type variables in CSV files. (default "\"")                                                                                             | No       | Only works in non-interactive mode.                  |
| --csv.null-value string          | Representation of null values in CSV files. (default "\\N")                                                                                                 | No       | Only works in non-interactive mode.                  |
| --csv.separator string           | Separator of each value in CSV files. (default ",")                                                                                                         | No       | Only works in non-interactive mode.                  |
| --csv.skip-header                | Export CSV files of the tables without header.                                                                                                              | No       | Only works in non-interactive mode.                  |
| --parquet.compression string     | The parquet compression algorithm. One of ["GZIP" "SNAPPY" "ZSTD" "NONE"]. (default "ZSTD")                                                                 | No       | Only works in non-interactive mode.                  |
| --filter strings                 | Specify the exported table(s) with table filter patterns. See https://docs.pingcap.com/tidb/stable/table-filter to learn table filter.                      | No       | Only works in non-interactive mode.                  |
| --sql string                     | Filter the exported data with SQL SELECT statement.                                                                                                         | No       | Only works in non-interactive mode.                  |
| --where string                   | Filter the exported table(s) with the where condition, it can not be used with --sql                                                                        | No       | Only works in non-interactive mode.                  |
| --compression string             | Specifies the compression algorithm of the export file. The supported algorithms include `GZIP`, `SNAPPY`, `ZSTD`, and `NONE`. The default value is `GZIP`. | No       | Only works in non-interactive mode.                  |
| --force                          | Create without confirmation. You need to confirm when you want to export the whole cluster in non-interactive mode.                                         | No       | Only works in non-interactive mode.                  |
| -h, --help                       | Shows help information for this command.                                                                                                                    | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

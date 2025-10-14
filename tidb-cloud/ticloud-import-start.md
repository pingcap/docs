---
title: ticloud serverless import start
summary: The reference of `ticloud serverless import start`.
aliases: ['/tidbcloud/ticloud-import-start-local','/tidbcloud/ticloud-import-start-mysql','/tidbcloud/ticloud-import-start-s3']
---

# ticloud serverless import start

Start a data import task:

```shell
ticloud serverless import start [flags]
```

Or use the following alias command:

```shell
ticloud serverless import create [flags]
```

> **Note:**
>
> Currently, you can only import one CSV file for one local import task.

## Examples

Start an import task in interactive mode:

```shell
ticloud serverless import start
```

Start a local import task in non-interactive mode:

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table>
```

Start a local import task with custom upload concurrency:

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type <file-type> --local.target-database <target-database> --local.target-table <target-table> --local.concurrency 10
```

Start a local import task with custom CSV format:

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type CSV --local.target-database <target-database> --local.target-table <target-table> --csv.separator \" --csv.delimiter \' --csv.backslash-escape=false --csv.trim-last-separator=true
```

Start an S3 import task in non-interactive mode:

```shell
ticloud serverless import start --source-type S3 --s3.uri <s3-uri> --cluster-id <cluster-id> --file-type <file-type> --s3.role-arn <role-arn>
```

Start a GCS import task in non-interactive mode:

```shell
ticloud serverless import start --source-type GCS --gcs.uri <gcs-uri> --cluster-id <cluster-id> --file-type <file-type> --gcs.service-account-key <service-account-key>
```

Start an Azure Blob import task in non-interactive mode:

```shell
ticloud serverless import start --source-type AZURE_BLOB --azblob.uri <azure-blob-uri> --cluster-id <cluster-id> --file-type <file-type> --azblob.sas-token <sas-token>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                             | Description                                                                                                                | Required | Note                                                 |
|----------------------------------|----------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| --azblob.sas-token string        | Specifies the SAS token of Azure Blob.                                                                                               | No       | Only works in non-interactive mode.                  |
| --azblob.uri string              | Specifies the Azure Blob URI in `azure://<account>.blob.core.windows.net/<container>/<path>` format.                                   | No       | Only works in non-interactive mode.                  |
| --gcs.service-account-key string | Specifies the base64 encoded service account key of GCS.                                                                             | No       | Only works in non-interactive mode.                  |
| --gcs.uri string                 | Specifies the GCS URI in `gcs://<bucket>/<path>` format. Required when source type is GCS.                                             | Yes      | Only works in non-interactive mode.                  |
| --s3.access-key-id string        | Specifies the access key ID of Amazon S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`].     | No       | Only works in non-interactive mode.                  |
| --s3.role-arn string             | Specifies the role ARN of Amazon S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`].          | No       | Only works in non-interactive mode.                  |
| --s3.secret-access-key string    | Specifies the secret access key of Amazon S3. You only need to set one of the `s3.role-arn` and [`s3.access-key-id`, `s3.secret-access-key`]. | No       | Only works in non-interactive mode.                  |
| --s3.uri string                  | Specifies the S3 URI in `s3://<bucket>/<path>` format. Required when source type is S3.                                                | Yes      | Only works in non-interactive mode.                  |
| --source-type string             | Specifies the import source type, one of [`"LOCAL"` `"S3"` `"GCS"` `"AZURE_BLOB"`]. The default value is `"LOCAL"`.                                        | No       | Only works in non-interactive mode.                  |
| -c, --cluster-id string          | Specifies the cluster ID.                                                                                                  | Yes      | Only works in non-interactive mode.                  |
| --local.concurrency int          | Specifies the concurrency for uploading files. The default value is `5`.                                                   | No       | Only works in non-interactive mode.                  |
| --local.file-path string         | Specifies the path of the local file to be imported.                                                                       | No       | Only works in non-interactive mode.                  |
| --local.target-database string   | Specifies the target database to which the data is imported.                                                               | No       | Only works in non-interactive mode.                  |
| --local.target-table string      | Specifies the target table to which the data is imported.                                                                  | No       | Only works in non-interactive mode.                  |
| --file-type string               | Specifies the import file type, one of ["CSV" "SQL" "AURORA_SNAPSHOT" "PARQUET"].                                                    | Yes      | Only works in non-interactive mode.                  |
| --csv.backslash-escape           | Specifies whether to parse backslash inside fields as escape characters in a CSV file. The default value is `true`.        | No       | Only works in non-interactive mode.                  |
| --csv.delimiter string           | Specifies the delimiter used for quoting a CSV file. The default value is `\`.                                             | No       | Only works in non-interactive mode.                  |
| --csv.separator string           | Specifies the field separator in a CSV file. The default value is `,`.                                                     | No       | Only works in non-interactive mode.                  |
| --csv.skip-header                | Specifies whether the CSV file contains a header line.                                                                     | No       | Only works in non-interactive mode.                  |
| --csv.trim-last-separator        | Specifies whether to treat the separator as the line terminator and trim all trailing separators in a CSV file.            | No       | Only works in non-interactive mode.                  |
| --csv.not-null                   | Specifies whether a CSV file can contain any NULL values.                                                                  | No       | Only works in non-interactive mode.                  |
| --csv.null-value string          | Specifies the representation of NULL values in the CSV file. (default "\\N")                                                       | No       | Only works in non-interactive mode.                  |
| -h, --help                       | Shows help information for this command.                                                                                   | No       | Works in both non-interactive and interactive modes. |                                                                           | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

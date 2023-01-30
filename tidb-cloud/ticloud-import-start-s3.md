---
title: ticloud import start s3
Summary: The reference of `ticloud import start s3`.
---

# ticloud import start s3

Import files from Amazon S3 into TiDB Cloud:

```shell
ticloud import start s3 [flags]
```

> **Note:**
>
> Before importing files from Amazon S3 into TiDB Cloud, you need to configure the Amazon S3 bucket access for TiDB Cloud and get the Role ARN. For more information, see [Configure Amazon S3 access](/tidb-cloud/config-s3-and-gcs-access.md#configure-amazon-s3-access).

## Examples

Start an import task in interactive mode:

```shell
ticloud import start s3
```

Start an import task in non-interactive mode:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format <data-format> --source-url <source-url>
```

Start an import task with a custom CSV format:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format CSV --source-url <source-url> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                    | Description                                              | Required | Note                             |
|-------------------------|----------------------------------------------------------|----------|-----------------------------------|
| --aws-role-arn string   | AWS S3 IAM Role ARN                                      | Yes      | Only works in non-interactive mode. |
| -c, --cluster-id string | Cluster ID                                               | Yes      | Only works in non-interactive mode. |
| --data-format string    | Data format. Valid values are `CSV`, `SqlFile`, `Parquet`, or `AuroraSnapshot`. | Yes      | Only works in non-interactive mode. |
| -h, --help              | Gets the help information for this command                                | No       | Works in both non-interactive and interactive modes. |
| -p, --project-id string | Project ID                                               | Yes      | Only works in non-interactive mode. |
| --source-url string     | The S3 path where the source data files are stored         | Yes      | Only works in non-interactive mode. |

## Inherited flags

| Flag                  | Description                                                                                    | Required | Note                                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --backslash-escape    | Parses backslashes inside fields as escape characters (`true` by default) for CSV files | No       | Only works in non-interactive mode when `--data-format CSV` is specified.                                                         |
| --delimiter string    | Specifies the delimiter used for quoting (`"` by default) for CSV files                                     | No       | Only works in non-interactive mode when `--data-format CSV` is specified.                                                         |
| --no-color            | Disables color in output                                                                           | No       | Only works in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string  | Specifies the active [user profile](tidb-cloud/cli-reference.md#user-profile) used in this command      | No       | Works in both non-interactive and interactive modes.                                                               |
| --separator string    | Specifies the field separator of CSV files (`,` by default)                                                  | No       | Only works in non-interactive mode when `--data-format CSV` is specified.                                                         |
| --trim-last-separator | Treats separators as the line terminators and trims all trailing separators for CSV files | No       | Only works in non-interactive mode when `--data-format CSV` is specified.                                                |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

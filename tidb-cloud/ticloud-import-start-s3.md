---
title: ticloud import start s3
Summary: The reference of `ticloud import start s3`.
---

# ticloud import start s3

Import files from Amazon S3 into TiDB Cloud

```shell
ticloud import start s3 [flags]
```

## Examples

Start an import task in interactive mode:

```shell
ticloud import start s3
```

Start an import task in non-interactive mode:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format <data-format> --source-url <source-url>
```

Start an import task with custom CSV format:

```shell
ticloud import start s3 --project-id <project-id> --cluster-id <cluster-id> --aws-role-arn <aws-role-arn> --data-format CSV --source-url <source-url> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                    | Description                                              | Required | Notes                             |
|-------------------------|----------------------------------------------------------|----------|-----------------------------------|
| --aws-role-arn string   | AWS S3 IAM Role ARN                                      | Yes      | Only work in non-interactive mode |
| -c, --cluster-id string | Cluster ID                                               | Yes      | Only work in non-interactive mode |
| --data-format string    | Data format, one of [CSV SqlFile Parquet AuroraSnapshot] | Yes      | Only work in non-interactive mode |
| -h, --help              | Get the help information                                 | No       |                                   |
| -p, --project-id string | Project ID                                               | Yes      | Only work in non-interactive mode |
| --source-url string     | The S3 path where the source data file is stored         | Yes      | Only work in non-interactive mode |

## Inherited flags

| Flag                  | Description                                                                                    | Required | Notes                                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --backslash-escape    | In CSV file whether to parse backslash inside fields as escape characters (default true)       | No       | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --delimiter string    | The delimiter used for quoting of CSV file (default "\"")                                      | No       | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --no-color            | Disable color output                                                                           | No       | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string  | The active [user profile](tidb-cloud/cli-reference.md#user-profile) used in this command.      | No       | Work in both non-interactive and interactive modes.                                                               |
| --separator string    | The field separator of CSV file (default ",")                                                  | No       | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --trim-last-separator | In CSV file whether to treat Separator as the line terminator and trim all trailing separators | No       | Only work in non-interactive mode and "--data-format CSV"                                                         |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

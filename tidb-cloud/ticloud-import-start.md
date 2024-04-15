---
title: ticloud serverless import start
summary: The reference of `ticloud serverless import start`.
aliases: ['/tidbcloud/ticloud-import-start-local', '/tidbcloud/ticloud-import-start-mysql, '/tidbcloud/ticloud-import-start-s3']
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
> Currently, you can only import one CSV file for one import task.

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

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                           | Description                                                                                                         | Required | Note                                                                      |
|--------------------------------|---------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------|
| -c, --cluster-id string        | Specifies the cluster ID.                                                                                           | Yes      | Only works in non-interactive mode.                                       |
| --source-type string           | Specifies the import source type. The default value is `LOCAL`.                                                     | No       | Only works in non-interactive mode.                                       |
| --local.concurrency int        | Specifies the concurrency for uploading files. The default value is `5`.                                            | No       | Only works in non-interactive mode.                                       |
| --local.file-path string       | Specifies the path of the local file to be imported.                                                                | No       | Only works in non-interactive mode.                                       |
| --local.target-database string | Specifies the target database to which the data is imported.                                                        | No       | Only works in non-interactive mode.                                       |
| --local.target-table string    | Specifies the target table to which the data is imported.                                                           | No       | Only works in non-interactive mode.                                       |
| --file-type string             | Specifies the import file type. Currently, only `CSV` is supported.                                                 | Yes      | Only works in non-interactive mode.                                       |
| --csv.backslash-escape         | Specifies whether to parse backslash inside fields as escape characters in a CSV file. The default value is `true`. | No       | Only works in non-interactive mode.                                       |
| --csv.delimiter string         | Specifies the delimiter used for quoting a CSV file. The default value is `\`.                                      | No       | Only works in non-interactive mode.                                       |
| --csv.separator string         | Specifies the field separator in a CSV file. The default value is `,`.                                              | No       | Only works in non-interactive mode.                                       |
| --csv.trim-last-separator      | Specifies whether to treat the separator as the line terminator and trim all trailing separators in a CSV file.     | No       | Only works in non-interactive mode.                                       |
| -h, --help                     | Shows help information for this command.                                                                            | No       | Works in both non-interactive and interactive modes.                      |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

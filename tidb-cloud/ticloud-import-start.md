---
title: ticloud serverless import start
summary: The reference of `ticloud serverless import start`.
---

# ticloud serverless import start local

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

Start an local import task with custom CSV format:

```shell
ticloud serverless import start --local.file-path <file-path> --cluster-id <cluster-id> --file-type CSV --local.target-database <target-database> --local.target-table <target-table> --csv.separator \" --csv.delimiter \' --csv.backslash-escape=false --csv.trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                           | Description                                                                                                                   | Required | Note                                                                      |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------------------|----------|---------------------------------------------------------------------------|
| -c, --cluster-id string        | Specifies the cluster ID.                                                                                                     | Yes      | Only works in non-interactive mode.                                       |
| --source-type string           | The import source type, one of ["LOCAL"]. (default "LOCAL")                                                                   | No       | Only works in non-interactive mode.                                       |
| --local.concurrency int        | The concurrency for uploading file. (default 5)                                                                               | No       | Only works in non-interactive mode.                                       |
| --local.file-path string       | The local file path to import.                                                                                                | No       | Only works in non-interactive mode.                                       |
| --local.target-database string | Target database to which import data.                                                                                         | No       | Only works in non-interactive mode.                                       |
| --local.target-table string    | Target table to which import data.                                                                                            | No       | Only works in non-interactive mode.                                       |
| --local.file-path string       | The local file path to import.                                                                                                | No       | Only works in non-interactive mode.                                       |
| --file-type string             | The import file type, one of ["CSV"].                                                                                         | Yes      | Only works in non-interactive mode.                                       |
| --csv.backslash-escape         | In CSV file whether to parse backslash inside fields as escape characters. (default true)                                     | No       | Only works in non-interactive mode.                                       |
| --csv.delimiter string         | The delimiter used for quoting of CSV file. (default "\"")                                                                    | No       | Only works in non-interactive mode.                                       |
| --csv.separator string         | The field separator of CSV file. (default ",")                                                                                | No       | Only works in non-interactive mode.                                       |
| --csv.trim-last-separator      | In CSV file whether to treat separator as the line terminator and trim all trailing separators.                               | No       | Only works in non-interactive mode.                                       |
| -h, --help                     | Shows help information for this command.                                                                                      | No       | Works in both non-interactive and interactive modes.                      |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

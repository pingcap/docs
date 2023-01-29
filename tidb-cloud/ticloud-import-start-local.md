---
title: ticloud import start local
Summary: The reference of `ticloud import start local`.
---

# ticloud import start local

Import a local file to TiDB Cloud

```shell
ticloud import start local <file-path> [flags]
```

## Examples

Start an import task in interactive mode:

```shell
ticloud import start local <file-path>
```

Start an import task in non-interactive mode:

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format <data-format> --target-database <target-database> --target-table <target-table>
```

Start an import task with custom CSV format:

```shell
ticloud import start local <file-path> --project-id <project-id> --cluster-id <cluster-id> --data-format CSV --target-database <target-database> --target-table <target-table> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                     | Description                          | Required | Notes                             |
|--------------------------|--------------------------------------|----------|-----------------------------------|
 | -c, --cluster-id string  | Cluster ID                           | Yes      | Only work in non-interactive mode |
 | --data-format string     | Data format, one of [CSV]            | Yes      | Only work in non-interactive mode |
 | -h, --help               | Get the help information             | No       |                                   |
 | -p, --project-id string  | Project ID                           | Yes      | Only work in non-interactive mode |
 | --target-database string | Target database to which import data | Yes      | Only work in non-interactive mode |
 | --target-table string    | Target table to which import data    | Yes      | Only work in non-interactive mode |

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

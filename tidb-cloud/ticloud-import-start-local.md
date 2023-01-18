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

| Flag                     | Description                          | Required | Extra                             |
|--------------------------|--------------------------------------|----------|-----------------------------------|
 | -c, --cluster-id string  | Cluster ID                           | true     | Only work in non-interactive mode |
 | --data-format string     | Data format, one of [CSV]            | true     | Only work in non-interactive mode |
 | -h, --help               | help for local                       |          |                                   |
 | -p, --project-id string  | Project ID                           | true     | Only work in non-interactive mode |
 | --target-database string | Target database to which import data | true     | Only work in non-interactive mode |
 | --target-table string    | Target table to which import data    | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                  | Description                                                                                    | Required | Extra                                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --backslash-escape    | In CSV file whether to parse backslash inside fields as escape characters (default true)       | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --delimiter string    | The delimiter used for quoting of CSV file (default "\"")                                      | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --no-color            | Disable color output                                                                           | false    | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string  | Profile to use from your configuration file.                                                   | false    | Work in both modes                                                                                                |
| --separator string    | The field separator of CSV file (default ",")                                                  | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --trim-last-separator | In CSV file whether to treat Separator as the line terminator and trim all trailing separators | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we welcome any contributions.

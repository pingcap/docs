# ticloud import start local

Import a local file to TiDB Cloud

{{< copyable "shell-regular" >}}

```shell
ticloud import start local <filePath> [flags]
```

## Examples

Start an import task in interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import start local <filePath>
```

Start an import task in non-interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import start local <filePath> --project-id <project-id> --cluster-id <cluster-id> --data-format <data-format> --target-database <target-database> --target-table <target-table>
```

Start an impor task with custom CSV format:

{{< copyable "shell-regular" >}}

```
ticloud import start local <filePath> --project-id <project-id> --cluster-id <cluster-id> --data-format CSV --target-database <target-database> --target-table <target-table> --separator \" --delimiter \' --backslash-escape=false --trim-last-separator=true
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
| --delimiter string    | the delimiter used for quoting of CSV file (default "\"")                                      | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --no-color            | Disable color output                                                                           | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string  | Profile to use from your configuration file.                                                   | false    | Work in both modes                                                                                                |
| --separator string    | the field separator of CSV file (default ",")                                                  | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |
| --trim-last-separator | In CSV file whether to treat Separator as the line terminator and trim all trailing separators | false    | Only work in non-interactive mode and "--data-format CSV"                                                         |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.

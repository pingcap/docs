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

| Flag                    | Description                                              | Required | Extra                             |
|-------------------------|----------------------------------------------------------|----------|-----------------------------------|
| --aws-role-arn string   | AWS S3 IAM Role ARN                                      | true     | Only work in non-interactive mode |
| -c, --cluster-id string | Cluster ID                                               | true     | Only work in non-interactive mode |
| --data-format string    | Data format, one of [CSV SqlFile Parquet AuroraSnapshot] | true     | Only work in non-interactive mode |
| -h, --help              | help for s3                                              |          |                                   |
| -p, --project-id string | Project ID                                               | true     | Only work in non-interactive mode |
| --source-url string     | The S3 path where the source data file is stored         | true     | Only work in non-interactive mode |

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
Also, we welcome any contributions.

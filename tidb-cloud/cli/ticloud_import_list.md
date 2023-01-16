# ticloud import list

List data import tasks

{{< copyable "shell-regular" >}}

```shell
ticloud import list [flags]
```

## Examples

List import tasks in interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import list
```

List import tasks in non-interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import list --project-id <project-id> --cluster-id <cluster-id>
```

List the clusters in the project with json format:

{{< copyable "shell-regular" >}}

``` 
ticloud import list --project-id <project-id> --cluster-id <cluster-id> --output json
```

## Flags

| Flag                    | Description                                                                                            | Required | Extra                             |
|-------------------------|--------------------------------------------------------------------------------------------------------|----------|-----------------------------------|
| -c, --cluster-id string | Cluster ID                                                                                             | true     | Only work in non-interactive mode |
| -h, --help              | help for list                                                                                          |          |                                   |
| -o, --output string     | Output format. One of: human, json. For the complete result, please use json format. (default "human") | false    | Work in both modes                |
| -p, --project-id string | Project ID                                                                                             | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.

# ticloud import cancel

Cancel a data import task

{{< copyable "shell-regular" >}}

```shell
ticloud import cancel [flags]
```

## Examples

Cancel an import task in interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import cancel
```

Cancel an import task in non-interactive mode:

{{< copyable "shell-regular" >}}

```shell
ticloud import cancel --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## Flags

| Flag                    | Description                           | Required | Extra                             |
|-------------------------|---------------------------------------|----------|-----------------------------------|
| -c, --cluster-id string | Cluster ID                            | true     | Only work in non-interactive mode |
| --force                 | Delete a profile without confirmation | false    | Work in both modes                |
| -h, --help              | help for cancel                       |          |                                   |
| --import-id string      | The ID of import task                 | true     | Only work in non-interactive mode |
| -p, --project-id string | Project ID                            | true     | Only work in non-interactive mode |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.

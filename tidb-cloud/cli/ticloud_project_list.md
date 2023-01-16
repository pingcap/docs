# ticloud project list

List all accessible projects

{{< copyable "shell-regular" >}}

```shell
ticloud project list [flags]
```

## Examples

List the projects:

{{< copyable "shell-regular" >}}

```shell
ticloud project list
```

List the projects with json format:

{{< copyable "shell-regular" >}}

```shell
ticloud project list -o json
```

## Flags

| Flag                | Description                                                                                            | Required | Extra              |
|---------------------|--------------------------------------------------------------------------------------------------------|----------|--------------------|
| -h, --help          | help for list                                                                                          |          |                    |
| -o, --output string | Output format. One of: human, json. For the complete result, please use json format. (default "human") | false    | Work in both modes |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, Disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose).
Also, we are welcome to any contributions.

---
title: ticloud import list
Summary: The reference of `ticloud import list`.
---

# ticloud import list

List data import tasks

```shell
ticloud import list [flags]
```

Or use alias

```shell
ticloud import ls [flags]
```

## Examples

List import tasks in interactive mode:

```shell
ticloud import list
```

List import tasks in non-interactive mode:

```shell
ticloud import list --project-id <project-id> --cluster-id <cluster-id>
```

List the clusters in the project with json format:

```shell 
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
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

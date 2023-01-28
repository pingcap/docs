---
title: ticloud cluster list
Summary: The reference of `ticloud cluster list`.
---

# ticloud cluster list

List all clusters in a project

```shell
ticloud cluster list <project-id> [flags]
```

Or use alias

```shell
ticloud cluster ls <project-id> [flags]
```

## Examples

List all clusters in the project (interactive mode):

```shell
ticloud cluster list
```

List the clusters in the project (non-interactive mode):

```shell
ticloud cluster list <project-id> 
```

List the clusters in the project with json format:

```shell
ticloud cluster list <project-id> -o json
```

## Flags

| Flag                | Description                                                                                            | Required | Extra                                               |
|---------------------|--------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -h, --help          | help for list                                                                                          |          |                                                     |
| -o, --output string | Output format. One of: human, json. For the complete result, please use json format. (default "human") | false    | Work in both non-interactive and interactive modes. |

<Note> For flags required in non-interactive mode, fill them according to the prompt in interactive mode. </Note>

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

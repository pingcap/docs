---
title: ticloud serverless cluster list
summary: The reference of `ticloud serverless list`.
---

# ticloud serverless list

List all serverless clusters in a project:

```shell
ticloud serverless list [flags]
```

Or use the following alias command:

```shell
ticloud serverless ls [flags]
```

## Examples

List all serverless clusters in interactive mode:

```shell
ticloud serverless list
```

List all serverless clusters in a specified project in non-interactive mode:

```shell
ticloud serverless list -p <project-id>
```

List all clusters in a specified project with the JSON format in non-interactive mode:

```shell
ticloud serverless list -p <project-id> -o json
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                                              | Required | Note                                                 |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -p, --project-id string | The ID of the project, in which the cluster will be created                                                              | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Help information for this command                                                                                        | No       | Works in both non-interactive and interactive modes. |
| -o, --output string     | Output format (`human` by default). Valid values are `human` or `json`. To get a complete result, use the `json` format. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

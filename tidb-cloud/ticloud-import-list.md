---
title: ticloud serverless import list
summary: The reference of `ticloud serverless import list`.
---

# ticloud serverless import list

List data import tasks:

```shell
ticloud serverless import list [flags]
```

Or use the following alias command:

```shell
ticloud serverless import ls [flags]
```

## Examples

List import tasks in interactive mode:

```shell
ticloud serverless import list
```

List import tasks in non-interactive mode:

```shell
ticloud serverless import list --project-id <project-id> --cluster-id <cluster-id>
```

List import tasks for a specified cluster in the JSON format:

```shell
ticloud serverless import list --project-id <project-id> --cluster-id <cluster-id> --output json
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                                              | Required | Note                                                 |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Cluster ID                                                                                                               | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Help information for this command                                                                                        | No       | Works in both non-interactive and interactive modes. |
| -o, --output string     | Output format (`human` by default). Valid values are `human` or `json`. To get a complete result, use the `json` format. | No       | Works in both non-interactive and interactive modes. |
| -p, --project-id string | Project ID                                                                                                               | Yes      | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless cluster list
summary: The reference of `ticloud serverless list`.
---

# ticloud serverless list

List all TiDB Serverless clusters in a project:

```shell
ticloud serverless list [flags]
```

Or use the following alias command:

```shell
ticloud serverless ls [flags]
```

## Examples

List all TiDB Serverless clusters in interactive mode:

```shell
ticloud serverless list
```

List all TiDB Serverless clusters in a specified project in non-interactive mode:

```shell
ticloud serverless list -p <project-id>
```

List all TiDB Serverless clusters in a specified project with the JSON format in non-interactive mode:

```shell
ticloud serverless list -p <project-id> -o json
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                                              | Required | Note                                                 |
|-------------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -p, --project-id string | Specifies the ID of the project.                                                              | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                                                                       | No       | Works in both non-interactive and interactive modes. |
| -o, --output string     | Specifies the output format (`human` by default). Valid values are `human` or `json`. To get a complete result, use the `json` format. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

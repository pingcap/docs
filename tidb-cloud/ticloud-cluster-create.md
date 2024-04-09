---
title: ticloud serverless create
summary: The reference of `ticloud serverless create`.
---

# ticloud serverless create

Create a serverless cluster:

```shell
ticloud serverless create [flags]
```

## Examples

Create a serverless cluster in interactive mode:

```shell
ticloud serverless create
```

Create a serverless cluster in non-interactive mode:

```shell
ticloud serverless create --project-id <project-id> --display-name <display-name> --region <region>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                         | Description                                                                                | Required  | Note                                                |
|------------------------------|--------------------------------------------------------------------------------------------|-----------|-----------------------------------------------------|
| -n --display-name string     | DisplayName of the cluster to be created                                                   | Yes       | Only works in non-interactive mode.                 |
| --spending-limit-monthly int | Maximum monthly spending limit in USD cents                                                | No        | Only works in non-interactive mode.                 |
| -p, --project-id string      | The ID of the project, in which the cluster will be created (default is "default project") | No        | Only works in non-interactive mode.                 |
| -r, --region string          | Cloud region                                                                               | Yes       | Only works in non-interactive mode.                 |
| -h, --help                   | Get help information for this command                                                      | No        | Works in both non-interactive and interactive modes |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

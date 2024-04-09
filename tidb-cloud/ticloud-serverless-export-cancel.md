---
title: ticloud serverless export cancel
summary: The reference of `ticloud serverless export cancel`.
---

# ticloud serverless export describe

Cancel a serverless cluster export

```shell
ticloud serverless export cancel [flags]
```

## Examples

Cancel an export in interactive mode:

```shell
ticloud serverless export cancel
```

Cancel an export in non-interactive mode:

```shell
ticloud serverless export cancel -c <cluster-id> -e <export-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                  | Required | Note                                                 |
|-------------------------|----------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The cluster ID of the export to be described | Yes      | Only works in non-interactive mode.                  |
| -e, --export-id string  | The ID of the export to be described         | Yes      | Only works in non-interactive mode.                  |
| --force                 | Cancel an export without confirmation        | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Help information for this command            | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

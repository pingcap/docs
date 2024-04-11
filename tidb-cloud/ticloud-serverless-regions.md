---
title: ticloud serverless cluster regions
summary: The reference of `ticloud serverless regions`.
---

# ticloud serverless regions

List all available regions for TiDB Serverless clusters:

```shell
ticloud serverless regions [flags]
```

## Examples

List all available regions for TiDB Serverless clusters:

```shell
ticloud serverless regions
```

List all available regions for TiDB Serverless clusters in the JSON format:

```shell
ticloud serverless regions -o json
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                | Description                                                                                                              | Required | Note                                                 |
|---------------------|--------------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -o, --output string | Specifies the output format (`human` by default). Valid values are `human` or `json`. To get a complete result, use the `json` format. | No       | Works in both non-interactive and interactive modes. |
| -h, --help          | Shows help information for this command.                                                                                       | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                         | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

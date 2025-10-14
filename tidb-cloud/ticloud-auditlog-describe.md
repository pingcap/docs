---
title: ticloud serverless audit-log describe
summary: The reference of `ticloud serverless audit-log describe`.
---

# ticloud serverless audit-log describe

Describe the database audit logging configuration for a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log describe [flags]
```

Or use the following alias command:

```shell
ticloud serverless audit-log get [flags]
```

## Examples

Get the database audit logging configuration in interactive mode:

```shell
ticloud serverless audit-log describe
```

Get the database audit logging configuration in non-interactive mode:

```shell
ticloud serverless audit-log describe -c <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                | Required | Note                                                 |
|-------------------------|----------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The cluster ID.            | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
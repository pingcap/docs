---
title: ticloud serverless audit-log filter-rule describe
summary: The reference of `ticloud serverless audit-log filter-rule describe`.
---

# ticloud serverless audit-log filter-rule describe

Describe an audit log filter rule for a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log filter-rule describe [flags]
```

Or use the following alias command:

```shell
ticloud serverless audit-log filter describe [flags]
```

## Examples

Describe an audit log filter rule in interactive mode:

```shell
ticloud serverless audit-log filter describe
```

Describe an audit log filter rule in non-interactive mode:

```shell
ticloud serverless audit-log filter describe --cluster-id <cluster-id> --name <rule-name>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                  | Required | Note                                                 |
|-------------------------|------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.       | Yes      | Only works in non-interactive mode.                  |
| --name string           | The name of the filter rule. | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

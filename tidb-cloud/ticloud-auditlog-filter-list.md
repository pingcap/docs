---
title: ticloud serverless audit-log filter-rule list
summary: The reference of `ticloud serverless audit-log filter-rule list`.
---

# ticloud serverless audit-log filter-rule list

List audit log filter rules for a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log filter-rule list [flags]
```

Or use the following alias command:

```shell
ticloud serverless audit-log filter list [flags]
```

## Examples

List all audit log filter rules in interactive mode:

```shell
ticloud serverless audit-log filter list
```

List all audit log filter rules in non-interactive mode:

```shell
ticloud serverless audit-log filter list -c <cluster-id>
```

List all audit log filter rules with JSON format in non-interactive mode:

```shell
ticloud serverless audit-log filter list -c <cluster-id> -o json
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                       | Required | Note                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster whose audit log filter rules you want to list.                                        | No       | Only works in non-interactive mode.                  |
| -o, --output string     | Specifies the output format (`human` by default). Valid values are `human` or `json`. To get a complete result, use the `json` format. | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Shows help information for this command.                                                          | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless audit-log filter-rule describe
summary: The reference of `ticloud serverless audit-log filter-rule describe`.
---

# ticloud serverless audit-log filter-rule describe

Describe an audit log filter rule for a {{{ .essential }}} cluster.

```shell
ticloud serverless audit-log filter-rule describe [flags]
```

## Examples

Describe an audit log filter rule in interactive mode:

```shell
ticloud serverless audit-log filter-rule describe
```

Describe an audit log filter rule in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule describe --cluster-id <cluster-id> --filter-rule-id <rule-id>
```

## Flags

| Flag                    | Description                  | Required | Note                                                 |
|-------------------------|------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.       | Yes      | Only works in non-interactive mode.                  |
| --filter-rule-id string | The ID of the filter rule.   | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disables color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

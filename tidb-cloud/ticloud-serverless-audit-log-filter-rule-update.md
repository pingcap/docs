---
title: ticloud serverless audit-log filter-rule update
summary: The reference of `ticloud serverless audit-log filter-rule update`.
---

# ticloud serverless audit-log filter-rule update

Update an audit log filter rule for a {{{ .essential }}} cluster.

```shell
ticloud serverless audit-log filter-rule update [flags]
```

## Examples

Update an audit log filter rule in interactive mode:

```shell
ticloud serverless audit-log filter-rule update
```

Enable audit log filter rule in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled
```

Disable audit log filter rule in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --enabled=false
```

Update filters of an audit log filter rule in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule update --cluster-id <cluster-id> --filter-rule-id <rule-id> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY"],"tables":["test.t"]}]}'
```

## Flags

| Flag                    | Description                                                                                                 | Required | Note                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.                                                                                      | Yes      | Only works in non-interactive mode.                  |
| --display-name string   | The display name of the filter rule.                                                                        | No       | Only works in non-interactive mode.                  |
| --enabled               | Enables or disables the filter rule.                                                                          | No       | Only works in non-interactive mode.                  |
| --filter-rule-id string | The ID of the filter rule.                                                                                  | Yes      | Only works in non-interactive mode.                  |
| --rule string           | Complete filter rule expressions. Use "ticloud serverless audit-log filter template" to see filter templates. | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                                                    | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disables color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

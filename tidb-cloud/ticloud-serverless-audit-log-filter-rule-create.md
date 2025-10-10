---
title: ticloud serverless audit-log filter-rule create
summary: The reference of `ticloud serverless audit-log filter-rule create`.
---

# ticloud serverless audit-log filter-rule create

Create an audit log filter rule for a {{{ .essential }}} cluster.

```shell
ticloud serverless audit-log filter-rule create [flags]
```

## Examples

Create a filter rule in interactive mode:

```shell
ticloud serverless audit-log filter-rule create
```

Create a filter rule to capture all audit logs in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{}]}'
```

Create a filter rule to capture `QUERY` and `EXECUTE` events for the `test.t` table, and `QUERY` events for all tables in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule create --cluster-id <cluster-id> --display-name <rule-name> --rule '{"users":["%@%"],"filters":[{"classes":["QUERY","EXECUTE"],"tables":["test.t"]},{"classes":["QUERY"]}]}'
```

## Flags

| Flag                    | Description                                                                                                 | Required | Note                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.                                                                                      | Yes      | Only works in non-interactive mode.                  |
| --display-name string   | The display name of the filter rule.                                                                        | Yes      | Only works in non-interactive mode.                  |
| --rule string           | Filter rule expressions. Use `ticloud serverless audit-log filter-rule template` to see filter templates.        | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                                                    | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enable debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disable color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless audit-log filter-rule list
summary: The reference of `ticloud serverless audit-log filter-rule list`.
---

# ticloud serverless audit-log filter-rule list

List audit log filter rules for a TiDB Cloud Essential cluster.

```shell
ticloud serverless audit-log filter-rule list [flags]
```

## Examples

List all audit log filter rules in interactive mode:

```shell
ticloud serverless audit-log filter-rule list
```

List all audit log filter rules in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id>
```

List all audit log filter rules with JSON format in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule list -c <cluster-id> -o json
```

## Flags

| Flag                    | Description                                                                                       | Required | Note                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.                                                                            | No       | Only works in non-interactive mode.                  |
| -o, --output string     | Specifies the output format. Valid values are `human` (default) or `json`. For the complete result, use the `json` format. | No       | Works in both interactive and non-interactive modes. |
| -h, --help              | Shows help information for this command.                                                          | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enable debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disable color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## SEE ALSO

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

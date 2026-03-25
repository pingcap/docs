---
title: ticloud serverless audit-log filter-rule template
summary: The reference of `ticloud serverless audit-log filter-rule template`.
---

# ticloud serverless audit-log filter-rule template

Show audit log filter rule templates for a {{{ .essential }}} cluster.

```shell
ticloud serverless audit-log filter-rule template [flags]
```

## Examples

Show filter templates in interactive mode:

```shell
ticloud serverless audit-log filter-rule template
```

Show filter templates in non-interactive mode:

```shell
ticloud serverless audit-log filter-rule template --cluster-id <cluster-id>
```

## Flags

| Flag                    | Description                  | Required | Note                                                 |
|-------------------------|------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.       | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disables color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Specifies the profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

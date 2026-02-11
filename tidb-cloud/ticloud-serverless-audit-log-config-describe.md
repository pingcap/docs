---
title: ticloud serverless audit-log config describe
summary: The reference of `ticloud serverless audit-log config describe`.
---

# ticloud serverless audit-log config describe

Describe the database audit logging configuration for a {{{ .essential }}} cluster.

```shell
ticloud serverless audit-log config describe [flags]
```

## Examples

Get the database audit logging configuration in interactive mode:

```shell
ticloud serverless audit-log config describe
```

Get the database audit logging configuration in non-interactive mode:

```shell
ticloud serverless audit-log config describe -c <cluster-id>
```

## Flags

| Flag                    | Description                | Required | Note                                                 |
|-------------------------|----------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The cluster ID.            | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disables color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Specifies the profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless audit-log config
summary: The reference of `ticloud serverless audit-log config`.
---

# ticloud serverless audit-log config

Configure the database audit logging for a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log config [flags]
```

## Examples

Configure the database audit logging in interactive mode:

```shell
ticloud serverless audit-log config
```

Enable the database audit logging in non-interactive mode:

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled
```

Disable the database audit logging in non-interactive mode:

```shell
ticloud serverless audit-log config -c <cluster-id> --enabled=false
```

Unredact the database audit logging in non-interactive mode:

```shell
ticloud serverless audit-log config -c <cluster-id> --unredacted
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                 | Required | Note                                                 |
|-------------------------|-----------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.                                       | Yes      | Only works in non-interactive mode.                  |
| --enabled               | Enable or disable the database audit logging.                              | No       | Only works in non-interactive mode.                  |
| --unredacted            | Enable or disable data redaction in audit logs.                             | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                   | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

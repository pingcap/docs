---
title: ticloud serverless audit-log filter-rule template
summary: The reference of `ticloud serverless audit-log filter-rule template`.
---

# ticloud serverless audit-log filter-rule template

Show audit log filter rule templates for a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log filter-rule template [flags]
```

Or use the following alias command:

```shell
ticloud serverless audit-log filter template [flags]
```

## Examples

Show filter templates in interactive mode:

```shell
ticloud serverless audit-log filter template
```

Show filter templates in non-interactive mode:

```shell
ticloud serverless audit-log filter template --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                  | Required | Note                                                 |
|-------------------------|------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster (optional, for context if templates might become cluster-specific).       | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

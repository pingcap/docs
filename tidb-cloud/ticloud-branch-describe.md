---
title: ticloud serverless branch describe
summary: The reference of `ticloud serverless branch describe`.
---

# ticloud serverless branch describe

Get information about a branch (such as the endpoints, [user name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix), and usages):

```shell
ticloud serverless branch describe [flags]
```

Or use the following alias command:

```shell
ticloud serverless branch get [flags]
```

## Examples

Get branch information of a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless branch describe
```

Get branch information of a TiDB Serverless cluster in non-interactive mode:

```shell
ticloud serverless branch describe --branch-id <branch-id> --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                       | Required | Note                                                 |
|-------------------------|-----------------------------------|----------|------------------------------------------------------|
| -b, --branch-id string  | Specifies the ID of the branch.              | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |
| -c, --cluster-id string | Specifies the ID of the cluster.      | Yes      | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

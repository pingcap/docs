---
title: ticloud serverless branch create
summary: The reference of `ticloud serverless branch create`.
---

# ticloud serverless branch create

Create a [branch](/tidb-cloud/branch-overview.md) for a TiDB Serverless cluster:

```shell
ticloud serverless branch create [flags]
```

## Examples

Create a branch for a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless branch create
```

Create a branch for a TiDB Serverless cluster in non-interactive mode:

```shell
ticloud serverless branch create --cluster-id <cluster-id> --display-name <branch-name>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                      | Description                                                | Required | Note                                                |
|---------------------------|------------------------------------------------------------|----------|-----------------------------------------------------|
| -c, --cluster-id string   | Specifies the ID of the cluster, in which the branch will be created. | Yes      | Only works in non-interactive mode.                 |
| -n, --display-name string | Specifies the name of the branch to be created.               | Yes      | Only works in non-interactive mode.                 |
| -h, --help                | Shows help information for this command.                     | No       | Works in both non-interactive and interactive modes |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

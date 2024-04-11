---
title: ticloud serverless cluster update
summary: The reference of `ticloud serverless update`.
---

# ticloud serverless update

Update a TiDB Serverless cluster:

```shell
ticloud serverless update [flags]
```

## Examples

Update a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless update
```

Update the name of a TiDB Serverless cluster in non-interactive mode:

```shell
ticloud serverless update -c <cluster-id> --display-name <new-display-mame>
```

Update labels of a TiDB Serverless cluster in non-interactive mode

```shell
ticloud serverless update -c <cluster-id> --labels "{\"label1\":\"value1\"}"
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                     | Description                                           | Required | Note                                                 |
|--------------------------|-------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string  | Specifies the ID of the cluster.                   | Yes      | Only works in non-interactive mode.                  |
| -n --display-name string | Specifies a new name for the cluster.      | No       | Only works in non-interactive mode.                  |.
| --annotations string     | Specifies new annotations for the cluster | No       | Only works in non-interactive mode.                  |
| --labels string          | Specifies new labels for the cluster.      | No       | Only works in non-interactive mode.                  |
| -h, --help               | Shows help information for this command.                    | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

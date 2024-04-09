---
title: ticloud serverless cluster update
summary: The reference of `ticloud serverless update`.
---

# ticloud serverless update

Update a serverless cluster:

```shell
ticloud serverless update [flags]
```

## Examples

Update a serverless cluster in interactive mode:

```shell
ticloud serverless update
```

Update displayName of a serverless cluster in non-interactive mode:

```shell
ticloud serverless update -c <cluster-id> --display-name <new-display-mame>
```

Update labels of a serverless cluster in non-interactive mode

```shell
ticloud serverless update -c <cluster-id> --labels "{\"label1\":\"value1\"}"
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                     | Description                                           | Required | Note                                                 |
|--------------------------|-------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string  | The ID of the cluster to be updated                   | Yes      | Only works in non-interactive mode.                  |
| -n --display-name string | The new displayName of the cluster to be updated      | No       | Only works in non-interactive mode.                  |
| --annotations string     | The annotations of the cluster to be added or updated | No       | Only works in non-interactive mode.                  |
| --labels string          | The labels of the cluster to be added or updated      | No       | Only works in non-interactive mode.                  |
| -h, --help               | Help information for this command                     | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

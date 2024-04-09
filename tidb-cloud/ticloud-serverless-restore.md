---
title: ticloud serverless restore
summary: The reference of `ticloud serverless restore`.
---

# ticloud serverless restore

Restore a serverless cluster

```shell
ticloud serverless restore [flags]
```

## Examples

Restore a serverless cluster in interactive mode:

```shell
ticloud serverless restore
```

Restore a serverless cluster with snapshot mode in non-interactive mode:

```
ticloud serverless restore --backup-id <backup-id>
```

Restore a serverless cluster with pointInTime mode in non-interactive mode:

```
ticloud serverless restore -c <cluster-id> --backup-time <backup-time>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                              | Required | Note                                                 |
|-------------------------|------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| --backup-id string      | The ID of the backup, used in snapshot restore mode                                      | NO       | Only works in non-interactive mode.                  |
| --backup-time   string  | The time to restore to (e.g. 2023-12-13T07:00:00Z), used with point-in-time restore mode | NO       | Only works in non-interactive mode.                  |
| -c, --cluster-id string | The ID of cluster, used in point-in-time restore mode.                                   | NO       | Only works in non-interactive mode.                  |
| -h, --help              | Help information for this command                                                        | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                                    | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

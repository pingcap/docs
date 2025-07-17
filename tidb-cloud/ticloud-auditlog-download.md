---
title: ticloud serverless audit-log download
summary: The reference of `ticloud serverless audit-log download`.
---

# ticloud serverless audit-log download

Download the database audit logs from a TiDB Cloud Serverless cluster.

```shell
ticloud serverless audit-log download [flags]
```

## Examples

Download the database audit logs in interactive mode:

```shell
ticloud serverless audit-log download
```

Download the database audit logs in non-interactive mode:

```shell
ticloud serverless audit-log download -c <cluster-id> --start-date <start-date> --end-date <end-date>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                                         | Required | Note                                                 |
|-------------------------|---------------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Cluster ID.                                                                                                         | Yes      | Only works in non-interactive mode.                  |
| --start-date string     | The start date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.              | Yes      | Only works in non-interactive mode.                  |
| --end-date string       | The end date of the audit log you want to download in the format of `YYYY-MM-DD`, for example `2025-01-01`.                | Yes      | Only works in non-interactive mode.                  |
| --output-path string    | The path where you want to download the audit logs. If not specified, logs are downloaded to the current directory. | No       | Only works in non-interactive mode.                  |
| --concurrency int       | Download concurrency (`3` by default).                                                                              | No       | Works in both non-interactive and interactive modes. |
| --force                 | Download without confirmation.                                                                                      | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Shows help information for this command.                                                                            | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

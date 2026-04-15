---
title: ticloud serverless audit-log download
summary: The reference of `ticloud serverless audit-log download`.
---

# ticloud serverless audit-log download

Download the database audit log files from a {{{ .essential }}} cluster.

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

| Flag                    | Description                                                                                   | Required | Note                                                 |
|-------------------------|-----------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster.                                                                        | Yes      | Only works in non-interactive mode.                  |
| --start-date string     | The start date of the audit log you want to download in the format of `YYYY-MM-DD`, for example, `2025-01-01`. | Yes      | Only works in non-interactive mode.                  |
| --end-date string       | The end date of the audit log you want to download in the format of `YYYY-MM-DD`, for example, `2025-01-01`.   | Yes      | Only works in non-interactive mode.                  |
| --output-path string    | The path to download the audit logs. If not specified, logs are downloaded to the current directory.  | No       | Only works in non-interactive mode.                  |
| --concurrency int       | The number of concurrent downloads. The default value is `3`.                                                             | No       | Works in both interactive and non-interactive modes. |
| --force                 | Downloads audit logs without confirmation.                                                                | No       | Works in both interactive and non-interactive modes. |
| -h, --help              | Shows help information for this command.                                                      | No       | Works in both interactive and non-interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both interactive and non-interactive modes.                                                             |
| --no-color           | Disables color output.                                                                                | No       | Only works in non-interactive mode.                                                                              |
| -P, --profile string | Specifies the profile to use from your configuration file.                                                         | No       | Works in both interactive and non-interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

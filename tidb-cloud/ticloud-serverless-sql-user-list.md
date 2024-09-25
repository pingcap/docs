---
title: ticloud serverless sql-user list
summary: The reference of `ticloud serverless sql-user list`.
---

# ticloud serverless sql-user list

List TiDB Cloud Serverless SQL users:

```shell
ticloud serverless sql-user list [flags]
```

## Examples

List TiDB Cloud Serverless SQL users in interactive mode:

```shell
ticloud serverless sql-user list
```

List TiDB Cloud Serverless SQL users in non-interactive mode:

```shell
ticloud serverless sql-user list -c <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                                                 | Required | Note                                                 |
|-------------------------|-------------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.                                                                            | Yes      | Only works in non-interactive mode.                  |
| -o, --output string     | Specifies the output format, one of ["human" "json"]. To get a complete result, use "json" format. (default "human"). | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                                                    | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

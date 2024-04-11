---
title: ticloud serverless cluster shell
summary: The reference of `ticloud serverless shell`.
---

# ticloud serverless shell

Connect to a TiDB Serverless cluster:

```shell
ticloud serverless shell [flags]
```

## Examples

Connect to a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless shell
```

Connect to a TiDB Serverless cluster with the default user in non-interactive mode:

```shell
ticloud serverless shell -c <cluster-id>
```

Connect to a TiDB Serverless cluster with the default user and password in non-interactive mode:

```shell
ticloud serverless shell -c <cluster-id> --password <password>
```

Connect to a TiDB Serverless cluster with a specific user and password in non-interactive mode:

```shell
ticloud connect -c <cluster-id> -u <user-name> --password <password>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                       | Required | Note                                                 |
|-------------------------|-----------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.                        | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |
| --password              | Specifies the password of the user.          | No       | Only works in non-interactive mode.                  |
| -u, --user string       | Specifies the user for login.         | No       | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
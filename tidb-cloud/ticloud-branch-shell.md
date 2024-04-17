---
title: ticloud serverless branch shell
summary: The reference of `ticloud serverless branch shell`.
aliases: ['/tidbcloud/ticloud-connect']
---

# ticloud serverless branch shell

Connect to a branch of a TiDB Serverless cluster:

```shell
ticloud serverless branch shell [flags]
```

## Examples

Connect to a TiDB Serverless branch in interactive mode:

```shell
ticloud serverless branch shell
```

Connect to a TiDB Serverless branch with the default user in non-interactive mode:

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id>
```

Connect to a TiDB Serverless branch with the default user and password in non-interactive mode:

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> --password <password>
```

Connect to a TiDB Serverless branch with a specific user and password in non-interactive mode:

```shell
ticloud serverless branch shell -c <cluster-id> -b <branch-id> -u <user-name> --password <password>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                       | Required | Note                                                 |
|-------------------------|-----------------------------------|----------|------------------------------------------------------|
| -b, --branch-id string  | Specifies the ID of the branch.                         | Yes      | Only works in non-interactive mode.                  |
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
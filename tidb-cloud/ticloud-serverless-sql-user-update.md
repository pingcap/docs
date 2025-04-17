---
title: ticloud serverless sql-user update
summary: The reference of `ticloud serverless sql-user update`.
---

# ticloud serverless sql-user update

Update a TiDB Cloud SQL user:

```shell
ticloud serverless sql-user update [flags]
```

## Examples

Update a TiDB Cloud SQL user in interactive mode:

```shell
ticloud serverless sql-user update
```

Update a TiDB Cloud SQL user in non-interactive mode:

```shell
ticloud serverless sql-user update -c <cluster-id> --user <user-name> --password <password> --role <role>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                                   | Required | Note                                                 |
|-------------------------|-------------------------------------------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.                                              | Yes      | Only works in non-interactive mode.                  |
| --password string       | Specifies the new password of the SQL user.                                             | No       | Only works in non-interactive mode.                  |
| --role strings          | Specifies the new roles of the SQL user. Passing this flag replaces existing roles. | No       | Only works in non-interactive mode.                  |
| --add-role strings      | Specifies the roles to be added to the SQL user.                                      | No       | Only works in non-interactive mode.                  |
| --delete-role strings   | Specifies the roles to be deleted from the SQL user.                                  | No       | Only works in non-interactive mode.                  |
| -u, --user string       | Specifies the name of the SQL user to be updated.                                       | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.                                      | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

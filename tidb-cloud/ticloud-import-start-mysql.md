---
title: ticloud import start mysql
summary: The reference of `ticloud import start mysql`.
---

# ticloud import start mysql

Import one table from a MySQL compatible database to a [TiDB Serverless](/tidb-cloud/select-cluster-tier.md#tidb-serverless-beta) cluster, the target table name is the same as the source table name:

```shell
ticloud import start mysql [flags]
```

> **Note:**
>
> It depends on 'mysql' command-line tool, please make sure you have installed it and add to path.

## Examples

Start an import task in interactive mode:

```shell
ticloud import start mysql
```

Start an import task in non-interactive mode(using the default user '<token>.root'):

```shell
ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password>
```

Start an import task with a specific user:

```shell
ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --target-user <target-user>
```

Start an import task skipping create table:

```shell
ticloud import start mysql --project-id <project-id> --cluster-id <cluster-id> --source-host <source-host> --source-port <source-port> --source-user <source-user> --source-password <source-password> --source-database <source-database> --source-table <source-table> --target-database <target-database> --target-password <target-password> --skip-create-table
```

> **Note:**
>
> Mysql 8.0 uses `utf8mb4_0900_ai_ci` as the default collation, which is not supported by TiDB. You can alter the source table collation, or manually create the target table.

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                     | Description                                   | Required | Note                                                 |
|--------------------------|-----------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string  | Cluster ID                                    | Yes      | Only works in non-interactive mode.                  |
| -h, --help               | Help information for this command             | No       | Works in both non-interactive and interactive modes. |
| -p, --project-id string  | Project ID                                    | Yes      | Only works in non-interactive mode.                  |
| --skip-create-table      | Skip create table                             | No       | Only works in non-interactive mode.                  |
| --source-database string | The database of the source MySQL              | Yes      | Only works in non-interactive mode.                  |
| --source-host string     | The host of the source MySQL                  | Yes      | Only works in non-interactive mode.                  |
| --source-password string | The password of the source MySQL              | Yes      | Only works in non-interactive mode.                  |
| --source-port int        | The port of the source MySQL                  | Yes      | Only works in non-interactive mode.                  |
| --source-table string    | The table of the source MySQL                 | Yes      | Only works in non-interactive mode.                  |
| --source-user string     | The user of the source MySQL                  | Yes      | Only works in non-interactive mode.                  |
| --target-database string | Target database to import data to             | Yes      | Only works in non-interactive mode.                  |
| --target-password string | The password of the target serverless cluster | Yes      | Only works in non-interactive mode.                  |
| --target-table string    | Target table to import data to                | Yes      | Only works in non-interactive mode.                  |
| --target-user string     | The user of the target serverless cluster     | No       | Only works in non-interactive mode.                  |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output                                                                             | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

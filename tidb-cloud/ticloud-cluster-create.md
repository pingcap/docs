---
title: ticloud serverless create
summary: The reference of `ticloud serverless create`.
---

# ticloud serverless create

Create a TiDB Cloud Starter cluster:

```shell
ticloud serverless create [flags]
```

## Examples

Create a TiDB Cloud Starter cluster in interactive mode:

```shell
ticloud serverless create
```

Create a TiDB Cloud Starter cluster in non-interactive mode:

```shell
ticloud serverless create --display-name <display-name> --region <region>
```

Create a TiDB Cloud Starter cluster with a spending limit in non-interactive mode:

```shell
ticloud serverless create --display-name <display-name> --region <region> --spending-limit-monthly <spending-limit-monthly>
``` 

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                         | Description                                                                                                    | Required | Note                                                |
|------------------------------|----------------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -n --display-name string     | Specifies the name of the cluster to be created.                                                               | Yes      | Only works in non-interactive mode.                 |
| --spending-limit-monthly int | Specifies the maximum monthly spending limit in USD cents.                                                     | No       | Only works in non-interactive mode.                 |
| -p, --project-id string      | Specifies the ID of the project, in which the cluster will be created. The default value is `default project`. | No       | Only works in non-interactive mode.                 |
| -r, --region string          | Specifies the name of the cloud region. You can view all available regions using the `ticloud serverless region` command.                | Yes      | Only works in non-interactive mode.                 |
| --disable-public-endpoint    | Disables the public endpoint. Use this option if you want to prevent public access to the cluster.                                                                                 | No       | Only works in non-interactive mode.                 |
| --encryption                 | Enables enhanced encryption at rest.                                                                           | No       | Only works in non-interactive mode.                 |
| --max-rcu int32              | Sets the maximum Request Capacity Units (RCUs) for the cluster, up to 100000.                                                                  | No       | Only works in non-interactive mode.                 |
| --min-rcu int32              | Sets the minimum Request Capacity Units (RCUs) for the cluster, at least 2000.                                                                    | No       | Only works in non-interactive mode.                 |
| -h, --help                   | Shows help information for this command.                                                                       | No       | Works in both non-interactive and interactive modes |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

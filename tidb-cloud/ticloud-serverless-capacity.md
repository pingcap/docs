---
title: ticloud serverless capacity
summary: The reference of `ticloud serverless capacity`.
---

# ticloud serverless capacity

Set the capacity, in terms of maximum and minimum Request Capacity Units (RCUs), for a TiDB Cloud cluster.

```shell
ticloud serverless capacity [flags]
```

## Examples

Set capacity for a TiDB Cloud cluster in interactive mode:

```shell
 ticloud serverless capacity
```

Set capacity for a TiDB Cloud cluster in non-interactive mode:

```shell
ticloud serverless capacity -c <cluster-id> --max-rcu <maximum-rcu> --min-rcu <minimum-rcu>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                  | Required | Note                                                 |
|-------------------------|----------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.             | Yes      | Only works in non-interactive mode.                  |
| --max-rcu int32         | Specifies the maximum Request Capacity Units (RCUs) for the cluster, up to 100000. | No       | Only works in non-interactive mode.                  |
| --min-rcu int32         | Specifies the minimum Request Capacity Units (RCUs) for the cluster, at least 2000.  | No       | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.     | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

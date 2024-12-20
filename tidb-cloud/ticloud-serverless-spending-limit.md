---
title: ticloud serverless spending-limit
summary: The reference of `ticloud serverless spending-limit`.
---

# ticloud serverless spending-limit

Set the maximum monthly [spending limit](/tidb-cloud/manage-serverless-spend-limit.md) for a TiDB Cloud Serverless cluster:

```shell
ticloud serverless spending-limit [flags]
```

## Examples

Set the spending limit for a TiDB Cloud Serverless cluster in interactive mode:

```shell
ticloud serverless spending-limit
```

Set the spending limit for a TiDB Cloud Serverless cluster in non-interactive mode:

```shell
ticloud serverless spending-limit -c <cluster-id> --monthly <spending-limit-monthly>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                 | Required | Note                                                 |
|-------------------------|---------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.                       | Yes      | Only works in non-interactive mode.                  |
| --monthly int32         | Specifies the maximum monthly spending limit in USD cents. | Yes      | Only works in non-interactive mode.                  |
| -h, --help              | Shows help information for this command.          | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                          | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

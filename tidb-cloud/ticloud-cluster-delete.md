---
title: ticloud serverless cluster delete
summary: The reference of `ticloud serverless delete`.
---

# ticloud serverless delete

Delete a TiDB Serverless cluster from your project:

```shell
ticloud serverless delete [flags]
```

Or use the following alias command:

```shell
ticloud serverless rm [flags]
```

## Examples

Delete a TiDB Serverless cluster in interactive mode:

```shell
ticloud serverless delete
```

Delete a TiDB Serverless cluster in non-interactive mode:

```shell
ticloud serverless delete --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                            | Required | Note                                                 |
|-------------------------|----------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster to be deleted.    | Yes      | Only works in non-interactive mode.                  |
| --force                 | Deletes a cluster without confirmation. | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Shows help information for this command.     | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                          | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless cluster spending-limit
summary: The reference of `ticloud serverless spending-limit`.
---

# ticloud serverless spending-limit

Set spending limit for a serverless cluster

```shell
ticloud serverless spending-limit [flags]
```

## Examples

Set spending limit for a serverless clusters in interactive mode:

```shell
ticloud serverless spending-limit
```

Set spending limit for a serverless clusters in non-interactive mode:

```shell
ticloud serverless spending-limit -c <cluster-id> --monthly <spending-limit-monthly>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                 | Required | Note                                                 |
|-------------------------|---------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | The ID of the cluster                       | Yes      | Only works in non-interactive mode.                  |
| --monthly int32         | Maximum monthly spending limit in USD cents | Yes      | Only works in non-interactive mode.                  |
| --force                 | Deletes a cluster without confirmation      | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Help information for this command           | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                          | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

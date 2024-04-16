---
title: ticloud ai
summary: The reference of `ticloud ai`.
---

# ticloud ai

Chat with TiDB Bot:

```shell
ticloud ai [flags]
```

## Examples

Chat with TiDB Bot in interactive mode:

```shell
ticloud serverless delete
```

Chat with TiDB Bot in non-interactive mode:

```shell
ticloud ai -q "How to create a cluster?"
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag               | Description                       | Required | Note                                                 |
|--------------------|-----------------------------------|----------|------------------------------------------------------|
| -q, --query string | Specifies your query to TiDB Bot.   | Yes      | Only works in non-interactive mode.                  |
| -h, --help         | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                         | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

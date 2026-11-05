---
title: ticloud help
summary: The reference of `ticloud help`.
---

# ticloud help

Get help information for any command in TiDB Cloud CLI:

```shell
ticloud help [command] [flags]
```

## Examples

To get help for the `auth` command:

```shell
ticloud help auth
```

To get help for the `serverless create` command:

```shell
ticloud help serverless create
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                                                   | Required | Note                                                 |
|-------------------------|---------------------------------------------------------------|----------|------------------------------------------------------|
| -h, --help              | Shows help information for this command.                      | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |
| -D, --debug          | Enables debug mode.                                                                                   | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.
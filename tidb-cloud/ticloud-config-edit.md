---
title: ticloud config edit
Summary: The reference of `ticloud config edit`.
---

# ticloud config edit

Open the config file with the default text editor in Unix system. If using with Windows, the path of config file will be printed instead.

```shell
ticloud config edit [flags]
```

## Examples

To open the config

```shell
ticloud config edit
```

## Flags

| Flag       | Description              |
|------------|--------------------------|
 | -h, --help | Get the help information |

## Inherited flags

| Flag                 | Description                                                                               | Required | Notes                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                                                                  | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active [user profile](tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

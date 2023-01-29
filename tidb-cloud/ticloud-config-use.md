---
title: ticloud config use
Summary: The reference of `ticloud config use`.
---

# ticloud config use

Use the specified profile as the active [user profile](tidb-cloud/cli-reference.md#user-profile)

```shell
ticloud config use <profile-name> [flags]
```

## Examples

Use the "test" profile as the active user profile:

```shell
ticloud config use test
```

## Flags

| Flag       | Description              |
|------------|--------------------------|
| -h, --help | Get the help information |

## Inherited flags

| Flag                 | Description                                   | Required | Notes                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                      | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active user profile used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

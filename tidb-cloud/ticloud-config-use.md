---
title: ticloud config use
Summary: The reference of `ticloud config use`.
---

# ticloud config use

Use the specified profile as the active profile

```shell
ticloud config use <profile-name> [flags]
```

## Examples

Use the "test" profile as the active profile:

```shell
ticloud config use test
```

## Flags

| Flag       | Description  |
|------------|--------------|
| -h, --help | help for use |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

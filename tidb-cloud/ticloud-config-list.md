---
title: ticloud config list
Summary: The reference of `ticloud config list`.
---

# ticloud config list

List all profiles

```shell
ticloud config list [flags]
```

Or use alias

```shell
ticloud config ls [flags]
```

## Examples

List all available profiles:

```shell
ticloud config list
```

## Flags

| Flag       | Description   |
|------------|---------------|
| -h, --help | help for list |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

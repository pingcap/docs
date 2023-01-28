---
title: ticloud config edit
Summary: The reference of `ticloud config edit`.
---

# ticloud config edit

Open the config file with the default text editor

```shell
ticloud config edit [flags]
```

## Examples

To open the config

```shell
ticloud config edit
```

## Flags

| Flag       | Description   |
|------------|---------------|
 | -h, --help | help for edit |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

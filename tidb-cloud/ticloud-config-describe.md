---
title: ticloud config describe
Summary: The reference of `ticloud config describe`.
---

# ticloud config describe

You can use the `ticloud config describe` to get the private and public keys for a specific profile:

```shell
ticloud config describe <profile-name> [flags]
```

Or use the following alias command:

```shell
ticloud config get <profile-name> [flags]
```

## Examples

Describe the profile configuration:

```shell
ticloud config describe <profile-name>
```

## Flags

| Flag       | Description       |
|------------|-------------------|
| -h, --help | help for describe |

## Inherited flags

| Flag                 | Description                                  | Required | Extra                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

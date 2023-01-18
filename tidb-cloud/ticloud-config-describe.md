---
title: ticloud config describe
Summary: The reference of `ticloud config describe`.
---

# ticloud config describe

Describe a specific profile

```shell
ticloud config describe <profile-name> [flags]
```

Or use alias

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

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

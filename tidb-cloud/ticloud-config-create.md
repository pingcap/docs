---
title: ticloud config create
Summary: The reference of `ticloud config create`.
---

# ticloud config create

Configure a [user profile](tidb-cloud/cli-reference.md#user-profile) to store settings

```shell
ticloud config create [flags]
```

## Examples

To configure a new user profile in interactive mode:

```shell
ticloud config create
```

To configure a new user profile in non-interactive mode:

```shell
ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                  | Description                                   | Required | Notes                             |
|-----------------------|-----------------------------------------------|----------|-----------------------------------|
| -h, --help            | Get the help information                      | No       |                                   |
| --private-key string  | The private key of the TiDB Cloud API         | Yes      | Only work in non-interactive mode |
| --profile-name string | The name of the profile, must not contain '.' | Yes      | Only work in non-interactive mode |
| --public-key string   | The public key of the TiDB Cloud API          | Yes      | Only work in non-interactive mode |

## Inherited flags

| Flag                 | Description                                  | Required | Notes                                                                                                                    |
|----------------------|----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                     | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active user profile used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud auth login
summary: The reference of `ticloud auth login`.
---

# ticloud auth login

Authenticate with the TiDB Cloud:

```shell
ticloud auth login [flags]
```

## Examples

To start the login for your account:

```shell
ticloud auht login
```

Login with insecure storage:

```shell
ticloud auht login --insecure-storage
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag               | Description                                                               | Required | Note                                                 |
|--------------------|---------------------------------------------------------------------------|----------|------------------------------------------------------|
| --insecure-storage | Save authentication credentials in plain text instead of credential store | No       | Works in both non-interactive and interactive modes. |
| -h, --help         | Help information for this command                                         | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                | Required | Note                                                                                                             |
|----------------------|--------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                                                          | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

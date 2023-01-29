---
title: ticloud project list
Summary: The reference of `ticloud project list`.
---

# ticloud project list

List all accessible projects

```shell
ticloud project list [flags]
```

Or use the following alias command

```shell
ticloud project ls [flags]
```

## Examples

List the projects:

```shell
ticloud project list
```

List the projects with json format:

```shell
ticloud project list -o json
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                | Description                                                                                            | Required | Notes                                               |
|---------------------|--------------------------------------------------------------------------------------------------------|----------|-----------------------------------------------------|
| -h, --help          | Get the help information                                                                               | No       |                                                     |
| -o, --output string | Output format. One of: human, json. For the complete result, please use json format. (default "human") | No       | Work in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                               | Required | Notes                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                                                                  | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active [user profile](tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud import cancel
Summary: The reference of `ticloud import cancel`.
---

# ticloud import cancel

Cancel a data import task:

```shell
ticloud import cancel [flags]
```

## Examples

Cancel an import task in interactive mode:

```shell
ticloud import cancel
```

Cancel an import task in non-interactive mode:

```shell
ticloud import cancel --project-id <project-id> --cluster-id <cluster-id> --import-id <import-id>
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                    | Description                           | Required | Note                                               |
|-------------------------|---------------------------------------|----------|-----------------------------------------------------|
| -c, --cluster-id string | Cluster ID                            | Yes      | Only works in non-interactive mode.                   |
| --force                 | Deletes a profile without confirmation | No       | Works in both non-interactive and interactive modes. |
| -h, --help              | Gets the help information for this command             | No       | Works in both non-interactive and interactive modes. |
| --import-id string      | The ID of the import task                 | Yes      | Only works in non-interactive mode.                   |
| -p, --project-id string | Project ID                            | Yes      | Only works in non-interactive mode.                   |

## Inherited flags

| Flag                 | Description                                                                               | Required | Note                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                  | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

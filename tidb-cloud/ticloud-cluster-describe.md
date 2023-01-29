---
title: ticloud cluster describe
Summary: The reference of `ticloud cluster describe`.
---

# ticloud cluster describe

You can use `ticloud cluster describe` to get information about a cluster, such as the cloud provider, cluster type, cluster configurations, and cluster status.

```shell
ticloud cluster describe [flags]
```

Or use the following alias command

```shell
ticloud cluster get [flags]
```

## Examples

Get the cluster info in interactive mode:

```shell
ticloud cluster describe
```

Get the cluster info in non-interactive mode:

```shell
ticloud cluster describe --project-id <project-id> --cluster-id <cluster-id>
```

## Flags

In non-interactive mode, you need to manually enter required flags. In interactive mode, you can just follow CLI prompts to fill in them.

| Flag                    | Description                   | Required | Notes                             |
|-------------------------|-------------------------------|----------|-----------------------------------|
| -c, --cluster-id string | The ID of the cluster         | Yes      | Only work in non-interactive mode |
| -h, --help              | Get the help information      | No       |                                   |
| -p, --project-id string | The project ID of the cluster | Yes      | Only work in non-interactive mode |

## Inherited flags

| Flag                 | Description                                                                               | Required | Notes                                                                                                                    |
|----------------------|-------------------------------------------------------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                                                                  | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active [user profile](tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

---
title: ticloud serverless authorized-network update
summary: The reference of `ticloud serverless authorized-network update`.
---

# ticloud serverless authorized-network update

Update an authorized network:

```shell
ticloud serverless authorized-network update [flags]
```

## Examples

Update an authorized network in interactive mode:

```shell
ticloud serverless authorized-network update
```

Update an authorized network in non-interactive mode:

```shell
ticloud serverless authorized-network update -c <cluster-id> --start-ip-address <start-ip-address> --end-ip-address <end-ip-address> --new-start-ip-address <new-start-ip-address> --new-end-ip-address <new-end-ip-address>
```

## Flags

In non-interactive mode, you need to manually enter the required flags. In interactive mode, you can just follow CLI prompts to fill them in.

| Flag                    | Description                              | Required | Note                                                 |
|-------------------------|------------------------------------------|----------|------------------------------------------------------|
| -c, --cluster-id string | Specifies the ID of the cluster.         | Yes      | Only works in non-interactive mode.                  |
| --start-ip-address string          | Specifies the starting IP address of the authorized network.             | Yes       | Only works in non-interactive mode.                  |
| --end-ip-address string          | Specifies the ending IP address of the authorized network.             | Yes       | Only works in non-interactive mode.   |
| --new-display-name string       | Specifies the new name of the authorized network.            | No       | Only works in non-interactive mode.                  |
| --new-start-ip-address string          | Specifies the new start IP address of the authorized network.             | No       | Only works in non-interactive mode.                  |
| --new-end-ip-address string          | Specifies the new end IP address of the authorized network.             | No       | Only works in non-interactive mode.   |
| -h, --help              | Shows help information for this command. | No       | Works in both non-interactive and interactive modes. |

## Inherited flags

| Flag                 | Description                                                                                          | Required | Note                                                                                                             |
|----------------------|------------------------------------------------------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                                                                            | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active [user profile](/tidb-cloud/cli-reference.md#user-profile) used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enables debug mode.                                                                                  | No       | Works in both non-interactive and interactive modes.                                                             |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

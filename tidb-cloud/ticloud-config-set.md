---
title: ticloud config set
Summary: The reference of `ticloud config set`.
---

# ticloud config set

Configure specific properties of the active [user profile](tidb-cloud/cli-reference.md#user-profile)

## Synopsis

Configure specific properties of the active user profile. Available properties : [public-key private-key api-url].

| Properties  | Description                                                        | Required |
|-------------|--------------------------------------------------------------------|----------|
| public-key  | The public key of the TiDB Cloud API                               | Yes      |
| private-key | The private key of the TiDB Cloud API                              | Yes      |
| api-url     | The base url of TiDB Cloud, default is `https://api.tidbcloud.com` | No       | 

If using -P flag, the config in the specific profile will be set. If not, the config in the active profile will be set

```shell
ticloud config set <property-name> <value> [flags]
```

## Examples

Set the value of the public-key in active profile:

```shell
ticloud config set public-key <public-key>
```

Set the value of the public-key in the specific profile "test":

```shell
ticloud config set public-key <public-key> -P test
```

Set the API host:

```shell
ticloud config set api-url https://api.tidbcloud.com
```

> **Note:**
> 
> Usually you don't need to set up the TiDB Cloud API url, the default value is `https://api.tidbcloud.com`.

## Flags

| Flag       | Description              |
|------------|--------------------------|
| -h, --help | Get the help information |

## Inherited flags

| Flag                 | Description                                   | Required | Notes                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                      | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active user profile used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

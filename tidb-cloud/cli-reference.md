---
title: TiDB Cloud CLI Reference
summary: Provides an overview of TiDB Cloud CLI.
---

# TiDB Cloud CLI Reference <span style="color: #fff; background-color: #00bfff; border-radius: 4px; font-size: 0.5em; vertical-align: middle; margin-left: 16px; padding: 0 2px;">Beta</span>

> **Note:**
>
> TiDB Cloud CLI is in beta.

TiDB Cloud CLI is a command line interface, which allows you to operate TiDB Cloud from your terminal with a few lines of commands. In the TiDB Cloud CLI, you can easily manage your TiDB Cloud clusters, import data to your clusters, and perform more operations.

## Before you begin

Make sure to first [set up your TiDB Cloud CLI environment](/tidb-cloud/get-started-with-cli.md). Once you have installed the `ticloud` CLI, you can use it to manage your TiDB Cloud clusters from the command lines.

## Commands available

The following table lists the commands available for the TiDB Cloud CLI.

To use the `ticloud` CLI in your terminal, run `ticloud [command] [subcommand]`. If you are using [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview), use `tiup cloud [command] [subcommand]` instead.

| Command           | Subcommand                                                               | Description                                                                                             |
|-------------------|--------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| auth              | login, logout                                                            | Login and logout                                                                                        |
| serverless (alias: s)     | create, delete, describe, list, update, spending-limit, regions, shell   | Manage TiDB Serverless clusters                                                                         |
| serverless branch | create, delete, describe, list, shell                                    | Manage TiDB Serverless branches                                                                         |
| serverless import | cancel, describe, list, start                                            | Manage TiDB Serverless import tasks |
| serverless export | create, describe, list, cancel, download                                 | Manage TiDB Serverless export tasks                                                                      |
| ai                | -                                                                        | Chat with TiDB Bot                                                                                      |
| completion        | bash, fish, powershell, zsh                                              | Generate completion script for specified shell                                                          |
| config            | create, delete, describe, edit, list, set, use                           | Configure user profiles                                                                                 |
| project           | list                                                                     | Manage projects                                                                                         |
| update            | -                                                                        | Update the CLI to the latest version                                                                    |
| help              | cluster, completion, config, help, import, project, update               | View help for any command                                                                               |

## Command modes

The TiDB Cloud CLI provides two modes for some commands for easy use:

- Interactive mode

    You can run a command without flags (such as `ticloud config create`), and the CLI prompts you for input.

- Non-interactive mode

    You must provide all arguments and flags that are required when running a command, such as `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`.

## User profile

For the TiDB Cloud CLI, a user profile is a collection of properties associated with a user, including the profile name, public key, private key, and OAuth token. To use TiDB Cloud CLI, you must have a user profile.

### Create a user profile with TiDB Cloud API key

Use [`ticloud config create`](/tidb-cloud/ticloud-config-create.md) to create a user profile.

### Create a user profile with OAuth token

Use [`ticloud auth login`](/tidb-cloud/ticloud-auth-login.md) to assign OAuth token to the current profile. If no profiles exist, a profile named `default` will be created automatically.

### List all user profiles

Use [`ticloud config list`](/tidb-cloud/ticloud-config-list.md) to list all user profiles.

An example output is as follows:

```
Profile Name
default (active)
dev
staging
```

In this example output, the user profile `default` is currently active.

### Describe a user profile

Use [`ticloud config describe`](/tidb-cloud/ticloud-config-describe.md) to get the properties of a user profile.

An example output is as follows:

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### Set properties in a user profile

Use [`ticloud config set`](/tidb-cloud/ticloud-config-set.md) to set properties in a user profile.

### Switch to another user profile

Use [`ticloud config use`](/tidb-cloud/ticloud-config-use.md) to switch to another user profile.

An example output is as follows:

```
Current profile has been changed to default
```

### Edit the config file

Use [`ticloud config edit`](/tidb-cloud/ticloud-config-edit.md) to open the configuration file for editing.

### Delete a user profile

Use [`ticloud config delete`](/tidb-cloud/ticloud-config-delete.md) to delete a user profile.

## Global flags

The following table lists the global flags for the TiDB Cloud CLI.

| Flag                 | Description                                             | Required | Note                                                                                                             |
|----------------------|---------------------------------------------------------|----------|------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disables color in output.                               | No       | Only works in non-interactive mode. In interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Specifies the active user profile used in this command. | No       | Works in both non-interactive and interactive modes.                                                             |
| -D, --debug          | Enable debug mode                                       | No       | Works in both non-interactive and interactive modes.                                                          |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

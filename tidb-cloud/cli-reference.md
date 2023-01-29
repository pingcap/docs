---
title: TiDB Cloud CLI Reference
Summary: Provides an overview of TiDB Cloud CLI.
---

# TiDB Cloud CLI Reference

TiDB Cloud CLI is a command line interface, which allows you to operate TiDB Cloud from your terminal with a few lines of commands. In TiDB Cloud CLI, you can easily manage your TiDB Cloud clusters, import data to your clusters, and perform more operations. 

## Before you begin

Make sure to first [set up your TiDB Cloud CLI environment](/tidb-cloud/get-started-with-cli.md). Once you installed the `ticloud` CLI, you can use it to manage your TiDB Cloud clusters from the command lines.

## Available commands

The following table lists the available commands for the TiDB Cloud CLI. 
To start up the `ticloud` CLI in your terminal, you can use `ticloud [command] [subcommand]`. For users using [TiUP](https://docs.pingcap.com/tidb/stable/tiup-overview), use `tiup cloud [command] [subcommand]` instead.

| Command    | Subcommands                                                | Description                                                                                              |
|------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| cluster    | create, delete, describe, list                             | Manage clusters                                                                                          | 
| completion | bash, fish, powershell, zsh                                | Generate completion script for specified shell                                                           | 
| config     | create, delete, describe, edit, list, set, use             | Configure settings in a user profile.                                                                    | 
| help       | cluster, completion, config, help, import, project, update | View help for any command                                                                                | 
| import     | cancel, describe, list, start                              | Manage [import](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) tasks |
| project    | list                                                       | Manage projects                                                                                          | 
| update     |                                                            | Update the CLI to the latest version                                                                     | 

## Command modes

The TiDB Cloud CLI provides two modes for some commands for easy use: interactive mode and non-interactive mode.

- In the interactive mode, the CLI prompts you for input when you run a command, such as `ticloud config create`.
- In the non-interactive mode, you must provide all the required arguments and flags when running a command, such as `ticloud config create --profile-name <profile-name> --public-key <public-key> --private-key <private-key>`

## User profile

A user profile is a collection of properties associated with a user. In order to execute commands, you must configure one user profile first.

### Create a user profile 

Use [`ticloud config create`](tidb-cloud/ticloud-config-create.md) to create a new user profile.

### List all user profiles

Use [`ticloud config list`](tidb-cloud/ticloud-config-list.md) to list all user profiles. The output is as follows:

```
Profile Name
default (active)
dev     
staging
```

The user profile `defalut` is currently active.

### Describe one user profile

If you want to get the properties in one user profile, use [`ticloud config describe`](tidb-cloud/ticloud-config-describe.md)

```json
{
  "private-key": "xxxxxxx-xxx-xxxxx-xxx-xxxxx",
  "public-key": "Uxxxxxxx"
}
```

### Set properties in user profile

Use [`ticloud config set`](tidb-cloud/ticloud-config-set.md) to set properties in the user profile.

### Switch to another user profile

Use [`ticloud config use`](tidb-cloud/ticloud-config-use.md) to switch to another user profile. The output is as follows:

```
Current profile has been changed to default
```

### Open config file with editor

Use [`ticloud config use`](tidb-cloud/ticloud-config-edit.md) to open config file with editor. 

### Delete one user profile

Use [`ticloud config delete`](tidb-cloud/ticloud-config-delete.md) to delete the user profile.

## Global flags

The following table lists the global flags for the TiDB Cloud CLI. 

| Flag                 | Description                                   | Required | Extra                                                                                                                    |
|----------------------|-----------------------------------------------|----------|--------------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                      | No       | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | The active user profile used in this command. | No       | Work in both non-interactive and interactive modes.                                                                      |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

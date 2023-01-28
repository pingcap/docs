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

## Global flags

The following table lists the global flags for the TiDB Cloud CLI. 

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color in output.                         | false    | Only works in the non-interactive mode. In the interactive mode, disabling color might not work with some UI components. |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both non-interactive and interactive modes.                                                                                                |

## Feedback

If you have any questions or suggestions on the TiDB Cloud CLI, feel free to create an [issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

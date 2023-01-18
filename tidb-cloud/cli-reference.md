---
title: TiDB Cloud CLI Reference
Summary: The reference of the TiDB Cloud CLI.
---

# TiDB Cloud CLI Reference

Use the TiDB Cloud CLI to manage your TiDB Cloud clusters, import data to your clusters, and more from your terminal.

## Getting Started

Make sure to first [set up your TiDB Cloud CLI environment](/tidb-cloud/get-started-with-cli.md). Once you installed the `ticloud` CLI, you can use it to manage your TiDB Cloud clusters from the command line.

## Available Commands

Use `ticloud [command] [subcommand]` to start up the `ticloud` CLI in your terminal. For users using TiUP, use `tiup cloud [command] [subcommand]` instead.

| Command    | Subcommands                                                | Description                                                                                              |
|------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| cluster    | create, delete, describe, list                             | Manage clusters                                                                                          | 
| completion | bash, fish, powershell, zsh                                | Generate completion script for specified shell                                                           | 
| config     | create, delete, describe, edit, list, set, use             | Configure settings in a user profile.                                                                    | 
| help       | cluster, completion, config, help, import, project, update | View help for any command                                                                                | 
| import     | cancel, describe, list, start                              | Manage [import](/tidb-cloud/tidb-cloud-migration-overview.md#import-data-from-files-to-tidb-cloud) tasks |
| project    | list                                                       | Manage projects                                                                                          | 
| update     |                                                            | Update the CLI to the latest version                                                                     | 

## Global Flags

| Flag                 | Description                                  | Required | Extra                                                                                                             |
|----------------------|----------------------------------------------|----------|-------------------------------------------------------------------------------------------------------------------|
| --no-color           | Disable color output                         | false    | Only work in non-interactive mode. In interactive mode, disable color output may not work with some UI components |
| -P, --profile string | Profile to use from your configuration file. | false    | Work in both modes                                                                                                |

## Feedback

If you have any questions or suggestions, please [file an issue](https://github.com/tidbcloud/tidbcloud-cli/issues/new/choose). Also, we welcome any contributions.

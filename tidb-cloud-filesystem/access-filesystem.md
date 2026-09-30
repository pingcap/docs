---
title: Access an Existing File System
summary: Learn how to access an existing file system from your current machine, another machine, CI job, or agent environment.
---

# Access an Existing File System

In TiDB Cloud Filesystem, you can access an existing file system using either a locally stored token or a token provided for another machine or environment:

- If you created the file system or imported its token on the current machine, TiDB Cloud CLI (`ti`) can use the stored token.
- If you are working from another machine, CI job, or agent environment, provide a file system token and region for that environment.

## Prerequisites

Before you begin, [install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) and make sure you have access to the file system. For information about owner and scoped tokens and their permissions, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Continue using a file system on the same machine

If you created the file system by using `ti` on the current machine, or previously imported its token, the CLI already has a token stored locally.

The environment variables `TI_FS_TOKEN` and `TI_REGION_CODE` override the locally stored token and region.

Clear these overrides, then select the file system whose token is stored locally:

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<file-system-id>"
```

</div>

</SimpleTab>

List the file system root. If the stored token is scoped to a directory, replace `/` with that directory's path:

```shell
ti fs list-files --path /
```

Setting `TI_FS_FILE_SYSTEM_ID` selects the file system for subsequent commands in the current shell. It does not change or revoke any file system tokens.

Alternatively, you can select the file system for an individual command:

```shell
ti fs list-files --file-system-id "<file-system-id>" --path /
```

## Access a file system from another environment

In another environment, provide the token and region. For CI or agents, inject `TI_FS_TOKEN` from a secret manager and set `TI_REGION_CODE` in each process. Skip the input prompts and clear `TI_FS_FILE_SYSTEM_ID` to remove any previous file system selection.

In an interactive terminal, enter the token at the prompt; input is hidden:

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_FILE_SYSTEM_ID
export TI_REGION_CODE="<filesystem-region-code>"
printf 'File system token: '
read -rs TI_FS_TOKEN && export TI_FS_TOKEN && printf '\n'
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_FILE_SYSTEM_ID -ErrorAction SilentlyContinue
$env:TI_REGION_CODE = "<filesystem-region-code>"
$env:TI_FS_TOKEN = [System.Net.NetworkCredential]::new(
  "", (Read-Host "File system token" -AsSecureString)
).Password
```

</div>

</SimpleTab>

The token identifies the file system. You do not need a separate file system ID, a configured CLI profile, or TiDB Cloud API keys for file access.

You can then run commands that the token permits. For example:

```shell
ti fs list-files --path "<allowed-path>"
```

A scoped token can access only the paths and operations included in its scope. If another user or administrator gave you the token, check which paths and operations you are allowed to use.

If you need to create a token for another environment, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

## Switch between file systems

To switch between locally stored tokens, clear the token and region overrides and change the file system ID:

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

```shell
unset TI_FS_TOKEN TI_REGION_CODE
export TI_FS_FILE_SYSTEM_ID="<another-file-system-id>"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

```powershell
Remove-Item Env:TI_FS_TOKEN -ErrorAction SilentlyContinue
Remove-Item Env:TI_REGION_CODE -ErrorAction SilentlyContinue
$env:TI_FS_FILE_SYSTEM_ID = "<another-file-system-id>"
```

</div>

</SimpleTab>

The CLI uses the token and region stored for the selected file system. `TI_FS_TOKEN` and `TI_REGION_CODE` override those values; leaving either set for another file system or region causes a mismatch.

A file system can have multiple remote tokens, while each CLI profile stores at most one selected local token for each file system. Changing which file system or local token the CLI uses does not disable or revoke other remote tokens.

## Credential selection

In most workflows, use one of the approaches above rather than specifying credentials on every command.

If multiple token sources are available, `ti` selects the token in the following order:

1. `--fs-token`
2. `TI_FS_TOKEN`
3. The locally stored token for the selected file system

For the complete file system and credential selection rules, see [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md#file-system-credentials-and-remote-inventory).

## What's next

- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)
- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)

---
title: Access an Existing TiDB Cloud Filesystem
summary: Learn how to access an existing TiDB Cloud Filesystem from your current machine, another machine, CI job, or agent environment.
---

# Access an Existing TiDB Cloud Filesystem

If a TiDB Cloud Filesystem already exists, you can access it from your current machine or another environment.

How you connect depends on where you are working:

- If you created or imported a Filesystem on the current machine, TiDB Cloud CLI (`ti`) can use the token already stored locally.
- If you are working from another machine, CI job, or agent environment, provide a Filesystem token and region for that environment.

## Prerequisites

Before you begin, [install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli) and make sure you have access to the Filesystem. For information about owner and scoped tokens and their permissions, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Continue using a Filesystem on the same machine

If you created the Filesystem by using `ti` on the current machine, or previously imported its token, the CLI already has a token stored locally.

Select the Filesystem for the current shell:

```shell
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

You can then run Filesystem commands without providing the Filesystem ID or token each time:

```shell
ti fs list-files --path /
```

Setting `TI_FS_FILE_SYSTEM_ID` selects the Filesystem for subsequent commands in the current shell. It does not change or revoke any Filesystem tokens.

Alternatively, you can select the Filesystem for an individual command:

```shell
ti fs list-files \
  --file-system-id "<file-system-id>" \
  --path /
```

## Access a Filesystem from another environment

If you are accessing the Filesystem from another machine, CI job, agent sandbox, or other environment without its locally stored credential, provide a Filesystem token and the Filesystem region:

```shell
export TI_FS_TOKEN="<filesystem-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

The token identifies its Filesystem, so you do not need to provide the Filesystem ID separately.

You can then run commands that the token permits. For example:

```shell
ti fs list-files --path "<allowed-path>"
```

A scoped token can access only the paths and operations included in its scope. If another user or administrator gave you the token, check which paths and operations you are allowed to use.

Treat Filesystem tokens as secrets. For CI jobs and agent environments, inject the token from a secret manager instead of storing it in source code, scripts, or container images.

If you need to create a token for another environment, see [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

## Switch between Filesystems

If you have access to multiple Filesystems with locally stored tokens, change `TI_FS_FILE_SYSTEM_ID` to select the Filesystem you want to use in the current shell:

```shell
export TI_FS_FILE_SYSTEM_ID="<another-file-system-id>"
```

The CLI uses the locally stored token for the selected Filesystem.

A Filesystem can have multiple remote tokens, while each CLI profile stores at most one selected local token for each Filesystem. Changing which Filesystem or local token the CLI uses does not disable or revoke other remote tokens.

## Credential selection

In most workflows, use one of the approaches above rather than specifying credentials on every command.

If multiple token sources are available, `ti` selects the token in the following order:

1. `--fs-token`
2. `TI_FS_TOKEN`
3. The locally stored token for the selected Filesystem

For the complete Filesystem and credential selection rules, see [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md#filesystem-credentials-and-remote-inventory).

## What's next

- [Work with Files and Directories](/tidb-cloud-filesystem/work-with-filesystem-data.md)
- [Mount TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-mount.md)
- [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)

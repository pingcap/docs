---
title: TiDB Cloud Filesystem Authorization
summary: Choose TiDB Cloud API keys, owner tokens, or scoped tokens to separate Filesystem administration from application data access.
---

# TiDB Cloud Filesystem Authorization

The person who creates a Filesystem and the agent that uses its files do not need the same credentials. Keep account-level management on a trusted machine and give each application only the Filesystem access it needs.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Choose the credential type

| Credential | Use it for | Scope | Who should hold it |
| --- | --- | --- | --- |
| TiDB Cloud API keys | Create and manage Filesystem resources and generate owner tokens | The account's permissions | A trusted administrator or automation environment |
| Owner FS token | Manage files and tokens within one Filesystem | One Filesystem | A trusted machine or secret manager |
| Scoped FS token | Delegate selected file operations | Specified paths and operations in one Filesystem | The user or application that needs that access |

### TiDB Cloud API keys

A TiDB Cloud public/private API key pair authorizes resource-management operations according to the account's permissions. Use it to create, list, describe, and delete Filesystems, generate owner tokens, and configure Filesystem AI providers.

Configure the keys with `ti configure`, or provide `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY` together. They are not FS tokens and do not directly replace the token used by a mount.

### Owner FS tokens

An owner token grants broad access within one Filesystem, including reading, writing, and deleting files. It can issue scoped tokens, list token metadata, and revoke tokens in that Filesystem. It can enable or disable scoped tokens, but enabling or disabling owner tokens requires TiDB Cloud API keys. It is a high-privilege secret, not a read-only mount credential.

An owner FS token is not interchangeable with TiDB Cloud API keys: it cannot create or delete the Filesystem resource or generate another owner token through `ti`. In particular, deleting a file and deleting its Filesystem are different permissions.

Filesystem creation returns an owner token and stores it locally for the creating profile. To generate another owner token, use [`ti fs generate-file-system-token`](/tidb-cloud-filesystem/manage-filesystem-tokens.md#generate-an-owner-token) with TiDB Cloud API keys.

### Scoped FS tokens

A scoped token limits access to specified path prefixes and operations. The supported operations are `read`, `list`, `search`, `write`, and `delete`. The service enforces these permissions, including when requests arrive through a mount.

- A reporting agent might need `read,list` for `/inputs` and `read,list,write` for `/reports`.
- A reviewer might need only `read,list` for `/reports`.
- `search` also requires `read` on the scope.

Scoped tokens cannot generate child tokens or manage token inventory. A scoped token can refresh itself while valid; refresh does not turn it into an owner token or broaden its permissions.

Choose a scoped token when delegating access to an agent or another machine. Keep the owner token on a trusted machine, and use a secret manager to deliver only the scoped token. To generate and use one, see [Manage TiDB Cloud Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md#generate-and-delegate-a-scoped-token).

## Understand local selection

One Filesystem can have multiple remote tokens, but one CLI profile stores at most one selected local token for that Filesystem. Local state is a credential selection, not the authoritative remote token inventory.

### Select a token for data access

- `--fs-token` takes precedence over `TI_FS_TOKEN` for token-based operations.
- Without an explicit token, data-access commands use the locally stored credential for `--file-system-id` or `TI_FS_FILE_SYSTEM_ID`.
- An explicit token contains the Filesystem ID. A clean environment therefore needs only `TI_FS_TOKEN` and `TI_REGION_CODE` for data access.
- Generating a token does not select it locally unless you pass `--store-locally`. Replacing the local selection does not revoke the previous remote token.

### Keep management credentials separate

For token list, enable, disable, and delete commands, an explicitly supplied owner token selects bearer authentication; otherwise the CLI uses TiDB Cloud API keys and requires a Filesystem ID.

> **Note:**
>
> A scoped token does not gain administrative capability merely because account keys also exist in the profile.

## What's next

- [Share one Filesystem with multiple machines](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Generate, rotate, or revoke Filesystem tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).
- [Mount a token-scoped directory](/tidb-cloud-filesystem/filesystem-mount.md).

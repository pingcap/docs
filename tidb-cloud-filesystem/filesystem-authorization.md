---
title: TiDB Cloud Filesystem Authorization
summary: Learn how TiDB Cloud API credentials, owner tokens, and scoped tokens provide different levels of access to TiDB Cloud Filesystem.
---

# TiDB Cloud Filesystem Authorization

TiDB Cloud Filesystem uses different credentials for managing a file system and accessing its data. This lets you keep high-privilege credentials in a trusted environment while giving users, applications, and agents only the access they need.

In general, access becomes more limited at each level:

```plaintext
TiDB Cloud API credentials
        ↓
Manage file system resources
        ↓
Owner token
        ↓
Access one file system
        ↓
Scoped token
        ↓
Access selected paths and operations
```

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Authorization model

TiDB Cloud Filesystem uses the following credential types:

| Credential                 | Access                                                                              | Typical use                                                             |
| -------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| TiDB Cloud API credentials | Manage file system resources and owner tokens according to the account's permissions | File system administration in a trusted environment                      |
| Owner token                | Broad access to one file system, including its data and scoped-token management      | Trusted workflows that need full file system access                      |
| Scoped token               | Access only to specified paths and operations in one file system                     | Users, applications, agents, or other machines that need limited access |

These credentials are not interchangeable. TiDB Cloud API credentials manage the file system resource itself, while file system tokens control access within a file system.

## TiDB Cloud API credentials

TiDB Cloud API credentials consist of a public and private API key pair. Their permissions are determined by the associated TiDB Cloud account.

Use TiDB Cloud API credentials for resource-level operations such as creating, listing, describing, and deleting file systems. They are also required to generate owner tokens.

Keep these credentials in a trusted administrative or automation environment rather than distributing them to applications or agents that only need access to file system data.

Configure these credentials with `ti configure`, or provide `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY` together. For details, see [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md).

## Owner tokens

An owner token provides broad access to one file system. It can read, write, and delete files and can create and manage scoped tokens for that file system.

An owner token applies only to its file system. It does not replace TiDB Cloud API credentials for resource-level operations such as creating or deleting file systems. An owner token also cannot create another owner token; generating another owner token requires TiDB Cloud API credentials.

Because an owner token has broad privileges within a file system, keep it on a trusted machine or in a secret manager. When another user, application, or agent needs only limited access, create a scoped token instead of sharing the owner token.

A file system can have multiple active owner tokens. This lets different users, applications, or environments use separate credentials instead of sharing the same token.

For instructions on generating and managing owner tokens, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md).

## Scoped tokens

A scoped token limits access to specified paths and operations within one file system.

The supported operations are:

- `read`: read file content and metadata.
- `list`: list entries under a directory.
- `search`: search for files under the allowed path. `search` also requires `read`.
- `write`: create or modify files and directories.
- `delete`: delete files or directories.

For example, a reporting application could have:

- `read,list` access to `/inputs`
- `read,list,write` access to `/reports`

Another user that only needs to review generated reports could receive `read,list` access to `/reports`.

Scoped permissions are enforced by the file system service, including when the file system is accessed through a mount. A scoped token cannot broaden its own permissions or create or manage other tokens. A scoped token can be refreshed while it is valid, but refreshing it does not broaden its permissions.

After a scoped token is issued, disabling or revoking the owner token that created it does not automatically revoke the scoped token. Revoke scoped tokens separately when their access is no longer needed.

Use scoped tokens when giving file system access to users, applications, agents, or other machines that do not need full access to the file system.

For instructions on creating and delegating scoped tokens, see [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md#generate-and-delegate-a-scoped-token).

## Credential boundaries

Use the credential with the minimum access required for a workflow:

* Use **TiDB Cloud API credentials** to manage the file system resource.
* Use an **owner token** when a trusted workflow needs broad access to one file system or needs to delegate access.
* Use a **scoped token** when a user, application, or agent needs access only to specific paths and operations.

Having multiple credential types available in the same environment does not combine their permissions. For example, a scoped token remains scoped even if TiDB Cloud API credentials are also configured.

TiDB Cloud CLI can store a selected file system token locally for convenience. Local credential selection does not change, disable, or revoke remote tokens. For details about how `ti` selects file systems and credentials, see [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md).

## What's next

- [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [Share a File System Across Machines](/tidb-cloud-filesystem/filesystem-sharing.md)
- [Mount a File System](/tidb-cloud-filesystem/filesystem-mount.md)

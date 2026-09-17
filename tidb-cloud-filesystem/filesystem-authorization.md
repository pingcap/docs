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

### TiDB Cloud API keys

A TiDB Cloud public/private API key pair authorizes resource-management operations according to the account's permissions. Use it to create, list, describe, and delete Filesystems, generate owner tokens, and configure Filesystem AI providers.

Configure the keys with `ti configure`, or provide `TIDB_CLOUD_PUBLIC_KEY` and `TIDB_CLOUD_PRIVATE_KEY` together. They are not FS tokens and do not directly replace the token used by a mount.

### Owner FS tokens

An owner token grants broad access within one Filesystem, including reading, writing, and deleting files. It can issue scoped tokens, list token metadata, and revoke tokens in that Filesystem. It can enable or disable scoped tokens, but enabling or disabling owner tokens requires TiDB Cloud API keys. It is a high-privilege secret, not a read-only mount credential.

An owner FS token is not interchangeable with TiDB Cloud API keys: it cannot create or delete the Filesystem resource or generate another owner token through `ti`. In particular, deleting a file and deleting its Filesystem are different permissions.

Filesystem creation returns an owner token and stores it locally for the creating profile. To generate another owner token, use `ti fs generate-file-system-token` with TiDB Cloud API keys.

### Scoped FS tokens

A scoped token limits access to specified path prefixes and operations. The supported operations are `read`, `list`, `search`, `write`, and `delete`. The service enforces these permissions, including when requests arrive through a mount.

- A reporting agent might need `read,list` for `/inputs` and `read,list,write` for `/reports`.
- A reviewer might need only `read,list` for `/reports`.
- `search` also requires `read` on the scope.

Scoped tokens cannot generate child tokens or manage token inventory. A scoped token can refresh itself while valid; refresh does not turn it into an owner token or broaden its permissions.

## Delegate access to an agent

On a trusted machine with a locally stored owner token, select the Filesystem and generate a limited token:

```bash
# Capture the one-time token response without printing the secret.
SCOPED_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "<file-system-id>" \
  --subject report-agent \
  --ttl 24h \
  --allow /workspace:read,list,write \
  --query fs_token --output text)"
```

Transfer `SCOPED_TOKEN` through a secret manager. In the agent's environment, inject it as `TI_FS_TOKEN` and provide the Filesystem's region:

```bash
# In the agent environment, these values normally come from secret injection.
export TI_FS_TOKEN="<scoped-token>"
export TI_REGION_CODE="aws-us-east-1"
ti fs list-files --path /workspace
```

The remote `/workspace` directory must already exist. For a mount, select the allowed subtree with `--remote-path /workspace`. Mounting the root `/` is not appropriate for a token that has access only to `/workspace`.

## Understand local selection

One Filesystem can have multiple remote tokens, but one CLI profile stores at most one selected local token for that Filesystem. Local state is a credential selection, not the authoritative remote token inventory.

- `--fs-token` takes precedence over `TI_FS_TOKEN` for token-based operations.
- Without an explicit token, data-access commands use the locally stored credential for `--file-system-id` or `TI_FS_FILE_SYSTEM_ID`.
- An explicit token contains the Filesystem ID. A clean environment therefore needs only `TI_FS_TOKEN` and `TI_REGION_CODE` for data access.
- Generating a token does not select it locally unless you pass `--store-locally`. Replacing the local selection does not revoke the previous remote token.

For token list, enable, disable, and delete commands, an explicitly supplied owner token selects bearer authentication; otherwise the CLI uses TiDB Cloud API keys and requires a Filesystem ID. A scoped token does not gain administrative capability merely because account keys also exist in the profile.

## Rotate and revoke credentials

List token metadata to identify the token you want to manage:

```bash
# Use TiDB Cloud API keys when no explicit FS token is present.
ti fs list-file-system-tokens --file-system-id "<file-system-id>" --output text
```

The list does not return token plaintext. Preserve newly generated or refreshed tokens in a secret manager. If you lose an owner token, generate a replacement using TiDB Cloud API keys; do not expect to recover the original secret by listing tokens.

To retire a token, stop its consumers and use its token ID:

```bash
# Revoke only the retired token, not the Filesystem itself.
ti fs delete-file-system-token --file-system-id "<file-system-id>" --token-id "<token-id>"
```

Token changes can take time to propagate through authorization caches. Rotate by distributing and validating a replacement before retiring the old token. Do not treat disabling an owner token as an implicit replacement for reviewing and revoking previously issued scoped tokens.

> **Warning:**
>
> Stop writes and unmount consumers before refreshing, disabling, or deleting their token. The CLI checks known local mounts but cannot discover every remote machine using the secret. Token refresh is non-idempotent: if the request might have succeeded but the response was lost, do not blindly retry it with the old token.

## What's next

- [Share one Filesystem with multiple machines](/tidb-cloud-filesystem/filesystem-sharing.md).
- [Look up token management commands](/tidb-cloud-filesystem/manage-filesystem-tokens.md).
- [Mount a token-scoped directory](/tidb-cloud-filesystem/filesystem-mount.md).

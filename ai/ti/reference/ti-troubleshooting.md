---
title: Troubleshoot TiDB Cloud CLI
summary: Diagnose TiDB Cloud CLI authentication, project, Filesystem selection, companion, quota, SQL user, mount, and interrupted-cleanup failures.
---

# Troubleshoot TiDB Cloud CLI

Use this reference to diagnose common current TiDB Cloud CLI failures. Add `--debug` only when needed; debug output is redacted but should still be reviewed before sharing.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## API authentication fails

Symptoms include missing credentials, Digest authentication failure, or permission denied.

Check that both environment values are set together:

```bash
test -n "$TI_PUBLIC_KEY"
test -n "$TI_PRIVATE_KEY"
```

If you intend to use saved credentials, unset both variables and verify the profile:

```bash
unset TI_PUBLIC_KEY TI_PRIVATE_KEY
ti db list-db-clusters --db-cluster-type starter --profile default
```

An API key can authenticate successfully but still lack the permission declared by a command. Use a key with the access required by that operation. `ti configure` validates and stores local values without contacting TiDB Cloud, so credential failures first appear on a remote command.

## Filesystem token is missing

For a clean sandbox, provide the token and region. `ti` derives the file system ID from the token:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
ti fs check-file-system
```

The FS token is not the TiDB Cloud API private key. `TI_FS_FILE_SYSTEM_ID` is optional when a token is supplied; set it only when you want `ti` to verify that a separately distributed ID matches the token.

If the token is known but is not stored on the current machine, import it and then select the derived ID:

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1
ti fs list-files --file-system-id <file-system-id> --path /
```

If every known token is lost or revoked, use TiDB Cloud API keys to generate another owner token:

```bash
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name recovery \
  --ttl 24h
```

The new plaintext appears once in the response. Store it securely or add `--store-locally` to select it on the current machine.

## Filesystem token is rejected

A data-plane HTTP 401 cannot distinguish a token that was disabled, expired, refreshed on another machine, or revoked. Inspect remote metadata with TiDB Cloud API keys:

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

Token names are not unique. Use the immutable `token_id` from this output for enable, disable, or delete operations. Old credentials created or imported without token lifecycle metadata can remain valid, but `ti` cannot safely identify their list row and never guesses a match.

After enable, disable, delete, or refresh, allow approximately 10 seconds for authentication caches to converge. If refresh reports `fs.token_refresh_ambiguous`, the server might have rotated the token even though the response was lost. Do not retry with the old token. Generate another owner token through TiDB Cloud credentials.

If token mutation reports `fs.token_mount_active`, use the exact mount path in the error:

```bash
ti fs drain-file-system --mount-path /path/to/workspace
ti fs unmount-file-system --mount-path /path/to/workspace
```

Then retry the token operation. A mount on another machine is not visible locally; coordinate rotation with that machine separately.

## Filesystem selection is missing

List remote resources in the configured region with TiDB Cloud API keys and select one explicitly:

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

Or select the Filesystem for subsequent commands in the current shell:

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

The TiDB Cloud CLI intentionally does not infer a Filesystem from local credential count, including when only one credential exists. Supply its ID or an FS token whose embedded ID can be derived.

## Filesystem region is unsupported

The configured TiDB Cloud region might not be one of the Filesystem endpoints built into the installed TiDB Cloud CLI release. Compare it with [current Filesystem regions](/ai/ti/reference/ti-regions-security-and-limitations.md#filesystem-regions). Change placement with a valid profile or command-scoped `--region`; do not configure a raw server URL.

## Companion is missing or incompatible

The release installer places `ti-drive9` next to `ti`. Re-run the current installer when the TiDB Cloud CLI reports a missing companion:

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

Verify that `PATH` resolves the expected `ti`:

```bash
command -v ti
ti --version
```

Do not copy an arbitrary standalone Drive9 binary into place.

## Starter or Filesystem creation reaches quota

Quota and capacity errors can mean the organization has reached its free Starter limit. List existing resources before creating another:

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

Never delete an unrelated resource to make automation pass. A Starter spending limit can require configured billing.

## SQL credentials are missing

Prepare or repair users for the exact cluster:

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
```

Then retry with an explicit role:

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

Deleting `~/.ti/db_users/<cluster-id>/credentials` removes local passwords. Run the create/repair command rather than inventing credentials.

## Mount does not become ready

Background mount success prints the TiDB Cloud CLI result without Drive9 startup messages. If startup fails or times out, inspect the companion log path in the error. Confirm:

- the mount path exists and is writable;
- no existing mount covers the path;
- the FS token and region are valid;
- FUSE prerequisites or the WebDAV helper are installed;
- the remote region is reachable.

macOS defaults to WebDAV. To request FUSE after installing macFUSE:

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux needs FUSE3 and access to `/dev/fuse`. Windows WebDAV needs the WebClient service and a drive letter such as `X:`.

## Ubuntu 26.04 rejects a FUSE mount under `/workspace`

Ubuntu 26.04 applies an AppArmor profile to `fusermount3`. Its default mount-path allowlist does not include `/workspace`, so root and non-root users can both receive:

```text
/usr/bin/fusermount3: mount failed: Permission denied
```

Confirm the denial:

```bash
sudo journalctl -k --since "10 minutes ago" |
  grep 'profile="fusermount3"'
```

An entry with `operation="mount"`, `name="/workspace/"`, and `info="failed mntpnt match"` identifies this restriction. Mount under `$HOME` or `/mnt` instead:

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

Changing the owner or mode of `/workspace` does not bypass AppArmor. If the path cannot change, add explicit `/workspace` mount and unmount rules to `/etc/apparmor.d/local/fusermount3` as described in [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md#ubuntu-2604-mount-paths).

## Mount becomes stale after a process crash

If the companion is killed without graceful unmount, FUSE access can return `EIO` or `Transport endpoint is not connected`. Stop processes with open files, then try:

```bash
ti fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

Use `--ignore-absent` when cleanup should succeed if no locator remains. Abrupt cleanup cannot guarantee recovery of pending writes from a deleted local disk.

## Unmount reports busy

Close editors, shells whose working directory is inside the mount, and other open file handles, and then retry:

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

Unmount performs the graceful FUSE drain automatically. Running `drain-file-system` separately does not close file descriptors or resolve a busy mount; use it only when you need to flush pending work while leaving the mount online. Drain is not supported for WebDAV.

## An interrupted command leaves resources

List resources and identify only those created by your workflow. Use describe before delete:

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
ti fs describe-file-system --file-system-id "<filesystem-name>"
```

Preview supported cleanup:

```bash
ti db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
ti fs delete-file-system \
  --file-system-id "<filesystem-name>" \
  --dry-run
```

## Report a problem

Include the TiDB Cloud CLI version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, FS or vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/ti/issues](https://github.com/tidbcloud/ti/issues).

---
title: Troubleshoot TiDB Cloud Filesystem
summary: Learn how to diagnose TiDB Cloud Filesystem token, region, runtime, mount, and access failures and choose a safe recovery path.
---

# Troubleshoot TiDB Cloud Filesystem

Use the symptoms below to diagnose Filesystem access and mount failures. Add `--debug` only when needed, and review redacted output before sharing it. For CLI installation, API key authentication, Starter, or SQL failures, see [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md).

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Filesystem token is missing

For a clean sandbox, provide the token and region. `ti` derives the Filesystem ID from the token:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

The Filesystem token is not the TiDB Cloud API private key. `TI_FS_FILE_SYSTEM_ID` is optional when a token is supplied; set it only when you want `ti` to verify that a separately distributed ID matches the token.

If the token is known but is not stored on the current machine, import it and then select the derived ID:

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region <filesystem-region-code>
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

After enable, disable, delete, or refresh, allow approximately 10 seconds for authentication caches to converge. If refresh reports `fs.token_refresh_ambiguous`, the server might have rotated the token even though the response was lost. The outcome is unknown: the old token might still work if the refresh did not commit, or it might already be invalid. The replacement token from a committed refresh cannot be recovered because its response was lost. Do not retry the refresh with the old token. Instead, use TiDB Cloud credentials to generate an independent owner token.

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

The CLI intentionally does not infer a Filesystem from local credential count, including when only one credential exists. Supply its ID or a Filesystem token whose embedded ID can be derived.

## Filesystem region is unsupported

The configured TiDB Cloud region might not be one of the Filesystem endpoints built into the installed `ti` release. Compare it with [supported Filesystem regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions). Change placement with a valid profile or command-scoped `--region`; do not configure a raw server URL.

## Filesystem runtime is missing or incompatible

The release installer places the bundled Filesystem runtime component next to `ti`. You do not invoke this runtime directly. Re-run the current installer when the CLI reports a missing runtime component:

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

Verify that `PATH` resolves the expected `ti`:

```bash
command -v ti
ti --version
```

Do not copy an arbitrary standalone runtime binary into place.

## Filesystem creation reaches quota

If creation returns a quota or capacity error, list existing Filesystems in the configured region before trying again:

```bash
ti fs list-file-systems --output text
```

Do not delete an unrelated Filesystem to make automation pass. If the error links to TiDB Cloud billing because a payment method is required, follow that guidance before retrying.

## Mount does not become ready

Background mount success prints the CLI result without runtime startup messages. If startup fails or times out, inspect the runtime log path in the error. Confirm:

- the mount path exists and is writable;
- no existing mount covers the path;
- the Filesystem token and region are valid;
- FUSE prerequisites or the WebDAV helper are installed;
- the remote region is reachable.

On macOS without macFUSE, `ti` uses WebDAV. If macFUSE is installed, automatic driver selection prefers FUSE. To explicitly request FUSE:

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux needs FUSE support, the `fuse3` package, and access to `/dev/fuse`. Filesystem and Vault mounts are not supported on Windows; use `ti fs` data-plane commands or non-mount Vault commands instead.

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

Changing the owner or mode of `/workspace` does not bypass AppArmor. If the path cannot change, add explicit `/workspace` mount and unmount rules to `/etc/apparmor.d/local/fusermount3` as described in [Ubuntu 26.04 mount-path restrictions](/tidb-cloud-filesystem/filesystem-mount-linux.md#ubuntu-2604-mount-path-restrictions).

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

## Report a problem

Include the `ti` version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, Filesystem or Vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues).

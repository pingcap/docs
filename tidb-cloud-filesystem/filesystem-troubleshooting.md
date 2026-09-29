---
title: Troubleshoot TiDB Cloud Filesystem
summary: Learn how to diagnose file system token, region, runtime, mount, and access failures and choose a safe recovery path.
---

# Troubleshoot TiDB Cloud Filesystem

Use the symptoms below to diagnose file system access and mount failures. Add `--debug` only when needed, and review redacted output before sharing it. For CLI installation, API key authentication, Starter, or SQL failures, see [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md).

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## File system token is missing

For a clean sandbox, provide the token and region. `ti` derives the file system ID from the token:

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

The file system token is not the TiDB Cloud API private key. `TI_FS_FILE_SYSTEM_ID` is optional when a token is supplied; set it only when you want `ti` to verify that a separately distributed ID matches the token.

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

## File system token is rejected

A data-plane HTTP 401 cannot distinguish a token that was disabled, expired, refreshed on another machine, or revoked. Inspect remote metadata with TiDB Cloud API keys:

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

Token names are not unique, so use the immutable `token_id` from this output for enable, disable, or delete operations. An older credential that was created or imported without token lifecycle metadata can still be valid, but it has no row in this list, and `ti` never guesses a match.

After you enable, disable, delete, or refresh a token, allow about 10 seconds for authentication caches to converge.

If refresh reports `fs.token_refresh_ambiguous`, the response was lost and the outcome is unknown. The old token might still work, if the rotation never committed, or it might already be invalid, and the replacement token cannot be recovered. Do not retry the refresh with the old token. Use TiDB Cloud credentials to generate an independent owner token instead.

If a file command reports `invalid API key` and exit code 1 while you are passing a file system token, check the token status before you look at your API key pair. A deleted or disabled token produces this message even when the API key pair is correct.

If token mutation reports `fs.token_mount_active`, use the exact mount path in the error:

```bash
ti fs drain-file-system --mount-path /path/to/workspace
ti fs unmount-file-system --mount-path /path/to/workspace
```

Then retry the token operation. A mount on another machine is not visible locally; coordinate rotation with that machine separately.

## Scoped token access is denied

A scoped token used outside its scope causes the command to exit with code 1 and report one of two messages. Most commands report `fs access denied`. `ti fs copy-file` can report an empty `HTTP 403:` instead.

In this context, both messages indicate that the token does not allow this operation on this path. Neither one is a connectivity problem or a sign that the token is invalid. Check what the token allows before you change anything:

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --output text
```

Compare the token scope with the path and the operation you used. `search` also requires `read`. A scoped token cannot list the file system root unless its allowed path is `/`. A scoped token cannot widen its own permissions, so use an owner token to generate a new scoped token with the operations you need instead of trying to change the existing token.

## File system selection is missing

List remote resources in the configured region with TiDB Cloud API keys and select one explicitly:

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

Or select the file system for subsequent commands in the current shell:

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

The CLI intentionally does not infer a file system from local credential count, including when only one credential exists. Supply its ID or a file system token whose embedded ID can be derived.

## File system region is unsupported

The configured TiDB Cloud region might not be one of the file system endpoints built into the installed `ti` release. Compare it with [supported file system regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions). Change placement with a valid profile or command-scoped `--region`; do not configure a raw server URL.

## File system runtime is missing or incompatible

The release installer places the bundled file system runtime component next to `ti`. You do not invoke this runtime directly. Re-run the current installer when the CLI reports a missing runtime component:

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

Verify that `PATH` resolves the expected `ti`:

```bash
command -v ti
ti --version
```

Do not copy an arbitrary standalone runtime binary into place.

## File system creation reaches quota

If creation returns a quota or capacity error, list existing file systems in the configured region before trying again:

```bash
ti fs list-file-systems --output text
```

Do not delete an unrelated file system to make automation pass. If the error links to TiDB Cloud billing because a payment method is required, follow that guidance before retrying.

## Mount does not become ready

Background mount success prints the CLI result without runtime startup messages. If startup fails or times out, inspect the runtime log path in the error. Confirm:

- the mount path exists and is writable;
- no existing mount covers the path;
- the file system token and region are valid;
- FUSE prerequisites or the WebDAV helper are installed;
- the remote region is reachable.

On macOS without macFUSE, `ti` uses WebDAV. If macFUSE is installed, automatic driver selection prefers FUSE. To explicitly request FUSE:

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux needs FUSE support, the `fuse3` package, and access to `/dev/fuse`. File system and Vault mounts are not supported on Windows; use `ti fs` data-plane commands or non-mount Vault commands instead.

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

## Exit codes

`ti fs` uses the following exit codes. Automation can branch on them instead of matching error text.

| Code | Meaning | What to do |
| --- | --- | --- |
| 0 | Success | Continue. |
| 1 | Runtime or remote API error | Read the message and address the reported runtime, network, or service error. Scoped token denials and some other service errors also use this code. |
| 2 | Local usage, validation, or configuration error | Fix the command or the profile. Examples include an unknown flag, missing required input, an unsupported region, or a token file with loose permissions. |
| 3 | Authentication failed | Check the token or the API key pair. |
| 4 | The account lacks permission for the operation | Ask an organization administrator. This is different from a scoped-token denial, which returns exit code 1. |
| 5 | The file system, token, or other resource named in the request does not exist | Check the ID. A path that does not exist inside a file system returns 1, not 5. |

A deleted or disabled file system token is an exception to the preceding table: file commands return exit code 1 rather than 3. See [File system token is rejected](#file-system-token-is-rejected).

## Report a problem

Include the `ti` version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, file system or Vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues).

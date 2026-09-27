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

An HTTP 401 or `invalid API key` error from a file operation can indicate that the file system token is disabled, expired, refreshed on another machine, or revoked. In this context, `API key` can refer to the file system token; it does not necessarily indicate a problem with your TiDB Cloud API keys. Inspect token metadata using TiDB Cloud API keys:

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

Token names are not unique. Use the immutable `token_id` from this output for enable, disable, or delete operations. Old credentials created or imported without token lifecycle metadata can remain valid, but `ti` cannot safely identify their list row and never guesses a match.

After enable, disable, delete, or refresh, allow approximately 10 seconds for authentication caches to converge. If refresh reports `fs.token_refresh_ambiguous`, the server might have rotated the token even though the response was lost. The outcome is unknown: the old token might still work if the refresh did not commit, or it might already be invalid. The replacement token from a committed refresh cannot be recovered because its response was lost. Do not retry the refresh with the old token. Instead, use TiDB Cloud credentials to generate an independent owner token.

If token mutation reports `fs.token_mount_active`, stop applications using the mount, close open files, and unmount using the exact path in the error:

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

A normal FUSE unmount drains pending writes automatically. WebDAV does not support `drain-file-system`; use normal unmount for WebDAV.

Then retry the token operation. A mount on another machine is not visible locally; coordinate rotation with that machine separately.

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

Select a file system explicitly, even if only one token is stored locally. Supply its ID or a token that identifies it.

## File system region is unsupported

Your installed `ti` release might not support the configured region for file system access. Check the [supported file system regions](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md#supported-regions). Select a supported region in your profile or with `--region` for the command; do not configure a raw server URL.

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

When a background mount starts successfully, the CLI prints the result without runtime startup messages. If startup fails or times out, inspect the log at the path reported in the error. Confirm that:

- The mount path exists and is writable.
- No existing mount uses the path.
- The file system token and region are valid.
- The FUSE prerequisites or WebDAV helper are installed.
- The remote region is reachable.

On macOS without macFUSE, `ti` uses WebDAV. If macFUSE is installed, automatic driver selection prefers FUSE. To explicitly request FUSE:

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux needs FUSE support, the `fuse3` package, and access to `/dev/fuse`. File system and Vault mounts are not supported on Windows; use `ti fs` data-plane commands or non-mount Vault commands instead.

## Mount succeeds but file access hangs

A `mounted` result confirms that mount startup completed. It does not prove that subsequent file reads or writes succeed. A directory listing can also succeed while reading a file hangs.

For a known small test file, use the following procedure:

1. If the mounted read or write has not returned after 30 seconds, interrupt the command with Ctrl+C. If it remains blocked, open another terminal outside the mount for diagnosis. Do not start additional workloads on the mount.
2. Read the same file through `ti fs read-file --path "<remote-file-path>"`, using the same token and region. If the mount uses `--remote-path`, include that prefix in the remote file path. If this read also fails, resolve the reported authentication, region, or service error first. If it succeeds, focus diagnosis on the local mount path.
3. Record `ti --version`, the OS version, the selected driver, elapsed time, and the mount diagnostic log when available. Do not include tokens or file contents. On macOS, automatic selection can choose WebDAV or FUSE; specify `--driver webdav` or `--driver fuse` when reproducing the problem.
4. Stop applications using the mount, close open files, leave any shell working directory inside the mount, and try normal unmount:

    ```bash
    ti fs unmount-file-system --mount-path /path/to/workspace
    ```

5. After successful unmount, verify any required writes with direct CLI reads. Continue with direct `ti fs` commands while investigating the mount, and verify file I/O before using a replacement mount.

Do not use `drain-file-system` for WebDAV. If unmount fails or remote data is missing, keep the machine and local mount data available for recovery. Do not delete the cache or force unmount as a routine retry: pending writes might still exist only locally. The 30-second cutoff above is a diagnostic limit for a small-file smoke test, not a service latency guarantee.

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

A successful FUSE unmount flushes pending writes automatically. Running `drain-file-system` separately does not close open files or resolve a busy mount. Use it to flush pending writes while keeping the mount running. WebDAV does not support drain.

## Unmount returns success but the mount process exits abnormally

In `ti v0.2.6`, a layer or checkpoint mount can return `unmounted` after approximately 30 seconds even when its background process reports `late pending drain` followed by `reason=force_quit` and exit code `1`. This behavior has been observed after reading a small file from a layer and after writing, fsyncing, and draining a layer mount.

Treat this result as an abnormal shutdown. Keep the machine and local cache available, and verify required files with direct CLI reads. For a layer, supply its `--layer-id` when reading; for committed changes, read the base file system without selecting a layer. Do not delete local state or discard the layer until verification completes. Include the CLI version and redacted mount log when reporting the problem.

## Report a problem

Include the `ti` version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, file system or Vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues).

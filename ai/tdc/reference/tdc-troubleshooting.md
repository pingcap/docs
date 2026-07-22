---
title: Troubleshoot tdc
summary: Diagnose tdc authentication, project, Filesystem selection, companion, quota, SQL user, mount, and interrupted-cleanup failures.
---

# Troubleshoot tdc

Use this reference to diagnose common current tdc failures. Add `--debug` only when needed; debug output is redacted but should still be reviewed before sharing.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## API authentication fails

Symptoms include missing credentials, Digest authentication failure, or permission denied.

Check that both environment values are set together:

```bash
test -n "$TDC_PUBLIC_KEY"
test -n "$TDC_PRIVATE_KEY"
```

If you intend to use saved credentials, unset both variables and verify the profile:

```bash
unset TDC_PUBLIC_KEY TDC_PRIVATE_KEY
tdc organization list-projects --profile default
```

An API key can authenticate successfully but still lack the permission declared by a command. Use a key with the required organization or project access.

## Configure cannot find a virtual project

`tdc configure` requires exactly one accessible project whose `type` is `tidbx_virtual`.

```bash
tdc organization list-projects \
  --query 'projects[].{id:id,name:name,type:type}'
```

If no virtual project appears, confirm the API key's organization and project access. If multiple virtual projects appear, report the ambiguous account state through the [tdc issue tracker](https://github.com/tidbcloud/tdc/issues).

## Filesystem token is missing

For a clean sandbox, provide all three values:

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
tdc fs check-file-system
```

The FS token is not the TiDB Cloud API private key.

## Filesystem selection is ambiguous

List registered resources and select one explicitly:

```bash
tdc fs list-file-systems --output text
tdc fs list-files --file-system-name workspace --path /
```

Or set a default:

```bash
tdc fs set-default-file-system --file-system-name workspace
```

tdc intentionally does not guess among multiple resources.

## Filesystem region is unsupported

The configured TiDB Cloud region might not have a `tidb_cloud_native` Filesystem endpoint. Compare it with [current Filesystem regions](/ai/tdc/reference/tdc-regions-security-and-limitations.md#filesystem-regions). Change placement with a valid profile or command-scoped `--region`; do not configure a raw server URL.

## Companion is missing or incompatible

The release installer places `tdc-drive9` next to `tdc`. Re-run the current installer when tdc reports a missing companion:

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
```

Verify that `PATH` resolves the expected tdc:

```bash
command -v tdc
tdc --version
```

Do not copy an arbitrary standalone Drive9 binary into place.

## Starter or Filesystem creation reaches quota

Quota and capacity errors can mean the organization has reached its free Starter limit. List existing resources before creating another:

```bash
tdc db list-db-clusters --output text
tdc fs list-file-systems --output text
```

Never delete an unrelated resource to make automation pass. A Starter spending limit can require configured billing.

## SQL credentials are missing

Prepare or repair users for the exact cluster:

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
```

Then retry with an explicit role:

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

Deleting `~/.tdc/db_users/<cluster-id>/credentials` removes local passwords. Run the create/repair command rather than inventing credentials.

## Mount does not become ready

Inspect the log path printed by the timeout error. Confirm:

- the mount path exists and is writable;
- no existing mount covers the path;
- the FS token and region are valid;
- FUSE prerequisites or the WebDAV helper are installed;
- the remote region is reachable.

macOS defaults to WebDAV. To request FUSE after installing macFUSE:

```bash
tdc fs mount-file-system \
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
tdc fs mount-file-system --mount-path "$HOME/workspace"
```

Changing the owner or mode of `/workspace` does not bypass AppArmor. If the path cannot change, add explicit `/workspace` mount and unmount rules to `/etc/apparmor.d/local/fusermount3` as described in [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md#ubuntu-2604-mount-paths).

## Mount becomes stale after a process crash

If the companion is killed without graceful unmount, FUSE access can return `EIO` or `Transport endpoint is not connected`. Stop processes with open files, then try:

```bash
tdc fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

Use `--ignore-absent` when cleanup should succeed if no locator remains. Abrupt cleanup cannot guarantee recovery of pending writes from a deleted local disk.

## Unmount reports busy

Close editors, shells whose working directory is inside the mount, and other open file handles, and then retry:

```bash
tdc fs unmount-file-system --mount-path /path/to/workspace
```

Unmount performs the graceful FUSE drain automatically. Running `drain-file-system` separately does not close file descriptors or resolve a busy mount; use it only when you need to flush pending work while leaving the mount online. Drain is not supported for WebDAV.

## An interrupted command leaves resources

List resources and identify only those created by your workflow. Use describe before delete:

```bash
tdc db describe-db-cluster --db-cluster-id "<cluster-id>"
tdc fs describe-file-system --file-system-name "<filesystem-name>"
```

Preview supported cleanup:

```bash
tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
tdc fs delete-file-system \
  --file-system-name "<filesystem-name>" \
  --dry-run
```

## Report a problem

Include the tdc version, OS and architecture, command name, stable error code, and redacted logs. Never include API keys, FS or vault tokens, DB passwords, SQL containing private data, or file contents. Report issues at [github.com/tidbcloud/tdc/issues](https://github.com/tidbcloud/tdc/issues).

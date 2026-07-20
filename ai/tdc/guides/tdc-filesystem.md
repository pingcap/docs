---
title: Manage TiDB Cloud Filesystem with tdc
summary: Manage Filesystem resources, operate on files, use layers and packs, and mount Filesystems through the bundled Drive9 companion.
---

# Manage TiDB Cloud Filesystem with tdc

Use `tdc fs` to provision TiDB Cloud Filesystem resources and access their data from commands or local mounts.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

- Run `tdc configure` before provisioning or deleting a Filesystem.
- Install tdc with the release installer so the `tdc-drive9` companion is next to the `tdc` binary.
- Treat the returned FS owner token as a secret.

Data-plane commands can instead use an existing Filesystem with `TDC_FS_TOKEN`, `TDC_REGION_CODE`, and `TDC_FS_FILE_SYSTEM_NAME`, without TiDB Cloud API keys.

## Manage Filesystem resources

Create a resource and make it the profile default:

```bash
tdc fs create-file-system \
  --file-system-name workspace \
  --set-default \
  --wait
```

Without `--wait`, tdc returns after Drive9 accepts provisioning. With the flag, tdc waits up to 10 minutes until the root is readable through the public Drive9 data-plane CLI. A failed wait leaves the resource and locally stored credential intact.

The JSON response includes `fs_token`. Capture it without displaying the complete result:

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name sandbox \
  --wait \
  --query fs_token \
  --output text)"
```

List and describe locally registered resources:

```bash
tdc fs list-file-systems
tdc fs describe-file-system --file-system-name workspace
```

Set or clear a profile default:

```bash
tdc fs set-default-file-system --file-system-name workspace
tdc fs unset-default-file-system
```

Check the selected resource and companion:

```bash
tdc fs check-file-system --file-system-name workspace
```

Delete a resource only after removing data you need:

```bash
tdc fs delete-file-system \
  --file-system-name workspace
```

Create and delete support `--dry-run`. Deletion requires TiDB Cloud API keys and a locally registered resource; an FS token alone cannot delete the resource. Drive9 deletion is asynchronous, so a successfully accepted request reports `status: "deleting"` while tdc removes the selected local registry entry and credential.

## Select one of multiple Filesystems

One profile can own multiple resources. Selection precedence is:

1. `--file-system-name`;
2. `TDC_FS_FILE_SYSTEM_NAME`;
3. the profile default;
4. the only registered resource.

When selection is ambiguous, tdc fails. It never chooses an arbitrary Filesystem.

## Copy and read data

Upload, download, and copy remotely:

```bash
tdc fs copy-file --from-local ./README.md --to-remote /workspace/README.md
tdc fs copy-file --from-remote /workspace/README.md --to-local ./README.copy.md --create-parents
tdc fs copy-file --from-remote /workspace/README.md --to-remote /archive/README.md
```

Use `--overwrite` to replace an existing target, `--resume` for a supported interrupted upload or download, and `--recursive` for directories:

```bash
tdc fs copy-file --from-local ./src --to-remote /workspace/src --recursive
tdc fs copy-file --from-local ./large.bin --to-remote /workspace/large.bin --resume
```

Append and stream:

```bash
tdc fs copy-file --from-local ./tail.log --to-remote /logs/app.log --append
printf 'hello\n' | tdc fs copy-file --from-stdin --to-remote /workspace/stdin.txt
tdc fs copy-file --from-remote /workspace/stdin.txt --to-stdout
```

Add metadata during upload:

```bash
tdc fs copy-file \
  --from-local ./report.md \
  --to-remote /workspace/report.md \
  --tag owner=agent \
  --tag stage=review \
  --description "agent review report"
```

Read a complete file or a byte range:

```bash
tdc fs read-file --path /workspace/report.md
tdc fs read-file --path /workspace/large.bin --offset 1024 --length 4096
```

## Inspect and modify the namespace

```bash
tdc fs list-files --path /workspace
tdc fs describe-file --path /workspace/report.md
tdc fs create-directory --path /workspace/archive --mode 0755
tdc fs move-file --from-remote /workspace/report.md --to-remote /workspace/archive/report.md
tdc fs chmod-file --path /workspace/archive/report.md --mode 0600
tdc fs create-symlink --target archive/report.md --link-path /workspace/report.link
tdc fs create-hardlink --source-path /workspace/archive/report.md --link-path /workspace/report.hard
tdc fs delete-file --path /workspace/report.link
tdc fs delete-file --path /workspace/archive --recursive
```

Mutating namespace commands support `--dry-run`.

Search content and metadata:

```bash
tdc fs search-file-content --path /workspace --pattern "TODO" --limit 50
tdc fs find-files --path /workspace --file-name-pattern "*.md" --tag stage=review
```

`find-files` also supports resource type, time, size, and result-limit filters. Both search commands accept `--layer-id`.

## Use layers and checkpoints

A layer records changes over a base root before you commit or discard them:

```bash
tdc fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

Use the returned layer ID:

```bash
tdc fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

tdc fs list-layers
tdc fs describe-layer --layer-id "<layer-id>"
tdc fs diff-layer --layer-id "<layer-id>"
tdc fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id before-review \
  --label "before review"
```

Finish the layer by rolling it back or committing it:

```bash
tdc fs rollback-layer --layer-id "<layer-id>"
tdc fs commit-layer --layer-id "<layer-id>"
```

These two commands represent alternative outcomes for the same work; do not run both in sequence in a real workflow.

## Pack local overlay state

FUSE mount profiles can route selected paths to local overlay storage. Pack those paths to a remote archive before moving to another machine:

```bash
tdc fs pack-file-system --mount-path /path/to/workspace
tdc fs unpack-file-system --mount-path /path/to/workspace
```

Without an active mount, provide `--local-root`, `--remote-root`, and `--mount-profile`. `--archive-path` selects the remote archive, repeatable `--path` limits pack contents, and `--no-replace` makes unpack merge rather than replace manifest paths.

## Mount a Filesystem

Create the local mount path and mount in the background:

```bash
mkdir -p /path/to/workspace
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace
```

The default `--driver auto` is platform-specific. `--remote-path` exposes a subtree, `--read-only` prevents writes, and `--foreground` keeps the runtime attached to the terminal.

### Platform behavior

| Platform | `--driver auto` | Optional or required dependency | Notes |
| --- | --- | --- | --- |
| macOS | WebDAV | No extra dependency for WebDAV | Install macFUSE and select `--driver fuse` for the complete FUSE experience |
| Linux | FUSE | FUSE3 and access to `/dev/fuse`; install `davfs2` for explicit WebDAV | FUSE supports drain and FUSE cache controls |
| Windows | WebDAV | Windows WebClient service | Mount path must be a drive letter such as `X:`; FUSE and vault mount are unavailable |

### Mount in Docker and Docker Compose

Installing FUSE3 inside an image is not sufficient by itself. The Docker host must provide `/dev/fuse`, and the container must receive permission to perform the mount. The following Dockerfile installs the required Ubuntu package and tdc without storing any cloud or Filesystem credentials in the image:

```dockerfile
FROM ubuntu:24.04

ARG TDC_VERSION=latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl fuse3 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh \
    | sh -s -- --yes --version "${TDC_VERSION}"

ENV PATH="/root/.tdc/bin:${PATH}"

RUN mkdir -p /workspace

CMD ["bash"]
```

Build the image, then pass the Filesystem owner token, canonical region code, and Filesystem name at runtime:

```bash
docker build -t tdc-fuse .

docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TDC_FS_TOKEN \
  --env TDC_REGION_CODE \
  --env TDC_FS_FILE_SYSTEM_NAME \
  tdc-fuse
```

The three environment variables must already exist in the host shell. Inside the container, mount and use the Filesystem normally:

```bash
tdc fs mount --mount-path /workspace
printf 'hello from Docker\n' > /workspace/hello.txt
tdc fs umount --mount-path /workspace
```

Use the equivalent runtime settings in `compose.yaml`:

```yaml
services:
  agent:
    build:
      context: .
      args:
        TDC_VERSION: latest
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TDC_FS_TOKEN: ${TDC_FS_TOKEN}
      TDC_REGION_CODE: ${TDC_REGION_CODE}
      TDC_FS_FILE_SYSTEM_NAME: ${TDC_FS_FILE_SYSTEM_NAME}
    stdin_open: true
    tty: true
```

Start an interactive container with:

```bash
docker compose run --rm agent
```

`fuse3` provides `/usr/bin/fusermount3`. If mounting reports `fusermount3: mount failed: Permission denied`, confirm that the host has `/dev/fuse` and that all required `devices`, `cap_add`, and AppArmor settings reached the container. `apparmor=unconfined` applies to AppArmor-enabled hosts such as Ubuntu and can be omitted where AppArmor is not active.

> **Warning:**
>
> `SYS_ADMIN` and an unconfined AppArmor profile weaken container isolation. Use them only for a dedicated, trusted agent container. Rootless Docker and managed container platforms might prohibit these settings; use tdc fs data-plane commands without a mount when FUSE cannot be granted. The mount exists in the container mount namespace and disappears when the container stops, so wait for graceful unmount to succeed before stopping a container that might have pending writes.

macOS intentionally keeps WebDAV as the automatic choice even when macFUSE is installed. To use FUSE, install a supported release from the [official macFUSE site](https://macfuse.github.io/), complete any approval or restart requested by its installer, and run:

```bash
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace \
  --driver fuse
```

Explicit FUSE supports cache controls:

```bash
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /path/to/workspace \
  --driver fuse \
  --cache-dir "$HOME/.tdc/cache/workspace" \
  --read-cache-size-mb 256 \
  --read-cache-max-file-mb 16 \
  --read-cache-ttl 30s
```

### Ubuntu 26.04 mount paths

Ubuntu 26.04 enforces an AppArmor profile for `/usr/bin/fusermount3`. The default profile allows FUSE mounts under the current user's home directory, `/mnt`, `/media`, `/tmp`, and `/run/user/<uid>`, but not directly under `/workspace`. This restriction applies to root as well as non-root users and produces an error similar to `/usr/bin/fusermount3: mount failed: Permission denied`.

Prefer an allowed mount path:

```bash
mkdir -p "$HOME/workspace"
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path "$HOME/workspace"
```

For a system-level path, `/mnt/workspace` is allowed by the default profile:

```bash
sudo mkdir -p /mnt/workspace
sudo chown "$(id -u):$(id -g)" /mnt/workspace
tdc fs mount-file-system \
  --file-system-name workspace \
  --mount-path /mnt/workspace
```

If an application requires `/workspace`, add the following rules to `/etc/apparmor.d/local/fusermount3`, and then reload the profile with `sudo apparmor_parser -r /etc/apparmor.d/fusermount3`:

```text
mount fstype=@{fuse_types} options=(nosuid,nodev) options in (ro,rw,noatime,dirsync,nodiratime,noexec,sync) -> /workspace/{,**/},
umount /workspace/{,**/},
```

The default mount profile is `coding-agent`, which keeps common development state such as dependencies, caches, generated output, and Git internals in a local overlay. Those local-only files do not survive machine deletion unless you pack or preserve the local volume. Use `--mount-profile portable` when you want automatic portable pack behavior, or `none` when you do not want the coding-agent overlay policy.

## Drain and unmount

Stop writers and close open files before cleanup. A normal unmount performs a graceful shutdown: the companion flushes open handles and pending FUSE write-back work, waits for its upload queues, and then exits. You do not need to run drain first:

```bash
tdc fs unmount-file-system \
  --mount-path /path/to/workspace
```

Use drain when you need an explicit durability barrier while keeping a FUSE mount online, for example before handing the mount to another process or checking remote visibility:

```bash
tdc fs drain-file-system \
  --mount-path /path/to/workspace \
  --timeout 30s
```

Drain flushes dirty handles and waits for pending writes, but the mount remains available and can accept new writes afterward. It is not supported for WebDAV. `unmount-file-system` also supports `--timeout`, `--force`, `--ignore-absent`, `--pack-archive-path`, and `--no-auto-pack`.

A successful background mount writes a non-secret locator under `~/.tdc/mounts/`. Drain and unmount can use that locator from the same `HOME` without `TDC_FS_TOKEN` or `TDC_REGION_CODE`.

> **Warning:**
>
> Do not terminate a sandbox or virtual machine while writes remain pending or after unmount returns a timeout or error. Remote-committed data survives, but in-memory writes, write-back data on a deleted local disk, and coding-agent local-only files can be lost.

## Unix-style aliases

Aliases change only the command name. All flags remain long and identical to the canonical command.

| Alias | Canonical command |
| --- | --- |
| `tdc fs cp` | `tdc fs copy-file` |
| `tdc fs cat` | `tdc fs read-file` |
| `tdc fs ls` | `tdc fs list-files` |
| `tdc fs stat` | `tdc fs describe-file` |
| `tdc fs mv` | `tdc fs move-file` |
| `tdc fs rm` | `tdc fs delete-file` |
| `tdc fs mkdir` | `tdc fs create-directory` |
| `tdc fs chmod` | `tdc fs chmod-file` |
| `tdc fs symlink` | `tdc fs create-symlink` |
| `tdc fs hardlink` | `tdc fs create-hardlink` |
| `tdc fs grep` | `tdc fs search-file-content` |
| `tdc fs find` | `tdc fs find-files` |
| `tdc fs mount` | `tdc fs mount-file-system` |
| `tdc fs drain` | `tdc fs drain-file-system` |
| `tdc fs umount` | `tdc fs unmount-file-system` |

## Command summary

| Area | Commands |
| --- | --- |
| Resources | `create-file-system`, `list-file-systems`, `describe-file-system`, `set-default-file-system`, `unset-default-file-system`, `check-file-system`, `delete-file-system` |
| Data | `copy-file`, `read-file`, `list-files`, `describe-file`, `move-file`, `delete-file`, `create-directory`, `chmod-file`, `create-symlink`, `create-hardlink`, `search-file-content`, `find-files` |
| Layers | `create-layer`, `list-layers`, `describe-layer`, `diff-layer`, `create-layer-checkpoint`, `rollback-layer`, `commit-layer` |
| Portability | `pack-file-system`, `unpack-file-system` |
| Mounts | `mount-file-system`, `drain-file-system`, `unmount-file-system` |

## What's next

- [Use a Filesystem in an Agent Sandbox](/ai/tdc/examples/tdc-agent-sandbox-example.md)
- [Share a Filesystem Across Machines](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)
- [Use Git Workspaces on TiDB Cloud Filesystem](/ai/tdc/guides/tdc-filesystem-git.md)

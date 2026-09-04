---
title: TiDB Cloud Filesystem CLI Command Reference
summary: Reference every `ti fs` command for Filesystem resources, files, layers, packs, and mounts.
---

# TiDB Cloud Filesystem CLI Command Reference

Use `ti fs` to provision TiDB Cloud Filesystem resources and access their data from commands or local mounts.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## Command tree

```text
ti fs
├── create-file-system
├── import-file-system-token
├── generate-file-system-token
├── generate-file-system-scoped-token
├── list-file-system-tokens
├── enable-file-system-token
├── disable-file-system-token
├── delete-file-system-token
├── refresh-file-system-token
├── list-file-systems
├── describe-file-system
├── describe-file-system-extract-configuration
├── update-file-system-extract-configuration
├── describe-file-system-embedding-configuration
├── update-file-system-embedding-configuration
├── check-file-system
├── delete-file-system
├── copy-file
├── read-file
├── list-files
├── describe-file
├── move-file
├── delete-file
├── create-directory
├── chmod-file
├── create-symlink
├── create-hardlink
├── search-file-content
├── find-files
├── create-layer
├── list-layers
├── fork-layer
├── list-layer-chain
├── describe-layer
├── diff-layer
├── create-layer-checkpoint
├── delete-layer
├── rollback-layer
├── commit-layer
├── pack-file-system
├── unpack-file-system
├── mount-file-system
├── drain-file-system
└── unmount-file-system
```

## Command details

### Resource commands

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `create-file-system` | Provisions a Filesystem with a server-assigned ID and optional display metadata; `--wait` waits until data-plane access is ready. | `ti fs create-file-system --display-name agent-workspace --wait` |
| `import-file-system-token` | Validates and stores an existing token under its embedded file system ID. | `ti fs import-file-system-token --from-file ./fs-token --region aws-us-east-1` |
| `generate-file-system-token` | Uses TiDB Cloud API credentials to generate an additional owner token and returns its plaintext once. | `ti fs generate-file-system-token --file-system-id <file-system-id> --token-name ci --ttl 24h` |
| `generate-file-system-scoped-token` | Uses an owner token to generate a finite path-and-operation-limited token. | `ti fs generate-file-system-scoped-token --ttl 24h --allow /workspace:read,list` |
| `list-file-system-tokens` | Lists non-secret token metadata for one Filesystem. | `ti fs list-file-system-tokens --file-system-id <file-system-id>` |
| `enable-file-system-token` | Re-enables a disabled token by immutable token ID. | `ti fs enable-file-system-token --file-system-id <file-system-id> --token-id <token-id>` |
| `disable-file-system-token` | Temporarily disables a token by immutable token ID. | `ti fs disable-file-system-token --file-system-id <file-system-id> --token-id <token-id>` |
| `delete-file-system-token` | Permanently revokes a token by immutable token ID. | `ti fs delete-file-system-token --file-system-id <file-system-id> --token-id <token-id>` |
| `refresh-file-system-token` | Rotates the supplied token and returns its replacement plaintext once. | `ti fs refresh-file-system-token --file-system-id <file-system-id>` |
| `list-file-systems` | Lists authoritative remote metadata and quota information, optionally filtered by display-name substring and one exact label. | `ti fs list-file-systems --output text` |
| `describe-file-system` | Reads authoritative remote metadata and quota information by ID without requiring its FS token. | `ti fs describe-file-system --file-system-id <file-system-id>` |
| `describe-file-system-extract-configuration` | Reads effective image, audio, or video extraction configuration by Filesystem ID. | `ti fs describe-file-system-extract-configuration --file-system-id <file-system-id> --media-type image` |
| `update-file-system-extract-configuration` | Enables, updates, or disables optional media extraction configuration. | `ti fs update-file-system-extract-configuration --file-system-id <file-system-id> --media-type image --enabled false` |
| `describe-file-system-embedding-configuration` | Reads effective app-managed or database-managed embedding configuration. | `ti fs describe-file-system-embedding-configuration --file-system-id <file-system-id>` |
| `update-file-system-embedding-configuration` | Enables or disables optional app-managed embedding configuration. | `ti fs update-file-system-embedding-configuration --file-system-id <file-system-id> --enabled false` |
| `check-file-system` | Verifies resource selection, endpoint resolution, credentials, and companion access. | `ti fs check-file-system --file-system-id <file-system-id>` |
| `delete-file-system` | Uses TiDB Cloud API credentials to request asynchronous deletion by explicit ID and removes a matching local credential after acceptance. | `ti fs delete-file-system --file-system-id <file-system-id>` |

### Data and namespace commands

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `copy-file` | Uploads, downloads, streams, appends, resumes, or recursively copies local and remote paths. | `ti fs copy-file --from-local ./report.md --to-remote /reports/report.md` |
| `read-file` | Writes a complete file or byte range to stdout. | `ti fs read-file --path /reports/report.md --offset 0 --length 1024` |
| `list-files` | Lists entries under a remote path. | `ti fs list-files --path /reports --output text` |
| `describe-file` | Returns metadata for one remote path. | `ti fs describe-file --path /reports/report.md` |
| `move-file` | Moves or renames one remote path. | `ti fs move-file --from-remote /draft.md --to-remote /reports/final.md` |
| `delete-file` | Deletes one remote path; `--recursive` is required for non-empty directories. | `ti fs delete-file --path /scratch --recursive` |
| `create-directory` | Creates a remote directory and optionally sets its mode. | `ti fs create-directory --path /reports/archive --mode 0755` |
| `chmod-file` | Changes remote POSIX mode metadata. | `ti fs chmod-file --path /reports/final.md --mode 0600` |
| `create-symlink` | Creates a symbolic link with a target string and link path. | `ti fs create-symlink --target final.md --link-path /reports/latest.md` |
| `create-hardlink` | Creates a hard link from an existing remote path. | `ti fs create-hardlink --source-path /reports/final.md --link-path /reports/final-copy.md` |
| `search-file-content` | Searches file contents below a path, optionally within a layer. | `ti fs search-file-content --path /reports --pattern "TODO"` |
| `find-files` | Finds paths by name, type, tags, size, or timestamps. | `ti fs find-files --path /reports --file-name-pattern "*.md" --tag stage=review` |

### Layer and portability commands

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `create-layer` | Creates an isolated change layer over `--base-root-path`; returns a generated layer ID when one is not supplied. | `ti fs create-layer --base-root-path /workspace --layer-name task` |
| `list-layers` | Lists layers for the selected Filesystem. | `ti fs list-layers --output text` |
| `fork-layer` | Forks a copy-on-write child from a parent tip or checkpoint. | `ti fs fork-layer --parent-layer-ref research-base --layer-name experiment --checkpoint-id seed` |
| `list-layer-chain` | Lists pinned ancestry from the root layer to a selected child. | `ti fs list-layer-chain --layer-ref experiment --output text` |
| `describe-layer` | Reads one layer by ID. | `ti fs describe-layer --layer-id "<layer-id>"` |
| `diff-layer` | Lists changes recorded in one layer. | `ti fs diff-layer --layer-id "<layer-id>"` |
| `create-layer-checkpoint` | Records a named checkpoint for a layer. | `ti fs create-layer-checkpoint --layer-id "<layer-id>" --checkpoint-id before-review` |
| `delete-layer` | Logically abandons a leaf layer, or explicitly abandons its descendants with `--cascade`. | `ti fs delete-layer --layer-ref experiment` |
| `rollback-layer` | Restores a layer to its rollback state without committing it to the base. | `ti fs rollback-layer --layer-id "<layer-id>"` |
| `commit-layer` | Applies a layer's changes to the base Filesystem. | `ti fs commit-layer --layer-id "<layer-id>"` |
| `pack-file-system` | Stores selected local overlay state in a remote archive. | `ti fs pack-file-system --mount-path /path/to/workspace` |
| `unpack-file-system` | Restores local overlay state from a remote archive. | `ti fs unpack-file-system --mount-path /path/to/workspace` |

### Mount commands

| Command | Purpose and key inputs | Example |
| --- | --- | --- |
| `mount-file-system` | Mounts a flat Filesystem, writable layer, or read-only checkpoint. Layer views require FUSE. | `ti fs mount-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace --driver fuse --layer-ref experiment` |
| `drain-file-system` | Flushes pending FUSE work while leaving the mount online. | `ti fs drain-file-system --mount-path /path/to/workspace --timeout 30s` |
| `unmount-file-system` | Gracefully flushes and unmounts a background FUSE or WebDAV mount. | `ti fs unmount-file-system --mount-path /path/to/workspace` |

## Prerequisites

- Run `ti configure` before provisioning, listing, describing, or deleting Filesystems.
- Install `ti` with the release installer so the `ti-drive9` companion is next to the `ti` binary.
- Install `jq` to run the JSON extraction examples as written, or use an equivalent JSON processor.
- Treat the returned FS owner token as a secret.

Data-plane commands can instead use an existing Filesystem with only `TI_FS_TOKEN` and `TI_REGION_CODE`, without TiDB Cloud API keys. `TI_FS_FILE_SYSTEM_ID` is an optional assertion.

## Manage Filesystem resources

Create a resource, wait until data-plane access is ready, and save the server-assigned ID and one-time owner token without making the file world-readable:

```bash
umask 077
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait > ./filesystem.json
export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

Without `--wait`, `ti` returns after Drive9 accepts provisioning. With the flag, `ti` waits up to 10 minutes until the root is readable through the public Drive9 data-plane CLI. A failed wait leaves the resource and locally stored credential intact.

The JSON response includes `fs_token` exactly once. Store it in a secret manager, then delete `filesystem.json`. A configured machine can use the locally stored credential by ID without exporting the token. Display names and labels are organization-visible inventory metadata, not resource selectors. Do not store credentials, connection strings, private paths, personal data, or other secrets in labels.

List remote resources in the effective region and describe one by ID:

```bash
ti fs list-file-systems
ti fs describe-file-system --file-system-id <file-system-id>
```

Filter the inventory by a display-name substring and one exact label:

```bash
ti fs list-file-systems \
  --display-name workspace \
  --label environment=development
```

List and describe results include authoritative display metadata, status, region, quota, and usage. The quota object includes storage, file-count, media-extraction, and video-extraction limits and counters when returned by the service. `has_local_token` reports only whether the selected local profile has a matching token; token values are never included.

Select a resource for subsequent commands in the current shell:

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

Check the selected resource and companion:

```bash
ti fs check-file-system --file-system-id <file-system-id>
```

Delete a resource only after removing data you need:

```bash
ti fs delete-file-system \
  --file-system-id <file-system-id>
```

Create and delete support `--dry-run`. Deletion requires TiDB Cloud API keys and an ID, but not a local FS token. Drive9 deletion is asynchronous, so a successfully accepted request reports `status: "deleting"` while `ti` removes only a matching ID-keyed local credential.

## Configure optional AI providers

Filesystem AI provider configuration is optional and independent of ordinary resource, file, search, layer, and mount operations. If you do not configure it, those workflows continue to work normally with the Filesystem service's effective defaults.

The configuration commands require TiDB Cloud API public/private keys and an explicit Filesystem ID. They do not accept an FS owner or scoped token. The provider API key is read only from `TI_FS_AI_PROVIDER_API_KEY`, sent to the Filesystem service for validation and encrypted storage, and never persisted locally by `ti`. Describe responses return only a masked key.

Configure image extraction through an OpenAI provider:

```bash
# Provider validation sends a small built-in image and can incur a provider charge.
TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

Configure Alibaba Cloud Model Studio Qwen ASR for audio:

```bash
# qwen-asr is supported only for audio extraction.
TI_FS_AI_PROVIDER_API_KEY="<dashscope-api-key>" \
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type audio \
  --enabled true \
  --provider-api-base https://dashscope.aliyuncs.com/compatible-mode/v1 \
  --provider-model qwen3-asr-flash \
  --provider-protocol qwen-asr
```

Configure an OpenAI-compatible embedding provider whose model returns exactly 1024 dimensions:

```bash
# The Filesystem service validates the provider before saving the configuration.
TI_FS_AI_PROVIDER_API_KEY="<provider-api-key>" \
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model text-embedding-3-small
```

OpenAI is supported for embedding and image, audio, and video extraction. An API from another vendor is conditionally compatible only when it implements the exact OpenAI request and response contract required by the selected operation. Qwen ASR through Alibaba Cloud Model Studio is additionally supported for audio extraction. Native Anthropic, Gemini, Vertex AI, Bedrock, and Azure OpenAI interfaces are not supported.

After extraction is enabled, Filesystem image, audio, or video content is sent to the configured extraction provider. Text or extracted descriptions are sent to the configured embedding provider. Choose provider accounts and retention policies appropriate for your data. A provider validation request can incur a small charge. If an update times out or loses its response, describe the configuration before retrying because the service might already have validated and saved it.

For complete options and safe update behavior, see the individual [extract configuration](/ai/ti/reference/commands/fs/ti-fs-update-file-system-extract-configuration.md) and [embedding configuration](/ai/ti/reference/commands/fs/ti-fs-update-file-system-embedding-configuration.md) command references.

## Manage Filesystem tokens

One Filesystem can have multiple owner or scoped tokens. The remote service is authoritative for token inventory and lifecycle state. Each local profile stores only one selected operational token per Filesystem; it does not mirror every remote token.

An owner FS token grants Filesystem use and token-management capabilities, but it does not grant TiDB Cloud resource administration. Generating another owner token requires TiDB Cloud API credentials and an explicit Filesystem ID. Listing, enabling, disabling, and deleting tokens can instead use an owner token; in that mode, `ti` derives the Filesystem ID from the token and `--file-system-id` is optional. Creating, listing, describing, and deleting Filesystem resources always require TiDB Cloud API credentials, and Filesystem deletion always requires an explicit `--file-system-id`.

Generate an additional owner token for CI and save its one-time plaintext response securely:

```bash
umask 077
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name ci-deploy \
  --ttl 24h > ./ci-token.json
```

Generation does not change local selection by default. Add `--store-locally` to select the generated token. If another local token exists, `--replace` is also required. Replacing local selection does not disable or revoke the old remote token.

List token metadata and use the immutable token ID for state changes:

```bash
ti fs list-file-system-tokens --file-system-id "<file-system-id>" --output text
ti fs disable-file-system-token --file-system-id "<file-system-id>" --token-id "<token-id>"
ti fs enable-file-system-token --file-system-id "<file-system-id>" --token-id "<token-id>"
ti fs delete-file-system-token --file-system-id "<file-system-id>" --token-id "<token-id>"
```

Token names are not unique. List output never contains token plaintext, and revoked tokens do not appear. Authentication changes can take approximately 10 seconds to converge.

Refresh a selected local token atomically:

```bash
ti fs refresh-file-system-token --file-system-id "<file-system-id>"
```

To refresh a token held by an external secret manager, supply `TI_FS_TOKEN` and `TI_REGION_CODE`. The command returns the replacement plaintext but cannot update the external store. Refresh is non-idempotent: when the request might have committed but the response was lost, do not retry with the old token. Generate another owner token with TiDB Cloud credentials instead.

Before refreshing, disabling, or deleting a token used by a known local mount, drain and unmount it:

```bash
ti fs drain-file-system --mount-path /path/to/workspace
ti fs unmount-file-system --mount-path /path/to/workspace
```

Older credentials created or imported before token lifecycle metadata was available can continue to access data, but `ti` cannot correlate them with a remote token row. It never guesses a token ID from name, timestamp, or list order.

## Select one of multiple Filesystems

One profile can own multiple resources. Selection precedence is:

1. `--file-system-id`;
2. `TI_FS_FILE_SYSTEM_ID`;
3. the ID embedded in an explicitly supplied FS token;
4. otherwise fail with `fs.missing_file_system_id`.

`ti` does not infer a resource from local credential count, even when only one credential exists. This makes scripts deterministic when resources are added or removed.

## Copy and read data

Upload, download, and copy remotely:

```bash
ti fs copy-file --from-local ./README.md --to-remote /workspace/README.md
ti fs copy-file --from-remote /workspace/README.md --to-local ./README.copy.md --create-parents
ti fs copy-file --from-remote /workspace/README.md --to-remote /archive/README.md
```

Use `--overwrite` to replace an existing target, `--resume` for a supported interrupted upload or download, and `--recursive` for directories:

```bash
ti fs copy-file --from-local ./src --to-remote /workspace/src --recursive
ti fs copy-file --from-local ./large.bin --to-remote /workspace/large.bin --resume
```

Append and stream:

```bash
ti fs copy-file --from-local ./tail.log --to-remote /logs/app.log --append
printf 'hello\n' | ti fs copy-file --from-stdin --to-remote /workspace/stdin.txt
ti fs copy-file --from-remote /workspace/stdin.txt --to-stdout
```

Add metadata during upload:

```bash
ti fs copy-file \
  --from-local ./report.md \
  --to-remote /workspace/report.md \
  --tag owner=agent \
  --tag stage=review \
  --description "agent review report"
```

Read a complete file or a byte range:

```bash
ti fs read-file --path /workspace/report.md
ti fs read-file --path /workspace/large.bin --offset 1024 --length 4096
```

## Inspect and modify the namespace

```bash
ti fs list-files --path /workspace
ti fs describe-file --path /workspace/report.md
ti fs create-directory --path /workspace/archive --mode 0755
ti fs move-file --from-remote /workspace/report.md --to-remote /workspace/archive/report.md
ti fs chmod-file --path /workspace/archive/report.md --mode 0600
ti fs create-symlink --target archive/report.md --link-path /workspace/report.link
ti fs create-hardlink --source-path /workspace/archive/report.md --link-path /workspace/report.hard
ti fs delete-file --path /workspace/report.link
ti fs delete-file --path /workspace/archive --recursive
```

Mutating namespace commands support `--dry-run`.

Search content and metadata:

```bash
ti fs search-file-content --path /workspace --pattern "TODO" --limit 50
ti fs find-files --path /workspace --file-name-pattern "*.md" --tag stage=review
```

`find-files` also supports resource type, time, size, and result-limit filters. Both search commands accept `--layer-id`.

## Use layers and checkpoints

A layer records changes over a base root before you commit or discard them. Use `copy-file --layer-id` for individual files. Recursive copy and `--layer-id` are mutually exclusive; seed a directory tree through a writable FUSE layer mount instead.

```bash
ti fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

Use the returned layer ID for individual file writes and inspection:

```bash
ti fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

ti fs list-layers
ti fs describe-layer --layer-id "<layer-id>"
ti fs diff-layer --layer-id "<layer-id>"
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"
```

Fork independent copy-on-write timelines from the checkpoint, inspect their ancestry, and mount a child through FUSE:

```bash
ti fs fork-layer \
  --parent-layer-ref "<layer-id>" \
  --layer-name experiment \
  --checkpoint-id seed

ti fs list-layer-chain --layer-ref experiment
ti fs mount-file-system \
  --file-system-id <file-system-id> \
  --mount-path /path/to/experiment \
  --remote-path /workspace \
  --driver fuse \
  --layer-ref experiment
```

Drain and unmount a writable layer before creating a checkpoint, rolling it back, or committing it. Finish the layer by rolling it back or committing it:

```bash
ti fs rollback-layer --layer-id "<layer-id>"
ti fs commit-layer --layer-id "<layer-id>"
```

These two commands represent alternative outcomes for the same work; do not run both in sequence in a real workflow.

## Pack local overlay state

FUSE mount profiles can route selected paths to local overlay storage. Pack those paths to a remote archive before moving to another machine:

```bash
ti fs pack-file-system --mount-path /path/to/workspace
ti fs unpack-file-system --mount-path /path/to/workspace
```

Without an active mount, provide `--local-root`, `--remote-root`, and `--mount-profile`. `--archive-path` selects the remote archive, repeatable `--path` limits pack contents, and `--no-replace` makes unpack merge rather than replace manifest paths.

## Mount a Filesystem

Create the local mount path and mount in the background:

```bash
mkdir -p /path/to/workspace
ti fs mount-file-system \
  --file-system-id <file-system-id> \
  --mount-path /path/to/workspace
```

The default `--driver auto` is platform-specific. `--remote-path` exposes a subtree, and `--read-only` prevents writes. The command starts the mount runtime in the background, waits until it is ready, and then returns. Use `ti fs unmount-file-system` to end the mount.

### Platform behavior

| Platform | `--driver auto` | Optional or required dependency | Notes |
| --- | --- | --- | --- |
| macOS | WebDAV | No extra dependency for WebDAV | Install macFUSE and select `--driver fuse` for the complete FUSE experience |
| Linux | FUSE | FUSE3 and access to `/dev/fuse`; install `davfs2` for explicit WebDAV | FUSE supports drain and FUSE cache controls |
| Windows | WebDAV | Windows WebClient service | Mount path must be a drive letter such as `X:`; FUSE and vault mount are unavailable |

### Mount in Docker and Docker Compose

Installing FUSE3 inside an image does not enable mounts by itself. The Docker host must provide `/dev/fuse`, and the container must receive permission to perform the mount. The following Dockerfile installs the required Ubuntu package and `ti` without storing any cloud or Filesystem credentials in the image:

```dockerfile
FROM ubuntu:24.04

ARG TI_VERSION=latest

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl fuse3 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh \
    | sh -s -- --yes --version "${TI_VERSION}"

ENV PATH="/root/.ti/bin:${PATH}"

RUN mkdir -p /workspace

CMD ["bash"]
```

Build the image, then pass the Filesystem owner token and canonical region code at runtime:

```bash
docker build -t ti-fuse .

docker run --rm -it \
  --device /dev/fuse \
  --cap-add SYS_ADMIN \
  --security-opt apparmor=unconfined \
  --env TI_FS_TOKEN \
  --env TI_REGION_CODE \
  ti-fuse
```

The two environment variables must already exist in the host shell. Inside the container, mount and use the Filesystem normally:

```bash
ti fs mount --mount-path /workspace
printf 'hello from Docker\n' > /workspace/hello.txt
ti fs umount --mount-path /workspace
```

Use the equivalent runtime settings in `compose.yaml`:

```yaml
services:
  agent:
    build:
      context: .
      args:
        TI_VERSION: latest
    devices:
      - /dev/fuse:/dev/fuse
    cap_add:
      - SYS_ADMIN
    security_opt:
      - apparmor=unconfined
    environment:
      TI_FS_TOKEN: ${TI_FS_TOKEN}
      TI_REGION_CODE: ${TI_REGION_CODE}
      TI_FS_FILE_SYSTEM_ID: ${TI_FS_FILE_SYSTEM_ID}
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
> `SYS_ADMIN` and an unconfined AppArmor profile weaken container isolation. Use them only for a dedicated, trusted agent container. Rootless Docker and managed container platforms might prohibit these settings; use `ti fs` data-plane commands without a mount when FUSE cannot be granted. The mount exists in the container mount namespace and disappears when the container stops, so wait for graceful unmount to succeed before stopping a container that might have pending writes.

macOS intentionally keeps WebDAV as the automatic choice even when macFUSE is installed. To use FUSE, install a supported release from the [official macFUSE site](https://macfuse.github.io/), complete any approval or restart requested by its installer, and run:

```bash
ti fs mount-file-system \
  --file-system-id <file-system-id> \
  --mount-path /path/to/workspace \
  --driver fuse
```

Explicit FUSE supports cache controls:

```bash
ti fs mount-file-system \
  --file-system-id <file-system-id> \
  --mount-path /path/to/workspace \
  --driver fuse \
  --cache-dir "$HOME/.ti/cache/workspace" \
  --read-cache-size-mb 256 \
  --read-cache-max-file-mb 16 \
  --read-cache-ttl 30s
```

### Ubuntu 26.04 mount paths

Ubuntu 26.04 enforces an AppArmor profile for `/usr/bin/fusermount3`. The default profile allows FUSE mounts under the current user's home directory, `/mnt`, `/media`, `/tmp`, and `/run/user/<uid>`, but not directly under `/workspace`. This restriction applies to root as well as non-root users and produces an error similar to `/usr/bin/fusermount3: mount failed: Permission denied`.

Prefer an allowed mount path:

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system \
  --file-system-id <file-system-id> \
  --mount-path "$HOME/workspace"
```

For a system-level path, `/mnt/workspace` is allowed by the default profile:

```bash
sudo mkdir -p /mnt/workspace
sudo chown "$(id -u):$(id -g)" /mnt/workspace
ti fs mount-file-system \
  --file-system-id <file-system-id> \
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
ti fs unmount-file-system \
  --mount-path /path/to/workspace
```

Use drain when you need an explicit durability barrier while keeping a FUSE mount online, for example before handing the mount to another process or checking remote visibility:

```bash
ti fs drain-file-system \
  --mount-path /path/to/workspace \
  --timeout 30s
```

Drain flushes dirty handles and waits for pending writes, but the mount remains available and can accept new writes afterward. It is not supported for WebDAV. `unmount-file-system` also supports `--timeout`, `--force`, `--ignore-absent`, `--pack-archive-path`, and `--no-auto-pack`.

A successful background mount writes a non-secret locator under `~/.ti/mounts/`. Drain and unmount can use that locator from the same `HOME` without `TI_FS_TOKEN` or `TI_REGION_CODE`.

> **Warning:**
>
> Do not terminate a sandbox or virtual machine while writes remain pending or after unmount returns a timeout or error. Remote-committed data survives, but in-memory writes, write-back data on a deleted local disk, and coding-agent local-only files can be lost.

## Unix-style aliases

Aliases change only the command name. All flags remain long and identical to the canonical command.

| Alias | Canonical command |
| --- | --- |
| `ti fs cp` | `ti fs copy-file` |
| `ti fs cat` | `ti fs read-file` |
| `ti fs ls` | `ti fs list-files` |
| `ti fs stat` | `ti fs describe-file` |
| `ti fs mv` | `ti fs move-file` |
| `ti fs rm` | `ti fs delete-file` |
| `ti fs mkdir` | `ti fs create-directory` |
| `ti fs chmod` | `ti fs chmod-file` |
| `ti fs symlink` | `ti fs create-symlink` |
| `ti fs hardlink` | `ti fs create-hardlink` |
| `ti fs grep` | `ti fs search-file-content` |
| `ti fs find` | `ti fs find-files` |
| `ti fs mount` | `ti fs mount-file-system` |
| `ti fs drain` | `ti fs drain-file-system` |
| `ti fs umount` | `ti fs unmount-file-system` |

## What's next

- [Use a Filesystem in an Agent Sandbox](/ai/ti/reference/ti-agent-sandbox-example.md)
- [Share a Filesystem Across Machines](/ai/ti/reference/ti-share-filesystem-across-machines-example.md)
- [TiDB Cloud Filesystem Git CLI Command Reference](/ai/ti/reference/ti-filesystem-git.md)

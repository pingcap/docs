---
title: TiDB Cloud Filesystem Regions and Limitations
summary: Review supported TiDB Cloud Filesystem regions, mount platform requirements, durability boundaries, and current product limitations.
---

# TiDB Cloud Filesystem Regions and Limitations

TiDB Cloud Filesystem is available only in the regions and environments listed below. Check these boundaries before creating a file system or choosing how to access its data.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## Supported regions

| Provider | Location | Canonical region code |
| --- | --- | --- |
| AWS | N. Virginia | `aws-us-east-1` |
| AWS | Oregon | `aws-us-west-2` |
| AWS | Singapore | `aws-ap-southeast-1` |
| Alibaba Cloud | Singapore | `alicloud-ap-southeast-1` |

TiDB Cloud Starter also supports some regions where TiDB Cloud Filesystem is not available. File system commands in those regions fail with an `unsupported endpoint` error. Supported file system regions are built into each `ti` release. If a region was added after your installed version was released, upgrade `ti`; specifying a service URL cannot enable it.

The `list` and `describe` file system commands query only the selected region. They do not aggregate resources across regions. For CLI-wide region selection and Starter availability, see [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions).

## Mount platform support

| Platform | File system mount | Vault mount | Requirements and alternatives |
| --- | --- | --- | --- |
| macOS | WebDAV without macFUSE; FUSE when macFUSE is installed (automatic or explicit) | FUSE | The built-in WebDAV helper supports file system mounts. Install macFUSE and approve its system extension for FUSE or Vault mounts. |
| Linux | FUSE | FUSE | Install the `fuse3` package and provide access to `/dev/fuse`. WebDAV mounting is not supported. |
| Windows | Not supported | Not supported | Use `ti fs` data-plane commands and non-mount Vault commands instead. |

FUSE and WebDAV are implemented by the bundled file system runtime component. The CLI does not fall back to a separate native mount implementation. A running mount keeps the runtime version loaded when it started; unmount and remount after updating `ti`.

Ubuntu 26.04 also confines `fusermount3` with AppArmor. Use a mount path under `$HOME` or `/mnt`; `/workspace` requires an explicit local AppArmor rule even when `ti` runs as root. For setup and workarounds, see [Mount a File System on Linux](/tidb-cloud-filesystem/filesystem-mount-linux.md#ubuntu-2604-mount-path-restrictions).

## Durability boundaries

- Default FUSE behavior uses local buffering and asynchronous remote work where the companion permits it. Abruptly killing the mount process or deleting a machine can lose uncommitted memory or write-back state.
- When you select the `coding-agent` mount profile with `--mount-profile coding-agent`, dependency trees, generated output, caches, and Git internals are stored locally. Local-only data disappears when its disk disappears unless it is packed or otherwise preserved.
- Remote-committed file system data survives client or sandbox deletion; deleting the machine does not delete the remote file system.

For the supported drain and graceful unmount workflow, see [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely). `drain-file-system` is a FUSE-only online durability barrier; WebDAV does not support it.

## Current limitations

- Journals are append-only, and the current public command surface has no journal delete command.
- The local credential store keeps one selected token per profile and file system. It does not mirror all remote tokens. Older create or import credentials without a known token ID remain usable, but cannot be correlated with remote token metadata.
- File system extraction and embedding provider configuration is optional. Leaving it unconfigured does not block resource administration, file access, search, layers, Git, journal, vault, or mount workflows.
- OpenAI provider interfaces are supported for embedding and image, audio, and video extraction. Alibaba Cloud Model Studio Qwen ASR is supported only for audio extraction. Other vendors are conditionally compatible only through the exact OpenAI-compatible contract; native Anthropic, Gemini, Vertex AI, Bedrock, and Azure OpenAI interfaces are not supported.
- App-managed embedding requires a provider model that returns exactly 1024 dimensions. File systems that report `source=database_auto` use database-managed embedding and reject app-managed configuration. For configuration steps, see [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md).
- File system runtime operations, including direct file access, layers, mounts, Git workspaces, journals, and Vault operations, depend on the bundled file system runtime component installed with `ti`.

For token or mount failures, see [Troubleshoot TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md). For command syntax and options, see the [TiDB Cloud Filesystem CLI command reference](/ai/ti/reference/ti-filesystem.md).

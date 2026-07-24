---
title: tdc Regions, Security, and Limitations
summary: Reference supported regions, authentication boundaries, platform dependencies, Preview constraints, and Filesystem companion behavior.
---

# tdc Regions, Security, and Limitations

This reference describes current placement, authentication, platform, and Preview boundaries.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## TiDB Cloud regions

tdc accepts one canonical region code:

| Canonical code | Provider | Location |
| --- | --- | --- |
| `aws-us-east-1` | AWS | N. Virginia |
| `aws-us-west-2` | AWS | Oregon |
| `aws-eu-central-1` | AWS | Frankfurt |
| `aws-ap-northeast-1` | AWS | Tokyo |
| `aws-ap-southeast-1` | AWS | Singapore |
| `ali-ap-southeast-1` | Alibaba Cloud | Singapore |

Alibaba Cloud currently supports only Singapore in tdc. Users cannot configure raw service URLs.

## Filesystem regions

Filesystem endpoint availability is resolved from the hosted Drive9 region manifest. At publication time, TiDB Cloud native Filesystem mode is available in:

| Cloud provider | Canonical region code |
| --- | --- |
| AWS | `aws-ap-southeast-1` |
| AWS | `aws-us-east-1` |
| AWS | `aws-us-west-2` |
| Alibaba Cloud | `ali-ap-southeast-1` |

The hosted manifest is authoritative and can change during Preview. A profile in another TiDB Cloud region can manage Starter databases but receives an unsupported Filesystem endpoint error until that placement appears in the manifest.

## Credential requirements

| Operation | Required credential |
| --- | --- |
| `tdc configure`, `tdc organization`, all `tdc db` control-plane operations | TiDB Cloud API public/private key |
| `tdc fs create-file-system` | TiDB Cloud API key |
| `tdc fs delete-file-system` | TiDB Cloud API key, local resource registration, and owner resource credential |
| Remote file, layer, pack, mount, Git, journal, and owner vault operations | FS owner token or registered resource credential |
| Delegated vault read, list, run, or mount | Scope-appropriate delegated vault token |
| Drain and unmount after a successful background mount | Non-secret mount locator in the same `HOME` |

TiDB Cloud API calls use Digest authentication. SQL HTTPS execution uses generated SQL username/password Basic authentication over TLS. These credentials are not interchangeable.

## Security best practices

- Create TiDB Cloud API keys with only the organization and project access required for the workflow. Do not reuse a personal administrator key in unattended automation.
- Inject automation credentials from a CI secret store or runtime secret manager. Do not place credentials in source control, container images, shell scripts, or command-line arguments that can appear in process listings and shell history.
- Do not copy the complete `~/.tdc/` directory into an agent sandbox. For an existing Filesystem, pass only `TDC_FS_TOKEN`, `TDC_REGION_CODE`, and `TDC_FS_FILE_SYSTEM_NAME`.
- Treat an FS owner token as full access to that Filesystem. When an agent needs only selected secrets, create a vault grant with the narrowest field scope and shortest practical TTL, and pass the delegated vault token instead.
- Use `--read-only` for SQL inspection by untrusted or exploratory agents. Use `--admin` only for DDL or privilege management, and use `--read-write` only when data changes are intended.
- Use `--dry-run` before destructive control-plane operations. Keep `~/.tdc/credentials`, resource credentials, and DB SQL credentials owner-readable only.
- Grant Docker access to `/dev/fuse`, `SYS_ADMIN`, and an unconfined AppArmor profile only to dedicated, trusted containers. These settings reduce container isolation.
- Review local operation logs before sharing diagnostics. tdc redacts known secret classes, but SQL text, resource names, paths, and operational context can still be sensitive.

## Mount platform limitations

| Platform | Default | Limitations |
| --- | --- | --- |
| macOS | WebDAV | Install macFUSE and explicitly use `--driver fuse` for FUSE caches, drain, and complete POSIX-oriented behavior |
| Linux | FUSE | Requires FUSE3 and `/dev/fuse`; explicit WebDAV requires `davfs2` |
| Windows | WebDAV | Requires the WebClient service and a drive-letter mount path; FUSE and vault mount are unavailable |

FUSE and WebDAV are implemented by the bundled [Drive9](https://github.com/mem9-ai/drive9) companion. tdc does not fall back to a separate native mount implementation.

Ubuntu 26.04 additionally confines `fusermount3` with AppArmor. Use a mount path under `$HOME` or `/mnt`; `/workspace` requires an explicit local AppArmor rule even when tdc runs as root.

## Durability limitations

- Default FUSE behavior uses local buffering and asynchronous remote work where permitted by the companion.
- A successful `unmount-file-system` gracefully flushes and drains FUSE work; a separate drain is not required first.
- `drain-file-system` is a FUSE-only online durability barrier that leaves the mount active.
- Abruptly killing the mount process or deleting a machine can lose uncommitted memory/write-back state.
- The default coding-agent mount profile stores dependency trees, generated output, caches, and Git internals locally. Local-only data disappears when its disk disappears unless it is packed or otherwise preserved.
- A running mount remains on the companion version loaded at mount time. Unmount and remount after updating tdc.
- Remote-committed Filesystem data survives client or sandbox deletion; deleting the machine does not delete the remote resource.

## Product limitations

- tdc is Preview and command contracts can change.
- Database management targets TiDB Cloud Starter, not every TiDB Cloud cluster tier.
- SQL execution accepts one statement per invocation.
- Read-write is the default SQL role; use explicit role flags in security-sensitive automation.
- Journals are append-only and the current public command surface has no journal delete command.
- Filesystem resource list and describe commands operate on the local registry; they are not an organization-wide discovery API.
- Telemetry commands, serverless-function deployment, Homebrew, and Scoop distribution are not implemented.
- tdc depends on its installed `tdc-drive9` companion for all public Filesystem runtime behavior.

## Related documentation

- [tdc fs Command Reference](/ai/tdc/reference/tdc-filesystem.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [Troubleshoot tdc](/ai/tdc/reference/tdc-troubleshooting.md)

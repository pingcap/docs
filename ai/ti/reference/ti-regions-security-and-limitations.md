---
title: TiDB Cloud CLI Regions, Security, and Limitations
summary: Reference supported regions, authentication boundaries, platform dependencies, preview constraints, and Filesystem companion behavior.
---

# TiDB Cloud CLI Regions, Security, and Limitations

This reference describes current placement, authentication, platform, and preview boundaries.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## TiDB Cloud regions

The TiDB Cloud CLI accepts one canonical region code:

| Canonical code | Provider | Location |
| --- | --- | --- |
| `aws-us-east-1` | AWS | N. Virginia |
| `aws-us-west-2` | AWS | Oregon |
| `aws-eu-central-1` | AWS | Frankfurt |
| `aws-ap-northeast-1` | AWS | Tokyo |
| `aws-ap-southeast-1` | AWS | Singapore |
| `alicloud-ap-southeast-1` | Alibaba Cloud | Singapore |

Alibaba Cloud currently supports only the Singapore region in the TiDB Cloud CLI. Users cannot configure raw service URLs.

## Filesystem regions

The TiDB Cloud CLI includes endpoint mappings for the following TiDB Cloud Filesystem regions:

| Cloud provider | Canonical region code |
| --- | --- |
| AWS | `aws-ap-southeast-1` |
| AWS | `aws-us-east-1` |
| AWS | `aws-us-west-2` |
| Alibaba Cloud | `alicloud-ap-southeast-1` |

The TiDB Cloud CLI does not download a Drive9 region manifest at runtime. A profile in another TiDB Cloud region can manage Starter databases but receives an unsupported Filesystem endpoint error until that placement is included in a TiDB Cloud CLI release.

## Credential requirements

| Operation | Required credential |
| --- | --- |
| `ti configure`, all `ti db` control-plane operations | TiDB Cloud API public/private key |
| `ti fs create-file-system` | TiDB Cloud API key |
| `ti fs delete-file-system` | TiDB Cloud API key and file system ID |
| Describe or update Filesystem extraction and embedding configuration | TiDB Cloud API key and explicit file system ID |
| Generate, list, enable, disable, or delete Filesystem tokens | TiDB Cloud API key and explicit file system ID |
| Refresh a Filesystem token | The current FS bearer token only |
| Remote file, layer, pack, mount, Git, journal, and owner vault operations | FS owner token or registered resource credential |
| Delegated vault read, list, run, or mount | Scope-appropriate delegated vault token |
| Drain and unmount after a successful background mount | Non-secret mount locator in the same `HOME` |

TiDB Cloud API calls use Digest authentication. SQL HTTPS execution uses generated SQL username/password Basic authentication over TLS. These credentials are not interchangeable.

## Security best practices

- Create TiDB Cloud API keys with only the access required for the workflow. Do not reuse a personal administrator key in unattended automation.
- Inject automation credentials from a CI secret store or runtime secret manager. Do not place credentials in source control, container images, shell scripts, or command-line arguments that can appear in process listings and shell history.
- Do not copy the complete `~/.ti/` directory into an agent sandbox. For an existing Filesystem, pass only `TI_FS_TOKEN` and `TI_REGION_CODE`; use `TI_FS_FILE_SYSTEM_ID` only as an optional assertion.
- Treat an FS owner token as full access to that Filesystem. When an agent needs only selected secrets, create a vault grant with the narrowest field scope and shortest practical TTL, and pass the delegated vault token instead.
- Use a separate Filesystem token for each machine, CI workflow, or sandbox class so that one environment can be disabled or revoked without interrupting others. Token names are operational labels, not unique identifiers; mutate tokens only by `token_id`.
- Capture generated and refreshed token plaintext immediately because it is returned only once. A token refreshed from `TI_FS_TOKEN` is not written back to an external secret manager. Refresh is non-idempotent, so do not retry after an ambiguous network failure.
- For shared-token rotation, generate and distribute a replacement, validate access, then disable and delete the old token. Allow approximately 10 seconds for authentication caches to converge after a state change.
- Pass an AI provider key only through `TI_FS_AI_PROVIDER_API_KEY`. The TiDB Cloud CLI does not persist this value locally, and the Filesystem service returns it only in masked form. Do not retry an AI configuration update after an ambiguous failure until you describe the effective configuration.
- Enabling extraction shares Filesystem media with the configured extraction provider. Enabling app-managed embedding shares text or extracted descriptions with the configured embedding provider. Review that provider's data retention and security terms before enabling either feature.
- Use `--read-only` for SQL inspection by untrusted or exploratory agents. Use `--admin` only for DDL or privilege management, and use `--read-write` only when data changes are intended.
- Use `--dry-run` before destructive control-plane operations. Keep `~/.ti/credentials`, resource credentials, and DB SQL credentials owner-readable only.
- Grant Docker access to `/dev/fuse`, `SYS_ADMIN`, and an unconfined AppArmor profile only to dedicated, trusted containers. These settings reduce container isolation.
- Review local operation logs before sharing diagnostics. The logs exclude SQL text, paths, payloads, and credential values, but command names, flag names, profile and region metadata, status codes, and operational timing can still be sensitive.

## Mount platform limitations

| Platform | Default | Limitations |
| --- | --- | --- |
| macOS | WebDAV | Install macFUSE and explicitly use `--driver fuse` for FUSE caches, drain, and complete POSIX-oriented behavior |
| Linux | FUSE | Requires FUSE3 and `/dev/fuse`; explicit WebDAV requires `davfs2` |
| Windows | WebDAV | Requires the WebClient service and a drive-letter mount path; FUSE and vault mount are unavailable |

FUSE and WebDAV are implemented by the bundled [Drive9](https://github.com/mem9-ai/drive9) companion. The TiDB Cloud CLI does not fall back to a separate native mount implementation.

Ubuntu 26.04 additionally confines `fusermount3` with AppArmor. Use a mount path under `$HOME` or `/mnt`; `/workspace` requires an explicit local AppArmor rule even when `ti` runs as root.

## Durability limitations

- Default FUSE behavior uses local buffering and asynchronous remote work where permitted by the companion.
- A successful `unmount-file-system` gracefully flushes and drains FUSE work; a separate drain is not required first.
- `drain-file-system` is a FUSE-only online durability barrier that leaves the mount active.
- Abruptly killing the mount process or deleting a machine can lose uncommitted memory/write-back state.
- The default coding-agent mount profile stores dependency trees, generated output, caches, and Git internals locally. Local-only data disappears when its disk disappears unless it is packed or otherwise preserved.
- A running mount remains on the companion version loaded at mount time. Unmount and remount after updating the TiDB Cloud CLI.
- Remote-committed Filesystem data survives client or sandbox deletion; deleting the machine does not delete the remote resource.

## Product limitations

- The TiDB Cloud CLI is in preview, and command contracts can change.
- Database management targets TiDB Cloud Starter, not every TiDB Cloud cluster tier.
- SQL execution accepts one statement per invocation.
- Read-write is the default SQL role; use explicit role flags in security-sensitive automation.
- Journals are append-only and the current public command surface has no journal delete command.
- Filesystem list and describe commands query the region-scoped remote inventory with TiDB Cloud credentials. They do not aggregate across regions.
- The local credential store keeps one selected token per profile and Filesystem. It does not mirror all remote tokens. Older create/import credentials without a known token ID remain usable, but cannot be correlated with remote token metadata.
- Filesystem extraction and embedding provider configuration is optional. Leaving it unconfigured does not block resource administration, file access, search, layers, Git, journal, vault, or mount workflows.
- OpenAI provider interfaces are supported for embedding and image, audio, and video extraction. Alibaba Cloud Model Studio Qwen ASR is supported only for audio extraction. Other vendors are conditionally compatible only through the exact OpenAI-compatible contract; native Anthropic, Gemini, Vertex AI, Bedrock, and Azure OpenAI interfaces are not supported.
- App-managed embedding requires a provider model that returns exactly 1024 dimensions. Filesystems that report `source=database_auto` use database-managed embedding and reject app-managed configuration.
- Telemetry management commands are intentionally not implemented. Control telemetry through `~/.ti/.preferences` or `TI_TELEMETRY`; serverless-function deployment, Homebrew, and Scoop distribution are not implemented.
- The TiDB Cloud CLI depends on its installed `ti-drive9` companion for all public Filesystem runtime behavior.

## Related documentation

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)

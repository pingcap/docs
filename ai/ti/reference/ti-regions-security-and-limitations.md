---
title: TiDB Cloud CLI Regions, Security, and Limitations
summary: Reference supported regions, authentication boundaries, security best practices, and current TiDB Cloud CLI limitations.
---

# TiDB Cloud CLI Regions, Security, and Limitations

This reference describes current regions, authentication, platform, and preview boundaries for TiDB Cloud CLI. For Filesystem regions and limitations, see [TiDB Cloud Filesystem Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md).

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## Supported regions

When using TiDB Cloud CLI, you need to configure a default region for CLI operations.

The following table lists the supported regions for TiDB Cloud CLI and shows which TiDB Cloud CLI services are available in each region.

| Provider | Location | Canonical region code | TiDB Cloud Starter | TiDB Cloud Filesystem |
| --- | --- | --- | --- | --- |
| AWS | N. Virginia | `aws-us-east-1` | Supported | Supported |
| AWS | Oregon | `aws-us-west-2` | Supported | Supported |
| AWS | Singapore | `aws-ap-southeast-1` | Supported | Supported |
| AWS | Frankfurt | `aws-eu-central-1` | Supported | Not supported |
| AWS | Tokyo | `aws-ap-northeast-1` | Supported | Not supported |
| Alibaba Cloud | Singapore | `alicloud-ap-southeast-1` | Supported | Supported |

If your configured region supports TiDB Cloud Starter but not TiDB Cloud Filesystem, you can manage Starter instances in that region. Filesystem commands fail with an `unsupported endpoint` error.

Supported Filesystem regions are built into each `ti` release. To use Filesystem in a region added after your installed version was released, upgrade `ti`. You cannot enable an unsupported region by specifying a service URL.

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
- Use `--read-only` for SQL inspection by untrusted or exploratory agents. Use `--admin` only for DDL or privilege management, and use `--read-write` only when data changes are intended.
- Use `--dry-run` before destructive control-plane operations. Keep `~/.ti/credentials`, resource credentials, and DB SQL credentials owner-readable only.
- Review local operation logs before sharing diagnostics. The logs exclude SQL text, paths, payloads, and credential values, but command names, flag names, profile and region metadata, status codes, and operational timing can still be sensitive.

For Filesystem token, mount, Vault, and AI provider security, see [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md), [Manage Filesystem Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md), and [Configure Filesystem AI Providers](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md).

## Product limitations

- The TiDB Cloud CLI is in preview, and command contracts can change.
- Database management targets TiDB Cloud Starter instances, not other TiDB Cloud database plans.
- SQL execution accepts one statement per invocation.
- Read-write is the default SQL role; use explicit role flags in security-sensitive automation.
- Telemetry management commands are intentionally not implemented. Control telemetry through `~/.ti/.preferences` or `TI_TELEMETRY`; serverless-function deployment, Homebrew, and Scoop distribution are not implemented.

## Related documentation

- [TiDB Cloud Filesystem Regions and Limitations](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [Troubleshoot TiDB Cloud CLI](/ai/ti/reference/ti-troubleshooting.md)

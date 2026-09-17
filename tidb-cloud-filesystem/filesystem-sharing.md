---
title: Share a TiDB Cloud Filesystem
summary: Share a remote workspace across machines and sandboxes with separate access tokens, and hand off files after writes reach the service.
---

# Share a TiDB Cloud Filesystem

Sharing a Filesystem gives participants access to the same remote namespace, not independent copies. For example, an agent can produce a report in a sandbox and a reviewer can open that report from a laptop without downloading and redistributing an archive for every revision.

> **Note:**
>
> TiDB Cloud Filesystem is currently in public preview. Its features and interfaces are subject to change without notice.

## What each participant needs

The trusted machine uses TiDB Cloud API keys to create the Filesystem. Other participants need `ti`, an FS token, and the Filesystem region. They do not need a copy of `~/.ti/`, account API keys, or their own Filesystem resource.

Use separate tokens so you can retire one participant's access without changing every participant's credentials. Choose a scoped token for a restricted task; an owner token grants broad Filesystem access. See [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md).

## Prepare the workspace on machine A

With `ti` installed and configured, create a Filesystem or use an existing one. This example creates a new resource:

```bash
# Retain the ID; the creator's token is stored locally by the CLI.
FILE_SYSTEM_ID="$(ti fs create-file-system \
  --display-name shared-reports --wait \
  --query file_system_id --output text)"
```

Create a directory and publish the first report:

```bash
# Write through the direct file interface, without a local mount.
ti fs create-directory --file-system-id "$FILE_SYSTEM_ID" --path /reports
printf 'The first report is ready for review.\n' | ti fs copy-file \
  --file-system-id "$FILE_SYSTEM_ID" \
  --from-stdin --to-remote /reports/summary.txt
```

Issue a read-only token for the reviewer:

```bash
# Keep this value in a secret manager, not in a shared log.
REVIEW_TOKEN="$(ti fs generate-file-system-scoped-token \
  --file-system-id "$FILE_SYSTEM_ID" \
  --subject reviewer --ttl 24h \
  --allow /reports:read,list \
  --query fs_token --output text)"
```

Deliver `REVIEW_TOKEN` and the Filesystem's region code securely to machine B. Retain the Filesystem ID on machine A for administration. The token expires after the requested lifetime; a saved environment variable does not extend it.

## Open the report on machine B

Inject the reviewer's token and matching region into the environment:

```bash
# In production, inject the token from a secret manager instead of pasting it into a shell.
# No ti configure is needed on the receiving machine.
export TI_FS_TOKEN="<reviewer-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs read-file --path /reports/summary.txt
```

On macOS or Linux with the [mount dependencies](/tidb-cloud-filesystem/filesystem-mount.md#choose-your-environment), expose the allowed directory locally:

```bash
# Mount only the scope allowed by the reviewer token.
mkdir -p "$HOME/reports"
ti fs mount-file-system \
  --remote-path /reports \
  --mount-path "$HOME/reports" \
  --read-only
cat "$HOME/reports/summary.txt"
```

The remote `/reports` prefix becomes the local mount root, so the local file is `$HOME/reports/summary.txt`, not `$HOME/reports/reports/summary.txt`.

The token enforces read-only access at the service. `--read-only` also tells the local mount to reject writes; using that flag with an owner token alone would not restrict the owner's other API or CLI access.

## Hand off new data safely

A successful write to a FUSE-mounted file might still be buffered on the producing machine. Before telling the reviewer that a revision is ready, stop the application's writes and drain its FUSE mount, or unmount it successfully. For WebDAV, close application files and finish a normal unmount. See [Finish safely](/tidb-cloud-filesystem/filesystem-mount.md#finish-safely).

Use a direct remote read to verify a handoff independently of another mount's cache. Existing open handles and client caches can retain older content; do not assume every reader instantly sees each local write.

Coordinate writers to the same path. Shared storage is not a distributed lock or an automatic merge system. Use separate paths or [layers](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md) for independent drafts, and publish only after review.

## End access without deleting the workspace

On machine B, stop readers and unmount:

```bash
# Remove the local mount, not the shared remote data.
ti fs unmount-file-system --mount-path "$HOME/reports"
unset TI_FS_TOKEN TI_REGION_CODE
```

On machine A, identify and revoke the reviewer's token when no longer needed:

```bash
# Find the reviewer token ID in the metadata, then revoke that token only.
ti fs list-file-system-tokens --file-system-id "$FILE_SYSTEM_ID" --output text
ti fs delete-file-system-token \
  --file-system-id "$FILE_SYSTEM_ID" --token-id "<reviewer-token-id>"
```

Do not delete the Filesystem to disconnect one participant: resource deletion affects everyone and removes the shared data.

## What's next

- [Understand layers and checkpoints for independent drafts](/tidb-cloud-filesystem/filesystem-layers-checkpoints.md).
- [Run the agent sandbox example](/ai/ti/guides/ti-agent-sandbox-example.md).

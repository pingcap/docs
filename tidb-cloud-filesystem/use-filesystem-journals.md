---
title: Use TiDB Cloud Filesystem Journals
summary: Learn how to create, append, read, search, and verify append-only journals for agent and automation events in a Filesystem.
aliases: ['/ai/use-filesystem-journals']
---

# Use TiDB Cloud Filesystem Journals

Journals provide append-only, hash-chained event logs for agent workflows and automation pipelines running on a TiDB Cloud Filesystem. Use [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) to create a journal, append ordered events, search or read them, and verify the hash chain.

## Prerequisites

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- For the commands below, set `TI_FS_FILE_SYSTEM_ID` to the Filesystem ID and use its locally stored FS token. Alternatively, set `TI_FS_TOKEN` and `TI_REGION_CODE` for token-only access; the token identifies the Filesystem. To select a Filesystem per command instead, add `--file-system-id "<file-system-id>"` to each command. Use a token with journal permissions. See [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md#understand-local-selection) for selection details.

## Create a journal

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

Save the returned journal ID.

## Append entries

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --entry-json '{"type":"review_started"}'
```

For supported input forms and entry fields, see the [`append-journal-entries` reference](/ai/ti/reference/ti-fs-journal-append-journal-entries.md).

## Read and search entries

Read entries in sequence order:

```shell
ti fs-journal read-journal-entries --journal-id "<journal-id>"
```

Search across journals and entries:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --include-entries
```

## Verify a journal

Verify that the journal's hash chain is intact:

```shell
ti fs-journal verify-journal --journal-id "<journal-id>"
```

## What's next

- [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)

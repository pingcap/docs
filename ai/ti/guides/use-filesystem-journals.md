---
title: Use TiDB Cloud Filesystem Journals
summary: Learn how to create, append, read, search, and verify append-only journals for agent and automation events in a Filesystem.
---

# Use TiDB Cloud Filesystem Journals

Journals provide append-only, hash-chained event logs for agent workflows and automation pipelines running on a TiDB Cloud Filesystem. Use [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) to create a journal, append ordered events, search or read them, and verify the hash chain.

## Prerequisites

- [Install and configure TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md).
- Select a Filesystem by passing `--file-system-id`, setting `TI_FS_FILE_SYSTEM_ID`, or supplying an FS token that identifies the Filesystem.
- Provide an FS token with journal permissions through `--fs-token`, `TI_FS_TOKEN`, or the local credential stored for the selected Filesystem.

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

---
title: Use TiDB Cloud Filesystem Journals
summary: Learn how to create, append, read, search, and verify append-only journals for agent and automation events in a Filesystem.
---

# Use TiDB Cloud Filesystem Journals

Use `ti fs-journal` to record ordered workflow events in an append-only journal with a verifiable hash chain.

## Prerequisites

Select a Filesystem through a profile or Filesystem environment variables.

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

For supported input forms and entry fields, see the [`append-journal-entries` reference](/ai/ti/reference/commands/fs-journal/ti-fs-journal-append-journal-entries.md).

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

- [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/reference/ti-journal-agent-workflow-example.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)

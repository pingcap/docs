---
title: Use TiDB Cloud Filesystem Journals
summary: Learn how to create, append, read, search, and verify append-only journals for agent and automation events in a Filesystem.
aliases: ['/ai/use-filesystem-journals']
---

# Use TiDB Cloud Filesystem Journals

Journals provide append-only, hash-chained event logs for agent workflows and automation pipelines running on a TiDB Cloud Filesystem. Use [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) to create a journal, append ordered events, search or read them, and verify the hash chain.

Use a journal when you need to trace the order of agent actions or handoffs across sessions. The hash chain lets you check the integrity and order of recorded entries. A journal records events; it does not replay actions or replace the files produced by a workflow.

## Prerequisites

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-the-cli).
- Have access to an existing TiDB Cloud Filesystem with a token that provides the required journal permissions.
- Select the Filesystem and make its token available to `ti`. For available access options, see [Access an Existing TiDB Cloud Filesystem](/tidb-cloud-filesystem/access-filesystem.md).

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

`--entry-json` accepts a JSON object. Each entry needs a `type`, unless you supply `--entry-type`; optional fields include `summary`, `actor`, and `occurred_at`. For the complete fields and input forms, see the [`append-journal-entries` reference](/ai/ti/reference/ti-fs-journal-append-journal-entries.md).

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

The current public CLI has no journal delete command. Keep retention needs in mind before recording sensitive or high-volume events.

## What's next

- [Record an Agent Workflow in a TiDB Cloud Filesystem Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md)
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)

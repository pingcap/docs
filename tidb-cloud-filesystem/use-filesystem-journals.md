---
title: Use Journals in a File System
summary: Learn how to record, read, search, and verify ordered events from agent and automation workflows in a file system.
aliases: ['/ai/use-filesystem-journals']
---

# Use Journals in a File System

In TiDB Cloud Filesystem, you can use a file system journal when you need an ordered, persistent record of events from an agent or automation workflow. For example, a journal can record when a task starts or finishes, which agent performed an action, and when work is handed off between agents or processes. You can later read or search these events to understand what happened during the workflow.

Journal entries are append-only: new events are added as new entries, and existing entries cannot be modified. The entries are also linked through a hash chain, which lets you verify that the recorded history remains intact and in order.

This guide shows you how to create a journal, record events, read and search recorded events, and verify the journal history.

Journals are intended for workflow events and history. Store artifacts, working files, and other workflow outputs as regular files in the file system. A journal records what happened; it does not replay workflow actions or replace the files produced by the workflow.

> **Note:**
>
> The current `ti` CLI does not provide a command to delete individual journals. Do not record secrets or other data that you might need to remove later.

## Prerequisites

Before you begin:

- [Install TiDB Cloud CLI](/tidb-cloud-filesystem/filesystem-quick-start.md#step-1-install-tidb-cloud-cli).
- Have access to an existing file system in TiDB Cloud Filesystem.
- Make the file system and its token available to `ti`. See [Access an Existing File System](/tidb-cloud-filesystem/access-filesystem.md).

## Create a journal

Create a journal for the workflow you want to record:

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

Because no journal ID is specified, the service generates one. Save the returned journal ID—you will use it to append, read, and verify entries in this journal.

The journal kind, title, and actor provide context that can also help you find related workflow records later.

## Append entries

Append an event to the journal:

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --idempotency-key review-started \
  --entry-json '{"type":"review_started"}'
```

Each entry needs a `type`, unless you provide one with `--entry-type`. You can also include fields such as `summary`, `actor`, and `occurred_at`.

Reuse the same `--idempotency-key` when retrying this event to avoid duplicate entries. Use a new key for a different event.

For all supported fields and input formats, see the [`append-journal-entries` reference](/ai/ti/reference/ti-fs-journal-append-journal-entries.md).

## Read and search entries

### Read one journal

To review the history of one journal, read its entries:

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>"
```

Entries are returned in sequence order, with at most 100 entries per call by default. For the next page, replace `<last-seq>` with the last returned entry's `seq`:

```shell
ti fs-journal read-journal-entries \
  --journal-id "<journal-id>" \
  --after-seq "<last-seq>" \
  --limit 100
```

Continue from each page's last sequence until a successful response has an empty `entries` array. If a request fails, retry from the same sequence. An active journal can receive more entries while you read; pagination does not create a snapshot.

### Search across journals

Find `review_started` events across journals in the selected file system:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100
```

Search defaults to at most 100 matches per call. Pass the last match's `cursor` to the next request, keeping the same filters:

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --limit 100 \
  --cursor "<last-match-cursor>"
```

Continue until a successful response has an empty `matches` array. If a request fails, retry with the same cursor. To limit the search to a fixed time range, supply RFC3339 `--since` and `--until` values and keep them unchanged across pages.

For a single page of full entry contents, add `--include-entries`. Omit it when paginating: that output does not retain match cursors. To retrieve a matched entry separately, use its `journal_id` with `read-journal-entries --after-seq <seq-minus-one> --limit 1`.

## Verify a journal

To check that the stored journal history is internally consistent, verify its hash chain:

```shell
ti fs-journal verify-journal \
  --journal-id "<journal-id>"
```

A successful verification confirms that the stored sequence and hash chain are consistent.

Hash-chain verification checks the integrity of the recorded journal history. It does not prove that the original event information recorded by an agent or application was accurate.

## What's next

- [Record an Agent Workflow in a File System Journal](/ai/ti/guides/ti-journal-agent-workflow-example.md) for an end-to-end agent workflow example.
- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md) for all journal commands and options.

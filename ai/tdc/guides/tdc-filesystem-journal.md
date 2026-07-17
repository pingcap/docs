---
title: Use TiDB Cloud Filesystem Journals
summary: Create append-only workflow journals, append and search structured events, and verify their hash chains.
---

# Use TiDB Cloud Filesystem Journals

`tdc fs-journal` provides an append-only, verifiable ledger for agent and workflow events. Unlike a mutable text file, a journal assigns ordered sequence numbers, supports structured search, and maintains a hash chain that can detect alteration.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

Select a Filesystem through a profile or provide `TDC_FS_TOKEN`, `TDC_REGION_CODE`, and `TDC_FS_FILE_SYSTEM_NAME`.

## Create a journal

```bash
tdc fs-journal create-journal \
  --journal-id jrn-demo \
  --journal-kind agent \
  --title "demo task" \
  --actor agent:tdc \
  --label env=dev
```

`--journal-id` is optional and generated when omitted. Labels are repeatable.

## Append entries

Append one or more JSON objects:

```bash
tdc fs-journal append-journal-entries \
  --journal-id jrn-demo \
  --entry-json '{"type":"task.started","status":"running"}' \
  --entry-json '{"type":"tool.called","tool":"tdc"}'
```

Use `--entry-type` as a default for entries without `type`, and add `--source` or repeatable `--subject` metadata. `--idempotency-key` makes a retry deterministic; tdc generates one when omitted.

For pipelines, send JSON Lines on stdin, or use `--json-array` for a JSON array.

## Read and search

Read entries after a sequence:

```bash
tdc fs-journal read-journal-entries \
  --journal-id jrn-demo \
  --after-seq 0 \
  --limit 100
```

Search across journals:

```bash
tdc fs-journal search-journal-entries \
  --entry-type task.started \
  --journal-kind agent \
  --label env=dev \
  --include-entries
```

Search also supports status, actor, subject, `--since`, `--until`, `--limit`, and pagination cursor filters.

## Verify integrity

```bash
tdc fs-journal verify-journal \
  --journal-id jrn-demo \
  --output text
```

Verification recalculates the ordered hash chain and reports whether the entries are internally consistent. It does not assert that the event payload was truthful when originally appended.

## What's next

- [Record an Agent Workflow in a Journal](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
- [tdc Configuration and Credentials](/ai/tdc/reference/tdc-configuration-and-credentials.md)

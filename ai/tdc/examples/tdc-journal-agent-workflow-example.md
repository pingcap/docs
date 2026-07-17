---
title: Record an Agent Workflow in a Filesystem Journal
summary: Create a journal, append structured agent events, search the workflow, and verify the journal hash chain.
---

# Record an Agent Workflow in a Filesystem Journal

This example records an agent task as structured, ordered events rather than appending unvalidated text to a mutable file.

> **Note:**
>
> tdc is currently in Preview. Its features and command-line interface might change without prior notice.

## Prerequisites

Select a Filesystem through a configured profile or FS token environment.

## Step 1. Create the journal

```bash
tdc fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## Step 2. Append workflow events

```bash
tdc fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

tdc fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

## Step 3. Read and search

```bash
tdc fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

tdc fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

The ordered result should include the start, test, and completion events.

## Step 4. Verify integrity

```bash
tdc fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

A successful result confirms the stored sequence and hash chain are consistent.

## Cleanup

Journals are append-only and currently have no delete command in the tdc public surface. Use a synthetic journal ID and retain it as workflow evidence. Delete the containing Filesystem only when its complete contents are no longer needed.

## Security notes

- Do not put API keys, passwords, SQL text containing secrets, or raw file contents in journal payloads.
- Hash-chain verification detects stored-chain inconsistency; it does not prove the original event was truthful.

## What's next

- [Use TiDB Cloud Filesystem Journals](/ai/tdc/guides/tdc-filesystem-journal.md)
- [Delegate Secrets to an Agent](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)

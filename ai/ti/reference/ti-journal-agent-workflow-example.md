---
title: Record an Agent Workflow in a TiDB Cloud Filesystem Journal
summary: Create a journal, append structured agent events, search the workflow, and verify the journal hash chain.
---

# Record an Agent Workflow in a TiDB Cloud Filesystem Journal

This example records an agent task as a structured, ordered, and verifiable event history.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## The agent problem

An agent task can span planning, tool calls, tests, retries, and handoffs between workers. When the task fails, operators need to know which events happened and in what order. Plain console output is often scattered across processes, while a mutable status file shows only the latest state.

## Limitations of appending to a normal file

A text file can be edited or truncated after an event is written, has no intrinsic sequence or hash chain, and requires every producer to invent parsing and concurrency rules. Retrying an append can also create duplicate events unless the application builds its own idempotency layer.

## How TiDB Cloud CLI changes the workflow

A Filesystem journal stores structured append-only entries with sequence information, searchable fields, optional idempotency keys, and hash-chain verification. Agents append semantic events such as `task.started` and `test.finished`; operators can query the workflow and verify the stored chain without treating a mutable log file as evidence.

## Prerequisites

Select a Filesystem through a configured profile or FS token environment.

## Step 1. Create the journal

```bash
ti fs-journal create-journal \
  --journal-id jrn-agent-demo \
  --journal-kind agent \
  --title "dependency update" \
  --actor agent:dependency-bot \
  --label repository=demo \
  --label environment=test
```

## Step 2. Append workflow events

```bash
ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --idempotency-key dependency-update-start \
  --entry-json '{"type":"task.started","status":"running"}'

ti fs-journal append-journal-entries \
  --journal-id jrn-agent-demo \
  --entry-json '{"type":"test.finished","status":"passed","suite":"unit"}' \
  --entry-json '{"type":"task.finished","status":"completed"}'
```

## Step 3. Read and search

```bash
ti fs-journal read-journal-entries \
  --journal-id jrn-agent-demo \
  --after-seq 0 \
  --limit 100 \
  --output text

ti fs-journal search-journal-entries \
  --entry-type task.finished \
  --status completed \
  --label repository=demo \
  --include-entries
```

The ordered result should include the start, test, and completion events.

## Step 4. Verify integrity

```bash
ti fs-journal verify-journal \
  --journal-id jrn-agent-demo \
  --output text
```

A successful result confirms the stored sequence and hash chain are consistent.

## Cleanup

Journals are append-only and currently have no delete command in the public `ti` command surface. Use a synthetic journal ID and retain it as workflow evidence. Delete the containing Filesystem only when its complete contents are no longer needed.

## Security notes

- Do not put API keys, passwords, SQL text containing secrets, or raw file contents in journal payloads.
- Hash-chain verification detects stored-chain inconsistency; it does not prove the original event was truthful.

## What's next

- [TiDB Cloud Filesystem Journal CLI Command Reference](/ai/ti/reference/ti-filesystem-journal.md)
- [Delegate Secrets to an Agent](/ai/ti/reference/ti-vault-agent-secrets-example.md)

---
title: Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem
summary: Persist build output in TiDB Cloud Filesystem and consume it from a later CI job without copying a complete TiDB Cloud CLI profile.
---

# Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem

This scenario uses a Filesystem as a durable handoff point between isolated CI jobs or runners.

> **Note:**
>
> The TiDB Cloud Command Line Interface — `ti` — is currently in preview. Its features and command-line interface might change without prior notice.

## The problem

Build and verification jobs often run on different ephemeral machines. Local output disappears with the producer, while provider-specific artifact services add another upload API, retention model, and download step to agent automation.

## How TiDB Cloud CLI changes the workflow

The pipeline injects one Filesystem token and region into both jobs. The token identifies the Filesystem. The producer uploads output under a run-specific path, and the consumer downloads or streams that exact path. Neither job needs TiDB Cloud API keys or a copied `~/.ti/` directory.

## Prerequisites

Provision a Filesystem on a trusted machine and store these values as protected CI secrets or variables:

```text
TI_FS_TOKEN
TI_REGION_CODE
```

Use a CI-generated run identifier such as `RUN_ID` to isolate concurrent pipelines.

## Producer job

Build the artifact, then upload it:

```bash
tar -czf app.tar.gz ./dist
ti fs copy-file \
  --from-local ./app.tar.gz \
  --to-remote "/ci/${RUN_ID}/app.tar.gz" \
  --tag pipeline=build \
  --description "artifact for run ${RUN_ID}"
```

## Consumer job

Download and verify the artifact from another runner:

```bash
ti fs copy-file \
  --from-remote "/ci/${RUN_ID}/app.tar.gz" \
  --to-local ./app.tar.gz \
  --create-parents

tar -tzf app.tar.gz
```

For a command that accepts stdin, avoid an intermediate local file:

```bash
ti fs copy-file --from-remote "/ci/${RUN_ID}/app.tar.gz" --to-stdout \
  | tar -tzf -
```

## Cleanup and isolation

Delete only the run-specific directory after all consumers finish:

```bash
ti fs delete-file --path "/ci/${RUN_ID}" --recursive
```

Use unique run IDs and do not delete the whole Filesystem from an individual job. Filesystem deletion requires the trusted control-plane configuration and should remain a separate owner operation.

## Related reference

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)

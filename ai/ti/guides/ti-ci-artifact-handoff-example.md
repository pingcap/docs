---
title: Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem
summary: Persist build output in TiDB Cloud Filesystem and consume it from a later CI job without copying a complete TiDB Cloud CLI profile.
---

# Hand Off CI Artifacts Between Isolated Jobs with TiDB Cloud Filesystem

This workflow uses a Filesystem as a durable handoff point between isolated CI jobs or runners. Use it when build output must survive the producer job and become available to a later consumer without adding a provider-specific artifact API, retention model, and download workflow.

> **Note:**
>
> TiDB Cloud CLI (`ti`) is currently in public preview. Its features and command-line interface are subject to change without notice.

## How it works

The pipeline injects one Filesystem token and region into both jobs. The token identifies the Filesystem. The producer uploads output under a run-specific path such as `/ci/${RUN_ID}/`, and the consumer downloads or streams data from that exact path on another runner. Neither job needs TiDB Cloud API keys or a copied `~/.ti/` directory.

## Prerequisites

[Create a Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md#create-a-filesystem) on a trusted machine, and store these values as protected CI secrets or variables:

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

## What's next

- [TiDB Cloud Filesystem CLI Command Reference](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI Configuration and Credentials](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI Regions, Security, and Limitations](/ai/ti/reference/ti-regions-security-and-limitations.md)

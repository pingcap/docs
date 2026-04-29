---
title: Table Versioning
summary: Table versioning lets you create named references to specific snapshots of a FUSE table. These references survive automatic retention cleanup, giving you stable, human-readable pointers to historical table states.
---

# Table Versioning

Table versioning lets you create named references to specific snapshots of a FUSE table. These references survive automatic retention cleanup, giving you stable, human-readable pointers to historical table states.

> **Note:**
>
> Table versioning is an experimental feature. Enable it before use:
>
> ```sql
> SET enable_experimental_table_ref = 1;
> ```

## Snapshot Tags

Snapshot tags pin a specific point-in-time state of a table by name. Once created, a tag holds a reference to a particular snapshot so you can query that exact state at any time using the [AT](/tidb-cloud-lake/sql/at.md) clause, without needing to track snapshot IDs or timestamps.

**Use cases:**

- **Release checkpoints**: Tag the table state before and after a data pipeline run so you can compare or roll back.
- **Audit and compliance**: Preserve a named snapshot for regulatory review without worrying about retention expiry.
- **Safe experimentation**: Tag the current state, run experimental transforms, then query the tag to verify what changed.
- **Reproducible analytics**: Pin a dataset version so dashboards and reports always reference the same data.

**How it works:**

A snapshot tag attaches a human-readable name to a snapshot. As long as the tag exists, the referenced snapshot is protected from vacuum and garbage collection — even if the retention period has passed.

- A tag without `RETAIN` lives until explicitly dropped.
- A tag with `RETAIN <n> { DAYS | SECONDS }` is automatically removed after the specified duration during the next vacuum operation.

**SQL Commands:**

| Command | Description |
|---------|-------------|
| [CREATE SNAPSHOT TAG](/tidb-cloud-lake/sql/create-snapshot-tag.md) | Create a named tag on a table snapshot |
| [DROP SNAPSHOT TAG](/tidb-cloud-lake/sql/drop-snapshot-tag.md) | Remove a snapshot tag |
| [FUSE_TAG](/tidb-cloud-lake/sql/fuse-tag.md) | List all snapshot tags on a table |

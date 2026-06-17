---
title: TiDB Lightning Web Interface
summary: Learn about the removal of the TiDB Lightning Web Interface and the recommended alternatives.
aliases: ['/docs/dev/tidb-lightning/tidb-lightning-web-interface/','/docs/dev/reference/tools/tidb-lightning/web/']
---

# TiDB Lightning Web Interface

> **Warning:**
>
> Starting from TiDB v8.5.7, TiDB Lightning no longer supports the web interface.

To import data with TiDB Lightning, run `tidb-lightning` from the command line.

- For a basic procedure, see [Get Started with TiDB Lightning](/get-started-with-tidb-lightning.md).
- For command-line options, see [TiDB Lightning Command Line Flags](/tidb-lightning/tidb-lightning-command-line-full.md).

To check the import progress, search for the `progress` keyword in the TiDB Lightning log, or use the [TiDB Lightning monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).

For new data import workloads, you can also use the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement.

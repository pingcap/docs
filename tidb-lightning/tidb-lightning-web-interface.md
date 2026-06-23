---
title: TiDB Lightning Web Interface
summary: Learn about the removal of the TiDB Lightning Web Interface and the recommended alternatives.
---

# TiDB Lightning Web Interface

> **Warning:**
>
> Starting from TiDB v8.5.7, TiDB Lightning no longer supports the web interface. Starting from v8.5.6, the TiDB Lightning web interface is deprecated. The web UI build had been broken since v8.4.0.

To import data with TiDB Lightning, use the TiDB Lightning command-line tools: `tidb-lightning` for import tasks and `tidb-lightning-ctl` for checkpoint and troubleshooting operations.

- For a basic procedure, see [Get Started with TiDB Lightning](/get-started-with-tidb-lightning.md).
- For command-line options, see [TiDB Lightning Command Line Flags](/tidb-lightning/tidb-lightning-command-line-full.md).

To check the import progress, search for the `progress` keyword in the TiDB Lightning log, or use the [TiDB Lightning monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).

For new data import workloads, you can also use the [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) statement.

> **Note:**
>
> If you are using an earlier version of TiDB that still has the TiDB Lightning web interface, you can view the following content for reference.

TiDB Lightning provides a webpage for viewing the import progress and performing some simple task management. This is called the *server mode*.

To enable server mode, either start `tidb-lightning` with the `--server-mode` flag

```sh
tiup tidb-lightning --server-mode --status-addr :8289
```

or set the `lightning.server-mode` setting in the configuration file.

```toml
[lightning]
server-mode = true
status-addr = ':8289'
```

After TiDB Lightning is launched, visit `http://127.0.0.1:8289` to control the program (the actual URL depends on the `status-addr` setting).

In server mode, TiDB Lightning does not start running immediately. Rather, users submit (multiple) *tasks* via the web interface to import data.

## Front page

![Front page of the web interface](/media/lightning-web-frontpage.png)

Functions of the title bar, from left to right:

| Icon | Function |
|:----|:----|
| "TiDB Lightning" | Click to go back to the front page |
| ⚠ | Display any error message from *previous* task |
| ⓘ | List current and queued tasks; a badge may appear here to indicate number of queued tasks |
| + | Submit a task |
| ⏸/▶ | Pause/resume current execution |
| ⟳ | Configure auto-refresh of the web page |

Three panels below the title bar show all tables in different states:

* Active: these tables are currently being imported
* Completed: these tables have been imported successfully or failed
* Pending: these tables are not yet processed

Each panel contains cards describing the status of the table.

## Submit task

Click the **+** button on the title bar to submit a task.

![Submit task dialog](/media/lightning-web-submit.png)

Tasks are TOML files described as [task configurations](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-task). One could also open a local TOML file by clicking **UPLOAD**.

Click **SUBMIT** to run the task. If a task is already running, the new task will be queued and executed after the current task succeeds.

## Table progress

Click the **>** button of a table card on the front page to view the detailed progress of a table.

![Table progress](/media/lightning-web-table.png)

The page shows the import progress of every engine and data files associated with the table.

Click **TiDB Lightning** on the title bar to go back to the front page.

## Task management

Click the **ⓘ** button on the title bar to manage the current and queued tasks.

![Task management page](/media/lightning-web-queue.png)

Each task is labeled by the time it was submitted. Clicking the task would show the configuration formatted as JSON.

Manage tasks by clicking the **⋮** button next to a task. You can stop a task immediately, or reorder queued tasks.

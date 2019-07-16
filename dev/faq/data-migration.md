---
title: Data Migration FAQ
summary: Learn about two questions (FAQs) relating to Data Migration.
category: FAQ
---

# Data Migration FAQ

This is a simple FAQ page for DM, including:

+ How to handle the `invalid connection` error
+ How to handle the `driver: bad connection` error

## What can I do when a synchronization task is interrupted with the `invalid connection` error returned?

`invalid connection` error usually indicates that errors have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, TiKV busy and so on) and that part of the data for the current request has been sent to TiDB.

DM concurrently replicates data downstream in its synchronization tasks. Due to this feature, several errors might occur when a task is interrupted. You can check these errors through `query-status` or `query-error`.

- If there is only `invalid connection` error during the incremental replication, DM retries automatically.
- If DM doesn't or fail to retry automatically because of version problems, you can use `stop-task` to stop the task and then use`start-task` to restart the task.

## What can I do when a synchronization task is interrupted with the `driver: bad connection` error returned?

`driver: bad connection` usually indicates connection error between DM and upstream TiDB database (Network failure, TiDB restart and so on) and no data of current request are sent to TiDB temporarily.

In the current version, when facing this type of error, you should use `stop-task` to stop the task and then use `start-task` to restart the task. DM will improve its automatic retry function for this type of error later.

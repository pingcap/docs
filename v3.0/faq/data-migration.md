---
title: Data Migration FAQ
category: FAQ
---

# Data Migration FAQ

## What can I do when a synchronization task is interrupted with an `invalid connection` error returned ?

`invalid connection` error usually indicates connection error between DM and downstream TiDB database (Network failure, TiDB restart, Tikv busy and so on) and some data of current request have been sent to TiDB.

DM will concurrently replicate data downstream in synchronize tasks. Due to this feature, an interrupted task may contain several errors. ( You could check current error by using `query-status` or `query-error`. )

- If there is only `invalid connection` error during incremental replication, DM will retry automatically.
- If DM doesn't or fail to retry automatically because of version problems, you can use `stop-task` to stop the task and then use`start-task` to restart the task.

## What can I do when a synchronization task is interrupted with an `driver: bad connection` error ?

`driver: bad connection` usually indicates connection error between DM and upstream TiDB database (Network failure, TiDB restart and so on) and no data of current request are sent to TiDB temporarily.

In the current version, when facing this type of error, you should use `stop-task` to stop the task and then use `start-task` to restart the task. DM will improve its automatic retry function for this type of error later.

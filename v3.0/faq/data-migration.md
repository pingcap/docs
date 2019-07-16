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

## What can I do when a synchronization task is interrupted with the `driver: bad connection` error returned?

`driver: bad connection` error usually indicates that errors have occurred in the connection between DM and the upstream TiDB database (such as network failure, TiDB restart and so on) and that data of the current request has not been sent to TiDB at that moment.

When facing this type of error in the current version, use `stop-task` to stop the task and then use `start-task` to restart the task. DM will be improved on its automatic retry mechanism to cope with this type of error in the future.

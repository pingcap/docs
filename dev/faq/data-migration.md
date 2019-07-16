---
title: Data Migration FAQ
summary: Learn about two questions (FAQs) relating to Data Migration.
category: FAQ
---

# Data Migration FAQ

This is a simple FAQ page for Data Migration (DM), including:

+ How to handle the `invalid connection` error
+ How to handle the `driver: bad connection` error

## What can I do when a synchronization task is interrupted with the `invalid connection` error returned?

`invalid connection` error usually indicates that errors have occurred in the connection between DM and the downstream TiDB database (such as network failure, TiDB restart, TiKV busy and so on) and that a part of the data for the current request has been sent to TiDB.

DM concurrently replicates data downstream in its synchronization tasks. Due to this feature, several errors might occur when a task is interrupted. You can check these errors through `query-status` or `query-error`.

- If there is only the `invalid connection` error returned during the incremental replication, DM retries automatically.
- If DM does not or fails to retry automatically because of version problems, use `stop-task` to stop the task and then use`start-task` to restart the task.

## What can I do when a synchronization task is interrupted with the `driver: bad connection` error returned?

`driver: bad connection` error usually indicates that errors have occurred in the connection between DM and the upstream TiDB database (such as network failure, TiDB restart and so on) and that the data of the current request has not yet been sent to TiDB at that moment.

When facing this type of error in the current version, use `stop-task` to stop the task and then use `start-task` to restart the task. DM will be improved on its automatic retry mechanism to cope with this type of error in the future.

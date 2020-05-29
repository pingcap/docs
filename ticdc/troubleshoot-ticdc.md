---
title: Common Problems and Troubleshooting
summary: Fix common problems while using TiCDC.
category: reference
---

# Common Problems and Troubleshooting

This document includes some common problems that you might have while using TiCDC and provides appropriate solutions. It also summarizes some common operation failures and ways to fix them.

## How to choose start-ts while starting a task

First, you need to know that the `start-ts` of a replication task corresponds to a TSO of the upstream TiDB cluster. The replication task will start its data request from this TSO. Therefore, the `start-ts` should meet two conditions below:

- The value of `start-ts` must be larger than current `tikv_gc_safe_point`, otherwise, an error would occur when creating the task.
- While starting a task, you need to ensure that the downstream has already got all the data previous to `start-ts`. You can relax this requirement accordingly, if the replication task is for message queue or other scenarios, in which strict data consistency between upstream and downstream is not strictly required.

If `start-ts` is not specified or specified as `0`, when a replication task gets started, TiCDC will get the current TSO from PD and start to replicate data from it.

## When a task gets started, it prompts that some tables cannot be replicated

When you use `cdc cli changefeed create` to create a replication task, TiCDC will check if the upstream tables comply with the [restrictions](/ticdc/ticdc-overview.md#restrictions). If they don't, TiCDC will prompt that `some tables are not eligible to replicate`, and will list out the ineligible tables. If you choose `Y` or `y`, TiCDC will continue creating the replication task and automatically ignore all the updates of these ineligible tables. If you choose other inputs, the replication task will not be created.

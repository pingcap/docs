---
title: Common Problems and Troubleshooting
summary: Fix common problems while using TiCDC.
category: reference
aliases: ['/docs/dev/reference/tools/ticdc/troubleshoot-ticdc/']
---

# Common Problems and Troubleshooting

This document lists some common problems while using TiCDC and gives appropriate solutions. It also summarizes some common operation failures and ways to fix them.

## How to choose start-ts while starting a task

First, you should know that the `start-ts` of a replication task corresponds to a TSO of the upstream TiDB cluster. The replication task will start its data request from this TSO. Therefore, the `start-ts` should meet two conditions below:

- The value of `start-ts` should be larger than current `tikv_gc_safe_point`, otherwise, an error would occur when creating the task.
- While starting the task, you should ensure that the downstream has all the data before `start-ts`. You can relax this requirement accordingly, if the replication task is for message queue or other scenarios, in which strict data consistency between upstream and downstream is not strictly required.

If `start-ts` is not specified or specified 0 `start-ts=0`, when the task gets started, it will get the current TSO from PD and start to replicate data from this TSO.

## When a task gets started, it prompts that some tables cannot be synchronized

When using `cdc cli changefeed create` to create a replication task, it will check if the upstream tables comply with the [restrictions](/ticdc/ticdc-overview.md#restrictions). If there are tables , it will prompt that `some tables are not eligible to replicate` and list out the ineligible tables. If you choose `Y` or `y`, you will continue creating the replication task and automatically ignore all the updates of these ineligible tables. If you choose other inputs, the replication task will not be created.

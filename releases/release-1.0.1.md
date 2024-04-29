---
title: TiDB 1.0.1 Release Notes
aliases: ['/docs/dev/releases/release-1.0.1/','/docs/dev/releases/101/']
summary: TiDB 1.0.1 was released on November 1, 2017. Updates include support for canceling DDL Job, optimizing the `IN` expression, correcting the result type of the `Show` statement, supporting log slow query into a separate log file, and fixing bugs. TiKV now supports flow control with write bytes, reduces Raft allocation, increases coprocessor stack size to 10MB, and removes the useless log from the coprocessor.
---

# TiDB 1.0.1 Release Notes

On November 1, 2017, TiDB 1.0.1 is released with the following updates:

## TiDB

- Support canceling DDL Job.
- Optimize the `IN` expression.
- Correct the result type of the `Show` statement.
- Support log slow query into a separate log file.
- Fix bugs.

## TiKV

- Support flow control with write bytes.
- Reduce Raft allocation.
- Increase coprocessor stack size to 10MB.
- Remove the useless log from the coprocessor.

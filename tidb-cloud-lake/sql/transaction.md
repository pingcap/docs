---
title: Transaction
---

This page provides a comprehensive overview of Transaction operations in Databend, organized by functionality for easy reference.

## Transaction Control

| Command | Description |
|---------|-------------|
| [BEGIN](begin.md) | Starts a new transaction |
| [COMMIT](commit.md) | Commits the current transaction and makes all changes permanent |
| [ROLLBACK](rollback.md) | Aborts the current transaction and discards all changes |

## Transaction Information

| Command | Description |
|---------|-------------|
| [SHOW LOCKS](show-locks.md) | Displays information about active locks in the system |

:::note
Transactions in Databend ensure data consistency by grouping SQL operations into atomic units that either completely succeed or completely fail, maintaining database integrity.
:::
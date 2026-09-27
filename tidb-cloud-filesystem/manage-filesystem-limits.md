---
title: Manage TiDB Cloud Filesystem Limits
summary: Learn which TiDB Cloud Filesystem capacity limits apply without a credit card on your organization and what happens when a file system reaches a limit.
---

# Manage TiDB Cloud Filesystem Limits

> **Note:**
>
> The limits in this document apply only when your TiDB Cloud organization has no credit card.

You can create and use file systems in the TiDB Cloud Filesystem service without a credit card, but each free file system has tighter capacity limits. You can uplift these limits after adding a credit card to your organization.

## Limits without a credit card on the organization

When your organization has **no credit card registered**, the following limits apply to each free file system:

- One file system per region
- 2,000 files per file system
- 2 GB of storage per file system
- 500 MB maximum size for a single file

Organizations with a credit card are **exempt** from these limits.

## When a file system reaches a limit

When a file system hits one of these limits, your existing files stay readable and the file system **stops accepting new writes**. The TiDB Cloud console shows a warning.

To raise or remove the capacity limits, make sure your TiDB Cloud organization has a credit card registered, and then use `Edit Usage Limit` button to increase the limits on the Overview page of the specific file system.

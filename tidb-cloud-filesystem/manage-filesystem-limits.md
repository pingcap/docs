---
title: Manage TiDB Cloud Filesystem Usage Limit
summary: Learn how to view file system usage and free limits in the TiDB Cloud console, and edit usage limits after adding a credit card.
---

# Manage TiDB Cloud Filesystem Usage Limit

> **Note:**
>
> The limits in [Limits without a credit card on the organization](#limits-without-a-credit-card-on-the-organization) apply only when your TiDB Cloud organization has no credit card.

You can create and use file systems in the TiDB Cloud Filesystem service without a credit card, but each free file system has tighter capacity limits. You can raise these limits after adding a credit card to your organization.

## Limits without a credit card on the organization

When your organization has **no credit card registered**, the following limits apply to each free file system:

- One file system per region
- 2,000 files per file system
- 2 GB of storage per file system
- 500 MB maximum size for a single file

With a credit card, you can set higher limits and continue with pay-as-you-go usage. See [TiDB Cloud Filesystem pricing](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/) for billing details.

## View file system usage

To view the current usage of a file system, go to its overview page in the [TiDB Cloud console](https://tidbcloud.com/) and check the **Usage** area. For usage details, click **Usage** in the left navigation pane.

## When a file system reaches a limit

When a file system reaches a limit, existing files remain readable, but the file system stops accepting new writes. The TiDB Cloud console shows a warning.

## Update the usage limit

1. In the TiDB Cloud console, navigate to the [**File Systems**](https://tidbcloud.com/filesystems) page, select the **Cloud Provider** and **Region** for the file system, and click the name of your target file system.
2. On the overview page of the file system, click **Edit Usage Limit** in the **Usage** area.
3. Set maximum storage, file count, and file size as needed, then click **Save**.

    If your organization has no credit card, these fields are disabled. Add a credit card to edit them and enable pay-as-you-go usage.

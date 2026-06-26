---
title: Kernel Versioning for TiDB Cloud Premium
summary: Learn about the kernel versioning rules and format for TiDB Cloud Premium.
---

# Kernel Versioning for TiDB Cloud Premium

This document describes the versioning rules for the underlying database kernel used by TiDB Cloud Premium.

> **Note:**
>
> - This document applies only to TiDB Cloud Premium.
> - TiDB Cloud Starter and Essential instances run on a customized TiDB X engine based on the classic TiDB v8.5.3 kernel. This kernel differs slightly from the TiDB Cloud Premium kernel.
> - TiDB Cloud Dedicated clusters run on the classic TiDB kernel, and their kernel versions correspond directly to TiDB Self-Managed versions.

## Kernel versioning

TiDB Cloud Premium kernel versions use the following time-based format:

```text
TiDB-X-CLOUD.YYYYMM.x
```

For example:

```text
TiDB-X-CLOUD.202510.1
```

Where:

- `YYYYMM` indicates the baseline code branch used to develop the kernel. For example, `202510` means that the baseline branch was created in October 2025. It does not indicate when the kernel version was released.
- `x` indicates the patch release number for that baseline branch.

For example, `TiDB-X-CLOUD.202510.1` indicates that the kernel is based on a branch created in October 2025 and is the first patch release built from that branch.

Because kernel development and release schedules are independent, a kernel version might be released several months after its baseline branch is created.

Because TiDB Cloud Premium follows its own kernel release cadence, TiDB Cloud Premium release notes are published separately from TiDB Self-Managed release notes.

## FAQ

### How do I check the kernel version of my TiDB Cloud Premium instance?

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the **My TiDB** page, and then click the name of your TiDB Cloud Premium instance to go to its overview page.
2. On the overview page, locate the **TiDB version** information in the details pane of your TiDB Cloud Premium instance.

### Can I choose the kernel version for my TiDB Cloud Premium instance?

No. TiDB Cloud manages the entire kernel lifecycle for TiDB Cloud Premium.

Although the kernel version is displayed for transparency, you cannot select a specific version when creating a TiDB Cloud Premium instance.

TiDB Cloud automatically provides validated kernel versions for new deployments and performs managed upgrades when appropriate. This helps ensure security, stability, compatibility, and access to the latest features and improvements without requiring manual maintenance.
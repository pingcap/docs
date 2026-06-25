---
title: Kernel Versioning for TiDB Cloud
summary: Learn about the versioning rules, format, and release notes for different TiDB Cloud offerings.
---

# TiDB Cloud Kernel Versioning

This document describes the versioning rules for the underlying database kernels used across different TiDB Cloud plans: Starter, Essential, Premium, and Dedicated.

## Default kernel versions

Based on your TiDB Cloud plan, your TiDB Cloud resources run on different different TiDB kernel versions:

| Plan      | Current default kernel version |
|-----------|--------------------------------|
| Starter   | TiDB v8.5.3                    |
| Essential | TiDB v8.5.3                    |
| Premium   | TiDB-X-CLOUD.202510.1          |
| Dedicated | TiDB v8.5.6                    |

The default kernel version is the TiDB version that is used by default for new instances or clusters. TiDB Cloud upgrades the default kernel version for newly created instances or clusters regularly to improve the security, stability, and performance of your TiDB Cloud resources.

## Kernel versioning

For TiDB Cloud Starter, Essential, and Dedicated, their kernel versions correspond directly to TiDB Self-Managed versions. To learn about features, improvements, and bug fixes included in a specific kernel version, refer to the corresponding [TiDB Self-Managed release notes](/releases/release-notes.md).

For TiDB Cloud Premium, its kernel version follows a time-based versioning convention:

```text
TiDB-X-CLOUD.YYYYMM.x
```

For example:

```text
TiDB-X-CLOUD.202510.1
```

Where:

- `YYYYMM` represents the baseline code branch used to develop the kernel. For example, `202510` means that the baseline branch was created in October 2025. It does not indicate when the kernel version was released.
- `x` represents the patch release number for that baseline branch.

For example, `TiDB-X-CLOUD.202510.1` means that the kernel is based on a branch created in October 2025 and is the first patch release built from that branch.

Because kernel development and release schedules are independent, a kernel version might be released several months after its baseline branch is created.

As the kernel of TiDB Cloud Premium follows its own release cadence and cycle, its release notes are published separately from the TiDB Self-Managed release notes.

## FAQ

### How do I check the kernel version of my TiDB Cloud resource?

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the **My TiDB** page, and then click the name of your TiDB Cloud resource (such as an instance or cluster) to go to its overview page.
2. On the overview page, locate the **TiDB version** information in the details pane of your TiDB Cloud resource.

### Can I choose the kernel version for my TiDB Cloud Starter, Essential, Premium instance, or TiDB Cloud Dedicated cluster?

No. TiDB Cloud manages the entire kernel lifecycle for all plans.

Although the kernel version is displayed for transparency, you cannot select a specific version when creating an instance or cluster.

TiDB Cloud automatically provides validated kernel versions for new deployments and performs managed upgrades when appropriate. This helps ensure security, stability, compatibility, and access to the latest features and improvements without requiring manual maintenance.
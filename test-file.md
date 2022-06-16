---
title: TiDB Cluster Alert Rules
summary: Learn the alert rules in a TiDB cluster.
aliases: ['/docs/dev/alert-rules/','/docs/dev/reference/alert-rules/']
---

<!-- markdownlint-disable MD024 -->

# TiDB Cluster Alert Rules

This document describes a large number of rules for different components in a TiDB cluster, including the rule descriptions and solutions of the alert items in TiDB, TiKV, PD, TiFlash, TiDB Binlog, TiCDC, Node_exporter and Blackbox_exporter.

According to the severity level, alert rules are divided into three categories (from high to low): emergency-level, critical-level, and warning-level. This division of severity levels applies to all alert items of each component below.

|  Severity level |  Description   |
| :-------- | :----- |
|  Emergency-level  |  The highest severity level at which the service is unavailable. Emergency-level alerts are often caused by a service or node failure. **Manual intervention is required immediately**. |
|  Critical-level  |  Decreased service availability. For the critical-level alerts, a close watch on the abnormal metrics is required. |
|  Warning-level  |  Warning-level alerts are a reminder for an issue or error.   |

## TiDB alert rules

This section gives the alert rules for the TiDB component.

### Emergency-level alerts

This section gives many alert rules for the TiDB component.

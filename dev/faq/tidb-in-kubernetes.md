---
title: TiDB FAQs in Kubernetes
summary: Learn about TiDB FAQs in Kubernetes.
category: FAQ
---

# TiDB FAQs in Kubernetes

This document collects frequently asked questions (FAQs) about the TiDB cluster in Kubernetes.

## How to modify time zone settings？

The time zone in component containers of the TiDB cluster deployed in the Kubernetes cluster is UTC by default. To modify time zone settings, perform the following steps:

* If it is the first time you deploy the cluster:

    Modify `timezone` settings in the `values.yaml` file of the TiDB cluster. For example, you can set it to `timezone: Asia/Shanghai` and then deploy the TiDB cluster.

* If the cluster is running:

    * Modify `timezone` settings in the `values.yaml` file of the TiDB cluster. For example, you can set it to `timezone: Asia/Shanghai` and then upgrade the TiDB cluster.
    * Refer to [Time Zone Support](/how-to/configure/time-zone.md) to modify TiDB service time zone settings.
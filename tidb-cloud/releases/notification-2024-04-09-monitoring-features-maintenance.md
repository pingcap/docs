---
title: 2024-04-09 TiDB Cloud 监控功能维护通知
summary: 了解 2024 年 4 月 9 日 TiDB Cloud 监控功能维护的详细信息，包括维护窗口、原因及影响。
---

# [2024-04-09] TiDB Cloud 监控功能维护通知

本通知描述了你需要了解的关于 2024 年 4 月 9 日 TiDB Cloud [监控功能](/tidb-cloud/monitor-tidb-cluster.md)维护的详细信息。

## 维护窗口

- 开始时间：2024-04-09 08:00 (UTC+0)
- 结束时间：2024-04-09 12:00 (UTC+0)
- 持续时间：4 小时

## 影响

### 受影响的 Region

在维护窗口期间，以下 Region 的监控功能将受到影响：

- TiDB Cloud Dedicated 集群：
    - 云服务商：AWS，Region：Oregon (us-west-2)
    - 云服务商：AWS，Region：Seoul (ap-northeast-2)
    - 云服务商：AWS，Region：Frankfurt (eu-central-1)
    - 云服务商：AWS，Region：Oregon (us-west-2)
    - 云服务商：Google Cloud，Region：Oregon (us-west1)
    - 云服务商：Google Cloud，Region：Tokyo (asia-northeast1)
    - 云服务商：Google Cloud，Region：Singapore (asia-southeast1)
    - 云服务商：Google Cloud，Region：Iowa (us-central1)
    - 云服务商：Google Cloud，Region：Taiwan (asia-east1)

- TiDB Cloud Starter 集群：
    - 云服务商：AWS，Region：Frankfurt (eu-central-1)
    - 云服务商：AWS，Region：Oregon (us-west-2)

### 受影响的监控功能

> **注意：**
>
> 本次维护仅影响 TiDB 集群中的监控功能。所有其他功能不受影响。你可以继续管理 TiDB 集群，并照常进行读写操作或其他操作。

- **Metrics** 页面将在多个短时间段内暂时不可用（每次小于 20 分钟）。
- **Slow Query** 页面将在多个短时间段内暂时不可用（每次小于 5 分钟）。
- 与 Prometheus、DataDog 和 NewRelic 的统计/指标（信息）集成可能会出现断点。

## 完成与恢复

维护成功完成后，受影响的功能将恢复，为你带来更优质的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系 [支持团队](/tidb-cloud/tidb-cloud-support.md)。我们将及时解答你的疑问并提供必要的指导。
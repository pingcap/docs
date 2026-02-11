---
title: 2024-04-11 TiDB Cloud Data Migration (DM) 功能维护通知
summary: 了解 2024 年 4 月 11 日 TiDB Cloud Data Migration (DM) 功能维护的详细信息，包括维护窗口和影响。
---

# [2024-04-11] TiDB Cloud Data Migration (DM) 功能维护通知

本通知描述了你需要了解的 2024 年 4 月 11 日 [Data Migration (DM) 功能](/tidb-cloud/migrate-from-mysql-using-data-migration.md) 在 TiDB Cloud Dedicated 上进行维护的相关细节。

## 维护窗口

- 开始时间：2024-04-11 08:00 (UTC+0)
- 结束时间：2024-04-11 09:00 (UTC+0)
- 持续时间：1 小时

## 影响

在维护窗口期间，以下区域的 TiDB Cloud Dedicated 集群的 DM 功能将受到影响：

- 云服务商：AWS，区域：Oregon (us-west-2)
- 云服务商：AWS，区域：N. Virginia (us-east-1)
- 云服务商：AWS，区域：Singapore (ap-southeast-1)
- 云服务商：AWS，区域：Seoul (ap-northeast-2)
- 云服务商：AWS，区域：Frankfurt (eu-central-1)
- 云服务商：AWS，区域：São Paulo (sa-east-1)
- 云服务商：AWS，区域：Oregon (us-west-2)
- 云服务商：Google Cloud，区域：Oregon (us-west1)
- 云服务商：Google Cloud，区域：Tokyo (asia-northeast1)
- 云服务商：Google Cloud，区域：Singapore (asia-southeast1)

本次维护仅影响 TiDB 集群中的 DM 功能。所有其他功能不受影响。你可以继续管理 TiDB 集群，并照常进行读写操作或其他操作。

对于部署在 AWS 上的集群：

- 升级期间，DM 任务可以持续运行，不会中断。DM 控制台可以正常使用。

对于部署在 Google Cloud 上的集群：

- DM 控制台最长将不可用 30 分钟。在此期间，你无法创建或管理 DM 任务。
- 如果 DM 任务处于增量迁移阶段，将会中断最长 30 分钟。在此期间，请勿清理 MySQL 数据库的二进制日志。升级完成后，DM 任务会自动恢复。
- 如果 DM 任务处于全量数据导出和导入阶段，升级期间任务将失败，且升级后无法恢复。建议在升级当天不要创建任何 DM 任务，以确保升级开始时没有 DM 任务处于全量数据导出和导入阶段。

## 完成与恢复

维护成功完成后，受影响的功能将恢复，为你带来更好的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系 [support team](/tidb-cloud/tidb-cloud-support.md)。我们将及时解答你的疑问并提供必要的指导。
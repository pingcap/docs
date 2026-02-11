---
title: 2024-09-15 TiDB Cloud 控制台维护通知
summary: 了解 2024 年 9 月 15 日 TiDB Cloud 控制台维护的详细信息，包括维护窗口、原因及影响。
---

# [2024-09-15] TiDB Cloud 控制台维护通知

本通知描述了你需要了解的关于 [TiDB Cloud 控制台](https://tidbcloud.com/) 在 2024 年 9 月 15 日进行维护的详细信息。

## 维护窗口

- 日期：2024-09-15
- 开始时间：8:00 (UTC+0)
- 结束时间：8:10 (UTC+0)
- 时长：约 10 分钟

> **Note:**
>
> - 目前，用户无法修改 TiDB Cloud 控制台的维护时间，因此你需要提前做好相应规划。
> - 在接下来的 3 个月内，部分用户可能会遇到额外 20 分钟的维护窗口。受影响的用户将会提前收到邮件通知。

## 维护原因

我们正在升级 TiDB Cloud 控制台的元数据库服务，以提升性能和效率。此次改进旨在为所有用户提供更优质的体验，这是我们持续致力于高质量服务承诺的一部分。

## 影响

在维护窗口期间，你可能会在 TiDB Cloud 控制台 UI 和 API 中与创建和更新相关的功能上遇到间歇性中断。然而，你的 TiDB 集群将保持正常的数据读写操作，确保不会对你的线上业务造成不良影响。

### TiDB Cloud 控制台 UI 受影响的功能

- 集群级别
    - 集群管理
        - 创建集群
        - 删除集群
        - 扩缩容集群
        - 暂停或恢复集群
        - 修改集群密码
        - 修改集群流量过滤器
    - 导入
        - 创建导入任务
    - 数据迁移
        - 创建迁移任务
    - Changefeed
        - 创建 changefeed 任务
    - 备份
        - 创建手动备份任务
        - 自动备份任务
    - 恢复
        - 创建恢复任务
    - 数据库审计日志
        - 测试连通性
        - 添加或删除访问记录
        - 启用或禁用数据库审计日志
        - 重启数据库审计日志
- 项目级别
    - 网络访问
        - 创建私有终端节点
        - 删除私有终端节点
        - 添加 VPC Peering
        - 删除 VPC Peering
    - 维护
        - 修改维护窗口
        - 延迟任务
    - 回收站
        - 删除集群
        - 删除备份
        - 恢复集群

### TiDB Cloud API 受影响的功能

- 集群管理
    - [CreateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateCluster)
    - [DeleteCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/DeleteCluster)
    - [UpdateCluster](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/UpdateCluster)
    - [CreateAwsCmek](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek)
- 备份
    - [CreateBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/CreateBackup)
    - [DeleteBackup](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Backup/operation/DeleteBackup)
- 恢复
    - [CreateRestoreTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Restore/operation/CreateRestoreTask)
- 导入
    - [CreateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/CreateImportTask)
    - [UpdateImportTask](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Import/operation/UpdateImportTask)

## 完成与恢复

维护成功完成后，受影响的功能将会恢复，为你带来更优质的体验。

## 获取支持

如果你有任何疑问或需要帮助，请联系 [支持团队](/tidb-cloud/tidb-cloud-support.md)。我们将及时解答你的疑问并提供必要的指导。
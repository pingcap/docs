---
title: 2023-09-26 TiDB Cloud 控制台维护通知
summary: 了解 2023 年 9 月 26 日 TiDB Cloud 控制台维护的详细信息，包括维护窗口、原因和影响。
---

# [2023-09-26] TiDB Cloud 控制台维护通知

本通知描述了你需要了解的关于 [TiDB Cloud 控制台](https://tidbcloud.com/) 在 2023 年 9 月 26 日进行维护的详细信息。

## 维护窗口

- 日期：2023-09-26
- 开始时间：8:00 (UTC+0)
- 结束时间：8:30 (UTC+0)
- 时长：约 30 分钟

> **Note:**
>
> 目前，TiDB Cloud 控制台的整体维护 schedule 不支持用户修改维护时间。

## 维护原因

我们正在升级 TiDB Cloud Starter 的管理基础设施，以提升 performance 和效率，为所有用户带来更好的体验。这是我们持续致力于提供高质量 service 的一部分。

## 影响

在维护窗口期间，你可能会在 TiDB Cloud 控制台 UI 和 API 中遇到与创建和更新相关的功能间歇性中断。然而，你的 TiDB cluster 将保持正常的数据读写操作，确保不会对你的线上业务造成不良影响。

### TiDB Cloud 控制台 UI 受影响的功能

- cluster 级别
    - cluster 管理
        - 创建 cluster
        - 删除 cluster
        - 扩缩容 cluster
        - 查看 cluster
        - 暂停或恢复 cluster
        - 修改 cluster 密码
        - 修改 cluster 流量过滤器
    - 导入
        - 创建导入任务
    - 数据 migration
        - 创建 migration 任务
    - Changefeed
        - 创建 changefeed 任务
    - 备份
        - 创建手动备份任务
        - 自动备份任务
    - 恢复
        - 创建恢复任务
    - 数据库审计日志
        - 测试连接
        - 添加或删除 access 记录
        - 启用或禁用数据库审计日志
        - 重启数据库审计日志
- 项目级别
    - 网络 access
        - 创建私有 endpoint
        - 删除私有 endpoint
        - 添加 VPC Peering
        - 删除 VPC Peering
    - 维护
        - 修改维护窗口
        - 延迟任务
    - 回收站
        - 删除 cluster
        - 删除备份
        - 恢复 cluster        

### TiDB Cloud API 受影响的功能

- 所有 [API request](https://docs.pingcap.com/tidbcloud/api/v1beta) 都会返回 500。
- [Data Service API](https://docs.pingcap.com/tidbcloud/data-service-overview) 不受影响。

## 完成与恢复

一旦维护成功完成，受影响的功能将会恢复，为你带来更优质的体验。

## 获取支持

如果你有任何问题或需要帮助，请联系 [support team](/tidb-cloud/tidb-cloud-support.md)。我们将为你解答疑问并提供必要的指导。
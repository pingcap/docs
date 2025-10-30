---
title: 2021 年 TiDB Cloud 发布说明
summary: 了解 2021 年 TiDB Cloud 的发布说明。
---

# 2021 年 TiDB Cloud 发布说明

本页面列出了 [TiDB Cloud](https://www.pingcap.com/tidb-cloud/) 在 2021 年的发布说明。

## 2021 年 12 月 28 日

新功能：

* 支持 [从 Amazon S3 或 GCS 导入 Apache Parquet 文件到 TiDB Cloud](/tidb-cloud/import-parquet-files.md)

Bug 修复：

* 修复了向 TiDB Cloud 导入超过 1000 个文件时出现的导入错误
* 修复了 TiDB Cloud 允许向已有数据的现有表导入数据的问题

## 2021 年 11 月 30 日

通用变更：

* 将 TiDB Cloud 的 Developer Tier 升级到 [TiDB v5.3.0](https://docs.pingcap.com/tidb/stable/release-5.3.0)

新功能：

* 支持 [为你的 TiDB Cloud 项目添加 VPC CIDR](/tidb-cloud/set-up-vpc-peering-connections.md)

改进：

* 提升了 Developer Tier 的监控能力
* 支持将自动备份时间设置为与 Developer Tier 集群创建时间一致

Bug 修复：

* 修复了 Developer Tier 中由于磁盘满导致的 TiKV 崩溃问题
* 修复了 HTML 注入漏洞

## 2021 年 11 月 8 日

* 上线 [Developer Tier](/tidb-cloud/select-cluster-tier.md#starter)，为你提供为期一年的 TiDB Cloud 免费试用

    每个 Developer Tier 集群都是一个全功能的 TiDB 集群，并包含以下内容：

    * 一个 TiDB 共享节点
    * 一个 TiKV 共享节点（含 500 MiB OLTP 存储）
    * 一个 TiFlash 共享节点（含 500 MiB OLAP 存储）

  立即开始使用 [这里](/tidb-cloud/tidb-cloud-quickstart.md)。

## 2021 年 10 月 21 日

* 开放用户注册支持个人邮箱账号
* 支持 [从 Amazon S3 或 GCS 导入或迁移到 TiDB Cloud](/tidb-cloud/import-csv-files.md)

## 2021 年 10 月 11 日

* 支持 [查看和导出 TiDB Cloud 的账单明细](/tidb-cloud/tidb-cloud-billing.md#billing-details)，包括每项服务和每个项目的费用
* 修复了 TiDB Cloud 内部功能的若干问题

## 2021 年 9 月 16 日

* 新部署集群的默认 TiDB 版本从 5.2.0 升级到 5.2.1。详细变更请参见 [5.2.1](https://docs.pingcap.com/tidb/stable/release-5.2.1) 发布说明。

## 2021 年 9 月 2 日

* 新部署集群的默认 TiDB 版本从 5.0.2 升级到 5.2.0。TiDB 5.1.0 和 5.2.0 的详细特性请参见 [5.2.0](https://docs.pingcap.com/tidb/stable/release-5.2.0) 和 [5.1.0](https://docs.pingcap.com/tidb/stable/release-5.1.0) 发布说明。
* 修复了 TiDB Cloud 内部功能的若干问题。

## 2021 年 8 月 19 日

* 修复了 TiDB Cloud 内部功能的若干问题。本次发布未带来任何用户行为变更。

## 2021 年 8 月 5 日

* 支持组织角色管理。组织所有者可根据需要配置组织成员的权限。
* 支持组织内多个项目的隔离。组织所有者可根据需要创建和管理项目，项目间的成员和实例支持网络与权限隔离。
* 优化账单，展示当月及上月各项明细账单。

## 2021 年 7 月 22 日

* 优化添加信用卡的用户体验
* 加强信用卡的安全管理
* 修复了从备份恢复的集群无法正常计费的问题

## 2021 年 7 月 6 日

* 新部署集群的默认 TiDB 版本从 4.0.11 升级到 5.0.2。此次升级带来了显著的性能和功能提升。详情请参见 [这里](https://docs.pingcap.com/tidb/stable/release-5.0.0)。

## 2021 年 6 月 25 日

* 修复了 [TiDB Cloud Pricing](https://www.pingcap.com/pricing/) 页面 **Select Region** 不生效的问题

## 2021 年 6 月 24 日

* 修复了将 Aurora 快照导入 TiDB 实例时 parquet 文件解析错误的问题
* 修复了 PoC 用户创建集群并更改集群配置时 Estimated Hours 未更新的问题

## 2021 年 6 月 16 日

* 注册账号时，**Country/Region** 下拉列表中新增 **China**

## 2021 年 6 月 14 日

* 修复了将 Aurora 快照导入 TiDB 实例时挂载 EBS 失败的问题

## 2021 年 5 月 10 日

通用

* TiDB Cloud 现已进入 Public Preview 阶段。你可以 [注册](https://tidbcloud.com/signup) 并选择以下试用选项之一：

    * 48 小时免费试用
    * 2 周 PoC 免费试用
    * Preview On-Demand

管理控制台

* 注册流程中新增了邮箱验证和反机器人 reCAPTCHA
* [TiDB Cloud 服务协议](https://pingcap.com/legal/tidb-cloud-services-agreement) 和 [PingCAP 隐私政策](https://pingcap.com/legal/privacy-policy/) 已更新
* 你可以在控制台填写申请表，申请 [PoC](/tidb-cloud/tidb-cloud-poc.md)
* 你可以通过 UI 向 TiDB Cloud 集群导入示例数据
* 不允许创建同名集群，以避免混淆
* 你可以通过 **Support** 菜单中的 **Give Feedback** 提交反馈
* PoC 和按需试用选项支持数据备份与恢复功能
* 免费试用和 PoC 新增积分计算器和积分使用仪表盘。所有试用选项均免除数据存储和传输费用
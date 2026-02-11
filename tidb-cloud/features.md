---
title: 功能特性
summary: 了解不同 TiDB Cloud 方案的功能支持状态。
---

# 功能特性

本文档列出了不同 TiDB Cloud 方案（包括 TiDB Cloud Starter、Essential 和 Dedicated）的功能支持状态。

> **提示：**
>
> [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 是开始体验 TiDB Cloud 的最佳方式。此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上试用 TiDB Cloud 的功能。

- ✅：该功能已**全面可用**或处于**公测**阶段。
- 🔒：该功能处于**私测**阶段。
- 🚧：该功能**开发中**。
- ❌：该功能**当前不可用**。

<table><thead>
  <tr>
    <th>类别</th>
    <th>功能</th>
    <th style="text-align:center;">Starter</th>
    <th style="text-align:center;">Essential</th>
    <th style="text-align:center;">Dedicated</th>
  </tr></thead>
<tbody>
  <tr>
    <td rowspan="4" style="background-color: white;">基础</td>
    <td>可扩展的事务处理</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>分析型处理</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>向量存储 &amp; 向量检索</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
  </tr>
  <tr>
    <td>API</td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">开发者体验</td>
    <td>数据分支</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>SQL 编辑器</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td rowspan="7" style="background-color: white;">集群管理</td>
    <td>按需付费</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>基于负载的自动扩缩容</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>手动集群修改</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>密码设置</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>暂停 &amp; 恢复</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>系统维护窗口</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>备份文件回收站</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="4" style="background-color: white;">数据处理</td>
    <td>从 CSV、Parquet 和 SQL 文件导入数据到 TiDB Cloud</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>从 MySQL 兼容数据库迁移数据到 TiDB Cloud</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>通过 CSV、Parquet 和 SQL 文件导出数据到本地或对象存储</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>通过 changefeed 将变更数据同步到 Kafka 或其他 MySQL 兼容数据库</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公测）</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="5" style="background-color: white;">备份 &amp; 恢复</td>
    <td>自动备份</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>手动备份</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>双区域备份</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>时间点恢复（PITR）</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>恢复</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="7" style="background-color: white;">可观测性</td>
    <td>内置指标</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>告警</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">🚧</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>SQL 语句分析</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>慢查询日志</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Top SQL</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>事件</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>第三方集成，如 Datadog、Prometheus 和 New Relic</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="1" style="background-color: white;">高可用性</td>
    <td>跨可用区故障切换</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">资源分配</td>
    <td>节点组</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>资源控制</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="3" style="background-color: white;">网络连接</td>
    <td>私有端口</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>公网端口</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>VPC 对等连接</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="6" style="background-color: white;">安全</td>
    <td>数据库审计日志</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">🔒</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>控制台审计日志</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>日志脱敏</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>CMEK</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>双层加密</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>IAM（包括邮箱和密码登录、标准 SSO 及组织 SSO）</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <CustomContent language="en,zh">
  <tr>
    <td rowspan="4" style="background-color: white;">云平台与区域</td>
    <td>AWS</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>阿里云</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>Azure</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Google Cloud</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  </CustomContent>
  <CustomContent language="ja">
  <tr>
    <td rowspan="3" style="background-color: white;">Cloud and regions</td>
    <td>AWS</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Azure</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>Google Cloud</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  </CustomContent>
</tbody></table>

> **提示：**
>
> 如需申请私测功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 跳转到 [帮助中心](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段填写 “Apply for `<feature_name>`”，然后点击 **Submit**。
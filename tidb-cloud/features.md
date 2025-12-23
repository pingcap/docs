---
title: 功能特性
summary: 了解不同 TiDB Cloud 方案的功能支持状态。
---

# 功能特性

本文档列出了不同 TiDB Cloud 方案（包括 TiDB Cloud Starter、Essential 和 Dedicated）的功能支持状态。

> **提示：**
>
> [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 是开始体验 TiDB Cloud 的最佳方式。此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上试用 TiDB Cloud 的功能。

- ✅：该功能已普遍可用，除非另有说明为预览版。
- ❌：该功能当前不可用。

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
    <td rowspan="3" style="background-color: white;">基础</td>
    <td>TiKV</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>TiFlash</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>API</td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center;">✅<br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
  </tr>
  <tr>
    <td rowspan="3" style="background-color: white;">集群管理</td>
    <td>暂停与恢复</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>维护窗口</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>回收站</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">数据导入</td>
    <td>导入（使用 <code>IMPORT INTO</code> 或 TiDB Cloud 控制台）</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>数据迁移</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（私有预览）</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">数据导出</td>
    <td>导出</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center; font-size: 14px;">❌</td>
  </tr>
  <tr>
    <td>变更数据订阅（Changefeed）</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（CLI 私有预览）</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="4" style="background-color: white;">备份与恢复</td>
    <td>自动备份</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>双区域备份</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>手动备份</td>
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
    <td style="background-color: white;">存储</td>
    <td>标准存储</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
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
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>SQL 语句</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>慢查询</td>
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
    <td>第三方集成</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="2" style="background-color: white;">高可用性</td>
    <td>故障转移（跨可用区）</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>恢复组（跨区域）</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
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
    <td rowspan="7" style="background-color: white;">安全</td>
    <td>私有端点</td>
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
    <td>数据库审计日志</td>
    <td style="text-align:center; font-size: 14px;">❌</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（私有预览）</span></td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>控制台审计日志</td>
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
    <td>日志脱敏</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td>双层加密</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
    <td style="text-align:center;">✅</td>
  </tr>
  <tr>
    <td rowspan="3" style="background-color: white;">AI 与开发</td>
    <td>向量检索</td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
    <td style="text-align:center;">✅ <br/><span style="font-size: 14px; white-space: nowrap;">（公开预览）</span></td>
  </tr>
  <tr>
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
    <td rowspan="4" style="background-color: white;">云与区域</td>
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
</tbody></table>

> **提示：**
>
> 如需申请私有预览功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Request Support**。接着，在 **Description** 字段中填写功能名称，并点击 **Submit**。
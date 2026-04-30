---
title: 通过公共连接连接到 {{{ .premium }}}
summary: 了解如何通过公共连接连接到你的 {{{ .premium }}}。
---

# 通过公共连接连接到 {{{ .premium }}}

本文档介绍如何通过公共连接连接到你的 {{{ .premium }}} 实例。公共连接会暴露一个带有流量过滤器的公共端点，因此你可以通过笔记本电脑上的 SQL 客户端连接到你的 {{{ .premium }}} 实例。

> **Tip:**
>
> - 如需了解如何通过公共连接连接到 {{{ .starter }}} 或 {{{ .essential }}} 实例，请参见 [通过公共端点连接到 {{{ .starter }}} 或 Essential](/tidb-cloud/connect-via-standard-connection-serverless.md)。
> - 如需了解如何通过公共端点连接到 TiDB Cloud Dedicated 集群，请参见 [通过公共连接连接到 TiDB Cloud Dedicated](/tidb-cloud/connect-via-standard-connection.md)。

## 前提条件：配置 IP 访问列表 {#prerequisite-configure-ip-access-list}

对于公共连接，{{{ .premium }}} 仅允许来自 IP 访问列表中地址的客户端连接。如果你尚未配置 IP 访问列表，请先按照 [配置 IP 访问列表](/tidb-cloud/premium/configure-ip-access-list-premium.md) 中的步骤进行配置，然后再进行首次连接。

## 连接到实例 {#connect-to-the-instance}

要通过公共连接连接到 {{{ .premium }}} 实例，请执行以下步骤：

1. 打开目标实例的概览页面。

    1. 登录 [TiDB Cloud console](https://tidbcloud.com/) 并导航到 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **Tip:**
        >
        > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

    2. 点击目标实例的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会显示连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    如果你尚未配置 IP 访问列表，请点击 **Configure IP Access List**，或按照 [配置 IP 访问列表](/tidb-cloud/premium/configure-ip-access-list-premium.md) 中的步骤在首次连接前完成配置。

4. 点击 **CA cert** 下载用于与 {{{ .premium }}} 实例建立 TLS 连接的 CA cert。该 CA cert 默认支持 TLS 1.2。

5. 选择你偏好的连接方法，然后参考对应标签页中的连接字符串和示例代码连接到你的实例。

## 后续操作 {#what-s-next}

成功连接到你的 {{{ .premium }}} 实例后，你可以[使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。
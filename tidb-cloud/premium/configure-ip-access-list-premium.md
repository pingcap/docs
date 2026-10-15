---
title: 为 {{{ .premium }}} 或 {{{ .byoc }}} 配置 IP 访问列表
summary: 了解如何配置允许访问你的 {{{ .premium }}} 或 {{{ .byoc }}} 实例的 IP 地址。
---

# 为 {{{ .premium }}} 或 {{{ .byoc }}} 配置 IP 访问列表

对于 TiDB Cloud 中的每个 {{{ .premium }}} 或 {{{ .byoc }}} 实例，你都可以配置一个 IP 访问列表，用于过滤尝试访问该实例的互联网流量，其工作方式类似于防火墙访问控制列表。完成配置后，只有 IP 地址位于该 IP 访问列表中的客户端和应用程序才能连接到你的 {{{ .premium }}} 或 {{{ .byoc }}} 实例。

> **注意：**
>
> - 本文档适用于 **{{{ .premium }}}** 和 **{{{ .byoc }}}**。有关为 **{{{ .starter }}}** 或 **{{{ .essential }}}** 配置 IP 访问列表的说明，请参见 [配置 TiDB Cloud Starter 或 Essential 公共端点的防火墙规则](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。
> - 对于 {{{ .byoc }}}，仅当你在 BYOC 部署期间提供公共托管区域时，公共连接才可用。如果你提供的是私有托管区域，请使用私有连接连接到你的实例。

要为你的 {{{ .premium }}} 或 {{{ .byoc }}} 实例配置 IP 访问列表，请执行以下步骤：

1. 前往 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .premium }}} 或 {{{ .byoc }}} 实例的名称，进入其实例概览页面。

    > **提示：**
    >
    > 如果你属于多个组织，请先使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Settings** > **Networking**。
3. 在 **Networking** 页面中，点击 **Public Endpoint** 的 **Enable** 以使该实例可通过公共端点访问，然后点击 **Add IP Address**。
4. 在显示的对话框中，选择以下选项之一：

    - **Allow access from anywhere**：允许所有 IP 地址访问 TiDB Cloud。此选项会将你的实例完全暴露在互联网中，风险极高。
    - **Use IP addresses**（推荐）：你可以添加一个 IP 和 CIDR 地址列表，以允许通过 SQL 客户端访问 TiDB Cloud。

5. 如果你选择 **Use IP addresses**，请添加 IP 地址或 CIDR 范围，并可选择填写描述。
6. 点击 **Confirm** 保存更改。
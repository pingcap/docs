---
title: 配置集群密码设置
summary: 了解如何配置 root 密码以连接到你的集群。
---

# 配置集群密码设置

对于 TiDB Cloud Dedicated 集群，你可以配置 root 密码以及允许连接到你集群的 IP 地址。

> **注意：**
>
> 对于 TiDB Cloud Serverless 集群，本篇文档不适用，你可以参考 [TLS Connection to TiDB Cloud Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md)。

1. 在 TiDB Cloud 控制台中，进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 在目标集群所在的行，点击 **...** 并选择 **Password Settings**。
3. 设置连接到你集群的 root 密码，然后点击 **Save**。

    你可以点击 **Auto-generate Password** 自动生成一个随机密码。生成的密码不会再次显示，请将你的密码保存在安全的位置。

> **提示：**
>
> 如果你正在查看集群的概览页面，也可以点击页面右上角的 **...**，选择 **Password Settings**，并进行相关设置。
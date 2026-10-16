---
title: 管理 TiDB Cloud Filesystem 使用限制
summary: 了解如何在 TiDB Cloud 控制台中查看文件系统用量和免费限制，以及如何在添加信用卡后修改使用限制。
---

# 管理 TiDB Cloud Filesystem 使用限制

你可以在不绑定信用卡的情况下，在 TiDB Cloud Filesystem 服务中创建和使用文件系统，但每个免费文件系统的容量限制会更严格。向组织添加信用卡后，你可以提高这些限制。

## 未绑定信用卡的组织的使用限制 {#usage-limits-for-organizations-without-a-credit-card}

当你的组织**未注册信用卡**时，每个免费文件系统适用以下限制：

- 每个 region 一个文件系统
- 每个文件系统 2,000 个文件
- 每个文件系统 2 GiB 存储空间
- 单个文件最大 500 MiB

绑定信用卡后，你可以设置更高的限制，并继续按量付费使用。有关计费详情，请参见[TiDB Cloud Filesystem pricing](https://www.pingcap.com/tidb-cloud-filesystem-pricing-details/)。

## 查看文件系统用量 {#view-file-system-usage}

要查看文件系统的当前用量，请前往 [TiDB Cloud 控制台](https://tidbcloud.com/)中该文件系统的概览页面，并查看 **Usage** 区域。要查看用量详情，请点击左侧导航栏中的 **Usage**。

## 当文件系统达到使用限制时 {#when-a-file-system-reaches-a-usage-limit}

当文件系统达到其存储空间或文件数量限制时，现有文件仍可读取，但文件系统将停止接受新的写入。单个文件也不能增长到超过文件大小限制。每个 region 仅允许一个文件系统的限制，会在你尝试在该 region 中创建另一个文件系统时生效。TiDB Cloud 控制台会显示警告。

## 修改使用限制 {#update-the-usage-limits}

1. 在 TiDB Cloud 控制台中，前往 [**File Systems**](https://tidbcloud.com/filesystems) 页面，选择该文件系统对应的 **Cloud Provider** 和 **Region**，然后点击目标文件系统的名称。
2. 在文件系统的概览页面中，点击 **Usage** 区域中的 **Edit Usage Limit**。
3. 根据需要设置最大存储空间、文件数量和文件大小，然后点击 **Save**。

    如果你的组织未绑定信用卡，这些字段会被禁用。添加信用卡后即可修改这些字段，并启用按量付费使用。
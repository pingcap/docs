---
title: 删除 {{{ .premium }}} 或 {{{ .byoc }}} 实例
summary: 了解如何删除 {{{ .premium }}} 或 {{{ .byoc }}} 实例。
---

# 删除 {{{ .premium }}} 或 {{{ .byoc }}} 实例

本文档介绍如何删除 {{{ .premium }}} 或 {{{ .byoc }}} 实例。

你可以随时按照以下步骤删除一个实例：

1. 前往 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。
2. 在要删除的目标实例所在行中，点击 **...**。

    > **Tip:**
    >
    > 或者，你也可以点击目标实例名称进入其实例概览页面，然后点击右上角的 **...**。

3. 在下拉菜单中点击 **Delete**。
4. 在删除确认窗口中，确认删除操作：

    输入 `<organization name>/<instance name>` 以确保正确删除该实例。

    如果你希望将来某个时间恢复该实例，请确保你已经拥有该实例的备份。否则，你将无法恢复它。有关如何备份 {{{ .premium }}} 或 {{{ .byoc }}} 实例的更多信息，请参见[备份与恢复 {{{ .premium }}} 或 {{{ .byoc }}} 数据](/tidb-cloud/premium/backup-and-restore-premium.md)。

5. 点击 **I understand, delete it**。

    删除已备份的 {{{ .premium }}} 或 {{{ .byoc }}} 实例后，该实例现有的备份文件会被移至回收站。

    自动备份会在保留时间结束后过期并被自动删除。如果你未修改，默认保留时间为 7 天。

    <CustomContent plan="premium">

    > **Note:**
    >
    > 备份在被删除之前将持续产生费用。

    </CustomContent>

    <CustomContent plan="byoc">

    > **Note:**
    >
    > 对于 BYOC 实例，TiDB Cloud 不对备份收费。您需要自行承担云账户中产生的存储和数据传输费用。在备份文件被删除之前，存储费用会持续产生。

    </CustomContent>

    如果你想从回收站恢复 {{{ .premium }}} 或 {{{ .byoc }}} 实例，请参见[从回收站恢复](/tidb-cloud/premium/backup-and-restore-premium.md#restore-from-recycle-bin)。

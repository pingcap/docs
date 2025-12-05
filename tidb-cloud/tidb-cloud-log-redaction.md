---
title: 用户可控的日志脱敏
summary: 了解如何在 TiDB Cloud 中启用或禁用用户可控的日志脱敏功能，以管理执行日志中敏感数据的可见性。
---

# 用户可控的日志脱敏

用户可控的日志脱敏功能允许你管理 <CustomContent plan="dedicated">[TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群</CustomContent><CustomContent plan="premium">TiDB Cloud 高级版实例</CustomContent>日志中敏感数据的可见性。通过切换该脱敏功能，你可以保护你的信息，在运维需求与安全之间取得平衡，并控制在 <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>日志中显示的内容。

日志脱敏功能默认启用，确保运行日志和执行计划中的敏感信息被隐藏。如果你需要获取更详细的日志信息以便 <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>维护或 SQL 调优，可以随时禁用该功能。

<CustomContent plan="dedicated">

> **注意：**
>
> 日志脱敏功能仅支持 TiDB Cloud Dedicated 集群。

</CustomContent>

<CustomContent plan="premium">

> **注意：**
>
> 日志脱敏功能支持 TiDB Cloud Dedicated 集群和 TiDB Cloud Premium 实例。

</CustomContent>

## 前置条件

<CustomContent plan="dedicated">

* 你必须是 TiDB Cloud 中组织的 **Organization Owner** 或 **Project Owner** 角色。
* 当集群处于 `paused` 状态时，无法启用或禁用日志脱敏功能。

</CustomContent>

<CustomContent plan="premium">

* 你必须是 TiDB Cloud 中组织的 **Organization Owner** 角色。

</CustomContent>

## 禁用日志脱敏

> **警告：**
>
> 禁用日志脱敏可能会暴露敏感信息，增加数据泄露的风险。在操作前请确保你已理解并知晓相关风险。请在完成诊断或维护任务后，及时重新启用该功能。

要禁用日志脱敏，请按以下步骤操作：

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)。
2. 进入 <CustomContent plan="dedicated">[**Clusters**](https://tidbcloud.com/project/clusters)</CustomContent><CustomContent plan="premium">[**TiDB Instances**](https://tidbcloud.com/tidbs)</CustomContent> 页面，然后点击目标 <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>的名称，进入其概览页面。

    <CustomContent plan="dedicated">

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    </CustomContent>

    <CustomContent plan="premium">

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织和实例之间切换。

    </CustomContent>

3. 在左侧导航栏，点击 **Settings** > **Security**。
4. 在 **Execution Log Redaction** 部分，你可以看到脱敏功能默认是 **Enabled**。
5. 点击 **Disable**。此时会弹出警告，说明禁用日志脱敏的风险。
6. 确认禁用操作。

禁用日志脱敏后，请注意以下事项：

* 该更改仅对新的数据库连接生效。
* 已有的连接不受影响。你需要重新连接，变更才会生效。
* 新会话的日志将不再被脱敏。

## 检查更新后的日志

禁用日志脱敏后，如需检查更新后的日志，请按以下步骤操作：

1. 模拟一个由慢查询引起的性能问题。例如，执行以下 SQL 语句：

    ```sql
    SELECT *, SLEEP(2) FROM users WHERE email LIKE "%useremail%";
    ```

2. 等待几分钟，直到慢查询日志更新。
3. 检查日志，确认敏感数据未被脱敏。

## 启用日志脱敏

为保障数据安全，在完成诊断或维护任务后，请**及时启用日志脱敏**，操作如下。

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)。
2. 进入 <CustomContent plan="dedicated">[**Clusters**](https://tidbcloud.com/project/clusters)</CustomContent><CustomContent plan="premium">[**TiDB Instances**](https://tidbcloud.com/tidbs)</CustomContent> 页面，然后点击目标 <CustomContent plan="dedicated">集群</CustomContent><CustomContent plan="premium">实例</CustomContent>的名称，进入其概览页面。

    <CustomContent plan="dedicated">

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

    </CustomContent>

    <CustomContent plan="premium">

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织和实例之间切换。

    </CustomContent>

3. 在左侧导航栏，点击 **Settings** > **Security**。
4. 在 **Execution Log Redaction** 部分，你可以看到脱敏功能当前为 **Disabled**。
5. 点击 **Enable** 以启用该功能。
6. 重新连接数据库，新会话才会生效。
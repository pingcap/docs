---
title: 身份访问管理
summary: 了解如何在 TiDB Cloud 中管理身份访问。
---

# 身份访问管理

本文档介绍如何在 TiDB Cloud 中管理对组织、项目、角色和用户资料的访问。

在访问 TiDB Cloud 之前，请先[创建一个 TiDB Cloud 账户](https://tidbcloud.com/free-trial)。你可以使用邮箱和密码注册，这样可以[通过 TiDB Cloud 管理你的密码](/tidb-cloud/tidb-cloud-password-authentication.md)，也可以选择使用 Google、GitHub 或 Microsoft 账户进行单点登录（SSO）到 TiDB Cloud。

## 组织与项目

TiDB Cloud 提供了基于组织和项目的分层结构，便于管理 TiDB Cloud 用户和集群。如果你是组织所有者，可以在你的组织下创建多个项目。

例如：

```
- Your organization
    - Project 1
        - Cluster 1
        - Cluster 2
    - Project 2
        - Cluster 3
        - Cluster 4
    - Project 3
        - Cluster 5
        - Cluster 6
```

在该结构下：

- 要访问某个组织，用户必须是该组织的成员。
- 要访问组织中的某个项目，用户至少需要拥有该组织下该项目的只读权限。
- 要管理项目中的集群，用户必须拥有 `Project Owner` 角色。

关于用户角色和权限的更多信息，请参见 [用户角色](#用户角色)。

### 组织

一个组织可以包含多个项目。

TiDB Cloud 在组织层面进行计费，并为每个项目提供账单明细。

如果你是组织所有者，你在组织中拥有最高权限。

例如，你可以执行以下操作：

- 为不同目的创建不同的项目（如开发、测试和生产环境）。
- 为不同用户分配不同的组织角色和项目角色。
- 配置组织设置。例如，为你的组织配置时区。

### 项目

一个项目可以包含多个集群。

如果你是项目所有者，可以管理你项目下的集群和项目设置。

例如，你可以执行以下操作：

- 根据业务需求创建多个集群。
- 为不同用户分配不同的项目角色。
- 配置项目设置。例如，为不同项目配置不同的告警设置。

## 用户角色

TiDB Cloud 定义了不同的用户角色，用于管理 TiDB Cloud 用户在组织、项目或两者中的不同权限。

你可以在组织层面或项目层面为用户授予角色。请确保为安全考虑，合理规划你的组织和项目的层级结构。

### 组织角色

在组织层面，TiDB Cloud 定义了四种角色，其中 `Organization Owner` 可以邀请成员并为成员分配组织角色。

| 权限  | `Organization Owner` | `Organization Billing Manager` | `Organization Billing Viewer` | `Organization Console Audit Manager` | `Organization Viewer` |
|---|---|---|---|---|---|
| 管理组织设置，如项目、API 密钥和时区。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 邀请用户加入或移除用户出组织，并编辑用户的组织角色。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 拥有该组织下所有项目的 `Project Owner` 权限。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 创建启用客户管理加密密钥（CMEK）的项目。 | ✅ | ❌ | ❌ | ❌ | ❌ |
| 编辑组织的支付信息。 | ✅ | ✅ | ❌ | ❌ | ❌ |
| 查看账单并使用 [成本分析器](/tidb-cloud/tidb-cloud-billing.md#cost-explorer)。 | ✅ | ✅ | ✅ | ❌ | ❌ |
| 管理组织的 TiDB Cloud [控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)。 | ✅ | ❌ | ❌ | ✅ | ❌ |
| 查看组织内的用户及成员所属的项目。 | ✅ | ✅ | ✅ | ✅ | ✅ |

> **注意：**
>
> - `Organization Console Audit Manager` 角色（由 `Organization Console Audit Admin` 重命名）用于管理 TiDB Cloud 控制台的审计日志，而非数据库审计日志。要管理数据库审计，请在项目层面使用 `Project Owner` 角色。
> - `Organization Billing Manager` 角色由 `Organization Billing Admin` 重命名，`Organization Viewer` 角色由 `Organization Member` 重命名。

### 项目角色

在项目层面，TiDB Cloud 定义了三种角色，其中 `Project Owner` 可以邀请成员并为成员分配项目角色。

> **注意：**
>
> - `Organization Owner` 拥有所有项目的 <code>Project Owner</code> 权限，因此 `Organization Owner` 也可以邀请项目成员并为成员分配项目角色。
> - 每个项目角色默认拥有 <code>Organization Viewer</code> 的所有权限。
> - 如果你组织中的某个用户不属于任何项目，则该用户没有任何项目权限。

| 权限  | `Project Owner` | `Project Data Access Read-Write` | `Project Data Access Read-Only` | `Project Viewer` |
|---|---|---|---|---|
| 管理项目设置 | ✅ | ❌ | ❌ | ❌ |
| 邀请用户加入或移除用户出项目，并编辑用户的项目角色。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目的 [数据库审计日志](/tidb-cloud/tidb-cloud-auditing.md)。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目下所有 TiDB Cloud Serverless 集群的 [消费限额](/tidb-cloud/manage-serverless-spend-limit.md)。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目中的集群操作，如集群创建、修改和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目下 TiDB Cloud Serverless 集群的分支，如分支创建、连接和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理项目下 TiDB Cloud Dedicated 集群的 [恢复组](/tidb-cloud/recovery-group-overview.md)，如恢复组的创建和删除。 | ✅ | ❌ | ❌ | ❌ |
| 管理集群数据，如数据导入、数据备份与恢复、数据迁移。 | ✅ | ✅ | ❌ | ❌ |
| 管理 [Data Service](/tidb-cloud/data-service-overview.md) 的只读操作，如使用或创建端点读取数据。 | ✅ | ✅ | ✅ | ❌ |
| 管理 [Data Service](/tidb-cloud/data-service-overview.md) 的读写操作。 | ✅ | ✅ | ❌ | ❌ |
| 使用 [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md) 查看集群数据。 | ✅ | ✅ | ✅ | ❌ |
| 使用 [SQL Editor](/tidb-cloud/explore-data-with-chat2query.md) 修改和删除集群数据。 | ✅ | ✅ | ❌ | ❌ |
| 管理 [changefeeds](/tidb-cloud/changefeed-overview.md)。 | ✅ | ✅ | ✅ | ❌ |
| 审核和重置集群密码。 | ✅ | ❌ | ❌ | ❌ |
| 查看项目中的集群概览、备份记录、监控指标、事件和 [changefeeds](/tidb-cloud/changefeed-overview.md)。 | ✅ | ✅ | ✅ | ✅ |

## 管理组织访问

### 查看并切换组织

要查看并切换组织，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左上角的下拉框，会显示你所属的组织和项目列表。

    > **提示：**
    >
    > - 如果你当前在某个集群页面，点击左上角下拉框后，还需要在下拉框中点击 ← 返回到组织和项目列表。
    > - 如果你属于多个组织，可以在下拉框中点击目标组织名称，在组织之间切换账户。

2. 若要查看组织的详细信息（如组织 ID 和时区），点击组织名称，然后在左侧导航栏点击 **Organization Settings** > **General**。

### 设置组织时区

如果你拥有 `Organization Owner` 角色，可以根据你的时区修改系统显示时间。

要更改本地时区设置，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **General**。

3. 在 **Time Zone** 区域，从下拉列表中选择你的时区。

4. 点击 **Update**。

### 邀请组织成员

如果你拥有 `Organization Owner` 角色，可以邀请用户加入你的组织。

> **注意：**
>
> 你也可以根据需要[直接邀请用户加入你的项目](#invite-a-project-member)，这同样会使该用户成为你的组织成员。

要邀请成员加入组织，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 点击 **Invite**。

5. 输入要邀请用户的邮箱地址，然后为该用户选择一个组织角色。

    > **提示：**
    >
    > - 如果你想一次邀请多个成员，可以输入多个邮箱地址。
    > - 被邀请用户默认不属于任何项目。要邀请用户加入项目，请参见 [邀请项目成员](#invite-a-project-member)。

6. 点击 **Confirm**。新用户会被成功添加到用户列表，同时会向被邀请邮箱发送一封带有验证链接的邮件。

7. 用户收到邮件后，需要点击邮件中的链接进行身份验证，页面会显示新的内容。

8. 如果被邀请邮箱尚未注册 TiDB Cloud 账户，用户会被引导至注册页面创建账户；如果邮箱已注册 TiDB Cloud 账户，用户会被引导至登录页面，登录后账户会自动加入组织。

> **注意：**
>
> 邮件中的验证链接 24 小时内有效。如果你要邀请的用户未收到邮件，可点击 **Resend** 重新发送。

### 修改组织角色

如果你拥有 `Organization Owner` 角色，可以修改组织内所有成员的组织角色。

要修改成员的组织角色，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 点击目标成员的角色，然后进行修改。

### 移除组织成员

如果你拥有 `Organization Owner` 角色，可以将组织成员从你的组织中移除。

要将成员从组织中移除，请执行以下步骤：

> **注意：**
>
> 如果成员被移除出组织，该成员也会被移除出其所属的项目。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Organization** 标签页。

4. 在目标成员所在行，点击 **...** > **Delete**。

## 管理项目访问

### 查看并切换项目

要查看并切换项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左上角的下拉框，会显示你所属的组织和项目列表。

    > **提示：**
    >
    > - 如果你当前在某个集群页面，点击左上角下拉框后，还需要在下拉框中点击 ← 返回到组织和项目列表。
    > - 如果你属于多个项目，可以在下拉框中点击目标项目名称，在项目之间切换。

2. 若要查看项目的详细信息，点击项目名称，然后在左侧导航栏点击 **Project Settings**。

### 创建项目

> **注意：**
>
> 免费试用用户无法创建新项目。

如果你拥有 `Organization Owner` 角色，可以在你的组织下创建项目。

要创建新项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Projects**。

3. 在 **Projects** 页面，点击 **Create New Project**。

4. 输入你的项目名称。

5. 点击 **Confirm**。

### 重命名项目

如果你拥有 `Organization Owner` 角色，可以重命名你组织下的任意项目。如果你拥有 `Project Owner` 角色，可以重命名你的项目。

要重命名项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Projects**。

3. 在要重命名的项目所在行，点击 **...** > **Rename**。

4. 输入新的项目名称。

5. 点击 **Confirm**。

### 邀请项目成员

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以邀请成员加入你的项目。

> **注意：**
>
> 当某个不在你组织内的用户加入你的项目时，该用户也会自动加入你的组织。

要邀请成员加入项目，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 点击 **Invite**。

5. 输入要邀请用户的邮箱地址，然后为该用户选择一个项目角色。

    > **提示：**
    >
    > 如果你想一次邀请多个成员，可以输入多个邮箱地址。

6. 点击 **Confirm**。新用户会被成功添加到用户列表，同时会向被邀请邮箱发送一封带有验证链接的邮件。

7. 用户收到邮件后，需要点击邮件中的链接进行身份验证，页面会显示新的内容。

8. 如果被邀请邮箱尚未注册 TiDB Cloud 账户，用户会被引导至注册页面创建账户；如果邮箱已注册 TiDB Cloud 账户，用户会被引导至登录页面，登录后账户会自动加入项目。

> **注意：**
>
> 邮件中的验证链接 24 小时内有效。如果你的用户未收到邮件，可点击 **Resend** 重新发送。

### 修改项目角色

如果你拥有 `Organization Owner` 角色，可以修改你组织下所有项目成员的项目角色。如果你拥有 `Project Owner` 角色，可以修改你项目下所有成员的项目角色。

要修改成员的项目角色，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 在目标成员所在行，点击 **Role** 列中的角色，然后从下拉列表中选择新角色。

### 移除项目成员

如果你拥有 `Organization Owner` 或 `Project Owner` 角色，可以移除项目成员。

要将成员从项目中移除，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，使用左上角下拉框切换到目标组织。

2. 在左侧导航栏点击 **Organization Settings** > **Users**。

3. 在 **Users** 页面，点击 **By Project** 标签页，然后在下拉列表中选择你的项目。

4. 在目标成员所在行，点击 **...** > **Delete**。

## 管理用户资料

在 TiDB Cloud 中，你可以轻松管理你的个人资料，包括名字、姓氏和手机号。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)中，点击左下角的 <MDSvgIcon name="icon-top-account-settings" />。

2. 点击 **Account Settings**。

3. 在弹出的对话框中，更新个人资料信息，然后点击 **Update**。
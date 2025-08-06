---
title: 控制台审计日志
summary: 了解 TiDB Cloud 控制台的审计日志功能。
---

# 控制台审计日志

TiDB Cloud 提供了控制台审计日志功能，帮助你追踪用户在 [TiDB Cloud 控制台](https://tidbcloud.com) 上的各种行为和操作。例如，你可以追踪邀请用户加入你的组织、创建集群等操作。

## 前提条件

- 你必须是 TiDB Cloud 组织中的 `Organization Owner` 或 `Organization Console Audit Manager` 角色。否则，你无法在 TiDB Cloud 控制台中看到与控制台审计日志相关的选项。
- 你只能为你的组织启用和禁用控制台审计日志。你只能追踪你所在组织用户的操作。
- 启用控制台审计日志后，TiDB Cloud 控制台的所有事件类型都会被审计，无法只指定审计其中的部分事件。

## 启用控制台审计日志

控制台审计日志功能默认处于禁用状态。要启用该功能，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Console Audit Logging**。
3. 点击右上角的 **Settings**，启用控制台审计日志，然后点击 **Update**。

## 禁用控制台审计日志

要禁用控制台审计日志，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Console Audit Logging**。
3. 点击右上角的 **Settings**，禁用控制台审计日志，然后点击 **Update**。

## 查看控制台审计日志

你只能查看你所在组织的控制台审计日志。

> **注意：**
>
> - 如果你的组织是第一次启用控制台审计日志，控制台审计日志内容为空。在执行任何被审计的事件后，你会看到相应的日志。
> - 如果控制台审计日志被禁用已超过 90 天，你将无法看到任何日志。

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Console Audit Logging**。
3. 如需获取特定部分的审计日志，可以筛选事件类型、操作状态和时间范围。
4. （可选）如需筛选更多字段，点击 **Advanced filter**，添加更多筛选条件，然后点击 **Apply**。
5. 点击某一日志行，可在右侧面板查看其详细信息。

## 导出控制台审计日志

要导出你所在组织的控制台审计日志，请按照以下步骤操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航栏中，点击 **Console Audit Logging**。
3. （可选）如需导出特定部分的控制台审计日志，可以通过多种条件进行筛选。否则可跳过此步骤。
4. 点击 **Download logs**，并选择所需的导出格式（JSON 或 CSV）。

## 控制台审计日志存储策略

控制台审计日志的存储时间为 90 天，超过后日志会被自动清理。

> **注意：**
>
> - 你无法在 TiDB Cloud 中指定控制台审计日志的存储位置。
> - 你无法手动删除审计日志。

## 控制台审计事件类型

控制台审计日志通过事件类型记录用户在 TiDB Cloud 控制台上的各种活动。

> **注意：**
>
> 目前，TiDB Cloud 控制台的大多数事件类型都可以被审计，你可以在下表中找到它们。对于尚未覆盖的事件类型，TiDB Cloud 会持续完善并纳入审计范围。

| 控制台审计事件类型                  | 描述                                                                 |
|-------------------------------------|----------------------------------------------------------------------|
| CreateOrganization                  | 创建组织                                                             |
| LoginOrganization                   | 登录组织                                                             |
| SwitchOrganization                  | 从当前组织切换到其他组织                                             |
| LogoutOrganization                  | 退出组织                                                             |
| InviteUserToOrganization            | 邀请用户加入组织                                                     |
| DeleteInvitationToOrganization      | 删除用户加入组织的邀请                                               |
| ResendInvitationToOrganization      | 重新发送用户加入组织的邀请                                           |
| ConfirmJoinOrganization             | 被邀请用户确认加入组织                                               |
| DeleteUserFromOrganization          | 删除已加入组织的用户                                                 |
| UpdateUserRoleInOrganization        | 更新组织中用户的角色                                                 |
| CreateAPIKey                        | 创建 API Key                                                         |
| EditAPIKey                          | 编辑 API Key                                                         |
| DeleteAPIKey                        | 删除 API Key                                                         |
| UpdateTimezone                      | 更新组织的时区                                                       |
| ShowBill                            | 查看组织账单                                                         |
| DownloadBill                        | 下载组织账单                                                         |
| ShowCredits                         | 查看组织积分                                                         |
| AddPaymentCard                      | 添加支付卡                                                           |
| UpdatePaymentCard                   | 更新支付卡                                                           |
| DeletePaymentCard                   | 删除支付卡                                                           |
| SetDefaultPaymentCard               | 设置默认支付卡                                                       |
| EditBillingProfile                  | 编辑账单信息                                                         |
| ContractAction                      | 组织合同相关操作                                                     |
| EnableConsoleAuditLog               | 启用控制台审计日志                                                   |
| ShowConsoleAuditLog                 | 查看控制台审计日志                                                   |
| InviteUserToProject                 | 邀请用户加入项目                                                     |
| DeleteInvitationToProject           | 删除用户加入项目的邀请                                               |
| ResendInvitationToProject           | 重新发送用户加入项目的邀请                                           |
| ConfirmJoinProject                  | 被邀请用户确认加入项目                                               |
| DeleteUserFromProject               | 删除已加入项目的用户                                                 |
| CreateProject                       | 创建项目                                                             |
| CreateProjectCIDR                   | 创建新的项目 CIDR                                                    |
| CreateAWSVPCPeering                 | 创建 AWS VPC Peering                                                 |
| DeleteAWSVPCPeering                 | 删除 AWS VPC Peering                                                 |
| CreateGCPVPCPeering                 | 创建 Google Cloud VPC Peering                                        |
| DeleteGCPVPCPeering                 | 删除 Google Cloud VPC Peering                                        |
| CreatePrivateEndpointService        | 创建私有终端节点服务                                                 |
| DeletePrivateEndpointService        | 删除私有终端节点服务                                                 |
| CreateAWSPrivateEndPoint            | 创建 AWS 私有终端节点                                                |
| DeleteAWSPrivateEndPoint            | 删除 AWS 私有终端节点                                                |
| SubscribeAlerts                     | 订阅告警                                                             |
| UnsubscribeAlerts                   | 取消订阅告警                                                         |
| CreateDatadogIntegration            | 创建 datadog 集成                                                    |
| DeleteDatadogIntegration            | 删除 datadog 集成                                                    |
| CreateVercelIntegration             | 创建 vercel 集成                                                     |
| DeleteVercelIntegration             | 删除 vercel 集成                                                     |
| CreatePrometheusIntegration         | 创建 Prometheus 集成                                                 |
| DeletePrometheusIntegration         | 删除 Prometheus 集成                                                 |
| CreateCluster                       | 创建集群                                                             |
| DeleteCluster                       | 删除集群                                                             |
| PauseCluster                        | 暂停集群                                                             |
| ResumeCluster                       | 恢复集群                                                             |
| ScaleCluster                        | 扩容集群                                                             |
| DownloadTiDBClusterCA               | 下载 CA 证书                                                         |
| OpenWebSQLConsole                   | 通过 Web SQL 连接 TiDB 集群                                          |
| SetRootPassword                     | 设置 TiDB 集群的 root 密码                                           |
| UpdateIPAccessList                  | 更新 TiDB 集群的 IP 访问列表                                         |
| SetAutoBackup                       | 设置 TiDB 集群的自动备份机制                                         |
| DoManualBackup                      | 执行 TiDB 集群的手动备份                                             |
| BackupCompleted                     | 备份任务完成                                                         |
| DeleteBackupTask                    | 删除备份任务                                                         |
| DeleteBackup                        | 删除备份文件                                                         |
| RestoreFromBackup                   | 基于备份文件恢复到 TiDB 集群                                         |
| RestoreFromTrash                    | 基于回收站中的备份文件恢复到 TiDB 集群                               |
| ImportDataFromAWS                   | 从 AWS 导入数据                                                      |
| ImportDataFromGCP                   | 从 Google Cloud 导入数据                                             |
| ImportDataFromLocal                 | 从本地磁盘导入数据                                                   |
| CreateMigrationJob                  | 创建迁移任务                                                         |
| SuspendMigrationJob                 | 暂停迁移任务                                                         |
| ResumeMigrationJob                  | 恢复迁移任务                                                         |
| DeleteMigrationJob                  | 删除迁移任务                                                         |
| ShowDiagnose                        | 查看诊断信息                                                         |
| DBAuditLogAction                    | 设置数据库审计日志活动                                               |
| AddDBAuditFilter                    | 添加数据库审计日志过滤器                                             |
| DeleteDBAuditFilter                 | 删除数据库审计日志过滤器                                             |
| EditProject                         | 编辑项目信息                                                         |
| DeleteProject                       | 删除项目                                                             |
| BindSupportPlan                     | 绑定支持计划                                                         |
| CancelSupportPlan                   | 取消支持计划                                                         |
| UpdateOrganizationName              | 更新组织名称                                                         |
| SetSpendLimit                       | 编辑 TiDB Cloud Serverless 弹性集群的消费上限                        |
| UpdateMaintenanceWindow             | 修改维护窗口开始时间                                                 |
| DeferMaintenanceTask                | 延迟维护任务                                                         |
| CreateBranch                        | 创建 TiDB Cloud Serverless 分支                                      |
| DeleteBranch                        | 删除 TiDB Cloud Serverless 分支                                      |
| SetBranchRootPassword               | 设置 TiDB Cloud Serverless 分支的 root 密码                          |
| ConnectBranchGitHub                 | 将集群与 GitHub 仓库连接以启用分支集成                               |
| DisconnectBranchGitHub              | 断开集群与 GitHub 仓库的连接以禁用分支集成                           |

## 控制台审计日志字段

为帮助你追踪用户活动，TiDB Cloud 为每条控制台审计日志提供了以下字段：

| 字段名                | 数据类型   | 描述                                                                                 |
|-----------------------|------------|--------------------------------------------------------------------------------------|
| type                  | string     | 事件类型                                                                             |
| ends_at               | timestamp  | 事件时间                                                                             |
| operator_type         | enum       | 操作人类型：`user` 或 `api_key`                                                      |
| operator_id           | uint64     | 操作人 ID                                                                            |
| operator_name         | string     | 操作人名称                                                                           |
| operator_ip           | string     | 操作人 IP 地址                                                                       |
| operator_login_method | enum       | 操作人登录方式：`google`、`github`、`microsoft`、`email` 或 `api_key`                |
| org_id                | uint64     | 事件所属组织 ID                                                                      |
| org_name              | string     | 事件所属组织名称                                                                     |
| project_id            | uint64     | 事件所属项目 ID                                                                      |
| project_name          | string     | 事件所属项目名称                                                                     |
| cluster_id            | uint64     | 事件所属集群 ID                                                                      |
| cluster_name          | string     | 事件所属集群名称                                                                     |
| trace_id              | string     | 操作人发起请求的 Trace ID。该字段当前为空，未来版本将会支持。                        |
| result                | enum       | 事件结果：`success` 或 `failure`                                                     |
| details               | json       | 事件详细描述                                                                         |
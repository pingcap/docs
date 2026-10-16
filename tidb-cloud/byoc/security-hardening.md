---
title: TiDB Cloud BYOC 安全加固
summary: 本文档概述了 TiDB Cloud BYOC 部署的安全加固步骤。
---

# TiDB Cloud BYOC 安全加固

在 BYOC 环境已完全交付并投入生产后，你可以选择移除仅在安装阶段使用的启动权限，以遵循云安全最佳实践中推荐的**最小权限原则（Principle of Least Privilege）**。

这些权限涉及两个 IAM 角色：

* **auto-deploy-cli**：权限最高的角色，用于创建基础设施，例如 VPC 和 EKS 集群。
* **auto-deploy-sync-image**：用于从 TiDB Cloud 拉取并同步镜像的角色。

> **Important:**
>
> **对于多 Region 和多个资源池：** `auto-deploy-cli` 和 `auto-deploy-sync-image` IAM 角色是全局（账户级）资源。如果你计划在多个 AWS Region 中部署 TiDB Cloud BYOC，或在你的账户内配置多个物理隔离的资源池，建议将此安全加固步骤延后，直到所有环境都已完成部署。

根据你对**自动升级**的要求，可以选择以下选项之一。

## 选项 1：保留自动升级，移除基础设施部署权限 {#option-1-retain-automatic-upgrades-remove-infrastructure-deployment-permissions}

**目标：**移除 `auto-deploy-cli` 角色，同时保留 `auto-deploy-sync-image` 角色。

**影响：**

* 安全性：控制面将无法再在你的账户中创建新的基础设施资源（例如 VPC）。
* 可维护性：由于保留了镜像同步权限，集群仍可执行自动升级。

**步骤：**

1. 找到部署期间使用的 CloudFormation 模板：`tidbcloud-byoc-setup-deploy.yaml`。

2. 编辑该文件。找到 `TiDBCloudAutoDeployRole` 字段并删除该行及其所有下属内容，同时保留 `TiDBCloudAutoDeploySyncImageRole` 部分不变。

3. 在终端中应用更新后的脚本：

    ```shell
    bash tidbcloud-byoc-update.sh --stack deploy
    ```

## 选项 2：移除所有启动权限（禁用自动升级） {#option-2-remove-all-bootstrap-permissions-automatic-upgrades-disabled}

**目标：**同时移除 `auto-deploy-cli` 和 `auto-deploy-sync-image` 角色。

**影响：**

* 最高安全性：启动阶段使用的所有 IAM 角色都会被移除。
* 功能限制：自动升级将不再可用。若将来需要升级数据库组件，你必须重新部署 sync-image 角色。

**步骤：**

通过 AWS CLI 删除对应的 CloudFormation stack：

```shell
aws cloudformation delete-stack --stack-name tidbcloud-byoc-setup-deploy
```

> **Important:**
>
> 无论你选择哪个选项，**都不要删除带有** `dataplane` **或** `o11y` **后缀的 stack**（例如 `tidbcloud-byoc-setup-dataplane`），因为它们提供了集群运行、监控和备份所需的运行时权限。
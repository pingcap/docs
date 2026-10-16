---
title: 配置 TiDB Cloud BYOC IAM 权限
summary: 本文档介绍了 TiDB Cloud BYOC 控制面访问所需的 IAM 配置。
---

# 配置 TiDB Cloud BYOC IAM 权限

在 AWS 环境准备完成后，你必须授予 TiDB Cloud 控制面在你的账户内管理资源的权限。这可以通过执行一个引导脚本来实现，该脚本会基于最小权限原则创建所需的 IAM Role。

## 准备工作 {#preparation}

在执行脚本之前，请确保你已具备以下条件：

1. **已安装 AWS CLI：** CLI 必须配置一个具有创建 IAM role 和 policy 权限的 Access Key。
2. **TiDB Cloud 账户信息：** 联系你的 TiDB Cloud 支持代表，获取 **Control Plane Account ID** 和 **Clinic Account ID**。

## 收集参数 {#gather-parameters}

使用下表映射脚本所需的参数：

| 参数 | 来源 | 说明 |
| :---- | :---- | :---- |
| `<ControlPlaneAccountId>` | **TiDB Support** | TiDB 控制面的 AWS 账户 ID。 |
| `<ClinicAccountId>` | **TiDB Support** | TiDB Clinic 服务的 AWS 账户 ID。 |
| `<TidbHostedZoneId>` | [所需信息](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | 你创建的 TiDB 集群 Hosted Zone 的 ID。 |
| `<TidbPCAArn>` | [所需信息](/tidb-cloud/byoc/byoc-prepare-environment-aws.md#summary-required-information) | 你创建的 Private CA 的 ARN。 |

## 执行引导脚本 {#execute-bootstrapping-script}

1. 从 [PingCAP GitHub 仓库](https://github.com/tidbcloud/byoc-account-setup/tree/main) 下载脚本。

2. 在终端中运行以下命令。注意将占位符替换为你的实际值。

    ```bash
    sh tidbcloud-byoc-setup.sh \
        --control-plane-id <ControlPlaneAccountId> \
        --clinic-id <ClinicAccountId> \
        --tidb-hz-id <TidbHostedZoneId> \
        --pca-arn <TidbPCAArn>
    ```

3. 监控执行过程。脚本运行后，会启动 AWS CloudFormation 来预配和修改资源。你可以在终端中看到日志流，其中会显示诸如 `waiting for changeset to be created` 和 `successfully created/updated stack` 之类的状态消息。

<!--To confirm: whether to add image-->

## 验证 {#verification}

执行完成后，脚本会输出已创建的 IAM role 的 ARN。

**需要执行的操作：** 将 **execution result/log** 分享给你的 TiDB Cloud 代表。

## 下一步 {#what-s-next}

在 TiDB Cloud 完成对 IAM role 的验证后，继续执行 [TiDB Cloud BYOC 自动化 Region 部署](/tidb-cloud/byoc/byoc-automated-deployment.md)。TiDB Cloud 将触发自动化 Region 部署。
---
title: 为 {{{ .byoc }}} 配置堡垒机主机
summary: 了解如何在 {{{ .byoc }}} 环境中部署和管理堡垒机主机，以实现安全的维护访问。
---

# 为 {{{ .byoc }}} 配置堡垒机主机

本文档介绍如何为 {{{ .byoc }}} 环境部署和管理堡垒机主机。堡垒机主机可为您 AWS 账户中的 TiDB 和可观测性 EKS 集群提供受控的访问路径，以便进行安全交互。

TiDB Cloud 仅在已授予权限的故障排查和维护场景中使用堡垒机主机。堡垒机主机通过安全的 Tailscale 隧道连接到 TiDB Cloud。您可以在需要时（权限）回收或恢复此访问。

> **Note:**
>
> 配置堡垒机主机是可选的。您也可以提供自己的安全访问方法来进行维护和故障排查。

## 开始之前 {#before-you-begin}

在部署堡垒机主机之前，请确保满足以下要求：

- 已在本地安装 Terraform。
- 已使用您的 AWS 账户凭证配置 AWS CLI。
- 您拥有管理所需 AWS 资源的权限，包括 EC2、IAM 和 EKS 资源。
- 您的 {{{ .byoc }}} 环境已完成部署。
- 您已从 TiDB Cloud Support 获取以下信息：
    - 您的 TiDB Cloud tenant ID。
    - 您的 {{{ .byoc }}} 环境部署所在的 AWS region ID。
    - TiDB 和可观测性的 EKS 集群名称。
    - 您要部署的堡垒机主机所需的 Tailscale authentication keys。
    - 对于 Single-AZ 部署，TiDB 和可观测性 EKS 集群的 subnet ID。

## 部署堡垒机主机 {#deploy-bastion-hosts}

要部署堡垒机主机，请执行以下步骤：

1. 从 [PingCAP GitHub repository](https://github.com/tidbcloud/byoc-account-setup/tree/main/bastion) 下载堡垒机主机部署脚本。

2. 配置 Terraform backend。

    默认 backend 为 Amazon S3。在 `terraform.tf` 中，使用您的 bucket、state file path 和 region 修改 S3 backend 配置：

    ```hcl
    terraform {
      required_providers {
        aws = {
          source  = "hashicorp/aws"
          version = "~> 5.0"
        }
      }

      backend "s3" {
        bucket = "YOUR_S3_BUCKET"
        key    = "TF_STATE_FILE_PATH"
        region = "us-west-2"
      }
    }
    ```

    如果您使用其他 [Terraform backend](https://developer.hashicorp.com/terraform/language/backend)，请相应修改 `terraform.tf`。

3. 初始化 Terraform：

    ```shell
    terraform init
    ```

4. 准备 Terraform 变量文件：

    ```shell
    cp examples/terraform.tfvars.example ./terraform.tfvars
    vim ./terraform.tfvars
    ```

5. 在 `terraform.tfvars` 中，配置以下必填字段：

    - `aws_region`：您的 {{{ .byoc }}} 环境部署所在的 AWS region，例如 `us-west-2`。
    - `tidbcloud_tenant_id`：您的 TiDB Cloud tenant ID。
    - `bastions`：堡垒机主机配置。您可以为 `tidb` 和 `o11y` 配置 bastion。
    - `<bastion_type>.eks_cluster_name`：对应 bastion 类型的 EKS 集群名称，例如 `tidb.eks_cluster_name` 或 `o11y.eks_cluster_name`。
    - `<bastion_type>.auth_key`：TiDB Cloud 提供的 Tailscale authentication key。
    - `<bastion_type>.subnet_id`：仅适用于 Single-AZ 部署，对应 EKS 集群的 subnet ID。

    以下示例为 TiDB 和可观测性同时配置堡垒机主机：

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
      o11y = {
        eks_cluster_name = "your-o11y-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

    如果您只需要 TiDB 堡垒机主机，则只配置 `tidb` 条目：

    ```hcl
    aws_region = "us-west-2"

    tidbcloud_tenant_id = "your_tidbcloud_tenant_id"

    bastions = {
      tidb = {
        eks_cluster_name = "your-tidb-eks-cluster"
        auth_key         = "tskey-key-xxxxxxxx"
        # subnet_id      = "subnet-xxxx"
      }
    }
    ```

6. 应用 Terraform 配置：

    ```shell
    terraform apply
    ```

    请仔细检查 Terraform plan。要确认并继续部署，请输入 `yes`。

## 验证部署 {#validate-the-deployment}

部署完成后，获取 Terraform output：

```shell
terraform output
```

输出类似如下：

```hcl
bastion_attributes = tomap({
  "bastion_name" = {
    "o11y" = "<bastion_o11y_name>"
    "tidb" = "<bastion_tidb_name>"
  }
  "instance_id" = {
    "o11y" = "<instance_o11y_id>"
    "tidb" = "<instance_tidb_id>"
  }
})
```

将该输出提供给 TiDB Cloud Support。TiDB Cloud Support 会使用该输出验证连通性，并完成所需的网络配置。

## 管理堡垒机主机 {#manage-bastion-hosts}

堡垒机主机部署完成后，您可以通过 AWS Systems Manager (SSM) 对其进行管理：

```shell
aws ssm start-session --region <region> --target <instance_id> --reason <reason>
```

如需临时（权限）回收 TiDB Cloud 对堡垒机主机的访问，请在堡垒机主机上运行以下命令：

```shell
tailscale down
```

如需恢复 TiDB Cloud 对堡垒机主机的访问，请在堡垒机主机上运行以下命令：

```shell
tailscale up
```

## 管理 authentication keys {#manage-authentication-keys}

TiDB Cloud 提供的 Tailscale authentication keys 为一次性且临时有效。它们通常会在 3 天后过期。

key 过期不会影响已经使用有效 key 完成部署和配置的堡垒机主机。但是，如果 key 过期后您需要再次运行 `terraform apply`，例如创建新的堡垒机主机或重新创建现有堡垒机主机，请向 TiDB Cloud Support 申请新的 authentication keys，并在应用配置前修改 `terraform.tfvars` 中的 `auth_key` 值。

## 审计日志 {#audit-logs}

出于安全和合规考虑，每个堡垒机主机都配置为通过 [auditd service](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/security_guide/chap-system_auditing) 收集已执行命令的详细审计轨迹。

审计日志存储在本地的 `/var/log/audit/audit.log`，并会自动转发到以下 AWS CloudWatch Log Group：

```text
/aws/eks/${eks_cluster_name}/byoc-bastion/audit
```

默认情况下，日志会在 CloudWatch 中保留 90 天。

如需禁用 CloudWatch 审计日志转发，请将 `cloudwatch_audit_enable` 设置为 `false`。

## 清理堡垒机主机 {#clean-up-bastion-hosts}

要移除 Terraform 配置创建的堡垒机主机及其相关资源，请运行以下命令：

```shell
terraform destroy
```
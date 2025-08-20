---
title: 获取 TiDB Cloud Terraform Provider
summary: 了解如何获取 TiDB Cloud Terraform Provider。
---

# 获取 TiDB Cloud Terraform Provider

你将在本文档中学习如何获取 TiDB Cloud Terraform Provider。

## 前置条件

请确保已满足 [TiDB Cloud Terraform Provider 概览](/tidb-cloud/terraform-tidbcloud-provider-overview.md#requirements) 中的要求。

## 第 1 步：安装 Terraform

TiDB Cloud Terraform Provider 已发布到 [Terraform Registry](https://registry.terraform.io/)。你只需要安装 Terraform（>=1.0）即可。

对于 macOS，你可以按照以下步骤使用 Homebrew 安装 Terraform。

1. 安装 HashiCorp tap，这是包含所有所需 Homebrew 包的仓库。

    ```shell
    brew tap hashicorp/tap
    ```

2. 使用 `hashicorp/tap/terraform` 安装 Terraform。

    ```shell
    brew install hashicorp/tap/terraform
    ```

对于其他操作系统，请参阅 [Terraform 官方文档](https://learn.hashicorp.com/tutorials/terraform/install-cli) 获取安装说明。

## 第 2 步：创建 API 密钥

TiDB Cloud API 使用 HTTP 摘要认证（Digest Authentication），可以保护你的私钥不会通过网络传输。

目前，TiDB Cloud Terraform Provider 不支持管理 API 密钥。因此，你需要在 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters) 中创建 API 密钥。

详细步骤请参见 [TiDB Cloud API 文档](https://docs.pingcap.com/tidbcloud/api/v1beta#section/Authentication/API-Key-Management)。

## 第 3 步：下载 TiDB Cloud Terraform Provider

1. 创建一个 `main.tf` 文件：

   ```
   terraform {
     required_providers {
       tidbcloud = {
         source = "tidbcloud/tidbcloud"
         version = "~> 0.3.0"
       }
     }
     required_version = ">= 1.0.0"
   }
   ```

   - `source` 属性指定要从 [Terraform Registry](https://registry.terraform.io/) 下载的目标 Terraform provider。
   - `version` 属性为可选项，用于指定 Terraform provider 的版本。如果未指定，则默认使用最新的 provider 版本。
   - `required_version` 为可选项，用于指定 Terraform 的版本。如果未指定，则默认使用最新的 Terraform 版本。

2. 运行 `terraform init` 命令，从 Terraform Registry 下载 TiDB Cloud Terraform Provider。

   ```
   $ terraform init

   Initializing the backend...

   Initializing provider plugins...
   - Reusing previous version of tidbcloud/tidbcloud from the dependency lock file
   - Using previously-installed tidbcloud/tidbcloud v0.1.0

   Terraform has been successfully initialized!

   You may now begin working with Terraform. Try running "terraform plan" to see
   any changes that are required for your infrastructure. All Terraform commands
   should now work.

   If you ever set or change modules or backend configuration for Terraform,
   rerun this command to reinitialize your working directory. If you forget, other
   commands will detect it and remind you to do so if necessary.
   ```

## 第 4 步：使用 API 密钥配置 TiDB Cloud Terraform Provider

你可以按如下方式配置 `main.tf` 文件：

```
terraform {
  required_providers {
    tidbcloud = {
      source = "tidbcloud/tidbcloud"
    }
  }
}

provider "tidbcloud" {
  public_key = "your_public_key"
  private_key = "your_private_key"
}
```

`public_key` 和 `private_key` 分别为 API 密钥的公钥和私钥。你也可以通过环境变量传递它们：

```
export TIDBCLOUD_PUBLIC_KEY=${public_key}
export TIDBCLOUD_PRIVATE_KEY=${private_key}
```

现在，你可以使用 TiDB Cloud Terraform Provider 了。

## 第 5 步：使用同步配置配置 TiDB Cloud Terraform Provider

Terraform provider（>= 0.3.0）支持一个可选参数 `sync`。

通过将 `sync` 设置为 `true`，你可以同步地创建、更新或删除资源。示例如下：

```
provider "tidbcloud" {
  public_key = "your_public_key"
  private_key = "your_private_key"
}
```

推荐将 `sync` 设置为 `true`，但请注意，`sync` 目前仅对集群资源生效。如果你需要对其他资源进行同步操作，请 [联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)。

## 下一步

通过 [`tidbcloud_serverless_cluster`](/tidb-cloud/terraform-use-serverless-cluster-resource.md) 或 [`tidbcloud_dedicated_cluster`](/tidb-cloud/terraform-use-dedicated-cluster-resource.md) 资源开始管理集群。
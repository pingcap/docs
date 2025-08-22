---
title: 将集群资源迁移到无服务器或专用集群资源
summary: 了解如何将集群资源迁移到无服务器或专用集群资源。
---

# 将集群资源迁移到无服务器或专用集群资源

从 TiDB Cloud Terraform Provider v0.4.0 开始，`tidbcloud_cluster` 资源被两个新资源所取代：`tidbcloud_serverless_cluster` 和 `tidbcloud_dedicated_cluster`。如果你正在使用 TiDB Cloud Terraform Provider v0.4.0 或更高版本，可以按照本文档将你的 `tidbcloud_cluster` 资源迁移到 `tidbcloud_serverless_cluster` 或 `tidbcloud_dedicated_cluster` 资源。

> **Tip:**
>
> 本文档中的步骤使用了 Terraform 的配置生成特性，通过自动重新创建集群资源的 `.tf` 配置来简化迁移流程。要了解更多信息，请参阅 Terraform 文档中的 [Generating configuration](https://developer.hashicorp.com/terraform/language/import/generating-configuration)。

## 前置条件

- 升级到 [TiDB Cloud Terraform Provider v0.4.0 或更高版本](https://registry.terraform.io/providers/tidbcloud/tidbcloud/latest)

## 第 1 步：识别需要迁移的 `tidbcloud_cluster` 资源

1. 列出所有 `tidbcloud_cluster` 资源：

    ```shell
    terraform state list | grep "tidbcloud_cluster"
    ```

2. 选择一个目标集群资源进行迁移，并获取其集群 `id` 以备后用：

    ```shell
    terraform state show ${your_target_cluster_resource} | grep ' id '
    ```

## 第 2 步：从 Terraform 状态中移除现有资源

从 Terraform 状态中移除你的目标集群资源：

```shell
terraform state rm ${your_target_cluster_resource}
```

## 第 3 步：删除目标集群资源的配置

在你的 `.tf` 文件中，找到目标集群资源的配置并删除对应的代码。

## 第 4 步：为新的无服务器或专用集群资源添加 import 块

- 如果你的目标集群是 TiDB Cloud Serverless，请将以下 import 块添加到你的 `.tf` 文件中，将 `example` 替换为你期望的资源名称，并将 `${id}` 替换为你在 [第 1 步](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate) 获取的集群 ID：

    ```
    # TiDB Cloud Serverless
    import {
      to = tidbcloud_serverless_cluster.example
      id = "${id}"
    }
    ```

- 如果你的目标集群是 TiDB Cloud Dedicated，请将以下 import 块添加到你的 `.tf` 文件中，将 `example` 替换为你期望的资源名称，并将 `${id}` 替换为你在 [第 1 步](#step-1-identify-the-tidbcloud_cluster-resource-to-migrate) 获取的集群 ID：

    ```
    # TiDB Cloud Dedicated
    import {
      to = tidbcloud_dedicated_cluster.example
      id = "${id}"
    }
    ```

## 第 5 步：生成新的配置文件

根据 import 块为新的无服务器或专用集群资源生成新的配置文件：

```shell
terraform plan -generate-config-out=generated.tf
```

不要在上述命令中指定已有的 `.tf` 文件名，否则 Terraform 会返回错误。

## 第 6 步：检查并应用生成的配置

检查生成的配置文件，确保其满足你的需求。你也可以选择将该文件的内容移动到你喜欢的位置。

然后，运行 `terraform apply` 以导入你的基础设施。应用后，示例输出如下：

```shell
tidbcloud_serverless_cluster.example: Importing... 
tidbcloud_serverless_cluster.example: Import complete 

Apply complete! Resources: 1 imported, 0 added, 0 changed, 0 destroyed.
```
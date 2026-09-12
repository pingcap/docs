---
title: Amazon S3 - 凭证
summary: 本页介绍如何创建 `Amazon S3 - Credentials` 数据源。该数据源用于存储访问 Amazon S3 所需的凭证，并可在多个 S3 集成任务之间复用。
---

# Amazon S3 - 凭证

本页介绍如何创建 `Amazon S3 - Credentials` 数据源。该数据源用于存储访问 Amazon S3 所需的凭证，并可在多个 S3 集成任务之间复用。

## 使用场景 {#use-cases}

- 为多个 S3 导入任务管理同一组 AWS Access Key 和 Secret Key 凭证
- 避免在每个任务中重复输入相同的 S3 访问凭证
- 在凭证轮转时集中修改凭证

## 创建 Amazon S3 - 凭证 {#create-amazon-s3-credentials}

1. 进入 **Data** > **Data Sources**，然后点击 **Create Data Source**。
2. 选择 **Amazon S3 - Credentials** 作为服务类型，然后填写凭证信息：

    | 字段 | 必填 | 说明 |
    |-------|----------|-------------|
    | **Name** | 是 | 此数据源的描述性名称 |
    | **Access Key** | 是 | AWS Access Key ID |
    | **Secret Key** | 是 | AWS Secret Access Key |

3. 点击 **Test Connectivity** 以验证凭证。如果测试成功，点击 **OK** 保存数据源。

## 权限要求 {#permission-requirements}

AWS 凭证必须具有目标 S3 存储桶的读访问权限。如果下游任务会启用 **Clean Up Original Files**，则该凭证还必须具有写入和删除权限。

## 后续步骤 {#next-steps}

创建此数据源后，你可以使用它来创建 [Amazon S3 集成任务](/tidb-cloud-lake/guides/integrate-with-amazon-s3.md)。

---
title: 使用客户管理的加密密钥（CMEK）进行静态数据加密
summary: 了解如何在 TiDB Cloud 中使用客户管理的加密密钥（CMEK）。
---

# 使用客户管理的加密密钥（CMEK）进行静态数据加密

客户管理的加密密钥（CMEK）允许你通过利用一把由你完全控制的对称加密密钥，来保护 TiDB Cloud 专用集群中的静态数据。该密钥被称为 CMEK 密钥。

一旦为某个项目启用 CMEK，所有在该项目中创建的集群都会使用 CMEK 密钥对其静态数据进行加密。此外，这些集群生成的任何备份数据也会使用相同的密钥进行加密。如果未启用 CMEK，TiDB Cloud 会使用托管密钥在数据静态存储时对所有数据进行加密。

> **注意：**
>
> - CMEK 类似于 Bring Your Own Key（BYOK）。使用 BYOK 时，你通常在本地生成密钥并上传。然而，TiDB Cloud 仅支持在 [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html) 内生成的密钥。
> - 当前，此功能仅在请求后提供。如果你需要试用此功能，请联系 [support](/tidb-cloud/tidb-cloud-support.md)。

## 限制条件

- 目前，TiDB Cloud 仅支持使用 AWS KMS 提供 CMEK。
- 要使用 CMEK，你需要在创建项目时启用 CMEK，并在创建集群前完成 CMEK 相关配置。不能为已存在的项目启用 CMEK。
- 当前，在启用 CMEK 的项目中，只能创建托管在 AWS 上的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。不支持托管在其他云提供商上的 TiDB Cloud Dedicated 集群和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。
- 当前，在启用 CMEK 的项目中，不支持 [双区域备份](/tidb-cloud/backup-and-restore-concepts.md#dual-region-backup)。
- 当前，对于某个特定项目，只能在一个 AWS 区域启用 CMEK。一旦配置完成，就不能在同一项目的其他区域创建集群。

## 启用 CMEK

如果你希望使用你账户拥有的 KMS 来加密数据，请按照以下步骤操作。

### 第1步：创建启用CMEK的项目

如果你在组织中拥有 `Organization Owner` 角色，可以通过 TiDB Cloud 控制台或 API 创建启用 CMEK 的项目。

<SimpleTab groupId="method">
<div label="使用控制台" value="console">

创建启用 CMEK 的项目，步骤如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)，通过左上角的组合框切换到目标组织。
2. 在左侧导航栏中点击 **Projects**。
3. 在 **Projects** 页面右上角点击 **Create New Project**。
4. 填写项目名称。
5. 选择启用项目的 CMEK 功能。
6. 点击 **Confirm** 完成项目创建。

</div>
<div label="使用 API" value="api">

你可以通过 [Create a CMEK-enabled project](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject) 端点，使用 TiDB Cloud API 完成此步骤。确保 `aws_cmek_enabled` 字段设置为 `true`。

目前，TiDB Cloud API 仍处于测试阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

### 第2步：完成项目的 CMEK 配置

你可以通过 TiDB Cloud 控制台或 API 完成项目的 CMEK 配置。

> **注意：**
>
> 确保密钥的策略符合要求，且没有权限不足或账户问题等错误。这些错误可能导致集群使用该密钥创建不正确。

<SimpleTab groupId="method">
<div label="使用控制台" value="console">

完成项目的 CMEK 配置，步骤如下：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com)，通过左上角的组合框切换到目标项目。
2. 在左侧导航栏中点击 **Project Settings** > **Encryption Access**。
3. 在 **Encryption Access** 页面，点击 **Create Encryption Key** 进入密钥创建页面。
4. 密钥提供者仅支持 AWS KMS。你可以选择密钥可用的区域。
5. 复制并保存 JSON 文件为 `ROLE-TRUST-POLICY.JSON`，该文件描述信任关系。
6. 将此信任关系添加到 AWS KMS 的密钥策略中。更多信息请参见 [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
7. 在 TiDB Cloud 控制台中，滚动到密钥创建页面底部，填写从 AWS KMS 获取的 **KMS Key ARN**。
8. 点击 **Create** 创建密钥。

</div>
<div label="使用 API" value="api">

1. 在 AWS KMS 上配置密钥策略，并在策略中添加以下内容：

    ```json
    {
        "Version": "2012-10-17",
        "Id": "cmek-policy",
        "Statement": [
            // EBS相关策略
            {
                "Sid": "Allow access through EBS for all principals in the account that are authorized to use EBS",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": [
                    "kms:Encrypt",
                    "kms:Decrypt",
                    "kms:ReEncrypt*",
                    "kms:GenerateDataKey*",
                    "kms:CreateGrant",
                    "kms:DescribeKey"
                ],
                "Resource": "*",
                "Condition": {
                    "StringEquals": {
                        "kms:CallerAccount": "<pingcap-account>",
                        "kms:ViaService": "ec2.<region>.amazonaws.com"
                    }
                }
            },
            // S3相关策略
            {
                "Sid": "Allow TiDB cloud role to use KMS to store encrypted backup to S3",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::<pingcap-account>:root"
                },
                "Action": [
                    "kms:Decrypt",
                    "kms:GenerateDataKey"
                ],
                "Resource": "*"
            },
            ... // 用户自己的管理员权限
        ]
    }
    ```

    - `<pingcap-account>` 是你的集群所在的账户。如果不知道账户信息，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
    - `<region>` 是你想创建集群的区域，例如 `us-west-2`。如果不想指定区域，可以用通配符 `*` 替代 `<region>`，并放在 `StringLike` 块中。
    - 关于前述策略中的 EBS 相关部分，参考 [AWS 文档](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account)。
    - 关于 S3 相关策略，参考 [AWS 博客](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption)。

2. 调用 TiDB Cloud API 的 [Configure AWS CMEK](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek) 端点。

目前，TiDB Cloud API 仍处于测试阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

> **注意：**
>
> 此功能未来将持续增强，后续版本可能需要额外权限。因此，此策略要求可能会发生变化。

### 第3步：创建集群

在 [第1步](#step-1-create-a-cmek-enabled-project) 创建的项目下，创建一个托管在 AWS 上的 TiDB Cloud 专用集群。详细步骤请参见 [此文档](/tidb-cloud/create-tidb-cluster.md)。确保集群所在的区域与 [第2步](/tidb-cloud/tidb-cloud-encrypt-cmek.md#step-2-complete-the-cmek-configuration-of-the-project) 中配置的区域一致。

> **注意：**
>
> 当启用 CMEK 时，集群节点使用的 EBS 卷和备份所用的 S3 都会使用 CMEK 进行加密。

## CMEK 轮换

你可以在 AWS KMS 上配置 [自动 CMEK 轮换](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)。启用轮换后，无需在 TiDB Cloud 的项目设置中更新 **Encryption Access**，包括 CMEK ID。

## 撤销与恢复 CMEK

如果你需要暂时撤销 TiDB Cloud 对 CMEK 的访问权限，请按照以下步骤操作：

1. 在 AWS KMS 控制台中，撤销相应权限并更新 KMS 密钥策略。
2. 在 TiDB Cloud 控制台中，暂停项目中的所有集群。

> **注意：**
>
> 在你在 AWS KMS 撤销 CMEK 后，已运行的集群不受影响。但当你暂停集群后再恢复，集群将无法正常恢复，因为无法访问 CMEK。

在撤销 TiDB Cloud 对 CMEK 的访问权限后，如果需要恢复访问权限，请按照以下步骤操作：

1. 在 AWS KMS 控制台中，恢复 CMEK 访问策略。
2. 在 TiDB Cloud 控制台中，恢复项目中的所有集群。
---
title: 使用客户管理的加密密钥进行静态数据加密
summary: 了解如何在 TiDB Cloud 中使用客户管理的加密密钥（CMEK）。
---

# 使用客户管理的加密密钥进行静态数据加密

客户管理的加密密钥（Customer-Managed Encryption Key，CMEK）允许你通过使用完全由你控制的对称加密密钥，保护 TiDB Cloud Dedicated 集群中的静态数据安全。该密钥被称为 CMEK 密钥。

一旦为项目启用 CMEK，该项目下创建的所有集群都会使用 CMEK 密钥对其静态数据进行加密。此外，这些集群生成的任何备份数据也会使用同一密钥进行加密。如果未启用 CMEK，TiDB Cloud 会使用托管密钥对集群中静态数据进行加密。

> **注意：**
>
> - CMEK 类似于自带密钥（BYOK）。在 BYOK 模式下，你通常会在本地生成密钥并上传。然而，TiDB Cloud 仅支持在 [AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html) 内生成的密钥。
> - 目前，该功能仅支持按需开通。如果你需要试用该功能，请联系 [support](/tidb-cloud/tidb-cloud-support.md)。

## 限制

- 目前，TiDB Cloud 仅支持使用 AWS KMS 提供 CMEK。
- 若要使用 CMEK，需在创建项目时启用 CMEK，并在创建集群前完成 CMEK 相关配置。无法为已存在的项目启用 CMEK。
- 目前，在启用 CMEK 的项目中，只能创建托管于 AWS 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群。不支持托管于其他云服务商的 TiDB Cloud Dedicated 集群和 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。
- 目前，在启用 CMEK 的项目中，不支持 [双区域备份](/tidb-cloud/backup-and-restore-concepts.md#dual-region-backup)。
- 目前，对于同一个项目，只能为一个 AWS 区域启用 CMEK。配置完成后，无法在同一项目下的其他区域创建集群。

## 启用 CMEK

如果你希望使用自己账户下的 KMS 对数据进行加密，请按照以下步骤操作。

### 步骤 1. 创建支持 CMEK 的项目

如果你拥有组织的 `Organization Owner` 角色，可以通过 TiDB Cloud 控制台或 API 创建支持 CMEK 的项目。

<SimpleTab groupId="method">
<div label="Use Console" value="console">

要创建支持 CMEK 的项目，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏点击 **Projects**。
3. 在 **Projects** 页面，点击右上角的 **Create New Project**。
4. 填写项目名称。
5. 选择启用项目的 CMEK 能力。
6. 点击 **Confirm** 完成项目创建。

</div>
<div label="Use API" value="api">

你可以通过 TiDB Cloud API 的 [Create a CMEK-enabled project](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Project/operation/CreateProject) 接口完成此步骤。请确保 `aws_cmek_enabled` 字段设置为 `true`。

目前，TiDB Cloud API 仍处于 beta 阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

### 步骤 2. 完成项目的 CMEK 配置

你可以通过 TiDB Cloud 控制台或 API 完成项目的 CMEK 配置。

> **注意：**
>
> 请确保密钥的策略符合要求，并且没有权限不足或账户问题等错误。这些错误可能导致集群无法正确使用该密钥创建。

<SimpleTab groupId="method">
<div label="Use Console" value="console">

要完成项目的 CMEK 配置，请执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标项目。
2. 在左侧导航栏点击 **Project Settings** > **Encryption Access**。
3. 在 **Encryption Access** 页面，点击 **Create Encryption Key** 进入密钥创建页面。
4. 密钥提供方仅支持 AWS KMS。你可以选择加密密钥可用的区域。
5. 复制并保存 JSON 文件为 `ROLE-TRUST-POLICY.JSON`。该文件描述了信任关系。
6. 将该信任关系添加到 AWS KMS 的密钥策略中。更多信息请参考 [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
7. 在 TiDB Cloud 控制台的密钥创建页面底部，填写从 AWS KMS 获取的 **KMS Key ARN**。
8. 点击 **Create** 创建密钥。

</div>
<div label="Use API" value="api">

1. 在 AWS KMS 上配置密钥策略，并将以下信息添加到密钥策略中：

    ```json
    {
        "Version": "2012-10-17",
        "Id": "cmek-policy",
        "Statement": [
            // EBS-related policy
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
            // S3-related policy
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
            ... // user's own admin access to KMS
        ]
    }
    ```

    - `<pingcap-account>` 是你的集群运行所在的账户。如果你不清楚该账户，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
    - `<region>` 是你希望创建集群的区域，例如 `us-west-2`。如果你不想指定区域，可以将 `<region>` 替换为通配符 `*`，并放在 `StringLike` 块中。
    - 有关上述 EBS 相关策略，请参考 [AWS 文档](https://docs.aws.amazon.com/kms/latest/developerguide/conditions-kms.html#conditions-kms-caller-account)。
    - 有关上述 S3 相关策略，请参考 [AWS 博客](https://repost.aws/knowledge-center/s3-bucket-access-default-encryption)。

2. 调用 TiDB Cloud API 的 [Configure AWS CMEK](https://docs.pingcap.com/tidbcloud/api/v1beta#tag/Cluster/operation/CreateAwsCmek) 接口。

    目前，TiDB Cloud API 仍处于 beta 阶段。更多信息请参见 [TiDB Cloud API Documentation](https://docs.pingcap.com/tidbcloud/api/v1beta)。

</div>
</SimpleTab>

> **注意：**
>
> 该功能未来会进一步增强，后续功能可能需要额外的权限。因此，该策略要求可能会发生变化。

### 步骤 3. 创建集群

在 [步骤 1](#step-1-create-a-cmek-enabled-project) 创建的项目下，创建托管于 AWS 的 TiDB Cloud Dedicated 集群。详细步骤请参考 [此文档](/tidb-cloud/create-tidb-cluster.md)。请确保集群所在区域与 [步骤 2](/tidb-cloud/tidb-cloud-encrypt-cmek.md#step-2-complete-the-cmek-configuration-of-the-project) 中配置的区域一致。

> **注意：**
>
> 启用 CMEK 后，集群节点使用的 EBS 卷以及集群备份使用的 S3 都会使用 CMEK 进行加密。

## 轮换 CMEK

你可以在 AWS KMS 上配置 [自动 CMEK 轮换](http://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)。启用轮换后，无需在 TiDB Cloud 项目的 **Encryption Access** 设置中更新 CMEK ID。

## 撤销与恢复 CMEK

如果你需要临时撤销 TiDB Cloud 对 CMEK 的访问权限，请按照以下步骤操作：

1. 在 AWS KMS 控制台撤销相应权限，并更新 KMS Key 策略。
2. 在 TiDB Cloud 控制台暂停该项目下的所有集群。

> **注意：**
>
> 在 AWS KMS 上撤销 CMEK 后，正在运行的集群不会受到影响。但当你暂停集群并尝试恢复时，由于无法访问 CMEK，集群将无法正常恢复。

撤销 TiDB Cloud 对 CMEK 的访问权限后，如果需要恢复访问权限，请按照以下步骤操作：

1. 在 AWS KMS 控制台恢复 CMEK 访问策略。
2. 在 TiDB Cloud 控制台恢复该项目下的所有集群。
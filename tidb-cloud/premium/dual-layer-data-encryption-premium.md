---
title: 双层数据加密
summary: 了解如何为托管在 AWS 上的 {{{ .premium }}} 实例启用和管理双层数据加密。
---

# 双层数据加密

本文档介绍如何为托管在 AWS 上的 {{{ .premium }}} 实例启用和管理双层数据加密。

> **注意：**
>
> 当前，双层数据加密功能仅可按需提供。如需申请此功能，请点击 [TiDB Cloud 控制台](https://tidbcloud.com) 右下角的 **?**，然后点击 **Support Tickets** 进入 [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals)。创建工单，在 **Description** 字段中填写 "Apply for Dual-Layer Data Encryption"，然后点击 **Submit**。

## 概述 {#overview}

默认情况下，{{{ .premium }}} 会对实例存储和快照卷中的静态数据进行加密，从而提供基础级别的数据安全性。此外，{{{ .premium }}} 支持将 TiDB 存储引擎加密与云服务提供商的 Key Management Service (KMS) 结合使用。这一额外的加密层称为 **双层数据加密**。

### 加密机制 {#encryption-mechanism}

为了提供更高级别的数据安全性，{{{ .premium }}} 对静态数据加密采用双层架构。存储层加密和数据库层加密都会保护你的数据。

- **存储层加密**

    - 底层云服务提供商会在其存储基础设施上提供存储层加密。例如，在 AWS 上，这包括 Amazon Elastic Block Store (EBS) 卷加密和 Amazon Simple Storage Service (S3) 存储桶加密。
    - 此层默认对所有 {{{ .premium }}} 实例启用，且无法禁用。它为静态数据提供基础安全保障。

- **数据库层加密**

    - 除了存储层加密之外，{{{ .premium }}} 还支持可选的数据库层加密功能（在 TiDB Cloud 控制台中标记为 **Dual-Layer Data Encryption**）。启用后，该功能会对存储在 TiKV 中的数据、changefeed 数据以及备份数据进行加密。
    - 该机制使数据在数据库系统内部始终保持加密状态，从而降低内部处理和数据传输过程中的数据泄露风险。
    - 与存储层加密不同，数据库层加密可由用户配置。你可以根据安全合规和运维要求，选择 Customer-Managed Encryption Key (CMEK) 或 Service-Managed Encryption Key。

### 备份与恢复注意事项 {#backup-and-restore-considerations}

启用双层数据加密后，{{{ .premium }}} 实例的备份数据也会被加密。任何从该备份恢复出的新实例都会继承原始实例的加密属性和 KMS 主密钥。

由于访问备份数据需要原始 KMS 主密钥，请确保满足以下要求：

- **保持密钥可用**：即使你删除了原始 {{{ .premium }}} 实例，也要保持关联的 KMS 主密钥处于激活状态，以便能够恢复备份数据。
- **确保授权正确**：在执行恢复操作时，配置与备份关联的完全相同的 KMS 主密钥，并确保该密钥具有访问数据所需的权限。

### 密钥管理选项 {#key-management-options}

双层数据加密使用 AWS KMS 管理静态数据加密的主密钥。你可以在以下两种密钥管理选项之间进行选择：

- **Customer-Managed Encryption Key (CMEK)**

    你可以创建、拥有并管理自己的 AWS KMS 主密钥。此选项可提供对加密的完全控制，适用于具有严格安全要求的组织。

    > **警告：**
    >
    > 你需要对密钥的安全性和可用性负全部责任。如果你删除了已配置的 CMEK，你的 {{{ .premium }}} 实例将变得不可用，并且你将无法恢复已加密的数据。

- **Service-Managed Encryption Key**

    {{{ .premium }}} 会自动代表你创建并管理 KMS 主密钥。此选项在安全性与便利性之间提供平衡，且无需维护开销。

    - 该密钥是对称加密密钥。
    - 当你在某个区域中创建第一个启用了加密的 {{{ .premium }}} 实例时，系统会自动生成该密钥。
    - 每个组织在每个区域只会创建一个密钥，并由该区域中的所有 {{{ .premium }}} 实例共享。
    - 只有在使用该密钥加密的所有数据都已从你的组织中移除后，该密钥才会被自动删除。

## 限制 {#limitations}

- 此功能当前仅支持 AWS KMS。对 Alibaba Cloud KMS 的支持计划在未来版本中提供。
- 数据加密适用于 TiKV 存储的数据、changefeed 数据和备份数据。对 TiFlash 数据加密的支持计划在未来版本中提供。
- 启用双层数据加密后，你无法修改 {{{ .premium }}} 实例的加密配置。
- 不支持自定义加密算法。你只能轮换 KMS 主密钥，不支持轮换其他加密密钥。
- 你的 AWS KMS 密钥必须与 {{{ .premium }}} 实例位于同一区域。因此，对于使用 CMEK 的备份，不支持跨区域恢复操作。

## 启用双层数据加密 {#enable-dual-layer-data-encryption}

你可以在创建 {{{ .premium }}} 实例时启用双层数据加密，也可以在实例创建后启用。

### 在创建实例时启用加密 {#enable-encryption-during-instance-creation}

创建 {{{ .premium }}} 实例时，你可以启用双层数据加密。根据你的安全和运维要求，选择 **Customer-Managed Encryption Key (CMEK)** 或 **Service-Managed Encryption Key**。

#### 选项 1：Customer-Managed Encryption Key (CMEK) {#option-1-customer-managed-encryption-key-cmek}

如需使用你自己的加密密钥，请执行以下步骤：

1. 在 AWS KMS 中创建一个对称加密密钥。

    该密钥必须与计划创建的 {{{ .premium }}} 实例位于**同一区域**。详细说明请参见 [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html)。

2. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中配置 CMEK：

    1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击 **Create Resource**。
    2. 选择 {{{ .premium }}} 计划并完成基本配置。
    3. 在 **Dual-Layer Data Encryption** 部分，点击 **Enable**。
    4. 选择 **Customer-Managed Encryption Key (CMEK)**，然后点击 **Add KMS Key ARN**。
    5. 复制显示的 JSON policy，并将其保存为 `ROLE-TRUST-POLICY.JSON`。该文件定义了所需的信任关系。
    6. 在 AWS KMS 控制台中，将此 trust policy 添加到你的密钥。更多信息，请参见 [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
    7. 返回 TiDB Cloud 控制台，滚动到密钥创建页面底部，输入你从 AWS KMS 获取的 **KMS Key ARN**。
    8. 要验证信任关系，点击 **Test and Add KMS Key ARN**。
    9. 验证成功后，点击 **Create** 完成 {{{ .premium }}} 实例创建。

#### 选项 2：Service-Managed Encryption Key {#option-2-service-managed-encryption-key}

如需由 TiDB Cloud 代表你管理加密密钥，请执行以下步骤：

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击 **Create Resource**。
2. 选择 {{{ .premium }}} 计划并完成基本配置。
3. 在 **Dual-Layer Data Encryption** 部分，点击 **Enable**。
4. 选择 **Service-Managed Encryption Key**。
5. 点击 **Create** 完成 {{{ .premium }}} 实例创建。

### 为现有实例启用加密 {#enable-encryption-for-an-existing-instance}

如果你在创建实例时未启用加密，也可以稍后启用。根据你的需求，选择 Customer-Managed Encryption Key (CMEK) 或 Service-Managed Encryption Key。

> **注意：**
>
> 为现有实例启用加密可能需要一些时间才能完成。

#### 选项 1：Customer-Managed Encryption Key (CMEK) {#option-1-customer-managed-encryption-key-cmek}

开始之前，请确保你已在 AWS KMS 中创建对称加密密钥。然后，执行以下步骤：

1. 在 {{{ .premium }}} 实例的 **Security** 页面中，在 **Dual-Layer Data Encryption** 部分点击 **Enable**。
2. 选择 **Customer-Managed Encryption Key (CMEK)**，然后点击 **Add KMS Key ARN**。
3. 复制显示的 JSON policy，并将其保存为 `ROLE-TRUST-POLICY.JSON`。该文件定义了所需的信任关系。
4. 在 AWS KMS 控制台中，将此 trust policy 添加到你的密钥。更多信息，请参见 [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
5. 返回 TiDB Cloud 控制台，滚动到页面底部，输入你从 AWS KMS 获取的 **KMS Key ARN**。
6. 要验证信任关系，点击 **Test and Add KMS Key ARN**。
7. 要启用双层数据加密，点击 **Enable**。

#### 选项 2：Service-Managed Encryption Key {#option-2-service-managed-encryption-key}

如需由 TiDB Cloud 代表你管理加密密钥，请执行以下步骤：

1. 在 {{{ .premium }}} 实例的 **Security** 页面中，在 **Dual-Layer Data Encryption** 部分点击 **Enable**。
2. 选择 **Service-Managed Encryption Key**。
3. 点击 **Enable**。

## 查看加密状态 {#view-encryption-status}

启用加密后，请在以下位置检查状态：

- 在 {{{ .premium }}} 实例的 **Overview** 页面，**Encryption** 字段会显示当前启用的密钥管理方式：**Enabled with Customer-Managed Encryption Key (CMEK)** 或 **Enabled with Service-Managed Encryption Key**。
- 在 **Security** 页面，你可以查看双层数据加密的详细配置。

## 从加密备份恢复 {#restore-from-an-encrypted-backup}

从启用了加密的 {{{ .premium }}} 实例创建的备份也会被加密。恢复加密备份时，新实例必须使用一致的加密设置。

### 恢复使用 CMEK 加密的备份 {#restore-a-backup-encrypted-with-a-cmek}

如果备份使用 CMEK 加密，请确保新实例在恢复期间能够访问 KMS 主密钥。密钥 ARN 保持不变。

要验证访问权限，点击 **Check** 开始 trust policy 验证。随后，TiDB Cloud 会检查密钥策略中已授权的 TiDB Cloud 账户是否与原始备份关联的账户一致：

- 如果账户一致，则无需进一步授权。
- 如果账户不一致，请复制提供的密钥策略并在 AWS KMS 中更新。此更新会重新授权该密钥，并确保新实例能够访问它。

### 恢复使用 Service-Managed Encryption Key 加密的备份 {#restore-a-backup-encrypted-with-a-service-managed-encryption-key}

如果备份使用 Service-Managed Encryption Key 加密，则恢复后的实例会自动继承相同的密钥类型。在恢复过程中，加密默认启用，且密钥类型设置为 **Service-Managed Encryption Key**。

## 轮换 Customer-Managed Encryption Key (CMEK) {#rotate-a-customer-managed-encryption-key-cmek}

要轮换 CMEK，你可以在 AWS KMS 中[启用自动密钥轮换](https://docs.aws.amazon.com/kms/latest/developerguide/rotating-keys-enable.html)。无需额外的 TiDB Cloud 配置。
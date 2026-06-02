---
title: Dual-Layer Data Encryption
summary: Learn how to enable and manage Dual-Layer Data Encryption for your {{{ .premium }}} instance.
---

# Dual-Layer Data Encryption

This document describes how to enable and manage Dual-Layer Data Encryption for your {{{ .premium }}} instance.

> **Note:**
>
> Currently, the Dual-Layer Data Encryption feature is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com), and then click **Support Tickets** to go to the [Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals). Create a ticket, fill in "Apply for Dual-Layer Data Encryption" in the **Description** field, and then click **Submit**.

## Overview

By default, {{{ .premium }}} encrypts data at rest on instance storage and snapshot volumes, providing a baseline level of data security. In addition, {{{ .premium }}} supports combining TiDB storage engine encryption with your cloud provider's Key Management Service (KMS). This additional layer is called **Dual-Layer Data Encryption**.

### Encryption mechanism

To provide a higher level of data security, {{{ .premium }}} uses a two-layer architecture for data-at-rest encryption. Both storage-layer and database-layer encryption protect your data.

- **Storage-layer encryption**

    - The underlying cloud service provider provides storage-layer encryption on its storage infrastructure. For example, on AWS, this includes Amazon Elastic Block Store (EBS) volume encryption and Amazon Simple Storage Service (S3) bucket encryption.
    - This layer is enabled by default for all {{{ .premium }}} instances and cannot be disabled. It provides the foundational security baseline for data at rest.

- **Database-layer encryption**

    - In addition to storage-layer encryption, {{{ .premium }}} supports an optional database-layer encryption feature (labeled **Dual-Layer Data Encryption** in the TiDB Cloud console). When you enable it, the feature encrypts data stored in TiKV, changefeed data, and backup data.
    - This mechanism keeps data encrypted within the database system, which reduces the risk of data leakage during internal processing and data movement.
    - Unlike storage-layer encryption, database-layer encryption is user-configurable. You can choose either a Customer-Managed Encryption Key (CMEK) or a Service-Managed Encryption Key, depending on your security compliance and operational requirements.

### Backup and restore considerations

When you enable Dual-Layer Data Encryption, the backup data for your {{{ .premium }}} instance is also encrypted. Any new instance restored from this backup inherits the encryption attributes and KMS master key of the original instance.

Because backup data requires the original KMS master key for access, make sure that you meet the following requirements:

- **Maintain key availability**: even if you delete the original {{{ .premium }}} instance, keep the associated KMS master key active so that you can recover the backup data.
- **Ensure correct authorization**: during a restore operation, configure the exact same KMS master key that is associated with the backup, and make sure that the key has the required permissions for data access.

### Key management options

Dual-Layer Data Encryption uses your cloud provider KMS to manage master keys for data-at-rest encryption. You can choose between two key management options:

- **Customer-Managed Encryption Key (CMEK)**

    You create, own, and manage your AWS KMS master key. This option provides full control over encryption and is suitable for organizations with strict security requirements.

    > **Warning:**
    >
    > You are fully responsible for maintaining the key's security and availability. If your CMEK is deleted or permanently damaged, your instance will malfunction and the encrypted data will become permanently unrecoverable. 

- **Service-Managed Encryption Key**

    {{{ .premium }}} automatically creates and manages the KMS master key on your behalf. This option offers a balance of security and convenience with no maintenance overhead.

    - The key is a symmetric encryption key.
    - The key is generated automatically when you create your first encrypted {{{ .premium }}} instance in a given region.
    - A single key is created per organization per region and is shared across all {{{ .premium }}} instances in that region.
    - The key is automatically deleted only after all data encrypted with it has been removed from your organization.

## Limitations

- Currently, this feature supports AWS KMS and Alibaba Cloud KMS.
- Data encryption applies to data stored by TiKV, changefeed data, and backup data. Support for TiFlash data encryption is planned for a future release.
- After you enable Dual-Layer Data Encryption, you cannot modify the encryption configuration of the {{{ .premium }}} instance.
- Custom encryption algorithms are not supported. You can rotate only the KMS master key. Rotating other encryption keys is not supported.
- Your cloud provider KMS key must reside in the same region as your {{{ .premium }}} instance. As a result, cross-region restore operations are not supported for backups that use a CMEK.

## Enable Dual-Layer Data Encryption

You can enable Dual-Layer Data Encryption either when you create a {{{ .premium }}} instance or after instance creation.

### Enable encryption during instance creation

When you create a {{{ .premium }}} instance, you can enable Dual-Layer Data Encryption. Depending on your security and operational requirements, choose either a **Customer-Managed Encryption Key (CMEK)** or a **Service-Managed Encryption Key**.

#### Option 1: Customer-Managed Encryption Key (CMEK)

To use your own encryption key, take the following steps:

1. Create a symmetric encryption key in your cloud provider KMS.

    Before proceeding, you must create a symmetric encryption key in your cloud provider KMS. Ensure the key resides in the **same region** as your planned TiDB service.  

    - For AWS, see [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html).
    - For Alibaba Cloud, see [Understanding KMS keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/overview-of-key-management).

2. Configure the CMEK in the [TiDB Cloud console](https://tidbcloud.com):

    1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click **Create Resource**.
    2. Select the {{{ .premium }}} plan and complete the basic configuration.
    3. In the **Dual-Layer Data Encryption** section, click **Enable**.
    4. Select **Customer-Managed Encryption Key (CMEK)**, and then click **Add KMS Key ARN**.
    5. Copy the displayed JSON policy statement. This policy statement defines the required key access permissions for TiDB Cloud.
    6. In your cloud provider KMS Console, append this policy statement to your key policy.

        - For AWS, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
        - For Alibaba Cloud, refer to [Manage Keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2).

    7. Return to the TiDB Cloud console, scroll to the bottom of the key creation page, and enter the **KMS Key ARN** that you obtained from your cloud provider KMS.
    8. To verify the trust relationship, click **Test and Add KMS Key ARN**.
    9. After the verification succeeds, click **Create** to finish creating your {{{ .premium }}} instance.

#### Option 2: Service-Managed Encryption Key

To let TiDB Cloud manage the encryption key on your behalf, take the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click **Create Resource**.
2. Select the {{{ .premium }}} plan and complete the basic configuration.
3. In the **Dual-Layer Data Encryption** section, click **Enable**.
4. Select **Service-Managed Encryption Key**.
5. Click **Create** to finish creating your {{{ .premium }}} instance.

### Enable encryption for an existing instance

If you do not enable encryption when creating an instance, you can enable it later. Depending on your requirements, choose either a Customer-Managed Encryption Key (CMEK) or a Service-Managed Encryption Key.

> **Note:**
>
> Enabling encryption on an existing instance might take some time to complete.

#### Option 1: Customer-Managed Encryption Key (CMEK)

Before you begin, make sure that you have created a symmetric encryption key in your cloud provider KMS. Then, take the following steps:

1. On the **Security** page of your {{{ .premium }}} instance, click **Enable** in the **Dual-Layer Data Encryption** section.
2. Select **Customer-Managed Encryption Key (CMEK)**, and then click **Add KMS Key ARN**.
3. Copy the displayed JSON policy statement. This policy statement defines the required key access permissions for TiDB Cloud.
4. In your cloud provider KMS console, append this policy statement to your key policy.

    - For AWS, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
    - For Alibaba Cloud, refer to [Manage Keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2).

5. Return to the TiDB Cloud console, scroll to the bottom of the page, and enter the **KMS Key ARN** that you obtained from your cloud provider KMS.
6. Click **Test and Add KMS Key ARN** to verify the key access configuration and enable Dual-Layer Data Encryption.

#### Option 2: Service-Managed Encryption Key

To let TiDB Cloud manage the encryption key on your behalf, take the following steps:

1. On the **Security** page of your {{{ .premium }}} instance, click **Enable** in the **Dual-Layer Data Encryption** section.
2. Select **Service-Managed Encryption Key**.
3. Click **Enable**.

## View encryption status

After you enable encryption, check the status in the following places:

- On the **Overview** page of your {{{ .premium }}} instance, the **Encryption** field shows the active key management method: either **Enabled with Customer-Managed Encryption Key (CMEK)** or **Enabled with Service-Managed Encryption Key**.
- On the **Security** page, you can view detailed configuration of Dual-Layer Data Encryption.

## Restore from an encrypted backup

Backups created from an encrypted {{{ .premium }}} instance are also encrypted. When you restore an encrypted backup, the new instance must use consistent encryption settings.

> **Note:**
> 
> Currently, you can only restore an encrypted backup to the **same account** and the **same region** as the original instance. Cross-region and cross-account restore operations are not supported.

> **Warning:**
>
> You are fully responsible for maintaining the key's security and availability. If your CMEK is deleted or permanently damaged, any backup data associated with this key will also be completely unrecoverable.

### Restore a backup encrypted with a CMEK

If the backup is encrypted with a CMEK, make sure that the new instance can access the KMS master key during the restore. The key ARN remains unchanged.

To verify access, click **Check** to start the trust policy verification. TiDB Cloud then checks whether the authorized TiDB Cloud account in the key policy matches the account that is associated with the original backup:

- If the accounts match, no further authorization is required.
- If the accounts do not match, copy the provided key policy and update it in your cloud provider KMS. This update re-authorizes the key and ensures that the new instance can access it.

### Restore a backup encrypted with a Service-Managed Encryption Key

If the backup is encrypted with a Service-Managed Encryption Key, the restored instance automatically inherits the same key type. During restore, encryption is enabled by default, and the key type is set to **Service-Managed Encryption Key**.

## Rotate a Customer-Managed Encryption Key (CMEK)

You can configure automatic CMEK rotation in your cloud provider KMS. No configuration updates are required in TiDB Cloud.

- For AWS, see [automatic CMEK rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html).
- For Alibaba Cloud, see [Key rotation](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/configure-key-rotation).

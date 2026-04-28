---
title: Dual-layer Data Encryption
summary: Learn how to enable Dual-layer Data Encryption on {{{ .premium }}} TiDB.
aliases: ['/tidbcloud/premium/tidb-cloud-encrypt-cmek']
---

# Dual-layer Data Encryption

## Overview
{{{ .premium }}} enables data encryption at rest by default on TiDB service instance storage and snapshot volumes. This provides basic encryption capabilities to enhance data security. Building on this, {{{ .premium }}} allows you to combine TiDB service's storage engine encryption with your cloud provider's KMS, adding another layer of data encryption (Dual-layer Data Encryption).

### Encryption mechanism

To provide the highest level of data security, {{{ .premium }}} TiDB adopts a two-tier architecture for data-at-rest encryption. Your data is safeguarded by both Storage-layer and Database-layer protections.

- Storage-layer Data Encryption
  - This is the underlying data encryption directly implemented by cloud service providers on their storage infrastructure. For example, on AWS, this includes EBS volume encryption and S3 bucket encryption.
  - This layer of encryption is enabled by default for all {{{ .premium }}} instances and cannot be disabled. It serves as the foundational security baseline for your data.

- Database-layer Encryption
  - Building on top of the storage-layer encryption, TiDB Cloud allows you to add an extra layer of data encryption at the database level (labeled as **Dual-layer Data Encryption** in the console). Once enabled, static data encryption specifically covers TiKV's stored data and BR's backup data.
  - The TiDB database system ensures that data remains encrypted at rest within the system, thereby effectively reducing the risk of data leakage during subsequent data transfers.
  - Unlike default storage encryption, this feature can be managed by users, allowing you to choose either a Customer-Managed Encryption Key (CMEK) or a Service-Managed Encryption Key based on your security compliance and operational requirements.


#### Backup & Restore Description
When Dual-layer Data Encryption is enabled, the backup data for your {{{ .premium }}} TiDB instance is also encrypted. Any new instance restored from this backup will natively inherit the encryption attributes and KMS master key of the original instance.

Since accessing the backup data relies on the originally configured KMS master key, please ensure the following:

- **Maintain key availability**: Even if you delete the original Premium TiDB instance, the associated KMS master key must remain active to successfully recover the backup data.
- **Ensure correct authorization**: During a restore operation, you must configure the exact same KMS master key associated with the backup and ensure it has the proper permissions for data access.

### Key Management Mechanism

Premium's Dual-layer Data Encryption uses AWS KMS to manage master keys for data-at-rest encryption. Depending on your compliance and maintenance requirements, you can choose between two key management options：

1. **Customer-Managed Encryption Key (CMEK)**: You provide and manage your own AWS KMS master key. This option offers maximum control over your encryption, making it ideal for organizations prioritizing strict security.
- **Important:** You are fully responsible for maintaining the key's security and availability. If the configured CMEK is deleted, your Premium TiDB instance will malfunction, and the encrypted data will become permanently unrecoverable.

2. **Service-Managed Encryption Key**：TiDB Cloud Premium automatically provisions and maintains the KMS master key for you, offering a balance of security and convenience with zero maintenance overhead.
- Key Characteristics:
  - It is a symmetric encryption key.
  - It is automatically generated when you create your first encrypted Premium TiDB instance in a specific region.
  - TiDB Cloud creates one key per organization per region, which is shared across all your Premium instances within that region.
  - The key is automatically removed only after all data encrypted by it within your organization has been completely deleted

## Limitations

- Currently, this feature only supports AWS KMS. Support for Alibaba Cloud KMS and Azure Key Vault will be available soon.
- Data encryption applies to TiKV, CDC, and BR components. Support for TiFlash data encryption is coming soon.
- Once Dual-layer Data Encryption is enabled, the encryption properties of the {{{ .premium }}} instance cannot be modified.
- Custom encryption algorithms are not supported. Additionally, you can only rotate the KMS master key; rotation of other keys is not supported.
- Your AWS KMS key must reside in the same region as your TiDB instance. Consequently, cross-region restore operations are not supported for CMEK-encrypted backups.

## Enable and Manage Encryption

### Enable encryption during instance creation

You can enable Dual-layer Data Encryption when creating a new {{{ .premium }}} instance. Depending on your security compliance and maintenance requirements, you can choose between two key management options: **Customer-Managed Encryption Key (CMEK)** or **Service-Managed Encryption Key**.

#### Option 1: Customer-Managed Encryption Key (CMEK)

To use your own encryption key, follow these steps:

- **Step 1. Create a symmetric encryption key in your AWS KMS (Preparation)**

Before proceeding, you must create a symmetric encryption key in AWS KMS. Ensure the key resides in the **same region** as your planned TiDB service.  For detailed instructions, see [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html).

- **Step 2. Configure CMEK in TiDB Cloud**

1. On the **My TiDB** page, click **Create Resource**.
2. Select the {{{ .premium }}} plan and complete the basic instance configuration.
3. In **Dual-Layer Data Encryption** section, click **Enable**.
4. Select **Customer-Managed Encryption Key (CMEK)** and click **Add KMS Key ARN**.
5. Copy the displayed JSON policy and save it as ROLE-TRUST-POLICY.JSON. This file describes the required trust relationship.
6. In your AWS KMS Console, add this trust relationship to the your key. For more information, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
7. Return to the TiDB Cloud console, scroll to the bottom of the key creation page, and enter the **KMS Key ARN** obtained from AWS KMS.
8. Click **Test and Add KMS Key ARN** to verigy the key trust relationship.
9. Once the verification passes, Click **Create** to finish creating your {{{ .premium }}} instance.

#### Option 2: Service-Managed Encryption Key

To let TiDB Cloud automatically manage the encryption key for you, follow these steps:

1. On the **My TiDB** page, click **Create Resource**.
2. Select the {{{ .premium }}} plan and complete the basic instance configuration.
3. In **Dual-Layer Data Encryption** section, click **Enable**.
4. Select **Service-Managed Encryption Key**.
5. Click **Create** to finish creating your {{{ .premium }}} instance.

### Enable Encryption for an existing instance

If you did not enable encryption during cluster creation, you can still enable it later. Depending on your requirements, you can choose between a Customer-Managed Encryption Key (CMEK) or a Service-Managed Encryption Key.

> **Note:**
>
> Enable Encryption on an existing instance requires some time to complete the activation process.

#### Option 1: Customer-Managed Encryption Key (CMEK)

Before proceeding, ensure you have created a symmetric encryption key in your AWS KMS. Then, follow these steps:

1. On the **Security** page of your {{{ .premium }}} instance, click **Enable** for in the Dual-layer Data Encryption section.
2. Select **Customer-Managed Encryption Key (CMEK)** and click **Add KMS Key ARN**.
3. Copy the displayed JSON policy and save it as ROLE-TRUST-POLICY.JSON. This file describes the required trust relationship.
4. In your AWS KMS console, add this trust policy to your key. For more information, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
5. Return to the TiDB Cloud console, scroll to the bottom of the page, and enter the **KMS Key ARN** obtained from AWS KMS.
6. Click **Test and Add KMS Key ARN** to check the key trust relationship. 
7. Click **Enable** to enable the Dual-layer Data Encryption feature.

#### Option 2: Service-Managed Encryption Key

To let TiDB Cloud automatically manage the encryption key for you, follow these steps:
1. On the Security page of your {{{ .premium }}} instance , click **Enable** in the Dual-layer Data Encryption section.
2. Select **Service-Managed Encryption Key**.
3. Click **Enable**.

### View encryption status

Once encryption is enabled, you can verify its status and configuration details in the following two places:
- Check the **Encryption** property on the **Overview** page of the instance to see the active key management method (either **Enabled with Customer-Managed Encryption Key (CMEK)** or **Enabled with Service-Managed Encryption Key**).
- Navigate to the Security page to view the detailed configuration properties of your Dual-layer Data Encryption.

### Restore from an encrypted backup

Backups generated from an encrypted {{{ .premium }}} instance are also encrypted. When restoring such a backup to a new instance, the restored instance must maintain consistent encryption properties.

#### Customer-Managed Encryption Key (CMEK)

If the backup is encrypted using a CMEK, you must verify that the new instance can correctly access the KMS master key during the restore process:

1. The key ARN will remain unchanged. Click **Check** to proceed with the trust policy verification.
2. The system will check if the authorized TiDB Cloud account in the key policy matches the one associated with the original backup.
3. If the TiDB Cloud account in the key policy is the same as the TiDB Cloud account associated with the original backup TiDB instance, no further authorization is required
4. If the TiDB Cloud account in the key policy is different from the TiDB Cloud account associated with the original backup TiDB instance, you must copy the provided key policy and update it in your AWS KMS. This re-authorizes the key and ensures the new instance can access it.

#### Service-Managed Encryption Key

If the backup is encrypted using a Service-Managed Encryption Key, the restored instance will automatically inherit the same key type. During the restore process, you will see that encryption is enabled by default and the key type is set to **Service-Managed Encryption Key**.


### Rotate Customer-Managed Encryption Key (CMEK)

You can configure [automatic CMEK rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) in AWS KMS. No configuration updates are required in TiDB Cloud.


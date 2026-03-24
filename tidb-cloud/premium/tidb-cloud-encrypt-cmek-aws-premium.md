---
title: Dual-layer Data Encryption
summary: Learn how to enable Dual-layer Data Encryption on Premium TiDB.
aliases: ['/tidbcloud/premium/tidb-cloud-encrypt-cmek']
---

# Dual-layer Data Encryption

Premium enables data encryption at rest by default on TiDB service instance storage and snapshot volumes. This provides basic encryption capabilities to enhance data security. Building on this, Premium allows you to combine TiDB service's storage engine encryption with your cloud provider's KMS, adding another layer of data encryption (Dual-layer Data Encryption).

> **Note:**
>
> The Premium Dual-layer Data Encryption feature will increase your data storage costs. Please see the pricing policy for more information.

## Restrictions

- Currently, Premium's Dual-layer Data Encryption only supports providing key services using AWS KMS.
- Premium's Dual-layer Data Encryption covers data from TiKV, CDC, and BR components. Encryption of TiFlash data will be supported soon.
- When Dual-layer Data Encryption is enabled on Premium TiDB, encryption properties will not be allowed to be modified.
- Only KMS master key rotation is supported; rotation of other keys is not supported.
- User-configured encryption algorithms are not supported. 
- The AWS region for CMEK needs to be consistent with the TiDB instance.
- When CMEK encryption is enabled in Premium, backup data for TiDB instances does not support cross-region recovery operations.

> **Note:**
>
> Premium will continue to be improved and will support Alibaba Cloud KMS and Azure Key Vault as soon as possible.

## Feature Introduction

### Encryption mechanism

Premium supports two layers of data-at-rest encryption to ensure data security. These two layers are Dual-layer Data Encryption and Storage-layer Data Encryption. You can manage Premium's Dual-layer Data Encryption yourself. Premium's Storage-layer Data Encryption is enabled by default, and you cannot disable it.

- Dual-layer Data Encryption
  - This is a layer of data encryption added by TiDB Cloud on top of the storage layer data encryption. 
  - This data encryption is at the database level. Static data encryption covers: TiKV's stored data and BR's backup data.
  - Data is already encrypted within the TiDB database system, effectively preventing data leakage during subsequent transfers.

- Storage-layer Data Encryption
  - This is data encryption implemented by cloud service providers on their storage services. 
  - It mainly includes disk encryption and bucket encryption.  For example, for AWS, this is EBS encryption and S3 encryption.

#### Backup & Restore Description
When Dual-layer Data Encryption is enabled for Premium TiDB, the backup data for that Premium TiDB instance is also encrypted. For a new Premium TiDB instance restored from backup data, its encryption attributes and KMS master key will remain consistent with the original Premium TiDB instance.

Access to backup data also relies on the KMS master key configured on the Dual-layer Data Encryption. To ensure backup data availability, the following aspects need attention:

- Customers need to maintain the availability of the KMS master key associated with the backup data. Even if Premium TiDB is deleted, customers still need to ensure the availability of the associated KMS master key to ensure backup data can be recovered.
- When performing backup data recovery operations, customers need to configure the same KMS master key (the KMS master key associated with the backup data) in the process. Customers need to ensure that the key is correctly authorized to guarantee that the backup data can be accessed normally.

### Key Management Mechanism

Premium's Dual-layer Data Encryption supports providing master keys for data encryption at rest based on AWS KMS. Customers can configure their KMS master keys according to their own security compliance and maintenance requirements. Premium offers two KMS master key configuration methods: Customer-Managed Encryption Key (CMEK) and Service-Managed Encryption Key.

- Customer-Managed Encryption Key (CMEK):
  - This is the KMS Master Key provided by the customer. This gives the customer greater control over TiDB data encryption, resulting in higher security. 
  - Customers are required to ensure the security and availability of their Customer-Managed Encryption Key (CMEK). If customers delete their configured Customer-Managed Encryption Key (CMEK), Premium TiDB will malfunction, and encrypted data at rest will be unrecoverable.
  - If customers prioritize encryption security, they can choose this option—providing CMEK to enable Dual-layer Data Encryption.

- Service-Managed Encryption Key
  - This is the KMS master key provided by TiDB Cloud for its customers. It does not require user maintenance. 
  - If customers prioritize both security and convenience, they can select the Service-Managed Encryption Key when enabling Dual-layer Data Encryption.

#### Service-Managed Encryption Key Description

- The Service-Managed Encryption Key is a symmetric encryption key.
- The Service-Managed Encryption Key is automatically created when a customer creates the first Premium TiDB instance in a region that uses this key for encryption.
- Premium creates one Service-Managed Encryption Key for each organization within the same region. Multiple Premium TiDB instances within the same region will share this key.
- Once all data encrypted with the Service-Managed Encryption Key within an organization has been cleaned up, the Service-Managed Encryption Key will be cleaned up as well.

## Feature Configuration

### Enable Dual-layer Data Encryption when creating Premium TiDB

Customers can choose to enable Dual-layer Data Encryption when creating Premium TiDB. When enabling Dual-layer Data Encryption, customers can configure the encrypted KMS master key according to their own security compliance and maintenance requirements. There are two configuration options for the KMS master key: Customer-Managed Encryption Key (CMEK) and Service-Managed Encryption Key.

#### Customer-Managed Encryption Key (CMEK)

If you wish to enable Dual-layer Data Encryption based on the Customer-Managed Encryption Key (CMEK), please follow these steps.

##### Step 1. Create a symmetric encryption key in your AWS KMS (Preparation)

To enable CMEK-based dual-layer data encryption, you need to create a symmetric encryption key in AWS KMS. The KMS master key you create must be consistent with the region where your TiDB service resides. For more details, see [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html).

##### Step 2. When creating Premium TiDB, configure CMEK in Dual-layer Data Encryption.

Dual-layer Data Encryption should only be enabled when creating Premium TiDB. To do this, follow these steps:

1. On the My TiDB page, click "Create Resource".
2. In the Plan, select Premium and complete the basic configuration.
3. In Dual-Layer Data Encryption, click "Enable".
4. Then select Customer-Managed Encryption Key (CMEK) and click "Add KMS Key ARN" to enter the key configuration page.
5. Copy and save the JSON file as ROLE-TRUST-POLICY.JSON. This file describes the trust relationship.
6. On your AWS KMS service, you need to add this trust relationship to the key policy. For more information, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
7. In the TiDB Cloud console, scroll to the bottom of the key creation page, and then fill in the KMS Key ARN obtained from AWS KMS.
8. Click “Test and Add KMS Key ARN” to check the key trust relationship. After the key trust relationship is configured correctly, you can return to the Premium creation process.
9. Click “Create” to create Premium TiDB.

#### Service-Managed Encryption Key

If you wish to enable Dual-layer Data Encryption based on the Service-Managed Encryption Key, you need to configure it when creating Premium TiDB. Please follow these steps.

1. On the My TiDB page, click "Create Resource".
2. In the Plan, select Premium and complete the basic configuration.
3. In Dual-Layer Data Encryption, click "Enable".
4. Then select Service-Managed Encryption Key.
5. After completing the remaining configurations for Premium TiDB, click "Create" to complete the creation of Premium TiDB.

### Enable Dual-layer Data Encryption on an existing unencrypted Premium TiDB

If you did not enable Dual-layer Data Encryption when creating Premium TiDB, you can still enable it after successful creation. There are two configuration options for the KMS master key: Customer-Managed Encryption Key (CMEK) and Service-Managed Encryption Key.

> **Note:**
>
> Enable Dual-layer Data Encryption on an existing Premium TiDB instance that does not have encryption enabled. This activation process will take some time.

#### Customer-Managed Encryption Key (CMEK)

You need to prepare a symmetric encryption key on your AWS KMS beforehand. Then follow these steps:

1. On the Security page of Premium TiDB service, you can click "Enable" for the Dual-layer Data Encryption feature.
2. Then select Customer-Managed Encryption Key (CMEK) and click "Add KMS Key ARN" to enter the key configuration page.
3. Copy and save the JSON file as ROLE-TRUST-POLICY.JSON. This file describes the trust relationship.
4. On your AWS KMS service, you need to add this trust relationship to the key policy. For more information, refer to [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
5. In the TiDB Cloud console, scroll to the bottom of the key creation page, and then fill in the KMS Key ARN obtained from AWS KMS.
6. Click “Test and Add KMS Key ARN” to check the key trust relationship. 
7. Click “Enable” to enable the Dual-layer Data Encryption feature.

#### Service-Managed Encryption Key

When enabling Dual-layer Data Encryption, you can directly select the Service-Managed Encryption Key. Please follow these steps.

1. On the Security page of Premium TiDB service, you can click "Enable" for the Dual-layer Data Encryption feature.
2. Then select Service-Managed Encryption Key.
3. Click “Enable” to enable the Dual-layer Data Encryption feature.

### View Dual-layer Data Encryption

After enabling Dual-layer Data Encryption in Premium TiDB, you can view it in the following two places:

- You can view the "Encryption" property on the Overview page. The encryption property will display the source of the KMS master key, namely "Enabled with Customer-Managed Encryption Key (CMEK)" and "Enabled with Service-Managed Encryption Key".
- You can view the Dual-layer Data Encryption configuration properties on the Premium TiDB Security page.

### Backup data restore operation under Dual-layer Data Encryption

Backup data generated by a Premium TiDB instance with Dual-layer Data Encryption enabled is also encrypted. Therefore, when restoring this backup data to a new TiDB instance, it is necessary to maintain the consistency of the encryption properties.

#### Customer-Managed Encryption Key (CMEK)

If the Premium TiDB instance is encrypted using a Customer-Managed Encryption Key (CMEK), then verification is required during the recovery process to ensure that the new Premium TiDB instance can correctly access the KMS master key.
During the recovery process, the following checks need to be performed in Dual-layer Data Encryption:

1. In Dual-layer Data Encryption, the key ARN remains unchanged. Click "Check" here to proceed with the KMS master key trust policy check process.
2. In the KMS master key trust check process, check whether the TiDB Cloud account granted in the key policy has changed (compare it with the TiDB Cloud account associated with the original backup TiDB instance).
3. If the TiDB Cloud account in the key policy is the same as the TiDB Cloud account associated with the original backup TiDB instance, then it is not necessary to re-authorize the KMS master key.
4. If the TiDB Cloud account in the key policy is different from the TiDB Cloud account associated with the original backup TiDB instance, then you need to copy the key policy here and then authorize the key in AWS KMS. This ensures that the new Premium TiDB can correctly access the KMS master key.

#### Service-Managed Encryption Key

If the Premium TiDB instance is encrypted using a Service-Managed Encryption Key, then the restored TiDB instance will also be encrypted using a Service-Managed Encryption Key.
Therefore, during the recovery process, you will see that Dual-layer Data Encryption for Premium TiDB is enabled, and the key type is Service-Managed Encryption Key.

### Rotate Customer-Managed Encryption Key (CMEK)

You can configure [automatic CMEK rotation](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html) on AWS KMS. You do not need to update the encryption configuration on TiDB Cloud.

### Customer-Managed Encryption Key (CMEK) Authorization Management

If you need to temporarily revoke TiDB Cloud's access to CMEK, follow these steps:

1. On the AWS KMS console, revoke the corresponding permissions and update the KMS Key policy.
2. On the TiDB Cloud console, pause all Premium TiDB instances that use this KMS master key.

> **Note:**
>
> - Revoking CMEK on AWS KMS will not affect running TiDB instances.
> - When pausing and then resuming a TiDB instance, the TiDB service will not be able to resume normally because CMEK is inaccessible.

After revoking TiDB Cloud's access to CMEK, if you need to restore the access, follow these steps:

1. On the AWS KMS console, restore the CMEK access policy.
2. In the TiDB Cloud console, restore the Premium TiDB instance that uses this KMS master key.

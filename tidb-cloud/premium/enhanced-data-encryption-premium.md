---
title: Enhanced Data Encryption
summary: Learn how to register a Customer-Managed Encryption Key (CMEK) and enable Enhanced Data Encryption for your {{{ .premium }}} instances.
aliases: ['tidbcloud/dual-layer-data-encryption-premium']
---

# Enhanced Data Encryption

Enhanced Data Encryption adds database-layer encryption on top of the cloud provider's default storage-layer encryption to protect your {{{ .premium }}} database data and backup data at rest. With a Customer-Managed Encryption Key (CMEK), you control master key authorization, rotation, and lifecycle in your own cloud account.

You register a key once at the TiDB Cloud organization level and reuse it across {{{ .premium }}} instances in the same cloud provider and region. Key material stays in your cloud KMS; TiDB Cloud stores only the key reference and the metadata needed to manage its authorization, status, and usage.

## Overview

| Task | Where to start | Result |
| --- | --- | --- |
| [Register and authorize a key](#register-a-key) | **Organization Settings** > **CMEK** | Registers and verifies the key in your organization before any instance uses it. |
| [Enable encryption](#enable-enhanced-data-encryption) | Instance creation or the instance **Security** page | Enables CMEK using a registered key in the same cloud provider and region. |
| [View key status and usage](#view-encryption-and-key-status) | **Organization Settings** > **CMEK** | Displays each registered key's status and associated instances and backups. |
| [Restore an encrypted backup](#restore-from-an-encrypted-backup) | The backup restore flow | Uses the required CMEK for restoring an encrypted backup. |
| [Remove an unused key](#remove-a-key) | **Organization Settings** > **CMEK** | Removes the key registration from TiDB Cloud after all usage references are cleared. |

## Before you begin

- Prepare a symmetric encryption key in AWS KMS or Alibaba Cloud KMS in the same cloud provider and region as your target {{{ .premium }}} instances, and ensure that you have permission to update its key policy.
    - For AWS, see [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html).
    - For Alibaba Cloud, see [Understanding KMS keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/overview-of-key-management). You must also be able to share your KMS instance through Alibaba Cloud Resource Directory (Resource Sharing) and enable **Alibaba Cloud Gateway** for the shared TiDB Cloud account.
- Ensure that you have the required TiDB Cloud role. For more information, see [User roles](/tidb-cloud/manage-user-access.md#user-roles).
    - **Manage and view organization keys** (**Organization Settings** > **CMEK**): `Organization Owner`.
    - **Select a registered key** when creating, enabling encryption on, or restoring an instance: the role required for that resource operation (`Organization Owner`, `Project Owner`, or `Instance Manager`).

## Register a key

You can register and authorize a key before creating any {{{ .premium }}} instance. Registering a key makes it available to your organization; it does not enable encryption on an instance.

1. In the [TiDB Cloud console](https://tidbcloud.com), switch to your target organization, navigate to **Organization Settings** > **CMEK**, and start adding a key.
2. Select the cloud provider and region, and copy all generated authorization statements (and on Alibaba Cloud, note the displayed TiDB Cloud account).
3. Configure access in your cloud provider console:

    - **AWS KMS**: Open the key policy of the selected symmetric key and append all generated statements to the existing `Statement` array. Preserve the generated `Principal`, `Action`, and `Condition` fields as well as your existing key administration statements. For more information, see [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html).
    - **Alibaba Cloud KMS**:
        1. In Alibaba Cloud Resource Directory (Resource Sharing), share the KMS instance with the TiDB Cloud account displayed in the TiDB Cloud console.
        2. In the shared list, enable **Alibaba Cloud Gateway** for that TiDB Cloud account.
        3. Open the key policy of the selected symmetric key and append all generated statements to the existing `Statement` array, preserving existing key administration statements. For more information, see [Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2).

    > **Warning:**
    >
    > Append the generated statements to the key policy of the selected KMS key. Do not replace the entire key policy with only the TiDB Cloud statements, or you might lose administrative access to your key.

4. Return to the TiDB Cloud console, enter the key ARN, run the access check to verify that TiDB Cloud can perform the required KMS operations, and save the key.
5. Confirm that the key appears in **Organization Settings** > **CMEK** with status **Idle**. Eligible instances in the same organization, cloud provider, and region can now select this key.

## Enable Enhanced Data Encryption

You can enable Enhanced Data Encryption when creating a {{{ .premium }}} instance or on an existing instance. Once enabled, CMEK cannot be disabled or switched to a different key in place.

Reusing a registered key requires no additional changes to your cloud KMS key policy.

### Enable encryption during instance creation

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click **Create Resource**, select **Premium**, and choose the cloud provider and region.
2. In the **Enhanced Data Encryption** section, enable CMEK and select a registered key in the selected cloud provider and region.
3. If no suitable key is registered, an `Organization Owner` can open the **CMEK** page from the creation flow (opens in a new tab) to register one, and then return to instance creation to select the new key.
4. Complete the remaining settings and click **Create**. TiDB Cloud verifies key access before enabling CMEK.

### Enable encryption for an existing instance

1. In the [TiDB Cloud console](https://tidbcloud.com), open your target {{{ .premium }}} instance, click **Security** in the left navigation pane, and then click **Enable** in the **Enhanced Data Encryption** section.
2. Select a registered key in the instance's cloud provider and region. If no suitable key is registered, an `Organization Owner` can register one in **Organization Settings** > **CMEK** first.
3. Confirm the configuration and check the encryption status after enablement completes.

## View encryption and key status

- **Instance level**: Open the instance **Overview** or **Security** page to view whether Enhanced Data Encryption is enabled and which CMEK protects the instance.
- **Organization level**: Open **Organization Settings** > **CMEK** (requires `Organization Owner`) to view each registered key's status, cloud provider, region, and associated instances and backups.

| Key status | Meaning and next action |
| --- | --- |
| **Verifying** | An access check is running. Wait for verification to complete. |
| **Idle** | The key is registered and verified, and is not currently used by any instance or backup. Eligible instances in the same cloud provider and region can select it. |
| **Applied** | The key is currently used by one or more instances or backups in the same cloud provider and region, and can be reused by other eligible instances. |
| **Error** | The key is unavailable or access verification failed. Restore key availability or authorization in your cloud KMS and verify access again. |

## Manage registered keys

### Handle unavailable keys

If a registered key changes to **Error** or access fails:

1. Review the affected key and resources in **Organization Settings** > **CMEK**.
2. Restore the required key state, policy, or (on Alibaba Cloud) KMS instance sharing and **Alibaba Cloud Gateway** configuration in your cloud KMS.
3. Verify that the key recovers from **Error** and review any affected instances or restore operations.

Because the database caches internal keys in memory for local data operations, disabling or revoking a CMEK does not necessarily affect ongoing operations immediately. The database might continue using cached keys until it next needs to call KMS to unwrap a protected key. All instances and backups using the same CMEK share this availability dependency.

### Remove a key

1. In **Organization Settings** > **CMEK**, review the key's associated instances and backup snapshots.
2. Remove the key registration. TiDB Cloud blocks removal while any instance, backup snapshot, or in-progress restore still depends on the key, even when the key status is **Error**.
3. If removal is blocked, clear all dependent resources first, and then retry and confirm removal.

> **Note:**
>
> Removing a key registration in TiDB Cloud does not delete, disable, or modify the key or its policy in your cloud KMS. Keep the key and its authorization in your cloud KMS for as long as any data or backup still requires it.

## Restore from an encrypted backup

When you restore a {{{ .premium }}} backup, TiDB Cloud checks its encryption metadata and applies the corresponding key requirements in the target region:

| Backup encryption state | Restore behavior and required action |
| --- | --- |
| Encrypted with a CMEK; source key is registered and available | TiDB Cloud matches the source key. Review it and continue; the restored instance uses the same key. |
| Encrypted with a CMEK; source key is not registered | An `Organization Owner` must register and authorize the original key before continuing. Another key cannot decrypt the {{{ .premium }}} backup. |
| Encrypted with a CMEK; source key is in **Error** | Restore the key's availability or correct its authorization in your cloud KMS, then verify access before continuing. |
| Encrypted with a Service-Managed Encryption Key | The restored instance inherits the original encryption configuration. You cannot disable encryption or switch to a CMEK during restore. |
| Database-layer encryption not enabled | Continue without Enhanced Data Encryption, or select a registered key in the target region to enable CMEK on the new instance. |

For a CMEK-protected {{{ .premium }}} backup, you cannot select another key or disable CMEK for the restored instance, and the restore must stay in the original cloud provider and region.

When restoring a CMEK-protected {{{ .dedicated }}} backup to a new {{{ .premium }}} instance (cross-plan restore) in the same cloud provider and region, TiDB Cloud uses the original {{{ .dedicated }}} key to decrypt the source backup and re-encrypts the data with a registered {{{ .premium }}} key for the new instance. Keep the original {{{ .dedicated }}} key active and authorized for decryption, and select a registered {{{ .premium }}} key in the same cloud provider and region (which can be the same key or a different key). For more information about supported restore sources and steps, see [Backup and Restore for {{{ .premium }}}](/tidb-cloud/premium/backup-and-restore-premium.md).

> **Warning:**
>
> Keep the original CMEK active and authorized for as long as you need to restore its backups, even after deleting the source instance. If the required key material is permanently deleted or destroyed, backups encrypted with that key cannot be recovered.

## Rotate a Customer-Managed Encryption Key (CMEK)

Configure key material rotation directly in your cloud KMS. In AWS KMS and Alibaba Cloud KMS, rotating key material keeps the key ID and ARN unchanged, so no configuration update is needed in TiDB Cloud.

Key material rotation updates the underlying material of the same CMEK. It does not switch the instance to a different CMEK, re-encrypt existing data, or remediate an already compromised data encryption key (DEK).

- For AWS, see [Rotate AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html).
- For Alibaba Cloud, see [Key rotation in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/configure-key-rotation).

## How encryption protects your data

### Encryption mechanism

By default, the cloud provider encrypts data at rest at the storage layer (for example, EBS volume encryption and S3 server-side encryption on AWS). Enhanced Data Encryption adds an independent database encryption layer that encrypts database data and backup data before writing it to storage.

Because storage access and database-layer key permissions are managed separately, obtaining a storage object (such as an S3 file after server-side decryption) is not enough to read the data—the database-layer protected contents remain encrypted without the corresponding key chain and KMS authorization.

Enhanced Data Encryption protects data at rest. Because the database processes plaintext during query execution, use [TLS connections](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) and database access controls to protect data in transit and control query access.

### Key hierarchy

The database encryption layer uses envelope encryption with a three-tier key hierarchy. The two encryption layers describe where encryption is applied, while the key hierarchy describes how encryption keys protect one another. A keyspace is the logical storage namespace for an instance.

| Key | Protects | Management |
| --- | --- | --- |
| Customer-managed KMS master key (CMEK) | Keyspace Master Key | Managed and authorized in your cloud KMS account. |
| Keyspace Master Key | Data encryption keys (DEKs) for the keyspace | Persisted copy is encrypted with the CMEK. |
| Data encryption key (DEK) | Database data and logs | Persisted copy is encrypted with the Keyspace Master Key. |

Each instance maintains its own internal key chain, and a single DEK can encrypt multiple files. The database encrypts and decrypts data locally using internal keys cached in memory, while calling your cloud KMS to protect and unwrap upper-level keys.

For symmetric keys generated by AWS KMS, plaintext master key material remains within the KMS hardware security module (HSM) boundary. For more information, see [Data protection in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/data-protection.html).

### Key authorization on AWS

On AWS, the generated key policy grants the displayed TiDB Cloud principal access to your key under an encryption-context condition containing your organization's External ID. AWS KMS evaluates this condition on cryptographic operations and binds the encryption context to the encrypted key material, requiring the exact same context for decryption.

Because TiDB Cloud derives the External ID from your authenticated organization, requests from another organization carry a different context and are rejected by AWS KMS even if the request includes your key ARN.

The External ID is an organization identifier, not a secret. Preserve the generated `Principal`, `Action`, and `Condition` fields when appending the statements to your key policy. For more information, see [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html) in the AWS KMS documentation.

### Key authorization on Alibaba Cloud

On Alibaba Cloud, cross-account access requires sharing your KMS instance with the displayed TiDB Cloud account through Alibaba Cloud Resource Directory (Resource Sharing), enabling **Alibaba Cloud Gateway** for that account in the shared list, and appending the generated statements to the key policy of the selected symmetric key.

Like AWS, the generated key policy grants the displayed TiDB Cloud principal access to your key under an encryption-context condition tied to your organization's External ID, preventing other organizations from using your key. Preserve the generated `Principal`, `Action`, and `Condition` fields when appending the statements to your key policy. For more information, see [Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2).

## Audit key usage

- **Key management in TiDB Cloud**: Enable [console audit logging](/tidb-cloud/tidb-cloud-console-auditing.md) to track key management and instance encryption actions in the TiDB Cloud console.
- **KMS API activity**: On AWS, use [AWS CloudTrail](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html) to review KMS key operations. Cross-account requests rejected for access denial are logged only in the calling account, and KMS events record key operations rather than individual SQL queries.
- **Database access**: Enable [database audit logging](/tidb-cloud/premium/tidb-cloud-auditing-premium.md) to audit SQL queries and database user activity.

## Limitations

- Enhanced Data Encryption for {{{ .premium }}} supports AWS KMS and Alibaba Cloud KMS.
- A registered key is selectable only within its organization, cloud provider, and region. Cross-region restore of CMEK-protected backups is not supported, and restoring a CMEK-protected {{{ .premium }}} backup cannot switch to another key.
- Once enabled, CMEK cannot be disabled or replaced with another key on the same instance.
- Exported data and downstream systems are not covered by the instance CMEK and must be encrypted separately.
- Deleting an instance does not remove its retained backup snapshots or their key dependencies. Permanently losing the required key material makes the dependent encrypted data unrecoverable.

## Troubleshoot key access verification

- **Key registration or verification fails**:
    - Confirm that the key is a symmetric encryption key in the selected cloud provider and region.
    - Confirm that the key is enabled (not disabled or pending deletion) in your cloud KMS.
    - Verify that all generated statements were appended to the key policy without modifying the `Principal`, `Action`, or `Condition` fields.
    - **Alibaba Cloud only**: Confirm that the KMS instance is shared with the displayed TiDB Cloud account through Resource Directory (Resource Sharing) and that **Alibaba Cloud Gateway** is enabled for that account in the shared list.
    - Correct the configuration in your cloud KMS and run the access check again.
- **Registration succeeds, but instance creation, enablement, or restore fails**:
    - Review the error message. If your key policy adds restrictions (such as VPC, IP, or service conditions) that block access, update the policy and retry.
- **Unresolved issues**:
    - Contact [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) with the cloud provider, region, key ARN, operation timestamp, and error message.

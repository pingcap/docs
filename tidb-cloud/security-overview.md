---
title: Security Overview
summary: Learn about the comprehensive security framework of TiDB Cloud, including identity management, network isolation, data protection, access control, and auditing.
---

# Security Overview

TiDB Cloud provides a comprehensive and flexible security framework, covering all stages of the data lifecycle. The platform offers full protection across identity and access management, network security and isolation, data access control, database access control, and audit logging.

## Identity and access management

TiDB Cloud supports multiple authentication methods, including [email and password login](/tidb-cloud/tidb-cloud-password-authentication.md), [standard SSO](/tidb-cloud/tidb-cloud-sso-authentication.md), and [organization-level SSO](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

TiDB Cloud provides layered role and permission management, and you can enable multi-factor authentication (MFA) to strengthen account security. Flexible [identity and access controls](/tidb-cloud/manage-user-access.md) let you manage project and resource access with fine-grained permissions, ensuring that you can maintain the principle of least privilege.

## Network security and isolation

TiDB Cloud provides private endpoints, VPC Peering, and IP access lists for network isolation and access control.

You can encrypt all communications using TLS to ensure the confidentiality and integrity of data in transit. Network access controls ensure that only authorized sources can access cluster resources, enhancing overall security.

## Data access control

For cluster types that support Customer-Managed Encryption Keys (CMEK), TiDB Cloud provides encryption for both data at rest and backups.

Combined with robust key management mechanisms, you can control the lifecycle and usage of encryption keys, further enhancing data security and compliance.

For more information, see [Encryption at Rest Using Customer-Managed Encryption Keys on AWS](/tidb-cloud/tidb-cloud-encrypt-cmek-aws.md) and [Encryption at Rest Using Customer-Managed Encryption Keys on Azure](/tidb-cloud/tidb-cloud-encrypt-cmek-azure.md).

## Database access control

TiDB Cloud provides a user- and role-based access control mechanism, combining static and dynamic privileges. You can assign roles to users to manage and distribute permissions in a more fine-grained way.

For [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) clusters, you can [configure and manage the root account password](/tidb-cloud/configure-security-settings.md) and restrict access through [IP access lists](/tidb-cloud/configure-ip-access-list.md) to protect sensitive accounts.

## Audit logging

TiDB Cloud provides audit logs for both console and database operations to support activity tracking, compliance monitoring, and security incident investigation.

Audit logs record your actions, operation times, and sources, providing reliable evidence for enterprise security management.

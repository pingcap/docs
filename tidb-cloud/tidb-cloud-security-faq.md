---
title: TiDB Cloud Security FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud security.
---

# TiDB Cloud Security FAQs

This document lists the most frequently asked questions about TiDB Cloud security.

## What security and privacy certifications has TiDB Cloud obtained?

TiDB Cloud has obtained the following security and privacy protection certifications:

- SOC 2 Type II
- ISO/IEC 27001:2013
- ISO/IEC 27701
- General Data Protection Regulation (GDPR)

For more information, see [PingCAP Trust & Compliance Center](https://en.pingcap.com/trust-compliance-center).

## How does TiDB Cloud ensure the security of data transfer between client applications and TiDB clusters?

TiDB Cloud provides the encryption ability of data transfer between client applications and TiDB clusters as follows:

- TiDB Cloud supports [VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md), which ensures the security of the data transfer between applications and TiDB cluster.
- For the connection to a TiDB Cloud cluster via a MySQL client, TiDB Cloud enables data transfer encryption by default.

## How does TiDB Cloud encrypt data at rest?

TiDB Cloud provides multi-layer encryption protection measures for data at rest：

- In the data storage layer, TiDB Cloud enables in-cloud service encryption by default, which protects the default encryption of EBS hard drives and S3 storage buckets.
- In the data dumping layer, TiDB Cloud supports users to export data to S3 storage buckets under their cloud accounts.

## What SSO login methods are supported by TiDB Cloud?

TiDB Cloud supports SSO login using Google or GitHub accounts.

## How do I connect to a cluster in TiDB Cloud?

To connect to a cluster in TiDB Cloud, you can use one of the following methods:

- Connect via standard connection, which allows you to create [traffic filters](/tidb-cloud/tidb-cloud-glossary.md#traffic-filter) for the cluster to secure user access.
- Connect via VPC peering connection, which is a networking connection between two VPCs that enables you to route traffic between them using private IP addresses.
- Connect via web SQL shell in the TiDB Cloud console

For more information, see [Connect to Your TiDB Cluster](/tidb-cloud/connect-to-tidb-cluster.md).

## How does TiDB Cloud ensure my account security?

TiDB Cloud accounts consist of TiDB Cloud console accounts and TiDB database accounts. TiDB Cloud ensures user account security with the following protection mechanisms:

- TiDB Cloud console supports email/password login and SSO login. The account security is based on the password security and SSO trust mechanism.

    - Password security:

        - Passwords are stored after being encrypted by bcrypt, not in plain text.
        - TiDB Cloud supports password policy management, including password complexity management, password reuse management, and password validity management.
        - TiDB Cloud supports anti-brute force cracking of passwords. After several consecutive failed login attempts of an account, the account will be locked.

    - SSO: GitHub and Google are currently supported. For SSO users, the account security is guaranteed by GitHub or Google.

- The database account supports account name/password login, and the account security is based on password security.

    - Password security: the password is encrypted and stored in the `mysql.user` system table. The password encryption type is determined by the authentication plug-in. Currently, SHA256 and SHA1 are supported.

## How does TiDB Cloud do role management?

TiDB Cloud manages roles at the following two levels:

- Role management of TiDB Cloud web console

    - To help you manage your organization securely, TiDB Cloud defines the following roles: Owner, Member, Billing Admin, and Billing Admin. For permissions of each role, see [Configure member roles](/tidb-cloud/manage-user-access.md#configure-member-roles).

        Each user has a unique role in an organization and participates in the organization and project management based on the privileges of the role.

    - Console user-defined roles are not supported.

- Role management of TiDB database

    - The role management of TiDB database is based on RBAC, and role permissions are more fine-grained by Access Control List (ACL).
    - Nesting of roles is supported.
    - Database user-defined roles are supported.

## How does TiDB Cloud do database auditing?

In TiDB Cloud, users with the Audit Admin role in an organization can enable or disable the database audit logging feature and configure the audit filtering rules to control which user access events to capture and write to audit logs versus which events to ignore.

The audit logs are stored in your cloud storage buckets so you can view the logs from the buckets easily.

For more information, see [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md).
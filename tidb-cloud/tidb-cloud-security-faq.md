---
title: TiDB Cloud Security FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Security.
---

# TiDB Cloud Security FAQs

This document lists the most frequently asked questions about TiDB Cloud Security.

## What security and privacy certifications has TiDB Cloud obtained?

TiDB Cloud has obtained ISO 27701, ISO27001, GDPR, SOC2, and other security and privacy protection certifications.

## How do you ensure that internal personnel of TiDB Cloud cannot access customer business data?

TiDB Cloud has established a multi-dimensional protection mechanism to ensure that TiDB Cloud internal personnel cannot access customer business data:

- At the strategic level: we adhere to data privacy protection and support the requirements of different industries and individuals for data rights.
- At the design level: we introduce data security and data privacy legal and regulatory requirements from the beginning of platform construction, and continuously integrate them into platform functions and architecture.
- At the architectural level: we design a multi-layer isolation architecture, such as account isolation, VPC isolation, container isolation, and key isolation.
- At the account level: we support the creation of database clusters under customers' own accounts, and realize natural multi-tenant isolation through the own accounts.
- At the VPC level: we support database cluster deployment of independent VPCs. VPCs can be deployed under their own accounts or under independent accounts.
- At the key management level: customers can define private keys, implement end-to-end application-level encryption, and implement data encryption on the application client and server side, and can also be refined to the encryption of business database tables and fields.
- At the privilege management level: customers have full management authority over the database clusters, and can combine their own account system to perform fine-grained authority division and track and audit authority access behaviors.
- At the audit level: we cross-check the authority division and isolation control mechanism of our database platform through multiple third-party audit institutions to ensure that the security compliance needs of customers in different industries are met.

## How does TiDB Cloud prevent a database from being deleted due to misoperations by customers' internal staff?

TiDB Cloud has established an effective mechanism to prevent accidental deletion of databases:

- At the management mechanism level: it is clearly stipulated that when performing the operation of deleting a database, the administrator needs to perform a second authentication and the operation of deleting the database will not be executed until the approval is passed.
- At the policy level: TiDB Cloud separates the special privilege of the system based on the different responsibilities of administrators, and establishes an approval process for special privilege synchronously.
- At the architectural level: we design a database multi-cluster deployment architecture and set a special backup storage directory for the database.
- At the privilege management level: we set administrators and operators based on RBAC or ABAC, and establish a minimum authorization policy including delegated authorization.
- At the level of backup mechanism: we establish database mirroring, backup, and set sub-regional storage location, and set up a backup and archive management mechanism.
- At the operational level: all privileged operations in the database must be approved and reviewed. For special operations, the execution time will be limited, and operators will be rotated regularly.
- At the disaster recovery level: customers need to establish an internal emergency plan for major emergencies, including accidental deletion of databases (recovery based on backup data)
- At the audit level: based on a sound audit management system, regular audit analysis of internal operations is carried out in order to reduce the risk of illegal operations.

## What is the data encryption mechanism during transmission?

TiDB Cloud provides a multi-layer data transmission encryption mechanism.

- At the VPC layer: TiDB Cloud provides VPC Peering and Private Link services for all users to ensure the security of data transmission between applications and TiDB clusters.
- At the container level: TiDB Cloud enables TLS between TiDB cluster internal components by default for business users to ensure data security during data transmission between the internal components of TiDB Cluster of each commercial user.
- At the application level, TiDB Cloud supports a variety of end-to-end data transmission security mechanisms for commercial customers, for example:

    - TiDB Cloud provides TiDB deployment in the customer's own independent account cluster, so that customers can use the KMS Encryption SDK in their cloud accounts to encrypt data of sensitive fields between applications and databases, and ensure the security and integrity of data transmission.
    - For login and remote access, TiDB Cloud provides Internet Web service certificates to provide users with data transmission security during login and registration. It also provides business users with remote access to TiDB cluster data from MySQL and Web Shell clients, and provides TLS to ensure data transmission security.

## What is the encryption mechanism for data at rest?

In terms of data-at-rest protection, TiDB Cloud also provides multi-layer data-at-rest encryption protection measures.

- For data storage, TiDB Cloud enables in-cloud service encryption by default to protect the default encryption of EBS hard drives and S3 storage buckets.
- For data dumping, TiDB Cloud supports users to dump data to S3 storage buckets under their cloud accounts.

## What is the key management mechanism for data-at-rest encryption?

Enable escrow key for data-at-rest encryption.

At the data backup and mirroring level, TiDB Cloud provides escrow key encryption during data backup and supports data backup cross-region at-rest encryption and decryption, helping users have the flexibility to store and restore data.

## How does TiDB Cloud ensure account security?

Accounts are divided into TiDB Cloud web console accounts and TiDB database accounts. The protection mechanisms are as follows:

- TiDB Cloud web console supports email/password login and SSO login, so account security is based on password security and SSO trust mechanism.

    - Password security: passwords are managed by Auth0, which provides the following security protections:

        - Passwords are stored after being encrypted by bcrypt, and passwords are not recorded in plain text.
        - Auth0 supports password policy management, including password complexity management, password reuse management, and password validity management.
        - Auth0 supports anti-brute force cracking of passwords. After several consecutive failed login attempts, the account will be locked.

    - SSO: GitHub and Google are currently supported, and account security is guaranteed by them.

- The database account supports account name/password login, and account security is based on password security.

    - Password security: The password is stored in the `mysql.user` system table, and the password is encrypted and stored (the password encryption type is determined by the authentication plug-in: SHA256 and SHA1 are supported).

## How does TiDB do role management?

- Role management of TiDB Cloud web console

    - For the purpose of organization management, the system defines the following roles: owner, billing_admin, audit_admin, and member. All users have unique roles in the organization, and all users participate in the use and management of organizations and projects based on role attributes.
    - User-defined roles are not supported.

- Role management of TiDB database

    - Role management is based on RBAC, and role permissions are more fine-grained by ACL.
    - Nesting of roles is supported.
    - Database user-defined roles are supported.

## What is the SQL auditing support specification?

SQL auditing supports audit filtering control at the object level (library, table).

SQL auditing supports the organization role audit_admin to enable or disable the auditing function in the TiDB Cloud web console, and supports configuring the audit filtering policy in the console.

SQL auditing supports storing logs in Cloud storage buckets, and supports UI access to auditing information.
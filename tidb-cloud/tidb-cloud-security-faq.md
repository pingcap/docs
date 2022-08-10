---
title: TiDB Cloud Security FAQs
summary: Learn about the most frequently asked questions (FAQs) relating to TiDB Cloud Security.
---

# TiDB Cloud Security FAQs

This document lists the most frequently asked questions about TiDB Cloud Security.

## What security and privacy certifications has TiDB Cloud obtained?

TiDB Cloud has obtained ISO 27701, ISO27001, GDPR, SOC2, and other security and privacy protection certifications.

## How does TiDB Cloud ensure the security of data transfer between client applications and TiDB clusters?

TiDB Cloud provides the ability to encrypt the data transfer between client applications and TiDB Cluster.

- TiDB Cloud provides VPC Peering for all users to secure the data transfer between applications and TiDB Cluster.
- For connecting to TiDB Cluster via mysql client, TiDB Cloud supports the ability to enable data transfer encryption.

## What is the encryption mechanism for data at rest?

TiDB Cloud provides multi-layer encryption protection measures for data at rest：

- In the data storage layer, TiDB Cloud enables in-cloud service encryption by default, which protects the default encryption of EBS hard drives and S3 storage buckets.
- In the data dumping layer, TiDB Cloud supports users to dump data to S3 storage buckets under their cloud accounts.

## What are SSO login methods supported by TiDB Cloud?

TiDB Cloud supports two SSO login methods as follows:

- Google
- GitHub

## How can I connect to a cluster in TiDB Cloud?

TiDB Cloud provides three ways to connect to a cluster.

- Via standard connection, which supports securing user access by creating traffic filters (IP/CIDR address lists) for the cluster.
- Via VPC peering connection
- Via web SQL shell

## How does TiDB Cloud ensure account security?

TiDB Cloud accounts consist of TiDB Cloud console accounts and TiDB database accounts. The protection mechanisms are as follows:

- TiDB Cloud console supports email/password login and SSO login. The account security is based on the password security and SSO trust mechanism.
    - Password security:
        - Passwords are stored after being encrypted by bcrypt, not in plain text.
        - TiDB Cloud supports password policy management, including password complexity management, password reuse management, and password validity management.
        - TiDB Cloud supports anti-brute force cracking of passwords. After several consecutive failed login attempts, the account will be locked.
    - SSO: GitHub and Google are currently supported. For SSO users, the account security is guaranteed by GitHub or Google.
- The database account supports account name/password login, and account security is based on password security.
    - Password security: the password is encrypted and stored in the `mysql.user` system table. The password encryption type is determined by the authentication plug-in. Currently, SHA256 and SHA1 are supported.

## How does TiDB do role management?

- Role management of TiDB Cloud web console

    - To help you manage your organization securely, TiDB Cloud defines the following roles: owner, billing_admin, audit_admin, and member.

    Each user has a unique role in an organization and participates in the organization and project management based on the previleges of the role.

    - Console user-defined roles are not supported.

- Role management of TiDB database

    - The role management of TiDB database is based on RBAC, and role permissions are more fine-grained by Access Control List (ACL).
    - Nesting of roles is supported.
    - Database user-defined roles are supported.

## Does TiDB Cloud support database auditing? If yes, what features are provided?

The database audit logging feature of TiDB Cloud supports controlling the audit filtering rules at both database and table levels.

Database auditing supports the organization role Audit Admin to enable or disable the auditing function in the TiDB Cloud web console, and supports configuring the audit filtering policy in the console.

Database auditing supports storing logs in Cloud storage buckets, and supports UI access to auditing information.
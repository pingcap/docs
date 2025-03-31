---
title: Security
summary: Learn about security concepts for TiDB Cloud.
---

# Security

TiDB Cloud provides a robust and flexible security framework designed to protect data, enforce access control, and meet modern compliance standards. This framework combines advanced security features with operational efficiency to support organizational needs at scale.

**Key components**

- **Identity and Access Management (IAM)**: Secure and flexible authentication and permission management for both the TiDB Cloud console and database environments.

- **Network access control**: Configurable connectivity options, including private endpoints, VPC peering, TLS encryption, and IP access lists.

- **Data access control**: Advanced encryption capabilities, such as Customer-Managed Encryption Keys (CMEK), to safeguard data at rest.

- **Audit logging**: Comprehensive activity tracking for both console actions and database operations, ensuring accountability and transparency.

By integrating these capabilities, TiDB Cloud empowers organizations to safeguard sensitive data, streamline access control, and optimize security operations.

## Identity and access management (IAM)

TiDB Cloud employs Identity and Access Management (IAM) to securely and efficiently manage user identities and permissions across both the console and database environments. IAM features are designed to meet organizational security and compliance needs through a combination of authentication options, role-based access control, and a hierarchical resource structure.

### TiDB Cloud user accounts

TiDB Cloud user accounts are the foundation for managing identity and access to resources. Each account represents an individual or entity within the platform and supports multiple authentication methods to suit organizational needs:

- **Default username and password**

    - Users create accounts with an email address and password.

    - Suitable for small teams or individuals without an external identity provider.

- **Standard SSO authentication**

    - Users log in via GitHub, Google, or Microsoft accounts.

    - Enabled by default for all organizations.

    - **Best practice**: Use for smaller teams or those without strict compliance needs.

    - For more information, see [Standard SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md).

- **Organization SSO authentication**

    - Integrates with corporate identity providers (IdPs) using OIDC or SAML protocols.

    - Enables features like MFA enforcement, password expiration policies, and domain restrictions.

    - **Best practice**: Ideal for larger organizations with advanced security and compliance requirements.

    - For more information, see [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md).

### Database access control

TiDB Cloud provides granular database access control through user-based and role-based permissions. These mechanisms allow administrators to securely manage access to data objects and schemas while ensuring compliance with organizational security policies.

- **Best practices:**

    - Implement the principle of least privilege by granting users only the permissions they need for their roles.

    - Regularly audit and update user access to align with changing organizational requirements.

### Database user accounts

Database user accounts are stored in the `mysql.user` system table and uniquely identified by a username and client host.

During database initialization, TiDB automatically creates a default account: `'root'@'%'`.

For more information, see [TiDB User Account Management](https://docs.pingcap.com/tidb/stable/user-account-management#user-names-and-passwords).

### TiDB privileges and roles

TiDB's privilege management system is based on MySQL 5.7, which enables fine-grained access to database objects. At the same time, TiDB also introduces MySQL 8.0's RBAC and dynamic privilege mechanism. This enables fine-grained and convenient management of database privileges.

**Static privileges**

- Supports fine-grained access control based on database objects, including tables, views, indexes, users, and other objects.

- *Example: Grant SELECT privileges on a specific table to a user.*

**Dynamic privileges**

- Supports reasonable splitting of database management privileges to achieve fine-grained control of system management privileges.

- Example: Assign `BACKUP_ADMIN` to accounts managing database backups without broader administrative permissions.

**SQL roles (RBAC)**

- Group permissions into roles that can be assigned to users, enabling streamlined privilege management and dynamic updates.

- Example: Assign a read-write role to analysts to simplify user access control.

This system ensures flexibility and precision in managing user access while aligning with organizational policies.

### Organization and projects

TiDB Cloud manages users and resources with a hierarchical structure: organizations, projects, and clusters.

**Organizations**

- The top-level entity for managing resources, roles, and billing.

- The organization owner has full permissions, including project creation and role assignment.

**Projects**

- Subdivisions of an organization containing clusters and project-specific configurations.

- Managed by project owners responsible for clusters within their scope.

**Clusters**

- Individual database instances within a project.

### Example structure

```
- Your organization
    - Project 1
        - Cluster 1
        - Cluster 2
    - Project 2
        - Cluster 3
        - Cluster 4
    - Project 3
        - Cluster 5
        - Cluster 6
```

### Key features

- **Granular permissions**:
    - Assign specific roles at both the organization and project levels for precise access control.

    - Ensure flexibility and security by carefully planning role assignments.

- **Billing management**:
    - Billing is consolidated at the organization level, with detailed breakdowns available for each project.

### Identity and Access Management (IAM) Roles

TiDB Cloud provides role-based access control to manage permissions across organizations and projects:

- **[Organization-Level roles](/tidb-cloud/manage-user-access.md#organization-roles)**: Grant permissions to manage the entire organization, including billing and project creation.

- **[Project-Level roles](/tidb-cloud/manage-user-access.md#project-roles)**: Assign permissions to manage specific projects, including clusters and configurations.

## Network access control

TiDB Cloud ensures secure cluster connectivity and data transmission through robust network access controls. Key features include:

### Private endpoints

- Enables secure connectivity for SQL clients within your Virtual Private Cloud (VPC) to TiDB Cloud clusters. For more information, see [Connect to TiDB Cloud via Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-serverless.md).

**Best practices:** Use private endpoints in production to minimize public exposure and review configurations regularly.

### TLS (Transport Layer Security)

- Encrypts communication between clients and servers to secure data transmission.

- Setup guides available for [TiDB Cloud clusters](/tidb-cloud/secure-connections-to-serverless-clusters.md).

**Best practices:** Ensure TLS certificates are current and rotate them periodically.

### IP access list

- Acts as a firewall to restrict cluster access to trusted IP addresses.

- For more information, see [Configure TiDB Cloud Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

**Best practices:** Regularly audit and update the access list to maintain security.

## Data access control

TiDB Cloud safeguards static data with advanced encryption capabilities, ensuring security and compliance with industry regulations.

## Audit logging

TiDB Cloud provides comprehensive audit logging to monitor user activities and database operations, ensuring security, accountability, and compliance.

### Console audit logging

Tracks key actions on the TiDB Cloud console, such as inviting users or managing clusters.

**Best practices:**

- Integrate logs with SIEM tools for real-time monitoring and alerts.

- Set retention policies to meet compliance requirements.
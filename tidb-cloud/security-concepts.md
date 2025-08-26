---
title: Security
summary: 了解 TiDB Cloud 的安全概念。
---

# Security

TiDB Cloud 提供了强大且灵活的安全框架，旨在保护数据、实施访问控制，并满足现代合规标准。该框架将先进的安全特性与高效的运维能力相结合，以支持大规模组织的需求。

**Key components**

- **Identity and Access Management (IAM)**：为 TiDB Cloud 控制台和数据库环境提供安全且灵活的身份认证与权限管理。

- **Network access control**：可配置的连接选项，包括私有终端节点、VPC 对等连接、TLS 加密和 IP 访问列表。

- **Data access control**：高级加密能力，如 Customer-Managed Encryption Keys (CMEK)，用于保护静态数据安全。

- **Audit logging**：对控制台操作和数据库操作的全面活动追踪，确保问责性和透明性。

通过集成这些能力，TiDB Cloud 使组织能够保护敏感数据、简化访问控制并优化安全运维。

## Identity and access management (IAM)

TiDB Cloud 采用 Identity and Access Management (IAM) 来安全高效地管理控制台和数据库环境中的用户身份与权限。IAM 功能通过多种认证选项、基于角色的访问控制以及分层资源结构，满足组织的安全与合规需求。

### TiDB Cloud user accounts

TiDB Cloud 用户账户是管理资源身份和访问的基础。每个账户代表平台内的个人或实体，并支持多种认证方式以适应组织需求：

- **Default username and password**

    - 用户通过邮箱地址和密码创建账户。

    - 适用于没有外部身份提供方的小型团队或个人。

- **Standard SSO authentication**

    - 用户可通过 GitHub、Google 或 Microsoft 账户登录。

    - 默认对所有组织启用。

    - **Best practice**：适用于小型团队或无严格合规需求的团队。

    - 详细信息参见 [Standard SSO Authentication](/tidb-cloud/tidb-cloud-sso-authentication.md)。

- **Organization SSO authentication**

    - 通过 OIDC 或 SAML 协议与企业身份提供方（IdP）集成。

    - 支持 MFA 强制、密码过期策略和域名限制等功能。

    - **Best practice**：适用于有高级安全和合规要求的大型组织。

    - 详细信息参见 [Organization SSO Authentication](/tidb-cloud/tidb-cloud-org-sso-authentication.md)。

### Database access control

TiDB Cloud 通过基于用户和基于角色的权限，提供细粒度的数据库访问控制。这些机制允许管理员安全地管理对数据对象和 schema 的访问，同时确保符合组织的安全策略。

- **Best practices:**

    - 实施最小权限原则，仅授予用户其角色所需的权限。

    - 定期审计和更新用户访问权限，以适应组织需求的变化。

### Database user accounts

数据库用户账户存储在 `mysql.user` 系统表中，并通过用户名和客户端主机唯一标识。

在数据库初始化期间，TiDB 会自动创建一个默认账户：`'root'@'%'`。

详细信息参见 [TiDB User Account Management](https://docs.pingcap.com/tidb/stable/user-account-management#user-names-and-passwords)。

### SQL Proxy accounts

SQL Proxy 账户是 TiDB Cloud 自动生成的特殊用途账户。其主要特性包括：

- **Linked to TiDB Cloud user accounts:** 每个 SQL Proxy 账户对应一个特定的 TiDB Cloud 用户。

- **Mapped to roles:** SQL Proxy 账户被授予 `role_admin` 角色。

- **Token-based:** SQL Proxy 账户使用安全的 JWT 令牌而非密码，确保通过 TiDB Cloud Data Service 或 SQL Editor 实现无缝且受限的访问。

### TiDB privileges and roles

TiDB 的权限管理系统基于 MySQL 5.7，实现了对数据库对象的细粒度访问控制。同时，TiDB 也引入了 MySQL 8.0 的 RBAC 和动态权限机制，实现了数据库权限的细粒度和便捷管理。

**Static privileges**

- 支持基于数据库对象（如表、视图、索引、用户等）的细粒度访问控制。

- *示例：为某用户授予对特定表的 SELECT 权限。*

**Dynamic privileges**

- 支持对数据库管理权限的合理拆分，实现系统管理权限的细粒度控制。

- 示例：为负责数据库备份的账户分配 `BACKUP_ADMIN`，而无需更广泛的管理权限。

**SQL roles (RBAC)**

- 将权限分组为角色，分配给用户，实现权限管理的简化和动态更新。

- 示例：为分析师分配读写角色，简化用户访问控制。

该系统确保了用户访问管理的灵活性和精确性，并与组织策略保持一致。

### Organization and projects

TiDB Cloud 通过分层结构（组织、项目和集群）管理用户和资源。

**Organizations**

- 管理资源、角色和账单的顶层实体。

- 组织所有者拥有全部权限，包括项目创建和角色分配。

**Projects**

- 组织下的子单元，包含集群和项目级配置。

- 由项目所有者管理，负责其范围内的集群。

**Clusters**

- 项目内的独立数据库实例。

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
    - 可在组织和项目级别分配特定角色，实现精确的访问控制。

    - 通过合理规划角色分配，确保灵活性和安全性。

- **Billing management**:
    - 账单在组织级别统一管理，并可为每个项目提供详细拆分。

### Identity and Access Management (IAM) Roles

TiDB Cloud 提供基于角色的访问控制，以管理组织和项目范围内的权限：

- **[Organization-Level roles](/tidb-cloud/manage-user-access.md#organization-roles)**：授予管理整个组织（包括账单和项目创建）的权限。

- **[Project-Level roles](/tidb-cloud/manage-user-access.md#project-roles)**：分配管理特定项目（包括集群和配置）的权限。

## Network access control

TiDB Cloud 通过强大的网络访问控制，确保集群连接和数据传输的安全。主要特性包括：

### Private endpoints

- 允许你在自己的 Virtual Private Cloud (VPC) 内安全连接到 TiDB Cloud Dedicated 集群。

- 支持 [AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections.md)、[Azure Private Link](/tidb-cloud/set-up-private-endpoint-connections-on-azure.md) 和 [Google Cloud Private Service Connect](/tidb-cloud/set-up-private-endpoint-connections-on-google-cloud.md)。

**Best practices:** 在生产环境中使用私有终端节点以最小化公网暴露，并定期检查配置。

### TLS (Transport Layer Security)

- 加密客户端与服务器之间的通信，保障数据传输安全。

- 提供 [Serverless](/tidb-cloud/secure-connections-to-serverless-clusters.md) 和 [Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md) 集群的配置指南。

**Best practices:** 确保 TLS 证书为最新，并定期轮换。

### VPC peering

- 建立虚拟私有云之间的私有连接，实现安全、无缝的通信。

- 详细信息参见 [Connect to TiDB Cloud Dedicated via VPC Peering](/tidb-cloud/set-up-vpc-peering-connections.md)。

**Best practices:** 用于关键业务负载，避免公网暴露，并监控性能。

### IP access list

- 作为防火墙，仅允许受信任的 IP 地址访问集群。

- 详细信息参见 [Configure an IP Access List](/tidb-cloud/configure-ip-access-list.md)。

**Best practices:** 定期审计和更新访问列表，确保安全。

## Data access control

TiDB Cloud 通过高级加密能力保护静态数据，确保安全性并符合行业法规。

**Customer-Managed Encryption Key (CMEK)**

- 为组织提供对 TiDB Cloud Dedicated 集群加密的完全控制权。

- 启用后，使用 CMEK 密钥对静态数据和备份进行加密。

- 对于未启用 CMEK 的 TiDB Cloud Dedicated 集群，TiDB Cloud 使用托管密钥；TiDB Cloud Serverless 集群仅依赖托管密钥。

**Best practices:**

- 定期轮换 CMEK 密钥，以提升安全性并满足合规标准。

- 始终使用 CMEK 密钥加密备份，增强保护。

- 针对如 HIPAA 和 GDPR 等有严格合规要求的行业，建议使用 CMEK。

详细信息参见 [Encryption at Rest Using Customer-Managed Encryption Keys](/tidb-cloud/tidb-cloud-encrypt-cmek.md)。

## Audit logging

TiDB Cloud 提供全面的审计日志功能，用于监控用户活动和数据库操作，确保安全、问责和合规。

### Console audit logging

追踪 TiDB Cloud 控制台上的关键操作，如邀请用户或管理集群。

**Best practices:**

- 将日志集成到 SIEM 工具，实现实时监控和告警。

- 设置日志保留策略，以满足合规要求。

### Database audit logging

记录详细的数据库操作，包括执行的 SQL 语句和用户访问情况。

**Best practices:**

- 定期检查日志，发现异常活动或未授权访问。

- 利用日志进行合规报告和取证分析。

详细信息参见 [Console Audit Logging](/tidb-cloud/tidb-cloud-console-auditing.md) 和 [Database Audit Logging](/tidb-cloud/tidb-cloud-auditing.md)。
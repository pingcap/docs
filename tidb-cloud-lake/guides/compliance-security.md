---
title: 合规与安全
summary: "{{{ .lake }}} 以安全为核心构建，通过多层安全防护、加密标准和合规认证，为您的数据提供全面保护。"
---

# 合规与安全

{{{ .lake }}} 以安全为核心构建，通过多层安全防护、加密标准和合规认证，为您的数据提供全面保护。

## 安全 {#security}

{{{ .lake }}} 实现了多层安全机制，以保护您的数据并控制对资源的访问：

### 访问控制 {#access-control}

{{{ .lake }}} 使用一套全面的访问控制系统，结合了以下机制：

- **Role-Based Access Control (RBAC)**：通过分配给用户的角色管理权限
- **Discretionary Access Control (DAC)**：允许资源所有者直接授予权限

### 数据保护 {#data-protection}

**Masking Policy**：通过控制不同用户查看数据的显示方式来保护敏感数据，帮助您在允许授权访问的同时满足隐私法规要求。

**Network Policy**：控制哪些 IP 地址可以连接到您的 {{{ .lake }}} 资源，使您能够将访问限制在特定网络或位置。

**Password Policy**：通过可自定义的长度、复杂度和轮换要求来强制使用高强度密码，以防止未授权访问。

### 安全连接 {#secure-connectivity}

**PrivateLink**：支持在您的 VPC 与 {{{ .lake }}} 之间建立私有连接，而无需将流量暴露到公共互联网。有关设置说明，请参阅[使用 AWS PrivateLink 连接](/tidb-cloud-lake/guides/connect-with-aws-privatelink.md)或[使用 Alibaba Cloud PrivateLink 连接](/tidb-cloud-lake/guides/connect-with-alibaba-cloud-privatelink.md)。

## 加密 {#encryption}

### TLS 1.2 {#tls-12}

我们为所有通信提供端到端加密。所有客户数据流都仅通过 HTTPS 传输。从客户端到 {{{ .lake }}} API gateway 的连接均使用 TLS 1.2 加密，以确保：

- 传输过程中的数据机密性
- 防止中间人攻击
- 安全的客户端-服务器通信

### 存储加密 {#storage-encryption}

{{{ .lake }}} Enterprise 支持在 Object Storage Service (OSS) 中进行服务端加密。此功能支持您为存储在 OSS 中的数据启用服务端加密，从而增强数据安全性和隐私保护。您可以选择最适合自身需求的加密方式：

- AES-256 加密
- 客户管理密钥 (CMK)
- 硬件安全模块 (HSM) 集成选项

## 合规 {#compliance}

在 {{{ .lake }}}，我们将数据安全和隐私放在首位，并已获得多项关键合规认证，以证明我们对保护您数据的承诺。我们的安全实践会定期接受独立第三方审计，以确保符合业界最高标准。

### SOC 2 Type II {#soc-2-type-ii}

我们已成功获得 SOC 2 Type II 合规认证，并经过独立审计机构验证。该认证确认我们的系统符合 American Institute of Certified Public Accountants (AICPA) 关于安全性、可用性、处理完整性、机密性和隐私的信任服务准则。我们持续监控并改进运营控制措施，以维持这一标准。

### GDPR {#gdpr}

{{{ .lake }}} 遵循《通用数据保护条例》(GDPR)。这是欧盟为保护个人隐私和个人数据而制定的法规。我们的合规实践包括严格执行数据隐私保护、采用强大的加密措施，以及定期开展隐私审计，以确保欧盟范围内用户的权利和数据隐私得到保护。
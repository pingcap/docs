---
title: 连接到 {{{ .premium }}} 的 TLS 连接
summary: 介绍 {{{ .premium }}} 中的 TLS 连接。
---

# 连接到 {{{ .premium }}} 的 TLS 连接

在 TiDB Cloud 上，建立 TLS 连接是连接到 {{{ .premium }}} 实例的基本安全实践之一。你可以从客户端、应用程序和开发工具配置到 {{{ .premium }}} 实例的多个 TLS 连接，以保护数据传输安全。出于安全原因，{{{ .premium }}} 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 或 TLS 1.1。

为确保数据安全，你的 {{{ .premium }}} 实例的证书颁发机构（CA）证书托管在 [AWS Private Certificate Authority](https://aws.amazon.com/private-ca/) 上。CA 证书的私钥存储在由 AWS 管理的硬件安全模块（HSM）中，这些模块符合 [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) 安全标准。

## 前提条件 {#prerequisites}

- 通过[密码认证](/tidb-cloud/tidb-cloud-password-authentication.md)或 [SSO 认证](/tidb-cloud/tidb-cloud-sso-authentication.md)登录 TiDB Cloud，然后[创建一个 {{{ .premium }}} 实例](/tidb-cloud/premium/create-tidb-instance-premium.md)。

- 在安全设置中设置访问实例的密码。

    为此，你可以进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击你的 {{{ .premium }}} 实例所在行中的 **...**，然后选择 **Change Root Password**。在密码设置中，你可以点击 **Auto-generate Password**，自动生成一个长度为 16 个字符的 root 密码，其中包含数字、大写和小写字符以及特殊字符。

## 安全连接到 {{{ .premium }}} 实例 {#secure-connection-to-a-premium-instance}

在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，你可以获取不同连接方法的示例，并按如下方式连接到你的 {{{ .premium }}} 实例：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击你的 {{{ .premium }}} 实例名称，进入其实例概览页面。

2. 点击右上角的 **Connect**。此时会显示一个对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    如果你尚未配置 IP 访问列表，请在首次连接前点击 **Configure IP Access List** 进行配置。更多信息，请参见[配置 IP 访问列表](/tidb-cloud/premium/configure-ip-access-list-premium.md)。

4. 点击 **CA cert** 下载用于连接 {{{ .premium }}} 实例的 TLS 连接 CA cert。该 CA cert 默认支持 TLS 1.2。

    > **注意：**
    >
    > - 你可以将下载的 CA cert 存储在操作系统的默认存储路径中，或指定其他存储路径。在后续步骤中，你需要将代码示例中的 CA cert 路径替换为你自己的 CA cert 路径。
    > - {{{ .premium }}} 不强制客户端使用 TLS 连接，并且当前不支持在 {{{ .premium }}} 上对 [`require_secure_transport`](/system-variables.md#require_secure_transport-new-in-v610) 变量进行用户自定义配置。

5. 选择你偏好的连接方法，然后参考对应标签页中的连接字符串和示例代码连接到你的实例。

## 管理 {{{ .premium }}} 的根证书 {#manage-root-certificates-for-premium}

{{{ .premium }}} 使用来自 [AWS Private Certificate Authority](https://aws.amazon.com/private-ca/) 的证书作为 CA，用于客户端与 {{{ .premium }}} 实例之间的 TLS 连接。通常，CA 证书的私钥会安全地存储在由 AWS 管理的硬件安全模块（HSM）中，这些模块符合 [FIPS 140-2 Level 3](https://csrc.nist.gov/projects/cryptographic-module-validation-program/Certificate/3139) 安全标准。

## 常见问题 {#faqs}

### 连接到我的 {{{ .premium }}} 实例支持哪些 TLS 版本？ {#which-tls-versions-are-supported-to-connect-to-my-premium-instance}

出于安全原因，{{{ .premium }}} 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 或 TLS 1.1。详情请参见 IETF 的 [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/)。

### 是否支持我的客户端与 {{{ .premium }}} 之间的双向 TLS 认证？ {#is-two-way-tls-authentication-between-my-client-and-premium-supported}

不支持。

{{{ .premium }}} 目前仅支持单向 TLS 认证，不支持双向 TLS 认证。如果你需要双向 TLS 认证，请联系 [TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md)。
---
title: TLS Connections to TiDB Cloud Starter or Essential
summary: Introduce TLS connections in TiDB Cloud Starter and TiDB Cloud Essential.
aliases: ['/tidbcloud/secure-connections-to-serverless-tier-clusters']
---

# TiDB Cloud Starter 或 Essential 的 TLS 连接

在你的客户端与 TiDB Cloud Starter 或 TiDB Cloud Essential 集群之间建立安全的 TLS 连接，是连接数据库的基本安全实践之一。TiDB Cloud 的服务器证书由独立的第三方证书颁发机构签发。你可以无需下载服务器端数字证书，轻松连接到你的 TiDB Cloud 集群。

> **Note:**
>
> 如需了解如何与 TiDB Cloud Dedicated 集群建立 TLS 连接，请参见 [TLS Connections to TiDB Cloud Dedicated](/tidb-cloud/tidb-cloud-tls-connect-to-dedicated.md)。

## 前置条件

- 通过 [密码认证](/tidb-cloud/tidb-cloud-password-authentication.md) 或 [SSO 认证](/tidb-cloud/tidb-cloud-sso-authentication.md) 登录 TiDB Cloud。
- [创建一个 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-quickstart.md)。

## 连接 TiDB Cloud 集群的 TLS 方式

在 [TiDB Cloud 控制台](https://tidbcloud.com/) 中，你可以获取不同连接方式的示例，并按如下步骤连接到你的 TiDB Cloud 集群：

1. 进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面，然后点击你的集群名称，进入该集群的概览页面。

2. 点击右上角的 **Connect**，弹出对话框。

3. 在对话框中，保持连接类型的默认设置为 `Public`，并选择你偏好的连接方式和操作系统。

4. 如果你还未设置密码，点击 **Generate Password**，为你的集群生成一个随机密码。该密码会自动嵌入到用于连接集群的示例连接字符串中，便于你快速连接。

    > **Note:**
    >
    > - 随机密码由 16 个字符组成，包括大小写字母、数字和特殊字符。
    > - 关闭该对话框后，生成的密码将不会再次显示，因此你需要将密码保存在安全的位置。如果忘记密码，可以在该对话框中点击 **Reset Password** 进行重置。
    > - TiDB Cloud 集群可通过互联网访问。如果你需要在其他地方使用该密码，建议重置密码以确保数据库安全。

5. 使用连接字符串连接到你的集群。

    > **Note:**
    >
    > 连接 TiDB Cloud 集群时，必须在用户名中包含集群的前缀，并用引号包裹用户名。更多信息请参见 [用户名前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。

## 根证书管理

### 根证书的颁发与有效期

TiDB Cloud 使用 [Let's Encrypt](https://letsencrypt.org/) 作为客户端与 TiDB Cloud 集群之间 TLS 连接的证书颁发机构（CA）。一旦 TiDB Cloud 证书过期，将自动轮换，不会影响你的集群正常运行及已建立的 TLS 安全连接。

如果客户端默认使用系统的根 CA 存储（如 Java 和 Go），你可以无需指定 CA 根路径，直接安全地连接 TiDB Cloud 集群。但部分驱动和 ORM 并不使用系统根 CA 存储，这种情况下，你需要将驱动或 ORM 的 CA 根路径配置为系统根 CA 存储。例如，在 macOS 上使用 [mysqlclient](https://github.com/PyMySQL/mysqlclient) 通过 Python 连接 TiDB Cloud 集群时，需要在 `ssl` 参数中设置 `ca: /etc/ssl/cert.pem`。

如果你使用的是如 DBeaver 这样的 GUI 客户端，且该客户端不接受包含多个证书的证书文件，则必须下载 [ISRG Root X1](https://letsencrypt.org/certs/isrgrootx1.pem) 证书。

### 根证书默认路径

在不同操作系统中，根证书的默认存储路径如下：

**MacOS**

```
/etc/ssl/cert.pem
```

**Debian / Ubuntu / Arch**

```
/etc/ssl/certs/ca-certificates.crt
```

**RedHat / Fedora / CentOS / Mageia**

```
/etc/pki/tls/certs/ca-bundle.crt
```

**Alpine**

```
/etc/ssl/cert.pem
```

**OpenSUSE**

```
/etc/ssl/ca-bundle.pem
```

**Windows**

Windows 没有提供特定的 CA 根路径，而是通过 [注册表](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/local-machine-and-current-user-certificate-stores) 存储证书。因此，在 Windows 上指定 CA 根路径时，请按以下步骤操作：

1. 下载 [ISRG Root X1 证书](https://letsencrypt.org/certs/isrgrootx1.pem)，并将其保存到你选择的路径（如 `<path_to_ca>`）。
2. 连接 TiDB Cloud 集群时，将该路径（`<path_to_ca>`）作为你的 CA 根路径。

## 常见问题

### 连接 TiDB Cloud 集群支持哪些 TLS 版本？

出于安全考虑，TiDB Cloud 仅支持 TLS 1.2 和 TLS 1.3，不支持 TLS 1.0 和 TLS 1.1。详情请参见 IETF [Deprecating TLS 1.0 and TLS 1.1](https://datatracker.ietf.org/doc/rfc8996/)。

### 我的连接客户端与 TiDB Cloud 支持双向 TLS 认证吗？

不支持。

TiDB Cloud 仅支持单向 TLS 认证，即你的客户端使用公钥验证 TiDB Cloud 集群证书私钥的签名，而集群不会验证客户端。

### TiDB Cloud 是否必须配置 TLS 才能建立安全连接？

对于标准连接，TiDB Cloud 只允许 TLS 连接，禁止非 SSL/TLS 连接。原因是 SSL/TLS 是你通过互联网连接 TiDB Cloud 集群时，降低数据暴露风险的最基本安全措施之一。

对于私有终端节点连接，由于其支持高度安全的单向访问 TiDB Cloud 服务且不会将你的数据暴露在公网，是否配置 TLS 是可选的。
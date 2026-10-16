---
title: TiDB Cloud Filesystem 授权
summary: 了解 TiDB Cloud API 凭证、所有者 Token 和范围受限 Token 如何为 TiDB Cloud Filesystem 提供不同级别的访问控制。
---

# TiDB Cloud Filesystem 授权

TiDB Cloud Filesystem 使用不同的凭证来管理文件系统并访问其数据。这样一来，你可以将高权限凭证保存在受信任的环境中，同时仅向用户、应用程序和代理授予其所需的访问权限。

通常情况下，每一层级的访问权限都会进一步收窄：

```plaintext
TiDB Cloud API credentials
        ↓
Manage file system resources
        ↓
Owner token
        ↓
Access one file system
        ↓
Scoped token
        ↓
Access selected paths and operations
```

> **Note:**
>
> TiDB Cloud Filesystem 当前处于公测阶段。其功能和接口如有变更，恕不另行通知。

## 授权模型 {#authorization-model}

TiDB Cloud Filesystem 使用以下几类凭证：

| 凭证 | 访问范围 | 典型用途 |
| -------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| TiDB Cloud API credentials | 根据账户权限管理文件系统资源和所有者 Token | 在受信任环境中进行文件系统管理 |
| Owner token                | 对单个文件系统具有广泛访问权限，包括其数据和范围受限 Token 管理 | 需要完整文件系统访问权限的受信任工作流 |
| Scoped token               | 仅可访问单个文件系统中指定的路径和操作 | 仅需受限访问权限的用户、应用程序、代理或其他机器 |

这些凭证不能互换使用。TiDB Cloud API credentials 用于管理文件系统资源本身，而文件系统 Token 用于控制文件系统内部的访问。

## TiDB Cloud API 凭证 {#tidb-cloud-api-credentials}

TiDB Cloud API 凭证由一对公钥和私钥 API key 组成。其权限由关联的 TiDB Cloud 账户决定。

对于创建、列出、查看和删除文件系统等 CLI 操作，请使用 TiDB Cloud API 凭证。使用 CLI 生成额外的所有者 Token 时，也需要这些凭证。

请将这些凭证保存在受信任的管理或自动化环境中，而不要分发给仅需访问文件系统数据的应用程序或代理。

你可以使用 `ti configure` 配置这些凭证，或者同时提供 `TIDB_CLOUD_PUBLIC_KEY` 和 `TIDB_CLOUD_PRIVATE_KEY`。详情请参见 [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)。

## 所有者 Token {#owner-tokens}

所有者 Token 为单个文件系统提供广泛的访问权限。它可以读、写和删除文件，也可以为该文件系统创建和管理范围受限 Token。

所有者 Token 仅适用于其所属的文件系统。它不能替代 TiDB Cloud API 凭证来执行资源级操作，例如创建或删除文件系统。所有者 Token 也不能创建另一个所有者 Token；生成新的所有者 Token 需要 TiDB Cloud API 凭证。

由于所有者 Token 在文件系统内具有广泛权限，请将其保存在受信任的机器上或 Secret 管理器中。当其他用户、应用程序或代理只需要有限访问权限时，应创建范围受限 Token，而不是共享所有者 Token。

一个文件系统可以同时拥有多个处于活动状态的所有者 Token。这样，不同的用户、应用程序或环境就可以使用各自独立的凭证，而无需共享同一个 Token。

有关生成和管理所有者 Token 的说明，请参见 [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

## 范围受限 Token {#scoped-tokens}

范围受限 Token 将访问限制在单个文件系统中的指定路径和操作范围内。

支持的操作包括：

- `read`：读取文件内容和元信息。
- `list`：列出目录下的条目。
- `search`：搜索允许路径下的文件。`search` 还需要 `read` 权限。
- `write`：创建或修改文件和目录。
- `delete`：删除文件或目录。

例如，一个报表应用程序可以具有：

- 对 `/inputs` 的 `read,list` 访问权限
- 对 `/reports` 的 `read,list,write` 访问权限

另一个仅需查看已生成报表的用户，则可以获得对 `/reports` 的 `read,list` 访问权限。

范围受限权限由文件系统服务强制执行，包括通过挂载访问文件系统时也是如此。范围受限 Token 不能扩大自身权限，也不能创建或管理其他 Token。范围受限 Token 在有效期内可以刷新，但刷新不会扩大其权限。

范围受限 Token 签发后，禁用或回收创建它的所有者 Token，并不会自动回收该范围受限 Token。当不再需要其访问权限时，需要单独回收范围受限 Token。

当你需要向用户、应用程序、代理或其他机器授予文件系统访问权限，而它们又不需要对文件系统的完整访问权限时，请使用范围受限 Token。

有关创建和委派范围受限 Token 的说明，请参见 [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md#generate-and-delegate-a-scoped-token)。

## 凭证边界 {#credential-boundaries}

请根据工作流所需的最小访问权限选择相应凭证：

* 使用 **TiDB Cloud API credentials** 管理文件系统资源。
* 当受信任的工作流需要对单个文件系统具有广泛访问权限，或需要委派访问权限时，使用 **owner token**。
* 当用户、应用程序或代理仅需访问特定路径和操作时，使用 **scoped token**。

即使同一环境中同时存在多种凭证类型，它们的权限也不会叠加。例如，即使同时配置了 TiDB Cloud API credentials，范围受限 Token 仍然只具有其受限范围内的权限。

为了方便使用，TiDB Cloud CLI 可以在本地存储所选的文件系统 Token。本地凭证选择不会更改、禁用或回收远程 Token。有关 `ti` 如何选择文件系统和凭证的详细信息，请参见 [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)。

## 后续内容 {#what-s-next}

- [管理文件系统 Token](/tidb-cloud-filesystem/manage-filesystem-tokens.md)
- [跨机器共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md)
- [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md)
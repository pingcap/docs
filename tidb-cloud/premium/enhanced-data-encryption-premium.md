---
title: 增强数据加密
summary: 了解如何注册 Customer-Managed Encryption Key (CMEK)，并为你的 {{{ .premium }}} 实例启用增强数据加密。
aliases: ['/zh/tidbcloud/dual-layer-data-encryption-premium']
---

# 增强数据加密

增强数据加密在云服务商默认的存储层加密之上增加了数据库层加密，用于保护静态存储的 {{{ .premium }}} 数据库数据和备份数据。借助 Customer-Managed Encryption Key (CMEK)，你可以在自己的云账户中控制主密钥的授权、轮转和生命周期。

你只需在 TiDB Cloud organization 级别注册一次密钥，即可在同一云服务商和 Region 中的多个 {{{ .premium }}} 实例之间复用。密钥材料保留在你的云 KMS 中；TiDB Cloud 仅存储密钥引用以及管理其授权、状态和使用情况所需的元信息。

## 概览 {#overview}

| 任务 | 开始位置 | 结果 |
| --- | --- | --- |
| [注册并授予权限给密钥](#register-a-key) | **Organization Settings** > **CMEK** | 在任何实例使用该密钥之前，在你的组织中注册并验证该密钥。 |
| [启用加密](#enable-enhanced-data-encryption) | 实例创建流程或实例的 **Security** 页面 | 使用同一云服务商和 Region 中已注册的密钥启用 CMEK。 |
| [查看密钥状态和使用情况](#view-encryption-and-key-status) | **Organization Settings** > **CMEK** | 显示每个已注册密钥的状态以及关联的实例和备份。 |
| [从加密备份恢复](#restore-from-an-encrypted-backup) | 备份恢复流程 | 使用恢复加密备份所需的 CMEK。 |
| [移除未使用的密钥](#remove-a-key) | **Organization Settings** > **CMEK** | 在清除所有使用引用后，从 TiDB Cloud 中移除该密钥的注册信息。 |

## 开始之前 {#before-you-begin}

- 在 AWS KMS 或 Alibaba Cloud KMS 中准备一个对称加密密钥，该密钥需与目标 {{{ .premium }}} 实例位于同一云服务商和 Region，并确保你有权限修改其 key policy。
    - 对于 AWS，请参见 [Create a symmetric encryption KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/create-symmetric-cmk.html)。
    - 对于 Alibaba Cloud，请参见 [Understanding KMS keys](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/overview-of-key-management)。你还必须能够通过 Alibaba Cloud Resource Directory (Resource Sharing) 共享你的 KMS 实例，并为共享的 TiDB Cloud 账户启用 **Alibaba Cloud Gateway**。
- 确保你拥有所需的 TiDB Cloud 角色。更多信息，请参见[用户角色](/tidb-cloud/manage-user-access.md#user-roles)。
    - **管理和查看 organization 密钥**（**Organization Settings** > **CMEK**）：`Organization Owner`。
    - 在创建实例、为实例启用加密或恢复实例时**选择已注册的密钥**：需要具备该资源操作所要求的角色（`Organization Owner`、`Project Owner` 或 `Instance Manager`）。

## 注册密钥 {#register-a-key}

你可以在创建任何 {{{ .premium }}} 实例之前注册并授予权限给密钥。注册密钥会使其可供你的 organization 使用；但这不会为某个实例启用加密。

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，切换到目标 organization，进入 **Organization Settings** > **CMEK**，然后开始添加密钥。
2. 选择云服务商和 Region，并复制所有生成的授权语句（对于 Alibaba Cloud，还需记下界面中显示的 TiDB Cloud 账户）。
3. 在云服务商控制台中配置访问权限：

    - **AWS KMS**：打开所选对称密钥的 key policy，并将所有生成的语句追加到现有的 `Statement` 数组中。保留生成的 `Principal`、`Action` 和 `Condition` 字段，以及你现有的密钥管理语句。更多信息，请参见 [Key policies in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)。
    - **Alibaba Cloud KMS**：
        1. 在 Alibaba Cloud Resource Directory (Resource Sharing) 中，将 KMS 实例共享给 TiDB Cloud console 中显示的 TiDB Cloud 账户。
        2. 在共享列表中，为该 TiDB Cloud 账户启用 **Alibaba Cloud Gateway**。
        3. 打开所选对称密钥的 key policy，并将所有生成的语句追加到现有的 `Statement` 数组中，同时保留现有的密钥管理语句。更多信息，请参见 [Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2)。

    > **Warning:**
    >
    > 请将生成的语句追加到所选 KMS 密钥的 key policy 中。不要仅用 TiDB Cloud 语句替换整个 key policy，否则你可能会失去对该密钥的管理访问权限。

4. 返回 TiDB Cloud console，输入 key ARN，运行访问检查以验证 TiDB Cloud 是否可以执行所需的 KMS 操作，然后保存该密钥。
5. 确认该密钥已显示在 **Organization Settings** > **CMEK** 中，且状态为 **Idle**。现在，同一 organization、云服务商和 Region 中符合条件的实例即可选择该密钥。

## 启用增强数据加密 {#enable-enhanced-data-encryption}

你可以在创建 {{{ .premium }}} 实例时启用增强数据加密，也可以在现有实例上启用。启用后，CMEK 不能被禁用，也不能原地切换为其他密钥。

复用已注册密钥时，无需对你的云 KMS key policy 进行额外修改。

### 在创建实例时启用加密 {#enable-encryption-during-instance-creation}

1. 在 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，点击 **Create Resource**，选择 **Premium**，然后选择云服务商和 Region。
2. 在 **Enhanced Data Encryption** 部分，启用 CMEK，并从所选云服务商和 Region 中选择一个已注册密钥。
3. 如果没有合适的已注册密钥，`Organization Owner` 可以在创建流程中打开 **CMEK** 页面（将在新标签页中打开）进行注册，然后返回实例创建页面选择新密钥。
4. 完成其余设置并点击 **Create**。TiDB Cloud 会在启用 CMEK 之前验证密钥访问权限。

### 为现有实例启用加密 {#enable-encryption-for-an-existing-instance}

1. 在 [TiDB Cloud console](https://tidbcloud.com) 中，打开目标 {{{ .premium }}} 实例，点击左侧导航栏中的 **Security**，然后在 **Enhanced Data Encryption** 部分点击 **Enable**。
2. 在该实例所属的云服务商和 Region 中选择一个已注册密钥。如果没有合适的已注册密钥，`Organization Owner` 可以先在 **Organization Settings** > **CMEK** 中注册一个。
3. 确认配置，并在启用完成后检查加密状态。

## 查看加密和密钥状态 {#view-encryption-and-key-status}

- **实例级别**：打开实例的 **Overview** 或 **Security** 页面，查看是否已启用增强数据加密，以及哪个加密密钥正在保护该实例。
- **organization 级别**：打开 **Organization Settings** > **CMEK**（需要 `Organization Owner`）以查看每个已注册密钥的状态、云服务商、Region 以及关联的实例和备份。

| 密钥状态 | 含义和下一步操作 |
| --- | --- |
| **Verifying** | 正在运行访问检查。请等待验证完成。 |
| **Idle** | 该密钥已注册并通过验证，当前未被任何实例或备份使用。同一云服务商和 Region 中符合条件的实例可以选择它。 |
| **Applied** | 该密钥当前正被同一云服务商和 Region 中的一个或多个实例或备份使用，并且可以被其他符合条件的实例复用。 |
| **Error** | 该密钥不可用或访问验证失败。请在你的云 KMS 中恢复密钥可用性或授权，然后再次验证访问。 |

## 管理已注册密钥 {#manage-registered-keys}

### 处理不可用的密钥 {#handle-unavailable-keys}

如果已注册密钥变为 **Error** 或访问失败：

1. 在 **Organization Settings** > **CMEK** 中检查受影响的密钥和资源。
2. 在你的云 KMS 中恢复所需的密钥状态、策略，或（对于 Alibaba Cloud）KMS 实例共享和 **Alibaba Cloud Gateway** 配置。
3. 验证该密钥是否已从 **Error** 状态恢复，并检查任何受影响的实例或恢复操作。

由于数据库会将内部密钥缓存在内存中以执行本地数据操作，因此禁用或撤销 CMEK 不一定会立即影响正在进行的操作。数据库可能会继续使用缓存的密钥，直到下一次需要调用 KMS 来解封受保护密钥时才会受到影响。所有使用同一 CMEK 的实例和备份都共享这一可用性依赖关系。

### 移除密钥 {#remove-a-key}

1. 在 **Organization Settings** > **CMEK** 中，检查该密钥关联的实例和备份快照。
2. 移除该密钥的注册信息。只要仍有任何实例、备份快照或进行中的恢复依赖该密钥，TiDB Cloud 就会阻止移除，即使该密钥状态为 **Error** 也是如此。
3. 如果移除被阻止，请先清除所有依赖资源，然后重试并确认移除。

> **Note:**
>
> 在 TiDB Cloud 中移除密钥注册信息，并不会删除、禁用或修改你云 KMS 中的该密钥或其策略。只要仍有任何数据或备份需要该密钥，就请在你的云 KMS 中保留该密钥及其授权。

## 从加密备份恢复 {#restore-from-an-encrypted-backup}

当你恢复 {{{ .premium }}} 备份时，TiDB Cloud 会检查其加密元信息，并在目标 Region 中应用相应的密钥要求：

| 备份加密状态 | 恢复行为和所需操作 |
| --- | --- |
| 使用 CMEK 加密；源密钥已注册且可用 | TiDB Cloud 会匹配源密钥。检查后继续；恢复出的实例将使用相同的密钥。 |
| 使用 CMEK 加密；源密钥未注册 | `Organization Owner` 必须先注册并授予原始密钥权限，然后才能继续。其他密钥无法解密该 {{{ .premium }}} 备份。 |
| 使用 CMEK 加密；源密钥处于 **Error** 状态 | 在你的云 KMS 中恢复该密钥的可用性或修正其授权，然后在继续之前验证访问。 |
| 使用 Service-Managed Encryption Key 加密 | 恢复出的实例会继承原始加密配置。你不能在恢复过程中禁用加密或切换到 CMEK。 |
| 未启用数据库层加密 | 可以在不启用增强数据加密的情况下继续，或者在目标 Region 中选择一个已注册密钥，为新实例启用 CMEK。 |

对于受 CMEK 保护的 {{{ .premium }}} 备份，你不能为恢复出的实例选择其他密钥，也不能禁用 CMEK，并且恢复必须保持在原始云服务商和 Region 中。

当将受 CMEK 保护的 {{{ .dedicated }}} 备份恢复到同一云服务商和 Region 中新的 {{{ .premium }}} 实例（跨套餐恢复）时，TiDB Cloud 会使用原始 {{{ .dedicated }}} 密钥解密源备份，并使用一个已注册的 {{{ .premium }}} 密钥为新实例重新加密数据。请保持原始 {{{ .dedicated }}} 密钥处于激活并已授权可用于解密的状态，并在同一云服务商和 Region 中选择一个已注册的 {{{ .premium }}} 密钥（可以是同一个密钥，也可以是不同密钥）。有关支持的恢复源和操作步骤的更多信息，请参见 [Backup and Restore for {{{ .premium }}}](/tidb-cloud/premium/backup-and-restore-premium.md)。

> **Warning:**
>
> 只要你仍需要恢复其备份，就请保持原始 CMEK 处于激活并已授权的状态，即使源实例已被删除也是如此。如果所需的密钥材料被永久删除或销毁，则使用该密钥加密的备份将无法恢复。

## 轮转 Customer-Managed Encryption Key (CMEK) {#rotate-a-customer-managed-encryption-key-cmek}

直接在你的云 KMS 中配置密钥材料轮转。在 AWS KMS 和 Alibaba Cloud KMS 中，轮转密钥材料时，密钥 ID 和 ARN 保持不变，因此无需在 TiDB Cloud 中更新配置。

密钥材料轮转会更新同一个 CMEK 的底层材料。它不会将实例切换到另一个 CMEK，不会重新加密现有数据，也不能修复已经泄露的数据加密密钥 (DEK)。

- 对于 AWS，请参见 [Rotate AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html)。
- 对于 Alibaba Cloud，请参见 [Key rotation in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/configure-key-rotation)。

## 加密如何保护你的数据 {#how-encryption-protects-your-data}

### 加密机制 {#encryption-mechanism}

默认情况下，云服务商会在存储层对静态数据进行加密（例如 AWS 上的 EBS 卷加密和 S3 服务端加密）。增强数据加密增加了一个独立的数据库加密层，在将数据库数据和备份数据写入存储之前先对其进行加密。

由于存储访问和数据库层密钥权限是分别管理的，因此仅获取存储对象（例如服务端解密后的 S3 文件）并不足以读取数据——如果没有相应的密钥链和 KMS 授权，数据库层保护的内容仍然是加密状态。

增强数据加密保护的是静态数据。由于数据库在执行查询期间会处理明文数据，请使用 [TLS connections](/tidb-cloud/premium/tidb-cloud-tls-connect-to-premium.md) 和数据库访问控制来保护传输中的数据并控制查询访问。

### 密钥层级 {#key-hierarchy}

数据库加密层使用信封加密，并采用三级密钥层级。两层加密描述的是加密应用的位置，而密钥层级描述的是加密密钥如何相互保护。keyspace 是实例的逻辑存储命名空间。

| 密钥 | 保护对象 | 管理方式 |
| --- | --- | --- |
| Customer-managed KMS 主密钥 (CMEK) | Keyspace Master Key | 在你的云 KMS 账户中管理并授权。 |
| Keyspace Master Key | keyspace 的数据加密密钥 (DEK) | 持久化副本使用 CMEK 加密。 |
| 数据加密密钥 (DEK) | 数据库数据和日志 | 持久化副本使用 Keyspace Master Key 加密。 |

每个实例都维护自己的内部密钥链，单个 DEK 可以加密多个文件。数据库使用缓存在内存中的内部密钥在本地执行数据加密和解密，同时调用你的云 KMS 来保护和解封上层密钥。

对于 AWS KMS 生成的对称密钥，明文主密钥材料始终保留在 KMS hardware security module (HSM) 边界内。更多信息，请参见 [Data protection in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/data-protection.html)。

### AWS 上的密钥授权 {#key-authorization-on-aws}

在 AWS 上，生成的 key policy 会在包含你的 organization External ID 的 encryption-context 条件下，向界面中显示的 TiDB Cloud principal 授予对你密钥的访问权限。AWS KMS 会在加密操作期间评估此条件，并将 encryption context 绑定到已加密的密钥材料上，因此解密时必须提供完全相同的上下文。

由于 TiDB Cloud 会根据你已认证的 organization 派生 External ID，因此来自其他 organization 的请求会携带不同的上下文，即使请求中包含你的 key ARN，也会被 AWS KMS 拒绝。

External ID 是 organization 标识符，而不是 Secret。将这些语句追加到你的 key policy 时，请保留生成的 `Principal`、`Action` 和 `Condition` 字段。更多信息，请参见 AWS KMS 文档中的 [Encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html)。

### Alibaba Cloud 上的密钥授权 {#key-authorization-on-alibaba-cloud}

在 Alibaba Cloud 上，跨账户访问要求你通过 Alibaba Cloud Resource Directory (Resource Sharing) 将 KMS 实例共享给界面中显示的 TiDB Cloud 账户，在共享列表中为该账户启用 **Alibaba Cloud Gateway**，并将生成的语句追加到所选对称密钥的 key policy 中。

与 AWS 类似，生成的 key policy 会在与你的 organization External ID 绑定的 encryption-context 条件下，向界面中显示的 TiDB Cloud principal 授予对你密钥的访问权限，从而防止其他 organization 使用你的密钥。将这些语句追加到你的 key policy 时，请保留生成的 `Principal`、`Action` 和 `Condition` 字段。更多信息，请参见 [Manage Keys in Alibaba Cloud KMS](https://www.alibabacloud.com/help/en/kms/key-management-service/user-guide/manage-keys-2)。

## 审计密钥使用情况 {#audit-key-usage}

- **TiDB Cloud 中的密钥管理**：启用[控制台审计日志](/tidb-cloud/tidb-cloud-console-auditing.md)，以跟踪 TiDB Cloud console 中的密钥管理和实例加密操作。
- **KMS API 活动**：在 AWS 上，使用 [AWS CloudTrail](https://docs.aws.amazon.com/kms/latest/developerguide/logging-using-cloudtrail.html) 查看 KMS 密钥操作。因访问被拒而失败的跨账户请求只会记录在调用方账户中，并且 KMS 事件记录的是密钥操作，而不是单独的 SQL 查询。
- **数据库访问**：启用[数据库审计日志](/tidb-cloud/premium/tidb-cloud-auditing-premium.md)以审计 SQL 查询和数据库用户活动。

## 限制 {#limitations}

- {{{ .premium }}} 的增强数据加密支持 AWS KMS 和 Alibaba Cloud KMS。
- 已注册密钥只能在其所属的 organization、云服务商和 Region 内被选择。不支持对受 CMEK 保护的备份进行跨 Region 恢复，并且恢复受 CMEK 保护的 {{{ .premium }}} 备份时不能切换到其他密钥。
- CMEK 一旦启用，就不能在同一实例上禁用，也不能替换为其他密钥。
- 导出的数据和下游系统不受实例 CMEK 保护，必须单独加密。
- 删除实例不会移除其保留的备份快照或这些快照对密钥的依赖关系。永久丢失所需的密钥材料会导致相关加密数据无法恢复。

## 排查密钥访问验证问题 {#troubleshoot-key-access-verification}

- **密钥注册或验证失败**：
    - 确认该密钥是在所选云服务商和 Region 中的对称加密密钥。
    - 确认该密钥在你的云 KMS 中处于启用状态（未被禁用，也未处于待删除状态）。
    - 验证所有生成的语句都已追加到 key policy 中，且未修改 `Principal`、`Action` 或 `Condition` 字段。
    - **仅适用于 Alibaba Cloud**：确认 KMS 实例已通过 Resource Directory (Resource Sharing) 共享给界面中显示的 TiDB Cloud 账户，并且已在共享列表中为该账户启用 **Alibaba Cloud Gateway**。
    - 在你的云 KMS 中修正配置后，再次运行访问检查。
- **注册成功，但实例创建、启用或恢复失败**：
    - 查看错误消息。如果你的 key policy 添加了会阻止访问的限制（例如 VPC、IP 或服务条件），请更新策略后重试。
- **问题仍未解决**：
    - 请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)，并提供云服务商、Region、key ARN、操作时间戳和错误消息。
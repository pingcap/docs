---
title: 通过公共端点连接 TiDB Cloud Starter 或 Essential
summary: 了解如何通过公共端点连接到你的 TiDB Cloud Starter 或 TiDB Cloud Essential 实例。
---

# 通过公共端点连接 TiDB Cloud Starter 或 Essential

本文档介绍了如何通过公共端点，使用你电脑上的 SQL 客户端连接到 TiDB Cloud Starter 或 TiDB Cloud Essential 实例，以及如何禁用公共端点。

## 选择端点模型 {#choose-an-endpoint-model}

根据你的 TiDB Cloud 计划，选择合适的端点模型：

- 对于 {{{ .starter }}} 实例，或在 2026 年 7 月 1 日之前创建的 {{{ .essential }}} 实例，请使用[**端点共享模型**](#connect-via-a-public-endpoint-endpoint-shared-model)。在此模型中，同一 Region 中的多个 {{{ .starter }}} 和 Essential 实例可以共享一个公共端点。
- 对于从 2026 年 7 月 1 日开始创建的 {{{ .essential }}} 实例，请使用[**端点独占模型**](#connect-via-a-public-endpoint-endpoint-exclusive-model)。在此模型中，每个 {{{ .essential }}} 实例都使用自己的独立公共端点。此模型无需在连接时包含[账户前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)，但你需要为每个 {{{ .essential }}} 实例重复执行设置步骤。

## 通过公共端点连接（端点共享模型） {#connect-via-a-public-endpoint-endpoint-shared-model}

> **提示：**
>
> 如需了解如何通过公共端点连接 TiDB Cloud Dedicated 集群，请参见 [Connect to TiDB Cloud Dedicated via Public Connection](/tidb-cloud/connect-via-standard-connection.md)。

要使用共享模型通过公共端点连接到 {{{ .starter }}} 或 {{{ .essential }}} 实例，请按照以下步骤操作：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 {{{ .starter }}} 或 Essential 实例的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 在对话框中，保持连接类型的默认设置为 `Public`，并选择你偏好的连接方式和操作系统，以获取对应的连接字符串。

    <CustomContent language="en,zh">

    > **注意：**
    >
    > - 保持连接类型为 `Public`，表示通过标准 TLS 连接进行连接。更多信息，请参见 [TLS Connection to {{{ .starter }}} or Essential](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    > - 如果你在 **Connection Type** 下拉列表中选择 **Private Endpoint**，则表示通过私有端点进行连接。更多信息，请参见以下文档：
    >
    >     - [Connect to {{{ .starter }}} or Essential via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)
    >     - [Connect to {{{ .starter }}} or Essential via Alibaba Cloud Private Endpoint](/tidb-cloud/set-up-private-endpoint-connections-on-alibaba-cloud.md)

    </CustomContent>

    <CustomContent language="ja">

    > **注意：**
    >
    > - 保持连接类型为 `Public`，表示通过标准 TLS 连接进行连接。更多信息，请参见 [TLS Connection to {{{ .starter }}} or Essential](/tidb-cloud/secure-connections-to-serverless-clusters.md)。
    > - 如果你在 **Connection Type** 下拉列表中选择 **Private Endpoint**，则表示通过私有端点进行连接。更多信息，请参见 [Connect to {{{ .starter }}} or Essential via AWS PrivateLink](/tidb-cloud/set-up-private-endpoint-connections-serverless.md)。

    </CustomContent>

4. TiDB Cloud 支持为你的 {{{ .starter }}} 实例创建 [branches](https://docs.pingcap.com/tidbcloud/branch-overview/?plan=starter)。创建分支后，你可以通过 **Branch** 下拉列表选择连接到某个分支。`main` 代表 {{{ .starter }}} 实例本身。

5. 如果你还没有设置密码，请点击 **Generate Password** 生成一个随机密码。生成的密码只会显示一次，请妥善保存。

6. 使用连接字符串连接到你的 {{{ .starter }}} 或 Essential 实例。

    > **注意：**
    >
    > 连接 {{{ .starter }}} 或 {{{ .essential }}} 实例时，必须在用户名中包含 {{{ .starter }}} 或 Essential 实例的前缀，并用引号包裹。更多信息，请参见 [User name prefix](/tidb-cloud/select-cluster-tier.md#user-name-prefix)。
    > 你的客户端 IP 必须在 {{{ .starter }}} 或 Essential 实例公共端点的允许 IP 规则中。更多信息，请参见 [Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md)。

## 通过公共端点连接（端点独占模型） {#connect-via-a-public-endpoint-endpoint-exclusive-model}

> **注意：**
>
> 目前，端点独占模型仅适用于在特定 Region 中从 2026 年 7 月 1 日开始创建的 {{{ .essential }}} 实例。如果你的实例不支持该模型，可以改用[端点共享模型](#connect-via-a-public-endpoint-endpoint-shared-model)。

在端点独占模型中，每个 {{{ .essential }}} 实例都使用自己的独立公共端点。此模型无需在连接时包含[账户前缀](/tidb-cloud/select-cluster-tier.md#user-name-prefix)，但你需要为每个 {{{ .essential }}} 实例重复执行设置步骤。

要使用独占模型通过公共端点连接到 {{{ .essential }}} 实例，请按照以下步骤操作：

1. 打开目标实例的概览页面。

    1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/)，然后进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面。

        > **提示：**
        >
        > 如果你属于多个组织，请先使用左上角的组合框切换到目标组织。

    2. 点击目标实例的名称，进入其概览页面。

2. 点击右上角的 **Connect**。此时会弹出连接对话框。

3. 在连接对话框中，从 **Connection Type** 下拉列表中选择 **Public**。

    - 如果公共连接已禁用，请在左侧窗格中点击 **Settings** > **Networking**，然后在 **Networking** 页面启用 **Public Endpoint** 选项。
    - 如果你尚未配置 IP 访问列表，请点击 **Configure IP Access List**，并在首次连接前完成配置。
    - 如果你尚未为 {{{ .essential }}} 实例配置 root 密码，请点击 **Set Root Password** 并进行设置。

4. 点击 **CA cert** 下载用于连接 {{{ .essential }}} 实例的 TLS CA 证书。该 CA 证书默认支持 TLS 1.2。

5. 在 **Connection with** 下拉列表中选择你偏好的连接方式，然后参考连接字符串连接到你的实例。

## 禁用公共端点

如果你不需要使用 TiDB Cloud Starter 或 TiDB Cloud Essential 实例的公共端点，可以将其禁用，以防止来自互联网的连接：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Starter 或 Essential 实例的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Public Endpoint** 对应的 **Disable**。此时会弹出确认对话框。

4. 在确认对话框中点击 **Disable**。

禁用公共端点后，连接对话框的 **Connection Type** 下拉列表中的 `Public` 选项会被禁用。如果用户仍尝试通过公共端点访问 TiDB Cloud Starter 或 Essential 实例，将会收到错误提示。

> **注意：**
>
> 禁用公共端点不会影响已有的连接，只会阻止新的互联网连接。

你可以在禁用后重新启用公共端点：

1. 进入 [**My TiDB**](https://tidbcloud.com/tidbs) 页面，然后点击目标 TiDB Cloud Starter 或 Essential 实例的名称，进入其概览页面。

2. 在左侧导航栏，点击 **Settings** > **Networking**。

3. 在 **Networking** 页面，点击 **Enable**。

## 后续操作

成功连接到 TiDB Cloud Starter 或 Essential 实例后，你可以 [使用 TiDB 探索 SQL 语句](/basic-sql-operations.md)。

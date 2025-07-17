---
title: TiDB Cloud 计费
summary: 了解 TiDB Cloud 计费。
---

# TiDB Cloud 计费

> **注意：**
>
> [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 在 2023 年 5 月 31 日之前免费，享受 100% 折扣。之后，超出[免费配额](/tidb-cloud/select-cluster-tier.md#usage-quota)的使用量将被收费。

TiDB Cloud 根据你消耗的资源进行收费。你可以访问以下页面获取更多关于定价的信息。

- [TiDB Cloud Serverless 定价详情](https://www.pingcap.com/tidb-serverless-pricing-details/)
- [TiDB Cloud Dedicated 定价详情](https://www.pingcap.com/tidb-dedicated-pricing-details/)

## 发票

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以管理 TiDB Cloud 的发票信息。否则，请跳过此部分。

设置支付方式后，TiDB Cloud 会在你的费用达到配额时生成发票，默认配额为 500 美元。如果你想提高配额或每月收到一张发票，可以[联系我们的销售团队](https://www.pingcap.com/contact-us/)。

> **注意：**
>
> 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud，你可以直接通过你的 AWS 账户、Azure 账户或 Google Cloud 账户付款，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

联系我们的销售团队要求每月收到发票后，TiDB Cloud 将在每月初为上个月生成发票。

发票费用包括你组织中的 TiDB 集群使用消耗、折扣、备份存储成本、支持服务成本、信用消费和数据传输成本。

对于每月的发票：

- TiDB Cloud 在每月 9 日向你提供发票。从 1 日到 9 日，你无法查看上个月的费用详情，但可以通过计费控制台获取本月的集群使用信息。
- 支付发票的默认方式是信用卡扣款。如果你想使用其他支付方式，请发送工单请求告知我们。
- 你可以查看当月和上月的费用摘要和详情。

> **注意：**
>
> 所有计费扣款都将通过第三方平台 Stripe 完成。

要查看发票列表，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。

2. 在左侧导航窗格中，点击 **Billing**。

3. 在 **Billing** 页面上，点击 **Invoices** 标签页。

## 计费详情

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以查看和导出 TiDB Cloud 的计费详情。否则，请跳过此部分。

设置支付方式后，TiDB Cloud 将生成历史月份的发票和计费详情，并在每月初生成当月的账单详情。计费详情包括你组织的 TiDB 集群使用消耗、折扣、备份存储成本、数据传输成本、支持服务成本、信用消费和项目拆分信息。

> **注意：**
>
> 由于延迟和其他原因，当月的计费详情仅供参考，不保证准确。TiDB Cloud 确保历史账单的准确性，以便你进行成本核算和满足其他需求。

要查看计费详情，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。

2. 在左侧导航窗格中，点击 **Billing**。

在 **Billing** 页面上，**Bills** 标签页默认显示。

**Bills** 标签页按项目和服务显示计费摘要。你还可以查看使用详情并以 CSV 格式下载数据。

> **注意：**
>
> 由于精度差异，月度账单中的总金额可能与每日使用详情中的总金额不同：
>
> - 月度账单中的总金额四舍五入到小数点后第 2 位。
> - 每日使用详情中的总金额精确到小数点后第 6 位。

## 成本资源管理器

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以查看和分析 TiDB Cloud 的使用成本。否则，请跳过此部分。

要分析和自定义你组织的成本报告，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Cost Explorer** 标签页。
4. 在 **Cost Explorer** 标签页上，展开右上角的 **Filter** 部分以自定义你的报告。你可以设置时间范围，选择分组选项（如按服务、项目、集群、区域、产品类型和收费类型），并通过选择特定服务、项目、集群或区域来应用过滤器。成本资源管理器将向你显示以下信息：

    - **成本图表**：可视化选定时间范围内的成本趋势。你可以在 **Monthly**、**Daily** 和 **Total** 视图之间切换。
    - **成本明细**：根据选定的分组选项显示你的成本的详细明细。为了进一步分析，你可以以 CSV 格式下载数据。

## 计费档案

付费组织可以创建计费档案。此档案中的信息将用于确定税费计算。

要查看或更新你组织的计费档案，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Billing Profile** 标签页。

计费档案中有四个字段。

### 公司名称（可选）

如果指定此字段，此名称将出现在发票上而不是你的组织名称。

### 计费邮箱（可选）

如果指定此字段，发票和其他计费相关通知将发送到此邮箱地址。

### 主要营业地址

这是购买 TiDB Cloud 服务的公司地址。它用于计算任何适用的税费。

### 商业税号（可选）

如果你的企业已注册增值税/商品及服务税，请填写有效的增值税/商品及服务税号。通过提供此信息，如果适用，我们将免除你的增值税/商品及服务税。这对于在增值税/商品及服务税注册允许某些税收豁免或退款的地区运营的企业很重要。

## 信用额度

TiDB Cloud 为概念验证 (PoC) 用户提供一定数量的信用额度。一个信用额度相当于一美元。你可以在信用额度过期之前使用信用额度支付 TiDB 集群费用。

> **提示：**
>
> 要申请 PoC，请参阅[使用 TiDB Cloud 进行概念验证 (PoC)](/tidb-cloud/tidb-cloud-poc.md)。

你的信用额度的详细信息在 **Credits** 标签页上可用，包括你的总信用额度、可用信用额度、当前使用情况和状态。

要查看信用额度信息，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Credits** 标签页。

> **注意：**
>
> - 设置支付方式后，集群费用首先从你的未使用信用额度中扣除，然后从你的支付方式中扣除。
> - 信用额度不能用于支付支持计划费用。

> **警告：**
>
> 在 PoC 过程中：
>
> - 如果你在添加支付方式之前所有信用额度都过期，你将无法创建新集群。3 天后，你现有的所有集群将被回收。7 天后，你的所有备份将被回收。要恢复过程，你可以添加支付方式。
> - 如果你在添加支付方式后所有信用额度都过期，你的 PoC 过程将继续，费用将从你的支付方式中扣除。

## 折扣

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以在 **Discounts** 标签页上查看 TiDB Cloud 的折扣信息。否则，请跳过此部分。

折扣信息包括你收到的所有折扣、状态、折扣百分比以及折扣开始和结束日期。

要查看折扣信息，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Discounts** 标签页。

## 支付方式

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以管理 TiDB Cloud 的支付信息。否则，请跳过此部分。

> **注意：**
>
> 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud，你可以直接通过你的 AWS 账户、Azure 账户或 Google Cloud 账户付款，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

费用根据你的集群使用情况从绑定的信用卡中扣除。要添加有效的信用卡，你可以使用以下任一方法：

- 当你创建 TiDB Cloud Dedicated 集群时：

    1. 在 **Create Cluster** 页面上，点击 **Add Credit Card**。
    2. 在 **Add a Card** 对话框中，填写卡片信息和账单地址。
    3. 点击 **Save Card**。

- 在计费控制台中的任何时候：

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
    2. 在左侧导航窗格中，点击 **Billing**。
    3. 在 **Billing** 页面上，点击 **Payment Method** 标签页，然后点击 **Add a New Card**。
    4. 填写信用卡信息和信用卡地址，然后点击 **Save Card**。

        如果你在[**Billing profile**](#billing-profile) 中没有指定主要营业地址，信用卡地址将用作你的主要营业地址进行税费计算。你可以随时在 **Billing profile** 中更新你的主要营业地址。

> **注意：**
>
> 为确保信用卡敏感数据的安全，TiDB Cloud 不保存任何客户信用卡信息，并将它们保存在第三方支付平台 Stripe 中。所有计费扣款都通过 Stripe 完成。

你可以绑定多张信用卡，并在计费控制台的支付方式中将其中一张设置为默认信用卡。设置后，后续计费将自动从默认信用卡中扣除。

要设置默认信用卡，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Payment Method** 标签页。
4. 在信用卡列表中选择一张信用卡，然后在提示将其设置为默认信用卡时点击 **Yes**。

## 合同

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以在 TiDB Cloud 控制台中管理你的自定义 TiDB Cloud 订阅以满足合规要求。否则，请跳过此部分。

如果你已与我们的销售团队就合同达成一致并收到一封电子邮件要求在线审查和接受合同，你可以执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到你的目标组织。
2. 在左侧导航窗格中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Contract** 标签页。
4. 在 **Contract** 标签页上，找到你想要审查的合同，然后点击合同行中的 **...**。

要了解有关合同的更多信息，请随时[联系我们的销售团队](https://www.pingcap.com/contact-us/)。

## 来自 AWS Marketplace、Azure Marketplace 或 Google Cloud Marketplace 的计费

如果你是组织的 `Organization Owner` 或 `Organization Billing Manager` 角色，你可以将你的 TiDB Cloud 账户链接到 AWS 计费账户、Azure 计费账户或 Google Cloud 计费账户。否则，请跳过此部分。

如果你是 TiDB Cloud 的新用户且没有 TiDB Cloud 账户，你可以通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud 账户，并通过 AWS、Azure 或 Google Cloud 计费账户支付使用费用。

- 要通过 AWS Marketplace 注册，在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账户。
- 要通过 Azure Marketplace 注册，在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账户。
- 要通过 Google Cloud Marketplace 注册，在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕上的说明设置你的 TiDB Cloud 账户。

如果你已有 TiDB Cloud 账户并想通过你的 AWS 或 Google Cloud 计费账户支付使用费用，你可以将你的 TiDB Cloud 账户链接到你的 AWS 或 Google Cloud 计费账户。

<SimpleTab>
<div label="AWS Marketplace">

要将你的 TiDB Cloud 账户链接到 AWS 计费账户，请执行以下步骤：

1. 打开 [AWS Marketplace 页面](https://aws.amazon.com/marketplace)，搜索 `TiDB Cloud` 并在搜索结果中选择 **TiDB Cloud**。显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **Continue to Subscribe**。显示订单页面。

3. 在订单页面上，点击 **Subscribe**，然后点击 **Set Up your Account**。你将被重定向到 TiDB Cloud 注册页面。

4. 检查注册页面上方的通知并点击 **Sign in**。

5. 使用你的 TiDB Cloud 账户登录。显示 **Link to Your AWS Billing Account** 页面。

6. 在 **Link to Your AWS Billing Account** 页面上，选择你的目标组织并点击 **Link** 链接到你的 AWS 计费账户。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已有支付方式，此组织的现有支付方式将被新添加的 AWS 计费账户替换。

</div>

<div label="Azure Marketplace">

要将你的 TiDB Cloud 账户链接到 Azure 计费账户，请执行以下步骤：

1. 打开 [Azure Marketplace 页面](https://azuremarketplace.microsoft.com)，搜索 `TiDB Cloud` 并在搜索结果中选择 **TiDB Cloud on Azure (Preview)**。显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **Get It Now**，接受使用条款，然后点击 **Continue** 进入订单页面。

    > **注意：**
    >
    > 如果你尚未为你的 Microsoft 账户添加国家和地区信息，你还需要在点击 **Continue** 之前输入该信息。

3. 在订单页面上，点击 **Subscribe**，在 **Basics** 标签页上填写所需信息，然后点击 **Review + subscribe**。如果一切看起来都很好，点击 **Subscribe**，然后等待几秒钟完成订阅。

4. 订阅完成后，点击 **Configure account now**。你将被重定向到 TiDB Cloud 注册页面。

5. 检查注册页面上方的通知并点击 **Sign in**。

6. 使用你的 TiDB Cloud 账户登录。显示 **Link to Your Azure Billing Account** 页面。

7. 在 **Link to Your Azure Billing Account** 页面上，选择你的目标组织并点击 **Link** 链接到你的 AWS 计费账户。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已有支付方式，此组织的现有支付方式将被新添加的 Azure 计费账户替换。

</div>

<div label="Google Cloud Marketplace">

要将你的 TiDB Cloud 账户链接到 Google Cloud 计费账户，请执行以下步骤：

1. 打开 [Google Cloud Marketplace 页面](https://console.cloud.google.com/marketplace)，搜索 `TiDB Cloud` 并在搜索结果中选择 **TiDB Cloud**。显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **SUBSCRIBE**。显示订阅页面。

3. 在订阅页面上，点击 **Subscribe**，然后点击 **Go to product page**。你将被重定向到 TiDB Cloud 注册页面。

4. 检查注册页面上方的通知并点击 **Sign in**。

5. 使用你的 TiDB Cloud 账户登录。显示链接到你的 Google Cloud 计费账户的页面。

6. 在页面上，选择目标组织并点击 **Link** 链接到你的 Google Cloud 计费账户。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已有支付方式，此组织的现有支付方式将被新添加的 Google Cloud 计费账户替换。

</div>
</SimpleTab>

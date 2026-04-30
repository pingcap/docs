---
title: TiDB Cloud 计费
summary: 了解 TiDB Cloud 计费。
---

# TiDB Cloud 计费

TiDB Cloud 根据你所消耗的资源进行收费。

## 定价 {#pricing}

### TiDB Cloud Dedicated 的定价 {#pricing-for-tidb-cloud-dedicated}

参见 [TiDB Cloud Dedicated Pricing Details](https://www.pingcap.com/tidb-dedicated-pricing-details/)。

### {{{ .starter }}} 的定价 {#pricing-for-starter}

参见 [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/)。

### {{{ .essential }}} 的定价 {#pricing-for-essential}

对于 {{{ .essential }}}，收费依据是已预配的 Request Capacity Units (RCUs) 数量，**而不是**应用程序的实际使用量。参见 [{{{ .essential }}} Pricing Details](https://www.pingcap.com/tidb-cloud-essential-pricing-details/)。

<CustomContent plan="premium">

### {{{ .premium }}} 的定价 {#pricing-for-premium}

对于 {{{ .premium }}}，计费依据是已预配的 Request Capacity Units (RCUs) 数量以及你实际使用的存储，而不是底层后端节点或已预配的磁盘大小。由于 {{{ .premium }}} 当前处于私有预览阶段，你可以[联系我们的销售团队](https://www.pingcap.com/contact-us/)了解定价详情。

</CustomContent>

## 发票 {#invoices}

如果你在组织中拥有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以管理 TiDB Cloud 的发票信息。否则，请跳过本节。

设置支付方式后，当你的费用达到某个额度时，TiDB Cloud 会生成发票，默认额度为 $500。如果你希望提高该额度或每月接收一张发票，可以[联系我们的销售团队](https://www.pingcap.com/contact-us/)。

<CustomContent language="en,zh">

> **注意：**
>
> 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/)、[Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 或 [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/) 注册 TiDB Cloud，你可以直接通过你的 AWS account、Azure account、Google Cloud account 或 Alibaba Cloud account 付款，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

</CustomContent>

<CustomContent language="ja">

> **注意：**
>
> 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/) 或 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册 TiDB Cloud，你可以直接通过你的 AWS account、Azure account 或 Google Cloud account 付款，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

</CustomContent>

在你联系我们的销售团队以按月接收发票后，TiDB Cloud 会在每月月初生成上个月的发票。

发票费用包括你组织中的 TiDB 资源使用消耗、折扣、备份存储费用、支持服务费用、credit 消耗以及数据传输费用。

对于每月发票：

- TiDB Cloud 会在每月 9 日向你提供发票。从每月 1 日到 9 日期间，你无法查看上个月的费用明细，但可以通过计费控制台获取本月的资源使用信息。
- 支付发票的默认方法是信用卡扣款。如果你希望使用其他支付方式，请提交 ticket 请求告知我们。
- 你可以查看当月和上月费用的汇总与明细。

> **注意：**
>
> 所有计费扣款都将通过第三方平台 Stripe 完成。

要查看发票列表，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Billing**。

3. 在 **Billing** 页面上，点击 **Invoices** 标签页。

## 计费明细 {#billing-details}

如果你在组织中拥有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以查看并导出 TiDB Cloud 的计费明细。否则，请跳过本节。

设置支付方式后，TiDB Cloud 会在每月月初生成历史月份的发票和计费明细，并生成当月的账单明细。计费明细包括你组织的 TiDB 资源使用消耗、折扣、备份存储费用、数据传输费用、支持服务费用、credit 消耗以及项目拆分信息。

> **注意：**
>
> 由于延迟等原因，当月的计费明细仅供参考，不保证准确性。TiDB Cloud 会确保历史账单的准确性，以便你进行成本核算和满足其他需求。

要查看计费明细，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。

2. 在左侧导航栏中，点击 **Billing**。

在 **Billing** 页面上，默认显示 **Bills** 标签页。

**Bills** 标签页显示按项目和实例划分的计费汇总，以及按服务划分的计费汇总。你还可以查看使用明细并以 CSV 格式下载数据。

> **注意：**
>
> 月账单中的总金额可能与每日使用明细中的总金额不同，这是由于精度差异造成的：
>
> - 月账单中的总金额会四舍五入到小数点后第 2 位。
> - 每日使用明细中的总金额精确到小数点后第 6 位。

## 成本分析器 {#cost-explorer}

如果你在组织中拥有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以查看和分析 TiDB Cloud 的使用成本。否则，请跳过本节。

要分析并自定义组织的成本报表，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Cost Explorer** 标签页。
4. 在 **Cost Explorer** 标签页中，展开右上角的 **Filter** 部分以自定义报表。你可以设置时间范围、选择分组选项（例如按服务、项目、集群、region、产品类型和收费类型分组），并通过选择特定服务、项目、集群或 region 来应用筛选条件。成本分析器将向你显示以下信息：

    - **Cost Graph**：以可视化方式展示所选时间范围内的成本趋势。你可以在 **Monthly**、**Daily** 和 **Total** 视图之间切换。
    - **Cost Breakdown**：根据所选分组选项显示成本的详细拆分。为了进一步分析，你可以将数据下载为 CSV 格式。

## 计费资料 {#billing-profile}

付费组织可以创建计费资料。此资料中的信息将用于确定税费计算。

要查看或修改组织的计费资料，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Billing Profile** 标签页。

计费资料中有四个字段。

### 公司名称（可选） {#company-name-optional}

如果指定了此字段，该名称将显示在发票上，而不是你的组织名称。

### 计费邮箱（可选） {#billing-email-optional}

如果指定了此字段，发票和其他与计费相关的通知将发送到此邮箱地址。

### 主要营业地址 {#primary-business-address}

这是购买 TiDB Cloud 服务的公司的地址。它用于计算适用的税费。

### 企业税号（可选） {#business-tax-id-optional}

如果你的企业已注册 VAT/GST，请填写有效的 VAT/GST ID。提供此信息后，如果适用，我们将免除向你收取 VAT/GST。这对于在 VAT/GST 注册可享受某些税务减免或退税的地区运营的企业非常重要。

## Credits {#credits}

TiDB Cloud 为概念验证 (PoC) 用户提供一定数量的 credits。一个 credit 等同于一美元。你可以在 credits 过期之前使用它们支付 TiDB 使用费用。

> **提示：**
>
> 要申请 PoC，请参见 [Perform a Proof of Concept (PoC) with TiDB Cloud](/tidb-cloud/tidb-cloud-poc.md)。

你的 credits 详细信息可在 **Credits** 标签页中查看，包括总 credits、可用 credits、当前使用量和状态。

要查看 credit 信息，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Credits** 标签页。

> **注意：**
>
> - 设置支付方式后，资源使用费用会先从你未使用的 credits 中扣除，然后再从你的支付方式中扣除。
> - credits 不能用于支付支持计划费用。

> **警告：**
>
> 在 PoC 过程中：
>
> - 如果在你添加支付方式之前，所有 credits 都已过期，则你无法创建新的 TiDB Cloud Dedicated 集群。3 天后，你现有的所有 TiDB Cloud Dedicated 集群都将被回收。7 天后，你的所有备份都将被回收。要恢复该过程，你可以添加支付方式。
> - 如果在你添加支付方式之后，所有 credits 都已过期，则你的 PoC 过程会继续，费用将从你的支付方式中扣除。

## 折扣 {#discounts}

如果你在组织中拥有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以在 **Discounts** 标签页中查看 TiDB Cloud 的折扣信息。否则，请跳过本节。

折扣信息包括你收到的所有折扣、状态、折扣百分比以及折扣开始和结束日期。

要查看折扣信息，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Discounts** 标签页。
## 支付方式 {#payment-method}

如果你在所属组织中具有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以管理 TiDB Cloud 的支付信息。否则，请跳过本节。

<CustomContent language="en,zh">

> **注意：**
>
> 如果你通过 [AWS Marketplace](https://aws.amazon.com/marketplace)、[Azure Marketplace](https://azuremarketplace.microsoft.com/)、[Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 或 [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/) 注册 TiDB Cloud，你可以直接通过你的 AWS account、Azure account、Google Cloud account 或 Alibaba Cloud account 付款，但无法在 TiDB Cloud 控制台中添加支付方式或下载发票。

</CustomContent>

<CustomContent language="ja">

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), [Azure Marketplace](https://azuremarketplace.microsoft.com/), or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account, Azure account, or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

</CustomContent>

费用会根据你的资源使用情况从已绑定的信用卡中扣除。要添加有效的信用卡，你可以使用以下任一方法：

- 在创建 TiDB Cloud Dedicated 集群时：

    1. 在 **Create Resource** 页面上，点击 **Add Credit Card**。
    2. 在 **Add a Card** 对话框中，填写卡信息和账单地址。
    3. 点击 **Save Card**。

- 在 billing 控制台中随时添加：

    1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
    2. 在左侧导航栏中，点击 **Billing**。
    3. 在 **Billing** 页面上，点击 **Payment Method** 页签，然后点击 **Add a New Card**。
    4. 填写信用卡信息和信用卡地址，然后点击 **Save Card**。

        如果你未在 [**Billing profile**](#billing-profile) 中指定主要营业地址，则信用卡地址将用作你的主要营业地址以进行税费计算。你可以随时在 **Billing profile** 中修改你的主要营业地址。

> **注意：**
>
> 为确保信用卡敏感数据的安全，TiDB Cloud 不保存任何客户信用卡信息，而是将其保存在第三方支付平台 Stripe 中。所有账单扣费均通过 Stripe 完成。

你可以绑定多张信用卡，并在 billing 控制台的支付方式中将其中一张设置为默认信用卡。设置后，后续账单将自动从默认信用卡中扣除。

要设置默认信用卡，请执行以下步骤：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Payment Method** 页签。
4. 在信用卡列表中选择一张信用卡，然后在系统提示将其设置为默认信用卡时点击 **Yes**。

## 合同 {#contract}

如果你在所属组织中具有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以在 TiDB Cloud 控制台中管理自定义的 TiDB Cloud 订阅，以满足合规要求。否则，请跳过本节。

如果你已与我们的销售团队就合同达成一致，并收到一封用于在线查看和接受合同的电子邮件，你可以执行以下操作：

1. 在 [TiDB Cloud 控制台](https://tidbcloud.com) 中，使用左上角的下拉框切换到目标组织。
2. 在左侧导航栏中，点击 **Billing**。
3. 在 **Billing** 页面上，点击 **Contract** 页签。
4. 在 **Contract** 页签上，找到你要查看的合同，然后点击该合同所在行中的 **...**。

如需了解有关合同的更多信息，欢迎[联系我们的销售团队](https://www.pingcap.com/contact-us/)。

## 来自云服务商 Marketplace 的计费 {#billing-from-cloud-provider-marketplace}

<CustomContent language="en,zh">

如果你在所属组织中具有 `Organization Owner` 或 `Organization Billing Manager` 角色，则可以将你的 TiDB Cloud 账户 关联到云服务商（AWS、Azure、Google Cloud 或 Alibaba Cloud）的 billing account。否则，请跳过本节。

</CustomContent>

<CustomContent language="ja">

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can link your TiDB Cloud account to the billing account of your cloud provider (AWS, Azure, or Google Cloud). Otherwise, skip this section.

</CustomContent>

如果你是 TiDB Cloud 新用户且还没有 TiDB Cloud 账户，你可以通过云服务商的 marketplace 注册 TiDB Cloud 账户，并通过云服务商的 billing account 支付使用费用。

<CustomContent language="en,zh">

- 要通过 [AWS Marketplace](https://aws.amazon.com/marketplace) 注册，请在 [AWS Marketplace](https://aws.amazon.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕提示设置你的 TiDB Cloud 账户。
- 要通过 [Azure Marketplace](https://azuremarketplace.microsoft.com) 注册，请在 [Azure Marketplace](https://azuremarketplace.microsoft.com) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕提示设置你的 TiDB Cloud 账户。
- 要通过 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 注册，请在 [Google Cloud Marketplace](https://console.cloud.google.com/marketplace) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕提示设置你的 TiDB Cloud 账户。
- 要通过 [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/) 注册，请在 [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/) 中搜索 `TiDB Cloud`，订阅 TiDB Cloud，然后按照屏幕提示设置你的 TiDB Cloud 账户。

如果你已经有 TiDB Cloud 账户，并且希望通过 AWS、Azure、Google Cloud 或 Alibaba Cloud 的 billing account 支付使用费用，则可以将你的 TiDB Cloud 账户关联到 AWS、Azure、Google Cloud 或 Alibaba Cloud 的 billing account。

</CustomContent>

<CustomContent language="ja">

- To sign up through [AWS Marketplace](https://aws.amazon.com/marketplace), search for `TiDB Cloud` in [AWS Marketplace](https://aws.amazon.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- To sign up through [Azure Marketplace](https://azuremarketplace.microsoft.com), search for `TiDB Cloud` in [Azure Marketplace](https://azuremarketplace.microsoft.com), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.
- To sign up through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), search for `TiDB Cloud` in [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), subscribe to TiDB Cloud, and then follow the onscreen instructions to set up your TiDB Cloud account.

If you already have a TiDB Cloud account and you want to pay for the usage via your AWS, Azure, or Google Cloud billing account, you can link your TiDB Cloud account to your AWS, Azure, or Google Cloud billing account.

</CustomContent>

<SimpleTab>
<div label="AWS Marketplace">

要将你的 TiDB Cloud 账户关联到 AWS billing account，请执行以下步骤：

1. 打开 [AWS Marketplace 页面](https://aws.amazon.com/marketplace)，搜索 `TiDB Cloud`，并在搜索结果中选择 **TiDB Cloud**。此时会显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **Continue to Subscribe**。此时会显示订单页面。

3. 在订单页面上，点击 **Subscribe**，然后点击 **Set Up your Account**。你将被引导至 TiDB Cloud 注册页面。

4. 查看注册页面上方的通知并点击 **Sign in**。

5. 使用你的 TiDB Cloud 账户登录。此时会显示 **Link to Your AWS Billing Account** 页面。

6. 在 **Link to Your AWS Billing Account** 页面上，选择目标组织并点击 **Link**，以关联到你的 AWS billing account。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已经有支付方式，则该组织现有的支付方式将被新添加的 AWS billing account 替换。

</div>

<div label="Azure Marketplace">

要将你的 TiDB Cloud 账户关联到 Azure billing account，请执行以下步骤：

1. 打开 [Azure Marketplace 页面](https://azuremarketplace.microsoft.com)，搜索 `TiDB Cloud`，并在搜索结果中选择 **TiDB Cloud on Azure (Preview)**。此时会显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **Get It Now**，接受使用条款，然后点击 **Continue** 进入订单页面。

    > **注意：**
    >
    > 如果你尚未为 Microsoft account 添加国家和 Region 信息，则还需要在点击 **Continue** 之前输入这些信息。

3. 在订单页面上，点击 **Subscribe**，在 **Basics** 页签中填写所需信息，然后点击 **Review + subscribe**。确认无误后，点击 **Subscribe**，然后等待几秒钟以完成订阅。

4. 订阅完成后，点击 **Configure account now**。你将被引导至 TiDB Cloud 注册页面。

5. 查看注册页面上方的通知并点击 **Sign in**。

6. 使用你的 TiDB Cloud 账户登录。此时会显示 **Link to Your Azure Billing Account** 页面。

7. 在 **Link to Your Azure Billing Account** 页面上，选择目标组织并点击 **Link**，以关联到你的 AWS billing account。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已经有支付方式，则该组织现有的支付方式将被新添加的 Azure billing account 替换。

</div>

<div label="Google Cloud Marketplace">

要将你的 TiDB Cloud 账户关联到 Google Cloud billing account，请执行以下步骤：

1. 打开 [Google Cloud Marketplace 页面](https://console.cloud.google.com/marketplace)，搜索 `TiDB Cloud`，并在搜索结果中选择 **TiDB Cloud**。此时会显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **SUBSCRIBE**。此时会显示订阅页面。

3. 在订阅页面上，点击 **Subscribe**，然后点击 **Go to product page**。你将被引导至 TiDB Cloud 注册页面。

4. 查看注册页面上方的通知并点击 **Sign in**。

5. 使用你的 TiDB Cloud 账户登录。此时会显示用于关联到你的 Google Cloud billing account 的页面。

6. 在该页面上，选择目标组织并点击 **Link**，以关联到你的 Google Cloud billing account。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已经有支付方式，则该组织现有的支付方式将被新添加的 Google Cloud billing account 替换。

</div>

<CustomContent language="en,zh">

<div label="Alibaba Cloud Marketplace">

要将你的 TiDB Cloud 账户关联到 Alibaba Cloud billing account，请执行以下步骤：

1. 打开 [Alibaba Cloud Marketplace 页面](https://marketplace.alibabacloud.com/)，搜索 `TiDB Cloud`，并在搜索结果中选择 **TiDB Cloud**。此时会显示 TiDB Cloud 产品页面。

2. 在 TiDB Cloud 产品页面上，点击 **Activate Now**，然后按照屏幕提示确认按量付费模式并查看激活申请。

3. 在订阅页面上，找到你的 TiDB Cloud 订阅，然后点击 **Auto Login**。你将被引导至 TiDB Cloud 注册页面。

4. 查看注册页面上方的通知并点击 **Sign in**。

5. 使用你的 TiDB Cloud 账户登录。此时会显示用于关联到你的 Alibaba Cloud billing account 的页面。

6. 在该页面上，选择目标组织并点击 **Link**，以关联到你的 Alibaba Cloud billing account。

    > **注意：**
    >
    > 如果你的组织在 TiDB Cloud 中已经有支付方式，则该组织现有的支付方式将被新添加的 Alibaba Cloud billing account 替换。

</div>
</CustomContent>
</SimpleTab>
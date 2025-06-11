---
title: TiDB Cloud Billing
summary: Learn about TiDB Cloud billing.
---

# TiDB Cloud Billing

> **Note:**
>
> [TiDB Cloud Starter clusters](/tidb-cloud/select-cluster-tier.md#tidb-cloud-starter) are free until June 9, 2025, with a 100% discount off. After that, usage beyond the [free quota](/tidb-cloud/select-cluster-tier.md#usage-quota) will be charged.

TiDB Cloud charges according to the resources that you consume.

## Pricing

TiDB Cloud offers the following two pricing options to suit different needs:

* TiDB Cloud Starter: you are charged based on the number of Request Units (RUs) consumed by your application.
* TiDB Cloud Essential: you are charged based on the number of provisioned Request Capacity Units (RCUs), **not** on the actual usage by your application.

> **Note:**
>
> Some features such as Restore are currently in beta and are free of charge. We will update the pricing for these features in the future.

### Request Unit (RU) and Request Capacity Unit (RCU)

A **Request Unit (RU)** is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

A **Request Capacity Unit (RCU)** is a unit of measure used to represent the provisioned compute capacity for your TiDB Cloud Essential cluster. One RCU provides a fixed amount of compute resources that can process a certain number of RUs per second. The number of RCUs you provision determines your cluster's baseline performance and throughput capacity.

Currently, the RU includes statistics for the following resources:

<table><thead>
  <tr>
    <th>Resource</th>
    <th>RU Consumption</th>
  </tr></thead>
<tbody>
  <tr>
    <td rowspan="3">Read</td>
    <td>2 storage read batches consume 1 RU</td>
  </tr>
  <tr>
    <td>8 storage read requests consume 1 RU</td>
  </tr>
  <tr>
    <td>64 KiB read request payload consumes 1 RU</td>
  </tr>
  <tr>
    <td rowspan="4">Write*</td>
    <td>2 storage write batches consume 1 RU</td>
  </tr>
  <tr>
    <td>2 storage write requests consume 1 RU</td>
  </tr>
  <tr>
    <td>2 KiB write request payload consumes 1 RU</td>
  </tr>
  <tr>
    <td>16 KiB write request payload consumes 1 RU (for transactions** &gt;= 16MiB)</td>
  </tr>
  <tr>
    <td>SQL CPU</td>
    <td>3 ms consumes 1 RU</td>
  </tr>
  <tr>
    <td rowspan="2">Network Egress</td>
    <td>1 KiB read consumes 1 RU for public endpoint</td>
  </tr>
  <tr>
    <td>4 KiB read consumes 1 RU for private endpoint</td>
  </tr>
</tbody>
</table>

> **Note:**
>
> - Write*: Each write operation is duplicated to multiple storage processes (3 for row-based storage without index), and each duplicate is considered a distinct write operation.
> - Transaction**: This applies only to optimistic transactions or autocommit.

### Pricing for TiDB Cloud Starter

See the detailed pricing for each available Alibaba Cloud region below.

| Resource | Singapore |
|----------|-----------|
| Compute (per 1 million RUs) | $0.1 |
| Row-based storage (per GiB/month) | $0.36 |
| Columnar storage (per GiB/month) | $0.09 |

> **Tip:**
>
> TiDB Cloud Starter is currently available in the Alibaba Cloud Singapore region. For other regions on Alibaba Cloud, contact the Help center in the console.

#### Free quota

TiDB Cloud offers a free quota up to the first 5 clusters created in each [organization](/tidb-cloud/manage-user-access.md#organizations). To create more clusters, you will be required to provide a credit card and set a [Monthly Spending Limit](#monthly-spending-limit). But if you delete some of your previous clusters before creating the 6th, the new cluster will still have a free quota. In other words, you can enjoy the free quota for up to 5 clusters.

Free quota is issued monthly to TiDB Cloud Starter clusters that meet these qualifications. With the free quota, each TiDB Cloud Starter cluster can store 5 GiB of row-based data, 5 GiB of columnar data, and consume up to 50 million RUs per month.

In total, each organization can get 25 GiB of row-based storage, 25 GiB of columnar storage, and 250 million Request Units (RUs) for free per month. Customers can take advantage of this offer and optimize their operations without worrying about initial costs.

#### Monthly Spending Limit

The Monthly Spending Limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that enables you to set a budget for your TiDB Cloud Starter clusters. The Monthly Spending Limit must be set to at least $0.01.

> **Note:**
>
> You cannot set a spending limit lower than the amount already spent in the current month.

#### Throttling

A cluster will not be throttled unless the spending limit is reached. Once the spending limit is reached, the cluster immediately denies any new connection attempts until the quota is increased or the usage is reset at the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling.

If the free quota of a cluster is exhausted within the month, the cluster is automatically throttled. This limit will remain in place until you [upgrade it to a scalable cluster](/tidb-cloud/manage-serverless-spend-limit.md#update-spending-limit) or until the next month.

In this way, customers can ensure basic business continuity without paying additional fees. At the same time, customers can adjust the spending limit according to their needs to control their usage and costs.

### Pricing for TiDB Cloud Essential

See the detailed pricing for each available Alibaba Cloud region below.

| Resource | Singapore |
|----------|-----------|
| Compute (per RCU/month) | $0.24 |
| Row-based storage (per GiB/month) | $0.36 |
| Columnar storage (per GiB/month) | $0.09 |

> **Tip:**
>
> TiDB Cloud Essential is currently available in the Alibaba Cloud Singapore region. For other regions on Alibaba Cloud, contact the Help center in the console.

#### Throttling

For TiDB Cloud Essential clusters, the throttling policy is based on the provisioned Request Capacity Units (RCUs). When the workload exceeds the maximum RCU capacity, the cluster will automatically throttle incoming requests to maintain stability. Existing connections will experience throttling, but new connection attempts will be accepted as long as they don't exceed the maximum RCU limit. This ensures predictable performance while protecting the cluster from overload.

### Billing cycle

Each TiDB Cloud bill, corresponding to the previous month's usage, is finalized at the start of every new month. This finalized bill is charged to your default payment method, typically occurring between the 3rd and 9th day of the respective month. If your usage within the current month reaches or exceeds $500, an automatic charge will be initiated. Note that the billing cycle operates strictly in accordance with the UTC (+00:00) time zone.

## Invoices

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can manage the invoice information of TiDB Cloud. Otherwise, skip this section.

After you set up the payment method, TiDB Cloud will generate an invoice once your cost reaches a quota, which is $500 by default. If you want to raise the quota or receive one invoice per month, you can [contact our sales](https://www.pingcap.com/contact-us/).

> **Note:**
>
> If you sign up for TiDB Cloud through [Alibaba Cloud Marketplace](https://marketplace.alibabacloud.com/), [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your Alibaba cloud account, AWS account, or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

After you contact our sales for receiving an invoice on a monthly basis, TiDB Cloud will generate the invoice for the previous month at the beginning of each month.

Invoice costs include TiDB cluster usage consumption, discounts, backup storage costs, support service cost, credit consumption, and data transmission costs in your organization.

For each monthly invoice:

- TiDB Cloud provides the invoice to you on the ninth of each month. From the first to the ninth day, you cannot view the last month's cost details, but can obtain the cluster usage information of this month via the billing console.
- The default method for paying invoices is credit card deduction. If you want to use other payment methods, please send a ticket request to let us know.
- You can view the summary and details of charges for the current month and the previous month.

> **Note:**
>
> All billing deductions will be completed through the third-party platform Stripe.

To view the list of invoices, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. In the left navigation pane, click the **Billing** tab.

3. Click the **Invoices** tab. The invoices page is displayed.

## Billing details

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can view and export the billing details of TiDB Cloud. Otherwise, skip this section.

After setting the payment method, TiDB Cloud will generate the invoice and billing details of the historical months, and generate the bill details of the current month at the beginning of each month. The billing details include your organization's TiDB cluster usage consumption, discounts, backup storage costs, data transmission costs, support service cost, credit consumption, and project splitting information.

> **Note:**
>
> Due to delays and other reasons, the billing details of the current month are for reference only, not guaranteed to be accurate. TiDB Cloud ensures the accuracy of historical bills so that you can perform cost accounting and meet other needs.

To view the billing details, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. Click **Billing**.
3. Click **Bills**. The billing details page is displayed.

The billing details page shows the billing summary by project and by service. You can also see the usage details and download the data in CSV format.

> **Note:**
>
> The total amount in the monthly bill might differ from that in the daily usage details due to differences in precision:
>
> - The total amount in the monthly bill is rounded off to the 2nd decimal place.
> - The total amount in the daily usage details is accurate to the 6th decimal place.

## Cost explorer

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can view and analyze the usage costs of TiDB Cloud. Otherwise, skip this section.

To analyze and customize your cost reports of your organization, perform the following steps:

1. In the lower-left corner of the [TiDB Cloud console](https://console.tidb.io/signup?provider_source=alicloud), click <MDSvgIcon name="icon-top-organization" />, and then click **Billing**.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. On the **Billing** page, click the **Cost Explorer** tab.
3. On the **Cost Explorer** page, expand the **Filter** section in the upper-right corner to customize your report. You can set the time range, select a grouping option (such as by service, project, cluster, region, product type, and charge type), and apply filters by selecting specific services, projects, clusters, or regions. The cost explorer will display you with the following information:

    - **Cost Graph**: visualizes the cost trends over the selected time range. You can switch between **Monthly**, **Daily**, and **Total** views.
    - **Cost Breakdown**: displays a detailed breakdown of your costs according to the selected grouping option. For further analysis, you can download the data in CSV format.

## Billing profile

Paid organizations can create a billing profile. Information in this profile will be used to determine the tax calculation.

To view or update the billing profile of your organization, click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner and then click **Billing** > **Billing Profile**.

There are four fields in the billing profile.

### Company name (optional)

If this field is specified, this name will appear on invoices instead of your organization name.

### Billing email (optional)

If this field is specified, invoices and other billing-related notifications will be sent to this email address.

### Primary business address

This is the address of the company that purchases TiDB Cloud services. It is used to calculate any applicable taxes.

### Business tax ID (optional)

If your business is registered for VAT/GST, fill in a valid VAT/GST ID. By providing this information, we will exempt you from charging VAT/GST if applicable. This is important for businesses operating in regions where VAT/GST registration allows for certain tax exemptions or refunds.

## Credits

TiDB Cloud offers a certain number of credits for Proof of Concept (PoC) users. One credit is equivalent to one U.S. dollar. You can use credits to pay TiDB cluster fees before the credits become expired.

The detailed information of your credits is available on the **Credits** page, including your total credits, available credits, current usage, and the status.

To view this page, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. Click **Billing**.
3. Click **Credits**. The credit details page is displayed.

> **Note:**
>
> - After you set up your payment method, the cluster fees are first deducted from your unused credits, then from your payment method.
> - Credits cannot be used to pay the support plan fees.

> **Warning:**
>
> During a PoC process:
>
> - If all your credits become expired before you add a payment method, you cannot create a new cluster. After 3 days, all your existing clusters will be recycled. After 7 days, all your backups will be recycled. To resume the process, you can add a payment method.
> - If all your credits become expired after you add a payment method, your PoC process goes on, and fees are deducted from your payment method.

## Discounts

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can view the discount information of TiDB Cloud on the **Discounts** page. Otherwise, skip this section.

The discount information includes all discounts that you have received, the status, the discount percentage, and the discount start and end date.

To view this page, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. Click **Billing**.
3. Click **Discounts**. The discount details page is displayed.

## Payment method

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can manage the payment information of TiDB Cloud. Otherwise, skip this section.

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://console.cloud.google.com/marketplace), you can pay through your AWS account or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud console.

The fee is deducted from a bound credit card according to your cluster usage. To add a valid credit card, you can use either of the following methods:

- When you are creating a cluster:

    1. Before you click **Create Cluster** on the **Create a Cluster** page, click **Add Credit Card** at the bottom of the **Billing Calculator** pane.
    2. In the **Add a Card** dialog box, fill in the card information and billing address.
    3. Click **Save Card**.

- Anytime in the billing console:

    1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

        > **Note:**
        >
        > If you are in multiple organizations, switch to your target organization by clicking its name.

    2. Click **Billing**.
    3. Under the **Payment Method** tab, click **Add a New Card**.
    4. Fill in the credit card information and credit card address, and then click **Save Card**.

        If you do not specify a primary business address in [**Billing profile**](#billing-profile), the credit card address will be used as your primary business address for tax calculation. You can update your primary business address in **Billing profile** anytime.

> **Note:**
>
> To ensure the security of credit card sensitive data, TiDB Cloud does not save any customer credit card information and saves them in the third-party payment platform Stripe. All billing deductions are completed through Stripe.

You can bind multiple credit cards, and set one of them as the default credit card in the payment method of the billing console. After setting, subsequent billings will be automatically deducted from the default credit card.

To set the default credit card, perform the following steps:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. Click **Billing**.
3. Click the **Payment Method** tab.
4. Select a credit card in the credit card list, and click **Set as default**.

## Contract

If you are in the `Organization Owner` or `Organization Billing Manager` role of your organization, you can manage your customized TiDB Cloud subscriptions in the TiDB Cloud console to meet compliance requirements. Otherwise, skip this section.

If you have agreed with our sales on a contract and received an email to review and accept the contract online, you can do the following:

1. Click <MDSvgIcon name="icon-top-organization" /> in the lower-left corner of the TiDB Cloud console.

    > **Note:**
    >
    > If you are in multiple organizations, switch to your target organization by clicking its name.

2. Click **Billing**.
3. Click **Contract**. The contract list is displayed.
4. Click **Download**, **Accept**, or **Reject** according to your need.

To learn more about contracts, feel free to [contact our sales](https://www.pingcap.com/contact-us/).
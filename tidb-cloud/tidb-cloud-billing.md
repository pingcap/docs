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

Two pricing options are available for TiDB Cloud:

* TiDB Cloud Starter: on-demand capacity mode
* TiDB Cloud Essential: provisioned capacity mode

### Request Unit (RU) and Request Capacity Unit (RCU)

A **Request Unit (RU)** is a unit of measure used to represent the amount of resources consumed by a single request to the database. The amount of RUs consumed by a request depends on various factors, such as the operation type or the amount of data being retrieved or modified.

A **Request Capacity Unit (RCU)** is a unit of measure used to represent the provisioned compute capacity for your TiDB Cloud Essential cluster. One RCU provides a fixed amount of compute resources that can process a certain number of RUs per second. The number of RCUs you provision determines your cluster's baseline performance and throughput capacity.

Currently, the RU will include statistics for the following resources:

| Resource        | RU Consumption                                 |
|-----------------|-------------------------------------------------|
| Read            | 2 storage read batches consume 1 RU             |
|                 | 8 storage read requests consume 1 RU            |
|                 | 64 KiB read request payload consumes 1 RU       |
| Write*          | 2 storage write batch consumes 1 RU             |
|                 | 2 storage write request consumes 1 RU           |
|                 | 1 KiB write request payload consumes 1 RU       |
|                 | 8 KiB write request payload consumes 1 RU (for transactions** >= 16MiB) |
| SQL CPU         | 3 ms consumes 1 RU                              |
| Network Egress  | 1 KiB read consumes 1 RU                        |

### Pricing for TiDB Cloud Starter

See the detailed pricing for each available Alibaba Cloud region below.

| Resource | Singapore | Japan (Tokyo) | Mexico (Querétaro) |
|----------|-----------|-------|--------|
| Compute (per 1M RUs) | $0.24 | $0.28 | $0.22 |
| Row-based storage (per GiB / month) | $0.36 | $0.36 | $0.36 |
| Columnar-based storage (per GiB / month) | $0.09 | $0.09 | $0.09 |

#### Free Quota

We are offering a free quota up to the first 5 clusters created in each Organization. If you need to create more clusters, you will be required to provide a credit card and set a Monthly pending Limit. But if you delete some of your previous clusters before creating the 6th, the new cluster will still have a free quota. In other words, you can enjoy the free quota for up to 5 clusters.

Free Quota will be issued monthly to serverless clusters that meet these qualifications. With the free quota, customers can store 5 GiB of row-based data, 5 GiB of columnar data, and consume 50 million RUs for one month.

In total, each Organization can get 25 GiB of row storage, 25 GiB of column storage, and 250M Request Units (RUs) for free per month. Customers can take advantage of this offer and optimize your operations without worrying about initial costs.

#### Monthly Spending Limit

The "Monthly Spending Limit" refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that enables you to set a budget for your TiDB Starter clusters. The Monthly Spending Limit must be set to a minimum of $0.01.

Note: It is impossible to set a spending limit value lower than the amount already spent for the current month.

#### Throttling

A cluster will not be throttled unless the spending limit is reached. Once the spending limit is reached, the cluster immediately denies any new connection attempts until the quota is increased or the usage is reset at the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling.

If the free quota of a cluster is exhausted within the month, the cluster will automatically be throttled. This limit will remain in place until the customer upgrade it to Scalable cluster or until the next month.

In this way, customers can ensure basic business continuity without paying additional fees. At the same time, customers can adjust the spending limit according to their needs to control their usage and costs.

### Pricing for TiDB Cloud Essential

See the detailed pricing for each available Alibaba Cloud region below.

| Resource | Singapore | Japan (Tokyo) | Mexico (Querétaro) |
|----------|-----------|-------|--------|
| Compute (per RCU / month) | $0.24 | $0.28 | $0.22 |
| Row-based storage (per GiB / month) | $0.36 | $0.36 | $0.36 |
| Columnar-based storage (per GiB / month) | $0.09 | $0.09 | $0.09 |

#### Throttling

For TiDB Cloud Essential clusters, the throttling policy is based on the provisioned Request Capacity Units (RCUs). When the workload exceeds the maximum RCU capacity, the cluster will automatically throttle incoming requests to maintain stability. Existing connections will experience throttling, but new connection attempts will be accepted as long as they don't exceed the maximum RCU limit. This ensures predictable performance while protecting the cluster from overload.

### Billing Cycle

Each TiDB Cloud bill, corresponding to the previous month's usage, is finalized at the start of every new month. This finalized bill is then charged to your default payment method, typically occurring between the 3rd and 9th day of the respective month. If your usage within the current month reaches or exceeds $250, an automatic charge will be initiated. Please note that the billing cycle operates strictly in accordance with the UTC (+00:00) time zone.

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

If you are in the `Organization Owner`
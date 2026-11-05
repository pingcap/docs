---
title: Manage Spending Limit for {{{ .starter }}} Instances
summary: Learn how to manage spending limit for your {{{ .starter }}} instances.
---

# Manage Spending Limit for {{{ .starter }}} Instances

> **Note:**
>
> The spending limit is only applicable to {{{ .starter }}} instances.

Spending limit refers to the maximum amount of money that you are willing to spend on a particular workload in a month. It is a cost-control mechanism that allows you to set a budget for your {{{ .starter }}} instances.

For each organization in TiDB Cloud, you can create a maximum of five [free {{{ .starter }}} instances](/tidb-cloud/select-cluster-tier.md#starter) by default. To create more {{{ .starter }}} instances, you need to add a credit card and set a monthly spending limit for the usage. But if you delete some of your previous {{{ .starter }}} instances before creating more, the new {{{ .starter }}} instance can still be created without a credit card.

## Usage quota

For the first five {{{ .starter }}} instances in your organization, whether they are free or scalable, TiDB Cloud provides a free usage quota for each of them as follows:

- Row-based storage: 5 GiB
- Columnar storage: 5 GiB
- [Request Units (RUs)](/tidb-cloud/tidb-cloud-glossary.md#request-unit-ru): 50 million RUs per month

Once a {{{ .starter }}} instance reaches its usage quota, it immediately denies any new connection attempts until you [increase the quota](#update-spending-limit) or the usage is reset upon the start of a new month. Existing connections established before reaching the quota will remain active but will experience throttling. For example, when the row-based storage of a {{{ .starter }}} instance exceeds 5 GiB for a free {{{ .starter }}} instance, the {{{ .starter }}} instance automatically restricts any new connection attempts.

To learn more about the RU consumption of different resources (including read, write, SQL CPU, and network egress), the pricing details, and the throttled information, see [{{{ .starter }}} Pricing Details](https://www.pingcap.com/tidb-cloud-starter-pricing-details/).

If you want to create a {{{ .starter }}} instance with an additional quota, you can edit the spending limit on the {{{ .starter }}} instance creation page. For more information, see [Create a {{{ .starter }}} instance](/tidb-cloud/create-tidb-cluster-serverless.md).

## Update spending limit

For a free {{{ .starter }}} instance, you can increase the usage quota by setting a monthly spending limit when creating the {{{ .starter }}} instance. For an existing {{{ .starter }}} instance, you can adjust the monthly spending limit directly.

To update the spending limit for a {{{ .starter }}} instance, perform the following steps:

1. On the [**My TiDB**](https://tidbcloud.com/tidbs) page, click the name of your target {{{ .starter }}} instance to go to its overview page.

    > **Tip:**
    >
    > If you are in multiple organizations, use the combo box in the upper-left corner to switch to your target organization first.

2. In the **Capacity used this month** area, click **Set Spending Limit**.

    If you have set the spending limit previously and want to update it, click <svg width="14" height="14" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M11 3.99998H6.8C5.11984 3.99998 4.27976 3.99998 3.63803 4.32696C3.07354 4.61458 2.6146 5.07353 2.32698 5.63801C2 6.27975 2 7.11983 2 8.79998V17.2C2 18.8801 2 19.7202 2.32698 20.362C2.6146 20.9264 3.07354 21.3854 3.63803 21.673C4.27976 22 5.11984 22 6.8 22H15.2C16.8802 22 17.7202 22 18.362 21.673C18.9265 21.3854 19.3854 20.9264 19.673 20.362C20 19.7202 20 18.8801 20 17.2V13M7.99997 16H9.67452C10.1637 16 10.4083 16 10.6385 15.9447C10.8425 15.8957 11.0376 15.8149 11.2166 15.7053C11.4184 15.5816 11.5914 15.4086 11.9373 15.0627L21.5 5.49998C22.3284 4.67156 22.3284 3.32841 21.5 2.49998C20.6716 1.67156 19.3284 1.67155 18.5 2.49998L8.93723 12.0627C8.59133 12.4086 8.41838 12.5816 8.29469 12.7834C8.18504 12.9624 8.10423 13.1574 8.05523 13.3615C7.99997 13.5917 7.99997 13.8363 7.99997 14.3255V16Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg> **Edit**.

3. Edit the monthly spending limit as needed. If you have not added a payment method, you will need to add a credit card after editing the limit.
4. Click **Update Spending Limit**.

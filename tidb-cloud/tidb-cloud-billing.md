---
title: TiDB Cloud Billing
summary: Learn about TiDB Cloud billing.
---

# TiDB Cloud Billing

> **Note:**
>
> [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier) are free to use for up to one year. You will not be charged for the use of your Developer Tier cluster, and your TiDB Cloud bill will not display any Developer Tier charges.

TiDB Cloud charges according to the resources that you consume. You can visit [TiDB Cloud Pricing Details](https://en.pingcap.com/tidb-cloud-pricing-details/) to get more information.

## Invoices

If you are the owner or billing administrator of your organization, you can manage the invoice information of TiDB Cloud. Otherwise, skip this section.

After you set up the payment method, TiDB Cloud will generate an invoice once your cost reaches a quota, which is $500 by default. If you want to raise the quota or receive one invoice per month, you can [contact our sales](https://www.pingcap.com/contact-us/).

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace) or [Google Cloud Marketplace](https://cloud.google.com/marketplace), you can pay through your AWS account or Google Cloud account directly but cannot add payment methods or download invoices in the TiDB Cloud portal.

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

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**. The invoices page is displayed.

## Billing details

If you are the owner or billing administrator of the organization, you can view and export the billing details of TiDB Cloud. Otherwise, skip this section.

After setting the payment method, TiDB Cloud will generate the invoice and billing details of the historical months, and generate the bill details of the current month at the beginning of each month. The billing details include your organization's TiDB cluster usage consumption, discounts, backup storage costs, data transmission costs, support service cost, credit consumption, and project splitting information.

> **Note:**
>
> Due to delays and other reasons, the billing details of the current month are for reference only, not guaranteed to be accurate. TiDB Cloud ensures the accuracy of historical bills so that you can perform cost accounting and meet other needs.

To view the billing details, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click **Bills**. The billing details page is displayed.

The billing details page shows the billing summary by project and by service. You can also see the usage details and download the data in CSV format.

> **Note:**
>
> The total amount in the monthly bill might differ from that in the daily usage details due to differences in precision:
>
> - The total amount in the monthly bill is rounded off to the 2nd decimal place.
> - The total amount in the daily usage details is accurate to the 6th decimal place.

## Credits

TiDB Cloud offers a certain number of credits for Proof of Concept (PoC) users. One credit is equivalent to one U.S. dollar. You can use credits to pay TiDB cluster fees before the credits become expired.

> **Tip:**
>
> To apply for a PoC, see [Perform a Proof of Concept (PoC) with TiDB Cloud](/tidb-cloud/tidb-cloud-poc.md).

The detailed information of your credits is available on the **Credits** page, including your total credits, available credits, current usage, and the status.

To view this page, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
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

## Payment method

If you are the owner or billing administrator of your organization, you can manage the payment information of TiDB Cloud. Otherwise, skip this section.

> **Note:**
>
> If you sign up for TiDB Cloud through [AWS Marketplace](https://aws.amazon.com/marketplace), you can pay through your AWS account directly but cannot add payment methods or download invoices in the TiDB Cloud portal.

### Add a credit card

The fee is deducted from a bound credit card according to your cluster usage. To add a valid credit card, you can use either of the following methods:

- When you are creating a cluster:

    1. Before you click **Create Cluster** on the **Create a Cluster** page, click **Add Credit Card** at the bottom of the **Billing Calculator** pane.
    2. In the **Add a Card** dialog box, fill in the card information and billing address.
    3. Click **Save Card**.

- Anytime in the billing console:

    1. Click the account name in the upper-right corner of the TiDB Cloud console.
    2. Click **Billing**.
    3. Under the **Payment Method** tab, click **Add a New Card**.
    4. Fill in the billing address and card information, and then click **Save**.

> **Note:**
>
> To ensure the security of credit card sensitive data, TiDB Cloud does not save any customer credit card information and saves them in the third-party payment platform Stripe. All billing deductions are completed through Stripe.

You can bind multiple credit cards, and set one of them as the default credit card in the payment method of the billing console. After setting, subsequent billings will be automatically deducted from the default credit card.

To set the default credit card, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click the **Payment Method** tab.
4. Select a credit card in the credit card list, and click **Set as default**.

### Edit billing profile information

The billing profile information includes the business legal address and tax registration information. By providing your tax registration number, certain taxes might be exempted from your invoice.

To edit the billing profile information, perform the following steps:

1. Click the account name in the upper-right corner of the TiDB Cloud console.
2. Click **Billing**.
3. Click the **Payment Method** tab.
4. Edit the billing profile information, and then click **Save**.

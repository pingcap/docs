---
title: TiDB Cloud Support
summary: Learn how to contact the support team of TiDB Cloud.
---

# TiDB Cloud Support

TiDB Cloud offers tiered support plan offerings tailored to meet customers' needs. For more information about our support offerings, see [Connected Care Details](/tidb-cloud/connected-care-detail.md).

## Support channels

TiDB Cloud provides multiple support channels. The available options depend on the type of issue and your [support plan](/tidb-cloud/connected-care-detail.md).

- Support tickets ([Help Center](#access-pingcap-help-center))

    Use this ticket-based channel for issues that require direct assistance from the TiDB Cloud support team.

    - [Billing and account tickets](/tidb-cloud/tidb-cloud-support.md#create-an-account-or-billing-support-ticket) are available to all TiDB Cloud users.
    - [Technical support tickets](/tidb-cloud/tidb-cloud-support.md#create-a-technical-support-ticket) with guaranteed response times are available for paid support plans. If you do not have a paid support plan, use community channels for technical questions.

    The **Enterprise** and **Premium** support plans include the following enhanced capabilities. For more information, see [Connected Care Details](/tidb-cloud/connected-care-detail.md).
 
    - Faster response times with defined SLAs
    - Real-time communication through IM-based support
    - Proactive support programs, such as [Clinic](/tidb-cloud/tidb-cloud-clinic.md)
    - Dedicated or named support roles, such as Technical Account Managers (TAMs)

- Community ([Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) and [Discord](https://discord.com/invite/KVRZBR2DrG))

    Use these open discussion channels to ask questions, share experiences, and get guidance from other users and PingCAP engineers. These channels are suitable for general questions, usage discussions, and non-urgent technical issues.

- [TiDB.AI](https://tidb.ai/)

    TiDB.AI is an AI-powered assistant that answers common technical and documentation-related questions. It is suitable for quick and self-service help.

## Access PingCAP Help Center

The [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals) is the central hub for TiDB Cloud users to access support services and manage support tickets.

You can access the PingCAP Help Center via <https://tidb.support.pingcap.com/servicedesk/customer/portals> directly, or through the [TiDB Cloud console](https://tidbcloud.com/) in the following ways:

- Click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com/), and then click **Request Support**.
- Click **Support** in the lower-left corner of [TiDB Cloud console](https://tidbcloud.com/), and then click **Create Ticket**.
- On the [**Clusters**](https://tidbcloud.com/project/clusters) page of your project, click **...** in the row of your cluster, and then select **Get Support**.
- On your cluster overview page, click **...** in the upper-right corner, and then select **Get Support**.

## Create an account or billing support ticket

All TiDB Cloud users can create billing and account-related tickets. To create a support ticket about account or billing issues, take the following steps:

1. Log in to the [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals), and then click [TiDB Cloud Account/Billing Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/16).
2. Click **Submit a request**.
3. Fill in the following fields:

    - **Summary**: provide a brief summary of your question.
    - **TiDB Cloud Org**: select the relevant TiDB Cloud organization, if applicable.
    - **TiDB Cloud Cluster**: select the relevant TiDB Cloud cluster, if applicable.
    - **Description**: provide the details about the issue.
    - **Severity**: estimate the business impact of the issue and choose the proper severity for it. (S1 is not applicable to billing or account issues.)

4. Click **Submit**.

## Create a technical support ticket

To create a support ticket about technical issues, take the following steps:

1. Log in to the [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals), and then click [TiDB Cloud Technical Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/6).

    > **Note:**
    >
    > The [TiDB Cloud Technical Support](https://tidb.support.pingcap.com/servicedesk/customer/portal/6) entry is only available for **Developer**, **Enterprise**, or **Premium** [support plans](/tidb-cloud/connected-care-detail.md). If you are on the **Basic** plan, you can ask technical questions through the community channels on [Slack](https://slack.tidb.io/invite?team=tidb-community&channel=everyone&ref=pingcap) or [Discord](https://discord.com/invite/KVRZBR2DrG), where PingCAP engineers and community members provide guidance.

2. Click **Submit a request**.

3. Fill in the following fields:

    - **Summary**: provide a brief summary of your question.
    - **TiDB Cloud Org**: select the relevant TiDB Cloud organization for the issue.
    - **TiDB Cloud Cluster**: select the relevant TiDB Cloud cluster, if applicable.
    - **Environment**: select the corresponding environment in which you use the TiDB Cloud cluster.
    - **Description**: describe the issue you encountered as detailed as possible. For example, share the exact timestamp when you encountered the issue, attach the detailed error messages and call stack of the issue, and add your troubleshooting or analysis of the issue.
    - **Severity**: estimate the business impact of the issue and choose the proper severity for it.

        | Severity | Description |
        | --- | --- |
        | S1 | Complete loss of production environmental functionality |
        | S2 | High impact on operations in production environments |
        | S3 | Non-critical database usage issues in production or non-production environments |
        | S4 | General question on how a particular feature or function performs or should be configured. An issue that has minimal impact on business and can be tolerated for a reasonable period. |

    - **Components**: select the relevant TiDB Cloud component to report the issue for, such as TiDB, TiKV, PD, or TiFlash.
    - **Affects versions**: specify the TiDB Cloud cluster version related to the issue.

4. Click **Submit**.

## View support tickets

To view all the historical support tickets, log in to the [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/portals), click your avatar in the upper-right corner, and then click **Requests**.

## Check or upgrade your support plan

TiDB Cloud offers a free basic support plan by default. For extended services, you can upgrade to a paid plan.

To check or upgrade your support plan, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Support** in the lower-left corner.

    On this page, you can find your current plan. By default, the **Basic** free plan is selected.

2. Choose your desired support plan.

    <SimpleTab>
    <div label="Upgrade to Developer or Enterprise">

    To upgrade to **Developer** or **Enterprise**:

    1. Click **Upgrade** in the **Developer** or **Enterprise** pane. An **Upgrade to Developer Plan** or **Upgrade to Enterprise Plan** page is displayed.
    2. Check the corresponding support service information on the page. For a complete version of each support plan, see [Connected Care Details](/tidb-cloud/connected-care-detail.md).
    3. Click **Add Credit Card and Upgrade**, and then fill in the **Credit Card** details.

        For more information about billing, see [TiDB Cloud Payment Method](/tidb-cloud/tidb-cloud-billing.md#payment-method).

    4. Click **Save Card** in the lower-right corner of the page.

    After the payment is finished, you have upgraded your plan to **Standard** or **Enterprise**.

    </div>
    <div label="Upgrade to Premium">

    To upgrade your plan to **Premium**:

    1. Click **Contact Sales** in the **Premium** pane. A **Contact Us** page is displayed.
    2. Fill in and submit your contact information on the page. Then, the support team will contact you and help you with your subscription.

    </div>
    </SimpleTab>

## Downgrade your support plan

To downgrade your support plan, perform the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), click **Support** in the lower-left corner.
2. Choose the support plan you want to switch to, and then click **Downgrade**.

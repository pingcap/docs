---
title: Interact with Support Tickets via Slack
summary: Introduces detailed information about the Slack interaction for support tickets.
---

# Interact with Support Tickets via Slack

For customers subscribed to the **Premium** [support plan](/tidb-cloud/connected-care-detail.md), TiDB Cloud provides a ticket bot called **PingCAP Support Bot** in [Slack](https://slack.com/), to support more comprehensive interaction and management of support tickets.

> **Note:**
>
> The ticket support feature for Slack is available upon request. If you are interested in trying this feature, contact TiDB Cloud support at <a href="mailto:support@pingcap.com">support@pingcap.com</a> or reach out to your Technical Account Manager (TAM).

You can use **PingCAP Support Bot** to create a support ticket in Slack:

![Create a support ticket in Slack](/media/tidb-cloud/connected-slack-ticket-interaction-creation.gif)

You can also reply to the support ticket directly in Slack:

![Reply to a support ticket in Slack](/media/tidb-cloud/connected-slack-ticket-interaction-reply.gif)

## Interact with support tickets

In the Slack support channel, you only need to mention **PingCAP Support Bot** and describe the problem in a message. Then, the bot will send you a message with a **Raise request** button.

![slack-ticket-interaction-1](/media/tidb-cloud/connected-slack-ticket-interaction-1.png)

Click **Raise request** to open a form, fill it out according to the problem, and then click **Create** to submit the ticket.

![slack-ticket-interaction-2](/media/tidb-cloud/connected-slack-ticket-interaction-2.png)

After submission, the bot will send a confirmation message in the thread, which includes the ticket link.

![slack-ticket-interaction-3](/media/tidb-cloud/connected-slack-ticket-interaction-3.png)

For customers subscribed to the **Premium** [support plan](/tidb-cloud/connected-care-detail.md), two-way information synchronization is supported between Slack and the ticket system.

The support engineer's comments on the ticket will be synchronized to the Slack message thread, and users do not need to jump to the support portal to view them. Users can reply directly in this message thread, and these replies will be synchronized to the ticket system.

In this way, customers subscribed to the **Premium** support plan can quickly create, respond, and manage tickets without leaving Slack.

![slack-ticket-interaction-4](/media/tidb-cloud/connected-slack-ticket-interaction-4.png)

## FAQs

- How can I check the status of my ticket?

    Log in to the [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/user/requests) with the email address used to create the ticket. You can view all historical tickets and their status for the current account.

## Contact support

For help or questions, please contact our support team at <a href="mailto:support@pingcap.com">support@pingcap.com</a>. 

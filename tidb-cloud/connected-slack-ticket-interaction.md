---
title: Interact with Support Tickets via Slack
summary: Introduces detailed information about the Slack interaction for support tickets.
---

# Interact with Support Tickets via Slack

For customers subscribed to the **Premium** [support plan](/tidb-cloud/connected-care-detail.md), TiDB Cloud provides a ticket bot called **Assist** in [Slack](https://slack.com/), to support more comprehensive interaction and management of support tickets.

## Interact with support tickets

If an **Assist** app is added to the channel, you can use **Assist** to submit the ticket. There are two ways to submit the request.

- **Method 1: Add a  🎫 emoji to the message for ticket creation**

    Click the emoji icon next to the message that you need to create a ticket. Type `ticket` in the search box to quickly find the 🎫 emoji, and then click 🎫.

    ![slack-ticket-interaction-1](/media/tidb-cloud/connected-slack-ticket-interaction-1.png)

    ![slack-ticket-interaction-2](/media/tidb-cloud/connected-slack-ticket-interaction-2.png)

    The **Assist** app will send you a message with a **Raise Request** button. Then, you can click the button, fill out the form, and submit your request.

    ![slack-ticket-interaction-3](/media/tidb-cloud/connected-slack-ticket-interaction-3.png)

    ![slack-ticket-interaction-4](/media/tidb-cloud/connected-slack-ticket-interaction-4.png)

- **Method 2: Type `/assist` or `/assist` along with the problem description for ticket creation**

    Another faster way is to type `/assist` or `/assist + [problem description]` in the message box and press **Enter**. A request submission form will appear for you to complete and submit.

    ![slack-ticket-interaction-5](/media/tidb-cloud/connected-slack-ticket-interaction-5.png)

After submission, the Assist app will send a confirmation message in the thread, which includes the ticket link and ticket status.

For customers subscribed to the **Premium** [support plan](/tidb-cloud/connected-care-detail.md), two-way information synchronization is supported between Slack and the ticket system.

The support engineer's comments on the ticket will be synchronized to the Slack message thread, and users do not need to jump to the support portal to view them. Users can reply directly in this message thread, and these replies will be synchronized to the ticket system.

In this way, customers subscribed to the **Premium** support plan can quickly create, respond, and manage tickets without leaving Slack.

![slack-ticket-interaction-6](/media/tidb-cloud/connected-slack-ticket-interaction-6.png)

## FAQs

1. How can I check the status of my ticket?

    Log in to the [PingCAP Help Center](https://tidb.support.pingcap.com/servicedesk/customer/user/requests) with the email address used to create the ticket. You can view all historical tickets and their status for the current account.

## Contact support

For help or questions, please contact our support team at <support@pingcap.com>. 

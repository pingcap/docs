---
title: Notifications in the TiDB Cloud Console
summary: Learn about notifications in the TiDB Cloud Console, including notification types, purposes, and how to view them.
---

# Notifications in the TiDB Cloud Console

The [TiDB Cloud console](https://tidbcloud.com/) provides notifications to keep you informed about important updates, system messages, product changes, billing reminders, and other relevant information. These notifications help you stay up-to-date and take necessary actions without leaving the console.

## Notification types

You might receive different types of notifications in the TiDB Cloud console, such as:

- **Informational notifications**

    Provide helpful updates, such as feature usage tips, application changes, or reminders for upcoming events.

- **Actionable notifications**

   Prompt you to perform specific actions, such as adding a credit card.

- **Alert notifications**

    Notify you of critical issues or urgent events requiring immediate attention, such as system errors, security warnings, or important updates.

- **Billing notifications**

    Deliver updates about billing-related activities, such as credit and discount updates.

- **Feedback notifications**

    Request feedback on your experience with a feature, such as rating a recent interaction or completing a survey.

## Notifications list

The following table lists the notifications available in TiDB Cloud, along with their trigger events and recipients:

| Notification | Trigger event | Notification recipient |
| --- | --- | --- |
| TiDB Cloud Serverless cluster creation | A TiDB Cloud Serverless cluster is created. | All project members |
| TiDB Cloud Serverless cluster deletion | A TiDB Cloud Serverless cluster is deleted. | All project members |
| TiDB Cloud Dedicated cluster creation | A TiDB Cloud Dedicated cluster is created. | All project members |
| TiDB Cloud Dedicated cluster deletion | A TiDB Cloud Dedicated cluster is deleted. | All project members |
| Organization Budget threshold alert | The organization [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Project Budget threshold alert | The project [budget threshold](/tidb-cloud/tidb-cloud-budget.md) is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Serverless cluster spending limit threshold alert | The [spending limit threshold](/tidb-cloud/manage-serverless-spend-limit.md) for TiDB Cloud Serverless clusters in the organization is reached. | `Organization Owner`, `Organization Billing Manager`, `Organization Billing Viewer`, and `Project Owner` |
| Credits update | [Credits](/tidb-cloud/tidb-cloud-billing.md#credits) for the organization are applied, fully used, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Discount update | [Discounts](/tidb-cloud/tidb-cloud-billing.md#discounts) for the organization are applied, reclaimed, or expired. | `Organization Owner`, `Organization Billing Manager`, and `Organization Billing Viewer` |
| Marketplace update | The organization has a subscription or unsubscription through a cloud provider marketplace. | All organization members |
| Support plan update | The support plan subscription for the organization is changed. | All organization members |

## View notifications

When a new notification is available, a blue dot is displayed on the <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9.354 21c.705.622 1.632 1 2.646 1s1.94-.378 2.646-1M18 8A6 6 0 1 0 6 8c0 3.09-.78 5.206-1.65 6.605-.735 1.18-1.102 1.771-1.089 1.936.015.182.054.252.2.36.133.099.732.099 1.928.099H18.61c1.196 0 1.795 0 1.927-.098.147-.11.186-.179.2-.361.014-.165-.353-.755-1.088-1.936C18.78 13.206 18 11.09 18 8Z" stroke-width="inherit"></path></svg> icon in the lower-right corner of the TiDB Cloud console. Click <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" stroke-width="2"><path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" d="M9.354 21c.705.622 1.632 1 2.646 1s1.94-.378 2.646-1M18 8A6 6 0 1 0 6 8c0 3.09-.78 5.206-1.65 6.605-.735 1.18-1.102 1.771-1.089 1.936.015.182.054.252.2.36.133.099.732.099 1.928.099H18.61c1.196 0 1.795 0 1.927-.098.147-.11.186-.179.2-.361.014-.165-.353-.755-1.088-1.936C18.78 13.206 18 11.09 18 8Z" stroke-width="inherit"></path></svg> to view the notification.

Alternatively, click <MDSvgIcon name="icon-top-account-settings" /> in the lower-left corner of the TiDB Cloud console, and then click **Notifications** to view a list of all notifications, where you can click a specific notification for more details.

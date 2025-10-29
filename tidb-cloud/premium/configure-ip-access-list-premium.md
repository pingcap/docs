---
title: Configure an IP Access List for {{{ .premium }}}
summary: Learn how to configure IP addresses that are allowed to access your {{{ .premium }}} instance.
---

# Configure an IP Access List for {{{ .premium }}}

For each {{{ .premium }}} instance in TiDB Cloud, you can configure an IP access list to filter internet traffic trying to access the instance, which works similarly to a firewall access control list. After the configuration, only the clients and applications whose IP addresses are in the IP access list can connect to your {{{ .premium }}} instance.

> **Note:**
>
> This document applies to **{{{ .premium }}}**. For instructions on configuring an IP access list for **{{{ .starter }}}** or **{{{ .essential }}}**, see [Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints](/tidb-cloud/configure-serverless-firewall-rules-for-public-endpoints.md).

To configure an IP access list for your {{{ .premium }}} instance, take the following steps:

1. Navigate to the [**TiDB Instances**](https://tidbcloud.com/tidbs) page, and then click the name of your target instance to go to its overview page.

    > **Tip:**
    >
    > You can use the combo box in the upper-left corner to switch between organizations.

2. In the left navigation pane, click **Settings** > **Networking**.
3. On the **Networking** page, click **Enable** for **Public Endpoint** to to make the instance accessible via a public endpoint, and then click **Add IP Address**.
4. In the displayed dialog, choose one of the following options:

    - **Allow access from anywhere**: allows all IP addresses to access TiDB Cloud. This option exposes your instance to the internet completely and is highly risky.
    - **Use IP addresses** (recommended): you can add a list of IPs and CIDR addresses that are allowed to access TiDB Cloud via a SQL client.

5. If you choose **Use IP addresses**, add IP addresses or CIDR ranges with an optional description. 
6. Click **Confirm** to save your changes.

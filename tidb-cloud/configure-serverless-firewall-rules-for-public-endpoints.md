---
title: Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints
summary: Learn how to configure and manage firewall rules with public access to your {{{ .starter }}} or {{{ .essential }}} instance securely.
---

# Configure {{{ .starter }}} or Essential Firewall Rules for Public Endpoints

This document describes the public connectivity option for {{{ .starter }}} and {{{ .essential }}} instances. You will learn key concepts for securely managing a {{{ .starter }}} or Essential instance accessible via the internet.

> **Note:**
>
> This document applies to **{{{ .starter }}}** and **{{{ .essential }}}**. For instructions on configuring an IP access list for **TiDB Cloud Dedicated**, see [Configure an IP Access List for TiDB Cloud Dedicated](/tidb-cloud/configure-ip-access-list.md).

## Public endpoints

Configuring public access on your {{{ .starter }}} or Essential instance allows the instance access through a public endpoint. That is, the {{{ .starter }}} or Essential instance is accessible through the internet. The public endpoint is a publicly resolvable DNS address. The term "authorized network" refers to a range of IP addresses you choose to permit access to your {{{ .starter }}} or Essential instance. These permissions are enforced through **firewall rules**.

### Characteristics of public access

- Only specified IP addresses can access your {{{ .starter }}} or Essential instance.  
    - By default, all IP addresses (`0.0.0.0 - 255.255.255.255`) are allowed.  
    - You can update allowed IP addresses after {{{ .starter }}} or Essential instance creation.  
- Your {{{ .starter }}} or Essential instance has a publicly resolvable DNS name.  
- Network traffic to and from your {{{ .starter }}} or Essential instance is routed over the **public internet** rather than a private network.

### Firewall rules

Granting access to an IP address is done via **firewall rules**. If a connection attempt originates from an unapproved IP address, the client will receive an error.

You can create a maximum of 200 IP firewall rules.

### Allow AWS access

If your {{{ .starter }}} instance is hosted on AWS, you can enable access from **all AWS IP addresses** by referring to the official [AWS IP address list](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html).  

TiDB Cloud regularly updates this list and uses the reserved IP address **169.254.65.87** to represent all AWS IP addresses.

## Create and manage a firewall rule

This section describes how to manage firewall rules for a {{{ .starter }}} or {{{ .essential }}} instance. With a public endpoint, the connections to your instance are restricted to the IP addresses specified in the firewall rules.

To add firewall rules to a {{{ .starter }}} or {{{ .essential }}} instance, take the following steps:

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .starter }}} or Essential instance to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, enable **Public Endpoint** if it is disabled.

4. (Optional) For a newly created {{{ .starter }}} or {{{ .essential }}} instance, TiDB Cloud enables **Allow_all_public_connections** by default. To allow access only from specified IP addresses or IP address ranges, click **...** in the row of **Allow_all_public_connections**, and then click **Delete**.

5. In **Authorized Networks**, click **Add rule**, and then add the IP address or IP address range that you want to allow.

    - To add the current IP address of your computer, click **Add Current IP**. This automatically creates a firewall rule with the public IP address of your computer, as perceived by TiDB Cloud.

        > **Note:**
        >
        > In some situations, the IP address perceived by the TiDB Cloud console might be different from the IP address used by your database client to connect to TiDB Cloud. Therefore, you might need to change the start and end IP addresses to make the rule work as expected. You can use a search engine or an online tool to check your public IP address. For example, search for "what is my IP".

    - To enable access from all AWS IP addresses if your {{{ .starter }}} or Essential instance is hosted on AWS, click **Add AWS Access**. This automatically creates a firewall rule for all AWS IP addresses. TiDB Cloud uses the reserved IP address **169.254.65.87** to represent all AWS IP addresses and regularly updates this list according to the official [AWS IP address list](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html).

    - To add more address ranges, specify a single IP address or a range of IP addresses. To limit the rule to a single IP address, enter the same IP address in the **Start IP Address** and **End IP Address** fields.

        >**Note:**
        >
        > Opening the firewall enables administrators, users, and applications from the specified IP addresses or IP address ranges to access any database on your {{{ .starter }}} or Essential instance to which they have valid credentials.

6. Click **Save**.

## What's next

- [Connect to {{{ .starter }}} or Essential via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)
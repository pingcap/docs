---
title: Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints 
summary: Learn how to configure and manage firewall rules with public access to your TiDB Cloud Serverless cluster securely.
---

# Configure TiDB Cloud Serverless Firewall Rules for Public Endpoints

This document describes the public connectivity option for TiDB Cloud Serverless. You will learn key concepts for securely managing a TiDB Cloud Serverless cluster accessible via the internet.

> **Note:**
>
> This document applies to **TiDB Cloud Serverless**. For instructions on configuring an IP access list for **TiDB Cloud Dedicated**, see [Configure an IP Access List for TiDB Cloud Dedicated](/tidb-cloud/configure-ip-access-list.md).

## Public endpoints

Configuring public access on your TiDB Cloud Serverless cluster allows the cluster access through a public endpoint. That is, the cluster is accessible through the internet. The public endpoint is a publicly resolvable DNS address. The term "authorized network" refers to a range of IP addresses you choose to permit access to your cluster. These permissions are enforced through **firewall rules**.

### Characteristics of public access

- Only specified IP addresses can access TiDB Cloud Serverless.  
    - By default, all IP addresses (`0.0.0.0 - 255.255.255.255`) are allowed.  
    - You can update allowed IP addresses after cluster creation.  
- Your cluster has a publicly resolvable DNS name.  
- Network traffic to and from your cluster is routed over the **public internet** rather than a private network.

### Firewall rules

Granting access to an IP address is done via **firewall rules**. If a connection attempt originates from an unapproved IP address, the client will receive an error.

You can create a maximum of 200 IP firewall rules.

### Allow AWS access

You can enable access from **all AWS IP addresses** by referring to the official [AWS IP address list](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html).  

TiDB Cloud regularly updates this list and uses the reserved IP address **169.254.65.87** to represent all AWS IP addresses.

## Create and manage a firewall rule

This section describes how to manage firewall rules for a TiDB Cloud Serverless cluster. With a public endpoint, the connections to the TiDB Cloud Serverless cluster are restricted to the IP addresses specified in the firewall rules.

To add firewall rules to a TiDB Cloud Serverless cluster, take the following steps:

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. In the left navigation pane, click **Settings** > **Networking**.

3. On the **Networking** page, enable **Public Endpoint** if it is disabled. In **Authorized Networks**, click **+ Add Current IP**. This automatically creates a firewall rule with the public IP address of your computer, as perceived by TiDB Cloud.

    > **Note:**
    >
    > In some situations, the IP address observed by the TiDB Cloud console differs from the IP address used when accessing the internet. Therefore, you might need to change the start and end IP addresses to make the rule function as expected. You can use a search engine or other online tool to check your own IP address. For example, search for "what is my IP."

4. Click **Add rule** to add more address ranges. In the displayed window, you can specify a single IP address or a range of IP addresses. If you want to limit the rule to a single IP address, type the same IP address in the **Start IP Address** and **End IP Address** fields. Opening the firewall enables administrators, users, and applications to access any database on your TiDB Cloud Serverless cluster to which they have valid credentials. Click **Submit** to add the firewall rule.

## What's next

- [Connect to TiDB Cloud Serverless via Public Endpoint](/tidb-cloud/connect-via-standard-connection-serverless.md)
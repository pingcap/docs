---
title: Connect to TiDB Cloud Serverless via Public Endpoint
summary: Learn how to configure and manage public access to your TiDB Cloud Serverless cluster securely.
---

# Connect to TiDB Cloud Serverless via Public Endpoint

This article describes the public connectivity option for TiDB Cloud Serverless. You will learn key concepts for securely managing a TiDB Cloud Serverless cluster accessible via the internet.

> **Note:**
>
> This document applies to **TiDB Cloud Serverless**. For instructions on configuring an IP access list for **TiDB Cloud Dedicated**, see [Configure an IP Access List for TiDB Cloud Dedicated](/tidb-cloud/configure-ip-access-list.md).


## Public Endpoint

Configuring public access on your TiDB Cloud Serverless cluster allows the cluster access through a public endpoint. That is, the cluster is accessible through the internet. The public endpoint is a publicly resolvable DNS address. The phrase authorized networks refers to a range of IPs you choose to permit access to your cluster. These permissions are enforced through **firewall rules**.

### Characteristics of public access

- Only specified IP addresses can access TiDB Cloud Serverless.  
  - **Default:** All IP addresses (`0.0.0.0 - 255.255.255.255`) are allowed.  
  - You can update allowed IP addresses after cluster creation.  
- Your cluster has a publicly resolvable DNS name.  
- Network traffic to and from your cluster is routed over the **public internet** rather than a private network.

### Firewall Rules

Granting access to an IP address is done via **firewall rules**. If a connection attempt originates from an unapproved IP address, the client will receive an error.

You can create a maximum of 200 IP firewall rules.

### Allow AWS access

You can enable access from **all AWS IP addresses** by referring to the official [AWS IP address list](https://docs.aws.amazon.com/vpc/latest/userguide/aws-ip-ranges.html).  
TiDB Cloud regularly updates this list and uses the reserved IP address **169.254.65.87** to represent all AWS IP addresses.

## Create and manage a firewall rule 

This section provides an overview of managing firewall rules after creating a TiDB Cloud Serverless cluster. With Public endpoint, the connections to the TiDB Cloud Serverless cluster are restricted to allowed IP addresses only. The client IP addresses need to be allowed in firewall rules.

1. In the TiDB Cloud console, select the TiDB Cloud Serverless cluster on which you want to add firewall rules.

2. Under **Security** heading, select **Networking** to open Networking page for the TiDB Cloud Serverless cluster.

3. **Enable** Public Endpoint if it's disabled. Select **+ Add Current IP** in the Firewall Rules. This automatically creates a firewall rule with the public IP address of your computer, as perceived by the TiDB Cloud.

> **Note:**
>
> In some situations, the IP address observed by the TiDB Cloud console differs from the IP address used when accessing the internet. Therefore, you might need to change the Start and End IP addresses to make the rule function as expected. You can use a search engine or other online tool to check your own IP address. For example, search for "what is my IP."

4. Add more address ranges by clicking **Add rule** button. In the Add Firewall Rule window, you can specify a single IP address or a range of addresses. If you want to limit the rule to a single IP address, type the same address in the field for the Start IP address and End IP address. Opening the firewall enables administrators, users, and applications to access any database on TiDB Cloud Serverless cluster to which they have valid credentials.

5. To connect your TiDB Cloud Serverless cluster, visit [Connect to Your TiDB Cloud Serverless Cluster](/tidbcloud/connect-to-tidb-cluster-serverless.md) to learn more. 
---
title: Tapdata
---

[Tapdata](https://tapdata.net) is a platform-oriented product designed for data services, aimed at helping enterprises break down multiple data silos, achieve rapid data delivery, and enhance data transfer efficiency through real-time data synchronization. We also support the creation of tasks through a low-code approach, making it easy to create tasks with a simple drag-and-drop of nodes, effectively reducing development complexity and shortening project deployment cycles.

Databend is one of the data sources supported by Tapdata. You can use Tapdata to synchronize data from other platforms to Databend, using Databend as the **destination** for data migration/synchronization.

![Alt text](@site/static/img/documents_cn/getting-started/tapdata-databend.png)

## Integrating with Tapdata Cloud

To establish a connection with Databend Cloud and set it as the synchronization destination in [Tapdata Cloud](https://tapdata.net/tapdata-cloud.html), you need to complete the following steps:

### Step 1: Deploy Tapdata Agent

Tapdata Agent is a key program in data synchronization, data heterogeneity, and data development scenarios. Given the high real-time requirements for data flow in these scenarios, deploying Tapdata Agent in your local environment ensures optimal performance based on low-latency local networks to guarantee real-time data flow.

For Tapdata Agent download and installation instructions, please refer to [Step 1: Provision TapData - Tapdata Cloud](https://docs.tapdata.io/faq/agent-installation).

### Step 2: Create Connections

You need to establish a connection for each of the data source and data destination for data synchronization. For example, if you want to synchronize data from MySQL to Databend Cloud, you need to create two connections on Tapdata Cloud—one connecting to MySQL and the other to Databend Cloud. Follow the steps outlined in [Step 2: Connect Data Sources](https://docs.tapdata.io/connectors/) for creating connections.

Here is an example of connecting to Databend Cloud:

![Alt text](@site/static/img/documents_cn/getting-started/tapdata-connect.png)

### Step 3: Create Data Replication Tasks

Once connections to the data source and Databend Cloud are established, you can begin data synchronization by creating data replication tasks. Refer to [Create a Data Replication Task](https://docs.tapdata.io/data-replication/create-task/) for the operational steps.

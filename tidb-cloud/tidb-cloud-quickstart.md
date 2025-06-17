---
title: TiDB Cloud Quick Start
summary: Sign up quickly to try TiDB Cloud and create your TiDB cluster.
category: quick start
---

# TiDB Cloud Quick Start

*Estimated completion time: 10 minutes*

This tutorial guides you through an easy way to get started with TiDB Cloud. You can also follow the step-by-step tutorials on the [**Getting Started**](https://console.tidb.io/getting-started) page in the TiDB Cloud console.

## Step 1: Create a TiDB cluster

[TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#tidb-cloud-starter) is the best way to get started with TiDB Cloud. To create a TiDB Cloud Starter cluster, follow these steps:

1. If you do not have a TiDB Cloud account, click [here](https://console.tidb.io/free-trial?provider_source=alicloud) to sign up.

    You can sign up with your email and password to manage your password using TiDB Cloud, or choose to sign in with your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

2. [Log in](https://console.tidb.io/signup?provider_source=alicloud) to your TiDB Cloud account.

    The [**Clusters**](https://console.tidb.io/project/clusters) page is displayed by default.

3. For new sign-up users, TiDB Cloud automatically creates a default TiDB Cloud Starter cluster named `Cluster0` for you.
    - To create a new TiDB Cloud Starter cluster on your own, follow these steps:

        1. Click **Create Cluster**.
        2. On the **Create Cluster** page, **Starter** is selected by default. Select the target region for your cluster, update the default cluster name if necessary, select your [cluster plan](/tidb-cloud/select-cluster-tier.md#cluster-plans), and then click **Create**. Your TiDB Cloud Starter cluster will be created in approximately 30 seconds.

## Step 2: Connect to your TiDB cluster

After your TiDB Cloud Starter cluster is created, you can connect to it using different methods depending on your preference:

1. On the cluster overview page, click **Connect** in the upper-right corner.

2. In the displayed dialog, choose a connection option from the **Connect With** drop-down list. Then, follow the tutorials in [Developer Guide](/develop/dev-guide-overview.md) to connect to your cluster.

## What's next

- To learn how to connect to your cluster using different methods, see [Connect to a TiDB Cloud Starter cluster](/tidb-cloud/connect-to-tidb-cluster-serverless.md).
- For TiDB SQL usage, see [Explore SQL with TiDB](/basic-sql-operations.md).
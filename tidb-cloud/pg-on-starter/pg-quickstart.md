---
title: Get Started with PostgreSQL-compatible TiDB Cloud Starter
summary: Learn how to create and connect to a PostgreSQL-compatible TiDB Cloud Starter instance.
category: quick start
---

# TiDB Cloud Quick Start

This tutorial guides you through creating and connecting to a PostgreSQL-compatible TiDB Cloud Starter instance.

Additionally, you can try out TiDB features on [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start).

## Step 1: Create a {{{ .starter }}} instance {#step-1-create-a-starter-instance}

To create a {{{ .starter }}} instance, follow these steps:

1. If you do not have a TiDB Cloud account, click [here](https://tidbcloud.com/free-trial) to sign up.

    You can sign up with your email and password to manage your password using TiDB Cloud, or choose to sign in with your Google, GitHub, or Microsoft account for single sign-on (SSO) to TiDB Cloud.

2. [Log in](https://tidbcloud.com/) to your TiDB Cloud account.

    The [**My TiDB**](https://tidbcloud.com/tidbs) page is displayed by default.

3. To create a new PostgreSQL-compatible {{{ .starter }}} instance, follow these steps:

    1. Click **Create Resource**.
    2. On the **Create Resource** page, select **Starter**.
    3. In the **Compatibility Mode** section, select **PostgreSQL Compatible**.
    4. Enter a name for the {{{ .starter }}} instance, select the cloud provider and target region, and then click **Create**.

    > **Note:**
    >
    > PostgreSQL-compatible {{{ .starter }}} instances are currently free during the Preview.
    >
    > The first 10 PostgreSQL-compatible {{{ .starter }}} instances in your account are eligible for the free quota. Each eligible instance includes the following monthly free quota:
    >
    > + 50 GiB of row-based storage
    > + 500 M Request Units (RUs)
    >
    > When the free quota is exhausted, new connection attempts are rejected. Existing connections remain active but are throttled.

## Step 2: Connect to your {{{ .starter }}} instance

PostgreSQL-compatible {{{ .starter }}} instances support the PostgreSQL wire protocol, so you can connect to them using most PostgreSQL tools, drivers, and ORMs. The following steps use the PostgreSQL CLI client `psql` as an example.

1. Navigate to the [**My TiDB**](https://tidbcloud.com/tidbs) page, and then click the name of your target {{{ .starter }}} instance to go to its overview page.
2. Click **Connect** in the upper-right corner. A connection dialog is displayed with connection parameters.
3. Ensure that the configurations in the connection dialog match your operating environment.
4. Click **Generate Password** to create a random password.
5. In the **Connect With** drop-down list, select **PostgreSQL CLI**.
6. Copy the connection command, paste it into your terminal, and then press **Enter** to run it.

The PostgreSQL CLI client `psql` opens and connects to your {{{ .starter }}} instance.

## What's next
- To learn how to connect to your PostgreSQL-compatible {{{ .starter }}} instance, see [Connect to a {{{ .starter }}} or Essential instance](/tidb-cloud/connect-via-standard-connection-serverless.md).
- To learn about PostgreSQL compatibility, see [PostgreSQL Compatibility](/tidb-cloud/pg-on-starter/postgresql-compatibility.md).
- To learn about the PostgreSQL extensions currently supported by TiDB Cloud, see [PostgreSQL extensions](/tidb-cloud/pg-on-starter/pg-extensions.md).
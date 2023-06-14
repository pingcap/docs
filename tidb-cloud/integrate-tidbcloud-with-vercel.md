---
title: Integrate TiDB Cloud with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

<!-- markdownlint-disable MD029 -->

# Integrate TiDB Cloud with Vercel

[Vercel](https://vercel.com/) is the platform for frontend developers, providing the speed and reliability innovators need to create at the moment of inspiration.

Using TiDB Cloud with Vercel enables you to build new frontend applications faster with a MySQL-compatible relational model and grow your app with confidence with a platform built for resilience, scale, and the highest levels of data privacy and security.

This guide describes how to connect your TiDB Cloud clusters to Vercel projects using one of the following methods:

* [Connect via the TiDB Cloud Vercel integration](#connect-via-the-tidb-cloud-vercel-integration)
* [Connect via manually configuring environment variables](#connect-via-manually-setting-environment-variables)

## Choosing a connection method

TiDB Cloud provides several options for programmatically connecting to your database:

- Direct connection: Connect your TiDB Cloud cluster to your Vercel project directly using MySQL's standard connection system.
- [Data App](/tidb-cloud/data-service-manage-data-app.md): Access data of TiDB Cloud cluster through a group of HTTP endpoints.

## Prerequisites

Before connection, make sure the following prerequisites are met.

### A Vercel account and a Vercel project

You are expected to have an account and a project in Vercel. If you do not have any, refer to the following Vercel documents to create one:

* [Creating a new personal account](https://vercel.com/docs/teams-and-accounts#creating-a-personal-account) or [Creating a new team](https://vercel.com/docs/teams-and-accounts/create-or-join-a-team#creating-a-team).
* [Creating a project](https://vercel.com/docs/concepts/projects/overview#creating-a-project) in Vercel, or if you do not have an application to deploy, you can use the [TiDB Cloud Starter Template](https://vercel.com/templates/next.js/tidb-cloud-starter) to have a try.

One Vercel project can only connect to one TiDB Cloud cluster. To change the integration, you need to first disconnect the current cluster and then connect to a new cluster.

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

To [integrate with Vercel via the TiDB Cloud Vercel Integration](#connect-via-the-tidb-cloud-vercel-integration), you are expected to have the "Owner" access to your organization or the "Member" access to the target project in TiDB Cloud. For more information, see [Manage role access](/tidb-cloud/manage-user-access.md#manage-role-access).

One TiDB Cloud cluster can connect to multiple Vercel projects.

<SimpleTab>
<div label="Direct connection">

### All IP addresses allowed for traffic filter in TiDB Cloud

For TiDB Dedicated clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Vercel deployments use [dynamic IP addresses](https://vercel.com/guides/how-to-allowlist-deployment-ip-address). If you use the TiDB Cloud Vercel integration, TiDB Cloud automatically adds a `0.0.0.0/0` traffic filter to your cluster in the integration workflow if there is none.

TiDB Serverless clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

</div>

<div label="Data App">

### A Data App and endpoints

1. [Create a Data App](/tidb-cloud/data-service-manage-data-app.md#create-a-data-app) on the [**Data Service**](https://tidbcloud.com/console/data-service) page of your project.
2. [Link the Data App](/tidb-cloud/data-service-manage-data-app.md#manage-linked-data-sources) to the target TiDB Cloud cluster.
3. [Manage endpoints](/tidb-cloud/data-service-manage-endpoint.md) that you can customize to execute SQL statements.

</div>
</SimpleTab>

## Connect via the TiDB Cloud Vercel integration

To connect via the TiDB Cloud Vercel integration, go to the [TiDB Cloud integration](https://vercel.com/integrations/tidb-cloud) page from the [Vercel's Integrations Marketplace](https://vercel.com/integrations). Using this method, you can choose which cluster to connect to, and TiDB Cloud will automatically generate all the necessary environment variables for your Vercel projects.

The detailed steps are as follows:

<SimpleTab>
<div label="Direct connection">

1. Click **Add Integration** in the upper-right area of the [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud) page. The **Add TiDB Cloud** dialog is displayed.
2. Select the scope of your integration in the drop-down list and click **CONTINUE**.
3. Select the Vercel Projects to which the integration will be added and click **CONTINUE**.
4. Confirm the required permissions for integration and click **ADD INTEGRATION**. Then you are directed to an integration page of the TiDB Cloud console.
5. Select the target Vercel projects and click **Next**. 
6. Select the target TiDB Cloud Organization and TiDB Cloud Project.
7. Select the Connection Type **Cluster**. 
8. Select the target TiDB Cloud cluster.
9. Select the framework your Vercel projects using. If the framework isn't listed, select **General**. Different frameworks determine different environment variables.
10. Click **Add Integration and Return to Vercel**.
![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-cluster-page.png)
11. Back to your Vercel dashboard, go to your Vercel project, click **Settings** > **Environment Variables**, and confirm that the environment variables have been automatically added.

    If the variables have been added, the connection is completed.

After you have completed the integration setup and successfully connected a TiDB Cloud cluster to your Vercel projects, the information necessary for the connection is automatically set in the projects' environment variables.

**General**

```shell
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

For TiDB Dedicated clusters, the root CA is set in this variable:

```
TIDB_SSL_CA
```

**Prisma**

```
DATABASE_URL
```

</div>

<div label="Data App">

1. Click **Add Integration** in the upper-right area of the [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud) page. The **Add TiDB Cloud** dialog is displayed.
2. Select the scope of your integration in the drop-down list and click **CONTINUE**.
3. Select the Vercel Projects to which the integration will be added and click **CONTINUE**.
4. Confirm the required permissions for integration and click **ADD INTEGRATION**. Then you are directed to an integration page of the TiDB Cloud console.
5. Select the target Vercel projects and click **Next**.
6. Select the target TiDB Cloud Organization and TiDB Cloud Project.
7. Select the Connection Type **Data App**.
8. Select the target TiDB Cloud Data App. 
9. Click **Add Integration and Return to Vercel**.
![Vercel Integration Page](/media/tidb-cloud/vercel/integration-link-data-app-page.png)
10. Back to your Vercel dashboard, go to your Vercel project, click **Settings** > **Environment Variables**, and confirm that the environment variables have been automatically added.

   If the variables have been added, the connection is completed.

After you have completed the integration setup and successfully connected a TiDB Cloud Data App to your Vercel projects, the information necessary for the connection is automatically set in the projects' environment variables.

```shell
DATA_APP_BASE_URL
DATA_APP_PUBLIC_KEY
DATA_APP_PRIVATE_KEY
```

</div>
</SimpleTab>

## Connect via manually setting environment variables

<SimpleTab>
<div label="Direct connection">

1. Follow the steps in [Connect to a TiDB Cloud cluster via standard connection](/tidb-cloud/connect-via-standard-connection.md) to get the connection information of your TiDB cluster.

    > **Note:**
    >
    > For TiDB Dedicated clusters, make sure that you have set the **Allow Access from Anywhere** traffic filter in this step.

2. Go to your Vercel dashboard > Vercel project > **Settings** > **Environment Variables**, and then [declare each environment variable value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) according to the connection information of your TiDB cluster.

  ![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

Here we use a Prisma application as an example. The following is a datasource setting in the Prisma schema file for a TiDB Serverless cluster:

```
datasource db {
    provider = "mysql"
    url      = env("DATABASE_URL")
}
```

In Vercel, you can declare the environment variables as follows.

- **Key** = `DATABASE_URL`
- **Value** = `mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict`

You can get the information of `<User>`, `<Password>`, `<Endpoint>`, `<Port>`, and `<Database>` in the TiDB Cloud console.

</div>
<div label="Data App">

1. Follow the steps in [Manage a Data APP](/tidb-cloud/data-service-manage-data-app.md) to create a data app and endpoints.

2. Go to your Vercel dashboard > Vercel project > **Settings** > **Environment Variables**, and then [declare each environment variable value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) according to the connection information of your Data App.

![Vercel Environment Variables](/media/tidb-cloud/vercel/integration-vercel-environment-variables.png)

In Vercel, you can declare the environment variables as follows.

- **Key** = `DATA_APP_BASE_URL`
- **Value** = `<DATA_APP_BASE_URL>`
- **Key** = `DATA_APP_PUBLIC_KEY`
- **Value** = `<DATA_APP_PUBLIC_KEY>`
- **Key** = `DATA_APP_PRIVATE_KEY`
- **Value** = `<DATA_APP_PRIVATE_KEY>`

You can get the information of `<DATA_APP_BASE_URL>`, `<DATA_APP_PUBLIC_KEY>`, `<DATA_APP_PRIVATE_KEY>` in the TiDB Cloud **Data Service** panel.

</div>
</SimpleTab>


## Configure connections

If you have installed [TiDB Cloud Vercel integration](https://vercel.com/integrations/tidb-cloud), you can add or remove connections inside the integration.

1. In your Vercel dashboard, click **Integrations**.
2. Click **Manage** in the TiDB Cloud entry.
3. Click **Configure**.
4. Click **Add Link** or **Remove** to add or remove connections.

![Vercel Integration Configuration Page](/media/tidb-cloud/vercel/integration-vercel-configuration-page.png)

When you remove a connection, environment variables set by the integration workflow are removed from the Vercel project either. The traffic filter and the data of the TiDB Cloud cluster are not affected.

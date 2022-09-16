---
title: Integrate with Vercel
summary: Learn how to connect your TiDB Cloud clusters to Vercel projects.
---

# Integrate with Vercel

## Introduction

This guide will walk you through connecting your TiDB Cloud clusters to Vercel projects.

It will cover two options:

* Connecting your TiDB Cloud database to your Vercel projects by manually adding environment variables
* Connecting your TiDB Cloud database to your Vercel projects by using the Vercel integration

## Considerations

### Vercel Accounts and Projects 

The integration with Vercel requires that you have an account and a project in Vercel. If you don't have any, refer to

* [Create a new personal account](https://vercel.com/docs/concepts/personal-accounts/overview) or [create a new team](https://vercel.com/docs/concepts/teams/overview) in Vercel.
* [Create a new project](https://vercel.com/docs/concepts/projects/overview) in Vercel.

A Vercel project can only be connected to one TiDB Cloud cluster. To change the integration, you need to first disconnect the current cluster and then connect to a new cluster.

### TiDB Cloud Accounts and Clusters

The integration with Vercel requires that you have an account and a cluster in TiDB Cloud. If you don't have any, refer to [create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md) in TiDB Cloud.

To integrate with Vercel, you must have the `Organization Owner` access to your organization or `Organization Member + Project Access` to the target project in TiDB Cloud.

A TiDB Cloud cluster can connect to more than one Vercel projects.

### TiDB Cloud Cluster Traffic Filter

Vercel deployments use [dynamic IP addresses](https://vercel.com/guides/how-to-allowlist-deployment-ip-address).

To connect to a TiDB Cloud cluster, the traffic filter of your TiDB Cloud cluster must allow all IP addresses (0.0.0.0/0). If TiDB Cloud doesn't find an entry for 0.0.0.0/0 in your cluster's traffic filters, TiDB Cloud adds it on your behalf, as part of the integration workflow.

## Connect via the TiDB Cloud Vercel Integration

You can install the [TiDB Cloud integration](https://vercel.com/integrations/tidb-cloud) from the [Vercel's Integrations Marketplace](https://vercel.com/integrations). You can choose which cluster you want to connect to, and we'll automatically generate all the necessary environment variables into your Vercel projects.

1. Click **Add Integration** button on the [TiDB Cloud integration page](https://vercel.com/integrations/tidb-cloud).
2. Choose the scope of your integration (personal or team).
3. Select Vercel projects to connect to a TiDB Cloud cluster.
4. Confirm the required permissions for integration.
5. On the left side, select the Vercel projects you want to connect to.
6. On the right side, select the TiDB Cloud cluster. Clusters resides under [organizations and projects](/tidb-cloud/manage-user-access.md#view-the-organization-and-project).
7. Click **Add Integration and Return to Vercel** button.
8. Back to your Vercel dashboard, confirm the environment variables were added by going to your Vercel project > **Settings** > **Environment Variables**.

### Environment Variables

After you have completed the integration setup and successfully connected a TiDB Cloud cluster to your Vercel projects, the information necessary to connect the TiDB Cloud cluster are set in the projects' environment variables

```
TIDB_HOST
TIDB_PORT
TIDB_USER
TIDB_PASSWORD
```

For *Dedicated Tier* clusters, the root CA is set in

```
TIDB_SSL_CA
```

## Connect Manually

1. Follow [connect via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to get the connection information. Don't forget to set the *Allow Access from Anywhere* traffic filter and save the password.
2. Go to your Vercel dashboard, [declare each value](https://vercel.com/docs/concepts/projects/environment-variables#declare-an-environment-variable) got from the previous step on your Vercel project > **Settings** > **Environment Variables**.

For example, for a *Dedicated Tier* cluster, you get connection variables like

```
var connection = mysql.createConnection({
  host: '<your_host>',
  port: 4000,
  user: 'root',
  password: '<your_password>',
  database: 'test',
  ssl: {
    ca: fs.readFileSync('ca.pem'),
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true
  }
});
```

In Vercel, you could declare them as follows (you could use whatever name, just suits your projects)

* **NAME** = TIDB\_HOST **VALUE** = <your_host>
* **NAME** = TIDB\_PORT **VALUE** = 4000
* **NAME** = TIDB\_USER **VALUE** = root
* **NAME** = TIDB\_PASSWORD **VALUE** = <your_password>
* **NAME** = TIDB\_SSL\_CA **VALUE** = <content_of_ca.pem>

## Configure Connections

After you install an integration, you can add or remove connections inside the integration.

1. In your Vercel dashboard, click **Integrations**.
2. Click the **Manage** button of TiDB Cloud entry.
3. Click the **Configure** button.
4. Click the **Add Project** button or **Remove** to add or remove connections.

When removing a connection, environment variables set by the integration workflow are removed from the Vercel project. Traffic filter and data of the TiDB Cloud cluster are left untouched.

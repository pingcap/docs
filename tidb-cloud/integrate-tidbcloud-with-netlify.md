---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# Integrate TiDB Cloud with Netlify

[Netlify](https://netlify.com/) is an all-in-one platform for automating modern web projects. It replaces your hosting infrastructure, continuous integration, and deployment pipeline with a single workflow and integrates dynamic functionality like serverless functions, user authentication, and form handling as your projects grow.

This guide describes how to connect your TiDB Cloud clusters to Netlify projects.

## Prerequisites

Before connecting, make sure the following prerequisites are met.

### A Netlify account and a deployed site

You are expected to have an account and a site in Netlify. If you do not have any, refer to the following links to create one:

* [Sign up a new account](https://app.netlify.com/signup).
* [Add a site](https://docs.netlify.com/welcome/add-new-site/) in Netlify. If you do not have an application to deploy, you can use the [TiDB Cloud Starter Template](https://github.com/pingcap/tidb-prisma-vercel-demo#deploy-on-netlify) to have a try.

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

To integrate with Netlify, you are expected to have the "Owner" access to your organization or the "Member" access to the target project in TiDB Cloud. For more information, see [Configure member roles](/tidb-cloud/manage-user-access.md#configure-member-roles).

One TiDB Cloud cluster can connect to multiple Netlify sites.

### All IP addresses allowed for traffic filter in TiDB Cloud

For Dedicated Tier clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Netlify deployments use dynamic IP addresses.

Serverless Tier clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

## Connect via manually setting environment variables

To use this method, make sure that you have set the **Allow Access from Anywhere** traffic filter in the [**Security Settings**](/tidb-cloud/configure-security-settings.md) dialog and save the password.

1. Follow the steps in [Connect to a TiDB Cloud cluster via standard connection](/tidb-cloud/connect-to-tidb-cluster.md#connect-via-standard-connection) to get the connection information of your TiDB cluster.
2. Go to your Netlify dashboard > Netlify project > **Site settings** > **Environment Variables**, and then [Update variables](https://docs.netlify.com/environment-variables/get-started/#update-variables-with-the-netlify-ui) according to the connection information of your TiDB cluster.

The following is an example of the connection variables for a TiDB Cloud Dedicated Tier cluster:

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

In Netlify, you can declare the variables as follows. You can customize the name according to your project need.

* **NAME** = TIDB\_HOST **VALUE** = `<your_host>`
* **NAME** = TIDB\_PORT **VALUE** = 4000
* **NAME** = TIDB\_USER **VALUE** = root
* **NAME** = TIDB\_PASSWORD **VALUE** = `<your_password>`
* **NAME** = TIDB\_SSL\_CA **VALUE** = `<content_of_ca.pem>`

---
title: Metabase
sidebar_position: 4
---

[Metabase](https://www.metabase.com/) is an open-source business intelligence platform. You can use Metabase to ask questions about your data, or embed Metabase in your app to let your customers explore their data on their own.

Databend provides a JDBC driver named [Metabase Databend Driver](https://github.com/databendcloud/metabase-databend-driver/releases/latest), enabling you to connect to Metabase and dashboard your data in Databend / Databend Cloud. For more information about the Metabase Databend Driver, refer to https://github.com/databendcloud/metabase-databend-driver

## Downloading & Installing Metabase Databend Driver

To download and install the Metabase Databend Driver:

1. Create a folder named **plugins** in the directory where the file **metabase.jar** is stored.

```bash
$ ls
metabase.jar
$ mkdir plugins
```

2. [Download](https://github.com/databendcloud/metabase-databend-driver/releases/latest) the Metabase Databend Driver, then save it in the **plugins** folder.

3. To start Metabase, run the following command:

```bash
java -jar metabase.jar
```

## Tutorial: Integrating with Metabase

This tutorial guides you through the process of integrating Databend / Databend Cloud with Metabase using the Metabase Databend Driver.

### Step 1. Set up Environment

To follow along, you'll need to install Metabase with Docker. Before you begin, make sure that Docker is installed on your system.

For this tutorial, you can integrate either with Databend or Databend Cloud:

- If you choose to integrate with a local Databend instance, follow the [Deployment Guide](/guides/self-hosted) to deploy it if you don't have one already.
- If you prefer to integrate with Databend Cloud, make sure you can log in to your account and obtain the connection information for a warehouse. For more details, see [Connecting to a Warehouse](/guides/cloud/resources/warehouses#connecting).

### Step 2. Deploy Metabase

Follow these steps to install and deploy Metabase with Docker:

1. Pull the latest Docker image of Metabase from the Docker Hub registry.

```bash
docker pull metabase/metabase
```

2. Deploy Metabase.

```bash
docker run  -d -p 3000:3000 --name metabase metabase/metabase
```

3. [Download](https://github.com/databendcloud/metabase-databend-driver/releases/latest) the Metabase Databend Driver, then import it to the **plugins** folder of the Metabase container in Docker.

![Alt text](/img/integration/add2plugins.gif)

4. Restart the Metabase container.

### Step 3. Connect to Metabase

1. Open your web browser, and go to http://localhost:3000/.

2. Complete the initial sign-up process. Select **I'll add my data later** in step 3.

![Alt text](/img/integration/add-later.png)

3. Click on the **gear** icon in the top right, and navigate to **Admin settings** > **Databases** > **Add a database** to create a connection:

| Parameter                     | Databend               | Databend Cloud                     |
| ----------------------------- | ---------------------- | ---------------------------------- |
| Database type                 | `Databend`             | `Databend`                         |
| Host                          | `host.docker.internal` | Obtain from connection information |
| Port                          | `8000`                 | `443`                              |
| Username                      | For example, `root`    | `cloudapp`                         |
| Password                      | Enter your password    | Obtain from connection information |
| Use a secure connection (SSL) | Toggle off             | Toggle on                          |

4. Click **Save changes**, then click **Exit admin**.

You're all set! You can now start creating a query and building a dashboard. For more information, please refer to the Metabase documentation: https://www.metabase.com/docs/latest/index.html

![Alt text](/img/integration/allset.png)

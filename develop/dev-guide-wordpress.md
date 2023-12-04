---
title: Connect to TiDB Serverless with Wordpress
summary: Learn how to use TiDB Serverless to run Wordpress. This tutorial gives step-by-step guidance to run Wordpress + TiDB Serverless in a few minutes.
---

# Connect to TiDB Serverless with Wordpress

TiDB is a MySQL-compatible database, and [WordPress](https://github.com/WordPress) is a free, open-source content management system (CMS) that lets users create and manage websites. It's written in PHP and uses a MySQL database.

In this tutorial, you can learn how to use TiDB Serverless run Wordpress for free.

> **Note:**
>
> This tutorial works with TiDB Serverless, TiDB Dedicated, and TiDB Self-Hosted clusters. However, it is highly recommended to run Wordpress with TiDB Serverless for cost-efficiency.

## Prerequisites

To complete this tutorial, you need:

- A TiDB Serverless cluster. Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster if you don't have one.


## Run Wordpress with TiDB Serverless

This section demonstrates how to run Wordpress with TiDB Serverless.

### Step 1: Clone the Wordpress sample reposiroty

Run the following commands in your terminal window to clone the sample code repository:

```shell
git clone https://github.com/pingcap/wordpress-tidb-docker.git
cd wordpress-tidb-docker
```

### Step 2: Install dependencies

1. The sample repository requires [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) to start Wordpress. If you have them installed. You can skip this step. It is highly recommended to run your Wordpress in Linux enviroment (e.g., Ubuntu). Run the following command to install them:

    ```shell
    sudo sh install.sh
    ```

2. The sample repository includes the [TiDB Compatibility Plugin](https://github.com/pingcap/wordpress-tidb-plugin) as a submodule. Run the following command to update the submodule:

    ```shell
    git submodule update --init --recursive
    ```

### Step 3: Configure connection information

Configure the Wordpress database connection to TiDB Serverless. 

1. Navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page, and then click the name of your target cluster to go to its overview page.

2. Click **Connect** in the upper-right corner. A connection dialog is displayed.

3. Ensure the configurations in the connection dialog match your operating environment.

    - **Endpoint Type** is set to `Public`
    - **Connect With** is set to `General`
    - **Operating System** is set to `Debian/Ubuntu/Arch`.

4. Click **Create password** to create a random password.

    > **Tip:**
    > 
    > If you have created a password before, you can either use the original password or click **Reset password** to generate a new one.

5. Run the following command to copy `.env.example` and rename it to `.env`:

    ```shell
    cp .env.example .env
    ```

6. Copy and paste the corresponding connection string into the `.env` file. The example result is as follows:

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    Be sure to replace the placeholders `{}` with the connection parameters obtained from the connection dialog. By default, your TiDB Serverless comes with a `test` DB. You can change the value `TIDB_DB_NAME` to the DB you've created in your TiDB Serverless.

7. Save the `.env` file.


### Step 4: Start Wordpress with TiDB Serverless

1. Execute the following command to run Wordpress as a Docker container:

    ```shell
    docker compose up -d
    ```

2. Setup your Wordpress site by visiting [localhost](http://localhost/) if you start the container on your local machine or **http://<your_instance_ip>** if the Wordpress is running on the remote machine.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](/support.md).

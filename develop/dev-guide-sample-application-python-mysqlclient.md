---
title: Connect TiDB with mysqlclient
summary: Learn how to connect TiDB using mysqlclient. And you can find sample code snippets that works with TiDB with mysqlclient.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Connect TiDB with mysqlclient

TiDB is a MySQL compatible database. And [mysqlclient](https://github.com/PyMySQL/mysqlclient) is a popular open-source driver for Python.

In this tutorial, use TiDB and mysqlclient to complete the following tasks:

- Prepare your environment. 
- Connect to TiDB Serverless, TiDB Dedicated or TiDB Self-hosted using mysqlclient.
- Build and run your app. Optionally, you can find sample code snippets for basic CRUD operations. 

> **Note:**
> This tutorial works with TiDB Serverless, TiDB Dedicated and TiDB Self-Hosted.

## Prerequisites

- [Python **3.10** or higher](https://www.python.org/downloads/).
- [Git](https://git-scm.com/downloads).
- A TiDB cluster. If you don't have a TiDB cluster, you can create one as follows:
    - (Recommended) Follow [Creating a TiDB Serverless Cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
    - Follow [Deploy a Local Test TiDB Cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster.md) or [Deploy a Production TiDB Cluster](/production-deployment-using-tiup.md) to create a local cluster.

## Run sample app to connect to TiDB

This section demonstrates how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample app repository

Run the following command in your terminal window to clone the sample code repository.

```bash
git clone https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart.git
```

### Step 2: Install dependencies (including mysqlclient)

Run the following commands to install required packages for the sample app.

```bash
cd tidb-python-mysqlclient-quickstart;
pip install -r requirements.txt
```

<Tip> If you encounter installation issues, please refer to the [mysqlclient official documentation](https://github.com/PyMySQL/mysqlclient#install). </Tip>

### Step 3: Configure connection information

Connect to your TiDB cluster depending on the TiDB deployment option you've selected.

<SimpleTab>
<div label="TiDB Serverless">

1. In the TiDB Cloud, select your TiDB Serverless cluster. Go to the **Overview** page, and click the **Connect** button in the upper right corner.

2. Ensure the configurations in the confirmation window match your operating environment.

    - **Endpoint Type** is set to **Public**
    - Connect With is set to **General**
    - Operating System matches your environment.

    <Tip>If you are running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.</Tip>

3. Click **Create Password** to create a password.

    <Tip>If you have created a password before, you can either use the original password or click **Reset Password** to generate a new one.</Tip>

4. Run the following command to copy `.env.example` and rename it to `.env`:

    ```bash
    cp .env.example .env
    ```

5. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

    ```python
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH=''
    ```

    Be sure to replace the placeholders `{}` with the values obtained from the **Connect** window.

    TiDB Serverless requires a secure connection. Since the `ssl_mode` of mysqlclient defaults to `PREFERRED`, you don't need to manually specify `CA_PATH`. Just leave it empty. But if you have a special reason to specify `CA_PATH` manually, you can refer to the [TLS Connections to TiDB Serverless](/tidb-cloud/secure-connections-to-serverless-tier-clusters.md) to get the certificate paths for different operating systems.

6. Save the `.env` file.

</div>
<div label="TiDB Dedicated">

1. In the TiDB Cloud, select your TiDB Dedicated cluster. Go to the **Overview** page, and click the **Connect** button in the upper right corner. Click **Allow Access from Anywhere** and then click **Download TiDB cluster CA** to download the certificate.
     <Tip> For more configuration details, refer to [TiDB Dedicated Standard Connection](/tidb-cloud/connect-via-standard-connection.md).</Tip>

2. Run the following command to copy `.env.example` and rename it to `.env`:

    ```bash
    cp .env.example .env
    ```

3. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

    ```python
    TIDB_HOST='{host}.clusters.tidb-cloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{username}'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    CA_PATH='{your-downloaded-ca-path}'
    ```

    Be sure to replace the placeholders `{}` with the values obtained from the **Connect** window, and configure `CA_PATH` with the certificate path downloaded in the previous step.

4. Save the `.env` file.

</div>
<div label="TiDB Self-Hosted">

1. Run the following command to copy `.env.example` and rename it to `.env`:

    ```bash
    cp .env.example .env
    ```

2. Copy and paste the corresponding connection string into the `.env` file. Example result is as follows:

    ```python
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'

    ```

    Be sure to replace the placeholders `{}` with the values, and remove the `CA_PATH` line. If you are running TiDB locally, the default host address is `127.0.0.1`, and the password is empty.

3. Save the `.env` file.

</div>
</SimpleTab>

## Sample Code Snippets

You can refer to the following sample code snippets to complete your own application development.

### Connect to TiDB

```python
def get_mysqlclient_connection(autocommit:bool=True) -> MySQLdb.Connection:
    db_conf = {
        "host": ${tidb_host},
        "port": ${tidb_port},
        "user": ${tidb_user},
        "password": ${tidb_password},
        "database": ${tidb_db_name},
        "autocommit": autocommit
    }

    if ${ca_path}:
        db_conf["ssl_mode"] = "VERIFY_IDENTITY"
        db_conf["ssl"] = {"ca": ${ca_path}}

    return MySQLdb.connect(**db_conf)
```

When using this function, you need to replace `${tidb_host}`, `${tidb_port}`, `${tidb_user}`, `${tidb_password}`, `${tidb_db_name}` and `${ca_path}` with the actual values of your TiDB cluster.

### Insert Data

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player = ("1", 1, 1)
        cursor.execute("INSERT INTO players (id, coins, goods) VALUES (%s, %s, %s)", player)
```

For more information, refer to [Insert Data](/develop/dev-guide-insert-data.md).

### Query Data

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM players")
        print(cur.fetchone()[0])
```

For more information, refer to [Query Data](./dev-guide-get-data-from-single-table.md).

### Update Data

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id, amount, price="1", 10, 500
        cursor.execute("UPDATE players SET goods = goods + %s, coins = coins + %s WHERE id = %s", (-amount, price, player_id))
```

For more information, refer to [Update Data](/develop/dev-guide-update-data.md).

### Delete Data

```python
with get_mysqlclient_connection(autocommit=True) as conn:
    with conn.cursor() as cur:
        player_id = "1"
        cursor.execute("DELETE FROM players WHERE id = %s", (player_id,))
```

For more information, refer to [Update Data](/develop/dev-guide-delete-data.md).

## Useful Notes

- For complete code and how to run it, see the [tidb-python-mysqlclient-quickstart GitHub repository](https://github.com/tidb-samples/tidb-python-mysqlclient-quickstart).
- This Python driver is relatively low-level, so you will see a lot of SQL statements in the sample app. Unlike ORMs, there is no data object, and `mysqlclient` represents query objects with tuples. Although Python's driver is more convenient to use than those in other languages, due to its exposure to underlying implementations and the manual transaction management required, it is still recommended to use ORMs for programming unless there is a significant need for SQL. This can reduce the coupling of your app.
- For more on how to use `mysqlclient`, refer to the [mysqlclient official documentation](https://mysqlclient.readthedocs.io/).

## Next Steps

- You can continue reading the developer documentation to get more knowledge about TiDB development, such as: [Insert Data](/develop/dev-guide-insert-data.md), [Update Data](/develop/dev-guide-update-data.md), [Delete Data](/develop/dev-guide-delete-data.md), [Single Table Reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), [SQL Performance Optimization](/develop/dev-guide-optimize-sql-overview.md), etc.
- If you prefer to learn through courses, we also offer professional [TiDB Developer Courses](https://www.pingcap.com/education/), and provide [TiDB certifications](https://www.pingcap.com/education/certification/) after the exam.
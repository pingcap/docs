---
title: Connect to TiDB by using mysql2 in AWS Lambda Function
summary: This article describes how to connect TiDB using mysql2 in AWS Lambda Function and provides a simple example code snippet.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Connect to TiDB by using mysql2 in AWS Lambda Function

TiDB is a MySQL-compatible database.

[mysql2](https://www.npmjs.com/package/mysql2) is one of the most popular open-source Node.js drivers.

[AWS Lambda Function](https://aws.amazon.com/lambda/) is a serverless computing service provided by AWS.

This document shows you how to use TiDB and mysql2 to build a simple CRUD application.

## Prerequisites

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- TiDB cluster. If you don't have a TiDB cluster, you can create one by following the steps below:
  - (Recommended) Refer to [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster) to create your own TiDB Cloud cluster.
  - Refer to [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a formal TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.
- AWS account. If you don't have an AWS account, you can create one by following the steps below:
  - Refer to [Create an AWS Lambda Function](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) to create an AWS Lambda Function.

## Run the sample application

This section shows you how to run the sample application code and connect to TiDB.

### Step 1: Clone the sample application repository to your local machine

```bash
git clone TODO
```

### Step 2: Install dependencies

```bash
cd TODO
yarn
```

### step 3: Configure the connection string

Depending on the way you deploy TiDB, use different methods to connect to the TiDB cluster.

<SimpleTab>

<div label="TiDB Serverless">

1. In the TiDB Cloud Clusters page, select your TiDB Serverless cluster and go to the **Overview** page. Click **Connect** in the upper right corner.

2. In the pop-up window, confirm that the configuration is consistent with your runtime environment.

   - Endpoint Type is **Public**.
   - Connect With is **General**.
   - Operating System is your runtime environment.

   <Tip>If you are running in Windows Subsystem for Linux (WSL), switch to the corresponding Linux distribution.</Tip>

3. Click **Create Password** to generate a password.

   <Tip>If you have generated a password before, you can use the original password directly, or click **Reset Password** to generate a new password.</Tip>

4. Copy and paste the corresponding connection string to `env.json`. The following is an example:

   ```json
   {
     "Parameters": {
       "TIDB_HOST": "{gateway-region}.aws.tidbcloud.com",
       "TIDB_PORT": "4000",
       "TIDB_USER": "{prefix}.root",
       "TIDB_PASSWORD": "{password}"
     }
   }
   ```

   Replace the placeholders in `{}` with the values obtained in the **Connect** window.

5. [Configure Step.4 environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) in Lambda Function.

</div>

<div label="Self-hosted TiDB">

1. Copy and paste the corresponding connection string. The following is an example:

   ```json
   {
     "Parameters": {
       "TIDB_HOST": "{tidb_server_host}",
       "TIDB_PORT": "4000",
       "TIDB_USER": "root",
       "TIDB_PASSWORD": "{password}"
     }
   }
   ```

   Replace the placeholders in `{}` with the values obtained in the **Connect** window.

2. [Configure Step.1 environment variables](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) in Lambda Function..

</div>

</SimpleTab>

### Step 4: Run the sample application locally

1. Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2.  Run the following command to start the application:

    ```bash
    sam local invoke --env-vars env.json -e event.json "tidbHelloWorldFunction"
    ```

3.  Check the output in the terminal. If the output is similar to the following, the connection is successful:

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

## Key Code Snippets

Complete code snippets are available in the [tidb-example-nodejs](TODO) GitHub repository.

You can refer to the following key code snippets to complete your application development.

### Connect to TiDB

```typescript
import mysql from 'mysql2';

const pool = mysql.createPool({
  host,
  port,
  user,
  password,
  database,
  ssl: {
    minVersion: 'TLSv1.2',
    rejectUnauthorized: true,
  },
  waitForConnections: true,
  connectionLimit: 1,
  maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
  idleTimeout: 60000, // idle connections timeout, in milliseconds, the default value 60000
  queueLimit: 0,
  enableKeepAlive: true,
  keepAliveInitialDelay: 0,
});
```

### Insert data

```typescript
const player = ['1', 10, 500];
await pool.execute(
  `INSERT INTO player (id, goods, coins) VALUES (${player[0]}, ${player[1]}, ${player[2]})`
);
```

Refer to [Insert data](/develop/dev-guide-insert-data.md) for more information.

### Query data

```typescript
const results = await pool.execute('SELECT count(*) FROM player');
console.log(results);
```

Refer to [Query data](/develop/dev-guide-get-data-from-single-table.md) for more information.

### Update data

```typescript
const player = ['1', 10, 500];
await pool.execute(
  `UPDATE player SET goods = goods + ${play[0]}, coins = coins + ${play[1]} WHERE id = ${play[2]}`
);
```

Refer to [Update data](/develop/dev-guide-update-data.md) for more information.

### Delete data

```typescript
await pool.execute('DELETE FROM player WHERE id = 1');
```

Refer to [Delete data](/develop/dev-guide-delete-data.md) for more information.

## Considerations

- Complete code snippets and how to run them, see [tidb-example-nodejs](TODO) GitHub repository.
- The driver is not highly encapsulated, so you will see a lot of SQL statements in the program. Unlike ORM, because there is no data object, the query object of `mysql2` is represented by a object. Although the Node.js driver is convenient, it still requires manual control of the transaction characteristics because it cannot shield the underlying implementation. If there are no scenarios that must use SQL, it is still recommended to use ORM to write programs. This can reduce the coupling of the program.
- For more information about how to use mysql2, see [mysql2 official documentation](https://github.com/sidorares/node-mysql2).
- For more information about how to use AWS Lambda Function with TiDB Cloud, see [Designing High-Performance Applications Using Serverless TiDB Cloud and AWS Lambda](https://aws.amazon.com/blogs/apn/designing-high-performance-applications-using-serverless-tidb-cloud-and-aws-lambda/).

## What's next

- You can continue to read the developer documentation to learn more about TiDB. For example: [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Get data from single table](/develop/dev-guide-get-data-from-single-table.md), [Transaction](/develop/dev-guide-transaction-overview.md), [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md), etc.

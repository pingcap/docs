---
title: Connect to TiDB by using mysql2 in AWS Lambda Function
summary: This article describes how to build a CRUD application using TiDB and mysql2 in AWS Lambda Function and provides a simple example code snippet.
---

# Connect to TiDB by using mysql2 in AWS Lambda Function

TiDB is a MySQL-compatible database, [AWS Lambda Function](https://aws.amazon.com/lambda/) is a compute service, and [mysql2](https://github.com/sidorares/node-mysql2) is a popular open-source driver for Node.js.

In this tutorial, you can learn how to use TiDB and mysql2 in AWS Lambda Function to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql2.
- Build and run your application. Optionally, you can find sample code snippets for basic CRUD operations.

> **Note**
>
> This tutorial works with TiDB Serverless and TiDB Self-Hosted.

## Prerequisites

To complete this tutorial, you need:

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- A running TiDB cluster.
- An [AWS account](https://repost.aws/knowledge-center/create-and-activate-aws-account).
- An AWS user with access to the Lambda function.
- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

<CustomContent platform="tidb">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](/quick-start-with-tidb.md#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

</CustomContent>
<CustomContent platform="tidb-cloud">

**If you don't have a TiDB cluster, you can create one as follows:**

- (Recommended) Follow [Creating a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Follow [Deploy a local test TiDB cluster](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster) or [Deploy a production TiDB cluster](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup) to create a local cluster.

</CustomContent>

If you don't have an AWS account or a user, you can create them by following the steps in the [Getting Started with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) guide.

## Run the sample application

This section demonstrates how to run the sample application code and connect to TiDB.

> **Note**
>
> For complete code snippets and running instructions, refer to the [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub repository.

### Step 1: Clone the sample application repository

Run the following commands in your terminal window to clone the sample code repository:

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### Step 2: Install dependencies

Run the following command to install the required packages (including `mysql2`) for the sample app:

```bash
npm install
```

### Step 3: Configure connection information

The method to connect to the TiDB cluster varies based on your deployment method.

<SimpleTab>

<div label="TiDB Serverless">

1. In the TiDB Cloud [Clusters](https://tidbcloud.com/console/clusters) page, select your TiDB Serverless cluster and go to the **Overview** page. Click **Connect** in the upper right corner.

2. In the connection dialog, select `General` from the **Connect With** dropdown and keep the default setting of the **Endpoint Type** as `Public`.

    > **Note**
    >
    > In Node.js applications, you don't have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

3. If you have not set a password yet, click **Create password** to generate a random password.

    > **Tip**
    >
    > If you have generated a password before, you can use the original password directly, or click **Reset password** to generate a new password.

4. Copy and paste the corresponding connection string into `env.json`. The following is an example:

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

    Replace the placeholders in `{}` with the values obtained in the connection dialog.

5. [Copy and configure the corresponding connection string](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) in Lambda Function.

    ![quickstart-lambda-env](/media/develop/quickstart-lambda-env.png)

</div>

<div label="TiDB Self-Hosted">

1. Copy and paste the corresponding connection string into `env.json`. The following is an example:

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

2. [Copy and configure the corresponding connection string](https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html) in Lambda Function.

  ![quickstart-lambda-env](/media/develop/quickstart-lambda-env.png)

</div>

</SimpleTab>

### Step 4: Run the sample application locally

1. (Prerequisite) Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2. Invoke the sample Lambda function:

    ```bash
    sam local invoke --env-vars env.json -e events/event.json "tidbHelloWorldFunction"
    ```

3. Check the output in the terminal. If the output is similar to the following, the connection is successful:

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

## Sample code snippets

You can refer to the following sample code snippets to complete your own application development.

For complete sample code and how to run it, check out the [tidb-samples/tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) repository.

### Connect to TiDB

```typescript
// lib/tidb.ts
import mysql from 'mysql2';

let pool: mysql.Pool | null = null;

function connect() {
  pool = mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB password
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
    enableKeepAlive: true,
  });
}

export function getConnection(): mysql.Pool {
  if (!pool) {
    connect();
  }
  return pool as mysql.Pool;
}
```

### Insert data

```typescript
const player = ['1', 10, 500];
await pool.execute(
  `INSERT INTO player (id, goods, coins) VALUES (${player[0]}, ${player[1]}, ${player[2]})`
);
```

For more information, refer to [Insert data](/develop/dev-guide-insert-data.md).

### Query data

```typescript
const [rows] = await pool.execute('SELECT count(*) AS cnt FROM player');
console.log(rows[0]['cnt']);
```

For more information, refer to [Query data](/develop/dev-guide-get-data-from-single-table.md).

### Update data

```typescript
const player = ['1', 10, 500];
await pool.execute(
  `UPDATE player SET goods = goods + ${player[0]}, coins = coins + ${player[1]} WHERE id = ${player[2]}`
);
```

For more information, refer to [Update data](/develop/dev-guide-update-data.md).

### Delete data

```typescript
await pool.execute('DELETE FROM player WHERE id = ?', [1]);
```

For more information, refer to [Delete data](/develop/dev-guide-delete-data.md).

## Useful notes

- Using [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) to manage database connections can reduce the performance overhead caused by frequently establishing and destroying connections.
- To avoid SQL injection, it is recommended to use [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements).
- In scenarios where there are not many complex SQL statements involved, using ORM frameworks like [Sequelize](https://sequelize.org/), [TypeORM](https://typeorm.io/), or [Prisma](https://www.prisma.io/) can greatly improve development efficiency. 
- For building a RESTful API for your application, it is recommended to [use AWS Lambda with API Gateway](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html).

## Next steps

- For more details on how to use TiDB in AWS Lambda Function, see our [TiDB-Lambda-integration/aws-lambda-bookstore Demo](https://github.com/pingcap/TiDB-Lambda-integration/blob/main/aws-lambda-bookstore/README.md). You can also use AWS API Gateway to build a RESTful API for your application.
- Learn more usage of `mysql2` from [the documentation of `mysql2`](https://github.com/sidorares/node-mysql2/tree/master/documentation/en).
- Learn more usage of AWS Lambda from [the AWS developer guide of `Lambda`](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).

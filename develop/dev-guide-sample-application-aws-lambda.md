---
title: Build a CRUD Application with TiDB and AWS Lambda Function
summary: This article describes how to connect TiDB using mysql2 in AWS Lambda Function and provides a simple example code snippet.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Build a CRUD Application with TiDB and mysql2 in AWS Lambda Function

This guide demonstrates how to use TiDB, a MySQL-compatible database, and [mysql2](https://www.npmjs.com/package/mysql2), a popular open-source Node.js driver, in an [AWS Lambda Function](https://aws.amazon.com/lambda/) to build a simple CRUD application.

## Prerequisites

Ensure you have the following installed and set up:

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- A running TiDB cluster.
- An [AWS account](https://repost.aws/knowledge-center/create-and-activate-aws-account).
- An AWS user with access to the Lambda function.

If you don't have a TiDB cluster yet, you can create one using one of the following methods:

- (Recommended) Refer to [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Refer to [Deploy a local test TiDB cluster](/quick-start-with-tidb.md) or [Deploy a formal TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

If you don't have an AWS account or a user, you can create them by following the steps in the [Getting Started with Lambda](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html) guide.

## Run the sample application

This section shows you how to run the sample application code and connect to TiDB.

> **Note:**
>
> For complete code snippets and running instructions, refer to the[tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub repository.

### Step 1: Clone the sample application repository

Clone the repository to your local machine:

```bash
git clone git@github.com:tidb-samples/tidb-aws-lambda-quickstart.git
cd tidb-aws-lambda-quickstart
```

### Step 2: Install dependencies

Install the necessary dependencies:

```bash
npm install
```

### Step 3: Configure the connection string

The method to connect to the TiDB cluster varies based on your deployment method.

<SimpleTab>

<div label="TiDB Serverless">

1. In the TiDB Cloud [Clusters](https://tidbcloud.com/console/clusters) page, select your TiDB Serverless cluster and go to the **Overview** page. Click **Connect** in the upper right corner.

2. In the connection dialog, select `General` from the **Connect With** dropdown and keep the default setting of the **Endpoint Type** as `Public`.

    > **Note:**
    >
    > In Node.js applications, you don't have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

3. If you have not set a password yet, click **Create password** to generate a random password.

    <Tip>
    
    If you have generated a password before, you can use the original password directly, or click **Reset password** to generate a new password.
    
    </Tip>

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

1. Install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html).

2. Invoke the sample Lambda function:

    ```bash
    sam local invoke --env-vars env.json -e event.json "tidbHelloWorldFunction"
    ```

3. Check the output in the terminal. If the output is similar to the following, the connection is successful:

    ```bash
    {"statusCode":200,"body":"{\"results\":[{\"Hello World\":\"Hello World\"}]}"}
    ```

## Example code

Complete code snippets are available in the [tidb-aws-lambda-quickstart](https://github.com/tidb-samples/tidb-aws-lambda-quickstart) GitHub repository.

You can refer to the following key code snippets to complete your application development.

### Connect to TiDB

```typescript
import mysql from 'mysql2';

let pool: mysql.Pool;

function connect() {
  pool = mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // TiDB password
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
    enableKeepAlive: true
  });
}

export async function handler(event: any) {
  if (!pool) {
    connect();
  }
  const results = await pool.execute('SELECT "Hello World"');
  return {
    statusCode: 200,
    body: JSON.stringify({ results }),
  };
}
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
const [rows] = await pool.execute('SELECT count(*) AS cnt FROM player');
console.log(rows[0]['cnt']);
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

- It is recommended to use ORM frameworks like [Sequelize](https://sequelize.org/), [Prisma](https://www.prisma.io/), and [TypeORM](https://typeorm.io/) to improve development efficiency in scenarios that do not involve a lot of complex SQL.

## What's next

To deepen your understanding of TiDB, you can explore the developer documentation, which covers various topics such as:

- [Insert data](/develop/dev-guide-insert-data.md)
- [Update data](/develop/dev-guide-update-data.md)
- [Delete data](/develop/dev-guide-delete-data.md)
- [Get data from single table](/develop/dev-guide-get-data-from-single-table.md)
- [Transaction](/develop/dev-guide-transaction-overview.md)
- [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md)

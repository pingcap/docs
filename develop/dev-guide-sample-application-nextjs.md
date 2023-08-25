---
title: Connect to TiDB by using mysql2 in Next.js
summary: This article describes how to build a CRUD application using TiDB and mysql2 in Next.js and provides a simple example code snippet.
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD029 -->

# Connect to TiDB by using mysql2 in Next.js

TiDB is a MySQL-compatible database, and [mysql2](https://github.com/sidorares/node-mysql2) is a popular open-source driver for Node.js.

In this tutorial, you can learn how to use TiDB and mysql2 in Next.js to accomplish the following tasks:

- Set up your environment.
- Connect to your TiDB cluster using mysql2.
- Build and run your application. Optionally, you can find sample code snippets for basic CRUD operations.

> **Note:**
>
> This tutorial works with TiDB Serverless and TiDB Self-Hosted.

## Prerequisites

Ensure you have the following installed:

- [Node.js **18**](https://nodejs.org/en/download/) or later.
- [Git](https://git-scm.com/downloads).
- A running TiDB cluster. 

If you don't have a TiDB cluster yet, you can create one using one of the following methods:

- (Recommended) Refer to [Create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md) to create your own TiDB Cloud cluster.
- Refer to [Deploy a local test TiDB cluster](/quick-start-with-tidb.md) or [Deploy a production TiDB cluster](/production-deployment-using-tiup.md) to create a local cluster.

## Run the sample application

This section illustrates how to run the sample application code and connect to TiDB. 

> **Note:**
>
> For complete code snippets and running instructions, refer to the [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub repository.

### Step 1. Clone the sample application repository

Clone the repository to your local machine:

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### Step 2. Install dependencies

Run the following command to install the required packages (including `mysql2`) for the sample app:

```bash
npm install
```

### Step 3. Configure the connection string

The method to connect to the TiDB cluster varies based on your deployment method.

<SimpleTab>

<div label="TiDB Serverless">

1. In the TiDB Cloud [Clusters page](https://tidbcloud.com/console/clusters), select your TiDB Serverless cluster and go to the **Overview** page. Click **Connect** in the upper right corner.

2. In the connection dialog, select `General` from the **Connect With** dropdown and keep the default setting of the **Endpoint Type** as `Public`.

  > **Note**:
  >
  > In Node.js applications, you do not have to provide an SSL CA certificate, because Node.js uses the built-in [Mozilla CA certificate](https://wiki.mozilla.org/CA/Included_Certificates) by default when establishing the TLS (SSL) connection.

3. If you have not set a password yet, click **Create password** to generate a random password.

   <Tip>
   
   If you have generated a password before, you can use the original password directly, or click **Reset password** to generate a new password.
   
   </Tip>

4. Copy and rename `.env.example` to `.env`:

   ```bash
   # Linux
   cp .env.example .env
   ```

   ```powershell
   # Windows
   Copy-Item ".env.example" -Destination ".env"
   ```

5. Copy and paste the corresponding connection string into `.env`. The following is an example:

   ```bash
   TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
   TIDB_PORT='4000'
   TIDB_USER='{prefix}.root'
   TIDB_PASSWORD='{password}'
   TIDB_DB_NAME='test'
   ```

   Replace the placeholders in `{}` with the values obtained in the **Connect** window.

6. Save the file.

</div>

<div label="TiDB Self-Hosted">

1. Copy and rename `.env.example` to `.env`:

   ```bash
   # Linux
   cp .env.example .env
   ```

   ```powershell
   # Windows
   Copy-Item ".env.example" -Destination ".env"
   ```

2. Copy and paste the corresponding connection string into `.env`. The following is an example:

   ```bash
   TIDB_HOST='{tidb_server_host}'
   TIDB_PORT='4000'
   TIDB_USER='root'
   TIDB_PASSWORD='{password}'
   TIDB_DB_NAME='test'
   ```

   Replace the placeholders in `{}` with the values obtained in the **Connect** window. If you are running TiDB on your local machine, the default Host address is `127.0.0.1` and the password is empty.

3. Save the file.

</div>

</SimpleTab>

### Step 4. Run the sample application locally

1. Start the application:

   ```bash
   npm run dev
   ```

2. Open your browser and visit `http://localhost:3000`. (Check your terminal for the actual port number, and the default is `3000`.)

3. Click the `run SQL` button to execute the sample code.

4. Check the output in the terminal. If the output is similar to the following, the connection is successful:

   ```json
   {
     "results": [
       {
         "Hello World": "Hello World"
       }
     ]
   }
   ```

## Key code snippets

Complete code snippets are available in the [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub repository.

You can refer to the following key code snippets to complete your application development.

### Connect to TiDB

```javascript
import mysql from 'mysql2';

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
```

### Insert data

```javascript
const player = ['1', 1, 1];
await pool.execute(
  `INSERT INTO player (id, goods, coins) VALUES (${player[0]}, ${player[1]}, ${player[2]})`
);
```

Refer to [Insert data](/develop/dev-guide-insert-data.md) for more information.

### Query data

```javascript
const [rows] = await pool.execute('SELECT count(*) AS cnt FROM player');
console.log(rows[0]['cnt']);
```

Refer to [Query data](/develop/dev-guide-get-data-from-single-table.md) for more information.

### Update data

```javascript
const player = ['1', 10, 500];
await pool.execute(
  `UPDATE player SET goods = goods + ${play[0]}, coins = coins + ${play[1]} WHERE id = ${play[2]}`
);
```

Refer to [Update data](/develop/dev-guide-update-data.md) for more information.

### Delete data

```javascript
await pool.execute('DELETE FROM player WHERE id = 1');
```

Refer to [Delete data](/develop/dev-guide-delete-data.md) for more information.

## Useful notes

- Using [connection pools](https://github.com/sidorares/node-mysql2#using-connection-pools) to manage database connections, which can reduce the performance overhead caused by frequently establishing/destroying connections.
- Using [prepared statements](https://github.com/sidorares/node-mysql2#using-prepared-statements) to avoid SQL injection.
- Using ORM frameworks to improve development efficiency in scenarios without a number of complex SQL statements, such as: [Sequelize](https://sequelize.org/), [TypeORM](https://typeorm.io/), and [Prisma](/develop/dev-guide-sample-application-nodejs-prisma.md).

## Next steps

- For more details on how to build a complex application with ORM and Next.js, see [our Bookshop Demo](https://github.com/pingcap/tidb-prisma-vercel-demo).
- Learn more usage of `mysql2` from [the documentation of `mysql2`](https://github.com/sidorares/node-mysql2/tree/master/documentation/en).
- Learn the best practices for TiDB application development with the chapters in the [Developer guide](/develop/dev-guide-overview.md), such as [Insert data](/develop/dev-guide-insert-data.md), [Update data](/develop/dev-guide-update-data.md), [Delete data](/develop/dev-guide-delete-data.md), [Single table reading](/develop/dev-guide-get-data-from-single-table.md), [Transactions](/develop/dev-guide-transaction-overview.md), and [SQL performance optimization](/develop/dev-guide-optimize-sql-overview.md).
- Learn through the professional [TiDB developer courses](https://www.pingcap.com/education/) and earn [TiDB certifications](https://www.pingcap.com/education/certification/) after passing the exam.

## Need help?

Ask questions on the [Discord](https://discord.gg/vYU9h56kAX), or [create a support ticket](https://support.pingcap.com/).

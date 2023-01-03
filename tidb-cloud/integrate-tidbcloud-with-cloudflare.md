---
title: Integrate TiDB Cloud with Cloudflare
summary: Learn how deploy Cloudflare Workers with TiDB Cloud.
---

[Cloudflare Workers](https://workers.cloudflare.com/) is a platform that allows you to run code in response to specific events, such as HTTP requests or changes to a database. Cloudflare Workers is easy to use and can be used to build a variety of applications, including custom APIs, serverless functions, and microservices. It is particularly useful for applications that require low-latency performance or need to scale quickly.

However, you may find it is hard to connect to TiDB Cloud from Cloudflare Workers. Because Cloudflare Workers runs on V8 engine which can not make direct TCP connection

Fortunately, Prisma has your back with the [Data Proxy](https://www.prisma.io/docs/data-platform/data-proxy). It can help us to use Cloudflare Workers to process and manipulate the data being transmitted over a TCP connection.

This article will show how to deploy Cloudflare Workers with TiDB Cloud and Prisma Data Proxy step by step.

> **Note:**
>
> If you want to connect a locally deployed TiDB to Cloudflare Workers, you can try [worker-tidb](https://github.com/shiyuhang0/worker-tidb) which use Cloudflare tunnels as a proxy. But it is not recommended for production use.

# Integrate TiDB Cloud with Cloudflare Workers

## Before you begin

Before you try the steps in this article, you need to prepare the following things: 

- Free TiDB Cloud account and a Serverless Tier on TiDB Cloud, See [TiDB Cloud Quick Start](https://docs.pingcap.com/tidbcloud/tidb-cloud-quickstart#step-1-create-a-tidb-cluster) for more details.
- Free [Cloudflare Workers account](https://dash.cloudflare.com/login)
- Free [Prisma Data Platform account](https://cloud.prisma.io/).
- Free [GitHub account](https://github.com/login)
- Node.js & NPM installed
- Install dependencies with `npm install -D prisma typescript wrangler`

## Step 1: Set up Wrangler

To authenticate Wrangler, run wrangler login:

```
wrangler login
```

Then, you can use the wrangler to create a worker project:

```
wrangler init prisma-tidb-cloudflare
```

In your terminal, you will be asked a series of questions related to your project. Choose the default values for all of them.

## Step 2: Set up Prisma

Enter your project:

```
cd prisma-tidb-cloudflare
```

Then, you can use the prisma init command to set up Prisma:

```
npx prisma init
```

This creates a Prisma schema in prisma/schema.prisma.

Inside prisma/schema.prisma, add the schema according to your table in TiDB. Assume that you have `table1` and `table2` in TiDB, you can add the following schema:

```
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}

model table1 {
  id   Int                   @id @default(autoincrement())
  name String
}

model table2 {
  id   Int                   @id @default(autoincrement())
  name String
}
```

This data model will be used to store incoming requests from your Worker.

## Step 3: Push your project to GitHub

Create a [repository](https://github.com/new) named prisma-tidb-cloudflare on GitHub.

After you create the repository, you can push your project to GitHub:

```
git remote add origin https://github.com/<username>/prisma-tidb-cloudflare 
git add . 
git commit -m "initial commit" 
git push -u origin main
```

## Step 4: Import your Project into the Prisma Data Platform

With Cloudflare Workers, you can't directly access your database because there is no TCP support. Fortunately, You can use Prisma Data Proxy as described above.

1. To get started, sign in the [Prisma Data Platform](https://cloud.prisma.io/).
2. Click **New Project** and then select **Import a Prisma repository**.
3. Fill in the repository and project details, and click **Next**.

   ![img.png](/media/tidb-cloud/cloudflare/cloudflare-project.png)

4. Fill in the **Connection string** with this pattern `mysql://USER:PASSWORD@HOST:PORT/DATABASE?sslaccept=strict`. You can find the connection information in your [TiDB Cloud dashboard](https://tidbcloud.com/console/clusters).
5. Under **Location**, select a Data Proxy location that is geographically close to your TiDB Cloud cluster location.
6. You need not enable **Static IPs** because TiDB Cloud Serverless Tier is accessible from any IP address.

   ![img.png](/media/tidb-cloud/cloudflare/cloudflare-env.png)

7. After you click **Create Project**. You'll be greeted with a new connection string that starts with `prisma://.` You must copy this connection string and save it for later.

   ![img.png](/media/tidb-cloud/cloudflare/cloudflare-connection.png)

## Step 5: Set the Data Proxy Connection string in your environment

Add the Data Proxy connection string to your local environment .env file.

```
prisma://aws-us-east-1.prisma-data.com/?api_key=•••••••••••••••••"
```

Add the Data Proxy connection to Cloudflare Workers with secret

```
wrangler secret put DATABASE_URL
```

Then, enter the Data Proxy connection string.

> Note
> You can also edit the DATABASE_URL via the Cloudflare Workers dashboard.

## Step 6: Generate a Prisma Client

Next, you'll generate a Prisma Client that connects through the [Data Proxy](https://www.prisma.io/docs/data-platform/data-proxy).

```
npx prisma generate --data-proxy 
```

## Step 7: Develop the Cloudflare Worker function

You need to change the `src/index.ts` according to your needs.

For example, if you want to query different table with url variable, you can use the following code:

```
import { PrismaClient } from '@prisma/client/edge'
const prisma = new PrismaClient()

addEventListener('fetch', (event) => {
  event.respondWith(handleEvent(event))
})

async function handleEvent(event: FetchEvent): Promise<Response> {
  // Get URL parameters
  const { request } = event
  const url = new URL(request.url);
  const table = url.searchParams.get('table');
  let limit = url.searchParams.get('limit');
  const limitNumber = limit? parseInt(limit): 100;

  // Get model
  let model
  for (const [key, value] of Object.entries(prisma)) {
    if (typeof value == 'object' && key == table) {
      model = value
      break
    }
  }
  if(!model){
    return new Response("Table not defined")
  }

  // Get data
  const result = await model.findMany({ take: limitNumber })
  return new Response(JSON.stringify({ result }))
}
```

## Step 8: Publish to Cloudflare Workers

You're now ready to deploy to Cloudflare Workers. Run the following command:

```
npx wrangler publish
```

## Step 9: Try your Cloudflare Workers

Go to [cloudflare dashboard](https://dash.cloudflare.com) to find your worker. You can find the URL of your worker in the overview page.

Visit the URL with your table name: `https://your-worker-url/?table={table_name}`, you will get the result from the corresponding TiDB table.

## Step 10: How to update

If you want to change the serverless function. Update `src/index.ts` and publish to Cloudflare Workers again.

If you create a new table and want to query it. You need to:

1. Add new model in `prisma/schema.prisma`.
2. Push the changes to your repository. `git add prisma && git commit -m "add new model" && git push`.
3. Generate the Prisma Client again. `npx prisma generate --data-proxy`.
4. Publish the cloudflare worker again. `npx wrangler publish`.
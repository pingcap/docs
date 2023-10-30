---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Kysely.
---

# TiDB Cloud Serverless Driver Kysely Tutorial

[Kysely](https://www.prisma.io/docs) is a type-safe and autocompletion-friendly TypeScript SQL query builder. TiDB Cloud offers [@tidbcloud/kysely](https://github.com/tidbcloud/kysely) that enables you use Kysely over HTTPS with our [TiDB Cloud serverless driver](./tidb-cloud/serverless-driver.md). Compared with the traditional TCP way, it brings the following benefits:

- Better performance in serverless environment.
- Ability to use Kysely in edge environment.

Learn how to use TiDB Cloud serverless driver with Kysely in this step-by-step tutorial.

## Use TiDB Cloud Kysely dialect in edge environments

### Before you begin

This tutorial use vercel Edge Function as an example. To complete this tutorial, you need the following:

- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- A [Vercel](https://vercel.com/docs) account that provides edge environment.
- The [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.

### Step 1. Create a project

1. Install the vercel CLI:

    ```
    npm i -g vercel@latest
    ```

2. Create a [Next](https://nextjs.org/) project called `kysely-example` with the following terminal commands:

   ```
   npx create-next-app@latest # you need to type the project name `kysely-example`
   cd kysely-example
   ```
   
3. You should also install `kysely` and `@tidbcloud/serverless` with `@tidbcloud/kysely`, as they are both required peer dependencies.

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

### Step 2. Set the environment

On the overview page of your TiDB Cloud Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks something like this:

```
mysql://[username]:[password]@[host]/[database]
```

### Step 3. Create an Edge Function

1. Before you create the edge function. Create a table in your TiDB Serverless with the following DDL:

   ```
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   ```
   
   You can insert some data into the table in order to test the query later. Here is an example

   ```
   insert into test.person values (1,'pingcap','male')
   ```

2. In the app directory, create /api/edge-function-example/route.ts with the following code:

   ```
   import { NextResponse } from 'next/server';
   import type { NextRequest } from 'next/server';
   import { Kysely,GeneratedAlways,Selectable } from 'kysely'
   import { TiDBServerlessDialect } from '@tidbcloud/kysely'
   
   export const runtime = 'edge';
   
   // Types
   interface Database {
     person: PersonTable
   }
   
   interface PersonTable {
     id: GeneratedAlways<number>
     name: string
     gender: "male" | "female" | "other"
   }
   
   // Dialect
   const db = new Kysely<Database>({
     dialect: new TiDBServerlessDialect({
       url: process.env.DATABASE_URL
     }),
   })
   
   // Query
   type Person = Selectable<PersonTable>
   async function findPeople(criteria: Partial<Person> = {}) {
     let query = db.selectFrom('person')
   
     if (criteria.name){
       query = query.where('name', '=', criteria.name)
     }
   
     return await query.selectAll().execute()
   }
   
   export async function GET(request: NextRequest) {
   
     const searchParams = request.nextUrl.searchParams
     const query = searchParams.get('query')
   
     let response = null;
     if (query) {
       response = await findPeople({name: query})
     } else {
       response = await findPeople()
     }
   
     return NextResponse.json(response);
   }
   ```
   
   This code accepts a query parameter `query` and returns the result of the query. If the query parameter is not provided, it returns all the records in the `person` table.

3. Test your code locally

   ```
   export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
   next dev
   ```
   
   Then navigate to http://localhost:3000/api/edge-function-example to see the response from your route.

### Step 4. Deploy your code to Vercel

1. Deploy your code to Vercel with the `DATABASE_URL` environment variable:

   ```
   vercel -e DATABASE_URL=mysql://[username]:[password]@[host]/[database] --prod 
   ```

2. After the deployment is complete, you will get the URL of your project. Navigate to the `${Your-URL}/api/edge-function-example` to see the response from your route.

## Going further

- Learn more about [Kysely](https://www.prisma.io/docs) and [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)
- See how we [integrate with Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)
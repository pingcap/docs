---
title: TiDB Cloud Serverless Driver Kysely Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Kysely.
---

# TiDB Cloud Serverless Driver Kysely Tutorial

[Kysely](https://www.prisma.io/docs) is a type-safe and autocompletion-friendly TypeScript SQL query builder. TiDB Cloud offers [@tidbcloud/kysely](https://github.com/tidbcloud/kysely) that enables you use Kysely over HTTPS with our [TiDB Cloud serverless driver](/tidb-cloud/serverless-driver.md). Compared with the traditional TCP way, it brings the following benefits:

- Better performance in serverless environment.
- Ability to use Kysely in edge environment.

Learn how to use TiDB Cloud serverless driver with Kysely in this step-by-step tutorial.

## Use TiDB Cloud Kysely dialect in Node.js environments

### Before you begin

To complete this tutorial, you need the following:

- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- The [Node.js](https://nodejs.org/en) >= 18.0.0.
- The [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.

### Step 1. Create a project

1. Create a project named `kysely-node-example`:

    ```
    mkdir kysely-node-example
    cd kysely-node-example
    ```

2. Install the `@tidbcloud/kysely` with `kysely` and `@tidbcloud/serverless`, as they are both required peer dependencies:

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

3. In the `package.json` file, specify the ESM module by adding `type: "module"`:

   ```
   {
     "type": "module",
     "dependencies": {
       "@tidbcloud/kysely": "^0.0.4",
       "@tidbcloud/serverless": "^0.0.7",
       "kysely": "^0.26.3",
     }
   }
   ```
   
4. Add a `tsconfig.json` file to the root of your project to define the TypeScript compiler options. Here is an example:

   ```
   {
     "compilerOptions": {
       "module": "ES2022",
       "target": "ES2022",
       "moduleResolution": "node",
       "strict": false,
       "declaration": true,
       "outDir": "dist",
       "removeComments": true,
       "allowJs": true,
       "esModuleInterop": true,
       "resolveJsonModule": true
     }
   }
   ```

### Step 2. Set the environment

1. On the overview page of your TiDB Cloud Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks something like this:

    ```
    mysql://[username]:[password]@[host]/[database]
    ```

2. Set the environment variable `DATABASE_URL` in your local environment. For example, in Linux or macOS, you can run the following command:

    ```  
    export DATABASE_URL=mysql://[username]:[password]@[host]/[database]
    ```
   
### Step 3. Use Kysely to query data

1. Create a table in your TiDB Serverless cluster and insert some data. You can use the [Chat2Query on console](/tidb-cloud/explore-data-with-chat2query.md) to execute the SQL. Here is an example:

   ```
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
   insert into test.person values (1,'pingcap','male')
   ```

2. Create a file named `hello-word.ts` and add the following code:

   ```
   import { Kysely,GeneratedAlways,Selectable } from 'kysely'
   import { TiDBServerlessDialect } from '@tidbcloud/kysely'
   
   // Types
   interface Database {
     person: PersonTable
   }
   
   interface PersonTable {
     id: GeneratedAlways<number>
     name: string
     gender: "male" | "female"
   }
   
   // Dialect
   const db = new Kysely<Database>({
     dialect: new TiDBServerlessDialect({
       url: process.env.DATABASE_URL
     }),
   })
   
   // Simple Querying
   type Person = Selectable<PersonTable>
   export async function findPeople(criteria: Partial<Person> = {}) {
     let query = db.selectFrom('person')
   
     if (criteria.name){
       query = query.where('name', '=', criteria.name)
     }
   
     return await query.selectAll().execute()
   }
   
   console.log(await findPeople())
   ```

### Step 4. Run the Typescript code

1. Install the `ts-node` to transforms TypeScript into JavaScript and `@types/node` to install type definitions for node.

   ```
   npm install -g ts-node
   npm i --save-dev @types/node
   ```
   
2. Run the code with the following command:

   ```
   ts-node --esm hello-world.ts
   ```

## Use TiDB Cloud Kysely dialect in edge environments

### Before you begin

This tutorial use Vercel Edge Function as an example. To complete this tutorial, you need the following:

- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- A [Vercel](https://vercel.com/docs) account that provides edge environment.
- The [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.

### Step 1. Create a project

1. Install the Vercel CLI:

    ```
    npm i -g vercel@latest
    ```

2. Create a [Next](https://nextjs.org/) project called `kysely-example` with the following terminal commands:

   ```
   npx create-next-app@latest kysely-example --ts --no-eslint --tailwind --no-src-dir --app --import-alias "@/*"
   cd kysely-example
   ```
   
3. Install the `@tidbcloud/kysely` with `kysely` and `@tidbcloud/serverless`, as they are both required peer dependencies.

   ```
   npm install kysely @tidbcloud/kysely @tidbcloud/serverless
   ```

### Step 2. Set the environment

On the overview page of your TiDB Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks something like this:

```
mysql://[username]:[password]@[host]/[database]
```

### Step 3. Create an Edge Function

1. Create a table in your TiDB Serverless cluster and insert some data. You can use the [Chat2Query on console](/tidb-cloud/explore-data-with-chat2query.md) to execute the SQL. Here is an example:

   ```
   CREATE TABLE `test`.`person`  (
     `id` int(11) NOT NULL AUTO_INCREMENT,
     `name` varchar(255) NULL DEFAULT NULL,
     `gender` enum('male','female') NULL DEFAULT NULL,
     PRIMARY KEY (`id`) USING BTREE
   );
   
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
   
   Then navigate to `http://localhost:3000/api/edge-function-example` to see the response from your route.

### Step 4. Deploy your code to Vercel

1. Deploy your code to Vercel with the `DATABASE_URL` environment variable:

   ```
   vercel -e DATABASE_URL=mysql://[username]:[password]@[host]/[database] --prod 
   ```

2. After the deployment is complete, you will get the URL of your project. Navigate to the `${Your-URL}/api/edge-function-example` to see the response from your route.

## Going further

- Learn more about [Kysely](https://www.prisma.io/docs) and [@tidbcloud/kysely](https://github.com/tidbcloud/kysely)
- See how we [integrate with Vercel](/tidb-cloud/integrate-tidbcloud-with-vercel.md)
---
title: TiDB Cloud Serverless Driver Prisma Tutorial
summary: Learn how to use TiDB Cloud serverless driver with Prisma ORM.
---

# TiDB Cloud Serverless Driver Prisma Tutorial

[Prisma](https://www.prisma.io/docs) is an open source next-generation ORM (Object-Relational Mapping) that helps developers interact with their database in an intuitive, efficient, and safe way. TiDB Cloud offers [@tidbcloud/prisma-adapter](https://github.com/tidbcloud/prisma-adapter) that enables you use Prisma Client over HTTPS with our [TiDB Cloud serverless driver](./tidb-cloud/serverless-driver.md). Compared with the traditional TCP way, it brings the following benefits:

- Better performance in serverless environment
- [Possibility of using Prisma client in edge environment](https://github.com/prisma/prisma/issues/21394)

Learn how to use TiDB Cloud serverless driver with the Prisma adapter in this step-by-step tutorial.

## Use Prisma adapter on Node.js environment

### Before you begin

To complete this tutorial, you need the following:

- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- The [Node.js](https://nodejs.org/en) >= 18.0.0.
- The [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.

### Step 1. Create a project

1. Create a project named `prisma-example`:

    ```
    mkdir prisma-example
    cd prisma-example
    ```

2. Install the `@tidbcloud/prisma-adapter` driver adapter, the `@tidbcloud/serverless` serverless driver and the Prisma CLI.

   The following command takes installation with npm as an example. Executing this command will create a `node_modules` directory and a `package.json` file in your project directory.

    ```
    npm install @tidbcloud/prisma-adapter
    npm install @tidbcloud/serverless
    npm install prisma --save-dev
    ```
 
3. In the `package.json` file, specify the ESM module by adding `type: "module"`:

   ```
   {
     "type": "module",
     "dependencies": {
       "@prisma/client": "^5.5.2",
       "@tidbcloud/prisma-adapter": "^5.5.2",
       "@tidbcloud/serverless": "^0.0.7"
     },
     "devDependencies": {
       "prisma": "^5.5.2"
     }
   }
   ```


### Step 2. Set the environment

1. On the overview page of your TiDB Cloud Serverless cluster, click **Connect** in the upper-right corner, and then get the connection string for your database from the displayed dialog. The connection string looks something like this:

    ```
    mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict
    ```

2. Create a file named `.env` in your project directory and replace the placeholders with your TiDB Serverless cluster information.

    ```  
    DATABASE_URL="mysql://[username]:[password]@[host]:4000/[database]?sslaccept=strict"
    ```

   > **Note:**
   > The adapter only supports Prisma Client. Prisma migration and introspection still go through the traditional TCP way. The DATABASE_URL can be simplified to `mysql://[username]:[password]@[host]/[database]` format if you only need Prisma Client.

3. Install the `dotenv` to enables you load environment variables from the `.env`

   ```
   npm install dotenv
   ```

### Step 3. Define your schema

1. Create a file named `schema.prisma`. Then reference the environment variable and include the driverAdapters Preview feature in the schema.prisma. Here is an example:

   ```
   // schema.prisma
   generator client {
     provider        = "prisma-client-js"
     previewFeatures = ["driverAdapters"]
   }
   
   datasource db {
     provider     = "mysql"
     url          = env("DATABASE_URL")
   } 
   ```

2. Define your data model in the `schema.prisma` file. Here we take `user` as an example:

   ```
   // schema.prisma
   generator client {
     provider        = "prisma-client-js"
     previewFeatures = ["driverAdapters"]
   }
   
   datasource db {
     provider     = "mysql"
     url          = env("DATABASE_URL")
   } 
   
   // define data model according to your database table
   model user {
     id    Int     @id @default(autoincrement())
     email String? @unique(map: "uniq_email") @db.VarChar(255)
     name  String? @db.VarChar(255)
   }
   ```

3. Sync your database with the Prisma schema. You can create the database tables in TiDB Serverless cluster manually or use the Prisma CLI to create them automatically. Here we take the Prisma CLI as an example:

    ```
    npx prisma db push
    ```
   
    This command will go through the traditional TCP way rather than the adapter to create the tables called `user` in TiDB Serverless cluster automatically. Learn more about [prototype migrate](https://www.prisma.io/docs/concepts/components/prisma-migrate).

4. Generate Prisma Client. The Prisma CLI will generate the Prisma Client based on the schema:

    ```
    npx prisma generate
    ```

### Step 4. Execute CRUD operations

1. Create a file named `hello-word.js` and add the following code to initialize the Prisma Client:

   ```js
   import { connect } from '@tidbcloud/serverless';
   import { PrismaTiDBCloud } from '@tidbcloud/prisma-adapter';
   import { PrismaClient } from '@prisma/client';
   import dotenv from 'dotenv';
   
   // setup
   dotenv.config();
   const connectionString = `${process.env.DATABASE_URL}`;
   
   // init prisma client
   const connection = connect({ url: connectionString });
   const adapter = new PrismaTiDBCloud(connection);
   const prisma = new PrismaClient({ adapter });
   ```

2. Execute CRUD operations with the Prisma Client:

   ```js
   // insert
   const user = await prisma.user.create({
     data: {
       email: 'test@pingcap.com',
       name: 'test',
     },
   })
   console.log(user)
   
   // query
   console.log(await prisma.user.findMany())
   
   // delete
   await prisma.user.delete({
      where: {
         id: user.id,
      },
   })
   ```
   
3. Execute transaction operations with the Prisma Client:

   ```js
   const createUser1 = prisma.user.create({
     data: {
       email: 'test1@pingcap.com',
       name: 'test1',
     },
   })
   const createUser2 = prisma.user.create({
     data: {
       email: 'test1@pingcap.com',
       name: 'test1',
     },
   })
   const createUser3 = prisma.user.create({
     data: {
       email: 'test2@pingcap.com',
       name: 'test2',
     },
   })
   
   try {
     await prisma.$transaction([createUser1, createUser2]) // Operations fail because the email address is duplicated
   } catch (e) {
     console.log(e)
   }
   
   try {
     await prisma.$transaction([createUser2, createUser3]) // Operations success because the email address is unique
   } catch (e) {
     console.log(e)
   }
   ```
   
## Use Prisma adapter on Edge environments

The adapter can not work on edge environment like Vercel and Cloudflare Workers now. But it will be supported in the future, click [here](https://github.com/prisma/prisma/issues/21394) to track the progress.
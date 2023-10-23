---
title: TiDB Cloud Serverless Driver Node.js tutorial
summary: Learn how to use TiDB Cloud Serverless Driver in a local Node.js project.
---

# TiDB Cloud Serverless Driver Node.js tutorial

Learn how to use TiDB Cloud Serverless Driver in a local Node.js project.

> **Note:**
>
> This tutorial is compatible with TiDB Serverless only. Be sure to check out our [Insights into Automotive Sales](https://car-sales-insight.vercel.app/) and [sample repository](https://github.com/tidbcloud/car-sales-insight) to learn how to use it with Cloudflare Workers, Vercel Edge Functions, and Netlify Edge Functions.

## Before you begin

To complete this step-by-step tutorial, you need:

- The [Node.js](https://nodejs.org/en) >= 18.0.0.
- The [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md)

## Create the project

1. Create a project named `node-example`:

    ```
    mkdir node-example
    cd node-example
    ```

2. Run the following command to install the driver with your preferred package manager, here we use npm as an example. This should create a `node_modules` directory and a `package-lock.json` file in your project directory.

    ```
    npm install @tidbcloud/serverless
    ```

## Use the serverless driver

> The serverless driver supports both the CommonJS and ESM module. We use ESM module as an example in this tutorial.

1. First you need to obtain the connection string for your database from the **Connect window** on TiDB Cloud cluster overview page. Your TiDB Serverless connection string will look something like this:

    ```
   mysql://[username]:[password]@[host]/[database]
    ```
   
2. Then add `type: "module"` to your `package.json` to specify ESM module. The `package.json` should look like this:

   ```
   {
     "type": "module",
     "dependencies": {
       "@tidbcloud/serverless": "^0.0.7",
     }
   }
   ```

3. Next, create a file named `index.js` in your project directory and add the following code:

    ```js
    import { connect } from '@tidbcloud/serverless'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Serverless cluster information
    console.log(await conn.execute("show tables"))
    ```

4. Now, run your project with the following command:

    ```
    node index.js
    ```

## Compatability with older Node.js versions

If you are using Node.js < 18.0.0 which doesn't have a global `fetch`, you can:

1. Install the package provides `fetch`, for example the `undici`:

    ```
    npm install undici
    ``` 

2. Pass the `fetch` function to the `connect` function:

    ```js
    import { connect } from '@tidbcloud/serverless'
    import { fetch } from 'undici'
    
    const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]',fetch})
    ```
---
title: Use TiDB Cloud Serverless Driver (Beta) in Node.js
summary: Learn how to use TiDB Cloud Serverless Driver in Node.js.
---

# Use TiDB Cloud Serverless Driver in Node.js

Learn how to use TiDB Cloud Serverless Driver in Node.js.

## Before you begin

To complete this step-by-step tutorial, you need:

- [Node.js](https://nodejs.org/en) >= 18.0.0.
- [NPM](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) or your preferred package manager.
- A TiDB Serverless cluster. If you don't have any, you can [create a TiDB Serverless cluster](/develop/dev-guide-build-cluster-in-cloud.md)

## Build the project

1. Create a project named `node-example`:

    ```
    mkdir node-example
    cd node-example
    ```
   
2. Install the serverless driver, here we use npm. This should create a `node_modules` directory and a `package-lock.json` file in your project directory.

    ```
    npm install @tidbcloud/serverless
    ```

## Use the serverless driver

1. First you need to obtain the connection string for your database from the **Connect window** on TiDB Cloud cluster overview page. Your TiDB Serverless connection string will look something like this:

    ```
   mysql://[username]:[password]@[host]/[database]
    ```
   
2. The serverless driver supports both the CommonJS and ESM module, you can choose the one you prefer.

<SimpleTab>

<div label="CommonJS">

```js
const { connect } = require("@tidbcloud/serverless")

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Serverless cluster information
conn.execute('show tables').then((result) => console.log(result));
```

</div>

<div label="ESM">

```js
import { connect } from '@tidbcloud/serverless'

const conn = connect({url: 'mysql://[username]:[password]@[host]/[database]'}) // replace with your TiDB Serverless cluster information
console.log(await conn.execute("show tables"))
```

</div>

</SimpleTab>

Don't forget to add `type: "module"` to your `package.json` if you are using ESM. The `package.json` should look like this:

```
{
  "type": "module",
  "dependencies": {
    "@tidbcloud/serverless": "^0.0.7",
  }
}
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
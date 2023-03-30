---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# Integrate TiDB Cloud with Netlify

[Netlify](https://netlify.com/) is an all-in-one platform for automating modern web projects. It replaces your hosting infrastructure, continuous integration, and deployment pipeline with a single workflow and integrates dynamic functionality like serverless functions, user authentication, and form handling as your projects grow.

This document describes how to deploy a fullstack app on Netlify with TiDB Cloud as the database backend.

## Prerequisites

Before connecting, make sure the following prerequisites are met.

### A Netlify account and CLI

You are expected to have a Netlify account and CLI. If you do not have any, refer to the following links to create one:

* [Sign up for a Netlify account](https://app.netlify.com/signup).
* [Get Netlify CLI](https://docs.netlify.com/cli/get-started/).

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

One TiDB Cloud cluster can connect to multiple Netlify sites.

### All IP addresses allowed for traffic filter in TiDB Cloud

For Dedicated Tier clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Netlify deployments use dynamic IP addresses.

Serverless Tier clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

## Step 1. Get example projects and set the connection string

To help you get started quickly, TiDB Cloud provides a fullstack example app in TypeScript with Next.js using React and Prisma Client. It is a simple blog site where you can post and delete your own blogs. All the content is stored in TiDB Cloud through Prisma.

### Fork the example and clone it to your own space

1. Fork the [Fullstack Example with Next.js and Prisma](https://github.com/tidbcloud/nextjs-prisma-example) repository to your own GitHub repository.

2. Clone the forked repository to your own space:

    ```shell
    git clone https://github.com/${your_username}/nextjs-prisma-example.git
    cd nextjs-prisma-example/
    ```

### Get the TiDB Cloud connection string

<SimpleTab>
<div label="TiDB Cloud CLI">

> **Note:**
>
> Only Serverless Tier clusters support getting Prisma connection string from TiDB Cloud CLI. If you are using a Dedicated Tier cluster, you can get the connection string from the TiDB Cloud console.

Get the connection string of a cluster in interactive mode:

```shell
ticloud cluster connect-info
```

Then, follow the prompts to select your cluster and system, and select `Prisma` as the client.

```
Choose the cluster
> [x] Cluster0(13796194496)
Choose the client
> [x] Prisma
Choose the operating system
> [x] macOS/Alpine (Detected)
```
The output is as follows, where the connection string for Prisma can be found in the `url` value.

```
datasource db {
  provider = "mysql"
  url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
}
```

> **Note:**
> 
> - Make sure to replace the parameters in the connection string with actual values.
> 
> - This example requires a new database, so you need to replace `<Database>` with a name that does not exist.

For more information about TiDB Cloud CLI, see [TiDB Cloud CLI Reference](./cli-reference.md).

</div>
<div label="TiDB Cloud console">

1. Navigate to the [TiDB Cloud console](https://tidbcloud.com/), and get the following connection parameters from the connection string in the [**Connect**](/tidb-cloud/connect-via-standard-connection.md) dialog.

    - `${host}`
    - `${port}`
    - `${user}`
    - `${password}`
    
2.  Fill the connection parameters in the following connection string:

```
mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
```

> **Note:**
>
> - Make sure to replace the parameters in the connection string with actual values.
> 
> - This example requires a new database, so you need to replace `<Database>` with a name that does not exist.


</div>
</SimpleTab>

## Step 2. Deploy the App to Netlify

1. Authenticate your Netlify account and obtain an access token.

    ```shell
    netlify login
    ```

2. Start the automatic setup. This step will connect your repository for continuous deployment, so Netlify CLI needs access to create a deploy key and a webhook on the repository.

    ```shell
    netlify init
    ```
   
    When you are prompted, choose **Create & configure a new site**, and grant GitHub access. Use the default values for all other options.

    ``` 
    Adding local .netlify folder to .gitignore file...
    ? What would you like to do? +  Create & configure a new site
    ? Team: your_username’s team
    ? Site name (leave blank for a random name; you can change it later):

    Site Created

    Admin URL: https://app.netlify.com/sites/mellow-crepe-e2ca2b
    URL:       https://mellow-crepe-e2ca2b.netlify.app
    Site ID:   b23d1359-1059-49ed-9d08-ed5dba8e83a2

    Linked to mellow-crepe-e2ca2b


    ? Netlify CLI needs access to your GitHub account to configure Webhooks and Deploy Keys. What would you like to do? Authorize with GitHub through app.netlify.com
    Configuring Next.js runtime...

    ? Your build command (hugo build/yarn run build/etc): npm run netlify-build
    ? Directory to deploy (blank for current dir): .next

    Adding deploy key to repository...
    (node:36812) ExperimentalWarning: The Fetch API is an experimental feature. This feature could change at any time
    (Use `node --trace-warnings ...` to show where the warning was created)
    Deploy key added!

    Creating Netlify GitHub Notification Hooks...
    Netlify Notification Hooks configured!

    Success! Netlify CI/CD Configured!

    This site is now configured to automatically deploy from github branches & pull requests

    Next steps:

    git push       Push to your git repository to trigger new site builds
    netlify open   Open the Netlify admin URL of your site
    ```

3. Set environment variables. To connect to your TiDB Cloud cluster from your own space and the Netlify space, you must set the `DATABASE_URL` as the connection string obtained from the previous step.

    ```shell
    # set the environment variable for your own space
    export DATABASE_URL='mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    
    # set the environment variable for the Netlify space
    netlify env:set DATABASE_URL 'mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    ```
   
    Check your environment variables.

    ```shell
    # set on your own space
    env | grep DATABASE_URL
       
    # set on Netlify space 
    netlify env:list
    ```

4. Build the application locally and migrate schema to the TiDB Cloud cluster.

    > **Tips:**
    > 
    > If you want to direct deploy on Netlify instead of your own space, you can skip this step and go to step 6.

    ```shell
    npm install .
    npm run netlify-build
    ```

5. Run the application locally. You can start a local development server to preview your site.

    ```shell
    netlify dev
    ```

    Then, go to `http://localhost:3000/` in your browser to explore its UI.

6. Deploy the site. Once you are satisfied with the preview, you can deploy your site to Netlify using the following command. `--trigger` means deployment without uploading local files. If you make any changes, make sure that you have committed them to your GitHub repository.

    ```shell
    netlify deploy --prod --trigger
    ```
    
    Go to your Netlify console to check the deployment state. After the deployment is done, your site will have a public IP provided by Netlify so that everyone can access it.
---
title: Integrate TiDB Cloud with Netlify
summary: Learn how to connect your TiDB Cloud clusters to Netlify projects.
---

# Integrate TiDB Cloud with Netlify

[Netlify](https://netlify.com/) is an all-in-one platform for automating modern web projects. It replaces your hosting infrastructure, continuous integration, and deployment pipeline with a single workflow and integrates dynamic functionality like serverless functions, user authentication, and form handling as your projects grow.

This guide will tell you how to deploy a fullstack app on Netlify with TiDB Cloud as database backend.

## Prerequisites

Before connecting, make sure the following prerequisites are met.

### A Netlify account and CLI

You are expected to have a Netlify account and CLI. If you do not have any, refer to the following links to create one:

* [Sign up a new account](https://app.netlify.com/signup).
* [Get Netlify CLI](https://docs.netlify.com/cli/get-started/).

### A TiDB Cloud account and a TiDB cluster

You are expected to have an account and a cluster in TiDB Cloud. If you do not have any, refer to [Create a TiDB cluster](/tidb-cloud/create-tidb-cluster.md).

One TiDB Cloud cluster can connect to multiple Netlify sites.

### All IP addresses allowed for traffic filter in TiDB Cloud

For Dedicated Tier clusters, make sure that the traffic filter of the cluster allows all IP addresses (set to `0.0.0.0/0`) for connection, this is because Netlify deployments use dynamic IP addresses.

Serverless Tier clusters allow all IP addresses for connection by default, so you do not need to configure any traffic filter.

## Get example projects and set connection string

We provide a fullstack app in TypeScript with Next.js using React and Prisma Client here. It's a simple blog site where you can post and delete your own blog. All the content is stored in TiDB cloud through prisma.

### Fork example and clone it to your own space

Navigate to [Fullstack Example with Next.js and Prisma](https://github.com/tidbcloud/nextjs-prisma-example), fork it to your own GitHub repository.

Then, use the following command to clone it.

```shell
git clone https://github.com/${your_username}/nextjs-prisma-example.git
cd nextjs-prisma-example/
```

### Get TiDB Cloud database connection string

<SimpleTab>
<div label="TiDB Cloud CLI">

> **Note:**
>
> Only **Serverless Tier** can get Prisma connection string from TiDB Cloud CLI. If your database is Dedicated Tier, please use TiDB Cloud console to get.
>

```shell
ticloud cluster connect-info
```

Then, follow the prompts to select your cluster and system and select Prisma as client.

```
Choose the cluster
> [x] Cluster0(13796194496)
Choose the client
> [x] Prisma
Choose the operating system
> [x] macOS/Alpine (Detected)

datasource db {
  provider = "mysql"
  url      = "mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict"
}
```

> **Note:**
> 
> Don't forget to replace the parameters in the connection string.
> 
> This example must create a new database, so replace `<Database>` with a name that doesn't exist.

The output is the connection string for Prisma connecting to TiDB Cloud.

For more information about TiDB Cloud CLI, see [TiDB Cloud CLI Reference](./cli-reference.md).

</div>
<div label="TiDB Cloud console">

Navigate to [TiDB Cloud console](https://tidbcloud.com/). Get the following connection parameters `${host}`, `${port}`, `${user}` and `${password}` from the connection string in the [**Connect**](/tidb-cloud/connect-via-standard-connection.md) dialog and fill them into the following connection string.

```
mysql://<User>:<Password>@<Host>:<Port>/<Database>?sslaccept=strict
```

> **Note:**
>
> Don't forget to replace the parameters in the connection string.
>
> This example must create a new database, so replace `<Database>` with a name that doesn't exist.


</div>
</SimpleTab>

## Deploy App to Netlify

1. Authenticate your Netlify account and obtain an access token.

    ```shell
    netlify login
    ```

2. Automated setup. This will connect your repository for continuous deployment, Netlify CLI will need access to create a deploy key and a webhook on the repository.

    ```shell
    netlify init
    ```
   
    Please choose **Create & configure a new site**, and grant GitHub access. Use the default values for all other options.

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

3. Set environment variables. You must set the `DATABASE_URL`, a connection string, obtained from previous step to connect to your TiDB Cloud cluster on both your own space and Netlify space.

    ```shell
    # set on your own space
    export DATABASE_URL='mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    
    # set on Netlify space   
    netlify env:set DATABASE_URL 'mysql://<User>:<Password>@<Endpoint>:<Port>/<Database>?sslaccept=strict'
    ```
   
    Check your environment variables.

    ```shell
    # set on your own space
    env | grep DATABASE_URL
       
    # set on Netlify space 
    netlify env:list
    ```

4. Build application locally and migrate schema to TiDB Cloud cluster.

    > **Tips:**
    > 
    > If you want to direct deploy on Netlify instead of own space, you can skip to step 6: Deploy site.

    ```shell
    npm install .
    npm run netlify-build
    ```

5. Run application locally. You can start a local development server to preview your site.

    ```shell
    netlify dev
    ```

    Then, navigate to http://localhost:3000/ in your browser to explore its UI.

6. Deploy site. Once you're satisfied with the preview, you can deploy your site to Netlify using the following command.`--trigger` means deploy without uploading local files. If you make any changes, don't forget to commit them to your GitHub repository first.

    ```shell
    netlify deploy --prod --trigger
    ```
    
    Go to your Netlify console to check deploying statement. After deploying done, your site will have a public ip provided by Netlify so that everyone can access it.

## Conclusion

This article describes how to deploy a next.js project in Netlify and connect to TiDB Cloud as a data storage service.

There are two point keys: One is to build the connection string to TiDB Cloud, which usually depends on the database driver used in the project. The second is to set the connection string in the Netlify environment variable. If you're using TiDB Serverless, you can easily use the [TiDB Cloud CLI](./ticloud-cluster-connect-info.md) to get the connection strings for the most common drivers.
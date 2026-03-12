---
title: Deepnote
sidebar_position: 5
---

[Deepnote](https://deepnote.com) allows you to easily work on your data science projects, together in real-time and in one place with your friends and colleagues; helping you turn your ideas and analyses into products faster. Deepnote is built for the browser so you can use it across any platform (Windows, Mac, Linux or Chromebook). No downloads required, with updates shipped to you daily. All changes are instantly saved.

Both Databend and Databend Cloud support integration with Deepnote, requiring a secure connection. When integrating with Databend, please note that the default port is `8124`.

## Tutorial: Integrating with Deepnote

This tutorial guides you through the process of integrating Databend Cloud with Deepnote.

### Step 1. Set up Environment

Make sure you can log in to your Databend Cloud account and obtain the connection information for a warehouse. For more details, see [Connecting to a Warehouse](/guides/cloud/resources/warehouses#connecting).

### Step 2. Connect to Databend Cloud

1. Sign in to Deepnote, or create an account if you don't have one.

2. Click **+** to the right of **INTEGRATIONS** in the left sidebar, then select **ClickHouse**.

![Alt text](/img/integration/11.png)

3. Complete the fields with your connection information.

| Parameter        | Description                        |
| ---------------- | ---------------------------------- |
| Integration name | For example, `Databend`            |
| Host name        | Obtain from connection information |
| Port             | `443`                              |
| Username         | `cloudapp`                         |
| Password         | Obtain from connection information |

4. Create a notebook.

5. In the notebook, navigate to the **SQL** section, and then choose the connection you previously created.

![Alt text](/img/integration/13.png)

You're all set! Refer to the Deepnote documentation for how to work with the tool.

![Alt text](/img/integration/15.png)

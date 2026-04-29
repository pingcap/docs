---
title: Deepnote
summary: Deepnote allows you to easily work on your data science projects, together in real-time and in one place with your friends and colleagues; helping you turn your ideas and analyses into products faster. Deepnote is built for the browser so you can use it across any platform (Windows, Mac, Linux or Chromebook). No downloads required, with updates shipped to you daily. All changes are instantly saved.
---

# Deepnote

[Deepnote](https://deepnote.com) allows you to easily work on your data science projects, together in real-time and in one place with your friends and colleagues; helping you turn your ideas and analyses into products faster. Deepnote is built for the browser so you can use it across any platform (Windows, Mac, Linux or Chromebook). No downloads required, with updates shipped to you daily. All changes are instantly saved.

Both {{{ .lake }}} and {{{ .lake }}} support integration with Deepnote, requiring a secure connection. When integrating with {{{ .lake }}}, please note that the default port is `8124`.

## Tutorial: Integrating with Deepnote

This tutorial guides you through the process of integrating {{{ .lake }}} with Deepnote.

### Step 1. Set up Environment

Make sure you can log in to your {{{ .lake }}} account and obtain the connection information for a warehouse. For more details, see [Connecting to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

### Step 2. Connect to {{{ .lake }}}

1. Sign in to Deepnote, or create an account if you don't have one.

2. Click **+** to the right of **INTEGRATIONS** in the left sidebar, then select **ClickHouse**.

    ![Integration with ClickHouse](/media/tidb-cloud-lake/integration-clickhouse.png)

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

You're all set! Refer to the Deepnote documentation for how to work with the tool.

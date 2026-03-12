---
title: Grafana
sidebar_position: 1
---

[Grafana](https://grafana.com/) is a monitoring dashboard system, which is an open-source monitoring tool developed by Grafana Labs. It can greatly simplify the complexity of monitoring by allowing us to provide the data to be monitored, and it generates various visualizations. Additionally, it has an alarm function that sends notifications when there is an issue with the system.

Databend Cloud and Databend can integrate with Grafana in two ways:

- **Loki Protocol (Recommended for Databend Cloud)**: Use Grafana's built-in Loki data source to connect to Databend Cloud via Loki-compatible API endpoints.
- **Custom Plugin**: Use the [Grafana Databend Data Source Plugin](https://github.com/databendlabs/grafana-databend-datasource) for direct SQL access.

## Using Loki Protocol (Recommended)

Databend Cloud provides a Loki-compatible API that allows you to use Grafana's native Loki data source without installing additional plugins. This is the recommended approach for most use cases.

:::note
The Loki protocol feature requires activation. Please contact support to enable this feature for your account.
:::

### Step 1. Configure Table

Before connecting to Grafana, configure your Databend Cloud table for log data visualization. Below are two recommended schema types:

#### Loki Schema

This schema stores labels as a VARIANT/MAP alongside the log body:

```sql
CREATE TABLE logs (
  `timestamp` TIMESTAMP NOT NULL,
  `labels` VARIANT NOT NULL,
  `line` STRING NOT NULL,
  `stream_hash` UInt64 NOT NULL AS (city64withseed(labels, 0)) STORED
) CLUSTER BY (to_start_of_hour(timestamp), stream_hash);

CREATE INVERTED INDEX logs_line_idx ON logs(line);
REFRESH INVERTED INDEX logs_line_idx ON logs;
```

- `timestamp`: log event timestamp
- `labels`: VARIANT storing serialized Loki labels
- `line`: raw log line
- `stream_hash`: computed hash for clustering

#### Flat Schema

This schema uses a wide table where each attribute is a separate column:

```sql
CREATE TABLE nginx_logs (
  `agent` STRING,
  `client` STRING,
  `host` STRING,
  `path` STRING,
  `request` STRING,
  `status` INT,
  `timestamp` TIMESTAMP NOT NULL
) CLUSTER BY (to_start_of_hour(timestamp), host, status);

CREATE INVERTED INDEX nginx_request_idx ON nginx_logs(request);
REFRESH INVERTED INDEX nginx_request_idx ON nginx_logs;
```

Every column except the timestamp and line column becomes a LogQL label.

![Configure Table](/img/connect/grafana-configure-table.png)

### Step 2. Get Connection Information

1. Log in to your Databend Cloud account.

2. On the dashboard, click **Connect** to view the connection information. Note down:
   - **Host**: The warehouse endpoint (e.g., `tnxxxxxxx.gw.aws-us-east-2.default.databend.com`)
   - **User**: Your username (typically `cloudapp`)
   - **Password**: Your password or API key
   - **Database**: The database name containing your log table
   - **Warehouse**: The warehouse name

![Get Connection Info](/img/connect/grafana-get-connect-info.png)

For detailed information on obtaining connection details, see [Connecting to a Warehouse](/guides/cloud/resources/warehouses#connecting).

### Step 3. Configure Grafana Data Source

1. In Grafana, navigate to **Connections** > **Data sources** > **Add data source**.

2. Search for and select **Loki**.

3. Configure the basic settings:
   - **Name**: Give your data source a descriptive name (e.g., "Databend Cloud Logs")
   - **URL**: Enter `https://<host>` using the host from Step 2

![Configure Loki Data Source - Basic](/img/connect/grafana-configure-loki-datasource-basic.png)

4. Configure authentication:
   - Enable **Basic auth** under the Authentication section
   - **User**: Enter your username (typically `cloudapp`)
   - **Password**: Enter your password or API key

5. Add custom HTTP headers. Under **Custom HTTP Headers**, add the following:
   - **Header**: `X-Databend-Warehouse`, **Value**: Your warehouse name
   - **Header**: `X-Databend-Database`, **Value**: Your database name
   - **Header**: `X-Databend-Table`, **Value**: Your table name

![Configure Loki Data Source - Headers](/img/connect/grafana-configure-loki-datasource-header.png)

6. Click **Save & test** to verify the connection.

![Configure Loki Data Source - Complete](/img/connect/grafana-configure-loki-datasource-complete.png)

### Step 4. Test Queries

1. Navigate to **Explore** in Grafana.

2. Select your Databend Cloud Loki data source.

3. Use LogQL queries to visualize your data. For example:
   - `{service="api"}` - Filter logs by service label
   - `{level="error"}` - Show only error-level logs
   - `{service="api"} |= "timeout"` - Search for specific text in logs
   - `count_over_time({status="500"}[5m])` - Count errors over time

4. Customize the visualization as needed using Grafana's panel options.

![Test Loki Query with Explore](/img/connect/grafana-test-loki-query-with-explore.png)

## Using Custom Plugin (Alternative)

For advanced use cases requiring direct SQL access or when working with self-hosted Databend, you can use the Grafana Databend Data Source Plugin.

### Step 1. Set up Environment

Before you start, ensure you have:

- Grafana installed. Refer to the official installation guide: [https://grafana.com/docs/grafana/latest/setup-grafana/installation](https://grafana.com/docs/grafana/latest/setup-grafana/installation)
- Either:
  - A local Databend instance (follow the [Deployment Guide](/guides/self-hosted) to deploy)
  - Or Databend Cloud access with connection information for a warehouse (see [Connecting to a Warehouse](/guides/cloud/resources/warehouses#connecting))

### Step 2. Modify Grafana Configuration

Add the following lines to your `grafana.ini` file:

```ini
[plugins]
allow_loading_unsigned_plugins = databend-datasource
```

### Step 3. Install the Grafana Databend Data Source Plugin

1. Find the latest release on [GitHub Release](https://github.com/databendlabs/grafana-databend-datasource/releases).

2. Get the download URL for the plugin zip package, for example, `https://github.com/databendlabs/grafana-databend-datasource/releases/download/v1.0.2/databend-datasource-1.0.2.zip`.

3. Get the Grafana plugins folder and unzip the downloaded zip package into it:

```shell
curl -fLo /tmp/grafana-databend-datasource.zip https://github.com/databendlabs/grafana-databend-datasource/releases/download/v1.0.2/databend-datasource-1.0.2.zip
unzip /tmp/grafana-databend-datasource.zip -d /var/lib/grafana/plugins
rm /tmp/grafana-databend-datasource.zip
```

4. Restart Grafana to load the plugin.

5. Navigate to the **Plugins** page in the Grafana UI, for example, `http://localhost:3000/plugins`, and ensure the plugin is installed.

![Plugins](/img/integration/grafana-plugins.png)
![Plugin detail](/img/integration/grafana-plugin-detail.png)

### Step 4. Configure Data Source

1. Go to the `Add new connection` page, for example, `http://localhost:3000/connections/add-new-connection?search=databend`, search for `databend`, and select it.

2. Click **Add new data source** on the top right corner of the page.

3. Input the `DSN` field for your Databend instance. For example:
   - Self-hosted: `databend://root:@localhost:8000?sslmode=disable`
   - Databend Cloud: `databend://cloudapp:******@tnxxxxxxx.gw.aws-us-east-2.default.databend.com:443/default?warehouse=xsmall-fsta`

4. Optionally, input the `SQL User Password` field to override the password in the `DSN` field.

5. Click **Save & test**. If the page displays "Data source is working", the data source has been successfully created.

### Step 5. Test Queries

1. Create a new dashboard and add a panel.

2. Select your Databend data source.

3. Write SQL queries to retrieve and visualize your data.

4. Configure the panel visualization options as needed.

---
title: Connect to Databend
---

Databend supports multiple connection methods to suit different use cases. All options below work with both **Databend Cloud** and **self-hosted Databend**.

## Quick Selection

| I want to... | Recommended | Link |
|-------------|-------------|------|
| Run SQL queries interactively | **BendSQL** (CLI) or **DBeaver** (GUI) | [SQL Clients](/guides/connect/sql-clients) |
| Build an application | Language-specific **Driver** | [Drivers](/guides/connect/drivers) |
| Create dashboards & reports | **BI/Visualization Tools** | [Visualization](/guides/connect/visualization) |

## Connection Strings

| Deployment | Format |
|------------|--------|
| **Databend Cloud** | `databend://<user>:<pass>@<tenant>.gw.<region>.default.databend.com:443/<db>?warehouse=<name>` |
| **Self-Hosted** | `databend://<user>:<pass>@<host>:<port>/<db>` |

:::tip Getting Your Connection String
- **Databend Cloud**: Log in → Click **Connect** → Copy the generated DSN
- **Self-Hosted**: Use your server address with the configured user credentials
:::

## SQL Clients

| Tool | Type | Best For |
|------|------|----------|
| [BendSQL](/guides/connect/sql-clients/bendsql) | CLI | Developers, Scripting, Automation |
| [DBeaver](/guides/connect/sql-clients/jdbc) | GUI | Data Analysis, Visual Query Building |

## Drivers

| Language | Guide | Use Case |
|----------|-------|----------|
| Go | [Golang Driver](/guides/connect/drivers/golang) | Backend services, microservices |
| Python | [Python Connector](/guides/connect/drivers/python) | Data science, analytics, ML |
| Node.js | [Node.js Driver](/guides/connect/drivers/nodejs) | Web applications |
| Java | [JDBC Driver](/guides/connect/drivers/java) | Enterprise applications |
| Rust | [Rust Driver](/guides/connect/drivers/rust) | System programming |

## Visualization Tools

| Tool | Type |
|------|------|
| [Grafana](/guides/connect/visualization/grafana) | Monitoring & Dashboards |
| [Tableau](/guides/connect/visualization/tableau) | Business Intelligence |
| [Superset](/guides/connect/visualization/superset) | Data Exploration |
| [Metabase](/guides/connect/visualization/metabase) | Self-Service BI |
| [Jupyter](/guides/connect/visualization/jupyter) | Data Science Notebooks |
| [Deepnote](/guides/connect/visualization/deepnote) | Collaborative Notebooks |
| [MindsDB](/guides/connect/visualization/mindsdb) | ML Platform |
| [Redash](/guides/connect/visualization/redash) | SQL-Based Dashboards |


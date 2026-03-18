---
title: Connect to TiDB Cloud Lake
summary: TiDB Cloud Lake supports multiple connection methods to suit different use cases. All options below work with both **TiDB Cloud Lake** and **self-hosted Databend**.
---
Databend supports multiple connection methods to suit different use cases. All options below work with both **Databend Cloud** and **self-hosted Databend**.

## Quick Selection

| I want to... | Recommended |
|-------------|-------------|
| Run SQL queries interactively | **BendSQL** (CLI) or **DBeaver** (GUI) |
| Build an application | Language-specific **Driver** |
| Create dashboards & reports | **BI/Visualization Tools** |

## Connection Strings

| Deployment | Format |
|------------|--------|
| **Databend Cloud** | `databend://<user>:<pass>@<tenant>.gw.<region>.default.databend.com:443/<db>?warehouse=<name>` |
| **Self-Hosted** | `databend://<user>:<pass>@<host>:<port>/<db>` |

> **Tip:**
>
> - **Databend Cloud**: Log in → Click **Connect** → Copy the generated DSN
> - **Self-Hosted**: Use your server address with the configured user credentials

## SQL Clients

| Tool | Type | Best For |
|------|------|----------|
| [BendSQL](/tidb-cloud-lake/guides/connect-using-bendsql.md) | CLI | Developers, Scripting, Automation |
| [DBeaver](/tidb-cloud-lake/guides/connect-using-dbeaver.md) | GUI | Data Analysis, Visual Query Building |

## Drivers

| Language | Guide | Use Case |
|----------|-------|----------|
| Go | [Golang Driver](/tidb-cloud-lake/guides/connect-using-golang.md) | Backend services, microservices |
| Python | [Python Connector](/tidb-cloud-lake/guides/connect-using-python.md) | Data science, analytics, ML |
| Node.js | [Node.js Driver](/tidb-cloud-lake/guides/connect-using-node-js.md) | Web applications |
| Java | [JDBC Driver](/tidb-cloud-lake/guides/connect-using-java.md) | Enterprise applications |
| Rust | [Rust Driver](/tidb-cloud-lake/guides/connect-using-rust.md) | System programming |

## Visualization Tools

| Tool | Type |
|------|------|
| [Grafana](/tidb-cloud-lake/guides/grafana.md) | Monitoring & Dashboards |
| [Tableau](/tidb-cloud-lake/guides/tableau.md) | Business Intelligence |
| [Superset](/tidb-cloud-lake/guides/superset.md) | Data Exploration |
| [Metabase](/tidb-cloud-lake/guides/metabase.md) | Self-Service BI |
| [Jupyter](/tidb-cloud-lake/guides/jupyter-notebook.md) | Data Science Notebooks |
| [Deepnote](/tidb-cloud-lake/guides/deepnote.md) | Collaborative Notebooks |
| [MindsDB](/tidb-cloud-lake/guides/mindsdb.md) | ML Platform |
| [Redash](/tidb-cloud-lake/guides/redash.md) | SQL-Based Dashboards |


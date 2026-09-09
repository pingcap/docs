---
title: Connect to TiDB Cloud Lake with Jupyter Notebook
summary: Learn how to connect Jupyter Notebook to TiDB Cloud Lake with SQLAlchemy, run queries, and visualize query results with pandas.
---

# Connect to TiDB Cloud Lake with Jupyter Notebook

[Jupyter Notebook](https://jupyter.org/) is an interactive environment for running code, querying data, and creating visualizations. You can connect a notebook to {{{ .lake }}} through the [TiDB Cloud Lake dialect for SQLAlchemy](https://github.com/tidbcloud/lake-sqlalchemy).

## Prerequisites

Before you begin, make sure that you have the following:

- Python 3.8 or later
- A {{{ .lake }}} account, database, and warehouse
- The host, username, password, database, and warehouse name for your connection

For information about obtaining connection information, see [Connect to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

## Install Jupyter Notebook and the SQLAlchemy dialect

Create and activate a virtual environment:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install Jupyter Notebook, the SQLAlchemy dialect, and the visualization dependencies:

```shell
python3 -m pip install notebook tidbcloudlake-sqlalchemy pandas matplotlib
```

The `tidbcloudlake-sqlalchemy` package installs SQLAlchemy and the required {{{ .lake }}} Python driver.

Start Jupyter Notebook:

```shell
jupyter notebook
```

In the Jupyter interface, create a Python notebook.

## Connect to TiDB Cloud Lake

The SQLAlchemy connection URI uses the following format:

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

To avoid storing credentials in the notebook, set the connection URI in an environment variable before starting Jupyter Notebook:

```shell
export LAKE_SQLALCHEMY_URI='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

In the notebook, create a SQLAlchemy engine:

```python
import os

from sqlalchemy import create_engine, text

engine = create_engine(os.environ["LAKE_SQLALCHEMY_URI"])
```

## Query and visualize data

Run the following cell to create a sample table and query it:

```python
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS jupyter_sales"))
    connection.execute(
        text(
            """
            CREATE TABLE jupyter_sales (
                sale_date DATE,
                quantity INT
            )
            """
        )
    )
    connection.execute(
        text(
            """
            INSERT INTO jupyter_sales VALUES
                ('2026-08-01', 5),
                ('2026-08-01', 3),
                ('2026-08-02', 4),
                ('2026-08-03', 10)
            """
        )
    )
    result = connection.execute(
        text(
            """
            SELECT sale_date, SUM(quantity) AS total_quantity
            FROM jupyter_sales
            GROUP BY sale_date
            ORDER BY sale_date
            """
        )
    )
    rows = result.fetchall()
    columns = list(result.keys())
```

Convert the query result to a pandas DataFrame and create a bar chart:

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(rows, columns=columns)
df.plot.bar(x="sale_date", y="total_quantity", legend=False)
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()
```

When you finish the tutorial, remove the sample table:

```python
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS jupyter_sales"))
```

## Related resources

- [`tidbcloudlake-sqlalchemy` on PyPI](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [Connect to TiDB Cloud Lake using Python](/tidb-cloud-lake/guides/connect-using-python.md)

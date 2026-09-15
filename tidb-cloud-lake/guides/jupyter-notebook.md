---
title: 使用 Jupyter Notebook 连接到 TiDB Cloud Lake
summary: 了解如何通过 SQLAlchemy 将 Jupyter Notebook 连接到 TiDB Cloud Lake，执行查询，并使用 pandas 可视化查询结果。
---

# 使用 Jupyter Notebook 连接到 TiDB Cloud Lake

[Jupyter Notebook](https://jupyter.org/) 是一个用于运行代码、查询数据和创建可视化内容的交互式环境。你可以通过 [TiDB Cloud Lake dialect for SQLAlchemy](https://github.com/tidbcloud/lake-sqlalchemy) 将 notebook 连接到 {{{ .lake }}}。

## 准备工作 {#prerequisites}

开始之前，请确保你具备以下条件：

- Python 3.8 或更高版本
- 一个 {{{ .lake }}} 账户、数据库和计算集群 (Warehouse)
- 连接所需的 host、用户名、密码、数据库和计算集群名称

如需了解如何获取连接信息，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

## 安装 Jupyter Notebook 和 SQLAlchemy 方言 {#install-jupyter-notebook-and-the-sqlalchemy-dialect}

创建并激活虚拟环境：

```shell
python3 -m venv .venv
source .venv/bin/activate
```

安装 Jupyter Notebook、SQLAlchemy 方言以及可视化所需的依赖：

```shell
python3 -m pip install notebook tidbcloudlake-sqlalchemy pandas matplotlib
```

`tidbcloudlake-sqlalchemy` 包会安装 SQLAlchemy 以及所需的 {{{ .lake }}} Python 驱动。

启动 Jupyter Notebook：

```shell
jupyter notebook
```

在 Jupyter 接口中，创建一个 Python notebook。

## 连接到 TiDB Cloud Lake {#connect-to-tidb-cloud-lake}

SQLAlchemy 连接 URI 使用以下格式：

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

为避免将凭证存储在 notebook 中，请在启动 Jupyter Notebook 之前，将连接 URI 设置到环境变量中：

```shell
export LAKE_SQLALCHEMY_URI='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

在 notebook 中，创建一个 SQLAlchemy engine：

```python
import os

from sqlalchemy import create_engine, text

engine = create_engine(os.environ["LAKE_SQLALCHEMY_URI"])
```

## 查询并可视化数据 {#query-and-visualize-data}

运行以下单元以创建示例表并对其进行查询：

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

将查询结果转换为 pandas DataFrame，并创建柱状图：

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(rows, columns=columns)
df.plot.bar(x="sale_date", y="total_quantity", legend=False)
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()
```

完成本教程后，删除示例表：

```python
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS jupyter_sales"))
```

## 相关资源 {#related-resources}

- [PyPI 上的 `tidbcloudlake-sqlalchemy`](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [使用 Python 连接到 TiDB Cloud Lake](/tidb-cloud-lake/guides/connect-using-python.md)
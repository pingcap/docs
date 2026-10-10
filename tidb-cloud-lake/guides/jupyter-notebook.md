---
title: Jupyter Notebook で TiDB Cloud Lake に接続する
summary: SQLAlchemy を使用して Jupyter Notebook を TiDB Cloud Lake に接続し、クエリを実行して、pandas でクエリ結果を可視化する方法を学びます。
---

# Jupyter Notebook で TiDB Cloud Lake に接続する

[Jupyter Notebook](https://jupyter.org/) は、コードの実行、データのクエリ、可視化の作成を行うためのインタラクティブな環境です。[SQLAlchemy 用 TiDB Cloud Lake dialect](https://github.com/tidbcloud/lake-sqlalchemy) を通じて、ノートブックを {{{ .lake }}} に接続できます。

## 前提条件 {#prerequisites}

開始する前に、次のものを用意してください。

- Python 3.8 以降
- {{{ .lake }}} のアカウント、データベース、および warehouse
- 接続に使用する host、username、password、database、および warehouse 名

接続情報の取得方法については、[Warehouse に接続する](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

## Jupyter Notebook と SQLAlchemy dialect をインストールする {#install-jupyter-notebook-and-the-sqlalchemy-dialect}

仮想環境を作成して有効化します。

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Jupyter Notebook、SQLAlchemy dialect、および可視化に必要な依存関係をインストールします。

```shell
python3 -m pip install notebook tidbcloudlake-sqlalchemy pandas matplotlib
```

`tidbcloudlake-sqlalchemy` パッケージには、SQLAlchemy と必要な {{{ .lake }}} Python ドライバーが含まれています。

Jupyter Notebook を起動します。

```shell
jupyter notebook
```

Jupyter のインターフェースで、Python ノートブックを作成します。

## TiDB Cloud Lake に接続する {#connect-to-tidb-cloud-lake}

SQLAlchemy の接続 URI は、次の形式を使用します。

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

ノートブックに認証情報を保存しないようにするため、Jupyter Notebook を起動する前に、接続 URI を環境変数に設定します。

```shell
export LAKE_SQLALCHEMY_URI='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

ノートブックで SQLAlchemy engine を作成します。

```python
import os

from sqlalchemy import create_engine, text

engine = create_engine(os.environ["LAKE_SQLALCHEMY_URI"])
```

## データをクエリして可視化する {#query-and-visualize-data}

次のセルを実行して、サンプルテーブルを作成し、それに対してクエリを実行します。

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

クエリ結果を pandas DataFrame に変換し、棒グラフを作成します。

```python
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(rows, columns=columns)
df.plot.bar(x="sale_date", y="total_quantity", legend=False)
plt.ylabel("Quantity")
plt.tight_layout()
plt.show()
```

チュートリアルが完了したら、サンプルテーブルを削除します。

```python
with engine.connect() as connection:
    connection.execute(text("DROP TABLE IF EXISTS jupyter_sales"))
```

## 関連リソース {#related-resources}

- [PyPI の `tidbcloudlake-sqlalchemy`](https://pypi.org/project/tidbcloudlake-sqlalchemy/)
- [Python を使用して TiDB Cloud Lake に接続する](/tidb-cloud-lake/guides/connect-using-python.md)
---
title: App Development for mysql-connector-python
summary: Learn how to build a simple Python application based on TiDB and mysql-connector-python.
aliases: ['/appdev/dev/for-python-mysql-connector']
---

# mysql-connector-pythonのアプリ開発 {#app-development-for-the-mysql-connector-python}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDBとmysql-connector-pythonに基づいて単純なPythonアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

## 手順1.TiDBクラスタを開始します {#step-1-start-a-tidb-cluster}

ローカルストレージで疑似TiDBクラスタを開始します。

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

上記のコマンドは、モックTiKVを使用して一時的な単一ノードクラスタを開始します。クラスタはポート`$LOCAL_PORT`でリッスンします。クラスタが停止した後、データベースにすでに加えられた変更は保持されません。

> **ノート：**
>
> 「実際の」TiDBクラスタを実稼働環境にデプロイするには、次のガイドを参照してください。
>
> -   [オンプレミスのTiUPを使用してTiDBをデプロイ](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [KubernetesにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> また、無料トライアルを提供するフルマネージドのDatabase-as- [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) -Service（DBaaS）も可能です。

## ステップ2.データベースを作成します {#step-2-create-a-database}

1.  SQLシェルで、アプリケーションが使用する`tidb_example`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE tidb_example;
    ```

2.  アプリケーションのSQLユーザーを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    ユーザー名とパスワードをメモします。プロジェクトを初期化するときに、アプリケーションコードでそれらを使用します。

3.  作成したSQLユーザーに必要な権限を付与します。

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON tidb_example.* TO <username>;
    ```

## ステップ3.仮想環境を設定し、プロジェクトを初期化します {#step-3-set-virtual-environments-and-initialize-the-project}

1.  Pythonの依存関係およびパッケージマネージャーである[詩](https://python-poetry.org/docs/)を使用して、仮想環境を設定し、プロジェクトを初期化します。

    詩は、システムの依存関係を他の依存関係から分離し、依存関係の汚染を回避できます。次のコマンドを使用して、Poetryをインストールします。

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2.  Poetryを使用して開発環境を初期化します。

    {{< copyable "" >}}

    ```bash
    mkdir tidb_example
    cd tidb_example
    poetry init --no-interaction --dependency mysql-connector-python
    ```

## ステップ4.アプリケーションコードを取得して実行する {#step-4-get-and-run-the-application-code}

このチュートリアルのサンプルアプリケーションコード（ `main.py` ）は、mysql-connector-pythonを使用して、Pythonメソッドをコードコメントで説明されているSQL操作にマップします。サンプルアプリケーションコードを`main.py`という名前のPythonファイルとしてローカルマシンに保存できます。

{{< copyable "" >}}

```python
import mysql.connector

# Connects to the database in TiDB.
mydb = mysql.connector.connect(
  host="localhost",
  port="4000",
  user="root",
  passwd="",
  database="tidb_example"
)

# Creates the database cursor.
mycursor = mydb.cursor()

# Created the orders and customer tables.
mycursor.execute("CREATE TABLE IF NOT EXISTS orders (oid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, cid INT UNSIGNED, price FLOAT);")
mycursor.execute("CREATE TABLE IF NOT EXISTS customer (cid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), gender ENUM ('Male', 'Female') NOT NULL)")


# Inserts data into the orders and customer tables.

add_customer = ("INSERT INTO customer (name, gender) VALUES (%(name)s, %(gender)s);")
add_order = "INSERT INTO orders (cid, price) VALUES ({}, {});"

data_customers = [
    {'name': 'Ben', 'gender': 'Male'},
    {'name': 'Alice', 'gender': 'Female'},
    {'name': 'Peter', 'gender': 'Male'},
]

data_orders = [
    [1.3, 4.0, 52.0, 123.0, 45.0],
    [2.4, 23.4],
    [100.0],
]

# Inserts new employees.
for data_customer in data_customers:
    mycursor.execute(add_customer, data_customer)
    mydb.commit()

cid = 1
for price in data_orders[cid-1]:
    mycursor.execute(add_order.format(cid, price))
    cid = cid + 1
    mydb.commit()

# Queries the customer table.
mycursor.execute("SELECT * FROM customer")
myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Updates the orders table.
mycursor.execute("UPDATE orders SET price = %s WHERE oid = %s", (100.0, 1))
mydb.commit()

# Joins the two tables.
mycursor.execute("SELECT customer.name, orders.price FROM customer INNER JOIN orders ON customer.cid = orders.cid")

myresult = mycursor.fetchall()
for x in myresult:
  print(x)

# Closes the database connection.
mycursor.close()
mydb.close()
```

### 手順1.接続パラメーターを更新し、TiDBに接続します {#step-1-update-the-connection-parameters-and-connect-to-tidb}

`mysql.connector.connect()`に渡された文字列を、データベースの作成時に取得した接続文字列に置き換えます。

{{< copyable "" >}}

```python
mydb = mysql.connector.connect(
  host="localhost",
  port=4000,
  user="root",
  passwd="",
  database="tidb_example"
)
```

### ステップ2.アプリケーションコードを実行します {#step-2-run-the-application-code}

次のコマンドを実行して、 `main.py`のコードを実行します。

{{< copyable "" >}}

```python
python3 main.py
```

期待される出力は次のとおりです。

```
(1, 'Ben', 'Male')
(2, 'Alice', 'Female')
(3, 'Peter', 'Male')
('Ben', 100.0)
('Alice', 4.0)
('Peter', 52.0)
```

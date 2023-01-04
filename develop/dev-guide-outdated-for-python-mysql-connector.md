---
title: App Development for mysql-connector-python
summary: Learn how to build a simple Python application based on TiDB and mysql-connector-python.
---

# mysql-connector-python のアプリ開発 {#app-development-for-the-mysql-connector-python}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細は[開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDB と mysql-connector-python に基づいて単純な Python アプリケーションを構築する方法を示します。ここで構築するサンプル アプリケーションは、顧客情報と注文情報を追加、クエリ、および更新できるシンプルな CRM ツールです。

## ステップ 1. TiDB クラスターを開始する {#step-1-start-a-tidb-cluster}

ローカル ストレージで疑似 TiDB クラスターを開始します。

{{< copyable "" >}}

```bash
docker run -p 127.0.0.1:$LOCAL_PORT:4000 pingcap/tidb:v5.1.0
```

上記のコマンドは、モック TiKV を使用して一時的な単一ノード クラスターを開始します。クラスタはポート`$LOCAL_PORT`でリッスンします。クラスターが停止すると、データベースに対して既に行われた変更は保持されません。

> **ノート：**
>
> 実稼働用に「実際の」TiDB クラスターをデプロイするには、次のガイドを参照してください。
>
> -   [TiUP for On-Premises を使用して TiDB をデプロイ](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [TiDB を Kubernetes にデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) 、TiDB のフルマネージド Database-as-a-Service (DBaaS) も可能です。

## ステップ 2. データベースを作成する {#step-2-create-a-database}

1.  SQL シェルで、アプリケーションが使用する`tidb_example`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE tidb_example;
    ```

2.  アプリケーションの SQL ユーザーを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE USER <username> IDENTIFIED BY <password>;
    ```

    ユーザー名とパスワードをメモします。プロジェクトを初期化するときに、アプリケーション コードでそれらを使用します。

3.  作成した SQL ユーザーに必要な権限を付与します。

    {{< copyable "" >}}

    ```sql
    GRANT ALL ON tidb_example.* TO <username>;
    ```

## ステップ 3. 仮想環境を設定してプロジェクトを初期化する {#step-3-set-virtual-environments-and-initialize-the-project}

1.  Python の依存関係およびパッケージ マネージャーである[詩](https://python-poetry.org/docs/)を使用して、仮想環境を設定し、プロジェクトを初期化します。

    詩は、システムの依存関係を他の依存関係から分離し、依存関係の汚染を回避できます。次のコマンドを使用して、Poetry をインストールします。

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2.  Poetry を使用して開発環境を初期化します。

    {{< copyable "" >}}

    ```bash
    mkdir tidb_example
    cd tidb_example
    poetry init --no-interaction --dependency mysql-connector-python
    ```

## ステップ 4. アプリケーション コードを取得して実行する {#step-4-get-and-run-the-application-code}

このチュートリアルのサンプル アプリケーション コード ( `main.py` ) では、mysql-connector-python を使用して、コード コメントで説明されている SQL 操作に Python メソッドをマップします。サンプル アプリケーション コードは、ローカル マシンに`main.py`という名前の Python ファイルとして保存できます。

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

### ステップ 1. 接続パラメーターを更新して TiDB に接続する {#step-1-update-the-connection-parameters-and-connect-to-tidb}

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

### ステップ 2. アプリケーション コードを実行する {#step-2-run-the-application-code}

次のコマンドを実行して、 `main.py`のコードを実行します。

{{< copyable "" >}}

```python
python3 main.py
```

予想される出力は次のとおりです。

```
(1, 'Ben', 'Male')
(2, 'Alice', 'Female')
(3, 'Peter', 'Male')
('Ben', 100.0)
('Alice', 4.0)
('Peter', 52.0)
```

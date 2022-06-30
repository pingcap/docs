---
title: App Development for SQLAlchemy
summary: Learn how to build a simple Python application based on TiDB and SQLAlchemy.
aliases: ['/appdev/dev/for-sqlalchemy']
---

# SQLAlchemyのアプリ開発 {#app-development-for-sqlalchemy}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDBとSQLAlchemyに基づいて単純なPythonアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

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
> -   [オンプレミスにデプロイを使用してTiDBを導入する](https://docs.pingcap.com/tidb/v5.1/production-deployment-using-tiup)
> -   [KubernetesにTiDBをデプロイ](https://docs.pingcap.com/tidb-in-kubernetes/stable)
>
> また、無料トライアルを提供するフルマネージドのサービスとしてのデータベース（ [TiDB Cloudを使用する](https://pingcap.com/products/tidbcloud/) ）を使用することもできます。

## ステップ2.データベースを作成する {#step-2-create-a-database}

1.  SQLシェルで、アプリケーションが使用する`test_sqlalchemy`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE test_sqlalchemy;
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
    GRANT ALL ON test_sqlalchemy.* TO <username>;
    ```

## ステップ3.仮想環境を設定し、プロジェクトを初期化します {#step-3-set-virtual-environments-and-initialize-the-project}

1.  Pythonの依存関係およびパッケージマネージャーである[詩](https://python-poetry.org/docs/)を使用して、仮想環境を設定し、プロジェクトを初期化します。

    詩は、システムの依存関係を他の依存関係から分離し、依存関係の汚染を回避することができます。次のコマンドを使用して、Poetryをインストールします。

    {{< copyable "" >}}

    ```bash
    pip install --user poetry
    ```

2.  Poetryを使用して開発環境を初期化します。

    {{< copyable "" >}}

    ```bash
    poetry init --no-interaction --dependency sqlalchemy

    poetry add git+https://github.com/pingcap/sqlalchemy-tidb.git#main
    ```

## ステップ4.アプリケーションコードを取得して実行します {#step-4-get-and-run-the-application-code}

このチュートリアルのサンプルアプリケーションコード（ `main.py` ）は、SQLAlchemyを使用してPythonメソッドをSQL操作にマップします。サンプルアプリケーションコードを`main.py`という名前のPythonファイルとしてローカルマシンに保存できます。

このコードは次の操作を実行します。

1.  `User`および`Order`マッピングクラスで指定されているように、 `test_sqlalchemy`データベースに`users`および`orders`テーブルを作成します。
2.  `users`および`orders`テーブルにデータを挿入します。
3.  注文からデータを`oid`削除します。
4.  `orders` `oid`ずつ更新します。
5.  `users`と`orders`のテーブルをテーブル結合します。
6.  同じ`uid`を使用して`users`と`orders`のテーブルを照会します。

{{< copyable "" >}}

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import enum
engine = create_engine(
    'tidb://{username}:{password}@{hostname}:{port}/test_sqlalchemy?charset=utf8mb4',
    echo=False)

# The base class on which the objects will be defined.
Base = declarative_base()

class Gender(enum.Enum):
    Female = 1
    Male = 2

class User(Base):
    __tablename__ = 'users'
    uid = Column(Integer, primary_key=True)
    name = Column(String(50))
    gender = Column(Enum(Gender))

    def __repr__(self):
        return "<User(name='%s', gender='%s')>" % (
            self.name, self.gender)

class Order(Base):
    __tablename__ = 'orders'

    # Every SQLAlchemy table should have a primary key named 'id'.
    oid = Column(Integer, primary_key=True, autoincrement=True)

    uid = Column(Integer)
    price = Column(Float)

    # Prints out a user object conveniently.
    def __repr__(self):
        return "<User(oid='%d', uid='%d', price'%f')>" % (
            self.name, self.uid, self.price)

# Creates all tables by issuing CREATE TABLE commands to the database.
Base.metadata.create_all(engine)

# Creates a new session to the database by using the described engine.
Session = sessionmaker(bind=engine)
session = Session()

# Inserts users into the database.
session.add_all([
    User(name='Alice', gender=Gender.Female),
    User(name='Peter', gender=Gender.Male),
    User(name='Ben', gender=Gender.Male),
])
session.commit()

# Inserts Order into the database.
ed_user = Order(uid=1, price=2.5)

# Adds the created users to the DB and commit.
session.add(ed_user)
session.commit()

# Inserts Orders into the database.
session.add_all([
    Order(uid=1, price=0.5),
    Order(uid=2, price=4.5),
    Order(uid=2, price=2123.87),
    Order(uid=3, price=212.5),
    Order(uid=3, price=8.5),
]
)
session.commit()

# Deletes orders by oid.
session.query(Order).filter(Order.oid == 4).delete()
session.commit()

# Updates orders.
session.query(Order).filter(Order.oid == 1).update({'price': 3.5})
session.commit()

# Joins orders and users tables.
print(
    session.query(User.name, Order.price)
    .select_from(User)
    .filter(User.uid == Order.uid)
    .filter(Order.uid == 3)
    .all()
)
```

### ステップ1.接続パラメーターを更新し、TiDBに接続します {#step-1-update-the-connection-parameters-and-connect-to-tidb}

上記の`main.py`ファイルで、 `create_engine()`に渡された文字列を、データベースの作成時に取得した接続文字列に置き換えます。

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://{username}:{password}@{hostname}:{port}/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

デフォルトでは、文字列を次のように設定できます。

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://root:@127.0.0.1:4000/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

### ステップ2.アプリケーションコードを実行します {#step-2-run-the-application-code}

接続文字列が正しく設定されたら、アプリケーションコードを実行します。

{{< copyable "" >}}

```bash
python3 main.py
```

期待される出力は次のとおりです。

```
[('Ben', 212.5), ('Ben', 8.5)]
```

---
title: App Development for SQLAlchemy
summary: Learn how to build a simple Python application based on TiDB and SQLAlchemy.
---

# SQLAlchemy のアプリ開発 {#app-development-for-sqlalchemy}

> **ノート：**
>
> このドキュメントはアーカイブされました。これは、このドキュメントがその後更新されないことを示しています。詳細は[開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDB と SQLAlchemy に基づいて単純な Python アプリケーションを構築する方法を示します。ここで構築するサンプル アプリケーションは、顧客情報と注文情報を追加、クエリ、および更新できるシンプルな CRM ツールです。

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

1.  SQL シェルで、アプリケーションが使用する`test_sqlalchemy`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE test_sqlalchemy;
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
    GRANT ALL ON test_sqlalchemy.* TO <username>;
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
    poetry init --no-interaction --dependency sqlalchemy

    poetry add git+https://github.com/pingcap/sqlalchemy-tidb.git#main
    ```

## ステップ 4. アプリケーション コードを取得して実行する {#step-4-get-and-run-the-application-code}

このチュートリアルのサンプル アプリケーション コード ( `main.py` ) は、SQLAlchemy を使用して Python メソッドを SQL 操作にマップします。サンプル アプリケーション コードは、ローカル マシンに`main.py`という名前の Python ファイルとして保存できます。

コードは次の操作を実行します。

1.  `User`および`Order`マッピング クラスの指定に従って、 `test_sqlalchemy`データベースに`users`および`orders`テーブルを作成します。
2.  `users`と`orders`のテーブルにデータを挿入します。
3.  オーダーからデータを`oid`削除します。
4.  `orders`つずつ`oid`更新します。
5.  `users`と`orders`のテーブルをテーブル結合します。
6.  同じ`uid`を使用して`users`および`orders`テーブルをクエリします。

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

### ステップ 1. 接続パラメーターを更新して TiDB に接続する {#step-1-update-the-connection-parameters-and-connect-to-tidb}

上記の`main.py`ファイルで、 `create_engine()`に渡された文字列を、データベースの作成時に取得した接続文字列に置き換えます。

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://{username}:{password}@{hostname}:{port}/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

デフォルトでは、次のように文字列を設定できます。

{{< copyable "" >}}

```python
engine = create_engine(
    'tidb://root:@127.0.0.1:4000/test_sqlalchemy?charset=utf8mb4',
    echo=False)
```

### ステップ 2. アプリケーション コードを実行する {#step-2-run-the-application-code}

接続文字列が正しく設定されたら、アプリケーション コードを実行します。

{{< copyable "" >}}

```bash
python3 main.py
```

予想される出力は次のとおりです。

```
[('Ben', 212.5), ('Ben', 8.5)]
```

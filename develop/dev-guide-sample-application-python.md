---
title: Build a Simple CRUD App with TiDB and Golang
summary: Learn how to build a simple CRUD application with TiDB and Golang.
aliases: ['/tidb/v6.5/dev-guide-outdated-for-python-mysql-connector','/tidb/v6.5/dev-guide-outdated-for-sqlalchemy']
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB と Python を使用して単純な CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-python}

このドキュメントでは、TiDB と Python を使用して単純な CRUD アプリケーションを構築する方法について説明します。

> **ノート：**
>
> Python 3.10 以降のバージョンの Python を使用することをお勧めします。

## ステップ 1. TiDB クラスターを起動する {#step-1-launch-your-tidb-cluster}

<CustomContent platform="tidb">

以下にTiDBクラスターの起動方法を紹介します。

**TiDB Cloud Serverless Tierクラスターを使用する**

詳細な手順については、 [Serverless Tierクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

**ローカル クラスターを使用する**

詳細な手順については、 [ローカル テスト クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[Serverless Tierクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

</CustomContent>

## ステップ 2. コードを取得する {#step-2-get-the-code}

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

<SimpleTab groupId="language">

<div label="SQLAlchemy (Recommended)" value="SQLAlchemy">

[SQL錬金術](https://www.sqlalchemy.org/)は、人気のある Python 用のオープンソース ORM ライブラリです。以下では、例として SQLAlchemy 1.44 を使用します。

```python
import uuid
from typing import List

from sqlalchemy import create_engine, String, Column, Integer, select, func
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('mysql://root:@127.0.0.1:4000/test')
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Player(Base):
    __tablename__ = "player"

    id = Column(String(36), primary_key=True)
    coins = Column(Integer)
    goods = Column(Integer)

    def __repr__(self):
        return f'Player(id={self.id!r}, coins={self.coins!r}, goods={self.goods!r})'


def random_player(amount: int) -> List[Player]:
    players = []
    for _ in range(amount):
        players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

    return players


def simple_example() -> None:
    with Session() as session:
        # create a player, who has a coin and a goods.
        session.add(Player(id="test", coins=1, goods=1))

        # get this player, and print it.
        get_test_stmt = select(Player).where(Player.id == "test")
        for player in session.scalars(get_test_stmt):
            print(player)

        # create players with bulk inserts.
        # insert 1919 players totally, with 114 players per batch.
        # each player has a random UUID
        player_list = random_player(1919)
        for idx in range(0, len(player_list), 114):
            session.bulk_save_objects(player_list[idx:idx + 114])

        # print the number of players
        count = session.query(func.count(Player.id)).scalar()
        print(f'number of players: {count}')

        # print 3 players.
        three_players = session.query(Player).limit(3).all()
        for player in three_players:
            print(player)

        session.commit()


def trade_check(session: Session, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    # sell player goods check
    sell_player = session.query(Player.goods).filter(Player.id == sell_id).with_for_update().one()
    if sell_player.goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    buy_player = session.query(Player.coins).filter(Player.id == buy_id).with_for_update().one()
    if buy_player.coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade(sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with Session() as session:
        if trade_check(session, sell_id, buy_id, amount, price) is False:
            return

        # deduct the goods of seller, and raise his/her the coins
        session.query(Player).filter(Player.id == sell_id). \
            update({'goods': Player.goods - amount, 'coins': Player.coins + price})
        # deduct the coins of buyer, and raise his/her the goods
        session.query(Player).filter(Player.id == buy_id). \
            update({'goods': Player.goods + amount, 'coins': Player.coins - price})

        session.commit()
        print("trade success")


def trade_example() -> None:
    with Session() as session:
        # create two players
        # player 1: id is "1", has only 100 coins.
        # player 2: id is "2", has 114514 coins, and 20 goods.
        session.add(Player(id="1", coins=100, goods=0))
        session.add(Player(id="2", coins=114514, goods=20))
        session.commit()

    # player 1 wants to buy 10 goods from player 2.
    # it will cost 500 coins, but player 1 cannot afford it.
    # so this trade will fail, and nobody will lose their coins or goods
    trade(sell_id="2", buy_id="1", amount=10, price=500)

    # then player 1 has to reduce the incoming quantity to 2.
    # this trade will be successful
    trade(sell_id="2", buy_id="1", amount=2, price=100)

    with Session() as session:
        traders = session.query(Player).filter(Player.id.in_(("1", "2"))).all()
        for player in traders:
            print(player)
        session.commit()


simple_example()
trade_example()
```

ドライバーを直接使用する場合と比較して、SQLAlchemy は、データベース接続を作成するときに、さまざまなデータベースの特定の詳細を抽象化します。さらに、SQLAlchemy は、セッション管理や基本オブジェクトの CRUD などの一部の操作をカプセル化するため、コードが大幅に簡素化されます。

`Player`のクラスは、アプリケーション内の属性へのテーブルのマッピングです。 `Player`の各属性は、 `player`テーブルのフィールドに対応します。 SQLAlchemy に詳細情報を提供するために、属性は`id = Column(String(36), primary_key=True)`として定義され、フィールド タイプとその追加属性を示します。たとえば、 `id = Column(String(36), primary_key=True)` `id`属性が`String`型であること、データベース内の対応するフィールドが`VARCHAR`型であること、長さが`36`であること、および主キーであることを示します。

SQLAlchemy の使用方法の詳細については、 [SQLAlchemy ドキュメント](https://www.sqlalchemy.org/)を参照してください。

</div>

<div label="peewee (Recommended)" value="peewee">

[ピーウィー](http://docs.peewee-orm.com/en/latest/)は、人気のある Python 用のオープンソース ORM ライブラリです。以下では例として peewee 3.15.4 を使用しています。

```python
import os
import uuid
from typing import List

from peewee import *

from playhouse.db_url import connect

db = connect('mysql://root:@127.0.0.1:4000/test')


class Player(Model):
    id = CharField(max_length=36, primary_key=True)
    coins = IntegerField()
    goods = IntegerField()

    class Meta:
        database = db
        table_name = "player"


def random_player(amount: int) -> List[Player]:
    players = []
    for _ in range(amount):
        players.append(Player(id=uuid.uuid4(), coins=10000, goods=10000))

    return players


def simple_example() -> None:
    # create a player, who has a coin and a goods.
    Player.create(id="test", coins=1, goods=1)

    # get this player, and print it.
    test_player = Player.select().where(Player.id == "test").get()
    print(f'id:{test_player.id}, coins:{test_player.coins}, goods:{test_player.goods}')

    # create players with bulk inserts.
    # insert 1919 players totally, with 114 players per batch.
    # each player has a random UUID
    player_list = random_player(1919)
    Player.bulk_create(player_list, 114)

    # print the number of players
    count = Player.select().count()
    print(f'number of players: {count}')
    
    # print 3 players.
    three_players = Player.select().limit(3)
    for player in three_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


def trade_check(sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    sell_goods = Player.select(Player.goods).where(Player.id == sell_id).get().goods
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    buy_coins = Player.select(Player.coins).where(Player.id == buy_id).get().coins
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False

    return True


def trade(sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with db.atomic() as txn:
        try:
            if trade_check(sell_id, buy_id, amount, price) is False:
                txn.rollback()
                return

            # deduct the goods of seller, and raise his/her the coins
            Player.update(goods=Player.goods - amount, coins=Player.coins + price).where(Player.id == sell_id).execute()
            # deduct the coins of buyer, and raise his/her the goods
            Player.update(goods=Player.goods + amount, coins=Player.coins - price).where(Player.id == buy_id).execute()

        except Exception as err:
            txn.rollback()
            print(f'something went wrong: {err}')
        else:
            txn.commit()
            print("trade success")


def trade_example() -> None:
    # create two players
    # player 1: id is "1", has only 100 coins.
    # player 2: id is "2", has 114514 coins, and 20 goods.
    Player.create(id="1", coins=100, goods=0)
    Player.create(id="2", coins=114514, goods=20)

    # player 1 wants to buy 10 goods from player 2.
    # it will cost 500 coins, but player 1 cannot afford it.
    # so this trade will fail, and nobody will lose their coins or goods
    trade(sell_id="2", buy_id="1", amount=10, price=500)

    # then player 1 has to reduce the incoming quantity to 2.
    # this trade will be successful
    trade(sell_id="2", buy_id="1", amount=2, price=100)

    # let's take a look for player 1 and player 2 currently
    after_trade_players = Player.select().where(Player.id.in_(["1", "2"]))
    for player in after_trade_players:
        print(f'id:{player.id}, coins:{player.coins}, goods:{player.goods}')


db.connect()

# recreate the player table
db.drop_tables([Player])
db.create_tables([Player])

simple_example()
trade_example()
```

ドライバーを直接使用する場合と比較して、peewee は、データベース接続を作成するときに、さまざまなデータベースの特定の詳細を抽象化します。さらに、peewee は、セッション管理や基本オブジェクトの CRUD などの一部の操作をカプセル化するため、コードが大幅に簡素化されます。

`Player`のクラスは、アプリケーション内の属性へのテーブルのマッピングです。 `Player`の各属性は、 `player`テーブルのフィールドに対応します。 SQLAlchemy に詳細情報を提供するために、属性は`id = Column(String(36), primary_key=True)`として定義され、フィールド タイプとその追加属性を示します。たとえば、 `id = Column(String(36), primary_key=True)` `id`属性が`String`型であること、データベース内の対応するフィールドが`VARCHAR`型であること、長さが`36`であること、および主キーであることを示します。

peewee の使用方法の詳細については、 [ピーウィーのドキュメント](http://docs.peewee-orm.com/en/latest/)を参照してください。

</div>

<div label="mysqlclient" value="mysqlclient">

[mysql クライアント](https://pypi.org/project/mysqlclient/)は、人気のある Python 用のオープンソース ドライバーです。以下では、例として mysqlclient 2.1.1 を使用します。 Python 用のドライバーは、他の言語よりも使いやすいですが、基盤となる実装を保護せず、トランザクションを手動で管理する必要があります。 SQL が必要なシナリオがあまりない場合は、プログラムの結合を減らすのに役立つ ORM を使用することをお勧めします。

```python
import uuid
from typing import List

import MySQLdb
from MySQLdb import Connection
from MySQLdb.cursors import Cursor

def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )


def create_player(cursor: Cursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: Cursor, player_id: str) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: Cursor, limit: int) -> List[tuple]:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((uuid.uuid4(), 10000, 10000))

    return players


def bulk_create_player(cursor: Cursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: Cursor) -> None:
    cursor.execute("SELECT count(*) FROM player")
    return cursor.fetchone()[0]


def trade_check(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    _, sell_goods = cursor.fetchone()
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buy_coins, _ = cursor.fetchone()
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: Cursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: Connection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as conn:
        with conn.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(f'id:{test_player[0]}, coins:{test_player[1]}, goods:{test_player[2]}')

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(f'id:{player[0]}, coins:{player[1]}, goods:{player[2]}')


def trade_example() -> None:
    with get_connection(autocommit=False) as conn:
        with conn.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            conn.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(conn, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(conn, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with conn.cursor() as cur:
            _, player1_coin, player1_goods = get_player(cur, "1")
            print(f'id:1, coins:{player1_coin}, goods:{player1_goods}')
            _, player2_coin, player2_goods = get_player(cur, "2")
            print(f'id:2, coins:{player2_coin}, goods:{player2_goods}')


simple_example()
trade_example()
```

ドライバーは ORM よりもカプセル化のレベルが低いため、プログラムには多くの SQL ステートメントがあります。 ORM とは異なり、ドライバーにはデータ オブジェクトがないため、ドライバーによってクエリされた`Player`タプルとして表されます。

mysqlclient の使用方法の詳細については、 [mysqlclient ドキュメント](https://mysqlclient.readthedocs.io/)を参照してください。

</div>

<div label="PyMySQL" value="PyMySQL">

[PyMySQL](https://pypi.org/project/PyMySQL/)は、人気のある Python 用のオープンソース ドライバーです。以下では、例として PyMySQL 1.0.2 を使用します。 Python 用のドライバーは、他の言語よりも使いやすいですが、基盤となる実装を保護せず、トランザクションを手動で管理する必要があります。 SQL が必要なシナリオがあまりない場合は、プログラムの結合を減らすのに役立つ ORM を使用することをお勧めします。

```python
import uuid
from typing import List

import pymysql.cursors
from pymysql import Connection
from pymysql.cursors import DictCursor


def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='127.0.0.1',
                           port=4000,
                           user='root',
                           password='',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit)


def create_player(cursor: DictCursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: DictCursor, player_id: str) -> dict:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: DictCursor, limit: int) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((uuid.uuid4(), 10000, 10000))

    return players


def bulk_create_player(cursor: DictCursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: DictCursor) -> int:
    cursor.execute("SELECT count(*) as count FROM player")
    return cursor.fetchone()['count']


def trade_check(cursor: DictCursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    seller = cursor.fetchone()
    if seller['goods'] < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buyer = cursor.fetchone()
    if buyer['coins'] < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: DictCursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: Connection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as connection:
        with connection.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(test_player)

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(player)


def trade_example() -> None:
    with get_connection(autocommit=False) as connection:
        with connection.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            connection.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(connection, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(connection, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with connection.cursor() as cur:
            print(get_player(cur, "1"))
            print(get_player(cur, "2"))


simple_example()
trade_example()
```

ドライバーは ORM よりもカプセル化のレベルが低いため、プログラムには多くの SQL ステートメントがあります。 ORM とは異なり、ドライバーにはデータ オブジェクトがないため、ドライバーによってクエリされる`Player`ディクショナリとして表されます。

PyMySQL の使用方法の詳細については、 [PyMySQL ドキュメント](https://pymysql.readthedocs.io/en/latest/)を参照してください。

</div>

<div label="mysql-connector-python" value="mysql-connector-python">

[mysql-コネクタ-python](https://dev.mysql.com/doc/connector-python/en/)は、人気のある Python 用のオープンソース ドライバーです。以下では、例として mysql-connector-python 8.0.31 を使用しています。 Python 用のドライバーは、他の言語よりも使いやすいですが、基盤となる実装を保護せず、トランザクションを手動で管理する必要があります。 SQL が必要なシナリオがあまりない場合は、プログラムの結合を減らすのに役立つ ORM を使用することをお勧めします。

```python
import uuid
from typing import List

from mysql.connector import connect, MySQLConnection
from mysql.connector.cursor import MySQLCursor


def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(host='127.0.0.1',
                         port=4000,
                         user='root',
                         password='',
                         database='test')
    connection.autocommit = autocommit
    return connection


def create_player(cursor: MySQLCursor, player: tuple) -> None:
    cursor.execute("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", player)


def get_player(cursor: MySQLCursor, player_id: str) -> tuple:
    cursor.execute("SELECT id, coins, goods FROM player WHERE id = %s", (player_id,))
    return cursor.fetchone()


def get_players_with_limit(cursor: MySQLCursor, limit: int) -> List[tuple]:
    cursor.execute("SELECT id, coins, goods FROM player LIMIT %s", (limit,))
    return cursor.fetchall()


def random_player(amount: int) -> List[tuple]:
    players = []
    for _ in range(amount):
        players.append((str(uuid.uuid4()), 10000, 10000))

    return players


def bulk_create_player(cursor: MySQLCursor, players: List[tuple]) -> None:
    cursor.executemany("INSERT INTO player (id, coins, goods) VALUES (%s, %s, %s)", players)


def get_count(cursor: MySQLCursor) -> int:
    cursor.execute("SELECT count(*) FROM player")
    return cursor.fetchone()[0]


def trade_check(cursor: MySQLCursor, sell_id: str, buy_id: str, amount: int, price: int) -> bool:
    get_player_with_lock_sql = "SELECT coins, goods FROM player WHERE id = %s FOR UPDATE"

    # sell player goods check
    cursor.execute(get_player_with_lock_sql, (sell_id,))
    _, sell_goods = cursor.fetchone()
    if sell_goods < amount:
        print(f'sell player {sell_id} goods not enough')
        return False

    # buy player coins check
    cursor.execute(get_player_with_lock_sql, (buy_id,))
    buy_coins, _ = cursor.fetchone()
    if buy_coins < price:
        print(f'buy player {buy_id} coins not enough')
        return False


def trade_update(cursor: MySQLCursor, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    update_player_sql = "UPDATE player set goods = goods + %s, coins = coins + %s WHERE id = %s"

    # deduct the goods of seller, and raise his/her the coins
    cursor.execute(update_player_sql, (-amount, price, sell_id))
    # deduct the coins of buyer, and raise his/her the goods
    cursor.execute(update_player_sql, (amount, -price, buy_id))


def trade(connection: MySQLConnection, sell_id: str, buy_id: str, amount: int, price: int) -> None:
    with connection.cursor() as cursor:
        if trade_check(cursor, sell_id, buy_id, amount, price) is False:
            connection.rollback()
            return

        try:
            trade_update(cursor, sell_id, buy_id, amount, price)
        except Exception as err:
            connection.rollback()
            print(f'something went wrong: {err}')
        else:
            connection.commit()
            print("trade success")


def simple_example() -> None:
    with get_connection(autocommit=True) as connection:
        with connection.cursor() as cur:
            # create a player, who has a coin and a goods.
            create_player(cur, ("test", 1, 1))

            # get this player, and print it.
            test_player = get_player(cur, "test")
            print(f'id:{test_player[0]}, coins:{test_player[1]}, goods:{test_player[2]}')

            # create players with bulk inserts.
            # insert 1919 players totally, with 114 players per batch.
            # each player has a random UUID
            player_list = random_player(1919)
            for idx in range(0, len(player_list), 114):
                bulk_create_player(cur, player_list[idx:idx + 114])

            # print the number of players
            count = get_count(cur)
            print(f'number of players: {count}')

            # print 3 players.
            three_players = get_players_with_limit(cur, 3)
            for player in three_players:
                print(f'id:{player[0]}, coins:{player[1]}, goods:{player[2]}')


def trade_example() -> None:
    with get_connection(autocommit=False) as conn:
        with conn.cursor() as cur:
            # create two players
            # player 1: id is "1", has only 100 coins.
            # player 2: id is "2", has 114514 coins, and 20 goods.
            create_player(cur, ("1", 100, 0))
            create_player(cur, ("2", 114514, 20))
            conn.commit()

        # player 1 wants to buy 10 goods from player 2.
        # it will cost 500 coins, but player 1 cannot afford it.
        # so this trade will fail, and nobody will lose their coins or goods
        trade(conn, sell_id="2", buy_id="1", amount=10, price=500)

        # then player 1 has to reduce the incoming quantity to 2.
        # this trade will be successful
        trade(conn, sell_id="2", buy_id="1", amount=2, price=100)

        # let's take a look for player 1 and player 2 currently
        with conn.cursor() as cur:
            _, player1_coin, player1_goods = get_player(cur, "1")
            print(f'id:1, coins:{player1_coin}, goods:{player1_goods}')
            _, player2_coin, player2_goods = get_player(cur, "2")
            print(f'id:2, coins:{player2_coin}, goods:{player2_goods}')


simple_example()
trade_example()
```

ドライバーは ORM よりもカプセル化のレベルが低いため、プログラムには多くの SQL ステートメントがあります。 ORM とは異なり、ドライバーにはデータ オブジェクトがないため、ドライバーによってクエリされた`Player`タプルとして表されます。

mysql-connector-python の使用方法の詳細については、 [mysql-connector-python ドキュメント](https://dev.mysql.com/doc/connector-python/en/)を参照してください。

</div>

</SimpleTab>

## ステップ 3. コードを実行する {#step-3-run-the-code}

次のコンテンツでは、コードを実行する方法を順を追って紹介します。

### ステップ 3.1 テーブルの初期化 {#step-3-1-initialize-table}

コードを実行する前に、テーブルを手動で初期化する必要があります。ローカルの TiDB クラスターを使用している場合は、次のコマンドを実行できます。

<SimpleTab groupId="cli">

<div label="MySQL CLI" value="mysql-client">

```shell
mysql --host 127.0.0.1 --port 4000 -u root < player_init.sql
```

</div>

<div label="MyCLI" value="mycli">

```shell
mycli --host 127.0.0.1 --port 4000 -u root --no-warn < player_init.sql
```

</div>

</SimpleTab>

ローカル クラスターを使用していない場合、または MySQL クライアントをインストールしていない場合は、任意の方法 (Navicat、DBeaver、またはその他の GUI ツールなど) を使用してクラスターに接続し、 `player_init.sql`のファイルで SQL ステートメントを実行します。

### ステップ 3.2 TiDB Cloudのパラメーターを変更する {#step-3-2-modify-parameters-for-tidb-cloud}

TiDB Cloud Serverless Tierクラスターを使用している場合は、CA ルート パスを指定し、次の例の`<ca_path>`を CA パスに置き換える必要があります。システムの CA ルート パスを取得するには、 [システムの CA ルート パスはどこにありますか?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system)を参照してください。

<SimpleTab groupId="language">

<div label="SQLAlchemy (Recommended)" value="SQLAlchemy">

TiDB Cloud Serverless Tierクラスターを使用している場合は、 `sqlalchemy_example.py`の`create_engine`関数のパラメーターを変更します。

```python
engine = create_engine('mysql://root:@127.0.0.1:4000/test')
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次のとおりであるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のように`create_engine`を変更できます。

```python
engine = create_engine('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', connect_args={
    "ssl_mode": "VERIFY_IDENTITY",
    "ssl": {
        "ca": "<ca_path>"
    }
})
```

</div>

<div label="peewee (Recommended)" value="peewee">

TiDB Cloud Serverless Tierクラスターを使用している場合は、 `sqlalchemy_example.py`の`create_engine`関数のパラメーターを変更します。

```python
db = connect('mysql://root:@127.0.0.1:4000/test')
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次のとおりであるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のように`connect`を変更できます。

-   peewee が PyMySQL をドライバーとして使用する場合:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', 
        ssl_verify_cert=True, ssl_ca="<ca_path>")
    ```

-   peewee がドライバーとして mysqlclient を使用する場合:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test',
        ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<ca_path>"})
    ```

peewee はドライバーにパラメーターを渡すため、peewee を使用する場合はドライバーの使用タイプに注意する必要があります。

</div>

<div label="mysqlclient" value="mysqlclient">

TiDB Cloud Serverless Tierクラスターを使用している場合は、 `get_connection`関数を`mysqlclient_example.py`に変更します。

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="127.0.0.1",
        port=4000,
        user="root",
        password="",
        database="test",
        autocommit=autocommit
    )
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次のとおりであるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のように`get_connection`を変更できます。

```python
def get_connection(autocommit: bool = True) -> MySQLdb.Connection:
    return MySQLdb.connect(
        host="xxx.tidbcloud.com",
        port=4000,
        user="2aEp24QWEDLqRFs.root",
        password="123456",
        database="test",
        autocommit=autocommit,
        ssl_mode="VERIFY_IDENTITY",
        ssl={
            "ca": "<ca_path>"
        }
    )
```

</div>

<div label="PyMySQL" value="PyMySQL">

TiDB Cloud Serverless Tierクラスターを使用している場合は、 `get_connection`関数を`pymysql_example.py`に変更します。

```python
def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='127.0.0.1',
                           port=4000,
                           user='root',
                           password='',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit)
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次のとおりであるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のように`get_connection`を変更できます。

```python
def get_connection(autocommit: bool = False) -> Connection:
    return pymysql.connect(host='xxx.tidbcloud.com',
                           port=4000,
                           user='2aEp24QWEDLqRFs.root',
                           password='123546',
                           database='test',
                           cursorclass=DictCursor,
                           autocommit=autocommit,
                           ssl_ca='<ca_path>',
                           ssl_verify_cert=True,
                           ssl_verify_identity=True)
```

</div>

<div label="mysql-connector-python" value="mysql-connector-python">

TiDB Cloud Serverless Tierクラスターを使用している場合は、 `get_connection`関数を`mysql_connector_python_example.py`に変更します。

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(host='127.0.0.1',
                         port=4000,
                         user='root',
                         password='',
                         database='test')
    connection.autocommit = autocommit
    return connection
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次のとおりであるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、次のように`get_connection`を変更できます。

```python
def get_connection(autocommit: bool = True) -> MySQLConnection:
    connection = connect(
        host="xxx.tidbcloud.com",
        port=4000,
        user="2aEp24QWEDLqRFs.root",
        password="123456",
        database="test",
        autocommit=autocommit,
        ssl_ca='<ca_path>',
        ssl_verify_identity=True
    )
    connection.autocommit = autocommit
    return connection
```

</div>

</SimpleTab>

### ステップ 3.3 コードを実行する {#step-3-3-run-the-code}

コードを実行する前に、次のコマンドを使用して依存関係をインストールします。

```bash
pip3 install -r requirement.txt
```

スクリプトを複数回実行する必要がある場合は、 [テーブルの初期化](#step-31-initialize-table)セクションに従って、各実行前にテーブルを再度初期化します。

<SimpleTab groupId="language">

<div label="SQLAlchemy (Recommended)" value="SQLAlchemy">

```bash
python3 sqlalchemy_example.py
```

</div>

<div label="peewee (Recommended)" value="peewee">

```bash
python3 peewee_example.py
```

</div>

<div label="mysqlclient" value="mysqlclient">

```bash
python3 mysqlclient_example.py
```

</div>

<div label="PyMySQL" value="PyMySQL">

```bash
python3 pymysql_example.py
```

</div>

<div label="mysql-connector-python" value="mysql-connector-python">

```bash
python3 mysql_connector_python_example.py
```

</div>

</SimpleTab>

## ステップ 4. 期待される出力 {#step-4-expected-output}

<SimpleTab groupId="language">

<div label="SQLAlchemy (Recommended)" value="SQLAlchemy">

[SQLAlchemy の期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#SQLAlchemy)

</div>

<div label="peewee (Recommended)" value="peewee">

[peewee 期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#peewee)

</div>

<div label="mysqlclient" value="mysqlclient">

[mysqlclient の期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysqlclient)

</div>

<div label="PyMySQL" value="PyMySQL">

[PyMySQL の期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#PyMySQL)

</div>

<div label="mysql-connector-python" value="mysql-connector-python">

[mysql-connector-python 期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysql-connector-python)

</div>

</SimpleTab>

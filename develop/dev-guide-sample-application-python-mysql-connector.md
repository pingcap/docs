---
title: Build a Simple CRUD App with TiDB and MySQL Connector/Python
summary: Learn how to build a simple CRUD application with TiDB and MySQL Connector/Python.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB と MySQL Connector/Python を使用してシンプルな CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-mysql-connector-python}

[<a href="https://dev.mysql.com/doc/connector-python/en/">MySQL コネクタ/Python</a>](https://dev.mysql.com/doc/connector-python/en/)は、Python 用の人気のあるオープンソース ドライバーです。

このドキュメントでは、TiDB と MySQL Connector/Python を使用して単純な CRUD アプリケーションを構築する方法について説明します。

> **ノート：**
>
> Python 3.10 以降の Python バージョンを使用することをお勧めします。

## ステップ 1. TiDB クラスターを起動する {#step-1-launch-your-tidb-cluster}

<CustomContent platform="tidb">

TiDB クラスターの起動方法を紹介します。

**TiDB CloudServerless Tierクラスターを使用する**

詳細な手順については、 [<a href="/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster">Serverless Tierクラスターの作成</a>](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

**ローカルクラスターを使用する**

詳細な手順については、 [<a href="/quick-start-with-tidb.md#deploy-a-local-test-cluster">ローカルテストクラスターをデプロイ</a>](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[<a href="/production-deployment-using-tiup.md">TiUPを使用して TiDB クラスターをデプロイ</a>](/production-deployment-using-tiup.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[<a href="/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster">Serverless Tierクラスターの作成</a>](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

</CustomContent>

## ステップ 2. コードを取得する {#step-2-get-the-code}

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

以下では、例として MySQL Connector/Python 8.0.31 を使用します。 Python のドライバーは他の言語よりも使いやすいですが、基礎となる実装を保護せず、トランザクションを手動で管理する必要があります。 SQL が必要なシナリオがそれほど多くない場合は、プログラムの結合を減らすのに役立つ ORM を使用することをお勧めします。

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

ドライバーのカプセル化レベルは ORM よりも低いため、プログラム内に多数の SQL ステートメントが含まれます。 ORM とは異なり、ドライバーにはデータ オブジェクトがないため、ドライバーによってクエリされる`Player`タプルとして表されます。

MySQL Connector/Python の使用方法の詳細については、 [<a href="https://dev.mysql.com/doc/connector-python/en/">MySQL コネクタ/Python ドキュメント</a>](https://dev.mysql.com/doc/connector-python/en/)を参照してください。

## ステップ 3. コードを実行する {#step-3-run-the-code}

次のコンテンツでは、コードを実行する方法をステップごとに紹介します。

### ステップ 3.1 テーブルの初期化 {#step-3-1-initialize-table}

コードを実行する前に、テーブルを手動で初期化する必要があります。ローカル TiDB クラスターを使用している場合は、次のコマンドを実行できます。

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

ローカル クラスターを使用していない場合、または MySQL クライアントをインストールしていない場合は、好みの方法 (Navicat、DBeaver、またはその他の GUI ツールなど) を使用してクラスターに接続し、 `player_init.sql`ファイル内の SQL ステートメントを実行します。

### ステップ 3.2 TiDB Cloudのパラメータを変更する {#step-3-2-modify-parameters-for-tidb-cloud}

TiDB CloudServerless Tierクラスターを使用している場合は、CA ルート パスを指定し、次の例の`<ca_path>`を CA パスに置き換える必要があります。システム上の CA ルート パスを取得するには、 [<a href="https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system">私のシステム上の CA ルート パスはどこにありますか?</a>](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system)を参照してください。&gt;

TiDB CloudServerless Tierクラスターを使用している場合は、 `mysql_connector_python_example.py`の`get_connection`関数を変更します。

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

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、 `get_connection`を次のように変更できます。

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

### ステップ 3.3 コードを実行する {#step-3-3-run-the-code}

コードを実行する前に、次のコマンドを使用して依存関係をインストールします。

```bash
pip3 install -r requirement.txt
```

スクリプトを複数回実行する必要がある場合は、各実行前に[<a href="#step-31-initialize-table">テーブルの初期化</a>](#step-31-initialize-table)セクションに従ってテーブルを再度初期化します。

```bash
python3 mysql_connector_python_example.py
```

## ステップ 4. 期待される出力 {#step-4-expected-output}

[<a href="https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysql-connector-python">MySQL コネクタ/Python の予想される出力</a>](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#mysql-connector-python)

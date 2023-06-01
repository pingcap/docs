---
title: Build a Simple CRUD App with TiDB and peewee
summary: Learn how to build a simple CRUD application with TiDB and peewee.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB と peewee を使用してシンプルな CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-peewee}

[ピーピー](http://docs.peewee-orm.com/en/latest/)は、Python 用の人気のあるオープンソース ORM ライブラリです。

このドキュメントでは、TiDB と peewee を使用して単純な CRUD アプリケーションを構築する方法について説明します。

> **ノート：**
>
> Python 3.10 以降の Python バージョンを使用することをお勧めします。

## ステップ 1. TiDB クラスターを起動する {#step-1-launch-your-tidb-cluster}

<CustomContent platform="tidb">

TiDB クラスターの起動方法を紹介します。

**TiDB CloudServerless Tierクラスターを使用する**

詳細な手順については、 [Serverless Tierクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

**ローカルクラスターを使用する**

詳細な手順については、 [TiUPを使用して TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[Serverless Tierクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を参照してください。

</CustomContent>

## ステップ 2. コードを取得する {#step-2-get-the-code}

```shell
git clone https://github.com/pingcap-inc/tidb-example-python.git
```

以下では例として peewee 3.15.4 を使用します。

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

ドライバーを直接使用する場合と比較して、peewee は、データベース接続を作成するときにさまざまなデータベースの特定の詳細を抽象化します。さらに、peewee はセッション管理や基本オブジェクトの CRUD などの一部の操作をカプセル化するため、コードが大幅に簡素化されます。

`Player`のクラスは、アプリケーション内のテーブルの属性へのマッピングです。 `Player`の各属性は、 `player`テーブルのフィールドに対応します。 SQLAlchemy に詳細情報を提供するために、フィールド タイプとその追加属性を示す属性は`id = Column(String(36), primary_key=True)`として定義されています。たとえば、 `id = Column(String(36), primary_key=True)` 、 `id`属性が`String`タイプ、データベース内の対応するフィールドが`VARCHAR`タイプ、長さが`36`で、主キーであることを示します。

peeweee の使用方法の詳細については、 [ピーウィーのドキュメント](http://docs.peewee-orm.com/en/latest/)を参照してください。

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

TiDB CloudServerless Tierクラスターを使用している場合は、CA ルート パスを指定し、次の例の`<ca_path>`を CA パスに置き換える必要があります。システム上の CA ルート パスを取得するには、 [私のシステム上の CA ルート パスはどこにありますか?](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system)を参照してください。

TiDB CloudServerless Tierクラスターを使用している場合は、 `peewee_example.py`の`connect`関数のパラメーターを変更します。

```python
db = connect('mysql://root:@127.0.0.1:4000/test')
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、 `connect`を次のように変更できます。

-   peewee がドライバーとして PyMySQL を使用する場合:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', 
        ssl_verify_cert=True, ssl_ca="<ca_path>")
    ```

-   peewee が mysqlclient をドライバーとして使用する場合:

    ```python
    db = connect('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test',
        ssl_mode="VERIFY_IDENTITY", ssl={"ca": "<ca_path>"})
    ```

peewee はドライバーにパラメーターを渡すため、peewee を使用する場合はドライバーの使用タイプに注意する必要があります。

### ステップ 3.3 コードを実行する {#step-3-3-run-the-code}

コードを実行する前に、次のコマンドを使用して依存関係をインストールします。

```bash
pip3 install -r requirement.txt
```

スクリプトを複数回実行する必要がある場合は、各実行前に[テーブルの初期化](#step-31-initialize-table)セクションに従ってテーブルを再度初期化します。

```bash
python3 peewee_example.py
```

## ステップ 4. 期待される出力 {#step-4-expected-output}

[期待される出力](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#peewee)

---
title: Build a Simple CRUD App with TiDB and SQLAlchemy
summary: Learn how to build a simple CRUD application with TiDB and SQLAlchemy.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB と SQLAlchemy を使用してシンプルな CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-sqlalchemy}

[<a href="https://www.sqlalchemy.org/">SQLアルケミー</a>](https://www.sqlalchemy.org/)は、Python 用の人気のあるオープンソース ORM ライブラリです。

このドキュメントでは、TiDB と SQLAlchemy を使用して単純な CRUD アプリケーションを構築する方法について説明します。

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

以下では、例として SQLAlchemy 1.44 を使用します。

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

ドライバーを直接使用する場合と比較して、SQLAlchemy は、データベース接続を作成するときに、さまざまなデータベースの特定の詳細を抽象化します。さらに、SQLAlchemy はセッション管理や基本オブジェクトの CRUD などの一部の操作をカプセル化し、コードを大幅に簡素化します。

`Player`のクラスは、アプリケーション内のテーブルの属性へのマッピングです。 `Player`の各属性は、 `player`テーブルのフィールドに対応します。 SQLAlchemy に詳細情報を提供するために、フィールド タイプとその追加属性を示す属性は`id = Column(String(36), primary_key=True)`として定義されています。たとえば、 `id = Column(String(36), primary_key=True)` 、 `id`属性が`String`タイプ、データベース内の対応するフィールドが`VARCHAR`タイプ、長さが`36`で、主キーであることを示します。

SQLAlchemy の使用方法の詳細については、 [<a href="https://www.sqlalchemy.org/">SQLAlchemy ドキュメント</a>](https://www.sqlalchemy.org/)を参照してください。

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

TiDB CloudServerless Tierクラスターを使用している場合は、CA ルート パスを指定し、次の例の`<ca_path>`を CA パスに置き換える必要があります。システム上の CA ルート パスを取得するには、 [<a href="https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system">私のシステム上の CA ルート パスはどこにありますか?</a>](https://docs.pingcap.com/tidbcloud/secure-connections-to-serverless-tier-clusters#where-is-the-ca-root-path-on-my-system)を参照してください。

TiDB CloudServerless Tierクラスターを使用している場合は、 `sqlalchemy_example.py`の`create_engine`関数のパラメーターを変更します。

```python
engine = create_engine('mysql://root:@127.0.0.1:4000/test')
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、 `create_engine`を次のように変更できます。

```python
engine = create_engine('mysql://2aEp24QWEDLqRFs.root:123456@xxx.tidbcloud.com:4000/test', connect_args={
    "ssl_mode": "VERIFY_IDENTITY",
    "ssl": {
        "ca": "<ca_path>"
    }
})
```

### ステップ 3.3 コードを実行する {#step-3-3-run-the-code}

コードを実行する前に、次のコマンドを使用して依存関係をインストールします。

```bash
pip3 install -r requirement.txt
```

スクリプトを複数回実行する必要がある場合は、各実行前に[<a href="#step-31-initialize-table">テーブルの初期化</a>](#step-31-initialize-table)セクションに従ってテーブルを再度初期化します。

```bash
python3 sqlalchemy_example.py
```

## ステップ 4. 期待される出力 {#step-4-expected-output}

[<a href="https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#SQLAlchemy">SQLAlchemy の予想される出力</a>](https://github.com/pingcap-inc/tidb-example-python/blob/main/Expected-Output.md#SQLAlchemy)

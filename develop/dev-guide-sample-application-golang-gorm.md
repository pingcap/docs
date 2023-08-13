---
title: Build a Simple CRUD App with TiDB and GORM
summary: Learn how to build a simple CRUD application with TiDB and GORM.
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDB と GORM を使用してシンプルな CRUD アプリを構築する {#build-a-simple-crud-app-with-tidb-and-gorm}

[ゴーム](https://gorm.io/)は、 Golang用の人気のあるオープンソース ORM ライブラリです。

このドキュメントでは、TiDB と GORM を使用して単純な CRUD アプリケーションを構築する方法について説明します。

> **注記：**
>
> Golang 1.20 以降のバージョンを使用することをお勧めします。

## ステップ 1. TiDB クラスターを起動する {#step-1-launch-your-tidb-cluster}

<CustomContent platform="tidb">

TiDB クラスターの起動方法を紹介します。

**TiDB サーバーレス クラスターを使用する**

詳細な手順については、 [TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster)を参照してください。

**ローカルクラスターを使用する**

詳細な手順については、 [ローカルテストクラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[TiUPを使用した TiDBクラスタのデプロイ](/production-deployment-using-tiup.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB サーバーレスクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster)を参照してください。

</CustomContent>

## ステップ 2. コードを取得する {#step-2-get-the-code}

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

次の手順では`v1.23.5`を例として説明します。

TiDB トランザクションを適応させるには、次のコードに従ってツールキット[ユーティリティ](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)を作成します。

```go
package util

import (
    "gorm.io/gorm"
)

// TiDBGormBegin start a TiDB and Gorm transaction as a block. If no error is returned, the transaction will be committed. Otherwise, the transaction will be rolled back.
func TiDBGormBegin(db *gorm.DB, pessimistic bool, fc func(tx *gorm.DB) error) (err error) {
    session := db.Session(&gorm.Session{})
    if session.Error != nil {
        return session.Error
    }

    if pessimistic {
        session = session.Exec("set @@tidb_txn_mode=pessimistic")
    } else {
        session = session.Exec("set @@tidb_txn_mode=optimistic")
    }

    if session.Error != nil {
        return session.Error
    }
    return session.Transaction(fc)
}
```

`gorm`ディレクトリに移動します。

```shell
cd gorm
```

このディレクトリの構造は次のとおりです。

```
.
├── Makefile
├── go.mod
├── go.sum
└── gorm.go
```

`gorm.go`は`gorm`の本体です。 go-sql-driver/mysql と比較して、GORM は異なるデータベース間でのデータベース作成の差異を回避します。また、AutoMigrate やオブジェクトの CRUD などの多くの操作も実装されており、コードが大幅に簡素化されます。

`Player`は、テーブルのマッピングであるデータ エンティティ構造体です。 `Player`の各プロパティは、 `player`テーブルのフィールドに対応します。 go-sql-driver/mysql と比較すると、 GORM の`Player`では、詳細情報のマッピング関係を示す struct タグが追加されています ( `gorm:"primaryKey;type:VARCHAR(36);column:id"`など)。

```go

package main

import (
    "fmt"
    "math/rand"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
    "gorm.io/gorm/clause"
    "gorm.io/gorm/logger"
)

type Player struct {
    ID    string `gorm:"primaryKey;type:VARCHAR(36);column:id"`
    Coins int    `gorm:"column:coins"`
    Goods int    `gorm:"column:goods"`
}

func (*Player) TableName() string {
    return "player"
}

func main() {
    // 1. Configure the example database connection.
    db := createDB()

    // AutoMigrate for player table
    db.AutoMigrate(&Player{})

    // 2. Run some simple examples.
    simpleExample(db)

    // 3. Explore more.
    tradeExample(db)
}

func tradeExample(db *gorm.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := &Player{ID: "1", Coins: 100}
    player2 := &Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player1)
    db.Clauses(clause.OnConflict{UpdateAll: true}).Create(player2)

    // Player 1 wants to buy 10 goods from player 2.
    // It will cost 500 coins, but player 1 cannot afford it.
    fmt.Println("\nbuyGoods:\n    => this trade will fail")
    if err := buyGoods(db, player2.ID, player1.ID, 10, 500); err == nil {
        panic("there shouldn't be success")
    }

    // So player 1 has to reduce the incoming quantity to two.
    fmt.Println("\nbuyGoods:\n    => this trade will success")
    if err := buyGoods(db, player2.ID, player1.ID, 2, 100); err != nil {
        panic(err)
    }
}

func simpleExample(db *gorm.DB) {
    // Create a player, who has a coin and a goods.
    if err := db.Clauses(clause.OnConflict{UpdateAll: true}).
        Create(&Player{ID: "test", Coins: 1, Goods: 1}).Error; err != nil {
        panic(err)
    }

    // Get a player.
    var testPlayer Player
    db.Find(&testPlayer, "id = ?", "test")
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.
    bulkInsertPlayers := make([]Player, 1919, 1919)
    total, batch := 1919, 114
    for i := 0; i < total; i++ {
        bulkInsertPlayers[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    if err := db.Session(&gorm.Session{Logger: db.Logger.LogMode(logger.Error)}).
        CreateInBatches(bulkInsertPlayers, batch).Error; err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount := int64(0)
    db.Model(&Player{}).Count(&playersCount)
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers := make([]Player, 3, 3)
    db.Limit(3).Find(&threePlayers)
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func createDB() *gorm.DB {
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}

func buyGoods(db *gorm.DB, sellID, buyID string, amount, price int) error {
    return util.TiDBGormBegin(db, true, func(tx *gorm.DB) error {
        var sellPlayer, buyPlayer Player
        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&sellPlayer, "id = ?", sellID).Error; err != nil {
            return err
        }

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        if err := tx.Clauses(clause.Locking{Strength: "UPDATE"}).
            Find(&buyPlayer, "id = ?", buyID).Error; err != nil {
            return err
        }

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateSQL := "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
        if err := tx.Exec(updateSQL, -amount, price, sellID).Error; err != nil {
            return err
        }

        if err := tx.Exec(updateSQL, amount, -price, buyID).Error; err != nil {
            return err
        }

        fmt.Println("\n[buyGoods]:\n    'trade success'")
        return nil
    })
}
```

## ステップ 3. コードを実行する {#step-3-run-the-code}

次のコンテンツでは、コードを実行する方法をステップごとに紹介します。

### ステップ 3.1 TiDB Cloudのパラメータを変更する {#step-3-1-modify-parameters-for-tidb-cloud}

TiDB サーバーレス クラスターを使用している場合は、 `dsn` in `gorm.go`の値を変更します。

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

設定したパスワードが`123456`で、クラスターの詳細ページから取得した接続パラメーターが次であるとします。

-   エンドポイント: `xxx.tidbcloud.com`
-   ポート: `4000`
-   ユーザー: `2aEp24QWEDLqRFs.root`

この場合、 `dsn`を次のように変更できます。

```go
dsn := "2aEp24QWEDLqRFs.root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4&tls=true"
```

### ステップ 3.2 コードを実行する {#step-3-2-run-the-code}

コードを実行するには、 `make build`と`make run`をそれぞれ実行します。

```shell
make build # this command executes `go build -o bin/gorm-example`
make run # this command executes `./bin/gorm-example`
```

または、ネイティブ コマンドを使用することもできます。

```shell
go build -o bin/gorm-example
./bin/gorm-example
```

または、 `make build`と`make run`を組み合わせた`make`コマンドを直接実行します。

## ステップ 4. 期待される出力 {#step-4-expected-output}

[GORM の期待される出力](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)

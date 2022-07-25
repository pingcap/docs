---
title: Build a Simple CRUD App with TiDB and Golang
summary: Learn how to build a simple CRUD application with TiDB and Golang.
aliases: ['/tidb/stable/dev-guide-outdated-for-go-sql-driver-mysql','/tidb/stable/dev-guide-outdated-for-gorm','/appdev/dev/for-go-sql-driver-mysql','/appdev/dev/for-gorm']
---

<!-- markdownlint-disable MD024 -->

<!-- markdownlint-disable MD029 -->

# TiDBとGolangを使用してシンプルなCRUDアプリを構築する {#build-a-simple-crud-app-with-tidb-and-golang}

このドキュメントでは、TiDBとGolangを使用して単純なCRUDアプリケーションを構築する方法について説明します。

> **ノート：**
>
> Golang1.16以降のバージョンを使用することをお勧めします。

## 手順1.TiDBクラスタを起動します {#step-1-launch-your-tidb-cluster}

以下に、TiDBクラスタを開始する方法を紹介します。

### TiDB Cloudの無料クラスタを使用する {#use-a-tidb-cloud-free-cluster}

詳細な手順については、 [無料のクラスタを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster)を参照してください。

### ローカルクラスタを使用する {#use-a-local-cluster}

詳細な手順については、 [ローカルテストクラスタをデプロイする](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[TiUPを使用してTiDBクラスターをデプロイする](/production-deployment-using-tiup.md)を参照してください。

## ステップ2.コードを取得する {#step-2-get-the-code}

{{< copyable "" >}}

```shell
git clone https://github.com/pingcap-inc/tidb-example-golang.git
```

<SimpleTab>

<div label="Using go-sql-driver/mysql">

`sqldriver`ディレクトリに移動します。

{{< copyable "" >}}

```shell
cd sqldriver
```

このディレクトリの構造は次のとおりです。

```
.
├── Makefile
├── dao.go
├── go.mod
├── go.sum
├── sql
│   └── dbinit.sql
├── sql.go
└── sqldriver.go
```

テーブル作成の初期化ステートメントは`dbinit.sql`にあります。

{{< copyable "" >}}

```sql
USE test;
DROP TABLE IF EXISTS player;

CREATE TABLE player (
    `id` VARCHAR(36),
    `coins` INTEGER,
    `goods` INTEGER,
   PRIMARY KEY (`id`)
);
```

`sqldriver.go`は`sqldriver`の本体です。 TiDBはMySQLプロトコルとの互換性が高いため、TiDBに接続するにはMySQLソースインスタンス`db, err := sql.Open("mysql", dsn)`を初期化する必要があります。次に、 `dao.go`を使用して、データの読み取り、編集、追加、および削除を行うことができます。

{{< copyable "" >}}

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)

func main() {
    // 1. Configure the example database connection.
    dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
    openDB("mysql", dsn, func(db *sql.DB) {
        // 2. Run some simple examples.
        simpleExample(db)

        // 3. Explore more.
        tradeExample(db)
    })
}

func simpleExample(db *sql.DB) {
    // Create a player, who has a coin and a goods.
    err := createPlayer(db, Player{ID: "test", Coins: 1, Goods: 1})
    if err != nil {
        panic(err)
    }

    // Get a player.
    testPlayer, err := getPlayer(db, "test")
    if err != nil {
        panic(err)
    }
    fmt.Printf("getPlayer: %+v\n", testPlayer)

    // Create players with bulk inserts. Insert 1919 players totally, with 114 players per batch.

    err = bulkInsertPlayers(db, randomPlayers(1919), 114)
    if err != nil {
        panic(err)
    }

    // Count players amount.
    playersCount, err := getCount(db)
    if err != nil {
        panic(err)
    }
    fmt.Printf("countPlayers: %d\n", playersCount)

    // Print 3 players.
    threePlayers, err := getPlayerByLimit(db, 3)
    if err != nil {
        panic(err)
    }
    for index, player := range threePlayers {
        fmt.Printf("print %d player: %+v\n", index+1, player)
    }
}

func tradeExample(db *sql.DB) {
    // Player 1: id is "1", has only 100 coins.
    // Player 2: id is "2", has 114514 coins, and 20 goods.
    player1 := Player{ID: "1", Coins: 100}
    player2 := Player{ID: "2", Coins: 114514, Goods: 20}

    // Create two players "by hand", using the INSERT statement on the backend.
    if err := createPlayer(db, player1); err != nil {
        panic(err)
    }
    if err := createPlayer(db, player2); err != nil {
        panic(err)
    }

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

func openDB(driverName, dataSourceName string, runnable func(db *sql.DB)) {
    db, err := sql.Open(driverName, dataSourceName)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}
```

TiDBトランザクションを適応させるには、次のコードに従ってツールキット[util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)を記述します。

{{< copyable "" >}}

```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

`dao.go`は、データを書き込む機能を提供するためのデータ操作メソッドのセットを定義します。これは、この例のコア部分でもあります。

{{< copyable "" >}}

```go
package main

import (
    "database/sql"
    "fmt"
    "math/rand"
    "strings"

    "github.com/google/uuid"
    "github.com/pingcap-inc/tidb-example-golang/util"
)

type Player struct {
    ID    string
    Coins int
    Goods int
}

// createPlayer create a player
func createPlayer(db *sql.DB, player Player) error {
    _, err := db.Exec(CreatePlayerSQL, player.ID, player.Coins, player.Goods)
    return err
}

// getPlayer get a player
func getPlayer(db *sql.DB, id string) (Player, error) {
    var player Player

    rows, err := db.Query(GetPlayerSQL, id)
    if err != nil {
        return player, err
    }
    defer rows.Close()

    if rows.Next() {
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            return player, nil
        } else {
            return player, err
        }
    }

    return player, fmt.Errorf("can not found player")
}

// getPlayerByLimit get players by limit
func getPlayerByLimit(db *sql.DB, limit int) ([]Player, error) {
    var players []Player

    rows, err := db.Query(GetPlayerByLimitSQL, limit)
    if err != nil {
        return players, err
    }
    defer rows.Close()

    for rows.Next() {
        player := Player{}
        err = rows.Scan(&player.ID, &player.Coins, &player.Goods)
        if err == nil {
            players = append(players, player)
        } else {
            return players, err
        }
    }

    return players, nil
}

// bulk-insert players
func bulkInsertPlayers(db *sql.DB, players []Player, batchSize int) error {
    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    stmt, err := tx.Prepare(buildBulkInsertSQL(batchSize))
    if err != nil {
        return err
    }

    defer stmt.Close()

    for len(players) > batchSize {
        if _, err := stmt.Exec(playerToArgs(players[:batchSize])...); err != nil {
            tx.Rollback()
            return err
        }

        players = players[batchSize:]
    }

    if len(players) != 0 {
        if _, err := tx.Exec(buildBulkInsertSQL(len(players)), playerToArgs(players)...); err != nil {
            tx.Rollback()
            return err
        }
    }

    if err := tx.Commit(); err != nil {
        tx.Rollback()
        return err
    }

    return nil
}

func getCount(db *sql.DB) (int, error) {
    count := 0

    rows, err := db.Query(GetCountSQL)
    if err != nil {
        return count, err
    }

    defer rows.Close()

    if rows.Next() {
        if err := rows.Scan(&count); err != nil {
            return count, err
        }
    }

    return count, nil
}

func buyGoods(db *sql.DB, sellID, buyID string, amount, price int) error {
    var sellPlayer, buyPlayer Player

    tx, err := util.TiDBSqlBegin(db, true)
    if err != nil {
        return err
    }

    buyExec := func() error {
        stmt, err := tx.Prepare(GetPlayerWithLockSQL)
        if err != nil {
            return err
        }
        defer stmt.Close()

        sellRows, err := stmt.Query(sellID)
        if err != nil {
            return err
        }
        defer sellRows.Close()

        if sellRows.Next() {
            if err := sellRows.Scan(&sellPlayer.ID, &sellPlayer.Coins, &sellPlayer.Goods); err != nil {
                return err
            }
        }
        sellRows.Close()

        if sellPlayer.ID != sellID || sellPlayer.Goods < amount {
            return fmt.Errorf("sell player %s goods not enough", sellID)
        }

        buyRows, err := stmt.Query(buyID)
        if err != nil {
            return err
        }
        defer buyRows.Close()

        if buyRows.Next() {
            if err := buyRows.Scan(&buyPlayer.ID, &buyPlayer.Coins, &buyPlayer.Goods); err != nil {
                return err
            }
        }
        buyRows.Close()

        if buyPlayer.ID != buyID || buyPlayer.Coins < price {
            return fmt.Errorf("buy player %s coins not enough", buyID)
        }

        updateStmt, err := tx.Prepare(UpdatePlayerSQL)
        if err != nil {
            return err
        }
        defer updateStmt.Close()

        if _, err := updateStmt.Exec(-amount, price, sellID); err != nil {
            return err
        }

        if _, err := updateStmt.Exec(amount, -price, buyID); err != nil {
            return err
        }

        return nil
    }

    err = buyExec()
    if err == nil {
        fmt.Println("\n[buyGoods]:\n    'trade success'")
        tx.Commit()
    } else {
        tx.Rollback()
    }

    return err
}

func playerToArgs(players []Player) []interface{} {
    var args []interface{}
    for _, player := range players {
        args = append(args, player.ID, player.Coins, player.Goods)
    }
    return args
}

func buildBulkInsertSQL(amount int) string {
    return CreatePlayerSQL + strings.Repeat(",(?,?,?)", amount-1)
}

func randomPlayers(amount int) []Player {
    players := make([]Player, amount, amount)
    for i := 0; i < amount; i++ {
        players[i] = Player{
            ID:    uuid.New().String(),
            Coins: rand.Intn(10000),
            Goods: rand.Intn(10000),
        }
    }

    return players
}
```

`sql.go`は、SQLステートメントを定数として定義します。

{{< copyable "" >}}

```go
package main

const (
    CreatePlayerSQL      = "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"
    GetPlayerSQL         = "SELECT id, coins, goods FROM player WHERE id = ?"
    GetCountSQL          = "SELECT count(*) FROM player"
    GetPlayerWithLockSQL = GetPlayerSQL + " FOR UPDATE"
    UpdatePlayerSQL      = "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
    GetPlayerByLimitSQL  = "SELECT id, coins, goods FROM player LIMIT ?"
)
```

</div>

<div label="Using GORM (Recommended)">

GORMと比較すると、go-sql-driver / mysqlの実装はベストプラクティスではない可能性があります。これは、エラー処理ロジックを記述し、 `*sql.Rows`を手動で閉じ、コードを簡単に再利用できないため、コードがわずかに冗長になるためです。

GORMは、Golangで人気のあるオープンソースのORMライブラリです。次の手順では、例として`v1.23.5`を取り上げます。

TiDBトランザクションを適応させるには、次のコードに従ってツールキット[util](https://github.com/pingcap-inc/tidb-example-golang/tree/main/util)を記述します。

{{< copyable "" >}}

```go
package util

import (
    "context"
    "database/sql"
)

type TiDBSqlTx struct {
    *sql.Tx
    conn        *sql.Conn
    pessimistic bool
}

func TiDBSqlBegin(db *sql.DB, pessimistic bool) (*TiDBSqlTx, error) {
    ctx := context.Background()
    conn, err := db.Conn(ctx)
    if err != nil {
        return nil, err
    }
    if pessimistic {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "pessimistic")
    } else {
        _, err = conn.ExecContext(ctx, "set @@tidb_txn_mode=?", "optimistic")
    }
    if err != nil {
        return nil, err
    }
    tx, err := conn.BeginTx(ctx, nil)
    if err != nil {
        return nil, err
    }
    return &TiDBSqlTx{
        conn:        conn,
        Tx:          tx,
        pessimistic: pessimistic,
    }, nil
}

func (tx *TiDBSqlTx) Commit() error {
    defer tx.conn.Close()
    return tx.Tx.Commit()
}

func (tx *TiDBSqlTx) Rollback() error {
    defer tx.conn.Close()
    return tx.Tx.Rollback()
}
```

`gorm`ディレクトリに移動します。

{{< copyable "" >}}

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

`gorm.go`は`gorm`の本体です。 go-sql-driver / mysqlと比較して、GORMは異なるデータベース間のデータベース作成の違いを回避します。また、オブジェクトのAutoMigrateやCRUDなどの多くの操作を実装しているため、コードが大幅に簡素化されます。

`Player`は、テーブルのマッピングであるデータエンティティ構造体です。 `Player`の各プロパティは、 `player`テーブルのフィールドに対応します。 go-sql-driver / mysqlと比較して、GORMの`Player`は、 `gorm:"primaryKey;type:VARCHAR(36);column:id"`などの詳細情報のマッピング関係を示すstructタグを追加します。

{{< copyable "" >}}

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

</div>

</SimpleTab>

## ステップ3.コードを実行します {#step-3-run-the-code}

次のコンテンツでは、コードを段階的に実行する方法を紹介します。

### ステップ3.1テーブルの初期化 {#step-3-1-table-initialization}

<SimpleTab>

<div label="Using go-sql-driver/mysql">

go-sql-driver / mysqlを使用する場合は、データベーステーブルを手動で初期化する必要があります。ローカルクラスタを使用していて、MySQLクライアントがローカルにインストールされている場合は、次の`sqldriver`のディレクトリで直接実行できます。

{{< copyable "" >}}

```shell
make mysql
```

または、次のコマンドを実行できます。

{{< copyable "" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
```

非ローカルクラスタを使用している場合、またはMySQLクライアントがインストールされていない場合は、クラスタに接続し、 `sql/dbinit.sql`ファイルでステートメントを実行します。

</div>

<div label="Using GORM (Recommended)">

テーブルを手動で初期化する必要はありません。

</div>

</SimpleTab>

### ステップTiDB Cloudのパラメーターを変更する {#step-3-2-modify-parameters-for-tidb-cloud}

<SimpleTab>

<div label="Using go-sql-driver/mysql">

TiDB Cloudやその他のリモートクラスターなど、ローカル以外のデフォルトクラスタを使用している場合は、 `sqldriver.go`分の`dsn`の値を変更します。

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

設定したパスワードが`123456`で、 TiDB Cloudから取得した接続文字列が次のとおりであるとします。

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

この場合、次のようにパラメータを変更できます。

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

<div label="Using GORM (Recommended)">

TiDB Cloudやその他のリモートクラスターなど、ローカル以外のデフォルトクラスタを使用している場合は、 `gorm.go`分の`dsn`の値を変更します。

{{< copyable "" >}}

```go
dsn := "root:@tcp(127.0.0.1:4000)/test?charset=utf8mb4"
```

設定したパスワードが`123456`で、 TiDB Cloudから取得した接続文字列が次のとおりであるとします。

```
mysql --connect-timeout 15 -u root -h xxx.tidbcloud.com -P 4000 -p
```

この場合、次のようにパラメータを変更できます。

{{< copyable "" >}}

```go
dsn := "root:123456@tcp(xxx.tidbcloud.com:4000)/test?charset=utf8mb4"
```

</div>

</SimpleTab>

### ステップ3.3実行 {#step-3-3-run}

<SimpleTab>

<div label="Using go-sql-driver/mysql">

コードを実行するには、それぞれ`make mysql`を`make run`し`make build` 。

{{< copyable "" >}}

```shell
make mysql # this command executes `mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql`
make build # this command executes `go build -o bin/sql-driver-example`
make run # this command executes `./bin/sql-driver-example`
```

または、ネイティブコマンドを使用できます。

{{< copyable "" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root<sql/dbinit.sql
go build -o bin/sql-driver-example
./bin/sql-driver-example
```

または、 `make mysql`の`make run`である`make all`コマンドを直接実行し`make build` 。

</div>

<div label="Using GORM (Recommended)">

コードを実行するには、それぞれ`make build`と`make run`を実行します。

{{< copyable "" >}}

```shell
make build # this command executes `go build -o bin/gorm-example`
make run # this command executes `./bin/gorm-example`
```

または、ネイティブコマンドを使用できます。

{{< copyable "" >}}

```shell
go build -o bin/gorm-example
./bin/gorm-example
```

または、 `make build`と`make run`の組み合わせである`make`コマンドを直接実行します。

</div>

</SimpleTab>

## ステップ4.期待される出力 {#step-4-expected-output}

<SimpleTab>

<div label="Using go-sql-driver/mysql">

[go-sql-driver/mysql期待される出力](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#sqldriver)

</div>

<div label="Using GORM (Recommended)">

[GORMの期待される出力](https://github.com/pingcap-inc/tidb-example-golang/blob/main/Expected-Output.md#gorm)

</div>

</SimpleTab>

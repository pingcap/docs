---
title: App Development for GORM
summary: Learn how to build a simple Golang application based on TiDB and GORM.
aliases: ['/appdev/dev/for-gorm']
---

# GORMのアプリ開発 {#app-development-for-gorm}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDBとGORMに基づいて単純なGolangアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

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

1.  SQLシェルで、アプリケーションが使用する`gorm`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE gorm;
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
    GRANT ALL ON gorm.* TO <username>;
    ```

## ステップ3.アプリケーションコードを取得して実行します {#step-3-get-and-run-the-application-code}

このチュートリアルのサンプルアプリケーションコード（ `main.go` ）は、GORMを使用して、コードコメントで説明されているSQL操作にGolangメソッドをマップします。サンプルアプリケーションコードを`main.go`という名前のGolangファイルとしてローカルマシンに保存できます。

{{< copyable "" >}}

```go
package main

import (
    "fmt"

    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)
// The schema of the Order table to be created.
type Order struct {
    Oid   int     `gorm:"primary_key;autoIncrement:true"`
    Uid   int     `gorm:"column:uid"`
    Price float64 `gorm:"column:price"`
}

type GenderModel string

const (
    Female GenderModel = "Female"
    Male   GenderModel = "Male"
)
// The schema of the User table to be created.
type User struct {
    Uid    int         `gorm:"primary_key;autoIncrement:true"`
    Name   string      `gorm:"column:name"`
    Gender GenderModel `sql:"type:gender_model"`
}

func PrintResult(tx *gorm.DB, result []Order) {
    if tx.Error == nil && tx.RowsAffected > 0 {
        for _, order := range result {
            fmt.Printf("%+v\n", order)
        }
    }
}

type JoinResult struct {
    Name  string  `json:"name"`
    Price float64 `json:"price"`
}

func PrintJoinResult(tx *gorm.DB, result []JoinResult) {
    if tx.Error == nil && tx.RowsAffected > 0 {
        for _, order := range result {
            fmt.Printf("%+v\n", order)
        }
    }
}
// Connects to TiDB.
func main() {
    dsn := "{user}:{password}@{host}:4000/{database}?charset=utf8&parseTime=True&loc=Local"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("failed to connect database")
    }

    // Creates the Order table and the User table.
    db.AutoMigrate(&Order{})
    db.AutoMigrate(&User{})

    // Inserts data into the Order and User tables.
    db.Create(&Order{Uid: 1, Price: 100})
    db.Create(&Order{Uid: 2, Price: 200})
    db.Create(&Order{Uid: 2, Price: 300})
    db.Create(&Order{Uid: 3, Price: 400})
    db.Create(&Order{Uid: 4, Price: 500})

    db.Create(&User{Name: "Alice", Gender: Female})
    db.Create(&User{Name: "John", Gender: Male})
    db.Create(&User{Name: "Ben", Gender: Male})
    db.Create(&User{Name: "Aileen", Gender: Female})

    // Deletes data from the Order table.
    db.Delete(&Order{}, 1)
    db.Where("uid = ?", 2).Delete(&Order{})

    // Updates data to the Order table.
    db.Model(&Order{}).Where("oid = ?", 2).Update("price", gorm.Expr("price * ? + ?", 2, 100))

    var orders []Order
    // Gets all records.
    result := db.Find(&orders)
    PrintResult(result, orders)

    // Gets records with conditions.
    result = db.Where("uid IN ?", []int{2, 3}).Find(&orders)
    PrintResult(result, orders)

    result = db.Where("price >= ?", 300).Find(&orders)
    PrintResult(result, orders)

    result = db.Raw("SELECT * FROM orders WHERE price = ?", 500).Scan(&orders)
    PrintResult(result, orders)

    var join_result []JoinResult
    // Joins orders and users.
    result = db.Table("users").Select("orders.price as price, users.name as name").Joins("INNER JOIN orders ON orders.uid = users.uid").Where("users.uid = ?", 4).Find(&join_result)
    PrintJoinResult(result, join_result)
}
```

### ステップ1.接続パラメーターを更新し、TiDBに接続します {#step-1-update-the-connection-parameters-and-connect-to-tidb}

上記の`main.go`ファイルで、 `sql.Open()`に渡された文字列を、データベースの作成時に取得した接続文字列に置き換えます。 `sql.Open()`関数呼び出しは、次のようになります。

{{< copyable "" >}}

```go
dsn := "root:@tcp(localhost:4000)/gorm?charset=utf8&parseTime=True&loc=Local"
```

### ステップ2.コードを実行します {#step-2-run-the-code}

1.  GORMモジュールを初期化します。

    {{< copyable "" >}}

    ```bash
    go mod init gorm_demo
    ```

2.  `main.go`のコードを実行します。

    {{< copyable "" >}}

    ```bash
    go run main.go
    ```

    期待される出力は次のとおりです。

    ```
    {Oid:4 Uid:3 Price:400}
    {Oid:5 Uid:4 Price:500}
    {Oid:4 Uid:3 Price:400}
    {Oid:4 Uid:3 Price:400}
    {Oid:5 Uid:4 Price:500}
    {Oid:5 Uid:4 Price:500}
    {Name:Aileen Price:500}
    ```

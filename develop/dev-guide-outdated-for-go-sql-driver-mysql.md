---
title: App Development for go-sql-driver/mysql
summary: Learn how to build a simple Golang application based on TiDB and go-sql-driver/mysql.
aliases: ['/appdev/dev/for-go-sql-driver-mysql']
---

# go-sql-driver/mysqlのアプリ開発 {#app-development-for-go-sql-driver-mysql}

> **ノート：**
>
> このドキュメントはアーカイブされています。これは、このドキュメントがその後更新されないことを示しています。詳細については、 [開発者ガイドの概要](/develop/dev-guide-overview.md)を参照してください。

このチュートリアルでは、TiDBとgo-sql-driver/mysqlに基づいて単純なGolangアプリケーションを構築する方法を示します。ここで構築するサンプルアプリケーションは、顧客および注文情報を追加、照会、および更新できる単純なCRMツールです。

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

1.  SQLシェルで、アプリケーションが使用する`go_mysql`のデータベースを作成します。

    {{< copyable "" >}}

    ```sql
    CREATE DATABASE django;
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
    GRANT ALL ON go_mysql.* TO <username>;
    ```

## ステップ3.アプリケーションコードを取得して実行します {#step-3-get-and-run-the-application-code}

このチュートリアルのサンプルアプリケーションコード（ `main.go` ）は、go-sql-driver / mysqlを使用して、コードコメントで説明されているSQL操作にGolangメソッドをマップします。サンプルアプリケーションコードを`main.go`という名前のGolangファイルとしてローカルマシンに保存できます。

{{< copyable "" >}}

```go
package main

import (
    "database/sql"
    "fmt"

    _ "github.com/go-sql-driver/mysql"
)
// Creates the orders and customer tables.
func init_table(db *sql.DB) (err error) {
    _, err = db.Exec(
        "CREATE TABLE IF NOT EXISTS orders (oid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, cid INT UNSIGNED, price FLOAT);")
    if err != nil {
        return
    }

    _, err = db.Exec(
        "CREATE TABLE IF NOT EXISTS customer (cid INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(255), gender ENUM ('Male', 'Female') NOT NULL)")
    if err != nil {
        return
    }
    return
}
// Inserts data into the orders and customer tables.
func init_data(db *sql.DB) (err error) {
    sqls := []string{
        "INSERT INTO customer (name, gender) value ('Ben','Male');",
        "INSERT INTO customer (name, gender) value ('Alice','Female');",
        "INSERT INTO customer (name, gender) value ('Peter','Male');",
        "INSERT INTO orders (cid, price) value (1,10.23);",
        "INSERT INTO orders (cid, price) value (2,122);",
        "INSERT INTO orders (cid, price) value (2,72.5);",
    }
    for _, sql := range sqls {
        _, err = db.Exec(sql)
        if err != nil {
            return
        }
    }

    return
}

// Connects to TiDB.
func main() {
    db, err := sql.Open("mysql", "{user}:{password}@{globalhost}:26257/go_mysql?charset=utf8mb4")
    if err != nil {
        fmt.Println(err)
        return
    }

    if err := init_table(db); err != nil {
        panic(err)
    }
    if err := init_data(db); err != nil {
        panic(err)
    }

    // Updates data in orders.
    _, err = db.Exec("UPDATE orders SET price = price + 1 WHERE oid = 1")
    if err != nil {
        panic(err)
    }
    // Deletes data from orders.
    _, err = db.Exec("DELETE FROM orders WHERE oid = 1")
    if err != nil {
        panic(err)
    }
    // Reads data from orders.
    rows, err := db.Query("SELECT * FROM orders")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    for rows.Next() {
        var oid, cid int
        var price float64
        err := rows.Scan(&oid, &cid, &price)
        if err != nil {
            panic(err)
        }
        fmt.Printf("%d %d %.2f\n", oid, cid, price)
    }
    // Joins orders and customer tables.
    rows, err = db.Query("SELECT customer.name, orders.price FROM customer, orders WHERE customer.cid = orders.cid")
    if err != nil {
        panic(err)
    }
    defer rows.Close()
    for rows.Next() {
        var name string
        var price float64
        err := rows.Scan(&name, &price)
        if err != nil {
            panic(err)
        }
        fmt.Printf("%s %.2f\n", name, price)
    }
}
```

### ステップ1.接続パラメーターを更新し、TiDBに接続します {#step-1-update-the-connection-parameters-and-connect-to-tidb}

上記の`main.go`ファイルで、 `sql.Open()`に渡された文字列を、データベースの作成時に取得した接続文字列に置き換えます。 `sql.Open()`の関数呼び出しは、次のようになります。

{{< copyable "" >}}

```go
db, err := sql.Open("mysql", "{user}:{password}@{globalhost}:26257/go_mysql?charset=utf8mb4")
```

### ステップ2.アプリケーションコードを実行します {#step-2-run-the-application-code}

1.  go-sql-driver/mysqlモジュールを初期化します。

    {{< copyable "" >}}

    ```bash
     go mod init mysql-driver-demo
    ```

2.  `main.go`のコードを実行します。

    {{< copyable "" >}}

    ```bash
    go run main.go
    ```

    期待される出力は次のとおりです。

    ```
    2 2 122.00
    3 2 72.50
    Alice 72.50
    Alice 122.00
    ```

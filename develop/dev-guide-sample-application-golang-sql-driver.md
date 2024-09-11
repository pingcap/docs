---
title: Connect to TiDB with Go-MySQL-Driver
summary: Go-MySQL-Driver を使用して TiDB に接続する方法を学びます。このチュートリアルでは、Go-MySQL-Driver を使用して TiDB で動作するGolangサンプル コード スニペットを紹介します。
---

# Go-MySQL-Driver で TiDB に接続する {#connect-to-tidb-with-go-mysql-driver}

TiDB は MySQL 互換データベースであり、 [Go-MySQL-ドライバー](https://github.com/go-sql-driver/mysql) [データベース/SQL](https://pkg.go.dev/database/sql)インターフェイス用の MySQL 実装です。

このチュートリアルでは、TiDB と Go-MySQL-Driver を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   Go-MySQL-Driver を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [行く](https://go.dev/) **1.20**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart.git
cd tidb-golang-sql-driver-quickstart
```

### ステップ2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプは**`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先は**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    プレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに必ず置き換えてください。

    TiDB Cloud Serverless では安全な接続が必要です。そのため、 `USE_SSL`の値を`true`に設定する必要があります。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    TiDB Dedicated は、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)を参照してください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    プレースホルダー`{}`を、接続ダイアログから取得した接続パラメータに必ず置き換えてください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  対応する接続文字列をコピーして`.env`ファイルに貼り付けます。例の結果は次のようになります。

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    プレースホルダー`{}`を接続パラメータに置き換え、 `USE_SSL`を`false`に設定してください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  サンプル コードを実行するには、次のコマンドを実行します。

    ```shell
    make
    ```

2.  [予想される出力.txt](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart/blob/main/Expected-Output.txt)をチェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb サンプル/tidb-golang-sql-driver クイックスタート](https://github.com/tidb-samples/tidb-golang-sql-driver-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

```golang
func openDB(driverName string, runnable func(db *sql.DB)) {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})
    db, err := sql.Open(driverName, dsn)
    if err != nil {
        panic(err)
    }
    defer db.Close()

    runnable(db)
}
```

この関数を使用する場合、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、 `${tidb_db_name}`を TiDB クラスターの実際の値に置き換える必要があります。TiDB TiDB Cloud Serverless では安全な接続が必要です。したがって、 `${use_ssl}`の値を`true`に設定する必要があります。

### データを挿入 {#insert-data}

```golang
openDB("mysql", func(db *sql.DB) {
    insertSQL = "INSERT INTO player (id, coins, goods) VALUES (?, ?, ?)"
    _, err := db.Exec(insertSQL, "id", 1, 1)

    if err != nil {
        panic(err)
    }
})
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```golang
openDB("mysql", func(db *sql.DB) {
    selectSQL = "SELECT id, coins, goods FROM player WHERE id = ?"
    rows, err := db.Query(selectSQL, "id")
    if err != nil {
        panic(err)
    }

    // This line is extremely important!
    defer rows.Close()

    id, coins, goods := "", 0, 0
    if rows.Next() {
        err = rows.Scan(&id, &coins, &goods)
        if err == nil {
            fmt.Printf("player id: %s, coins: %d, goods: %d\n", id, coins, goods)
        }
    }
})
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

```golang
openDB("mysql", func(db *sql.DB) {
    updateSQL = "UPDATE player set goods = goods + ?, coins = coins + ? WHERE id = ?"
    _, err := db.Exec(updateSQL, 1, -1, "id")

    if err != nil {
        panic(err)
    }
})
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

```golang
openDB("mysql", func(db *sql.DB) {
    deleteSQL = "DELETE FROM player WHERE id=?"
    _, err := db.Exec(deleteSQL, "id")

    if err != nil {
        panic(err)
    }
})
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役に立つメモ {#useful-notes}

### ドライバーまたは ORM フレームワークを使用していますか? {#using-driver-or-orm-framework}

Golangドライバーはデータベースへの低レベルのアクセスを提供しますが、開発者は次の作業を行う必要があります。

-   データベース接続を手動で確立および解放します。
-   データベース トランザクションを手動で管理します。
-   データ行をデータ オブジェクトに手動でマップします。

複雑な SQL 文を書く必要がない限り、開発には[ゴーム](/develop/dev-guide-sample-application-golang-gorm.md)などの[ORM](https://en.wikipedia.org/w/index.php?title=Object-relational_mapping)フレームワークを使用することをお勧めします。これは次の点で役立ちます。

-   接続とトランザクションを管理するために[定型コード](https://en.wikipedia.org/wiki/Boilerplate_code)減らします。
-   多数の SQL ステートメントの代わりにデータ オブジェクトを使用してデータを操作します。

## 次のステップ {#next-steps}

-   Go-MySQL-Driver の詳しい使い方については、 [Go-MySQL-Driver のドキュメント](https://github.com/go-sql-driver/mysql/blob/master/README.md)をご覧ください。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブル読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>

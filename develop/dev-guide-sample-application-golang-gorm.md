---
title: Connect to TiDB with GORM
summary: TiDBはMySQL互換データベースであり、GORMはGolang用の人気のあるオープンソースORMフレームワークです。このチュートリアルでは、TiDBとGORMを使用して環境をセットアップし、TiDBクラスターに接続し、アプリケーションをビルドして実行する方法を学びます。また、基本的なCRUD操作のサンプルコードスニペットも提供されています。このチュートリアルは、TiDBサーバーレス、TiDB専用、およびTiDBセルフホストで動作します。
---

# GORM を使用して TiDB に接続する {#connect-to-tidb-with-gorm}

TiDB は MySQL 互換データベースであり、 [ゴーム](https://gorm.io/index.html)はGolang用の人気のあるオープンソース ORM フレームワークです。 GORM は、 `AUTO_RANDOM`や[デフォルトのデータベース オプションとして TiDB をサポートします](https://gorm.io/docs/connecting_to_the_database.html#TiDB)などの TiDB 機能に適応します。

このチュートリアルでは、TiDB と GORM を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   GORM を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [行く](https://go.dev/) **1.20**以上。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-golang-gorm-quickstart.git
cd tidb-golang-gorm-quickstart
```

### ステップ 2: 接続情報を構成する {#step-2-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **ブランチは**`main`に設定されています

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **ヒント：**
    >
    > プログラムが Windows Subsystem for Linux (WSL) で実行されている場合は、対応する Linux ディストリビューションに切り替えます。

4.  **「パスワードの生成」**をクリックして、ランダムなパスワードを作成します。

    > **ヒント：**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. gateway01.ap-northeast-1.prod.aws.tidbcloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. xxxxxx.root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='true'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

    TiDB サーバーレスには安全な接続が必要です。したがって、 `USE_SSL` ～ `true`の値を設定する必要があります。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  **「どこからでもアクセスを許可」**をクリックし、 **「TiDB クラスター CA のダウンロード」**をクリックして CA 証明書をダウンロードします。

    接続文字列の取得方法の詳細については、 [TiDB専用標準接続](https://docs.pingcap.com/tidbcloud/connect-via-standard-connection)を参照してください。

4.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'  # e.g. tidb.xxxx.clusters.tidb-cloud.com
    TIDB_PORT='4000'
    TIDB_USER='{user}'  # e.g. root
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    プレースホルダー`{}` 、接続ダイアログから取得した接続パラメーターに必ず置き換えてください。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```dotenv
    TIDB_HOST='{host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    USE_SSL='false'
    ```

    必ずプレースホルダー`{}`接続パラメーターに置き換えて、 `USE_SSL`を`false`に設定してください。 TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 3: コードを実行して結果を確認する {#step-3-run-the-code-and-check-the-result}

1.  次のコマンドを実行してサンプル コードを実行します。

    ```shell
    make
    ```

2.  [予想される出力.txt](https://github.com/tidb-samples/tidb-golang-gorm-quickstart/blob/main/Expected-Output.txt)チェックして、出力が一致するかどうかを確認します。

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-golang-gorm-quickstart](https://github.com/tidb-samples/tidb-golang-gorm-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

```golang
func createDB() *gorm.DB {
    dsn := fmt.Sprintf("%s:%s@tcp(%s:%s)/%s?charset=utf8mb4&tls=%s",
        ${tidb_user}, ${tidb_password}, ${tidb_host}, ${tidb_port}, ${tidb_db_name}, ${use_ssl})

    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Info),
    })
    if err != nil {
        panic(err)
    }

    return db
}
```

この関数を使用する場合、 `${tidb_host}` 、 `${tidb_port}` 、 `${tidb_user}` 、 `${tidb_password}` 、および`${tidb_db_name}`を TiDB クラスターの実際の値に置き換える必要があります。 TiDB サーバーレスには安全な接続が必要です。したがって、 `${use_ssl}`の値を`true`に設定する必要があります。

### データの挿入 {#insert-data}

```golang
db.Create(&Player{ID: "id", Coins: 1, Goods: 1})
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

```golang
var queryPlayer Player
db.Find(&queryPlayer, "id = ?", "id")
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

```golang
db.Save(&Player{ID: "id", Coins: 100, Goods: 1})
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

```golang
db.Delete(&Player{ID: "id"})
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 次のステップ {#next-steps}

-   GORM の使い方については[GORM のドキュメント](https://gorm.io/docs/index.html)と[GORM のドキュメントの TiDB セクション](https://gorm.io/docs/connecting_to_the_database.html#TiDB)から学びましょう。
-   TiDB アプリケーション開発[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>

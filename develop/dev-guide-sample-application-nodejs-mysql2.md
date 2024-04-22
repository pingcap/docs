---
title: Connect to TiDB with node-mysql2
summary: TiDBはMySQL互換データベースであり、node-mysql2はNode.js用の高速mysqljs/mysql互換MySQLドライバーです。このチュートリアルでは、TiDBとnode-mysql2を使用して環境をセットアップし、TiDBクラスターに接続し、アプリケーションをビルドして実行する方法を学習できます。必要なものはNode.js >= 16.xとGit、TiDBクラスターが実行中であることです。サンプルアプリケーションコードを実行してTiDBに接続する方法や、データの挿入、クエリデータ、データの更新、データの削除などの操作方法も学ぶことができます。
---

# node-mysql2 を使用して TiDB に接続します {#connect-to-tidb-with-node-mysql2}

TiDB は MySQL 互換データベースであり、 [ノードmysql2](https://github.com/sidorares/node-mysql2)は Node.js 用の高速[mysqljs/mysql](https://github.com/mysqljs/mysql)互換 MySQL ドライバーです。

このチュートリアルでは、TiDB と node-mysql2 を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   node-mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB サーバーレス、TiDB 専用、および TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 16.x がマシンにインストールされている。
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています。
-   TiDB クラスターが実行中です。

**TiDB クラスターがない場合は、次のように作成できます。**

<CustomContent platform="tidb">

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   (推奨) [TiDB サーバーレスクラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカル テスト TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番TiDB クラスターをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプル アプリを実行して TiDB に接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart.git
cd tidb-nodejs-mysql2-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`と`dotenv`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>依存関係を既存のプロジェクトにインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

```shell
npm install mysql2 dotenv --save
```

</details>

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます。
    -   **ブランチは**`main`に設定されます。
    -   **[接続先] は**`General`に設定されます。
    -   **[オペレーティング システム] は、**アプリケーションを実行するオペレーティング システムと一致します。

4.  パスワードをまだ設定していない場合は、 **「パスワードの生成」を**クリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    ```

    > **注記**
    >
    > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は、TLS 接続を`TIDB_ENABLE_SSL`経由で有効にする**必要があります**。

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

5.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=true
    TIDB_CA_PATH={downloaded_ssl_ca_path}
    ```

    > **注記**
    >
    > パブリック エンドポイントを使用して TiDB Dended に接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、 `TIDB_ENABLE_SSL`を`true`に変更し、 `TIDB_CA_PATH`使用して接続ダイアログからダウンロードした CA 証明書のファイル パスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

次のコマンドを実行してサンプル コードを実行します。

```shell
npm start
```

接続が成功すると、コンソールには次のように TiDB クラスターのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v7.5.1)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-mysql2-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart)リポジトリを確認してください。

### 接続オプションを使用して接続する {#connect-with-connection-options}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

```javascript
// Step 1. Import the 'mysql' and 'dotenv' packages.
import { createConnection } from "mysql2/promise";
import dotenv from "dotenv";
import * as fs from "fs";

// Step 2. Load environment variables from .env file to process.env.
dotenv.config();

async function main() {
   // Step 3. Create a connection to the TiDB cluster.
   const options = {
      host: process.env.TIDB_HOST || '127.0.0.1',
      port: process.env.TIDB_PORT || 4000,
      user: process.env.TIDB_USER || 'root',
      password: process.env.TIDB_PASSWORD || '',
      database: process.env.TIDB_DATABASE || 'test',
      ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
         minVersion: 'TLSv1.2',
         ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
      } : null,
   }
   const conn = await createConnection(options);

   // Step 4. Perform some SQL operations...

   // Step 5. Close the connection.
   await conn.end();
}

void main();
```

> **注記**
>
> TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は`TIDB_ENABLE_SSL`経由の TLS 接続を有効にする**必要があります**。ただし、Node.js はデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用し、TiDB Serverless によって信頼されるため、 `TIDB_CA_PATH`経由で SSL CA 証明書を指定する必要は**ありません**。

### データの挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```javascript
const [rsh] = await conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `1`による単一の`Player`レコードを返します。

```javascript
const [rows] = await conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `1`の`Player`に`50`コインと`50`グッズを追加します。

```javascript
const [rsh] = await conn.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、ID `1`の`Player`レコードを削除します。

```javascript
const [rsh] = await conn.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 便利なメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理すると、接続の頻繁な確立と破棄によって生じるパフォーマンスのオーバーヘッドを軽減できます。
-   SQL インジェクションを回避するには、 [準備されたステートメント](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、 [続編](https://sequelize.org/) 、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)のような ORM フレームワークを使用すると、開発効率が大幅に向上します。
-   データベースで大きな数値 ( `BIGINT`と`DECIMAL`列) を扱う場合は、 `supportBigNumbers: true`オプションを有効にすることをお勧めします。
-   ネットワークの問題によるソケット エラー`read ECONNRESET`を回避するには、 `enableKeepAlive: true`オプションを有効にすることをお勧めします。 (関連問題: [シドラレス/node-mysql2#683](https://github.com/sidorares/node-mysql2/issues/683) )

## 次のステップ {#next-steps}

-   node-mysql2 ドライバーの使用法については[node-mysql2 のドキュメント](https://github.com/sidorares/node-mysql2#readme)から学びましょう。
-   [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) で TiDB [トランザクション](/develop/dev-guide-transaction-overview.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md) [データを更新する](/develop/dev-guide-update-data.md)ベスト プラクティス[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)学習[データの削除](/develop/dev-guide-delete-data.md)ます。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>

---
title: Connect to TiDB with mysql.js
summary: mysql.js を使用して TiDB に接続する方法を学びます。このチュートリアルでは、mysql.js を使用して TiDB で動作する Node.js サンプル コード スニペットを紹介します。
---

# mysql.js で TiDB に接続する {#connect-to-tidb-with-mysql-js}

TiDB は MySQL 互換のデータベースであり、 [js の](https://github.com/mysqljs/mysql)ドライバーは MySQL プロトコルを実装する純粋な Node.js JavaScript クライアントです。

このチュートリアルでは、TiDB と mysql.js ドライバーを使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   mysql.js ドライバーを使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Serverless、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 16.x がマシンにインストールされています。
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています。
-   実行中の TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

<CustomContent platform="tidb">

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   (推奨) [TiDB Cloud Serverless クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart.git
cd tidb-nodejs-mysqljs-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql`と`dotenv`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

```shell
npm install mysql dotenv --save
```

</details>

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプは**`Public`に設定されています。
    -   **ブランチは**`main`に設定されています。
    -   **Connect With は**`General`に設定されています。
    -   **オペレーティング システムは**、アプリケーションを実行するオペレーティング システムと一致します。

4.  まだパスワードを設定していない場合は、「**パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数を次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

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
    > TiDB Cloud Serverless の場合、パブリック エンドポイントを使用する場合は、 `TIDB_ENABLE_SSL`経由で TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    **パブリック**接続タイプに加えて、TiDB Dedicated は**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、環境変数を次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

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
    > パブリック エンドポイントを使用してTiDB Cloud Dedicated に接続する場合は、TLS 接続を有効にすることをお勧めします。
    >
    > TLS 接続を有効にするには、 `TIDB_ENABLE_SSL`から`true`変更し、 `TIDB_CA_PATH`使用して接続ダイアログからダウンロードした CA 証明書のファイル パスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、対応するプレースホルダー`{}`クラスターの接続パラメータに置き換えます。設定例は次のとおりです。

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

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

サンプル コードを実行するには、次のコマンドを実行します。

```shell
npm start
```

接続が成功すると、コンソールに次のように TiDB クラスターのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.1.2)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-サンプル/tidb-nodejs-mysqljs-クイックスタート](https://github.com/tidb-samples/tidb-nodejs-mysqljs-quickstart)リポジトリを参照してください。

### 接続オプションで接続する {#connect-with-connection-options}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

```javascript
// Step 1. Import the 'mysql' and 'dotenv' packages.
import { createConnection } from "mysql";
import dotenv from "dotenv";
import * as fs from "fs";

// Step 2. Load environment variables from .env file to process.env.
dotenv.config();

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
const conn = createConnection(options);

// Step 4. Perform some SQL operations...

// Step 5. Close the connection.
conn.end();
```

> **注記**
>
> TiDB Cloud Serverless の場合、パブリック エンドポイントを使用するときは、 `TIDB_ENABLE_SSL`経由で TLS 接続を有効にする**必要があります**。ただし、Node.js はデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)使用し、これはTiDB Cloud Serverless によって信頼されているため、 `TIDB_CA_PATH`経由で SSL CA 証明書を指定する必要は**ありません**。

### データを挿入 {#insert-data}

次のクエリは、 `Player`つのレコードを作成し、新しく作成されたレコードの ID を返します。

```javascript
conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100], (err, ok) => {
   if (err) {
       console.error(err);
   } else {
       console.log(ok.insertId);
   }
});
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、 ID `1`の単一の`Player`レコードを返します。

```javascript
conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1], (err, rows) => {
   if (err) {
      console.error(err);
   } else {
      console.log(rows[0]);
   }
});
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは、 ID `1`の`Player`にコイン`50`枚と商品`50`を追加します。

```javascript
conn.query(
   'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
   [50, 50, 1],
   (err, ok) => {
      if (err) {
         console.error(err);
      } else {
          console.log(ok.affectedRows);
      }
   }
);
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `1`の`Player`のレコードを削除します。

```javascript
conn.query('DELETE FROM players WHERE id = ?;', [1], (err, ok) => {
    if (err) {
        reject(err);
    } else {
        resolve(ok.affectedRows);
    }
});
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役に立つメモ {#useful-notes}

-   [接続プール](https://github.com/mysqljs/mysql#pooling-connections)使用してデータベース接続を管理すると、接続の確立と破棄を頻繁に行うことによって発生するパフォーマンスのオーバーヘッドを削減できます。

-   SQL インジェクション攻撃を回避するには、SQL を実行する前に[クエリ値のエスケープ](https://github.com/mysqljs/mysql#escaping-query-values)使用することをお勧めします。

    > **注記**
    >
    > `mysqljs/mysql`パッケージはまだ準備されたステートメントをサポートしておらず、クライアント側で値をエスケープするだけです (関連する問題: [mysqljs/mysql#274](https://github.com/mysqljs/mysql/issues/274) )。
    >
    > この機能を使用して SQL インジェクションを回避したり、バッチ挿入/更新の効率を向上させたい場合は、代わりに[マイSQL2](https://github.com/sidorares/node-mysql2)パッケージを使用することをお勧めします。

-   ORM フレームワークを使用して、 [続編](https://sequelize.org/) 、 [タイプORM](https://typeorm.io/) 、 [プリズマ](/develop/dev-guide-sample-application-nodejs-prisma.md)などの複雑な SQL ステートメントを多数使用しないシナリオで開発効率を向上させます。

-   データベース内の大きな数値 ( `BIGINT`と`DECIMAL`列) を処理する場合は、 `supportBigNumbers: true`オプションを有効にすることをお勧めします。

## 次のステップ {#next-steps}

-   [mysql.js のドキュメント](https://github.com/mysqljs/mysql#readme)からの mysql.js ドライバーの使用法について詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

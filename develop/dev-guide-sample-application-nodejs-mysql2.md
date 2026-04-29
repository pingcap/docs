---
title: Connect to TiDB with node-mysql2
summary: node-mysql2 を使用して TiDB に接続する方法を学びましょう。このチュートリアルでは、node-mysql2 を使用して TiDB と連携する Node.js のサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-nodejs-mysql2/','/ja/tidb/dev/dev-guide-sample-application-nodejs-mysql2/','/ja/tidbcloud/dev-guide-sample-application-nodejs-mysql2/']
---

# node-mysql2を使用してTiDBに接続する {#connect-to-tidb-with-node-mysql2}

TiDBはMySQL互換のデータベースであり、 [node-mysql2](https://github.com/sidorares/node-mysql2)はNode.js用の高速な[mysqljs/mysql](https://github.com/mysqljs/mysql)互換MySQLドライバです。

このチュートリアルでは、TiDBとnode-mysql2を使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   node-mysql2を使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Premium、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   お使いのコンピューターに[Node.js](https://nodejs.org/en) &gt;= 16.xがインストールされていること。
-   お使いのマシンに[Git](https://git-scm.com/downloads)がインストールされています。
-   TiDBクラスタが稼働中です。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart.git
cd tidb-nodejs-mysql2-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `mysql2`および`dotenv`を含む）をインストールするには、次のコマンドを実行します。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールします</b></summary>

既存のプロジェクトの場合、以下のコマンドを実行してパッケージをインストールしてください。

```shell
npm install mysql2 dotenv --save
```

</details>

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`General`に設定されています。
    -   **オペレーティングシステムは、**アプリケーションを実行するオペレーティングシステムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメータに置き換えます。

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
    > TiDB Cloud Starterの場合、パブリックエンドポイントを使用する際には、 `TIDB_ENABLE_SSL`を介して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Premium">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Premiumインスタンスの名前をクリックして概要ページに移動します。

2.  左側のナビゲーションペインで、 **[設定]** &gt; **[ネットワーク]**をクリックします。

3.  **ネットワークの**ページで、 **[パブリックエンドポイント****を有効にする]**をクリックし、次に**[IP アドレスの追加]**をクリックします。

    クライアントのIPアドレスがアクセスリストに追加されていることを確認してください。

4.  左側のナビゲーションペインで**「概要」**をクリックすると、インスタンスの概要ページに戻ります。

5.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

6.  接続ダイアログで、 **「接続タイプ」**ドロップダウンリストから**「パブリック」**を選択します。

    -   公開エンドポイントがまだ有効化中であることを示すメッセージが表示された場合は、処理が完了するまでお待ちください。
    -   まだパスワードを設定していない場合は、ダイアログの**「ルートパスワードを設定」**をクリックしてください。
    -   サーバー証明書を確認する必要がある場合、または接続に失敗して認証局（CA）証明書が必要な場合は、 **「CA証明書」**をクリックしてダウンロードしてください。
    -   **パブリック**接続タイプに加えて、 TiDB Cloud Premium は**プライベート エンドポイント**接続をサポートします。詳細については、 [AWS PrivateLink経由でTiDB Cloud Premiumに接続します。](/tidb-cloud/premium/connect-to-premium-via-aws-private-endpoint.md)を参照してください。

7.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

8.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER={user}
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    TIDB_ENABLE_SSL=false
    ```

9.  `.env`ファイルを保存します。

</div>
<div label="TiDB Cloud Dedicated">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Dedicatedクラスタの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログで、「**接続タイプ」**ドロップダウンリストから**「パブリック」**を選択し、 **「CA証明書」**をクリックしてCA証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、最初の接続の前に、 **[IP アクセス リストの設定] をクリックするか、「IP アクセス リストを設定する」**の手順に従って[IPアクセスリストを設定する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)。

    TiDB Cloud Dedicated は、**パブリック**接続タイプに加えて、**プライベート エンドポイント**および**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud Dedicatedクラスタに接続します](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)参照してください。

4.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメータに置き換えます。

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
    > TiDB Cloud Dedicatedへの接続にパブリックエンドポイントを使用する場合は、TLS接続を有効にすることをお勧めします。
    >
    > TLS接続を有効にするには、 `TIDB_ENABLE_SSL`を`true`に変更し、 `TIDB_CA_PATH`を使用して、接続ダイアログからダウンロードしたCA証明書のファイルパスを指定します。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数を以下のように設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    TIDB_HOST={host}
    TIDB_PORT=4000
    TIDB_USER=root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    ```

    TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>
</SimpleTab>

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

サンプルコードを実行するには、以下のコマンドを実行してください。

```shell
npm start
```

接続が成功すると、コンソールには次のようにTiDBのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.4)
    ⏳ Loading sample game data...
    ✅ Loaded sample game data.

    🆕 Created a new player with ID 12.
    ℹ️ Got Player 12: Player { id: 12, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 12, updated 1 row.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-nodejs-mysql2-quickstart](https://github.com/tidb-samples/tidb-nodejs-mysql2-quickstart)リポジトリを参照してください。

### 接続オプションを使用して接続します {#connect-with-connection-options}

以下のコードは、環境変数で定義されたオプションを使用してTiDBへの接続を確立します。

```javascript
// Step 1. Import the 'mysql' and 'dotenv' packages.
import { createConnection } from "mysql2/promise";
import dotenv from "dotenv";
import * as fs from "fs";

// Step 2. Load environment variables from .env file to process.env.
dotenv.config();

async function main() {
   // Step 3. Create a connection to TiDB.
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
> TiDB Cloud StarterおよびTiDB Cloud Essentialでは、パブリック エンドポイントを使用する場合、 `TIDB_ENABLE_SSL`を介して TLS 接続を有効にする必要が**あり****ます**。ただし、Node.js はデフォルトで組み込みの Mozilla CA を使用するため、 `TIDB_CA_PATH`を介して SSL CA 証明書を指定する必要はありません。この組み込みの[Mozilla CA証明書](https://wiki.mozilla.org/CA/Included_Certificates)はTiDB Cloud Starterによって信頼されています。

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```javascript
const [rsh] = await conn.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `Player` `1` } レコードを返します。

```javascript
const [rows] = await conn.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

以下のクエリは、 `50`の ID を持つ`50`に`Player`コインと`1`の商品を追加します。

```javascript
const [rsh] = await conn.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、IDが`Player`である`1`レコードを削除します。

```javascript
const [rsh] = await conn.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理することで、接続の頻繁な確立と切断によって発生するパフォーマンスのオーバーヘッドを削減できます。
-   SQL インジェクションを回避するには、 [準備された声明](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、[シークエライズ](https://sequelize.org/)、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)などの ORM フレームワークを使用すると、開発効率が大幅に向上します。
-   データベースで大きな数値（ `supportBigNumbers: true`列と`BIGINT`列）を扱う場合は、 `DECIMAL`オプションを有効にすることをお勧めします。
-   ネットワークの問題によるソケットエラー`enableKeepAlive: true`回避するために、{ `read ECONNRESET`オプションを有効にすることをお勧めします。（関連する問題： [sidorares/node-mysql2#683](https://github.com/sidorares/node-mysql2/issues/683) ）

## 次のステップ {#next-steps}

-   node-mysql2 ドライバーの使用方法の詳細については[node-mysql2 のドキュメント](https://github.com/sidorares/node-mysql2#readme)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)、SQL [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)などの章を読んで、TiDB アプリケーション開発のベスト プラクティスを学びましょう。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

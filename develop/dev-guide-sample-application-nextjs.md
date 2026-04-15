---
title: Connect to TiDB with mysql2 in Next.js
summary: この記事では、Next.jsでTiDBとmysql2を使用してCRUDアプリケーションを構築する方法を説明し、簡単なサンプルコードを提供します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-nextjs/','/ja/tidb/dev/dev-guide-sample-application-nextjs/','/ja/tidbcloud/dev-guide-sample-application-nextjs/']
---

# Next.jsでmysql2を使用してTiDBに接続する {#connect-to-tidb-with-mysql2-in-next-js}

TiDBはMySQL互換のデータベースであり、 [mysql2](https://github.com/sidorares/node-mysql2)はNode.jsで広く使われているオープンソースのドライバです。

このチュートリアルでは、Next.jsでTiDBとmysql2を使用して以下のタスクを実行する方法を学びます。

-   環境をセットアップしてください。
-   mysql2を使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記**
>
> このチュートリアルは、TiDB Cloud Starter、 TiDB Cloud Essential、およびTiDB Self-Managedに対応しています。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、以下が必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
-   [Git](https://git-scm.com/downloads) 。
-   TiDBクラスタ。

**TiDBクラスタをお持ちでない場合は、以下の手順で作成できます。**

-   (推奨) [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [ローカルテスト用のTiDBセルフマネージドクラスタをデプロイ。](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番本番のTiDBセルフマネージドクラスタをデプロイ。](/production-deployment-using-tiup.md)

## TiDBに接続するには、サンプルアプリを実行してください。 {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプルアプリケーションコードを実行してTiDBに接続する方法を説明します。

> **注記**
>
> 完全なコードスニペットと実行手順については、 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHubリポジトリを参照してください。

### ステップ1：サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプルコードリポジトリをクローンするには、ターミナルウィンドウで以下のコマンドを実行してください。

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `mysql2`を含む）をインストールするには、次のコマンドを実行してください。

```bash
npm install
```

### ステップ3：接続情報の設定 {#step-3-configure-connection-information}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>

<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。

    -   **ブランチ**は`main`に設定されています。

    -   **Connect With は**`General`に設定されています。

    -   お使いの環境に合った**オペレーティングシステム**を選択してください。

    > **注記**
    >
    > Node.jsアプリケーションでは、SSL CA証明書を提供する必要はありません。Node.jsはTLS（SSL）接続を確立する際に、デフォルトで組み込みの[Mozilla CA証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用するためです。

4.  **「パスワードを生成」を**クリックすると、ランダムなパスワードが生成されます。

    > **ヒント**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードをリセット」**をクリックして新しいパスワードを生成できます。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`内のプレースホルダーを、接続ダイアログで取得した値に置き換えてください。

7.  `.env`ファイルを保存します。

</div>

<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2.  対応する接続​​文字列`.env`ファイルにコピー＆ペーストしてください。例は以下のとおりです。

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`内のプレースホルダーを、 **[接続]**ウィンドウで取得した値に置き換えてください。TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空欄です。

3.  `.env`ファイルを保存します。

</div>

</SimpleTab>

### ステップ4：コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  アプリケーションを起動します:

    ```bash
    npm run dev
    ```

2.  ブラウザを開いて`http://localhost:3000`にアクセスしてください。（実際のポート番号は端末で確認してください。デフォルトは`3000`です。）

3.  サンプルコードを実行するには、 **「SQLを実行」**をクリックしてください。

4.  ターミナルの出力を確認してください。出力が以下の例と似ていれば、接続は成功しています。

    ```json
    {
      "results": [
        {
          "Hello World": "Hello World"
        }
      ]
    }
    ```

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-nextjs-vercel-quickstart](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

以下のコードは、環境変数で定義されたオプションを使用してTiDBへの接続を確立します。

```javascript
// src/lib/tidb.js
import mysql from 'mysql2';

let pool = null;

export function connect() {
  return mysql.createPool({
    host: process.env.TIDB_HOST, // TiDB host, for example: {gateway-region}.aws.tidbcloud.com
    port: process.env.TIDB_PORT || 4000, // TiDB port, default: 4000
    user: process.env.TIDB_USER, // TiDB user, for example: {prefix}.root
    password: process.env.TIDB_PASSWORD, // The password of TiDB user.
    database: process.env.TIDB_DATABASE || 'test', // TiDB database name, default: test
    ssl: {
      minVersion: 'TLSv1.2',
      rejectUnauthorized: true,
    },
    connectionLimit: 1, // Setting connectionLimit to "1" in a serverless function environment optimizes resource usage, reduces costs, ensures connection stability, and enables seamless scalability.
    maxIdle: 1, // max idle connections, the default value is the same as `connectionLimit`
    enableKeepAlive: true,
  });
}

export function getPool() {
  if (!pool) {
    pool = createPool();
  }
  return pool;
}
```

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `Player` `1` } レコードを返します。

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

以下のクエリは、 `50`の ID を持つ`50`に`Player`コインと`1`の商品を追加します。

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、IDが`Player`である`1`レコードを削除します。

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理することで、接続の頻繁な確立と切断によって発生するパフォーマンスのオーバーヘッドを削減できます。
-   SQL インジェクションを回避するには、 [準備された声明](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、[シークエライズ](https://sequelize.org/)、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)などの ORM フレームワークを使用すると、開発効率が大幅に向上します。

## 次のステップ {#next-steps}

-   ORM と Next.js を使用して複雑なアプリケーションを構築する方法の詳細については、 [書店デモ](https://github.com/pingcap/tidb-prisma-vercel-demo)を参照してください。
-   node-mysql2 ドライバーの使用方法の詳細については[node-mysql2 のドキュメント](https://sidorares.github.io/node-mysql2/docs/documentation)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、「SQL パフォーマンス最適化」などの章[単一表の読み取り](/develop/dev-guide-get-data-from-single-table.md)読んで、TiDB アプリケーション [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

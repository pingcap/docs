---
title: Connect to TiDB with mysql2 in Next.js
summary: This article describes how to build a CRUD application using TiDB and mysql2 in Next.js and provides a simple example code snippet.
---

# Next.js の mysql2 を使用して TiDB に接続する {#connect-to-tidb-with-mysql2-in-next-js}

TiDB は MySQL 互換データベースであり、 [mysql2](https://github.com/sidorares/node-mysql2)は Node.js 用の人気のあるオープンソース ドライバーです。

このチュートリアルでは、Next.js で TiDB と mysql2 を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記**
>
> このチュートリアルは、TiDB サーバーレスおよび TiDB セルフホストで動作します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
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

> **注記**
>
> 完全なコード スニペットと実行手順については、 [tidb-nextjs-vercel-クイックスタート](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub リポジトリを参照してください。

### ステップ 1: サンプル アプリ リポジトリのクローンを作成する {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`を含む) をインストールします。

```bash
npm install
```

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>

<div label="TiDB Serverless">

1.  [**クラスター**ページ](https://tidbcloud.com/console/clusters)に移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

    -   **エンドポイント タイプは**`Public`に設定されます

    -   **[接続先] は**`General`に設定されています

    -   **オペレーティング システムが**環境に一致します。

    > **注記**
    >
    > Node.js アプリケーションでは、TLS (SSL) 接続を確立するときにデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用するため、SSL CA 証明書を提供する必要はありません。

4.  **「パスワードの作成」**をクリックしてランダムなパスワードを作成します。

    > **ヒント**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」**をクリックして新しいパスワードを生成できます。

5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`のプレースホルダーを、接続ダイアログで取得した値に置き換えます。

7.  `.env`ファイルを保存します。

</div>

<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2.  対応する接続​​文字列をコピーして`.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`のプレースホルダーを、 **「接続」**ウィンドウで取得した値に置き換えます。 TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>

</SimpleTab>

### ステップ 4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  アプリケーションを起動します。

    ```bash
    npm run dev
    ```

2.  ブラウザを開いて`http://localhost:3000`にアクセスします。 (実際のポート番号については端末を確認してください。デフォルトは`3000`です。)

3.  **「RUN SQL」**をクリックしてサンプルコードを実行します。

4.  端末の出力を確認します。出力が次のような場合、接続は成功しています。

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

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-nextjs-vercel-クイックスタート](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart)リポジトリを確認してください。

### TiDB に接続する {#connect-to-tidb}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

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

### データの挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `1`による単一の`Player`レコードを返します。

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `1`の`Player`に`50`コインと`50`グッズを追加します。

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、ID `1`の`Player`レコードを削除します。

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 便利なメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)を使用してデータベース接続を管理すると、接続の頻繁な確立と破棄によって生じるパフォーマンスのオーバーヘッドを軽減できます。
-   SQL インジェクションを回避するには、 [準備されたステートメント](https://github.com/sidorares/node-mysql2#using-prepared-statements)を使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、 [続編](https://sequelize.org/) 、 [TypeORM](https://typeorm.io/) 、または[プリズマ](https://www.prisma.io/)のような ORM フレームワークを使用すると、開発効率が大幅に向上します。

## 次のステップ {#next-steps}

-   ORM と Next.js を使用して複雑なアプリケーションを構築する方法の詳細については、 [私たちの書店デモ](https://github.com/pingcap/tidb-prisma-vercel-demo)を参照してください。
-   node-mysql2 ドライバーの使用法については[node-mysql2 のドキュメント](https://github.com/sidorares/node-mysql2/tree/master/documentation/en)から学びましょう。
-   TiDB アプリケーション開発[単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md)ベスト プラクティスについて[取引](/develop/dev-guide-transaction-overview.md) 、 [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md)など) [データを更新する](/develop/dev-guide-update-data.md)参照[データの削除](/develop/dev-guide-delete-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)ください。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](/support.md)について質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

</CustomContent>

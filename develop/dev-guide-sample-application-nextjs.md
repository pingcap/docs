---
title: Connect to TiDB with mysql2 in Next.js
summary: この記事では、Next.js で TiDB と mysql2 を使用して CRUD アプリケーションを構築する方法について説明し、簡単なサンプル コード スニペットを示します。
---

# Next.js で mysql2 を使用して TiDB に接続する {#connect-to-tidb-with-mysql2-in-next-js}

TiDB は MySQL 互換のデータベースであり、 [MySQL2](https://github.com/sidorares/node-mysql2) Node.js 用の人気のオープンソース ドライバーです。

このチュートリアルでは、Next.js で TiDB と mysql2 を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   mysql2 を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的なCRUD操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることもできます。

> **注記**
>
> このチュートリアルは {{{ .starter }}} と TiDB Self-Managed を使用します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js **18**](https://nodejs.org/en/download/)以降。
-   [ギット](https://git-scm.com/downloads) 。
-   TiDB クラスター。

<CustomContent platform="tidb">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [{{{ .starter }}} クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [{{{ .starter }}} クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

> **注記**
>
> 完全なコード スニペットと実行手順については、 [tidb-nextjs-vercel-クイックスタート](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart) GitHub リポジトリを参照してください。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリのクローンを作成するには、ターミナル ウィンドウで次のコマンドを実行します。

```bash
git clone git@github.com:tidb-samples/tidb-nextjs-vercel-quickstart.git
cd tidb-nextjs-vercel-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `mysql2`を含む) をインストールします。

```bash
npm install
```

### ステップ3: 接続情報を構成する {#step-3-configure-connection-information}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>

<div label="{{{ .starter }}}">

1.  [**クラスター**ページ](https://tidbcloud.com/project/clusters)に移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています

    -   **ブランチ**は`main`に設定されています

    -   **接続先が**`General`に設定されています

    -   **オペレーティング システムは**環境に適合します。

    > **注記**
    >
    > Node.js アプリケーションでは、TLS (SSL) 接続を確立するときに Node.js がデフォルトで組み込みの[Mozilla CA証明書](https://wiki.mozilla.org/CA/Included_Certificates)使用するため、SSL CA 証明書を提供する必要はありません。

4.  ランダムなパスワードを作成するには、 **「パスワードの生成」を**クリックします。

    > **ヒント**
    >
    > 以前にパスワードを作成したことがある場合は、元のパスワードを使用するか、 **「パスワードのリセット」を**クリックして新しいパスワードを生成することができます。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

6.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```bash
    TIDB_HOST='{gateway-region}.aws.tidbcloud.com'
    TIDB_PORT='4000'
    TIDB_USER='{prefix}.root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`のプレースホルダーを接続ダイアログで取得した値に置き換えます。

7.  `.env`ファイルを保存します。

</div>

<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```bash
    # Linux
    cp .env.example .env
    ```

    ```powershell
    # Windows
    Copy-Item ".env.example" -Destination ".env"
    ```

2.  対応する接続文字列をコピーして、 `.env`ファイルに貼り付けます。結果の例は次のとおりです。

    ```bash
    TIDB_HOST='{tidb_server_host}'
    TIDB_PORT='4000'
    TIDB_USER='root'
    TIDB_PASSWORD='{password}'
    TIDB_DB_NAME='test'
    ```

    `{}`のプレースホルダーを**「接続」**ウィンドウで取得した値に置き換えます。TiDB をローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

</div>

</SimpleTab>

### ステップ4: コードを実行して結果を確認する {#step-4-run-the-code-and-check-the-result}

1.  アプリケーションを起動します。

    ```bash
    npm run dev
    ```

2.  ブラウザを開いて`http://localhost:3000`アクセスします。(実際のポート番号はターミナルで確認してください。デフォルトは`3000`です。)

3.  サンプル コードを実行するには、 **[SQL 実行]**をクリックします。

4.  ターミナルの出力を確認します。出力が以下のようになっている場合、接続は成功しています。

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

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-nextjs-vercel-クイックスタート](https://github.com/tidb-samples/tidb-nextjs-vercel-quickstart)リポジトリを参照してください。

### TiDBに接続する {#connect-to-tidb}

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

### データを挿入する {#insert-data}

次のクエリは、 `Player`つのレコードを作成し、 `ResultSetHeader`オブジェクトを返します。

```javascript
const [rsh] = await pool.query('INSERT INTO players (coins, goods) VALUES (?, ?);', [100, 100]);
console.log(rsh.insertId);
```

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID `1`の`Player`つのレコードを返します。

```javascript
const [rows] = await pool.query('SELECT id, coins, goods FROM players WHERE id = ?;', [1]);
console.log(rows[0]);
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `1`の`Player`にコイン`50`と商品`50`を追加します。

```javascript
const [rsh] = await pool.query(
    'UPDATE players SET coins = coins + ?, goods = goods + ? WHERE id = ?;',
    [50, 50, 1]
);
console.log(rsh.affectedRows);
```

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `1`の`Player`レコードを削除します。

```javascript
const [rsh] = await pool.query('DELETE FROM players WHERE id = ?;', [1]);
console.log(rsh.affectedRows);
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

-   [接続プール](https://github.com/sidorares/node-mysql2#using-connection-pools)使用してデータベース接続を管理すると、接続の確立と破棄を頻繁に行うことによって発生するパフォーマンスのオーバーヘッドを削減できます。
-   SQL インジェクションを回避するには、 [準備された文](https://github.com/sidorares/node-mysql2#using-prepared-statements)使用することをお勧めします。
-   複雑な SQL ステートメントがあまり含まれないシナリオでは、 [続編](https://sequelize.org/) 、 [タイプORM](https://typeorm.io/) 、 [プリズマ](https://www.prisma.io/)などの ORM フレームワークを使用すると、開発効率が大幅に向上します。

## 次のステップ {#next-steps}

-   ORM と Next.js を使用して複雑なアプリケーションを構築する方法の詳細については、 [書店デモ](https://github.com/pingcap/tidb-prisma-vercel-demo)参照してください。
-   [node-mysql2のドキュメント](https://sidorares.github.io/node-mysql2/docs/documentation)から node-mysql2 ドライバーの使用法について詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [単一テーブルの読み取り](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

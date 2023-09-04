---
title: Connect to TiDB with Prisma
summary: Learn how to connect to TiDB using Prisma. This tutorial gives Node.js sample code snippets that work with TiDB using Prisma.
---

# Prisma を使用して TiDB に接続する {#connect-to-tidb-with-prisma}

TiDB は MySQL 互換データベースであり、 [プリズマ](https://github.com/prisma/prisma)は Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDB と Prisma を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   Prisma を使用して TiDB クラスターに接続します。
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
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `prisma`を含む) をインストールします。

```shell
npm install
```

<details>
  <b>依存関係を既存のプロジェクトにインストールする</b>

  既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

  ```shell
  npm install prisma typescript ts-node @types/node --save-dev
  ```
</details>

### ステップ 3: 接続パラメータを指定する {#step-3-provide-connection-parameters}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
  <div label="TiDB Serverless">
    1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして、その概要ページに移動します。

    2.  右上隅にある**「接続」**をクリックします。接続ダイアログが表示されます。

    3.  接続ダイアログの設定が動作環境と一致していることを確認してください。

        -   **エンドポイント タイプは**`Public`に設定されます。
        -   **[接続先] は**`General`に設定されます。
        -   **[オペレーティング システム] は、**アプリケーションを実行するオペレーティング システムと一致します。

    4.  パスワードをまだ設定していない場合は、 **「パスワードの作成」**をクリックしてランダムなパスワードを生成します。

    5.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

        ```shell
        cp .env.example .env
        ```

    6.  `.env`ファイルを編集し、次のように環境変数`DATABASE_URL`を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

        ```dotenv
        DATABASE_URL=mysql://{user}:{password}@{host}:4000/test?sslaccept=strict
        ```

        > **注記**
        >
        > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は、 `sslaccept=strict`設定して TLS 接続を有効にする**必要があります**。

    7.  `.env`ファイルを保存します。

    8.  `prisma/schema.prisma`では、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

        ```prisma
        datasource db {
          provider = "mysql"
          url      = env("DATABASE_URL")
        }
        ```
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

    5.  `.env`ファイルを編集し、次のように環境変数`DATABASE_URL`を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

        ```dotenv
        DATABASE_URL=mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}
        ```

        > **注記**
        >
        > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は`sslaccept=strict`設定して TLS 接続を有効にすることが**推奨され**ます。 `sslaccept=strict`を設定して TLS 接続を有効にする場合は、 `sslcert=/path/to/ca.pem`を介して接続ダイアログからダウンロードした CA 証明書のファイル パスを指定する**必要があります**。

    6.  `.env`ファイルを保存します。

    7.  `prisma/schema.prisma`では、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

        ```prisma
        datasource db {
          provider = "mysql"
          url      = env("DATABASE_URL")
        }
        ```
  </div>

  <div label="TiDB Self-Hosted">
    1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

        ```shell
        cp .env.example .env
        ```

    2.  `.env`ファイルを編集し、次のように環境変数`DATABASE_URL`を設定し、対応するプレースホルダー`{}` TiDB クラスターの接続パラメーターに置き換えます。

        ```dotenv
        DATABASE_URL=mysql://{user}:{password}@{host}:4000/test
        ```

        TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

    3.  `.env`ファイルを保存します。

    4.  `prisma/schema.prisma`では、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

        ```prisma
        datasource db {
          provider = "mysql"
          url      = env("DATABASE_URL")
        }
        ```
  </div>
</SimpleTab>

### ステップ 4. データベース スキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して[プリズママイグレーション](https://www.prisma.io/docs/concepts/components/prisma-migrate)を呼び出し、 `prisma/prisma.schema`で定義したデータ モデルを使用してデータベースを初期化します。

```shell
npx prisma migrate dev
```

**`prisma.schema`で定義されたデータ モデル:**

```prisma
// Define a Player model, which represents the `players` table.
model Player {
  id        Int      @id @default(autoincrement())
  name      String   @unique(map: "uk_player_on_name") @db.VarChar(50)
  coins     Decimal  @default(0)
  goods     Int      @default(0)
  createdAt DateTime @default(now()) @map("created_at")
  profile   Profile?

  @@map("players")
}

// Define a Profile model, which represents the `profiles` table.
model Profile {
  playerId  Int    @id @map("player_id")
  biography String @db.Text

  // Define a 1:1 relation between the `Player` and `Profile` models with foreign key.
  player    Player @relation(fields: [playerId], references: [id], onDelete: Cascade, map: "fk_profile_on_player_id")

  @@map("profiles")
}
```

Prisma でデータ モデルを定義する方法については、ドキュメント[データ・モデル](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model)を参照してください。

**予想される実行出力:**

```
Your database is now in sync with your schema.

✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms
```

このコマンドは、 `prisma/prisma.schema`に基づいて TiDB データベースにアクセスする場合も[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)を生成します。

### ステップ 5: コードを実行する {#step-5-run-the-code}

次のコマンドを実行してサンプル コードを実行します。

```shell
npm start
```

**サンプルコードの主なロジック:**

```typescript
// Step 1. Import the auto-generated `@prisma/client` package.
import {Player, PrismaClient} from '@prisma/client';

async function main(): Promise<void> {
  // Step 2. Create a new `PrismaClient` instance.
  const prisma = new PrismaClient();
  try {

    // Step 3. Perform some CRUD operations with Prisma Client ...

  } finally {
    // Step 4. Disconnect Prisma Client.
    await prisma.$disconnect();
  }
}

void main();
```

**予想される実行出力:**

接続が成功すると、ターミナルは次のように TiDB クラスターのバージョンを出力します。

```
🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v6.6.0-serverless)
🆕 Created a new player with ID 1.
ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
🚮 Player 1 has been deleted.
```

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart)リポジトリを確認してください。

### データの挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`id`フィールドを含む、作成された`Player`オブジェクトを返します。

```javascript
const player: Player = await prisma.player.create({
   data: {
      name: 'Alice',
      coins: 100,
      goods: 200,
      createdAt: new Date(),
   }
});
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、レコードが見つからない場合、ID `101`または`null`を持つ単一の`Player`オブジェクトを返します。

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `101`の`Player`に`50`コインと`50`グッズを追加します。

```javascript
await prisma.player.update({
   where: {
      id: 101,
   },
   data: {
      coins: {
         increment: 50,
      },
      goods: {
         increment: 50,
      },
   }
});
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、ID `101`の`Player`削除します。

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

## 便利なメモ {#useful-notes}

### 外部キー制約と Prisma リレーション モードの比較 {#foreign-key-constraints-vs-prisma-relation-mode}

TiDB v6.6.0 以降では、 [参照整合性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)のチェックに[プリズマ関係モード](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode)ではなく[外部キー制約](https://docs.pingcap.com/tidb/stable/foreign-key)を使用することをお勧めします。

関係モードは、Prisma クライアント側での参照整合性のエミュレーションです。ただし、参照整合性を維持するために追加のデータベース クエリが必要になるため、パフォーマンスに影響があることに注意してください。

> **注記**
>
> **外部キーは、小規模および中規模のデータ シナリオに適しています。**大量のデータで外部キーを使用すると、パフォーマンスに重大な問題が発生し、システムに予期せぬ影響を与える可能性があります。外部キーを使用する予定がある場合は、最初に徹底的な検証を実行し、慎重に使用してください。

## 次のステップ {#next-steps}

-   ORM フレームワーク Prisma ドライバーの詳しい使用方法を[Prisma のドキュメント](https://www.prisma.io/docs)から学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md) ) で TiDB [トランザクション](/develop/dev-guide-transaction-overview.md)開発[データを更新する](/develop/dev-guide-update-data.md)ベスト プラクティス[データの削除](/develop/dev-guide-delete-data.md)学習[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)ます。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

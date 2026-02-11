---
title: Connect to TiDB with Prisma
summary: Prisma を使用して TiDB に接続する方法を学びます。このチュートリアルでは、Prisma を使用して TiDB を操作する Node.js のサンプルコードスニペットを紹介します。
aliases: ['/tidb/stable/dev-guide-sample-application-nodejs-prisma/','/tidb/dev/dev-guide-sample-application-nodejs-prisma/','/tidbcloud/dev-guide-sample-application-nodejs-prisma/']
---

# PrismaでTiDBに接続する {#connect-to-tidb-with-prisma}

TiDB は MySQL 互換のデータベースであり、 [プリズマ](https://github.com/prisma/prisma) Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDB と Prisma を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   Prisma を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的なCRUD操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることもできます。

> **注記：**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、および TiDB Self-Managed で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 16.x がマシンにインストールされています。
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています。
-   実行中の TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

-   (推奨) [TiDB Cloud Starter クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を説明します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

ターミナル ウィンドウで次のコマンドを実行して、サンプル コード リポジトリのクローンを作成します。

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `prisma`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>既存のプロジェクトへの依存関係をインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### ステップ3: 接続パラメータを指定する {#step-3-provide-connection-parameters}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With が**`Prisma`に設定されています。
    -   **オペレーティング システムは、**アプリケーションを実行するオペレーティング システムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」をクリックしてランダムなパスワード**を生成します。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、接続ダイアログ内の対応するプレースホルダー`{}`接続文字列に置き換えます。

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **注記**
    >
    > TiDB Cloud Starter の場合、パブリック エンドポイントを使用するときは、 `sslaccept=strict`設定して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

8.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Cloud Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストをまだ設定していない場合は、 **「IP アクセス リストの設定」を**クリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って、最初の接続の前に設定してください。

    TiDB Cloud Dedicatedは、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPCピアリング**接続タイプもサポートしています。詳細については、 [TiDB Cloud専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)ご覧ください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **注記**
    >
    > TiDB Cloud Starterでは、パブリックエンドポイントを使用する場合、 `sslaccept=strict`設定してTLS接続を有効にすることを**推奨します**。5 `sslaccept=strict`設定してTLS接続を有効にする場合、接続ダイアログからダウンロードしたCA証明書のファイルパスを`sslcert=/path/to/ca.pem`で指定する**必要があります**。

6.  `.env`ファイルを保存します。

7.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、対応するプレースホルダー`{}` TiDB クラスターの接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空になります。

3.  `.env`ファイルを保存します。

4.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### ステップ4. データベーススキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して[プリズママイグレーション](https://www.prisma.io/docs/concepts/components/prisma-migrate)呼び出し、 `prisma/prisma.schema`で定義されたデータ モデルを使用してデータベースを初期化します。

```shell
npx prisma migrate dev
```

**`prisma.schema`で定義されたデータモデル:**

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

Prisma でデータ モデルを定義する方法については、 [データモデル](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model)ドキュメントを確認してください。

**期待される実行出力:**

    Your database is now in sync with your schema.

    ✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms

このコマンドは、 `prisma/prisma.schema`に基づいて TiDB データベース アクセス用の[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)生成します。

### ステップ5: コードを実行する {#step-5-run-the-code}

サンプル コードを実行するには、次のコマンドを実行します。

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

**期待される実行出力:**

接続が成功すると、ターミナルは次のように TiDB クラスターのバージョンを出力します。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.5)
    🆕 Created a new player with ID 1.
    ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
    🚮 Player 1 has been deleted.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-prisma-クイックスタート](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart)リポジトリを参照してください。

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`id`フィールドを含む作成された`Player`オブジェクトを返します。

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

詳細については[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、レコードが見つからない場合は ID `101`または`null`を持つ単一の`Player`オブジェクトを返します。

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `101`の`Player`にコイン`50`と商品`50`を追加します。

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

詳細については[データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `101`の`Player`を削除します。

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

### 外部キー制約とPrismaリレーションモード {#foreign-key-constraints-vs-prisma-relation-mode}

[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)確認するには、外部キー制約または Prisma リレーション モードを使用できます。

-   [外部キー](https://docs.pingcap.com/tidb/stable/foreign-key)はTiDB v6.6.0からサポートされ、v8.5.0から一般公開される機能です。外部キーは関連データのテーブル間参照を可能にし、外部キー制約は関連データの一貫性を保証します。

    > **警告：**
    >
    > **外部キーは、小規模および中規模のデータを扱うシナリオに適しています。**大規模なデータで外部キーを使用すると、深刻なパフォーマンスの問題が発生する可能性があり、システムに予期せぬ影響を与える可能性があります。外部キーを使用する場合は、事前に十分な検証を行い、慎重に使用してください。

-   [Prisma関係モード](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode)はPrismaクライアント側で参照整合性をエミュレートします。ただし、参照整合性を維持するために追加のデータベースクエリが必要となるため、パフォーマンスに影響があることに注意してください。

## 次のステップ {#next-steps}

-   ORM フレームワーク Prisma ドライバーの使用方法を[Prismaのドキュメント](https://www.prisma.io/docs)から詳しく学びます。
-   [開発者ガイド](https://docs.pingcap.com/developer/)の[データを挿入する](/develop/dev-guide-insert-data.md) 、 [データを更新する](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB開発者コース](https://www.pingcap.com/education/)を通じて学習し、試験に合格すると[TiDB認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに問い合わせてください。
-   [TiDB Cloudのサポートチケットを送信する](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDBセルフマネージドのサポートチケットを送信する](/support.md)

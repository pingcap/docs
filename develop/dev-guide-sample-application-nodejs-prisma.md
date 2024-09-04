---
title: Connect to TiDB with Prisma
summary: Prisma を使用して TiDB に接続する方法を学びます。このチュートリアルでは、Prisma を使用して TiDB を操作する Node.js サンプル コード スニペットを紹介します。
---

# PrismaでTiDBに接続する {#connect-to-tidb-with-prisma}

TiDB は MySQL 互換のデータベースであり、 [プリズマ](https://github.com/prisma/prisma) Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDB と Prisma を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   Prisma を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記：**
>
> このチュートリアルは、TiDB Serverless、TiDB Dedicated、および TiDB Self-Hosted で機能します。

## 前提条件 {#prerequisites}

このチュートリアルを完了するには、次のものが必要です。

-   [Node.js](https://nodejs.org/en) &gt;= 16.x がマシンにインストールされています。
-   [ギット](https://git-scm.com/downloads)マシンにインストールされています。
-   実行中の TiDB クラスター。

**TiDB クラスターがない場合は、次のように作成できます。**

<CustomContent platform="tidb">

-   (推奨) [TiDB サーバーレス クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](/quick-start-with-tidb.md#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](/production-deployment-using-tiup.md)に従ってローカル クラスターを作成します。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   (推奨) [TiDB サーバーレス クラスターの作成](/develop/dev-guide-build-cluster-in-cloud.md)に従って、独自のTiDB Cloudクラスターを作成します。
-   [ローカルテストTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/quick-start-with-tidb#deploy-a-local-test-cluster)または[本番のTiDBクラスタをデプロイ](https://docs.pingcap.com/tidb/stable/production-deployment-using-tiup)に従ってローカル クラスターを作成します。

</CustomContent>

## サンプルアプリを実行してTiDBに接続する {#run-the-sample-app-to-connect-to-tidb}

このセクションでは、サンプル アプリケーション コードを実行して TiDB に接続する方法を示します。

### ステップ1: サンプルアプリのリポジトリをクローンする {#step-1-clone-the-sample-app-repository}

サンプル コード リポジトリを複製するには、ターミナル ウィンドウで次のコマンドを実行します。

```shell
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `prisma`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### ステップ3: 接続パラメータを指定する {#step-3-provide-connection-parameters}

選択した TiDB デプロイメント オプションに応じて、TiDB クラスターに接続します。

<SimpleTab>
<div label="TiDB Serverless">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログの構成が動作環境と一致していることを確認します。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **Connect With は**`Prisma`に設定されています。
    -   **オペレーティング システムは**、アプリケーションを実行するオペレーティング システムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードの生成」**をクリックしてランダムなパスワードを生成します。

5.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数`DATABASE_URL`を次のように設定し、接続ダイアログ内の対応するプレースホルダー`{}`を接続文字列に置き換えます。

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **注記**
    >
    > TiDB Serverless の場合、パブリック エンドポイントを使用するときは、 `sslaccept=strict`設定して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

8.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`を設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Dedicated">

1.  [**クラスター**](https://tidbcloud.com/console/clusters)ページに移動し、ターゲット クラスターの名前をクリックして概要ページに移動します。

2.  右上隅の**「接続」**をクリックします。接続ダイアログが表示されます。

3.  接続ダイアログで、 **[接続タイプ]**ドロップダウン リストから**[パブリック]**を選択し、 **[CA 証明書]**をクリックして CA 証明書をダウンロードします。

    IP アクセス リストを設定していない場合は、 **「IP アクセス リストの設定」**をクリックするか、手順[IPアクセスリストを構成する](https://docs.pingcap.com/tidbcloud/configure-ip-access-list)に従って最初の接続の前に設定してください。

    TiDB Dedicated は、**パブリック**接続タイプに加えて、**プライベートエンドポイント**と**VPC ピアリング**接続タイプもサポートしています。詳細については、 [TiDB専用クラスタに接続する](https://docs.pingcap.com/tidbcloud/connect-to-tidb-cluster)を参照してください。

4.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

5.  `.env`ファイルを編集し、環境変数`DATABASE_URL`を次のように設定し、接続ダイアログで対応するプレースホルダー`{}`を接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **注記**
    >
    > TiDB Serverless の場合、パブリックエンドポイントを使用する場合は、 `sslaccept=strict`設定して TLS 接続を有効にすることを**お勧めします**。 `sslaccept=strict`を設定して TLS 接続を有効にする場合は、 `sslcert=/path/to/ca.pem`を介して接続ダイアログからダウンロードした CA 証明書のファイルパスを指定する**必要があります**。

6.  `.env`ファイルを保存します。

7.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`を設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数`DATABASE_URL`を次のように設定し、対応するプレースホルダー`{}`を TiDB クラスターの接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

    TiDB をローカルで実行している場合、デフォルトのホスト アドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

4.  `prisma/schema.prisma`で、接続プロバイダーとして`mysql`を設定し、接続 URL として`env("DATABASE_URL")`設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### ステップ4. データベーススキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して[プリズマ移行](https://www.prisma.io/docs/concepts/components/prisma-migrate)呼び出し、 `prisma/prisma.schema`で定義されたデータ モデルを使用してデータベースを初期化します。

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

Prisma でデータ モデルを定義する方法については、 [データモデル](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model)ドキュメントを参照してください。

**予想される実行出力:**

    Your database is now in sync with your schema.

    ✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms

このコマンドは、 `prisma/prisma.schema`に基づいて TiDB データベースにアクセスするための[プリズマクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)生成します。

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

**予想される実行出力:**

接続が成功すると、ターミナルは次のように TiDB クラスターのバージョンを出力します。

    🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v6.6.0-serverless)
    🆕 Created a new player with ID 1.
    ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
    🚮 Player 1 has been deleted.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-prisma-クイックスタート](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart)リポジトリを参照してください。

### データを挿入 {#insert-data}

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

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

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

### データの更新 {#update-data}

次のクエリは、 ID `101`の`Player`にコイン`50`と商品`50`を追加します。

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

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `101`の`Player`削除します。

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役に立つメモ {#useful-notes}

### 外部キー制約と Prisma リレーション モード {#foreign-key-constraints-vs-prisma-relation-mode}

[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)確認するには、外部キー制約または Prisma リレーション モードを使用できます。

-   [外部キー](https://docs.pingcap.com/tidb/stable/foreign-key)は、TiDB v6.6.0 からサポートされている実験的機能であり、関連データのテーブル間参照と、データの一貫性を維持するための外部キー制約を可能にします。

    > **警告：**
    >
    > **外部キーは、小規模および中規模のデータ シナリオに適しています。**大規模なデータ ボリュームで外部キーを使用すると、重大なパフォーマンスの問題が発生し、システムに予期しない影響が生じる可能性があります。外部キーを使用する予定の場合は、まず徹底的な検証を実施し、慎重に使用してください。

-   [プリズマ関係モード](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode) 、Prisma クライアント側での参照整合性のエミュレーションです。ただし、参照整合性を維持するために追加のデータベース クエリが必要になるため、パフォーマンスに影響があることに注意してください。

## 次のステップ {#next-steps}

-   ORM フレームワーク Prisma ドライバーの使用方法を[Prismaのドキュメント](https://www.prisma.io/docs)から詳しく学びます。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>

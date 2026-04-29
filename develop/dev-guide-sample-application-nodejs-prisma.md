---
title: Connect to TiDB with Prisma
summary: Prismaを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、Prismaを使用してTiDBと連携するNode.jsのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-nodejs-prisma/','/ja/tidb/dev/dev-guide-sample-application-nodejs-prisma/','/ja/tidbcloud/dev-guide-sample-application-nodejs-prisma/']
---

# Prismaを使用してTiDBに接続する {#connect-to-tidb-with-prisma}

TiDB は MySQL 互換データベースであり、[プリズマ](https://github.com/prisma/prisma)Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDBとPrismaを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   Prismaを使用してTiDBに接続します。
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
git clone https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart.git
cd tidb-nodejs-prisma-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `prisma`を含む）をインストールするには、次のコマンドを実行してください。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールします</b></summary>

既存のプロジェクトの場合、以下のコマンドを実行してパッケージをインストールしてください。

```shell
npm install prisma typescript ts-node @types/node --save-dev
```

</details>

### ステップ3：接続パラメータを指定する {#step-3-provide-connection-parameters}

選択したTiDBのデプロイオプションに応じて、TiDBに接続してください。

<SimpleTab>
<div label="TiDB Cloud Starter or Essential">

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud StarterまたはEssentialインスタンスの名前をクリックして、概要ページに移動します。

2.  右上隅の**「接続」**をクリックしてください。接続ダイアログが表示されます。

3.  接続ダイアログの設定がご使用のオペレーティング環境と一致していることを確認してください。

    -   **接続タイプ**は`Public`に設定されています。
    -   **ブランチ**は`main`に設定されています。
    -   **「接続」は**`Prisma`に設定されています。
    -   **オペレーティングシステムは、**アプリケーションを実行するオペレーティングシステムと一致します。

4.  まだパスワードを設定していない場合は、 **「パスワードを生成」**をクリックしてランダムなパスワードを生成してください。

5.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

6.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続文字列に置き換えます。

    ```dotenv
    DATABASE_URL='{connection_string}'
    ```

    > **注記**
    >
    > TiDB Cloud Starterの場合、パブリックエンドポイントを使用する際には`sslaccept=strict`を設定して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

8.  `prisma/schema.prisma`で、 `mysql`を接続プロバイダとして、 `env("DATABASE_URL")`接続 URL として設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

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

8.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

9.  `.env`ファイルを保存します。

10. `prisma/schema.prisma`で、 `mysql`を接続プロバイダとして、 `env("DATABASE_URL")`接続 URL として設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

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

5.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、接続ダイアログで対応するプレースホルダー`{}`接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test?sslaccept=strict&sslcert={downloaded_ssl_ca_path}'
    ```

    > **注記**
    >
    > TiDB Cloud Starterの場合、パブリックエンドポイントを使用する際には`sslaccept=strict`を設定して TLS 接続を有効にすることをお**勧め****します**。 `sslaccept=strict`を設定して TLS 接続を有効にする場合は、 `sslcert=/path/to/ca.pem`を介して接続ダイアログからダウンロードした CA 証明書のファイルパスを指定する必要があります。

6.  `.env`ファイルを保存します。

7.  `prisma/schema.prisma`で、 `mysql`を接続プロバイダとして、 `env("DATABASE_URL")`接続 URL として設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数`DATABASE_URL`次のように設定し、対応するプレースホルダー`{}` TiDB の接続パラメータに置き換えます。

    ```dotenv
    DATABASE_URL='mysql://{user}:{password}@{host}:4000/test'
    ```

    TiDBをローカルで実行している場合、デフォルトのホストアドレスは`127.0.0.1`で、パスワードは空です。

3.  `.env`ファイルを保存します。

4.  `prisma/schema.prisma`で、 `mysql`を接続プロバイダとして、 `env("DATABASE_URL")`接続 URL として設定します。

    ```prisma
    datasource db {
      provider = "mysql"
      url      = env("DATABASE_URL")
    }
    ```

</div>
</SimpleTab>

### ステップ4．データベーススキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して[プリズマ・マイグレート](https://www.prisma.io/docs/concepts/components/prisma-migrate)を呼び出し、 `prisma/prisma.schema`で定義されたデータ モデルでデータベースを初期化します。

```shell
npx prisma migrate dev
```

**`prisma.schema`で定義されたデータモデル：**

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

Prisma でデータ モデルを定義する方法については、データモデル[データモデル](https://www.prisma.io/docs/concepts/components/prisma-schema/data-model)ドキュメントを確認してください。

**期待される実行出力:**

    Your database is now in sync with your schema.

    ✔ Generated Prisma Client (5.1.1 | library) to ./node_modules/@prisma/client in 54ms

このコマンドは`prisma/prisma.schema`に基づいて TiDB データベースにアクセスするための[Prismaクライアント](https://www.prisma.io/docs/concepts/components/prisma-client)も生成します。

### ステップ5：コードを実行する {#step-5-run-the-code}

サンプルコードを実行するには、以下のコマンドを実行してください。

```shell
npm start
```

**サンプルコードの主なロジック：**

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

接続が成功すると、ターミナルには次のようにTiDBのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.4)
    🆕 Created a new player with ID 1.
    ℹ️ Got Player 1: Player { id: 1, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 1, now player 1 has 150 coins and 150 goods.
    🚮 Player 1 has been deleted.

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-nodejs-prisma-quickstart](https://github.com/tidb-samples/tidb-nodejs-prisma-quickstart)リポジトリを参照してください。

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`Player`フィールドを含む、作成された`id`オブジェクトを返します。

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

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、単一の`Player`オブジェクトを返します。このオブジェクトは、レコードが見つからない場合は、ID `101`または`null`となります。

```javascript
const player: Player | null = prisma.player.findUnique({
   where: {
      id: 101,
   }
});
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

以下のクエリは、 `50`の ID を持つ`50`に`Player`コインと`101`の商品を追加します。

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

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、IDが`Player`である`101` }を削除します。

```javascript
await prisma.player.delete({
   where: {
      id: 101,
   }
});
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

## 役立つメモ {#useful-notes}

### 外部キー制約とPrismaリレーションモードの比較 {#foreign-key-constraints-vs-prisma-relation-mode}

[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity?useskin=vector)をチェックするには、外部キー制約または Prisma リレーション モードを使用できます。

-   [外部キー](https://docs.pingcap.com/tidb/stable/foreign-key)、TiDB v6.6.0 以降でサポートされている機能であり、v8.5.0 以降で一般的に利用可能です。外部キーを使用すると、関連データのテーブル間参照が可能になり、外部キー制約によって関連データの一貫性が確保されます。

    > **警告：**
    >
    > **外部キーは、小規模から中規模のデータ量を扱う場合に適しています。**大規模なデータ量で外部キーを使用すると、深刻なパフォーマンス問題が発生したり、システムに予期せぬ影響を及ぼしたりする可能性があります。外部キーを使用する場合は、事前に徹底的な検証を行い、慎重に使用してください。

-   [プリズマ関係モード](https://www.prisma.io/docs/concepts/components/prisma-schema/relations/relation-mode)Prisma クライアント側の参照整合性のエミュレーションです。ただし、参照整合性を維持するために追加のデータベース クエリが必要になるため、パフォーマンスに影響があることに注意してください。

## 次のステップ {#next-steps}

-   ORM フレームワーク Prisma ドライバーの使用方法の詳細については[Prismaのドキュメント](https://www.prisma.io/docs)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)、SQL [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)などの章を読んで、TiDB アプリケーション開発のベスト プラクティスを学びましょう。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

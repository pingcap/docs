---
title: Connect to TiDB with TypeORM
summary: TypeORM を使用して TiDB に接続する方法を学びます。このチュートリアルでは、TypeORM を使用して TiDB で動作する Node.js サンプル コード スニペットを紹介します。
---

# TypeORM で TiDB に接続する {#connect-to-tidb-with-typeorm}

TiDB は MySQL 互換のデータベースであり、 [タイプORM](https://github.com/TypeORM/TypeORM) Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDB と TypeORM を使用して次のタスクを実行する方法を学習します。

-   環境を設定します。
-   TypeORM を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)見つけることができます。

> **注記**
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
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### ステップ2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `typeorm`と`mysql2`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

-   `typeorm` : Node.js 用の ORM フレームワーク。
-   `mysql2` : Node.js 用の MySQL ドライバー。2 `mysql`も使用できます。
-   `dotenv` : `.env`ファイルから環境変数を読み込みます。
-   `typescript` : TypeScript コードを JavaScript にコンパイルします。
-   `ts-node` : コンパイルせずに TypeScript コードを直接実行します。
-   `@types/node` : Node.js 用の TypeScript 型定義を提供します。

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
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
    > TiDB Cloud Serverless の場合、パブリック エンドポイントを使用するときは、 `TIDB_ENABLE_SSL`経由で TLS 接続を有効にする**必要があります**。

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
    > TiDB Cloud Dedicated の場合、パブリックエンドポイントを使用する場合は、 `TIDB_ENABLE_SSL`経由で TLS 接続を有効にすることを**お勧めします**。 `TIDB_ENABLE_SSL=true`設定する場合は、 `TIDB_CA_PATH=/path/to/ca.pem`経由で接続ダイアログからダウンロードした CA 証明書のパスを指定する**必要があります**。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed">

1.  次のコマンドを実行して`.env.example`コピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数を次のように設定し、対応するプレースホルダー`{}` TiDB クラスターの接続パラメータに置き換えます。

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

### ステップ4: データベーススキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して TypeORM CLI を起動し、 `src/migrations`フォルダー内の移行ファイルに記述された SQL ステートメントを使用してデータベースを初期化します。

```shell
npm run migration:run
```

<details><summary><b>期待される実行出力</b></summary>

次の SQL ステートメントは、テーブル`players`とテーブル`profiles`を作成し、2 つのテーブルは外部キーを通じて関連付けられます。

```sql
query: SELECT VERSION() AS `version`
query: SELECT * FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA` = 'test' AND `TABLE_NAME` = 'migrations'
query: CREATE TABLE `migrations` (`id` int NOT NULL AUTO_INCREMENT, `timestamp` bigint NOT NULL, `name` varchar(255) NOT NULL, PRIMARY KEY (`id`)) ENGINE=InnoDB
query: SELECT * FROM `test`.`migrations` `migrations` ORDER BY `id` DESC
0 migrations are already loaded in the database.
1 migrations were found in the source code.
1 migrations are new migrations must be executed.
query: START TRANSACTION
query: CREATE TABLE `profiles` (`player_id` int NOT NULL, `biography` text NOT NULL, PRIMARY KEY (`player_id`)) ENGINE=InnoDB
query: CREATE TABLE `players` (`id` int NOT NULL AUTO_INCREMENT, `name` varchar(50) NOT NULL, `coins` decimal NOT NULL, `goods` int NOT NULL, `created_at` datetime NOT NULL, `profilePlayerId` int NULL, UNIQUE INDEX `uk_players_on_name` (`name`), UNIQUE INDEX `REL_b9666644b90ccc5065993425ef` (`profilePlayerId`), PRIMARY KEY (`id`)) ENGINE=InnoDB
query: ALTER TABLE `players` ADD CONSTRAINT `fk_profiles_on_player_id` FOREIGN KEY (`profilePlayerId`) REFERENCES `profiles`(`player_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
query: INSERT INTO `test`.`migrations`(`timestamp`, `name`) VALUES (?, ?) -- PARAMETERS: [1693814724825,"Init1693814724825"]
Migration Init1693814724825 has been  executed successfully.
query: COMMIT
```

</details>

移行ファイルは、 `src/entities`フォルダーで定義されたエンティティから生成されます。TypeORM でエンティティを定義する方法については、 [タイプORM: エンティティ](https://typeorm.io/entities)を参照してください。

### ステップ5: コードを実行して結果を確認する {#step-5-run-the-code-and-check-the-result}

サンプル コードを実行するには、次のコマンドを実行します。

```shell
npm start
```

**予想される実行出力:**

接続が成功すると、ターミナルは次のように TiDB クラスターのバージョンを出力します。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.0)
    🆕 Created a new player with ID 2.
    ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了することができます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-typeorm-クイックスタート](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart)リポジトリを参照してください。

### 接続オプションで接続する {#connect-with-connection-options}

次のコードは、環境変数で定義されたオプションを使用して TiDB への接続を確立します。

```typescript
// src/dataSource.ts

// Load environment variables from .env file to process.env.
require('dotenv').config();

export const AppDataSource = new DataSource({
  type: "mysql",
  host: process.env.TIDB_HOST || '127.0.0.1',
  port: process.env.TIDB_PORT ? Number(process.env.TIDB_PORT) : 4000,
  username: process.env.TIDB_USER || 'root',
  password: process.env.TIDB_PASSWORD || '',
  database: process.env.TIDB_DATABASE || 'test',
  ssl: process.env.TIDB_ENABLE_SSL === 'true' ? {
    minVersion: 'TLSv1.2',
    ca: process.env.TIDB_CA_PATH ? fs.readFileSync(process.env.TIDB_CA_PATH) : undefined
  } : null,
  synchronize: process.env.NODE_ENV === 'development',
  logging: false,
  entities: [Player, Profile],
  migrations: [__dirname + "/migrations/**/*{.ts,.js}"],
});
```

> **注記**
>
> TiDB Cloud Serverless の場合、パブリックエンドポイントを使用するときは TLS 接続を有効にする必要があります。このサンプルコードでは、 `.env`ファイルの環境変数`TIDB_ENABLE_SSL` `true`に設定してください。
>
> ただし、Node.js はデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)使用し、これはTiDB Cloud Serverless によって信頼されているため、 `TIDB_CA_PATH`で SSL CA 証明書を指定する必要は**ありません**。

### データを挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`id`フィールドを含む作成された`Player`オブジェクトを返します。

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

詳細については[データを挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID 101 の単一のオブジェクト`Player`を返します。レコードが見つからない場合は`null`返します。

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

詳細については[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは、ID `101`の商品`Player`に商品`50`を追加します。

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

詳細については[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

次のクエリは、ID `101`の`Player`削除します。

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

詳細については[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

### 生のSQLクエリを実行する {#execute-raw-sql-queries}

次のクエリは生のSQL文（ `SELECT VERSION() AS tidb_version;` ）を実行し、TiDBクラスタのバージョンを返します。

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

詳細については[タイプORM: データソースAPI](https://typeorm.io/data-source-api)を参照してください。

## 役に立つメモ {#useful-notes}

### 外部キー制約 {#foreign-key-constraints}

[外部キー制約](https://docs.pingcap.com/tidb/stable/foreign-key)使用すると、データベース側でチェックを追加することで、データの[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)保証されます。ただし、大量のデータを扱うシナリオでは、重大なパフォーマンスの問題が発生する可能性があります。

`createForeignKeyConstraints`オプション (デフォルト値は`true` ) を使用して、エンティティ間のリレーションシップを構築するときに外部キー制約を作成するかどうかを制御できます。

```typescript
@Entity()
export class ActionLog {
    @PrimaryColumn()
    id: number

    @ManyToOne((type) => Person, {
        createForeignKeyConstraints: false,
    })
    person: Person
}
```

詳細については、 [TypeORMFAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation)および[外部キー制約](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints)を参照してください。

## 次のステップ {#next-steps}

-   TypeORM の詳しい使い方については、 [TypeORMのドキュメント](https://typeorm.io/)をご覧ください。
-   [開発者ガイド](/develop/dev-guide-overview.md)の[データを挿入](/develop/dev-guide-insert-data.md) 、 [データの更新](/develop/dev-guide-update-data.md) 、 [データを削除する](/develop/dev-guide-delete-data.md) 、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md) 、 [取引](/develop/dev-guide-transaction-overview.md) 、 [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md)などの章で、 TiDB アプリケーション開発のベスト プラクティスを学習します。
-   プロフェッショナル[TiDB 開発者コース](https://www.pingcap.com/education/)を通じて学び、試験に合格すると[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

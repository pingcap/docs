---
title: Connect to TiDB with TypeORM
summary: Learn how to connect to TiDB using TypeORM. This tutorial gives Node.js sample code snippets that work with TiDB using TypeORM.
---

# TypeORM で TiDB に接続する {#connect-to-tidb-with-typeorm}

TiDB は MySQL 互換データベースであり、 [TypeORM](https://github.com/TypeORM/TypeORM)は Node.js 用の人気のあるオープンソース ORM フレームワークです。

このチュートリアルでは、TiDB と TypeORM を使用して次のタスクを実行する方法を学習できます。

-   環境をセットアップします。
-   TypeORM を使用して TiDB クラスターに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記**
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
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### ステップ 2: 依存関係をインストールする {#step-2-install-dependencies}

次のコマンドを実行して、サンプル アプリに必要なパッケージ ( `typeorm`と`mysql2`を含む) をインストールします。

```shell
npm install
```

<details><summary><b>依存関係を既存のプロジェクトにインストールする</b></summary>

既存のプロジェクトの場合は、次のコマンドを実行してパッケージをインストールします。

-   `typeorm` : Node.js の ORM フレームワーク。
-   `mysql2` : Node.js 用の MySQL ドライバー。 `mysql`ドライバーも使えます。
-   `dotenv` : `.env`ファイルから環境変数をロードします。
-   `typescript` : TypeScript コードを JavaScript にコンパイルします。
-   `ts-node` : TypeScript コードをコンパイルせずに直接実行します。
-   `@types/node` : Node.js の TypeScript 型定義を提供します。

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
```

</details>

### ステップ 3: 接続情報を構成する {#step-3-configure-connection-information}

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

6.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

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
    > TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は`TIDB_ENABLE_SSL`経由の TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

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

5.  `.env`ファイルを編集し、次のように環境変数を設定し、接続ダイアログ上の対応するプレースホルダー`{}`接続パラメーターに置き換えます。

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
    > TiDB D dedicated の場合、パブリック エンドポイントを使用する場合は`TIDB_ENABLE_SSL`経由の TLS 接続を有効にすることが**推奨され**ます。 `TIDB_ENABLE_SSL=true`を設定する場合は、 `TIDB_CA_PATH=/path/to/ca.pem`を介して接続ダイアログからダウンロードした CA 証明書のパスを指定する**必要があります**。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Hosted">

1.  次のコマンドを実行して`.env.example`をコピーし、名前を`.env`に変更します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、次のように環境変数を設定し、対応するプレースホルダー`{}` TiDB クラスターの接続パラメーターに置き換えます。

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

### ステップ 4: データベース スキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して TypeORM CLI を呼び出し、 `src/migrations`フォルダー内の移行ファイルに書き込まれた SQL ステートメントでデータベースを初期化します。

```shell
npm run migration:run
```

<details><summary><b>予想される実行出力</b></summary>

次の SQL ステートメントは`players`テーブルと`profiles`テーブルを作成し、2 つのテーブルは外部キーを介して関連付けられます。

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

移行ファイルは、 `src/entities`フォルダーで定義されたエンティティから生成されます。 TypeORM でエンティティを定義する方法については、 [TypeORM: エンティティ](https://typeorm.io/entities)を参照してください。

### ステップ 5: コードを実行して結果を確認する {#step-5-run-the-code-and-check-the-result}

次のコマンドを実行してサンプル コードを実行します。

```shell
npm start
```

**予想される実行出力:**

接続が成功すると、ターミナルは次のように TiDB クラスターのバージョンを出力します。

    🔌 Connected to TiDB cluster! (TiDB version: 5.7.25-TiDB-v7.1.0)
    🆕 Created a new player with ID 2.
    ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

次のサンプル コード スニペットを参照して、独自のアプリケーション開発を完了できます。

完全なサンプル コードとその実行方法については、 [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart)リポジトリを確認してください。

### 接続オプションを使用して接続する {#connect-with-connection-options}

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
> TiDB サーバーレスの場合、パブリック エンドポイントを使用する場合は TLS 接続を有効にする必要があります。このサンプルコードでは、 `.env`ファイルの環境変数`TIDB_ENABLE_SSL` `true`に設定してください。
>
> ただし、Node.js はデフォルトで組み込みの[Mozilla CA 証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用し、TiDB Serverless によって信頼されるため、 `TIDB_CA_PATH`経由で SSL CA 証明書を指定する必要は**ありません**。

### データの挿入 {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`id`フィールドを含む、作成された`Player`オブジェクトを返します。

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

詳細については、 [データの挿入](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、ID 101 の単一の`Player`オブジェクトを返します。レコードが見つからない場合は`null`返します。

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データを更新する {#update-data}

次のクエリは、ID `101`の商品`Player`に商品`50`を追加します。

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

詳細については、 [データを更新する](/develop/dev-guide-update-data.md)を参照してください。

### データの削除 {#delete-data}

次のクエリは、ID `101`の`Player`削除します。

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

詳細については、 [データの削除](/develop/dev-guide-delete-data.md)を参照してください。

### 生のSQLクエリを実行する {#execute-raw-sql-queries}

次のクエリは、生の SQL ステートメント ( `SELECT VERSION() AS tidb_version;` ) を実行し、TiDB クラスターのバージョンを返します。

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

詳細については、 [TypeORM: データソース API](https://typeorm.io/data-source-api)を参照してください。

## 便利なメモ {#useful-notes}

### 外部キー制約 {#foreign-key-constraints}

外部キー制約を使用すると、データベース側でチェックを追加することでデータの[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)が保証されます。ただし、これにより、データ量が大きいシナリオでは、パフォーマンスに重大な問題が発生する可能性があります。

`createForeignKeyConstraints`オプション (デフォルト値は`true` ) を使用して、エンティティ間の関係を構築するときに外部キー制約を作成するかどうかを制御できます。

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

-   TypeORM の詳しい使い方は[TypeORM のドキュメント](https://typeorm.io/)からご覧ください。
-   [開発者ガイド](/develop/dev-guide-overview.md)の章 ( [データの挿入](/develop/dev-guide-insert-data.md) [SQLパフォーマンスの最適化](/develop/dev-guide-optimize-sql-overview.md) ) で TiDB [トランザクション](/develop/dev-guide-transaction-overview.md)開発[データを更新する](/develop/dev-guide-update-data.md)ベスト プラクティス[データの削除](/develop/dev-guide-delete-data.md)学習[クエリデータ](/develop/dev-guide-get-data-from-single-table.md)ます。
-   プロフェッショナルとして[TiDB 開発者コース](https://www.pingcap.com/education/)を学び、試験合格後に[TiDB 認定](https://www.pingcap.com/education/certification/)獲得します。

## 助けが必要？ {#need-help}

[不和](https://discord.gg/vYU9h56kAX)または[サポートチケットを作成する](https://support.pingcap.com/)について質問してください。

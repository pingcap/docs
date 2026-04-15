---
title: Connect to TiDB with TypeORM
summary: TypeORMを使用してTiDBに接続する方法を学びましょう。このチュートリアルでは、TypeORMを使用してTiDBと連携するNode.jsのサンプルコードを紹介します。
aliases: ['/ja/tidb/stable/dev-guide-sample-application-nodejs-typeorm/','/ja/tidb/dev/dev-guide-sample-application-nodejs-typeorm/','/ja/tidbcloud/dev-guide-sample-application-nodejs-typeorm/']
---

# TypeORMを使用してTiDBに接続する {#connect-to-tidb-with-typeorm}

TiDBはMySQL互換のデータベースであり、 [TypeORM](https://github.com/TypeORM/TypeORM)はNode.js向けの人気の高いオープンソースのORMフレームワークです。

このチュートリアルでは、TiDBとTypeORMを使用して以下のタスクを実行する方法を学ぶことができます。

-   環境をセットアップしてください。
-   TypeORMを使用してTiDBに接続します。
-   アプリケーションをビルドして実行します。オプションで、基本的な CRUD 操作用の[サンプルコードスニペット](#sample-code-snippets)を見つけることができます。

> **注記**
>
> このチュートリアルは、 TiDB Cloud Starter、 TiDB Cloud Essential、 TiDB Cloud Dedicated、およびTiDB Self-Managedに対応しています。

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
git clone https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart.git
cd tidb-nodejs-typeorm-quickstart
```

### ステップ2：依存関係をインストールする {#step-2-install-dependencies}

サンプルアプリに必要なパッケージ（ `typeorm`および`mysql2`を含む）をインストールするには、次のコマンドを実行します。

```shell
npm install
```

<details><summary><b>既存のプロジェクトに依存関係をインストールする</b></summary>

既存のプロジェクトの場合、以下のコマンドを実行してパッケージをインストールしてください。

-   `typeorm` : Node.js 用の ORM フレームワーク。
-   `mysql2` : Node.js 用の MySQL ドライバーです`mysql`ドライバーも使用できます。
-   `dotenv` : `.env`ファイルから環境変数を読み込みます。
-   `typescript` : TypeScript コードを JavaScript にコンパイルします。
-   `ts-node` : TypeScript コードをコンパイルせずに直接実行します。
-   `@types/node` : Node.js 用の TypeScript 型定義を提供します。

```shell
npm install typeorm mysql2 dotenv --save
npm install @types/node ts-node typescript --save-dev
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
    > TiDB Cloud StarterおよびTiDB Cloud Essentialの場合、パブリック エンドポイントを使用する際には`TIDB_ENABLE_SSL`を介して TLS 接続を有効にする**必要があります**。

7.  `.env`ファイルを保存します。

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
    > TiDB Cloud Dedicatedの場合、パブリックエンドポイントを使用する際には`TIDB_ENABLE_SSL`を介して TLS 接続を有効にすることをお**勧め**します。 `TIDB_ENABLE_SSL=true`を設定する際には、 `TIDB_CA_PATH=/path/to/ca.pem`を介して接続ダイアログからダウンロードした CA 証明書のパスを指定する**必要があります**。

6.  `.env`ファイルを保存します。

</div>
<div label="TiDB Self-Managed" value="tidb">

1.  `.env.example`をコピーして`.env`に名前を変更するには、次のコマンドを実行します。

    ```shell
    cp .env.example .env
    ```

2.  `.env`ファイルを編集し、環境変数を以下のように設定し、対応するプレースホルダー`{}` TiDB の接続パラメータに置き換えてください。

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

### ステップ4：データベーススキーマを初期化する {#step-4-initialize-the-database-schema}

次のコマンドを実行して TypeORM CLI を起動し、 `src/migrations`フォルダー内の移行ファイルに記述された SQL ステートメントを使用してデータベースを初期化します。

```shell
npm run migration:run
```

<details><summary><b>期待される実行出力</b></summary>

以下の SQL ステートメントは`players`テーブルと`profiles`テーブルを作成し、2 つのテーブルは外部キーによって関連付けられます。

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

移行ファイルは、 `src/entities`フォルダーで定義されたエンティティから生成されます。TypeORM でエンティティを定義する方法については、 [TypeORM: エンティティ](https://typeorm.io/entities)を参照してください。

### ステップ5：コードを実行して結果を確認する {#step-5-run-the-code-and-check-the-result}

サンプルコードを実行するには、以下のコマンドを実行してください。

```shell
npm start
```

**期待される実行出力:**

接続が成功すると、ターミナルには次のようにTiDBのバージョンが出力されます。

    🔌 Connected to TiDB cluster! (TiDB version: 8.0.11-TiDB-v8.5.4)
    🆕 Created a new player with ID 2.
    ℹ️ Got Player 2: Player { id: 2, coins: 100, goods: 100 }
    🔢 Added 50 coins and 50 goods to player 2, now player 2 has 100 coins and 150 goods.
    🚮 Deleted 1 player data.

## サンプルコードスニペット {#sample-code-snippets}

以下のサンプルコードスニペットを参考に、独自のアプリケーション開発を完成させてください。

完全なサンプルコードと実行方法については、 [tidb-samples/tidb-nodejs-typeorm-quickstart](https://github.com/tidb-samples/tidb-nodejs-typeorm-quickstart)リポジトリを参照してください。

### 接続オプションを使用して接続します {#connect-with-connection-options}

以下のコードは、環境変数で定義されたオプションを使用してTiDBへの接続を確立します。

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
> TiDB Cloud StarterおよびTiDB Cloud Essentialでは、パブリックエンドポイントを使用する際に TLS 接続を有効にする必要があります。このサンプルコードでは、 `TIDB_ENABLE_SSL` `.env` } を`true`に設定してください。
>
> ただし、Node.js はデフォルトで組み込みの[Mozilla CA証明書](https://wiki.mozilla.org/CA/Included_Certificates)を使用するため、 `TIDB_CA_PATH`を介して SSL CA 証明書を指定する必要は**ありません**。この証明書はTiDB Cloud StarterおよびTiDB Cloud Essentialによって信頼されています。

### データを挿入する {#insert-data}

次のクエリは、単一の`Player`レコードを作成し、TiDB によって生成された`Player`フィールドを含む、作成された`id`オブジェクトを返します。

```typescript
const player = new Player('Alice', 100, 100);
await this.dataSource.manager.save(player);
```

詳細については、[データを挿入する](/develop/dev-guide-insert-data.md)を参照してください。

### クエリデータ {#query-data}

次のクエリは、IDが101の単一の`Player`オブジェクトを返します。レコードが見つからない場合は`null`オブジェクトを返します。

```typescript
const player: Player | null = await this.dataSource.manager.findOneBy(Player, {
  id: id
});
```

詳細については、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)を参照してください。

### データの更新 {#update-data}

次のクエリは`50`の商品`Player`に`101`を追加します。

```typescript
const player = await this.dataSource.manager.findOneBy(Player, {
  id: 101
});
player.goods += 50;
await this.dataSource.manager.save(player);
```

詳細については、[データの更新](/develop/dev-guide-update-data.md)を参照してください。

### データを削除する {#delete-data}

以下のクエリは、IDが`Player`である`101` }を削除します。

```typescript
await this.dataSource.manager.delete(Player, {
  id: 101
});
```

詳細については、[データを削除する](/develop/dev-guide-delete-data.md)を参照してください。

### 生のSQLクエリを実行する {#execute-raw-sql-queries}

次のクエリは、生のSQLステートメント（ `SELECT VERSION() AS tidb_version;` ）を実行し、TiDBのバージョンを返します。

```typescript
const rows = await dataSource.query('SELECT VERSION() AS tidb_version;');
console.log(rows[0]['tidb_version']);
```

詳細については、 [TypeORM: データソースAPI](https://typeorm.io/data-source-api)を参照してください。

## 役立つメモ {#useful-notes}

### 外部キー制約 {#foreign-key-constraints}

[外部キー制約](https://docs.pingcap.com/tidb/stable/foreign-key)を使用すると、データベース側でチェックを追加することでデータの[参照整合性](https://en.wikipedia.org/wiki/Referential_integrity)が保証されます。ただし、これにより、データ量が大きいシナリオでは重大なパフォーマンスの問題が発生する可能性があります。

`createForeignKeyConstraints`オプションを使用すると、エンティティ間のリレーションシップを構築する際に外部キー制約を作成するかどうかを制御できます (デフォルト値は`true`です)。

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

詳細については、 [TypeORMに関するFAQ](https://typeorm.io/relations-faq#avoid-foreign-key-constraint-creation)および[外部キー制約](https://docs.pingcap.com/tidbcloud/foreign-key#foreign-key-constraints)を参照してください。

## 次のステップ {#next-steps}

-   TypeORM の使用法の詳細については[TypeORMのドキュメント](https://typeorm.io/)参照してください。
-   [開発者ガイド](https://docs.pingcap.com/developer/)[データを挿入する](/develop/dev-guide-insert-data.md)、[データの更新](/develop/dev-guide-update-data.md)、[データを削除する](/develop/dev-guide-delete-data.md)、 [クエリデータ](/develop/dev-guide-get-data-from-single-table.md)、SQL [取引](/develop/dev-guide-transaction-overview.md)[SQLパフォーマンス最適化](/develop/dev-guide-optimize-sql-overview.md)などの章を読んで、TiDB アプリケーション開発のベスト プラクティスを学びましょう。
-   プロフェッショナルな[TiDB開発者向けコース](https://www.pingcap.com/education/)コースを通じて学習し、試験に合格すると[TiDB認定資格](https://www.pingcap.com/education/certification/)を取得します。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

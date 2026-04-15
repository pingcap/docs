---
title: Create a Database
summary: データベースを作成するための手順、ルール、および例を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-create-database/','/ja/tidb/dev/dev-guide-create-database/','/ja/tidbcloud/dev-guide-create-database/']
---

# データベースを作成する {#create-a-database}

このドキュメントでは、SQLと様々なプログラミング言語を使用してデータベースを作成する方法と、データベース作成のルールについて説明します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)を例として、データベース作成の手順を順を追って説明します。

## 始める前に {#before-you-start}

データベースを作成する前に、以下の手順を実行してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)お読みください。

## データベースとは何か {#what-is-database}

TiDB のオブジェクトには[データベース](/develop/dev-guide-schema-design-overview.md)**テーブル**、**ビュー**、**シーケンス**、およびその他のオブジェクトが含まれます。

## データベースを作成する {#create-databases}

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用できます。

例えば、 `bookshop`という名前のデータベースが存在しない場合、それを作成するには、次のステートメントを使用します。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

`CREATE DATABASE`ステートメントの詳細と例については、 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)ドキュメントを参照してください。

`root`ユーザーとしてライブラリビルドステートメントを実行するには、次のコマンドを実行します。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

## データベースをビュー {#view-databases}

データベースを表示するには、 [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)ステートメントを使用します。

例えば：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

以下は出力例です。

    +--------------------+
    | Database           |
    +--------------------+
    | INFORMATION_SCHEMA |
    | PERFORMANCE_SCHEMA |
    | bookshop           |
    | mysql              |
    | test               |
    +--------------------+

## データベース作成におけるルール {#rules-in-database-creation}

-   データベース[データベース命名規則](/develop/dev-guide-object-naming-guidelines.md)に従って、データベースに意味のある名前を付けます。
-   TiDBには`test`という名前のデフォルトデータベースが付属しています。ただし、必要がない限り、本番環境での使用は推奨されません。 `CREATE DATABASE`ステートメントを使用して独自のデータベースを作成し、SQLセッションで[`USE {databasename};`](/sql-statements/sql-statement-use.md)ステートメントを使用して現在のデータベースを変更できます。
-   `root`ユーザーを使用して、データベース、ロール、ユーザーなどのオブジェクトを作成します。ロールとユーザーには、必要な権限のみを付与してください。
-   ベストプラクティスとして、データベーススキーマの変更を実行する際には、ドライバやORMではなく、 **MySQLコマンドラインクライアント**または**MySQL GUIクライアント**を使用することをお勧めします。

## 次のステップ {#next-step}

データベースを作成したら、そこに**テーブル**を追加できます。詳細については、[テーブルを作成する](/develop/dev-guide-create-table.md)参照してください。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

---
title: Create a Database
summary: データベースを作成する手順、ルール、および例を学びます。
---

# データベースを作成する {#create-a-database}

このドキュメントでは、SQLと様々なプログラミング言語を用いてデータベースを作成する方法と、データベース作成のルールを列挙します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例に、データベース作成の手順を順を追って説明します。

## 始める前に {#before-you-start}

データベースを作成する前に、次の操作を行います。

-   [TiDB Cloudサーバーレスクラスタの構築](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)読んでください。

## データベースとは {#what-is-database}

TiDB の[データベース](/develop/dev-guide-schema-design-overview.md)オブジェクトには、**テーブル**、**ビュー**、**シーケンス**、およびその他のオブジェクトが含まれます。

## データベースを作成する {#create-databases}

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用できます。

たとえば、存在しない場合に`bookshop`という名前のデータベースを作成するには、次のステートメントを使用します。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

`CREATE DATABASE`ステートメントの詳細と例については、 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)ドキュメントを参照してください。

ライブラリ ビルド ステートメントを`root`ユーザーとして実行するには、次のコマンドを実行します。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "CREATE DATABASE IF NOT EXISTS bookshop;"
```

## データベースをビュー {#view-databases}

クラスター内のデータベースを表示するには、 [`SHOW DATABASES`](/sql-statements/sql-statement-show-databases.md)ステートメントを使用します。

例えば：

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    -e "SHOW DATABASES;"
```

出力例は次のとおりです。

    +--------------------+
    | Database           |
    +--------------------+
    | INFORMATION_SCHEMA |
    | PERFORMANCE_SCHEMA |
    | bookshop           |
    | mysql              |
    | test               |
    +--------------------+

## データベース作成のルール {#rules-in-database-creation}

-   [データベースの命名規則](/develop/dev-guide-object-naming-guidelines.md)に従って、データベースに意味のある名前を付けます。
-   TiDBには、 `test`というデフォルトのデータベースが付属しています。ただし、必要がない限り、本番環境での使用は推奨されません。SQLセッションで`CREATE DATABASE`ステートメントを使用して独自のデータベースを作成し、 [`USE {databasename};`](/sql-statements/sql-statement-use.md)ステートメントを使用して現在のデータベースを変更できます。
-   `root`ユーザーを使用して、データベース、ロール、ユーザーなどのオブジェクトを作成します。ロールとユーザーには必要な権限のみを付与します。
-   ベスト プラクティスとして、データベース スキーマの変更を実行するには、ドライバーまたは ORM ではなく**、MySQL コマンドライン クライアント**または**MySQL GUI クライアント**を使用することをお勧めします。

## 次のステップ {#next-step}

データベースを作成したら、**テーブル**を追加できます。詳細については、 [テーブルを作成する](/develop/dev-guide-create-table.md)参照してください。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、あるいは[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

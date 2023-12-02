---
title: Create a Database
summary: Learn steps, rules, and examples to create a database.
---

# データベースを作成する {#create-a-database}

このドキュメントでは、SQL およびさまざまなプログラミング言語を使用してデータベースを作成する方法を説明し、データベース作成のルールを示します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、データベース作成の手順を説明します。

## 始める前に {#before-you-start}

データベースを作成する前に、次の手順を実行します。

-   [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読みます。

## データベースとは {#what-is-database}

TiDB のオブジェクトには[データベース](/develop/dev-guide-schema-design-overview.md)**テーブル**、**ビュー**、**シーケンス**、およびその他のオブジェクトが含まれます。

## データベースの作成 {#create-databases}

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用できます。

たとえば、 `bookshop`という名前のデータベースが存在しない場合にそれを作成するには、次のステートメントを使用します。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

`CREATE DATABASE`ステートメントの詳細と例については、 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)ドキュメントを参照してください。

ライブラリのビルド ステートメントを`root`ユーザーとして実行するには、次のコマンドを実行します。

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

## データベース作成時のルール {#rules-in-database-creation}

-   [データベースの命名規則](/develop/dev-guide-object-naming-guidelines.md)に従って、データベースに意味のある名前を付けます。
-   TiDB には、 `test`という名前のデフォルトのデータベースが付属しています。ただし、必要がない場合は、本番環境で使用することはお勧めできません。 SQL セッションで`CREATE DATABASE`ステートメントを使用して独自のデータベースを作成し、 [`USE {databasename};`](/sql-statements/sql-statement-use.md)ステートメントを使用して現在のデータベースを変更できます。
-   `root`ユーザーを使用して、データベース、ロール、ユーザーなどのオブジェクトを作成します。必要な権限のみをロールとユーザーに付与します。
-   ベスト プラクティスとして、データベース スキーマの変更を実行するには、ドライバーまたは ORM の代わりに**MySQL コマンドライン クライアント**または**MySQL GUI クライアント**を使用することをお勧めします。

## 次のステップ {#next-step}

データベースを作成したら、そこに**テーブル**を追加できます。詳細については、 [テーブルを作成する](/develop/dev-guide-create-table.md)を参照してください。

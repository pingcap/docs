---
title: Create a Database
summary: Learn steps, rules, and examples to create a database.
---

# データベースを作成する {#create-a-database}

このドキュメントでは、SQL とさまざまなプログラミング言語を使用してデータベースを作成する方法について説明し、データベース作成のルールを一覧表示します。このドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションを例として、データベース作成の手順を説明します。

## 始める前に {#before-you-start}

データベースを作成する前に、次のことを行います。

-   [TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) .
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読んでください。

## データベースとは {#what-is-database}

TiDB の[データベース](/develop/dev-guide-schema-design-overview.md)のオブジェクトには、**テーブル**、<strong>ビュー</strong>、<strong>シーケンス</strong>、およびその他のオブジェクトが含まれています。

## データベースを作成する {#create-databases}

データベースを作成するには、 `CREATE DATABASE`ステートメントを使用できます。

たとえば、存在しない場合に`bookshop`という名前のデータベースを作成するには、次のステートメントを使用します。

```sql
CREATE DATABASE IF NOT EXISTS `bookshop`;
```

`CREATE DATABASE`ステートメントの詳細と例については、 [`CREATE DATABASE`](/sql-statements/sql-statement-create-database.md)ドキュメントを参照してください。

`root`人のユーザーとしてライブラリ ビルド ステートメントを実行するには、次のコマンドを実行します。

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

次に出力例を示します。

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| bookshop           |
| mysql              |
| test               |
+--------------------+
```

## データベース作成時のルール {#rules-in-database-creation}

-   [データベースの命名規則](/develop/dev-guide-object-naming-guidelines.md)に従って、データベースに意味のある名前を付けます。
-   TiDB には`test`という名前のデフォルト データベースが付属しています。ただし、必要がなければ本番環境で使用することはお勧めしません。 `CREATE DATABASE`ステートメントを使用して独自のデータベースを作成し、SQL セッションで[`USE {databasename};`](/sql-statements/sql-statement-use.md)ステートメントを使用して現在のデータベースを変更できます。
-   `root`ユーザーを使用して、データベース、ロール、およびユーザーなどのオブジェクトを作成します。ロールとユーザーには必要な権限のみを付与してください。
-   ベスト プラクティスとして、ドライバーや ORM の代わりに**MySQL コマンドライン クライアント**または<strong>MySQL GUI クライアント</strong>を使用してデータベース スキーマの変更を実行することをお勧めします。

## 次のステップ {#next-step}

データベースを作成したら、それに**テーブル**を追加できます。詳細については、 [テーブルを作成する](/develop/dev-guide-create-table.md)を参照してください。

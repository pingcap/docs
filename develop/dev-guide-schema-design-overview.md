---
title: TiDB Database Schema Design Overview
summary: Learn the basics on TiDB database schema design.
---

# TiDB データベース スキーマ設計の概要 {#tidb-database-schema-design-overview}

このドキュメントでは、TiDB のオブジェクト、アクセス制御、データベース スキーマの変更、オブジェクトの制限など、TiDB データベース スキーマ設計の基本について説明します。

以降のドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)例として、データベースを設計し、データベース内でデータの読み取りおよび書き込み操作を実行する方法を示します。

## TiDB のオブジェクト {#objects-in-tidb}

いくつかの一般的な用語を区別するために、TiDB で使用される用語に関する簡単な合意を以下に示します。

-   一般用語[データベース](https://en.wikipedia.org/wiki/Database)との混同を避けるため、このドキュメントでは**データベースは**論理オブジェクトを指し、 **TiDB**は TiDB 自体を指し、**クラスターは**TiDB のデプロイされたインスタンスを指します。

-   TiDB は MySQL 互換の構文を使用します。この**構文**では、スキーマとはデータベース内の論理オブジェクトの代わりに一般的な用語[スキーマ](https://en.wiktionary.org/wiki/schema)を意味します。詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)を参照してください。スキーマを論理オブジェクトとして持つデータベース ( [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html) 、 [オラクル](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html) 、 [Microsoft SQLサーバー](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15)など) から移行する場合は、この違いに必ず注意してください。

### データベース {#database}

TiDB のデータベースは、テーブルやインデックスなどのオブジェクトのコレクションです。

TiDB には、 `test`という名前のデフォルトのデータベースが付属しています。ただし、 `test`データベースを使用する代わりに、独自のデータベースを作成することをお勧めします。

### テーブル {#table}

テーブルは、関連するデータを[データベース](#database)にまとめたものです。

各テーブルは**行**と**列**で構成されます。行内の各値は特定の**列**に属します。各列では 1 つのデータ型のみが許可されます。列をさらに修飾するには、 [制約](/constraints.md)を追加します。計算を高速化するには、 [生成された列](/generated-columns.md)を追加します。

### 索引 {#index}

インデックスは、テーブル内で選択された列のコピーです。 [テーブル](#table)の 1 つ以上の列を使用してインデックスを作成できます。インデックスを使用すると、TiDB はテーブル内のすべての行を毎回検索する必要がなく、データをすばやく見つけることができるため、クエリのパフォーマンスが大幅に向上します。

インデックスには一般的に 2 つのタイプがあります。

-   **主キー**: 主キー列のインデックス。
-   **セカンダリ インデックス**: 非主キー列のインデックス。

> **注記：**
>
> TiDB では、**主キー**のデフォルトの定義が[InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) (MySQL の共通storageエンジン) とは異なります。
>
> -   InnoDB では、**主キー**の定義は一意であり、null ではなく、**クラスター化インデックス**です。
> -   TiDB では、**主キー**の定義は一意であり、null ではありません。ただし、主キーが**クラスター化インデックス**であるとは保証されません。主キーがクラスター化インデックスであるかどうかを指定するには、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に非予約キーワード`CLUSTERED`または`NONCLUSTERED`を追加します。ステートメントでこれらのキーワードが明示的に指定されていない場合、デフォルトの動作はシステム変数`@@global.tidb_enable_clustered_index`によって制御されます。詳細については、 [クラスター化インデックス](/clustered-indexes.md)参照してください。

#### 特殊なインデックス {#specialized-indexes}

<CustomContent platform="tidb">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB はいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、 [インデックス作成と制約](/basic-features.md#indexing-and-constraints)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB はいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、 [インデックス作成と制約](https://docs.pingcap.com/tidb/stable/basic-features#indexing-and-constraints)を参照してください。

</CustomContent>

### その他のサポートされている論理オブジェクト {#other-supported-logical-objects}

TiDB は、 **table**と同じレベルで次の論理オブジェクトをサポートします。

-   [ビュー](/views.md) : ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。
-   [シーケンス](/sql-statements/sql-statement-create-sequence.md) : シーケンスはシーケンシャルデータを生成して保存します。
-   [一時テーブル](/temporary-tables.md) : データが永続的ではないテーブル。

## アクセス制御 {#access-control}

<CustomContent platform="tidb">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートします。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](/privilege-management.md) ～ [ユーザー](/user-account-management.md)直接ユーザーに付与するか、ユーザーに[権限](/privilege-management.md) ～ [役割](/role-based-access-control.md)を付与します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートします。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](https://docs.pingcap.com/tidb/stable/privilege-management) ～ [ユーザー](https://docs.pingcap.com/tidb/stable/user-account-management)直接ユーザーに付与するか、ユーザーに[権限](https://docs.pingcap.com/tidb/stable/privilege-management) ～ [役割](https://docs.pingcap.com/tidb/stable/role-based-access-control)を付与します。

</CustomContent>

## データベーススキーマの変更 {#database-schema-changes}

ベスト プラクティスとして、データベース スキーマの変更を実行するには、ドライバーまたは ORM の代わりに[MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または GUI クライアントを使用することをお勧めします。

## オブジェクトの制限 {#object-limitations}

詳細については、 [TiDB の制限事項](/tidb-limitations.md)を参照してください。

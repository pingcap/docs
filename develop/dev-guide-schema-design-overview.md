---
title: TiDB Database Schema Design Overview
summary: Learn the basics on TiDB database schema design.
---

# TiDB データベース スキーマ設計の概要 {#tidb-database-schema-design-overview}

このドキュメントでは、TiDB のオブジェクト、アクセス制御、データベース スキーマの変更、オブジェクトの制限など、TiDB データベース スキーマ設計の基本について説明します。

以降のドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)例として、データベースを設計し、データベースでデータの読み取りおよび書き込み操作を実行する方法を示します。

## TiDB のオブジェクト {#objects-in-tidb}

いくつかの一般的な用語を区別するために、TiDB で使用される用語について簡単に説明します。

-   一般的な用語[データベース](https://en.wikipedia.org/wiki/Database)との混同を避けるために、このドキュメントの**データベースは**論理オブジェクトを指し、 <strong>TiDB</strong>は TiDB 自体を指し、<strong>クラスターは</strong>TiDB のデプロイされたインスタンスを指します。

-   TiDB は MySQL 互換の構文を使用します。この**構文**では、スキーマはデータベース内の論理オブジェクトではなく、一般的な用語[スキーマ](https://en.wiktionary.org/wiki/schema)を意味します。詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)を参照してください。論理オブジェクトとしてスキーマを持つデータベース (たとえば、 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html) 、 [オラクル](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html) 、および[マイクロソフト SQL サーバー](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) ) から移行する場合は、この違いに注意してください。

### データベース {#database}

TiDB のデータベースは、テーブルやインデックスなどのオブジェクトのコレクションです。

TiDB には`test`という名前のデフォルト データベースが付属しています。ただし、 `test`データベースを使用する代わりに、独自のデータベースを作成することをお勧めします。

### テーブル {#table}

テーブルは、関連するデータを[データベース](#database)に集めたものです。

各テーブルは**行**と<strong>列</strong>で構成されます。行の各値は特定の<strong>列</strong>に属します。各列には 1 つのデータ型のみが許可されます。列をさらに修飾するには、いくつかの[制約](/constraints.md)を追加できます。計算を高速化するために、 [生成された列 (実験的機能)](/generated-columns.md)を追加できます。

### 索引 {#index}

インデックスは、テーブル内の選択された列のコピーです。 [テーブル](#table)の 1 つ以上の列を使用してインデックスを作成できます。インデックスを使用すると、TiDB はテーブル内のすべての行を毎回検索することなくデータをすばやく見つけることができるため、クエリのパフォーマンスが大幅に向上します。

インデックスには、次の 2 つの一般的なタイプがあります。

-   **Primary Key** : 主キー列のインデックス。
-   **セカンダリ インデックス**: 非主キー列のインデックス。

> **ノート：**
>
> TiDB では、 **Primary Key**のデフォルト定義が[InnoDB](https://mariadb.com/kb/en/innodb/) (MySQL の一般的なstorageエンジン) とは異なります。
>
> -   InnoDB では、 **Primary Key**の定義は一意であり、null ではなく、<strong>クラスター化されたインデックスです</strong>。
> -   TiDB では、 **Primary Key**の定義は一意であり、null ではありません。ただし、主キーが<strong>クラスター化インデックス</strong>であるとは限りません。主キーがクラスター化インデックスかどうかを指定するには、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に予約されていないキーワード`CLUSTERED`または`NONCLUSTERED`を追加します。ステートメントでこれらのキーワードが明示的に指定されていない場合、デフォルトの動作はシステム変数`@@global.tidb_enable_clustered_index`によって制御されます。詳細については、 [クラスタ化インデックス](/clustered-indexes.md)参照してください。

#### 特殊なインデックス {#specialized-indexes}

<CustomContent platform="tidb">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB はいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、 [索引付けと制約](/basic-features.md#indexing-and-constraints)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB はいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、 [索引付けと制約](https://docs.pingcap.com/tidb/stable/basic-features#indexing-and-constraints)を参照してください。

</CustomContent>

### サポートされているその他の論理オブジェクト {#other-supported-logical-objects}

TiDB は、 **table**と同じレベルで次の論理オブジェクトをサポートします。

-   [ビュー](/views.md) : ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。
-   [シーケンス](/sql-statements/sql-statement-create-sequence.md) : シーケンスはシーケンシャル データを生成して格納します。
-   [一時テーブル](/temporary-tables.md) : データが永続的でないテーブル。

## アクセス制御 {#access-control}

<CustomContent platform="tidb">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートしています。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](/privilege-management.md)から[ユーザー](/user-account-management.md)直接付与するか、 [権限](/privilege-management.md)から[役割](/role-based-access-control.md)までをユーザーに付与します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートしています。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](https://docs.pingcap.com/tidb/stable/privilege-management)から[ユーザー](https://docs.pingcap.com/tidb/stable/user-account-management)直接付与するか、 [権限](https://docs.pingcap.com/tidb/stable/privilege-management)から[役割](https://docs.pingcap.com/tidb/stable/role-based-access-control)までをユーザーに付与します。

</CustomContent>

## データベース スキーマの変更 {#database-schema-changes}

ベスト プラクティスとして、ドライバまたは ORM の代わりに[MySQL クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または GUI クライアントを使用してデータベース スキーマの変更を実行することをお勧めします。

## オブジェクトの制限 {#object-limitations}

詳細については、 [TiDB の制限事項](/tidb-limitations.md)を参照してください。

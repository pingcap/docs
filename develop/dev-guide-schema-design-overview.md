---
title: TiDB Database Schema Design Overview
summary: TiDB データベース スキーマ設計の基礎を学びます。
---

# TiDB データベース スキーマ設計の概要 {#tidb-database-schema-design-overview}

このドキュメントでは、TiDB 内のオブジェクト、アクセス制御、データベース スキーマの変更、オブジェクトの制限など、TiDB データベース スキーマ設計の基本について説明します。

以降のドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)例に、データベースを設計し、データベース内でデータの読み取りおよび書き込み操作を実行する方法を説明します。

## TiDB 内のオブジェクト {#objects-in-tidb}

いくつかの一般的な用語を区別するために、TiDB で使用される用語に関する簡単な合意を次に示します。

-   一般的な用語[データベース](https://en.wikipedia.org/wiki/Database)との混同を避けるため、このドキュメントでは、**データベース**は論理オブジェクトを指し、 **TiDB は**TiDB 自体を指し、**クラスターは**TiDB のデプロイされたインスタンスを指します。

-   TiDB は MySQL 互換の構文を使用します。この構文では、**スキーマは**データベース内の論理オブジェクトではなく、一般的な用語[スキーマ](https://en.wiktionary.org/wiki/schema)を意味します。詳細については、 [MySQL ドキュメント](https://dev.mysql.com/doc/refman/8.0/en/create-database.html) [マイクロソフトSQLサーバー](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15)してください。論理オブジェクトとしてスキーマを持つデータベース (たとえば、 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html) ) から移行する場合は[オラクル](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)この違いに注意してください。

### データベース {#database}

TiDB のデータベースは、テーブルやインデックスなどのオブジェクトのコレクションです。

TiDB には`test`という名前のデフォルトのデータベースが付属しています。ただし、 `test`データベースを使用するのではなく、独自のデータベースを作成することをお勧めします。

### テーブル {#table}

テーブルは、 [データベース](#database)内の関連するデータの集合です。

各テーブルは**行**と**列**で構成されています。行の各値は特定の**列**に属します。各列では 1 つのデータ型のみが許可されます。列をさらに限定するには、 [制約](/constraints.md)追加できます。計算を高速化するには、 [生成された列](/generated-columns.md)追加できます。

### 索引 {#index}

インデックスは、テーブル内の選択された列のコピーです。 [テーブル](#table)の 1 つ以上の列を使用してインデックスを作成できます。 インデックスを使用すると、TiDB はテーブル内のすべての行を毎回検索しなくてもデータをすばやく見つけることができるため、クエリのパフォーマンスが大幅に向上します。

一般的なインデックスには次の 2 つの種類があります。

-   **主キー**: 主キー列のインデックス。
-   **セカンダリ インデックス**: 主キー以外の列のインデックス。

> **注記：**
>
> TiDB では、**主キー**のデフォルト定義が[インノDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) (MySQL の共通storageエンジン) とは異なります。
>
> -   InnoDB では、**主キー**の定義は一意であり、null ではなく、**クラスター化されたインデックス**です。
> -   TiDB では、**主キー**の定義は一意であり、null ではありません。ただし、主キーがクラスター**化インデックス**であるとは限りません。主キーがクラスター化インデックスであるかどうかを指定するには、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に非予約キーワード`CLUSTERED`または`NONCLUSTERED`追加できます。ステートメントでこれらのキーワードを明示的に指定しない場合、デフォルトの動作はシステム変数`@@global.tidb_enable_clustered_index`によって制御されます。詳細については、 [クラスター化インデックス](/clustered-indexes.md)参照してください。

#### 専門インデックス {#specialized-indexes}

<CustomContent platform="tidb">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB ではいくつかの特殊なタイプのインデックスを提供しています。各タイプの詳細については、 [インデックスと制約](/basic-features.md#indexing-and-constraints)参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB ではいくつかの特殊なタイプのインデックスを提供しています。各タイプの詳細については、 [インデックスと制約](https://docs.pingcap.com/tidb/stable/basic-features#indexing-and-constraints)参照してください。

</CustomContent>

### サポートされているその他の論理オブジェクト {#other-supported-logical-objects}

TiDB は、**テーブル**と同じレベルで次の論理オブジェクトをサポートします。

-   [ビュー](/views.md) : ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`のステートメントによって定義されます。
-   [シーケンス](/sql-statements/sql-statement-create-sequence.md) : シーケンスは連続したデータを生成して保存します。
-   [一時テーブル](/temporary-tables.md) : データが永続化されないテーブル。

## アクセス制御 {#access-control}

<CustomContent platform="tidb">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートしています。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](/privilege-management.md)から[ユーザー](/user-account-management.md)直接付与するか、ユーザーに[権限](/privilege-management.md)から[役割](/role-based-access-control.md)を付与します。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートしています。ユーザーがデータ オブジェクトとデータ スキーマを表示、変更、または削除できるようにするには、 [権限](https://docs.pingcap.com/tidb/stable/privilege-management)から[ユーザー](https://docs.pingcap.com/tidb/stable/user-account-management)直接付与するか、ユーザーに[権限](https://docs.pingcap.com/tidb/stable/privilege-management)から[役割](https://docs.pingcap.com/tidb/stable/role-based-access-control)を付与します。

</CustomContent>

## データベーススキーマの変更 {#database-schema-changes}

ベスト プラクティスとして、データベース スキーマの変更を実行するには、ドライバーまたは ORM ではなく、 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)または GUI クライアントを使用することをお勧めします。

## オブジェクトの制限 {#object-limitations}

詳細については[TiDB の制限](/tidb-limitations.md)参照してください。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](/support.md)についてコミュニティに質問してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

[不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)または[スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs) 、または[サポートチケットを送信する](https://tidb.support.pingcap.com/)についてコミュニティに質問してください。

</CustomContent>

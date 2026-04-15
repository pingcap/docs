---
title: TiDB Database Schema Design Overview
summary: TiDBデータベースのスキーマ設計の基本を学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-schema-design-overview/','/ja/tidb/dev/dev-guide-schema-design-overview/','/ja/tidbcloud/dev-guide-schema-design-overview/']
---

# TiDBデータベーススキーマ設計の概要 {#tidb-database-schema-design-overview}

このドキュメントでは、TiDBのオブジェクト、アクセス制御、データベーススキーマの変更、オブジェクトの制限など、TiDBデータベーススキーマ設計の基本について説明します。

以降の[書店](/develop/dev-guide-bookshop-schema-design.md)では、を例として、データベースの設計方法、およびデータベース内でのデータ読み書き操作の実行方法を示します。

## TiDB内のオブジェクト {#objects-in-tidb}

一般的な用語を区別するために、TiDBで使用される用語に関する簡単な合意事項を以下に示します。

-   一般的な用語との混同を避けるため 本ドキュメントでは、**データベース**とは論理オブジェクトを指し、 **TiDBと**[データベース](https://en.wikipedia.org/wiki/Database)TiDB自体を指し、**クラスターとは**実行中のTiDBデプロイメントを指します。

-   TiDB は MySQL 互換の構文を使用します。この**構文**では、スキーマはデータベース内の論理オブジェクトの代わりに一般用語[スキーマ](https://en.wiktionary.org/wiki/schema)を意味します。詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)を参照してください。スキーマを論理オブジェクトとして持つデータベース (たとえば、 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html) 、 [オラクル](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html)、 [Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) ) から移行する場合は、この違いに必ず注意してください。

### データベース {#database}

TiDBにおけるデータベースとは、テーブルやインデックスなどのオブジェクトの集合体です。

TiDBには`test`という名前のデフォルトデータベースが付属しています。ただし、 `test`データベースを使用する代わりに、独自のデータベースを作成することをお勧めします。

### テーブル {#table}

テーブルは、[データベース](#database)内の関連データのコレクションです。

各テーブルは**行**と**列**で構成されます。行の各値は特定の**列**に属します。各列は単一のデータ型のみを許可します。列をさらに絞り込むには、いくつかの を追加できます。計算を高速化するには、[制約](/constraints.md)[生成された列](/generated-columns.md)追加できます。

### 索引 {#index}

インデックスとは、テーブル内の選択された列のコピーです。[テーブル](#table)の1つまたは複数の列を使用してインデックスを作成できます。インデックスを使用すると、TiDBはテーブル内のすべての行を毎回検索することなくデータを迅速に検索できるため、クエリのパフォーマンスが大幅に向上します。

インデックスには大きく分けて2種類あります。

-   **主キー**：主キー列に対するインデックス。
-   **セカンダリインデックス**：主キー以外の列に設定されるインデックス。

> **注記：**
>
> TiDBでは、**プライマリキー**のデフォルト定義は[InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) （MySQLの一般的なstorageエンジン）とは異なります。
>
> -   InnoDBでは、**プライマリキー**の定義は一意であり、nullではなく、**クラスタ化されたインデックス**です。
> -   TiDB では、**プライマリ キー**の定義は一意であり、NULL ではありません。ただし、プライマリ キーが**クラスタ化インデックス**であるとは限りません。プライマリ キーがクラスタ化インデックスであるかどうかを指定するには、 `CLUSTERED`ステートメントの`NONCLUSTERED`の後に、予約されていないキーワード`PRIMARY KEY`または`CREATE TABLE`追加します。ステートメントでこれらのキーワードが明示的に指定されていない場合、デフォルトの動作はシステム変数`@@global.tidb_enable_clustered_index`によって制御されます。詳細については、[クラスター化インデックス](/clustered-indexes.md)参照してください。

#### 専門索引 {#specialized-indexes}

さまざまなユーザー シナリオのクエリ パフォーマンスを向上させるために、TiDB はいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、[インデックスと制約](/basic-features.md#indexing-and-constraints)参照してください。

### その他のサポートされている論理オブジェクト {#other-supported-logical-objects}

TiDBは、**テーブル**と同じレベルで以下の論理オブジェクトをサポートしています。

-   [ビュー](/views.md): ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。
-   [シーケンス](/sql-statements/sql-statement-create-sequence.md): シーケンスはシーケンシャルデータを生成し、保存します。
-   [一時テーブル](/temporary-tables.md): データが永続的ではないテーブル。

## アクセス制御 {#access-control}

TiDB は、ユーザーベースとロールベースの両方のアクセス制御をサポートします。ユーザーがデータ オブジェクトおよびデータ スキーマを表示、変更、または削除できるようにするには、[ユーザー](/user-account-management.md)に直接[権限](/privilege-management.md)付与するか、[役割](/role-based-access-control.md)を通じて[権限](/privilege-management.md)ユーザーに付与します。

## データベーススキーマの変更 {#database-schema-changes}

ベストプラクティスとして、データベーススキーマの変更を実行する際には、ドライバやORMではなく、 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)またはGUIクライアントを使用することをお勧めします。

## 対象物の制限 {#object-limitations}

詳細については、 [TiDBの制限事項](/tidb-limitations.md)を参照してください。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)

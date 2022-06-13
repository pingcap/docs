---
title: TiDB Database Schema Design Overview
summary: Learn the basics on TiDB database schema design.
---

# TiDBデータベーススキーマ設計の概要 {#tidb-database-schema-design-overview}

このドキュメントでは、TiDB内のオブジェクト、アクセス制御、データベーススキーマの変更、オブジェクトの制限など、TiDBデータベーススキーマの設計の基本について説明します。

以降のドキュメントでは、 [書店](/develop/dev-guide-bookshop-schema-design.md)を例として取り上げ、データベースを設計し、データベースでデータの読み取りおよび書き込み操作を実行する方法を示します。

## TiDBのオブジェクト {#objects-in-tidb}

いくつかの一般的な用語を区別するために、TiDBで使用される用語に関する簡単な合意を次に示します。

-   一般的な用語[データベース](https://en.wikipedia.org/wiki/Database)との混同を避けるために、このドキュメントの**データベース**は論理オブジェクトを指し、 <strong>TiDB</strong>はTiDB自体を指し、<strong>クラスタ</strong>はTiDBのデプロイされたインスタンスを指します。

-   TiDBは、MySQL互換の構文を使用します。この構文では、**スキーマ**は、データベース内の論理オブジェクトではなく、一般的な用語[スキーマ](https://en.wiktionary.org/wiki/schema)を意味します。詳細については、 [MySQLドキュメント](https://dev.mysql.com/doc/refman/8.0/en/create-database.html)を参照してください。スキーマを論理オブジェクトとして持つデータベース（たとえば、 [PostgreSQL](https://www.postgresql.org/docs/current/ddl-schemas.html) 、および[オラクル](https://docs.oracle.com/en/database/oracle/oracle-database/21/tdddg/creating-managing-schema-objects.html) ）から移行する場合は、この違いに注意して[Microsoft SQL Server](https://docs.microsoft.com/en-us/sql/relational-databases/security/authentication-access/create-a-database-schema?view=sql-server-ver15) 。

### データベース {#database}

TiDBのデータベースは、テーブルやインデックスなどのオブジェクトのコレクションです。

TiDBには、 `test`という名前のデフォルトデータベースが付属しています。ただし、 `test`データベースを使用するのではなく、独自のデータベースを作成することをお勧めします。

### テーブル {#table}

テーブルは、 [データベース](#database)の関連データのコレクションです。

各テーブルは**行**と<strong>列</strong>で構成されています。行の各値は特定の<strong>列</strong>に属します。各列は単一のデータ型のみを許可します。列をさらに限定するために、 [制約](/constraints.md)を追加できます。計算を高速化するために、 [生成された列（実験的機能）](/generated-columns.md)を追加できます。

### 索引 {#index}

インデックスは、テーブル内の選択された列のコピーです。 1の[テーブル](#table)つ以上の列を使用してインデックスを作成できます。インデックスを使用すると、TiDBはテーブル内のすべての行を毎回検索しなくてもデータをすばやく見つけることができるため、クエリのパフォーマンスが大幅に向上します。

インデックスには2つの一般的なタイプがあります。

-   **主キー**：主キー列のインデックス。
-   **セカンダリインデックス**：非プライマリキー列のインデックス。

> **ノート：**
>
> TiDBでは、**主キー**のデフォルト定義は[InnoDB](https://mariadb.com/kb/en/innodb/) （MySQLの一般的なストレージエンジン）の定義とは異なります。
>
> -   InnoDBでは、**主キー**の定義は一意であり、nullではなく、<strong>クラスター化インデックス</strong>です。
> -   TiDBでは、**主キー**の定義は一意であり、nullではありません。ただし、主キーが<strong>クラスター化インデックス</strong>であるとは限りません。主キーがクラスター化インデックスであるかどうかを指定するには、 `CREATE TABLE`ステートメントの`PRIMARY KEY`の後に予約されていないキーワード`CLUSTERED`または`NONCLUSTERED`を追加できます。ステートメントでこれらのキーワードが明示的に指定されていない場合、デフォルトの動作はシステム変数`@@global.tidb_enable_clustered_index`によって制御されます。詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。

#### 特殊なインデックス {#specialized-indexes}

さまざまなユーザーシナリオのクエリパフォーマンスを向上させるために、TiDBはいくつかの特殊なタイプのインデックスを提供します。各タイプの詳細については、次のリンクを参照してください。

-   [式インデックス](/sql-statements/sql-statement-create-index.md#expression-index) （実験的）
-   [列型ストレージ（TiFlash）](/tiflash/tiflash-overview.md)
-   [RocksDBエンジン](/storage-engine/rocksdb-overview.md)
-   [Titanプラグイン](/storage-engine/titan-overview.md)
-   [見えないインデックス](/sql-statements/sql-statement-add-index.md)
-   [複合`PRIMARY KEY`](/constraints.md#primary-key)
-   [一意のインデックス](/constraints.md#unique-key)
-   [整数の`PRIMARY KEY`のクラスター化インデックス](/constraints.md)
-   [複合キーまたは非整数キーのクラスター化インデックス](/constraints.md)

### その他のサポートされている論理オブジェクト {#other-supported-logical-objects}

TiDBは、**テーブル**と同じレベルで次の論理オブジェクトをサポートします。

-   [意見](/views.md) ：ビューは仮想テーブルとして機能し、そのスキーマはビューを作成する`SELECT`ステートメントによって定義されます。
-   [順序](/sql-statements/sql-statement-create-sequence.md) ：シーケンスはシーケンシャルデータを生成して保存します。
-   [一時的なテーブル](/temporary-tables.md) ：データが永続的でないテーブル。

## アクセス制御 {#access-control}

TiDBは、ユーザーベースとロールベースの両方のアクセス制御をサポートします。ユーザーがデータオブジェクトとデータスキーマを表示、変更、または削除できるようにするには、 [特権](/privilege-management.md)から[ユーザー](/user-account-management.md)を直接付与するか、 [特権](/privilege-management.md)から[役割](/role-based-access-control.md)をユーザーに付与します。

## データベーススキーマの変更 {#database-schema-changes}

ベストプラクティスとして、データベーススキーマの変更を実行するには、ドライバーまたはORMの代わりに[MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)またはGUIクライアントを使用することをお勧めします。

## オブジェクトの制限 {#object-limitations}

このセクションでは、識別子の長さ、単一のテーブル、および文字列型に関するオブジェクトの制限を示します。詳細については、 [TiDBの制限](/tidb-limitations.md)を参照してください。

### 識別子の長さの制限 {#limitations-on-identifier-length}

| 識別子の種類 | 最大長（許可される文字数） |
| :----- | :------------ |
| データベース | 64            |
| テーブル   | 64            |
| 桁      | 64            |
| 索引     | 64            |
| 意見     | 64            |
| 順序     | 64            |

### 単一のテーブルの制限 {#limitations-on-a-single-table}

| タイプ      | 上限（デフォルト値）                                                                                                                |
| :------- | :------------------------------------------------------------------------------------------------------------------------ |
| 列        | デフォルトは1017で、最大4096まで調整できます。                                                                                               |
| インデックス   | デフォルトは64で、最大512まで調整できます                                                                                                   |
| パーティション  | 8192                                                                                                                      |
| 単一の行サイズ  | デフォルトでは6MB。サイズ制限は、 [**txn-entry-size-limit**](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50)の構成アイテムで調整できます。 |
| 行サイズの単一列 | 6 MB                                                                                                                      |

### 文字列タイプの制限 {#limitations-on-string-types}

| タイプ       | 上限      |
| :-------- | :------ |
| CHAR      | 256文字   |
| バイナリ      | 256文字   |
| VARBINARY | 65535文字 |
| VARCHAR   | 16383文字 |
| 文章        | 6 MB    |
| BLOB      | 6 MB    |

### 行の数 {#number-of-rows}

TiDBは、クラスタにノードを追加することにより、**無制限**の数の行をサポートします。関連する原則については、 [TiDBのベストプラクティス](/best-practices/tidb-best-practices.md)を参照してください。
